"""
check_groups.py -- pre-flight validation of a GAP-produced groups_out.txt
before committing hours to consume_gap.py stage 3.

Degree n is auto-detected from the orbital-map length (must be triangular);
override with --n.  Exit status 0 = green light, 1 = problems found.

Usage:
  python3 check_groups.py                      # ./groups_out.txt
  python3 check_groups.py --file path --n 12
  python3 check_groups.py --maxt 8             # preview a battery cut
"""
import argparse, collections, itertools, sys
from math import comb, isqrt

ap = argparse.ArgumentParser()
ap.add_argument('--file', default='groups_out.txt')
ap.add_argument('--n', type=int, default=0, help='degree (default: auto-detect)')
ap.add_argument('--maxt', type=int, default=0,
                help='if set, also report the battery surviving this orbital cap')
ap.add_argument('--top', type=int, default=6, help='how many top-m* groups to show')
args = ap.parse_args()

lines = [l.strip() for l in open(args.file) if l.strip()]
if not lines:
    sys.exit(f"{args.file} is empty")

# ---- degree detection ----
first_len = len(lines[0].split('|')[3].split(','))
if args.n:
    n = args.n
else:
    n = (1 + isqrt(1 + 8 * first_len)) // 2
NPAIRS = comb(n, 2)
if NPAIRS != first_len:
    sys.exit(f"orbital-map length {first_len} is not C(n,2) for any n "
             f"(detected n={n} gives {NPAIRS}); pass --n explicitly")
print(f"file: {args.file}   detected degree n = {n}   C(n,2) = {NPAIRS}")

# ---- per-line validation ----
tags, ts, bad = collections.Counter(), collections.Counter(), []
groups = []
for ln_no, ln in enumerate(lines, 1):
    parts = ln.split('|')
    if len(parts) != 4:
        bad.append((ln_no, f"{len(parts)} fields, expected 4")); continue
    key, desc, tag, om = parts
    try:
        omap = [int(x) for x in om.split(',')]
    except ValueError:
        bad.append((ln_no, "non-integer in orbital map")); continue
    if len(omap) != NPAIRS:
        bad.append((ln_no, f"orbital map length {len(omap)} != {NPAIRS}")); continue
    t = max(omap)
    if sorted(set(omap)) != list(range(1, t + 1)):
        bad.append((ln_no, "orbital indices not 1..t contiguous")); continue
    tags[tag] += 1; ts[t] += 1
    c = collections.Counter(omap)
    groups.append(dict(key=key, desc=desc, tag=tag, t=t,
                       mstar=min(c.values()), sizes=sorted(c.values())))

print(f"lines: {len(lines)}   valid: {len(groups)}   malformed: {len(bad)}")
for ln_no, why in bad[:10]:
    print(f"  line {ln_no}: {why}")
if len(bad) > 10:
    print(f"  ... and {len(bad)-10} more")

# ---- summaries ----
print(f"tags: {dict(sorted(tags.items()))}")
print(f"  (tag '0' = trivial-top Oliver, chi==1 exactly -- the harshest condition;"
      f"\n   tag q  = Oliver with top prime q;  tag P<p> = p-group, Smith battery)")
print(f"t distribution: {dict(sorted(ts.items()))}")
print(f"  CSP lattice cost sum(2^t) over Oliver groups = "
      f"{sum(2**g['t'] for g in groups if not g['tag'].startswith('P')):,}")

oliver = [g for g in groups if not g['tag'].startswith('P')]
psub   = [g for g in groups if g['tag'].startswith('P')]
oliver.sort(key=lambda g: (-g['mstar'], g['t']))
print(f"\ntop {args.top} Oliver groups by minimum u-orbital m*:")
for g in oliver[:args.top]:
    print(f"  m*={g['mstar']:5d}  t={g['t']:2d}  tag={g['tag']:3s}  {g['key']:22s} {g['desc'][:44]}")
if oliver:
    best = oliver[0]['mstar']
    print(f"mu_lower from this file: {best}/{NPAIRS} = {best/NPAIRS:.3f}"
          f"   (proven ceiling for non-prime-power n: {NPAIRS//2}/{NPAIRS} = 0.500)")

if args.maxt:
    keep = [g for g in groups if g['t'] <= args.maxt]
    ko = [g for g in keep if not g['tag'].startswith('P')]
    print(f"\nwith --maxt {args.maxt}: {len(keep)} groups survive "
          f"({len(ko)} Oliver, {len(keep)-len(ko)} p-groups), "
          f"sum(2^t) = {sum(2**g['t'] for g in keep):,}")

# ---- green-light criteria ----
print("\ngreen-light checks:")
ok = True
def chk(cond, msg):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {msg}")
    if not cond: ok = False
chk(not bad, "no malformed lines")
chk(tags.get('0', 0) > 0, "trivial-top groups present (chi==1-exact constraints)")
chk(len(psub) > 0, "p-groups present (Smith battery)")
chk(len(oliver) > 0, "Oliver groups present")
chk(bool(ts) and min(ts) >= 2, "every group has >= 2 orbitals (non-prime-power n)")
print("\n" + ("GREEN: proceed to consume_gap.py" if ok else
              "PROBLEMS: inspect before proceeding"))
sys.exit(0 if ok else 1)
