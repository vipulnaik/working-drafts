# Toward exhaustiveness of the configuration enumeration

*Working proof document. Companion to `orbital-evasiveness-notes.md` §2.6 and §3. Each part carries an explicit status: **PROVED**, **SKETCH** (argument complete but unchecked), or **OPEN**. The goal is the statement*

> **Target.** For every Oliver group Γ of degree n, m\*(Γ) ≤ B(n), where B(n) is the maximum over the enumerated configurations.

*Together with the constructions (each an explicit group, hence unconditional lower bounds), the Target would give μ(n) = B(n) exactly.*

---

## Part A. Reduction to orbits and crosses — **PROVED**

Let Γ have vertex orbits O₁, …, O_k with |O_i| = s_i. A pair inside O_i has its whole Γ-orbital inside O_i, and a pair between O_i and O_j has its orbital inside O_i × O_j. Hence

> m\*(Γ) ≤ min( min_i M_i , min_{i<j} s_i·s_j ),

where M_i is the minimum intra-orbital of the transitive group Γ|_{O_i}. Both terms are needed: the first is the intra-orbit content, the second bounds every cross class by the total number of pairs available to it. Parts of size 1 are permitted but contribute a cross bound of s_j, so any configuration containing a fixed point has m\* ≤ max_j s_j ≤ n−1 and is dominated except at tiny n.

## Part B. Per-orbit classification — **PROVED** (Singer step **SKETCH**)

By Lemma A, Γ|_{O} inherits the chain with the same (p, q). Since Oliver's condition forces solvability, Γ|_O is solvable and transitive, so exactly one of:

**(B1) Primitive.** A solvable primitive group is affine: O carries the structure of 𝔽_{p₀}^a and Γ|_O = 𝔽_{p₀}^a ⋊ H with H ≤ GL(a, p₀) irreducible.

- *H is cyclic-by-q.* H inherits the chain, so it is p-by-cyclic-by-q; its normal p-subgroup is unipotent, and a normal unipotent subgroup of an irreducible linear group has a nonzero invariant fixed space, contradicting irreducibility unless trivial.
- *H lies in ΓL(1, p₀^a).* **[SKETCH]** Let C ◁ H be the cyclic normal subgroup. If C acts irreducibly then 𝔽_{p₀}[C] is a division algebra by Schur and a field by Wedderburn, so O is one-dimensional over it and C ⊆ 𝔽_{p₀^a}^\*, a Singer cycle; then H ≤ N_{GL}(C) = ΓL(1, p₀^a). If C is reducible, O splits into C-isotypic components permuted by the q-group H/C, so their number is a q-power and the configuration is imprimitive — case (B2).
- Consequently the intra-orbitals are the classes ±δ·T for T the twist group, and the minimum intra-orbital is **orb(s, t) = s·t/2 if t is even or p₀ = 2, else s·t**, where t = |T|.
- *Foreign characteristic (p₀ ≠ p).* Lemma B′: π_O(Γ₂) is a normal p-subgroup of a primitive group, hence trivial; π_O(Γ₁) is cyclic normal, so contains the socle, forcing a = 1; being cyclic it centralises the socle, so equals it; hence the entire twist lies in Γ/Γ₁, a q-group. **So s is prime and t is a power of q.**
- *Own characteristic (p₀ = p).* t may be any divisor of s−1, realised by a subgroup of the Singer cycle inside the cyclic layer.

**(B2) Imprimitive.** There is a block system; taking a coarsest one, the induced action on blocks is primitive solvable, hence affine of prime-power degree — and it must be a **q**-group action for the chain, so the number of blocks is a power of q. The block stabiliser acts transitively on a block, again inheriting the chain, and the intra-block orbital valencies are its suborbit sizes. Recurse.

## Part C. The valency recursion — **PROVED** given Part B

Define, for chain primes (p, q),

> V(s; p, q) = s − 1 if s is a power of p;
> V(s; p, q) = t or 2t (t the q-part of s−1, the former iff t is even) if s is a prime ≠ p;
> V(s; p, q) = max over q-power divisors b > 1 of s of V(s/b; p, q) otherwise;

and cap(s; p,q) = s·V(s; p,q)/2. Induction on s using Part B gives M_i ≤ cap(s_i; p, q) for every orbit. The restriction of b to q-powers is essential and was the source of an earlier over-count.

## Part D. Coherence across parts — **PROVED**

**Lemma C (corrected justification).** Let O_i be a p-characteristic part with twist order d_i, and O_j a foreign prime part of size r_j whose translations lie in Γ₁ (Part B). The images of Γ₁/Γ₂ in the two parts are C_{d_i} and C_{r_j}. The top q-group acts on the cyclic group Γ₁/Γ₂ by conjugation; on part j it induces the twist, of order t_j > 1, and on part i it induces the identity (it acts trivially there). If r_j | d_i, the r_j-primary component of Γ₁/Γ₂ surjects onto both images, so the conjugation action cannot be simultaneously trivial on one and of order t_j on the other. Hence **gcd(d_i, r_j) = 1**.

*Note.* The earlier justification — "independent pieces generate a direct product which must be cyclic" — is **incomplete**: a single generator can act as a twist on one part and a translation on another, in which case no coprimality follows from cyclicity alone. The conjugation argument above is the correct one, and it is what makes the constraint survive.

Twists on distinct p-characteristic parts carry **no** mutual constraint: a single cyclic generator surjects onto each, which is exactly what the diagonal constructions exploit.

## Part E. Completeness of the enumeration — **OPEN**

This is the remaining gap, and it is a real one rather than a formality.

**The general configuration.** Parts B–D leave the following shape. Fix chain primes (p, q). The orbits are: some p-characteristic parts, each a p-power, grouped into fusion classes permuted by transitive q-groups (so each class has q-power size); and some foreign parts, each a prime with a q-power twist, subject to Lemma C against every p-part twist. Writing one fusion class of F blocks of size m together with foreign primes r₁, …, r_v:

> value = min( F·orb(m, d), (F or F/2)·m², min_j orb(r_j, t_j), min_j F·m·r_j, min_{j<j'} r_j·r_{j'} )

with d the largest divisor of m−1 coprime to every r_j, t_j the q-part of r_j−1, and the second term present only when F > 1 (its coefficient F for odd q, F/2 for q = 2, from the pattern-orbit count of the transitive q-group on the blocks).

**A counterexample to the previous five-family list.** The families used in §2.6 were: fused blocks alone; two p-power parts; one p-power part plus one foreign prime; plus two foreign primes; and the transitive fallback. Searching the general shape above found a configuration outside all of them:

> **n = 273 = 16·11 + 97.** Take F = 16 fused blocks of m = 11 with diagonal twist d = 10, and one foreign prime r = 97 with twist t = 32 (the 2-part of 96); q = 2, p = 11. The chain is 𝔽₁₁^16 ◁ 𝔽₁₁^16 ⋊ (C₁₀ × 𝔽₉₇) ◁ Γ, whose middle quotient C₁₀ × C₉₇ = C₉₇₀ is cyclic since gcd(10, 97) = 1, and whose top layer is the transitive 2-group on the sixteen blocks together with C₃₂. Orbital sizes are {880, 968, 1552, 17072}, so m\* = **880**, against the 689 the five families gave.

A second instance: **n = 315 = 2·61 + 193**, with two fused blocks of 61 (twist 60) and the foreign prime 193 (twist 64, the 2-part of 192) at q = 2, giving orbitals {3660, 3721, 6176, 23546} and m\* = **3660** against 2016 — a factor 1.82. Sweeping this shape over n ≤ 1000 improves **45 values**, median 1.54× and up to 4.05× (n = 651: 8,128 → 32,896); the hits are always at q = 2 and usually involve a foreign prime whose predecessor is a large power of 2, with 257 = 2⁸ + 1 alone accounting for 33 of the 45 — its full twist C₂₅₆ gives the binding orbital 257·128 = 32,896. Restricted to n ≤ 400 the affected rows are exactly n = 273 and n = 315, i.e. 2 of 302.

So **the five-family list is not exhaustive**: it separated "fused blocks" from "foreign primes" and never combined them. The general configuration above is the natural repair, and it subsumes families (i), (iii) and (iv) as the cases v = 0, F = 1 with v = 1, and F = 1 with v = 2.

**Scale of the omission.** Sweeping the mixed shape (F > 1 fused blocks together with one or two foreign primes) over n ≤ 1000 finds **45 values** where it beats the previous best construction, with a median gain of 1.54× and a maximum of 4.05× (n = 651: 8,128 → 32,896). The mechanism is uniform: **every one of the 45 has q = 2**, and the foreign prime is almost always one whose predecessor is 2-heavy — 257 appears 33 times, then 577, 193, 449, 641. Since 257 − 1 = 2⁸, the twist on that block is the full C₂₅₆, giving an intra-orbital of 257·128 = 32,896, and that term is what binds. Fusion sizes are F = 2 (32 cases), 4 (10), 8 (1), 16 (2).

So the family exploits **Fermat-like foreign primes at q = 2** in combination with fused blocks — a combination neither the fused-only nor the foreign-only families could express.

**Consequence for the exactness claim.** Because the *bound* was computed from the same five families, it too was too small at these 45 values: the constructions there now exceed it, so the five-family bound was not a valid upper bound and the claim that μ is determined exactly for every n below 1000 **fails at (at least) those 45 values**. The claim survives at the remaining 761, subject to the same completeness caveat as before. Both the bound and the constructions must be recomputed with the mixed family included before any exactness figure is quoted again.

**What is still not established.** Even the general configuration above is a *shape*, not a proof of exhaustiveness. The open points:

1. **Several fusion classes.** The display treats one class of equal-sized p-parts. Configurations with two or more classes of different sizes are covered only in the special case F₁ = F₂ = 1 (family (ii)). The cross-orbital bookkeeping between two fused classes needs writing down.
2. **Nested towers.** Part C's recursion handles imprimitive orbits by dropping to blocks, but the interaction between a nested tower and *foreign* parts elsewhere in the partition has not been checked.
3. **The number of foreign parts.** The search that found n = 273 capped v at 3. Nothing rules out v ≥ 4 contributing at some n, though the cross terms r_j r_{j'} make large v self-defeating.
4. **A completeness argument.** What is wanted is a proof that every configuration permitted by Parts B–D is dominated by one of an explicit finite list — ideally by showing that any two fusion classes may be merged or one discarded without decreasing the value.

**Methodological note, earned the hard way.** Under-enumeration has now produced three separate corrections: five violations before three-part configurations were added; Theorem 2.4 (block counts may be prime powers, not just primes); Theorem 2.5 (the two foreign twists need only share a prime q, not fit a multiplier menu); and now the mixed fused-plus-foreign family at n = 273. In every case the *bound* was right and the *construction list* was missing something, which is the safer direction to err — but it means "no violations found" is weak evidence for exhaustiveness, and the GAP batteries (which enumerate Oliver groups independently of our families) are the only genuinely non-circular check currently available. At n = 10 they confirm the bound: all 967 groups have minimum orbital at most 20, the bound's value.
