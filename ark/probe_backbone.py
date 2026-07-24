"""
probe_backbone.py -- compute the TRUE backbone of the CSP, class by class,
without enumerating solutions.

For each target class c and each value v in {0,1}: pin x[c]=v, propagate, and
run the stage4-style DFS to the first verified solution (or exhaustion, or a
node cap).  Outcomes per (c,v): SAT / UNSAT / CAP.  Interpretation:
    (c,0)=UNSAT           => c is FORCED IN every admissible property
    (c,1)=UNSAT           => c is FORCED OUT
    both SAT              => c is genuinely free
    any CAP               => undetermined at this node budget (rerun bigger)
UNSAT verdicts are exact (exhaustion under the full constraint system);
SAT verdicts are exact; only CAP is inconclusive.

Checkpointed: results append to probe_results.csv; already-recorded (c,v)
pairs are skipped on restart.  Anytime-stoppable (Ctrl-C between probes).

Usage:
  python3 probe_backbone.py                     # probe every class (slow)
  python3 probe_backbone.py --classes 27,37,15  # probe specific classes
  python3 probe_backbone.py --auto 40           # probe the 40 most interesting
                                                # (maximal-IN and minimal-OUT
                                                #  of solution1.pkl, if present)
  python3 probe_backbone.py --nodecap 5000000   # per-probe node budget
Needs the ckpt_*.pkl files and oliver_mu.py / ark_intersect.py / smith.py
alongside (same directory), like stage4_fast.py.
"""
import sys, os, pickle, time, argparse, csv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smith import fp_acyclic

ap = argparse.ArgumentParser()
ap.add_argument('--classes', default='')
ap.add_argument('--auto', type=int, default=0)
ap.add_argument('--nodecap', type=int, default=5_000_000)
args = ap.parse_args()

gst = pickle.load(open('ckpt_groups.pkl', 'rb'))
cst = pickle.load(open('ckpt_catalog.pkl', 'rb'))
groups = cst['groups'] if isinstance(cst, dict) and 'groups' in cst else \
         (gst['groups'] if isinstance(gst, dict) else gst)
cat = cst['cat']
ost = pickle.load(open('ckpt_order.pkl', 'rb'))
order = ost['order'] if 'order' in ost else [ost['rows'][a] for a in range(ost['V'])]
V = len(order)
edges = [cat.reps[i].number_of_edges() for i in range(V)]
NVERT = cat.reps[0].number_of_nodes()
NFULL = NVERT * (NVERT - 1) // 2

def log(m):
    line = f"{time.strftime('%H:%M:%S')}  {m}"
    print(line, flush=True)
    with open('probe_backbone.log', 'a') as f: f.write(line + '\n')

oliver = [g for g in groups if not g['tag'].startswith('P')]
psub   = [g for g in groups if g['tag'].startswith('P')]
ALLG = oliver + psub
for g in ALLG:
    g['classes'] = sorted(set(g['uc'].values()))
    g['q'] = (None if g['tag'] == '0' else int(g['tag'])) \
             if not g['tag'].startswith('P') else None
    g['p'] = int(g['tag'][1:]) if g['tag'].startswith('P') else None
touch = [[] for _ in range(V)]
for gi, g in enumerate(ALLG):
    for c in g['classes']: touch[c].append(gi)

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
        ok = (cp == 1 and cd == 1) if q is None else \
             (cp % q == 1 % q and cd % q == 1 % q)
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

def solve(pin_class, pin_val, nodecap):
    """Returns 'SAT', 'UNSAT', or 'CAP'."""
    x = [None] * V
    x[cat.classify(set())] = 1
    for i in range(V):
        if edges[i] == NFULL: x[i] = 0
    pend = None

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

    if x[pin_class] is not None and x[pin_class] != pin_val:
        return 'UNSAT'
    x[pin_class] = pin_val
    if not full_prop(): return 'UNSAT'
    pend = [sum(1 for c in ALLG[gi]['classes'] if x[c] is None)
            for gi in range(len(ALLG))]
    for gi in range(len(ALLG)):
        if pend[gi] == 0 and not group_ok(gi, x): return 'UNSAT'

    unknowns = [i for i in range(V) if x[i] is None]
    placed = set(i for i in range(V) if x[i] is not None)
    ordered = []
    remaining = set(range(len(ALLG)))
    while remaining:
        gi = min(remaining,
                 key=lambda g_: (sum(1 for c in ALLG[g_]['classes'] if c not in placed),
                                 len(ALLG[g_]['classes'])))
        for c in sorted(ALLG[gi]['classes'], key=lambda c: -edges[c]):
            if c not in placed:
                placed.add(c); ordered.append(c)
        remaining.discard(gi)
    ordered += [i for i in unknowns if i not in set(ordered)]
    unknowns = [i for i in ordered if x[i] is None]

    nodes = [0]; found = [False]; capped = [False]

    def assign(i, val, changed):
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
        if nodes[0] > nodecap: capped[0] = True; return
        if found[0] or capped[0]: return
        while k < len(unknowns) and x[unknowns[k]] is not None: k += 1
        if k == len(unknowns):
            if all(group_ok(gi, x) for gi in range(len(ALLG))):
                found[0] = True
            return
        i = unknowns[k]
        for val in (0, 1):
            ch = []
            if assign(i, val, ch): dfs(k + 1)
            undo(ch)
            if found[0] or capped[0]: return

    sys.setrecursionlimit(10000)
    dfs(0)
    if found[0]: return 'SAT'
    if capped[0]: return 'CAP'
    return 'UNSAT'

# ---- target selection ----
if args.classes:
    targets = [int(x) for x in args.classes.split(',')]
elif args.auto and os.path.exists('solution1.pkl'):
    solx = pickle.load(open('solution1.pkl', 'rb'))['x']
    INs = [i for i in range(V) if solx[i] == 1]
    maxIN = [i for i in INs if not any(j != i and solx[j] == 1 and order[i][j] for j in INs)]
    OUTs = [i for i in range(V) if solx[i] == 0 and edges[i] < NFULL]
    minOUT = [i for i in OUTs if not any(j != i and solx[j] == 0 and order[j][i] for j in OUTs)]
    targets = (maxIN + minOUT)[:args.auto]
else:
    targets = list(range(V))

done = set()
if os.path.exists('probe_results.csv'):
    for r in csv.reader(open('probe_results.csv')):
        if r and r[0] != 'class': done.add((int(r[0]), int(r[1])))
fh = open('probe_results.csv', 'a', newline='')
cw = csv.writer(fh)
if not done: cw.writerow(['class', 'pinned_value', 'result', 'edges', 'nodes_note'])

forced_in, forced_out = [], []
for c in targets:
    for v in (0, 1):
        if (c, v) in done: continue
        t0 = time.time()
        res = solve(c, v, args.nodecap)
        cw.writerow([c, v, res, edges[c], f"{time.time()-t0:.0f}s"]); fh.flush()
        log(f"class {c} (e={edges[c]}) pinned {v}: {res} ({time.time()-t0:.0f}s)")
        if v == 0 and res == 'UNSAT': forced_in.append(c)
        if v == 1 and res == 'UNSAT': forced_out.append(c)
log(f"probing done. forced IN: {forced_in}  forced OUT: {forced_out}")
log("full record: probe_results.csv")
