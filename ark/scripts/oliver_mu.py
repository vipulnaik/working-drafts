"""
mu(n) via template Oliver groups, and the counterexample constraint it forces.

Framework (BBKN / our notes):
  - We build permutation groups Gamma on [n] satisfying Oliver's condition
    (p-group <| cyclic <| q-group chain), from affine building blocks:
      * a "bottom" layer: k >= 1 copies of AGL(1, p^a)-type blocks over one
        prime p, with a common diagonal multiplicative twist of order d | p^a - 1
        (the twist lives in the middle cyclic layer),
      * "middle" blocks: distinct primes r_j (their translation groups join the
        middle cyclic layer; must be pairwise coprime with each other and d),
      * "top" twists: on each middle block r_j, a multiplicative twist of order
        q^{e_j} (largest power of one common prime q dividing r_j - 1); these
        form the top q-group.
  - For each such Gamma we compute m*(Gamma): the minimum size of an orbit of
    Gamma acting on unordered pairs of [n] (u-orbitals), by explicit BFS.
  - mu_template(n) = max over enumerated Gamma of m*(Gamma).

Constraint derived (the "Engstrom-style" flip): if P is a non-evasive
nontrivial monotone property at n, then for EVERY Oliver Gamma the fixed-point
complex of P is nonempty (chi = 1 mod q), i.e. P contains a nonempty union of
u-orbitals of Gamma, hence a graph with >= m*(Gamma) edges. Therefore
    dim(P) + 1 >= mu(n) >= mu_template(n).
The program reports mu_template(n) / C(n,2): the forced edge-density of any
counterexample to ARK at that n, as certified by the template family.

Everything is verified by brute force: group elements are generated from
explicit permutation generators; orbit computations are exact.
"""

from itertools import combinations
from math import comb
from functools import lru_cache

# ---------------------------------------------------------------- utilities

def is_prime(m):
    if m < 2: return False
    if m < 4: return True
    if m % 2 == 0: return False
    f = 3
    while f * f <= m:
        if m % f == 0: return False
        f += 2
    return True

def prime_power(m):
    """Return (p, a) if m = p^a with p prime, else None."""
    if m < 2: return None
    for p in range(2, m + 1):
        if p * p > m:
            return (m, 1) if is_prime(m) else None
        if m % p == 0:
            a, t = 0, m
            while t % p == 0:
                t //= p; a += 1
            return (p, a) if t == 1 else None
    return None

def divisors(m):
    return [d for d in range(1, m + 1) if m % d == 0]

# ------------------------------------------------- finite field GF(p^a)

@lru_cache(maxsize=None)
def gf(p, a):
    """
    Return (elements, add, mul) for GF(p^a); elements are ints 0..p^a-1
    encoding polynomial coefficients base p. add/mul are dicts keyed by pairs.
    Brute-force search for an irreducible monic polynomial of degree a.
    """
    q = p ** a
    if a == 1:
        add = {(x, y): (x + y) % p for x in range(p) for y in range(p)}
        mul = {(x, y): (x * y) % p for x in range(p) for y in range(p)}
        return tuple(range(q)), add, mul

    def to_poly(x):
        c = []
        for _ in range(a):
            c.append(x % p); x //= p
        return c  # low-degree first, length a

    def from_poly(c):
        x = 0
        for coef in reversed(c):
            x = x * p + (coef % p)
        return x

    def poly_mul_mod(u, v, modpoly):
        # u, v coefficient lists (low first); modpoly monic of degree a
        res = [0] * (len(u) + len(v) - 1)
        for i, cu in enumerate(u):
            if cu:
                for j, cv in enumerate(v):
                    res[i + j] = (res[i + j] + cu * cv) % p
        # reduce
        for i in range(len(res) - 1, a - 1, -1):
            c = res[i]
            if c:
                # subtract c * x^{i-a} * modpoly
                for j in range(a + 1):
                    res[i - a + j] = (res[i - a + j] - c * modpoly[j]) % p
        return res[:a] + [0] * max(0, a - len(res))

    def is_irreducible(modpoly):
        # modpoly monic degree a, low-first, length a+1
        # check x^{p^a} = x and gcd conditions via brute: no roots for a<=3 is
        # insufficient for a>3; use: polynomial has no divisor of degree <= a//2.
        # Brute-force trial division by all monic polys of degree 1..a//2.
        def polydivmod_check(divpoly):
            # returns True if divpoly divides modpoly
            rem = list(modpoly)
            da, db = a, len(divpoly) - 1
            inv_lead = pow(divpoly[-1], p - 2, p)  # leading coeff inverse (monic anyway)
            for i in range(da - db, -1, -1):
                c = rem[i + db] * inv_lead % p
                if c:
                    for j in range(db + 1):
                        rem[i + j] = (rem[i + j] - c * divpoly[j]) % p
            return all(x == 0 for x in rem[:db])  # remainder degree < db
        for deg in range(1, a // 2 + 1):
            for mask in range(p ** deg):
                dp = to_poly(mask)[:deg] + [1]
                if polydivmod_check(dp):
                    return False
        return True

    modpoly = None
    for mask in range(q):
        cand = to_poly(mask)[:a] + [1]  # monic degree a
        if is_irreducible(cand):
            modpoly = cand
            break
    assert modpoly is not None

    add = {}
    mul = {}
    polys = {x: to_poly(x) for x in range(q)}
    for x in range(q):
        for y in range(q):
            add[(x, y)] = from_poly([(polys[x][i] + polys[y][i]) % p for i in range(a)])
            mul[(x, y)] = from_poly(poly_mul_mod(polys[x], polys[y], modpoly))
    return tuple(range(q)), add, mul

def gf_generator(p, a):
    """A generator g of GF(p^a)^* (cyclic of order p^a - 1)."""
    q = p ** a
    _, _, mul = gf(p, a)
    for g in range(2, q):
        x, order = g, 1
        while x != 1:
            x = mul[(x, g)]
            order += 1
            if order > q: break
        if order == q - 1:
            return g
    raise RuntimeError("no generator found")

def gf_element_of_order(p, a, d):
    """Element of multiplicative order exactly d in GF(p^a)^* (d | p^a - 1)."""
    q = p ** a
    assert (q - 1) % d == 0
    _, _, mul = gf(p, a)
    g = gf_generator(p, a)
    # g^((q-1)/d)
    e = (q - 1) // d
    x = 1
    for _ in range(e):
        x = mul[(x, g)]
    return x

# ------------------------------------------------- group construction

class TemplateGroup:
    """
    Gamma on [n] from:
      bottom: k copies of block GF(p^a), each with independent translations,
              plus ONE diagonal multiplicative twist of order d | p^a - 1,
              plus (optional) a cyclic rotation of the k copies of prime order s
              (s must be prime, k % s == 0 pattern: we only rotate when k == s
               for simplicity, acting as an s-cycle on the blocks).
      middle blocks: distinct primes r_1..r_t (translations),
      top: on block r_j, a twist of order q^{e_j} (common prime q).
    Oliver-condition checks (by design + verified coprimality):
      bottom p-group = translations of the p^a-blocks;
      middle cyclic  = <diagonal twist (order d)> x prod Z_{r_j} x <rotation Z_s>
                       -- cyclic iff d, r_1..r_t, s pairwise coprime;
      top q-group    = prod of the q-power twists.
    """
    def __init__(self, n, p=None, a=1, k=0, d=1, s=1, middle=()):
        # middle: tuple of (r_j, q, e_j)
        self.n = n
        self.desc_parts = []
        self.generators = []   # list of tuples: perm[i] = image of i
        offset = 0

        # --- bottom blocks
        self.valid = True
        if k > 0:
            q0 = p ** a
            elems, add, mul = gf(p, a)
            blocks = [list(range(offset + i * q0, offset + (i + 1) * q0)) for i in range(k)]
            offset += k * q0
            # translations: for each block, one generator per additive generator
            # (the additive group is generated by translations by basis elems;
            #  we add translation-by-x for x in a generating set: powers of p base)
            basis = [p ** 0]
            for i in range(1, a):
                basis.append(p ** i)  # encoding: these are the "x^i" coefficients
            for b in blocks:
                for x in basis:
                    perm = list(range(n))
                    for idx, e in enumerate(elems):
                        perm[b[e]] = b[add[(e, x)]]
                    self.generators.append(tuple(perm))
            # diagonal twist of order d
            if d > 1:
                if (q0 - 1) % d != 0:
                    self.valid = False
                else:
                    w = gf_element_of_order(p, a, d)
                    perm = list(range(n))
                    for b in blocks:
                        for e in elems:
                            perm[b[e]] = b[mul[(e, w)]]
                    self.generators.append(tuple(perm))
            # rotation of blocks (only when k == s, s prime, s > 1)
            if s > 1:
                if k != s or not is_prime(s):
                    self.valid = False
                else:
                    perm = list(range(n))
                    for i in range(k):
                        src, dst = blocks[i], blocks[(i + 1) % k]
                        for e in elems:
                            perm[src[e]] = dst[e]
                    self.generators.append(tuple(perm))
            self.desc_parts.append(f"{k}xAGL-ish(1,{q0})[d={d}" + (f",rot={s}" if s > 1 else "") + "]")

        # --- middle blocks
        mid_orders = []
        for (r, qq, e) in middle:
            block = list(range(offset, offset + r))
            offset += r
            # translation
            perm = list(range(n))
            for x in range(r):
                perm[block[x]] = block[(x + 1) % r]
            self.generators.append(tuple(perm))
            # twist of order qq^e
            tw = qq ** e
            if tw > 1:
                if (r - 1) % tw != 0:
                    self.valid = False
                else:
                    w = gf_element_of_order(r, 1, tw)
                    perm = list(range(n))
                    for x in range(r):
                        perm[block[x]] = block[(x * w) % r]
                    self.generators.append(tuple(perm))
            mid_orders.append(r)
            self.desc_parts.append(f"F{r}:C{tw}")

        if offset != n:
            self.valid = False

        # --- Oliver coprimality for the middle cyclic layer
        middle_cyclic_factors = [x for x in ([d] if d > 1 else []) + mid_orders + ([s] if s > 1 else []) if x > 1]
        for i in range(len(middle_cyclic_factors)):
            for j in range(i + 1, len(middle_cyclic_factors)):
                from math import gcd
                if gcd(middle_cyclic_factors[i], middle_cyclic_factors[j]) != 1:
                    self.valid = False
        # common top prime q
        qs = {qq for (r, qq, e) in middle if e > 0 and qq ** e > 1}
        if len(qs) > 1:
            self.valid = False
        # bottom prime distinct from middle content is automatic by block disjointness;
        # also need gcd(p, each middle factor) fine automatically (p acts on bottom only).

    def description(self):
        return " x ".join(self.desc_parts) if self.desc_parts else "trivial"

    def min_u_orbital(self):
        """Exact minimum u-orbital size via BFS over pairs."""
        n = self.n
        gens = self.generators
        pairs = list(combinations(range(n), 2))
        pair_index = {pr: i for i, pr in enumerate(pairs)}
        seen = [False] * len(pairs)
        m_star = None
        for start_i, start in enumerate(pairs):
            if seen[start_i]:
                continue
            # BFS
            frontier = [start]
            seen[start_i] = True
            size = 1
            while frontier:
                new_frontier = []
                for (u, v) in frontier:
                    for g in gens:
                        a2, b2 = g[u], g[v]
                        pr = (a2, b2) if a2 < b2 else (b2, a2)
                        i2 = pair_index[pr]
                        if not seen[i2]:
                            seen[i2] = True
                            size += 1
                            new_frontier.append(pr)
                frontier = new_frontier
            m_star = size if m_star is None else min(m_star, size)
        return m_star

# ------------------------------------------------- enumeration per n

def candidate_groups(n, max_middle=3):
    """Enumerate template groups on [n]. Yields TemplateGroup objects (valid ones)."""
    from math import gcd
    results = []

    # partitions: choose bottom (p, a, k) with k*p^a <= n, then middle distinct primes summing to remainder
    pps = [(m, prime_power(m)) for m in range(2, n + 1)]
    pps = [(m, pa) for (m, pa) in pps if pa]

    def middle_choices(remainder, max_parts):
        """Yield tuples of distinct primes summing to remainder, up to max_parts."""
        primes = [m for m in range(2, remainder + 1) if is_prime(m)]
        out = []
        def rec(rem, start, acc):
            if rem == 0:
                out.append(tuple(acc)); return
            if len(acc) == max_parts: return
            for i in range(start, len(primes)):
                r = primes[i]
                if r > rem: break
                rec(rem - r, i + 1, acc + [r])
        rec(remainder, 0, [])
        return out

    # Case A: with a bottom layer
    for (blocksize, (p, a)) in pps:
        for k in range(1, n // blocksize + 1):
            rem = n - k * blocksize
            for mids in middle_choices(rem, max_middle):
                # skip if any middle prime equals p and would collide? distinct domains, fine,
                # but middle translations must be coprime to each other: distinct primes ok;
                # d chosen below must be coprime to all mids.
                dcands = sorted(divisors(blocksize - 1), reverse=True)
                # rotation only when k is prime and rotating all k blocks
                s_options = [1] + ([k] if (k > 1 and is_prime(k)) else [])
                for s in s_options:
                    for d in dcands:
                        if any(gcd(d, r) != 1 for r in mids):
                            continue
                        if s > 1 and (gcd(d, s) != 1 or any(gcd(s, r) != 1 for r in mids)):
                            continue
                        # top twists: choose common q maximizing per-block q-part of r-1
                        best = None
                        qset = set()
                        for r in mids:
                            for qq in range(2, r):
                                if is_prime(qq) and (r - 1) % qq == 0:
                                    qset.add(qq)
                        qset.add(2)
                        for qq in qset:
                            middle = []
                            for r in mids:
                                e = 0
                                while (r - 1) % (qq ** (e + 1)) == 0:
                                    e += 1
                                middle.append((r, qq, e))
                            g = TemplateGroup(n, p=p, a=a, k=k, d=d, s=s, middle=tuple(middle))
                            if g.valid:
                                results.append(g)
                        break  # only the largest valid d (smaller d only shrinks orbitals)
    # Case B: no bottom layer -- pick one middle block to serve as bottom instead:
    # i.e. one prime block r0 with FULL twist r0-1 (AGL(1,r0)), rest q-twisted.
    for mids_all in middle_choices(n, max_middle + 1):
        for r0 in mids_all:
            rest = tuple(r for r in mids_all if r != r0)
            from math import gcd
            d = r0 - 1
            if any(gcd(d, r) != 1 for r in rest):
                # try largest divisor of r0-1 coprime to rest
                dc = [dd for dd in sorted(divisors(r0 - 1), reverse=True)
                      if all(gcd(dd, r) == 1 for r in rest)]
                d = dc[0] if dc else 1
            qset = {2}
            for r in rest:
                for qq in range(2, r):
                    if is_prime(qq) and (r - 1) % qq == 0:
                        qset.add(qq)
            for qq in qset:
                middle = []
                ok = True
                for r in rest:
                    e = 0
                    while (r - 1) % (qq ** (e + 1)) == 0:
                        e += 1
                    middle.append((r, qq, e))
                g = TemplateGroup(n, p=r0, a=1, k=1, d=d, s=1, middle=tuple(middle))
                if g.valid:
                    results.append(g)
    return results

def analyze(n, verbose_top=3):
    N = comb(n, 2)
    pa = prime_power(n)
    header = f"n = {n}   (C(n,2) = {N})" + ("   [prime power: KSS applies directly]" if pa else "")
    print("=" * len(header)); print(header); print("=" * len(header))
    groups = candidate_groups(n)
    scored = []
    for g in groups:
        m = g.min_u_orbital()
        scored.append((m, g.description()))
    scored.sort(reverse=True)
    # deduplicate descriptions
    seen, top = set(), []
    for m, desc in scored:
        if desc not in seen:
            seen.add(desc); top.append((m, desc))
    mu = top[0][0] if top else 0
    print(f"  template groups tried: {len(groups)}   mu_template(n) = {mu}"
          f"   density forced on any ARK counterexample: {mu}/{N} = {mu/N:.3f}")
    for m, desc in top[:verbose_top]:
        print(f"    m* = {m:4d}   Gamma = {desc}")
    print(f"  ==> any non-evasive nontrivial monotone property at n={n} must contain")
    print(f"      a graph with >= {mu} edges invariant under EACH listed extremal group.")
    print()
    return mu, N

if __name__ == "__main__":
    for n in [6, 10, 12, 15, 18, 21, 22, 26]:
        analyze(n)
