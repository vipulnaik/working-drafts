# Consolidation docket — ARK project handoff

> **EXECUTION STATUS (Fable pass, July 26).** §1 stage-3 v3: **implemented** (inference-first: free lattice containments, equal-edge exclusion, invariant domination on degrees/tri/P₃/C₄, two-sided transitive closure, batched parallel VF2 with per-batch re-closure and checkpointing) — resolves **79.9%** of ordered pairs before any VF2 and retires ~7 further pairs per call on the n = 10 acceptance battery; bit-identical acceptance comparison **in progress** (single-core container; checkpointed, resumable). §4a: **PROVED** (duality involution theorem, notes §7.9) and its three outstanding predictions (classes 493, 439, 457) **empirically confirmed** UNSAT-pinned-0. §2: notes **rev 5 written** (§§7.9, 7.9′, 7.10, 7.11 added; certificate framing now carries literature anchors). §3: `adversary.py` **built and validated** — monotone scorpion reproduced exactly at n = 5, 6 with 141×/982× canonical-state reductions; matching-closure (decreasing mode) verified evasive at n = 6; skeleton attack at n = 10 **launched** (budgeted, memo-persistent, resumable). §4c: first-pass literature check done — instance-optimality of the scorpion found and cited; defect interpolation not found, still flagged. §4b, §4d, deeper §4c: **open**, unchanged.

*Prepared end of the Opus brainstorming stretch, July 26 2026. Everything below is either (a) a result obtained since the last notes revision that needs writing up, (b) a code change that should be made by the stronger model because it produces a persistent artifact, or (c) an open item with enough context to start on immediately. Ordered by dependency, with a recommended sequence at the end.*

---

## 0. State of play in one paragraph

`orbital-evasiveness-notes.md` is at rev 4 and does **not** yet contain: the n = 10 probe-backbone results, the complementation discovery, the scorpion analysis, or the n = 12 campaign status. The n = 10 CSP is **SAT** at the 75-group full battery (leaf-verified, reproduced on two machines); the surviving candidate skeleton is ten maximal generators archived in `skeleton.pkl`. A per-class backbone sweep (`probe_backbone.py`) is 32 % complete and still producing exact forcings. The n = 12 campaign has GAP output complete (8 819 groups) and validated, but stage 3 is parked at an unacceptable 48 h ETA pending optimization. No unconditional ARK value beyond n = 6 has been established; nothing has falsified ARK.

---

## 1. Code: stage-3 optimization (blocking n = 12) — **highest priority**

**Problem.** `consume_gap.py` stage 3 (subgraph-monomorphism order matrix) costs ~293 s/row at n = 12 versus ~19 s/row at n = 10 — a 15× per-row blowup on a *smaller* catalog (600 classes vs 1242), because 12-vertex graphs at 25–45 of 66 edges are worst-case for VF2 and the complement trick fails when neither graph nor complement is sparse. Measured ETA 172 719 s ≈ 48 h at `--maxt 8`; `--maxt 10` would be roughly a week.

**Three fixes, all valid, in increasing payoff:**

1. **Invariant pre-filters in `ark_intersect.mono()`.** Currently screens on edge count and degree-sequence domination only. Containment H ⊆ G also requires *every* subgraph count to dominate — tri(H) ≤ tri(G), C₄(H) ≤ C₄(G), P₃(H) ≤ P₃(G), and so on — all cheap and all valid necessary conditions. Should kill most negative pairs before VF2 is called.
2. **Free within-lattice containments.** If two catalog classes arise as orbital unions of the *same* group with masks m₁ ⊂ m₂, containment holds by construction — zero isomorphism tests. Seeds the matrix densely for free. (Flagged repeatedly during the session, never implemented.)
3. **Two-sided transitive inference.** Positive: a ⊆ c ∧ c ⊆ b ⟹ a ⊆ b. Negative: c ⊆ a ∧ c ⊄ b ⟹ a ⊄ b. Seed from (2), close transitively, VF2 only the pairs neither rule decides, re-close after each parallel batch. This restructures stage 3 from "independent rows farmed to workers" to "batched with shared inference," which is why it needs a real edit rather than a patch — and it changes the checkpoint format for `ckpt_order.pkl`, so bump the signature scheme accordingly.

**Acceptance test.** Re-run n = 10 at `--maxgroups 40 --maxt 8`; the resulting order matrix must be **identical** to the archived one (428 classes, relation density 0.189, zero transitivity violations), and `stage4_fast.py --first` must still return the same verified SAT. Then n = 12 at `--maxt 8` should complete in hours.

**Caution.** The order matrix is load-bearing for every downstream verdict. A too-permissive `mono()` silently invalidates every forcing and every SAT/UNSAT result. Add an assertion pass: reflexivity, antisymmetry-up-to-iso, and random transitivity sampling (the n = 10 matrix passed 20 000 random triples).

---

## 2. Write-up: notes rev 5

Four blocks of new content, all with data in hand.

**2a. The n = 10 backbone (from `probe_results.csv`, 793 probes / 397 classes / 25.9 h).** Exact forcings under the full 75-group primal+dual battery: **25 classes forced IN** (edge counts 0–10) and **18 forced OUT** (35–45). UNSAT-on-pin verdicts are exact theorems, so these are unconditional statements about every property satisfying the battery's conditions. Named members of the forced-IN set worth quoting: the empty graph, K₃, K₄, C₁₀, the perfect matching, K₁,₈, and assorted forests. Discovery rate is steady at ~5 forcings per 100 probes across the whole sweep (8, 9, 3, 6, 3, 9, 2, 3 per block of 100), so the remaining ~845 classes should yield ~85 more.

**2b. The complementation theorem (new, and it resolves an open question).** All 18 forced-OUT classes are complements of forced-IN classes — 15 verified against already-probed classes, 3 predictions pending (classes 493, 439, 457 should come back forced IN). Examples: C₁₀ ↔ co-C₁₀, K₄ ↔ co-K₄, perfect matching ↔ its complement, K₃ ↔ co-K₃, ∅ ↔ K₁₀. **This is §7.6's dual battery caught in the act**: it converts every sparse forced-IN class into a dense forced-OUT class, which is precisely the down-forcing that §7.5's one-sidedness analysis said the primal machinery lacked. It is nonetheless insufficient — the two forced sets stay pinned to the extremes (≤ 10 and ≥ 35 edges) and never meet in the middle, which is *why* the CSP remains SAT. Given the dual conditions have the form y[S] = 1 − x[comp S], this ought to be a short proof rather than an empirical pattern; **proving it is a docket item in its own right** (see §4a) and would halve the remaining probe cost.

**2c. Correction: the "free middle band" framing of rev 3–4 is too crude and must be replaced.** The forced/free distinction is *not* density-stratified. Classes with ≤ 4 edges are uniformly forced IN and ≥ 41 uniformly forced OUT, but across the entire range 5–40 forced and free classes coexist at every edge count — 29 free classes at ≤ 10 edges interleave with the 25 forced-IN ones. Clean witness that no invariant-based heuristic can predict the backbone: **classes 5 and 43 are both 35-edge, 7-regular, with 50 triangles and 200 four-cycles, yet class 43 is forced OUT and class 5 is free.** The distinction is visible only in the complement — cls 43 = co-C₁₀, cls 5 = co-(C₅ ⊔ C₅) — and follows from 2b plus the fact that C₁₀ is forced IN while 2C₅ is free.

**2d. The scorpion section** (new material, none of it in the notes). Content: the elimination-engine mechanism — sting/tail/body are pinned by degree constraints that are *two-sided*, so every query answer disqualifies a candidate for some role, giving linear convergence; this is the celebrity-problem trick ("does a know b?" — yes kills a, no kills b) transplanted into undirected graphs. Why monotonicity destroys it: a positive answer can never disqualify anything, it only moves you toward membership, so half the engine is unavailable by fiat. **The structural point worth stating prominently:** monotonicity is not a hypothesis that happens to rescue ARK, it is what makes the topological method *definable* — non-monotone P has no downward-closed family, hence no complex, no χ, no Oliver argument. So the scorpion is not a counterexample the method must dodge; it inhabits a regime where the method's central object does not exist. **The duality worth recording:** the algorithmic one-sidedness (no pruning from positive answers) and the CSP one-sidedness (everything forces into P, only nontriviality forces out) are two faces of the same fact — monotone properties admit no upper-bound constraints. **Verified computation to include:** the monotone closure of the scorpion property, P = "∃ s, b and t ∉ {s,b} with {s,t} ∈ E and b adjacent to every vertex but s", is monotone, nontrivial, and **evasive at n = 4, 5, 6** by exact adversary search (states 276 / 28 869 / 3 563 639; code in `scorpion_test.py`, to be staged). Same combinatorial structure, O(n) queries with exact degrees, all C(n,2) once monotonized — the sharpest available illustration of where the linear algorithm's power comes from. **And the connection to our data:** three of the ten maximal generators of the n = 10 skeleton are **apex graphs** (K₁+3K₃, K₁+C₉ at 18 edges, K₁+K₄+5K₁ at 15), i.e. graphs with a dominating vertex — the scorpion's *body*. Corroborating detail from the backbone: K₁,₈ is forced IN but K₁,₉ (the spanning star) is **free**, so a monotone property is permitted to exclude the spanning star, which is exactly what an apex-witness property needs to stay nontrivial. If a counterexample at n = 10 exists, the CSP is pointing at apex-generated properties, and that is where the adversary search of §3 should aim.

**2e. n = 12 campaign status.** GAP output complete and validated: 8 819 groups (295 trivial-top, 657 at q = 2, 67 at q = 3, plus 6 094 p-groups); at `--maxt 8`, 2 293 raw → 59 kept → 600 catalog classes. Stage 3 parked pending §1. Note the transitive census finding: at degree 12 the wreath bound appears optimal — m\* = 18 achieved six ways, exceeded zero ways.

---

## 3. Code: the canonical-state adversary searcher — **highest marginal value**

The one tool that can *decide* rather than constrain, and the only route to testing the skeleton. `scorpion_test.py` has the correct recursion:

> `undetermined(L,A) = ¬P(L) ∧ P(all ∖ A)` (valid for monotone P);
> `survive(L,A) = undetermined(L,A) ∧ ∀ unqueried e ∃ answer: survive(child)`; base case |L|+|A| = N−1;
> P is evasive iff `survive(∅,∅)`.

It has no isomorph reduction, so it dies past n = 6. Needed: memoize on the **canonical form of the 3-coloured state** (present / absent / unqueried) via nauty certificates — this is the branch-wise symmetry reduction that makes the state space a DAG over isomorphism classes rather than a tree, ~3^{C(n,2)}/n! (≈ 10^{8.8} at n = 8, ≈ 10^{15} at n = 10 in general, but far smaller for a single fixed property with monotone early-exit pruning). Then point it at the ten-generator skeleton from `skeleton.pkl`. Either outcome is publishable: an adversary strategy proves that candidate evasive and removes it from the residual space; a decision tree of depth ≤ 44 **falsifies ARK at n = 10**.

---

## 4. Mathematics

**4a. Prove or refute the complementation rule** (see 2b): "the n = 10 backbone is closed under complementation, exchanging IN and OUT." Should follow from the dual conditions' form y[S] = 1 − x[comp S] together with the fact that complementation maps orbital unions of Γ to orbital unions of the same Γ. If it is a theorem: halves the remaining probe cost (probe only the sparse half, derive the dense verdicts) and gives the cleanest statement of what duality contributes. The three unprobed predictions are a free empirical test before relying on it.

**4b. Re-derive the extremal constants over the wreath-inclusive template** (Open Problem 2 in the notes). The rev-3 wreath correction invalidated the old layer-assignment case analysis, so §5's c\* and both δ₀ values are currently quoted as provisional. Also settle whether the n = 2p wreath value 1/4 is optimal on that family — the Appendix A table now brackets μ(22) ∈ [110, 115], narrow enough that a GAP sweep at n = 22 could determine μ(2p) = p(p−1) for one value.

**4c. Literature check before publication claims.** (i) The defect-interpolation idea — parametrize monotonicity defect and ask for D(P) ≥ N − g(defect), interpolating between the scorpion (high defect, D = O(n)) and ARK (defect 0, D = N). I could not verify whether this has been studied and it should not be written up as novel without a search. (ii) Whether the monotone-scorpion evasiveness is already covered by a known evasive class (it may fall under a published family, in which case cite rather than claim).

**4d. Remaining n = 10 gaps.** χ of the two structural closures (subgraphs of C₅[K₂]; of C₅ ⊔ C₅ ∪ K₅,₅) to finish the §7.4 minimal-completion screen — needs C-level canonical enumeration, ~10⁵–10⁶ classes each. And the global condition χ(Δ_P) = 1 over all 2^45 graphs is *not* enforced by the CSP, which is one of the two known gaps in the SAT certificate; worth stating explicitly in rev 5 even if not computed.

---

## 4.5 Low priority: the decision-tree counting thread (closed, recorded for completeness)

A side investigation into naively bounding the number of adaptive decision trees on graphs, pursued for its own sake. It reached a clean conclusion — **no counting-flavoured argument can prove ARK** — and produced one reframing worth keeping. Recorded here mainly so nobody re-treads it.

**The bound.** With N = C(n,2), a tree has 2^m nodes at depth m, each choosing among N − m unqueried edges, giving ∏_{m=0}^{N-2} (N−m)^{2^m} (the m = N−1 factor is 1). Substituting j = N − m gives log₂ = 2^N · Σ_{j≥2} log₂(j)/2^j, and that sum converges to **0.7326**, so the count is 2^{0.733·2^N} — i.e. log log₂ = N − 0.449, doubly exponential in N and hence 2^{2^{Θ(n²)}}. At n = 10 that is 2^{2.6×10¹³}.

**Why counting cannot prove ARK.** Compare Dedekind: monotone Boolean functions on N variables number 2^{C(N,N/2)} = 2^{4.1×10¹²} at n = 10, and monotone *graph* properties only about 2^{1.1×10⁶} (middle layer ÷ n!). Trees vastly outnumber properties, and non-evasive trees are almost all trees, so there is no union bound, no pigeonhole, no "too few algorithms to cover all properties" route. The thread is closed on this point.

**Two missteps, both instructive, both corrected by user pushback:**

1. *Conflating two notions of "distinct".* Asked for the optionality at each node up to symmetry, I computed instead the number of level-2 *trees* up to relabeling — orbits of Stab({1,2}) = S₂ × S_{n−2} on ordered pairs (present-branch query, absent-branch query), which is **11** for n ≥ 6 (4 with both queries meeting {1,2}, 2 + 2 mixed, 3 with both disjoint) — and wrongly called the per-node count of **4** an error. Both numbers are right for their respective questions; the per-node reading was the intended one.
2. *Asserting a single factor of n! as the ceiling on symmetry savings.* This is correct only for the equivalence "trees related by one global σ ∈ S_n" (orbit counting: a group of order n! has orbits of size ≤ n!). It is **wrong for the reduction actually in play**, where at each node the choice matters only up to Aut(current 3-coloured state) — legitimate for graph properties precisely because P is S_n-invariant, so survivability from a state depends only on its isomorphism class, and different branches reduce *independently*. The available saving is of order ∏_m |Aut_m|^{2^m}, not n!. Compounding the error, I had written "(n!)^{2^m}" two paragraphs earlier without noticing the tension.

**The corrected accounting**, which preserves the conclusion for a better reason. Residual symmetry of a partial state is dominated by S_{untouched vertices}, so it dies once every vertex has been touched — coupon-collector, m ≈ (n/2)·ln n. Bounding the saving by the levels below that cutoff, log₂(saving) ≲ 2^{M+1}·log₂(n!) with M ≈ (n/2)ln n:

| n | log₂(all trees) | log₂(max symmetry saving) | fraction of the log |
|---|---|---|---|
| 8 | 1.97×10⁸ | ≤ 9.8×10³ | 5×10⁻⁵ |
| 10 | 2.58×10¹³ | ≤ 1.3×10⁵ | 5×10⁻⁹ |
| 12 | 5.41×10¹⁹ | ≤ 1.8×10⁶ | 3×10⁻¹⁴ |

So the saving is astronomically larger than n! (the user's point stands) and still a vanishing sliver of the total (the conclusion stands). The mechanism is the one identified at the outset: the product's mass sits at levels m near N, where 2^m nodes each still face ~N−m choices *and* generic states are asymmetric, so no reduction of any kind is available there.

**The one durable takeaway**, which feeds §3. The branch-wise state equivalence is exactly what turns the search space from a tree into a **DAG over isomorphism classes of 3-coloured states**, of size ~3^{C(n,2)}/n! — ≈ 10^{4.3} at n = 6, 10^{6.3} at n = 7, 10^{8.8} at n = 8, 10^{15} at n = 10. That is the design principle behind the canonical-state adversary searcher: the counting thread's only positive contribution, and the reason §3 is feasible at all for a single fixed property with monotone pruning.

**Also worth recording from the same discussion** (and relevant to §2d): ARK is equivalent to the claim that monotone graph properties always exhibit a *maximal* gap between decision-tree depth D and certificate complexity C. The scorpion is certificate-optimal (D ≈ C ≈ O(n)); monotone graph properties can have tiny certificates (triangle-containment: C₁ = 3) yet ARK asserts D = N always. Stated that way, ARK is the assertion that no search-and-verify strategy ever works for monotone graph properties, however small their witnesses — a more useful mental model than "you have to query everything."

---

## 5. Operational notes

- **Probe sweep** (`probe_backbone.py`, running off and on): 397/1242 classes done, 25.9 h, ~55 h remaining at current rate. 47 CAP verdicts cluster at 9–36 edges and are the time sink (max 63 min, mean 118 s vs median 46 s); the CAPs at **9–14 edges** are the valuable re-probe targets at higher `--nodecap`, since resolving them either lifts the forced-IN frontier above 10 edges or confirms it stalls. If 4a lands, restrict the sweep to sparse classes.
- **Flag hygiene** (just patched): `consume_gap.py` now records `--maxgroups/--maxt` in `ckpt_groups.pkl` and adopts them on a bare rerun; a genuine mismatch prints both flag sets. The recent n = 12 rebuild was caused by `--maxt 8` → `--maxt 10` (confirmed: "2293 raw" is exactly the t ≤ 8 cumulative count), not by `--procs`, which is deliberately outside the signature.
- **Directory discipline**: canonical scripts in one place, per-degree working directories (`n10/`, `n12/`); GAP takes `ARK_N` from the environment. GAP's `done_keys.txt` does not embed the degree, so directory separation is a mechanism, not a convention.
- **Files staged**: `check_groups.py` (institutionalized pre-flight validator, auto-detects n, PASS/FAIL green-light checks), `probe_backbone.py` (now hard-errors when `--auto` lacks `solution1.pkl`, logs targets, 30 s heartbeat inside probes), `stage4_fast.py` (saves `solution1.pkl`; leaf-verifies every group), `mu_fast.py` + `mu_table_full.csv` (closed-form μ lower bounds to n = 1000, proper CSV quoting), `skeleton.pkl`. **Not yet staged: `scorpion_test.py`** — should be added when 2d is written.

---

## 6. Recommended sequence

1. §1 stage-3 optimization, with the n = 10 acceptance test. *Unblocks everything at n = 12.*
2. §4a complementation proof. *Cheap, halves probe cost, and is the cleanest new theorem available.*
3. §2 notes rev 5 (all five blocks). *Largest volume of unrecorded results; do it before more compute accumulates.*
4. §3 adversary searcher, aimed at the apex-generated part of the skeleton. *Highest marginal value: the only two-sided tool.*
5. §4b, §4c, §4d as capacity allows.
6. §4.5 needs no work — it is closed. Fold its one durable result (the state-DAG sizing, and the D-versus-C framing of ARK) into rev 5 alongside §2d if a natural place appears; otherwise leave it in this docket as a record of ground already covered.

Two standing cautions from this session's error record. Errors in conversation were caught within a message by the user's pushback; errors in artifacts survived far longer — a solver bug produced a **false SAT** that lived until independent reproduction, a checkpoint-coherence bug burned 6.5 h of compute, and wrong mathematical claims (the bounded-block repair for odd n, the (2,6) chain's local failure at 3 | n, the "3/2 is template-intrinsic" claim) persisted across two notes revisions. Hence: any solver change re-runs the archived acceptance tests, and any new construction gets its local solubility checked at small primes before it is written down.
