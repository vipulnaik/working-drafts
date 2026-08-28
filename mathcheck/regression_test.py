#!/usr/bin/env python3
"""
regression_test.py

Guards against both directions of failure:
  FALSE NEGATIVES - inject known errors into clean pages, assert the
                    checker catches them.
  FALSE POSITIVES - run the clean pages, assert the issue count stays
                    at or below a recorded baseline.

Run: python3 regression_test.py
"""

import sys
from pathlib import Path
import latex_semantic_scan as sem

CLEAN_PAGES = {
    "sample-page (subnormal examples)": "sample-page.mediawiki",
    "sample-page-2 (Wedderburn, tabular)": "sample-page-2.mediawiki",
}

# Recorded post-fix baselines. If a change pushes these UP, that's new noise.
BASELINES = {
    "sample-page (subnormal examples)": 6,
    "sample-page-2 (Wedderburn, tabular)": 2,
}


def run(text, approved=None):
    """Run both layers. `approved` defaults to the page's own extracted
    table, mirroring the real workflow (extract -> human review -> check).
    Passing an empty table instead would make every declaration DRIFT,
    which measures nothing useful."""
    decls = sem.extract_declarations(text, sem.DEFAULT_PATTERNS)
    decls = sem.dedupe_declarations(decls)
    if approved is None:
        approved = sem.build_draft_table(decls)
    issues = [
        ("MALFORMED_MATH_TAG", m) for _, m in sem.find_malformed_math_tags(text)
    ]
    issues += sem.check_consistency(decls, approved)
    return decls, issues


def severities(issues):
    return [s for s, _ in issues]


# --------------------------------------------------------------------------
# Injected-error cases: (name, base_file, mutation_fn, expected_severity)
# --------------------------------------------------------------------------

def inject_redefinition(text):
    """Re-bind an already-bound symbol to something incompatible, in the
    SAME scope, using an explicit binding marker so it must be caught."""
    return text.replace(
        "'''To prove''': <math>K</math> is a field.",
        "'''To prove''': <math>K</math> is a field. Let <math>K</math> be a "
        "cyclic group of prime order.",
    )


def inject_self_reference(text):
    return text.replace(
        "'''Given''': A division ring <math>K</math> of finite size.",
        "'''Given''': A division ring <math>K</math> of finite size. "
        "Let <math>K</math> be a subring of <math>K</math>.",
    )


def inject_undeclared_referent(text):
    return text.replace(
        "'''To prove''': <math>K</math> is a field.",
        "'''To prove''': <math>K</math> is a field. "
        "Let <math>T</math> be a subgroup of <math>Z</math>.",
    )


def inject_malformed_tag(text):
    return text.replace(
        "<math>L</math> be the center", "<MATH>L</math> be the center", 1
    )


def inject_redefinition_p1(text):
    return text.replace(
        "Let <math>p</math> be a prime.",
        "Let <math>p</math> be a prime. Let <math>p</math> be a "
        "wreath product of two groups.",
        1,
    )


CASES = [
    ("redefinition (sample-page-2)", "sample-page-2.mediawiki", inject_redefinition, "REDEFINITION"),
    ("self-reference (sample-page-2)", "sample-page-2.mediawiki", inject_self_reference, "SELF_REFERENCE"),
    ("undeclared referent (sample-page-2)", "sample-page-2.mediawiki", inject_undeclared_referent, "UNDECLARED_REFERENT"),
    ("malformed math tag (sample-page-2)", "sample-page-2.mediawiki", inject_malformed_tag, "MALFORMED_MATH_TAG"),
    ("redefinition (sample-page)", "sample-page.mediawiki", inject_redefinition_p1, "REDEFINITION"),
]


def main():
    failures = []

    missing = [p for p in set(list(CLEAN_PAGES.values()) + [c[1] for c in CASES])
               if not Path(p).exists()]
    if missing:
        print("Missing sample page(s) in the current directory:")
        for p in sorted(missing):
            print("  -", p)
        print("\nRun this from the directory containing the sample .mediawiki "
              "files, or edit CLEAN_PAGES/CASES to point at your copies.")
        return 2

    print("=" * 70)
    print("FALSE-POSITIVE CHECK (clean pages should stay at/below baseline)")
    print("=" * 70)
    for label, path in CLEAN_PAGES.items():
        text = open(path).read()
        decls, issues = run(text)
        base = BASELINES[label]
        status = "OK " if len(issues) <= base else "FAIL"
        if len(issues) > base:
            failures.append(f"{label}: {len(issues)} issues > baseline {base}")
        print(f"[{status}] {label}: {len(issues)} issues "
              f"(baseline {base}), {len(decls)} declarations")
        for s, m in issues:
            print(f"         {s}: {m[:95]}")

    print()
    print("=" * 70)
    print("FALSE-NEGATIVE CHECK (injected errors must be caught)")
    print("=" * 70)
    for name, path, mutate, expected in CASES:
        clean = open(path).read()
        dirty = mutate(clean)
        if dirty == clean:
            failures.append(f"{name}: mutation did not apply (anchor text not found)")
            print(f"[FAIL] {name}: mutation anchor not found in source")
            continue

        # Realistic scenario: an approved table already exists for the clean
        # page, then someone edits the page and introduces an error. So both
        # runs are checked against the CLEAN page's approved table.
        clean_decls = sem.dedupe_declarations(
            sem.extract_declarations(clean, sem.DEFAULT_PATTERNS)
        )
        approved = sem.build_draft_table(clean_decls)

        _, clean_issues = run(clean, approved)
        _, dirty_issues = run(dirty, approved)

        clean_n = severities(clean_issues).count(expected)
        dirty_n = severities(dirty_issues).count(expected)

        caught = dirty_n > clean_n
        status = "OK " if caught else "FAIL"
        if not caught:
            failures.append(f"{name}: expected new {expected}, got {clean_n}->{dirty_n}")
        print(f"[{status}] {name}: {expected} count {clean_n} -> {dirty_n}")

    print()
    print("=" * 70)
    if failures:
        print(f"{len(failures)} FAILURE(S):")
        for f in failures:
            print("  -", f)
        return 1
    print("All regression checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
