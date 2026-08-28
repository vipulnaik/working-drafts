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

  # crawl mode: run syntax layer over every .md file in a directory
  python3 mathcheck.py syntax-batch ./wiki-export/ --registry registry.json

No LaTeX installation or external dependencies required (PyYAML optional,
only needed if you use .yaml table files instead of .json).
"""

import argparse
import sys
from pathlib import Path

import latex_var_scan as syn
import latex_semantic_scan as sem


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


def cmd_check(args):
    """Run both layers together: syntactic new-variable/unknown-macro check,
    plus semantic redefinition/drift/alias check against an approved table."""
    exit_code = 0

    print("=== syntactic layer ===")
    exit_code += cmd_syntax(argparse.Namespace(
        file=args.file, registry=args.registry, update_registry=False,
    ))

    if args.approved:
        print("\n=== semantic layer ===")
        patterns = sem.load_patterns(args.patterns_file)
        text = Path(args.file).read_text()
        declarations = sem.extract_declarations(text, patterns)
        approved = sem.read_table(args.approved)
        issues = [
            ("MALFORMED_MATH_TAG", (f"line {ln}: " if ln else "") + msg)
            for ln, msg in sem.find_malformed_math_tags(text)
        ]
        issues += sem.check_consistency(declarations, approved)
        if not issues:
            print("Clean: no redefinitions, drift, or possible aliases detected.")
        for severity, msg in issues:
            print(f"[{severity}] {msg}")
            if severity in ("REDEFINITION", "MALFORMED_MATH_TAG"):
                exit_code += 1
        print(f"-- semantic: {len(issues)} issue(s) across {len(declarations)} declaration(s)")
    else:
        print("\n(no --approved table given; skipping semantic layer)")

    return exit_code


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

    args = ap.parse_args()

    if args.cmd == "syntax":
        sys.exit(0 if cmd_syntax(args) == 0 else 1)
    elif args.cmd == "syntax-batch":
        cmd_syntax_batch(args)
    elif args.cmd == "semantic-extract":
        cmd_semantic_extract(args)
    elif args.cmd == "check":
        sys.exit(cmd_check(args))


if __name__ == "__main__":
    main()
