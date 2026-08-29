#!/usr/bin/env python3
r"""
mathcheck.py

Single entry point for the two sanity-check layers:

  SYNTACTIC layer (latex_var_scan.py)
    - tokenizes math spans, classifies atoms as OPERATOR / FUNCTION /
      CONSTANT / VARIABLE / UNKNOWN, flags unrecognized macros and
      "new" variables against a registry.

  SEMANTIC layer (latex_semantic_scan.py)
    - pattern-matches declaration sentences ("$G$ is a group") near math
      spans, drafts a symbol -> meaning table for human review, and later
      checks a page against the human-approved table for redefinitions,
      drift, and possible aliasing.

Usage:

  # one-time: syntactic scan of a page, using/growing a project registry
  python3 mathcheck.py syntax page.md --registry registry.json --update-registry

  # one-time: draft the semantic table for a page (then hand-edit it)
  python3 mathcheck.py semantic-extract page.md --out page.symbols.yaml

  # ongoing: check a page against BOTH layers at once
  python3 mathcheck.py check page.md \
      --registry registry.json \
      --approved page.symbols.yaml

  # per-edit: compare two revisions, reporting ONLY what the edit introduced
  python3 mathcheck.py diff old.mediawiki new.mediawiki \
      --approved page.symbols.json

  # crawl mode: run syntax layer over every .md file in a directory
  python3 mathcheck.py syntax-batch ./wiki-export/ --registry registry.json

No LaTeX installation or external dependencies required (PyYAML optional,
only needed if you use .yaml table files instead of .json).
"""

import argparse
import json
import sys
from pathlib import Path

import latex_var_scan as syn
import latex_semantic_scan as sem
import suggest as sug
import gapcheck as gc
import arith
import tablecheck


def cmd_syntax(args):
    text = Path(args.file).read_text()
    spans = syn.extract_math_spans(text)
    known = syn.load_registry(args.registry) if args.registry else set()
    all_vars, new_vars, unknown = set(), set(), set()

    for pos, content in spans:
        line = text.count("\n", 0, pos) + 1
        for atom in syn.classify(content):
            if atom.kind == "VARIABLE":
                all_vars.add(atom.name)
                if atom.name not in known:
                    new_vars.add(atom.name)
                    print(f"{args.file}:{line}: [NEW-VAR] '{atom.name}'  ({content.strip()[:60]})")
            elif atom.kind == "UNKNOWN":
                unknown.add(atom.name)
                print(f"{args.file}:{line}: [UNKNOWN-MACRO] '\\{atom.name}'  ({content.strip()[:60]})")

    print(f"-- {args.file}: {len(spans)} math spans, {len(all_vars)} vars "
          f"({len(new_vars)} new), {len(unknown)} unknown macros")

    if args.registry and args.update_registry:
        syn.save_registry(args.registry, known | all_vars)
        print(f"registry updated: {args.registry}")
    return len(new_vars) + len(unknown)


def cmd_syntax_batch(args):
    root = Path(args.dir)
    files = sorted(root.rglob(args.glob))
    known = syn.load_registry(args.registry) if args.registry else set()
    total_new = 0
    total_unknown = 0
    all_vars_ever = set(known)

    for f in files:
        text = f.read_text()
        spans = syn.extract_math_spans(text)
        for pos, content in spans:
            line = text.count("\n", 0, pos) + 1
            for atom in syn.classify(content):
                if atom.kind == "VARIABLE":
                    if atom.name not in all_vars_ever:
                        print(f"{f}:{line}: [NEW-VAR] '{atom.name}'  ({content.strip()[:60]})")
                        total_new += 1
                    all_vars_ever.add(atom.name)
                elif atom.kind == "UNKNOWN":
                    print(f"{f}:{line}: [UNKNOWN-MACRO] '\\{atom.name}'  ({content.strip()[:60]})")
                    total_unknown += 1

    print(f"\n-- batch: {len(files)} files, {total_new} new-vs-registry vars, "
          f"{total_unknown} unknown-macro occurrences")

    if args.registry and args.update_registry:
        syn.save_registry(args.registry, all_vars_ever)
        print(f"registry updated: {args.registry}")


def cmd_semantic_extract(args):
    patterns = sem.load_patterns(args.patterns_file)
    text = Path(args.file).read_text()
    declarations = sem.extract_declarations(text, patterns)
    table = sem.build_draft_table(declarations)
    sem.write_table(table, args.out)
    print(f"Extracted {len(declarations)} declarations, {len(table)} distinct symbols.")
    print(f"Draft table written to {args.out} -- review and correct before using as --approved.")


# Severities that should FAIL a pipeline. Everything else is reported but
# advisory. MATH_TAG_CASE is cosmetic (MediaWiki matches tag case
# insensitively, so <matH> renders identically). DRIFT compares against a
# possibly-stale approved table and fires on incidental mid-sentence
# descriptions, so it is informational until the table is re-reviewed.
GATING_SEVERITIES = {
    "REDEFINITION",
    "SELF_REFERENCE",
    "MALFORMED_MATH_TAG",
    "UNBALANCED_MATH",
    "GAP_PROSE_CONFLICT",
    "PROSE_SELF_CONFLICT",
    "ARITHMETIC_ERROR",
    "TABLE_INCONSISTENCY",
}

ADVISORY_SEVERITIES = {
    "MATH_TAG_CASE",
    "DRIFT",
    "POSSIBLE_ALIAS",
    "AMBIGUOUS_ATTACHMENT",
    "UNDECLARED_REFERENT",
    "UNCITED_GIVEN",
}


def cmd_check(args):
    """Run both layers together. Returns the number of GATING issues, so
    the exit code reflects real problems rather than a raw issue count
    (which the syntactic layer's new-variable tally would otherwise
    dominate and render meaningless)."""
    cmd_syntax(argparse.Namespace(
        file=args.file, registry=args.registry, update_registry=False,
    ))

    gating = 0
    if args.approved:
        print("\n=== semantic layer ===")
        text = Path(args.file).read_text()
        patterns = sem.load_patterns(args.patterns_file)
        declarations = sem.dedupe_declarations(
            sem.extract_declarations(text, patterns))
        approved = sem.read_table(args.approved)
        issues = [
            (sev, (f"line {ln}: " if ln else "") + msg)
            for sev, ln, msg in sem.find_malformed_math_tags(text)
        ]
        issues += [
            (sev, (f"line {ln}: " if ln else "") + msg)
            for sev, ln, msg in sem.find_uncited_givens(text)
        ]
        issues += [
            (sev, (f"line {ln}: " if ln else "") + msg)
            for sev, ln, msg in sem.find_unbalanced_math(text)
        ]
        issues += [
            (sev, (f"line {ln}: " if ln else "") + msg)
            for sev, ln, msg in gc.find_gap_prose_conflicts(text)
        ]
        issues += [
            (sev, (f"line {ln}: " if ln else "") + msg)
            for sev, ln, msg in gc.find_prose_self_conflicts(text)
        ]
        issues += [
            (sev, (f"line {ln}: " if ln else "") + msg)
            for sev, ln, msg in arith.find_arithmetic_errors(text)
        ]
        issues += [
            (sev, (f"line {ln}: " if ln else "") + msg)
            for sev, ln, msg in tablecheck.find_table_inconsistencies(text)
        ]
        issues += sem.check_consistency(declarations, approved)

        if not issues:
            print("Clean: no issues detected.")
        for severity, msg in issues:
            marker = "" if severity in GATING_SEVERITIES else " (advisory)"
            print(f"[{severity}]{marker} {msg}")
            if severity in GATING_SEVERITIES:
                gating += 1
        print(f"-- semantic: {len(issues)} issue(s), {gating} gating, "
              f"across {len(declarations)} declaration(s)")

        groups = sem.find_multiple_characterizations(declarations)
        if groups:
            high = [g for g in groups if g["priority"] == "high"]
            print("\n=== characterizations to verify (not errors) ===")
            print(sem.format_characterizations(groups))
            print(f"-- {len(groups)} symbol(s) characterized multiple ways; "
                  f"{len(high)} asserted equivalent. Run "
                  f"'mathcheck.py characterize --json' for machine-readable output.")
    else:
        print("\n(no --approved table given; skipping semantic layer)")

    return gating


def _collect_syntactic(text):
    """Return (variables, unknown_macros) for a revision, as sets."""
    variables, unknown = set(), set()
    for pos, content in syn.extract_math_spans(text):
        for atom in syn.classify(content):
            if atom.kind == "VARIABLE":
                variables.add(atom.name)
            elif atom.kind == "UNKNOWN":
                unknown.add(atom.name)
    return variables, unknown


def _collect_semantic(text, approved, patterns_file=None):
    """Return the list of (severity, message) issues for a revision."""
    patterns = sem.load_patterns(patterns_file)
    declarations = sem.dedupe_declarations(sem.extract_declarations(text, patterns))
    issues = [
        (sev, (f"line {ln}: " if ln else "") + msg)
        for sev, ln, msg in sem.find_malformed_math_tags(text)
    ]
    issues += [
        (sev, (f"line {ln}: " if ln else "") + msg)
        for sev, ln, msg in sem.find_uncited_givens(text)
    ]
    issues += [
        (sev, (f"line {ln}: " if ln else "") + msg)
        for sev, ln, msg in sem.find_unbalanced_math(text)
    ]
    issues += [
        (sev, (f"line {ln}: " if ln else "") + msg)
        for sev, ln, msg in gc.find_gap_prose_conflicts(text)
    ]
    issues += [
        (sev, (f"line {ln}: " if ln else "") + msg)
        for sev, ln, msg in gc.find_prose_self_conflicts(text)
    ]
    issues += [
        (sev, (f"line {ln}: " if ln else "") + msg)
        for sev, ln, msg in arith.find_arithmetic_errors(text)
    ]
    issues += [
        (sev, (f"line {ln}: " if ln else "") + msg)
        for sev, ln, msg in tablecheck.find_table_inconsistencies(text)
    ]
    if approved is not None:
        issues += sem.check_consistency(declarations, approved)
    return issues


def cmd_diff(args):
    """Compare two revisions of one page and report only what the EDIT
    introduced.

    The registry is built from the OLD revision in memory, so there is no
    registry file to forget to update - and no way to accidentally seed it
    from the new revision, which would silently disable the check.

    Pre-existing problems are deliberately NOT reported: an edit should be
    judged on what it changed. Run 'check' on the page itself for the
    page's full current state.

    Returns the count of GATING issues introduced (see GATING_SEVERITIES);
    new symbols and advisory severities are reported but do not gate.
    """
    old_text = Path(args.old).read_text()
    new_text = Path(args.new).read_text()

    old_vars, old_unknown = _collect_syntactic(old_text)
    new_vars, new_unknown = _collect_syntactic(new_text)

    approved = sem.read_table(args.approved) if args.approved else None
    old_issues = _collect_semantic(old_text, approved, args.patterns_file)
    new_issues = _collect_semantic(new_text, approved, args.patterns_file)

    introduced_vars = sorted(new_vars - old_vars)
    removed_vars = sorted(old_vars - new_vars)
    introduced_unknown = sorted(new_unknown - old_unknown)

    old_seen = {(s, m) for s, m in old_issues}
    introduced_issues = [(s, m) for s, m in new_issues if (s, m) not in old_seen]

    print(f"=== diff: {args.old} -> {args.new} ===")

    gating = 0
    for v in introduced_vars:
        print(f"[NEW-SYMBOL] '{v}' does not appear in the previous revision")
        gating += 1
    for u in introduced_unknown:
        print(f"[NEW-UNKNOWN-MACRO] '\\{u}' introduced by this edit")
        gating += 1
    for sev, msg in introduced_issues:
        marker = "" if sev in GATING_SEVERITIES else " (advisory)"
        print(f"[{sev}]{marker} {msg}")
        if sev in GATING_SEVERITIES:
            gating += 1

    if args.show_removed:
        for v in removed_vars:
            print(f"[REMOVED-SYMBOL] '{v}' no longer appears (informational)")

    total = len(introduced_vars) + len(introduced_unknown) + len(introduced_issues)
    if total == 0:
        print("Clean: this edit introduces no new symbols, macros, or issues.")

    print(f"\n--- {total} item(s) introduced by this edit; {gating} gating "
          f"({len(introduced_vars)} new symbols, "
          f"{len(introduced_unknown)} new unknown macros, "
          f"{len(introduced_issues)} new semantic issues) ---")
    if not args.approved:
        print("(no --approved table given; semantic layer limited to "
              "math-tag checks)")
    return gating


def cmd_suggest(args):
    """List what the page could gain, as opposed to what is wrong with it.

    Kept OUT of `check` deliberately: absence checks are judged against an
    expectation rather than against the page, so they are the noisiest kind
    and would drown correctness findings if mixed in.
    """
    text = Path(args.file).read_text()
    items = sug.suggest(text, args.file)
    if args.json:
        print(json.dumps(items, indent=2, ensure_ascii=False))
        return 0
    print(sug.render(items, args.file))
    return 0


def cmd_characterize(args):
    """List symbols characterized more than one way, for review.

    Not an error report - a checklist. The intended workflow is:
    resolve everything `check` flags as a problem first, then walk this
    list confirming each set of characterizations really does pick out
    the same object. Catches the dropped-qualifier failure ("the largest
    normal subgroup of G containing H" vs "...containing H as a normal
    subgroup") that no purely structural check can see.
    """
    text = Path(args.file).read_text()
    patterns = sem.load_patterns(args.patterns_file)
    declarations = sem.dedupe_declarations(sem.extract_declarations(text, patterns))
    groups = sem.find_multiple_characterizations(declarations)

    if args.json:
        print(json.dumps(groups, indent=2, ensure_ascii=False))
        return 0

    if not groups:
        print("No symbol is characterized more than one way.")
        return 0

    high = [g for g in groups if g["priority"] == "high"]
    print(sem.format_characterizations(groups))
    print(f"\n-- {len(groups)} symbol(s) with multiple characterizations; "
          f"{len(high)} explicitly asserted equivalent (review these first) --")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("syntax", help="Syntactic scan of a single page")
    p1.add_argument("file")
    p1.add_argument("--registry", default=None)
    p1.add_argument("--update-registry", action="store_true")

    p2 = sub.add_parser("syntax-batch", help="Syntactic scan of every matching file in a directory")
    p2.add_argument("dir")
    p2.add_argument("--glob", default="*.md")
    p2.add_argument("--registry", default=None)
    p2.add_argument("--update-registry", action="store_true")

    p3 = sub.add_parser("semantic-extract", help="Draft a symbol->meaning table for a page")
    p3.add_argument("file")
    p3.add_argument("--out", required=True)
    p3.add_argument("--patterns-file", default=None)

    p4 = sub.add_parser("check", help="Run syntactic + semantic checks together")
    p4.add_argument("file")
    p4.add_argument("--registry", default=None)
    p4.add_argument("--approved", default=None, help="Human-approved semantic table (omit to skip semantic layer)")
    p4.add_argument("--patterns-file", default=None)

    p7 = sub.add_parser(
        "suggest",
        help="What this page could gain (missing caveats, examples, orders, "
             "GAP) - separate from check, and noisier by nature",
    )
    p7.add_argument("file")
    p7.add_argument("--json", action="store_true")

    p6 = sub.add_parser(
        "characterize",
        help="List symbols characterized more than one way, for human/LLM review",
    )
    p6.add_argument("file")
    p6.add_argument("--patterns-file", default=None)
    p6.add_argument("--json", action="store_true",
                    help="Machine-readable output for a calling script or LLM")

    p5 = sub.add_parser(
        "diff",
        help="Compare two revisions of a page; report only what the edit introduced",
    )
    p5.add_argument("old", help="Previous revision of the page")
    p5.add_argument("new", help="Edited revision of the page")
    p5.add_argument("--approved", default=None,
                    help="Human-approved semantic table for this page")
    p5.add_argument("--patterns-file", default=None)
    p5.add_argument("--show-removed", action="store_true",
                    help="Also list symbols that disappeared (informational)")

    args = ap.parse_args()

    if args.cmd == "syntax":
        sys.exit(0 if cmd_syntax(args) == 0 else 1)
    elif args.cmd == "syntax-batch":
        cmd_syntax_batch(args)
    elif args.cmd == "semantic-extract":
        cmd_semantic_extract(args)
    elif args.cmd == "check":
        sys.exit(1 if cmd_check(args) else 0)
    elif args.cmd == "suggest":
        sys.exit(cmd_suggest(args))
    elif args.cmd == "characterize":
        sys.exit(cmd_characterize(args))
    elif args.cmd == "diff":
        sys.exit(1 if cmd_diff(args) else 0)


if __name__ == "__main__":
    main()
