# Signed weights of connected bipartite graphs with k=8..10 vertices,
# parts a,b<=5, and vertex cover tau<=3, via Koenig cover-structure enumeration.
# Output: dict (k,(a,b),tau) -> signed weight k!/|Aut| summed over classes.
import itertools, math
import pynauty
import networkx as nx

def max_matching_bip(G):
    return len(nx.algorithms.matching.max_weight_matching(G, maxcardinality=True))

results={}
seen=set()
for cA in range(0,4):
    for cB in range(0,4-cA):
        c=cA+cB
        if c==0: continue
        for nA in range(0,6-cA):
            for nB in range(0,6-cB):
                a=cA+nA; b=cB+nB; k=a+b
                if k<8 or a>5 or b>5: continue
                # types
                tA=list(range(1,1<<cB)) if cB>0 else []   # nonempty nbhd in C_B
                tB=list(range(1,1<<cA)) if cA>0 else []
                if nA>0 and not tA: continue
                if nB>0 and not tB: continue
                for msA in itertools.combinations_with_replacement(tA,nA) if nA>0 else [()]:
                    for msB in itertools.combinations_with_replacement(tB,nB) if nB>0 else [()]:
                        for inner in range(1<<(cA*cB)):
                            # vertices: A side: 0..a-1 (cover first cA), B side: a..a+b-1 (cover first cB)
                            G=nx.Graph(); G.add_nodes_from(range(k))
                            for i in range(cA):
                                for j in range(cB):
                                    if inner>>(i*cB+j)&1: G.add_edge(i,a+j)
                            for idx,t in enumerate(msA):
                                u=cA+idx
                                for j in range(cB):
                                    if t>>j&1: G.add_edge(u,a+j)
                            for idx,t in enumerate(msB):
                                v=a+cB+idx
                                for i in range(cA):
                                    if t>>i&1: G.add_edge(v,i)
                            if not nx.is_connected(G): continue
                            g=pynauty.Graph(k,adjacency_dict={v:sorted(G.neighbors(v)) for v in range(k)})
                            cert=pynauty.certificate(g)
                            if (k,cert) in seen: continue
                            seen.add((k,cert))
                            tau=max_matching_bip(G)
                            if tau>3: continue
                            _,order,_,_,_=pynauty.autgrp(g)
                            e=G.number_of_edges()
                            w=(-1 if e%2 else 1)*round(math.factorial(k)/order)
                            key=(k,(min(a,b),max(a,b)),tau)
                            results[key]=results.get(key,0)+w
print("big bipartite nu<=3 weights:")
for key in sorted(results):
    print(" ",key,results[key])
import pickle; pickle.dump(results,open('bigbip_nu.pkl','wb'))
