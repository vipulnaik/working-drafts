# A(alpha>=7) = A(tau<=3) via nauty canonical certificates + group orders.
import itertools, math
import pynauty

def to_pyn(adj):  # adj: dict v->set
    return pynauty.Graph(10, adjacency_dict={v:sorted(adj[v]) for v in range(10)})

seen={}  # certificate -> (edges, autorder)
inner_pairs=[(0,1),(0,2),(1,2)]
cnt=0
for inner in range(8):
    for ms in itertools.combinations_with_replacement(range(8),7):
        adj={v:set() for v in range(10)}
        e=0
        for pi,(a,b) in enumerate(inner_pairs):
            if inner>>pi&1: adj[a].add(b); adj[b].add(a); e+=1
        for i,t in enumerate(ms):
            v=3+i
            for c in range(3):
                if t>>c&1: adj[v].add(c); adj[c].add(v); e+=1
        g=to_pyn(adj)
        cert=pynauty.certificate(g)
        if cert not in seen:
            gens,order,_,_,_=pynauty.autgrp(g)
            seen[cert]=(e,order)
        cnt+=1
print("raw:",cnt," classes:",len(seen))
A=0
f10=math.factorial(10)
for (e,order) in seen.values():
    A += (-1 if e%2 else 1)*round(f10/order)
print("A(alpha>=7) =",A," chi(closure of K3vE7) =",1-A)
