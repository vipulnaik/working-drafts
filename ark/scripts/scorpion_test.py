"""Exact evasiveness of the MONOTONIZED scorpion, by adversary game search.

Exact scorpion (Best-van Emde Boas-Lenstra, non-monotone): sting deg 1, tail
deg 2, body deg n-2 -- decidable in O(n) queries.
Monotone closure "contains a spanning scorpion subgraph":
  P(G) = exists distinct s,b and t not in {s,b} with {s,t} in E
         and {b,x} in E for all x not in {s,b}.
This is monotone and nontrivial.  ARK predicts D(P) = C(n,2) exactly.

Adversary recursion: state (L = known present, A = known absent).
undetermined(L,A) = not P(L) and P(all edges minus A)     [monotone]
survive(L,A) = undetermined(L,A) and for EVERY unqueried e,
               SOME answer keeps surviving (base: |L|+|A| = N-1).
P is evasive iff survive(empty, empty).
"""
import sys, itertools
from functools import lru_cache

def build(n):
    pairs=list(itertools.combinations(range(n),2))
    idx={p:i for i,p in enumerate(pairs)}
    N=len(pairs)
    def P(mask):
        adj=[0]*n
        for i,(a,b) in enumerate(pairs):
            if mask>>i&1: adj[a]|=1<<b; adj[b]|=1<<a
        for b in range(n):
            for s in range(n):
                if s==b: continue
                # b adjacent to all x not in {s,b}?
                need=((1<<n)-1) & ~(1<<b) & ~(1<<s)
                if adj[b]&need!=need: continue
                # some t not in {s,b} adjacent to s
                cand=((1<<n)-1) & ~(1<<b) & ~(1<<s)
                if adj[s]&cand: return True
        return False
    return pairs,N,P

def evasive(n, verbose=False):
    pairs,N,P=build(n)
    FULL=(1<<N)-1
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def undet(L,A):
        return (not P(L)) and P(FULL & ~A)
    @lru_cache(maxsize=None)
    def survive(L,A):
        if not undet(L,A): return False
        k=bin(L).count('1')+bin(A).count('1')
        if k==N-1: return True
        for i in range(N):
            if (L>>i&1) or (A>>i&1): continue
            if not (survive(L|1<<i,A) or survive(L,A|1<<i)):
                return False
        return True
    r=survive(0,0)
    if verbose:
        print(f"  n={n} N={N}: evasive={r}  (memo states: {survive.cache_info().currsize})")
    return r

for n in [4,5,6]:
    evasive(n, verbose=True)
