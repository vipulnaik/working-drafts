# Exact chi(P_low) per admissible pattern at n=10, via inclusion-exclusion over
# generator closures, with component-multiset predicates evaluated by the
# exponential formula.  Big bipartite components (k=8..10) use EGF weights.
import sys, math
from fractions import Fraction
sys.path.insert(0,'/home/claude')
from engine import FEATS, N, FACT
from bigbip import n_ab

# ---- extended feature list ----
EXT=[]
for f,w in sorted(FEATS.items(), key=lambda t:(t[0][0],t[0][1],t[0][2],t[0][3] or (-1,-1),t[0][4])):
    EXT.append((f,w))
for k in range(8,11):
    for a in range(1,k//2+1):
        b=k-a
        if b>9: continue
        w=n_ab(a,b)
        if w!=0:
            EXT.append(((k,None,None,(a,b),'BIGBIP'),w))

def A_of(pred):
    result=[Fraction(0)]
    L=len(EXT)
    def dfs(idx, used, coeff, wprod, chosen):
        if used==N:
            if pred(chosen): result[0]+=coeff*wprod
            return
        if idx==L: return
        f,w=EXT[idx]; k=f[0]
        # skip
        dfs(idx+1, used, coeff, wprod, chosen)
        m=1
        while used+m*k<=N:
            c2=coeff/(Fraction(FACT[k])**m*FACT[m])
            chosen.append((f,m))
            dfs(idx+1, used+m*k, c2, wprod*(w**m), chosen)
            chosen.pop()
            m+=1
    dfs(0,0,Fraction(FACT[N]),1,[])
    assert result[0].denominator==1
    return int(result[0])

# ---- predicate primitives on chosen=[(feature,mult)] ----
def nobig(ch): return all(f[4]!='BIGBIP' for f,m in ch)
def maxdeg1(ch): return all(f[0]<=2 for f,m in ch)
def support_le(ch,c): return sum(f[0]*m for f,m in ch if f[0]>=2)<=c
def sizes_pack(ch,bins):
    items=[]
    for f,m in ch:
        if f[0]>=2: items+=[f[0]]*m
    states={tuple([0]*len(bins))}
    for it in items:
        ns=set()
        for st in states:
            for i in range(len(bins)):
                if st[i]+it<=bins[i]:
                    l=list(st); l[i]+=it
                    ns.add(tuple(sorted(zip(bins,l))) if False else tuple(l))
        states=ns
        if not states: return False
    return True
def bip_pack(ch,capA,capB):
    lp=[]
    for f,m in ch:
        bp=f[3]
        if f[0]==1: continue
        if bp is None: return False
        lp+=[bp]*m
    states={(0,0)}
    for (a,b) in lp:
        ns=set()
        for (x,y) in states:
            if x+a<=capA and y+b<=capB: ns.add((x+a,y+b))
            if x+b<=capA and y+a<=capB: ns.add((x+b,y+a))
        states=ns
        if not states: return False
    return True
def alpha_total(ch):
    s=0
    for f,m in ch:
        if f[1] is None: return None
        s+=f[1]*m
    return s
def shapes_pack_C5C5(ch):
    # comps must be vertices/edges/paths (k<=5) or C5; sizes pack into [5,5]
    for f,m in ch:
        k,al,ta,bp,sh=f
        if k==1: continue
        if sh not in ('E','P','C5'): return False
        if k>5: return False
    return sizes_pack(ch,[5,5])

# ---- named closure predicates ----
P_M5   = lambda ch: maxdeg1(ch)
P_K3   = lambda ch: support_le(ch,3)
P_K5K5 = lambda ch: sizes_pack(ch,[5,5])
P_K3K7 = lambda ch: sizes_pack(ch,[3,7])
P_K55  = lambda ch: bip_pack(ch,5,5)
P_K37  = lambda ch: bip_pack(ch,3,7)
P_C5C5 = lambda ch: shapes_pack_C5C5(ch)
def P_A7(ch):
    a=alpha_total(ch)
    return a is not None and a>=7
def P_A5(ch):
    a=alpha_total(ch)
    return a is not None and a>=5
# NOTE: P_A7 / P_A5 as multiset predicates are only valid in conjunction with a
# predicate capping components at k<=7 (BIGBIP components have unknown alpha and
# make the conjunction False, correctly, since... they CAN'T appear: any
# conjunct that caps sizes excludes them).  Standalone A(alpha>=m) values are
# computed elsewhere: A7 = 1722 (tau enumeration), A3 = 4425 (geng -t),
# A5 = pending K5-free run.

A7_EXACT = 1722
A3_EXACT = 4425

def AND(*ps): return lambda ch: all(p(ch) for p in ps)

def incl_excl(named, extra_exact=None):
    """named: dict name->predicate for the generators of P_low.
    extra_exact: dict frozenset(names)->exact A value overriding DP (for
    standalone alpha terms).  Returns A(union)."""
    import itertools as it
    names=list(named)
    A=0
    for r in range(1,len(names)+1):
        for S in it.combinations(names,r):
            key=frozenset(S)
            if extra_exact and key in extra_exact:
                val=extra_exact[key]
            else:
                val=A_of(AND(*[named[s] for s in S]))
            A += val if r%2 else -val
    return A

if __name__=="__main__":
    res={}
    print("Computing exact A and chi=1-A for pattern minimal completions...")
    # single-closure sanity values first
    for nm,p in [('K5K5',P_K5K5),('K3K7',P_K3K7),('K55',P_K55),('K37',P_K37),('C5C5',P_C5C5)]:
        a=A_of(p); print(f"  A(closure {nm}) = {a}   chi = {1-a}")
    pats = {
      0: dict(named={'K37':P_K37,'K55':P_K55}),
      1: dict(named={'K3':P_K3,'K55':P_K55}),
      5: dict(named={'K5K5':P_K5K5,'M5':P_M5}),
      6: dict(named={'K3K7':P_K3K7,'K5K5':P_K5K5,'M5':P_M5}),
      7: dict(named={'A7':P_A7,'K5K5':P_K5K5,'M5':P_M5},
              extra={frozenset(['A7']):A7_EXACT}),
      8: dict(named={'A7':P_A7,'K3K7':P_K3K7,'K5K5':P_K5K5,'M5':P_M5},
              extra={frozenset(['A7']):A7_EXACT}),
    }
    for pid,spec in pats.items():
        A=incl_excl(spec['named'], spec.get('extra'))
        print(f"  pattern {pid:2d}: A(P_low) = {A:8d}   chi(P_low) = {1-A:8d}   {'KILLED' if 1-A!=1 else 'chi==1 !!'}")
