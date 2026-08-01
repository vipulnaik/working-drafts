# The arithmetic of the density ladder

*Supplement to `orbital-evasiveness-notes.md` and `enumeration-proof.md`. Where those two ask what μ(n) is and prove that the enumeration computes it, this one asks **which arithmetic conditions on n control the answer**, sets up the Hardy–Littlewood and Bateman–Horn machinery that governs them, and checks the predictions against the 1,848 exactly computed values. Written after the exact values became available, which changes the picture: statements that used to be conjectures about a construction menu can now be tested against μ itself.*

**Status labels as in the other documents.** *Verified* — an independent computation agreed. *Sound* — argued and read, no independent computation. *Heuristic* — a singular-series prediction, i.e. conditional on Hardy–Littlewood or Bateman–Horn.

---

## 1. The thesis, in one page

The framework has **two arithmetic engines**, and they are of different kinds.

> **The multiplicative engine.** A single **fused class** — F blocks of size c permuted by the top q-group, with n = F·c, F a power of q and c a prime power — achieves density **1/F**. It requires n to have at most two distinct prime factors, and it is the only structure that breaks density 1/4.
>
> **The additive engine.** k unfused parts, balanced, achieve density **1/k²** and no more. Two parts need n = c + r with c a prime power and r a prime; three parts need n = 2c + r. These are Hardy–Littlewood conditions, and they carry all the number theory.

Everything else in this document elaborates that split. Three consequences set the agenda:

1. **The density ladder's thresholds are the engine caps, not artefacts.** 1/2 and 1/3 are fused-class values at F = 2 and F = 3; **1/4 is the two-part cap; 1/9 is the three-part cap; 1/16 is the four-part cap.** The thresholds that appear throughout the other two documents — δ₀^even = 1/4, Theorem E.1's 1/9, Corollary F.3's 1/16 — are all the same quantity read at different k.
2. **The parity asymmetry is multiplicative in origin, not additive.** Even n has 2 | n, so F = 2 is available whenever n/2 is a prime power, giving density 1/2. Odd n has F ≥ 3, capping the multiplicative engine at 1/3; and its two-part route needs the *even* part to be a power of 2, which is scarce. So odd n loses on both engines at once — and the loss is a matter of caps, not of representation counts: both Bateman–Horn systems supply ~n/log³n where they are soluble at all (§§3.1–3.3).
3. **The ladder's hypothesis is checkable, not merely conjectural.** Whether a given n admits the representation its family needs costs O(n/log n) to decide, against n^2.9 to compute B(n). Verified to 10⁷, with no failure above n = 96,568 and none new beyond 2×10⁵ (§3.5), so the conditional statements are unconditional over a range two orders of magnitude past the table.
4. **The ceiling splits by residue class mod 12, for both parities**, from local obstructions at ℓ = 2 and ℓ = 3 — and those are the only two moduli that can obstruct, because each system is three linear polynomials so ω(ℓ) ≤ 3 < ℓ for ℓ ≥ 5. Six distinct constants result, from 1/4 down to 0.05051, each met by the constructions to within 2% (§3.3).
5. **One global floor covers everything.** Collapsing the six class constants and the finite exceptional set into a single number: **δ(n) ≥ 0.02 for every composite non-prime-power n**, conjecturally, with the observed floor 0.02504 at n = 3239 and the extremal class n ≡ 11 (mod 12) throughout (§5).
6. **The multiplicative engine covers a density-zero set, so asymptotically the additive engine is everything.** The fraction of n with ω(n) = 2 thins like log log n / log n — measured at 52% below 2000 but 29% near 10⁶. So the asymptotic behaviour of μ is governed entirely by the Hardy–Littlewood side, and the observed density floor should be expected to drift downward as the fused family's reach recedes.

---

## 2. The two engines, exactly

### 2.1 The multiplicative engine: density 1/F

Let n = F·c with F a power of q and c a power of p. The single fused class has intra-orbital F·C(c,2), within-class cross (F or F/2)·c², and no other terms, so

> m\* = F·C(c,2) = F·c(c−1)/2, and **δ = m\*/C(n,2) = (c−1)/(Fc−1) → 1/F.**

Two things follow immediately. Since a fused class needs F ≥ q ≥ 2, the engine cannot exceed **1/2**. And since n = F·c with both factors prime powers forces **ω(n) ≤ 2**, it is available only on that set.

To maximise, take F to be the **smallest prime-power cofactor** of n — the least F such that F and n/F are both prime powers.

> *Verified.* Over all 733 one-part winners in the table, the predicted density 1/F agrees with the computed value to O(1/n), with no exceptions. By F: 184 rows at F = 2 with median density 0.4994, 137 at F = 3 with median 0.3325, 105 at F = 4 with 0.2491, 88 at F = 5 with 0.1991, 62 at F = 7 with 0.1419, 39 at F = 9 with 0.1102. Maxima 0.49977, 0.33300, 0.24960, 0.19960, 0.14240, 0.11060 against 1/F = 0.5, 0.3333, 0.25, 0.2, 0.1429, 0.1111.

> *Verified.* All 733 one-part winners have ω(n) = 2, and **no** value with ω(n) ≥ 3 has a one-part winner. Of the 1,045 table values with ω(n) = 2, 733 are one-part winners and the other 312 do better with a split.

**Why fusion is worth a factor of F.** F *unfused* equal parts of size c give min(C(c,2), c²) = C(c,2) ≈ n²/(2F²), density 1/F². Fusing them replaces the mutual capping by a single intra term F·C(c,2), density 1/F. So fusion buys exactly F, which is why reduction (R1) of the proof document — merge equal-size classes when F₁ + F₂ is a q-power — is the single most valuable simplification in the search, and why the enumeration's winners are so often a single fused class.

### 2.2 The additive engine: density 1/k²

For k unfused parts of sizes sᵢ summing to n, the between-orbit classes sᵢsⱼ and the intra terms C(cᵢ,2) cap each other. Proposition F.1 of the proof document gives k < 1/√δ; read backwards,

> **k parts ⟹ δ < 1/k²**, and the bound is saturated by balanced parts.

> *Verified, and tight.* Maximum observed density is 0.24939 among two-part winners and 0.11037 among three-part winners; **no two-part winner exceeds 1/4 and no three-part winner exceeds 1/9**, over 875 and 240 rows respectively. Medians 0.1985 and 0.0915.

So the ladder of thresholds is one sequence: 1/4, 1/9, 1/16 at k = 2, 3, 4. The 1/9 above which Theorem E.1 settles the collapse, and the 1/16 above which Corollary F.3 gives k ≤ 3, are not independently chosen constants; they are the points at which the next part count becomes possible.

### 2.3 The two engines cover complementary sets

| | condition on n | density | share of table |
|---|---|---|---|
| fused, one class | n = F·c, both prime powers (so ω(n) ≤ 2) | 1/F, up to 1/2 | 678 rows |
| two parts | n = c + r\*, c a prime power, r prime | ≤ 1/4 | 793 rows |
| three parts | n = 2c + r\*, c a prime power, r prime | ≤ 1/9 | 201 rows |

> *Verified.* Every one of the 347 table values with density above 1/4 has ω(n) = 2 and a one-part winner. Maximum density over all 803 values with ω(n) ≥ 3 is 0.2493 — the two-part cap.

**So density above 1/4 is a purely multiplicative phenomenon**, and everything at or below it is additive and therefore Hardy–Littlewood.

---

## 3. The Hardy–Littlewood conditions, family by family

The additive families need simultaneous prime and prime-power values, so the right general tool is Bateman–Horn. Write the singular series for a system of polynomials f₁, …, f_k with product f as

> 𝔖(f₁,…,f_k) = ∏_p (1 − ω_f(p)/p)·(1 − 1/p)^{−k},  ω_f(p) = #{a mod p : f(a) ≡ 0}.

### 3.1 Two parts at even n, and why 1/4 needs a safe prime

To reach the two-part cap the configuration needs c ≈ r ≈ n/2 with the foreign block at **full efficiency**: cap(r) = C(r,2) requires the twist to have order (r−1)/2 or r−1, and Lemma B′ forces it to be a power of the top prime q. So r − 1 = 2qᵉ or qᵉ. The clean case is **r a safe prime** — r = 2s + 1 with s prime, so q = s, e = 1 — which is why safe primes are the objects the notes keep returning to.

The representation required at even n is therefore: **n = c + r with c a prime power near n/2 and r a safe prime near n/2.** Taking the leading case c prime, this is the Bateman–Horn system

> f₁(x) = x,  f₂(x) = (x−1)/2,  f₃(x) = n − x

— r, its Sophie Germain partner, and the complementary prime — so the predicted count of representations is

> R₂(n) ~ 𝔖₃(n) · n / (2 log³ n),  with 𝔖₃(n) = ∏_{p>2} (1 − ω(p)/p)(1 − 1/p)^{−3}, ω(p) = 3 for p ∤ n(n−2) and correspondingly fewer otherwise.

The exponent is what matters: **three log factors, so ~n/log³n representations.** Existence is therefore not the binding constraint at even n where the system is locally soluble; the count grows. *Heuristic*, and unproven in every case — a ternary problem with two of the three conditions on the same variable, beyond current technology in the same way binary Goldbach is.

> **Even n carries an ℓ = 3 obstruction.** Substituting r = 2s+1, the system is {s, 2s+1, n−2s−1}, with roots mod 3 at s ≡ 0, 1 and 2(n−1). These are distinct — so ω(3) = 3 and the singular series vanishes — exactly when **n ≡ 2 (mod 3)**. Re-optimising at the reduced efficiency gives x² = (1−x)²/3, hence x = 1/(1+√3) and **cap = 1/(1+√3)² ≈ 0.13397**. So δ₀^even = 1/4 holds for n ≢ 2 (mod 3), and 0.13397 otherwise.

### 3.2 Three parts at odd n: the family, and its ceilings

Odd n cannot use a balanced two-part split: c + r odd forces one part even, and an even prime foreign part must be 2, which is useless. So the even part would have to be the p-characteristic one, i.e. c = 2^a, leaving only ~log₂n candidate splits. That route is genuinely scarce.

The route that avoids it is **three parts with two equal p-characteristic blocks**: n = 2c + r with c an odd prime power and r an odd prime, all parts odd. This is what the enumeration overwhelmingly finds — **200 of the 240 three-part winners** have exactly this shape — and it is *not* the family §5 of the notes analyses (see §3.3). Balancing gives the cap 1/9 at c ≈ r ≈ n/3.

**Full efficiency is obstructed locally, and the obstructions split the ceiling by residue class.** Write **η** for a foreign block's efficiency, η = orb(r, t)/C(r,2) with t the q-part of r − 1 — the fraction of full 2-homogeneous capacity its twist reaches. (η rather than e, to keep clear of Euler's number.) Efficiency η = 1 requires the foreign twist to have order (r−1)/2, which Lemma B′ forces to be a power of q — so (r−1)/2 must be a prime power, the clean case being r a safe prime. Which n admit it, and at what efficiency, is settled in §3.3. Re-optimising δ(x) at reduced efficiency gives the other ceilings in closed form:

> at **η = 1/2**: δ(x) = min(x², 2x(1−2x), (1−2x)²/2) is maximised where x√2 = 1−2x, i.e. **x = 1/(2+√2) ≈ 0.29289**, giving **1/(2+√2)² = (2−√2)²/4 ≈ 0.08579**;
> at **η = 1/3**: **≈ 0.07180** at x ≈ 0.2679.

Where the family is locally soluble the predicted representation count is ~𝔖₃(n)·n/log³n, with

> 𝔖₃(n) = ∏_{p>2} (1 − ω(p)/p)(1 − 1/p)^{−3},  ω(p) = #{r mod p : r(r−1)(n−r) ≡ 0},

so ω(p) = 3 for p ∤ n(n−2) and smaller on the divisors, with the 2-adic and 3-adic factors as computed in §3.3. *Heuristic*, and unproven — a ternary system with two conditions on the same variable, out of reach for the same reasons as binary Goldbach.

### 3.3 Local solubility, and the ceiling by residue class

Full efficiency needs (r−1)/2 to be a prime power, so with r prime and c = (n−r)/2 a prime power the requirement is a Bateman–Horn system in one variable,

> f₁(r) = r,  f₂(r) = (r−1)/2,  f₃(r) = (n−r)/2,

of the same three-condition shape as the even case. Its singular series is positive iff ω(ℓ) < ℓ at every prime ℓ. For **odd ℓ** the forbidden residues are r ≡ 0, 1, n — a set of size at most three — so **only ℓ = 3 can be fatal**, and it is fatal exactly when **n ≡ 2 (mod 3)**. At **ℓ = 2** the division by 2 must be handled directly: full efficiency wants (r−1)/2 odd, so r ≡ 3 (mod 4), and then c = (n−r)/2 is odd only when **n ≡ 1 (mod 4)**; for n ≡ 3 (mod 4) the alternative r ≡ 1 (mod 4) gives 4 | r−1 and caps the efficiency at 1/2.

**Only ℓ = 2 and ℓ = 3 can obstruct, and no prime power beyond them.** Two facts, both needed.

*No prime beyond 3.* Each family's system is three *linear* polynomials in one variable, and a linear polynomial has at most one root mod ℓ, so **ω(ℓ) ≤ 3 for every ℓ**. An obstruction requires ω(ℓ) ≥ ℓ, hence ℓ ≤ 3. Brute-force confirmation over all residues and all ℓ < 500 finds none, as the argument requires.

*No higher power of 2 or 3 either.* The singular series is a product of local densities σ_ℓ = (1 − ω(ℓ)/ℓ)(1 − 1/ℓ)^{−3}, one factor per **prime**, and ω(ℓ) counts roots mod ℓ only. Nothing is imposed mod ℓ²: the local condition being enforced is "f_i(s) is not divisible by ℓ", and divisibility by ℓ is decided mod ℓ. A residue s mod ℓ that avoids all three roots already guarantees ℓ ∤ f_i(s) whatever s is mod ℓ². So there is no obstruction at 8, at 9, or at any higher power.

*Then why do the conditions read mod 4 and mod 3 in terms of n?* Purely the change of variable. The system lives in s, with r = 2s+1 and (for odd n) c = m − s where m = (n−1)/2. The ℓ = 2 condition is a condition on **m mod 2**, and since m = (n−1)/2 that is a condition on **n mod 4**. The ℓ = 3 condition is on m mod 3, and 2 is invertible mod 3, so it is a condition on **n mod 3**. Hence mod 12 in n, with nothing finer available. Verified empirically: representability rates computed modulo 24, 36, 48, 72 and 144 show no spread within a fixed class mod 12 beyond sampling noise. The efficiency available in each class then follows from the structure of r − 1: writing r − 1 = 2^a·u with u odd and L the largest prime power dividing u, the best top prime gives

> **η = max(1/u, L/(2^{a−1}u))**, so **η = 1 exactly when a = 1 and u is a prime power** (the safe-prime-like case r − 1 = 2q^e).

The ℓ = 2 obstruction forces a ≥ 2 and hence η ≤ 1/2; the ℓ = 3 obstruction forces 3 | u and hence η ≤ 1/3 generically; both together give η ≤ 1/6.

> **The density ladder, complete by residue class mod 12.** Every entry is derived, not fitted; the "observed" column is the largest density attained in the computed table by a winner whose foreign block runs at the generic efficiency for its class.
>
> | n mod 12 | parity | family | ℓ=2 | ℓ=3 | η | **exact cap** | decimal | observed | ratio |
> |---|---|---|---|---|---|---|---|---|---|
> | 0, 4, 6, 10 | even | c + r | — | — | 1 | **1/4** | 0.25000 | 0.24939 | 0.998 |
> | 2, 8 | even | c + r | — | ✗ | 1/3 | **(2 − √3)/2** | 0.13397 | 0.13374 | 0.998 |
> | 1, 9 | odd | 2c + r | — | — | 1 | **1/9** | 0.11111 | 0.11037 | 0.993 |
> | 3, 7 | odd | 2c + r | ✗ | — | 1/2 | **(3 − 2√2)/2** | 0.08579 | 0.08565 | 0.998 |
> | 5 | odd | 2c + r | — | ✗ | 1/3 | **(2 − √3)²** | 0.07180 | 0.07043 | 0.981 |
> | 11 | odd | 2c + r | ✗ | ✗ | 1/6 | **(5 − 2√6)/2** | 0.05051 | 0.05036 | 0.997 |
>
> All six are the same formula. Balancing x² against η(1−kx)² gives x\* = √η/(1 + k√η), where k = 1 for the two-part family and k = 2 for the three-part, so
>
> > **cap = η/(1 + k√η)²**,
>
> and each rationalises to an integer denominator as tabulated. The class-5 value is a perfect square, (2 − √3)² = 7 − 4√3. In every case the cross term 2x\*(1 − kx\*) exceeds the cap, so the minimum is genuinely the intra/foreign balance and not the cross class.
>
> The obstructed classes admit **sparse escapes** — the ℓ=3 classes when (r−1)/2 or c is a power of 3, the ℓ=2 classes when c is a power of 2 — which lift individual n to the unobstructed cap. In range these occur at 30, 49, 24 and 5 values in classes 2, 8, 5, 11 respectively and at **none** in classes 3 and 7. Each pins n near 2·3^k, 4·3^k or 2^k, so they are available at O(log n) values of n and do not affect the asymptotic constants.

*How this is validated, and why the maximum alone would not do it.* A class maximum meeting its cap only shows the cap is **attainable**; it is met whenever some n in the class happens to have a good representation, and would go on being met even if a further condition were quietly suppressing most of the class. Two stronger checks are therefore needed, and both pass.

*Upper: no row exceeds its own cap.* Computing each winner's actual efficiency from its own foreign block and top prime, and comparing its density against cap(η) for that efficiency: over all **1,112** two- and three-part winners, **zero exceed it**. So δ(x) = min(x², 2x(1−kx), η(1−kx)²) bounds every individual row, not just the extremes.

*Lower: the distribution is uniform across classes.* An unmodelled obstruction acting on some class would show as that class failing to reach its cap, or as its bulk sitting systematically lower than its siblings'. Restricting to additive-family winners running at their class's generic efficiency, and normalising by the class cap:
>
> | n mod 12 | rows | min | median | max |
> |---|---|---|---|---|
> | 0 | 172 | 0.471 | 0.885 | 0.998 |
> | 1 | 50 | 0.798 | 0.930 | 0.993 |
> | 2 | 54 | 0.453 | 0.836 | 0.997 |
> | 3 | 37 | 0.736 | 0.920 | 0.998 |
> | 4 | 121 | 0.537 | 0.887 | 0.994 |
> | 5 | 18 | 0.637 | 0.894 | 0.981 |
> | 6 | 178 | 0.555 | 0.870 | 0.995 |
> | 7 | 30 | 0.644 | 0.909 | 0.990 |
> | 8 | 63 | 0.487 | 0.853 | 0.998 |
> | 9 | 71 | 0.594 | 0.897 | 0.992 |
> | 10 | 89 | 0.485 | 0.851 | 0.988 |
> | 11 | 4 | 0.814 | 0.936 | 0.997 |
>
> **Every class reaches 0.98–1.00 and none exceeds 1**, and the medians (0.84–0.94) and minima (0.45–0.81) are indistinguishable between obstructed and unobstructed classes. The spread below the cap is representation *availability* — the Hardy–Littlewood side, which varies with n and not with its residue class — so there is no residual class-dependent effect to explain.

**The ℓ = 3 obstruction has a sparse escape.** If (r−1)/2 or c is itself a power of 3, full efficiency returns, because the divisibility that kills primality is harmless for prime powers. In range this lifts n ≡ 5 (mod 12) to a maximum of 0.10975 — but 22 of those 35 rows use the *same* foreign prime r = 487, with (r−1)/2 = 243 = 3⁵, and the others use r = 163 with 81 = 3⁴ or c = 243, 729. Candidates of the form r = 2·3^k + 1 are as thin as any other exponential family, so the escape supplies O(log n) candidates rather than n/log³n and should be read as a feature of the computed range. **The generic ceiling 0.0718 is the one to quote asymptotically.**

### 3.4 The balanced window, and why it leaves the singular series intact

Every cap above is attained at a specific balance point — x = c/n equal to 1/2, 1/3, or the values in the table — so the representations that matter are not all representations of n but those in a window around that point. Whether the Bateman–Horn heuristic survives that restriction needs checking, because a window shrinking with n would turn each of these into a short-interval problem and put it out of reach.

It does not shrink. Each δ(x) is continuous with an **interior maximum**, so asking for δ ≥ δ₀ at any δ₀ strictly below the cap confines x to an interval of positive length, and that length is a fixed fraction of n rather than a vanishing one. Taking δ₀ = 0.9 × cap in each class:

| class | family, efficiency | cap | attained at | x-window | width |
|---|---|---|---|---|---|
| 0, 4, 6, 10 | two parts, η = 1 | 0.25000 | 0.5000 | [0.474, 0.526] | 0.052 |
| 2, 8 | two parts, η = 1/3 | 0.13397 | 0.3660 | [0.347, 0.399] | 0.051 |
| 1, 9 | three parts, η = 1 | 0.11111 | 0.3333 | [0.316, 0.342] | 0.026 |
| 3, 7 | three parts, η = 1/2 | 0.08579 | 0.2929 | [0.278, 0.304] | 0.026 |
| 5 | three parts, η = 1/3 | 0.07180 | 0.2680 | [0.254, 0.280] | 0.026 |
| 11 | three parts, η = 1/6 | 0.05051 | 0.2247 | [0.213, 0.239] | 0.026 |

So in every class the count required is of primes in an interval of length **c·n for an absolute constant c between 0.026 and 0.052** — not primes in a short interval. That is exactly the regime where the Hardy–Littlewood and Bateman–Horn heuristics are standard: the predicted count over the window is the full-range prediction times the window's measure, up to the smooth variation of 1/log across it, and no short-interval input is needed. The asymptotic ~𝔖(n)·n/log³n of §§3.1–3.2 therefore stands as written, with 𝔖(n) unchanged and only the constant scaled.

Two caveats, both real and both explaining why the observed maxima of §3.3 fall just short of their caps rather than meeting them.

**Approaching the cap costs.** Requiring δ ≥ (1−ε)·cap confines x to a window of relative width Θ(√ε), so the predicted count degrades like √ε·n/log³n. It stays positive for fixed ε but not uniformly in ε, so the caps are suprema rather than values guaranteed to be attained at any particular n.

**Exact balance is arithmetically impossible anyway.** At the balance point the three-part family needs c = r = n/3 exactly, but r is the foreign prime and c the p-characteristic block size, and admissibility requires r ≠ p. The same obstruction applies to the two-part family at x = 1/2. So the caps are approached and never met, independently of any analytic question.

### 3.5 Effectivity: what the conjectures give, and why the gap is not where it looks

The heuristic survives the window, then, but it remains a *heuristic* — and an asymptotic one. Since the computations of this programme are exact statements about small n, the natural worry is a middle range covered by neither. The worry is real but misplaced, and the resolution matters for how the ladder should be stated.

**Standard Bateman–Horn has no error term at all.** Its content is π_f(x) ~ (1/D)·𝔖(f)·∫₂^x dt/(log t)^k, a bare asymptotic with an ineffective implied constant. It therefore says *nothing whatever* about any specific n, and the uncovered range is not a middle interval that computation can close from below — it is everything above wherever the computation stops, with no upper end.

**Quantitative refinements exist but are the wrong shape.** The conjectured square-root form, π_f(x) = (1/D)·𝔖(f)·Li_k(x) + O_ε(x^{1/2+ε}), is a statement about the *counting function up to x*. Our families need a representation at each individual n, and a count with an error term does not deliver one: an exceptional n contributes O(1) to a count whose error term is a power of x. Nor can one assume uniformity in n to compensate — Friedlander and Granville showed that sufficiently uniform versions of Hardy–Littlewood-type conjectures are false outright, so uniformity is not a free hypothesis.

**But existence at a given n is decidable, and cheap.** This is the point that dissolves the difficulty. What the ladder needs at each n is not an asymptotic count but a single bit: does *some* admissible representation exist? For n = 2c + r that is a sieve computation costing O(n/log n) — against the n^2.9 of computing B(n) itself. The asymmetry is enormous, and it means the ladder's hypothesis can be verified far past the range where μ(n) is known.

> *Verified* (`ladder_verify.py`, 193 s). Over eligible n < 10⁷ — those in the locally soluble classes — a balanced full-efficiency representation fails to exist for:
>
> | family | eligible n < 10⁷ | failures | largest failure | verified from |
> |---|---|---|---|---|
> | odd, n = 2c + r, n ≡ 1 (4) and n ≢ 2 (3) | 1,666,666 | 61 | **28,993** | 28,994 |
> | even, n = c + r, n ≢ 2 (3) | 3,333,332 | 1,196 | **96,568** | 96,569 |
>
> So the ladder's hypothesis holds **unconditionally and by direct verification at every eligible n between 96,569 and 10⁷** — five million values, against a table of B(n) reaching 2,212.
>
> The shape of the failure sets is worth more than the range. Extending the scan from 2×10⁵ to 10⁷ — a factor of fifty, and 4.8 million additional eligible values — produced **not one new failure in either family**: the counts 61 and 1,196 are unchanged, and every failure in both lies below 10⁵. So the exceptional set is not merely sparse but, on this evidence, **finite** — which is the shape the singular-series heuristic predicts (a positive density of representations once n is large enough that ~𝔖(n)·n/log³n exceeds 1) and considerably stronger than anything the asymptotic itself asserts.

So the honest structure of the ladder is not "computed below, conjectural above" with a gap between. It is:

| | range | status |
|---|---|---|
| μ(n) known exactly | n ≤ 2,212 | computed |
| collapse μ(n) = B(n) certified | n ≤ 100,000 | computed, from lower bounds (Part E″ of the proof document) |
| ladder hypothesis verified | n ≤ 10⁷, no failure above 96,568 | computed |
| ladder hypothesis assumed | n > that | conjectural, ineffectively |

**One consistency check worth recording.** The obstructions of §3.3 were derived there from the structure of r − 1 — which twists Lemma B′ permits. They also fall out of the singular series: 𝔖(n) vanishes precisely when ω(2) = 2 or ω(3) = 3, which is exactly n ≡ 3 (mod 4) or n ≡ 2 (mod 3). Two independent routes to the same two classes.

**What would be worth proving instead.** Given that per-n verification is cheap and the asymptotic is ineffective, the statement that would actually add something is an **exceptional-set bound**: not "every large n admits a representation" but "all but O(x^θ) of n ≤ x do", for some θ < 1. Results of that shape are known for binary Goldbach (Montgomery–Vaughan, and subsequently Pintz, with θ well below 1) and are sometimes effective. Combined with verification up to N, an effective exceptional-set bound would give a genuine unconditional density statement about the ladder, which no amount of asymptotic Bateman–Horn can.

## 4. Asymptotics: the multiplicative engine is a thinning exception

The fused family requires ω(n) ≤ 2, which is a **density-zero condition**: the count of n ≤ N with exactly two distinct prime factors is ~N log log N / log N.

> *Verified.* Fraction of composite non-prime-power n with ω(n) = 2, by dyadic block: **52.3%** on [10³, 2·10³), 43.1% on [5·10³, 10⁴), 35.0% on [5·10⁴, 10⁵), 29.8% on [5·10⁵, 10⁶), 28.5% on [10⁶, 2·10⁶).

**The prediction has begun to show up in the table, on both of its halves.** Extending the computed range to n = 2212 moved the density floor off n = 575 for the first time — the new minimum is **0.041107 at n = 2183** — and the thirds of the range behave as the argument requires:

| n | ω(n) = 2 share | median smallest cofactor F | min density |
|---|---|---|---|
| [6, 800) | 64.9% | 4 | 0.04181 |
| [800, 1500) | 53.6% | 5 | 0.04229 |
| [1500, 2212) | 50.8% | **7** | **0.04111** |

Two effects, not one. The ω(n) = 2 population thins, as predicted; and **among the values that remain, the smallest prime-power cofactor grows**, so the 1/F the multiplicative engine delivers shrinks even where the engine applies. n = 2183 = 37·59 is the illustration: ω(n) = 2, so a fused class exists, but only at F = 37, worth 1/37 ≈ 0.027 — which loses to the three-part configuration 1297\* + 443 + 443 at 0.041107. That configuration is itself unbalanced, x = c/n = 0.2029 against the balance point 0.2679 for its class (2183 ≡ 11 mod 12, the ℓ = 3 class), and its binding term is x² = 0.041181, matching B exactly. So the new floor is a value where **both engines are weak at once**: the multiplicative one available but expensive, the additive one locally obstructed and with no balanced representation on offer.

Two consequences, and both should temper how the computed range is read.

**The observed density floor should drift downward.** Fully 57% of the current table has ω(n) = 2, so more than half the computed values are served by an engine whose reach halves over the next few decades of n. The floor of 0.0418 at n = 575, and the median of 0.1995, are both propped up by a population that thins.

**The asymptotic question is entirely Hardy–Littlewood.** Since the multiplicative engine vanishes in density, the asymptotic behaviour of μ(n) for almost all n is set by the additive families, whose caps are 1/4 and 1/9 and whose availability is a Bateman–Horn question. In particular the ladder constants of §5 of the notes — the §3.3 constants — are the right asymptotic quantities, and the fused family's 1/2 and 1/3 are not, however dominant they look in the table.

---

## 5. A single global lower bound

The residue analysis gives six different constants, and the verification of §3.5 leaves a finite exceptional set below 10⁵. It is worth collapsing all of that into one number that should hold everywhere, even at the cost of being loose.

**Where the floor lives.** The worst class is **n ≡ 11 (mod 12)**, the only one carrying both local obstructions, with cap 0.05051. `ladder_verify.py` computes for each n the best density achievable by the three families of §2, scanning the block size over a window wide enough to contain every balance point, x ∈ [0.10, 0.55]. Over all composite non-prime-power n ≤ 2·10⁵ the smallest value is

> **δ ≥ 0.02504, at n = 3239**,

and the eight smallest are **all** in class 11 mod 12. No class is anomalously weak relative to its own cap: the per-class minima of δ/cap run from 0.33 to 0.72, which is the spread expected from representation availability alone. This is a *lower* bound on δ(n) rather than δ(n) itself, since it uses only three families; the true μ-based minimum over the range where B(n) is known is higher, 0.041107 at n = 2183.

**The floor rises with n**, as the singular-series picture requires — once representations near the balance point become plentiful, the achievable density approaches the class cap:

| range | floor |
|---|---|
| [6, 5·10³) | 0.02504 |
| [5·10³, 2·10⁴) | 0.02516 |
| [2·10⁴, 5·10⁴) | 0.03911 |
| [5·10⁴, 10⁵) | 0.04083 |
| [10⁵, 2·10⁵) | 0.04125 |

So the small-n dips are a finite phenomenon, and the asymptotic floor is the class-11 cap.

> **Conjecture (global density floor).** For every composite non-prime-power n,
>
> **μ(n) ≥ C(n,2)/50**,  i.e. **δ(n) ≥ 0.02**,
>
> and asymptotically
>
> **δ(n) ≥ (5 − 2√6)/2 − o(1) = 0.050510…**,
>
> the extremal class being n ≡ 11 (mod 12) — the only one carrying both local obstructions, where the cap is η/(1 + k√η)² at η = 1/6, k = 2.

The constant 1/50 is deliberately loose: the observed floor is 0.02504, so 1/50 carries about 25% margin, and 1/40 = 0.025 would be tight to four decimal places at n = 3239. Two things are being absorbed into that margin — the finite exceptional set of §3.5, whose members fall back on whatever configuration they can find, and the windowing loss of §3.4, which costs a factor Θ(√ε) when the balance point is not exactly available.

**What would refute it.** A single n with δ(n) < 0.02. Nothing below 2·10⁵ comes close: the count of n with δ < 0.02 is **zero**, and the floor 0.02504 at n = 3239 is unchanged between 10⁵ and 2·10⁵. The scan costs O(N²/log N) — 33 s to 10⁵, 190 s to 2.5·10⁵ — so 10⁶ is about an hour and 10⁷ is multi-day; the first is worth doing, the second only if something else motivates it. `ladder_verify.py` reports a checkpoint every 10⁴ and a cumulative summary every 10⁵, so a long run can be watched rather than waited on. What would *prove* the asymptotic half — δ(n) ≥ (5 − 2√6)/2 − o(1) — is an effective exceptional-set bound of the kind §3.5 describes, applied to the class-11 family n = 2c + r with r − 1 = 12q^a.

**Tightening the finite half.** The 0.02 is loose because `ladder_verify.py` computes a *lower bound* on δ(n), not δ(n): it searches three families over a window, and in particular does not model the **fused-plus-foreign** shape (F, c) + r\* that the enumeration frequently prefers. Where both are available the two agree exactly at 1,700 of 1,848 values, and where they differ the scan is low by up to a factor of 2 — at n = 555 it finds 0.07172 against the true 0.14344, whose witness `2x149 + 1x257*` is exactly that missing shape. So the script now writes every n falling below the asymptotic constant to **`ladder_weak.txt`** (2,163 values below 6·10⁴), as a worklist: computing the true B(n) at those n with `mu_enumerate.py` would raise the observed floor, and quite possibly to the point where 0.02 could be replaced by something close to the asymptotic value itself.

## 6. What this says about the open problems

**Open Problem 2** is now sharply posed. The ladder constants are the six values of §3.3, and the question is whether any *family* beats them. Two parts:

**(a) Exceed 1/9 strictly at odd n.** Theorem E.1 of the proof document settles the collapse only *above* density 1/9, and the 2c + r family approaches 1/9 without attaining it — exact balance needs c = r = n/3, and admissibility requires r ≠ p. That gap is exactly what keeps the collapse open at odd n. Per §2.1 the place to look is fusion, which beats splitting by a factor of F.

**(b) Lift the obstructed classes.** The efficiency losses at ℓ = 2 and ℓ = 3 are obstructions to *these* families, not to μ. A family with a different local structure — unequal p-blocks, a fused pair, a foreign block whose twist is a higher q-power — might avoid them. The one worked instance in range is n = 551 = 256 + 167\* + 128, which uses two *distinct* powers of 2 and sidesteps the equal-block form entirely.

Since both Bateman–Horn systems already supply ~n/log³n representations where they are soluble at all, no strengthening of the sieve input helps with either part; this is a question about mechanisms.

**Open Problem 9(a) (k ≤ 3)** is the statement that the four-part cap 1/16 is never the best available. By §2.2 the four-part family is only in play below density 1/16, and by §2.3 that means ω(n) ≥ 3 and no good two- or three-part representation — a triple coincidence whose predicted frequency is the natural next computation. Note that the revised odd-n ceilings of §3.2 are both **above** 1/16, so on that footing the residue is closed for odd n as well as even, leaving only the local-solubility gap.

**Open Problem 9(b) (the collapse below 1/9)** lives exactly in the regime where the three-part family is the best available. That is why it is an odd-n problem, and why δ₀^odd > 1/9 would close it: at density above 1/9 the three-part family is no longer optimal, so the configurations that create the difficulty do not arise.

**The §4 barrier at exponent 3/2** is untouched by any of this, since both engines give density Θ(1) when they apply and the barrier is about proving *lower* bounds on the least prime in an arithmetic progression. The barrier and the caps are independent obstructions.

---

## 7. Open questions specific to this document

1. **Predict the density-1/12 shortfall from the singular series.** §5 of the notes measures 19.3% of odd and 0.9% of even values below 1/12. Both engines' availability is computable heuristically; the comparison would test the whole framework of this document rather than any single family.
2. **Is the four-part family ever optimal?** Equivalently, does the triple coincidence of §5 above ever occur? A negative heuristic estimate would be strong evidence for Open Problem 9(a) even without a proof.
3. **Extend the global-floor scan to 10⁶.** §5 conjectures δ(n) ≥ 0.02 on the strength of a scan to 2·10⁵, where the floor is 0.02504 and nothing is below 0.02. The scan is O(N²/log N), so 10⁶ is roughly half an hour and would either strengthen the conjecture materially or refute it. Beyond that the cost grows faster than the information.
4. **Local solubility of the 2c + r family.** Settled in §3.3 for the classes mod 12; what remains is whether the escapes behave as the O(log n) heuristic says: §5's chain analysis found two of its candidate chains locally dead (one always divisible by 3, one dead whenever 3 | n), so the analogous check is required before the revised ceilings 1/9 and 0.0858 can be quoted as ladder constants rather than as caps.
5. **The fused family at ω(n) = 2 but bad splitting.** 282 of the 960 ω(n) = 2 values do better with a split than with fusion, which happens when the smallest prime-power cofactor F is large. The distribution of F over ω(n) = 2 integers is classical; predicting the 678/282 division is a clean test.
6. **Efficiency below 1.** §5 of the notes tabulates η(r,q) = orb(r, qpart(r−1,q))/C(r,2) and finds efficiency 1 at 77% of foreign blocks. The distribution of the largest prime-power divisor of r − 1 over primes r is a shifted-prime question of Erdős type; its known results should be imported here rather than re-derived.
7. **Does the density floor drift as predicted?** The concrete test: extend the table and check whether the floor tracks the thinning of the ω(n) = 2 population. This is the cheapest available check on §4's central claim, and `wide_cert.py` already reaches n = 10⁵ for the collapse question, so the infrastructure exists.
