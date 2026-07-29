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

def detect_N(infile):
    for line in open(infile):
        line=line.strip()
        if line:
            L=len(line.split('|')[3].split(','))
            N=int((1+(1+8*L)**.5)/2)
            assert N*(N-1)//2==L, "orbmap length is not a triangular number"
            return N
    raise SystemExit("empty groups file")
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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--maxgroups', type=int, default=None,
                    help='default 200, or the value stored in ckpt_groups.pkl')
    ap.add_argument('--maxt', type=int, default=None,
                    help='default 10, or the value stored in ckpt_groups.pkl')
    ap.add_argument('--procs', type=int, default=os.cpu_count())
    ap.add_argument('--infile', default='groups_out.txt')
    ap.add_argument('--verify', type=int, default=3000,
                    help='number of random ordered pairs to re-decide by VF2 '
                         'after stage 3, as a check on the inference layers '
                         '(0 to skip)')
    args = ap.parse_args()

    import networkx as nx  # noqa
    from ark_intersect import Catalog

    # adopt flags from the existing checkpoint when not given explicitly, so a
    # bare rerun resumes the same battery instead of silently redefining it
    stored = None
    if os.path.exists('ckpt_groups.pkl'):
        try:
            _st = pickle.load(open('ckpt_groups.pkl', 'rb'))
            if isinstance(_st, dict): stored = _st.get('flags')
        except Exception:
            stored = None
    if stored:
        if args.maxgroups is None:
            args.maxgroups = stored['maxgroups']
            log(f"adopting --maxgroups {args.maxgroups} from checkpoint")
        if args.maxt is None:
            args.maxt = stored['maxt']
            log(f"adopting --maxt {args.maxt} from checkpoint")
    if args.maxgroups is None: args.maxgroups = 200
    if args.maxt is None: args.maxt = 10

    N = detect_N(args.infile)
    PAIRS = list(itertools.combinations(range(N), 2))
    NPAIRS = len(PAIRS)
    log(f"detected n = {N} ({NPAIRS} pairs)")

    # ---------------- stage 1 ----------------
    # DEDUP CORRECTNESS.  The condition a group imposes on the CSP depends only on
    # its orbital partition up to S_n (the invariant graphs are exactly the unions
    # of orbitals) together with the prime in its tag.  The v1/v2 key was
    #     (t, sorted orbital sizes, tag, per-vertex valency-multiset signature)
    # which is a strong INVARIANT of that data but not a complete one, and it was
    # used to DISCARD groups.  Measured at n = 12 over the 7,115 groups in
    # groups_out.txt: 41 of 278 collision buckets merged inequivalent orbital
    # partitions, so the retained representatives covered 381 of the 425 distinct
    # (partition, prime) conditions available -- 44 dropped, 10.4% overall and
    # 22.4% of the Smith (p-group) conditions specifically.  The failure direction
    # is the dangerous one: a dropped condition can only turn a real UNSAT into
    # SAT, never the reverse.
    #
    # The key below is complete.  Build a layered graph with N point-nodes,
    # C(N,2) pair-nodes and t ORBITAL-nodes; each pair-node is adjacent to its two
    # points and to its orbital-node.  Colour classes: points | pair-nodes | one
    # class per orbital-STAT group (size, valency multiset).  Because every orbital
    # carries its own node, a colour-preserving isomorphism must map each
    # orbital's pair-set onto some orbital's pair-set, which is exactly equivalence
    # of orbital partitions up to relabelling the orbitals.  Tied orbitals share a
    # colour class, so the form does not depend on GAP's orbital indexing -- an
    # earlier attempt that ordered ties by index over-split equivalent partitions
    # and inflated the apparent loss sevenfold.
    try:
        import pynauty
        def _orbital_canon(g):
            t = g['t']
            adj = {i: [] for i in range(N)}
            stats = []
            for o in range(t):
                mem = [i for i in range(NPAIRS) if g['omap'][i] == o]
                val = tuple(sorted(sum(1 for i in mem if u in PAIRS[i])
                                   for u in range(N)))
                stats.append((len(mem), val))
            for idx, (u, v) in enumerate(PAIRS):
                adj[N + idx] = [u, v, N + NPAIRS + g['omap'][idx]]
            for o in range(t):
                adj[N + NPAIRS + o] = []
            grp = {}
            for o in range(t):
                grp.setdefault(stats[o], []).append(N + NPAIRS + o)
            cols = ([set(range(N)), set(range(N, N + NPAIRS))] +
                    [set(grp[k]) for k in sorted(grp)])
            G = pynauty.Graph(N + NPAIRS + t, adjacency_dict=adj,
                              vertex_coloring=cols)
            return (pynauty.certificate(G), t, tuple(sorted(stats)))
        _CANON_KIND = 'pynauty canonical orbital partition'
    except ImportError:
        # Correct fallback, no new dependency: bucket by the cheap invariant, then
        # separate buckets by explicit colour-preserving isomorphism search on the
        # layered graph.  Slower but exact; buckets are small.
        def _orbital_canon(g, _cache={}, _reps=[]):
            deg = tuple(sorted(tuple(sorted(sum(1 for p in o if u in p)
                        for o in g['orbs'])) for u in range(N)))
            bkey = (g['t'], tuple(sorted(len(o) for o in g['orbs'])), deg)
            lay = _layered(g)
            for i, (bk, H) in enumerate(_reps):
                if bk == bkey and nx.is_isomorphic(
                        lay, H, node_match=lambda a, b: a['c'] == b['c']):
                    return ('fallback', i)
            _reps.append((bkey, lay))
            return ('fallback', len(_reps) - 1)

        def _layered(g):
            H = nx.Graph()
            stats = {}
            for o in range(g['t']):
                mem = [i for i in range(NPAIRS) if g['omap'][i] == o]
                stats[o] = (len(mem), tuple(sorted(
                    sum(1 for i in mem if u in PAIRS[i]) for u in range(N))))
            for u in range(N):
                H.add_node(('p', u), c='point')
            for o in range(g['t']):
                H.add_node(('o', o), c=('orb', stats[o]))
            for idx, (u, v) in enumerate(PAIRS):
                H.add_node(('e', idx), c='pair')
                H.add_edges_from([(('e', idx), ('p', u)), (('e', idx), ('p', v)),
                                  (('e', idx), ('o', g['omap'][idx]))])
            return H
        _CANON_KIND = 'networkx colour-preserving isomorphism (pynauty absent)'

    def build_selection():
        raw = []
        for line in open(args.infile):
            line = line.strip()
            if not line: continue
            key, desc, tag, om = line.split('|')
            omap = [int(x) - 1 for x in om.split(',')]
            t = max(omap) + 1
            if t > args.maxt: continue
            orbs = [frozenset(PAIRS[i] for i in range(NPAIRS) if omap[i] == o)
                    for o in range(t)]
            raw.append(dict(key=key, desc=desc, tag=tag, t=t, orbs=orbs,
                            omap=tuple(omap),
                            mstar=min(len(o) for o in orbs)))
        seen = {}
        dedup = []
        ncoll = 0
        for g in raw:
            sig = (_orbital_canon(g), g['tag'])   # complete: see note above
            if sig in seen:
                ncoll += 1
                continue
            seen[sig] = True
            dedup.append(g)
        log(f"stage 1: dedup by {_CANON_KIND}; {ncoll} groups impose a condition "
            f"already present, {len(dedup)} distinct (partition, prime) conditions")
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
        if isinstance(st, dict) and st.get('sig') == SIG:
            groups = st['groups']
            log(f"stage 1: checkpoint matches selection ({len(groups)} groups)")
        else:
            was = st.get('flags') if isinstance(st, dict) else None
            log("stage 1: SELECTION CHANGED -> rebuilding all downstream checkpoints")
            if was:
                log(f"  checkpoint was built with maxgroups={was['maxgroups']}, "
                    f"maxt={was['maxt']}; this invocation uses "
                    f"maxgroups={args.maxgroups}, maxt={args.maxt}")
                log("  (to resume the old battery instead, rerun with those flags "
                    "or omit both and they will be adopted automatically)")
            else:
                log("  (old checkpoint predates flag recording; rebuild is expected once)")
            for f in ('ckpt_groups.pkl', 'ckpt_catalog.pkl', 'ckpt_order.pkl'):
                if os.path.exists(f): os.remove(f)
    if not os.path.exists('ckpt_groups.pkl'):
        pickle.dump(dict(sig=SIG, groups=groups,
                         flags=dict(maxgroups=args.maxgroups, maxt=args.maxt)),
                    open('ckpt_groups.pkl', 'wb'))
        npg = sum(1 for g in groups if g['tag'].startswith('P'))
        log(f"stage 1: {nraw} raw -> {len(groups)} kept "
            f"({len(groups)-npg} Oliver, {npg} p-groups)  sig={SIG}")

    # ---------------- stage 2 ----------------
    rebuild = True
    if os.path.exists('ckpt_catalog.pkl'):
        st = pickle.load(open('ckpt_catalog.pkl', 'rb'))
        if isinstance(st, dict) and st.get('sig') == SIG:
            cat, gidx = st['cat'], st['gidx']
            groups = st['groups']          # carries uc maps computed so far
            rebuild = False
            log(f"stage 2: resumed at group {gidx}, catalog {len(cat.reps)} classes")
        else:
            log("stage 2: signature mismatch -> rebuilding catalog (and order matrix)")
            if os.path.exists('ckpt_order.pkl'): os.remove('ckpt_order.pkl')
    if rebuild:
        cat = Catalog(N); gidx = 0
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

    # ------- stage 3: inference-first order matrix (v3) -------
    # Three layers before any isomorphism test:
    #   (i)  free containments: within one group's lattice, mask m1 subset m2
    #        gives containment of the corresponding classes by construction;
    #        plus e(a) > e(b) => False, and e(a) == e(b) with a != b => False
    #        (distinct iso classes of equal size cannot embed);
    #   (ii) invariant pre-filters: subgraph containment forces every subgraph
    #        count to dominate -- sorted degree sequence, triangles, P3 paths,
    #        C4 counts -- violations => False;
    #   (iii) two-sided transitive closure: T[a][c] & T[c][b] => T[a][b];
    #        T[c][a] & F[c][b] => F[a][b];  F[a][d] & T[b][d] => F[a][b].
    # Only pairs undecided after fixpoint go to parallel VF2, in batches,
    # re-closing after each batch.  Checkpointed per batch.
    import numpy as np

    def invariants(G):
        A = nx.to_numpy_array(G, nodelist=sorted(G.nodes()))
        degs = A.sum(1)
        A2 = A @ A
        tri = int(np.trace(A2 @ A)) // 6
        p3 = int(sum(d * (d - 1) // 2 for d in degs))
        cod = A2.copy(); np.fill_diagonal(cod, 0)
        c4 = int(sum(c * (c - 1) // 2 for c in cod[np.triu_indices(len(A), 1)])) // 2
        return (int(A.sum()) // 2, tuple(sorted(degs, reverse=True)), tri, p3, c4)

    inv = [invariants(cat.reps[i]) for i in range(V)]

    def inv_allows(a, b):
        ea, da, ta, pa, ca = inv[a]; eb, db, tb, pb, cb = inv[b]
        if ea > eb or ta > tb or pa > pb or ca > cb: return False
        return all(x <= y for x, y in zip(da, db))

    T = [0] * V   # T[a] bit b set: a embeds in b (includes a itself)
    F = [0] * V   # F[a] bit b set: a does NOT embed in b
    for a in range(V):
        T[a] |= 1 << a
    ecount = [inv[a][0] for a in range(V)]
    for a in range(V):
        for b in range(V):
            if a == b: continue
            if ecount[a] >= ecount[b] or not inv_allows(a, b):
                F[a] |= 1 << b
    # free within-lattice containments
    seeded = 0
    for g in groups:
        t = g['t']; uc = g['uc']
        for m1 in range(1 << t):
            c1 = uc[m1]
            m2 = m1
            # enumerate strict supersets of m1 cheaply via submask trick on complement
            comp = ((1 << t) - 1) ^ m1
            sub = comp
            while sub:
                c2 = uc[m1 | sub]
                if c2 != c1 and not (T[c1] >> c2 & 1):
                    T[c1] |= 1 << c2; seeded += 1
                sub = (sub - 1) & comp
    log(f"stage 3: seeds -- {seeded} free containments; "
        f"{sum(bin(f).count('1') for f in F)} invariant/size exclusions")

    def close():
        # T transitivity (fixpoint), then rebuild F by the two rules (fixpoint)
        changed = True
        while changed:
            changed = False
            for a in range(V):
                cur = T[a]; acc = cur; m = cur
                while m:
                    c = (m & -m).bit_length() - 1; m &= m - 1
                    acc |= T[c]
                if acc != cur: T[a] = acc; changed = True
        changed = True
        while changed:
            changed = False
            # rule: T[c][a] & F[c][b] => F[a][b]  (push F up the first index)
            TD = [0] * V
            for c in range(V):
                m = T[c]
                while m:
                    b = (m & -m).bit_length() - 1; m &= m - 1
                    TD[b] |= 1 << c
            for a in range(V):
                m = TD[a]; acc = F[a]
                while m:
                    c = (m & -m).bit_length() - 1; m &= m - 1
                    acc |= F[c]
                if acc != F[a]: F[a] = acc; changed = True
            # rule: F[a][d] & T[b][d] => F[a][b]  (pull F down the second index)
            for a in range(V):
                add = 0
                for b in range(V):
                    if not (F[a] >> b & 1) and (T[b] & F[a] & ~(1 << b)):
                        add |= 1 << b
                if add: F[a] |= add; changed = True
        for a in range(V):
            assert not (T[a] & F[a]), f"T/F contradiction at class {a}"

    # resume support
    done_pairs = 0
    if os.path.exists('ckpt_order.pkl'):
        st = pickle.load(open('ckpt_order.pkl', 'rb'))
        if isinstance(st, dict) and st.get('sig') == SIG and st.get('V') == V:
            if 'order' in st:
                log("stage 3: complete checkpoint found"); order = st['order']
                pickle.dump(dict(sig=SIG, V=V, order=order, row=V),
                            open('ckpt_order.pkl', 'wb'))
                log("stage 3 complete")
                log("now run:  python3 stage4_fast.py --first")
                return
            if 'TU' in st:
                T, F = st['TU'], st['F']
                log("stage 3: resumed inference checkpoint")
        else:
            log("stage 3: signature/V mismatch -> rebuilding order matrix")

    close()
    def unknown_pairs():
        out = []
        for a in range(V):
            und = ~(T[a] | F[a]) & ((1 << V) - 1)
            m = und
            while m:
                b = (m & -m).bit_length() - 1; m &= m - 1
                out.append((a, b))
        return out

    todo = unknown_pairs()
    total_pairs = V * (V - 1)
    log(f"stage 3: after inference, {len(todo)} of {total_pairs} ordered pairs "
        f"need VF2 ({100*len(todo)/max(1,total_pairs):.1f}%)")

    import multiprocessing as mp
    reps_pickle = pickle.dumps(cat.reps)
    BATCH = max(64, args.procs * 16)
    t0 = time.time()
    with mp.get_context('spawn').Pool(args.procs, _init_worker,
                                      (reps_pickle,)) as pool:
        while todo:
            batch, todo = todo[:BATCH], todo[BATCH:]
            for a, b, res in pool.imap_unordered(_pair, batch, chunksize=4):
                if res: T[a] |= 1 << b
                else:   F[a] |= 1 << b
            done_pairs += len(batch)
            close()
            todo = [p for p in todo
                    if not (T[p[0]] >> p[1] & 1) and not (F[p[0]] >> p[1] & 1)]
            pickle.dump(dict(sig=SIG, V=V, TU=T, F=F),
                        open('ckpt_order.pkl', 'wb'))
            log(f"stage 3: {done_pairs} VF2 calls done, {len(todo)} pairs left "
                f"({time.time()-t0:.0f}s)")
    # SAMPLE VERIFICATION of the inference layers.  At n = 10 the rebuilt matrix
    # was accepted by being bit-identical to an archived full-VF2 reference; no
    # such reference exists at other degrees, and ~80% of ordered pairs are
    # decided by inference alone.  Verify a random sample by VF2 so that the
    # implementation (not merely the rules) is checked at every degree.
    import random
    from ark_intersect import mono as _mono
    rnd = random.Random(20260729)
    allpairs = [(a, b) for a in range(V) for b in range(V) if a != b]
    samp = rnd.sample(allpairs, min(args.verify, len(allpairs)))
    mism = []
    for a, b in samp:
        claimed = bool(T[a] >> b & 1)
        if claimed != _mono(cat.reps[a], cat.reps[b]):
            mism.append((a, b, claimed))
    if mism:
        log(f"stage 3: *** {len(mism)} of {len(samp)} sampled pairs DISAGREE with "
            f"VF2 -- inference is wrong, do NOT trust downstream verdicts ***")
        for a, b, c in mism[:10]:
            log(f"    class {a} -> {b}: inference said {c}")
        sys.exit("stage 3 verification failed")
    log(f"stage 3: verification PASSED -- {len(samp)} random ordered pairs "
        f"re-decided by VF2 agree with the inference matrix")

    order = [[bool(T[a] >> b & 1) for b in range(V)] for a in range(V)]
    pickle.dump(dict(sig=SIG, V=V, order=order, row=V),
                open('ckpt_order.pkl', 'wb'))
    log("stage 3 complete")
    log("now run:  python3 stage4_fast.py --first")

def _pair(ab):
    a, b = ab
    reps = _W['reps']; mono = _W['mono']
    return a, b, mono(reps[a], reps[b])

if __name__ == '__main__':
    main()
