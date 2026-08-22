#!/usr/bin/env python3
r"""
latex_semantic_scan.py

Companion to latex_var_scan.py. Where that script finds *what symbols exist*,
this one drafts *what each symbol means*, by pattern-matching declaration
sentences ("$G$ is a group", "$H$ is a subgroup of $G$") near math spans.

Pipeline:
    1. extract   -> scan a page, produce a DRAFT symbol->meaning table (YAML)
    2. (human edits the draft - fixes misparses, fills gaps, deletes noise)
    3. check     -> re-scan the page, compare against the human-approved
                    table, flag:
                      - REDEFINITION: same symbol, conflicting role/meaning
                      - DRIFT: new declaration not yet in the approved table
                      - POSSIBLE_ALIAS (soft): different symbol, near-identical
                        meaning string (maybe intentional, maybe a slip)

Patterns are configurable (see DEFAULT_PATTERNS / --patterns-file) so this
isn't tied to group theory specifically - swap in a template file for
whatever area of math a given wiki section covers.

No LaTeX installation or external dependencies required.
"""

import re
import sys
import json
import argparse
import difflib
from pathlib import Path

try:
    import yaml
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False


# --------------------------------------------------------------------------
# 1. Declaration templates (configurable)
#
# Each pattern is applied to a *desugared* sentence where every math span
# has been replaced by a placeholder token \x01<content>\x02, so the regex
# only has to deal with the surrounding English, not LaTeX escaping.
#
# Capture groups:
#   sym   - the symbol being declared (required)
#   role  - short role label, e.g. "group", "subgroup", "homomorphism"
#   rel   - the related symbol, if any (e.g. the G in "subgroup of G")
# --------------------------------------------------------------------------

DEFAULT_PATTERNS = [
    # "G is a group" / "let G be a group"
    {
        "regex": r"(?:let\s+)?SYM\((?P<sym>[^)]+)\)\s+(?:is|be)\s+an?\s+(?P<role>[\w -]+?)(?:\.|,|$)",
        "template": "{sym} is a {role}",
    },
    # "H is a subgroup of G"
    {
        "regex": r"SYM\((?P<sym>[^)]+)\)\s+is\s+an?\s+(?P<role>[\w -]+?)\s+of\s+SYM\((?P<rel>[^)]+)\)",
        "template": "{sym} is a {role} of {rel}",
    },
    # "N is normal in G"
    {
        "regex": r"SYM\((?P<sym>[^)]+)\)\s+is\s+(?P<role>normal|central|characteristic|abelian|solvable|nilpotent)\s+in\s+SYM\((?P<rel>[^)]+)\)",
        "template": "{sym} is {role} in {rel}",
    },
    # "phi: G -> H is a homomorphism"
    {
        "regex": r"SYM\((?P<sym>[^)]+)\)\s*:\s*SYM\([^)]+\)\s*\\?to\s*SYM\([^)]+\)\s+is\s+an?\s+(?P<role>[\w -]+)",
        "template": "{sym} is a {role} (map)",
    },
    # "x in G" as a bare membership declaration (weaker signal, lower confidence)
    {
        "regex": r"SYM\((?P<sym>[^)]+)\)\s*\\in\s*SYM\((?P<rel>[^)]+)\)",
        "template": "{sym} is an element of {rel}",
        "confidence": "low",
    },
]


def load_patterns(path):
    if path is None:
        return DEFAULT_PATTERNS
    data = json.loads(Path(path).read_text())
    return data


# --------------------------------------------------------------------------
# 2. Sentence splitting + math-span placeholder substitution
# --------------------------------------------------------------------------

MATH_SPAN_RE = re.compile(
    r"(?<!\\)\$\$(.+?)(?<!\\)\$\$"
    r"|(?<!\\)\$(.+?)(?<!\\)\$"
    r"|\\\((.+?)\\\)"
    r"|<math>(.+?)</math>",
    re.DOTALL,
)

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\\$])")


def desugar(text):
    """Replace math spans with SYM(<content>) placeholders; return
    (desugared_text, list_of_original_spans_in_order)."""
    spans = []

    def repl(m):
        content = next(g for g in m.groups() if g is not None)
        spans.append(content.strip())
        return f"SYM({content.strip()})"

    return MATH_SPAN_RE.sub(repl, text), spans


def normalize_symbol(raw):
    """Strip outer whitespace and common no-op wrapping so 'G' and ' G '
    and '{G}' collapse to the same key. Deliberately shallow - reuses the
    same notion of 'atom' as latex_var_scan.py would, but kept standalone
    here to avoid a hard dependency between the two scripts."""
    s = raw.strip()
    s = re.sub(r"^\{(.*)\}$", r"\1", s)
    return s


# --------------------------------------------------------------------------
# 3. Extraction
# --------------------------------------------------------------------------

def extract_declarations(text, patterns):
    """Return list of dicts: {sym, role, rel, sentence, confidence}."""
    desugared, _ = desugar(text)
    sentences = SENTENCE_SPLIT_RE.split(desugared)

    results = []
    for sent in sentences:
        for pat in patterns:
            # Patterns are written with a literal "SYM(" for readability;
            # turn that into the escaped "SYM\(" the regex engine needs.
            working = pat["regex"].replace("SYM(", r"SYM\(")
            m = re.search(working, sent, flags=re.IGNORECASE)
            if not m:
                continue
            gd = m.groupdict()
            sym = normalize_symbol(gd.get("sym", ""))
            role = (gd.get("role") or "").strip()
            rel = normalize_symbol(gd.get("rel", "")) if gd.get("rel") else None
            meaning = pat["template"].format(sym=sym, role=role, rel=rel)
            results.append({
                "sym": sym,
                "role": role,
                "rel": rel,
                "meaning": meaning,
                "sentence": sent.strip(),
                "confidence": pat.get("confidence", "high"),
            })
            break  # first matching pattern wins per sentence
    return results


# --------------------------------------------------------------------------
# 4. Draft table generation (extract mode)
# --------------------------------------------------------------------------

def build_draft_table(declarations):
    """Group by symbol; a symbol may have multiple declarations if reused
    (that's exactly what we want the human to review)."""
    table = {}
    for d in declarations:
        table.setdefault(d["sym"], []).append({
            "meaning": d["meaning"],
            "confidence": d["confidence"],
            "source_sentence": d["sentence"],
        })
    return table


def write_table(table, path):
    if path.endswith((".yml", ".yaml")) and HAVE_YAML:
        Path(path).write_text(yaml.dump(table, sort_keys=True, allow_unicode=True))
    else:
        Path(path).write_text(json.dumps(table, indent=2, ensure_ascii=False))


def read_table(path):
    text = Path(path).read_text()
    if path.endswith((".yml", ".yaml")) and HAVE_YAML:
        return yaml.safe_load(text) or {}
    return json.loads(text)


# --------------------------------------------------------------------------
# 5. Consistency checking (check mode)
# --------------------------------------------------------------------------

def similar(a, b, threshold=0.82):
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio() >= threshold


def check_consistency(declarations, approved_table):
    """Return list of (severity, message) tuples."""
    issues = []
    seen_in_doc = {}  # sym -> list of meanings seen so far in this pass

    for d in declarations:
        sym, meaning = d["sym"], d["meaning"]
        prior = seen_in_doc.get(sym, [])

        # REDEFINITION: same symbol, meaningfully different meaning, within this doc
        for prior_meaning in prior:
            if not similar(prior_meaning, meaning):
                issues.append((
                    "REDEFINITION",
                    f"'{sym}' previously declared as \"{prior_meaning}\", "
                    f"now \"{meaning}\" -- (\"{d['sentence'][:70]}\")",
                ))

        # DRIFT: not present in the human-approved table at all
        approved = approved_table.get(sym)
        if approved is None:
            issues.append((
                "DRIFT",
                f"'{sym}' declared as \"{meaning}\" but not in approved table "
                f"-- (\"{d['sentence'][:70]}\")",
            ))
        else:
            approved_meanings = [a["meaning"] for a in approved]
            if not any(similar(meaning, am) for am in approved_meanings):
                issues.append((
                    "DRIFT",
                    f"'{sym}' now means \"{meaning}\" but approved table says "
                    f"{approved_meanings} -- (\"{d['sentence'][:70]}\")",
                ))

        seen_in_doc.setdefault(sym, []).append(meaning)

    # POSSIBLE_ALIAS (soft): different symbols, near-identical meaning text
    items = [(d["sym"], d["meaning"]) for d in declarations]
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            sym_a, mean_a = items[i]
            sym_b, mean_b = items[j]
            if sym_a != sym_b and similar(mean_a, mean_b, threshold=0.9):
                issues.append((
                    "POSSIBLE_ALIAS",
                    f"'{sym_a}' and '{sym_b}' both mean \"{mean_a}\" -- "
                    f"confirm this is intentional (e.g. two distinct subgroups)",
                ))

    return issues


# --------------------------------------------------------------------------
# 6. CLI
# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_extract = sub.add_parser("extract", help="Draft a symbol->meaning table from a page")
    p_extract.add_argument("file")
    p_extract.add_argument("--out", required=True, help="Output path for draft table (.json or .yaml)")
    p_extract.add_argument("--patterns-file", default=None)

    p_check = sub.add_parser("check", help="Check a page against a human-approved table")
    p_check.add_argument("file")
    p_check.add_argument("--approved", required=True, help="Path to human-approved table")
    p_check.add_argument("--patterns-file", default=None)

    args = ap.parse_args()
    patterns = load_patterns(args.patterns_file)
    text = Path(args.file).read_text()
    declarations = extract_declarations(text, patterns)

    if args.cmd == "extract":
        table = build_draft_table(declarations)
        write_table(table, args.out)
        print(f"Extracted {len(declarations)} declarations, {len(table)} distinct symbols.")
        print(f"Draft table written to {args.out} -- please review before using as 'approved'.")

    elif args.cmd == "check":
        approved = read_table(args.approved)
        issues = check_consistency(declarations, approved)
        if not issues:
            print("Clean: no redefinitions, drift, or possible aliases detected.")
        for severity, msg in issues:
            print(f"[{severity}] {msg}")
        print(f"\n--- summary: {len(issues)} issue(s) across {len(declarations)} declaration(s) ---")


if __name__ == "__main__":
    main()
