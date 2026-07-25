import sys, itertools, pickle
from math import comb
import networkx as nx
sys.path.insert(0,'/home/claude')
import ark_intersect as ai
from oliver_mu import candidate_groups
from smith import SMITH, fp_acyclic

nn=10
# ---- rebuild original battery + patterns (as in earlier runs) ----
scored=[]
for g in candidate_groups(nn):
    orbs=ai.u_orbitals(g)
    if len(orbs)>6: continue
    scored.append((min(len(o) for o in orbs), len(orbs), g, orbs))
scored.sort(key=lambda x:(-x[0],x[1]))
chosen=[]; sigs=set()
for m,t,g,orbs in scored:
    key=(tuple(sorted(len(o) for o in orbs)), g.description())
    if key in sigs: continue
    sigs.add(key); chosen.append((m,g,orbs))
    if len(chosen)==5: break
cat=ai.Catalog(nn); gdata=[]
for m,g,orbs in chosen:
    t=len(orbs); q=ai.top_prime(g); uc={}
    for mask in range(1<<t):
        E=set()
        for i in range(t):
            if mask>>i&1: E|=orbs[i]
        uc[mask]=cat.classify(E)
    gdata.append(dict(t=t,q=q,uc=uc))
V0=len(cat.reps)
# ---- add Smith groups' union classes ----
for Q in SMITH:
    t=Q['t']; uc={}
    for mask in range(1<<t):
        E=set()
        for i in range(t):
            if mask>>i&1: E|=Q['orbs'][i]
        uc[mask]=cat.classify(E)
    Q['uc']=uc
V=len(cat.reps)
print(f"catalog: {V0} original classes, {V-V0} new, {V} total")

# ---- order matrix ----
order=[[False]*V for _ in range(V)]
for a in range(V):
    for b in range(V):
        if a==b: order[a][b]=True
        elif cat.reps[a].number_of_edges()<=cat.reps[b].number_of_edges():
            order[a][b]=ai.mono(cat.reps[a],cat.reps[b])
print("order matrix done")

# ---- original 18 patterns (re-solve on original variables) ----
x=[None]*V
x[cat.classify(set())]=1
for i in range(V0):
    if cat.reps[i].number_of_edges()==45: x[i]=0
base=list(x)
sols=[]
unknowns=[i for i in range(V0) if base[i] is None]
def gchk(xv, final):
    for gd in gdata:
        t,q,uc=gd['t'],gd['q'],gd['uc']
        if any(xv[uc[mm]] is None for mm in range(1,1<<t)):
            if final: return False
            continue
        c=0
        for mm in range(1,1<<t):
            if xv[uc[mm]]==1: c += 1 if bin(mm).count('1')%2 else -1
        if q is None:
            if c!=1: return False
        elif c%q!=1%q: return False
    return True
def dfs0(k,xv):
    if not gchk(xv,False): return
    if k==len(unknowns):
        if gchk(xv,True): sols.append(list(xv))
        return
    i=unknowns[k]
    if xv[i] is not None: dfs0(k+1,xv); return
    snap=list(xv)
    for val in (0,1):
        xv[i]=val; ok=True
        if val==1:
            for h in range(V0):
                if order[h][i]:
                    if xv[h]==0: ok=False;break
                    if xv[h] is None: xv[h]=1
        else:
            for g_ in range(V0):
                if order[i][g_]:
                    if xv[g_]==1: ok=False;break
                    if xv[g_] is None: xv[g_]=0
        if ok: dfs0(k+1,xv)
        xv[:]=snap
dfs0(0,list(base))
print(f"original patterns: {len(sols)}")

# ---- per pattern: extend with Smith constraints ----
def smith_check(xv, final):
    for Q in SMITH:
        t=Q['t']; uc=Q['uc']
        vals=[xv[uc[mm]] for mm in range(1<<t)]
        if any(v is None for v in vals):
            if final: return False
            continue
        faces={frozenset(i for i in range(t) if mm>>i&1) for mm in range(1<<t) if xv[uc[mm]]==1}
        if not fp_acyclic(faces, t, Q['p']): return False
    return True

results={}
for si,sol in enumerate(sols):
    xv=list(sol)+[None]*(V-V0) if len(sol)<V else list(sol)
    xv=[sol[i] if i<V0 else None for i in range(V)]
    # propagate pinned old bits to new classes via monotonicity
    def prop():
        ch=True
        while ch:
            ch=False
            for g_ in range(V):
                if xv[g_]==1:
                    for h in range(V):
                        if order[h][g_]:
                            if xv[h]==0: return False
                            if xv[h] is None: xv[h]=1; ch=True
                elif xv[g_]==0:
                    for h in range(V):
                        if order[g_][h]:
                            if xv[h]==1: return False
                            if xv[h] is None: xv[h]=0; ch=True
        return True
    if not prop():
        results[si]='KILLED (propagation)'
        print(f"pattern {si:2d}: KILLED at propagation"); continue
    free=[i for i in range(V) if xv[i] is None]
    # order free bits: complete Z5^2's classes first, then Z9's
    prio={}
    for qi,Q in enumerate(SMITH):
        for mm in range(1<<Q['t']):
            prio.setdefault(Q['uc'][mm], qi)
    free.sort(key=lambda i:(prio.get(i,99), -cat.reps[i].number_of_edges()))
    found=[False]
    def dfs(k):
        if found[0]: return
        if not smith_check(xv, False): return
        if k==len(free):
            if smith_check(xv, True) and gchk(xv, True): found[0]=True
            return
        i=free[k]
        if xv[i] is not None: dfs(k+1); return
        snap=list(xv)
        for val in (1,0):
            xv[i]=val; ok=True
            if val==1:
                for h in range(V):
                    if order[h][i]:
                        if xv[h]==0: ok=False;break
                        if xv[h] is None: xv[h]=1
            else:
                for g_ in range(V):
                    if order[i][g_]:
                        if xv[g_]==1: ok=False;break
                        if xv[g_] is None: xv[g_]=0
            if ok: dfs(k+1)
            xv[:]=snap
            if found[0]: return
    dfs(0)
    results[si]='SURVIVES (completion exists)' if found[0] else 'KILLED GLOBALLY'
    print(f"pattern {si:2d}: {results[si]}")

killed=[s for s,v in results.items() if v.startswith('KILLED')]
print(f"\nSMITH BATTERY RESULT: {len(killed)}/18 patterns killed globally: {sorted(killed)}")
if len(killed)==18:
    print("ALL PATTERNS DEAD => the CSP is UNSAT => ARK HOLDS UNCONDITIONALLY AT n=10")
pickle.dump(results,open('smith_results.pkl','wb'))
