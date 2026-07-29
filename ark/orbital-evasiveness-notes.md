# The Minimum-Orbital Function μ(n): Limits and Arithmetic Content of the Group-Theoretic Approach to Sparse Evasiveness

*Working notes, July 2026. Status: an asymptotic framework with proof sketches, together with exact machine computations at n = 10 and a campaign in progress at n = 12 (code, checkpoints, and logs accompany this note). Claims marked ★ are unproven; everything else is either proved here or cited. Intended as a starting point for others.*

## Overview

**The question.** The Aanderaa–Rosenberg–Karp conjecture says every nontrivial monotone graph property is evasive: deciding it requires querying all C(n,2) pairs in the worst case. Kahn–Saks–Sturtevant reduce this to fixed-point topology — a non-evasive property has a collapsible complex, so any group action satisfying Oliver's condition forces a congruence on Euler characteristics. Whether that reduction *bites* at a given n comes down to one number.

**The invariant.** μ(n) is the largest possible minimum u-orbital of an Oliver group of degree n. Any monotone property all of whose members have fewer than μ(n) edges is evasive at n, so μ(n) measures the reach of the topological method. This note is about μ(n) from four directions.

**§§1–3, what determines μ (group theory).** Oliver's condition forces solvability, and solvable primitive groups have prime-power degree. Iterating that gives a block recursion (Theorem 2.2) and a per-orbit capacity law (Theorem 2.3), which together bound μ(n) by a purely arithmetic max–min over partitions of n into prime powers — unconditional. Lemmas A–C then derive the coherence conditions constraining which twists coexist, and a canonical enumeration of the configurations they permit — together with two construction families the enumeration itself uncovered (Theorems 2.4, 2.5) — determines μ(n) **exactly at 761 of the 806 non-prime-power n below 1000** (the residue traced to a configuration family the enumeration omitted, §2.6). The ★ conjecture the framework once rested on turns out to be substantially provable, leaving only the exhaustiveness of that enumeration (§3).

**§§4–6, what μ encodes (number theory).** BBKN's n^{3/2} bound turns out to be exactly the ceiling of a pointwise least-prime oracle (§4); beyond it, μ is governed by binary-Goldbach-type statements with multiplicative side conditions on shifted primes, parity-split and locally delicate (§5). Granting the extremal claim, this is an equivalence: μ encodes the Hardy–Littlewood stratum and nothing finer (§6). The safe-prime hypothesis that the ladder's top rung assumes is not an assumption — Lemma B derives it.

**§7, where each test sits.** Before the computations, a metaproperty ladder — trivial ⟹ non-evasive ⟹ collapsible ⟹ contractible ⟹ ℤ-acyclic ⟹ 𝔽_p-acyclic ⟹ χ = 1 — with the group-dependent tests hung off the weakest rung each needs, and the *particular versus all* distinctions (one prime or every prime; one group and one (p,q) or the whole battery; one modulus or χ = 1) made explicit. Two things fall out: at some n a **single** 𝔽_p-acyclicity is contradicted rather than the conjunction, and since Oliver's congruence is tight at each fixed group, the only places left to gain are more groups, the restriction to Δ_P complexes, or working above the acyclicity level at all.

**§8, exact computation.** Flipping the method at n = 10: a machine-checked CSP over batteries of Oliver groups and Smith p-subgroups, primal and dual, with exact Euler characteristics. Nine candidate patterns die outright; the rest survive, and understanding *why* they survive is the most useful output — the topological method is structurally one-sided, every constraint pushing graphs into P and only nontriviality pushing one out. The campaign has moved to n = 12.

**§9, why.** A three-state shape calculus explains the one-sidedness: monotonicity deletes one state from the pattern alphabet, so a monotone property can never exhibit the two-sided don't-care region that makes the scorpion fast. It also identifies monotone shape complexity 1 as precisely the forbidden-subgraph class BBKN leave open.

**Where the pieces stand.** §10 assesses; §11 lists the open problems, of which two are sharp and finite (proving the configuration enumeration of §2.6 exhaustive; an exhaustive single-shape search at n = 6) and the rest are genuinely hard.

**In one paragraph.** Abstracting BBKN, sparse evasiveness via orbital annihilation is governed by μ(n), conjecturally equivalent (modulo the wreath-inclusive extremality claim ★ about solvable permutation groups) to a graded family of additive prime-representation statements: BBKN's n^{3/2} is precisely the Chowla-saturated ceiling of pointwise least-prime inputs; exponents in (3/2, 2] are equivalent to binary-Goldbach-type statements with multiplicative side conditions on shifted primes — parity-cased and locally delicate — even n via a two-block safe-prime system, odd n via a covering system of three-block chains ((4,6) for 3∤n, (6,12) for 3|n; the (2,4) chain is mod-3-impossible and (2,6) fails locally at 3|n), whose constant is capped in closed form at δ = 2a/(a+b+√(2a))² ≤ 0.0486 — positive, explicit, and about a fifth of the even-n 1/4, and n = 2·(prime power) determined exactly at n(n−2)/4 by Theorem 2.1 — and, per §5.4, unconditional at every representation-admitting n with the conjectures asserting only finiteness of exceptions, ineffectively; and the method terminally caps at density 1/2 relative to C(n,2) by Zassenhaus, independent of number theory. At n = 10 the flipped, exact version of the method — a machine-checked CSP over batteries of Oliver groups and Smith p-subgroups, primal and dual, with exact Euler characteristics of candidate closures — has killed nine of eighteen candidate patterns outright, characterized the survivors' free middle band, exposed the method's structural one-sidedness (all forces push into P; only nontriviality pushes out), and, on a 75-group GAP-enumerated battery, produced a SAT skeleton that the global χ test then killed outright — while also establishing that no catalog-side work can settle a fixed n, since a CSP solution constrains 1,242 of 12,005,168 classes and therefore does not determine a property. The campaign has accordingly moved to n = 12, the first arithmetically weak composite and, independently, the first n at which the known non-monotone mechanism has room to beat brute force. A three-state shape calculus (§9) reorganizes the surrounding facts: monotonicity is exactly the deletion of one state from the pattern alphabet, so a monotone property's shape complexity equals its generator count and can never exhibit the scorpion's two-sided don't-care region; monotone shape complexity 1 is precisely the forbidden-subgraph class BBKN leave open; certificate counting permits monotone savings of order n, so the obstruction is topological rather than certificate-theoretic; and the question of how small a single-shape construction can be is exhaustively decidable at n = 6 over 25,506 shapes.

## 1. Background: ARK, KSS, and the reduction to μ(n)

Babai–Banerjee–Kulkarni–Naik (BBKN, arXiv:1001.4829) prove evasiveness of sparse monotone graph properties via the Kahn–Saks–Sturtevant (KSS) topological method: find Γ ≤ Sym([n]) satisfying **Oliver's condition** (Γ₂ ◁ Γ₁ ◁ Γ with Γ₂ a p-group, Γ₁/Γ₂ cyclic, Γ/Γ₁ a q-group) such that every orbit of Γ on unordered pairs ("u-orbital") exceeds the property's maximum edge count. Any invariant graph in the property is then empty, the fixed-point complex is {∅} with χ = 0 ≢ 1 mod q, contradicting Oliver's fixed-point theorem plus the KSS contractibility lemma.

> **Definition.** μ(n) := max { m\*(Γ) : Γ ≤ Sym([n]) satisfies Oliver's condition }, where m\*(Γ) is Γ's minimum u-orbital size.

> **Meta-theorem (implicit in BBKN).** If nontrivial monotone P holds only for graphs with < μ(n) edges, P is evasive at n; hence f = o(μ) ⟹ f-sparse properties eventually evasive.

Throughout, **densities are relative to C(n,2)**, the total number of pairs. Two normalisations bound the whole subject: μ(n) = C(n,2) exactly when n is a prime power (AGL(1,n) is 2-transitive and Oliver), while for every non-prime-power n an Oliver group has at least two u-orbitals, so

> **μ(n) ≤ ⌊C(n,2)/2⌋ — density at most 1/2 — for all non-prime-power n**, and this is attained in the limit on n = 2·(prime power) by Theorem 2.1.

BBKN: μ(n) = Ω(n log n) unconditionally (Vinogradov/Haselgrove), Ω(n^{5/4−ε}) under ERH — made unconditional by Shparlinski (TCS 2015) via average-type results on linear equations in primes — and Ω(n^{3/2−ε}) under Chowla.

**Questions addressed.** (1) Is n^{3/2} intrinsic to μ or to proof technique? (2) How far does μ reach under believed conjectures, and where does the method terminally cap? (3) Does large μ(n) conversely imply number-theoretic statements? Answers: (1) technique — 3/2 is the provable/conjectural boundary, not a group-theoretic ceiling; (2) exponent 2 with explicit constants (parity-dependent; see §5), terminally capped at density 1/2 relative to C(n,2), c\* < 1/2, by group theory (Zassenhaus) rather than number theory; (3) yes — conjecturally μ(n) ≥ n^{1+θ−o(1)} is equivalent to a θ-graded family of binary-Goldbach-type statements with multiplicative side conditions on shifted primes.

### Part I — What determines μ: the group theory

*The reach of the topological method at a given n is a group-theoretic quantity before it is anything else. This part determines it as far as it currently can be determined, and isolates what is left.*

## 2. The group theory of μ: block structure, capacity, coherence

Everything the topological method can do at a given n is bounded by μ(n), and μ(n) is decided by which Oliver groups exist on n points. This section determines it as far as it currently can be: two ceilings, a block recursion, a capacity law, and the coherence conditions that say which twists can coexist. The results here are unconditional; §3 states what is still assumed.

μ(n) = C(n,2) requires orbital-transitivity, essentially sharply 2-transitive structure, existing only on prime-power domains (Zassenhaus). For every other n there are at least two u-orbitals, so **μ(n) ≤ ⌊C(n,2)/2⌋: density at most 1/2**. That ceiling is sharp in the limit — the n = 2·(prime power) family attains density (m−1)/(2m−1) → 1/2 by Theorem 2.1 — so no general improvement below 1/2 is possible, and the interesting question is which n fall short of it. Refining that is what Theorems 2.2–2.3 do, and the single-top-prime coherence of §2.4 is what taxes all but the wreath-fused blocks.

> **Theorem 2.1 (exact values on n = 2·(odd prime power)).** For every odd prime power m ≥ 3, with n = 2m,

> **μ(n) = m(m−1) = n(n−2)/4.**
>
> *Lower bound.* Γ = 𝔽_m² ⋊ (C_{m−1} × C₂) where the translations act independently on the two blocks, C_{m−1} = 𝔽_m^* acts by the **same** multiplicative twist on both, and C₂ swaps them. Oliver chain 𝔽_m² ◁ 𝔽_m² ⋊ C_{m−1} ◁ Γ — elementary abelian p-group, cyclic quotient, 2-group on top. Its orbitals are exactly two: the intra-block class of size 2·C(m,2) = m(m−1) (the full twist makes all within-block differences equivalent, and the swap fuses the two blocks) and the cross class of size m². Verified by orbit computation at m = 3, 5, 7, 9, 11, 13, 25, 27.
>
> *Upper bound (counting; due to VN).* If Γ is transitive on n points then each u-orbital Ω has a common valency d (every vertex lies in d pairs of Ω), so 2|Ω| = n·d, i.e. **|Ω| = n·d/2 with Σ_i d_i = n−1** over the t orbitals. Hence min_i d_i ≤ ⌊(n−1)/t⌋. For n = 2m: t = 2 gives m\* ≤ m·(m−1); t ≥ 3 gives m\* ≤ m⌊(2m−1)/3⌋ < m(m−1) for m ≥ 3. If Γ is intransitive, its smallest orbit has size s ≤ m, and if s ≥ 2 the pairs inside it are covered by orbitals of total size C(s,2) ≤ C(m,2) = m(m−1)/2; if s = 1 the pairs joining that fixed point to the largest orbit form orbitals of total size ≤ n−1 = 2m−1 < m(m−1). Finally t = 1 means orbital-transitivity, hence 2-homogeneity, hence (n even) 2-transitivity; Oliver's condition forces Γ solvable and a solvable 2-transitive group has prime-power degree (Zassenhaus, Huppert), while 2m is not one — this single step is where solvability is needed, the rest of the argument being pure counting. ∎

> **Theorem 2.2 (block recursion; 177 exact values below n = 1000).** Let n be a non-prime-power and p₁ its least prime factor. Then

> **μ(n) ≤ max( n(n/p₁ − 1)/2 , n(n−2)/8 )**,
> and equality with the first term holds — so μ(n) is *determined* — whenever n = p₁·m with m a prime power and p₁ ∈ {2, 3}.
>
> *Proof of the bound.* Oliver's condition makes Γ solvable (p-group by cyclic by q-group). A solvable **primitive** group has prime-power degree (affine type), so for non-prime-power n a transitive Γ is imprimitive; taking a coarsest block system, the induced action on blocks is primitive solvable, hence the number of blocks b is a prime power dividing n, with blocks of size c = n/b. Inside a block the intra-block orbital valencies sum to c−1 (orbit–stabilizer applied to the block stabilizer acting on the block), so some orbital has valency ≤ c−1 and hence size ≤ n(c−1)/2; the weakest such bound over admissible b is at b = p₁. If instead Γ is intransitive with ≥ 2 orbits, its smallest orbit has size s ≤ n/2 and the pairs inside it are covered by orbitals of total size C(s,2) ≤ n(n−2)/8. *Matching construction:* 𝔽_m^k ⋊ (C_{m−1} diagonal × C_k rotation) on n = km has minimum orbital k·m(m−1)/2 = n(n/k − 1)/2 (Oliver chain: 𝔽_m^k, cyclic C_{m−1}, top C_k). For k = p₁ ∈ {2,3} the transitive branch dominates the intransitive one and the two meet. ∎
>
> Theorem 2.1 is the case p₁ = 2; Theorem 2.3 subsumes and sharpens this bound.

> **Theorem 2.3 (per-orbit capacities; the arithmetic upper bound).** Define the *valency capacity* V of a degree by the recursion

> **V(c) = c − 1 if c is a prime power; otherwise V(c) = max over prime-power divisors b > 1 of c of V(c/b),**
> and set **cap(s) = s·V(s)/2**.
> Then for every Oliver Γ on n points, decomposing n into orbit sizes,

> **μ(n) ≤ max over partitions n = s₁+…+s_k (parts ≥ 2, k ≥ 1) of min( minᵢ cap(sᵢ), min_{i<j} sᵢsⱼ )**,
> the k = 1 term being Theorem 2.2's transitive bound.
>
> *Proof.* Pairs inside an orbit stay inside it, so the intra-orbital structure of O is that of the transitive solvable group Γ|_O of degree s. If s is a prime power, a single orbital can cover all C(s,2) pairs (2-homogeneity, achieved by AGL(1,s)), giving V(s) = s−1. If not, Γ|_O is imprimitive; taking a coarsest block system, the block action is primitive solvable, so the number of blocks b is a prime power dividing s, blocks have size s/b, and — this is the recursive step — the intra-block valencies are exactly the suborbit sizes of the block stabilizer acting on its block, a transitive solvable group of degree s/b, whose minimum is at most V(s/b). Maximizing over the admissible b gives the recursion. Cross-orbitals between O_i and O_j lie among the sᵢsⱼ pairs between them. Taking the minimum over all orbitals and the maximum over orbit partitions gives the bound; partitions into ≥ 3 parts never beat the best 2-part split, since more parts only shrink minᵢ cap(sᵢ). ∎
>
> *Recursion in action:* V(19) = 18 (prime), V(475) = 24, V(1425) = 24, V(35) = 6, V(26) = 12. The recursion matters: the non-recursive reading (one block step only) would give cap(1425) = 337,725 against the true 17,100.
>
> This is a **purely arithmetic, unconditional** upper bound: a max–min over partitions of n into prime powers, with each part's capacity given by a divisor recursion. Verified with **zero violations** over all **8,719 non-prime-power n ≤ 10⁴**, and **met at 2,318 of them (26.6%)** — 1,493 where the transitive/block branch binds and 825 where a partition does. Example: **μ(35) = 120** via 35 = 16 + 19 and Γ = AGL(1,16) × (𝔽₁₉ ⋊ C₉), beating the transitive ceiling of 105. Shapes of the exact set: 699 of the form 2·(prime power), 489 of the form 3·(prime power), 1,130 others. The exact fraction *declines* with n — 42.7% below 10³, 33.2% below 3·10³, 26.6% below 10⁴ — mirroring the odd-n thinning of §5.5.

**What the residual gap is, exactly.** Over the 6,401 still-gapped n ≤ 10⁴ the median ratio construction/bound is 0.533, worst cases being the familiar weak odd n (n = 1425: 10,025 against 171,991, ratio 0.058; then 4245, 3393, 5457, 4059). The cause is identifiable rather than mysterious: the bound grants *every* part its full capacity C(sᵢ,2), but full capacity requires the full multiplicative twist C_{sᵢ−1}, and an Oliver chain has only **one cyclic middle layer** — so C_{a−1} × C_{b−1} must itself be cyclic, forcing gcd(a−1, b−1) = 1, with any further twists confined to a single top q-group. **That gcd-and-q-coherence condition is precisely what converts the max–min over partitions into the Hardy–Littlewood systems of §5.** So the framework now divides cleanly: *partition and block structure, and per-orbit capacity, are theorems; which twists are simultaneously realizable across parts is the sole conjectural ingredient*, and it is exactly the ingredient that carries the number theory.

**2.6 The canonical enumeration, and the block-fusion family it uncovered.** Lemmas A–C cut the configuration space down to something finite and explicitly listable, and doing so carefully removes the ambiguity that a naive implementation suffers (max–min and min–max differ, so the *order* of optimisation must be pinned down). Two observations make the enumeration canonical.

*Twists may always be taken maximal.* The value of a configuration is a **minimum** of terms — one per orbital — and each term is non-decreasing in its own twist order. So the optimum is attained with every twist as large as the coherence conditions allow, and no inner search is needed: for a p-part of size a the twist is the largest divisor of a−1 coprime to the foreign parts (Lemma C), and for a foreign prime r it is the q-part of r−1 (Lemma B′).

*The block recursion must respect the single top prime.* A transitive q-group has q-power degree, so a block system usable by the chain has a number of blocks that is a **power of q**. Writing V(s; p, q) for the valency capacity of an orbit of size s under chain primes (p,q): V = s−1 if s is a power of p; V = t or 2t (t the q-part of s−1) if s is a prime other than p; and otherwise V(s; p,q) = max over q-power divisors b > 1 of s of V(s/b; p,q). Allowing arbitrary block counts here — maximising the twist prime independently at each level — is exactly the leak that made earlier implementations disagree.

With those two fixes the bound is a single well-defined max–min over configurations: (i) k identical p-power blocks fused by a transitive q-group; (ii) two p-power parts of the same characteristic; (iii) a p-power part plus one foreign prime; (iv) a p-power part plus two foreign primes sharing one q; (v) the transitive/block-recursion fallback. Verified with **zero violations** over all 806 non-prime-power n ≤ 1000.

*The family this uncovered.* Comparing bound against construction left one conspicuous gap — at n = 531 the bound gave 15,399 against a construction of 2,124 — and the culprit was a missing family, not a loose bound. Since a transitive q-group has q-power degree, **the number of fused blocks may be any prime power, not merely a prime**:

> **Theorem 2.4 (block fusion at prime-power block counts).** Let n = k·m with **k a prime power** and **m a prime power**, m ≥ 2. Then Γ = 𝔽_m^k ⋊ (C_{m−1} diagonal × T), with T a transitive q-group on the k blocks (q the prime dividing k), is an Oliver group whose minimum orbital is **k·C(m,2) = n(m−1)/2**; hence μ(n) ≥ n(m−1)/2. Combined with Theorem 2.2's upper bound this is an equality whenever the block branch dominates.

Verified by orbit computation at n = 12, 20, 28, 44, 45, 56, 117 — for example n = 20 = 4·5 gives orbital sizes {40, 50, 50, 50} and n = 28 = 4·7 gives {84, 98, 98, 98}. Theorems 2.1 and 2.2 are the special cases k = 2 and k prime.

*Effect.* The new family raises μ_lower at **90 of the 806** non-prime-power n below 1000 (and supplies the winning witness at 3,053 of the 8,719 below 10⁴), including both values Appendix A had left open, giving **μ(20) = 40** and **μ(28) = 84**; the canonical bound was then met at 791 of 806.

*And one more, found the same way.* Diagnosing the fifteen survivors showed every one of them achieved by a three-part configuration that the constructions were not attempting. The chain family of §5 imposes the rigid shape m + (aq+1) + (bq+1) with (a,b) drawn from a small multiplier menu, but Lemmas B′ and C ask for nothing of the kind: the two foreign blocks need only be **primes whose twists are powers of a common q**, with the p-block twist coprime to both.

> **Theorem 2.5 (unrestricted three-part family).** Let n = m + r + s with m a prime power and r ≠ s primes, let q be a prime dividing both r−1 and s−1, and let d be the largest divisor of m−1 coprime to rs. Then there is an Oliver group with chain 𝔽_m ◁ 𝔽_m ⋊ (C_d × 𝔽_r × 𝔽_s) ◁ Γ, top layer the q-group of twists, and minimum orbital min(orb(m,d), orb(r, q-part of r−1), orb(s, q-part of s−1), mr, ms, rs).

Example at n = 693: the configuration 151 + 163 + 379 with q = 3 carries twists 150, 81 and 27 — two *different* powers of 3, which no fixed multiplier pair produces — and yields 10,233 against the chain family's 3,916. Adding this family closes **all fifteen** remaining values below 1000 and changes nothing else in that range; across n ≤ 10⁴ it supplies the winning witness at 1,198 values. Between them Theorems 2.4 and 2.5 account for the best construction at **4,251 of the 8,719** non-prime-powers below 10⁴ — very nearly half the table.

*Result, and a subsequent correction.* On the five families listed above the canonical bound was met at every non-prime-power n below 1000. That claim does **not** survive: probing a wider configuration class found a sixth family the list omitted — **F fused blocks together with foreign primes**, which the five families expressed only in isolation (fused-only, or F = 1 with foreign parts). The witness is n = 273 = 16·11 + 97, where F = 16 fused blocks of 11 with diagonal twist 10 and one foreign prime 97 with twist 32 give orbital sizes {880, 968, 1552, 17072} and hence m\* = 880, against 689 from the five families. Sweeping the mixed shape over n ≤ 1000 improves **45 values**, median 1.54× and up to 4.05× (n = 651: 8,128 → 32,896), always at q = 2 and almost always with a foreign prime whose predecessor is a large power of 2 — 257 = 2⁸ + 1 accounts for 33 of the 45, its full twist C₂₅₆ giving the binding orbital 257·128 = 32,896.

Since the bound was computed from the same five families, it was too small at those 45 values as well, so **exactness holds at 761 of the 806 rather than all of them**, and both sides must be recomputed with the mixed family before a figure is quoted again. See `enumeration-proof.md` for the general configuration shape and the current status of each part of the argument.

*The progression across this section, on the five-family enumeration: Theorem 2.3 alone 42.7%; ad hoc coherence refinements 69–71%, with an ambiguity between implementations; the canonical enumeration 87.0%; plus Theorem 2.4, 98.1%; plus Theorem 2.5, 100% — reduced to 94.4% by the omission just described.

*Evidence for the enumeration, and what it does not cover.* Running the bound against the constructions to 10⁴: **zero violations** and the bound **met at every one of 1,182 tested values** (all 1,062 non-prime-powers below 1300, plus 120 sampled between 1300 and 10⁴). Two different things are being tested here and they should not be conflated.

The 100% agreement is genuine evidence of *tightness from below*: every configuration the enumeration permits is realised by an explicit group, so Lemmas A–C admit no phantom configurations. That is not circular, and it is the property one would expect to fail first if the coherence conditions were merely necessary rather than characteristic.

But the same comparison is **blind to exhaustiveness from above** — a missing family would show up as a violation only if the constructions implemented it, which by hypothesis they do not. For that one needs Oliver groups from an independent source, and the GAP batteries of §8 supply them: at n = 10 they enumerate **all 967** Oliver groups with at most twelve orbitals, and the largest minimum orbital over all of them is **20**, exactly the bound, attained by T(10,17) of order 200 with orbital sizes {20, 25}. No enumerated group exceeds the bound. That is a real if narrow exhaustiveness check, and extending it to the 8,819 groups at n = 12 is the cheapest available strengthening.

*The remaining assumption, stated plainly.* The lower bounds are unconditional — each is an explicit group. The matching upper bound is Theorem 2.3 refined by Lemmas B′ and C, and adding necessary conditions can only shrink the feasible set, so the refined bound is valid **provided the enumeration covers every configuration those lemmas permit**. Under-enumeration is a demonstrated hazard, not a theoretical one, and it has now bitten four times: five violations before three-part configurations were admitted; Theorem 2.4 (block counts may be prime powers, not merely primes); Theorem 2.5 (the two foreign twists need only share a prime q); and the mixed fused-plus-foreign family above, which cost 45 values below 1000. In every instance the *bound* was correct and the *construction list* was short — the safe direction to err, but it means "no violations found" is weak evidence for exhaustiveness.

The general configuration that repairs the list, and the four points still not established — several fusion classes of different sizes, nested towers meeting foreign parts, four or more foreign parts, and a domination argument reducing every permitted configuration to a finite list — are set out in the companion document `enumeration-proof.md`, which also records the status of each ingredient: Parts A–D (orbit reduction, per-orbit classification, the valency recursion, coherence) are proved, with the Singer step of Part B a sketch; Part E, completeness, is open. The only genuinely non-circular evidence available is the GAP batteries, which enumerate Oliver groups independently of our families: at n = 10 all 967 have minimum orbital at most 20, exactly the bound.

**2.4 The coherence conditions are derivable.** Theorem 2.3's gap is the assumption-free bound's failure to know that only certain twists coexist. That knowledge is not extra hypothesis — it follows from the chain.

> **Lemma A (inheritance).** For each Γ-orbit O the induced group Γ|_O inherits an Oliver chain with the *same* bottom prime p and top prime q, namely the images of Γ₂ ◁ Γ₁ ◁ Γ.
>

> **Lemma B (foreign orbits).** Let O have full capacity — Γ|_O is 2-homogeneous, hence primitive affine of degree s = p₀^a — and suppose p₀ ≠ p. Then π_O(Γ₂) is a normal p-subgroup of a primitive group; a nontrivial normal subgroup of a primitive group is transitive, which would force p = p₀, so π_O(Γ₂) = 1. Hence π_O(Γ₁) is cyclic and normal, so it contains the socle 𝔽_s, forcing **a = 1**; being cyclic it centralises the socle, and the centraliser of the socle in AGL(1,s) is the socle itself, so π_O(Γ₁) = 𝔽_s and the entire twist lies in Γ/Γ₁, a q-group. Since 2-homogeneity on s points requires a twist of order s−1 or (s−1)/2:

> **an orbit of foreign characteristic attains full capacity only if s is prime with s − 1 ∈ {qᵉ, 2qᵉ}.**
>

> **Lemma C (the cyclic layer).** Full twists of p-blocks on distinct blocks, and translations of foreign prime blocks, all lie in Γ₁/Γ₂ and act on disjoint supports; they therefore generate a direct product, which must be cyclic. Hence their orders are pairwise coprime — in particular **gcd(m−1, r) = 1** between a p-block of size m and a foreign block of size r. (Twists acting *diagonally* on several p-blocks are not independent and carry no coprimality condition — this is what Theorem 2.1's construction exploits.)

These are exactly the conditions §5 imposes on its ladder, now derived rather than assumed. Lemma B is the origin of the safe-prime hypothesis: the top rung wants a foreign block of prime size r with a twist of order ∼r/2, and Lemma B says the twist must be a q-power, so r − 1 ∈ {qᵉ, 2qᵉ} — with e = 1 in the 2qᵉ case being precisely "r is a safe prime." Verified against every two-block witness in `mu_table_full.csv`: of 5,025 such rows, the 3,316 whose foreign block attains full capacity satisfy Lemma B **without exception** (3,302 of shape 2qᵉ, 14 of shape qᵉ), and Lemma C's gcd condition holds in all 5,025. Lemma B also predicts the density split measured in §5.5: among rows clearing the 1/12 diagnostic threshold, 73.1% have r − 1 ∈ {qᵉ, 2qᵉ}; among those below, 9.9%.

**2.5 Strengthening, validation, and the state of the refined bound.**

*Lemma B′.* The proof of Lemma B never uses 2-homogeneity — only that Γ|_O is **primitive**. So the conclusion is wider: **any orbit of foreign characteristic on which Γ acts primitively has prime size s, with its twist group a q-group** (order a power of q dividing s−1). Consequently its capacity is not C(s,2) but s·t/2 for t even, s·t for t odd, where t is the q-part of s−1 — which is exactly the `block_intra` quantity of the constructions in §5. Full capacity is the special case t ∈ {s−1, (s−1)/2}, recovering Lemma B.

*Independent validation.* The earlier check of Lemmas B–C was against our own constructions, so it could only confirm consistency. The GAP battery at n = 10 gives an independent test, since those 967 Oliver groups were enumerated exhaustively with no reference to the lemmas. Extracting vertex orbits by colour refinement and locating orbitals that induce a complete graph on their support: **1,061 full-capacity orbits across 728 groups, of sizes 2, 3, 4, 5, 7, 8, 9 — every one a prime power, with no exceptions**; **no group** has two proper-prime-power full-capacity orbits of different primes (confirming the uniqueness of p); and of the 88 prime-sized full-capacity orbits inside groups with a genuine top prime q, **all 88** satisfy s − 1 ∈ {qᵉ, 2qᵉ}.

*Effect on the bound.* Restoring the coherence conditions inside Theorem 2.3 tightens it substantially: carrying the bottom prime through the capacity recursion, so that only p-power orbits receive C(s,2) and foreign primitive orbits receive the q-power-twist value of Lemma B′, raises the fraction of n at which the bound is met from 42.7% to about 70%. Making the enumeration canonical (§2.6) and adding the two families it uncovered takes that to **100% of non-prime-power n below 1000**. The earlier ambiguity — two faithful-looking implementations disagreeing at 71.0% versus 68.9% — was caused by leaving the optimisation order unpinned and by a block recursion that ignored the single top prime; §2.6 resolves both.

**Consequence for ★.** With Lemmas A–C the remaining half of ★ is no longer a classification problem about solvable permutation groups but a *finite arithmetic optimisation*: enumerate the orbit partitions and twist assignments permitted by A–C, and maximise the minimum orbital. Theorem 2.3's bound is that optimisation with the coherence constraints dropped; restoring them should close most of the residual gap. Lemma B′ of §2.5 covers partial-capacity primitive orbits as well; what is left is a canonical, provably exhaustive enumeration of the permitted configurations, and the analogue of Lemma C inside nested imprimitive towers (Open Problem 9).

**Why the method stalls at p₁ = 3, and the route past it.** For k ≥ 5 the intransitive branch n(n−2)/8 overtakes the transitive one (at n = 35: 144 versus 105), so exactness is lost — a weakness of the *estimate*, not of the construction. Equality in C(n/2,2) demands two orbits of size exactly n/2 with the group 2-homogeneous on each half, which forces **n/2 to be a prime power**; so the suborbit refinement (each suborbit size divides the point-stabilizer order, and the sizes sum to s−1) should kill the intransitive branch whenever n/2 is not a prime power, extending exactness to p₁ = 5, 7, …. This is the natural next increment and is recorded as Open Problem 9.

**Status of ★.** The recursive *shape* asserted by ★ is proved rather than assumed (and §2.4 derives the coherence conditions too): non-prime-power degree forces a block system, the block system forces the ceiling n(c−1)/2, and that ceiling is keyed to the divisor lattice of n. What ★ still carries is the finer claim about which twists are *simultaneously* available across blocks — the q-coherence that drives the number theory of §5. So: **block recursion, theorem; coherence conditions for full-capacity orbits, theorem (§2.4); their extension to partial-capacity and nested configurations, open.**

Two consequences. The general even-n form of the counting bound is **μ(n) ≤ n(n−2)/4 for even non-prime-power n**, improving the ⌊C(n,2)/2⌋ = ⌊n(n−1)/4⌋ ceiling above by n/4; for odd n the t = 2 bound degenerates to the old ceiling. And exact values follow immediately where they were previously only bracketed: **μ(22) = 110**, μ(6) = 6, μ(10) = 20, μ(14) = 42, μ(18) = 72, μ(26) = 156, all exact.

*Implementation note.* The construction above is easy to miss in code: a diagonal-plus-rotation family that requires gcd(d, k) = 1 excludes it, since the rotation belongs in the top q-group rather than the cyclic middle layer and any d | m−1 is admissible. For k = 2 that spurious condition always rules out the full (even) twist d = m−1 — exactly the optimum. `mu_fast.py` had this bug; fixing it raised 103 of 999 rows up to n = 1000, median ratio 2.0 (n = 26: 78 → 156; n = 50: 300 → 600; n = 75: 301 → 900).

Beyond density 1/2, dense properties intrinsically require levers whose limiting resource is not prime distribution: recursion to quotient properties on fixed complexes (CKS-style), or finer topological invariants — for whose limits see §8.6–7.7.

## 3. The extremal claim ★, and how much of it survives

§2 proves the *shape* of the extremal groups — that non-prime-power degree forces blocks, that capacity obeys a divisor recursion, and that coherence constrains the twists. Historically the framework rested instead on the following claim, which is stated here for the record together with an assessment of what is still assumed.

> **Claim 3.1 (extremal form) ★.** If Γ satisfies Oliver's condition with m\*(Γ) > n^{3/2+ε}, then up to subgroup/quotient preserving the bound, Γ is assembled from affine blocks over a partition of n into prime powers: a bottom layer of p^α-blocks (single prime p) with multiplicative twists, distinct-prime middle blocks 𝔽_{r_j} with q-power twists for a single top prime q, one general cyclic twist available via the middle layer — **and, when q-power block permutations are available, wreath-type tops**: the top q-group may permute isomorphic blocks *and* carry their twists simultaneously (e.g. AGL(1,p) ≀ C₂ with top 2-group C₄ ≀ C₂). Each block has size ≥ √(2m\*) — in particular **no bounded blocks and no fixed points** in any configuration with m\* = ω(n), since a block B contributes cross-orbitals of size O(|B|·n).

The wreath clause is what machine enumeration (§8.8) forces: block-swaps need not live in the cyclic middle layer, so the natural-looking gcd conditions between swap and twist are illusory. The witness is AGL(1,5)≀C₂ at n = 10, which fuses the two intra-block orbitals to reach m\* = 20 where a swap-in-the-middle template manages only 10. Two consequences: (i) for n = 2p with p prime, μ(n) ≥ p(p−1) ∼ n²/4 **with no number-theoretic hypothesis at all** (given the form of n) — sharpened to an equality in §2; (ii) any case analysis behind the extremal constants of §2, and the exact reduction of μ to representation functions (Cor. 3.2), must range over the enlarged template. The unproven core (★) — ruling out imprimitive solvable towers that beat affine-wreath forms at intermediate exponents — is substantially reduced by §2's Theorems 2.2–2.3, which prove the block structure and leave only the twist-coherence half.

> **Corollary 3.2 (shape unchanged).** For 3/2 < 1+θ ≤ 2: μ(n) ≥ n^{1+θ−o(1)} iff n admits a decomposition into O(1) prime-power blocks each ≥ n^{3/4}, with q-coherent twist/wreath structure supplying per-block orbital factors ≥ n^{1+θ}/(block size).

**How much of Claim 3.1 is now proved.** Substantially all of its structural content, as follows.

- *Decomposition into prime-power pieces.* Oliver's condition makes Γ solvable; a solvable **primitive** group is affine of prime-power degree; so each orbit is either primitive-affine or imprimitive with a block system whose block count is a q-power (Theorem 2.2), and the recursion terminates at primitive prime-power pieces (Theorem 2.3, Lemma A). Foreign-characteristic primitive orbits are prime with q-power twists (Lemma B′), and the cyclic layer forces the coprimality of Lemma C. The block-size floor is the elementary cross-orbital count already given.
- *Affine of prime-power degree ⟹ affine **line**.* This is the step the claim needed and §2 did not supply, and Oliver's condition settles it. Write a primitive affine orbit as 𝔽_p^a ⋊ H with H ≤ GL(a,p) irreducible. H inherits the chain, so it is p-by-cyclic-by-q; but its normal p-subgroup is unipotent, and a normal unipotent subgroup of an irreducible group has a nonzero invariant fixed space, so it is trivial and **H is cyclic-by-q**. Let C ◁ H be the cyclic normal subgroup. If C is irreducible then 𝔽_p[C] is a division algebra by Schur, hence a field by Wedderburn, so V is one-dimensional over it and **C lies in a Singer cycle 𝔽_{p^a}^\***, whence H ≤ N_{GL}(C) = **ΓL(1,p^a)** — exactly the affine-line form the capacity formulas assume. If C is reducible, V splits into C-isotypic components permuted by the q-group H/C, so their number is a q-power and the configuration is imprimitive, returning to the recursion. Field automorphisms do not disturb the capacities: with a full multiplicative twist the intra-orbital is already all of C(s,2), and foreign orbits have a = 1.

**What therefore remains open** is narrower than Claim 3.1 as stated: not a classification of solvable permutation groups, but the **exhaustiveness of the configuration enumeration** of §2.6 — whether the five families listed there cover every arrangement Lemmas A–C permit, the untested cases being partitions into four or more parts and nested towers mixing characteristics. That is finite bookkeeping over a constrained space rather than a structural conjecture, and it is the sole assumption behind the claim that μ is determined exactly below 1000. The argument above is a sketch assembled here and deserves a careful independent reading before Claim 3.1 is retired outright.

### Part II — What μ encodes: the number theory

*Granting the extremal claim of §3, μ is not merely bounded by arithmetic but equivalent to it. This part locates the barrier that stops the unconditional bounds, climbs the conditional ladder above it, and states the converse.*

## 4. The provability barrier at exponent 3/2

Turning from what determines μ to what μ encodes. BBKN's unconditional and ERH-conditional bounds stop at exponent 3/2, and the reason is not a limitation of effort: 3/2 is exactly the ceiling of the proof architecture they use.

The BBKN/Shparlinski architecture fixes moduli first and invokes a least-prime oracle: with joint modulus D ≥ p^α q controlling r mod p^α and r ≡ 1 mod q, any oracle whatsoever satisfies r ≥ D, forcing m\* ≤ min{n·p^α, qr} ≤ n^{3/2+o(1)} at the balance p^α ∼ √n; Chowla is the optimal oracle hypothesis and exactly saturates it. Exceeding 3/2 requires pinning r = n − m exactly while demanding primality plus a multiplicative side condition on r − 1 — a thin binary problem in the class of binary Goldbach, outside the implication range of ERH/GRH/Elliott–Halberstam and structurally inaccessible to sieves (parity problem + thin set). The barrier is epistemic, not ontological.

## 5. The conditional ladder, and what it costs

Above the barrier, μ is governed by binary-Goldbach-type statements. The ladder below climbs from exponent 3/2 to the density-1/2 ceiling; its rungs are parity-split, its constants are computable in closed form, and — per §2.4 — its arithmetic side conditions are consequences of the Oliver chain rather than modelling choices.

**Even n: two-block rungs.** n = m + r, both prime; Γ = AGL(1,m) × (𝔽_r ⋊ C_{q^e}), q^e | r − 1, Oliver chain 𝔽_m ◁ 𝔽_m ⋊ (C_{m−1} × 𝔽_r) ◁ Γ. With q^e ∼ r^θ, m ∼ r^{(1+θ)/2}: μ(n) ≥ n^{1+θ−o(1)} conditional on the θ-side-condition Goldbach statement. Top rung θ = 1 via safe primes r = 2q+1: assuming every large even n = m + 2q + 1 with m, q, 2q+1 prime (Hardy–Littlewood two-variable system, ∼ c·n/log³n representations). Balancing the blocks, m ≈ r ≈ n/2: the m-block carries a full twist so its orbital is C(m,2) ≈ n²/8, the r-block's twist has order q ≈ r/2 (odd, so −1 is outside it) giving r·q ≈ n²/8, and the cross orbital is m·r ≈ n²/4. Hence

> **δ₀^{even} = 1/4** (density relative to C(n,2); equivalently μ ≥ n²/8).

Confirmed by the table: over 5,025 rows whose best witness is this two-block family the maximum density attained is **0.2499**.

**Odd n: the two-block template is parity-blocked, and any fix must keep every block large.** Two odd primes sum to an even number. The tempting repair — an auxiliary bounded block — fails, and instructively: a bounded block B has cross-orbitals of size O(|B|·n), collapsing m\* from density Θ(1) to O(1/n), the same mechanism that makes a fixed point fatal (cf. Claim 3.1's block floor). The correct repair uses **three large prime blocks with a chained twist prime**:

> n = m + r + s with r = aq+1, s = bq+1, m = n − (a+b)q − 2, all of q, r, s, m prime, q ∼ cn. Chain: bottom 𝔽_m; middle C_d × 𝔽_r × 𝔽_s (d | m−1, gcd(d, rs) = 1); top C_q × C_q (both middle blocks twisted by the *same* q — q-coherence is exactly why r, s ≡ 1 mod a common q). All orbitals Θ(C(n,2)).

Two local traps, both real and both instructive. The chain (a,b) = (2,4) is impossible outright — one of {q, 2q+1, 4q+1} is always divisible by 3 (except at q = 3). And the chain (2,6), which looks obstruction-free, is **locally dead whenever 3 | n**: it forces q ≡ 2 (mod 3), whence m ≡ n (mod 3). A **covering system of chains** is therefore required. Joint local solubility (positive singular series) is verified explicitly at ℓ = 2, 3, 5 and for ℓ ≥ 7 by counting (≤ 4 forbidden residues among ℓ−1). Each hypothesis is a four-condition Hardy–Littlewood system in one variable (predicted count ∼ 𝔖(n)·n/log⁴n), one condition beyond the even case, same believed tier.

> **Proposition 5.3 (the chain constant, closed form).** Put q = γn. The binding pair of orbitals is the full-twist block against the *weaker* twisted block (a < b makes intra-r = aq² smaller than intra-s = bq²); balancing intra-m = m²/2 against aq² gives γ = 1/(a + b + √(2a)) and

> **δ(a,b) = 2a / (a + b + √(2a))².**
> Maximizing over locally admissible even pairs: **(a,b) = (4,6) gives δ = 0.0486**, admissible whenever q ≡ 1 (mod 3); (2,6) gives only 0.0400. For 3 | n the (4,6) chain is unusable (it forces m ≡ 0 mod 3) and the best admissible pair is (6,12) with δ ≈ 0.028.

So the covering system is **(4,6) for 3 ∤ n and (6,12) for 3 | n**, and

> **δ₀^{odd} ≈ 0.049 (3 ∤ n), ≈ 0.028 (3 | n),  against δ₀^{even} = 1/4** — a factor of five to nine, all relative to C(n,2).

Two things are worth stating plainly. First, δ₀^{odd} is *positive and now explicitly computed*, on exactly the same conditional footing as the even case — the odd-n rung is not in doubt, only weaker. Second, 0.0486 is a **ceiling of the three-block mechanism, not a current best estimate**: every chain is capped by Prop. 5.3, the only route upward is smaller multipliers, and the one pair that would beat it — (2,4), at 0.0625 — is exactly the mod-3 casualty. Empirical confirmation that the wall is real rather than a sampling shortfall: over n ≤ 10⁴ the maximum density attained by any chain witness is **0.0485**, flush against the closed form, and attained repeatedly by (4,6) chains (n = 9325, 7409, 4795, …). Improving on 0.049 for odd n requires a structurally different family — four blocks, a twisted bottom block, or something evading the (a+b)q < n budget that caps γ (Open Problem 2). For n = 2·(prime power) Theorem 2.1 gives density (m−1)/(2m−1) → 1/2, the proven ceiling, with no conjecture at all.

**5.4 Effectivity, and what the ladder actually asserts.** Hardy–Littlewood-type conjectures are *asymptotic and ineffective*: they assert R(n) → ∞ along locally admissible n, hence R(n) > 0 for all *sufficiently large* such n, with no effective threshold — and their all-n strengthenings are strictly stronger conjectures with, for our bespoke systems, no verification literature (classical Goldbach's all-even-n form, verified to 4·10¹⁸, is the cultural exception, not the rule). Since ARK is an all-n statement, this matters, and the honest formulation of the ladder inverts the usual conditionality: **for any specific n, existence of a representation is machine-checkable in microseconds, and a found representation *constructs the group*, making μ(n) ≥ δ₀·C(n,2) an unconditional theorem at that n.** The conjecture's sole role is the claim that the exceptional set (admissible n with no representation) is finite; its ineffectivity means the asymptotic framework can never, even fully granted, say anything about a specific small n — the finite computations of §8 are the only tool for the values ARK actually mentions, and the division of labor between §§4–6 and §8 is forced, not stylistic. The known model for welding the two regimes into an all-n theorem is ternary Goldbach (Vinogradov's ineffective asymptotic, effectivized by Helfgott to 10²⁷, verified below); for binary-type systems both halves of that weld are presently out of reach. A cheap and worthwhile ledger item: verify computationally that every n up to a large bound admits its covering-chain representation with blocks in the δ₀-window, recording unconditional μ(n) ≥ δ₀·C(n,2) for all checked n.

**5.5 The ledger, measured to n = 10⁴** (`mu_fast.py`; full output `mu_table_full.csv`). Every n in [2, 10⁴] admits *some* construction — no empty rows — so the family menu is complete in the weak sense. A **diagnostic threshold of 1/12** — chosen to sit between the odd-n chain ceiling of 0.049 and the even-n two-block constant of 1/4, so that it separates the two regimes — splits sharply by parity: of 4,987 even composites only **25 (0.5%)** fall below it, while of 3,732 odd composites **2,439 (65.4%)** do, and the odd shortfall is *widening* with n (36.5% below it for odd n ≤ 1000, 53.9% to 3000, 65.4% to 10⁴). Every one of the composites whose best witness is a three-block chain lies below the threshold, as Prop. 5.3 forces (the chain ceiling is 0.049). Note the threshold is diagnostic, not a derived constant: measured instead against δ₀^{even} = 1/4, which is attained only when a balanced safe-prime split exists, 85.8% of even and 86.9% of odd composites fall short, and the parity signal disappears.

The mechanism is structural and worth recording, since it identifies where a new family is needed. The strong two-block family needs exactly one even block, and it must be the **prime-power** block: the other block's translations occupy the cyclic middle layer, so that block must be of *prime* degree, and the only even prime is 2. Hence odd n reach the strong family only via n = 2^a + r with r prime — about log₂n candidate splits, against ~n/2 for even n. Existence is not the binding constraint (94–96% of odd n have n − 2^a prime for some a, barely declining); *quality* is, because clearing the threshold additionally requires r − 1 to carry a prime-power divisor ≳ 0.06n, i.e. r near-safe-prime, a condition of density ~1/log n. The remaining rescue for odd n is the diagonal family, needing n = k·(prime power) with small k, whose density thins like ~1/ln n. Two thinning routes against a hard chain ceiling gives the widening gap: of odd composites clearing the threshold, 1,032 do so by the diagonal family, 249 by a two-power two-block split, 12 by wreaths.

Caveat on interpretation: all of this measures the *current family menu*, not μ(n). The proven ceiling remains ⌊C(n,2)/2⌋, and whether odd n are genuinely poorer or merely poorly served by this template is precisely the extremality question of Open Problem 1.

> **Proposition 5.2′ (top rung, both parities).** Unconditionally: μ(n) ≥ δ₀·C(n,2) for every n admitting the relevant representation (checkable per n; two-block for even n, covering-chain for odd n), with δ₀^{even} = 1/4 and δ₀^{odd} ≈ 0.049 (3 ∤ n) or ≈ 0.028 (3 | n) per Prop. 5.3 — all densities relative to C(n,2). Conditionally (Hardy–Littlewood for the three systems): the exceptional set is finite, hence μ(n) = Θ(C(n,2)) for all sufficiently large n — with an *ineffective* threshold, so this asserts eventual evasiveness only. All-n statements at specific values belong to §8's finite methods.

## 6. The converse: μ encodes prime distribution

Granting the structure reduction of §3, Cor. 3.2 is an equivalence, so lower bounds on μ yield additive prime theorems: μ = ω(n^{3/2}) for all large n implies binary-Goldbach-difficulty representation theorems; μ = Θ(C(n,2)) for all sufficiently large n is equivalent to finiteness of the exceptional sets of the Hardy–Littlewood systems of §5 (two-block for even n, covering-chain three-block for odd n) — the parity split and the effectivity caveat of §5.4 both propagate here: the equivalence is between eventual statements, ineffective on both sides. The scope limit stands: μ probes exactly the Hardy–Littlewood/Bateman–Horn stratum, nothing finer; and the equivalence's one potential leak is the ★ extremality claim, with wreath forms included on the group side.

### Part III — Exact computation, and the structure of the obstruction

*The asymptotic framework says nothing about any specific n. This part reports what exhaustive computation says at n = 10 and 12, and then explains — via a presentation calculus for properties — why the method behaves as it does.*

## 7. The metaproperty ladder: where each hypothesis and test sits

**7.1 The metaproperty ladder.** It clarifies everything downstream to fix where each hypothesis and each test lives. For a monotone decreasing P with complex Δ_P:

> **trivial ⟹ non-evasive ⟹ collapsible ⟹ contractible ⟹ ℤ-acyclic ⟺ (𝔽_p-acyclic for every p) ⟹ 𝔽_p-acyclic for one p ⟹ χ(Δ_P) = 1.**

This is the spine; §7.2 hangs the group-dependent tests off it and draws the whole diagram.

**ARK is exactly the assertion that the first implication reverses.** The ladder also runs from combinatorial to topological to algebraic invariants: non-evasiveness and collapsibility depend on the simplicial structure, contractibility only on homotopy type, acyclicity and χ only on homology — each step discarding information.

*Strictness for general complexes.* Every implication is strict. There are collapsible complexes that are evasive; the dunce hat is contractible but not collapsible; presentation complexes of perfect groups are ℤ-acyclic but not contractible; a complex with H̃₁ = ℤ/q is 𝔽_p-acyclic for p ≠ q but not ℤ-acyclic; and χ = 1 obviously does not imply acyclicity.

*Where our tests sit — and why they are independent.* Each computational test in §8 is a consequence of a different rung.

| test | rung it needs | what it yields |
|---|---|---|
| Oliver congruences | ℤ-acyclic | χ(Δ_P^Γ) ≡ 1 mod q for each Oliver Γ |
| Smith conditions | 𝔽_p-acyclic | Δ_P^{P₀} is 𝔽_p-acyclic for p-subgroups P₀ |
| global χ test (§8.12) | χ(Δ_P) = 1 | the weakest rung of all |

The fixed-complex conditions and the global condition are **independent** consequences of acyclicity — neither implies the other — which is exactly why the n = 10 skeleton satisfied the entire CSP and then failed the global χ test.

*The prime-power collapse, and where it stops.* For n = p^k take Γ = AGL(1,n) = 𝔽_n ⋊ C_{n−1}: an Oliver chain with **trivial** top layer, so ℤ-acyclicity would force χ(Δ_P^Γ) = 1 exactly, while the invariant graphs are only ∅ and K_n, giving a fixed complex {∅} with χ = 0. Hence at prime powers

> trivial ⟺ non-evasive ⟺ collapsible ⟺ contractible ⟺ ℤ-acyclic (all empty among nontrivial P),

which is KSS. But the collapse **stops there**: 𝔽_p-acyclicity and χ(Δ_P) = 1 are not excluded, because Smith theory applied to the translation subgroup leaves a large fixed complex (all unions of difference-class orbitals) and yields no contradiction. So even at prime powers the last two rungs are strictly weaker than the rest.

*What is open below the prime powers.* The sharp question the framework actually confronts is not ARK but its weakening:

> **Is there a nontrivial monotone graph property at some non-prime-power n whose complex is ℤ-acyclic (or contractible)?**

Nothing rules this out, and it is *strictly weaker* than ¬ARK, which additionally demands non-evasiveness. This reframes the computations of §8: the CSP searches for properties satisfying **consequences of acyclicity**, so even a satisfying assignment that also passed the global χ test would not disprove ARK — it would exhibit a property that every topological test accepts. That is the precise content of the "certificate gap" recorded in §8.12, and the reason the adversary search of §8 is the only tool in the note that could settle a candidate outright.


**7.2 Oliver congruences as metaproperties: the diagram branches, and single primes get attacked.** The conditions the machinery actually tests are indexed by a group and a prime pair, and — this is the point — **they do not all consume the same rung of §7.1**. Write an Oliver group as Γ₂ ◁ Γ₁ ◁ Γ with Γ₂ a p-group, Γ₁/Γ₂ cyclic, Γ/Γ₁ a q-group.

| shape of Γ | hypothesis consumed | conclusion |
|---|---|---|
| pure p-group | **AC_p** (one prime) | Δ_P^Γ is AC_p, so χ(Δ_P^Γ) = 1 |
| p-group ⋊ q-group, **cyclic layer trivial** | **AC_p** (one prime) | χ(Δ_P^Γ) ≡ 1 mod q |
| nontrivial cyclic middle layer | **ℤ-acyclic** (all primes) | χ(Δ_P^Γ) ≡ 1 mod q |

The middle row is the useful refinement: Smith gives χ(Δ_P^{Γ₂}) = 1 from AC_p alone, and the q-group's non-fixed cells lie in orbits of size divisible by q, so χ(Δ_P^Γ) ≡ 1 mod q follows without touching any other prime. With a nontrivial cyclic middle the Lefschetz step over 𝔽_p returns only a congruence mod p, and the argument genuinely needs ℤ-acyclicity. **So the cyclic layer is exactly what upgrades the hypothesis from one prime to all of them.**

Hence the implication structure is a branching diagram rather than a chain:

```
                +-------------------------+
                |         trivial         |
                +------------+------------+
                             |
                             |   ARK  <=>  this arrow reverses
                             |
                +------------v------------+
                |       non-evasive       |     combinatorial:
                +------------+------------+     depends on the
                             |                  simplicial structure
                +------------v------------+
                |       collapsible       |
                +------------+------------+
                             |            - - - - - - - - - - - - -
                +------------v------------+     topological:
                |      contractible       |     homotopy type only
                +------------+------------+
                             |            - - - - - - - - - - - - -
                +------------v------------+     algebraic:
                |        Z-acyclic        |     homology only
                |    ( = AND_p  AC_p )    |
                +------------+------------+
                             |
                             |     +-----------------------------------------+
                             +---->|  OLIVER(p,q; G)    chi(D^G) = 1 mod q   |
                             |     |  G HAS a nontrivial cyclic middle       |
                             |     +-----------------------------------------+
                             |
                   (drop to a single prime)
                             |
                +------------v------------+
                |          AC_p           |
                |  (F_p-acyclic, ONE p)   |
                +------------+------------+
                             |
                             |     +-----------------------------------------+
                             +---->|  SMITH(p; G)       D^G is AC_p          |
                             |     |  G a p-group        (so chi(D^G) = 1)   |
                             |     +-----------------------------------------+
                             |
                             |     +-----------------------------------------+
                             +---->|  OLIVER(p,q; G)    chi(D^G) = 1 mod q   |
                             |     |  G = p-group : q-group, NO cyclic mid.  |
                             |     +--------------------+--------------------+
                             |                          |
                             |     +--------------------v--------------------+
                             |     |  EVERY box above gives   chi(D^G) != 0  |
                             |     |  (not > 0: a congruence mod q permits   |
                             |     |   1-q, 1-2q, ...; only SMITH and the    |
                             |     |   trivial-top case give chi = 1 exactly)|
                             |     +--------------------+--------------------+
                             |                          |
                             |     +--------------------v--------------------+
                             |     |  D^G is NONVOID                         |
                             |     |  <=> P contains at least one orbital    |
                             |     |      of G     (transversal cond., 8.7)  |
                             |     +-----------------------------------------+
                             |
                +------------v------------+
                |     chi(Delta_P) = 1    |
                +------------+------------+
                             |
                +------------v------------+
                | chi(Delta_P) = 1 (mod q)|
                +-------------------------+
```

*Monotonicity is an outer condition, not a rung.* The entire diagram presupposes that P is a **monotone** (downward-closed) graph property — that is what makes the family of members a simplicial complex Δ_P in the first place, so without it not one of the boxes below "non-evasive" is even defined (§9.2 develops the consequences of this, and §9 as a whole is about what monotonicity costs). Nontriviality is likewise a side hypothesis rather than a rung: it is what makes the fixed complexes of §7.2's right-hand boxes small enough to contradict, since it is exactly the statement that ∅ ∈ P and K_n ∉ P.

*The bottom of the right column is what the structural criterion uses.* Every test box yields **χ(Δ_P^Γ) ≠ 0**, since 0 ≢ 1 mod q for any q ≥ 2 — and a *void* complex has χ = 0, so the fixed complex must contain at least one face. By downward closure a face is a nonempty invariant graph, i.e. a union of orbitals, each of whose orbitals is then also in P. That is precisely the transversal condition of §9.7: **P contains at least one orbital of Γ**. Two things follow. It is the weakest consequence of every box above it, which is why the transversal condition can never deliver more than the CSP does — the point recorded in §9.7 and now visible in the diagram. And it is *strictly* weaker at two steps: χ ≠ 0 does not recover the congruence, and non-voidness does not recover χ ≠ 0, since a nonvoid complex can perfectly well have χ = 0. Note also that the extraction gives χ ≠ 0 rather than χ > 0; strict positivity is available only from SMITH (where χ = 1 exactly, the fixed complex being 𝔽_p-acyclic) and from the trivial-top Oliver case.

*Reading the diagram.* The spine is the chain of §7.1, running from combinatorial through topological to algebraic invariants; the three boxes on the right are the conditions the machinery actually tests, each hanging off the weakest rung that implies it. **Particular versus all** appears at three places: AC_p is one prime while ℤ-acyclicity is the conjunction over all of them; each right-hand box is one group Γ and one pair (p,q), while the CSP of §8 enforces the conjunction over an entire battery, i.e. all (p,q) realisable at this n; and χ(Δ_P) ≡ 1 mod q is one modulus while χ(Δ_P) = 1 is all of them at once. The global test of §8.12 enforces only the single weakest node in the diagram, which is why it is cheap, why passing it means nothing, and why it nevertheless killed the n = 10 skeleton — the CSP had enforced the right-hand boxes and never that one.

*Which particular primes are attacked.* Two families give a contradiction from a **single** AC_p rather than from ℤ-acyclicity.

**(A) n a prime power with n − 1 a prime power.** Then AGL(1,n) = 𝔽_n ⋊ C_{n−1} has its whole twist inside a q-group, so the cyclic layer is trivial and it is p-by-q. It is 2-transitive, so its only orbital is K_n, and K_n ∉ P by nontriviality — the fixed complex is {∅} with χ = 0 ≢ 1 mod q **unconditionally**. So for every nontrivial monotone P, **AC_p fails**, where p = char(n), while AC_r for r ≠ p is untouched. These n are exactly the Fermat primes, 9, and 2^k with 2^k − 1 a Mersenne prime:

> n = 3 (AC₃), 4 (AC₂), 5 (AC₅), 8 (AC₂), 9 (AC₃), 17 (AC₁₇), 32 (AC₂), 128 (AC₂), 257 (AC₂₅₇), 8192 (AC₂), 65537 (AC₆₅₅₃₇), …

At the *other* prime powers — 7, 11, 13, 16, 19, 23, 25, 27, … — n − 1 is not a prime power, the twist has a genuine cyclic part, and only the conjunction ℤ-acyclicity is contradicted. So even KSS's theorem attacks a single prime at some n and only the whole conjunction at others.

**(B) n = q·m with m = p^a a prime power and m − 1 a q-power.** Then the block group 𝔽_m^q ⋊ (C_{m−1} × C_q) has top layer C_{m−1} × C_q, itself a q-group, so again there is no cyclic middle and **AC_p alone** yields χ ≡ 1 mod q. Here the conclusion is *conditional* on the transversal condition of §9.7 — the fixed complex is void only when P contains neither orbital:

> n = 6 (AC₃), 10 (**AC₅**), 12 (**AC₂**), 18 (AC₃), 34 (AC₁₇), 56 (AC₂), …

So at n = 10 the machinery attacks 𝔽₅-acyclicity specifically, and at n = 12 it attacks 𝔽₂-acyclicity — in each case leaving acyclicity at every other prime formally untouched. This is worth keeping in view when reading §8: a battery that mixes p-subgroups for several p is testing several *different* single-prime hypotheses at once, not one global one, and a property could in principle fail AC₅ while remaining AC₃.


**7.3 The quantifiers are reversed, and that bounds what is left to extract.** Oliver's theorem is a statement *about the group*: for a finite group G, the set of Euler characteristics χ(X^G) realisable over **all** finite contractible (equivalently ℤ-acyclic) complexes X on which G acts is exactly **1 + n_G·ℤ**, where n_G = 0 when G is a p-group (Smith forces χ = 1), n_G = q when G is p-by-cyclic-by-q, and n_G = 1 otherwise — the last case meaning G admits a fixed-point-free action, so nothing at all is forced. "Oliver's condition" is precisely the condition n_G ≠ 1, i.e. the fixed-point property on finite contractible complexes, and that is how the condition was arrived at.

We use the theorem with the quantifiers the other way round: the complex Δ_P is the unknown, and we range over every G satisfying the condition, harvesting one congruence per group. Three consequences follow, and together they delimit what remains to be extracted.

*The congruence is tight at each fixed group.* Since **every** value in 1 + n_G·ℤ is realised by some contractible complex, no sharpening of "χ(Δ_P^G) ≡ 1 mod q" is available at a fixed G from topological input alone. Whatever additional strength exists must come from somewhere other than a better theorem about one group acting on an acyclic complex.

*So there are exactly three places left to look.* **(a) More groups** — the transversal condition and the CSP of §8, which is the direction this note has pushed hardest and which is bounded by the arithmetic of which Oliver groups exist at n (§§2–6). **(b) The restriction to Δ_P complexes** — Δ_P is not an arbitrary contractible complex but the order complex of a downward-closed, S_n-invariant family, and Oliver's tightness says nothing about that subclass. A fixed-point theorem with a stronger conclusion for monotone-graph-property complexes would be new topology, and nothing in the literature we are aware of attempts it; this is the least explored of the three. **(c) Use a stronger hypothesis than acyclicity.** The KSS chain discards non-evasiveness → collapsible → contractible → acyclic in a single step and everything downstream lives at the acyclicity level, where Oliver is provably tight. Collapsibility and non-evasiveness are strictly stronger (§7.1), and the *only* tool in this note that touches them is the canonical-state adversary search of §8, which decides evasiveness directly rather than through the complex.

That last point is the cleanest explanation of the one-sidedness recorded throughout §8 and of the certificate gap of §8.12. Every topological test we run is a consequence of acyclicity, Oliver's theorem says those consequences are individually optimal, and acyclicity is three strict implications weaker than what ARK actually concerns. A property can therefore pass every test in the diagram of §7.2 and still be evasive — which is exactly what happened to the n = 10 skeleton, and exactly why a search that certifies rather than constrains has to work at the top of the ladder.

**Before the computations: where each test sits.** The three subsections below fix the logical position of every hypothesis and every test used in §8, which is what makes the results there — and their limits — legible.

## 8. Exact computation at n = 10, and the pivot to n = 12

The asymptotic framework is ineffective (§5.4), so it says nothing about any specific n — least of all the small composite values ARK actually leaves open. This section reports the other half of the division of labour: exhaustive machine computation, run flipped, asking not "is this property evasive" but "what must a counterexample look like".

(Code: `oliver_mu.py`, `ark_intersect.py`, `engine.py`, `bigbip*.py`, `tau_small.py`, `g6sum.py`, `patterns.py`, `smith*.py`, `dual_solve.py`; GAP campaign: `ark_gap.g`, `consume_gap.py`, `stage4_fast.py`; logs in `run_logs.txt`.)

**8.1 Where the hand template sits.** A hand-built affine template gives μ ≥ 10/45 at n = 10, 10/66 at n = 12, 110/231 at n = 22, with the constant visibly controlled by the arithmetic of the parts (22 = 2·11, 11 safe). GAP enumeration (§8.8) shows the template's layer rules are too strict: μ(10) = 20 via AGL(1,5)≀C₂ alone (density 0.444), and §2 now determines the n = 2·(prime power) family outright. The weak-composite diagnosis (n = 12, 21) stands.

**8.2 The intersection CSP.** Constraints on a hypothetical non-evasive nontrivial monotone P: for each Oliver Γ with top prime q, χ((P)_Γ) ≡ 1 mod q, with χ = 1 *exactly* when the top layer is trivial. Orbitals are edge-disjoint, so subsets ↔ union graphs; membership depends only on iso class, downward closed under subgraph embedding. Five-group battery: **18 admissible patterns** on 18 classes; backbone: perfect matching forced IN (the ℤ₂⁵⋊C₅ χ=1-exact condition), ≥40-edge classes OUT.

**8.3 Disjunctive density.** Every one of the 18 patterns contains a ≥20-edge class, forcing density 0.444 on any counterexample disjunctively. At n = 10 a single m\* = 20 group (§8.8) forces the same density directly, so the disjunctive route is not needed here — but it remains the tool wherever no single large group exists.

**8.4 Exact χ kills (nine minimal completions).** Via three cross-validated exact methods — exponential formula over signed connected-component weights (all 2.1M labeled graphs on ≤7 vertices; two-sort EGF log(eˣ+eʸ−1) for bipartite components on 8–10 vertices, agreeing on every overlapping class), König-cover enumerations, and nauty/geng streams (full 10-vertex stream: 12,005,168 classes, matching the known count; 10.16M K₅-free) — the minimal completions of patterns 0–2, 5–8, 13, 14 are evasive *exactly*, with χ values from ~1.8×10⁴ to ~9.3×10⁵ in absolute value against the required conspiracy value 1. Sample values: χ(closure K₅,₅) = −288729; χ(α≥5) = 36541 (billion-scale intermediate cancellation collapsing to A = −36540); χ(max-deg≤1) = −1215 = −5·3⁵ (the matching complex M₁₀ — these closures are recognizable objects with known homology literature). Remaining: nine patterns involving two structural closures (subgraphs of C₅[K₂]; of C₅⊔C₅ ∪ K₅,₅) needing a dedicated subgraph-class enumeration.

**8.5 The Smith battery and one-sidedness.** Non-evasive ⟹ collapsible ⟹ 𝔽ₚ-acyclic, and Smith's theorem forces the fixed complex of *any* p-subgroup of Σₙ to be 𝔽ₚ-acyclic — binding on every realization, not just minimal ones. Run with ℤ₅², ℤ₉: all 18 patterns survive, and the survival mechanism is the finding: every surviving fixed complex is a **cone** (an orbital O with U ∈ P ⟹ U∪O ∈ P), and blocking cones needs OUT-forcing the patterns lack. Structural conclusion: χ conditions, acyclicity, and monotone propagation all push graphs *into* P; the only OUT-generator is nontriviality. **The topological method is one-sided**; KSS wins at prime powers because coarse lattices make IN-forcing plus the single top OUT jointly unsatisfiable, while composite-n lattices leave a free middle band.

**8.6 The dual battery.** P^∨ = {G : Ḡ ∉ P} is monotone, nontrivial, and evasiveness-equivalent to P; since complements of orbital unions are orbital unions of the same group, dual bits are y[S] = 1 − x[comp S] — **no new variables**. Every group contributes a complement-reflected second condition; dual forced-INs are primal forced-OUTs on dense graphs. Results: primal+dual χ admits 878 joint patterns on the 36-class catalog; adding primal+dual Smith cuts to 138 (6.4×), but all 18 original patterns survive in projection: **the cone escape is self-dual**, and the free middle band (forced-INs ≤ 5 edges, OUTs ≥ 40) is contractible from either direction when lattices are decoupled from the band's boundary.

**8.7 Attacks on the band.** (a) Dual χ-magnitude screen (exact χ of dual minimal completions kills primal-*maximal* realizations — mirror of §8.4, closing intervals at both endpoints); (b) p-groups with lattices *coupled* to pinned classes (e.g. the diagonal C₄ ≤ AGL(1,5)² with a singleton edge-orbital); (c) a quantitative interval bound |χ(P) − χ(P_low)| < deficit via orbit-size divisibility mod p. None yet run to completion.

**8.8 The full-battery campaign at n = 10.** A GAP pipeline (`ark_gap.g`) enumerates groups far beyond any hand template: all 45 transitive groups of degree 10 (24 are Oliver with ≤ 12 orbitals), direct products over partitions, imprimitive wreaths — where AGL(1,5)≀C₂ with m\* = 20 lives, the witness for §3's wreath clause — and every p-subgroup of every Sylow subgroup of S₁₀ up to Sylow-conjugacy: **967 groups (268 Oliver + 699 p-groups)**. A checkpointed consumer (`consume_gap.py`: selection-signature-guarded, inference-first monomorphism stage) builds the joint catalog, and a memoized event-driven solver (`stage4_fast.py`) enforces primal+dual χ plus primal+dual 𝔽ₚ-acyclicity with leaf-level verification of every group.

Result: on 75 groups (40 Oliver at t ≤ 10 plus 35 p-groups) and 1242 classes, the system is **SAT with a leaf-verified solution**, found at 339k nodes and independently reproduced bit-for-bit on a second machine (the solver is deterministic). The verified candidate-property skeleton is the monotone closure of **ten explicit maximal graphs** (graph6 strings in `skeleton.pkl`): the circulant C₁₀(1,2) (20 edges), the apex graphs K₁+3K₃ and K₁+C₉ (18 edges, from the 3+3+3+1 and 9+1 block lattices), a K₁+K₄ apex (15 edges), an unidentified 5-regular 25-edge graph with 20 triangles from the transitive lattices (graph6 `IQjVRiyVO` — not K₅,₅, C₅[K₂], or the Petersen complement), and five further 12–15-edge graphs. Its anatomy — apex and circulant maximal elements interleaved with excluded classes from 8 edges up — resembles no nameable natural property, which is itself informative about what a counterexample at n = 10 would have to look like. The skeleton is subsequently killed by the global χ test (§8.12).

Two methodological notes for successors. A solver bug once produced a **false SAT** (an early return inside a bookkeeping loop desynchronising from its undo); the fixed solver re-verifies every group at every leaf, and no SAT verdict should be trusted without that. And variable ordering by greedy group-completion — closing the harsh χ = 1-exact and acyclicity conditions early — was the difference between 28M-node thrashing and near-instant verdicts.

**8.8′ The pivot to n = 12.** With the n = 10 SAT stable across escalating batteries — as the one-sidedness analysis of §8.5–7.6 predicts — the higher-information target is n = 12: the first arithmetically weak composite (density 0.273 in Appendix A even after the wreath rescue), where the topological obstruction is weakest relative to n² and both outcomes of the CSP remain genuinely live. The entire pipeline is now degree-generic: `ark_gap.g` takes N := 12 at the top (301 transitive groups at degree 12 vs. 45; expect proportionally larger stages), and `consume_gap.py` / `stage4_fast.py` / `probe_backbone.py` auto-detect the degree from the data.

**8.9 The probed backbone, and the duality involution theorem.** Per-class probing (`probe_backbone.py`: pin x[c] = v, run the full solver to SAT/UNSAT; UNSAT verdicts are exact) has covered 400 of the 1242 classes of the full 75-group battery (~26 h). Results: **28 classes forced IN** (edge counts 0–10: the empty graph, K₃, K₄, C₁₀, the perfect matching, K₁,₈, assorted forests and small unions) and **18 forced OUT** (35–45 edges). Discovery rate is steady at ~5 forcings per 100 probes with no decay.

Inspection of the two lists revealed, and the following theorem now explains, a perfect pairing:

> **Theorem (duality involution).** Let the catalog C consist of all orbital-union iso-classes of a battery of groups, and let the constraint system comprise: the pinnings x[∅] = 1, x[K_n] = 0; monotonicity under subgraph embedding; and, for every group in the battery, *both* the primal and the dual condition (χ ≡ 1 mod q or χ = 1 exactly for Oliver groups; 𝔽ₚ-acyclicity of the fixed complex for p-groups). Then x*[c] := 1 − x[c̄], where c̄ is the complement class, is a well-defined involution on the solution set. Consequently the forced-IN and forced-OUT sets are exchanged by complementation, and the free set is complement-symmetric.
>
> *Proof.* (1) C is complement-closed: the complement of a union of Γ-orbitals is the union of the complementary orbitals of the same Γ, C contains all 2^t unions per group, and complementation commutes with relabeling, hence descends to an involution on iso-classes. (2) x* pins correctly: x*[∅] = 1 − x[K_n] = 1 and x*[K_n] = 1 − x[∅] = 0. (3) Monotonicity: a ⊆ σ(b) implies σ(b)‾ = σ(b̄) ⊆ ā, so a ≤ b ⟹ b̄ ≤ ā; if x*[b] = 1 and a ≤ b, then x[b̄] = 0 with b̄ ≤ ā, and upward propagation of exclusion gives x[ā] = 0, i.e. x*[a] = 1. (4) For each group, the primal condition evaluated at x* is literally the dual condition evaluated at x — the substitution x*[∪_{i∈S} O_i] = 1 − x[∪_{i∉S} O_i] is the defining relation y[S] = 1 − x[comp S] — and vice versa; since both are enforced for x, both hold for x*. Identically for the Smith conditions. (5) (x*)* = x. ∎

Three remarks. *(i)* The hypothesis that the battery enforces **both** directions is essential and satisfied by our solver (which computes cp/cd and pf/df for every group); a primal-only battery would not support the involution and its backbone need not be complement-paired. *(ii)* At n = 10 there are no self-complementary classes (C(10,2) = 45 is odd), so the pairing is perfect. *(iii)* Empirical status: 18/18 forced-OUT classes are complements of forced-IN classes — 15 observed directly, and the theorem's three outstanding predictions (classes 493, 439, 457, the complements of the 36-, 36-, and 38-edge forced-OUT classes) were probed after the proof was found and all came back **UNSAT-pinned-0, i.e. forced IN**, as required. Practical corollary: probing one representative per complement pair suffices, halving the remaining sweep.

The theorem also settles what the dual battery of §8.6 contributes, at class resolution: it converts every sparse forced-IN class into a dense forced-OUT class — the down-forcing §8.5 said the primal machinery lacked — and simultaneously shows why this cannot reach UNSAT by itself: the involution guarantees the OUT-forcings are mirror images of the IN-forcings, pinned to the complementary density extreme, never meeting in the middle.

**8.9′ The forced/free geometry is not density-stratified.** A natural first guess — a sparse forced-IN region, a dense forced-OUT region, and a clean free band between them — is wrong. Classes with ≤ 4 edges are uniformly forced IN and ≥ 41 uniformly forced OUT, but across the entire range 5–40, forced and free classes coexist at every edge count: 29 free classes at ≤ 10 edges interleave with the forced-IN set. Clean witness that no invariant-based heuristic predicts the backbone: classes 5 and 43 are both 35-edge, 7-regular, with 50 triangles *and* 200 four-cycles, yet 43 is forced OUT and 5 is free; the distinction lives in the complement (43 = co-C₁₀, 5 = co-(C₅⊔C₅)) and follows from the involution plus the facts that C₁₀ is forced IN while C₅⊔C₅ is free. A detail relevant to §8.10: K₁,₈ is forced IN but K₁,₉ — the spanning star — is free, so an admissible property may exclude the spanning star.

**8.10 The scorpion, and the algorithmic side of the ledger.** The scorpion property (Best–van Emde Boas–Lenstra) is the standing example of a nontrivial *non-monotone* graph property decidable in O(n) queries. Its engine is the celebrity-elimination trick: sting (degree exactly 1), tail (exactly 2), body (exactly n−2) are pinned by *two-sided* degree constraints, so every query answer disqualifies some vertex for some role — "present" can kill a sting/tail candidacy, "absent" a body candidacy — giving linear convergence to an O(n)-checkable witness. Monotonicity destroys the engine by fiat: a positive answer can never disqualify anything. Three points deserve permanent record.

*Monotonicity is constitutive, not protective.* Without monotonicity there is no downward-closed family, hence no simplicial complex Δ_P, no χ, no Oliver argument: the topological method is not *dodging* the scorpion; it is undefined in the scorpion's regime. Correspondingly, the algorithmic one-sidedness (no pruning from positive answers) and the constraint one-sidedness of §8.5 (every condition forces graphs into P; only nontriviality forces out) are two faces of one fact — monotone properties admit no upper-bound clauses.

*The monotonized scorpion is evasive — verified.* P = "∃ s, b and t ∉ {s,b} with {s,t} ∈ E and b adjacent to every vertex except s" (the monotone closure, keeping the witness shape and dropping the upper bounds) is nontrivial monotone and **evasive at n = 4, 5, 6 by exact adversary search** (`scorpion_test.py`; memoized states 276 / 28,869 / 3,563,639). The same combinatorial structure: O(n) queries with exact degrees, all C(n,2) once monotonized.

*The skeleton is scorpion-shaped.* Three of the ten maximal generators of the n = 10 SAT skeleton are apex graphs — K₁+3K₃ and K₁+C₉ (18 edges), K₁+K₄+5K₁ (15) — a dominating vertex over structured remainder: the scorpion's body, monotonized. The K₁,₉-free fact of §8.9′ shows the backbone permits exactly what an apex-witness property needs. If a counterexample exists at n = 10, the machinery is pointing at apex-generated properties, and that is where the decision procedure below should aim first.

*The certificate framing, with literature anchors.* ARK is equivalent to: monotone graph properties always exhibit the maximal gap between decision-tree depth D and certificate complexity (triangle-containment has certificates of size 3, yet ARK asserts D = C(n,2)); the scorpion is the canonical demonstration that search-and-verify is not absurd in general, and ARK says it never works under monotonicity. This theme has an existing formalization: the scorpion property is provably *R-instance optimal* (Grossman–Komargodski–Naor, instance complexity in the decision-tree model), with the explicit conjecture there that no monotone graph property is randomized instance-optimizable — a randomized cousin of the framing here. The scorpion lineage is Best–van Emde Boas–Lenstra and Milner–Welsh (1975); for the rarity and artificiality of nonevasive constructions see Kulkarni, *The smallest nonevasive graph property* (arXiv:1303.5601); for the quantum side, the scorpion has quantum query complexity Θ̃(√n) against the Ω(n^{2/3}) monotone lower bound (Sun–Yao–Zhang). The quantitative interpolation proposed here — a monotonicity-defect parameter with D(P) ≥ N − g(defect) — was *not found* in a first literature pass and remains flagged as plausibly novel pending a deeper check. Relatedly, a counting attack is impossible: adaptive decision trees number 2^{0.7326·2^N} (N = C(n,2)), dwarfing the ~2^{1.1×10⁶} monotone graph properties at n = 10, so no union bound exists; and the branch-wise symmetry reduction (choices matter only up to Aut of the current 3-coloured state, legitimate because survivability depends only on the state's iso-class) yields a state DAG of size ~3^N/n! — the design basis for the exact adversary search that complements this note's one-sided machinery.

**8.11 Infrastructure, and n = 12 status.** Stage 3 of the pipeline was rebuilt inference-first: within-lattice mask containments are free by construction; equal-edge-count distinct classes are automatically non-embeddable; invariant domination (degree sequence, triangles, P₃, C₄) excludes most negative pairs; and two-sided transitive closure (a⊆c⊆b ⟹ a⊆b; c⊆a ∧ c⊄b ⟹ a⊄b; a⊄d ∧ b⊆d ⟹ a⊄b) runs to fixpoint after every parallel VF2 batch. **Acceptance: PASSED** — on the full 1,242-class n = 10 battery the rebuilt matrix is *bit-identical* to the archived reference (249,711 true entries, density 0.162), so two algorithmically independent computations agree, one by VF2 on every ordered pair and one deciding 79.9% by inference. Every downstream verdict (the forcings of §8.9, the involution predictions, the SAT, hence the χ kill of §8.12) now rests on a reproduced object. At n = 12: GAP enumeration complete and validated (8,819 groups: 295 trivial-top, 657 at q = 2, 67 at q = 3, 6,094+ p-groups; at t ≤ 8, 2,293 raw → 59 kept → 600 classes); the transitive census finds m\* = 18 achieved six ways and exceeded zero ways, consistent with the wreath bound (𝔽₄⋊C₃)≀C₃ being optimal at 12. Stage 3 is running with **20.6% of ordered pairs needing VF2** (versus 19.9% at n = 10 — the invariant filters transfer intact to 12 vertices), so the measured 48 h ETA of the unoptimized code should collapse to hours.

**8.12 The global χ test, and the third gap in the certificate.** For downward-closed P let S := Σ over *labelled* G ∈ P of (−1)^{|E(G)|}. Then χ(Δ_P) = 1 − S, and since D(f) ≥ deg(f) with deg = C(n,2) exactly when the top Fourier coefficient is nonzero, **S ≠ 0 ⟹ P is evasive** — no game search required. This is the §8.4 screen in Fourier dress, and it is *not* expressible on the CSP variables, so it must be applied to fully specified properties.

Applied to the n = 10 skeleton (`chi_test.py`): the down-closure has **64,333 iso classes** and 153,468,934,696 labelled graphs, with **S = −15,183,000**, so χ(Δ_P) = 15,183,001 ≠ 1 and the candidate property is **evasive**. Cost ≈ 2 minutes. Cross-validated three ways: the down-closure intersected with the catalog is exactly the solution's 214 IN classes (agreeing with an independent monomorphism-based check), it contains ∅, and it excludes K₁₀. *Method warning for successors:* S must be summed over the **full** down-closure, not over its intersection with the catalog. The catalog is 1,242 of the 12,005,168 iso classes and the down-closure is emphatically not contained in it; summing over the 214 catalog classes instead gives 438,480, a meaningless number that happens to be nonzero.

This exposes a **third gap in the SAT certificate**, more fundamental than the two already noted (unenforced global χ; battery-relative scope): **a CSP solution is not a property.** It constrains only the 1,242 catalog classes; membership on the other ~12M is free apart from monotonicity. Random sampling finds explicit classes outside the skeleton's down-closure with no OUT catalog class below them (e.g. graph6 `Ib@_IPCW?` at 12 edges, `ISmQG@?sO` at 14) — each addable, giving a different property with the *same* CSP solution and its own χ. Consequently the χ kill eliminates one canonical extension (the minimal one), **not** the solution and **not** n = 10. Since the χ condition cannot be added to the CSP, no amount of catalog-side work can settle a fixed n: the pipeline's ceiling at n = 10 is now understood. `stage4_fast.py --seed` samples distinct solutions (shuffling within equal-edge blocks, preserving the group-completion heuristic) so that many minimal extensions can be χ-tested; that is evidence-gathering, not proof.

**8.13 The smallest nonevasive property, and the complementation symmetry (Adamaszek, arXiv:1303.5601).** There is a nontrivial nonevasive property ℰ of *5-vertex* graphs — eleven graphs, Bob winning in 9 of the 10 questions — and ℰ together with its set-complement are the only ones at n ≤ 5; every nontrivial 4-vertex property is evasive. Three points bear on this note.

*Independent validation of our machinery.* His count of 758 iso classes of positions is reproduced exactly by `adversary.py`'s canonicalization: we count 792 classes of 3-coloured K₅, and 792 − 34 = 758, the difference being the terminal positions with no unknown edge. We also **recovered ℰ itself** (the paper gives it only as figures): filtering the 8,736 candidates matching his structural description by the vanishing-alternating-sum condition leaves 118, and an exact game solve leaves exactly one — {K₁,₃+K₁, C₄+K₁, paw, K₁,₄, bull, cricket, [3,3,2,2,0], K₄+K₁, butterfly, dart, [4,3,3,3,1]}, complementation-closed with the bull self-complementary. ℰ is now available as the **negative control** our adversary searcher lacked; every validation so far returned EVASIVE, so a bug always answering "evasive" would have passed them all.

*The complementation parallel.* ℰ satisfies G ∈ ℰ ⟺ Ḡ ∈ ℰ, which Adamaszek uses to identify positions with their complements and halve his search. Our duality involution (§8.9) is the *twisted* form x\* = 1 − x∘complement, used to halve the probe sweep. The difference is forced: complementation-invariance is impossible for a nontrivial monotone property, since ∅ ∈ P would drag in K_n. So complementation is the governing symmetry of the evasiveness game in both worlds, and the monotone world can access only the twisted version — which is also why ℰ is necessarily non-monotone.

*A tempting but invalid inference.* Since the scorpion's 6n − 10 budget exceeds C(10,2), one might argue that "the scorpion mechanism has no room at n = 10" and take this as evidence that n = 10 is evasive. ℰ refutes the general form of that reasoning: nonevasive properties exist at n = 5, saving exactly one query out of ten. Budget arithmetic constrains the scorpion's *particular* mechanism and nothing more. The usable evidence at n = 10 comes from the χ test of §8.12.

## 9. The shape calculus: why monotone properties are handicapped

§8 keeps running into the same wall: every constraint the method produces pushes graphs *into* the property and only nontriviality pushes one out. That one-sidedness is not an artefact of the batteries — it is a fact about monotone properties, and the following presentation calculus makes it visible in one line.

Give each of the C(n,2) edges one of three states — **present**, **absent**, **irrelevant** — and call an S_n-orbit of such an assignment a **shape**. A property's **shape complexity** is the least number of shapes whose union is exactly the property. The point of the language is that it makes monotonicity, certificate complexity, and the forbidden-subgraph class visible as facts about *presentations*.

**9.0 Terminology and prior art.** Most of the framework below is standard under other names, and one item is textbook; a literature check gives the following dictionary.

- The three-state pattern is essentially Chudnovsky–Seymour's **trigraph**: an adjacency function θ : pairs → {1, 0, −1} with *strongly adjacent* / *semiadjacent* / *strongly antiadjacent*, and their **realizations** of a trigraph are exactly the members of our cube. One difference matters: in their theory the semiadjacent ("undecided") pairs are required to form a *matching*, whereas our irrelevant set is arbitrary — the scorpion's has C(n−3,2) pairs. So the object is named, our version is strictly more general, and their motivation (structure theory of claw-free and Berge graphs) is unrelated.
- Deciding whether a cube *meets* a property is the **graph sandwich problem** (Golumbic–Kaplan–Shamir): given mandatory and forbidden edge sets, is there a member of the class in between?
- Our maximal cubes inside P are **prime implicants**; positive shape complexity is **minimum DNF size** (number of terms), and the minimum-cover-of-prime-implicants formulation is classical **Quine–McCluskey**. Hardness is known: deciding whether a monotone formula has a DNF of size ≤ k is PP-complete (coNP for k in unary), and Σ₂ᵖ-complete for arbitrary formulas (Umans). So computing shape complexity is hard in general, and our small-n numbers come from exhaustive search precisely because of this.
- **§9.2 below is not new:** for a monotone Boolean function the prime implicants are exactly the minimal true points, the minimal DNF is unique, and it consists of all of them — a textbook fact (Quine; see e.g. Crama–Hammer). Our contribution is only the specialization: for a monotone *graph* property the terms are S_n-orbits, so shape complexity equals the generator count *up to isomorphism*, and the reading of the missing third state as the locus of the scorpion's engine.
- On the graph-theoretic side, the induced-subgraph version of shape complexity is the classical count of **minimal forbidden induced subgraphs** of a hereditary class (unique, and finite exactly for "finitely defined" classes); the subgraph version is the minimal forbidden subgraph set, dual to the saturated graphs of §9.4.
- What I did **not** find named is the S_n-*symmetrized* measure as a studied invariant of graph properties — i.e. minimum DNF size where terms must be orbits, and its formula analogue fsc. The framework below is best described as a repackaging of standard Boolean-function notions in the S_n-invariant setting, with the evasiveness-specific readings (§§9.3, 9.5, 9.6) as the new content.

**9.1 The scorpion is a single shape; that is its whole content.** On a fixed triple (s, t, b): n−1 present (b to all but s, plus st), 2n−5 absent (bs, and s, t to each of the n−3 feet), C(n−3,2) irrelevant, and (n−1)+(2n−5)+C(n−3,2) = C(n,2) exactly. The determined support is **3n−6**, which is simultaneously the positive certificate size — so "certificate complexity" and "determined part of the one shape" are the same number, explaining why its algorithm is certificate-optimal. Measured shape complexities elsewhere: **ℰ of §8.13 has shape complexity 4** (computed exactly: 290 maximal subcubes, 5 up to isomorphism, minimum orbit cover 4), each shape carrying a high-degree distinguished vertex and 2–4 irrelevant edges; so does 𝒢₅∖ℰ. Hence *no* nonevasive property at n ≤ 5 is a single shape.

**9.2 Monotonicity deletes a state.** For downward-closed P, any cube (L present, F free) inside P is strictly contained in (∅, L∪F), also inside P since L∪F ∈ P — because a decreasing property can never *require* an edge. So every maximal cube has an empty present-set, minimum covers may be taken from maximal cubes, and

> **shape complexity of a monotone decreasing property = number of maximal elements, up to isomorphism** — the S_n-invariant reading of the classical prime-implicant fact (§9.0) (each shape being "irrelevant on E(M), absent elsewhere"), and dually for increasing properties with minimal elements and empty absent-sets.

Verified on the down-closure of the C₅ orbit at n = 5: all 12 maximal cubes have empty present-set, every free-set of size exactly |E(C₅)| = 5. By contrast all 290 maximal cubes of ℰ have nonempty present-sets. So **monotone properties use only two of the three states, non-monotone properties can use all three**, and the missing state is exactly where the scorpion's two-sided elimination engine lives. This is the same asymmetry as §8.5's constraint one-sidedness and §8.10's algorithmic one-sidedness — three faces of one cause.

Caution on the invariant: **graph complementation** (G ↦ Ḡ) maps (L, F, A) ↦ (A, F, L) and so preserves shape complexity; **logical negation** (P ↦ 𝒢_n∖P) preserves evasiveness but *not* shape complexity. "Contains H" is shape complexity 1; its negation "H-free" has shape complexity equal to the number of H-saturated graphs. Shape complexity is a property of the presentation, not of the evasiveness question.

**9.3 Monotone shape complexity 1 = the forbidden-subgraph class.** By 9.2, a monotone increasing property of shape complexity 1 is exactly **"G contains a copy of H"** for one graph H — and its negation is the forbidden-subgraph property Q_n^H that BBKN name as open. So "is there a nonevasive monotone property of shape complexity 1?" is not a triviality but a named special case of ARK. What is known, in this language: BBKN's sparse theorem says shape-1 monotone properties with **forest** generators are evasive for all large n unconditionally, since ex(n,H) = O(n) < μ(n) = Ω(n log n); Chakrabarti–Khot–Shi extend to further H.

Exhaustive small-n check (χ screen, then adversary search on survivors): **every nontrivial shape-1 monotone property is evasive at n ≤ 6.** At n = 4 and 5 not one survives the χ screen. At n = 6 exactly one does — H = P₄ ⊔ 2K₁, i.e. "contains a path with three edges," holding for 32,056 of 32,768 graphs, with χ(Δ_P) = 1 — and it falls to exact adversary search over 2,022 canonical states. Two lessons: the χ screen is genuinely one-sided (passing it settles nothing, and only the game search closes the case), and the one near-miss is a forest, hence already inside BBKN's theorem for large n.

**9.4 Forbidden-subgraph properties: the generators are the saturated graphs.** The maximal elements of Q_n^H are the **H-saturated** graphs — H-free, with every non-edge completing a copy of H. For H = K₃ this unwinds to *triangle-free of diameter ≤ 2* (plus the star). So the shapes of Q_n^{K₃} are the maximal triangle-free graphs, and their edge counts span **sat(n,K₃) = n−1** (the star; Erdős–Hajnal–Moon) up to **ex(n,K₃) = ⌊n²/4⌋** (Turán/Mantel) — a factor ~n/4 spread, which is why the translation from H to generators is not transparent. Measured: K₃-free has 3, 4, 6 shapes at n = 5, 6, 7 (generator edges 4–6, 5–9, 6–12); C₄-free has 3, 5, 8 (5–6, 6–7, 8–9).

Where the μ-machinery reaches, by regime, via the sparse criterion ex(n,H) < μ(n): **forests** — unconditional for large n (above); **bipartite H with a cycle** — ex(n,C₄) ∼ ½n^{3/2} sits exactly at the §4 barrier, with the §5 rungs conditionally covering all bipartite H; **non-bipartite H** — Erdős–Stone gives ex(n,H) = (1−1/(χ−1))n²/2 + o(n²), so ⌊n²/4⌋ for triangles, while §2's proven ceiling is μ(n) ≤ ⌊C(n,2)/2⌋ = ⌊n(n−1)/4⌋ < ⌊n²/4⌋. Hence the **counting** criterion provably cannot prove triangle-freeness evasive at any non-prime-power n. But the counting criterion is not the only one available — see §9.7, which settles triangle-freeness at every n = 3·(prime power) by a structural argument that ignores edge counts entirely. (At n = 10: μ(10) = 20 against K₅,₅ with 25 edges. Note K₅,₅ *is* the n = 10 triangle-free Turán graph, and χ(closure K₅,₅) = −288729 was one of §8.4's nine kills: we were unknowingly killing the densest generator of triangle-freeness.) The global χ test covers the gap at small n: K₃-free gives S = 4, 3, 61 and C₄-free gives S = −36, 228, 880 at n = 5, 6, 7 — all nonzero, all evasive, in seconds.

**9.5 Certificate complexity in the shape language, and why it is not the obstruction.** For a k-shape presentation with determined supports D_i: the *positive* side is bounded by a single shape, C₁ ≤ maxᵢ|D_i|, independent of k; the *negative* side must block every shape at every placement, and that is where k bites. For monotone decreasing P the two sides invert relative to the scorpion:

> **C₁(P) = C(n,2) − sat(P)** (a positive certificate is the complement of a maximal member, worst case the smallest one), while C₀ is the size of one forbidden configuration. Hence C = max(C₀,C₁) = C(n,2) − sat(P), and any algorithm can save **at most sat(P)** queries.

Exact values: triangle-free has (C₀, C₁) = (3, 6) at n = 5 and (3, 10) at n = 6, matching C(n,2) − sat with sat = 4, 5; ℰ has (6, 8) at n = 5 and saves exactly 1 of an allowed 2; the scorpion has C = Θ(n) against C(n,2) = Θ(C(n,2)), an enormous licence it actually uses. So counting *permits* monotone savings of order n — for triangle-freeness up to n−1 queries — and ARK asserts the saving is always 0. **The obstruction to monotone nonevasiveness is therefore topological, not certificate-theoretic**, which sharpens the D-versus-C framing of §8.10: the gap that must be maximal is D against the *permitted* C(n,2) − sat(P), not against C in absolute terms.

**9.5′ Formula shape complexity (fsc).** Allowing shape *literals* (a shape or its negation) and arbitrary Boolean connectives, define fsc(P) as the least number of literals in a formula computing P. In standard terms this is **formula size over a shape basis**, and the DNF-versus-formula gap it measures is classical. The logical reading: a shape-property is existential ("∃ a placement of a partial pattern that fits"), so sc measures Σ₁-length, sc(¬·) measures Π₁-length, and mixed formulas climb the **quantifier-alternation hierarchy** — which is why alternation should be expected to buy a lot. It does: exhaustively at n = 5 over all 789 distinct shape-properties, **100,338 properties have fsc = 2 while requiring ≥ 3 shapes in *both* polarities**, the commonest winning form being S₁ ∨ ¬S₂ (an implication). ℰ is not among them — it has sc = sc(¬) = 4 and no ≤2-literal formula, so 3 ≤ fsc(ℰ) ≤ 4.

Measured values at n = 5 (sc, sc(¬), fsc): bipartite (2, 2, 2); forest (3, 3, 2); connected (3, 2, 2); triangle-free (3, 1, **1**); Hamiltonian (1, 3, **1**); ℰ (4, 4, ≥3). Regimes for n-varying families, all upper bounds: **fsc = 1** for any single forbidden or required subgraph — H-free, "contains H" (so Hamiltonicity = "contains C_n"), the induced versions, and the scorpion; **fsc = O(1)** for finitely many forbidden patterns; **fsc = O(n)** for bipartite (⌊(n−1)/2⌋ odd cycles), forest, chordal (no induced C_k, k ≥ 4), perfect (odd holes/antiholes, by SPGT), and connectivity via ⌊n/2⌋ cut-shapes; **fsc = poly(n) of high degree** for planarity, ≈ n⁹ via Kuratowski subdivisions. The starkest gap is connectivity: sc(connected) is the number of trees on n vertices, ∼2.9557ⁿ/n^{5/2}, while fsc(connected) ≤ ⌊n/2⌋ — an exponential presentation collapsing to a linear one purely by admitting negation. Caution: forest has fsc = 2 at n = 5 against the cycle-list bound of 3, so forbidden-family lists are *not* tight and none of these should be quoted as equalities.

Two readings for the evasiveness question. Since fsc = 1 contains both the scorpion (nonevasive) and every H-free property (conjecturally evasive), **fsc does not determine evasiveness**. But it sharpens the question "how simple can a nonevasive property be?", whose exact answer at n = 5 is fsc(ℰ) ∈ {3, 4} — the first datum of a *minimum presentation complexity of nonevasiveness*, computable at n = 5 by finite search.

Aside on the scorpion's design: it is the shape that fully specifies the neighbourhoods of **three** vertices and ignores the rest (determined support 3n−6). The same template at k = 1 gives "has an isolated vertex" or "has a dominating vertex" — fsc = 1, both classically evasive. Locating k special vertices costs ≈2kn against a C(n,2) allowance, so nonevasiveness first becomes affordable at k = 3, which is a cleaner account of the scorpion's anatomy than its degree list — and suggests k = 2 (support 2n−3) as the place to look in the n = 6…11 window of Open Problem 7.

**9.6 How low can a single shape go?** The scorpion works from n = 12 (6n−10 < C(n,2)); n ≤ 5 is closed by 9.1; **n = 6 through 11 is open**, and the "n ≥ 12" folklore is a statement about the scorpion pattern specifically, not about all shapes. Crucially the search space here is shapes, not properties — by Burnside, the number of shapes up to S_n is **792 (n=5), 25,506 (n=6), 2,302,938 (n=7)**. So n = 6 is *exhaustively decidable*: enumerate the 25,506 shapes, discard trivial ones, run the adversary search. Either outcome is a theorem (Open Problem 7).

**9.7 The structural criterion: orbitals as graphs, not as edge counts.** Everything above uses only the *sizes* of the orbitals. But an Oliver group also hands us the orbitals as explicit graphs, and the fixed-point argument constrains membership rather than cardinality. Restating it:

> **Structural criterion.** Let Γ be Oliver on [n] with top prime q, orbitals O₁,…,O_t, and let P be nontrivial monotone decreasing. The Γ-invariant graphs are exactly the orbital unions, and by downward closure a union lies in P only if each of its orbitals does. So if **every O_i ∉ P**, the fixed complex Δ_P^Γ is void, χ = 0 ≢ 1 mod q, and P is evasive. Contrapositive: *a nontrivial non-evasive monotone property must contain at least one orbital graph of every Oliver group.*

This is strictly weaker as a hypothesis than the sparse criterion, which demands |O_i| exceed the maximum edge count in P; here we need only O_i ∉ P. The gain is largest exactly where counting fails — for dense properties.

The most useful instance comes from the k-block full-twist group Γ = 𝔽_m^k ⋊ (C_{m−1} diagonal × C_k) of §2, whose orbitals are, for **k ∈ {2,3}**, exactly two graphs: **kK_m** (the fused intra-block class) and the **complete k-partite K_{m,…,m}** (the fused cross class). Hence:

> **Two-graph criterion.** For m ≥ 2 a prime power and k ∈ {2,3}, n = km: if a nontrivial monotone decreasing P contains neither kK_m nor K_{m,…,m}, then P is evasive at n.

Consequences, all verified by direct containment checks:

- **Triangle-freeness is evasive at n = 3m for every prime power m ≥ 3** (n = 12, 15, 21, 33, 39, 51, 57, 75, …), since 3K_m and K_{m,m,m} both contain K₃ — a case the counting criterion provably cannot reach (§2), and one that does not care that ex(n,K₃) = ⌊n²/4⌋ dwarfs μ(n).
- **Bipartiteness** evasive at n = 3m (m ≥ 3); **planarity** at n = 2m and 3m for m ≥ 5; **acyclicity** at n = km for m ≥ 3, k ∈ {2,3}; **C₄-freeness** at both; **K₃,₃-freeness** at n = 18 and 21.

*Relation to BBKN — this criterion is theirs, not new here.* BBKN's forbidden-subgraph results use exactly this argument: their stated techniques include "a universality property of cyclotomic graphs derivable using Weil's character sum estimates", which is how one verifies that *every* orbital of a metacyclic group contains a given H. Their conclusions are accordingly much stronger in coverage than anything the two-graph criterion gives: **(a)** under Chowla, "forbidden subgraph H" is eventually evasive for *every* H; **(a′)** unconditionally, its query complexity is **C(n,2) − O(1)** for every H. So the material below is a *simplification at special n*, not a strengthening: for χ(H) ≤ 3 the k = 3 block group's orbitals are a disjoint union of cliques and a complete tripartite graph, so containment of H is immediate and **no character-sum input is needed**. What the cyclotomic route buys, and this one does not, is general n and unrestricted H.

The one place a small increment may sit is the gap between (a′) and (a): unconditionally BBKN obtain C(n,2) − O(1), whereas exact evasiveness for all large n needs Chowla. The two-graph criterion closes that O(1) unconditionally, but only on the density-~1/log n set n ∈ {2·prime power, 3·prime power} and only for χ(H) ≤ 3. Whether that is already implicit in BBKN's intermediate lemmas has not been checked.

*Why it caps at χ(H) ≤ 3, and why Weil is not needed.* Catching H requires the cross orbital's clique number to be at least χ(H). The cross pairs fuse into a single complete k-partite orbital only when the top q-group is transitive on the C(k,2) block-pairs. For k = 3 this holds — C(3,2) = 3 = k and C₃ rotates them — giving clique number 3. For k = 5 the ten pairs split into two C₅-blow-up orbitals of clique number 2; and full fusion for k ≥ 4 would need the top group 2-transitive on blocks, impossible for a nilpotent q-group. **So k = 3 is the unique case with a cross orbital of clique number exceeding 2**, and the method reaches exactly the H with χ(H) ≤ 3. Character-sum estimates are what let *cyclotomic* orbitals be shown to contain every fixed H (BBKN's universality property), and that is unavoidable if one wants general n and unrestricted H. It is only within the restricted k ∈ {2,3} block family that they can be dispensed with, because the full twist collapses the orbital count to two and makes both of them trivially H-universal for χ(H) ≤ 3.

*The cap at χ(H) ≤ 3 is permanent for block constructions.* Catching H needs every orbital's clique number to be at least χ(H). A blown-up orbital's clique number equals that of its **pattern** graph on the k blocks — independent of the block size m — and patterns are the pair-orbitals of the top q-group. That is bounded:

> **Theorem 9.1 (pattern cap).** Let T be a transitive q-group of degree k. Then some pair-orbital of T has clique number ≤ 3, and every orbital has clique number 3 only when q = 3.
>
> *Proof.* T is nilpotent, so its point stabiliser T_v is subnormal: there is a chain T_v ◁ H ◁ ⋯ ◁ T with each step of index q. The first step yields a block system with blocks of size exactly q. The block stabiliser acts transitively on a block of size q, and a transitive q-group of degree q is regular, hence C_q, so its orbits on the intra-block pairs are the difference classes {±d}. The corresponding orbital of T is a disjoint union of circulants C_q(d): a perfect matching for q = 2, disjoint **triangles** for q = 3, and q-cycles for q ≥ 5. ∎

Verified on every transitive q-group of small degree: C₂, C₄, C₂², D₄, C₈, C₂³ and C₂≀C₂≀C₂ all have an orbital of clique number 2; so do C₅, C₇, C₉; while **C₃, C₃×C₃ and C₃≀C₃ have all orbitals of clique number 3**. So the block route reaches exactly the H with χ(H) ≤ 3, necessarily through q = 3 — and since q = 3 works at k = 3 and k = 9 (C₃≀C₃ gives two orbitals, both of clique number 3), the criterion applies at **n = 3^a·m** for any a ≥ 1 and prime power m ≥ |V(H)|, not merely n = 3m.

*Why this makes character sums unavoidable.* Theorem 9.1 says a blow-up orbital's clique number is bounded by 3 **no matter how large the blocks are**. A cyclotomic orbital on 𝔽_m, by contrast, has clique number growing with m — for the Paley graph, about ½log₂m — so for any fixed H it eventually contains H. That is the structural reason BBKN reach for Weil's estimates rather than a block construction: character sums are the only route to orbitals of unbounded clique number, hence the only route to unrestricted H. Equivalently, the division of labour is: **number theory decides which groups exist at a given n; character sums decide whether a given group's orbitals are H-universal.** Better number-theoretic input (the ladder of §5 rather than Chowla) does not remove the need for the second step — what it does is lower the *index* of the available cyclotomic orbitals, and since universality for an h-vertex, e-edge H needs roughly m ≫ (index)^{2e(H)}, index 2 (the Paley case, delivered by a safe prime) gives the smallest effective threshold. For H with few edges the difference is immaterial; it grows exponentially in e(H).

*Several groups at once: the transversal formulation.* Each Oliver group Γ_i on [n] independently forces P to contain one of its orbitals, so across a family Γ_1,…,Γ_s:

> A nontrivial non-evasive monotone P must contain **at least one orbital of every Oliver group on n points** — P is a *transversal* of the hypergraph whose edges are the orbital families. Being downward closed, P then contains ⋃ᵢ down(O_{i,jᵢ}) for some choice.

This is the density-free upgrade of the disjunctive statement of §8.3, and the two lenses disagree about what combining groups buys. **Density-wise, nothing:** the floor is max over groups of that group's minimum orbital, so the single best group already determines it. Worked example at n = 50, with A = 2 blocks of 25 (orbitals 2K₂₅, K₂₅,₂₅), B = 27+23 (K₂₇, K₂₃, K₂₇,₂₃), E = 47+3 (K₄₇, K₃, K₄₇,₃), G = 49 + a fixed point (K₄₉, K₁,₄₉), F = 25 blocks of 2 (25K₂, a C₅²-pattern blow-up): the minimum over hitting sets of the maximum edge count is 600, density 0.490 — exactly group A's contribution alone.

**Structurally, a great deal.** Cross-group containment collapses the 72 raw choices to **36 distinct minimal hitting sets**, each using only 2–4 graphs rather than one per group, because an orbital of one group often already contains an orbital of another (choosing 2K₂₅ satisfies B via K₂₅ ⊇ K₂₃ and E via K₃). And the narrowing is sharp once a target property is fixed: of the 36, exactly **one** contains no triangle-bearing orbital, namely {K₁,₄₉, K₂₅,₂₅, K₂₇,₂₃, K₄₇,₃}, all complete bipartite. So a triangle-free property at n = 50 must contain all four of those graphs at once — a far stronger constraint than any single group yields, and not a contradiction, since "bipartite" is such a property. That is consistent with Theorem 9.1: 50 has no factor 3, so no group on 50 points has all cross orbitals of clique number ≥ 3.

Two limits worth stating plainly. The transversal condition can never yield a contradiction by itself, because any hitting set's down-closure *is* a legitimate nontrivial monotone family; it is a candidate generator and a per-property test, not a proof method. And it is strictly weaker than the CSP of §8, which enforces the full χ congruences rather than mere non-emptiness of the fixed complex. What it supplies is the explanation of *why* the n = 10 CSP is satisfiable: the surviving skeleton contains one orbital of every battery group, which is precisely what the transversal condition allows.

*What this says about n = 10.* The two orbitals there are 2K₅ (20 edges) and K₅,₅ (25 edges), so the criterion reads: any counterexample must contain 2K₅ or K₅,₅. That is precisely the "disjunctive density" statement of §8.3, sharpened from "some class with ≥ 20 edges" to two named graphs. The surviving skeleton of §8.8 **contains 2K₅** and not K₅,₅ — so it satisfies the criterion legitimately, which is why n = 10 remained SAT and why the global χ test of §8.12 was needed to kill it.

### Part IV — Assessment and problems

## 10. Assessment

Two questions deserve explicit answers: how much should one believe ARK, and what is this framework's actual reach.

Read against May–July 2026: the falsifications of the Erdős unit distance conjecture (Golod–Shafarevich class field towers), the Jacobian conjecture in C³, and the Dinitz–Garg–Goemans conjecture — all AI-assisted, all having "survived decades of attention." Transfers: survival-under-attention arguments measured the human-search regime, now ended; and a falsifying mechanism can be principled and long-visible in an adjacent field. Against this: ARK's support differs in kind (a partial mechanism with exactly-proven subclasses — prime powers, bipartite, sparse regime, minor-closed). Net: ARK ~0.80 (from ~0.90), failure mass at arithmetically weak composite n; weak evasiveness at density Θ(1) ≥ 0.97. The §8.8 search is run sincerely in both directions, and each verified SAT solution is treated as a candidate-property skeleton, not merely a negative result.

## 11. Open problems

1. **(Extremality ★, the keystone.)** Prove the wreath-inclusive extremal form: among Oliver groups of degree n, minimum u-orbital beyond n^{3/2}-scale forces affine-wreath type on prime-power block decompositions, ruling out exotic imprimitive solvable towers at intermediate exponents. Theorems 2.2–2.3 now prove the block-structure half unconditionally, so what remains is the twist-coherence half (Open Problem 9). Any layer-assignment argument must admit block-swaps in the top q-group, not only in the cyclic middle layer, or it will miss the wreath forms and understate the target.
2. **(Beat 0.049 for odd n.)** δ₀^{odd} is no longer an unknown constant to compute — Prop. 5.3 gives δ(a,b) = 2a/(a+b+√(2a))², maximized at 0.0486 by the (4,6) chain, with 0.0625 unreachable because (2,4) is mod-3 dead. So the problem is now: **find any odd-n family beating 0.049.** Every three-block chain is capped by Prop. 5.3, so an improvement must be structurally different — four blocks, a twisted bottom block, or a design evading the (a+b)q < n budget that caps γ. Still open alongside: whether the density-1/2 ceiling of §2 is approached on families other than n = 2·(prime power). The n = 2·(odd prime power) family is **closed** by Theorem 2.1 at exactly n(n−2)/4.
3. **(Number theory — the attackable frontier.)** "Almost all n" is a friendlier regime than "all large n": Montgomery–Vaughan exceptional-set technology proves almost-all binary Goldbach unconditionally. The safe-prime rung cannot ride this (infinitude of safe primes is open), but intermediate rungs might: primes p with a prime factor of p−1 exceeding p^θ have unconditionally positive relative density for θ up to ≈ 0.67 (Fouvry; Baker–Harman lineage). If binary Goldbach restricted to this positive-density prime set yields to exceptional-set methods — the nontrivial input is a level-of-distribution theorem for the restricted set — the consequence is **μ(n) ≥ n^{1.67−o(1)} for almost all n, unconditionally**, beating the Chowla-saturated pointwise 3/2 barrier in the almost-all sense. Separately: effectivize anything (à la Helfgott for ternary Goldbach) and record the computational verification of the covering-chain representations up to a large explicit bound.
4. **(Formalization.)** Make the §4 oracle-architecture barrier a theorem about a delimited proof class.
5. **(Small-n closure, re-scoped by §8.12.)** The CSP cannot settle a fixed n, since the global χ condition is not expressible on catalog variables and a solution does not determine a property. What remains productive: (a) χ of the two structural closures at n = 10, finishing the §8.4 minimal-completion screen; (b) the n = 12 battery — UNSAT would give the first unconditional composite non-prime-power ARK value beyond 6, SAT yields a skeleton to χ-test; (c) sampling solutions with `--seed` and χ-testing their minimal extensions, as evidence rather than proof; (d) the dual χ-magnitude screen and interval bound of §8.7; (e) run `adversary.py` against ℰ (§8.13) as the negative control before trusting any EVASIVE verdict it returns.
6. **(Down-forcing in general.)** Beyond duality, does any principle derive exclusion of dense-but-incomplete graphs from non-evasiveness at composite n? What is the joint primal-dual forcing invariant μ∪, and do the weak-n dips of μ fill in for it?

7. **(How low can one shape go? — exhaustively decidable at n = 6.)** Is there a nontrivial nonevasive property of shape complexity 1 for some 6 ≤ n ≤ 11? The scorpion supplies n ≥ 12; §9.1 closes n ≤ 5. The search space is shapes, not properties: 25,506 at n = 6 (Burnside), so enumerate them, discard trivial ones, and run the adversary search of §8.12's toolchain. A positive answer is a new smallest scorpion-like construction; a negative answer gives the "n ≥ 12" folklore its first proven data point below 12. n = 7 (2,302,938 shapes) is borderline with a cheap prefilter.

8. **(Monotone shape-1 = BBKN's open class.)** Can "G contains a copy of H" ever be nonevasive? Equivalently (§9.3) is any forbidden-subgraph property Q_n^H nonevasive? Forest H is settled for large n by BBKN's sparse theorem; every nontrivial case is evasive at n ≤ 6 by §9.3; non-bipartite H is provably beyond the μ-method by §9.4, so progress there needs either the recursion route or a genuinely new invariant. Sub-question with a clean shape reading: characterize the H-saturated graphs well enough to bound the *negative* certificate complexity, which is the quantity §9.5 leaves without a formula.

9. **(Finish the coherence optimisation.)** Theorem 2.3 bounds μ(n) unconditionally by a max–min over partitions into prime powers, and §2.4 derives the coherence conditions that the bound ignores — Lemma B (foreign full-capacity orbits are prime with s−1 ∈ {qᵉ,2qᵉ}) and Lemma C (pairwise-coprime independent orders in the cyclic layer). Restoring them turns the bound into a finite arithmetic optimisation over partitions and twist assignments. Lemma B′ already covers partial-capacity *primitive* orbits. What remains: (a) a **canonical, provably exhaustive enumeration** of the permitted (partition, bottom prime, twist assignment) configurations — two plausible enumerations currently differ, 71.0% versus 68.9% of n ≤ 1000 met, because max–min ≤ min–max and the optimisation order matters; (b) the analogue of Lemma C inside **nested imprimitive towers**. Preliminary runs put the achievable exactness near 70% at n ≤ 1000 against Theorem 2.3's 42.7%. Prove that these coherence conditions are *necessary* and §6's equivalence becomes unconditional, with the Hardy–Littlewood systems of §5 as its exact content. The tool that closed the block-structure half should be pushed further here: suborbit divisibility — for a point v in an orbit of size s, the Γ_v-orbits on the rest have sizes dividing |Γ_v| and summing to s−1 — constrains which twist orders can coexist across parts, which is exactly the missing ingredient.

## Appendix A. The invariant table for small n

Columns: **every value here is exact.** The canonical enumeration of §2.6 together with the block-fusion family determines μ(n) at **all** n ≤ 100 and at 791 of the 806 non-prime-powers below 1000 (98.1%); the upper-bound column has been dropped since no gap survives in this range. Computing scripts: **C(n,2)** trivial; **prime power?** — if yes, μ(n) = C(n,2) *exactly* (AGL(1,n) is 2-transitive and Oliver; conversely a Zassenhaus-type argument — orbital-transitive means 2-homogeneous, whose solvable instances are affine of prime-power degree, and whose non-affine instances are non-solvable hence non-Oliver — gives that every Oliver group on non-prime-power n has ≥ 2 u-orbitals, whence μ(n) ≤ ⌊C(n,2)/2⌋: the interval column's upper endpoint, and a density ceiling of 1/2 that the n = 2p wreath rows (two-orbital partitions, e.g. {20, 25} at n = 10) approach from below); **μ(n) / lower bound** — exact minimum-orbital sizes, computed by orbit BFS (`mu_table.py`, which unions the affine template of `oliver_mu.py` — this covers the two-block ladder and the three-block chains of §5, when the relevant primes exist at that n — with the wreath family (𝔽_{p^a} ⋊ C_d) ≀ C_k of §3); **witness** — a group achieving the bound, in the scripts' naming. Exhaustive per-n enumeration beyond these families is the GAP pipeline (`ark_gap.g` → `consume_gap.py`); at n = 10 it confirmed the wreath value 20 as the best over 268 Oliver groups with ≤ 12 orbitals, so the lower bounds below are plausibly tight-ish for the small non-prime-powers, though only the prime-power rows are proven exact.

Reading the table against the framework: prime powers sit at density 1 (KSS's regime); the n = 2·(prime power) rows realize Theorem 2.1's exact value n(n−2)/4 (0.46–0.48 at 14, 18, 22 — a small-n boost over the asymptotic 1/4); and the arithmetically weak composites show up as density dips. The dips share a diagnosis — no large prime-power part and no good two-part split with coherent twists — which makes them the leading candidate locations for weakness in the framework, and hence (per §10) for counterexample search after n = 12. Note that wreath forms rescue several apparently weak values: (4:3)≀3 lifts n = 12 from 0.152 to 0.273 and (7:3)≀3 lifts n = 21 from 0.133 to 0.300, a concrete measure of what the §3 clause is worth.

**The n ≤ 10⁴ extension** (`mu_fast.py`, closed-form orbital sizes over families P/W/D/B2/B3, validated exactly against the BFS values for n ≤ 30; full output `mu_table_full.csv`, 9,999 rows). Over the 8,719 non-prime-powers up to 10⁴ the density μ_lower/C(n,2) has median 0.161, maximum 0.4999 (the diagonal and wreath families pressing against the proven 1/2 ceiling), and minimum 0.0099; no n lacks a construction. Attainment by family: B2 two-block reaches 0.2499 (median 0.211, 5,077 rows), D diagonal 0.4999 (median 0.200, 2,238 rows), W wreath 0.4990 (26 rows), B3 chain **0.0485** (median 0.027, 1,378 rows — every one far below δ₀^{even} = 1/4, as Prop. 5.3 forces).

**The weak tail is a parity effect, not a mod-9 effect.** Read only at n ≤ 30, or even n ≤ 1000, the weak set looks like "odd multiples of 9." At 10⁴ scale that reading is wrong: of the 2,464 composites below the 1/12 diagnostic threshold, only 473 are divisible by 9 (against ~274 expected by chance — a mild bias, not the mechanism), while **2,439 of 2,464 are simply odd**. The dominant signal is parity, explained by the structural starvation of odd n analyzed in §5.5; a small-n window makes that parity effect look like a mod-9 effect. The genuinely weakest rows (n = 1425 at density 0.0099, then 3393, 5457, 5271, 5061, …) are odd n whose only good witness is a chain or a two-power split with a small available twist.

| n | C(n,2) | μ(n) | density | witness |
|---|--------|------|---------|---------|
| 2 | 1 | **1** | 1.000 | AGL(1,2) prime power |
| 3 | 3 | **3** | 1.000 | AGL(1,3) prime power |
| 4 | 6 | **6** | 1.000 | AGL(1,4) prime power |
| 5 | 10 | **10** | 1.000 | AGL(1,5) prime power |
| 6 | 15 | **6** | 0.400 | (3:2)wr2 |
| 7 | 21 | **21** | 1.000 | AGL(1,7) prime power |
| 8 | 28 | **28** | 1.000 | AGL(1,8) prime power |
| 9 | 36 | **36** | 1.000 | AGL(1,9) prime power |
| 10 | 45 | **20** | 0.444 | (5:4)wr2 |
| 11 | 55 | **55** | 1.000 | AGL(1,11) prime power |
| 12 | 66 | **18** | 0.273 | (4:3)wr3 |
| 13 | 78 | **78** | 1.000 | AGL(1,13) prime power |
| 14 | 91 | **42** | 0.462 | 2x(7:6)blockfused |
| 15 | 105 | **30** | 0.286 | 3x(5:4)blockfused |
| 16 | 120 | **120** | 1.000 | AGL(1,16) prime power |
| 17 | 136 | **136** | 1.000 | AGL(1,17) prime power |
| 18 | 153 | **72** | 0.471 | (9:8)wr2 |
| 19 | 171 | **171** | 1.000 | AGL(1,19) prime power |
| 20 | 190 | **40** | 0.211 | 4x(5:4)blockfused |
| 21 | 210 | **63** | 0.300 | (7:3)wr3 |
| 22 | 231 | **110** | 0.476 | 2x(11:10)blockfused |
| 23 | 253 | **253** | 1.000 | AGL(1,23) prime power |
| 24 | 276 | **84** | 0.304 | 3x(8:7)blockfused |
| 25 | 300 | **300** | 1.000 | AGL(1,25) prime power |
| 26 | 325 | **156** | 0.480 | 2x(13:12)blockfused |
| 27 | 351 | **351** | 1.000 | AGL(1,27) prime power |
| 28 | 378 | **84** | 0.222 | 4x(7:6)blockfused |
| 29 | 406 | **406** | 1.000 | AGL(1,29) prime power |
| 30 | 435 | **78** | 0.179 | AGL(1,13)xF17:C16 |

## Appendix B. Glossary

Terms are grouped by where they come from. Several that read as binary are in fact **graded**; those carry their grading formula.

### Permutation-group vocabulary (standard)

- **orbital** (here always *u-orbital*): an orbit of Γ on unordered pairs of points — equivalently a Γ-invariant graph that cannot be split. For transitive Γ each orbital has a common **valency** d, the number of Ω-neighbours of a vertex, and |Ω| = n·d/2.
- **m\*(Γ)**: the smallest orbital of Γ. **μ(n)**: the largest m\*(Γ) over Oliver groups of degree n. **density**: m\*/C(n,2), so 1 for prime powers and at most 1/2 otherwise.
- **block system, imprimitive, primitive**: a Γ-invariant partition into equal blocks; imprimitive means one exists nontrivially. **suborbit**: an orbit of a point stabiliser; the suborbit sizes are the orbital valencies and sum to n−1.

### The Oliver chain

- **Oliver's condition / Oliver group**: a chain Γ₂ ◁ Γ₁ ◁ Γ with Γ₂ a **p**-group, Γ₁/Γ₂ cyclic, and Γ/Γ₁ a **q**-group. Any layer may be trivial.
- **bottom prime p**, **cyclic layer** Γ₁/Γ₂, **top prime q**. These are fixed once for the whole group and are inherited by every orbit and block (Lemma A, G.1) — most of the coherence conditions are consequences of that single fact.

### Configuration vocabulary

A **configuration** is what the enumeration ranges over: a choice of (p, q) and orbits n = Σ Fᵢcᵢ with twists. **Certified** means the Part F stopping criterion 1/√δ ≤ K has been met, so no larger configuration can win.

- **part / orbit**: one Γ-orbit, of size F·c.
- **p-characteristic vs foreign** — *binary*. An orbit is p-characteristic if its finest block has characteristic equal to the bottom prime p, foreign otherwise. Lemma B′: a foreign orbit's finest block must be of **prime** size with a twist that is a power of q.
- **foreign prime**: the size r of a foreign part. Always prime, never repeated across orbits (two copies would put C_r × C_r in the cyclic layer).
- **twist**: the multiplicative part of an affine block 𝔽_c ⋊ T, T ≤ 𝔽_c^\*. The **twist order** is |T| = d. *Graded* by **d/(c−1)**, the fraction of the multiplicative group used: 1 means the block is 2-homogeneous and its whole intra-orbital is a single class of size C(c,2).
- **twist prime**: the top prime q, so named because Lemma B′ forces every *foreign* twist order to be a power of it. For a p-characteristic block the twist is unconstrained and lives in the cyclic layer instead.
- **fused / fusion count F** — *graded*. A top-group element permuting several blocks merges their separate intra-orbitals into one, multiplying the orbital size by the number of blocks merged. F is always a power of q (a transitive q-group has q-power degree), and F = 1 means unfused. Tower depth contributes nothing beyond F (G.2).
- **capacity** cap(s): the largest possible minimum intra-orbital of an orbit of size s, given by the recursion of Part C.

### Arithmetic vocabulary

- **prime power**: p^a with a ≥ 1. Blocks are always of prime-power size, because solvable primitive groups have prime-power degree.
- **shifted prime**: r − 1 for r prime (occasionally r + 1). Nearly every arithmetic condition in these notes is a condition on the *factorisation of r − 1*, which is why the subject reduces to Hardy–Littlewood-type statements rather than to primality alone.
- **q-part** of x: the largest power of q dividing x.
- **safe prime**: r = 2q + 1 with q prime. **Fermat prime**: r = 2^k + 1 (only 3, 5, 17, 257, 65537 are known).
- **foreign-block efficiency** — *the key spectrum*. For a foreign prime r under top prime q, the usable twist is t = (q-part of r−1), and the intra-orbital is r·|±δT|/2 against a maximum of C(r,2). So

> **eff(r, q) = (t if t is even, else 2t) / (r − 1) ∈ (0, 1]**,

> and **eff = 1 exactly when r − 1 = qᵉ or 2qᵉ** — which is precisely Lemma B′'s condition, i.e. the case where restricting foreign twists to q-powers costs nothing. Fermat primes achieve it with q = 2 (r − 1 a pure 2-power); safe primes achieve it with t = q odd and 2t = r − 1; and the general full-efficiency blocks are r = 2qᵉ + 1, e.g. 163 = 2·3⁴+1 and 251 = 2·5³+1. Measured over the winning configurations below n = 685, **74.8% of foreign blocks used have efficiency 1**, the commonest being 227, 163, 257, 107, 263 — safe primes, Fermat primes, and the r = 2qᵉ+1 generalisation.

### Method vocabulary

- **orbital annihilation**: the sparse criterion — if every member of P has fewer than m\*(Γ) edges then no nonempty invariant graph lies in P, so the fixed complex is void.
- **transversal condition** (§9.7): a non-evasive nontrivial monotone P must contain at least one orbital of *every* Oliver group.
- **battery**: the set of groups whose conditions the CSP enforces. **catalog**: the isomorphism classes those groups constrain (1,242 of 12,005,168 at n = 10). **skeleton**: the monotone closure of a solution's maximal graphs. **backbone**: the classes forced IN or OUT across all solutions. **primal / dual**: a condition and its complement-reflected image under the involution of §8.9.
- **ladder / rung**: the sequence of conditional constructions of §5, each rung a stronger arithmetic hypothesis buying a larger exponent.

### Topology and metaproperties

- **evasive**: worst-case query complexity is exactly C(n,2). **collapsible, contractible, ℤ-acyclic, 𝔽_p-acyclic**: the rungs of §7.1, in decreasing strength.
- **fixed complex** Δ_P^Γ: the subcomplex of Γ-invariant members of P — exactly the unions of orbitals lying in P.
- **metaproperty**: a property of graph properties (evasiveness, monotonicity, sparseness); §7 organises the ones this framework uses.

### Shape calculus (§9)

- **shape**: an S_n-orbit of a three-state assignment (present / absent / irrelevant) to the edges — essentially a **trigraph** in Chudnovsky–Seymour's sense, but with the undecided pairs unrestricted. **shape complexity**: fewest shapes whose union is the property, equal to minimum DNF size; the maximal shapes inside a property are its **prime implicants**. **fsc**: the same with negated shapes allowed.

## References (indicative)

- L. Babai, A. Banerjee, R. Kulkarni, V. Naik, *Evasiveness and the distribution of prime numbers*, STACS 2010; arXiv:1001.4829.
- I. Shparlinski, *Evasive properties of sparse graphs and some linear equations in primes*, Theoret. Comp. Sci. (2015).
- J. Kahn, M. Saks, D. Sturtevant, *A topological approach to evasiveness*, Combinatorica 4 (1984).
- A. Chakrabarti, S. Khot, Y. Shi, *Evasiveness of subgraph containment and related properties*, SIAM J. Comput. 31 (2001).
- R. Oliver, *Fixed-point sets of group actions on finite acyclic complexes*, Comment. Math. Helv. 50 (1975).
- H. Zassenhaus, *Über endliche Fastkörper*, Abh. Math. Sem. Hamburg 11 (1935).
- F. H. Lutz, *Examples of Z-acyclic and contractible vertex-homogeneous simplicial complexes*, Discrete Comput. Geom. 27 (2002).
- C. A. Miller, *Evasiveness of graph properties and topological fixed-point theorems*, Found. Trends TCS 7 (2013).
- R. Kulkarni, *Evasiveness through a circuit lens*, ITCS 2013.
- S. Bouc, *Homologie de certains ensembles de 2-sous-groupes des groupes symétriques*, J. Algebra 150 (1992) (matching-complex homology, relevant to §8.4).
- M. Adamaszek, *The smallest nonevasive graph property*, arXiv:1303.5601 (2013) (§8.13).
- P. Erdős, A. Hajnal, J. W. Moon, *A problem in graph theory*, Amer. Math. Monthly 71 (1964) (saturation numbers; sat(n,K_p); §9.4).
- M. Chudnovsky, P. Seymour, *Claw-free graphs I–V* (trigraphs, semiadjacent pairs, realizations; §9.0).
- M. C. Golumbic, H. Kaplan, R. Shamir, *Graph sandwich problems*, J. Algorithms 19 (1995) (§9.0).
- W. V. Quine (1952, 1955); E. J. McCluskey (1956) (prime implicants, minimum DNF cover; §9.0).
- Y. Crama, P. L. Hammer, *Boolean Functions: Theory, Algorithms, and Applications*, CUP 2011 (monotone prime implicants = minimal true points; §9.0, §9.2).
- C. Umans, *The minimum equivalent DNF problem and shortest implicants*, JCSS 63 (2001); and the monotone case (PP-completeness) (§9.0).
- P. Erdős, A. H. Stone, *On the structure of linear graphs*, Bull. AMS 52 (1946) (ex(n,H) for non-bipartite H; §9.4).
- W. Mantel (1907) / P. Turán (1941) (ex(n,K₃) = ⌊n²/4⌋; §9.4).
- M. R. Best, P. van Emde Boas, H. W. Lenstra, *A sharpened version of the Aanderaa–Rosenberg conjecture*, Math. Centrum Amsterdam ZW 30/74 (1974) (scorpion; the D(f) ≥ deg(f) bound of §8.12).
- D. Grieser, *Some results on the complexity of families of sets*, (scorpion complexity ≤ 6n − 10, sharpened to ≈ 6n − √(2n) − 6; §8.10).
- E. C. Milner, D. J. A. Welsh, *On the computational complexity of graph theoretical properties*, Proc. 5th British Comb. Conf. (1976).
