import collections
n = 10 # replace by n used
tags, ts, bad = collections.Counter(), collections.Counter(), 0
for ln in open('groups_out.txt'):
    ln = ln.strip()
    if not ln: continue
    parts = ln.split('|')
    if len(parts) != 4: bad += 1; continue
    om = [int(x) for x in parts[3].split(',')]
    t = max(om)
    if len(om) != n * (n - 1) / 2 or sorted(set(om)) != list(range(1, t+1)): bad += 1; continue
    tags[parts[2]] += 1; ts[t] += 1
print("malformed:", bad)
print("tags:", dict(tags))       # counts per '0', each prime q, 'P2','P3','P5','P7'
print("t distribution:", dict(sorted(ts.items())))
