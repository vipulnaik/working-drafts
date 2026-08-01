#!/usr/bin/env python3
"""
ladder_verify.py -- verify the ladder's hypothesis directly, per n.

WHY THIS EXISTS.  The conditional lower bounds of section 5 of the notes hold at
any n admitting the representation their family needs.  Bateman-Horn predicts
such representations are plentiful, but it is an asymptotic with an ineffective
constant and says nothing about any particular n.  Deciding the question at a
given n, however, is a sieve computation costing O(n/log n) -- against the n^2.9
of computing B(n).  So the hypothesis can be verified far past the range where
mu(n) is known, and the conditional statements made unconditional there.

FAMILIES CHECKED
  even n, two parts:   n = c + r,   c a prime power, r prime, (r-1)/2 a prime
                       power (full efficiency), c/n near 1/2
  odd n, three parts:  n = 2c + r,  same conditions on c and r, c/n near 1/3

Only n in the locally soluble classes are eligible.  For the odd family that is
n = 1 mod 4 and n != 2 mod 3; for the even family it is n != 2 mod 3 -- the l = 3
obstruction applies to BOTH parities, which earlier drafts missed.  See
arithmetic-of-density.md 3.1 and 3.3, and 3.4 for the independent derivation of
the same obstructions from the singular series.

Both families admit a sparse escape from the l = 3 obstruction, since c and
(r-1)/2 need only be prime POWERS: a power of 3 is divisible by 3 yet admissible.
That pins n near 2*3^k or 4*3^k, so it is available at O(log n) values of n and
is excluded here.

Usage:
    python3 ladder_verify.py 300000
    python3 ladder_verify.py 300000 --window 0.30,0.36
"""
import sys, time

_A = sys.argv
N = int(_A[1]) if len(_A) > 1 and not _A[1].startswith("-") else 300000
LO, HI = 0.30, 0.36
for i, x in enumerate(_A):
    if x == "--window":
        LO, HI = (float(v) for v in _A[i + 1].split(","))

t = time.time()
sieve = bytearray([1]) * (N + 1)
sieve[0] = sieve[1] = 0
for i in range(2, int(N ** 0.5) + 1):
    if sieve[i]:
        sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
ispp = bytearray(N + 1)
for p in range(2, N + 1):
    if sieve[p]:
        q = p
        while q <= N:
            ispp[q] = 1
            q *= p
print(f"sieve to {N:,} in {time.time()-t:.1f}s")

def ok_foreign(r):
    """r prime with (r-1)/2 a prime power: full efficiency by Lemma B'."""
    if r < 3 or r > N or not sieve[r]:
        return False
    h = (r - 1) // 2
    return h == 1 or ispp[h]

def has_rep_odd(n):
    for c in range(int(LO * n), int(HI * n) + 1):
        if ispp[c] and ok_foreign(n - 2 * c):
            return True
    return False

def has_rep_even(n):
    for c in range(int((0.5 - (HI - LO) / 2) * n), int((0.5 + (HI - LO) / 2) * n) + 1):
        if ispp[c] and ok_foreign(n - c):
            return True
    return False

t = time.time()
miss_o, el_o, miss_e, el_e = [], 0, [], 0
for n in range(5, N + 1):
    if n % 2:
        if n % 4 != 1 or n % 3 == 2:
            continue                      # not locally soluble at full efficiency
        el_o += 1
        if not has_rep_odd(n):
            miss_o.append(n)
    else:
        if n % 3 == 2:
            continue          # l = 3 obstruction applies to even n too (3.1)
        el_e += 1
        if not has_rep_even(n):
            miss_e.append(n)
print(f"scan in {time.time()-t:.0f}s")
print()
for lbl, el, miss in (("odd  n = 1 mod 4, != 2 mod 3", el_o, miss_o),
                      ("even n != 2 mod 3", el_e, miss_e)):
    print(f"{lbl}: {el:,} eligible, {len(miss)} without a balanced "
          f"full-efficiency representation")
    if miss:
        print(f"    largest failure n = {max(miss)}")
        print(f"    => every eligible n in [{max(miss)+1:,}, {N:,}] admits one, "
              f"verified rather than conjectured")
        print(f"    failures: {miss if len(miss) <= 40 else miss[:40] + ['...']}")
    print()
