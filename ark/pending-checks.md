# Pending runs and unverified details in the scripts

*Companion to `orbital-evasiveness-notes.md` and `enumeration-proof.md`. Written July 2026 after a review pass over `mu_enumerate.py`, `consume_gap.py`, `stage4_fast.py`, `probe_backbone.py`, `chi_test.py`, `ark_intersect.py`, `smith.py`, `oliver_mu.py` and `ark_gap.g`. Everything here is either a run that has not happened or an assumption a script makes that nothing has checked. Items are ordered by value per unit of effort within each section, not by severity.*

**How to read the status labels.** *Verified* means an independent computation agreed. *Sound* means an argument was read and found correct, with no independent computation. *Unverified* means neither. *Corrected* means a defect was found and fixed in the accompanying files, and the correction has not itself been exercised on a full run.

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

Also corrected in §5.5's caveat: "the proven ceiling remains ⌊C(n,2)/2⌋" was stale; beyond the computed range it is B₀.

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

**A6. Rerun `fallback_cert.py` whenever the table extends.** It is a per-n check, not a theorem: `python3 fallback_cert.py mu_table_safe_v2.csv` belongs in the routine after every batch of new values. It currently certifies all 1,672 with 0 inconclusive cases, and reports how many are settled by the δ > 1/9 theorem alone (1,275, i.e. 76.3%) versus by the exhaustive search (397, every one of them because δ ≤ 1/9 rather than because a Mersenne cap binds). Two things would retire it: a proof that δ is bounded below (the ladder does this conditionally, which forces s = 1 and lets the Cap(a) argument finish), or a general domination argument for the fallback.

**A7. Verify the dedup-collision audit at n = 10.** The measurement in §8.7′ was made at n = 12 because `groups_out.txt` for n = 12 was to hand. The same audit at n = 10 would say how much the *published* n = 10 SAT was affected, which matters for how the skeleton and the χ kill should be described. Requires the n = 10 `groups_out.txt`.

---

## B. Assumptions the scripts make that nothing has checked

**B1. `Catalog.classify` is a mutating lookup used as a pure query.** In `stage4_fast.py`, `probe_backbone.py` and `chi_test.py` the idiom `x[cat.classify(set())] = 1` assumes the empty graph is already in the catalog. If it were not, `classify` would **append**, silently extending `cat.reps` and desynchronising `V` from the order matrix. The same hazard applies to the complement lookups in the new involution check, which is why that block asserts the catalog did not grow. Status: **unverified, latent.** A `classify_or_fail` variant used everywhere the catalog is meant to be read-only would close it permanently.

**B2. `mono` is only ever called on representatives with the same vertex count.** The complement trick in `ark_intersect.mono` rests on the identity σ(E_H) ⊆ E_G ⟺ σ⁻¹(E_Ḡ) ⊆ E_H̄, which requires σ to be a **bijection** — true when H and G both carry all n vertices, false for a genuine injection. Every catalog representative does carry all n vertices, so the call sites are fine. Status: **sound, but undefended.** An assertion on the vertex counts inside `mono` would make it safe against reuse.

**B3. Purely-foreign configurations are reachable.** `best_with_k` skipped a prime p when no power of p landed in the pruning window, which is justified only for configurations containing a p-characteristic part. Configurations with a trivial bottom layer (all parts foreign) are legitimate Oliver groups, and reaching them relied on some *other* p surviving the skip and happening to make every part foreign — true in practice, unproven in general. Status: **corrected** — an explicit sentinel `p = 0` meaning "trivial bottom layer" is now enumerated and never skipped. The correction did not change B(n) on any of the 85 regression values.

**B4. The refined intra-orbital formula — RESOLVED in range; only the asymptotic statement is open.** Formerly the only place where the code computed something the proof did not license. Three changes.

*The posed question is answered NO.* Is the minimum ±H-orbit on 𝔽_c∖{0} at most 2d? For E = 3^{1+2} on 𝔽₇³ the ±E-orbits have sizes {18, 54} while d = |Z(E)| = 3, so the minimum is 18 against 2d = 6.

*So orb(c,d) is not a valid per-part upper bound — but B_refined is a valid lower bound.* With c = 343 and foreign primes {3, 19} stripping 342 = 2·3²·19 down to d = 2, the formula returns 343 where E achieves 3087, a factor of 9. This does **not** exhibit an n with μ(n) > B_refined(n), and none is known: the under-statement needs the small prime factors of c−1 stripped, hence small foreign blocks, and a foreign block of size r caps the density at 2r/n. The two affected configurations 343+3+19 and 343+2+3+19 have densities 0.00086 and 0.00009 — at n = 365 the winner is `5x73` with B = 13,140 while 343+3+19 has m\* ≤ 57, losing by 231×, and the exotic group is capped by that same cross class. Since B_refined = Ω(n log n) and any affected configuration has m\* = O(n), the mechanism cannot bite for large n. The correct frame is **B_refined(n) ≤ μ(n) ≤ B_safe(n)** unconditionally, with `--refined` computing the lower endpoint and their difference measuring the interval width.

*Attainment is certified by making the endpoints meet.* Part E already gives B_refined ≤ μ(n) by explicit construction; its conclusion is conditional on the fallback not biting, and that is what the certificate discharges. `fallback_cert.py` checks eight necessary conditions and finds no candidate at **all 1,672 values, 0 inconclusive**. So μ(n) = B(n) is proved per n, and B_refined = B_safe follows as a corollary rather than as a separate measurement.

*And beyond the range there is now partial coverage by theorem.* δ > 1/9 forces s = (c−1)/r = 1, which forces either r = 2 (score ≤ 1) or the Mersenne case with an absolute cap Cap(a) = O(n^{3/2}). Hence: collapse **unconditional** on n = 2·(prime power); **conditional** for even n via δ₀^even = 1/4; the s = 1 branch **unconditionally dead above exponent 3/2**, the same wall as §4; and **open for odd n**, whose ladder constants 0.049 and 0.028 fall below the 1/9 threshold. Status: **closed in range, partially closed beyond it, open for odd n at low density.** The certificate must be rerun as the table extends (A6). Note that pushing δ cannot give "almost all n" — δ ≥ 1/4 holds at only 19.2% of computed values.

**B5. Exhaustiveness of the four GAP stages.** Only the Oliver-condition test and the emission logic of `ark_gap.g` have been read. `IsOliverTop` is **sound** — taking Γ₂ = `PCore(N,p)` is WLOG since any normal p-subgroup with cyclic quotient lies in O_p(N) and the quotient is then a quotient of a cyclic group; and normality in Γ is automatic because O_p(N) is characteristic in N with N ◁ Γ. What has *not* been checked is whether stages A–D together are exhaustive over the intended families (transitive groups, direct products over partitions, imprimitive wreaths, p-subgroups up to Sylow-conjugacy). The n = 10 and n = 12 exhaustive comparisons are evidence that they are, at those degrees.

**B7. `TemplateGroup` places the block rotation in the cyclic middle layer, and that is the real template bug.** §2.4's implementation note describes the defect as a spurious gcd(d, k) = 1 filter plus a prime-only k, and both symptoms are visible in `candidate_groups`. They are not the cause. `TemplateGroup`'s own chain model puts the rotation in Γ₁/Γ₂ — its docstring requires d, the foreign primes and s pairwise coprime — and separately enforces k = s with s prime. Theorem 2.4 places the rotation in the top q-group, whence any d | c−1 is admissible and k need only be a prime power. Consequence: the template misses μ(10) = 20 (k = 2, d = 10) and μ(12) = 18 (k = 4).

**Do not repair this in the enumerator alone.** I tried; relaxing the filter builds groups that `TemplateGroup` marks invalid, and an unconditional `break` over the twist candidates then discards the smaller d that had been working — **n = 22 fell from 110 to 55**. The change was reverted and the defect documented in place. The `break` bug is genuine and independent and has been fixed (break only after a valid group is actually produced); with it fixed and the filter restored, the template reproduces Run 1 exactly at n = 6, 10, 12, 15, 18, 21, 22, 26 (6, 10, 10, 30, 36, 28, 110, 78). The real repair is to move the rotation into the top layer inside `TemplateGroup`, updating its Oliver validity check and `desc_parts`, which also changes what `top_prime` parses. Status: **open, deliberately deferred** — the GAP path has no such restriction and supersedes this enumerator, so the value is in correctness of the record rather than in better μ bounds.

**B6. The lcm strengthening is implemented but unexercised.** `IsOliverTop` now returns every usable top prime as a `+`-separated tag and the solvers enforce χ ≡ 1 mod lcm. Single-prime tags parse identically, so old files behave exactly as before — which also means **the new path has never run**. It needs one GAP re-emission and a check that some group actually receives a multi-prime tag before the strengthening can be claimed.

---

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
