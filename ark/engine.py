"""
Exact chi computation for monotone closures with component-decomposable
membership predicates, via the exponential formula.

A(P) = sum_{labeled G on [10] in P} (-1)^{e(G)},  chi(Delta_P) = 1 - A(P).
For P whose membership depends only on the multiset of connected-component
features (+ isolated vertex count), A(P) = sum over component structures:
   10!/(prod_f k_f!^{m_f} m_f!) * prod_f W_f^{m_f} * [pred]
where W_f = signed count of labeled connected graphs on [k_f] with feature f.
Features (for k <= 7): (k, alpha, tau=k-alpha, bipartition {a,b} or None,
shape in {V,E,P,C5,O}).  All connected components of every predicate used here
have <= 7 vertices (K7-cap or finer), except tau-threshold predicates handled
separately in tau_small.py.
"""
import itertools, math
from functools import lru_cache

def build_features(kmax=7):
    feats = {}   # feature tuple -> signed weight W_f
    for k in range(1, kmax+1):
        pairs = list(itertools.combinations(range(k),2))
        np_ = len(pairs)
        # precompute subset independence masks: for each vertex-subset S (bitmask),
        # the pair-bitmask of pairs inside S
        within = [0]*(1<<k)
        for S in range(1<<k):
            m=0
            for pi,(a,b) in enumerate(pairs):
                if (S>>a&1) and (S>>b&1): m|=1<<pi
            within[S]=m
        popc = [bin(S).count('1') for S in range(1<<k)]
        subsets_by_size = sorted(range(1<<k), key=lambda S:-popc[S])
        for em in range(1<<np_):
            # adjacency
            adj=[0]*k
            for pi,(a,b) in enumerate(pairs):
                if em>>pi&1:
                    adj[a]|=1<<b; adj[b]|=1<<a
            # connectivity (BFS) + 2-coloring
            if k==1:
                conn=True; color=[0]
            else:
                seen=1; frontier=[0]; color=[-1]*k; color[0]=0; bip=True
                while frontier:
                    nf=[]
                    for v in frontier:
                        av=adj[v]
                        while av:
                            w=(av & -av).bit_length()-1; av&=av-1
                            if not (seen>>w&1):
                                seen|=1<<w; color[w]=1-color[v]; nf.append(w)
                            elif color[w]==color[v]:
                                bip=False
                    frontier=nf
                conn = (seen == (1<<k)-1)
            if not conn: continue
            e = popc[em] if False else bin(em).count('1')
            # alpha: largest S with within[S]&em==0
            alpha=0
            for S in subsets_by_size:
                if popc[S]<=alpha: break
                if within[S] & em == 0:
                    alpha=popc[S]; break
            tau = k - alpha
            # bipartition part sizes
            if k==1:
                bip=True
            if bip:
                a=sum(1 for c in color if c==0); b=k-a
                bp=(min(a,b),max(a,b))
            else:
                bp=None
            # shape
            degs=sorted(bin(a2).count('1') for a2 in adj)
            if k==1: shape='V'
            elif k==2: shape='E'
            elif degs[-1]<=2:
                if degs[0]==1: shape='P'      # path
                elif k==5 and degs[0]==2: shape='C5'
                else: shape='O'               # longer cycle etc.
            else: shape='O'
            f=(k,alpha,tau,bp,shape)
            feats[f]=feats.get(f,0)+(-1 if e%2 else 1)
    # drop zero-weight features
    return {f:w for f,w in feats.items() if w!=0}

FEATS = build_features()
FLIST = sorted(FEATS.items(), key=lambda t:(t[0][0],t[0][1],t[0][2],t[0][3] or (-1,-1),t[0][4]))
N = 10
FACT = [math.factorial(i) for i in range(N+1)]

def A_of(pred, allow=None):
    """A(P) for predicate pred(multiset) where multiset is a list of
    (feature, count); isolated vertices are feature k=1 entries implicitly
    (the (1,1,0,(0,1),'V') feature has W=1 and is included in FLIST).
    allow(f): quick per-component filter (None = allow all)."""
    flist = [(f,w) for f,w in FLIST if allow is None or allow(f)]
    from fractions import Fraction
    result=[Fraction(0)]
    def dfs2(idx, used, coeff, wprod, chosen):
        if idx==len(flist):
            if used!=N: return
            if not pred(chosen): return
            result[0]+=coeff*wprod
            return
        f,w=flist[idx]; k=f[0]
        m=0
        while used+m*k<=N:
            c2 = coeff/ (Fraction(FACT[k])**m * FACT[m])
            if m>0: chosen.append((f,m))
            dfs2(idx+1, used+m*k, c2, wprod*(w**m), chosen)
            if m>0: chosen.pop()
            m+=1
    dfs2(0,0,Fraction(FACT[N]),1,[])
    assert result[0].denominator==1
    return int(result[0])

# ---------- packing helpers on chosen = list of ((k,alpha,tau,bp,shape), m) ----

def sizes_pack(chosen, bins):
    """Nontrivial components' sizes must pack into bins (list of capacities);
    size-1 components are free filler. Returns True/False (exact DP)."""
    items=[]
    for (f,m) in chosen:
        k=f[0]
        if k>=2: items += [k]*m
    # DP over bin loads
    states={tuple([0]*len(bins))}
    for it in items:
        ns=set()
        for st in states:
            for i,cap in enumerate(bins):
                if st[i]+it<=cap:
                    l=list(st); l[i]+=it; ns.add(tuple(sorted(l)) if len(set(bins))==1 else tuple(l))
        states=ns
        if not states: return False
    return bool(states)

def bip_pack(chosen, capA, capB):
    """All components bipartite; orient each part-pair into (A,B) with loads
    <= caps. Size-1 comps are (1,0) fillers (free). Exact DP on side-A load."""
    loadpairs=[]
    for (f,m) in chosen:
        k,al,ta,bp,sh=f
        if bp is None: return False
        a,b=bp
        if k==1: continue
        loadpairs += [(a,b)]*m
    states={(0,0)}
    for (a,b) in loadpairs:
        ns=set()
        for (x,y) in states:
            if x+a<=capA and y+b<=capB: ns.add((x+a,y+b))
            if x+b<=capA and y+a<=capB: ns.add((x+b,y+a))
        states=ns
        if not states: return False
    return True

def support_le(chosen, cap):
    s=sum(f[0]*m for (f,m) in chosen if f[0]>=2)
    return s<=cap

def all_shapes(chosen, okshapes):
    return all(f[4] in okshapes or f[0]==1 for (f,m) in chosen)

def max_deg_le1(chosen):
    return all(f[0]<=2 for (f,m) in chosen)

def tau_sum(chosen):
    return sum(f[2]*m for (f,m) in chosen)

def alpha_total(chosen):
    # alpha of whole graph = sum over components (incl isolated k=1: alpha=1)
    return sum(f[1]*m for (f,m) in chosen)

if __name__=="__main__":
    # validations
    A = A_of(lambda ch: max_deg_le1(ch))
    print("closure(M5) 'max deg<=1':  A =", A, " chi =", 1-A, " (expect chi=-1215)")
    A = A_of(lambda ch: support_le(ch,7))
    print("closure(K7) 'support<=7':  A =", A, " chi =", 1-A, " (expect chi=-243)")
    A = A_of(lambda ch: support_le(ch,5))
    print("closure(K5) 'support<=5':  A =", A, " chi =", 1-A)
    A = A_of(lambda ch: support_le(ch,3))
    print("closure(K3) 'support<=3':  A =", A, " chi =", 1-A)
