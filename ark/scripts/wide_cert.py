#!/usr/bin/env python3
"""
wide_cert.py -- run the fallback-collapse certificate far beyond the computed
table, using a PROVEN LOWER BOUND on B(n) in place of B(n).

SOUNDNESS.  A fallback configuration attaining B_safe(n) has every SAFE term
>= B_safe(n) >= B_lo(n), so it satisfies the certificate's necessary conditions
with B_lo in place of B.  An empty candidate list at n therefore proves the
collapse (mu(n) = B(n), B_refined = B_safe) at that n, exactly as in
fallback_cert.py.  A weaker bound can only ADD spurious candidates, never miss
a real one.  B_lo here is mu_enumerate.seed_value -- the family-menu score,
a genuine admissible-configuration value, hence <= B_safe(n).

Any n where candidates survive is reported as UNRESOLVED AT B_lo: it needs the
true B(n) (i.e. the table) to settle, and is not a counterexample.

Usage: python3 wide_cert.py NMAX
"""
import importlib.util, sys, time
from math import comb

_A = list(sys.argv); sys.argv = ['x']
spec = importlib.util.spec_from_file_location("me", "/home/claude/ark/mu_enumerate.py")
me = importlib.util.module_from_spec(spec); me.__name__ = "me"
spec.loader.exec_module(me)

NMAX = int(_A[1]) if len(_A) > 1 else 10000
S_MAX = 8                      # s <= 1/sqrt(delta_lo) - 1; menu floor 0.0147 -> 7.2
spf = me.sieve_spf(NMAX + 2)

def prime_power(x):
    if x < 2: return None
    p = spf[x]; e = 0
    while x % p == 0: x //= p; e += 1
    return (p, e) if x == 1 else None

def is_prime(x): return x > 1 and spf[x] == x

def qpart(x, q):
    t = 1
    while x % (t * q) == 0: t *= q
    return t

def orb(c, t):
    return min(c * t // 2 if t % 2 == 0 else c * t, comb(c, 2))

def prime_divisors(x):
    out = []
    while x > 1:
        p = spf[x]; out.append(p)
        while x % p == 0: x //= p
    return out

# ---- per-r foreign cap (including the trivial-twist q ∤ r-1 branch, orb = r)
def foreign_cap(r):
    if r <= 2: return 1
    return max([r] + [orb(r, qpart(r - 1, q)) for q in set(prime_divisors(r - 1))])

# ---- pass 1: B_lo for every composite non-prime-power n, and its suffix minimum
t0 = time.time()
Blo = [0] * (NMAX + 2)
ns = []
def three_part_lo(n):
    """SAFE score of the dominant three-part shape (1,c)+(1,c)+(1,r*):
    min(C(c,2), c*r*, foreign_cap(r*)) maximised over prime-power c with
    r* = n - 2c prime, r* != base(c).  Any admissible configuration's SAFE
    score lower-bounds B_safe, so this is a sound strengthening of B_lo."""
    best = 0
    for c in range(3, n // 2):
        pp = prime_power(c)
        if not pp: continue
        rr = n - 2 * c
        if rr < 3 or not is_prime(rr) or rr == pp[0]: continue
        v = min(comb(c, 2), c * rr, foreign_cap(rr))
        if v > best: best = v
    return best
for n in range(6, NMAX + 1):
    if prime_power(n): continue
    Blo[n] = max(me.seed_value(n, spf), three_part_lo(n))
    ns.append(n)
no_bound = [n for n in ns if Blo[n] == 0]        # menu empty: unresolved a priori
ns = [n for n in ns if Blo[n] > 0]
sufmin = [0] * (NMAX + 3)
cur = 10**18
for n in range(NMAX + 1, 5, -1):
    if Blo[n]: cur = min(cur, Blo[n])
    sufmin[n] = cur
dmin = min(2 * Blo[n] / (n * (n - 1)) for n in ns)
print(f"pass 1: B_lo for {len(ns)} values of n in [6, {NMAX}] "
      f"(+{len(no_bound)} with empty menu, unresolved a priori: {no_bound})  ({time.time()-t0:.0f}s); "
      f"weakest density {dmin:.6f} at n = {min(ns, key=lambda n: 2*Blo[n]/(n*(n-1)))} "
      f"(s adapts per n; no global cap)")
by_B = sorted(ns, key=lambda n: Blo[n])          # for capr-window iteration
Bvals = [Blo[n] for n in by_B]
import bisect

# ---- helpers for conditions (7)-(8), ported from fallback_cert.py
def intra_floor(B):
    s = 1
    while s * (s - 1) // 2 < B: s += 1
    return s

def multi_part_ok(L, B, p, q, r):
    """Can L split into >= 2 admissible parts, each meeting the necessary
    floors?  Sound over-approximation (necessary conditions only): foreign
    parts are distinct primes rj != r with orb(rj, qpart(rj-1, q)) >= B (for
    q = '*', the cap over all q); p-characteristic parts are (F', p^j) with F'
    a q-power and F'*C(p^j, 2) >= B, repeats allowed.  Exact-sum DP.  Returns
    False (proved impossible), True (a split exists -- candidate stands), or
    None if the candidate set is unexpectedly large."""
    fcands = []
    for rj in range(3, L + 1, 2):
        if not is_prime(rj) or rj == r: continue
        capj = (max(foreign_cap(rj), rj) if q == '*' else orb(rj, qpart(rj - 1, q)))
        if capj >= B: fcands.append(rj)
    pcands = []
    cj = p
    while cj <= L:
        F = 1
        while F * cj <= L:
            if F * comb(cj, 2) >= B: pcands.append(F * cj)
            if q == '*': break
            F *= q
        cj *= p
    if len(fcands) + len(pcands) > 60: return None
    # DP over subset sums: foreign distinct, p-char unbounded multiplicity
    reach = {0}
    for x in fcands:
        reach |= {v + x for v in reach if v + x <= L}
    for x in pcands:
        new = True
        while new:
            add = {v + x for v in reach if v + x <= L} - reach
            reach |= add; new = bool(add)
    return L in reach

def single_part_ok(L, B, p, q, r):
    """q is a concrete prime, or '*' for the generic branch (q unknown, over-
    approximated soundly: any F' | L, foreign twist up to the largest prime-power
    divisor of c2-1 or trivial)."""
    Fs = ([f for f in range(1, L + 1) if L % f == 0] if q == '*'
          else [q ** i for i in range(0, 64) if q ** i <= L])
    for F in Fs:
        if L % F: continue
        c2 = L // F
        pp = prime_power(c2)
        if not pp: continue
        if pp[0] == p:
            if F * comb(c2, 2) >= B: return True
        elif pp[1] == 1 and c2 != r:
            capf = max(foreign_cap(c2), c2) if q == '*' else orb(c2, qpart(c2 - 1, q))
            if F == 1 and capf >= B: return True
    return False

# ---- pass 2: pair scan
t0 = time.time()
cand = {}          # n -> list of (p,q,F,c,r,s,L)
pairs_seen = pairs_live = items = 0
for r in range(3, NMAX, 2):
    if not is_prime(r): continue
    capr = foreign_cap(r)
    s = 1
    while True:
        c = s * r + 1
        if c + r > NMAX: break
        s_this = s; s += 1
        pp = prime_power(c)
        if not pp: continue
        p = pp[0]
        if p == r: continue
        pairs_seen += 1
        hi = bisect.bisect_right(Bvals, capr)     # only n with B_lo <= capr
        if hi == 0: continue
        pairs_live += 1
        for n in by_B[:hi]:
            if n < c + r: continue
            B = Blo[n]
            items += 1
            qopts = list(set(prime_divisors(r - 1)))
            if r >= B: qopts.append('*')          # trivial-twist generic branch
            for q in qopts:
                t = 1 if q == '*' else qpart(r - 1, q)
                if orb(r, t) < B: continue
                Fmax = (n - r) // c
                Fs = ([1] if q == '*' else None)
                F = 1
                while F <= Fmax:
                    ok = (F * comb(c, 2) >= B and F * c * r >= B and
                          (F == 1 or (F if q % 2 else F // 2) * c * c >= B))
                    if ok:
                        L = n - F * c - r
                        if L != 0:
                            need = max(-(-B // min(F * c, r)), intra_floor(B))
                            if L < need: ok = False
                            elif L < 2 * need: ok = single_part_ok(L, B, p, q, r)
                            else:
                                ok = (single_part_ok(L, B, p, q, r)
                                      or multi_part_ok(L, B, p, q, r))
                    if ok:
                        cand.setdefault(n, []).append((p, q, F, c, r, s_this, n - F*c - r))
                        break
                    if ok is None:
                        cand.setdefault(n, []).append((p, q, F, c, r, s_this, 'MULTI-LEFTOVER'))
                        break
                    if q == '*': break            # generic branch: F = 1 only
                    F *= q
                if n in cand and cand[n] and cand[n][-1][3] == c: break
print(f"pass 2: {pairs_seen} (c,r,s) pairs, {pairs_live} with nonempty window, "
      f"{items} (pair, n) checks  ({time.time()-t0:.0f}s)")
print()
for n in no_bound: cand.setdefault(n, []).append(('NO-BOUND',))
res = sorted(cand)
print(f"values of n in [6, {NMAX}] UNRESOLVED at B_lo: {len(res)} of {len(ns)}")
inrange = [n for n in res if n <= 2007]
print(f"  of which n <= 2007 (settled by the true table already): {len(inrange)}")
print(f"  genuinely new unresolved (2008 <= n <= {NMAX}): {len(res) - len(inrange)}")
for n in res:
    if n > 2007:
        print(f"    n={n:6d} B_lo={Blo[n]:9d} d_lo={2*Blo[n]/(n*(n-1)):.4f}  {cand[n][:2]}")
print()
ok = len(ns) - len(res)
print(f"COLLAPSE CERTIFIED at {ok} of {len(ns)} values ({100*ok/len(ns):.2f}%) in [6, {NMAX}]")
print("using only proven lower bounds; unresolved values need the true B(n), and are")
print("not counterexamples -- at every n <= 2007 the true-table certificate already passes.")
