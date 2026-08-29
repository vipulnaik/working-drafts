#!/usr/bin/env python3
"""Exploratory: generate many subtle error variants and report which are
caught. Not a regression test - a discovery tool. Findings that pass get
promoted into regression_test.py; findings that fail get reported."""

import latex_semantic_scan as sem
import latex_var_scan as syn

P1 = open("sample-page.mediawiki").read()
P2 = open("sample-page-2.mediawiki").read()


def issues_for(text, approved=None):
    decls = sem.dedupe_declarations(
        sem.extract_declarations(text, sem.DEFAULT_PATTERNS))
    out = [(sev, m) for sev, _, m in sem.find_malformed_math_tags(text)]
    out += sem.check_consistency(decls, approved if approved is not None else {})
    return decls, out


def syms(text):
    s = set()
    for _, c in syn.extract_math_spans(text):
        for a in syn.classify(c):
            if a.kind == "VARIABLE":
                s.add(a.name)
    return s


def delta(base, mutated):
    """What does a diff-style comparison surface?"""
    new_syms = syms(mutated) - syms(base)
    b_decls, b_iss = issues_for(base)
    m_decls, m_iss = issues_for(mutated)
    approved = sem.build_draft_table(b_decls)
    _, m_iss_vs_approved = issues_for(mutated, approved)
    _, b_iss_vs_approved = issues_for(base, approved)
    base_set = {(s, m) for s, m in b_iss_vs_approved}
    new_iss = [(s, m) for s, m in m_iss_vs_approved if (s, m) not in base_set]
    return new_syms, new_iss


# (name, base, mutation, what_we_hope_catches_it)
CASES = []


def case(name, base, old, new, note=""):
    CASES.append((name, base, old, new, note))


# ---- symbol confusion: existing symbol used in wrong place ----------------
case("swap K* -> K in step 2 (both exist)", P2,
     "the multiplicative group <math>L^*</math> of nonzero elements of <math>L</math> is the center of <math>K^*</math>",
     "the multiplicative group <math>L^*</math> of nonzero elements of <math>L</math> is the center of <math>K</math>",
     "both symbols already on page; no new symbol")

case("swap L -> K in vector space claim", P2,
     "<math>K</math> is a vector space over <math>L</math>",
     "<math>K</math> is a vector space over <math>K</math>",
     "creates self-reference")

case("swap d -> r in size claim", P2,
     "<math>K</math> has size <math>q^d</math> for some positive integer <math>d</math>",
     "<math>K</math> has size <math>q^r</math> for some positive integer <math>r</math>",
     "subscript-ish swap, both exist")

# ---- subtly wrong subscript ---------------------------------------------
case("r_i -> r_j (undeclared index)", P2,
     "Each <math>r_i</math> divides <math>d</math>",
     "Each <math>r_j</math> divides <math>d</math>",
     "new symbol r_j")

case("H_1 -> H_3 in page 1", P1,
     "<math>H_1,H_2</math>", "<math>H_1,H_3</math>",
     "H_3 never declared")

# ---- redefinition variants ----------------------------------------------
case("rebind L mid-proof", P2,
     "Let <math>L</math> be the center of <math>K</math>",
     "Let <math>L</math> be the center of <math>K</math>. Let <math>L</math> be a cyclic group",
     "explicit rebinding")

case("rebind via 'denote by'", P2,
     "We denote by <math>K^*</math> the multiplicative group",
     "We denote by <math>K^*</math> the additive group. We denote by <math>K^*</math> the multiplicative group",
     "denote-by rebinding")

case("rebind p in page 1 example", P1,
     "Let <math>p</math> be a prime.",
     "Let <math>p</math> be a prime. Let <math>p</math> be a permutation.",
     "")

# ---- undeclared referent -------------------------------------------------
case("subgroup of undeclared Z", P2,
     "'''To prove''': <math>K</math> is a field.",
     "'''To prove''': <math>K</math> is a field. Let <math>T</math> be a subgroup of <math>Z</math>.",
     "")

case("normal in undeclared W", P1,
     "Let <math>p</math> be a prime.",
     "Let <math>p</math> be a prime. Let <math>V</math> be a subgroup normal in <math>W</math>.",
     "")

# ---- self reference ------------------------------------------------------
case("self-ref via 'in'", P2,
     "'''To prove''': <math>K</math> is a field.",
     "'''To prove''': <math>K</math> is a field. Let <math>K</math> be a subgroup in <math>K</math>.",
     "")

case("self-ref via appositive", P2,
     "'''To prove''': <math>K</math> is a field.",
     "'''To prove''': <math>K</math> is a field. The multiplicative group <math>K^*</math> of elements of <math>K</math> is the center of <math>K^*</math>.",
     "self-ref inside appositive pattern")

# ---- malformed markup ----------------------------------------------------
case("unclosed math tag", P2,
     "<math>L</math> be the center", "<math>L be the center", "")

case("mismatched case close", P1,
     "<math>p</math> be a prime", "<math>p</MATH> be a prime", "")

case("empty math span", P2,
     "<math>L</math> be the center", "<math></math> be the center", "")

# ---- unknown macro -------------------------------------------------------
case("typo'd macro", P2,
     "\\mathbb{F}_p", "\\mathbbb{F}_p", "only on page2? check")

case("typo'd macro p1", P1,
     "\\rtimes", "\\rtimess", "")

# ---- ambiguous attachment ------------------------------------------------
case("new ambiguous appositive", P1,
     "Let <math>p</math> be a prime.",
     "Let <math>p</math> be a prime. The additive group <math>R^+</math> of elements of <math>R</math> is the center of <math>S^+</math>.",
     "should warn + declare R^+")

# ---- things that should NOT fire (false-positive probes) -----------------
case("harmless rewording", P2,
     "This result was first proved by Wedderburn.",
     "This theorem was originally proved by Wedderburn.",
     "SHOULD BE CLEAN")

case("add a legit new step symbol w/ declaration", P2,
     "'''To prove''': <math>K</math> is a field.",
     "'''To prove''': <math>K</math> is a field. Let <math>F</math> be a finite field.",
     "new symbol BUT properly declared - expect NEW-SYMBOL only")

case("reorder clause, same meaning", P1,
     "Let <math>p</math> be a prime.",
     "Let the prime be <math>p</math>.",
     "SHOULD BE CLEAN-ish")


def main():
    print(f"{'CASE':44} {'NEWSYM':>7} {'ISSUES':>7}  DETAIL")
    print("-" * 110)
    misses = []
    for name, base, old, new, note in CASES:
        if old not in base:
            print(f"{name:44} {'--':>7} {'--':>7}  ANCHOR NOT FOUND")
            misses.append((name, "anchor not found", note))
            continue
        mutated = base.replace(old, new, 1)
        new_syms, new_iss = delta(base, mutated)
        tags = sorted({s for s, _ in new_iss})
        detail = ",".join(tags) if tags else ""
        if new_syms:
            detail = f"syms={sorted(new_syms)} " + detail
        caught = bool(new_syms or new_iss)
        flag = "" if caught else "  <-- NOT CAUGHT"
        print(f"{name:44} {len(new_syms):>7} {len(new_iss):>7}  {detail[:60]}{flag}")
        if not caught:
            misses.append((name, "no signal", note))

    print()
    if misses:
        print("NOT CAUGHT / PROBLEM CASES:")
        for n, why, note in misses:
            print(f"  - {n}: {why}" + (f" ({note})" if note else ""))


if __name__ == "__main__":
    main()
