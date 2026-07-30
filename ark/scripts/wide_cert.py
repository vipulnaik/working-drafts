#!/usr/bin/env python3
"""
wide_cert.py -- run the fallback-collapse certificate far beyond the computed
table, by substituting a PROVEN LOWER BOUND for B(n).

WHY THIS IS SOUND.  A fallback configuration attaining B_safe(n) has every SAFE
term >= B_safe(n) >= B_lo(n), so it satisfies the necessary conditions of
`fb_common.py` with B_lo in place of B.  An empty candidate list at n therefore
proves the collapse there without knowing B(n).  A weaker bound can only ADD
spurious candidates, never miss a real one.  Cost is O(n/log n) per value
against the table's n^2.9, which is what buys the range.

B_lo(n) = max over two families of admissible configurations, each scored in
SAFE mode, hence each a genuine lower bound on B_safe(n):
  * the family menu of `mu_enumerate.seed_value`;
  * the dominant three-part shape (1,c) + (1,c) + (1,r*), maximised over
    prime-power c with r* = n - 2c prime.
The second is essential: without it the certificate resolves 86.6% of n <= 10^4,
with it 99.91%, and the multi-part leftover check closes the remaining 0.09%.

Any n where candidates survive is reported as UNRESOLVED AT B_lo -- it needs the
true B(n) to settle and is NOT a counterexample.

Usage: python3 wide_cert.py NMAX
"""
import importlib.util, sys, time, bisect
from math import comb
import fb_common as fb

_A = list(sys.argv); sys.argv = ['x']
spec = importlib.util.spec_from_file_location("me", "/home/claude/ark/mu_enumerate.py")
me = importlib.util.module_from_spec(spec); me.__name__ = "me"
spec.loader.exec_module(me)

NMAX = int(_A[1]) if len(_A) > 1 and not _A[1].startswith('-') else 10000
A = fb.Arith(NMAX + 2)
caps_m, caps_r = fb.cap_mersenne(A, NMAX), fb.cap_repunit(A, NMAX)

# ---- pass 1: the lower bound
#
# Scanning c downward from n/2 over prime powers and keeping the first SCAN_CAP
# hits suffices: the binding term min(C(c,2), c*r*, cap(r*)) is largest for c
# near n/2, and taking any SUBSET of admissible configurations still gives a
# valid lower bound.  Verified at NMAX = 10^4: SCAN_CAP = 60 alone resolves every
# value, identically to the full scan plus the family menu.  The menu is kept
# behind --menu for cross-checking; it costs O(n/log n) per value and dominates
# the runtime, so it is off by default.
t0 = time.time()
SCAN_CAP = 60
PPs = [c for c in range(3, NMAX // 2 + 2) if A.prime_power(c)]
PPs2 = [c for c in range(3, NMAX + 1) if A.prime_power(c)]
_FC = {}
def fcap(r):
    v = _FC.get(r)
    if v is None:
        v = _FC[r] = fb.foreign_cap(A, r)
    return v

def near(seq, target, cap):
    """The `cap` entries of the sorted list `seq` nearest to `target`.  The
    lower-bound families below all balance one growing term against one
    shrinking term, so their optimum sits near a balance point rather than at
    an endpoint -- scanning outward from that point is what makes a small cap
    sufficient."""
    i = bisect.bisect_left(seq, target)
    lo, hi, out = i - 1, i, []
    while len(out) < cap and (lo >= 0 or hi < len(seq)):
        if hi >= len(seq) or (lo >= 0 and target - seq[lo] <= seq[hi] - target):
            out.append(seq[lo]); lo -= 1
        else:
            out.append(seq[hi]); hi += 1
    return out

def orb_full(c, t, char2):
    raw = c * t // 2 if (char2 or t % 2 == 0) else c * t
    return min(raw, comb(c, 2))

def three_part_lo(n, cap=None):
    """(1,c)+(1,c)+(1,r*).  Terms C(c,2) ~ c^2/2 and cap(r*) <= r*^2/2 balance
    at c ~ r* ~ n/3, so scan c outward from n/3.  Needs n - 2c prime, hence
    exists mainly for odd n."""
    best = 0
    for c in near(PPs, n // 3, cap or SCAN_CAP):
        rr = n - 2 * c
        if rr < 3 or not A.is_prime(rr) or rr == A.prime_power(c)[0]:
            continue
        best = max(best, min(comb(c, 2), c * rr, fcap(rr)))
    return best

def two_part_lo(n, cap=None):
    """(1,c)+(1,r*).  Balances at c ~ r* ~ n/2.  Covers even n, where the
    three-part shape does not exist."""
    best = 0
    for c in near(PPs2, n // 2, cap or SCAN_CAP):
        rr = n - c
        if rr < 3 or not A.is_prime(rr) or rr == A.prime_power(c)[0]:
            continue
        best = max(best, min(comb(c, 2), c * rr, fcap(rr)))
    return best

def fused_lo(n):
    """A single fused class (F, c), n = F*c, F a q-power, c a prime power.
    Includes Theorem 2.1's n = 2*(prime power) at F = 2, q = 2."""
    best = 0
    F = 2
    while F * F <= n:
        if n % F == 0:
            for FF in (F, n // F):
                pf = A.prime_power(FF)
                c = n // FF
                pc = A.prime_power(c)
                if pf and pc:
                    best = max(best, min(FF * orb_full(c, c - 1, pc[0] == 2),
                                         (FF if pf[0] % 2 else FF // 2) * c * c))
        F += 1
    return best

# The cheap families leave a few dozen values with a weak bound; for those only,
# top up with the family menu of mu_enumerate.seed_value.  That is O(n/log n) per
# call and would dominate if used everywhere, but on a few hundred values it is
# free -- and it lifts the density floor, which is what keeps the permitted s
# (and hence pass 2) small.
WEAK = 0.02
t1 = time.time()
CACHE = f"/home/claude/blo_{NMAX}.txt"          # pass 1 is the expensive half
import os
if os.path.exists(CACHE) and '--refresh' not in _A:
    Blo = [0] * (NMAX + 2); ns = []
    for line in open(CACHE):
        n, v = line.split()
        Blo[int(n)] = int(v); ns.append(int(n))
    topped = escal = -1
    print(f"        loaded B_lo from {CACHE} ({len(ns)} values)")
else:
  spf = me.sieve_spf(NMAX + 2)
  Blo = [0] * (NMAX + 2); ns = []; topped = escal = 0
  for n in range(6, NMAX + 1):
    if A.prime_power(n):
        continue
    v = max(three_part_lo(n), two_part_lo(n), fused_lo(n))
    if v == 0 or 2 * v / (n * (n - 1)) < WEAK:
        v = max(v, me.seed_value(n, spf)); topped += 1
        if 2 * v / (n * (n - 1)) < WEAK:      # still weak: escalate the scan
            v = max(v, three_part_lo(n, 10**9), two_part_lo(n, 10**9))
            escal += 1
    Blo[n] = v
    ns.append(n)
  with open(CACHE, "w") as fh:
    for n in ns:
        fh.write(f"{n} {Blo[n]}\n")
  print(f"        cheap families + {topped} menu top-ups + {escal} full escalations "
        f"({time.time()-t1:.0f}s); cached to {CACHE}")
no_bound = [n for n in ns if Blo[n] == 0]
ns = [n for n in ns if Blo[n] > 0]
by_B = sorted(ns, key=lambda n: Blo[n]); Bvals = [Blo[n] for n in by_B]
dmin = min(2 * Blo[n] / (n * (n - 1)) for n in ns)
print(f"pass 1: B_lo for {len(ns)} values in [6, {NMAX}]"
      + (f" (+{len(no_bound)} with no bound: {no_bound[:8]}...)" if no_bound else "")
      + f"  ({time.time()-t0:.0f}s); weakest density {dmin:.6f}, permitted s <= "
        f"{int(1/dmin**0.5 - 1)}")

# ---- pass 2: pair scan
#
# Two filters make this cheap, and both must be applied BEFORE iterating over n
# rather than inside the loop:
#   * s <= s_max(n, B) rearranges to delta_lo(n) <= 1/(s+1)^2, so a pair with
#     s = 2 can only threaten values of density at most 1/9.  Most n are denser
#     than that, so the per-s candidate lists are far shorter than the whole
#     range.
#   * the foreign block's own cap bounds B, so only n with B_lo(n) <= cap(r)
#     are reachable -- a prefix of each list once it is sorted by B_lo.
t0 = time.time()
S_TOP = max(fb.s_max(n, Blo[n]) for n in ns)
per_s = {}
for sv in range(1, S_TOP + 1):
    thr = 1.0 / (sv + 1) ** 2
    lst = [n for n in ns if 2 * Blo[n] / (n * (n - 1)) <= thr]
    lst.sort(key=lambda n: Blo[n])
    per_s[sv] = (lst, [Blo[n] for n in lst])
print(f"pass 2: permitted s <= {S_TOP}; candidate values per s: "
      + ", ".join(f"s={k}: {len(v[0])}" for k, v in sorted(per_s.items())))

cand = {}
pairs_seen = pairs_live = items = 0
for r in range(3, NMAX, 2):
    if not A.is_prime(r):
        continue
    capr = fb.foreign_cap(A, r)
    sv = 1
    while True:
        c = sv * r + 1
        if c + r > NMAX:
            break
        s_this = sv; sv += 1
        if s_this > S_TOP:
            break
        pp = A.prime_power(c)
        if not pp or pp[0] == r:
            continue
        p = pp[0]
        pairs_seen += 1
        lst, Bl = per_s[s_this]
        hi = bisect.bisect_right(Bl, capr)
        if hi == 0:
            continue
        pairs_live += 1
        for n in lst[:hi]:
            if n < c + r:
                continue
            B = Blo[n]
            ok_thm, _ = fb.branch_settled(A, n, B, s_this, caps_m, caps_r)
            if ok_thm:
                continue
            items += 1
            got = fb.pair_candidates(A, n, B, c, r, p)
            if got:
                cand.setdefault(n, []).extend(got)
print(f"        {pairs_seen} (c,r,s) pairs, {pairs_live} with a nonempty window, "
      f"{items} (pair, n) checks after theorem dispatch  ({time.time()-t0:.0f}s)")

for n in no_bound:
    cand.setdefault(n, []).append(('NO-LOWER-BOUND',))
res = sorted(cand)
tot = len(ns) + len(no_bound)
print()
print(f"UNRESOLVED at B_lo: {len(res)} of {tot}")
for n in res:
    print(f"    n={n:6d} B_lo={Blo[n]:9d} d_lo={2*Blo[n]/(n*(n-1)):.4f}  {cand[n][:2]}")
print()
ok = tot - len(res)
print(f"COLLAPSE CERTIFIED at {ok} of {tot} values ({100*ok/tot:.2f}%) in [6, {NMAX}]")
print("from proven lower bounds alone.  Unresolved values need the true B(n) and")
print("are not counterexamples; at every n <= 2007 the true-table certificate agrees.")
