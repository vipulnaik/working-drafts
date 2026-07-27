"""
probe_targets.py -- emit the remaining probe list for probe_backbone.py,
halved using the duality involution theorem (notes 7.9).

Since forced-IN and forced-OUT are exchanged by complementation, probing one
representative per complement pair suffices: the partner's verdict is implied.
This script pairs catalog classes by nauty certificate of the complement,
drops pairs already decided, and emits the SPARSER member of each undecided
pair (sparse probes are empirically much cheaper).

Usage (from the directory holding ckpt_catalog.pkl and probe_results.csv):
    python3 probe_targets.py                 # print summary + --classes string
    python3 probe_targets.py --emit          # print only the comma list
    python3 probe_targets.py --limit 200     # first N targets, sparsest first
Then:
    python3 probe_backbone.py --classes "$(python3 probe_targets.py --emit)" \
        --nodecap 20000000
"""
import pickle, csv, os, sys, argparse, itertools
import networkx as nx
import pynauty

ap = argparse.ArgumentParser()
ap.add_argument('--emit', action='store_true')
ap.add_argument('--limit', type=int, default=0)
ap.add_argument('--catalog', default='ckpt_catalog.pkl')
ap.add_argument('--results', default='probe_results.csv')
args = ap.parse_args()

cst = pickle.load(open(args.catalog, 'rb'))
reps = cst['cat'].reps
V = len(reps)
n = reps[0].number_of_nodes()

def cert(G):
    adj = {v: list(G.neighbors(v)) for v in range(n)}
    return pynauty.certificate(pynauty.Graph(n, adjacency_dict=adj))

by_cert = {}
for i, G in enumerate(reps):
    by_cert.setdefault(cert(G), i)
partner = {}
for i, G in enumerate(reps):
    j = by_cert.get(cert(nx.complement(G)))
    if j is not None:
        partner[i] = j

decided = {}
if os.path.exists(args.results):
    for r in csv.reader(open(args.results)):
        if r and r[0] != 'class' and r[2] in ('UNSAT', 'SAT'):
            decided.setdefault(int(r[0]), set()).add(r[1])
fully = {c for c, v in decided.items() if len(v) == 2 or 'UNSAT' in v}

targets = []
seen = set()
for i in range(V):
    j = partner.get(i)
    if i in seen: continue
    pair = {i} if j is None else {i, j}
    seen |= pair
    if pair & fully: continue                      # verdict implied by theorem
    pick = min(pair, key=lambda c: reps[c].number_of_edges())
    targets.append(pick)
targets.sort(key=lambda c: reps[c].number_of_edges())
if args.limit: targets = targets[:args.limit]

if args.emit:
    print(','.join(map(str, targets)))
else:
    unpaired = sum(1 for i in range(V) if i not in partner)
    print(f"catalog: {V} classes, {V - unpaired} in complement pairs, "
          f"{unpaired} unpaired (complement not in catalog)")
    print(f"pairs with a verdict already: {len(fully)} classes decided")
    print(f"remaining targets (one per undecided pair, sparsest member): "
          f"{len(targets)}")
    print(f"edge counts: {[reps[c].number_of_edges() for c in targets[:20]]}...")
    print(f"\n--classes {','.join(map(str, targets[:20]))}{',...' if len(targets)>20 else ''}")
