#!/usr/bin/env python3
"""
migrate_table.py -- convert a mu_table CSV from the old schema to the new one.

Old:  n,C(n2),mu_bound,density,orbits_K,certified,fallback,witness
New:  n,C(n2),mu_bound,density,parts,certified_K,partcap,certified,fallback,witness

NOTHING IS RECOMPUTED.  The migration is a pure text transform:

  * orbits_K is RENAMED to certified_K.  The values are unchanged; only the name
    was wrong.  It always was the certification level -- the first K at which
    Prop. F.1's 1/sqrt(delta) <= K holds -- and never the number of parts.
  * parts   is read off the witness string (count of '+'-separated orbits).
  * partcap is floor(1/sqrt(density)), the Prop. F.1 ceiling on the part count.

Both new columns are functions of data already present, so the old rows survive
intact and no value of B(n) is revisited.  Every migrated row is checked for
internal consistency: parts <= partcap, and 1/sqrt(density) <= certified_K.

Usage:
    python3 migrate_table.py mu_table_safe.csv mu_table_safe_v2.csv
    python3 migrate_table.py --check mu_table_safe.csv     # verify only, no write
"""
import csv, re, sys, argparse
from math import comb

OLD = "n,C(n2),mu_bound,density,orbits_K,certified,fallback,witness"
NEW = ("n,C(n2),mu_bound,density,parts,certified_K,partcap,"
       "certified,fallback,witness")

ap = argparse.ArgumentParser()
ap.add_argument("infile")
ap.add_argument("outfile", nargs="?")
ap.add_argument("--check", action="store_true",
                help="validate the input and report, without writing")
a = ap.parse_args()
if not a.check and not a.outfile:
    ap.error("give an outfile, or use --check")

with open(a.infile) as fh:
    header = fh.readline().rstrip("\n").lstrip("\ufeff").rstrip("\r")
    if header == NEW:
        sys.exit(f"{a.infile} is already in the new schema; nothing to do")
    if header != OLD:
        sys.exit(f"unrecognised header:\n    {header}\nexpected the old schema:\n"
                 f"    {OLD}")
    rows = list(csv.DictReader(fh, fieldnames=OLD.split(",")))

def parts_of(witness):
    """Number of orbits in a witness like 'p=277 q=2: 1x641* + 1x277 + 1x257*'."""
    m = re.match(r"p=\S+ q=\d+:\s*(.*?)(\s{2,}\(\* foreign\))?$", witness.strip())
    if not m:
        return None
    return len([t for t in m.group(1).split(" + ") if t.strip()])

out, bad = [], []
for r in rows:
    n = int(r["n"]); dens = float(r["density"])
    k = int(r["orbits_K"])
    npart = parts_of(r["witness"])
    cap = int(1.0 / dens ** 0.5) if dens > 0 else 0
    if npart is None:
        bad.append((n, "unparseable witness", r["witness"])); continue
    # consistency of the file with itself, and with Prop. F.1
    if abs(dens - int(r["mu_bound"]) / comb(n, 2)) > 5e-7:
        bad.append((n, "density does not match mu_bound/C(n,2)", r["density"]))
    if 1.0 / dens ** 0.5 > k:
        bad.append((n, "certification level below the Prop. F.1 requirement", k))
    if npart > cap:
        bad.append((n, f"parts {npart} exceeds the permitted {cap}", r["witness"]))
    out.append((n, r["C(n2)"], r["mu_bound"], r["density"], npart, k, cap,
                r["certified"], r["fallback"], r["witness"]))

print(f"{a.infile}: {len(rows)} rows, n from {rows[0]['n']} to {rows[-1]['n']}")
print(f"inconsistencies: {len(bad)}")
for b in bad[:10]:
    print("   ", b)
if out:
    ps = [o[4] for o in out]; ks = [o[5] for o in out]
    hist = lambda v: dict(sorted((x, v.count(x)) for x in set(v)))
    print(f"parts        {hist(ps)}   (max {max(ps)})")
    print(f"certified_K  {hist(ks)}   (max {max(ks)})")
    print(f"max parts {max(ps)} against min permitted {min(o[6] for o in out)} "
          f"-- the gap the old single column hid")

if a.check:
    sys.exit(0 if not bad else 1)
if bad:
    sys.exit("refusing to write a file with inconsistencies; investigate first")
with open(a.outfile, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(NEW.split(","))
    for o in out:
        w.writerow(o)
print(f"wrote {a.outfile} ({len(out)} rows). mu_enumerate.py will now append to "
      f"it and resume from n = {max(o[0] for o in out) + 1}.")
