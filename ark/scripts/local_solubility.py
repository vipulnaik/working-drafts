#!/usr/bin/env python3
"""
local_solubility.py -- which residue classes of n admit the odd-n family n = 2c + r,
and at what efficiency.

THE FAMILY.  Two equal p-characteristic blocks of size c plus one foreign prime r,
so n = 2c + r.  Its density, with x = c/n and e the foreign block's efficiency
e = orb(r,t)/C(r,2), is

    delta(x) = min( x^2, 2x(1-2x), e(1-2x)^2 ),

maximised at the balance point.  e = 1 gives the cap 1/9 at x = 1/3; e = 1/2 gives
1/(2+sqrt2)^2 ~ 0.0858 at x = 1/(2+sqrt2).

THE QUESTION.  Full efficiency needs the foreign twist to have order (r-1)/2, and
Lemma B' forces it to be a power of the top prime, so (r-1)/2 must be a prime
power.  Together with r prime and c = (n-r)/2 a prime power, that is a
Bateman-Horn system in the single variable r:

    f1(r) = r,   f2(r) = (r-1)/2,   f3(r) = (n-r)/2.

The singular series is positive iff omega(l) < l for every prime l, where
omega(l) = #{r mod l : f1 f2 f3 = 0 mod l}.  For odd l this is |{0, 1, n}| mod l,
so only l = 3 can be fatal.  The prime 2 needs separate treatment because f2 and
f3 involve a division by 2.

WHAT THIS SCRIPT DOES.  Enumerates the residue classes of n modulo a chosen
modulus, reports which admit the full-efficiency system, and -- for those that do
not -- reports the best efficiency still available and the corresponding cap.
Optionally checks the verdict against a computed table.

Usage:
    python3 local_solubility.py
    python3 local_solubility.py --table mu_table_safe_v2.csv
"""
import argparse, csv, re, collections
from math import comb

ap = argparse.ArgumentParser()
ap.add_argument("--table", default=None)
ap.add_argument("--modulus", type=int, default=12)
ap.add_argument("--primes", type=int, default=200, help="check odd l up to this")
a = ap.parse_args()

# ---------------------------------------------------------------- the caps
def cap_for(e, steps=400000):
    """max over x of min(x^2, 2x(1-2x), e(1-2x)^2)."""
    best = 0.0
    for i in range(1, steps):
        x = i / (2 * steps)
        if 1 - 2 * x <= 0:
            break
        d = min(x * x, 2 * x * (1 - 2 * x), e * (1 - 2 * x) ** 2)
        if d > best:
            best = d
    return best

# ---------------------------------------------------- local conditions
def two_adic(n_mod4):
    """At l = 2.  r must be odd.  Full efficiency wants (r-1)/2 odd, i.e.
    r = 3 mod 4; then c = (n-r)/2 is odd iff n = 1 mod 4.  If n = 3 mod 4 the
    only way to keep c odd is r = 1 mod 4, whence 4 | r-1 and the odd part of
    the twist is at most (r-1)/4, capping the efficiency at 1/2."""
    return 1.0 if n_mod4 == 1 else 0.5

def odd_local(l, n):
    """omega(l) for odd l: the forbidden residues are r = 0, r = 1, r = n."""
    return len({0 % l, 1 % l, n % l})

def verdict(n_res, mod, primes_upto):
    e2 = two_adic(n_res % 4)
    dead = [l for l in range(3, primes_upto)
            if all(l % d for d in range(2, int(l ** 0.5) + 1))
            and odd_local(l, n_res) >= l]
    return e2, dead

# ---------------------------------------------------------------- report
print(f"Local solubility of n = 2c + r over odd residues mod {a.modulus}")
print(f"(checking l = 3 .. {a.primes}; only l = 3 can ever be fatal, since for odd l")
print(" the forbidden set is {{0, 1, n}} and has size at most 3)")
print()
print(f"{'n mod '+str(a.modulus):>10} | {'2-adic e':>8} | {'dead odd l':>10} | "
      f"{'generic e':>9} | {'cap':>7}")
CAP1, CAPh, CAPt = cap_for(1.0), cap_for(0.5), cap_for(1/3)
rows_out = {}
for res in range(a.modulus):
    if res % 2 == 0:
        continue
    e2, dead = verdict(res, a.modulus, a.primes)
    if dead:
        # l = 3 fatal: full efficiency needs a sparse escape (a power of 3),
        # so generically the twist loses a factor of 3
        e = min(e2, 1/3)
        note = f"l={dead[0]}"
    else:
        e = e2
        note = "none"
    cap = cap_for(e)
    rows_out[res] = (e2, dead, e, cap)
    print(f"{res:>10} | {e2:>8.3f} | {note:>10} | {e:>9.3f} | {cap:>7.5f}")
print()
print(f"caps: e = 1 -> {CAP1:.5f} (= 1/9);  e = 1/2 -> {CAPh:.5f} (= 1/(2+sqrt2)^2);"
      f"  e = 1/3 -> {CAPt:.5f}")
print()
print("Reading: n = 1 mod 4 and n != 2 mod 3 is the generic full-efficiency case.")
print("n = 3 mod 4 loses a factor of 2 in the twist; n = 2 mod 3 loses a factor of 3")
print("unless (r-1)/2 or c is itself a power of 3, which is a sparse escape.")

# ---------------------------------------------------------------- validation
if a.table:
    N = 0
    rows = list(csv.DictReader(open(a.table)))
    N = max(int(r["n"]) for r in rows) + 2
    spf = list(range(N + 2)); i = 2
    while i * i <= N + 1:
        if spf[i] == i:
            for j in range(i * i, N + 2, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    def qpart(x, q):
        t = 1
        while x % (t * q) == 0:
            t *= q
        return t
    def pdivs(x):
        o = []
        while x > 1:
            p = spf[x]; o.append(p)
            while x % p == 0:
                x //= p
        return o
    def eff(r):
        return max((min(r * qpart(r-1,q) // 2 if qpart(r-1,q) % 2 == 0
                        else r * qpart(r-1,q), comb(r, 2)) / comb(r, 2))
                   for q in set(pdivs(r - 1)))
    def parse(w):
        m = re.match(r"p=(\S+) q=(\d+): (.*?)(\s{2,}\(\* foreign\))?$", w)
        toks = [t.strip() for t in m.group(3).split(" + ")]
        return [(int(re.match(r"(\d+)x", t).group(1)),
                 int(re.match(r"\d+x(\d+)", t).group(1)), t.endswith("*")) for t in toks]
    obs = collections.defaultdict(list)
    for r in rows:
        n = int(r["n"])
        if n % 2 == 0 or r["parts"] != "3":
            continue
        parts = parse(r["witness"])
        pp = [c for F, c, fg in parts if not fg]
        fo = [c for F, c, fg in parts if fg]
        if len(pp) == 2 and len(fo) == 1 and pp[0] == pp[1]:
            obs[n % a.modulus].append((float(r["density"]), eff(fo[0]), n))
    print()
    print(f"{a.table}: observed maxima among 2c+r winners")
    print(f"{'n mod '+str(a.modulus):>10} | {'rows':>5} | {'max delta':>9} | "
          f"{'predicted cap':>13} | {'ratio':>6} | {'# at e=1':>8}")
    for res in sorted(obs):
        v = obs[res]
        md = max(x[0] for x in v)
        e1 = sum(1 for x in v if x[1] > 0.99)
        pred = rows_out[res][3]
        # a class whose generic cap is lowered by l=3 can still reach 1/9 via the
        # sparse escape, so report against the unlowered cap where that happens
        shown = CAP1 if (e1 and md > pred * 1.05) else pred
        print(f"{res:>10} | {len(v):>5} | {md:>9.5f} | {shown:>13.5f} | "
              f"{md/shown:>6.3f} | {e1:>8}")
