"""
adversary.py -- exact evasiveness of a FIXED monotone graph property by
adversary game search over canonical states.

The state after some queries is the pair (L, A): known-present and
known-absent edge sets.  Because the property is S_n-invariant, survivability
depends only on the isomorphism class of the 3-coloured state, so the search
is memoized on a nauty certificate of (L, A) -- the branch-wise symmetry
reduction that turns the game tree into a DAG over iso-classes (~3^C(n,2)/n!
states in general; far fewer for one fixed property with monotone pruning).

Recursion (monotone DECREASING P, i.e. downward closed / given by the
down-closure of generator graphs):
    undetermined(L, A)  =  P(L) and not P(K_n - A)
    survive(L, A)       =  undetermined and for EVERY unqueried e,
                           SOME answer keeps surviving
    base                :  |L| + |A| = N - 1  ->  adversary has forced N
    P evasive  <=>  survive(empty, empty)
For monotone INCREASING P (given by a membership predicate on edge sets),
undetermined(L, A) = (not P(L)) and P(K_n - A); the rest is identical.

Verdicts: EVASIVE / NON-EVASIVE are exact; BUDGET means the node budget was
exhausted (rerun larger -- the memo is persisted to adversary_memo.pkl and
reloaded, so reruns resume most of the work).

Usage:
  python3 adversary.py --demo scorpion --n 6        # validation, increasing
  python3 adversary.py --demo matching --n 6        # validation, decreasing
  python3 adversary.py --skeleton skeleton.pkl --n 10 --budget 50000000
"""
import sys, os, time, pickle, argparse, itertools
import networkx as nx
import pynauty

ap = argparse.ArgumentParser()
ap.add_argument('--n', type=int, required=True)
ap.add_argument('--demo', choices=['scorpion', 'matching'], default=None)
ap.add_argument('--skeleton', default=None,
                help='pickle with g6 dict of generator graphs (decreasing mode)')
ap.add_argument('--budget', type=int, default=10_000_000)
ap.add_argument('--memo-file', default='adversary_memo.pkl')
args = ap.parse_args()

n = args.n
PAIRS = list(itertools.combinations(range(n), 2))
N = len(PAIRS)
BIT = {p: 1 << i for i, p in enumerate(PAIRS)}
FULL = (1 << N) - 1

def log(m):
    line = f"{time.strftime('%H:%M:%S')}  {m}"
    print(line, flush=True)
    with open('adversary.log', 'a') as f: f.write(line + '\n')

# ---------------- state canonicalisation ----------------
# encode (L, A) as a 2n-vertex two-layer graph: layer-0 vertex i and layer-1
# vertex n+i joined by a rung; present edge {u,v} -> (u,v); absent -> (n+u,n+v).
# vertex colouring separates the layers; certificate is the canonical key.
def state_cert(L, A):
    adj = {i: [] for i in range(2 * n)}
    for i in range(n):
        adj[i].append(n + i)
    m = L
    while m:
        b = (m & -m).bit_length() - 1; m &= m - 1
        u, v = PAIRS[b]; adj[u].append(v)
    m = A
    while m:
        b = (m & -m).bit_length() - 1; m &= m - 1
        u, v = PAIRS[b]; adj[n + u].append(n + v)
    g = pynauty.Graph(2 * n, adjacency_dict=adj,
                      vertex_coloring=[set(range(n)), set(range(n, 2 * n))])
    return pynauty.certificate(g)

def graph_cert(E):
    adj = {i: [] for i in range(n)}
    m = E
    while m:
        b = (m & -m).bit_length() - 1; m &= m - 1
        u, v = PAIRS[b]; adj[u].append(v)
    return pynauty.certificate(pynauty.Graph(n, adjacency_dict=adj))

# ---------------- properties ----------------
def edges_to_nx(E):
    G = nx.Graph(); G.add_nodes_from(range(n))
    m = E
    while m:
        b = (m & -m).bit_length() - 1; m &= m - 1
        G.add_edge(*PAIRS[b])
    return G

if args.demo == 'scorpion':
    MODE = 'increasing'
    def P_raw(E):
        adj = [0] * n
        m = E
        while m:
            b = (m & -m).bit_length() - 1; m &= m - 1
            u, v = PAIRS[b]; adj[u] |= 1 << v; adj[v] |= 1 << u
        for b in range(n):
            for s in range(n):
                if s == b: continue
                need = (FULLV := (1 << n) - 1) & ~(1 << b) & ~(1 << s)
                if adj[b] & need != need: continue
                if adj[s] & need: return True
        return False
elif args.demo == 'matching':
    MODE = 'decreasing'
    GENS = [edges_to_nx(sum(BIT[(2 * i, 2 * i + 1)] for i in range(n // 2)))]
    log(f"matching demo: generator = perfect matching on {n} vertices")
elif args.skeleton:
    MODE = 'decreasing'
    sk = pickle.load(open(args.skeleton, 'rb'))
    GENS = [nx.from_graph6_bytes(g6.encode()) for g6 in sk['g6'].values()]
    for G in GENS: G.add_nodes_from(range(n))
    log(f"skeleton: {len(GENS)} generators, edge counts "
        f"{sorted(g.number_of_edges() for g in GENS)}")
else:
    sys.exit("give --demo or --skeleton")

if MODE == 'decreasing':
    GEN_EMAX = max(g.number_of_edges() for g in GENS)
    _pmemo = {}
    def P_raw(E):
        e = bin(E).count('1')
        if e > GEN_EMAX: return False
        if e == 0: return True
        k = graph_cert(E)
        if k in _pmemo: return _pmemo[k]
        G = edges_to_nx(E)
        Gc = G.subgraph([v for v in G if G.degree(v) > 0])
        r = any(nx.algorithms.isomorphism.GraphMatcher(g, G).subgraph_is_monomorphic()
                for g in GENS if g.number_of_edges() >= e)
        _pmemo[k] = r
        return r

def undetermined(L, A):
    if MODE == 'decreasing':
        return P_raw(L) and not P_raw(FULL & ~A)
    return (not P_raw(L)) and P_raw(FULL & ~A)

# ---------------- search ----------------
memo = {}
if os.path.exists(args.memo_file):
    try:
        memo = pickle.load(open(args.memo_file, 'rb'))
        log(f"loaded {len(memo)} memoized states")
    except Exception:
        memo = {}
nodes = [0]; t0 = time.time(); beat = [t0]; out_of_budget = [False]

def survive(L, A, k):
    nodes[0] += 1
    if nodes[0] > args.budget:
        out_of_budget[0] = True; return False
    if time.time() - beat[0] > 30:
        beat[0] = time.time()
        log(f"  ... nodes {nodes[0]}, memo {len(memo)}, depth {k}, "
            f"{nodes[0]/(time.time()-t0):.0f}/s")
        # persist memo periodically so a hard kill loses at most this interval
        pickle.dump(memo, open(args.memo_file + '.tmp', 'wb'))
        os.replace(args.memo_file + '.tmp', args.memo_file)
    if not undetermined(L, A): return False
    if k == N - 1: return True
    key = state_cert(L, A)
    if key in memo: return memo[key]
    res = True
    for i in range(N):
        bit = 1 << i
        if (L | A) & bit: continue
        if not (survive(L | bit, A, k + 1) or survive(L, A | bit, k + 1)):
            res = False; break
        if out_of_budget[0]: return False
    memo[key] = res
    return res

sys.setrecursionlimit(20000)
try:
    r = survive(0, 0, 0)
finally:
    pickle.dump(memo, open(args.memo_file, 'wb'))
verdict = 'BUDGET EXHAUSTED (rerun with larger --budget; memo persisted)' \
          if out_of_budget[0] else ('EVASIVE' if r else 'NON-EVASIVE: a decision tree of depth < C(n,2) exists')
log(f"n={n} N={N}: {verdict}")
log(f"nodes {nodes[0]}, canonical states {len(memo)}, "
    f"P-memo {len(_pmemo) if MODE=='decreasing' else '-'}, {time.time()-t0:.0f}s")
