#!/usr/bin/env python3
"""
fallback_cert.py -- certify, per n, that no fallback configuration attains B(n),
using the TRUE B(n) from a computed table.

See `fb_common.py` for the question, the soundness rule, and the shared
necessary conditions; see Part E-prime of `enumeration-proof.md` for the
theorems.  For a run that reaches far beyond the computed table by substituting
a proven LOWER bound for B(n), see `wide_cert.py`.

Reports two things per table:
  * how many values every relevant s-branch is settled at by theorem alone
    (Theorems E.1, E.3(iii), E.4), needing no search;
  * whether any candidate survives the eight necessary conditions anywhere.
An empty candidate list proves mu(n) = B(n) at each n in the table.

Usage:
    python3 fallback_cert.py mu_table_safe_v2.csv [--verbose]
"""
import argparse, csv, sys
from math import comb
import fb_common as fb

ap = argparse.ArgumentParser()
ap.add_argument("table")
ap.add_argument("--verbose", action="store_true")
a = ap.parse_args()

rows = list(csv.DictReader(open(a.table)))
NMAX = max(int(r["n"]) for r in rows)
A = fb.Arith(NMAX + 2)
caps_m, caps_r = fb.cap_mersenne(A, NMAX), fb.cap_repunit(A, NMAX)

PP = [c for c in range(2, NMAX + 1) if A.prime_power(c)]

def candidates(n, B, skip):
    out = []
    for c in PP:
        if c + 2 > n:
            break
        p, _ = A.prime_power(c)
        for r in A.prime_divisors(c - 1):
            if r == p or not A.is_prime(r):
                continue
            out += fb.pair_candidates(A, n, B, c, r, p, skip_settled=skip)
            if out and not a.verbose:
                return out
    return out

bad, fully, branch_tot, branch_ok, reasons = [], 0, 0, 0, {}
for row in rows:
    n, B = int(row["n"]), int(row["mu_bound"])
    full, sm, per = fb.theorem_report(A, n, B, caps_m, caps_r)
    fully += full
    for s, (ok, why) in per.items():
        branch_tot += 1; branch_ok += ok
        if not ok:
            reasons[why] = reasons.get(why, 0) + 1
    skip = {s for s, (ok, _) in per.items() if ok}
    w = candidates(n, B, skip)
    if w:
        bad.append((n, B, float(row["density"]), w[:4]))

N = len(rows)
print(f"{a.table}: {N} values of n checked, n up to {NMAX}")
print(f"values where SOME fallback configuration could reach B(n): {len(bad)}")
for n, B, d, w in bad[:20]:
    print(f"   n={n} B={B} density={d:.4f}  candidates: {w}")
print()
print(f"settled by theorem alone, all branches: {fully} of {N} ({100*fully/N:.1f}%)")
print(f"s-branches dispatched by theorem: {branch_ok} of {branch_tot} "
      f"({100*branch_ok/branch_tot:.1f}%) -- the rest go to the search")
for why, k in sorted(reasons.items(), key=lambda t: -t[1]):
    print(f"    {k:5d}  {why}")
print()
print(f"largest permitted s over the range: "
      f"{max(fb.s_max(int(r['n']), int(r['mu_bound'])) for r in rows)}")
if not bad:
    print()
    print("CERTIFIED.  At every n in this table, no admissible configuration that")
    print("invokes the unconditional fallback can attain B(n).  So the SAFE optimum")
    print("is fallback-free independently of tie-breaking, the Part E construction")
    print("realises it, and mu(n) = B(n) is proved at each of these n.")
sys.exit(1 if bad else 0)
