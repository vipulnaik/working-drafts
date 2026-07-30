#!/usr/bin/env python3
"""
fb_common.py -- shared machinery for the two fallback-collapse certificates.

`fallback_cert.py` runs against the true B(n) from the computed table;
`wide_cert.py` runs against a proven lower bound B_lo(n) and so reaches much
further.  Both ask the same question and enforce the same necessary conditions,
so those live here once.

THE QUESTION.  A "fallback configuration" contains a p-characteristic part
(F, c) and a foreign prime r of the same configuration with r | c-1, so that
Lemma C strictly reduces the c-twist and SAFE scoring assigns F*C(c,2) where
the Part E construction reaches only F*orb(c, d).  If such a configuration
attains B_safe(n), the sandwich B_refined <= mu <= B_safe fails to collapse at
that n.  Certifying that none can attain it proves mu(n) = B(n).

SOUNDNESS RULE, obeyed everywhere below: every test is a NECESSARY condition on
such a configuration, and every over-approximation errs permissive.  A candidate
that survives may be spurious; a real one is never discarded.  In particular the
certificate is sound against any B <= B_safe(n), which is what lets wide_cert.py
substitute a lower bound.
"""
from math import comb, isqrt

# ---------------------------------------------------------------- arithmetic

def sieve_spf(N):
    spf = list(range(N + 2))
    i = 2
    while i * i <= N + 1:
        if spf[i] == i:
            for j in range(i * i, N + 2, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    return spf

class Arith:
    """Smallest-prime-factor arithmetic, shared by both certificates."""
    def __init__(self, N):
        self.N = N
        self.spf = sieve_spf(N)

    def is_prime(self, x):
        return x > 1 and self.spf[x] == x

    def prime_power(self, x):
        """(p, e) if x = p^e with e >= 1, else None."""
        if x < 2:
            return None
        p = self.spf[x]; e = 0
        while x % p == 0:
            x //= p; e += 1
        return (p, e) if x == 1 else None

    def prime_divisors(self, x):
        """Distinct prime divisors.  Uses the sieve when x is in range, and
        falls back to trial division otherwise (the theorem caps below factor
        numbers larger than the sieve, but only for pairs that fit in range,
        so the fallback is never called on anything unfactorable in practice)."""
        if x <= self.N:
            out = []
            while x > 1:
                p = self.spf[x]; out.append(p)
                while x % p == 0:
                    x //= p
            return out
        out, d = [], 2
        while d * d <= x:
            if x % d == 0:
                out.append(d)
                while x % d == 0:
                    x //= d
            d += 1 if d == 2 else 2
        if x > 1:
            out.append(x)
        return out

    def largest_pp_divisor(self, x):
        best = 1
        for p in self.prime_divisors(x):
            e = 1
            while x % (p ** (e + 1)) == 0:
                e += 1
            best = max(best, p ** e)
        return best

def qpart(x, q):
    t = 1
    while x % (t * q) == 0:
        t *= q
    return t

def orb(c, t):
    """Minimum intra-orbital of a c-block with cyclic twist of order t, capped
    at C(c,2).  The cap matters: it is what makes a 2-block worth 1, not 2."""
    return min(c * t // 2 if t % 2 == 0 else c * t, comb(c, 2))

def foreign_cap(A, r):
    """Max over top primes q of orb(r, q-part of r-1), including the q | r-1
    failing case where the twist is trivial and the block is worth r."""
    if r <= 2:
        return 1
    return max([r] + [orb(r, qpart(r - 1, q)) for q in set(A.prime_divisors(r - 1))])

# ------------------------------------------------- theorems of Part E-prime

MERSENNE = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607]
REPUNIT3 = [3, 7, 13, 71, 103, 541]          # a with (3^a-1)/2 prime

def cap_mersenne(A, nmax=None):
    """Theorem E.1, p = 2 branch: s = 1 forces c = 2^a, r = 2^a - 1 Mersenne,
    and SAFE <= (2^a - 1) * max(2, L(a)) with L(a) the largest prime-power
    divisor of 2^(a-1) - 1.  Lemma E.2 bounds L(a) <= 2^((a-1)/2) + 1."""
    out = {}
    nmax = nmax if nmax is not None else A.N
    for a in MERSENNE:
        if 2 ** (a + 1) - 1 > nmax:      # pair cannot fit at any n <= nmax
            break
        M = 2 ** (a - 1) - 1
        out[a] = (2 ** a - 1) * max(2, A.largest_pp_divisor(M) if M > 1 else 1)
    return out

def cap_repunit(A, nmax=None):
    """Theorem E.3(iii), s = 2 with a >= 2: forces p = 3 and r = (3^a - 1)/2 a
    base-3 repunit prime, with the foreign block's SAFE score capped by
    Cap'(a) = max over q of orb(r, q-part of r-1) = O(r^{3/2})."""
    out = {}
    nmax = nmax if nmax is not None else A.N
    for a in REPUNIT3:
        c = 3 ** a
        r = (c - 1) // 2
        if c + r > nmax:                 # pair cannot fit at any n <= nmax
            break
        out[a] = (c, r, max([orb(r, qpart(r - 1, q))
                             for q in set(A.prime_divisors(r - 1))] + [r]))
    return out

E4_PAIR = (16, 5)        # Theorem E.4: the entire s = 3 branch
E4_CAP = 10              # its absolute SAFE ceiling, orb(5, 4)

def s_max(n, B):
    """Largest s = (c-1)/r a fallback configuration can have at this n, from
    r^2 > delta*n(n-1) and c <= n - r (Part E-prime).  Returns floor."""
    d = B / comb(n, 2)
    return max(1, int(1 / d ** 0.5 - 1 + 1e-12))

def branch_settled(A, n, B, s, caps_m, caps_r):
    """Is the s-branch at this n settled by theorem alone?  Returns
    (True, reason) or (False, reason)."""
    if s == 1:
        for a, cap in caps_m.items():
            if 2 ** (a + 1) - 1 <= n and cap >= B:
                return False, f"E.1 Mersenne a={a}: Cap={cap} >= B"
        return True, "E.1 (r=2 branch worth 1; Mersenne caps all below B)"
    if s == 2:
        # a >= 2 repunit branch: capped
        for a, (c, r, cap) in caps_r.items():
            if c + r <= n and cap >= B:
                return False, f"E.3(iii) repunit a={a}: Cap'={cap} >= B"
        # a = 1 safe-prime branch: pairwise domination only, not global
        return False, "E.3(ii) is pairwise only; global promotion open"
    if s == 3:
        c, r = E4_PAIR
        if c + r <= n and E4_CAP >= B:
            return False, f"E.4 pair {E4_PAIR}: cap {E4_CAP} >= B"
        return True, "E.4 (branch is the single pair (16,5), cap 10)"
    return False, f"s={s} has no theorem"

def theorem_report(A, n, B, caps_m, caps_r):
    """Per-n theorem coverage: (fully_settled, s_max, {s: (ok, reason)})."""
    sm = s_max(n, B)
    per = {s: branch_settled(A, n, B, s, caps_m, caps_r) for s in range(1, sm + 1)}
    return all(ok for ok, _ in per.values()), sm, per

# --------------------------------------------- necessary conditions (1)-(8)

def intra_floor(B):
    """Smallest part size that can carry an intra-orbital of size B at all,
    i.e. least s with C(s,2) >= B.  Closed form via isqrt -- the obvious
    increment-by-one loop costs O(sqrt(B)) and this runs in the inner loop of
    both certificates, where B can be 10^8."""
    if B <= 0:
        return 1
    s = (1 + isqrt(1 + 8 * B)) // 2
    while s * (s - 1) // 2 < B:
        s += 1
    while s > 1 and (s - 1) * (s - 2) // 2 >= B:
        s -= 1
    return s

def single_part_ok(A, L, B, p, q, r):
    """Can the leftover L be ONE admissible part whose own intra term reaches B?
    q may be '*' for the generic branch, over-approximated permissively."""
    Fs = ([f for f in range(1, L + 1) if L % f == 0] if q == '*'
          else [q ** i for i in range(64) if q ** i <= L])
    for F in Fs:
        if L % F:
            continue
        c2 = L // F
        pp = A.prime_power(c2)
        if not pp:
            continue
        if pp[0] == p:
            if F * comb(c2, 2) >= B:
                return True
        elif pp[1] == 1 and c2 != r:
            capf = foreign_cap(A, c2) if q == '*' else orb(c2, qpart(c2 - 1, q))
            if F == 1 and capf >= B:
                return True
    return False

def multi_part_ok(A, L, B, p, q, r, limit=60):
    """Can L split into two or more admissible parts, each meeting the necessary
    floors?  Exact-sum reachability over: foreign primes r_j != r whose own cap
    reaches B (distinct, so subset sums), and p-characteristic sizes F'*p^j with
    F'*C(p^j,2) >= B (repeats allowed, so unbounded sums).  Necessary conditions
    only, hence permissive.  Returns True/False, or None if the candidate set is
    too large to enumerate (treated as surviving by callers)."""
    fcands = []
    for rj in range(3, L + 1, 2):
        if not A.is_prime(rj) or rj == r:
            continue
        capj = foreign_cap(A, rj) if q == '*' else orb(rj, qpart(rj - 1, q))
        if capj >= B:
            fcands.append(rj)
    pcands = []
    cj = p
    while cj <= L:
        F = 1
        while F * cj <= L:
            if F * comb(cj, 2) >= B:
                pcands.append(F * cj)
            if q == '*':
                break
            F *= q
        cj *= p
    if len(fcands) + len(pcands) > limit:
        return None
    reach = {0}
    for x in fcands:
        reach |= {v + x for v in reach if v + x <= L}
    for x in pcands:
        growing = True
        while growing:
            add = {v + x for v in reach if v + x <= L} - reach
            reach |= add
            growing = bool(add)
    return L in reach

def leftover_ok(A, L, B, p, q, r, Fc):
    """Conditions (7)-(8) on the leftover L = n - F*c - r.  True if L could be
    made of admissible parts, False if provably not, None if inconclusive."""
    if L == 0:
        return True
    need = max(-(-B // min(Fc, r)), intra_floor(B))
    if L < need:
        return False
    if L < 2 * need:
        return single_part_ok(A, L, B, p, q, r)
    if single_part_ok(A, L, B, p, q, r):
        return True
    return multi_part_ok(A, L, B, p, q, r)

def e3ii_resolves(A, n, c, r, F, L):
    """Theorem E.3(ii), applied as a RESOLUTION rather than a mere domination.

    When the whole configuration is the bare pair -- F = 1 and leftover L = 0,
    so n = c + r with c = 2r + 1 a safe prime -- the (p, q) = (r, r) re-reading
    of the same n is a different admissible configuration, namely the r-block
    p-characteristic at full twist plus the c-block foreign.  Three facts make
    that a proof of collapse at this n rather than a heuristic:

      * it scores min(C(c,2), C(r,2), cr), and the fallback reading scores
        min(C(c,2), orb(r,t), cr) with orb(r,t) <= C(r,2), so the re-reading
        scores at least as much;
      * it is itself FALLBACK-FREE -- the only foreign prime is c, the p-part is
        r, and c = 2r + 1 > r - 1 cannot divide r - 1 -- so its SAFE and REFINED
        scores coincide;
      * hence if the fallback reading attained B_safe(n), so does the re-reading,
        giving B_refined(n) >= B_safe(n) and therefore equality.

    This does NOT extend to L > 0.  With a leftover the re-reading must also
    re-type the leftover parts, and the commonest case L = c fails outright: two
    blocks of the same prime c would be two equal foreign parts, which Part E
    forbids (they would place C_c x C_c in the cyclic layer), and fusing them is
    forbidden too.  Those cases stay open -- Part J item 2."""
    return F == 1 and L == 0 and c == 2 * r + 1 and A.is_prime(c)

def pair_candidates(A, n, B, c, r, p, skip_settled=None):
    """All (p, q, F, c, r) meeting conditions (1)-(8) for this (c, r) at this n.
    `skip_settled` is an optional set of s values already settled by theorem."""
    out = []
    if (c - 1) % r or c + r > n:
        return out
    s = (c - 1) // r
    if skip_settled and s in skip_settled:
        return out
    qopts = list(set(A.prime_divisors(r - 1)))
    if r >= B:
        qopts.append('*')                  # trivial-twist generic branch
    Fmax = (n - r) // c
    for q in qopts:
        t = 1 if q == '*' else qpart(r - 1, q)
        if orb(r, t) < B:
            continue
        F = 1
        while F <= Fmax:
            ok = (F * comb(c, 2) >= B and F * c * r >= B and
                  (F == 1 or (F if q == '*' or q % 2 else F // 2) * c * c >= B))
            if ok:
                lo = leftover_ok(A, n - F * c - r, B, p, q, r, F * c)
                if lo is False:
                    ok = False
                elif lo is None:
                    out.append((p, q, F, c, r, s, 'INCONCLUSIVE-LEFTOVER'))
                    break
            if ok:
                L = n - F * c - r
                if e3ii_resolves(A, n, c, r, F, L):
                    break                       # dominated by the (r,r) re-reading
                out.append((p, q, F, c, r, s, L))
                break
            if q == '*':
                break
            F *= q
    return out
