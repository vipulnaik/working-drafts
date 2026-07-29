"""
Smith-theory constraints for the ARK CSP at n=10.

Non-evasive P => Delta_P collapsible => F_p-acyclic for all p.  Smith: for any
p-subgroup Q <= Sym(10), the fixed complex Delta_P^Q (faces = subsets S of Q's
u-orbitals with union(S) in P) must be F_p-acyclic: ALL reduced homology over
F_p vanishes (in particular nonempty with a vertex).

For each of the 18 admissible patterns (which pin membership on the original
catalog), we ask: does ANY monotone assignment of the new union classes
satisfy F_p-acyclicity for every p-group in the Smith battery?  If not, the
pattern is killed GLOBALLY (every realization, not just the minimal one).
"""
import sys, itertools
from math import comb
import networkx as nx
sys.path.insert(0,'/home/claude')
import ark_intersect as ai
from oliver_mu import candidate_groups

# ---------------- p-groups and their orbitals ----------------
def orbits_on_pairs(gens, n=10):
    pairs=list(itertools.combinations(range(n),2))
    pidx={p:i for i,p in enumerate(pairs)}
    seen=[False]*len(pairs); orbs=[]
    for i,st in enumerate(pairs):
        if seen[i]: continue
        orb={st}; seen[i]=True; fr=[st]
        while fr:
            nf=[]
            for (u,v) in fr:
                for g in gens:
                    a,b=g[u],g[v]
                    pr=(a,b) if a<b else (b,a)
                    j=pidx[pr]
                    if not seen[j]:
                        seen[j]=True; orb.add(pr); nf.append(pr)
            fr=nf
        orbs.append(frozenset(orb))
    return orbs

def perm_from_map(m,n=10):
    return tuple(m.get(i,i) for i in range(n))

# Z5^2: two blocks of 5, independent translations
g1=perm_from_map({i:(i+1)%5 for i in range(5)})
g2=perm_from_map({5+i:5+(i+1)%5 for i in range(5)})
Z55=dict(name='Z5^2', p=5, gens=[g1,g2])
# Z9: 9-cycle on 0..8, fixed point 9
g3=perm_from_map({i:(i+1)%9 for i in range(9)})
Z9=dict(name='Z9', p=3, gens=[g3])

SMITH=[Z55,Z9]
for Q in SMITH:
    Q['orbs']=orbits_on_pairs(Q['gens'])
    Q['t']=len(Q['orbs'])
    print(Q['name'],": t =",Q['t'],"orbital sizes",sorted(len(o) for o in Q['orbs']))

# ---------------- F_p homology ----------------
def fp_acyclic(faces, t, p):
    """faces: downward-closed set of frozensets over range(t), containing
    frozenset() (the empty graph is in P).  True iff all reduced F_p homology
    vanishes.  Cardinality convention: card-c faces have dim c-1; the empty
    face is the (-1)-dim face, so the augmentation is boundary_1."""
    if frozenset() not in faces: return False
    byd={}
    for F in faces: byd.setdefault(len(F),[]).append(F)
    maxc=max(byd)
    def rank_mod_p(rows):
        rows=[dict(r) for r in rows]
        rank=0; used={}
        for r in rows:
            r={c:v%p for c,v in r.items() if v%p}
            while r:
                piv=min(r)
                if piv in used:
                    pr=used[piv]; f=(r[piv]*pow(pr[piv],p-2,p))%p
                    for c,v in pr.items():
                        r[c]=(r.get(c,0)-f*v)%p
                        if r[c]==0: del r[c]
                else:
                    used[piv]=r; rank+=1; break
        return rank
    ranks={0:0}
    for c in range(1,maxc+1):
        Fc=sorted(byd.get(c,[]),key=sorted)
        Fcm=sorted(byd.get(c-1,[]),key=sorted)
        idx={F:i for i,F in enumerate(Fcm)}
        rows=[]
        for F in Fc:
            r={}; sl=sorted(F)
            for j,v in enumerate(sl):
                r[idx[frozenset(F-{v})]]=(-1)**j
            rows.append(r)
        ranks[c]=rank_mod_p(rows)
    for c in range(0,maxc+1):
        b=len(byd.get(c,[]))-ranks.get(c,0)-ranks.get(c+1,0)
        if b!=0: return False
    return True

# quick self-tests
full=set()
for r in range(0,4):
    for S in itertools.combinations(range(3),r): full.add(frozenset(S))
assert fp_acyclic(full,3,5)            # simplex: acyclic
circ={frozenset(),frozenset([0]),frozenset([1]),frozenset([2]),
      frozenset([0,1]),frozenset([1,2]),frozenset([0,2])}
assert not fp_acyclic(circ,3,5)        # boundary of triangle: H1 != 0
assert not fp_acyclic({frozenset()},3,5)  # just empty face: H_{-1} != 0
two_pts={frozenset(),frozenset([0]),frozenset([1])}
assert not fp_acyclic(two_pts,3,5)     # two points: H0-tilde != 0
cone={frozenset(),frozenset([0]),frozenset([1]),frozenset([0,1])}
assert fp_acyclic(cone,3,5)            # edge: contractible

# p-DEPENDENCE.  Every test above uses p=5 on torsion-free complexes, so a bug
# that ignored p entirely would pass all of them -- while section 7.2's whole
# "one prime versus all primes" apparatus depends on this function actually
# distinguishing primes.  A triangulated RP^2 has H1 = Z/2, so it is F_p-acyclic
# for odd p and NOT for p=2.
_RP2=[(0,1,2),(0,2,3),(0,3,4),(0,4,5),(0,1,5),(1,2,4),(2,3,5),(1,3,4),(1,3,5),(2,4,5)]
_f=set()
for _t in _RP2:
    for _r in range(4):
        for _S in itertools.combinations(_t,_r): _f.add(frozenset(_S))
assert not fp_acyclic(_f,6,2), "RP^2 must NOT be F_2-acyclic (H1 = Z/2)"
for _p in (3,5,7):
    assert fp_acyclic(_f,6,_p), f"RP^2 must be F_{_p}-acyclic"

# Cones are acyclic over every p -- section 8.5's survival mechanism, so a
# regression here would silently invalidate the one-sidedness analysis.
_c={frozenset()}
for _g in (frozenset([0,1,2]),frozenset([0,3]),frozenset([0,2,4])):
    for _r in range(len(_g)+1):
        for _S in itertools.combinations(sorted(_g),_r): _c.add(frozenset(_S))
for _p in (2,3,5,7):
    assert fp_acyclic(_c,5,_p), "a cone must be acyclic over every p"
print("homology self-tests passed (including p-dependence and cones)")
