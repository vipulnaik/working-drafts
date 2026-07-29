# Pending runs and unverified details in the scripts

*Companion to `orbital-evasiveness-notes.md` and `enumeration-proof.md`. Written July 2026 after a review pass over `mu_enumerate.py`, `consume_gap.py`, `stage4_fast.py`, `probe_backbone.py`, `chi_test.py`, `ark_intersect.py`, `smith.py`, `oliver_mu.py` and `ark_gap.g`. Everything here is either a run that has not happened or an assumption a script makes that nothing has checked. Items are ordered by value per unit of effort within each section, not by severity.*

**How to read the status labels.** *Verified* means an independent computation agreed. *Sound* means an argument was read and found correct, with no independent computation. *Unverified* means neither. *Corrected* means a defect was found and fixed in the accompanying files, and the correction has not itself been exercised on a full run.

---

## A. Runs that should happen before the next verdict is quoted

**A1. Rebuild the n = 12 battery with the corrected dedup key.** `consume_gap.py`'s stage-1 key was an incomplete invariant used to discard groups; it is now a canonical form of the orbital partition. Because the selection signature changes, a bare rerun will detect the mismatch and rebuild stages 1–3 automatically. Expected effect at n = 12: the battery grows from 381 to 425 distinct (partition, prime) conditions, and at `--maxt 8` from 205 to 230. Cost: stage 2 and stage 3 rerun. **Nothing downstream of the old key should be quoted as a verdict until this has run**, because a dropped condition can only turn a real UNSAT into SAT.

**A2. Run the stage-3 sample verification at n = 12.** Now automatic (`--verify`, default 3000 random ordered pairs re-decided by VF2). The n = 10 acceptance test was bit-identical agreement with an archived full-VF2 reference; there is no such reference at any other degree, and roughly 80% of ordered pairs are settled by inference alone. Until this passes, the n = 12 order matrix is an unchecked implementation of checked rules.

**A3. Settle the duality involution empirically.** `probe_backbone.py` now computes the complement class of every forced class and reports violations plus the specific unprobed complements the theorem predicts. Three pressure points exist in the current n = 10 record and all are cheap to close:
- the three forced-OUT classes at 38 edges (393, 401, 405) require three forced-IN classes at 7 edges, and the only 7-edge class probed (**class 108**) came back **free**. If 108 is the complement of any of the three, **the theorem is contradicted**; if not, the partners are unprobed.
- the five forced-IN classes at 8 edges require five forced-OUT at 37 edges; no 37-edge class has been probed.
- the forced-IN class at 2 edges requires a forced-OUT at 43; no 43-edge class has been probed.

The practical corollary of the theorem — probe one representative per complement pair, halving the sweep — is currently being relied on without this check.

**A4. Re-probe the 54 CAP classes at a larger node budget.** They sit at 12–36 edges, concentrated at 24, 28, 30, 33, 34, i.e. through the middle of the free band. A CAP class is *not* free. The log shows `--nodecap` was already raised from 5×10⁶ to 2×10⁷ partway through the sweep, so the earlier CAPs may resolve without a new idea. Until then no statement of the form "the band is free from 11 to 34 edges" is supported.

**A5. Decide how S will be computed at n = 12 before the CSP verdict arrives.** `chi_test.py` enumerates the full down-closure with a canonicalisation per node: 64,333 classes and about 60 s at n = 10, against `--cap 5000000`. At n = 12 the ambient count is 1.65 × 10¹¹ iso classes and the closure of an 18-edge-or-larger generator set may well exceed the cap. The global χ test is the only test that has actually killed anything, so losing it at n = 12 would be a real loss. The alternative is the §8.4 route — exponential formula over signed connected-component weights, two-sort EGF for bipartite components — which computes S without enumerating the closure. This is a design decision, not a bug.

**A6. Migrate `mu_table_safe.csv`, do not regenerate it.** The schema change is cosmetic and the 1,460 existing rows are correct and independently verified; `migrate_table.py` renames `orbits_K` to `certified_K` and derives `parts` from the witness string and `partcap` from the density, recomputing no value of B(n). It ran clean on the real table (0 inconsistencies, and every row satisfies both parts ≤ partcap and 1/√δ ≤ certified_K), and the migrated file resumes correctly from n = 1765. Regenerating instead would cost roughly the whole n^2.9 budget again for no gain.

**A7. Verify the dedup-collision audit at n = 10.** The measurement in §8.7′ was made at n = 12 because `groups_out.txt` for n = 12 was to hand. The same audit at n = 10 would say how much the *published* n = 10 SAT was affected, which matters for how the skeleton and the χ kill should be described. Requires the n = 10 `groups_out.txt`.

---

## B. Assumptions the scripts make that nothing has checked

**B1. `Catalog.classify` is a mutating lookup used as a pure query.** In `stage4_fast.py`, `probe_backbone.py` and `chi_test.py` the idiom `x[cat.classify(set())] = 1` assumes the empty graph is already in the catalog. If it were not, `classify` would **append**, silently extending `cat.reps` and desynchronising `V` from the order matrix. The same hazard applies to the complement lookups in the new involution check, which is why that block asserts the catalog did not grow. Status: **unverified, latent.** A `classify_or_fail` variant used everywhere the catalog is meant to be read-only would close it permanently.

**B2. `mono` is only ever called on representatives with the same vertex count.** The complement trick in `ark_intersect.mono` rests on the identity σ(E_H) ⊆ E_G ⟺ σ⁻¹(E_Ḡ) ⊆ E_H̄, which requires σ to be a **bijection** — true when H and G both carry all n vertices, false for a genuine injection. Every catalog representative does carry all n vertices, so the call sites are fine. Status: **sound, but undefended.** An assertion on the vertex counts inside `mono` would make it safe against reuse.

**B3. Purely-foreign configurations are reachable.** `best_with_k` skipped a prime p when no power of p landed in the pruning window, which is justified only for configurations containing a p-characteristic part. Configurations with a trivial bottom layer (all parts foreign) are legitimate Oliver groups, and reaching them relied on some *other* p surviving the skip and happening to make every part foreign — true in practice, unproven in general. Status: **corrected** — an explicit sentinel `p = 0` meaning "trivial bottom layer" is now enumerated and never skipped. The correction did not change B(n) on any of the 85 regression values.

**B4. The refined intra-orbital formula for partial capacity.** This is Part J item 2, restated here because it is the only place where the *code* computes something the *proof* does not fully license. Where Lemma C strictly reduces a p-characteristic twist, SAFE mode scores F·C(c,2) (valid for any stabiliser) while the construction reaches only F·orb(c, d). The bound stays valid; attainment does not. Reduces to one question: for a primitive affine orbit 𝔽_c ⋊ H with H cyclic-by-q and cyclic-layer image of order d, is the minimum ±H-orbit on 𝔽_c∖{0} at most 2d? Status: **open.** Empirically the fallback is invoked on a winner at **0 of 1,460** values, so μ(n) = B(n) throughout the computed range, but no argument excludes it at larger n.

**B5. Exhaustiveness of the four GAP stages.** Only the Oliver-condition test and the emission logic of `ark_gap.g` have been read. `IsOliverTop` is **sound** — taking Γ₂ = `PCore(N,p)` is WLOG since any normal p-subgroup with cyclic quotient lies in O_p(N) and the quotient is then a quotient of a cyclic group; and normality in Γ is automatic because O_p(N) is characteristic in N with N ◁ Γ. What has *not* been checked is whether stages A–D together are exhaustive over the intended families (transitive groups, direct products over partitions, imprimitive wreaths, p-subgroups up to Sylow-conjugacy). The n = 10 and n = 12 exhaustive comparisons are evidence that they are, at those degrees.

**B7. `TemplateGroup` places the block rotation in the cyclic middle layer, and that is the real template bug.** §2.4's implementation note describes the defect as a spurious gcd(d, k) = 1 filter plus a prime-only k, and both symptoms are visible in `candidate_groups`. They are not the cause. `TemplateGroup`'s own chain model puts the rotation in Γ₁/Γ₂ — its docstring requires d, the foreign primes and s pairwise coprime — and separately enforces k = s with s prime. Theorem 2.4 places the rotation in the top q-group, whence any d | c−1 is admissible and k need only be a prime power. Consequence: the template misses μ(10) = 20 (k = 2, d = 10) and μ(12) = 18 (k = 4).

**Do not repair this in the enumerator alone.** I tried; relaxing the filter builds groups that `TemplateGroup` marks invalid, and an unconditional `break` over the twist candidates then discards the smaller d that had been working — **n = 22 fell from 110 to 55**. The change was reverted and the defect documented in place. The `break` bug is genuine and independent and has been fixed (break only after a valid group is actually produced); with it fixed and the filter restored, the template reproduces Run 1 exactly at n = 6, 10, 12, 15, 18, 21, 22, 26 (6, 10, 10, 30, 36, 28, 110, 78). The real repair is to move the rotation into the top layer inside `TemplateGroup`, updating its Oliver validity check and `desc_parts`, which also changes what `top_prime` parses. Status: **open, deliberately deferred** — the GAP path has no such restriction and supersedes this enumerator, so the value is in correctness of the record rather than in better μ bounds.

**B6. The lcm strengthening is implemented but unexercised.** `IsOliverTop` now returns every usable top prime as a `+`-separated tag and the solvers enforce χ ≡ 1 mod lcm. Single-prime tags parse identically, so old files behave exactly as before — which also means **the new path has never run**. It needs one GAP re-emission and a check that some group actually receives a multi-prime tag before the strengthening can be claimed.

---

## C. Verified this pass — recorded so it is not re-done

- **`fp_acyclic` is correct.** Cross-checked against an independent dense-elimination implementation of reduced F_p homology on 4,000 randomised downward-closed complexes (t = 2…6, p ∈ {2,3,5,7,11}): **zero disagreements**. Genuine p-dependence confirmed on a triangulated RP² (False at p = 2, True at p = 3, 5, 7) — the property none of the original self-tests could detect, since all five used p = 5 on torsion-free complexes. Cones acyclic on 500/500. The RP² and cone cases are now asserts in `smith.py`.
- **The global χ test reproduces exactly.** Rebuilding the down-closure from the ten graph6 generators in `skeleton.pkl` and summing S independently gives 64,333 classes, 153,468,934,696 labelled graphs, S = −15,183,000, χ = 15,183,001 — all four figures matching §8.12. Contains ∅, excludes K₁₀, and n! is divisible by |Aut| on all 64,333 classes.
- **B(n) reproduces on all 1,460 rows** of `mu_table_safe.csv` from an independent reimplementation of the G.3 scoring, with all structural constraints holding and 1/√δ ≤ K on every row.
- **The n = 12 optimum.** 7,115 groups, max m\* = 18, exactly eight attaining it, all with orbital sizes {18, 48}, all one orbital partition, including the wreath witness.
- **The ten skeleton generators** are pairwise incomparable under monomorphism, and §8.8's identifications hold: C₁₀(1,2) = class 37, K₁+3K₃ = class 15, K₁+C₉ = class 20, the K₁+K₄+5K₁ apex = class 64. Class 27 is **K₅ □ K₂**.
- **The χ sign convention and dual encoding** in `stage4_fast.py`: `s = +1` on odd popcount is right for Σ(−1)^dim over nonempty faces, and `x[uc[full ^ m]] == 0` is exactly y[S] = 1 − x[comp S], so the duality involution's hypothesis that both directions are enforced per group is genuinely met.
- **Stage 3's inference rules** are all valid necessary conditions: T-transitivity; c ⊆ a ∧ c ⊄ b ⟹ a ⊄ b; a ⊄ d ∧ b ⊆ d ⟹ a ⊄ b; equal-edge-count distinct classes cannot embed; and domination of sorted degree sequence, triangles, P₃ and C₄ counts.
- **`mu_enumerate.py`'s pruning discipline.** `parts_for`/`rec` prune on the pre-Lemma-C optimistic capacity, so pruning never discards a viable configuration; and since orb(c, c−1, char2) = C(c,2) identically, SAFE mode's fallback term *equals* the pruning bound, which is the structural reason the two modes cannot disagree on a winner.

---

## D. Corrections applied to the scripts this pass

| file | change | changes results? |
|---|---|---|
| `consume_gap.py` | dedup key replaced by a canonical orbital partition (pynauty, with an exact networkx fallback) | **yes** — rebuilds the battery |
| `consume_gap.py` | stage-3 `--verify` sample re-decides random pairs by VF2 | no |
| `consume_gap.py` | dead `_row` worker removed | no |
| `stage4_fast.py` | leaf-check failure now raises instead of logging a warning | no (unless already broken) |
| `stage4_fast.py`, `probe_backbone.py` | `parse_q` enforces χ ≡ 1 mod lcm of all usable top primes | only with re-emitted tags |
| `probe_backbone.py` | CAP tail reported; automatic involution check against the catalog | no |
| `mu_enumerate.py` | `orb` capped at C(c,2) (the c = 2 foreign case) | no — screened out at every n ≥ 6 |
| `mu_enumerate.py` | sentinel `p = 0` for trivial-bottom-layer configurations | no on 85 regression values |
| `mu_enumerate.py` | `orbits_K` → `certified_K`, plus `parts` and `partcap` columns | **schema only** — migrate with `migrate_table.py`, no recomputation |
| `migrate_table.py` | new: lossless old→new schema conversion, with per-row consistency checks | no |
| `chi_test.py` | assert \|Aut\| integral and dividing n! | no |
| `smith.py` | RP² p-dependence and cone self-tests added | no |
| `oliver_mu.py` | `break` over twist candidates now fires only after a valid group is built | no — restores Run 1 values |
| `oliver_mu.py` | rotation restriction **left in place**, with the architectural cause documented (B7) | no |
| `ark_gap.g` | `IsOliverTop` returns all usable top primes, not the smallest | only on re-emission |
| `ark_intersect.py` | `top_prime` no longer asserts a unique q (it crashed at n = 12) | fixes a crash |

---

## E. Documentation corrections made, with the figures that were wrong

Recorded so the provenance is traceable, and because two of these were errors in *my own* first pass at the measurement.

- §8.11: n = 12 group count **8,819 → 7,115**; p-groups "6,094+" → 6,096. The 59-kept figure decodes as `--maxgroups 40`.
- §8.7′: dedup defect added. **My first measurement of the loss said 309 conditions and 108 unsound buckets; both were inflated about sevenfold** by a canonical form that ordered tied orbitals by GAP index, which over-splits equivalent partitions. Correct figures: **44 conditions dropped (10.4%), 41 unsound buckets, 26 of 116 Smith conditions (22.4%)**.
- Part I: "orbit counts K ∈ {2:261, 3:738, 4:254, 5:16} … K = 5 is exactly the predicted ceiling" — the column is the **certification level**, not an orbit count. Actual part counts {1:604, 2:695, 3:161}; nothing has five orbits; Prop. F.1 permits four at the floor.
- Part J item 1: "permitted orbit count up to 1/√δ ≈ 5" → four (1/√0.0418 = 4.89).
- §2.4 Lemma C: the "direct product must be cyclic" justification is a **pitfall Part D explicitly rejects**; replaced with the conjugation argument.
- §3: the Singer/ΓL(1) step was asserted as proved and retracted two paragraphs later. Restructured so the counterexample and the three inertness reasons come first.
- Validated range **1736 → 1764**; row count 1,269 → 1,460; the several stale ranges (1000, 1306, 1540) reconciled.
- §2 residual-gap paragraph: scoped to the menu-versus-ceiling comparison above the computed range, since B(1425) = 108,811 is attained.
- §8.9: forced IN **28 → 25**, forced OUT **18 → 20**, classes covered 400 → 409, and the **54 CAP verdicts** added. Classes 493/439/457 are absent from the record; the involution's empirical confirmation is withdrawn pending A3.
- §8.9′: "forced and free classes coexist at every edge count" across 5–40 is false (no forcings at 7 or 11–34); reworded. The "29 free classes at ≤ 10 edges" figure is exactly right.
- §8.8: class 27 identified as K₅ □ K₂.
- §8.1: the template's shortfall attributed to a specific architectural cause in `TemplateGroup` rather than to hand templates as such. **I first wrote that the fix had been applied; it has not.** The two symptoms in `candidate_groups` are downstream of the class placing the rotation in the cyclic middle layer, and fixing only the symptoms cost n = 22 a factor of two. Withdrawn and rewritten as a deferred item (B7).
- Appendix B: the lcm gain located in `IsOliverTop`'s `q < best` line.
- Reference list: arXiv:1303.5601 attributed to **Adamaszek**, not Kulkarni, in the one place it was wrong.
- §2: subsections reordered to 2.4, 2.5, 2.6.
- Part E: the (F or F/2)·c² cross bound now has a divisibility **proof** rather than an assertion of attainment.
