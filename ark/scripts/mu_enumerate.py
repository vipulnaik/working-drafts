#!/usr/bin/env python3
"""
mu_enumerate.py -- the general configuration enumeration of enumeration-proof.md
Part G.3, with the self-certifying termination of Part F.

A configuration on n points is

    n = sum_i  F_i * c_i        (i = 1..k orbits)

  * F_i is a power of the top prime q      (fusion count; tower depth is absorbed
                                            entirely into F_i, by Part G.2)
  * c_i is a prime power                   (finest-block size)
  * each c_i is either p-characteristic (a power of the bottom prime p, twist any
    divisor of c_i - 1) or FOREIGN (a prime != p, twist a q-power, by Lemma B')
  * Lemma C: a p-characteristic twist must be coprime to every foreign prime

Orbital sizes:
    intra orbit i          F_i * orb(c_i, d_i)
    within orbit i (F_i>1) (F_i if q odd else F_i/2) * c_i^2
    between orbits i, j    at most s_i * s_j,  s_i = F_i * c_i

and m*(config) is the minimum of these.  B(n) is the max over configurations.

Search bounds (Parts F and G.4), all free of number-theoretic input.  With
delta = B(n) / C(n,2):
    k     <= 1/sqrt(delta)          number of orbits
    c_i   >= delta * n              finest-block size
    F_i   <= 1/delta                fusion count
The iteration over K = 1, 2, ... halts at the first K with 1/sqrt(delta_K) <= K,
at which point B_K = B is certified.

Usage:
    python3 mu_enumerate.py --n 273
    python3 mu_enumerate.py --nmax 400 [--check mu_table_full.csv]
"""
import argparse, csv, os, sys, time
from collections import deque
from math import comb, isqrt


# ---------------------------------------------------------------- arithmetic
def sieve_spf(N):
    spf = list(range(N + 1))
    i = 2
    while i * i <= N:
        if spf[i] == i:
            for j in range(i * i, N + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    return spf


def is_prime(x, spf):
    return x > 1 and spf[x] == x


def prime_power(x, spf):
    """return (p, a) if x = p^a with a >= 1, else None"""
    if x < 2:
        return None
    p = spf[x]
    a = 0
    while x % p == 0:
        x //= p
        a += 1
    return (p, a) if x == 1 else None


def divisors(x):
    d = []
    i = 1
    while i * i <= x:
        if x % i == 0:
            d.append(i)
            if i != x // i:
                d.append(x // i)
        i += 1
    return sorted(d)


def qpart(x, q):
    t = 1
    while x % (t * q) == 0:
        t *= q
    return t


def strip(x, primes):
    for p in primes:
        while x % p == 0:
            x //= p
    return x


def orb(c, t, char2):
    """intra-block orbital size: pairs whose difference lies in +/- delta*T.
    |+/-dT| = |T| when -1 is in T (always in characteristic 2, else iff |T| even),
    otherwise 2|T|; the orbital has c * |+/-dT| / 2 pairs."""
    return c * t // 2 if (char2 or t % 2 == 0) else c * t



# ---------------------------------------------------------------- fast seed
def seed_value(n, spf):
    """A quick lower bound from the families that are cheap to evaluate.  Only
    used to prime the pruning: correctness never depends on it, but a good seed
    shrinks the admissible part pool enormously (a part needs F*C(c,2) > best and
    F*c <= n, hence c > 2*best/n + 1)."""
    best = 0
    pps = [c for c in range(2, n + 1) if prime_power(c, spf)]
    # fused blocks: n = F*c with F a prime power, c a prime power
    for F in range(2, n + 1):
        if n % F or not prime_power(F, spf):
            continue
        c = n // F
        if prime_power(c, spf):
            best = max(best, F * c * (c - 1) // 2)
    for c in pps:                                   # single orbit
        if c == n:
            best = max(best, comb(n, 2))
    # two parts: p-power + foreign prime, and two p-powers
    for a in pps:
        b = n - a
        if b < 2:
            continue
        pa = prime_power(a, spf)
        char2 = pa[0] == 2
        if is_prime(b, spf) and b != pa[0]:
            d = strip(a - 1, [b])
            A = orb(a, d, char2)
            for t in divisors(b - 1):
                if prime_power(t, spf) or t == 1:
                    best = max(best, min(A, orb(b, t, False), a * b))
        pb = prime_power(b, spf)
        if pb and pb[0] == pa[0]:
            best = max(best, min(comb(a, 2), comb(b, 2), a * b))
    return best

# ---------------------------------------------------------------- parts
class Part:
    __slots__ = ("F", "c", "foreign", "size", "cap", "cb")

    def __init__(self, F, c, foreign, q, p, spf):
        self.F = F
        self.c = c
        self.foreign = foreign
        self.size = F * c
        char2 = (not foreign) and p == 2
        if foreign:
            # Lemma B': twist is the q-part of c-1, fixed once q is chosen
            self.cap = F * orb(c, qpart(c - 1, q), False)
        else:
            # p-characteristic: twist at most c-1; the exact value depends on
            # which foreign primes appear (Lemma C) and is applied later
            self.cap = F * orb(c, c - 1, char2)
        self.cb = ((F if q % 2 else F // 2) * c * c) if F > 1 else None


def parts_for(n, p, q, spf, floor):
    """all (F, c) parts with F a q-power, c a prime power, F*c <= n, and whose
    optimistic capacity exceeds `floor` (pruning bound of Part G.4)"""
    out = []
    cmin = 2 * floor // n + 1 if floor else 2
    c = max(2, cmin)
    while c <= n:
        pp = prime_power(c, spf)
        if pp:
            foreign = not (pp[0] == p)
            if not (foreign and pp[1] > 1):          # Lemma B': foreign => prime
                F = 1
                while F * c <= n:
                    # a foreign part cannot be fused: its F copies of C_c would
                    # generate C_c^F inside the cyclic layer, which is cyclic only
                    # for F = 1.  (Diagonal translations keep it cyclic but drop
                    # the within-orbit cross class to ~F*c, always dominated.)
                    if foreign and F > 1:
                        break
                    pt = Part(F, c, foreign, q, p, spf)
                    # non-strict: a configuration that merely TIES the current
                    # best must still survive, so that a witness is recorded
                    if pt.cap >= floor and (pt.cb is None or pt.cb >= floor):
                        out.append(pt)
                    F *= q
        c += 1
    out.sort(key=lambda t: -t.size)
    return out


# ---------------------------------------------------------------- evaluation
# When SAFE is set, a p-characteristic part whose twist Lemma C strictly reduces
# is given the UNCONDITIONAL capacity F*C(c,2) instead of F*orb(c,d).  The refined
# value assumes a Gamma-L(1)-type point stabiliser; the Singer step that would
# justify that is false in general (Part B of enumeration-proof.md, extraspecial
# counterexample), and exotic stabilisers can have larger orbits than the +/-dT
# classes.  C(c,2) bounds ANY stabiliser, so SAFE mode is unconditional at the
# cost of looseness exactly where Lemma C bites.
SAFE = True     # default: unconditional.  See --refined to disable.


def value(sel, p, spf):
    """exact m* of a chosen configuration (list of Part), applying Lemma C.
    Returns None if the configuration is inadmissible."""
    foreigns = [t.c for t in sel if t.foreign]
    # distinct foreign primes: two foreign parts of the same prime r would put
    # C_r x C_r inside the cyclic layer Gamma_1/Gamma_2, which is not cyclic
    if len(foreigns) != len(set(foreigns)):
        return None
    terms = []
    for t in sel:
        if t.foreign:
            terms.append(t.cap)
        else:
            d = strip(t.c - 1, foreigns)             # Lemma C
            char2 = (p == 2)
            if SAFE and d < t.c - 1:
                terms.append(t.F * comb(t.c, 2))     # unconditional fallback
            else:
                terms.append(t.F * orb(t.c, d, char2))
        if t.cb is not None:
            terms.append(t.cb)
    for i in range(len(sel)):
        for j in range(i + 1, len(sel)):
            terms.append(sel[i].size * sel[j].size)
    return min(terms)


def best_with_k(n, K, spf, seed=0):
    """max over configurations with at most K orbits; `seed` prunes"""
    best, wit = seed, None
    primes = [x for x in range(2, n + 1) if is_prime(x, spf)]
    for p in primes:
        # a p-characteristic part needs some power of p that is large enough:
        # F*C(c,2) > best with F*c <= n forces c > 2*best/n + 1
        cmin = 2 * best // n + 1 if best else 2
        if p < cmin:
            v = p
            while v < cmin:
                v *= p
            if v > n:
                continue                              # no usable p-power at all
        elif p > n:
            continue
        for q in primes:
            if q > n:
                break
            pool = parts_for(n, p, q, spf, best)
            if not pool:
                continue

            def rec(idx, rem, sel):
                nonlocal best, wit
                if rem == 0:
                    if not sel:
                        return
                    v = value(sel, p, spf)
                    # record a witness on a tie too: the fast seed may already
                    # have reached the maximum, in which case nothing ever
                    # strictly improves and the witness would stay empty
                    if v is not None and (v > best or (wit is None and v == best)):
                        best = v
                        wit = (p, q, [(t.F, t.c, t.foreign) for t in sel])
                    return
                if len(sel) == K:
                    return
                for i in range(idx, len(pool)):
                    t = pool[i]
                    if t.size > rem:
                        continue
                    if t.cap < best or (t.cb is not None and t.cb < best):
                        continue
                    if sel and min(u.size for u in sel) * t.size < best:
                        continue
                    rec(i, rem - t.size, sel + [t])

            rec(0, n, [])
    return best, wit


def mu_bound(n, spf, kmax=12, verbose=False):
    """self-certifying iteration of Part F"""
    N2 = comb(n, 2)
    best, wit, cert = seed_value(n, spf), None, False
    for K in range(1, kmax + 1):
        b, w = best_with_k(n, K, spf, seed=best)
        if b > best or (wit is None and w is not None):
            best, wit = b, w
        delta = best / N2 if N2 else 0
        if verbose:
            lim = (1 / delta ** 0.5) if delta > 0 else float("inf")
            print(f"    K={K}: B={best}  delta={delta:.4f}  need K >= {lim:.2f}")
        if delta > 0 and 1.0 / delta ** 0.5 <= K:
            cert = True
            break
    return best, wit, K, cert


def fallback_used(w, spf):
    """True if the winning configuration contains a p-characteristic part whose
    twist Lemma C strictly reduces.  In SAFE mode such a part is scored with the
    unconditional F*C(c,2) rather than F*orb(c,d), so the reported bound may
    exceed what the refined (Gamma-L(1)-assuming) formula would give.  If this is
    False, the two modes provably agree at this n: the winning configuration is
    scored identically by both, and since safe >= refined pointwise, the maxima
    coincide."""
    if not w:
        return False
    p, q, ps = w
    foreigns = [c for F, c, fg in ps if fg]
    for F, c, fg in ps:
        if not fg and strip(c - 1, foreigns) < c - 1:
            return True
    return False


def show(w):
    """render a configuration: F x c per orbit, * marking a foreign part"""
    if not w:
        return "-"
    p, q, ps = w
    body = " + ".join(f"{F}x{c}{'*' if fg else ''}" for F, c, fg in ps)
    legend = "   (* foreign)" if any(fg for _, _, fg in ps) else ""
    return f"p={p} q={q}: {body}{legend}"


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Enumerate Oliver-group configurations and bound mu(n).")
    ap.add_argument("--n", type=int, help="single value of n, with a trace")
    ap.add_argument("--nmin", type=int, help="start of range (default: 6, or "
                    "resume after the last row of --out if that file exists)")
    ap.add_argument("--nmax", type=int)
    ap.add_argument("--check", help="mu_table_full.csv, to compare against")
    ap.add_argument("--out", help="results CSV; a NEW file, not mu_table_full.csv "
                    "(different schema). Written with a header, appended to on "
                    "re-runs, and used to resume when --nmin is omitted.")
    ap.add_argument("--quiet", action="store_true", help="only the final summary")
    ap.add_argument("--refined", action="store_true",
                    help="assume Gamma-L(1)-type point stabilisers, using "
                         "F*orb(c,d) for a p-characteristic part even where Lemma C "
                         "reduces the twist.  Default is the UNCONDITIONAL bound, "
                         "which uses F*C(c,2) there; the two agree on every optimum "
                         "computed so far, so this flag changes nothing in practice.")
    a = ap.parse_args()
    globals()['SAFE'] = not a.refined

    HEADER = "n,C(n2),mu_bound,density,orbits_K,certified,fallback,witness"

    if a.n:
        spf = sieve_spf(a.n + 1)
        print(f"n = {a.n},  C(n,2) = {comb(a.n,2)}")
        b, w, K, cert = mu_bound(a.n, spf, verbose=True)
        print(f"  B(n) = {b}   density {b/comb(a.n,2):.4f}   "
              f"certified at K={K}: {cert}")
        print(f"  witness  {show(w)}")
        sys.exit()

    if not a.nmax:
        ap.error("give --n or --nmax")

    # ---- resume logic -------------------------------------------------
    done = set()
    resume_from = None
    if a.out and os.path.exists(a.out) and os.path.getsize(a.out) > 0:
        with open(a.out) as fh:
            first = fh.readline().rstrip("\n").lstrip("\ufeff")
            if first != HEADER:
                sys.exit(
                    f"refusing to append to {a.out}: its header is\n"
                    f"    {first}\n"
                    f"but this version writes\n"
                    f"    {HEADER}\n"
                    f"The schema has changed (a 'fallback' column was added, and "
                    f"rows now depend on the safe/refined mode).\n"
                    f"Use a fresh --out file, or delete the old one.")
            for row in csv.DictReader(fh, fieldnames=HEADER.split(",")):
                try:
                    done.add(int(row["n"]))
                except (KeyError, ValueError, TypeError):
                    pass
        if done:
            resume_from = max(done) + 1
    nmin = a.nmin if a.nmin is not None else (resume_from or 6)

    spf = sieve_spf(a.nmax + 1)
    todo, skipped_pp, skipped_done = [], 0, 0
    for n in range(max(2, nmin), a.nmax + 1):
        if prime_power(n, spf):
            skipped_pp += 1
        elif n in done:
            skipped_done += 1
        else:
            todo.append(n)

    print(f"mode           {'UNCONDITIONAL (safe)' if not a.refined else 'REFINED (assumes Gamma-L(1)-type stabilisers)'}")
    if not a.refined:
        print(f"               p-parts scored F*C(c,2) where Lemma C cuts the twist;")
        print(f"               'fb' in the per-n line flags a winner that used it")
    print(f"range          n in [{nmin}, {a.nmax}]")
    if resume_from and a.nmin is None:
        print(f"resuming       {a.out} already holds {len(done)} rows "
              f"(max n = {max(done)}); continuing from {resume_from}")
        print(f"               NOTE: earlier rows were written by whichever mode "
              f"was used then; mixing safe and refined rows in one file is not "
              f"detected")
    print(f"to compute     {len(todo)} values"
          + (f"  ({todo[0]} … {todo[-1]})" if todo else ""))
    print(f"skipped        {skipped_pp} prime powers (mu = C(n,2) exactly)"
          + (f", {skipped_done} already in {a.out}" if skipped_done else ""))
    tbl = {}
    if a.check:
        for r in csv.DictReader(open(a.check)):
            tbl[int(r["n"])] = (int(r["mu_lower"]), int(r["prime_power"]))
        print(f"comparing      against {a.check}")
    if not todo:
        print("nothing to do"); sys.exit()
    print()

    fh = None
    if a.out:
        fresh = (not os.path.exists(a.out)) or os.path.getsize(a.out) == 0
        fh = open(a.out, "a")
        if fresh:
            fh.write(HEADER + "\n"); fh.flush()

    viol = exact = short = nfb = 0
    worst = []
    t0 = time.time()
    ndone = 0
    interrupted = False

    def summary():
        el = time.time() - t0
        el_s = (f"{el:.1f}s" if el < 90 else f"{el/60:.1f}m" if el < 5400 else f"{el/3600:.2f}h")
        print(f"\nn in [{nmin}, {a.nmax}]: computed {ndone} of {len(todo)}"
              f"{' (INTERRUPTED)' if interrupted else ''} in {el_s}"
              f" | exact {exact}, table-short {short}, violations {viol}")
        if ndone:
            print(f"timing         {el/ndone:.2f}s per value overall"
                  + (f", {sum(recent)/len(recent):.2f}s over the last {len(recent)}"
                     if recent else ""))
        if not a.refined:
            print(f"unconditional fallback invoked on the winner at {nfb} of {ndone} values"
                  + ("  -> the refined bound would be identical throughout" if nfb == 0
                     else "  -> at these n the refined bound may be smaller"))
        if interrupted and ndone:
            print(f"last completed n = {lastn}"
                  + (f"; resume with --nmin {lastn + 1}" if not a.out else
                     f"; re-run the same command to resume from {a.out}"))
        for x in sorted(worst, key=lambda t: t[3])[:10]:
            print(f"   n={x[0]:<5} table {x[1]:>8} < bound {x[2]:>8} ({x[3]:.3f})  {x[4]}")

    lastn = None
    recent = deque(maxlen=25)          # per-n times, for a rate that tracks growth
    try:
      for idx, n in enumerate(todo, 1):
          t_n = time.time()
          b, w, K, cert = mu_bound(n, spf)
          dt = time.time() - t_n
          recent.append(dt)
          dens = b / comb(n, 2)
          fb = (not a.refined) and fallback_used(w, spf)
          nfb += int(fb)
          note = ""
          if n in tbl and not tbl[n][1]:
              lo = tbl[n][0]
              if lo > b:
                  viol += 1; note = f"  VIOLATION: table {lo} > bound {b}"
              elif lo == b:
                  exact += 1; note = "  = table"
              else:
                  short += 1; note = f"  table SHORT at {lo} ({lo/b:.3f})"
                  worst.append((n, lo, b, lo / b, show(w)))
          if fh:
              fh.write(f'{n},{comb(n,2)},{b},{dens:.6f},{K},{int(cert)},'
                       f'{int(fb)},"{show(w)}"\n')
              fh.flush()
          if not a.quiet:
              rate = sum(recent) / len(recent)          # recent mean, not lifetime
              left = len(todo) - idx
              eta = left * rate
              eta_s = (f"{eta:.0f}s" if eta < 90 else
                       f"{eta/60:.0f}m" if eta < 5400 else f"{eta/3600:.1f}h")
              print(f"[{idx}/{len(todo)}] {time.strftime('%H:%M:%S')} "
                    f"n={n:<6} B={b:<10} d={dens:.4f} K={K} "
                    f"{'cert' if cert else 'UNCERT'}{' fb' if fb else ''} "
                    f"{dt:6.2f}s  (avg {rate:5.2f}s, eta {eta_s}){note}")
          ndone += 1
          lastn = n
    except KeyboardInterrupt:
        interrupted = True
        print("\n^C  -- stopping; results so far are already written")
    if fh:
        fh.close()
    summary()
