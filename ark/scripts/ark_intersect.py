"""
Engstrom-style intersection computation for the ARK conjecture at composite n.

For a hypothetical non-evasive nontrivial monotone property P on [n] and EVERY
Oliver group Gamma with top prime q:  chi((P)_Gamma) == 1 (mod q); if the top
layer is trivial (cyclic-extension-of-p-group), q is free, so chi == 1 exactly.
Orbitals are edge-disjoint, so subsets of orbitals biject with union graphs;
P's membership depends only on iso class and is closed downward under
subgraph-monomorphism.  We solve the joint CSP over membership bits of all
union-graph iso classes across a battery of groups:
  (a) empty graph in P; any union covering E(K_n) not in P (nontriviality);
  (b) monotone under monomorphism order;
  (c) chi condition per group.
UNSAT => ARK proved unconditionally at n by this battery.
SAT   => residual counterexample search space; report backbone.
"""
import sys
from itertools import combinations
from math import comb
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
sys.path.insert(0, '/home/claude')
from oliver_mu import candidate_groups, prime_power

def u_orbitals(group):
    n = group.n; gens = group.generators
    pairs = list(combinations(range(n), 2))
    pidx = {pr: i for i, pr in enumerate(pairs)}
    seen = [False]*len(pairs); orbitals = []
    for i, start in enumerate(pairs):
        if seen[i]: continue
        orb = {start}; seen[i] = True; frontier = [start]
        while frontier:
            nf = []
            for (u, v) in frontier:
                for g in gens:
                    a, b = g[u], g[v]
                    pr = (a, b) if a < b else (b, a)
                    j = pidx[pr]
                    if not seen[j]:
                        seen[j] = True; orb.add(pr); nf.append(pr)
            frontier = nf
        orbitals.append(frozenset(orb))
    return orbitals

def top_prime(group):
    qs = set()
    for part in group.desc_parts:
        if part.startswith('F') and ':C' in part:
            tw = int(part.split(':C')[1])
            if tw > 1: qs.add(prime_power(tw)[0])
    if not qs: return None
    assert len(qs) == 1
    return qs.pop()

def edges_to_graph(es, n):
    G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(es); return G

class Catalog:
    def __init__(self, n): self.n=n; self.reps=[]; self.invs=[]
    @staticmethod
    def inv(G):
        return (G.number_of_edges(), tuple(sorted(d for _,d in G.degree())),
                sum(nx.triangles(G).values())//3)
    def classify(self, es):
        G = edges_to_graph(es, self.n); iv = self.inv(G)
        for i,(H,hv) in enumerate(zip(self.reps,self.invs)):
            if hv==iv and nx.is_isomorphic(G,H): return i
        self.reps.append(G); self.invs.append(iv); return len(self.reps)-1

def _vf2mono(H, G):
    gm = GraphMatcher(G,H)
    if hasattr(gm,'subgraph_is_monomorphic'): return gm.subgraph_is_monomorphic()
    return any(True for _ in gm.subgraph_monomorphisms_iter())

def mono(H, G):
    if H.number_of_edges()==0: return True
    if H.number_of_edges()>G.number_of_edges(): return False
    dH=sorted((d for _,d in H.degree()),reverse=True)
    dG=sorted((d for _,d in G.degree()),reverse=True)
    if any(h>g for h,g in zip(dH,dG)): return False
    n = H.number_of_nodes()
    # exact complement trick: sigma(E_H) subset E_G  <=>  sigma^{-1}(E_Gc) subset E_Hc
    # use whichever pattern is sparser for VF2
    if H.number_of_edges() > n*(n-1)//4:
        Gc = nx.complement(G); Hc = nx.complement(H)
        if Gc.number_of_edges() < H.number_of_edges():
            Gc.add_nodes_from(range(n)); Hc.add_nodes_from(range(n))
            return _vf2mono(Gc, Hc)
    return _vf2mono(H, G)

def chi(t, member):
    c=0
    for m in range(1,1<<t):
        if member[m]: c += 1 if (bin(m).count('1')%2==1) else -1
    return c

def analyze(n, num_groups=5, max_orbitals=6, cap=500000):
    N=comb(n,2)
    print(f"\n{'='*66}\n  n = {n}   C(n,2) = {N}\n{'='*66}")
    scored=[]
    for g in candidate_groups(n):
        orbs=u_orbitals(g)
        if len(orbs)>max_orbitals: continue
        scored.append((min(len(o) for o in orbs), len(orbs), g, orbs))
    scored.sort(key=lambda x:(-x[0],x[1]))
    chosen=[]; sigs=set()
    for m,t,g,orbs in scored:
        key=(tuple(sorted(len(o) for o in orbs)), g.description())
        if key in sigs: continue
        sigs.add(key); chosen.append((m,g,orbs))
        if len(chosen)==num_groups: break
    cat=Catalog(n); gdata=[]
    for m,g,orbs in chosen:
        t=len(orbs); q=top_prime(g)
        uc={}
        for mask in range(1<<t):
            E=set()
            for i in range(t):
                if mask>>i&1: E|=orbs[i]
            uc[mask]=cat.classify(E)
        gdata.append(dict(desc=g.description(),t=t,q=q,uc=uc))
        print(f"  Gamma: {g.description():42s} t={t} m*={m:4d} sizes={sorted(len(o) for o in orbs)} chi==1 "+(f"mod {q}" if q else "(exact)"))
    V=len(cat.reps)
    print(f"  distinct union-graph iso classes: {V}")
    order=[[False]*V for _ in range(V)]
    for a in range(V):
        for b in range(V):
            if a==b: order[a][b]=True
            elif cat.reps[a].number_of_edges()<=cat.reps[b].number_of_edges():
                order[a][b]=mono(cat.reps[a],cat.reps[b])
    x=[None]*V
    x[cat.classify(set())]=1
    for i in range(V):
        if cat.reps[i].number_of_edges()==N: x[i]=0
    def prop_all():
        ch=True
        while ch:
            ch=False
            for g_ in range(V):
                if x[g_]==1:
                    for h_ in range(V):
                        if order[h_][g_]:
                            if x[h_]==0: return False
                            if x[h_] is None: x[h_]=1; ch=True
                elif x[g_]==0:
                    for h_ in range(V):
                        if order[g_][h_]:
                            if x[h_]==1: return False
                            if x[h_] is None: x[h_]=0; ch=True
        return True
    if not prop_all():
        print("  UNSAT at setup => ARK PROVED unconditionally at this n."); return 0
    sols=[0]; seen=[set() for _ in range(V)]
    unknowns=[i for i in range(V) if x[i] is None]
    unknowns.sort(key=lambda i:-cat.reps[i].number_of_edges())
    def gchk(final):
        for gd in gdata:
            t,q,uc=gd['t'],gd['q'],gd['uc']
            vals=[x[uc[m]] for m in range(1,1<<t)]
            if any(v is None for v in vals):
                if final: return False
                continue
            member=[False]*(1<<t)
            for m in range(1,1<<t): member[m]=(x[uc[m]]==1)
            c=chi(t,member)
            if q is None:
                if c!=1: return False
            elif c%q!=1%q: return False
        return True
    def dfs(k):
        if sols[0]>=cap: return
        if not gchk(False): return
        if k==len(unknowns):
            if gchk(True):
                sols[0]+=1
                for i in range(V): seen[i].add(x[i])
            return
        i=unknowns[k]
        if x[i] is not None: dfs(k+1); return
        snap=list(x)
        for val in (0,1):
            x[i]=val; ok=True
            if val==1:
                for h_ in range(V):
                    if order[h_][i]:
                        if x[h_]==0: ok=False; break
                        if x[h_] is None: x[h_]=1
            else:
                for g_ in range(V):
                    if order[i][g_]:
                        if x[g_]==1: ok=False; break
                        if x[g_] is None: x[g_]=0
            if ok: dfs(k+1)
            x[:]=snap
    dfs(0)
    if sols[0]==0:
        print(f"\n  RESULT: UNSAT. ARK holds UNCONDITIONALLY at n={n} (this battery).")
    else:
        capped=" (cap reached)" if sols[0]>=cap else ""
        print(f"\n  RESULT: SAT, {sols[0]} admissible membership patterns{capped}.")
        fin=[i for i in range(V) if seen[i]=={1}]
        fout=[i for i in range(V) if seen[i]=={0}]
        free=[i for i in range(V) if len(seen[i])==2]
        ec=lambda idxs: sorted(cat.reps[i].number_of_edges() for i in idxs)
        print(f"  forced IN : {len(fin)} classes, edges {ec(fin)}")
        print(f"  forced OUT: {len(fout)} classes, edges {ec(fout)}")
        print(f"  free      : {len(free)} classes, edges {ec(free)}")
        big=[cat.reps[i].number_of_edges() for i in fin]
        if big:
            mx=max(big)
            print(f"  ==> any counterexample MUST contain a specific {mx}-edge graph; density >= {mx/N:.3f}")
    return sols[0]

if __name__=="__main__":
    for n in [10, 12, 15, 18]:
        analyze(n)
