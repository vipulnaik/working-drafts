# Session log

*History of completed work on the ARK / μ(n) programme: what was verified, what was corrected, and what was found wrong. Kept separate from `pending-checks.md`, which lists only what is still outstanding. Figures quoted in the two main documents are authoritative; this file records how they got there.*

---

## Status note: full read-through of `enumeration-proof.md` (this session)

*Recorded before proceeding to Part J items 1 and 2, per request. The read-through is complete; the open problems have **not** been advanced yet — that work starts from here.*

**Nine defects found and fixed in the same pass** (all in `enumeration-proof.md`):

1. *Part B, dangling bullets.* The two bullets beginning "Consequently the intra-orbitals are the classes ±δ·T…" had lost their antecedent in the E′ restructuring — they followed text establishing that the ΓL(1) form *fails* in general, while asserting its consequences unconditionally. Now scoped: "*When the stabiliser IS of ΓL(1) type* — which Lemma B′ makes automatic for foreign parts, and which is the case the constructions of Part E realise…". An artifact of this session's own editing.
2. *Part G.3 truncation.* "The orbital data is" ended mid-sentence (a pre-existing defect). Completed with the value-formula reference.
3. *Part G.4 stale tail.* "What remains of Part E is now purely to write the enumeration of G.3 once" described a past state — the enumeration exists and Part E is proved. Rewritten.
4. *Part H, k-bounds off by one.* Under the ladder the forward pointer claimed k ≤ 2, 5, 6; the correct values are **k ≤ 2, 4, 5** (1/√0.049 = 4.52, 1/√0.028 = 5.98). Conservative direction, but wrong as stated.
5. *Part I filename.* `mu_table_safe.csv` → `mu_table_safe_v2.csv`.
6. *Part E, misleading parenthetical.* "127 winners use two classes of different sizes" read as contradicting Part I's equal-blocks finding, and "winning p ranges from 2 to 821" is stale. Corrected: 200 two-p-class winners, the two p-blocks **equal in 199 of 200**, winning p now 2 to 1129.
7. *Part I, mis-attributed exceptions.* "All but two have equal p-parts (the exception being … n = 1175)" named one exception where there are two. The other is **n = 551 = 256 + 167\* + 128** — the unique winner whose two p-parts are *distinct* powers of the same prime, newly identified this pass.
8. *Menu comparison unscoped.* The 173/127/46 figures against `mu_fast.py` are over n ≤ 1540; now said so.
9. *Part H cost projection.* Scoped as a historical measurement at n = 1540.

**Checked and clean on the same read** (recorded so it is not re-done): the E′ chain of inequalities (r(r−1) ≥ δn(n−1) from the foreign intra term; the sharp s = 1 threshold δ > (n−1)/9n); Theorem E.1's two branches, including that the p-odd branch's orb(2, t) = 1 relies on the C(c,2) cap in `orb` (a 2-block holds one pair — the text says why); Lemma E.2's coprime factorisation; the Part B under-statement table's strip/orb arithmetic (all seven rows); Proposition F.2's algebra ((2−√2)/√2 = √2−1); Cap(a) = r·max(2, L) as an upper bound (loose by ×2 at a = 2 only, safe direction); and the realisability paragraph's use of "coprime direct product is cyclic" — which is the *sufficient* direction and does not conflict with Part D's pitfall about the necessary direction.

**Progress on the open items (same session, after the read-through):**

*Item 2 (s = 2 branch) — Theorem E.3, now in Part E′.* (i) a ≥ 2 forces p = 3 and r = (3^a − 1)/2 a base-3 repunit prime (a = 3, 7, 13, 71, 103, …), and every Oliver group with orbits {3^a, r} has m\* ≤ c — proved by chain-reading case analysis. (ii) a = 1 makes c a safe prime, and the explicit group (𝔽_c ⋊ C_r) × AGL(1, r) — Oliver at (p, q) = (r, r), **verified by direct permutation-orbit computation at (11, 5) order 1,100 and (23, 11) order 27,830** — realises {C(c,2), C(r,2), cr}, dominating every fallback SAFE reading of the pair (orb(c, r) = C(c,2) identically). This explains why the certificate's five near-survivors, all safe-prime-shaped, were harmless. Extended same session: **Theorem E.4** — the s = 3 branch is the *single pair* (16, 5) (factorisation proof + scan to a = 200), SAFE ≤ 10 absolutely, dead at every feasible n (min B = 63). **E.3(iii)** — the a ≥ 2 repunit branch is SAFE-capped: Cap′(3) = 39, Cap′(7) = 14,209, Cap′(13) ≈ 5.8×10⁷, all O(r^{3/2}) via the 3^{a−1} − 1 factorisation; only (27, 13) is feasible in range and its cap sits below min B(n ≥ 40) = 140. **Corollary**: δ > 1/25 forces s ≤ 3, and every computed value clears 1/25, so the sole theorem-side residue in range is the global promotion of E.3(ii) (s = 2, a = 1, extra parts). TODO for the cleanup pass: teach `fallback_cert.py`'s theorem_covers() the E.4 and Cap′ checks so the coverage report reflects the new theorems. Also found and patched: G.0's twist-placement argument silently assumed nontrivial foreign twist; the q = ρ trivial-twist escape exists and is harmless (the trivialised block binds at ρ).

*Item 1 — reframed, not solved.* F.1 gives k ≤ 3 free wherever δ > 1/16, so the open content is the **δ ≤ 1/16 tail: 28 of 1,672 values** (all partcap 4; winners use 1/2/3 parts in 7/10/11 cases). Margin measurement over 18 sampled three-part winners (timed out at 18 of 24 — incomplete, rerun for the record): B₃/B₂ from 1.04 to **4.86** (n = 777), median ≈ 1.3 — refuting the perturbation/domination route and indicating k ≤ 3 in the tail is plausibly as hard as the low-density arithmetic. n = 551's unequal 2-powers rule out equal-parts assumptions. **Both items now converge on the same low-density (mostly odd-n) tail.**

*Item 2, continued (same session): the global-promotion residue.* Proved the structural trichotomy (α)–(γ) — within a fallback W's own partition the fallback reading is forced, so promotion must compare across partitions. Built `wide_cert.py`: the certificate run against **proven lower bounds** on B(n) (sound since any fallback attaining B_safe is a candidate against any B_lo ≤ B_safe), with B_lo = max(seed menu, three-part family) and two leftover extensions (single-part; multi-part exact-sum DP over necessary conditions). **Result: collapse certified at 8,719 of 8,719 composite non-prime-power n ≤ 10,000 — 100%, from lower bounds alone, no table needed.** The last eight survivors before the multi-part check were all Cunningham-chain pairs (719 → 1439 → 2879); their r − 1 = 2q structure pins the top prime and forces leftover foreigns ≡ 1 mod q, which kills them — the "q-pinning" mechanism, recorded in E″ as the likely ingredient of an unconditional argument. Soundness caveats for re-derivation: all over-approximations are permissive (never miss a real candidate); the three-part B_lo is a genuine admissible SAFE score; the nine menu-empty n are covered by the three-part bound. **Cleanup pass (done):** shared module `fb_common.py` now holds the arithmetic, the necessary conditions and the theorem checks; both certificates import it and reproduce their prior results exactly. Theorem dispatch is wired into the coverage report, which yields a new diagnostic — **1,700 of 2,097 s-branches over the table are dispatched by theorem (81.1%), and every one of the 397 that are not is the same case**, s = 2 with a = 1. E.4 and Cap′ dispatch their branches everywhere in range.

**Run extended to 10⁵:** 90,297 of 90,299 certified. Three fixes were needed and each is worth remembering. (a) B_lo must cover both parities — the three-part family needs n − 2c prime so it is essentially odd-only; even n needs the two-part and fused families. (b) Every family must be scanned **outward from its balance point** (c ≈ n/2, n/3), not downward from maximal c; scanning from the top gives a worthless cap(r\*) and drops the weakest density from 0.020 to 0.000007. (c) `intra_floor` incremented by one in a loop — O(√B) inside the inner loop, ~14,000 iterations per call at B ~ 10⁸. Replaced by an isqrt closed form, verified equal to the loop definition on all B < 3000 plus spot values.

**E.3(ii) upgraded to a resolution.** All seven values surviving at 10⁵ were the s = 2 safe-prime branch, and for the five with **no leftover** the (r, r) re-reading is fallback-free and scores at least as much — which *proves* collapse there rather than merely dominating. That closes the promotion for the bare pair. The two survivors (n = 50,817, n = 89,697) both have **leftover L = c**, where the re-reading is unavailable because two blocks of the same prime cannot both be foreign; they are not counterexamples (B_lo is a lower bound) but are the concrete open targets.

**Margin measurement completed** (was 18 of 23, timed out): min 1.040, **median 1.688**, mean 1.925, max 4.857, 7 of 23 at least 2. The partial run's "median ≈ 1.3" understated it.

**Refactor:** Corollary F.3 (δ > 1/(K+1)² ⟹ k ≤ K, hence δ > 1/16 ⟹ k ≤ 3) moved into Part F; the tail count and the margins moved into Part I; Part J items 1 and 2 reduced to open residue with back-references.

**Process note:** one `str.replace` silently failed to match while I printed a success message derived from a later `ast.parse`. Patches are now asserted on match and verified by re-reading the file. The same pattern could corrupt a document edit with no visible error.

## Status note: cleanup pass on `orbital-evasiveness-notes.md`

*Companion to the enumeration-proof pass above. The notes now summarise and point rather than duplicate; the companion document is authoritative for the enumeration.*

**Stale figures corrected.** §2.5's validated range 1764 → 2007. §2.6's certification-level distribution {2: 289, 3: 847, 4: 301, 5: 23} → {2: 321, 3: 954, 4: 369, 5: 28} and part counts {1: 604, 2: 695, 3: 161} → {1: 678, 2: 793, 3: 201} (these were the n ≤ 1764 figures sitting under a "1,672 computed values" header). Open Problem 9's "182 of 183 three-part winners" → the current 201, and its margin figure corrected to the completed measurement.

**Superseded claims removed.**
- §2.6 carried "One caveat survives — attainment there is empirical; that configuration never wins in the computed range." Attainment is now proved, so this is replaced by the Part E′ statement plus the certified ranges.
- §2's *Consequence for ★* listed the Singer-step gap as still open; it is closed.
- §2's *Status of ★* listed "extension to partial-capacity and nested configurations" as open; nested is closed by G.2 (tower depth absorbed into F) and partial capacity by E′.
- §3's *What therefore remains open* still named realisability as an open bookkeeping question; it is settled, and the residue is now two arithmetic questions.
- The Overview said "what remains is the enumeration's minimality and the realisability question of §3", and the one-paragraph summary made μ(n) "conjecturally equivalent modulo ★". Both updated: ★ has no unproven structural core left.

**Open Problem 9 compressed from five paragraphs to three.** It had grown into a near-duplicate of Parts E′–E″. It now states the two residues — (a) k ≤ 3 in the δ ≤ 1/16 tail, (b) the fallback exclusion as a theorem for the leftover case — with the apparatus left to the companion. The substantive addition is the observation that **both residues, and Open Problem 2, are the same low-density obstruction**; Open Problem 2 is now cross-linked as load-bearing for 9(b), since δ₀^odd > 1/9 would close it wholesale.

**Glossary gained the two concepts now central and previously undefined:** *fallback* (the one shape at which the two scorings differ) and *B_refined / B_safe / the sandwich*.

**Checked and clean:** §2.4's Lemmas A–C and their validation counts; §2.1–2.3 and Theorem 2.4/2.5 statements; §5.5's parity figures (the ~86% figure is consistent with the enumeration's 19.2% at δ ≥ 1/4 — different populations, no contradiction); §§4, 6–10; Appendix A; the assessment. Cross-document spot check: the shared figures (28 of 1,672; median 1.69; n = 50,817; the distributions) now agree in both files.

**Deliberately left as one-sided:** the notes do not repeat the 90,297-of-90,299 count; they say "all but two such n ≤ 100,000" and point to the companion. If that number moves, the companion is the only place to update.

**Defect found on review: B(n) was never defined in either document.** It is used from the Status header of the proof and the Overview of the notes onward, and the closest thing to a definition was Proposition F.1's "let B_K(n) be the maximum over configurations with at most K parts… so B_K = B", 240 lines after first use and only implicit. The glossary entry added earlier in this pass was worse than nothing: it said "B(n) denotes the common value where they meet", which does not cover the uses at §2's gap paragraph (B(1425) = 108,811) or §2.6 (a configuration "attaining B(n)"), both of which need B(n) defined whether or not the endpoints meet. Fixed in three places: a notation block in the proof's Status section, a notation paragraph at §2.6 of the notes where the enumeration is introduced, a forward reference at the Overview's first use, and a corrected glossary entry. **A second, deeper version of the same defect.** Theorem 2.3 states μ(n) ≤ [a max–min over partitions] but never names its right-hand side, and the very next paragraph began using B(1425). A reader would naturally take the two to be the same quantity, and they are not: the theorem's ceiling ranges over *partitions* with each part valued at cap(sᵢ), while B ranges over *configurations* carrying chain primes, fusion counts, prime-power part sizes, the Lemma B′/C coherence conditions and a within-class cross term. The theorem's side is strictly weaker. Fixed by naming it **B₀(n)**, stating the chain **μ(n) ≤ B(n) ≤ B₀(n)**, tabulating the four structural differences, and giving a worked contrast.

*The worked contrast is worth keeping.* B₀(1425) = 171,991 is attained by the partition 587 + 838, and **that partition supports no admissible configuration at all** — the 587-block needs twist order 293 to reach cap(587) = C(587,2), which as a foreign block forces q = 293 by Lemma B′, and then 838 = 2·419 is not Fc with F a power of 293 and c a prime power; reading 587 as p-characteristic forces p = 587, and 838 is neither a power of 587 nor prime. So B₀'s optimum is empty for B, which is the general reason B < B₀ rather than any per-part over-valuation. B(1425) = 108,811 at a consistent (p, q) = (479, 233), ratio 0.633. This example also corrects the framing of §2's gap paragraph: two thirds of the headline "0.058 ratio" at n = 1425 was B₀'s slack, not the menu's shortfall.

**The convention now stated explicitly is B(n) := B_safe(n)** — the enumeration's default output and the `mu_bound` column — with B_refined the lower endpoint; this matches all existing usage, checked against each occurrence.

## Status note: §2 of the notes reduced to statements, intuitions and Theorem 2.1

*Rationale, from the author: §2's value is now mainly foundational and pedagogical, so it should carry the main results and intuitions while the companion carries the arguments. Applied as follows.*

**Kept in the notes, with reasons.** The two ceilings (density 1/2, Zassenhaus). **Theorem 2.1 with its full proof** — framed explicitly for the first time as the *first exact value of μ at a non-prime power*, a feeder into nothing downstream, whose importance is that it showed exact composite-n values are obtainable at all by machinery keyed to the arithmetic of n; that is what started the programme, and its proof is the accessible introduction to orbit counting, the Oliver chain and the diagonal twist. The *statements* of Theorems 2.2–2.3 and Lemmas A/B/B′/C, since "the coherence conditions are derivable, not assumed" is a main intuition and the bridge from Part I to the number theory of Part II. Theorems 2.4–2.5 as the accessible constructions. §2.6's headline: B(n) is unconditional, attained, computed to 2007 and certified to 10⁵.

**Moved into the companion.**
- The **closed form V(s) = L(s) − 1** (L = largest prime-power divisor), which collapses Theorem 2.3's divisor recursion — new this pass, verified for all s < 4000 — now Part C.1.
- The **B₀ analysis**: definition, O(n) cost, the μ ≤ B ≤ B₀ chain, the four structural differences, and the n = 1425 worked contrast — now Part C.2. The notes keep a five-line pointer.
- The **validation of Lemmas B and C**: the 5,025-row construction check and, more importantly, the non-circular GAP check at n = 10 (1,061 full-capacity orbits all of prime-power size; all 88 prime-sized ones satisfying Lemma B). These existed *only* in the notes, so this was a move rather than a de-duplication — now in Part I.
- The proofs of Lemmas B and C, compressed in the notes to statement plus one-line mechanism, with the Lemma C pitfall left as a pointer.

**De-duplicated.** The notes' "Do not read the certification level as an orbit count" block was a verbatim duplicate of companion Part I; replaced by a short "Reading the output" paragraph that states what the output *is* and defers the two cautions.

**On B₀'s significance, since it determined the placement.** Measured rather than assumed: B₀ costs O(n) per value (B₀(200,000) in 0.26 s, against the enumeration's n^2.9), its proof needs only solvable-primitive ⟹ prime-power degree plus orbit–stabiliser, and its asymptotics carries no multiplicative side conditions on shifted primes. But its density floor below 3000 is **0.123** against B's 0.0418, and it sits near 1/4 generically. So it is a cheap, robust outer bracket that cannot identify arithmetically weak n and cannot prune the search — which is why the detailed comparison belongs in the companion and not the main flow.

## Status note: §§2–3 restructured, star notation retired, §5 brought up to date

**§2 now has subsections 2.1–2.6** (it previously jumped from an unnumbered opening to 2.4). Theorem 2.1 sits in its own §2.1 with the framing above; Theorems 2.2 and 2.3 are now §2.2 and §2.3 rather than blockquote continuations of 2.1. The "why exactness stops at p₁ = 3" discussion moved from §2.5 into §2.2, where it belongs. Fixed a stray Briticism ("used in anger").

**The menu-versus-B₀ figures moved to companion Part I**; §2.3 keeps only the conceptual half — that the gap between B₀ and B is the coherence condition, and that this is what converts a max–min over partitions into the Hardy–Littlewood systems of §5.

**★ notation retired** — 10 occurrences, all replaced by named references. It was undefined on first use, hard to search for, and its referent had drifted.

**§3 rewritten as a theorem plus a residue.** It previously stated a complicated claim and then annotated which parts were proved. Now: **Theorem 3.1** states the proved structure (orbit decomposition n = Σ Fᵢcᵢ, the p-characteristic/foreign typing, Lemma C coprimality, tower depth absorbed, forced orbital sizes, and the converse construction) with sources; two clauses that careless derivations lose are kept as warnings (wreath tops are necessary — AGL(1,5) ≀ C₂ at n = 10; no bounded blocks or fixed points); Corollary 3.2 follows and is noted to be an *equivalence* because 3.1 characterises rather than bounds; the false Singer step is isolated with its counterexample and the three reasons nothing rests on it; and the residue is two arithmetic questions. Historical framing dropped. Open Problem 1 is retired accordingly, retained only to record the two traps.

**§5 gained a new §5.6, measuring the ledger against μ instead of the menu.** §5.5's closing caveat asked whether odd n are genuinely poorer or merely poorly served, and deferred to the then-open extremality question; since μ(n) = B(n) is now known for n ≤ 2007 the question is answerable, and the answer is **both, in measurable proportions**:

- Odd n are genuinely poorer — median density 0.1104 against 0.2266 for even, a factor of two in μ itself.
- But the menu overstated it about threefold: below the 1/12 diagnostic the menu put 65.4% of odd composites, μ puts 19.3%. The reported "widening with n" is also much gentler at the level of μ (odd median 0.1434 → 0.1101 → 0.1037 across thirds, flattening rather than accelerating).
- δ₀^odd ≈ 0.049 is nearly tight as a floor: only 8 of 679 odd values (1.2%) fall below it, global minimum 0.0418 at n = 575. So Prop. 5.3's ceiling is close to the observed truth, not merely the best mechanism found.
- **Three thresholds line up by parity**: below 1/9 (Theorem E.1's threshold) sit 4.4% of even against 52.0% of odd; below 1/16 (Corollary F.3's) 0.1% against 4.0%. Both residues of Open Problem 9 are essentially even-free, so they and Open Problem 2 are one obstruction viewed three ways — and δ₀^odd > 1/9 would clear all three. Cross-linked from Prop. 5.3.

Also corrected in the old §5.5's caveat: "the proven ceiling remains ⌊C(n,2)/2⌋" was stale; beyond the computed range it is B₀.

**Then §5.5 was replaced outright, because its central structural claim is false.** It explained the odd-n shortfall by arguing that the strong two-block family needs its one even block to be the p-characteristic one (the other has prime degree, and 2 is the only even prime), so odd n reach it only via n = 2^a + r — about log₂n candidate splits against ~n/2 for even n, with the diagonal family as a thinning rescue. Sound about that family; **not how odd n are served.** Measured over the table: of the 548 odd values reaching density 1/12, **461 use no even part at all**, 339 are a single fused class (Theorem 2.4 with both factors odd), 122 use three parts, and the 2^a + r shape accounts for **53 — under 10%**. So the "two thinning routes" diagnosis measured the menu's coverage, not μ's behaviour, and the scarcity of 2-power splits is not what limits odd n.

Consequently §5.5 is now a short pointer, the corrected measurement sits in companion Part I beside the other Part-I measurements, and the former §5.6 has been merged in as the new §5.5. One orphan was rescued in the process: the observation that measuring against δ₀^even = 1/4 makes the parity signal vanish (menu: 85.8% even / 86.9% odd fall short) survives at the level of μ with 80.7% / 81.0%, and is retained because it is the reason 1/12 was chosen as the diagnostic in the first place. Appendix A's menu-based weak-tail paragraph now points to §5.5 for the μ-based comparison.

## C. Verified this pass — recorded so it is not re-done

- **`fp_acyclic` is correct.** Cross-checked against an independent dense-elimination implementation of reduced F_p homology on 4,000 randomised downward-closed complexes (t = 2…6, p ∈ {2,3,5,7,11}): **zero disagreements**. Genuine p-dependence confirmed on a triangulated RP² (False at p = 2, True at p = 3, 5, 7) — the property none of the original self-tests could detect, since all five used p = 5 on torsion-free complexes. Cones acyclic on 500/500. The RP² and cone cases are now asserts in `smith.py`.
- **The global χ test reproduces exactly.** Rebuilding the down-closure from the ten graph6 generators in `skeleton.pkl` and summing S independently gives 64,333 classes, 153,468,934,696 labelled graphs, S = −15,183,000, χ = 15,183,001 — all four figures matching §8.12. Contains ∅, excludes K₁₀, and n! is divisible by |Aut| on all 64,333 classes.
- **B(n) reproduces on all 1,672 rows** of `mu_table_safe.csv` from an independent reimplementation of the G.3 scoring, with all structural constraints holding and 1/√δ ≤ K on every row.
- **The n = 12 optimum.** 7,115 groups, max m\* = 18, exactly eight attaining it, all with orbital sizes {18, 48}, all one orbital partition, including the wreath witness.
- **The ten skeleton generators** are pairwise incomparable under monomorphism, and §8.8's identifications hold: C₁₀(1,2) = class 37, K₁+3K₃ = class 15, K₁+C₉ = class 20, the K₁+K₄+5K₁ apex = class 64. Class 27 is **K₅ □ K₂**.
- **The χ sign convention and dual encoding** in `stage4_fast.py`: `s = +1` on odd popcount is right for Σ(−1)^dim over nonempty faces, and `x[uc[full ^ m]] == 0` is exactly y[S] = 1 − x[comp S], so the duality involution's hypothesis that both directions are enforced per group is genuinely met.
- **Stage 3's inference rules** are all valid necessary conditions: T-transitivity; c ⊆ a ∧ c ⊄ b ⟹ a ⊄ b; a ⊄ d ∧ b ⊆ d ⟹ a ⊄ b; equal-edge-count distinct classes cannot embed; and domination of sorted degree sequence, triangles, P₃ and C₄ counts.
- **The extraspecial computation.** |E| = 27; the commutator of the two generators is the scalar 2·I, so E is extraspecial; E has no invariant line, so it is irreducible; |Z(E)| = 3; |⟨E, −I⟩| = 54; and the ±E-orbits on the 342 non-zero vectors of 𝔽₇³ have sizes {18 (×4), 54 (×5)}. Every claim Part B makes about this group is confirmed, and the minimum orbit of 18 is what answers the old ΓL(1) question negatively.
- **No cross-part-count ties.** At every value tested, B(n) is attained at exactly one part count, and no exactly-4-part or exactly-5-part configuration reaches it — so the max-3 observation is about optima, not about which witness the optimiser recorded.
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
| `mu_enumerate.py` | `orbits_K` → `certified_K`, plus `parts` and `partcap` columns | **schema only** — `migrate_table.py` converts in place, no recomputation |
| `chi_test.py` | assert \|Aut\| integral and dividing n! | no |
| `smith.py` | RP² p-dependence and cone self-tests added | no |
| `fallback_cert.py` | new: per-n certificate, plus the δ > 1/9 theorem coverage report | no |
| `mu_enumerate.py` | `--refined` help rewritten: heuristic, not a valid bound | no |
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
- Validated range **1736 → 1764**; row count 1,269 → 1,672; the several stale ranges (1000, 1306, 1540) reconciled.
- §2 residual-gap paragraph: scoped to the menu-versus-ceiling comparison above the computed range, since B(1425) = 108,811 is attained.
- §8.9: forced IN **28 → 25**, forced OUT **18 → 20**, classes covered 400 → 409, and the **54 CAP verdicts** added. Classes 493/439/457 are absent from the record; the involution's empirical confirmation is withdrawn pending A3.
- §8.9′: "forced and free classes coexist at every edge count" across 5–40 is false (no forcings at 7 or 11–34); reworded. The "29 free classes at ≤ 10 edges" figure is exactly right.
- §8.8: class 27 identified as K₅ □ K₂.
- §8.1: the template's shortfall attributed to a specific architectural cause in `TemplateGroup` rather than to hand templates as such. **I first wrote that the fix had been applied; it has not.** The two symptoms in `candidate_groups` are downstream of the class placing the rotation in the cyclic middle layer, and fixing only the symptoms cost n = 22 a factor of two. Withdrawn and rewritten as a deferred item (B7).
- Appendix B: the lcm gain located in `IsOliverTop`'s `q < best` line.
- Reference list: arXiv:1303.5601 attributed to **Adamaszek**, not Kulkarni, in the one place it was wrong.
- §2: subsections reordered to 2.4, 2.5, 2.6.
- Part E: the (F or F/2)·c² cross bound now has a divisibility **proof** rather than an assertion of attainment.

---

## New document: `arithmetic-of-density.md`

Created to hold the Hardy–Littlewood / Bateman–Horn side and the density implications, connected to the computed table. Its thesis, all of it verified against the 1,672 exact values before being written:

- **Two engines.** Multiplicative: a single fused class, n = F·c with both factors prime powers, density exactly **1/F** — matched to O(1/n) at all 678 one-part winners, and available only when ω(n) ≤ 2 (all 678 have ω(n) = 2; none of the 712 values with ω(n) ≥ 3 has a one-part winner). Additive: k balanced parts, density **1/k²** — Prop. F.1 read backwards, and tight, with zero two-part winners above 1/4 and zero three-part winners above 1/9.
- **Fusion is worth a factor of F** over splitting the same blocks, which is why (R1) matters and why single fused classes dominate the winners.
- **The recurring thresholds are one sequence**: 1/4, 1/9, 1/16 are the additive caps at k = 2, 3, 4, and coincide with δ₀^even, Theorem E.1's threshold and Corollary F.3's.
- **Density above 1/4 is purely multiplicative**: all 321 such values have ω(n) = 2 and a one-part winner; the maximum over ω(n) ≥ 3 is 0.2493.
- **The multiplicative engine covers a density-zero set**, thinning like log log n / log n — measured 52.3% of values on [10³, 2·10³) but 28.5% on [10⁶, 2·10⁶). So it props up 57% of the present table and vanishes asymptotically, and the observed floor should be expected to drift downward.
- **The parity gap is a shortage of caps, not of representations.** Odd n has F ≥ 3 where even n has F = 2, and its balanced additive route is three parts (1/9) not two (1/4); both Bateman–Horn systems supply ~n/log³n representations, so sieve input cannot substitute.

**Correction recorded.** Earlier in the session I called the old §5.5 mechanism claim (odd n need n = 2^a + r) *false* and replaced it. It is **correct but incompletely scoped** — binding for odd n with ω(n) ≥ 3 using two parts, which is the weak tail: of the 150 such values, 53 use two parts and 28 have exactly the predicted 2-power block, median density 0.0957 at the three-part cap. My refutation measured over all strong odd n, 444 of whose 548 have ω(n) = 2 and use the multiplicative engine. Both main documents now carry the scoped version.

**Process note.** The first attempt to add the cross-references failed silently: a script printed "ok" for an edit, then aborted on a later bad assertion *before* the file write, so none of the edits landed while the log read as success. Writes must be verified by re-reading the file, not by the absence of a traceback — this is the second instance of the same failure mode this session.

---

## The arithmetic supplement, and the odd-n revision

**New document `arithmetic-of-density.md`** and **new script `local_solubility.py`**.

**Thesis, verified against the table before being written.** Two engines: *multiplicative* — a single fused class, n = F·c with both factors prime powers, density exactly **1/F**, matched to O(1/n) at all 678 one-part winners and available only when ω(n) ≤ 2; *additive* — k balanced parts, density **1/k²**, tight, with zero two-part winners above 1/4 and zero three-part above 1/9. Fusion beats splitting by a factor of F. Density above 1/4 is purely multiplicative (all 321 such values have ω(n) = 2). The multiplicative engine covers a density-zero set, thinning like log log n / log n (52.3% of values on [10³, 2·10³) but 28.5% on [10⁶, 2·10⁶)), so it props up 57% of the present table and vanishes asymptotically.

**§5's odd-n family was the wrong one.** The three-block chain n = m + r + s with two foreign primes, whose ceiling 0.0486 gave δ₀^odd ≈ 0.049, has shape (1 p-block, 2 foreign) — which the enumeration selects **exactly once in 1,672 values** (n = 1175). The family that actually serves odd n is **n = 2c + r**, two equal p-blocks plus one foreign prime, 200 of 201 three-part winners. §5 missed it because it took the three blocks to be distinct primes each carrying its own twist; two equal blocks twist *diagonally* and need no coprimality between them (Lemma C's diagonal exemption).

**The new ceilings, by residue class**, from `local_solubility.py`. For odd ℓ the forbidden residues are r ≡ 0, 1, n, so only **ℓ = 3** can be fatal, exactly at n ≡ 2 (mod 3); at ℓ = 2 full efficiency needs r ≡ 3 (mod 4), which keeps c odd only when n ≡ 1 (mod 4).

| n mod 12 | efficiency | ceiling | observed max | ratio |
|---|---|---|---|---|
| 1, 9 | 1 | 1/9 = 0.11111 | 0.11037, 0.11019 | 0.993, 0.992 |
| 3, 7 | 1/2 | 1/(2+√2)² = 0.08579 | 0.08565, 0.08496 | 0.998, 0.990 |
| 5, 11 | 1/3 | 0.07180 | 0.07043, 0.07058 | 0.981, 0.983 |

So **δ₀^odd ≈ 0.0718 uniformly, 1/9 on n ≡ 1, 9 (mod 12)** — against the old 0.049. The ℓ = 3 obstruction has a **sparse escape** (if (r−1)/2 or c is a power of 3, full efficiency returns), which lifts n ≡ 5 (mod 12) to 0.10975 in range — but 22 of those 35 rows use the same prime r = 487 with (r−1)/2 = 243 = 3⁵, so it is a range artifact supplying O(log n) candidates, not a mechanism.

**Bateman–Horn window validity** (asked directly): the density δ(x) is continuous with an interior maximum, so requiring δ ≥ δ₀ strictly below the cap confines x to an interval of *positive* length (relative width 0.031–0.052 at 90% of cap). That is the standard Hardy–Littlewood regime, not a short-interval problem; no Montgomery–Vaughan-type input is needed. Two caveats: approaching the cap costs a factor Θ(√ε) in the count, and exact balance is arithmetically impossible anyway since r ≠ p is required.

**Corrections to my own earlier claims this session.** (i) I called the old §5.5 mechanism claim *false*; it is **correct but incompletely scoped** — binding for odd n with ω(n) ≥ 3 using two parts, which is the weak tail. (ii) I then said δ₀^odd = 1/9; that holds on only a third of odd residues, and the local-solubility algorithm was needed to find the ℓ = 3 obstruction I had missed.

**Process.** Two more scripts aborted before their write while printing "ok" for earlier edits in the same run. Writes are now verified by re-reading the file and asserting on content.

---

## The n = 12 battery rebuild (A1), first run

Run as `consume_gap.py --infile groups_out.txt --maxt 8 --procs 8`. Log and `ckpt_groups.pkl` / `ckpt_catalog.pkl` on file.

**What worked.** Stage 1 detected the changed selection signature and deleted all downstream checkpoints by itself — the predicted behaviour, no manual cleanup needed. Stage 2 completed in ~40 s: **2,293 raw → 230 distinct (partition, prime) conditions → 227 kept, 2,212 catalogue classes**.

**μ(12) = 18 survives the corrected dedup.** m\* = 18 is attained by **3 distinct conditions** — the 8 groups previously reported at {18, 48} collapsing to 3 genuinely distinct orbital partitions. The Oliver m\* distribution over the kept 200 is {1: 56, 2: 29, 3: 45, 4: 17, 5: 7, 6: 34, 7: 2, 10: 1, 11: 2, 12: 4, 18: 3}.

**Two problems found, both recorded in `pending-checks.md` A1.**

*The battery was silently truncated.* `--maxgroups` defaults to 200; stage 1 found 203 distinct Oliver conditions; `sel = ol[:maxgroups] + pg` dropped 3. Sorted by `(-mstar, t)`, so the casualties are lowest-m\* — harmless for reading off μ(12), but the battery feeds the Smith/χ computation where each condition is a constraint, so a positive verdict from a truncated battery would not be quotable. My commands block had omitted `--maxgroups`, which is what let the default bite.

*Stage 3 is a multi-week run.* Classes 600 → 2,212 and VF2-needed pairs 74,213 → **1,018,719 (13.7×)**. From the old logs: 2,176 VF2 calls, 30,002 s, 16,061 pairs resolved → **7.4 pairs/call at 13.8 s/call**, with yield decaying 13.5 → 3.6 → 5.4 as easy pairs are consumed. Extrapolation: 22 days at the early rate, 33–41 days at the late rate. The old battery never finished either — four sessions took it 22% of the way.

**Consequence: A5 was promoted to gate A1.** Stage 3 exists only to build the containment-order matrix; if the §8.4 EGF route computes χ without it, the whole cost is avoidable. That decision should precede any relaunch.

**Correction to the ledger's dedup figure.** It recorded "44 of 425 conditions dropped (10.4%)". This run shows 59 kept before against 227 now — but the old run used `maxgroups = 40` and this one 200, so **59 → 227 is confounded with the flag change and is not a measure of the dedup fix**. The clean figure from this log is that **2,063 of 2,293 groups impose an already-present condition, leaving 230 distinct**. Re-deriving the old battery's dedup rate at matched flags would settle it, and has not been done.
