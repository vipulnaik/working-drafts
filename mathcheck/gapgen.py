#!/usr/bin/env python3
r"""
gapgen.py

Generate a runnable-shaped GAP scaffold from a constructive proof page.

WHAT THIS IS. A scaffolding generator with typed holes, NOT a synthesizer.
Turning arbitrary mathematical English into correct GAP is a semantic task
and this script does not attempt it. What it does deterministically:

  1. classify each extracted declaration as an INPUT, a CONSTRUCTION, or a
     CHECK, using the declaration table latex_semantic_scan already builds;
  2. order constructions by dependency, so the emitted code defines things
     before it uses them;
  3. map recognized construction vocabulary ("wreath product", "semidirect
     product", "centralizer of X in Y", ...) to GAP idioms via an external,
     editable table;
  4. emit an explicit TODO hole for everything it cannot resolve, with the
     source sentence attached, so a human or LLM knows exactly what is
     missing and why.

The guarantee is about COMPLETENESS OF THE SKELETON, not correctness of the
mathematics: every symbol the proof introduces appears, in dependency
order, either as real GAP or as a labelled hole, and every assertion the
proof makes about those symbols appears as a check.

WHY HOLES ARE EXPECTED, NOT A FAILURE. Constructive proofs on a wiki lean
on results stated elsewhere. The 3-subnormal page needs "a nontrivial
2-subnormal subgroup that is not normal" and never exhibits one; the
potentially-characteristic page needs "a simple non-abelian group not
isomorphic to any subgroup of G". Those are genuine inputs to the
construction, not omissions to be papered over, and the right output names
them rather than guessing.

Emitted code will generally need editing before it runs. In particular
GAP's SemidirectProduct needs an explicit action homomorphism, and any
construction over an infinite or unspecified group must be instantiated at
a concrete finite example first.

Usage:
    python3 gapgen.py page.mediawiki                 # GAP scaffold
    python3 gapgen.py page.mediawiki --json          # holes, for an LLM
    python3 gapgen.py page.mediawiki --section Proof # restrict to a section
"""

import argparse
import json
import re
import sys
from pathlib import Path

import latex_semantic_scan as sem
import overlay as ov


# --------------------------------------------------------------------------
# Construction vocabulary -> GAP.
#
# Each entry: a regex over the declaration's `meaning`, plus a GAP template.
# `{sym}` is the symbol being defined; `{a}`, `{b}` are captured operands.
# `needs` lists what the template cannot supply on its own, which becomes a
# hole comment attached to that line. Edit this table freely - it is the
# main lever for coverage and is deliberately not buried in code.
# --------------------------------------------------------------------------

CONSTRUCTIONS = [
    {
        "name": "wreath product",
        "regex": r"\bwreath product\b(?:\s+of\s+(?P<a>\S+))?",
        "gap": "{sym} := WreathProduct({base}, {top});",
        "needs": ["base group", "top group", "the action used (GAP uses the "
                  "natural/regular action; a coset action on G/H must be "
                  "supplied explicitly)"],
    },
    {
        "name": "semidirect product",
        "regex": r"\bsemidirect product\b",
        "gap": "{sym} := SemidirectProduct({top}, {action}, {base});",
        "needs": ["an action homomorphism from the acting group into "
                  "Automorphism Group(base) - GAP will not infer this"],
    },
    {
        "name": "direct power",
        "regex": r"\b(?:restricted\s+)?direct power\b",
        "gap": "{sym} := DirectProduct(List([1..{n}], i -> {base}));",
        "needs": ["the index set size {n} (finite instantiation required)"],
    },
    {
        "name": "direct product",
        "regex": r"\b(?:restricted\s+)?direct product\b",
        "gap": "{sym} := DirectProduct({parts});",
        "needs": ["the list of factors"],
    },
    {
        "name": "group algebra / F_p[G]",
        "regex": r"\\mathbb\{F\}_(?P<p>\w+)\s*\[\s*(?P<a>[^\]]+)\s*\]",
        "gap": "# {sym} = F_{p}[{a}] as an ADDITIVE group is elementary abelian\n"
               "# of rank |{a}|; as a G-module it is the regular module.\n"
               "{sym} := ElementaryAbelianGroup({p}^Size({a}));",
        "needs": ["confirm whether the additive group or the full group "
                  "algebra module structure is needed"],
    },
    {
        "name": "centralizer",
        "regex": r"\bcentralizer of\s+(?P<a>\S+)\s+in\s+(?P<b>\S+)",
        "gap": "{sym} := Centralizer({b}, {a});",
        "needs": [],
    },
    {
        "name": "normalizer",
        "regex": r"\bnormalizer of\s+(?P<a>\S+)\s+in\s+(?P<b>\S+)",
        "gap": "{sym} := Normalizer({b}, {a});",
        "needs": [],
    },
    {
        "name": "join / generated subgroup",
        "regex": r"\\langle\s*(?P<a>[^\\]+?)\s*\\rangle",
        "gap": "{sym} := Subgroup({ambient}, [{a}]);   # join of listed subgroups",
        "needs": ["the ambient group", "generators rather than subgroups if "
                  "ClosureGroup is not appropriate"],
    },
    {
        # Deliberately anchored: a bare "A/B" appears inside exponents
        # (S^{G/H}) and in incidental prose, where it is NOT the thing being
        # defined. Only fire when the quotient IS the definition.
        "name": "quotient",
        "regex": r"is (?:defined as|the quotient(?: group)? of)\s*(?P<a>\w+)\s*/\s*(?P<b>\w+)\s*$",
        "gap": "{sym} := FactorGroup({a}, {b});",
        "needs": [],
    },
]


# Declarations that name an object the proof ASSUMES exists rather than
# builds. These become inputs the caller must supply.
INPUT_MARKERS = [
    (r"\bprime\b", "a prime, e.g. 2 or 3"),
    (r"\bsimple non-?abelian\b", "a simple non-abelian group, e.g. "
                                 "AlternatingGroup(5)"),
    (r"\bfinite group\b", "a concrete finite group"),
    (r"\b\d-subnormal\b", "a subgroup with the stated subnormality; the page "
                          "asserts existence but does not exhibit one"),
    (r"\bnot isomorphic to any subgroup\b", "must be checked against the "
                                            "chosen ambient group"),
    (r"\bnontrivial\b", "must be nontrivial"),
]


# Assertions worth turning into runnable checks.
CHECKS = [
    (r"^(?P<a>\S+) is characteristic in (?P<b>\S+)$",
     "IsCharacteristicSubgroup({b}, {a})",
     "GAP builtin (ref 39.3-7); short-circuits via normality first"),
    (r"^(?P<a>\S+) is normal in (?P<b>\S+)$", "IsNormal({b}, {a})", None),
    (r"^(?P<a>\S+) is a normal subgroup of (?P<b>\S+)$",
     "IsNormal({b}, {a})", None),
    (r"^(?P<a>\S+) is a subgroup of (?P<b>\S+)$", "IsSubgroup({b}, {a})", None),
]


def gap_name(sym):
    """Turn a mathematical symbol into a legal GAP identifier."""
    s = re.sub(r"\\[a-zA-Z]+", "", sym)
    s = re.sub(r"[^\w]", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "x"


def classify(decl):
    """Return ('construction'|'input'|'check'|'skip', detail)."""
    meaning = decl["meaning"]

    for spec in CONSTRUCTIONS:
        m = re.search(spec["regex"], meaning)
        if m:
            return "construction", (spec, m)

    for pat, hint in INPUT_MARKERS:
        if re.search(pat, meaning, re.IGNORECASE):
            return "input", hint

    for pat, gap, note in CHECKS:
        m = re.match(pat, meaning)
        if m:
            return "check", (gap, note, m)

    return "skip", None


def build(text, section=None):
    decls = sem.dedupe_declarations(
        sem.extract_declarations(text, sem.DEFAULT_PATTERNS))
    if section:
        decls = [d for d in decls
                 if any(section.lower() in s.lower() for s in d["scope"])]

    inputs, constructions, checks = [], [], []
    seen_defined = set()

    for d in decls:
        kind, detail = classify(d)
        entry = {
            "sym": d["sym"],
            "gap_name": gap_name(d["sym"]),
            "meaning": d["meaning"],
            "scope": list(d["scope"]),
            "sentence": d["sentence"],
        }
        if kind == "construction":
            spec, m = detail
            entry.update({
                "construction": spec["name"],
                "gap_template": spec["gap"],
                "needs": spec["needs"],
                "captured": {k: v for k, v in m.groupdict().items() if v},
            })
            constructions.append(entry)
            seen_defined.add(d["sym"])
        elif kind == "input":
            entry["hint"] = detail
            inputs.append(entry)
            seen_defined.add(d["sym"])
        elif kind == "check":
            gap, note, m = detail
            g = m.groupdict()
            entry.update({
                "gap_check": gap.format(**{k: gap_name(v) for k, v in g.items()}),
                "note": note,
            })
            checks.append(entry)

    # Any symbol a check or construction REFERENCES but nothing defines is
    # itself an input - typically the Given ("a group G, a normal subgroup
    # H of G"), which the proof assumes rather than builds. Without this the
    # scaffold silently references undefined GAP variables.
    # The same assertion often recurs across steps/scopes; one check each.
    seen_checks = set()
    deduped = []
    for e in checks:
        if e["gap_check"] in seen_checks:
            continue
        seen_checks.add(e["gap_check"])
        deduped.append(e)
    checks = deduped

    defined = {gap_name(x) for x in seen_defined}
    referenced = set()
    for e in checks:
        referenced |= set(re.findall(r"\b([A-Za-z]\w*)\b", e["gap_check"]))
    for e in constructions:
        referenced |= {gap_name(v) for v in e["captured"].values()}
    ignore = {"IsNormal", "IsSubgroup", "IsCharacteristicSubgroup",
              "Centralizer", "Normalizer", "FactorGroup", "DirectProduct",
              "WreathProduct", "SemidirectProduct", "Subgroup", "List",
              "Size", "ElementaryAbelianGroup", "i", "fail", "true", "false"}
    missing = sorted(referenced - defined - ignore)
    for name in missing:
        if name.startswith("TODO"):
            continue
        inputs.append({
            "sym": name,
            "gap_name": name,
            "meaning": f"referenced by the proof but never constructed in it",
            "scope": [],
            "sentence": "(implicit: given data, or defined on another page)",
            "hint": "supply a concrete group/subgroup; this is Given data, "
                    "not something the proof builds",
        })

    # A symbol characterized two ways yields two constructions with the same
    # name. Emitting both as assignments would silently overwrite; mark them
    # as alternatives so the reader picks one.
    by_sym = {}
    for e in constructions:
        by_sym.setdefault(e["gap_name"], []).append(e)
    for name, group in by_sym.items():
        if len(group) > 1:
            for i, e in enumerate(group, 1):
                e["alternative"] = (i, len(group))

    return {"inputs": inputs, "constructions": constructions, "checks": checks}


def render(model, source):
    L = []
    add = L.append
    add(f"# GAP scaffold generated from {source}")
    add("#")
    add("# THIS IS A SCAFFOLD, NOT A FINISHED SCRIPT. Every TODO below is a")
    add("# place the proof relies on something it does not itself construct,")
    add("# or a place GAP needs data the prose left implicit. Fill the TODOs,")
    add("# then run. Constructions over infinite or unspecified groups must")
    add("# be instantiated at a concrete finite example first.")
    add("")

    add("# " + "=" * 68)
    add("# INPUTS - supplied by you, not built by the proof")
    add("# " + "=" * 68)
    if not model["inputs"]:
        add("# (none detected)")
    for e in model["inputs"]:
        add(f"# {e['sym']}: {e['meaning']}")
        if e.get("required"):
            add(f"#   ACTUALLY REQUIRED: {e['required']}")
            add(f"#     (weaker than the page's stated condition above; the "
                f"instance need only satisfy this)")
        if e.get("case"):
            add(f"#   case note: {e['case']}")
        if not e.get("chosen"):
            add(f"#   hint: {e['hint']}")
        add(f"#   from: {e['sentence'][:88]}")
        if e.get("chosen"):
            add(f"{e['gap_name']} := {e['chosen']};   # from overlay")
        else:
            add(f"{e['gap_name']} := fail;   # TODO supply")
        add("")

    add("# " + "=" * 68)
    add("# CONSTRUCTIONS - in dependency order as they appear in the proof")
    add("# " + "=" * 68)
    if not model["constructions"]:
        add("# (none detected)")
    for e in model["constructions"]:
        add(f"# {e['sym']}: {e['meaning']}")
        add(f"#   construction recognized: {e['construction']}")
        if e.get("alternative"):
            i, n = e["alternative"]
            add(f"#   ALTERNATIVE {i} of {n} for '{e['sym']}' - the proof "
                f"characterizes it several ways; pick ONE, the others are "
                f"restatements and would overwrite it")
        for n in e["needs"]:
            add(f"#   TODO {n}")
        tmpl = e["gap_template"]
        placeholders = set(re.findall(r"\{(\w+)\}", tmpl))
        subs = {"sym": e["gap_name"]}
        for ph in placeholders:
            if ph == "sym":
                continue
            subs[ph] = e["captured"].get(ph) or f"TODO_{ph}"
        try:
            add(tmpl.format(**subs))
        except Exception:
            add(f"# (template needs manual completion) {tmpl}")
        add("")

    add("# " + "=" * 68)
    add("# CHECKS - assertions the proof makes, as runnable tests")
    add("# " + "=" * 68)
    if not model["checks"]:
        add("# (none detected)")
    for e in model["checks"]:
        add(f"# {e['meaning']}")
        if e.get("note"):
            add(f"#   note: {e['note']}")
        add(f'Print("{e["meaning"]}: ", {e["gap_check"]}, "\\n");')
        add("")

    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--section", default=None,
                    help="Restrict to sections whose name contains this string")
    ap.add_argument("--overlay", default=None,
                    help="Persisted refinement overlay (see overlay.py). "
                         "A 'chosen' entry fills that symbol's hole; a "
                         "'required' entry is shown instead of the page's "
                         "stated condition, since it is what actually "
                         "constrains the instance.")
    ap.add_argument("--json", action="store_true",
                    help="Machine-readable model (holes and all) for an LLM")
    args = ap.parse_args()

    text = Path(args.file).read_text()
    model = build(text, args.section)

    if args.overlay:
        data = ov.load(args.overlay)
        for e in model["inputs"]:
            entry = data.get(e["sym"])
            if not entry:
                continue
            if entry.get("required"):
                e["required"] = entry["required"]
            if entry.get("chosen"):
                e["chosen"] = entry["chosen"]
            if entry.get("case"):
                e["case"] = entry["case"]

    if args.json:
        print(json.dumps(model, indent=2, ensure_ascii=False))
        return 0

    print(render(model, args.file))
    n_todo = (len(model["inputs"])
              + sum(len(e["needs"]) for e in model["constructions"]))
    print(f"\n# -- {len(model['constructions'])} construction(s), "
          f"{len(model['inputs'])} input(s), {len(model['checks'])} check(s); "
          f"{n_todo} TODO(s) to fill --")
    return 0


if __name__ == "__main__":
    sys.exit(main())
