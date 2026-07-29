# Bounding μ(n) by enumeration of Oliver configurations

*Companion to `orbital-evasiveness-notes.md` §2. Establishes an upper bound on μ(n) by classifying the possible orbit-and-twist structures of an Oliver group and enumerating them. Implemented in `mu_enumerate.py`.*

**Status.** Parts A–D and F–H are proved. The enumeration of Part E is complete and finite but not known to be minimal. The bound computed by the implementation is **unconditional**: its one hypothesis-dependent ingredient is never invoked on an optimal configuration (Part B). Numerical validation currently reaches n = 1540. Open items are collected at the end.

**On the word "proved", and on what the numerical checks are for.** The statuses above mean *an argument has been written down that appears complete*, not *the argument has been verified by anyone else*. The distinction is not academic here: the ΓL(1) step of Part B was asserted as a plausible sketch and is false, which was established only by deliberately looking for a counterexample. Lemma B′'s socle argument, Lemma C's conjugation argument and the tower absorption of G.2 are of comparable intricacy and have had no independent scrutiny.

The numerical work therefore serves three distinct purposes, which are easy to conflate:

1. **Implementation fidelity.** Internal consistency, the Proposition F.1 stopping rule, and monotonicity of the certified maxima test whether `mu_enumerate.py` computes what Parts A–H specify. This validates code against a specification and is not evidence for any theorem.
2. **Tightness.** The inequality μ(n) ≤ B(n) is a consequence of the classification; the *equality* μ(n) = B(n) requires an attaining construction, which is checked case by case rather than proved in general. Similarly, that the unconditional scoring costs nothing relative to the ΓL(1)-assuming one is an observation, not a theorem — though the bound's validity does not depend on it.
3. **A hedge against errors in the arguments themselves.** If Lemma B′, Lemma C or the block recursion were wrong in a direction that made the bound too small, violations would be expected. None appears across 1,269 computed values or in either exhaustive battery, where the bound is not merely respected but attained. This is real evidence — for the correctness of the reasoning, rather than for filling a gap in reasoning already known to be sound.

**Which uncertainties are uniform in n, and which are range-limited.** These are easy to confuse, and the distinction determines what further computation buys.

*Uniform in n — the dominant risk.* Every simplification the search relies on (Proposition F.1's orbit bound, block counts restricted to q-powers, Lemma B′, Lemma C, the absorption of tower depth into F) is a consequence of an argument that either holds for every n or for none. There is no mechanism by which such a constraint could hold below some threshold and fail above it. So the residual doubt is not whether the trimmings continue but whether the arguments are correct — and if one is not, the computed values are wrong at small n as much as at large.

*Range-limited, and affecting tightness rather than validity.* The inequality μ(n) ≤ B(n) follows from the classification; the equality requires an attaining construction, verified for the four winning shapes and spot-checked by orbit computation. A fifth winning shape at larger n would still be covered by the enumeration, but its attainment would want separate verification. Likewise the observations that the unconditional scoring costs nothing, and that no winning configuration uses more than two p-characteristic classes or more than two foreign primes, are statements about the range examined.

*What this implies for effort.* Extending the numerical range mainly tests the implementation, since the classification's consequences do not vary with n. Extending the *exhaustive* comparison to further n tests the classification itself, and is therefore worth more per unit of compute — but exhaustive enumeration of Oliver groups is only feasible at small degrees, so the supply of such tests is short. Independent reading of Lemma B′, Lemma C and G.2 would be worth more than either.

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
3. **The refined formula for p-characteristic parts is only justified for ΓL(1)-type H.** Writing the minimum intra-orbital as c·(smallest ±H-orbit on non-zero vectors)/2, the code takes the twist to be cyclic of order d = strip(c−1, foreigns) and computes orb(c, d). For non-ΓL(1) H the orbits can be larger than the ±δT classes — up to |H| = |C|·qᵉ rather than |C| — so orb(c, d) can be an **under**-estimate by as much as a factor 2qᵉ. This is the only place where the ΓL(1) assumption could matter.

*How much this can matter.* The under-estimate only matters when the p-characteristic part is the *binding* orbital **and** Lemma C has cut d down **and** a non-ΓL(1) irreducible cyclic-by-q group exists at that degree. Continuing the counterexample: a block of 343 carrying E has all its ±E-orbits of size at most 54, so its minimum orbital is at most 343·54/2 = 9,261, whereas the ΓL(1) option with the full Singer twist gives C(343,2) = 58,653. The exotic group is worth roughly a sixth of the ordinary one, and is only competitive when Lemma C has already destroyed most of the Singer twist. In the natural test case — 343 together with a foreign prime 19, so that 19 | 342 forces d down to 18 — the foreign block's own orbital (19·9 = 171) binds long before either p-block value matters.

**The two agree on every optimum.** The unconditional option is to give a p-characteristic part the capacity F·C(c,2) — valid for *any* point stabiliser — whenever Lemma C strictly reduces its twist. This is the default in `mu_enumerate.py` (`--refined` restores the ΓL(1)-assuming formula), and it costs nothing:

> Across all 1,066 computed values to n = 1306, **Lemma C strictly reduces the twist of a p-characteristic part in 0 of the 1,163 such parts appearing in winning configurations.** Equivalently, an optimal configuration never pairs a p-block with a foreign prime dividing its twist order — the optimiser simply chooses a foreign prime elsewhere.
>
> Confirmed directly by a full unconditional-mode run to n = 1000 (`mu_table_safe.csv`, 806 rows): the fallback is invoked on the winning configuration at **0 of 806** values, and comparing the two modes row by row gives **0 of 806 differences**. The equality of the two bounds is therefore established across the whole computed range, not merely sampled.

That makes the two bounds identical, for a reason worth stating: when Lemma C does not bite, d = c−1 and **orb(c, c−1) = C(c,2)** exactly (in characteristic 2 because −1 = 1, and in odd characteristic because c−1 is even). So on every optimum the refined formula already *equals* the unconditional cap, and the failure of the Singer step cannot affect the computed value. Confirmed directly: over n ≤ 1000 in both modes, **0 of 806 rows differ**.

The refined formula is therefore only ever strictly below C(c,2) on configurations that lose anyway, and B(n) is valid independently of what the point stabilisers look like.
- Consequently the intra-orbitals are the classes ±δ·T for T the twist group, and the minimum intra-orbital is **orb(s, t) = s·t/2 if t is even or p₀ = 2, else s·t**, where t = |T|.
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

## Part D. Coherence across parts

**Lemma C (corrected justification).** Let O_i be a p-characteristic part with twist order d_i, and O_j a foreign prime part of size r_j whose translations lie in Γ₁ (Part B). The images of Γ₁/Γ₂ in the two parts are C_{d_i} and C_{r_j}. The top q-group acts on the cyclic group Γ₁/Γ₂ by conjugation; on part j it induces the twist, of order t_j > 1, and on part i it induces the identity (it acts trivially there). If r_j | d_i, the r_j-primary component of Γ₁/Γ₂ surjects onto both images, so the conjugation action cannot be simultaneously trivial on one and of order t_j on the other. Hence **gcd(d_i, r_j) = 1**.

> **Pitfall.** The weaker argument — "independent pieces generate a direct product, which must be cyclic" — does **not** establish this. A single generator can act as a twist on one part and a translation on another, in which case cyclicity alone imposes nothing. The conjugation action is what forces coprimality.

Twists on distinct p-characteristic parts carry **no** mutual constraint: a single cyclic generator surjects onto each, which is exactly what the diagonal constructions exploit.

## Part E. Completeness of the enumeration

This is the remaining gap, and it is a real one rather than a formality.

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

What does **not** reduce is parts of unequal size and the choice of bottom prime: both are genuinely distinct configurations, and the measured data shows both matter (127 winners use two classes of different sizes, and the winning p ranges from 2 to 821).

**Status of the enumeration.** Every configuration permitted by Parts A–D is enumerated, within the bounds proved in F and G, so the enumeration is **complete and finite**. It is not known to be **minimal**: no argument prunes it to a shortest sufficient list. That affects running time, not validity. Several structural questions that might have obstructed completeness do not: the number of foreign parts needs no separate cap, since foreign parts are orbits and Proposition F.1 bounds the orbit count; multiple p-characteristic classes of different sizes are enumerated as multisets of parts; and towers do not couple to foreign parts (Part G).

## Part F. The search is bounded

The enumeration needs no number-theoretic input to be finite, and the bound is small.

> **Proposition F.1 (part count).** If a configuration on n points achieves density δ = m\*/C(n,2), then it has at most **1/√δ** orbits.
>
> *Proof.* Each orbit's capacity is at most C(s_i, 2) < s_i²/2 (Part C), and m\* ≤ min_i cap(s_i) by Part A, so s_i > √(2m\*) = √(δ·n(n−1)) for every i. Summing over the k orbits, n = Σ s_i > k√(δ·n(n−1)), whence k < 1/√δ (up to the n/(n−1) factor). ∎

Two consequences.

*The search is small in practice.* The weakest density anywhere below 10⁴ is 0.0147 (at n = 4917), giving k ≤ 8; at the median density 0.2 the bound is k ≤ 2. So **no admissible configuration below 10⁴ has more than eight orbits**, and most have two.

*The search is self-certifying.* Let B_K(n) be the maximum over configurations with at most K parts, and δ_K its density. B_K is non-decreasing in K, so δ_K is too, and 1/√δ_K is non-increasing. Compute B_2, B_3, … and stop at the first K with 1/√δ_K ≤ K: by Proposition F.1 no configuration with more than K parts can achieve δ_K, so B_K = B. For every n below 10⁴ this terminates by K = 8. **No conjecture is consulted at any point.**

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

The part that could escape to the top is precisely the part that was never at risk. So `strip(c − 1, foreigns)` — the largest divisor of c − 1 coprime to the foreign primes — is exactly right, without modelling placement.

*Worked example (n = 26 as 9 + 17).* The 17-block is foreign, so its twist is forced to the top; with q = 2 all of C₁₆ survives and its orbital is 17·16/2 = 136. The 9-block is p-characteristic with twist C₈, which may go either way; gcd(8, 17) = 1 so Lemma C strips nothing and both readings give C(9,2) = 36. With the cross class at 9·17 = 153, m\* = 36 — the 9-block binds, and this configuration is far from μ(26) = 156, which comes from 2 × 13 instead. Lemma C does bite elsewhere: for c = 16 with foreign r = 3 the twist drops from 15 to 5, and there are 74 such (c, r) pairs below 200. In every one of them the q-part of the twist is too small to help, exactly as the equivalence above predicts.

**G.1 The chain descends to block stabilisers.** Let H be the setwise stabiliser of a block. Then H ∩ Γ₂ is a p-group, (H ∩ Γ₁)/(H ∩ Γ₂) embeds in the cyclic Γ₁/Γ₂ hence is cyclic, and H/(H ∩ Γ₁) embeds in the q-group Γ/Γ₁ hence is a q-group. So H — and therefore its action on the block — inherits an Oliver chain **with the same (p, q)**. The recursion of Part C is thus sound at every depth, with the primes fixed throughout.

**G.2 Every orbit is F·c with F a q-power and c a prime power.** Iterate Part B on an orbit O: each level of the tower has a block count that is a power of q (a transitive q-group has q-power degree), and the recursion terminates at the finest blocks, which are **primitive**, hence affine of prime-power degree. Writing the successive block counts b₁, …, b_t and the finest block size c,

> |O| = b₁·b₂ ⋯ b_t · c = **q^a · c**, with c a prime power.

The finest block is either p-characteristic (c a p-power, twist any divisor of c−1) or foreign, in which case Lemma B′ forces c prime with a q-power twist. **The tower depth t plays no further role: it is absorbed entirely into F = q^a.** A three-level tower and a one-level tower with the same F and c have the same orbital data.

**G.3 The general configuration, in final form.** Combining G.2 with Parts A–D, an Oliver group on n points is described by a choice of chain primes (p, q) and orbits O₁, …, O_k with

> **n = Σᵢ Fᵢ·cᵢ**, Fᵢ a q-power, cᵢ a prime power, each cᵢ p-characteristic or a foreign prime,

twists dᵢ | cᵢ−1 (a q-power when foreign), subject to Lemma C. The orbital data is

**G.4 The search is bounded on every axis.** With δ = m\*/C(n,2): the intra-orbital satisfies Fᵢ·orb(cᵢ,dᵢ) < Fᵢcᵢ²/2 and must be at least m\*, while Fᵢcᵢ ≤ n. Hence

> **cᵢ ≥ δn**,  **Fᵢ ≤ 1/δ**,  and **k ≤ 1/√δ** (Proposition F.1).

At the weakest density below 10⁴ (0.0147) this reads c ≥ 0.0147n, F ≤ 68, k ≤ 8; at the median density, c ≥ 0.2n, F ≤ 5, k ≤ 2. Checked against every fused-form witness in the table — **3,053 of 3,053** satisfy both derived constraints, with no exceptions.

So the configuration space is finite along all three axes, with bounds computable from the density alone, and the self-certifying iteration of Part F applies unchanged. **What remains of Part E is now purely to write the enumeration of G.3 once, generally, rather than as a menu of special cases** — the failure mode that produced all four corrections.

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

*Measured cost* on one core: 0.63 s per value at n ≈ 300, 4.79 s at n ≈ 600, 15.63 s at n ≈ 900, fitting **≈ n^2.9**. Projecting from n = 1540: roughly 11 h to reach 2000, 75 h to 3000, 595 h to 5000. Values of n are independent, so the work parallelises perfectly across disjoint ranges.

**The one term that is not bounded by anything elementary is δ itself**, and that is the whole of the dependence. Unconditionally, BBKN gives μ(n) = Ω(n log n), i.e. δ = Ω(log n / n), so the exponent 1/√δ is only bounded by **O(√(n / log n))** and the search is n^{O(√n)} — subexponential, but not polynomial. Empirically δ never drops below 0.0147 anywhere under 10⁴, giving k ≤ 8, but that is an observation about a finite range and not a theorem.

**Forward pointer.** This is where the number-theoretic conjectures re-enter, and in a role distinct from the one they play in §§4–5 of the notes. There they bound μ(n) from below; here the *same* bound bounds the **running time of the search**, because δ appears in the exponent. Under the ladder — δ ≥ 1/4 for even n, δ ≥ 0.049 for odd n with 3 ∤ n, δ ≥ 0.028 for 3 | n — the orbit count falls to k ≤ 2, 5, 6 respectively and the search becomes **polynomial of fixed degree** in n. So a Hardy–Littlewood-type hypothesis buys two things at once: the value of μ(n), and a guarantee that the certified enumeration terminates in polynomial rather than n^{O(√n)} time. That is worth stating explicitly in the number-theory sections, since it is a consequence of those conjectures that has nothing to do with what they were introduced for.

## Part I. Measurements

From `mu_table_safe.csv` — 1,269 values, n = 6 … 1540, unconditional mode:

- every value certified; no internal inconsistency; **no row violates the Proposition F.1 stopping rule**;
- orbit counts K ∈ {2: 261, 3: 738, 4: 254, 5: 16}. The weakest density is 0.0418 and 1/√0.0418 = 4.89, so **K = 5 is exactly the predicted ceiling**, reached by exactly the hardest rows — the stopping criterion is tight, not merely valid;
- the density floor is stable rather than eroding across the range (per-segment minima 0.074, 0.042, 0.051, 0.042, 0.058), with the median drifting 0.252 → 0.203;
- the unconditional fallback is invoked on the optimum at **0 of 1,269** values, so the bound is unconditional throughout.

Winning configuration shapes: 553 use one p-characteristic part with one foreign prime; 542 a single fused class; 127 two p-characteristic parts with one foreign prime; 46 a fused class with a foreign prime; 1 uses two foreign primes. The last two shapes are the ones a hand-built family menu is most likely to miss, since they combine features that are natural to treat separately.

Against the family menu of `mu_fast.py` the enumeration is **higher at 173 values and never lower**, and the shortfalls have exactly two shapes — 127 "two p-parts plus a foreign prime" and 46 "fused class plus a foreign prime" — with no third type appearing at larger n.

**Foreign-block efficiency.** For a foreign prime r under top prime q the usable twist is t = (q-part of r−1), and the intra-orbital is r·|±δT|/2 against a maximum of C(r,2). So

> **eff(r, q) = (t if t is even, else 2t)/(r − 1)**, with **eff = 1 exactly when r − 1 = qᵉ or 2qᵉ** — precisely the case in which Part B's restriction of foreign twists to q-powers costs nothing.

Fermat primes achieve this at q = 2, safe primes with t = q odd and 2t = r−1, and the general family is r = 2qᵉ + 1 (so 163 = 2·3⁴+1 and 251 = 2·5³+1 qualify without being either). Across winning configurations about 77% of the foreign blocks used have efficiency 1, the commonest being 487, 257, 347 and 383. The Fermat prime 257 is frequently the *binding* orbital, its full C₂₅₆ twist giving 257·128 = 32,896.

## Part J. Open items

1. **Minimality of the enumeration.** Finiteness and completeness are proved; a domination argument reducing the permitted configurations to a shortest sufficient list is not. This costs running time only. The winning configurations are empirically far narrower than the permitted space — across the computed range none uses more than two p-characteristic classes, more than two foreign primes, or more than one fused class, against a permitted orbit count of up to 1/√δ ≈ 5. Proving any of those three would shorten the search substantially.

2. **Recovering the ΓL(1) conclusion for partial capacity** (Part B). Huppert's classification of solvable 2-transitive groups supplies it for *full*-capacity orbits outside a finite list of exceptional degrees — but full capacity yields C(c,2) for any stabiliser and so needs no such input. The open case is partial capacity, where no classification is available. Nothing in the bound depends on it.
3. **Realisability — provable, and the construction is generic.** Every configuration the enumeration admits is realised by an explicit group, assembled from ingredients whose Oliver condition is verified purely arithmetically. Given (p, q) and parts (Fᵢ, cᵢ, type, twist dᵢ):

   - each p-characteristic part contributes the translations of its Fᵢ blocks of 𝔽_{cᵢ}, all of which lie in the bottom p-group Γ₂;
   - each foreign part contributes translations C_{r} lying in the cyclic layer;
   - one generator of the cyclic layer carries the twists of all p-characteristic parts *diagonally*, its image in each part being that part's full twist C_{dᵢ}, so distinct p-parts need no coprimality between their twist orders;
   - each foreign twist, a q-power, and each fusion class's block permutation both lie in the top q-group.

   Γ₂ is a p-group by construction; Γ₁/Γ₂ is cyclic exactly when the independent orders in it are pairwise coprime, which is Lemma C and is what the enumeration enforces; Γ/Γ₁ is a q-group as a product of q-groups on disjoint supports. And the resulting orbital sizes are *forced*, not chosen: the intra-orbital of a class is Fᵢ·orb(cᵢ, dᵢ) because the block permutation fuses the Fᵢ copies; the within-class cross is (Fᵢ or Fᵢ/2)·cᵢ² because the minimum pair-orbital of a transitive q-group on Fᵢ points is exactly Fᵢ/2 for q = 2 and Fᵢ for odd q (Part E); and the between-orbit classes are single orbitals of size sᵢsⱼ because the translations of distinct orbits act independently.

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

   So **B(n) is attained and μ(n) = B(n)**, with one caveat: in unconditional mode a p-characteristic part whose twist Lemma C reduces is scored F·C(c,2), which the construction does *not* reach — it reaches F·orb(c,d). At such a configuration the unconditional score is an over-estimate. This is the ΓL(1) question of Part B in another guise, and it is empty in the computed range, where the fallback is never invoked on an optimum.

   > **Pitfall.** When checking this by construction, the twist must be a multiplicative generator of the *field* 𝔽_c. Using ℤ/c instead is correct only for prime c, and silently gives wrong orbital sizes for proper prime powers — for n = 12 with three blocks of 4 it yields 6 rather than 18.


4. **Independent confirmation.** Agreement with constructions drawn from the same families is partly circular, so the only non-circular check is against an exhaustive enumeration of Oliver groups obtained independently. Two are available, and both are **tight** rather than merely consistent.

   | n | groups enumerated | max m\* over all of them | B(n) | attaining |
   |---|---|---|---|---|
   | 10 | 967 | 20 | 20 | T(10,17), order 200, orbitals {20, 25} |
   | 12 | 7,115 | 18 | 18 | 8 groups, all with orbitals {18, 48} |

   At n = 12 the optimum is realised by eight groups spanning orders 144 to 5184, including the wreath form T(4,4) ≀ T(3,1), and they fall into only two orbital partitions. Their common orbital data {18, 48} is exactly what Theorem 2.4 predicts for n = 3·4: three fused blocks of 4 with the full twist give 3·C(4,2) = 18, and the cross class, with coefficient 3 because q = 3 is odd, gives 3·4² = 48. So the exhaustive enumeration's optimum *is* the predicted construction, orbital sizes included.

   This does not establish exhaustiveness in general — both checks sit at small n, where few configurations are available — but it is the strongest form of evidence the framework admits, and at both values the bound is attained.

5. **Extending the numerical range.** Validation currently reaches n = 1540 at a measured cost of about n^2.9 per value; see Part H for projections.
