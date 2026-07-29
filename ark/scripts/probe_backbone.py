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
from math import gcd

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

def parse_q(tag):
    """Top-prime modulus from a group tag.

    Tags: 'P<p>' a p-group (Smith condition, no q); '0' trivial top (chi = 1
    EXACTLY, returned as None); otherwise a '+'-separated list of every usable
    top prime, e.g. '2+3'.  A group admitting chains with top primes q1 and q2
    forces chi = 1 modulo BOTH, hence modulo lcm(q1, q2) -- strictly stronger
    than either alone, and the strengthening Appendix B / Part G.0 flags as
    available and unused.  Plain single-prime tags from older groups_out.txt
    files parse identically to before, so this is backward compatible."""
    if tag.startswith('P'):
        return None
    if tag == '0':
        return None                     # chi = 1 exactly; handled by q is None
    qs = [int(v) for v in tag.split('+') if v]
    m = 1
    for q in qs:
        m = m * q // gcd(m, q)
    return m

oliver = [g for g in groups if not g['tag'].startswith('P')]
psub   = [g for g in groups if g['tag'].startswith('P')]
ALLG = oliver + psub
for g in ALLG:
    g['classes'] = sorted(set(g['uc'].values()))
    g['q'] = parse_q(g['tag'])
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
    tstart = time.time(); tbeat = [tstart]

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
        if time.time() - tbeat[0] > 30:
            tbeat[0] = time.time()
            log(f"  ... class {pin_class} pinned {pin_val}: {nodes[0]} nodes "
                f"({nodes[0]/(time.time()-tstart):.0f}/s, cap {nodecap})")
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
elif args.auto:
    if not os.path.exists('solution1.pkl'):
        sys.exit("--auto requires solution1.pkl: run  python3 stage4_fast.py --first"
                 "  on THIS battery's checkpoints first (it saves the solution).")
    solx = pickle.load(open('solution1.pkl', 'rb'))['x']
    INs = [i for i in range(V) if solx[i] == 1]
    maxIN = [i for i in INs if not any(j != i and solx[j] == 1 and order[i][j] for j in INs)]
    OUTs = [i for i in range(V) if solx[i] == 0 and edges[i] < NFULL]
    minOUT = [i for i in OUTs if not any(j != i and solx[j] == 0 and order[j][i] for j in OUTs)]
    targets = (maxIN + minOUT)[:args.auto]
else:
    targets = list(range(V))
    log(f"NOTE: probing ALL {V} classes (no --classes/--auto). This is the full"
        f" backbone sweep; at ~1 min/probe expect ~{2*V/60:.0f} hours, checkpointed.")

log(f"targets ({len(targets)}): " + ", ".join(
    f"{c}(e={edges[c]})" for c in targets[:25]) + (" ..." if len(targets) > 25 else ""))

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
        log(f"probing class {c} (e={edges[c]}) pinned {v} ...")
        res = solve(c, v, args.nodecap)
        cw.writerow([c, v, res, edges[c], f"{time.time()-t0:.0f}s"]); fh.flush()
        log(f"class {c} (e={edges[c]}) pinned {v}: {res} ({time.time()-t0:.0f}s)")
        if v == 0 and res == 'UNSAT': forced_in.append(c)
        if v == 1 and res == 'UNSAT': forced_out.append(c)
# Summarise the WHOLE record, including the CAP tail.  A class with a CAP probe is
# NOT known to be free -- free requires both probes SAT -- and reporting only the
# IN/OUT lists (as section 8.9 did) hides an inconclusive remainder that at n = 10
# ran to 54 of 817 probes, concentrated at 12-36 edges, i.e. straight through the
# free middle band whose freeness sections 8.6 and 8.9' reason from.
res = {}
for r in csv.reader(open('probe_results.csv')):
    if r and r[0] != 'class':
        res.setdefault(int(r[0]), {})[int(r[1])] = r[2]
def status(d):
    if 'CAP' in d.values(): return 'CAP'
    if len(d) < 2: return 'partial'
    if d[0] == 'UNSAT' and d[1] == 'UNSAT': return 'CONTRADICTORY'
    if d[0] == 'UNSAT': return 'IN'
    if d[1] == 'UNSAT': return 'OUT'
    return 'free'
tally = {}
for c, d in res.items(): tally[status(d)] = tally.get(status(d), 0) + 1
log(f"probing done. forced IN: {forced_in}  forced OUT: {forced_out}")
log(f"record over {len(res)} classes probed at all: " +
    ", ".join(f"{k}={v}" for k, v in sorted(tally.items())))
if tally.get('CAP'):
    caps = sorted(c for c, d in res.items() if status(d) == 'CAP')
    log(f"INCONCLUSIVE at this node budget ({args.nodecap}): {len(caps)} classes, "
        f"edges {sorted(edges[c] for c in caps)}")
    log("  these are NOT free; rerun them with a larger --nodecap before quoting "
        "any free-band conclusion")
if tally.get('CONTRADICTORY'):
    log("*** both pinnings UNSAT on some class: the constraint system is "
        "inconsistent, which would mean UNSAT outright -- investigate ***")
# Involution cross-check (section 8.9): x*[c] = 1 - x[complement of c] predicts
# that forced-IN and forced-OUT are exchanged by complementation.  Checkable only
# with the catalog, so it is done here rather than left to a manual edge-count
# argument.
try:
    import networkx as _nx
    comp_of = {}
    for i in range(V):
        comp_of[i] = cat.classify(set(_nx.complement(cat.reps[i]).edges()))
    assert len(cat.reps) == V, "catalog grew during complement lookup"
    viol, unpr = [], []
    for c, d in res.items():
        st = status(d); cc = comp_of[c]
        if st not in ('IN', 'OUT'): continue
        want = 'OUT' if st == 'IN' else 'IN'
        if cc not in res: unpr.append((c, st, cc)); continue
        got = status(res[cc])
        if got != want and got != 'CAP': viol.append((c, st, cc, got, want))
    log(f"involution check: {len(viol)} violations, {len(unpr)} forced classes "
        f"whose complement is unprobed")
    for c, st, cc, got, want in viol[:10]:
        log(f"  *** class {c} is {st} but its complement {cc} is {got} "
            f"(theorem requires {want}) ***")
    for c, st, cc in unpr[:10]:
        log(f"  predicted: class {cc} should be forced "
            f"{'OUT' if st == 'IN' else 'IN'} (complement of {c}, {st})")
except Exception as e:
    log(f"involution check skipped: {e}")
log("full record: probe_results.csv")
