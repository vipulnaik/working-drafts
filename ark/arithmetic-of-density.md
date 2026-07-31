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
2. **The parity asymmetry is multiplicative in origin, not additive.** Even n has 2 | n, so F = 2 is available whenever n/2 is a prime power, giving density 1/2. Odd n has F ≥ 3, capping the multiplicative engine at 1/3; and its two-part route needs the *even* part to be a power of 2, which is scarce. This is the correct version of a claim earlier drafts got half-right (§5).
3. **The odd-n ceiling splits by residue class mod 12** — 1/9 on n ≡ 1, 9; ≈ 0.0858 on n ≡ 3, 7; ≈ 0.0718 on n ≡ 5, 11 — from local obstructions at ℓ = 2 and ℓ = 3, each met by the constructions to within 2%. These supersede the older ladder constant 0.049, which was the ceiling of a *different* family (one p-block plus two foreign primes) that the enumeration selects exactly once in 1,848 values.
4. **The multiplicative engine covers a density-zero set, so asymptotically the additive engine is everything.** The fraction of n with ω(n) = 2 thins like log log n / log n — measured at 52% below 2000 but 29% near 10⁶. So the asymptotic behaviour of μ is governed entirely by the Hardy–Littlewood side, and the observed density floor should be expected to drift downward as the fused family's reach recedes.

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

The exponent is what matters: **three log factors, so ~n/log³n representations.** Existence is therefore not the binding constraint at even n; the count grows. *Heuristic*, and unproven in every case — this is a ternary problem with two of the three conditions on the same variable, so it is beyond current technology in the same way binary Goldbach is.

### 3.1a Does the window constraint invalidate the singular series?

Both families require the parts to be *balanced* — c ≈ r ≈ n/2 for two parts, c ≈ r ≈ n/3 for three — so the representation is not being counted over all splits but over a window. This needs stating carefully, because it is the difference between a standard heuristic and a short-interval problem.

Write the two-part split as c = xn, r = (1−x)n and let **e = orb(r,t)/C(r,2)** be the foreign block's efficiency. Then, to leading order,

> δ(x) = min( x², 2x(1−x), e(1−x)² ),

the three terms being the p-block's intra-orbital, the cross class, and the foreign intra-orbital. For three parts with n = 2c + r, c = xn:

> δ(x) = min( x², 2x(1−2x), e(1−2x)² ).

The point is that these are **continuous functions with an interior maximum**, so requiring δ ≥ δ₀ for any δ₀ *strictly below the cap* confines x to an interval of **positive length**, not to a shrinking window:

| family | cap | attained at | x-window for δ ≥ 0.9 × cap | relative width |
|---|---|---|---|---|
| two parts, e = 1 | 1/4 | x = 1/2 | [0.474, 0.526] | 0.052 |
| three parts, e = 1 | 1/9 | x = 1/3 | [0.316, 0.351] | 0.035 |
| three parts, e = 1/2 | 0.0858 | x = 0.293 | [0.278, 0.309] | 0.031 |

So the count needed is of primes r in an interval of length **c·n for an absolute constant c**, not of primes in a short interval. That is exactly the regime in which the Hardy–Littlewood and Bateman–Horn heuristics are standard: the predicted count over the window is the full-range prediction multiplied by the window's measure, up to the smooth variation of 1/log across it, and no short-interval input (no Montgomery–Vaughan, no density hypothesis) is required. The asymptotic ~𝔖(n)·n/log³n therefore stands, with 𝔖(n) unchanged and the constant scaled by the window.

Two caveats, both real.

**Approaching the cap does cost.** Requiring δ ≥ (1−ε)·cap confines x to a window of relative width Θ(√ε), so the predicted representation count degrades like √ε·n/log³n. It stays positive for fixed ε but not uniformly, which is why the caps below are suprema rather than attained values — consistent with the observed maxima falling just short (0.11037 against 1/9, 0.08565 against 0.0858).

**Exact balance is arithmetically impossible anyway.** At three parts, δ = 1/9 needs c = r = n/3, but r is the foreign prime and c the p-characteristic block size, and admissibility requires r ≠ p. So the cap is approached and never met, independently of the analytic question.

### 3.2 Three parts at odd n: the family, and its ceilings

Odd n cannot use a balanced two-part split: c + r odd forces one part even, and an even prime foreign part must be 2, which is useless. So the even part would have to be the p-characteristic one, i.e. c = 2^a, leaving only ~log₂n candidate splits. That route is genuinely scarce.

The route that avoids it is **three parts with two equal p-characteristic blocks**: n = 2c + r with c an odd prime power and r an odd prime, all parts odd. This is what the enumeration overwhelmingly finds — **200 of the 240 three-part winners** have exactly this shape — and it is *not* the family §5 of the notes analyses (see §3.3). Balancing gives the cap 1/9 at c ≈ r ≈ n/3.

**Full efficiency is obstructed locally, and the obstructions split the ceiling by residue class.** Efficiency e = 1 requires the foreign twist to have order (r−1)/2, which Lemma B′ forces to be a power of q — so (r−1)/2 must be a prime power, the clean case being r a safe prime. Which n admit that is computed in §3.3. Re-optimising δ(x) at reduced efficiency gives the other ceilings in closed form:

> at **e = 1/2**: δ(x) = min(x², 2x(1−2x), (1−2x)²/2) is maximised where x√2 = 1−2x, i.e. **x = 1/(2+√2) ≈ 0.29289**, giving **1/(2+√2)² = (2−√2)²/4 ≈ 0.08579**;
> at **e = 1/3**: **≈ 0.07180** at x ≈ 0.2679.

Where the family is locally soluble the predicted representation count is ~𝔖₃(n)·n/log³n, with

> 𝔖₃(n) = ∏_{p>2} (1 − ω(p)/p)(1 − 1/p)^{−3},  ω(p) = #{r mod p : r(r−1)(n−r) ≡ 0},

so ω(p) = 3 for p ∤ n(n−2) and smaller on the divisors; the 2-adic factor is computed separately in §3.3. *Heuristic*, and unproven — a ternary system with two conditions on the same variable, out of reach for the same reasons as binary Goldbach.

### 3.3 Local solubility, and the ceiling by residue class

Full efficiency needs (r−1)/2 to be a prime power, so with r prime and c = (n−r)/2 a prime power the requirement is a Bateman–Horn system in one variable,

> f₁(r) = r,  f₂(r) = (r−1)/2,  f₃(r) = (n−r)/2,

of the same three-condition shape as the even case. Its singular series is positive iff ω(ℓ) < ℓ at every prime ℓ. For **odd ℓ** the forbidden residues are r ≡ 0, 1, n — a set of size at most three — so **only ℓ = 3 can be fatal**, and it is fatal exactly when **n ≡ 2 (mod 3)**. At **ℓ = 2** the division by 2 must be handled directly: full efficiency wants (r−1)/2 odd, so r ≡ 3 (mod 4), and then c = (n−r)/2 is odd only when **n ≡ 1 (mod 4)**; for n ≡ 3 (mod 4) the alternative r ≡ 1 (mod 4) gives 4 | r−1 and caps the efficiency at 1/2.

`local_solubility.py` enumerates this. The resulting ceilings, with the observed maxima from the table:

| n mod 12 | obstruction | efficiency | ceiling | observed max | ratio | rows |
|---|---|---|---|---|---|---|
| 1, 9 | none | 1 | **1/9 = 0.11111** | 0.11037, 0.11019 | 0.993, 0.992 | 43, 62 |
| 3, 7 | ℓ = 2 | 1/2 | **1/(2+√2)² = 0.08579** | 0.08565, 0.08496 | 0.998, 0.990 | 29, 25 |
| 5, 11 | ℓ = 3 | 1/3 | **0.07180** | 0.07043, 0.07058 | 0.981, 0.983 | 35, 5 |

Every class is met to within 2%, so these are ceilings of the mechanism rather than artefacts of search.

**The ℓ = 3 obstruction has a sparse escape.** If (r−1)/2 or c is itself a power of 3, full efficiency returns, because the divisibility that kills primality is harmless for prime powers. In range this lifts n ≡ 5 (mod 12) to a maximum of 0.10975 — but 22 of those 35 rows use the *same* foreign prime r = 487, with (r−1)/2 = 243 = 3⁵, and the others use r = 163 with 81 = 3⁴ or c = 243, 729. Candidates of the form r = 2·3^k + 1 are as thin as any other exponential family, so the escape supplies O(log n) candidates rather than n/log³n and should be read as a feature of the computed range. **The generic ceiling 0.0718 is the one to quote asymptotically.**

### 3.4 The parity gap, stated correctly

Odd n loses on both engines, and neither loss is a shortage of representations — both Bateman–Horn systems supply ~n/log³n. The losses are **caps**:

- *Multiplicatively*, even n has F = 2 available whenever n/2 is a prime power, giving 1/2; odd n has F ≥ 3, giving at best 1/3.
- *Additively*, even n balances at two parts, cap 1/4; odd n must use three, cap 1/9, and loses a further factor of 2 or 3 to the local obstructions of §3.3.

An earlier account attributed the whole gap to the scarcity of splits n = 2^a + r. That is the binding constraint for **odd n with ω(n) ≥ 3 that use two parts** — of the 150 such values, 53 use two parts and 28 have exactly the predicted 2-power block, with median density 0.0957 — but it does not describe most strong odd n, which have ω(n) = 2 and use the multiplicative engine where no additive representation arises. The correction matters for what to work on: more sieve input cannot close a gap made of caps.

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

**The asymptotic question is entirely Hardy–Littlewood.** Since the multiplicative engine vanishes in density, the asymptotic behaviour of μ(n) for almost all n is set by the additive families, whose caps are 1/4 and 1/9 and whose availability is a Bateman–Horn question. In particular the ladder constants of §5 of the notes — δ₀^even = 1/4, δ₀^odd ≈ 0.049 — are the right asymptotic quantities, and the fused family's 1/2 and 1/3 are not, however dominant they look in the table.

---

## 5. What this says about the open problems

**Open Problem 2** needs restating, per §3.3. Its constant δ₀^odd ≈ 0.049 is the ceiling of the three-block chain family, which the enumeration selects exactly once in 1,848 values; the family that actually serves odd n caps at **1/9 for n ≡ 1 (mod 4)** and **≈ 0.0858 for n ≡ 3 (mod 4)**. So the problem is not to beat 0.049 — that is already done, subject to the local-solubility check §3.3 flags — but to **exceed 1/9 strictly**, which is what Theorem E.1 needs and which the 2c + r family approaches without attaining. Per §2.1 the place to look is fusion, which beats splitting by a factor of F; the target is a configuration that fuses at odd n more aggressively than n = 3·(prime power) allows. That is a mechanism question, and §3.4 explains why more Hardy–Littlewood input cannot substitute.

**Open Problem 9(a) (k ≤ 3)** is the statement that the four-part cap 1/16 is never the best available. By §2.2 the four-part family is only in play below density 1/16, and by §2.3 that means ω(n) ≥ 3 and no good two- or three-part representation — a triple coincidence whose predicted frequency is the natural next computation. Note that the revised odd-n ceilings of §3.2 are both **above** 1/16, so on that footing the residue is closed for odd n as well as even, leaving only the local-solubility gap.

**Open Problem 9(b) (the collapse below 1/9)** lives exactly in the regime where the three-part family is the best available. That is why it is an odd-n problem, and why δ₀^odd > 1/9 would close it: at density above 1/9 the three-part family is no longer optimal, so the configurations that create the difficulty do not arise.

**The §4 barrier at exponent 3/2** is untouched by any of this, since both engines give density Θ(1) when they apply and the barrier is about proving *lower* bounds on the least prime in an arithmetic progression. The barrier and the caps are independent obstructions.

---

## 6. Open questions specific to this document

1. **Predict the density-1/12 shortfall from the singular series.** §5 of the notes measures 19.3% of odd and 0.9% of even values below 1/12. Both engines' availability is computable heuristically; the comparison would test the whole framework of this document rather than any single family.
2. **Is the four-part family ever optimal?** Equivalently, does the triple coincidence of §5 above ever occur? A negative heuristic estimate would be strong evidence for Open Problem 9(a) even without a proof.
3. **Local solubility of the 2c + r family, in each class mod 4.** The gap §3.3 flags, and the highest-value item here: §5's chain analysis found two of its candidate chains locally dead (one always divisible by 3, one dead whenever 3 | n), so the analogous check is required before the revised ceilings 1/9 and 0.0858 can be quoted as ladder constants rather than as caps.
4. **The fused family at ω(n) = 2 but bad splitting.** 282 of the 960 ω(n) = 2 values do better with a split than with fusion, which happens when the smallest prime-power cofactor F is large. The distribution of F over ω(n) = 2 integers is classical; predicting the 678/282 division is a clean test.
5. **Efficiency below 1.** §5 of the notes tabulates eff(r,q) = orb(r, qpart(r−1,q))/C(r,2) and finds efficiency 1 at 77% of foreign blocks. The distribution of the largest prime-power divisor of r − 1 over primes r is a shifted-prime question of Erdős type; its known results should be imported here rather than re-derived.
6. **Does the density floor drift as predicted?** The concrete test: extend the table and check whether the floor tracks the thinning of the ω(n) = 2 population. This is the cheapest available check on §4's central claim, and `wide_cert.py` already reaches n = 10⁵ for the collapse question, so the infrastructure exists.
