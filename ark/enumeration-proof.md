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

## Part E. Completeness of the enumeration — **OPEN** (reduced to a bounded computation by Parts F–G)

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

## Part F. The search is bounded — **PROVED**

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

## Part G. Nested towers add no new shapes — **PROVED**

The one structural loose end left by Parts A–F was whether a deep imprimitive tower, interacting with foreign parts elsewhere in the partition, could escape the classification. It cannot, and the reason collapses the shape space rather than enlarging it.

**G.1 The chain descends to block stabilisers.** Let H be the setwise stabiliser of a block. Then H ∩ Γ₂ is a p-group, (H ∩ Γ₁)/(H ∩ Γ₂) embeds in the cyclic Γ₁/Γ₂ hence is cyclic, and H/(H ∩ Γ₁) embeds in the q-group Γ/Γ₁ hence is a q-group. So H — and therefore its action on the block — inherits an Oliver chain **with the same (p, q)**. The recursion of Part C is thus sound at every depth, with the primes fixed throughout.

**G.2 Every orbit is F·c with F a q-power and c a prime power.** Iterate Part B on an orbit O: each level of the tower has a block count that is a power of q (a transitive q-group has q-power degree), and the recursion terminates at the finest blocks, which are **primitive**, hence affine of prime-power degree. Writing the successive block counts b₁, …, b_t and the finest block size c,

> |O| = b₁·b₂ ⋯ b_t · c = **q^a · c**, with c a prime power.

The finest block is either p-characteristic (c a p-power, twist any divisor of c−1) or foreign, in which case Lemma B′ forces c prime with a q-power twist. **The tower depth t plays no further role: it is absorbed entirely into F = q^a.** A three-level tower and a one-level tower with the same F and c have the same orbital data.

**G.3 The general configuration, in final form.** Combining G.2 with Parts A–D, an Oliver group on n points is described by a choice of chain primes (p, q) and orbits O₁, …, O_k with

> **n = Σᵢ Fᵢ·cᵢ**, Fᵢ a q-power, cᵢ a prime power, each cᵢ p-characteristic or a foreign prime,

twists dᵢ | cᵢ−1 (a q-power when foreign), subject to Lemma C. The orbital data is
intra-orbit **Fᵢ·orb(cᵢ, dᵢ)**; within-orbit cross classes **(Fᵢ or Fᵢ/2)·cᵢ²** when Fᵢ > 1; and between-orbit classes at most **sᵢ·sⱼ**. Every family used anywhere in these notes is a special case: F = 1 with one part is the affine case, F > 1 with one part is Theorem 2.4, F = 1 with two or three parts is the two-block and three-part families, and F > 1 with foreign parts is the mixed family that the five-family list omitted.

**G.4 The search is bounded on every axis.** With δ = m\*/C(n,2): the intra-orbital satisfies Fᵢ·orb(cᵢ,dᵢ) < Fᵢcᵢ²/2 and must be at least m\*, while Fᵢcᵢ ≤ n. Hence

> **cᵢ ≥ δn**,  **Fᵢ ≤ 1/δ**,  and **k ≤ 1/√δ** (Proposition F.1).

At the weakest density below 10⁴ (0.0147) this reads c ≥ 0.0147n, F ≤ 68, k ≤ 8; at the median density, c ≥ 0.2n, F ≤ 5, k ≤ 2. Checked against every fused-form witness in the table — **3,053 of 3,053** satisfy both derived constraints, with no exceptions.

So the configuration space is finite along all three axes, with bounds computable from the density alone, and the self-certifying iteration of Part F applies unchanged. **What remains of Part E is now purely to write the enumeration of G.3 once, generally, rather than as a menu of special cases** — the failure mode that produced all four earlier corrections.

## Part H. The cost of the search, stated without number theory — **PROVED**

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

**The one term that is not bounded by anything elementary is δ itself**, and that is the whole of the dependence. Unconditionally, BBKN gives μ(n) = Ω(n log n), i.e. δ = Ω(log n / n), so the exponent 1/√δ is only bounded by **O(√(n / log n))** and the search is n^{O(√n)} — subexponential, but not polynomial. Empirically δ never drops below 0.0147 anywhere under 10⁴, giving k ≤ 8, but that is an observation about a finite range and not a theorem.

**Forward pointer.** This is where the number-theoretic conjectures re-enter, and in a role distinct from the one they play in §§4–5 of the notes. There they bound μ(n) from below; here the *same* bound bounds the **running time of the search**, because δ appears in the exponent. Under the ladder — δ ≥ 1/4 for even n, δ ≥ 0.049 for odd n with 3 ∤ n, δ ≥ 0.028 for 3 | n — the orbit count falls to k ≤ 2, 5, 6 respectively and the search becomes **polynomial of fixed degree** in n. So a Hardy–Littlewood-type hypothesis buys two things at once: the value of μ(n), and a guarantee that the certified enumeration terminates in polynomial rather than n^{O(√n)} time. That is worth stating explicitly in the number-theory sections, since it is a consequence of those conjectures that has nothing to do with what they were introduced for.

## Part I. What the general enumeration finds — **implemented** (`mu_enumerate.py`)

The G.3 enumeration is implemented with the Part F iteration and the Part G.4 pruning. It reproduces μ(10) = 20 (p = 5, q = 2, two fused blocks of 5) and μ(12) = 18 (p = 2, q = 3, three fused blocks of 4), and agrees with the construction table at all 55 non-prime-powers below 90.

Above that it diverges, always in the same direction and always by the same omitted shape — **two p-characteristic parts together with one foreign prime**:

| n | menu | general | factor | configuration |
|---|---|---|---|---|
| 255 | 2016 | 2628 | 1.30 | 73 + 73 + 109\* |
| 273 | 689 | 3403 | 4.94 | 83 + 83 + 107\* |
| 285 | 2041 | 3916 | 1.92 | 89 + 89 + 107\* |

At n = 285 the configuration is two orbits of 89 with the full diagonal twist C₈₈ and one foreign orbit of 107 with twist C₅₃; the chain is 𝔽₈₉² ◁ 𝔽₈₉² ⋊ (C₈₈ × 𝔽₁₀₇) ◁ Γ with cyclic middle since gcd(88, 107) = 1, and the orbitals are {3916, 5671, 7921, 9523}. Nothing exotic — simply a combination the hand-built menu never formed, exactly as at n = 273 with fusion and foreign parts.

Two implementation notes, both cases where the enumeration proposed inadmissible configurations before being corrected. **Foreign parts cannot be fused** (F copies of C_c inside the cyclic layer generate C_c^F, cyclic only for F = 1; diagonal translations restore cyclicity but collapse the within-orbit cross class to ≈ F·c and are always dominated). **Foreign primes must be pairwise distinct**, for the same reason applied across orbits. Both are consequences of Lemma C that the special-case menus had never had occasion to violate, and both inflate the bound if omitted.

**Methodological note, earned the hard way.** Under-enumeration has now produced three separate corrections: five violations before three-part configurations were added; Theorem 2.4 (block counts may be prime powers, not just primes); Theorem 2.5 (the two foreign twists need only share a prime q, not fit a multiplier menu); and now the mixed fused-plus-foreign family at n = 273. In every case the *bound* was right and the *construction list* was missing something, which is the safer direction to err — but it means "no violations found" is weak evidence for exhaustiveness, and the GAP batteries (which enumerate Oliver groups independently of our families) are the only genuinely non-circular check currently available. At n = 10 they confirm the bound: all 967 groups have minimum orbital at most 20, the bound's value.
