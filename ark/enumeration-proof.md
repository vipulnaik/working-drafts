# Bounding μ(n) by enumeration of Oliver configurations

*Companion to `orbital-evasiveness-notes.md` §2. Establishes an upper bound on μ(n) by classifying the possible orbit-and-twist structures of an Oliver group and enumerating them. Implemented in `mu_enumerate.py`.*

**Status.** Parts A–D and F–H are proved, and Part E proves completeness together with realisability. What Part E does not prove is *minimality*, which costs running time only. The framework now gives a two-sided statement:

> **B_refined(n) ≤ μ(n) ≤ B_safe(n)**, unconditionally — the lower bound from Part E's explicit construction, the upper bound because F·C(c,2) caps any point stabiliser whatever — with the two endpoints coinciding exactly when the optimum does not invoke the unconditional fallback.

**Notation, since three related quantities appear throughout.** A *configuration* is what the enumeration ranges over: a choice of chain primes (p, q) and orbit sizes n = Σ Fᵢcᵢ with twists, admissible in the sense of Parts B–D. Each configuration has a *score* — the minimum over its intra-orbital, within-class-cross and between-orbit terms (Part E) — and the two scorings differ on exactly one kind of part, a p-characteristic part whose twist Lemma C strictly reduces:

> **B_safe(n)** = max over admissible configurations of the score with such a part valued at F·C(c,2), the unconditional capacity. This is what `mu_enumerate.py` computes by default and what the `mu_bound` column of the table holds.
> **B_refined(n)** = the same max with such a part valued at F·orb(c, d) instead, which is what the Part E construction actually realises.
> **B(n)** := **B_safe(n)**, written without a subscript wherever the distinction is not at issue — which is everywhere the two are known to agree, and so everywhere in the computed range.

Since C(c,2) ≥ orb(c, d) always, B_refined ≤ B_safe; the point of E′ is that they are equal wherever it certifies, so B(n) is unambiguous there and equals μ(n).

That collapse is proved at every computed value (`fallback_cert.py`: 1,921 of 1,921, 0 inconclusive), and — since the certificate is sound against any proven *lower* bound on B(n) — at **every composite non-prime-power n ≤ 10,000**, and at all but two such n ≤ **100,000**, without needing the table at all (`wide_cert.py`: 90,297 of 90,299, Part E″). By theorem rather than search it holds **unconditionally** on the infinite family n = 2·(prime power) and wherever δ > 1/9, **conditionally** for even n; the one branch still lacking a theorem is s = 2 with c a safe prime, at odd n of low density. Numerical validation of B(n) itself reaches **n = 2298**, 1,921 composite values. Open items are collected at the end.

**On the word "proved", and on what the numerical checks are for.** The statuses above mean *an argument has been written down that appears complete*, not *the argument has been verified by anyone else*. The distinction is not academic here: the ΓL(1) step of Part B was asserted as a plausible sketch and is false, which was established only by deliberately looking for a counterexample. Lemma B′'s socle argument, Lemma C's conjugation argument and the tower absorption of G.2 are of comparable intricacy and have had no independent scrutiny.

The numerical work therefore serves three distinct purposes, which are easy to conflate:

1. **Implementation fidelity.** Internal consistency, the Proposition F.1 stopping rule, and monotonicity of the certified maxima test whether `mu_enumerate.py` computes what Parts A–H specify. This validates code against a specification and is not evidence for any theorem.
2. **Tightness.** μ(n) ≤ B_safe(n) is a consequence of the classification. The *equality* needs the two endpoints of the sandwich to meet, which is now a proved statement per n (Part E′) rather than a case-by-case observation — so this purpose has largely been discharged, and what the numbers add here is coverage of the range rather than evidence for the equality.
3. **A hedge against errors in the arguments themselves.** If Lemma B′, Lemma C or the block recursion were wrong in a direction that made the bound too small, violations would be expected. None appears at any computed value, nor in either exhaustive battery, where the bound is not merely respected but attained. This is real evidence — for the correctness of the reasoning, rather than for filling a gap in reasoning already known to be sound.

**Which uncertainties are uniform in n, and which are range-limited.** These are easy to confuse, and the distinction determines what further computation buys.

*Uniform in n — the dominant risk.* Every simplification the search relies on (Proposition F.1's orbit bound, block counts restricted to q-powers, Lemma B′, Lemma C, the absorption of tower depth into F) is a consequence of an argument that either holds for every n or for none. There is no mechanism by which such a constraint could hold below some threshold and fail above it. So the residual doubt is not whether the trimmings continue but whether the arguments are correct — and if one is not, the computed values are wrong at small n as much as at large.

*Range-limited, and affecting tightness rather than validity.* μ(n) ≤ B_safe(n) follows from the classification. The equality needs the two endpoints of the sandwich to meet, and that is no longer a case-by-case check: it is a proved statement per n (Part E′), settled by Theorem E.1 at 76.3% of computed values and by the exhaustive certificate at the rest. So the items genuinely limited by range are now narrower than they were, and worth listing exactly.

- **The certificate's coverage.** It is a per-n proof, not a theorem about all n. Each new batch of values needs it rerun, and nothing in it bounds the exceptional set as n → ∞. This is the main range-limited item.
- **Part E's construction spot-checks.** Realisability is argued in general, but the orbit computations confirming that the built group's orbital sizes equal the enumeration's terms cover eight configurations from n = 12 to n = 315. A shape not represented there would still be covered by the argument, but its arithmetic would want a separate check (Part J item 3). All five winning shapes are now represented in the computed range — the fifth, two foreign primes, appears exactly once, at n = 1175 — so the "a fifth shape at larger n" caveat earlier versions carried has been discharged rather than deferred.
- **The empirical narrowings behind minimality.** That no winner uses more than three parts (Part I) is a statement about the range examined, as are the sub-narrowings it implies. Unlike the two items above, this one has no per-n certificate: it is pure observation, verified in Part I to be about optima rather than about tie-breaking, but not proved anywhere.

*What this implies for effort.* Extending the numerical range tests the implementation and extends the certificate's coverage — the latter being a genuine per-n mathematical statement rather than only a code check — but it does not test the classification, whose consequences do not vary with n. Extending the *exhaustive* comparison to further n tests the classification itself, and is therefore worth more per unit of compute — but exhaustive enumeration of Oliver groups is only feasible at small degrees, so the supply of such tests is short. Independent reading of Lemma B′, Lemma C and G.2 would be worth more than either.

Read that way, the exhaustive checks at n = 10 and n = 12 are the most valuable of the three, because they are independent of both the code and the families: the groups were enumerated by GAP with no reference to any of this, and the optimum they exhibit matches the predicted construction exactly, orbital sizes included.

---

## Part A. Reduction to orbits and crosses

Let Γ have vertex orbits O₁, …, O_k with |O_i| = s_i. A pair inside O_i has its whole Γ-orbital inside O_i, and a pair between O_i and O_j has its orbital inside O_i × O_j. Hence

> m\*(Γ) ≤ min( min_i M_i , min_{i<j} s_i·s_j ),

where M_i is the minimum intra-orbital of the transitive group Γ|_{O_i}. Both terms are needed: the first is the intra-orbit content, the second bounds every cross class by the total number of pairs available to it. Parts of size 1 are permitted but contribute a cross bound of s_j, so any configuration containing a fixed point has m\* ≤ max_j s_j ≤ n−1 and is dominated except at tiny n.

## Part B. Per-orbit classification

By Lemma A, Γ|_{O} inherits the chain with the same (p, q). Since Oliver's condition forces solvability, Γ|_O is solvable and transitive, so exactly one of:

**(B1) Primitive.** A solvable primitive group is affine: O carries the structure of 𝔽_{p₀}^a and Γ|_O = 𝔽_{p₀}^a ⋊ H with H ≤ GL(a, p₀) irreducible.

- *H is cyclic-by-q.* H inherits the chain, so it is p-by-cyclic-by-q; its normal p-subgroup is unipotent, and a normal unipotent subgroup of an irreducible linear group has a nonzero invariant fixed space, contradicting irreducibility unless trivial.
- *The point stabiliser need not lie in ΓL(1, p₀^a).* The tempting argument runs: let C ◁ H be cyclic with H/C a q-group; if C acts *irreducibly* then 𝔽_{p₀}[C] is a division algebra by Schur and a field by Wedderburn, so O is one-dimensional over it, C lies in a Singer cycle, and H ≤ N_{GL}(C) = ΓL(1, p₀^a). That is valid **only when C acts irreducibly**. C need not be, and when it is not the conclusion fails:

> **Counterexample.** Let E = 3^{1+2} be the extraspecial group of order 27 acting on 𝔽₇³, generated by diag(1, 2, 4) and the cyclic shift. Verified by direct computation: |E| = 27; the commutator of the generators is the scalar 4·I, so E is extraspecial; E has **no invariant 1-dimensional subspace**, so it is irreducible; and its only cyclic normal subgroup is the centre C₃, of index 9 with quotient C₃ × C₃ — not cyclic. So E is **cyclic-by-q with q = 3** yet **not metacyclic**, hence not contained in ΓL(1, 343) = C₃₄₂ ⋊ C₃, which is cyclic-by-C₃ and therefore metacyclic.

The general obstruction is Clifford's theorem: V restricted to C is semisimple with isotypic components permuted transitively by the q-group H/C, and when there is more than one component — or one component of multiplicity m > 1 — H sits in ΓL(m, p₀^b) with bm = a rather than in ΓL(1, p₀^a). Extraspecial groups realise exactly this.

Three consequences.

1. **Foreign parts are unaffected.** Lemma B′ forces a = 1 there, so H ≤ GL(1, r) = 𝔽_r^\*, which is cyclic outright — ΓL(1, r) is automatic and the formula orb(r, t) is exact. Neither Lemma B′ nor Lemma C depends on it.
2. **The coarse capacity bound is unaffected.** cap(c) ≤ C(c,2) for a p-characteristic part holds for *any* H whatsoever, being just "at most all pairs inside the block". Theorem 2.3, Part C's recursion and Part F's bounds rest only on this.
3. **The refined formula can under-state a single group's minimum orbital, so it is not a valid per-part UPPER bound — but B_refined is a valid LOWER bound on μ(n).** Writing the minimum intra-orbital as c·(smallest ±H-orbit on non-zero vectors)/2, the code takes the twist to be cyclic of order d = strip(c−1, foreigns) and computes orb(c, d). For non-ΓL(1) H the orbits can be larger than the ±δT classes — up to |±H| = 2|C|·qᵉ rather than 2|C| — so orb(c, d) can be an **under**-estimate by as much as a factor 2qᵉ.

   *The phenomenon, concretely.* For the counterexample group itself, E = 3^{1+2} on 𝔽₇³, direct computation gives the ±E-orbit sizes on the 342 non-zero vectors as **{18 (×4), 54 (×5)}**, so a 343-block carrying E has minimum intra-orbital 343·18/2 = **3087**, while |Z(E)| = 3 means its cyclic-layer image has order only d = 3. Against that, with 342 = 2·3²·19:

   | foreign primes present | d | refined orb(343, d) | E achieves | under-statement |
   |---|---|---|---|---|
   | none | 342 | 58,653 = C(343,2) | 3087 | — |
   | 19 | 18 | 3087 | 3087 | — |
   | 2, 19 | 9 | 3087 | 3087 | — |
   | 3 | 38 | 6517 | 3087 | — |
   | 2, 3 | 19 | 6517 | 3087 | — |
   | **3, 19** | **2** | **343** | **3087** | **×9** |
   | **2, 3, 19** | **1** | **343** | **3087** | **×9** |

   Note that Part B's natural test case — 343 with a foreign prime 19 — is the third row, where the formula returns exactly E's value; the under-statement needs the sharper stripping.

   *This also answers the question the open items used to pose.* "For a primitive affine orbit 𝔽_c ⋊ H with H cyclic-by-q and cyclic-layer image of order d, is the minimum ±H-orbit on 𝔽_c∖{0} at most 2d?" — **no**: for E it is 18 against 2d = 6. An affirmative answer would have made orb(c, d) a valid per-part upper bound and hence made attainment follow directly; that route is closed, and E′ replaces it.

   *What this does and does not license saying.* It shows orb(c, d) is not an upper bound on the minimum intra-orbital of an arbitrary admissible group on that block. It does **not** exhibit an n with μ(n) > B_refined(n), and no such n is known. The reason is that the under-statement is confined to configurations of negligible density: driving d well below c−1 requires the *small* prime factors of c−1 stripped, hence *small foreign blocks*, and a foreign block of size r caps m\* at r(n−r), hence the density at 2r/n. Both under-statement rows need 3 as a foreign prime, and the configurations 343+3+19 and 343+2+3+19 have smallest cross classes 57 and 6 — densities 0.00086 and 0.00009. At n = 365, for instance, the winner is `5x73` with B = 13,140, and 343+3+19 (the same n) has m\* ≤ 57, losing by a factor of 231; the exotic group is capped by that same cross class and so does not beat B_refined(365) either. Since B_refined(n) = Ω(n log n) unconditionally and any configuration exhibiting the under-statement has m\* = O(n), the mechanism cannot produce μ(n) > B_refined(n) for large n.

   *The right frame is a sandwich.* Part E constructs, for every admitted configuration W, an explicit Oliver group with orbital data exactly the enumeration's terms at twist d — so m\*(Γ_W) = REFINED-score(W), whence B_refined is a **construction lower bound**. And F·C(c,2) caps any point stabiliser whatsoever, so B_safe is an upper bound. Hence, unconditionally,

   > **B_refined(n) ≤ μ(n) ≤ B_safe(n)**,

   and the two collapse exactly when the SAFE optimum is fallback-free, since orb(c, c−1) = C(c,2) identically and the foreign and cross terms are mode-independent. `--refined` is therefore best read as computing the lower endpoint, not as a rival upper bound.

**Why the endpoints meet, and why the Singer failure cannot reach B(n).** When Lemma C does not bite, d = c−1 and **orb(c, c−1) = C(c,2)** exactly — in characteristic 2 because −1 = 1, in odd characteristic because c−1 is even. So on any configuration the fallback does not touch, the refined and unconditional scores are *identical*, and the collapse B_refined(n) = B_safe(n) is equivalent to the statement that the optimum is fallback-free. That statement is not left to measurement: Part E′ gives two structural bounds and a per-n certificate, both proved and both checked over the whole computed range. The refined formula is therefore only ever strictly below C(c,2) on configurations that lose anyway.

*When the stabiliser IS of ΓL(1) type* — which Lemma B′ makes automatic for foreign parts, and which is the case the constructions of Part E realise — the per-part formulas are exact:

- The intra-orbitals are the classes ±δ·T for T the twist group, and the minimum intra-orbital is **orb(s, t) = s·t/2 if t is even or p₀ = 2, else s·t**, where t = |T|.
- *Foreign characteristic (p₀ ≠ p).* Lemma B′: π_O(Γ₂) is a normal p-subgroup of a primitive group, hence trivial; π_O(Γ₁) is cyclic normal, so contains the socle, forcing a = 1; being cyclic it centralises the socle, so equals it; hence the entire twist lies in Γ/Γ₁, a q-group. **So s is prime and t is a power of q.**
- *Own characteristic (p₀ = p).* t may be any divisor of s−1, realised by a subgroup of the Singer cycle inside the cyclic layer.

**(B2) Imprimitive.** There is a block system; taking a coarsest one, the induced action on blocks is primitive solvable, hence affine of prime-power degree — and it must be a **q**-group action for the chain, so the number of blocks is a power of q. The block stabiliser acts transitively on a block, again inheriting the chain, and the intra-block orbital valencies are its suborbit sizes. Recurse.

## Part C. The valency recursion

Define, for chain primes (p, q),

> V(s; p, q) = s − 1 if s is a power of p;
> V(s; p, q) = t or 2t (t the q-part of s−1, the former iff t is even) if s is a prime ≠ p;
> V(s; p, q) = max over q-power divisors b > 1 of s of V(s/b; p, q) otherwise;

and cap(s; p,q) = s·V(s; p,q)/2. Induction on s using Part B gives M_i ≤ cap(s_i; p, q) for every orbit.

> **Pitfall.** Restricting b to q-powers is essential. A recursion over arbitrary block counts implicitly maximises the twist prime independently at each level, whereas the group has a single q; the resulting quantity bounds nothing. 

**C.1 The recursion has a closed form.** The chain-free version of V — the one in Theorem 2.3 of the notes, where b ranges over all prime-power divisors rather than q-powers — collapses:

> **V(s) = L(s) − 1**, where **L(s)** is the largest prime-power divisor of s; hence **cap(s) = s(L(s) − 1)/2**.
>
> *Proof.* Each step replaces s by s/b for a prime-power divisor b > 1 and stops when the argument is a prime power, returning that argument minus 1. So the reachable return values are exactly c − 1 for prime powers c dividing s such that s/c is a product of prime powers — which every integer is. Hence the maximum is L(s) − 1. ∎

Verified against the recursion for every s < 4000, with no exceptions. This is worth recording because it makes the crude ceiling elementary: no memoised recursion is needed, and its arithmetic content is visibly just the divisor structure of the parts.

**C.2 The crude ceiling B₀, and why it is not the quantity of interest.** Write

> **B₀(n) = max over partitions n = Σ sᵢ into parts ≥ 2 of min( minᵢ cap(sᵢ), min_{i<j} sᵢsⱼ )**,

the right-hand side of the notes' Theorem 2.3. Since more parts only shrink minᵢ cap(sᵢ), the maximum is over one- and two-part splits, so B₀ costs **O(n) per value** after a sieve — B₀(200,000) takes a quarter of a second, against the enumeration's measured n^2.9. And **μ(n) ≤ B(n) ≤ B₀(n)**: every configuration determines a partition whose parts are valued at least as highly by cap.

The second inequality is typically strict, and the reason is structural rather than a per-part over-valuation: **B₀'s optimising partition frequently supports no admissible configuration at all.** B₀ ranges over partitions with parts of any size; a configuration additionally fixes chain primes (p, q), requires each part to be Fᵢcᵢ with Fᵢ a q-power and cᵢ a prime power, types each part as p-characteristic or foreign, constrains twists by Lemma B′ and Lemma C, and carries a within-class cross term that B₀ has no notion of.

> *Worked contrast at n = 1425.* B₀(1425) = 171,991 from the partition 587 + 838, where 587 is prime so cap(587) = C(587,2) = 171,991, cap(838) = 175,142 and the cross term is 491,906. No Oliver group realises it. Reaching cap(587) needs twist order 293 or 586; as a foreign block Lemma B′ forces that twist to be a power of the top prime, so q = 293, and then 838 = 2·419 is not Fc with F a power of 293 and c a prime power. Reading 587 as p-characteristic forces p = 587, and 838 is neither a power of 587 nor prime. The enumeration returns **B(1425) = 108,811** from `1x479 + 1x479 + 1x467*` at a consistent (p, q) = (479, 233) — attained, so μ(1425) = 108,811, a factor 0.633 below B₀.

**What B₀ is therefore good for, and what it is not.** Three genuine uses. It is the **robust fallback**: its proof needs only "solvable primitive ⟹ prime-power degree" plus orbit–stabiliser, so it survives intact if Lemma B′ or Lemma C — neither independently scrutinised — turns out to be wrong. It is **computable arbitrarily far**, which the enumeration is not. And its asymptotics is **cleaner**: with no coherence conditions there are no multiplicative side conditions on shifted primes, so B₀ is governed by additive representation by numbers of large prime-power core, not by the Hardy–Littlewood systems that govern B.

Against that, B₀ is **loose exactly where it would matter**. Its density floor below 3000 is 0.123 (at n = 551), against B's 0.0418, and it sits near 1/4 generically — B₀(200,000) has density 0.2494. So it does not identify arithmetically weak n, and it cannot be used to prune the enumeration. It is a cheap outer bracket, not a tool.

## Part D. Coherence across parts

**Lemma C (corrected justification).** Let O_i be a p-characteristic part with twist order d_i, and O_j a foreign prime part of size r_j whose translations lie in Γ₁ (Part B). The images of Γ₁/Γ₂ in the two parts are C_{d_i} and C_{r_j}. The top q-group acts on the cyclic group Γ₁/Γ₂ by conjugation; on part j it induces the twist, of order t_j > 1, and on part i it induces the identity (it acts trivially there). If r_j | d_i, the r_j-primary component of Γ₁/Γ₂ surjects onto both images, so the conjugation action cannot be simultaneously trivial on one and of order t_j on the other. Hence **gcd(d_i, r_j) = 1**.

> **Pitfall.** The weaker argument — "independent pieces generate a direct product, which must be cyclic" — does **not** establish this. A single generator can act as a twist on one part and a translation on another, in which case cyclicity alone imposes nothing. The conjugation action is what forces coprimality.

Twists on distinct p-characteristic parts carry **no** mutual constraint: a single cyclic generator surjects onto each, which is exactly what the diagonal constructions exploit.

## Part E. Completeness of the enumeration, and realisability

Completeness is proved below and realisability with it; what is *not* proved is minimality, which costs running time only (Part J item 1).

**The general configuration.** Parts B–D leave the following shape. Fix chain primes (p, q). The orbits are: some p-characteristic parts, each a p-power, grouped into fusion classes permuted by transitive q-groups (so each class has q-power size); and some foreign parts, each a prime with a q-power twist, subject to Lemma C against every p-part twist. Writing one fusion class of F blocks of size m together with foreign primes r₁, …, r_v:

> value = min( F·orb(m, d), (F or F/2)·m², min_j orb(r_j, t_j), min_j F·m·r_j, min_{j<j'} r_j·r_{j'} )

with d the largest divisor of m−1 coprime to every r_j, t_j the q-part of r_j−1, and the second term present only when F > 1 (its coefficient F for odd q, F/2 for q = 2, from the pattern-orbit count of the transitive q-group on the blocks).

**Admissibility constraints.** Two are easy to omit, and omitting either inflates the bound — the dangerous direction.

- **Foreign primes are pairwise distinct.** Two foreign parts of the same prime r would place C_r × C_r inside the cyclic layer, which is not cyclic.
- **Foreign parts are never fused.** Independent translations across F blocks generate C_r^F, cyclic only for F = 1. Diagonal translations *are* admissible, but are always dominated: they preserve the difference y − x, so the pairs with y = x form a cross class of size r·|block-pair orbit| ≈ F·r/2 which the twist can never merge, since it fixes 0. That class binds, leaving a fused foreign class worth ≈ F·r/2 rather than F·orb(r, t).

> **Pitfall.** Estimating the fused-foreign case *without* the diagonal cross class suggests it beats the bound at dozens of n; including that class shows it never does.

**Two reductions.**

> **(R1) Equal-size merge.** Two p-characteristic classes of the same block size c with fusion counts F₁, F₂ whose sum is a q-power are dominated by the single class of F₁+F₂ blocks: the intra-orbital rises from max(F₁,F₂)·orb(c,d) to (F₁+F₂)·orb(c,d) while every cross term is unchanged or larger. Accordingly no winning configuration in the computed range uses two fused classes.
>
> **(R2) Twist maximality.** Each term is non-decreasing in its own twist order, so the optimum is attained with every twist maximal subject to Lemma C, which removes the twist axis from the search.

> **Pitfall.** Without (R2) the order of optimisation matters — max–min and min–max differ — and an implementation that mixes them computes neither bound.

What does **not** reduce is multisets of distinct part sizes and the choice of bottom prime: both are genuinely distinct configurations, and the measured data shows both matter — 200 winners use two p-characteristic classes alongside a foreign prime of a different size (the two p-blocks themselves are *equal* in 199 of the 200; the exception is n = 551 = 256 + 167\* + 128, two distinct 2-powers), and the winning p ranges from 2 to 1129.

**Status of the enumeration.** Every configuration permitted by Parts A–D is enumerated, within the bounds proved in F and G, so the enumeration is **complete and finite**. It is not known to be **minimal**: no argument prunes it to a shortest sufficient list. That affects running time, not validity. Several structural questions that might have obstructed completeness do not: the number of foreign parts needs no separate cap, since foreign parts are orbits and Proposition F.1 bounds the orbit count; multiple p-characteristic classes of different sizes are enumerated as multisets of parts; and towers do not couple to foreign parts (Part G).

**Realisability: every admitted configuration is realised.** The enumeration does not over-generate. Every configuration the enumeration admits is realised by an explicit group, assembled from ingredients whose Oliver condition is verified purely arithmetically. Given (p, q) and parts (Fᵢ, cᵢ, type, twist dᵢ):

- each p-characteristic part contributes the translations of its Fᵢ blocks of 𝔽_{cᵢ}, all of which lie in the bottom p-group Γ₂;
- each foreign part contributes translations C_{r} lying in the cyclic layer;
- one generator of the cyclic layer carries the twists of all p-characteristic parts *diagonally*, its image in each part being that part's full twist C_{dᵢ}, so distinct p-parts need no coprimality between their twist orders;
- each foreign twist, a q-power, and each fusion class's block permutation both lie in the top q-group.

Γ₂ is a p-group by construction; Γ₁/Γ₂ is cyclic exactly when the independent orders in it are pairwise coprime, which is Lemma C and is what the enumeration enforces; Γ/Γ₁ is a q-group as a product of q-groups on disjoint supports. And the resulting orbital sizes are *forced*, not chosen: the intra-orbital of a class is Fᵢ·orb(cᵢ, dᵢ) because the block permutation fuses the Fᵢ copies; the within-class cross is (Fᵢ or Fᵢ/2)·cᵢ² because the minimum pair-orbital of a transitive q-group on Fᵢ points is exactly Fᵢ/2 for q = 2 and Fᵢ for odd q — **and that is an upper bound, not merely an attained value, by divisibility**: every orbital of a q-group has q-power size, and the q-part of C(F,2) = F(F−1)/2 is F for odd q and F/2 for q = 2 (F−1 is coprime to q), so if every orbital exceeded that value they would all be divisible by qF and so would their sum, contradicting the q-part of the sum; attainment then follows from the regular C_F action. This replaces an appeal to "the pattern-orbit count", which asserted attainment where the bound is what the argument needs; and the between-orbit classes are single orbitals of size sᵢsⱼ because the translations of distinct orbits act independently.

Verified by orbit computation that the built group's orbital sizes equal the enumeration's terms exactly:

| configuration | predicted m\* | built m\* | orbitals |
|---|---|---|---|
| n = 12, 3×4, q = 3 | 18 | 18 | {18, 48} |
| n = 18, 2×9, q = 2 | 72 | 72 | {72, 81} |
| n = 20, 4×5, q = 2 | 40 | 40 | {40, 50, 100} |
| n = 26, 9 + 17\*, q = 2 | 36 | 36 | {36, 136, 153} |
| n = 35, 16 + 19\*, q = 2 | 19 | 19 | {19, 120, 304} |
| n = 45, 2×11 + 23\*, q = 2 | 23 | 23 | {23, 110, 121, 506} |
| n = 255, 73+73+109\*, q = 3 | 2628 | 2628 | {2628, 2943, 5329, 7957} |
| n = 315, 2×61 + 193\*, q = 2 | 3660 | 3660 | {3660, 3721, 6176, 23546} |

So **B(n) is attained, and μ(n) = B(n)**, in every case where the enumeration's score for each part is the one the construction realises. The single exception is a p-characteristic part whose twist Lemma C strictly reduces, where unconditional scoring assigns F·C(c,2) rather than the F·orb(c, d) the construction reaches; that exception is discharged in E′ below, which proves it cannot arise at any optimum in the computed range.

> **Pitfall.** When checking this by construction, the twist must be a multiplicative generator of the *field* 𝔽_c. Using ℤ/c instead is correct only for prime c, and silently gives wrong orbital sizes for proper prime powers — for n = 12 with three blocks of 4 it yields 6 rather than 18.

**E′. Discharging the exception: the fallback never bites the optimum.** The construction above realises REFINED-score(W) for every admitted W, so **B_refined(n) ≤ μ(n)** unconditionally, and with the classification's F·C(c,2) cap on any point stabiliser,

> **B_refined(n) ≤ μ(n) ≤ B_safe(n)**.

Since orb(c, c−1) = C(c,2) identically (Part B), the two endpoints coincide exactly when the optimum does not invoke the fallback. So attainment reduces to excluding fallback configurations from the optimum, and that is provable rather than merely observable.

*The structural bound.* Let W contain a p-characteristic part (F, c) and a foreign prime r of W with r | c−1; put s = (c−1)/r and δ = B(n)/C(n,2). The foreign part's own intra term satisfies orb(r,t) ≤ C(r,2), so r(r−1) ≥ δ·n(n−1); and c ≤ n − r, so s ≤ (n−r−1)/r. Hence

> **s ≤ (1 − √δ)/√δ** — s ≤ 3 at δ ≥ 1/16, s ≤ 2 at δ ≥ 1/9, and **s = 1 as soon as δ > 1/9** (sharp form: s ≤ 1 needs only r > (n−1)/3, which r² > δn(n−1) delivers once δ > (n−1)/9n).

> **Theorem E.1 (collapse above density 1/9).** If δ(n) > 1/9 then any fallback configuration attaining B(n) has s = 1, so c − 1 = r is prime, and exactly one of:
>
> - **p odd.** Then c is odd and c − 1 even, so r = 2. A foreign block of size 2 contains a single pair, so orb(2, t) = 1 and SAFE(W) ≤ 1 — excluded at every n with B(n) > 1.
> - **p = 2.** Then c = 2^a and r = 2^a − 1 is a **Mersenne prime**, and d = strip(r, {r}) = 1, so the twist dies outright. Since r − 1 = 2(2^{a−1} − 1) and t is a q-power dividing it, SAFE(W) ≤ orb(r, t) ≤ **Cap(a) := (2^a − 1)·max(2, L(a))** with L(a) the largest prime-power divisor of 2^{a−1} − 1 — an absolute constant, independent of F and of n.
>
> So the collapse holds unless B(n) ≤ Cap(a) for some Mersenne exponent a with 2^{a+1} − 1 ≤ n: an O(log n) check.

> **Lemma E.2 (Cap is small).** For a an odd prime write a − 1 = 2m. Then 2^{2m} − 1 = (2^m − 1)(2^m + 1) with the factors coprime, so every prime power dividing 2^{a−1} − 1 divides one of them. Hence **L(a) ≤ 2^{(a−1)/2} + 1** and **Cap(a) = O(n^{3/2})**. Attained at a = 17, where L = 257 = 2⁸ + 1.

*Coverage.* Four cases, in decreasing strength.

- **n = 2·(prime power): unconditional.** Theorem 2.1 gives δ = (m−1)/(2m−1) → 1/2 > 1/9. An infinite family on which the sandwich provably collapses, with no conjecture at all.
- **Even n: conditional.** δ₀^even = 1/4 > 1/9, so granting the even-n Hardy–Littlewood statement the collapse holds at every even n admitting the representation, hence at all sufficiently large even n.
- **Above exponent 3/2: the s = 1 branch dies unconditionally.** Cap(a) = O(n^{3/2}) means it needs δ = O(n^{−1/2}), i.e. **μ(n) = O(n^{3/2})** — exactly the §4 provability barrier, so this residue is the same wall as the rest of Part II rather than an independent one. Shparlinski's Ω(n^{5/4−ε}) gives only δ = Ω(n^{−3/4−ε}) and does not suffice.
- **Odd n at low density: open** (Part J item 2).

> **Theorem E.3 (structure of the s = 2 branch).** Let (c, r) be an s = 2 fallback pair: c = p^a = 2r + 1 a prime power, r prime.
>
> **(i) a ≥ 2 forces p = 3 and r = (3^a − 1)/2 with a prime.** For p^a − 1 = 2r with r prime, factor p^a − 1 = (p−1)(1 + p + ⋯ + p^{a−1}); with a ≥ 2 both factors exceed 1, and the divisors of 2r are 1, 2, r, 2r, so p − 1 = 2. Hence r is a **base-3 repunit prime** — the exponents are a = 3, 7, 13, 71, 103, … (only c = 27, 2187, 1594323 below 4×10⁶): scarcity of the same order as the Mersenne branch of Theorem E.1. Moreover **every Oliver group with orbit sizes {3^a, r} has m\* ≤ c = 2r + 1**: with bottom 3, Lemma C confines the c-twist's cyclic-layer part to divisors of 2, and the top can add only the q-part of 2r — q = r rescues the c-block to full capacity but trivialises the foreign r-block's twist (r ∤ r − 1), giving m\* ≤ orb(r, 1) = r, while any other q leaves the c-block at orb(c, 2) = c; bottom r is impossible (𝔽₃^a is not cyclic, and c-translations in the top fail normality of Γ₁); and both-foreign fails since 3^a is not prime. So the pair is worth at most c — *linear* — to any actual group.
>
> **(ii) a = 1: a non-fallback re-reading dominates, and RESOLVES the bare-pair case.** Here c = 2r + 1 is a **safe prime**. The explicit group Γ = (𝔽_c ⋊ C_r) × AGL(1, r) is Oliver with (p, q) = (r, r) — chain 𝔽_r ◁ 𝔽_r ⋊ (C_{r−1} × 𝔽_c) ◁ Γ, the layer cyclic since gcd(r−1, c) = 1 — and its orbitals are exactly {C(c,2), C(r,2), cr}: the c-block's ±C_r classes merge because |±C_r| = 2r = c − 1, equivalently **orb(c, r) = c·r = C(c,2) identically**. Verified by direct permutation-orbit computation at (c, r) = (11, 5) and (23, 11), group orders 1100 and 27,830, orbitals matching. Since every fallback reading of the same pair scores min(C(c,2), orb(r, t), cr) with orb(r, t) ≤ C(r,2), the non-fallback reading — which is the enumeration's own (p, q) = (r, r) configuration, r-block p-characteristic at full twist, c-block foreign at twist r — scores at least as much. **This is why the five longest-surviving candidates in the certificate's development, all of shape "c safe prime, r = (c−1)/2", were harmless: they are exactly the re-readable pairs.**
>
> When the configuration is the **bare pair** — F = 1 with no leftover, so n = c + r — this is not merely a domination but a **proof of collapse at that n**. The re-reading is itself fallback-free: its only foreign prime is c, its p-part is r, and c = 2r + 1 > r − 1 cannot divide r − 1. So its SAFE and REFINED scores coincide, and if the fallback reading attained B_safe(n) then so does the re-reading, giving B_refined(n) ≥ B_safe(n) and hence equality. Both certificates apply this as a resolution.
>
> It does **not** extend past the bare pair, and the obstruction is sharp rather than technical. With a leftover the re-reading must re-type the leftover parts too, and the commonest case **L = c fails outright**: two blocks of the same prime c would be two *equal* foreign parts, which the admissibility constraints above forbid (they would place C_c × C_c in the cyclic layer), and fusing them is forbidden for the same reason. So the promotion is complete for L = 0 and open for L > 0.
>
> **(iii) The repunit branch is SAFE-capped too.** For a ≥ 2 the foreign block's own SAFE score is absolutely bounded: r − 1 = 3·(3^{a−1} − 1)/2 and 3^{a−1} − 1 = (3^{(a−1)/2} − 1)(3^{(a−1)/2} + 1) with gcd 2, so every odd prime-power divisor of r − 1 is at most 3^{(a−1)/2} + 1, whence orb(r, t) ≤ **Cap′(a) = O(r^{3/2})** for every top prime q. Concretely Cap′(3) = 39 (q = 3), Cap′(7) = 14,209 (q = 13), Cap′(13) = 58,192,753 (q = 73), each comfortably below r^{3/2}. So the a ≥ 2 branch is excluded as a SAFE candidate wherever B(n) > Cap′(a) — an O(log n) check per n, exactly parallel to Theorem E.1's Mersenne case, and it dies unconditionally above the same μ = ω(n^{3/2}) wall. In range: the only feasible pair is (27, 13) (n ≥ 40), whose cap 39 is below the minimum B(n) = 140 there; (2187, 1093) first fits at n = 3280, beyond the current table, where the certificate will test its cap 14,209 mechanically.

> **s = 4 is now reachable, and has no theorem.** The corollary below bounds s by 1/√δ − 1, so a lower density admits a larger s. At n = 2291, δ = 0.037524 gives s ≤ 4, and the certificate reports one branch it can only dispatch by search. Unlike s = 3, the branch is **not** thin: c − 1 = 4r with c a prime power and r prime carries no parity or congruence forcing — 33 such pairs exist with c < 4000, beginning (9,2), (13,3), (29,7), (53,13), (125,31) — so no analogue of E.4 is available and an absolute cap would have to come from the foreign block's twist, as in E.1 and E.3(iii). The search still clears it (0 candidates at every computed n), so nothing is unproved; but the theorem-side coverage now has a hole that widens as the density floor falls. This is the first branch to appear since the framework was set up, and it appeared because the computed minimum dropped from 0.041107 to 0.037524.

> **Theorem E.4 (the s = 3 branch is a single pair, and dead).** Let (c, r) be an s = 3 fallback pair: c − 1 = 3r. If r = 2 the foreign block holds one pair and SAFE ≤ 1. If r is odd then c = 3r + 1 is even, so c = 2^a with r = (2^a − 1)/3 and a = 2b even; then 2^{2b} − 1 = (2^b − 1)(2^b + 1) with exactly one factor divisible by 3, and after dividing that factor by 3 both factors exceed 1 — except at b = 2, where 2^b − 1 = 3 collapses to 1. Hence r is prime **only for (c, r) = (16, 5)** (verified by scan to a = 200). For that pair, t = qpart(4, q) gives orb(5, t) = 10 at q = 2 and 5 otherwise, so **SAFE ≤ 10 absolutely**. The pair fits only at n ≥ 21, where every computed B(n) is at least 63; beyond the table B(n) ≥ μ-constructions → ∞, so the branch never attains B(n) anywhere. **s = 3 is closed.**

> **Corollary (the fallback question below 1/9, reduced).** Since s ≤ 1/√δ − 1, **δ > 1/25 forces s ≤ 3** — and every computed value has δ ≥ 0.0418 > 1/25. So at every computed n the fallback question reduces by theorem to: s = 1 (Mersenne, Cap(a)); s = 2 with a ≥ 2 (repunit, Cap′(a)); s = 2 with a = 1 (safe prime; bare pair resolved by E.3(ii)); s = 3 (dead by E.4). The **only branch without an absolute cap is s = 2, a = 1**, and there E.3(ii) resolves the bare pair outright, leaving only configurations that carry a leftover. That remainder — sharply obstructed at L = c, where the re-reading would need two equal foreign parts — is the entire theorem-side residue of Part J item 2 within the computed density regime.

*The certificate.* `fallback_cert.py` enumerates the tuples (p, q, F, c, r) satisfying eight necessary conditions for a fallback configuration to score B(n) — c a p-power; r prime with r | c−1 and r ≠ p; F a q-power with Fc + r ≤ n; each of the p-part intra, foreign intra, cross and within-class-cross terms at least B; and the leftover L = n − Fc − r either 0 or large enough to be a legal part carrying an intra-orbital of size B. Further parts only lower the minimum, so the conditions are necessary and an empty list is a proof at that n. Cost O(n log n) per value. It also reports which values Theorem E.1 settles outright.

> Over the current table: **no candidate at any of the 1,921 values, 0 inconclusive**, with **1,390 (75.0%) settled by Theorem E.1 alone** and the other 458 by the search — every one of those 397 uncovered because δ ≤ 1/9, never because a Cap(a) binds. So μ(n) = B(n) is proved at each computed n, independently of tie-breaking, and B_refined = B_safe follows rather than being separately measured.

> **Pitfall.** Getting the necessary conditions right took two corrections, both in the permissive direction. Without the leftover-*size* condition, 58 of the then-1,582 values admit candidates; without the leftover-*decomposition* condition, 5 do. Those five are all one shape — c a safe prime with r = (c−1)/2: 359/179 at n = 725, 731 and 719/359 at n = 1457, 1595, 1643 — excluded because the leftover is either not of the form (q-power)·(prime power) (187 = 11·17, 517 = 11·47, 565 = 5·113) or is a prime with trivial q-part twist (193, 379). Reproduce those five before trusting an empty result. The check is also not exhaustive if a leftover could itself be two or more parts; that never arises in range and is reported when it does.

**E″. The global promotion, and the certificate at scale.** Promoting E.3(ii)'s pairwise domination to a global statement runs into a wall that is worth recording precisely, because it shows the residue is arithmetic rather than structural. For a fallback W with s = 2, a = 1 attaining B: **(α)** the r points admit no re-typing — a size-r part is foreign-r or p-characteristic with r = p^j, impossible since p = c; and splitting them fails since every part needs C(s,2) ≥ B while C(r,2) ≥ B already pins r ≈ √(2B); **(β)** the Fc points, kept whole, read uniquely as (F, c), since q^j·c factors no other way into (q-power)·(prime power); **(γ)** F > 1 pins the bottom prime to c — fused translations must lie in Γ₂ — recreating the conflict, while the q = r escape trivialises the r-twist and scores only r < B. So within W's own partition the fallback reading is forced, and any promotion must compare across partitions of n, where the arithmetic enters.

What *is* available is the certificate run at scale, and the key observation making that possible: **the certificate is sound against any proven lower bound on B(n)**. A fallback W attaining B_safe(n) has every SAFE term ≥ B_safe(n) ≥ B_lo(n), so it appears among the candidates computed against B_lo; an empty list against B_lo proves the collapse without knowing B(n). Since B_lo needs only *some* admissible configuration's SAFE score, it costs O(n/log n) per value instead of the table's n^2.9. `wide_cert.py` implements this. Three ingredients are each necessary, and each was found by watching the certificate fail without it.

*B_lo must cover both parities.* The three-part shape (1,c)+(1,c)+(1,r\*) needs n − 2c prime and so exists essentially only for odd n; even n is carried by the two-part shape (1,c)+(1,r\*) and by a single fused class (F, c) with n = F·c, the latter including Theorem 2.1 at F = 2. Using the three-part family alone leaves 4,987 of 8,719 values with no bound at all.

*Each family must be scanned outward from its balance point.* All of them trade a growing term against a shrinking one — C(c,2) against cap(r\*) — so the optimum is interior: near c ≈ n/2 for the two-part shape and c ≈ n/3 for the three-part. Scanning downward from maximal c instead gives r\* tiny and cap(r\*) worthless, which collapses the weakest density from 0.020 to 0.000007 and makes the permitted s explode. With outward scanning, keeping the 60 nearest prime powers suffices, and a few thousand values need a top-up from the family menu or a full scan.

*The leftover machinery needs both checks:* the single-part test of conditions (7)–(8), and a **multi-part decomposition check** — an exact-sum reachability computation over the admissible part sizes (foreign primes r_j ≠ r with orb(r_j, qpart(r_j−1, q)) ≥ B, distinct; p-characteristic sizes F′p^j with F′·C(p^j,2) ≥ B, repeats allowed), sound because it enforces necessary conditions only.

> **Result: the collapse B_refined(n) = B_safe(n) = B(n) is certified at every composite non-prime-power n ≤ 10,000 (8,719 of 8,719), and at 90,297 of the 90,299 such n ≤ 100,000 — from proven lower bounds alone.** That is fifty times the range of the computed table, for about three minutes of arithmetic; the lower-bound pass dominates the cost at roughly 150 s per 10⁵ and is cached, so the next decade is an afternoon rather than a research problem.

> **The two values that remain unresolved at 10⁵ are exactly the sharp case of E.3(ii).** They are n = 50,817 with (c, r) = (20327, 10163) and n = 89,697 with (35879, 17939) — both s = 2 with c a safe prime and **leftover L = c**, so the configuration is two equal c-blocks plus the foreign r. That is precisely where the (r, r) re-reading is unavailable, because two blocks of the same prime cannot both be foreign. They are **not counterexamples**: B_lo is only a lower bound, and the true B(n) at those two values may exceed the candidate's score, which would settle them. But they are the first two values in the framework whose collapse is settled neither by theorem nor by certificate, and they pin the open case to a concrete shape.

The survivors at 10⁴ before the multi-part check were themselves informative: every one involved the pairs (1439, 719) or (2879, 1439) — the **Cunningham chain 719 → 1439 → 2879**, each prime twice the previous plus one, the arithmetically worst case for this branch. Their structure is what kills them: r − 1 = 2q with q prime (718 = 2·359, 1438 = 2·719, 2878 = 2·1439), so the *only* top prime with orb(r, t) ≥ B is that q, which forces every extra foreign part in the leftover to satisfy **r_j ≡ 1 (mod q)** — a modulus of 359–1439 against a leftover window of ~1,100–4,600, leaving no admissible decomposition. This q-pinning mechanism is the general reason deep-chain candidates strangle themselves, and is worth extracting as a lemma in any eventual unconditional treatment.

*A free diagnostic.* **B_safe − B_refined is exactly the width of the interval containing μ(n)**, computable by running both modes. It is zero wherever the certificate passes, and if the certificate ever fails nothing becomes wrong — both endpoints stay valid and the sandwich merely opens.

## Part F. The search is bounded

The enumeration needs no number-theoretic input to be finite, and the bound is small.

> **Proposition F.1 (part count).** If a configuration on n points achieves density δ = m\*/C(n,2), then it has at most **1/√δ** orbits.
>
> *Proof.* Each orbit's capacity is at most C(s_i, 2) < s_i²/2 (Part C), and m\* ≤ min_i cap(s_i) by Part A, so s_i > √(2m\*) = √(δ·n(n−1)) for every i. Summing over the k orbits, n = Σ s_i > k√(δ·n(n−1)), whence k < 1/√δ (up to the n/(n−1) factor). ∎

Two consequences.

*The search is small in practice.* The weakest density anywhere below 10⁴ is 0.0147 (at n = 4917), giving k ≤ 8; at the median density 0.2 the bound is k ≤ 2. So **no admissible configuration below 10⁴ has more than eight orbits**, and most have two.

*The search is self-certifying.* Let B_K(n) be the maximum over configurations with at most K parts, and δ_K its density. B_K is non-decreasing in K, so δ_K is too, and 1/√δ_K is non-increasing. Compute B_2, B_3, … and stop at the first K with 1/√δ_K ≤ K: by Proposition F.1 no configuration with more than K parts can achieve δ_K, so B_K = B. For every n below 10⁴ this terminates by K = 8. **No conjecture is consulted at any point.**

> **Proposition F.2 (fused parts cost more).** Let f be the number of parts with F_i > 1. Then **k + (√2 − 1)·f ≤ 1/√δ**.
>
> *Proof.* An unfused part has s_i = c_i and needs F_i·C(c_i,2) ≥ m\*, i.e. s_i(s_i − 1) ≥ 2m\*, so s_i ≳ √(2m\*). A part with F_i ≥ q ≥ 2 has c_i = s_i/F_i, and the same requirement gives s_i² ≥ F_i(2m\* + s_i) ≥ 4m\*, so s_i ≥ 2√m\*. Summing over the k parts, n ≥ √m\*(√2(k − f) + 2f), and √m\* ≈ n√(δ/2) gives the claim. ∎
>
> **F.1 is tight and cannot be improved to k ≤ 3 by counting.** Running the same argument through the *smallest* part reproduces k ≤ 1/√δ exactly, so the equal-parts case saturates it, and no tightening of constants does better: at the observed density floor δ = 0.0418, F.2 gives k ≤ 4.48 against F.1's k ≤ 4.89 — still 4, not 3. Since no winning configuration anywhere in the computed range uses more than three parts (Part I), the residual factor is arithmetic, not metric: any proof of k ≤ 3 must use the prime-power structure and the Diophantine constraint n = Σ F_i c_i. This is Part J item 1.

> **Corollary F.3 (density thresholds for each part count).** δ > 1/(K+1)² ⟹ k ≤ K. In particular **δ > 1/16 ⟹ k ≤ 3** and δ > 1/9 ⟹ k ≤ 2. So the minimality target of Part J item 1 is *free* at all but the lowest densities, and what remains open there is only the δ ≤ 1/16 regime.
>
> *Do not conflate this with the s-bound of Part E′.* That one reads s ≤ 1/√δ − 1 and governs (c−1)/r, not the part count; the two happen to share the threshold 1/25 (δ > 1/25 gives k ≤ 4 by F.3 and s ≤ 3 by E′), which is a coincidence of arithmetic, not a shared mechanism.

This is the structural answer to the question of whether the enumeration needs Hardy–Littlewood-type input to cut down cases. It does not. The division of labour is:

| question | apparatus | conditional? |
|---|---|---|
| what shapes can an Oliver group have? | Parts A–D, group theory | no |
| what is the maximum at a given n? | bounded search, ≤ 1/√δ parts | no |
| how does that maximum behave as n → ∞? | Hardy–Littlewood, Chowla (§4–5 of the notes) | yes |

Number theory answers *which n admit a good configuration*, never *which configurations are admissible*. The temptation the four failures all yielded to was replacing the general shape by a menu of special cases because the general search looked expensive; Proposition F.1 removes the excuse, and writing the general enumeration once — over all configurations with at most 1/√δ parts — is what remains of Part E.

## Part G. Nested towers add no new shapes

The one structural loose end left by Parts A–F was whether a deep imprimitive tower, interacting with foreign parts elsewhere in the partition, could escape the classification. It cannot, and the reason collapses the shape space rather than enlarging it.

**G.0 The chain is a choice, not an invariant.** A group may admit several Oliver chains with different primes — a cyclic group of order pqr is exhibited as cyclic-with-trivial-top by Γ₂ = 1, Γ₁ = Γ for *every* (p, q), and other choices place any of the three primes at the bottom. So "the bottom prime" and "the top prime" always mean *of the chain under consideration*. Nothing below is affected, since every argument fixes a chain first, but two things follow that are worth separating.

*A gain not yet taken.* Each admissible chain yields its own congruence: a group with top primes q₁ and q₂ forces χ(Δ_P^Γ) ≡ 1 modulo both, hence modulo lcm(q₁, q₂). The batteries of §8 enforce one chain per group and therefore leave this on the table.

*Slack in the bound.* To bound m\*(Γ) any admissible chain may be used, so the truth is m\*(Γ) ≤ minimum over its chains of that chain's bound. The enumeration instead maximises over (p, q), which is the least restrictive choice. This is **safe** — every group is covered by at least one enumerated configuration, so the result remains an upper bound — but a tighter bound is available to anyone willing to pair each group with its most restrictive chain.

*What the enumeration does with the readings.* `mu_enumerate.py` loops over every pair (p, q) of primes, so every chain-prime reading is enumerated and no Oliver group escapes: each admits some chain, that chain's primes are in the loop, and its configuration is admissible there. Empirically the optimum is attained at a **unique** (p, q) — (5,2) at n = 10, (2,3) at n = 12, (83,53) at n = 273 — because the winning configuration determines both primes.

*Twist placement: why the code need not model it.* This looks like a gap and is worth spelling out. For a **foreign** block there is no choice at all: its translations and its twist do not commute (AGL(1,r) is nonabelian), the translations must lie in the abelian cyclic layer, so the twist is forced into the top — which is exactly the content of Lemma B′, and why foreign twist orders are q-powers. For a **p-characteristic** block there is a genuine choice: the twist may sit in the cyclic layer, in the top, or split between them. Only the placement in the cyclic layer is subject to Lemma C, so one might expect a q-power twist to escape the constraint by moving to the top.

It cannot. Write the twist order as d = d′·qᵉ with gcd(d′, q) = 1. Since Γ/Γ₁ is a q-group, the image of the twist there is a q-group, so **d′ is forced into Γ₁** and Lemma C binds d′ alone. But a foreign prime r carries a nontrivial q-power twist, so q | r − 1 and hence **q ≠ r**; therefore r never divides qᵉ, and

> **r | d ⟺ r | d′.**

The part that could escape to the top is precisely the part that was never at risk. So `strip(c − 1, foreigns)` — the largest divisor of c − 1 coprime to the foreign primes — is exactly right, without modelling placement. *One unstated case:* the argument assumes the foreign block's twist is nontrivial. If q equals a foreign prime ρ whose twist is trivial, a p-part's twist can carry a ρ-power in the top after all, and the strip-based score under-states that p-part (Theorem E.3(i)'s q = r reading is the instance). This never affects the configuration's minimum: a foreign block with trivialised twist binds at orb(ρ, 1) = ρ, below anything the escape gains.

*Worked example (n = 26 as 9 + 17).* The 17-block is foreign, so its twist is forced to the top; with q = 2 all of C₁₆ survives and its orbital is 17·16/2 = 136. The 9-block is p-characteristic with twist C₈, which may go either way; gcd(8, 17) = 1 so Lemma C strips nothing and both readings give C(9,2) = 36. With the cross class at 9·17 = 153, m\* = 36 — the 9-block binds, and this configuration is far from μ(26) = 156, which comes from 2 × 13 instead. Lemma C does bite elsewhere: for c = 16 with foreign r = 3 the twist drops from 15 to 5, and there are 74 such (c, r) pairs below 200. In every one of them the q-part of the twist is too small to help, exactly as the equivalence above predicts.

**G.1 The chain descends to block stabilisers.** Let H be the setwise stabiliser of a block. Then H ∩ Γ₂ is a p-group, (H ∩ Γ₁)/(H ∩ Γ₂) embeds in the cyclic Γ₁/Γ₂ hence is cyclic, and H/(H ∩ Γ₁) embeds in the q-group Γ/Γ₁ hence is a q-group. So H — and therefore its action on the block — inherits an Oliver chain **with the same (p, q)**. The recursion of Part C is thus sound at every depth, with the primes fixed throughout.

**G.2 Every orbit is F·c with F a q-power and c a prime power.** Iterate Part B on an orbit O: each level of the tower has a block count that is a power of q (a transitive q-group has q-power degree), and the recursion terminates at the finest blocks, which are **primitive**, hence affine of prime-power degree. Writing the successive block counts b₁, …, b_t and the finest block size c,

> |O| = b₁·b₂ ⋯ b_t · c = **q^a · c**, with c a prime power.

The finest block is either p-characteristic (c a p-power, twist any divisor of c−1) or foreign, in which case Lemma B′ forces c prime with a q-power twist. **The tower depth t plays no further role: it is absorbed entirely into F = q^a.** A three-level tower and a one-level tower with the same F and c have the same orbital data.

**G.3 The general configuration, in final form.** Combining G.2 with Parts A–D, an Oliver group on n points is described by a choice of chain primes (p, q) and orbits O₁, …, O_k with

> **n = Σᵢ Fᵢ·cᵢ**, Fᵢ a q-power, cᵢ a prime power, each cᵢ p-characteristic or a foreign prime,

twists dᵢ | cᵢ−1 (a q-power when foreign), subject to Lemma C. The orbital data is that of Part E's value formula: intra-orbital Fᵢ·orb(cᵢ, dᵢ) per class, within-class cross (Fᵢ or Fᵢ/2)·cᵢ² when Fᵢ > 1, and between-orbit classes of size sᵢsⱼ.

**G.4 The search is bounded on every axis.** With δ = m\*/C(n,2): the intra-orbital satisfies Fᵢ·orb(cᵢ,dᵢ) < Fᵢcᵢ²/2 and must be at least m\*, while Fᵢcᵢ ≤ n. Hence

> **cᵢ ≥ δn**,  **Fᵢ ≤ 1/δ**,  and **k ≤ 1/√δ** (Proposition F.1).

At the weakest density below 10⁴ (0.0147) this reads c ≥ 0.0147n, F ≤ 68, k ≤ 8; at the median density, c ≥ 0.2n, F ≤ 5, k ≤ 2. Checked against every fused-form witness in the table — **3,053 of 3,053** satisfy both derived constraints, with no exceptions.

So the configuration space is finite along all three axes, with bounds computable from the density alone, and the self-certifying iteration of Part F applies unchanged. The general enumeration of G.3 is written once, in `mu_enumerate.py`, rather than as a menu of special cases — the failure mode that produced all four historical corrections — and Part E records its status.

## Part H. The cost of the search, stated without number theory

Write δ = B(n)/C(n,2) for the density the search is currently certifying. Parts F and G.4 bound every axis of the configuration space:

| axis | bound | source |
|---|---|---|
| number of orbits k | **k ≤ 1/√δ** | Prop. F.1 |
| finest-block size cᵢ | **cᵢ ≥ δn** | G.4 |
| fusion count Fᵢ | **Fᵢ ≤ 1/δ** | G.4 |
| tower depth | *irrelevant* — absorbed into Fᵢ | G.2 |

From these the size of the search follows. The admissible parts are pairs (F, c) with c a prime power in [δn, n] and F a q-power at most 1/δ, so their number is

> **P(n, δ) = O( (n / log n) · log(1/δ) )**,

and a configuration is a multiset of at most k of them summing to n. Including the choice of chain primes (p, q), the whole search is

> **O( π(n)² · P(n,δ)^{1/√δ} ) = n^{O(1/√δ)}** operations,

with the self-certifying iteration of Part F guaranteeing that the correct K is reached and recognised. Every quantity here is elementary; no conjecture has been used, and the enumeration halts with a certificate regardless of how δ turns out.

*Preprocessing.* The primes and prime powers up to n, and the factorisations needed for the q-part and Lemma C computations, all come from a single smallest-prime-factor sieve: **O(n log log n)** time and O(n) space. Afterwards primality and prime-power tests cost O(log n), q-parts O(log n), and the divisors of c−1 cost O(√n). This is dominated by the search itself — at least π(n)² ≈ (n/log n)² from the choice of chain primes alone — so it never enters the asymptotics. It is stated only because the cost model would otherwise be silent about where the arithmetic comes from.

*Measured cost* on one core (recorded when the run stood at n = 1540): 0.63 s per value at n ≈ 300, 4.79 s at n ≈ 600, 15.63 s at n ≈ 900, fitting **≈ n^2.9**. Projecting from there: roughly 11 h to reach 2000, 75 h to 3000, 595 h to 5000. Values of n are independent, so the work parallelises perfectly across disjoint ranges.

**The one term that is not bounded by anything elementary is δ itself**, and that is the whole of the dependence. *Two different δ's appear in this document and must not be conflated.* Part F's self-certification uses δ = B(n)/C(n,2), the density the search is certifying; the figure "0.0147 at n = 4917" below comes from the family-menu table `mu_fast.py`, which is a *lower* bound on μ and hence a smaller δ. Using the smaller one is safe — a too-small δ yields a too-large k bound — but it is why that number can sit alongside Part I's floor of 0.0418 over the certified range without contradiction. Unconditionally, BBKN gives μ(n) = Ω(n log n), i.e. δ = Ω(log n / n), so the exponent 1/√δ is only bounded by **O(√(n / log n))** and the search is n^{O(√n)} — subexponential, but not polynomial. Empirically δ never drops below 0.0147 anywhere under 10⁴, giving k ≤ 8, but that is an observation about a finite range and not a theorem.

**Forward pointer.** This is where the number-theoretic conjectures re-enter, and in a role distinct from the one they play in §§4–5 of the notes. There they bound μ(n) from below; here the *same* bound bounds the **running time of the search**, because δ appears in the exponent. Under the ladder — δ ≥ 1/4 for even n, δ ≥ 0.049 for odd n with 3 ∤ n, δ ≥ 0.028 for 3 | n — the orbit count falls to k ≤ 2, 4, 5 respectively (1/√0.25 = 2, 1/√0.049 = 4.52, 1/√0.028 = 5.98) and the search becomes **polynomial of fixed degree** in n. So a Hardy–Littlewood-type hypothesis buys two things at once: the value of μ(n), and a guarantee that the certified enumeration terminates in polynomial rather than n^{O(√n)} time. That is worth stating explicitly in the number-theory sections, since it is a consequence of those conjectures that has nothing to do with what they were introduced for.

## Part I. Measurements

From `mu_table_safe_v2.csv` — n = 6 … 2212, unconditional mode, 1,921 rows:

- every value certified; no internal inconsistency; **no row violates the Proposition F.1 stopping rule** (checked directly: 1/√δ ≤ K on all 1,921);
- **independently re-derived**: recomputing m\* from each row's witness string by the G.3 formulas, in a separate implementation, reproduces `mu_bound` on **1,921 of 1,921** rows, with parts summing to n, foreign parts prime and unfused and pairwise distinct, p-characteristic parts powers of p, and every F a q-power;
- the unconditional fallback is invoked on the optimum at **0 of 1,921** values, so the bound is unconditional throughout;
- **certification level, not orbit count.** The `certified_K` column records the K at which the Part F iteration halts, which is one more than the part count it rules out. Its distribution is {2: 356, 3: 1085, 4: 435, 5: 44, 6: 1}, but the **actual part counts are {1: 754, 2: 909, 3: 258}** — no winner uses more than three parts. An earlier version of this list called the column an orbit count and concluded that "K = 5 is exactly the predicted ceiling, reached by exactly the hardest rows"; that is wrong twice over. At the weakest density 0.0418 (n = 575) Proposition F.1 permits **four** orbits and the winner there uses **one**. Nothing in range has five orbits;
- what *is* tight is Part G.4 on the individual axes, and tight on a single row. At n = 575 — no longer the density floor, but still the row where both G.4 bounds bind — the witness is `23x25` with δ = 0.041812: the fusion bound 1/δ = 23.9 is met by F = 23, and the block-size bound δn = 24.0 by c = 25. Both within one unit, simultaneously — better evidence than the bulk "3,053 of 3,053" count;
- the density floor is now falling with each extension: minimum **0.037524 at n = 2291** (`2x761 + 1x769*`), maximum 0.499778 at n = 2258 (`2x1129`, Theorem 2.1), median 0.1994. It sat at 0.041812 (n = 575) for most of the programme, moved to 0.041107 (n = 2183) at n ≤ 2212, and now to n = 2291 — the drift `arithmetic-of-density.md` §4 predicts, and the reason the s = 4 branch has become reachable;
- **Theorem E.1 settles 1,390 of the 1,921 values (75.0%) outright**, with no search needed. The other 458 rely on the exhaustive certificate, and *all* 458 are uncovered for the same reason — δ ≤ 1/9. The Mersenne branch of Theorem E.1 never binds: no n in range has Cap(a) ≥ B(n) for any applicable exponent. Only Cap(2) = 6, Cap(3) = 21, Cap(5) = 155 and Cap(7) = 1143 arise, with tightest margins B/Cap = 1.43 at n = 15, 1.63 at n = 63 and 1.90 at n = 20. So the entire residual difficulty is low density, not the Mersenne coincidence.

Winning configuration shapes, over all 1,921 rows: **851** use one p-characteristic part with one foreign prime; **754** a single fused class; **257** two p-characteristic parts with one foreign prime; **58** a fused class with a foreign prime; **1** uses two foreign primes. These are the same five shapes reported at n ≤ 1306 (553 / 542 / 127 / 46 / 1) — **no sixth shape appears** in the extended range, which is the more informative fact. The last two are the ones a hand-built family menu is most likely to miss, since they combine features that are natural to treat separately. The unique two-foreign winner is n = 1175 = 641\* + 277 + 257\* at (p, q) = (277, 2), binding on the Fermat prime 257 at 257·128 = 32,896.

Against the family menu of `mu_fast.py` (measured over the range its table covers, n ≤ 1540) the enumeration is **higher at 173 values and never lower**, and the shortfalls have exactly two shapes — 127 "two p-parts plus a foreign prime" and 46 "fused class plus a foreign prime" — with no third type appearing at larger n.

**The three-part winners have one shape.** Of the 201 winners using three parts, all but one are **"one foreign prime plus two unfused p-characteristic parts"**, and all but two have the **two p-parts of equal block size** — the two exceptions being the single two-foreign winner at n = 1175 (no two p-parts at all) and n = 551 = 256 + 167\* + 128, whose two p-parts are distinct powers of 2. They occur precisely where n admits no good two-part decomposition, and reduction (R1) cannot merge the equal pair because F₁ + F₂ = 2 is not a power of the relevant q — which in these rows is 3, 5, 41, 53, 83, 89, 163, 173, 179, 233. Why a *fourth* part never wins is visible in the same shape: the binding term is C(c,2), increasing in c, and a further part of the same kind reduces the budget per part, so three equal p-parts plus a foreign strictly loses to two. Making that a theorem needs the freed points to be reabsorbable at the same n — the Diophantine step of Part J item 1.

**The low-density tail, where minimality is still open.** Corollary F.3 gives k ≤ 3 wherever δ > 1/16, so the open content of Part J item 1 is confined to the tail below that threshold: **45 of the 1,921 computed values** (1.7%), namely n = 323, 455, 527, 551, 575, 725, 731, 851, … . Proposition F.1 permits four parts at every one of them, and the winners there use one, two and three parts in 7, 10 and 11 cases respectively — so nothing in the tail approaches the permitted ceiling either.

**Three-part winners beat two-part configurations by wide margins.** Over a sample of 23 three-part winners spread across the range, the ratio B₃/B₂ — the winner against the best configuration of at most two parts at the same n — has **minimum 1.040, median 1.688, mean 1.925 and maximum 4.857**, with 7 of 23 at least 2. The extremes are informative: n = 777 = 263\* + 257 + 257 at ratio 4.857, where the Fermat prime 257's full C₂₅₆ twist gives 32,896 against a best two-part value of 6,773; and n = 1989 = 701 + 701 + 587\* at 4.192. Three-part winners are therefore not marginal improvements on two-part ones, which is what rules out the perturbation route to k ≤ 3 (Part J item 1).

**The part count is a fact about optima, not about tie-breaking.** `mu_enumerate.py` records a witness on a tie only when none exists yet, so the *reported* part count is not canonical and "max 3 parts" could have been an artefact. It is not. Asking directly whether any configuration with **exactly** k parts attains B(n) — pruned at target B, so only configurations reaching B survive — gives, at every value tested (the three-part-winner values 247, 255, 273, 285, 323, 345, 357, 377, 425, 429, 437, 465, 575 and a further sweep through 493–633): B is attained at exactly **one** part count, and **no 4- or 5-part configuration reaches it**. There are no cross-part-count ties.

**Independent validation of Lemmas B and C.** These checks were made against the notes' construction tables and the GAP battery; they are recorded here because they test the classification rather than the search.

Against every two-block witness in `mu_table_full.csv`: of 5,025 such rows, the 3,316 whose foreign block attains full capacity satisfy **Lemma B without exception** (3,302 of shape 2qᵉ, 14 of shape qᵉ), and **Lemma C's gcd condition holds in all 5,025**. Lemma B also predicts a density split among two-block witnesses — among rows clearing the 1/12 diagnostic threshold, 73.1% have r − 1 ∈ {qᵉ, 2qᵉ}; among those below, 9.9%.

That check is partly circular, since the witnesses come from our own constructions. The GAP battery at n = 10 is not: those 967 Oliver groups were enumerated exhaustively with no reference to the lemmas. Extracting vertex orbits by colour refinement and locating orbitals that induce a complete graph on their support gives **1,061 full-capacity orbits across 728 groups, of sizes 2, 3, 4, 5, 7, 8, 9 — every one a prime power, with no exceptions**; **no group** has two proper-prime-power full-capacity orbits of different primes, confirming the uniqueness of p; and of the 88 prime-sized full-capacity orbits inside groups with a genuine top prime q, **all 88** satisfy s − 1 ∈ {qᵉ, 2qᵉ}.

**Independent confirmation against exhaustive group enumeration.** Agreement with constructions drawn from the same families is partly circular; the only non-circular check is against an exhaustive enumeration of Oliver groups obtained without reference to any of this. Two exist, and both are **tight** rather than merely consistent.

| n | groups enumerated | max m\* over all of them | B(n) | attaining |
|---|---|---|---|---|
| 10 | 967 | 20 | 20 | T(10,17), order 200, orbitals {20, 25} |
| 12 | 7,115 | 18 | 18 | 8 groups, all with orbitals {18, 48} |

The n = 12 row has been re-derived directly from `groups_out.txt`: the file holds exactly 7,115 groups (295 trivial-top, 657 at q = 2, 67 at q = 3, 6,096 p-groups), the maximum m\* is 18, and exactly eight attain it — `T(12,85)`, `T(12,164)`, `T(12,166)`, `T(12,207)`, `T(12,228)`, `T(12,229)`, `T(12,265)` and `T(4,4)≀T(3,1)`, orders 144 to 5184 — all with orbital sizes {18, 48} and all sharing a single orbital partition across three distinct tags. (§8.11 of the notes previously reported 8,819 for this file; that figure was wrong.) Their common orbital data is exactly what Theorem 2.4 predicts for n = 3·4: three fused blocks of 4 with the full twist give 3·C(4,2) = 18, and the cross class, with coefficient 3 because q = 3 is odd, gives 3·4² = 48. So the exhaustive optimum *is* the predicted construction, orbital sizes included. This does not establish exhaustiveness in general — both checks sit at small n, where few configurations are available — but it is the strongest form of evidence the framework admits.

**How odd n are actually served, and the correct scope of the older diagnosis.** An earlier §5.5 of the notes explained the odd-n shortfall by arguing that the strong two-block family needs exactly one even block, that the block must be the p-characteristic one since the other has prime degree and 2 is the only even prime, and hence that odd n reach the strong family only through n = 2^a + r with r prime — about log₂n candidate splits against ~n/2 for even n. The reasoning is sound about that *family*, and it is the binding constraint for odd n with **ω(n) ≥ 3 that use two parts** — which is precisely the weak tail. What it does not describe is how most odd n are served, because most *strong* odd n have ω(n) = 2 and use a single fused class, where no additive representation enters at all.

Of the 679 odd values in the table, 548 reach density 1/12 or better. Among those:

| route | count |
|---|---|
| **no even part at all** | **461** |
| one even part, a 2-power p-characteristic block (the 2^a + r shape) | 53 |
| one even part, odd block size with even fusion count | 34 |

and by part count, 339 use a **single fused class**, 87 two parts, 122 three parts. So the dominant route for a strong odd n is Theorem 2.4 with both factors odd — n = k·m with k a q-power and m a prime power — and after that the three-part configurations.

Restricting to the values where the fused family is *unavailable* recovers the older claim exactly. Of the **150 odd values with ω(n) ≥ 3**, 97 use a three-part configuration with no even part (n = 2c + r, all odd), and 53 use two parts, of which 28 have the 2-power p-characteristic block the argument predicts. Their median density is 0.0957, sitting at the three-part cap of 1/9 rather than the two-part 1/4.

What limits odd n is therefore a pair of **caps**, not a shortage of representations. The multiplicative fused family gives density 1/F, and odd n has F ≥ 3 where even n has F = 2; the balanced additive route for odd n is three parts, capped at 1/9, rather than two, capped at 1/4. Both engines and the Bateman–Horn conditions behind the additive one are set out in `arithmetic-of-density.md`.

**The hand family menu against B₀, above the computed range.** These figures compare `mu_fast.py`'s menu of constructions against the crude ceiling B₀ of Part C.2, and are the only measurements in this framework still taken against B₀ rather than B — which is why they look worse than they are. Over the 6,401 values n ≤ 10⁴ the menu leaves gapped against B₀, the median ratio menu/B₀ is 0.533, the worst cases being the familiar arithmetically weak odd n: n = 1425 at 10,025 against 171,991 (ratio 0.058), then 4245, 3393, 5457, 4059. At n = 1425 roughly two thirds of that apparent gap is B₀'s own slack, not the menu's shortfall — B(1425) = 108,811 against B₀ = 171,991, per the worked contrast in C.2. Below n = 2298 there is no gap at all, since B is computed exactly and attained.

**Foreign-block efficiency.** For a foreign prime r under top prime q the usable twist is t = (q-part of r−1), and the intra-orbital is r·|±δT|/2 against a maximum of C(r,2). So

> **eff(r, q) = (t if t is even, else 2t)/(r − 1)**, with **eff = 1 exactly when r − 1 = qᵉ or 2qᵉ** — precisely the case in which Part B's restriction of foreign twists to q-powers costs nothing.

Fermat primes achieve this at q = 2, safe primes with t = q odd and 2t = r−1, and the general family is r = 2qᵉ + 1 (so 163 = 2·3⁴+1 and 251 = 2·5³+1 qualify without being either). Across winning configurations about 77% of the foreign blocks used have efficiency 1, the commonest being 487, 257, 347 and 383. (The notes' glossary quotes 74.8% with a different top-five; that figure is over n < 685 and this one over the full range — same measurement, different windows.) The Fermat prime 257 is frequently the *binding* orbital, its full C₂₅₆ twist giving 257·128 = 32,896.

## Part J. Open items

*What is established, and where. Completeness and realisability: Part E. The sandwich B_refined ≤ μ ≤ B_safe, Theorem E.1, and the collapse certificate: Part E′. The search bounds and why counting cannot sharpen them further: Part F. All measurements: Part I. This section lists only what remains.*

1. **Minimality: k ≤ 3 in the low-density tail.** Corollary F.3 makes this free wherever δ > 1/16 — 97.9% of the computed table — so what is open is the tail below that threshold, measured in Part I at 28 of 1,921 values. (How much of n > 2007 lies below 1/16 is itself governed by the open density questions, so this is a per-n statement, not a global one.)

   Three findings constrain any proof there, all recorded elsewhere: Proposition F.2 shows counting saturates at four parts, so the argument must be arithmetic; the wide B₃/B₂ margins of Part I rule out a perturbation or small-domination route, since a proof must instead *produce* a strong ≤3-part decomposition at the given n; and n = 551 = 256 + 167\* + 128 (Part I) forbids assuming the two p-parts are equal, since distinct powers of one prime can win. The supply question that remains has the same shifted-prime character as the density questions, which is why this item and item 2 now sit in the same regime.

   The three older sub-narrowings — at most two p-characteristic classes, at most two foreign primes, at most one fused class — all follow from k ≤ 3 and remain individually worth proving, since each removes a different search axis regardless of density.

2. **The collapse for odd n at low density: the global promotion.** Part E′ closes every branch but one — s = 3 outright (E.4), the s = 2 repunit family by absolute cap (E.3(iii)), s = 1 by Cap(a) (E.1), and everything at δ > 1/9 (E.1) — and E″ certifies the collapse at all but two composite non-prime-power n ≤ 100,000 from lower bounds alone. The single surviving branch is **s = 2 with c a safe prime**, and within it E.3(ii) now resolves the bare pair outright, so what is open is only the case **with a leftover**.

   The obstruction there is sharp: at L = c the (r, r) re-reading would require two equal foreign parts, which admissibility forbids. The two values the certificate cannot settle below 100,000 — **n = 50,817 and n = 89,697**, both of shape two equal c-blocks plus the foreign r = (c−1)/2 — are exactly this, and are the concrete targets.

   What else is known: cases (α)–(γ) of E″ prove no *structural* argument can do it, since within a fallback configuration's own partition the fallback reading is forced, so any proof must compare across partitions of n where arithmetic supply enters. The Cunningham chain 719 → 1439 → 2879 is where the leftover cases bite hardest, and the **q-pinning mechanism** that kills those (r − 1 = 2q pins the top prime, forcing every leftover foreign part into r_j ≡ 1 mod q) is the likely ingredient of an unconditional argument.

   The alternative route is to raise δ₀^odd above 1/9, which would bring odd n under Theorem E.1 wholesale. That is Open Problem 2 of the notes — the 0.049 ceiling of Prop. 5.3 — and is the same obstruction as everything else about odd n.

   Two things to keep in view. The per-n frontier now stands at n ≤ 100,000 and extends cheaply, since E″'s lower-bound pass dominates the cost and is cached. And "almost all n" is the wrong target — the density thresholds of Part I show δ ≥ 1/4 at only 18.5% of computed values, so density-1/4 is a minority property; proving thinness of the exceptional set would land on the same shifted-prime condition, a Hardy–Littlewood-type statement of the tier this framework is trying to avoid depending on.

3. **More non-circular confirmation.** The two exhaustive comparisons (Part I) both sit at small degree, where few configurations are available, so they cannot establish exhaustiveness in general. A third degree would be worth more per unit of compute than any extension of the numerical range — but exhaustive enumeration of Oliver groups is only feasible at small degrees, so the supply is short. Per the epistemic note at the top, an independent reading of Lemma B′, Lemma C and G.2 is worth more than either.

4. **Extending the numerical range.** Validation currently reaches **n = 2298** at a measured cost of about n^2.9 per value; see Part H for projections. This extends the certificate's per-n coverage and tests the implementation, but does not test the classification, whose consequences do not vary with n.
