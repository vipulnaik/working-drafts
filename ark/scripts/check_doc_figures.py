#!/usr/bin/env python3
"""
check_doc_figures.py -- catch range-dependent figures that a table extension has
made stale.  Written after three consecutive extensions each left a different
subset of the documents behind.

It recomputes every figure the prose quotes and greps for the ones that no longer
match.  It does NOT edit: it reports, because several of the numbers appear in
sentences whose wording has to change with them.

Usage: python3 check_doc_figures.py mu_table_safe_v2.csv *.md
"""
import csv, sys, re, collections, statistics
from math import comb

table, docs = sys.argv[1], sys.argv[2:]
rows = list(csv.DictReader(open(table)))
N = len(rows); NMAX = max(int(r["n"]) for r in rows)
D = [float(r["density"]) for r in rows]
spf = list(range(NMAX + 2)); i = 2
while i * i <= NMAX + 1:
    if spf[i] == i:
        for j in range(i * i, NMAX + 2, i):
            if spf[j] == j: spf[j] = i
    i += 1
def omega(x):
    s = set()
    while x > 1:
        p = spf[x]; s.add(p)
        while x % p == 0: x //= p
    return len(s)
parts = collections.Counter(int(r["parts"]) for r in rows)
certK = collections.Counter(int(r["certified_K"]) for r in rows)
floor_n = rows[D.index(min(D))]["n"]; peak_n = rows[D.index(max(D))]["n"]
cur = {
    "row count":            f"{N:,}",
    "n max":                str(NMAX),
    "density floor":        f"{min(D):.6f} at n = {floor_n}",
    "density max":          f"{max(D):.6f} at n = {peak_n}",
    "median density":       f"{statistics.median(D):.4f}",
    "part counts":          str(dict(sorted(parts.items()))),
    "certified_K":          str(dict(sorted(certK.items()))),
    "delta >= 1/4":         f"{sum(1 for x in D if x >= .25)} ({100*sum(1 for x in D if x >= .25)/N:.1f}%)",
    "delta > 1/9":          f"{sum(1 for x in D if x > 1/9)} ({100*sum(1 for x in D if x > 1/9)/N:.1f}%)",
    "tail delta <= 1/16":   f"{sum(1 for x in D if x <= 1/16)}",
    "omega(n) = 2":         f"{sum(1 for r in rows if omega(int(r['n'])) == 2)}",
    "three-part winners":   str(parts[3]),
}
print(f"{table}: current values")
for k, v in cur.items():
    print(f"   {k:22} {v}")
print()
# figures that have appeared in the prose and are range-dependent
PAT = [r"1,\d{3} (?:values|rows|computed)", r"n = 6 … \d{4}", r"n ≤ \d{4}", r"n = \d{4}\b",
       r"0\.0\d{5} at n = \d+", r"δ ≥ 1/4 [^.]{0,30}\d\d\.\d%", r"δ > 1/9 [^.]{0,30}\d\d\.\d%",
       r"\{1: \d+, 2: \d+, 3: \d+\}", r"\{2: \d+, 3: \d+, 4: \d+, 5: \d+\}",
       r"\d+ of 1,\d{3}", r"\d+ three-part winners", r"median (?:density )?0\.\d{4}"]
stale = 0
for d in docs:
    try: txt = open(d).read()
    except OSError: continue
    hits = []
    for p in PAT:
        for m in re.finditer(p, txt):
            frag = m.group(0)
            if (str(N) not in frag and f"{N:,}" not in frag and str(NMAX) not in frag
                    and frag not in str(cur.values())):
                hits.append(frag)
    hits = sorted(set(hits))
    if hits:
        print(f"{d}: {len(hits)} range-dependent figures to eyeball")
        for h in hits[:14]: print(f"     {h}")
        stale += len(hits)
print()
print(f"{stale} figures flagged. Not all are stale -- historical citations are legitimate;")
print("the point is that each should be checked against the list above after an extension.")
