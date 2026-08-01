#!/usr/bin/env python3
"""
ladder_verify.py -- verify the density ladder directly, per n, over ALL residue
classes, and compute the global floor of arithmetic-of-density.md section 5.

WHAT THIS REPLACED, AND WHY.  An earlier version asked a single binary question
-- "does a full-efficiency representation exist near the balance point?" -- and
skipped every class where full efficiency is locally obstructed.  That silently
left half of all n unverified: classes 2, 3, 5, 7, 8 and 11 mod 12 were never
examined, and those are exactly the hard ones.  It also used one fixed window
around x = 1/3, which does not contain the balance point of the low-efficiency
classes, so scanning there and finding nothing looks like a failure but is an
artefact of the window.

This version computes, for each n, the best density any of the three families of
section 2 can achieve, scanning the block size over a window wide enough to hold
EVERY class's balance point.  That is strictly more informative: representability
is the special case "achieved density > 0", and the number obtained is a proven
lower bound on delta(n) = mu(n)/C(n,2).

THE FAMILIES (all scored in SAFE mode, so each is a genuine lower bound)
  fused        n = F*c,      F a q-power, c a prime power        -> ~1/F
  two parts    n = c + r,    c a prime power, r prime            -> <= 1/4
  three parts  n = 2c + r,   two equal c-blocks plus a foreign   -> <= 1/9

BALANCE POINTS, and hence the window.  With x = c/n and e the foreign block's
efficiency, delta(x) = min(x^2, 2x(1-kx), e(1-kx)^2) for k = 1 (two parts) or
k = 2 (three parts).  The optima run from x = 0.2247 (three parts at e = 1/6,
class 11) up to x = 0.5 (two parts at e = 1).  The window [0.10, 0.55] holds all
of them with room to spare; [0.20, 0.55] does NOT -- it clips n = 9179, whose
optimum sits at x = 0.1973, and reports a spurious shortfall there.

CLASS CAPS (section 3.3), used to report each n as a fraction of what its class
permits:
    n mod 12 in {0,4,6,10}   e=1     cap 1/4            = 0.25000
    n mod 12 in {2,8}        e=1/3   cap 1/(1+sqrt3)^2  = 0.13397
    n mod 12 in {1,9}        e=1     cap 1/9            = 0.11111
    n mod 12 in {3,7}        e=1/2   cap 1/(2+sqrt2)^2  = 0.08579
    n mod 12 == 5            e=1/3   cap                = 0.07180
    n mod 12 == 11           e=1/6   cap                = 0.05051

Usage:
    python3 ladder_verify.py 100000
    python3 ladder_verify.py 100000 --floor 0.02
"""
import sys, time, bisect, math
from math import comb

_A = sys.argv
N = int(_A[1]) if len(_A) > 1 and not _A[1].startswith("-") else 100000
FLOOR = 0.02
for i, x in enumerate(_A):
    if x == "--floor":
        FLOOR = float(_A[i + 1])

CAP = {0: .25, 4: .25, 6: .25, 10: .25,
       2: 1 / (1 + 3 ** .5) ** 2, 8: 1 / (1 + 3 ** .5) ** 2,
       1: 1 / 9, 9: 1 / 9,
       3: 1 / (2 + 2 ** .5) ** 2, 7: 1 / (2 + 2 ** .5) ** 2,
       5: 0.07180, 11: 0.05051}

t = time.time()
sieve = bytearray([1]) * (N + 1)
sieve[0] = sieve[1] = 0
for i in range(2, int(N ** 0.5) + 1):
    if sieve[i]:
        sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
ispp = bytearray(N + 1)
base = [0] * (N + 1)
for p in range(2, N + 1):
    if sieve[p]:
        q = p
        while q <= N:
            ispp[q] = 1
            base[q] = p
            q *= p

# Efficiency of a foreign prime r: e = max over top primes q of orb(r, q-part)/C(r,2).
# With r-1 = 2^a * u, u odd, L the largest prime power dividing u, this is
# max(2^a/(r-1), 2L/(r-1)) -- section 3.3.
EFF = [0.0] * (N + 1)
for r in range(3, N + 1, 2):
    if not sieve[r]:
        continue
    m = r - 1
    a, x = 0, m
    while x % 2 == 0:
        x //= 2
        a += 1
    best, y, d = 1, x, 3
    while d * d <= y:
        if y % d == 0:
            e = 1
            while y % d == 0:
                y //= d
                e += 1
            best = max(best, d ** (e - 1))
        d += 2
    if y > 1:
        best = max(best, y)
    EFF[r] = max((2 ** a) / m, 2 * best / m)

PPs = [c for c in range(2, N + 1) if ispp[c]]
print(f"sieve and efficiencies to {N:,} in {time.time()-t:.1f}s")

LO_X, HI_X = 0.10, 0.55        # contains every class's balance point

def achieved(n, stop_at=None):
    """Best density over the three families.  With stop_at set, returns as soon
    as that is exceeded; most n clear it at once, which is what makes the scan
    affordable."""
    C = n * (n - 1) / 2
    best = 0.0
    F = 2
    while F * F <= n:                              # fused
        if n % F == 0:
            for FF in (F, n // F):
                c = n // FF
                if ispp[FF] and ispp[c]:
                    q = base[FF]
                    v = min(FF * comb(c, 2), (FF if q % 2 else FF // 2) * c * c)
                    if v > best * C:
                        best = v / C
        F += 1
    if stop_at and best > stop_at:
        return best
    lo = bisect.bisect_left(PPs, int(LO_X * n))
    hi = bisect.bisect_right(PPs, int(HI_X * n))
    for k in range(lo, hi):
        c = PPs[k]
        bp = base[c]
        r = n - c                                  # two parts
        if 3 <= r <= N and sieve[r] and bp != r:
            v = min(comb(c, 2), EFF[r] * comb(r, 2), c * r)
            if v > best * C:
                best = v / C
                if stop_at and best > stop_at:
                    return best
        r = n - 2 * c                              # three parts, two equal blocks
        if 3 <= r <= N and sieve[r] and bp != r:
            v = min(comb(c, 2), EFF[r] * comb(r, 2), c * c, c * r)
            if v > best * C:
                best = v / C
                if stop_at and best > stop_at:
                    return best
    return best

TICK, SUMMARY = 10_000, 100_000

def stamp():
    return time.strftime("%H:%M:%S")

t0 = time.time()
per = {a: [1e9, None, 0] for a in range(12)}
gmin = (1e9, None)
below = []
blk_min = (1e9, None)              # minimum within the current SUMMARY block
last = t0
print(f"{stamp()}  scanning to {N:,}; checkpoint every {TICK:,}, "
      f"summary every {SUMMARY:,}")
for n in range(6, N + 1):
    if not ispp[n]:
        a = n % 12
        d = achieved(n, stop_at=0.9 * CAP[a])
        ratio = d / CAP[a]
        if ratio < per[a][0]:
            per[a][0], per[a][1] = ratio, n
        if d < gmin[0]:
            gmin = (d, n)
        if d < blk_min[0]:
            blk_min = (d, n)
        if d < FLOOR:
            per[a][2] += 1
            below.append((n, round(d, 5)))
    if n % TICK == 0:
        now = time.time()
        rate = TICK / max(now - last, 1e-9)
        # Per-n cost is proportional to the number of prime powers in the scan
        # window, i.e. to n/log n, so elapsed time grows like N^2/log N.  Scale
        # the elapsed time by that ratio rather than extrapolating linearly.
        f = lambda x: x * x / math.log(max(x, 3))
        eta = (now - t0) * (f(N) / f(n) - 1)
        print(f"{stamp()}  n = {n:>9,}  ({now-t0:>6.0f}s, {rate:>7.0f} n/s)  "
              f"floor so far {gmin[0]:.5f} at n = {gmin[1]}"
              f"{'  <' + str(len(below)) + ' below ' + str(FLOOR) + '>' if below else ''}"
              f"   eta ~{eta/60:.1f}m")
        last = now
    if n % SUMMARY == 0:
        b = f"{blk_min[0]:.5f} at n = {blk_min[1]}" if blk_min[1] else "n/a"
        print(f"{stamp()}  --- through {n:,}: block floor {b}; "
              f"global floor {gmin[0]:.5f} at n = {gmin[1]} "
              f"(mod 12 = {gmin[1] % 12}); {len(below)} below {FLOOR} ---")
        blk_min = (1e9, None)
print(f"{stamp()}  scan complete in {time.time()-t0:.0f}s")
print()
print(f"{'n mod 12':>9} {'cap':>9} {'min delta/cap':>14} {'at n':>8} "
      f"{'# below ' + str(FLOOR):>14}")
for a in range(12):
    r, n, cnt = per[a]
    if n is None:
        continue
    print(f"{a:>9} {CAP[a]:>9.5f} {r:>14.3f} {n:>8} {cnt:>14}")
print()
print(f"GLOBAL FLOOR over composite non-prime-power n <= {N:,}: "
      f"delta >= {gmin[0]:.5f}, attained at n = {gmin[1]} "
      f"(n mod 12 = {gmin[1] % 12})")
print(f"values with delta < {FLOOR}: {len(below)}"
      + (f" -> {below[:10]}" if below
         else "  -- the section 5 conjecture holds throughout this range"))
