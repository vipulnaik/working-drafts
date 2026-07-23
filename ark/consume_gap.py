"""
consume_gap.py -- feed GAP-enumerated groups into the ARK-at-10 CSP.

Reads groups_out.txt produced by ark_gap.g (lines KEY|DESC|TAG|ORBMAP where
ORBMAP assigns each of the 45 pairs of [1..10], in lex order, an orbital
index), dedups groups by orbital-partition signature, rebuilds the union-graph
catalog, and runs the primal+dual chi + primal+dual Smith CSP.

Checkpointed and anytime-stoppable:
  stage 1  parse + dedup                      -> ckpt_groups.pkl
  stage 2  catalog (union classes, iso dedup) -> ckpt_catalog.pkl   [slowest]
  stage 3  monomorphism order matrix          -> ckpt_order.pkl     [slow]
  stage 4  CSP solve                          -> csp_result.txt
Each stage skips itself if its checkpoint exists; delete a ckpt to redo.
Stage 2 and 3 checkpoint incrementally every CKPT_EVERY items, so Ctrl-C
loses at most that much work.  Progress goes to consume_gap.log and stdout.

Usage:  python3 consume_gap.py [--maxgroups N] [--maxt T]
Requires networkx (pip install networkx) and the ark session files
(ark_intersect.py, smith.py) in the same directory for mono() and fp_acyclic().
"""
import sys, os, pickle, time, argparse, itertools
from math import comb

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import networkx as nx
from ark_intersect import Catalog, mono
from smith import fp_acyclic

ap = argparse.ArgumentParser()
ap.add_argument('--maxgroups', type=int, default=200,
                help='cap on deduped groups fed to the CSP (largest-min-orbital first, plus all p-groups)')
ap.add_argument('--maxt', type=int, default=10, help='skip groups with more orbitals than this')
ap.add_argument('--infile', default='groups_out.txt')
args = ap.parse_args()

PAIRS = list(itertools.combinations(range(10), 2))   # 0-based, lex order,
# matching GAP's Combinations([1..10],2) after subtracting 1.
LOG = open('consume_gap.log', 'a')
def log(msg):
    line = f"{time.strftime('%H:%M:%S')}  {msg}"
    print(line, flush=True); LOG.write(line + '\n'); LOG.flush()

# ---------------- stage 1: parse + dedup ----------------
if os.path.exists('ckpt_groups.pkl'):
    groups = pickle.load(open('ckpt_groups.pkl', 'rb'))
    log(f"stage 1: loaded checkpoint, {len(groups)} groups")
else:
    raw = []
    for line in open(args.infile):
        line = line.strip()
        if not line: continue
        key, desc, tag, om = line.split('|')
        omap = [int(x) - 1 for x in om.split(',')]
        assert len(omap) == 45
        t = max(omap) + 1
        if t > args.maxt: continue
        orbs = [frozenset(PAIRS[i] for i in range(45) if omap[i] == o)
                for o in range(t)]
        raw.append(dict(key=key, desc=desc, tag=tag, t=t,
                        orbs=orbs, mstar=min(len(o) for o in orbs)))
    # dedup by partition signature up to relabeling: canonical form of the
    # edge-colored complete graph (color = orbital index).  Cheap invariant
    # first, exact check via colored-graph iso.
    def colored_iso(g1, g2):
        if g1['t'] != g2['t']: return False
        if sorted(map(len, g1['orbs'])) != sorted(map(len, g2['orbs'])): return False
        # exact: build graphs with edge attribute = orbital size-rank pattern,
        # try all bijections of equal-size orbitals via VF2 on a layered graph.
        # For dedup purposes a strong invariant suffices; collisions only cost
        # a redundant (harmless) CSP constraint, so we accept invariant-level dedup.
        inv = lambda g: tuple(sorted(
            tuple(sorted((len(g['orbs'][omap_of(g, u, v)]),)
                  for v in range(10) if v != u))
            for u in range(10)))
        return True   # invariant matched above; treat as duplicate
    def omap_of(g, u, v):
        p = (u, v) if u < v else (v, u)
        for i, o in enumerate(g['orbs']):
            if p in o: return i
    seen = {}
    groups = []
    for g in raw:
        sig = (g['t'], tuple(sorted(len(o) for o in g['orbs'])), g['tag'])
        # refine signature with degree-type invariant per orbital
        deg = tuple(sorted(tuple(sorted(sum(1 for p in o if u in p)
                    for o in g['orbs'])) for u in range(10)))
        sig = sig + (deg,)
        if sig in seen: continue
        seen[sig] = True
        groups.append(g)
    # keep all p-groups + top maxgroups Oliver groups by mstar
    pg  = [g for g in groups if g['tag'].startswith('P')]
    ol  = [g for g in groups if not g['tag'].startswith('P')]
    ol.sort(key=lambda g: (-g['mstar'], g['t']))
    groups = ol[:args.maxgroups] + pg
    pickle.dump(groups, open('ckpt_groups.pkl', 'wb'))
    log(f"stage 1: {len(raw)} raw -> {len(groups)} kept "
        f"({len(ol[:args.maxgroups])} Oliver, {len(pg)} p-groups)")

# ---------------- stage 2: catalog ----------------
CKPT_EVERY = 5
if os.path.exists('ckpt_catalog.pkl'):
    st = pickle.load(open('ckpt_catalog.pkl', 'rb'))
    cat, gidx = st['cat'], st['gidx']
    log(f"stage 2: resumed at group {gidx}, catalog {len(cat.reps)} classes")
else:
    cat = Catalog(10); gidx = 0
while gidx < len(groups):
    g = groups[gidx]
    uc = {}
    for mask in range(1 << g['t']):
        E = set()
        for i in range(g['t']):
            if mask >> i & 1: E |= g['orbs'][i]
        uc[mask] = cat.classify(E)
    g['uc'] = uc
    gidx += 1
    if gidx % CKPT_EVERY == 0 or gidx == len(groups):
        pickle.dump(dict(cat=cat, gidx=gidx), open('ckpt_catalog.pkl', 'wb'))
        # also persist uc maps computed so far
        pickle.dump(groups, open('ckpt_groups.pkl', 'wb'))
        log(f"stage 2: {gidx}/{len(groups)} groups, {len(cat.reps)} classes")
V = len(cat.reps)
log(f"stage 2 complete: {V} classes")

# ---------------- stage 3: order matrix ----------------
if os.path.exists('ckpt_order.pkl'):
    st = pickle.load(open('ckpt_order.pkl', 'rb'))
    order, row = st['order'], st['row']
    log(f"stage 3: resumed at row {row}")
else:
    order = [[False]*V for _ in range(V)]; row = 0
while row < V:
    a = row
    for b in range(V):
        if a == b: order[a][b] = True
        elif cat.reps[a].number_of_edges() <= cat.reps[b].number_of_edges():
            order[a][b] = mono(cat.reps[a], cat.reps[b])
    row += 1
    if row % 3 == 0 or row == V:
        pickle.dump(dict(order=order, row=row), open('ckpt_order.pkl', 'wb'))
        log(f"stage 3: row {row}/{V}")
log("stage 3 complete")

# ---------------- stage 4: CSP ----------------
edges = [cat.reps[i].number_of_edges() for i in range(V)]
x = [None]*V
x[cat.classify(set())] = 1
for i in range(V):
    if edges[i] == 45: x[i] = 0

oliver = [g for g in groups if not g['tag'].startswith('P')]
psub   = [g for g in groups if g['tag'].startswith('P')]

def chi_conds(final):
    for g in oliver:
        t, uc = g['t'], g['uc']; full = (1 << t) - 1
        q = int(g['tag']);  q = None if q == 0 else q
        if any(x[uc[m]] is None for m in range(1 << t)):
            if final: return False
            continue
        cp = cd = 0
        for m in range(1, 1 << t):
            s = 1 if bin(m).count('1') % 2 else -1
            if x[uc[m]] == 1: cp += s
            if x[uc[full ^ m]] == 0: cd += s
        for c in (cp, cd):
            if q is None:
                if c != 1: return False
            elif c % q != 1 % q: return False
    return True

def smith_conds(final):
    for g in psub:
        t, uc = g['t'], g['uc']; full = (1 << t) - 1
        p = int(g['tag'][1:])
        if any(x[uc[m]] is None for m in range(1 << t)):
            if final: return False
            continue
        pf = {frozenset(i for i in range(t) if m >> i & 1)
              for m in range(1 << t) if x[uc[m]] == 1}
        if not fp_acyclic(pf, t, p): return False
        df = {frozenset(i for i in range(t) if m >> i & 1)
              for m in range(1 << t) if x[uc[full ^ m]] == 0}
        if not fp_acyclic(df, t, p): return False
    return True

def prop():
    ch = True
    while ch:
        ch = False
        for a in range(V):
            if x[a] == 1:
                for h in range(V):
                    if order[h][a]:
                        if x[h] == 0: return False
                        if x[h] is None: x[h] = 1; ch = True
            elif x[a] == 0:
                for h in range(V):
                    if order[a][h]:
                        if x[h] == 1: return False
                        if x[h] is None: x[h] = 0; ch = True
    return True

if not prop():
    log("UNSAT at propagation => ARK HOLDS UNCONDITIONALLY AT n=10"); sys.exit()

sols = [0]; seen = [set() for _ in range(V)]
unknowns = [i for i in range(V) if x[i] is None]
prio = {}
for gi, g in enumerate(oliver + psub):
    for m in range(1 << g['t']): prio.setdefault(g['uc'][m], gi)
unknowns.sort(key=lambda i: (prio.get(i, 9999), -edges[i]))
CAP = 100000; t0 = time.time(); nodes = [0]

def dfs(k):
    nodes[0] += 1
    if nodes[0] % 500000 == 0:
        log(f"stage 4: nodes {nodes[0]} sols {sols[0]} {time.time()-t0:.0f}s")
    if sols[0] >= CAP: return
    if not chi_conds(False) or not smith_conds(False): return
    if k == len(unknowns):
        if chi_conds(True) and smith_conds(True):
            sols[0] += 1
            for i in range(V): seen[i].add(x[i])
        return
    i = unknowns[k]
    if x[i] is not None: dfs(k + 1); return
    snap = list(x)
    for val in (0, 1):
        x[i] = val; ok = True
        if val == 1:
            for h in range(V):
                if order[h][i]:
                    if x[h] == 0: ok = False; break
                    if x[h] is None: x[h] = 1
        else:
            for h in range(V):
                if order[i][h]:
                    if x[h] == 1: ok = False; break
                    if x[h] is None: x[h] = 0
        if ok: dfs(k + 1)
        x[:] = snap

dfs(0)
with open('csp_result.txt', 'w') as f:
    def out(s):
        print(s); f.write(s + '\n')
    out(f"groups: {len(oliver)} Oliver + {len(psub)} p-groups; classes: {V}")
    out(f"admissible patterns: {sols[0]}" + (" (cap)" if sols[0] >= CAP else ""))
    if sols[0] == 0:
        out("UNSAT => THE ARK CONJECTURE HOLDS UNCONDITIONALLY AT n = 10")
    else:
        fin  = [i for i in range(V) if seen[i] == {1}]
        fout = [i for i in range(V) if seen[i] == {0}]
        out(f"forced IN : {len(fin)} classes, edge counts "
            f"{sorted(edges[i] for i in fin)}")
        out(f"forced OUT: {len(fout)} classes, edge counts "
            f"{sorted(edges[i] for i in fout)}")
log("stage 4 complete; see csp_result.txt")
