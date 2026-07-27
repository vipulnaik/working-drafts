"""
stage4_fast.py -- drop-in replacement for consume_gap.py's stage 4.

Reads ckpt_groups.pkl / ckpt_catalog.pkl / ckpt_order.pkl produced by stages
1-3 (do NOT delete them).  Improvements over the original stage 4:

  * event-driven checks: each group's condition (primal+dual chi for Oliver
    groups, primal+dual F_p-acyclicity for p-groups) is evaluated exactly when
    the last class in its lattice becomes decided -- pruning happens at the
    highest possible tree level instead of rescanning all groups per node;
  * memoization: chi and homology results cached by (group, bit-pattern of its
    lattice), so repeated subtree contexts are free;
  * heartbeat logging every 30 seconds with nodes/sec, plus depth histogram;
  * --first flag: stop at the first solution (fast SAT/UNSAT verdict);
  * graceful Ctrl-C: prints partial statistics before exiting.

Usage:
    python3 stage4_fast.py             # full enumeration (cap 100000)
    python3 stage4_fast.py --first     # satisfiability verdict only
Requires oliver_mu.py, ark_intersect.py, smith.py alongside (for unpickling
and fp_acyclic), same as consume_gap.py.
"""
import sys, os, pickle, time, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smith import fp_acyclic   # also triggers its (quick) self-tests

ap = argparse.ArgumentParser()
ap.add_argument('--first', action='store_true', help='stop at first solution')
ap.add_argument('--cap', type=int, default=100000)
ap.add_argument('--seed', type=int, default=None,
                help='randomise variable ordering; different seeds give '
                     'different first solutions, for sampling the solution '
                     'space (each can then be chi-tested with chi_test.py)')
args = ap.parse_args()

gst = pickle.load(open('ckpt_groups.pkl', 'rb'))
cst = pickle.load(open('ckpt_catalog.pkl', 'rb'))
# v2 checkpoints store dicts with signatures; groups WITH uc maps live in the
# catalog checkpoint.  v1 stored a bare list in ckpt_groups.
if isinstance(cst, dict) and 'groups' in cst:
    groups = cst['groups']
elif isinstance(gst, dict):
    groups = gst['groups']
else:
    groups = gst
if isinstance(cst, dict) and isinstance(gst, dict) and 'sig' in cst and 'sig' in gst:
    assert cst['sig'] == gst['sig'], "checkpoint signature mismatch -- rerun consume_gap.py"
cat = cst['cat']
ost = pickle.load(open('ckpt_order.pkl', 'rb'))
if 'order' in ost:
    order = ost['order']
elif 'rows' in ost:
    rows = ost['rows']; Vv = ost['V']
    assert len(rows) == Vv, "order matrix incomplete -- rerun consume_gap.py stage 3"
    order = [rows[a] for a in range(Vv)]
elif 'TU' in ost:
    sys.exit("ckpt_order.pkl is a partial inference checkpoint -- "
             "finish consume_gap.py stage 3 first")
else:
    sys.exit("unrecognized ckpt_order.pkl format -- rerun consume_gap.py stage 3")
if isinstance(cst, dict) and 'sig' in cst and 'sig' in ost:
    assert ost['sig'] == cst['sig'], "order matrix from a different selection -- rerun consume_gap.py"
V = len(order)
edges = [cat.reps[i].number_of_edges() for i in range(V)]
assert all('uc' in g for g in groups), "groups lack lattice maps -- rerun consume_gap.py stage 2"

LOG = open('stage4_fast.log', 'a')
def log(msg):
    line = f"{time.strftime('%H:%M:%S')}  {msg}"
    print(line, flush=True); LOG.write(line + '\n'); LOG.flush()

# ---- per-group precomputation -------------------------------------------
oliver = [g for g in groups if not g['tag'].startswith('P')]
psub   = [g for g in groups if g['tag'].startswith('P')]
ALLG = oliver + psub
for gi, g in enumerate(ALLG):
    g['classes'] = sorted(set(g['uc'].values()))
    g['q'] = (None if g['tag'] == '0' else int(g['tag'])) \
             if not g['tag'].startswith('P') else None
    g['p'] = int(g['tag'][1:]) if g['tag'].startswith('P') else None
# class -> list of group indices whose lattice contains it
touch = [[] for _ in range(V)]
for gi, g in enumerate(ALLG):
    for c in g['classes']:
        touch[c].append(gi)

memo = {}
def group_ok(gi, x):
    g = ALLG[gi]; t = g['t']; uc = g['uc']; full = (1 << t) - 1
    key = (gi, tuple(x[c] for c in g['classes']))
    if key in memo: return memo[key]
    if g['p'] is None:
        cp = cd = 0
        for m in range(1, 1 << t):
            s = 1 if bin(m).count('1') % 2 else -1
            if x[uc[m]] == 1: cp += s
            if x[uc[full ^ m]] == 0: cd += s
        q = g['q']
        if q is None:
            ok = (cp == 1 and cd == 1)
        else:
            ok = (cp % q == 1 % q and cd % q == 1 % q)
    else:
        pf = {frozenset(i for i in range(t) if m >> i & 1)
              for m in range(1 << t) if x[uc[m]] == 1}
        ok = fp_acyclic(pf, t, g['p'])
        if ok:
            df = {frozenset(i for i in range(t) if m >> i & 1)
                  for m in range(1 << t) if x[uc[full ^ m]] == 0}
            ok = fp_acyclic(df, t, g['p'])
    memo[key] = ok
    return ok

# ---- initial pinning + propagation --------------------------------------
NVERT = cat.reps[0].number_of_nodes()
NFULL = NVERT * (NVERT - 1) // 2
x = [None] * V
x[cat.classify(set())] = 1
for i in range(V):
    if edges[i] == NFULL: x[i] = 0
pend = [sum(1 for c in ALLG[gi]['classes'] if x[c] is None) for gi in range(len(ALLG))]

def full_prop():
    ch = True
    while ch:
        ch = False
        for a in range(V):
            if x[a] == 1:
                for h in range(V):
                    if order[h][a] and x[h] != 1:
                        if x[h] == 0: return False
                        x[h] = 1; ch = True
            elif x[a] == 0:
                for h in range(V):
                    if order[a][h] and x[h] != 0:
                        if x[h] == 1: return False
                        x[h] = 0; ch = True
    return True

if not full_prop():
    log("UNSAT at initial propagation => ARK HOLDS UNCONDITIONALLY AT n=10")
    sys.exit()
for gi in range(len(ALLG)):
    pend[gi] = sum(1 for c in ALLG[gi]['classes'] if x[c] is None)
    if pend[gi] == 0 and not group_ok(gi, x):
        log(f"UNSAT: group {ALLG[gi]['key']} fails at root => ARK HOLDS AT n=10")
        sys.exit()

unknowns = [i for i in range(V) if x[i] is None]
# greedy group-completion ordering: repeatedly take the group with the fewest
# still-unplaced classes and append them, so whole lattices close as early as
# possible and harsh conditions (chi=1-exact, acyclicity) prune high in the
# tree instead of thrashing at the bottom.
placed = set(i for i in range(V) if x[i] is not None)
ordered = []
remaining = set(range(len(ALLG)))
while remaining:
    gi = min(remaining,
             key=lambda g: (sum(1 for c in ALLG[g]['classes'] if c not in placed),
                            len(ALLG[g]['classes'])))
    for c in sorted(ALLG[gi]['classes'], key=lambda c: -edges[c]):
        if c not in placed:
            placed.add(c); ordered.append(c)
    remaining.discard(gi)
ordered += [i for i in unknowns if i not in set(ordered)]
unknowns = [i for i in ordered if x[i] is None]
if args.seed is not None:
    import random
    rnd = random.Random(args.seed)
    # shuffle within equal-edge-count blocks: keeps the greedy group-completion
    # benefit (harsh conditions still close early) but varies which leaf is hit
    blocks = {}
    for i in unknowns: blocks.setdefault(edges[i], []).append(i)
    for k in blocks: rnd.shuffle(blocks[k])
    seen_e = []
    for i in unknowns:
        if edges[i] not in seen_e: seen_e.append(edges[i])
    unknowns = [i for e in seen_e for i in blocks[e]]
    log(f"variable ordering randomised with seed {args.seed}")
log(f"stage4_fast: {len(oliver)} Oliver + {len(psub)} p-groups, V={V}, "
    f"free={len(unknowns)}")

# ---- DFS -----------------------------------------------------------------
sols = [0]; seen = [set() for _ in range(V)]
nodes = [0]; t0 = time.time(); last = [t0]; maxdepth = [0]

def assign(i, val, changed):
    """set x[i]=val, propagate one step of monotonicity, update pend;
    record touched indices in changed.  Returns False on contradiction."""
    stack = [(i, val)]
    while stack:
        j, v = stack.pop()
        if x[j] is not None:
            if x[j] != v: return False
            continue
        x[j] = v; changed.append(j)
        zeroed = []
        for gi in touch[j]:
            pend[gi] -= 1
            if pend[gi] == 0: zeroed.append(gi)
        # checks AFTER the decrement loop completes: an early return mid-loop
        # would desynchronize pend from undo() (which re-increments all of
        # touch[j]) -- this was the bug that skipped most group checks
        for gi in zeroed:
            if not group_ok(gi, x): return False
        if v == 1:
            for h in range(V):
                if order[h][j] and x[h] != 1:
                    if x[h] == 0: return False
                    stack.append((h, 1))
        else:
            for h in range(V):
                if order[j][h] and x[h] != 0:
                    if x[h] == 1: return False
                    stack.append((h, 0))
    return True

def undo(changed):
    for j in changed:
        x[j] = None
        for gi in touch[j]: pend[gi] += 1

def dfs(k):
    nodes[0] += 1
    if time.time() - last[0] > 30:
        last[0] = time.time()
        log(f"heartbeat: nodes {nodes[0]} sols {sols[0]} depth<= {maxdepth[0]} "
            f"({nodes[0]/(time.time()-t0):.0f} nodes/s, memo {len(memo)})")
    if sols[0] >= args.cap or (args.first and sols[0] > 0): return
    while k < len(unknowns) and x[unknowns[k]] is not None: k += 1
    maxdepth[0] = max(maxdepth[0], k)
    if k == len(unknowns):
        # belt and braces: verify EVERY group at the leaf (memoized, cheap)
        if not all(group_ok(gi, x) for gi in range(len(ALLG))):
            log("WARNING: leaf reached with failing group -- bookkeeping bug")
            return
        sols[0] += 1
        for i in range(V): seen[i].add(x[i])
        if sols[0] == 1:
            fn = 'solution1.pkl' if args.seed is None else f'solution_seed{args.seed}.pkl'
            pickle.dump(dict(x=list(x)), open(fn, 'wb'))
            log(f"solution saved to {fn}; test it with:  python3 chi_test.py --solution {fn}")
        if args.first: log("first VERIFIED solution found (SAT)")
        return
    i = unknowns[k]
    for val in (0, 1):
        changed = []
        if assign(i, val, changed):
            dfs(k + 1)
        undo(changed)
        if sols[0] >= args.cap or (args.first and sols[0] > 0): return

try:
    sys.setrecursionlimit(10000)
    dfs(0)
    interrupted = False
except KeyboardInterrupt:
    interrupted = True
    log("interrupted by user")

with open('csp_result.txt', 'w') as f:
    def out(s):
        print(s); f.write(s + '\n')
    out(f"stage4_fast: nodes={nodes[0]} time={time.time()-t0:.0f}s "
        f"memo={len(memo)}" + (" [INTERRUPTED: results partial]" if interrupted else ""))
    if sols[0] == 0 and not interrupted:
        out("UNSAT => THE ARK CONJECTURE HOLDS UNCONDITIONALLY AT n = 10")
        out("(archive all ckpt_*.pkl + groups_out.txt and rerun once to reproduce)")
    else:
        out(f"admissible patterns: {sols[0]}"
            + (" (cap reached)" if sols[0] >= args.cap else "")
            + (" (stopped at first)" if args.first and sols[0] else ""))
        if sols[0]:
            fin  = [i for i in range(V) if seen[i] == {1}]
            fout = [i for i in range(V) if seen[i] == {0}]
            label = "(single solution's assignment)" if args.first or sols[0] == 1 \
                    else "(backbone over all solutions)"
            out(f"IN  {label}: {len(fin)} classes, edges {sorted(edges[i] for i in fin)}")
            out(f"OUT {label}: {len(fout)} classes, edges {sorted(edges[i] for i in fout)}")
log("done; see csp_result.txt")
