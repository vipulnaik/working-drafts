"""
consume_gap.py (v2) -- feed GAP-enumerated groups into the ARK-at-10 CSP.

Changes from v1:
  * SELECTION SIGNATURES: every checkpoint records the (flags, group-key)
    selection it was built for; a mismatch triggers a loud message and a clean
    rebuild of that stage instead of silent corruption.  Changing --maxgroups
    or --maxt now "just works" (it rebuilds what it must).
  * PARALLEL stage 3 (--procs N, default all cores): rows of the monomorphism
    matrix are computed by a worker pool; incremental checkpointing preserved
    (kill/resume safe, granularity CKPT_ROWS rows).
  * stage 4 removed: run stage4_fast.py afterwards (correct + fast solver).

Usage:  python3 consume_gap.py [--maxgroups N] [--maxt T] [--procs P]
Needs oliver_mu.py, ark_intersect.py, smith.py alongside; pip install networkx.
"""
import sys, os, pickle, time, argparse, itertools, hashlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PAIRS = list(itertools.combinations(range(10), 2))
CKPT_EVERY = 5
CKPT_ROWS = 8

def log(msg):
    line = f"{time.strftime('%H:%M:%S')}  {msg}"
    print(line, flush=True)
    with open('consume_gap.log', 'a') as f: f.write(line + '\n')

# ---- worker for parallel stage 3 (top-level for spawn-compatibility) ----
_W = {}
def _init_worker(reps_pickle):
    import networkx as nx  # noqa
    from ark_intersect import mono
    _W['reps'] = pickle.loads(reps_pickle)
    _W['mono'] = mono
def _row(a):
    reps = _W['reps']; mono = _W['mono']; V = len(reps)
    ea = reps[a].number_of_edges()
    out = []
    for b in range(V):
        if a == b: out.append(True)
        elif ea <= reps[b].number_of_edges():
            out.append(mono(reps[a], reps[b]))
        else:
            out.append(False)
    return a, out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--maxgroups', type=int, default=200)
    ap.add_argument('--maxt', type=int, default=10)
    ap.add_argument('--procs', type=int, default=os.cpu_count())
    ap.add_argument('--infile', default='groups_out.txt')
    args = ap.parse_args()

    import networkx as nx  # noqa
    from ark_intersect import Catalog

    # ---------------- stage 1 ----------------
    def build_selection():
        raw = []
        for line in open(args.infile):
            line = line.strip()
            if not line: continue
            key, desc, tag, om = line.split('|')
            omap = [int(x) - 1 for x in om.split(',')]
            t = max(omap) + 1
            if t > args.maxt: continue
            orbs = [frozenset(PAIRS[i] for i in range(45) if omap[i] == o)
                    for o in range(t)]
            raw.append(dict(key=key, desc=desc, tag=tag, t=t, orbs=orbs,
                            mstar=min(len(o) for o in orbs)))
        seen = {}
        dedup = []
        for g in raw:
            deg = tuple(sorted(tuple(sorted(sum(1 for p in o if u in p)
                        for o in g['orbs'])) for u in range(10)))
            sig = (g['t'], tuple(sorted(len(o) for o in g['orbs'])), g['tag'], deg)
            if sig in seen: continue
            seen[sig] = True
            dedup.append(g)
        pg = [g for g in dedup if g['tag'].startswith('P')]
        ol = [g for g in dedup if not g['tag'].startswith('P')]
        ol.sort(key=lambda g: (-g['mstar'], g['t']))
        sel = ol[:args.maxgroups] + pg
        return len(raw), sel

    def selection_sig(groups):
        s = f"maxgroups={args.maxgroups};maxt={args.maxt};" + \
            ";".join(g['key'] for g in groups)
        return hashlib.sha256(s.encode()).hexdigest()[:16]

    nraw, groups = build_selection()
    SIG = selection_sig(groups)
    if os.path.exists('ckpt_groups.pkl'):
        st = pickle.load(open('ckpt_groups.pkl', 'rb'))
        if st.get('sig') == SIG:
            groups = st['groups']
            log(f"stage 1: checkpoint matches selection ({len(groups)} groups)")
        else:
            log("stage 1: SELECTION CHANGED -> rebuilding all downstream checkpoints")
            for f in ('ckpt_groups.pkl', 'ckpt_catalog.pkl', 'ckpt_order.pkl'):
                if os.path.exists(f): os.remove(f)
    if not os.path.exists('ckpt_groups.pkl'):
        pickle.dump(dict(sig=SIG, groups=groups), open('ckpt_groups.pkl', 'wb'))
        npg = sum(1 for g in groups if g['tag'].startswith('P'))
        log(f"stage 1: {nraw} raw -> {len(groups)} kept "
            f"({len(groups)-npg} Oliver, {npg} p-groups)  sig={SIG}")

    # ---------------- stage 2 ----------------
    rebuild = True
    if os.path.exists('ckpt_catalog.pkl'):
        st = pickle.load(open('ckpt_catalog.pkl', 'rb'))
        if st.get('sig') == SIG:
            cat, gidx = st['cat'], st['gidx']
            groups = st['groups']          # carries uc maps computed so far
            rebuild = False
            log(f"stage 2: resumed at group {gidx}, catalog {len(cat.reps)} classes")
        else:
            log("stage 2: signature mismatch -> rebuilding catalog (and order matrix)")
            if os.path.exists('ckpt_order.pkl'): os.remove('ckpt_order.pkl')
    if rebuild:
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
            pickle.dump(dict(sig=SIG, cat=cat, gidx=gidx, groups=groups),
                        open('ckpt_catalog.pkl', 'wb'))
            log(f"stage 2: {gidx}/{len(groups)} groups, {len(cat.reps)} classes")
    V = len(cat.reps)
    log(f"stage 2 complete: {V} classes")

    # ---------------- stage 3 (parallel) ----------------
    done_rows = {}
    if os.path.exists('ckpt_order.pkl'):
        st = pickle.load(open('ckpt_order.pkl', 'rb'))
        if st.get('sig') == SIG and st.get('V') == V:
            done_rows = st['rows']
            log(f"stage 3: resumed with {len(done_rows)}/{V} rows")
        else:
            log("stage 3: signature/V mismatch -> rebuilding order matrix")
    todo = [a for a in range(V) if a not in done_rows]
    if todo:
        import multiprocessing as mp
        reps_pickle = pickle.dumps(cat.reps)
        t0 = time.time()
        with mp.get_context('spawn').Pool(args.procs, _init_worker,
                                          (reps_pickle,)) as pool:
            pending = 0
            for a, rowvals in pool.imap_unordered(_row, todo, chunksize=1):
                done_rows[a] = rowvals
                pending += 1
                if pending >= CKPT_ROWS or len(done_rows) == V:
                    pickle.dump(dict(sig=SIG, V=V, rows=done_rows),
                                open('ckpt_order.pkl', 'wb'))
                    pending = 0
                    el = time.time() - t0
                    d = len(done_rows)
                    log(f"stage 3: {d}/{V} rows "
                        f"(eta {el/max(1,d-(V-len(todo)))*(V-d):.0f}s)")
    order = [done_rows[a] for a in range(V)]
    pickle.dump(dict(sig=SIG, V=V, rows=done_rows, order=order, row=V),
                open('ckpt_order.pkl', 'wb'))
    log("stage 3 complete")
    log("now run:  python3 stage4_fast.py --first")

if __name__ == '__main__':
    main()
