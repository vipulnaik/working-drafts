#!/usr/bin/env python3
"""
fallback_cert.py -- certify, per n, that Part J item 2's caveat cannot bite.

BACKGROUND.  In SAFE mode `mu_enumerate.py` scores a p-characteristic part
(F, c) whose twist Lemma C strictly reduces with the UNCONDITIONAL capacity
F*C(c,2), valid for any point stabiliser.  The Part E construction reaches only
F*orb(c, d) with d = strip(c-1, foreigns).  So at such a configuration the bound
is valid but NOT attained, and if the SAFE optimum were ever achieved only by
such a configuration, mu(n) = B(n) would fail at that n.

`fallback_used()` answers the weaker question "did the REPORTED WITNESS use it",
which depends on how the optimiser broke ties.  This script answers the strong
question: could ANY admissible configuration invoking the fallback have scored
B(n)?  If not, the SAFE optimum is fallback-free whatever the optimiser chose,
so B(n) is attained and mu(n) = B(n) is PROVED at that n.

THE CERTIFICATE.  A fallback configuration contains a p-characteristic part
(F, c) and a foreign prime r of the same configuration with r | c-1.  Every term
of the min must be at least B, which forces all of:

    (1)  c = p^a  for some prime p,  and  r prime,  r != p,  r | c-1
    (2)  F a power of q,  F*c + r <= n            (the two parts fit)
    (3)  F*C(c,2)            >= B                 (the p-part's intra term)
    (4)  orb(r, qpart(r-1,q)) >= B                (the foreign part's intra term)
    (5)  F*c*r               >= B                 (the cross term between them)
    (6)  (F or F/2)*c^2      >= B  when F > 1      (the within-class cross)
    (7)  L := n - F*c - r  is either 0, or large enough to be a legal part:
         every other part s' must satisfy s'*(F*c) >= B and s'*r >= B (its cross
         terms with these two) and cap(s') >= B (its own intra term, so
         s'(s'-1)/2 >= B).  If L is split into j parts each meeting that floor
         then L >= j*floor >= floor.  So L = 0 or L >= max(ceil(B/min(Fc,r)),
         min{s : s(s-1)/2 >= B}).

Condition (7) is what does most of the work, and omitting it makes the check
badly incomplete: without it 58 of 1,582 values look dangerous, all of them
spurious because the leftover is a handful of points that cannot carry a cross
term of size B.  Any further parts only lower the minimum, so (1)-(7) are
NECESSARY.  Enumerating
the tuples (p, q, F, c, r) that satisfy them is O(n log n) with a smallest-prime-
factor sieve.  An empty list is a proof for that n.

STRUCTURAL COROLLARY (proved, and the reason the check almost always succeeds).
Write s = (c-1)/r and delta = B/C(n,2).  From (4), orb(r,t) <= C(r,2), so
r(r-1) >= delta*n(n-1), giving r >~ sqrt(delta)*n; and c <= n - r by (2).  Hence

    s = (c-1)/r <= (n - r - 1)/r <= (1 - sqrt(delta))/sqrt(delta),

so s <= 1 when delta >= 1/4, s <= 2 when delta >= 1/9, s <= 3 when delta >= 1/16.
And s = 1 means c - 1 = r is prime: for r > 2 that forces c even, so c = 2^a with
r = 2^a - 1 a MERSENNE PRIME, and then d = strip(r, {r}) = 1 -- the twist dies
completely.  In that case t = qpart(2^a - 2, q) divides 2*(2^(a-1) - 1), so

    orb(r, t) <= r * max(2, L(a)),      L(a) = largest prime-power divisor of 2^(a-1) - 1,

an ABSOLUTE constant Cap(a) independent of F and of n.  So the s = 1 branch can
only win at n with B(n) <= Cap(a), which is a finite condition per Mersenne
exponent: Cap(2)=6, Cap(3)=21, Cap(5)=155, Cap(7)=1143, Cap(13)=106483.

Usage:
    python3 fallback_cert.py mu_table_safe_v2.csv
    python3 fallback_cert.py mu_table_safe_v2.csv --verbose
"""
import argparse, csv, sys
from math import comb

ap = argparse.ArgumentParser()
ap.add_argument("table")
ap.add_argument("--verbose", action="store_true")
a = ap.parse_args()

rows = list(csv.DictReader(open(a.table)))
NMAX = max(int(r["n"]) for r in rows)

spf = list(range(NMAX + 2))
i = 2
while i * i <= NMAX + 1:
    if spf[i] == i:
        for j in range(i * i, NMAX + 2, i):
            if spf[j] == j:
                spf[j] = i
    i += 1

def is_prime(x):
    return x > 1 and spf[x] == x

def prime_power(x):
    if x < 2:
        return None
    p = spf[x]; e = 0
    while x % p == 0:
        x //= p; e += 1
    return (p, e) if x == 1 else None

def qpart(x, q):
    t = 1
    while x % (t * q) == 0:
        t *= q
    return t

def orb(c, t, char2):
    raw = c * t // 2 if (char2 or t % 2 == 0) else c * t
    return min(raw, comb(c, 2))

def intra_floor(B):
    """smallest s with s(s-1)/2 >= B: any part must be at least this big to carry
    an intra-orbital of size B at all."""
    s = 1
    while s * (s - 1) // 2 < B:
        s += 1
    return s

def single_part_ok(L, B, p, q, r):
    """Can L be ONE admissible part whose own intra term reaches B?  F' must be a
    power of q, c' = L/F' a prime power, and c' either p-characteristic (a power
    of the bottom prime p, twist optimistically full) or a foreign prime distinct
    from r and from p (twist a q-power, by Lemma B')."""
    F = 1
    while F <= L:
        if L % F == 0:
            c2 = L // F
            pp = prime_power(c2)
            if pp:
                if pp[0] == p:                       # p-characteristic
                    if F * comb(c2, 2) >= B:
                        return True
                elif pp[1] == 1 and c2 != r:         # foreign prime
                    if F == 1 and orb(c2, qpart(c2 - 1, q), False) >= B:
                        return True
        F *= q
        if q == 1:
            break
    return False

def prime_divisors(x):
    out = []
    while x > 1:
        p = spf[x]; out.append(p)
        while x % p == 0:
            x //= p
    return out

# prime powers up to NMAX, grouped for a quick scan
PP = [c for c in range(2, NMAX + 1) if prime_power(c)]

def witnesses(n, B):
    """All (p, q, F, c, r) satisfying the necessary conditions (1)-(6)."""
    found = []
    for c in PP:
        if c + 2 > n:
            break
        p, _ = prime_power(c)
        # (3) with F*c <= n - r <= n - 2  =>  need C(c,2)*floor((n-2)/c) >= B at best
        for r in prime_divisors(c - 1):
            if r == p or not is_prime(r):
                continue
            if c + r > n:
                continue
            # F ranges over q-powers with F*c + r <= n
            Fmax = (n - r) // c
            if Fmax < 1:
                continue
            for q in range(2, n + 1):
                if not is_prime(q):
                    continue
                t = qpart(r - 1, q)
                if orb(r, t, False) < B:            # (4)
                    continue
                F = 1
                while F <= Fmax:
                    ok = (F * comb(c, 2) >= B and      # (3)
                          F * c * r >= B and           # (5)
                          (F == 1 or
                           (F if q % 2 else F // 2) * c * c >= B))      # (6)
                    if ok:                             # (7)-(8): the leftover
                        L = n - F * c - r
                        if L != 0:
                            need = max(-(-B // min(F * c, r)), intra_floor(B))
                            if L < need:
                                ok = False
                            elif L < 2 * need:
                                # exactly one further part: L = F'*c' with F' a
                                # q-power and c' a prime power, and that part must
                                # itself carry an intra-orbital of size >= B
                                ok = single_part_ok(L, B, p, q, r)
                            else:
                                inconclusive.add(n)
                    if ok:
                        found.append((p, q, F, c, r, (c - 1) // r,
                                      n - F * c - r))
                        break
                    F *= q
                if found and not a.verbose:
                    return found
    return found

# ---- the delta > 1/9 theorem (Part J item 2), reported alongside the search ----
MERSENNE = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127]

def largest_pp_divisor(x):
    best, d, y = 1, 2, x
    while d * d <= y:
        if y % d == 0:
            e = 1
            while y % d == 0:
                y //= d; e += 1
            best = max(best, d ** (e - 1))
        d += 1
    return max(best, y) if y > 1 else best

CAP = {}
for _a in MERSENNE:
    _M = 2 ** (_a - 1) - 1
    CAP[_a] = (2 ** _a - 1) * max(2, largest_pp_divisor(_M) if _M > 1 else 1)

def theorem_covers(n, B):
    """True if the delta > 1/9 theorem settles this n outright, i.e. s = 1 is
    forced and both s = 1 branches are excluded.  The p-odd branch gives a
    foreign block of size 2, one pair, score <= 1.  The p = 2 branch is capped by
    Cap(a) for each Mersenne exponent a with 2^(a+1)-1 <= n, and Cap(a) <=
    (2^a-1)(2^((a-1)/2)+1) = O(n^{3/2})."""
    d = B / comb(n, 2)
    if d <= (n - 1) / (9 * n):
        return False, "delta <= ~1/9: s <= 2 or 3 survives"
    for a, cap in CAP.items():
        if 2 ** (a + 1) - 1 <= n and cap >= B:
            return False, f"Mersenne a={a}: Cap={cap} >= B={B}"
    return True, "delta > 1/9 and every Cap(a) < B(n)"

bad, smax, checked = [], 0, 0
inconclusive = set()
covered, uncovered = 0, []
for row in rows:
    n = int(row["n"]); B = int(row["mu_bound"])
    w = witnesses(n, B)
    checked += 1
    ok, why = theorem_covers(n, B)
    if ok:
        covered += 1
    else:
        uncovered.append((n, why))
    if w:
        bad.append((n, B, float(row["density"]), w[:4]))
    # record the proved bound on s for the record
    d = B / comb(n, 2)
    smax = max(smax, (1 - d ** 0.5) / d ** 0.5)

print(f"{a.table}: {checked} values of n checked, n up to {NMAX}")
print(f"values where SOME fallback configuration could reach B(n): {len(bad)}")
for n, B, d, w in bad[:20]:
    print(f"   n={n} B={B} density={d:.4f}  candidates (p,q,F,c,r,s,leftover): {w}")
print()
print()
print(f"settled by the delta > 1/9 theorem alone (no search needed): "
      f"{covered} of {checked} ({100*covered/checked:.1f}%)")
print(f"relying on the exhaustive search: {len(uncovered)}")
_r = {}
for _n, _w in uncovered:
    _r[_w.split(':')[0]] = _r.get(_w.split(':')[0], 0) + 1
for k, v in sorted(_r.items(), key=lambda t: -t[1]):
    print(f"    {v:5d}  {k}")
print()
print(f"largest permitted s = (c-1)/r over the range: {smax:.2f}  "
      f"(so s <= {int(smax)} everywhere here)")
print(f"values where the leftover could be 2+ parts (check not exhaustive there): "
      f"{len(inconclusive)}"
      + (f" -> {sorted(inconclusive)[:15]}" if inconclusive else ""))
if not bad:
    print()
    print("CERTIFIED.  At every n in this table, no admissible configuration that")
    print("invokes the unconditional fallback can attain B(n).  The SAFE optimum is")
    print("therefore fallback-free independently of tie-breaking, the Part E")
    print("construction realises it, and mu(n) = B(n) is proved at each of these n")
    print("-- upgrading Part J item 2's 'empirically 0 of N' to a checked statement")
    print("about all configurations rather than about the reported witness.")
sys.exit(1 if bad else 0)
