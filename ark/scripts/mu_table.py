"""
mu_table.py -- per-n invariant table for the minimum-orbital function mu(n).

Columns computed:
  C(n,2)          trivial
  prime power?    if yes, mu(n) = C(n,2) exactly (AGL(1,q) is 2-transitive and
                  Oliver; conversely Zassenhaus forbids orbital-transitive
                  Oliver groups elsewhere, so mu(n) < C(n,2) for other n)
  mu_lower        best lower bound from explicit constructions, exact by
                  orbit BFS over:
                    * the affine template of oliver_mu.candidate_groups
                      (covers the two-block ladder and three-block chains,
                      since Case B allows one full-twist block + q-coherent
                      twisted prime blocks)
                    * the wreath family (F_{p^a} x C_d) wr C_k on n = k*p^a,
                      k prime, d = k-part of p^a - 1  (the rev-3 correction:
                      twists and block rotation together in the top k-group)
  witness         description of a group achieving mu_lower
Scripts for other columns: mu_template alone = oliver_mu.py __main__;
exhaustive per-n batteries = ark_gap.g + consume_gap.py.
"""
import sys, itertools
from math import comb, gcd
sys.path.insert(0,'/home/claude')
from oliver_mu import candidate_groups, prime_power, is_prime, gf, gf_element_of_order

def min_orbital(gens, n):
    pairs=list(itertools.combinations(range(n),2))
    pidx={p:i for i,p in enumerate(pairs)}
    seen=[False]*len(pairs); best=None
    for i,st in enumerate(pairs):
        if seen[i]: continue
        seen[i]=True; size=1; fr=[st]
        while fr:
            nf=[]
            for (u,v) in fr:
                for g in gens:
                    a,b=g[u],g[v]
                    pr=(a,b) if a<b else (b,a)
                    j=pidx[pr]
                    if not seen[j]:
                        seen[j]=True; size+=1; nf.append(pr)
            fr=nf
        best=size if best is None else min(best,size)
    return best

def wreath_groups(n):
    """(F_{p^a} x C_d) wr C_k on n = k * p^a, k prime, d = k-part of p^a-1."""
    out=[]
    for k in range(2, n+1):
        if not is_prime(k) or n%k: continue
        m=n//k
        pp=prime_power(m)
        if not pp or m<2: continue
        p,a=pp
        # d = largest power of k dividing m-1 (may be 1)
        d=1
        while (m-1)%(d*k)==0: d*=k
        elems,add,mul=gf(p,a)
        blocks=[list(range(i*m,(i+1)*m)) for i in range(k)]
        gens=[]
        basis=[p**i for i in range(a)]
        for b in blocks:
            for x in basis:
                perm=list(range(n))
                for e in elems: perm[b[e]]=b[add[(e,x)]]
                gens.append(tuple(perm))
        if d>1:
            w=gf_element_of_order(p,a,d)
            for b in blocks:                     # independent twists per block
                perm=list(range(n))
                for e in elems: perm[b[e]]=b[mul[(e,w)]]
                gens.append(tuple(perm))
        perm=list(range(n))                       # block rotation
        for i in range(k):
            src,dst=blocks[i],blocks[(i+1)%k]
            for e in elems: perm[src[e]]=dst[e]
        gens.append(tuple(perm))
        out.append((gens, f"({m}:{d})wr{k}"))
    return out

def row(n):
    N=comb(n,2)
    pp=prime_power(n)
    if pp:
        return dict(n=n,N=N,pp=True,mu=N,wit="AGL(1,%d) [exact]"%n,dens=1.0)
    best=0; wit="-"
    for g in candidate_groups(n):
        m=min_orbital(g.generators,n)
        if m>best: best,wit=m,g.description()
    for gens,desc in wreath_groups(n):
        m=min_orbital(gens,n)
        if m>best: best,wit=m,desc
    return dict(n=n,N=N,pp=False,mu=best,wit=wit,dens=best/N)

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--nmax',type=int,default=30)
    args=ap.parse_args()
    print("| n | C(n,2) | prime power? | mu(n) status | best constructive lower bound | density | witness |")
    print("|---|--------|--------------|--------------|------------------------------|---------|---------|")
    for n in range(2,args.nmax+1):
        r=row(n)
        if r['pp']:
            print(f"| {n} | {r['N']} | yes | = {r['mu']} (exact) | {r['mu']} | 1.000 | {r['wit']} |")
        else:
            print(f"| {n} | {r['N']} | no | in [{r['mu']}, {r['N']//2}] | {r['mu']} | {r['dens']:.3f} | {r['wit']} |")
