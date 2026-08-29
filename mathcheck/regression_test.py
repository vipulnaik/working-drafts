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

import json
import re
import subprocess
import shutil
import sys
import tempfile
from pathlib import Path
import latex_semantic_scan as sem

CLEAN_PAGES = {
    "sample-page (subnormal examples)": "sample-page.mediawiki",
    "sample-page-updated (live revision)": "sample-page-updated.mediawiki",
    "sample-page-2 (Wedderburn, tabular)": "sample-page-2.mediawiki",
    "sample-page-4 (potentially characteristic)": "sample-page-4.mediawiki",
    "sample-page-5 (powering-invariant, prose)": "sample-page-5.mediawiki",
    "sample-page-6 (normality not transitive)": "sample-page-6.mediawiki",
}

# Recorded post-fix baselines. If a change pushes these UP, that's new noise.
BASELINES = {
    "sample-page (subnormal examples)": 3,
    # Live revision fetched from Groupprops. Its 2 issues are:
    # a real </matH> typo, and an AMBIGUOUS_ATTACHMENT on "group of
    # prime order p" - both legitimate, neither noise.
    "sample-page-updated (live revision)": 2,
    "sample-page-2 (Wedderburn, tabular)": 3,
    # Kept at the revision WITH the uncited-Given defect so the lint has
    # something real to catch. Its 2 issues: the uncited Given, and a
    # benign POSSIBLE_ALIAS (H and V are both characteristic in K).
    "sample-page-4 (potentially characteristic)": 1,
    # Prose-only proof over INFINITE groups. Its 5 issues: two cosmetic
    # </matH> typos, one undeclared G, and two POSSIBLE_ALIAS pairs that
    # are deliberately parallel constructions.
    "sample-page-5 (powering-invariant, prose)": 4,
    # A large survey page: many tables, <pre> GAP blocks, heavy annotation.
    # Symbols G/K/H are used by convention and never formally declared,
    # which is normal for this page type - hence 3 UNDECLARED_REFERENT
    # (one per symbol, NOT one per use) plus a benign POSSIBLE_ALIAS.
    "sample-page-6 (normality not transitive)": 4,
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
        (sev, m) for sev, _, m in sem.find_malformed_math_tags(text)
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



def _bold(s):
    """Build the wiki bold marker without embedding it as a literal here."""
    return "'" * 3 + s + "'" * 3


TO_PROVE = _bold("To prove") + ": <math>K</math> is a field."


def inject_self_ref_via_in(text):
    return text.replace(
        TO_PROVE,
        TO_PROVE + " Let <math>K</math> be a subgroup in <math>K</math>.", 1)


def inject_self_ref_appositive(text):
    """Self-reference hidden inside the appositive construction - the
    pattern that resolves subject attribution must still spot it."""
    return text.replace(
        TO_PROVE,
        TO_PROVE + " The multiplicative group <math>K^*</math> of elements "
        "of <math>K</math> is the center of <math>K^*</math>.", 1)


def inject_rebind_via_denote(text):
    """Rebinding through the 'denote by' idiom rather than 'Let X be'."""
    return text.replace(
        "We denote by <math>K^*</math> the multiplicative group",
        "We denote by <math>K^*</math> the additive group. "
        "We denote by <math>K^*</math> the multiplicative group", 1)


def inject_empty_math_span(text):
    """<math></math> matches no span, so the scanner runs on to the NEXT
    closing tag and swallows prose as math. Silent before this check."""
    return text.replace("<math>L</math> be the center",
                        "<math></math> be the center", 1)


def inject_unclosed_math_tag(text):
    return text.replace("<math>L</math> be the center",
                        "<math>L be the center", 1)


def inject_swapped_referent(text):
    """Both symbols already exist on the page, so no NEW-SYMBOL fires;
    only the semantic layer can catch this one."""
    return text.replace(
        "<math>K</math> is a vector space over <math>L</math>",
        "<math>K</math> is a vector space over <math>K</math>", 1)


def inject_restatement_not_redefinition(text):
    """A restatement ("Equivalently, ...", "In symbols, ...") re-expresses
    an existing object. It must NOT be read as a rebinding - this shape is
    everywhere in real proofs and was a major false-positive source."""
    return text.replace(
        "In symbols, <math>H = \\langle H_1 , H_2 \\rangle</math>.",
        "Equivalently, <math>H = \\langle H_1 , H_2 \\rangle</math>.", 1)


NEW_CASES = [
    ("self-ref via 'in' (sample-page-2)", "sample-page-2.mediawiki",
     inject_self_ref_via_in, "SELF_REFERENCE"),
    ("self-ref inside appositive (sample-page-2)", "sample-page-2.mediawiki",
     inject_self_ref_appositive, "SELF_REFERENCE"),
    ("rebind via 'denote by' (sample-page-2)", "sample-page-2.mediawiki",
     inject_rebind_via_denote, "REDEFINITION"),
    ("empty math span (sample-page-2)", "sample-page-2.mediawiki",
     inject_empty_math_span, "MALFORMED_MATH_TAG"),
    ("unclosed math tag (sample-page-2)", "sample-page-2.mediawiki",
     inject_unclosed_math_tag, "MALFORMED_MATH_TAG"),
    ("swapped referent, no new symbol (sample-page-2)", "sample-page-2.mediawiki",
     inject_swapped_referent, "SELF_REFERENCE"),
]


CASES = [
    ("redefinition (sample-page-2)", "sample-page-2.mediawiki", inject_redefinition, "REDEFINITION"),
    ("self-reference (sample-page-2)", "sample-page-2.mediawiki", inject_self_reference, "SELF_REFERENCE"),
    ("undeclared referent (sample-page-2)", "sample-page-2.mediawiki", inject_undeclared_referent, "UNDECLARED_REFERENT"),
    ("malformed math tag (sample-page-2)", "sample-page-2.mediawiki", inject_malformed_tag, "MATH_TAG_CASE"),
    ("redefinition (sample-page)", "sample-page.mediawiki", inject_redefinition_p1, "REDEFINITION"),
] + NEW_CASES


# --------------------------------------------------------------------------
# diff-mode cases: exercise `mathcheck.py diff` end to end as a subprocess,
# so the CLI surface, delta logic and exit code are all covered - not just
# the library functions underneath.
#
# Each case: (name, base_file, mutation_fn, expected_tag, expect_nonzero_exit)
# expected_tag=None means "expect a clean result".
# --------------------------------------------------------------------------

def inject_stray_symbol(text):
    """The real-world error Vipul hit: a symbol swapped for one that
    appears nowhere else on the page. Invisible to the semantic layer
    (it's the object of a prose noun phrase, never a declaration subject)
    but caught by the registry diff as a brand-new symbol."""
    return text.replace(
        "The class equation of <math>K^*</math>",
        "The class equation of <math>G</math>",
        1,
    )


def inject_new_unknown_macro(text):
    return text.replace("<math>L</math> be the center",
                        "<math>\\mathbbb{L}</math> be the center", 1)


def no_change(text):
    return text + "\n"  # whitespace-only edit: must come back clean


DIFF_CASES = [
    ("diff: stray symbol", "sample-page-2.mediawiki", inject_stray_symbol,
     "NEW-SYMBOL", True),
    ("diff: new unknown macro", "sample-page-2.mediawiki", inject_new_unknown_macro,
     "NEW-UNKNOWN-MACRO", True),
    ("diff: redefinition", "sample-page-2.mediawiki", inject_redefinition,
     "REDEFINITION", True),
    ("diff: self-reference", "sample-page-2.mediawiki", inject_self_reference,
     "SELF_REFERENCE", True),
    ("diff: no-op edit is clean", "sample-page-2.mediawiki", no_change,
     None, False),
    ("diff: pre-existing issues suppressed", "sample-page-2.mediawiki", no_change,
     "MALFORMED_MATH_TAG", False),  # matH typos exist in BOTH -> must NOT report
    ("diff: stray symbol (sample-page)", "sample-page.mediawiki",
     lambda t: t.replace("<math>H_1,H_2</math>", "<math>H_1,Q_9</math>", 1),
     "NEW-SYMBOL", True),
]


def run_parse_cases():
    """Pin specific parses that were previously WRONG, so they can't
    silently regress. Each case asserts the resolved subject symbol."""
    failures = []
    cases = [
        # Appositive subject: the true subject is L^* (head noun
        # "multiplicative group"), NOT the nearer L inside the
        # intervening "of nonzero elements of L" phrase.
        ("appositive subject",
         "The multiplicative group <math>L^*</math> of nonzero elements of "
         "<math>L</math> is the center of <math>K^*</math>.",
         "L^*", "K^*", True, ["L"]),
        # Once the author adds the commas the advisory asks for, the
        # sentence must STILL parse (same subject) and the advisory must
        # go quiet - otherwise the tool nags about a sentence already
        # fixed as instructed, or worse, goes blind to it entirely.
        ("appositive with commas",
         "The multiplicative group <math>L^*</math>, of nonzero elements of "
         "<math>L</math>, is the center of <math>K^*</math>.",
         "L^*", "K^*", False, ["L"]),
        ("appositive with parentheses",
         "The multiplicative group <math>L^*</math> (of nonzero elements of "
         "<math>L</math>) is the center of <math>K^*</math>.",
         "L^*", "K^*", False, ["L"]),
        # Declaration idioms using a verb other than "is/be a", or with
        # the descriptor before the symbol. Each was a silent recall gap.
        ("denote verb",
         "Let <math>G</math> denote a finite group.", "G", None, False, []),
        ("inverted binding",
         "Let the prime be <math>p</math>.", "p", None, False, []),
        # Ordinary subject-first sentence must be unaffected by the
        # object-position guard.
        # Appositive NAMING: "G is the group GA^+(1,\R)". The trailing
        # symbol names the subject rather than being a relation target.
        # Also exercises nested parens in the placeholder, which the usual
        # [^)]+ delimiter mis-splits.
        ("appositive naming with nested parens",
         "Suppose <math>G</math> is the group <math>GA^+(1,\\R)</math>, "
         "given explicitly as linear maps.", "G", None, False, []),
        ("plain subject unaffected",
         "Let <math>H</math> be a subgroup of a finite group <math>G</math>.",
         "H", "G", False, []),
    ]
    for name, text, want_sym, want_rel, want_ambiguous, forbidden_subjects in cases:
        decls = sem.extract_declarations(text, sem.DEFAULT_PATTERNS)
        primary = [d for d in decls if d.get("rel")] if want_rel else decls
        if not primary:
            failures.append(f"{name}: no relational declaration extracted")
            print(f"[FAIL] {name}: no relational declaration extracted")
            continue
        d = primary[0]
        problems = []
        if d["sym"] != want_sym:
            problems.append(f"subject {d['sym']!r} != {want_sym!r}")
        if want_rel is not None and d["rel"] != want_rel:
            problems.append(f"referent {d['rel']!r} != {want_rel!r}")
        if bool(d.get("ambiguous_attachment")) != want_ambiguous:
            problems.append(f"ambiguous flag {bool(d.get('ambiguous_attachment'))} != {want_ambiguous}")
        # The wrong parse must not merely be outranked - it must be absent.
        # Without the object-position guard it leaks in ALONGSIDE the
        # correct one, which a "check the first result" test would miss.
        leaked = sorted({x["sym"] for x in decls} & set(forbidden_subjects))
        if leaked:
            problems.append(f"misparsed subject(s) also present: {leaked}")
        if problems:
            failures.append(f"{name}: " + "; ".join(problems))
            print(f"[FAIL] {name}: " + "; ".join(problems))
        else:
            print(f"[OK ] {name}: subject={d['sym']}, referent={d['rel']}, "
                  f"ambiguous={bool(d.get('ambiguous_attachment'))}")
    return failures



def run_given_column_cases():
    """The uncited-Given lint. Whole-table by design: downstream steps
    inherit a hypothesis through the "Previous steps used" chain, so a
    per-row version would demand redundant citations."""
    failures = []
    checks = [
        # Hard direction states a Given and never cites it across 7 rows.
        ("fires on uncited Given", "sample-page-4.mediawiki", True),
        # Wedderburn's table DOES cite its Given -> must stay silent.
        ("silent when Given is cited", "sample-page-2.mediawiki", False),
        # No Given block at all -> nothing to say.
        ("silent with no Given block", "sample-page.mediawiki", False),
    ]
    for name, path, expect in checks:
        got = bool(sem.find_uncited_givens(Path(path).read_text()))
        ok = got == expect
        print(f"[{'OK ' if ok else 'FAIL'}] uncited-given: {name}")
        if not ok:
            failures.append(f"uncited-given: {name} (expected {expect}, got {got})")

    # A Given can be a CONJUNCTION ("a division ring K of finite size").
    # Both components are load-bearing and cited at different steps, so
    # dropping one citation must NOT be masked by the other still being
    # present - the whole-table check alone cannot see this.
    wed = Path("sample-page-2.mediawiki").read_text()
    partial = [
        ("drops finiteness citation",
         wed.replace("|| <math>K</math> is finite ||", "||  ||"), "finite"),
        ("drops division-ring citation",
         wed.replace("|| <math>K</math> is a division ring ||", "||  ||"), "ring"),
    ]
    for name, txt, keyword in partial:
        msgs = [m for _, _, m in sem.find_uncited_givens(txt)]
        ok = any(repr(keyword) in m for m in msgs)
        print(f"[{'OK ' if ok else 'FAIL'}] uncited-given: {name} is caught")
        if not ok:
            failures.append(f"uncited-given: {name} not caught")

    comps = sem.given_components(
        (chr(39) * 3) + "Given" + (chr(39) * 3)
        + ": A division ring <math>K</math> of finite size.")
    ok = len(comps) == 2 and {c[2] for c in comps} == {"ring", "finite"}
    print(f"[{'OK ' if ok else 'FAIL'}] uncited-given: conjunctive Given "
          f"splits into components -> {[c[2] for c in comps]}")
    if not ok:
        failures.append("uncited-given: Given not decomposed")
    return failures


def run_verbless_cases():
    """Verbless declaration idioms. Groupprops introduces symbols with no
    verb at all in Given / To prove blocks; without these, G and K look
    undeclared on essentially every proof page."""
    failures = []
    given = (chr(39)*3) + "Given" + (chr(39)*3) + ": "  # "'''Given''': "
    cases = [
        ("Given block, two symbols",
         given + "A group <math>G</math>, a normal subgroup "
         "<math>H</math> of <math>G</math>.", {"G", "H"}),
        ("equivalent-for idiom",
         "The following are equivalent for a subgroup <math>H</math> of a "
         "group <math>G</math>:", {"G", "H"}),
        ("qualifier tail, no symbol",
         given + "A division ring <math>K</math> of finite size.", {"K"}),
        # Must NOT fire outside a declaration context - this shape is far
        # too common in ordinary proof prose to trust on its own.
        ("ordinary prose stays silent",
         "Under any automorphism of <math>K</math>, the image of "
         "<math>V</math> is a homomorphic image of <math>V</math> in "
         "<math>K</math>.", set()),
    ]
    for name, text, expected in cases:
        syms = {d["sym"] for d in sem.extract_declarations(text, sem.DEFAULT_PATTERNS)}
        ok = (expected <= syms) if expected else (not syms)
        print(f"[{'OK ' if ok else 'FAIL'}] verbless: {name} -> {sorted(syms) or 'none'}")
        if not ok:
            failures.append(f"verbless: {name} (wanted {sorted(expected)}, got {sorted(syms)})")
    return failures





def run_overlay_cases():
    """The overlay exists so refinement is CUMULATIVE. The property that
    matters is that user-owned fields survive re-extraction, including
    across a page edit that changes the stated wording."""
    import overlay as ov
    import tempfile, shutil as _sh
    failures = []
    tmp = Path(tempfile.mkdtemp(prefix="overlay-"))
    try:
        text = Path("sample-page-4.mediawiki").read_text()
        merged, _ = ov.merge({}, text)
        ok = "S" in merged and merged["S"]["required"] is None
        print(f"[{'OK ' if ok else 'FAIL'}] overlay: init leaves 'required' unset")
        if not ok:
            failures.append("overlay: init did not create S cleanly")

        # user refines
        merged["S"]["required"] = "centerless, no nontrivial image embeds in G"
        merged["S"]["order"] = 60
        merged["S"]["chosen"] = "AlternatingGroup(5)"

        # re-run against the SAME page: refinement must persist
        again, delta = ov.merge(merged, text)
        ok = (again["S"]["required"] and again["S"]["order"] == 60
              and not delta["changed"])
        print(f"[{'OK ' if ok else 'FAIL'}] overlay: refinement survives re-init")
        if not ok:
            failures.append("overlay: refinement lost on re-init")

        # re-run against an EDITED page: refinement persists AND is flagged
        edited = text.replace(
            "a simple non-abelian group that is not isomorphic to any subgroup of",
            "a centerless group with no nontrivial homomorphic image embedding in")
        after, delta2 = ov.merge(merged, edited)
        ok = (after["S"]["order"] == 60
              and "stated_previous" in after["S"]
              and "S" in delta2["changed"])
        print(f"[{'OK ' if ok else 'FAIL'}] overlay: page edit preserves "
              f"refinement and flags re-check")
        if not ok:
            failures.append("overlay: page edit mishandled")

        # consumers read it
        ok = ov.resolved_orders(merged).get("S") == 60
        ok = ok and ov.resolved_choices(merged).get("S") == "AlternatingGroup(5)"
        print(f"[{'OK ' if ok else 'FAIL'}] overlay: consumers can resolve "
              f"orders and choices")
        if not ok:
            failures.append("overlay: resolution helpers wrong")
    finally:
        _sh.rmtree(tmp, ignore_errors=True)
    return failures


def run_noise_control_cases():
    """Two failure modes this large survey page exposed, both of which made
    findings unreadable rather than wrong."""
    failures = []
    text = Path("sample-page-6.mediawiki").read_text()
    decls = sem.dedupe_declarations(
        sem.extract_declarations(text, sem.DEFAULT_PATTERNS))
    issues = sem.check_consistency(decls, {})

    # 1. A symbol used throughout but never declared is ONE finding. This
    #    page used G that way 12 times.
    per_sym = {}
    for sev, msg in issues:
        if sev == "UNDECLARED_REFERENT":
            m = re.match(r"'([^']+)'", msg)
            if m:
                per_sym[m.group(1)] = per_sym.get(m.group(1), 0) + 1
    dupes = {k: v for k, v in per_sym.items() if v > 1}
    ok = not dupes
    print(f"[{'OK ' if ok else 'FAIL'}] noise: one UNDECLARED_REFERENT per "
          f"symbol" + ("" if ok else f" -> {dupes}"))
    if not ok:
        failures.append(f"noise: duplicate undeclared reports {dupes}")

    # 2. Equations are gathered in a second pass, so without re-sorting a
    #    definition looks LATER than a property derived from it. Here
    #    "K = H x H" (line 115) precedes "K is the base ..." (line 122);
    #    inverted, it manufactures a REDEFINITION that the text lacks.
    ks = [d["meaning"] for d in decls
          if d["sym"] == "K" and "Generic" in " ".join(d["scope"])]
    ok = bool(ks) and "defined as" in ks[0]
    print(f"[{'OK ' if ok else 'FAIL'}] noise: definition precedes derived "
          f"property -> {ks[:1]}")
    if not ok:
        failures.append("noise: declaration ordering inverted")

    # 3. <pre> blocks are code, not prose.
    ok = not any("gap>" in d["sentence"] for d in decls)
    print(f"[{'OK ' if ok else 'FAIL'}] noise: <pre> GAP blocks excluded "
          f"from prose")
    if not ok:
        failures.append("noise: pre blocks leaked into declarations")
    return failures


def run_suggest_cases():
    """Absence checks are judged against an expectation rather than the
    page, so they are the noisiest kind. The properties worth pinning are
    that each suggestion fires on POSITIVE evidence and that pages which
    already carry the content stay quiet."""
    import suggest as sug
    failures = []
    got = {f: {s["id"] for s in sug.suggest(Path(f).read_text())}
           for f in ("sample-page.mediawiki", "sample-page-2.mediawiki",
                     "sample-page-4.mediawiki", "sample-page-5.mediawiki")}

    checks = [
        # Infinite page, no caveat stated -> suggest one.
        ("finiteness caveat on page 5", "sample-page-5.mediawiki",
         "finiteness-caveat", True),
        # ...but never suggest computational content for an infinite page.
        ("no GAP suggestion for infinite page", "sample-page-5.mediawiki",
         "gap-verification", False),
        ("no order suggestion for infinite page", "sample-page-5.mediawiki",
         "order-computation", False),
        # Wedderburn states sizes throughout ("K has size q^d") - the word
        # "order" never appears, so a naive check false-positives here.
        ("no order suggestion when page states sizes",
         "sample-page-2.mediawiki", "order-computation", False),
        # Page 4 has an empty Given column and is a tabular proof.
        ("given-citation on page 4", "sample-page-4.mediawiki",
         "given-citation", True),
    ]
    for name, path, sid, expect in checks:
        present = sid in got[path]
        ok = present == expect
        print(f"[{'OK ' if ok else 'FAIL'}] suggest: {name}")
        if not ok:
            failures.append(f"suggest: {name} (expected {expect})")

    # Volume guard: a list people learn to ignore is worse than no list.
    for f, ids in got.items():
        ok = len(ids) <= 3
        print(f"[{'OK ' if ok else 'FAIL'}] suggest: {f} has {len(ids)} "
              f"suggestion(s)")
        if not ok:
            failures.append(f"suggest: {f} too noisy ({len(ids)})")
    return failures


def run_infinite_domain_cases():
    """Some pages have NO finite model at all - every finite subgroup is
    powering-invariant, so a counterexample to powering-invariance must be
    infinite. For those, order arithmetic and GAP scaffolds are
    structurally inapplicable, and saying so beats emitting output that
    can never be used. The precision risk is the reverse error: calling a
    page infinite when it has perfectly good finite examples."""
    failures = []
    cases = [
        ("sample-page-5.mediawiki", True,  "reals/rationals -> infinite"),
        ("sample-page-4.mediawiki", False, "mentions 'finitary' but |K|=14400 exists"),
        ("sample-page-2.mediawiki", False, "finite division rings"),
        ("sample-page.mediawiki",   False, "finite wreath products"),
    ]
    for path, expect, why in cases:
        got = bool(sem.find_infinite_domain(Path(path).read_text()))
        ok = got == expect
        print(f"[{'OK ' if ok else 'FAIL'}] infinite-domain: {path} -> "
              f"{'infinite' if got else 'quiet'} ({why})")
        if not ok:
            failures.append(f"infinite-domain: {path} expected {expect}")
    return failures


def run_setbuilder_cases():
    """A set-builder has no order formula. The failure mode to guard is
    NOT a crash - it is the fallback minting a free symbol named after the
    whole expression and reporting it as 'determined', which disguises
    total ignorance as a result."""
    import ordercalc
    failures = []
    res, _, _ = ordercalc.analyse(Path("sample-page-5.mediawiki").read_text())
    sets = [r for r in res if "mapsto" in r["expression"]]
    ok = bool(sets) and all(not r["inferrable"] for r in sets)
    print(f"[{'OK ' if ok else 'FAIL'}] ordercalc: set-builder reported "
          f"not inferrable ({len(sets)} found)")
    if not ok:
        failures.append("ordercalc: set-builder wrongly claimed determined")
    return failures


def run_ordercalc_cases():
    """Order formulas checked against HAND-DERIVED expectations, written
    from the mathematics rather than read off the tool's output."""
    import ordercalc
    import sympy as sp
    failures = []
    G, H, S, p, H1, H2 = sp.symbols(
        "ord_G ord_H ord_S p ord_H_1 ord_H_2", positive=True)
    LOC = {str(x): x for x in (G, H, S, p, H1, H2)}
    expect = {
        ("sample-page.mediawiki", "A"): p**G * G,
        ("sample-page.mediawiki", "B"): p**H,
        ("sample-page.mediawiki", "N_A(B)"): p**G * H,
        ("sample-page.mediawiki", "C_1"): p**G * H1,
        ("sample-page-4.mediawiki", "V"): S**(G / H),
        # K is defined only in prose, never as an equation - covers the
        # prose bridge.
        ("sample-page-4.mediawiki", "K"): S**(G / H) * G,
    }
    for f in ("sample-page.mediawiki", "sample-page-4.mediawiki"):
        res, _, _ = ordercalc.analyse(Path(f).read_text())
        got = {r["symbol"]: r for r in res}
        for (ff, name), exp in expect.items():
            if ff != f:
                continue
            r = got.get(name)
            if not r:
                print(f"[FAIL] ordercalc: {name} not found in {f}")
                failures.append(f"ordercalc: {name} missing")
                continue
            ok = sp.simplify(sp.sympify(r["order"], locals=LOC) - exp) == 0
            print(f"[{'OK ' if ok else 'FAIL'}] ordercalc: {name} = {r['order']}")
            if not ok:
                failures.append(f"ordercalc: {name} got {r['order']}, want {exp}")

    # A join has no general order formula: guessing one would be worse than
    # admitting ignorance.
    res, _, _ = ordercalc.analyse(Path("sample-page.mediawiki").read_text())
    joins = [r for r in res if "langle" in r["expression"]]
    ok = bool(joins) and all(not r["inferrable"] for r in joins)
    print(f"[{'OK ' if ok else 'FAIL'}] ordercalc: join reported as not inferrable")
    if not ok:
        failures.append("ordercalc: join wrongly claimed inferrable")

    # Emitted formulas must round-trip through sympify so a caller can use them.
    bad = []
    for r in res:
        try:
            sp.sympify(r["order"], locals=LOC)
        except Exception:
            bad.append(r["symbol"])
    ok = not bad
    print(f"[{'OK ' if ok else 'FAIL'}] ordercalc: formulas re-parse"
          + ("" if ok else f" -> {bad}"))
    if not ok:
        failures.append(f"ordercalc: unparseable formulas {bad}")
    return failures


def run_gapgen_cases():
    """gapgen is a scaffolding generator, so the invariant to test is
    COMPLETENESS OF THE SKELETON, not correctness of the mathematics:
    nothing may be referenced without being either constructed or listed
    as an input, and every hole must be explicit."""
    import gapgen
    failures = []

    for path, section in [("sample-page-4.mediawiki", "hard direction"),
                          ("sample-page.mediawiki", "no unique largest")]:
        model = gapgen.build(Path(path).read_text(), section)
        supplied = ({e["gap_name"] for e in model["inputs"]}
                    | {e["gap_name"] for e in model["constructions"]})
        referenced = set()
        for e in model["checks"]:
            referenced |= set(re.findall(r"\b([A-Za-z]\w*)\b", e["gap_check"]))
        builtins = {"IsNormal", "IsSubgroup", "IsCharacteristicSubgroup"}
        dangling = referenced - supplied - builtins
        ok = not dangling
        print(f"[{'OK ' if ok else 'FAIL'}] gapgen: no dangling refs in "
              f"{path} ({section})" + ("" if ok else f" -> {sorted(dangling)}"))
        if not ok:
            failures.append(f"gapgen: dangling refs {sorted(dangling)} in {path}")

    # The page asserts S exists but never exhibits it: must surface as an
    # input hole rather than being silently invented.
    model = gapgen.build(Path("sample-page-4.mediawiki").read_text(), "hard direction")
    ok = any(e["sym"] == "S" for e in model["inputs"])
    print(f"[{'OK ' if ok else 'FAIL'}] gapgen: unexhibited S becomes an input hole")
    if not ok:
        failures.append("gapgen: S not surfaced as input")

    # A symbol characterized two ways must be marked as alternatives, not
    # emitted as two silent overwriting assignments.
    alts = [e for e in model["constructions"] if e.get("alternative")]
    ok = bool(alts)
    print(f"[{'OK ' if ok else 'FAIL'}] gapgen: multi-characterized symbol "
          f"marked as alternatives")
    if not ok:
        failures.append("gapgen: alternatives not marked")

    proc = subprocess.run(
        [sys.executable, "gapgen.py", "sample-page-4.mediawiki", "--json"],
        capture_output=True, text=True)
    try:
        parsed = json.loads(proc.stdout)
        ok = all(k in parsed for k in ("inputs", "constructions", "checks"))
    except Exception:
        ok = False
    print(f"[{'OK ' if ok else 'FAIL'}] gapgen: --json is parseable")
    if not ok:
        failures.append("gapgen: --json not parseable")
    return failures


def run_characterization_cases():
    """The characterization service is a review checklist, not an error
    check, so it is tested on WHAT IT SURFACES rather than pass/fail on
    content: the right symbols must appear, at the right priority."""
    failures = []
    text = Path("sample-page-updated.mediawiki").read_text()
    decls = sem.dedupe_declarations(
        sem.extract_declarations(text, sem.DEFAULT_PATTERNS))
    groups = sem.find_multiple_characterizations(decls)
    by_sym = {}
    for g in groups:
        by_sym.setdefault(g["sym"], []).append(g)

    checks = [
        # The real-world case: K is characterized implicitly by the chain
        # "H < K < G" and then explicitly by an "In other words" restatement.
        # The implicit one can't be parsed into a meaning, so K must be
        # surfaced via its ANTECEDENT or it is invisible to review.
        ("K surfaced with antecedent", lambda: any(
            g["priority"] == "high" and g.get("antecedents")
            for g in by_sym.get("K", []))),
        # "Equivalently, A = F_p[G] x G ..." restates A - must be high.
        ("A restatement is high priority", lambda: any(
            g["priority"] == "high" for g in by_sym.get("A", []))),
        # One long sentence mentioning H incidentally three ways must NOT be
        # promoted to high just for sharing a sentence.
        ("incidental same-sentence H stays normal", lambda: any(
            g["priority"] == "normal" for g in by_sym.get("H", []))),
    ]
    for name, fn in checks:
        ok = False
        try:
            ok = bool(fn())
        except Exception as e:
            name += f" (raised {e})"
        print(f"[{'OK ' if ok else 'FAIL'}] characterize: {name}")
        if not ok:
            failures.append(f"characterize: {name}")

    # JSON mode must be machine-parseable end to end.
    proc = subprocess.run(
        [sys.executable, "mathcheck.py", "characterize",
         "sample-page-updated.mediawiki", "--json"],
        capture_output=True, text=True)
    try:
        parsed = json.loads(proc.stdout)
        ok = isinstance(parsed, list) and all("sym" in g for g in parsed)
    except Exception:
        ok = False
    print(f"[{'OK ' if ok else 'FAIL'}] characterize: --json is parseable")
    if not ok:
        failures.append("characterize: --json not parseable")
    return failures


def run_diff_cases():
    """Run each diff case as a real subprocess against mathcheck.py."""
    failures = []
    tmp = Path(tempfile.mkdtemp(prefix="mathcheck-diff-"))

    for name, path, mutate, expected_tag, expect_fail in DIFF_CASES:
        clean_text = Path(path).read_text()
        dirty_text = mutate(clean_text)

        if expected_tag not in (None, "MALFORMED_MATH_TAG") and dirty_text == clean_text:
            failures.append(f"{name}: mutation anchor not found")
            print(f"[FAIL] {name}: mutation anchor not found")
            continue

        old_f = tmp / "old.mediawiki"
        new_f = tmp / "new.mediawiki"
        old_f.write_text(clean_text)
        new_f.write_text(dirty_text)

        # Build an approved table from the OLD revision, as a real
        # workflow would.
        clean_decls = sem.dedupe_declarations(
            sem.extract_declarations(clean_text, sem.DEFAULT_PATTERNS)
        )
        approved_f = tmp / "approved.json"
        sem.write_table(sem.build_draft_table(clean_decls), str(approved_f))

        proc = subprocess.run(
            [sys.executable, "mathcheck.py", "diff", str(old_f), str(new_f),
             "--approved", str(approved_f)],
            capture_output=True, text=True,
        )
        out = proc.stdout

        ok = True
        detail = ""

        if name == "diff: pre-existing issues suppressed":
            # The <matH> typos are in BOTH revisions, so a diff must not
            # report them - that's the whole point of delta reporting.
            if "MALFORMED_MATH_TAG" in out:
                ok, detail = False, "pre-existing MALFORMED_MATH_TAG leaked into diff output"
        elif expected_tag is None:
            if "Clean:" not in out:
                ok, detail = False, "expected a clean result"
        else:
            if expected_tag not in out:
                ok, detail = False, f"expected {expected_tag} in output"

        if expect_fail and proc.returncode == 0:
            ok, detail = False, (detail + "; " if detail else "") + "expected nonzero exit"
        if not expect_fail and proc.returncode != 0:
            ok, detail = False, (detail + "; " if detail else "") + f"expected exit 0, got {proc.returncode}"

        status = "OK " if ok else "FAIL"
        print(f"[{status}] {name}"
              + (f" -- {detail}" if detail else f" (exit {proc.returncode})"))
        if not ok:
            failures.append(f"{name}: {detail}")

    shutil.rmtree(tmp, ignore_errors=True)
    return failures


def main():
    failures = []

    required = set(CLEAN_PAGES.values())
    required |= {c[1] for c in CASES}
    required |= {c[1] for c in DIFF_CASES}
    required.add("mathcheck.py")
    required.add("gapgen.py")
    required.add("ordercalc.py")
    required.add("overlay.py")
    required.add("suggest.py")   # diff cases invoke it as a subprocess
    missing = [p for p in required if not Path(p).exists()]
    if missing:
        print("Missing required file(s) in the current directory:")
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
    print("PARSE-CORRECTNESS CHECK (subject attribution)")
    print("=" * 70)
    failures.extend(run_parse_cases())

    print()
    print("=" * 70)
    print("OVERLAY CHECK (cumulative refinement)")
    print("=" * 70)
    failures.extend(run_overlay_cases())

    print()
    print("=" * 70)
    print("ORDERCALC CHECK (vs hand-derived formulas)")
    print("=" * 70)
    failures.extend(run_ordercalc_cases())
    failures.extend(run_setbuilder_cases())
    failures.extend(run_infinite_domain_cases())
    failures.extend(run_suggest_cases())
    failures.extend(run_noise_control_cases())

    print()
    print("=" * 70)
    print("GAPGEN SCAFFOLD CHECK")
    print("=" * 70)
    failures.extend(run_gapgen_cases())

    print()
    print("=" * 70)
    print("VERBLESS-DECLARATION CHECK")
    print("=" * 70)
    failures.extend(run_verbless_cases())

    print()
    print("=" * 70)
    print("UNCITED-GIVEN LINT CHECK")
    print("=" * 70)
    failures.extend(run_given_column_cases())

    print()
    print("=" * 70)
    print("CHARACTERIZATION CHECK (review-checklist service)")
    print("=" * 70)
    failures.extend(run_characterization_cases())

    print()
    print("=" * 70)
    print("DIFF-MODE CHECK (end-to-end via mathcheck.py subprocess)")
    print("=" * 70)
    failures.extend(run_diff_cases())

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
