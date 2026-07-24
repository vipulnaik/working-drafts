# Signed sums over geng streams: A = sum (-1)^e * 10!/|Aut| over classes
# passing a clique-bound filter.  Usage: geng ... | python3 g6sum.py MAXCLIQUE
import sys, math, itertools
import pynauty
maxclq=int(sys.argv[1])   # keep graphs with clique number < maxclq+1, i.e. K_{maxclq+1}-free
f10=math.factorial(10)
pairs=list(itertools.combinations(range(10),2))
def parse_g6(line):
    b=line.strip().encode()
    assert b[0]-63==10
    bits=[]
    for ch in b[1:]:
        v=ch-63
        for i in range(5,-1,-1): bits.append((v>>i)&1)
    adjmask=[0]*10; e=0
    idx=0
    for j in range(1,10):
        for i in range(j):
            if bits[idx]:
                adjmask[i]|=1<<j; adjmask[j]|=1<<i; e+=1
            idx+=1
    return adjmask,e
def clique_ge(adjmask,k):
    # simple branch and bound on bitmasks
    def ext(cands, need):
        if need==0: return True
        while cands:
            v=(cands & -cands).bit_length()-1
            cands&=cands-1
            if ext(cands & adjmask[v], need-1): return True
        return False
    return ext((1<<10)-1, k)
A=0; kept=0; tot=0
for line in sys.stdin:
    if not line.strip(): continue
    tot+=1
    if tot%1000000==0:
        print(f"progress: {tot} read, {kept} kept, A so far {A}", flush=True)
    adjmask,e=parse_g6(line)
    if clique_ge(adjmask,maxclq+1): continue
    kept+=1
    g=pynauty.Graph(10, adjacency_dict={v:[w for w in range(10) if adjmask[v]>>w&1] for v in range(10)})
    _,order,_,_,_=pynauty.autgrp(g)
    A += (-1 if e%2 else 1)*round(f10/order)
print(f"total classes read: {tot}  K{maxclq+1}-free kept: {kept}  A = {A}")
