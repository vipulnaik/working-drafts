"""
compare_order.py -- certify a stage-3 (v3) order matrix against a reference.

Usage:  python3 compare_order.py NEW_ckpt_order.pkl REF_ckpt_order.pkl

Accepts any checkpoint format this project has produced (v1 'order'+'row',
v2 'rows' dict, v3 final 'order', or v3 partial 'TU'/'F' -- partials are
reported as incomplete, with a count of undecided entries).  Prints PASS only
if both are complete, same V, and bit-identical.  Exit code 0 iff PASS.
"""
import sys, pickle

def load(path):
    st = pickle.load(open(path, 'rb'))
    if not isinstance(st, dict):
        sys.exit(f"{path}: unrecognized (not a dict)")
    if 'order' in st:
        order = st['order']
        return [[bool(x) for x in row] for row in order], None
    if 'rows' in st:
        V = st['V']
        if len(st['rows']) != V:
            return None, f"{path}: v2 partial ({len(st['rows'])}/{V} rows)"
        return [[bool(x) for x in st['rows'][a]] for a in range(V)], None
    if 'TU' in st:
        V = st['V']; T, F = st['TU'], st['F']
        undecided = V * V - sum(bin(T[a] | F[a]).count('1') for a in range(V))
        if undecided:
            return None, f"{path}: v3 partial ({undecided} entries undecided)"
        return [[bool(T[a] >> b & 1) for b in range(V)] for a in range(V)], None
    sys.exit(f"{path}: unrecognized checkpoint keys {sorted(st.keys())}")

if len(sys.argv) != 3:
    sys.exit(__doc__)
new, err1 = load(sys.argv[1])
ref, err2 = load(sys.argv[2])
for e in (err1, err2):
    if e: print(e)
if err1 or err2:
    sys.exit("INCOMPLETE -- rerun when stage 3 finishes")
if len(new) != len(ref):
    sys.exit(f"FAIL: V mismatch {len(new)} vs {len(ref)}")
V = len(new)
diffs = [(a, b) for a in range(V) for b in range(V) if new[a][b] != ref[a][b]]
if diffs:
    print(f"FAIL: {len(diffs)} differing entries; first 10: {diffs[:10]}")
    sys.exit(1)
n_true = sum(sum(r) for r in new)
print(f"PASS: matrices bit-identical (V={V}, {n_true} true entries, "
      f"density {n_true/(V*V):.3f})")
