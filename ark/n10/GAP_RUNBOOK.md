# Runbook: GAP-powered full battery for ARK at n = 10

Two programs, run in sequence. GAP enumerates the groups (its comparative advantage: subgroup lattices, transitive-groups library, wreath products); Python consumes them and runs the primal+dual χ + Smith CSP (files from the session: `ark_intersect.py`, `smith.py`, and the new `consume_gap.py` must sit in the working directory).

## 0. Install

- **GAP** ≥ 4.11 with the `transgrp` package (bundled in standard distributions). Linux: `apt install gap` usually suffices; check with `gap -q -c 'LoadPackage("transgrp"); Print(NrTransitiveGroups(10), "\n"); QUIT;'` — must print `45`.
- **Python** side: `pip install networkx pynauty` (pynauty only if you later extend; the CSP itself needs just networkx).

## 1. Run GAP

```
cd <workdir>            # ark_gap.g here; outputs land here too
gap -q -o 4g ark_gap.g
```

`-o 4g` raises the memory ceiling (stage C with p=2 wants it). Runtime: stages A/B/B2 in minutes; stage C minutes for p=3,5,7 and possibly ~an hour for p=2 (the Sylow 2-subgroup has order 256 and a large subgroup lattice — this is the one heavy step among the defaults).

**Checkpointing model.** Every finished group appends one line to `groups_out.txt` and its key to `done_keys.txt`. Kill it any time (Ctrl-C); rerun the same command to resume — completed keys are skipped, so at most one group is recomputed. The two files are append-only; don't edit them mid-run. Progress and timestamps go to `ark_gap.log` and stdout. To redo a stage from scratch, delete its keys from `done_keys.txt` (keys are prefixed `A:`, `B:`, `B2:`, `C:`) — or simplest, move both output files aside and rerun.

**Stage selection.** Edit `STAGES := [ "A", "B", "B2", "C" ];;` at the top. Recommended first run: exactly that default. `"FULL"` (all subgroup classes of S₁₀, filtered to Oliver) is deliberately off: the single call `ConjugacyClassesSubgroups(S10)` is hours-to-days, gigabytes of RAM, and **not checkpointable internally** (per-group emission after it *is* checkpointed). Run FULL only on a server you can leave alone, with `-o 16g`, ideally under `nohup`/`tmux`. The default stages already cover: all 45 transitive groups of degree 10, all direct products of transitive groups over partitions into ≤ 4 parts, both imprimitive wreath families (2≀5, 5≀2 — this is where the block-swap groups live), and every p-subgroup of every Sylow subgroup up to Sylow-conjugacy (the Smith battery, including the coupled diagonal 2-groups that Runs 6–7 lacked).

**Sanity checks after GAP finishes:**
- `grep -c '^A:' groups_out.txt` — should be well under 45 (only the Oliver transitive groups with ≤ MAXT orbitals survive; expect roughly the metacyclic/affine-type ones — if you get 0, the Oliver filter is broken; if 45, it isn't filtering).
- Every line has exactly 3 `|` characters and 45 comma-separated integers in the last field: `awk -F'|' 'NF!=4' groups_out.txt` should be empty.
- Spot-check one known group: some `B2:` line for T(2,1)≀T(5,1) (= our ℤ₂⁵⋊C₅ block group) should exist with tag `0` and orbital sizes recoverable as {5,20,20}.

**Known failure modes.**
- `TransitiveGroup: not available` → `LoadPackage("transgrp")` failed; install the package (`apt install gap-transgrp` on Debian-family, or GAP's `InstallPackage`).
- `StringFile` undefined → GAPDoc not loaded; add `LoadPackage("GAPDoc");` at the top.
- Memory exhaustion in stage C p=2 → rerun with `-o 8g`; if still failing, replace `ConjugacyClassesSubgroups(P)` for p=2 with `ConjugacyClassesSubgroups(P : OrderLimit := 64)` variant (or filter `Filtered(ccs, c -> Size(Representative(c)) <= 64)`) — subgroups of order > 64 almost always exceed MAXT orbitals anyway and would be skipped downstream.
- If a run was killed *mid-append* (rare), the last line of `groups_out.txt` may be truncated; the awk check above finds it — delete that line and its key, resume.

## 2. Run Python

```
python3 consume_gap.py --maxgroups 200 --maxt 10
```

Stages (each with its own checkpoint file; delete a `ckpt_*.pkl` to redo that stage):
1. Parse + dedup by orbital-partition signature → `ckpt_groups.pkl`. Dedup is invariant-level (orbital sizes + per-vertex degree types); collisions merely add a redundant constraint, which is harmless.
2. Union-graph catalog with isomorphism dedup → `ckpt_catalog.pkl`, checkpointed every 5 groups. **This is the slow stage** (VF2 isomorphism against a growing catalog); with 200 groups of t ≤ 10 expect hours. Watch `consume_gap.log`; the class count should grow sublinearly (heavy overlap between groups' lattices) — if it grows by ~2^t per group, the dedup invariants are missing (report it).
3. Subgraph-monomorphism order matrix → `ckpt_order.pkl`, checkpointed every 3 rows. Also slow (mid-density VF2); the complement trick in `ark_intersect.mono` handles the worst pairs.
4. CSP solve → `csp_result.txt`. Fast relative to 2–3. Output is either **`UNSAT => ARK holds unconditionally at n=10`** — the headline result, at which point please rerun stage 4 once from clean checkpoints as a reproduction — or a pattern count with the forced-IN/OUT backbone, which quantifies how much the enlarged battery shrank the space (compare: 18 patterns / backbone {5-edge matching IN, ≥40 OUT} from the 5-group session battery).

**Scaling knobs if stage 2/3 are too slow:** lower `--maxgroups` (the Oliver groups are sorted by minimum orbital size, so truncation keeps the strongest annihilators; all p-groups are always kept), or lower `--maxt` to 8 (halves lattice sizes; the cost is losing fine-lattice discriminators). Conversely, if everything is fast and SAT, raise both and add `"FULL"` on the GAP side.

## 3. Interpretation and escalation

- **UNSAT** at any battery size = unconditional ARK at n = 10 (first composite non-prime-power beyond 6). The proof object is: the group list (`groups_out.txt`), the catalog, and the CSP trace — worth archiving all checkpoints.
- **SAT with shrinking backbone**: the residual patterns' forced-IN/OUT profile tells you which of the three attacks from the notes (§7.7) to run next: if the free middle band (edge counts between the max forced-IN and min forced-OUT) narrows below ~10 edges, the dual χ-magnitude screen on both endpoints likely finishes it; if the band is static, the miss is lattice-decoupling and stage FULL is the escalation.
- Not covered by this pipeline (separate jobs, flagged in the notes): exact χ of the two structural closures (subgraphs of C₅[K₂] and C₅⊔C₅ ∪ K₅,₅ — a C+nauty enumeration, not GAP), and the n = 12 rerun (change `SymmetricGroup(10)`→`(12)`, `Combinations([1..12],2)` (66 pairs), the partition/wreath stages accordingly, and the Python `PAIRS`/sizes — grep both files for `10` and `45`).
