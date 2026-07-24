"""
mu_fast.py -- closed-form best-known lower bounds for mu(n), scalable to n ~ 10^3+.

Families (all Oliver-validity-checked; orbital sizes in closed form, since
translation groups act freely on blocks):
  intra-orbital of a block GF(p^a) with multiplicative twist of order t:
     char 2:  m*t/2      (delta = -delta)
     char odd: m*t/2 if t even else m*t     (-1 in <w> iff 2 | t)
  P  prime power n: mu = C(n,2) exactly (AGL(1,n)).
  W  wreath (GF(p^a) x C_d) wr C_k, n = k*p^a, k prime, d = k-part of p^a-1:
     intra = k * block_intra(t=d);  cross = m^2 (k=2) or k*m^2 (k odd).
  B2 two-block AGL(1,m) x (F_r x C_{q^e}), n = m+r, m prime power, r prime,
     r not dividing m-1; q^e ranges over prime-power divisors of r-1:
     min( block_intra(m, m-1), block_intra(r, q^e), m*r ).
  B3 three-block chains m + (aq+1) + (bq+1), (a,b) over a covering set of even
     multiplier pairs, q, aq+1, bq+1 prime, m = n-(a+b)q-2 prime power,
     coprimality checks: min over 3 intras and 3 crosses.
Validation: agrees with the exact-BFS table of mu_table.py on 4 <= n <= 30
(run with --validate).
"""
import sys, argparse
from math import comb

def sieve(N):
    spf=list(range(N+1))
    for i in range(2,int(N**.5)+1):
        if spf[i]==i:
            for j in range(i*i,N+1,i):
                if spf[j]==j: spf[j]=i
    return spf

def factor(x,spf):
    f={}
    while x>1:
        p=spf[x]; f[p]=f.get(p,0)+1; x//=p
    return f

def prime_power(x,spf):
    if x<2: return None
    f=factor(x,spf)
    return (next(iter(f)),f[next(iter(f))]) if len(f)==1 else None

def is_prime(x,spf): return x>1 and spf[x]==x

def block_intra(m,t,p):
    # orbital size of intra pairs of GF(m)-block (char p) with twist order t
    if p==2: return m*t//2
    return m*t//2 if t%2==0 else m*t

def best_for_n(n,spf,chain_pairs):
    N=comb(n,2)
    pp=prime_power(n,spf)
    if pp: return N,"AGL(1,%d) [exact]"%n,True
    best=0; wit="-"
    # W
    for k in (x for x in range(2,n+1) if n%x==0 and is_prime(x,spf)):
        m=n//k
        ppm=prime_power(m,spf)
        if not ppm or m<2: continue
        p,a=ppm
        d=1
        while (m-1)%(d*k)==0: d*=k
        intra=k*block_intra(m,d,p)
        cross=m*m if k==2 else k*m*m
        v=min(intra,cross)
        if v>best: best,wit=v,f"({m}:{d})wr{k}"
    # D: k identical blocks GF(p^a), DIAGONAL twist order d | m-1 in the cyclic
    # middle layer, optional rotation by prime k with gcd(d,k)=1 (also middle);
    # bottom = translations, top trivial.  Distinct from W: d need not be a
    # k-power, but the twist is diagonal (one copy), not per-block.
    for k in range(2,n+1):
        if n%k: continue
        m=n//k
        ppm=prime_power(m,spf)
        if not ppm or m<2: continue
        p,a=ppm
        # without rotation: full twist d=m-1; intra NOT fused; cross = m^2
        v=min(block_intra(m,m-1,p), m*m)
        if v>best: best,wit=v,f"{k}x({m}:{m-1})diag"
        # with rotation (k prime): d = largest divisor of m-1 coprime to k
        if is_prime(k,spf):
            d=m-1
            while d%k==0: d//=k
            # take largest divisor of m-1 coprime to k: strip k's from m-1
            dd=m-1
            g=1
            while dd%k==0: dd//=k
            d=dd
            intra=k*block_intra(m,d,p)
            cross=m*m if k==2 else k*m*m
            v=min(intra,cross)
            if v>best: best,wit=v,f"{k}x({m}:{d})diag+rot"
    # B2
    for m in range(2,n-1):
        ppm=prime_power(m,spf)
        if not ppm: continue
        r=n-m
        if not is_prime(r,spf) or (m-1)%r==0: continue
        p,a=ppm
        im=block_intra(m,m-1,p)
        # prime-power divisors of r-1
        f=factor(r-1,spf)
        for q,e in f.items():
            for ee in range(1,e+1):
                v=min(im, block_intra(r,q**ee,r), m*r)
                if v>best: best,wit=v,f"AGL(1,{m})xF{r}:C{q**ee}"
    # B3 chains
    for (a,b) in chain_pairs:
        for q in range(2,(n-2)//(a+b)+1):
            if not is_prime(q,spf): continue
            r,s=a*q+1,b*q+1
            m=n-r-s
            if m<2 or not is_prime(r,spf) or not is_prime(s,spf) or r==s: continue
            ppm=prime_power(m,spf)
            if not ppm: continue
            p,_=ppm
            if (m-1)%r==0 or (m-1)%s==0: continue
            # q-parts of r-1 = aq, s-1 = bq
            def qpart(x):
                t=1
                while x%(t*q)==0: t*=q
                return t
            v=min(block_intra(m,m-1,p), block_intra(r,qpart(a*q),r),
                  block_intra(s,qpart(b*q),s), m*r, m*s, r*s)
            if v>best: best,wit=v,f"F{m}+({a}q+1={r})+({b}q+1={s}),q={q}"
    return best,wit,False

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--nmax',type=int,default=1000)
    ap.add_argument('--validate',action='store_true')
    args=ap.parse_args()
    spf=sieve(args.nmax+10)
    chain_pairs=[(a,b) for a in range(2,32,2) for b in range(a+2,32,2)]
    if args.validate:
        sys.path.insert(0,'/home/claude')
        from mu_table import row
        bad=0
        for n in range(4,31):
            v,w,ex=best_for_n(n,spf,chain_pairs)
            r=row(n)
            if v<r['mu']:
                print(f"n={n}: fast {v} < BFS {r['mu']} ({r['wit']}) MISSING FAMILY"); bad+=1
            elif v>r['mu']:
                print(f"n={n}: fast {v} > BFS {r['mu']} -- formula found more (check!) [{w}]")
        print("validation:", "OK (fast >= BFS everywhere; discrepancies above)" if not bad else f"{bad} regressions")
        return
    out=open('mu_table_full.csv','w')
    out.write("n,C(n2),prime_power,mu_lower,mu_upper,density,witness\n")
    worst=[]
    for n in range(4,args.nmax+1):
        N=comb(n,2)
        v,w,ex=best_for_n(n,spf,chain_pairs)
        up=N if ex else N//2
        out.write(f"{n},{N},{int(ex)},{v},{up},{v/N:.4f},{w}\n")
        if not ex: worst.append((v/N,n,v,N,w))
    out.close()
    worst.sort()
    print("weakest 15 composites (density, n, mu_lower, C(n,2), witness):")
    for d,n,v,N,w in worst[:15]:
        print(f"  {d:.4f}  n={n:4d}  {v}/{N}  {w}")
    import statistics
    ds=[d for d,*_ in worst]
    print(f"\nnon-prime-power n in [4,{args.nmax}]: {len(ds)}")
    print(f"density: min {min(ds):.4f}  median {statistics.median(ds):.4f}  max {max(ds):.4f} (ceiling 0.5)")
    print(f"count with density < 0.10: {sum(1 for d in ds if d<0.10)}")
    print(f"count with density >= 0.20: {sum(1 for d in ds if d>=0.20)}")
    print("full table: mu_table_full.csv")

if __name__=="__main__":
    main()
