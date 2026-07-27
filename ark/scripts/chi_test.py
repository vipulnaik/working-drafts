"""
chi_test.py -- decisive evasiveness test for a fully specified monotone
property, via the top Fourier coefficient / global Euler characteristic.

For downward-closed P on n-vertex graphs let
    S = sum over LABELLED G in P of (-1)^{|E(G)|}.
Then chi(Delta_P) = 1 - S, and S != 0 forces Fourier degree = C(n,2), hence
D(P) = C(n,2): P is EVASIVE.  (S = 0 only means the screen is passed.)

Input: a solution pickle from stage4_fast.py plus the catalog checkpoint.  The
property tested is the MINIMAL monotone extension of the solution's IN set --
i.e. the down-closure of its maximal IN classes ("the skeleton").  IMPORTANT:
a CSP solution constrains only the catalog classes, so it does not determine a
unique property; this tests one canonical extension, not the solution itself.

The full down-closure (all iso classes, NOT just catalog ones) is enumerated by
edge-deletion BFS with nauty canonicalisation -- typically seconds to minutes.

Usage:
  python3 chi_test.py                        # solution1.pkl + ckpt_catalog.pkl
  python3 chi_test.py --solution other.pkl --out skeleton_chi.txt
"""
import argparse, pickle, sys, time
from math import factorial
import networkx as nx, pynauty

ap = argparse.ArgumentParser()
ap.add_argument('--solution', default='solution1.pkl')
ap.add_argument('--catalog', default='ckpt_catalog.pkl')
ap.add_argument('--cap', type=int, default=5_000_000, help='abort if the down-closure exceeds this many classes')
ap.add_argument('--out', default=None)
args = ap.parse_args()

cst = pickle.load(open(args.catalog, 'rb'))
reps = cst['cat'].reps
sol = pickle.load(open(args.solution, 'rb'))['x']
n = reps[0].number_of_nodes(); F = factorial(n)

def cert(G):
    return pynauty.certificate(pynauty.Graph(n, adjacency_dict={v: list(G.neighbors(v)) for v in range(n)}))
def autorder(G):
    g = pynauty.autgrp(pynauty.Graph(n, adjacency_dict={v: list(G.neighbors(v)) for v in range(n)}))
    return round(g[1] * 10 ** g[2])          # mantissa * 10^exp, rounded once

IN = [i for i in range(len(reps)) if sol[i] == 1]
# maximal IN classes = generators of the minimal extension
gens = []
for i in IN:
    e = reps[i].number_of_edges()
    if not any(j != i and sol[j] == 1 and reps[j].number_of_edges() > e and
               nx.algorithms.isomorphism.GraphMatcher(reps[j], reps[i]).subgraph_is_monomorphic()
               for j in IN):
        gens.append(reps[i])
print(f"n = {n}; solution has {len(IN)} IN catalog classes; "
      f"{len(gens)} maximal generators, edges {sorted(g.number_of_edges() for g in gens)}")

seen = {}; frontier = {}
for g in gens:
    c = cert(g); seen[c] = g; frontier[c] = g
S = 0; t0 = time.time()
for c, G in seen.items():
    S += (-1) ** G.number_of_edges() * (F // autorder(G))
level = 0
while frontier:
    level += 1; nxt = {}
    for c, H in frontier.items():
        for e in list(H.edges()):
            K = H.copy(); K.remove_edge(*e); ck = cert(K)
            if ck not in seen and ck not in nxt: nxt[ck] = K
    for ck, K in nxt.items():
        seen[ck] = K
        S += (-1) ** K.number_of_edges() * (F // autorder(K))
    frontier = nxt
    print(f"  level {level}: +{len(nxt)}, total {len(seen)}, {time.time()-t0:.0f}s", flush=True)
    if len(seen) > args.cap:
        sys.exit("ABORT: down-closure exceeds --cap")

lines = []
def out(s):
    print(s); lines.append(s)
out(f"down-closure: {len(seen)} iso classes, "
    f"{sum(F // autorder(G) for G in seen.values())} labelled graphs")
out(f"S = {S}")
out(f"chi(Delta_P) = 1 - S = {1 - S}")
if S != 0:
    out(f"VERDICT: EVASIVE -- Fourier degree = C({n},2), so D(P) = C({n},2).")
    out("(This kills this canonical extension; other extensions of the same "
        "CSP solution remain untested.)")
else:
    out("VERDICT: chi = 1, contractibility screen PASSED -- "
        "candidate survives; escalate to adversary search.")
# sanity assertions
empty = nx.Graph(); empty.add_nodes_from(range(n))
assert cert(empty) in seen, "down-closure lacks the empty graph"
full = nx.complete_graph(n)
assert cert(full) not in seen, "down-closure contains K_n (property is trivial)"
out("sanity: contains empty graph, excludes K_n (nontrivial) -- OK")
if args.out:
    open(args.out, 'w').write('\n'.join(lines) + '\n')
