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
    # "G is a group" / "let G be a group" / "let G be the group"
    {
        "regex": r"(?:let|suppose)?\s*SYM\((?P<sym>[^)]+)\)\s+(?:is|be)\s+(?:an?|the)\s+(?P<role>[\w -]+?)(?=[.,;]|\s+(?:of|that|which|among|with|in)\b|$)",
        "template": "{sym} is a {role}",
    },
    # "H is a subgroup of G" / "let H be a subgroup of G" / "let H be the subgroup of G"
    {
        "regex": r"SYM\((?P<sym>[^)]+)\)\s+(?:is|be)\s+(?:an?|the)\s+(?P<role>[\w -]+?)\s+of\s+SYM\((?P<rel>[^)]+)\)",
        "template": "{sym} is a {role} of {rel}",
    },
    # "H is a subgroup of a finite group G" - the "of" target carries its
    # OWN descriptor inline, which simultaneously declares that target too.
    # This is a very common idiom ("...of a finite group G", "...of an
    # abelian group A") and without it, G/A look permanently undeclared
    # even when the page does introduce them, just not via a standalone
    # "Let G be..." sentence.
    {
        "regex": r"SYM\((?P<sym>[^)]+)\)\s+(?:is|be)\s+(?:an?|the)\s+(?P<role>[\w -]+?)\s+of\s+(?:an?|the)\s+(?P<rel_role>[\w -]+?)\s+SYM\((?P<rel>[^)]+)\)",
        "template": "{sym} is a {role} of {rel}",
        "also_declares_rel": True,
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

# Patterns applied directly to a single math span's raw content (not to
# surrounding prose) - for definitional equations like "B = \mathbb{F}_p[H]"
# or "A = \mathbb{F}_p[G] \rtimes G", where the whole declaration lives
# inside one math span with no English words at all.
EQUATION_PATTERNS = [
    {
        # LHS must be a "simple" symbol (letters/digits/sub/superscript,
        # no top-level '=' of its own) so we don't misfire on e.g. "x^2 = y^2".
        "regex": r"^\s*(?P<sym>[A-Za-z](?:_\{[^{}]*\}|_[A-Za-z0-9]|\^\{[^{}]*\}|\^[A-Za-z0-9])*)\s*=\s*(?P<rhs>.+)$",
        "template": "{sym} is defined as {rhs}",
        "confidence": "medium",
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


def strip_wiki_markup(text):
    """Remove MediaWiki structural markup that isn't prose, so it can't
    break mid-sentence pattern matching. Applied BEFORE math-span
    desugaring, so it must not touch <math>...</math> contents."""
    # Protect math spans first so markup-stripping regexes can't reach inside them.
    protected = []

    def stash(m):
        protected.append(m.group(0))
        return f"\x00{len(protected) - 1}\x00"

    text = MATH_SPAN_RE.sub(stash, text)

    # [[fact about::X;| ]][[X]]  or  [[uses::X]]: -> drop annotation links entirely
    text = re.sub(r"\[\[[a-zA-Z ]+::[^\]]*\]\]", "", text)
    # [[Page name|Display text]] -> Display text ; [[Page name]] -> Page name
    text = re.sub(r"\[\[([^\]|]+)\|([^\]]*)\]\]", lambda m: m.group(2) or m.group(1), text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    # '' italics / ''' bold -> strip markers, keep text
    text = re.sub(r"'{2,3}", "", text)
    # == Headers == -> drop the line entirely (not prose)
    text = re.sub(r"^\s*=+.*=+\s*$", "", text, flags=re.MULTILINE)
    # leading list markers (* # :) -> drop, keep rest of line
    text = re.sub(r"^[ \t]*[*#:]+\s*", "", text, flags=re.MULTILINE)

    # Restore math spans
    def restore(m):
        return protected[int(m.group(1))]

    text = re.sub(r"\x00(\d+)\x00", restore, text)
    return text


def desugar(text):
    """Replace math spans with SYM(<content>) placeholders; return
    (desugared_text, list_of_original_spans_in_order)."""
    spans = []

    def repl(m):
        content = next(g for g in m.groups() if g is not None)
        spans.append(content.strip())
        return f"SYM({content.strip()})"

    return MATH_SPAN_RE.sub(repl, text), spans


HEADER_RE = re.compile(r"^(=+)\s*(.*?)\s*=+\s*$")


def split_into_scopes(text):
    """Split raw page text into (scope_path, segment_text) chunks using
    MediaWiki '== Header ==' lines to build a nesting path, e.g. a
    subsection under Proof gets scope_path ('Proof', 'Example 1').

    This runs BEFORE strip_wiki_markup/desugar - it only understands
    header syntax, nothing else. Content between headers (including
    text before the first header) is one segment per scope.
    """
    segments = []
    stack = []  # list of (level, title)
    current_lines = []

    def flush():
        if any(l.strip() for l in current_lines):
            path = tuple(title for _, title in stack)
            segments.append((path, "\n".join(current_lines)))
        current_lines.clear()

    for line in text.split("\n"):
        m = HEADER_RE.match(line.strip())
        if m:
            flush()
            level = len(m.group(1))
            title = m.group(2).strip()
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
        else:
            current_lines.append(line)
    flush()
    return segments


def scopes_related(a, b):
    """True if scope path `a` and `b` are the same, or one is an ancestor
    of the other (nested), so a declaration in one is visible from the
    other. False for siblings/cousins - e.g. two independent '===Example'
    subsections under the same '==Proof==' are NOT related, since each
    is its own self-contained construction and reusing a variable name
    across them is normal, not a redefinition."""
    n = min(len(a), len(b))
    return a[:n] == b[:n]


def scope_label(scope_path):
    return " > ".join(scope_path) if scope_path else "(page top)"


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

CLAUSE_SPLIT_RE = re.compile(r"\s+and\s+(?=SYM\()")


def split_clauses(sentence):
    """Split a sentence into clauses on ' and ' when the next clause starts
    with a math-span placeholder - e.g. 'A is a group and A is a subgroup
    of B' becomes two clauses. This deliberately only splits before SYM(
    (i.e. before a new subject), so 'the join of H1 and H2' or similar
    phrases inside a single clause are left alone."""
    return CLAUSE_SPLIT_RE.split(sentence)


def extract_declarations(text, patterns, equation_patterns=None):
    """Return list of dicts: {sym, role, rel, meaning, sentence, confidence,
    scope}. `scope` is a tuple of enclosing MediaWiki header titles, e.g.
    ('Proof', 'Example 1'), or () for content before any header."""
    results = []

    for scope_path, seg_text in split_into_scopes(text):
        seg_text = strip_wiki_markup(seg_text)
        desugared, spans = desugar(seg_text)
        sentences = SENTENCE_SPLIT_RE.split(desugared)

        for sent in sentences:
          for clause in split_clauses(sent):
            sent_matches = []
            for pat in patterns:
                # Patterns are written with a literal "SYM(" for readability;
                # turn that into the escaped "SYM\(" the regex engine needs.
                working = pat["regex"].replace("SYM(", r"SYM\(")
                # finditer (not search): a single clause can still carry
                # more than one pattern match (e.g. bare is-a + is-a-of
                # both matching overlapping text) - collect all, dedup below.
                for m in re.finditer(working, clause, flags=re.IGNORECASE):
                    gd = m.groupdict()
                    sym = normalize_symbol(gd.get("sym", ""))
                    role = (gd.get("role") or "").strip()
                    rel = normalize_symbol(gd.get("rel", "")) if gd.get("rel") else None
                    meaning = pat["template"].format(sym=sym, role=role, rel=rel)
                    sent_matches.append({
                        "sym": sym,
                        "role": role,
                        "rel": rel,
                        "meaning": meaning,
                        "sentence": sent.strip(),
                        "confidence": pat.get("confidence", "high"),
                        "scope": scope_path,
                        "span": (m.start(), m.end()),
                    })
                    # Some patterns (e.g. "...of a finite group G") declare
                    # BOTH symbols in one match: the primary sym, and the
                    # relation target via its own inline descriptor. Emit a
                    # second declaration for the latter, anchored to the
                    # same span so dedup treats it as part of the same match.
                    if pat.get("also_declares_rel") and gd.get("rel_role"):
                        rel_role = gd["rel_role"].strip()
                        sent_matches.append({
                            "sym": rel,
                            "role": rel_role,
                            "rel": None,
                            "meaning": f"{rel} is a {rel_role}",
                            "sentence": sent.strip(),
                            "confidence": pat.get("confidence", "high"),
                            "scope": scope_path,
                            "span": (m.start(), m.end()),
                        })

            # Dedup within this clause: when two matches overlap and share
            # the same symbol, keep only the wider (more specific) one,
            # e.g. "is-a-of" over bare "is-a" for the same span, since the
            # narrower one is almost always a partial submatch of the same
            # underlying declaration, not a second distinct one.
            sent_matches.sort(key=lambda r: -(r["span"][1] - r["span"][0]))
            kept = []
            for r in sent_matches:
                s0, e0 = r["span"]
                overlaps_kept_wider = any(
                    r["sym"] == k["sym"] and not (e0 <= k["span"][0] or s0 >= k["span"][1])
                    for k in kept
                )
                if not overlaps_kept_wider:
                    kept.append(r)
            for r in kept:
                del r["span"]
            results.extend(kept)

        # Second pass: definitional equations living entirely inside one
        # math span, e.g. "B = \mathbb{F}_p[H]" - these have no surrounding
        # English for the sentence-level patterns to anchor on.
        for content in spans:
            for pat in (equation_patterns or EQUATION_PATTERNS):
                m = re.match(pat["regex"], content.strip())
                if not m:
                    continue
                gd = m.groupdict()
                sym = normalize_symbol(gd.get("sym", ""))
                rhs = (gd.get("rhs") or "").strip()
                meaning = pat["template"].format(sym=sym, role="", rel=None, rhs=rhs)
                results.append({
                    "sym": sym,
                    "role": "",
                    "rel": None,
                    "meaning": meaning,
                    "sentence": f"${content.strip()}$",
                    "confidence": pat.get("confidence", "medium"),
                    "scope": scope_path,
                })
                break

    return results


# --------------------------------------------------------------------------
# 4. Draft table generation (extract mode)
# --------------------------------------------------------------------------

def build_draft_table(declarations):
    """Group by symbol; a symbol may have multiple declarations if reused
    (that's exactly what we want the human to review). Each entry keeps
    its scope path so re-use across independent sections (e.g. two
    sibling ===Example=== subsections) doesn't get treated the same as
    re-use within one section."""
    table = {}
    for d in declarations:
        table.setdefault(d["sym"], []).append({
            "meaning": d["meaning"],
            "confidence": d["confidence"],
            "source_sentence": d["sentence"],
            "scope": list(d["scope"]),
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
    """Return list of (severity, message) tuples.

    Scope-aware: a symbol re-used with a different meaning is only flagged
    as REDEFINITION if the two declarations occur in *related* scopes
    (same section, or one nested inside the other). Two sibling sections
    - e.g. two independent '===Example...===' subsections under the same
    '==Proof==', each running the same construction recipe with the same
    variable names - are NOT compared against each other, since that reuse
    is normal, not a slip.
    """
    issues = []
    seen_in_doc = {}  # sym -> list of (scope, meaning) seen so far in this pass
    declared_syms = []  # list of (scope, sym) for every symbol declared so far, in order

    # Symbols declared together in the same sentence (e.g. "N is a subgroup
    # of a group M" declares N and M in one match) count as simultaneous,
    # not sequential - without this, whichever of the pair happens to be
    # processed first would wrongly see the other as "not yet declared".
    same_sentence_syms = {}
    for d in declarations:
        key = (d["scope"], d["sentence"])
        same_sentence_syms.setdefault(key, set()).add(d["sym"])

    for d in declarations:
        sym, meaning, scope = d["sym"], d["meaning"], d["scope"]

        # UNDECLARED_REFERENT: this declaration explains sym in terms of
        # another symbol ("B is a subgroup of C"), but that other symbol
        # has never itself been declared anywhere in a related scope -
        # it's only ever appeared as someone else's "of X" target, never
        # as a subject in its own right. Checked against declarations seen
        # so far (textual order) PLUS anything declared in this same
        # sentence (simultaneous declarations, see same_sentence_syms above).
        if d.get("rel") and d["rel"] != sym:
            rel_declared = any(
                s == d["rel"] and scopes_related(rscope, scope)
                for rscope, s in declared_syms
            )
            if not rel_declared:
                rel_declared = d["rel"] in same_sentence_syms.get((scope, d["sentence"]), set())
            if not rel_declared:
                issues.append((
                    "UNDECLARED_REFERENT",
                    f"'{d['rel']}' is used to describe '{sym}' (\"{meaning}\") "
                    f"[{scope_label(scope)}] but '{d['rel']}' itself is never "
                    f"declared -- (\"{d['sentence'][:70]}\")",
                ))

        # SELF_REFERENCE: symbol declared in terms of itself, e.g.
        # "A is a subgroup of A". Always worth a human look regardless
        # of scope - this is a deterministic, high-confidence catch.
        if d.get("rel") and d["rel"] == sym:
            issues.append((
                "SELF_REFERENCE",
                f"'{sym}' is declared in terms of itself: \"{meaning}\" "
                f"[{scope_label(scope)}] -- (\"{d['sentence'][:70]}\")",
            ))

        prior = seen_in_doc.get(sym, [])

        # REDEFINITION: same symbol, meaningfully different meaning,
        # but ONLY within a related scope chain (not across siblings).
        for prior_scope, prior_meaning in prior:
            if scopes_related(prior_scope, scope) and not similar(prior_meaning, meaning):
                issues.append((
                    "REDEFINITION",
                    f"'{sym}' previously declared as \"{prior_meaning}\" "
                    f"[{scope_label(prior_scope)}], now \"{meaning}\" "
                    f"[{scope_label(scope)}] -- (\"{d['sentence'][:70]}\")",
                ))

        # DRIFT: not present in the human-approved table at all, or present
        # only under an unrelated scope.
        approved = approved_table.get(sym)
        if approved is None:
            issues.append((
                "DRIFT",
                f"'{sym}' declared as \"{meaning}\" [{scope_label(scope)}] "
                f"but not in approved table -- (\"{d['sentence'][:70]}\")",
            ))
        else:
            relevant = [
                a for a in approved
                if scopes_related(tuple(a.get("scope", [])), scope)
            ]
            candidates = relevant or approved  # fall back to all if scope info missing/unrelated
            approved_meanings = [a["meaning"] for a in candidates]
            if not any(similar(meaning, am) for am in approved_meanings):
                issues.append((
                    "DRIFT",
                    f"'{sym}' now means \"{meaning}\" [{scope_label(scope)}] but "
                    f"approved table (same-scope entries) says {approved_meanings} "
                    f"-- (\"{d['sentence'][:70]}\")",
                ))

        seen_in_doc.setdefault(sym, []).append((scope, meaning))
        declared_syms.append((scope, sym))

    # POSSIBLE_ALIAS (soft): different symbols, near-identical meaning text,
    # restricted to related scopes - otherwise every page-wide reuse of
    # "is a subgroup of" phrasing floods the output with noise.
    items = [(d["sym"], d["meaning"], d["scope"]) for d in declarations]
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            sym_a, mean_a, scope_a = items[i]
            sym_b, mean_b, scope_b = items[j]
            if (sym_a != sym_b
                    and scopes_related(scope_a, scope_b)
                    and similar(mean_a, mean_b, threshold=0.9)):
                issues.append((
                    "POSSIBLE_ALIAS",
                    f"'{sym_a}' [{scope_label(scope_a)}] and '{sym_b}' "
                    f"[{scope_label(scope_b)}] both mean \"{mean_a}\" -- "
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
