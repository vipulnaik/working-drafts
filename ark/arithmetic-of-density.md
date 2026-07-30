# The arithmetic of the density ladder

*Supplement to `orbital-evasiveness-notes.md` and `enumeration-proof.md`. Where those two ask what μ(n) is and prove that the enumeration computes it, this one asks **which arithmetic conditions on n control the answer**, sets up the Hardy–Littlewood and Bateman–Horn machinery that governs them, and checks the predictions against the 1,672 exactly computed values. Written after the exact values became available, which changes the picture: statements that used to be conjectures about a construction menu can now be tested against μ itself.*

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
3. **The multiplicative engine covers a density-zero set, so asymptotically the additive engine is everything.** The fraction of n with ω(n) = 2 thins like log log n / log n — measured at 52% below 2000 but 29% near 10⁶. So the asymptotic behaviour of μ is governed entirely by the Hardy–Littlewood side, and the observed density floor should be expected to drift downward as the fused family's reach recedes.

---

## 2. The two engines, exactly

### 2.1 The multiplicative engine: density 1/F

Let n = F·c with F a power of q and c a power of p. The single fused class has intra-orbital F·C(c,2), within-class cross (F or F/2)·c², and no other terms, so

> m\* = F·C(c,2) = F·c(c−1)/2, and **δ = m\*/C(n,2) = (c−1)/(Fc−1) → 1/F.**

Two things follow immediately. Since a fused class needs F ≥ q ≥ 2, the engine cannot exceed **1/2**. And since n = F·c with both factors prime powers forces **ω(n) ≤ 2**, it is available only on that set.

To maximise, take F to be the **smallest prime-power cofactor** of n — the least F such that F and n/F are both prime powers.

> *Verified.* Over all 678 one-part winners in the table, the predicted density 1/F agrees with the computed value to O(1/n), with no exceptions. By F: 184 rows at F = 2 with median density 0.4994, 137 at F = 3 with median 0.3325, 105 at F = 4 with 0.2491, 88 at F = 5 with 0.1991, 62 at F = 7 with 0.1419, 39 at F = 9 with 0.1102. Maxima 0.49975, 0.33300, 0.24960, 0.19960, 0.14240, 0.11060 against 1/F = 0.5, 0.3333, 0.25, 0.2, 0.1429, 0.1111.

> *Verified.* All 678 one-part winners have ω(n) = 2, and **no** value with ω(n) ≥ 3 has a one-part winner. Of the 960 table values with ω(n) = 2, 678 are one-part winners and the other 282 do better with a split.

**Why fusion is worth a factor of F.** F *unfused* equal parts of size c give min(C(c,2), c²) = C(c,2) ≈ n²/(2F²), density 1/F². Fusing them replaces the mutual capping by a single intra term F·C(c,2), density 1/F. So fusion buys exactly F, which is why reduction (R1) of the proof document — merge equal-size classes when F₁ + F₂ is a q-power — is the single most valuable simplification in the search, and why the enumeration's winners are so often a single fused class.

### 2.2 The additive engine: density 1/k²

For k unfused parts of sizes sᵢ summing to n, the between-orbit classes sᵢsⱼ and the intra terms C(cᵢ,2) cap each other. Proposition F.1 of the proof document gives k < 1/√δ; read backwards,

> **k parts ⟹ δ < 1/k²**, and the bound is saturated by balanced parts.

> *Verified, and tight.* Maximum observed density is 0.24926 among two-part winners and 0.11037 among three-part winners; **no two-part winner exceeds 1/4 and no three-part winner exceeds 1/9**, over 793 and 201 rows respectively. Medians 0.1985 and 0.0915.

So the ladder of thresholds is one sequence: 1/4, 1/9, 1/16 at k = 2, 3, 4. The 1/9 above which Theorem E.1 settles the collapse, and the 1/16 above which Corollary F.3 gives k ≤ 3, are not independently chosen constants; they are the points at which the next part count becomes possible.

### 2.3 The two engines cover complementary sets

| | condition on n | density | share of table |
|---|---|---|---|
| fused, one class | n = F·c, both prime powers (so ω(n) ≤ 2) | 1/F, up to 1/2 | 678 rows |
| two parts | n = c + r\*, c a prime power, r prime | ≤ 1/4 | 793 rows |
| three parts | n = 2c + r\*, c a prime power, r prime | ≤ 1/9 | 201 rows |

> *Verified.* Every one of the 321 table values with density above 1/4 has ω(n) = 2 and a one-part winner. Maximum density over all 712 values with ω(n) ≥ 3 is 0.2493 — the two-part cap.

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

### 3.2 Three parts at odd n, and the 1/9 ceiling

Odd n cannot use a balanced two-part split: c + r odd forces one part even, and a prime foreign part that is even must be 2, useless. So the even part must be the p-characteristic one, i.e. **c = 2^a**, giving the family n = 2^a + r with only ~log₂ n candidate splits. That route is genuinely scarce.

The route that avoids it is **three parts, all odd**: n = 2c + r with c an odd prime power and r an odd prime. Balancing C(c,2) against cap(r) with 2c + r = n gives c ≈ r ≈ n/3 and density → **1/9**. The Bateman–Horn system is the same shape as above with f₃(x) = (n − x)/2, so again ~n/log³n representations — plentiful, but the *cap* is 1/9 rather than 1/4.

> *Verified.* Among the 150 odd table values with ω(n) ≥ 3 — those for which the fused family is unavailable — 97 use a three-part configuration with **no even part**, and 53 use two parts, of which 28 have the 2-power p-characteristic block the argument predicts. Median density over the 150 is 0.0957, consistent with the three-part cap of 1/9 rather than the two-part 1/4.

**This is the source of the parity gap, stated correctly.** Odd n loses on both engines: multiplicatively because F ≥ 3 caps it at 1/3 instead of 1/2, and additively because its balanced route is three parts (cap 1/9) rather than two (cap 1/4). Nothing about the *density of representations* is binding — both systems give ~n/log³n. It is the **caps** that differ.

### 3.3 What the older analysis got right and wrong

An earlier draft of §5.5 of the notes explained the odd deficit entirely by the scarcity of n = 2^a + r splits. Scoped to **odd n with ω(n) ≥ 3 that use two parts**, this is correct and is confirmed above. As an account of all strong odd n it is wrong, because most strong odd n have ω(n) = 2 and use the multiplicative engine, where no additive representation is involved at all: of the 548 odd values reaching density 1/12, **444 have ω(n) = 2** and only 104 have ω(n) ≥ 3.

The correction matters for what to work on. The odd deficit is not primarily a shortage of additive representations, so producing more of them — better sieve input, stronger Hardy–Littlewood assumptions — will not close it. It is a shortage of *caps*, which is a question about mechanisms.

---

## 4. Asymptotics: the multiplicative engine is a thinning exception

The fused family requires ω(n) ≤ 2, which is a **density-zero condition**: the count of n ≤ N with exactly two distinct prime factors is ~N log log N / log N.

> *Verified.* Fraction of composite non-prime-power n with ω(n) = 2, by dyadic block: **52.3%** on [10³, 2·10³), 43.1% on [5·10³, 10⁴), 35.0% on [5·10⁴, 10⁵), 29.8% on [5·10⁵, 10⁶), 28.5% on [10⁶, 2·10⁶).

Two consequences, and both should temper how the computed range is read.

**The observed density floor should drift downward.** Fully 57% of the current table has ω(n) = 2, so more than half the computed values are served by an engine whose reach halves over the next few decades of n. The floor of 0.0418 at n = 575, and the median of 0.1995, are both propped up by a population that thins.

**The asymptotic question is entirely Hardy–Littlewood.** Since the multiplicative engine vanishes in density, the asymptotic behaviour of μ(n) for almost all n is set by the additive families, whose caps are 1/4 and 1/9 and whose availability is a Bateman–Horn question. In particular the ladder constants of §5 of the notes — δ₀^even = 1/4, δ₀^odd ≈ 0.049 — are the right asymptotic quantities, and the fused family's 1/2 and 1/3 are not, however dominant they look in the table.

---

## 5. What this says about the open problems

**Open Problem 2 (raise δ₀^odd above 1/9)** is now sharply posed: it asks for an odd-n family whose cap exceeds 1/9, i.e. something better than balanced three parts. §2.1 says where to look — fusion beats splitting by a factor of F, so the target is a configuration that fuses at odd n more aggressively than n = 3·(prime power) allows. This is a mechanism question, not a sieve question, and §3.3 explains why more Hardy–Littlewood input cannot substitute.

**Open Problem 9(a) (k ≤ 3)** is the statement that the four-part cap 1/16 is never the best available. By §2.2 the four-part family is only in play below density 1/16, and by §2.3 that means ω(n) ≥ 3 and no good two- or three-part representation — a triple coincidence whose predicted frequency is the natural next computation.

**Open Problem 9(b) (the collapse below 1/9)** lives exactly in the regime where the three-part family is the best available. That is why it is an odd-n problem, and why δ₀^odd > 1/9 would close it: at density above 1/9 the three-part family is no longer optimal, so the configurations that create the difficulty do not arise.

**The §4 barrier at exponent 3/2** is untouched by any of this, since both engines give density Θ(1) when they apply and the barrier is about proving *lower* bounds on the least prime in an arithmetic progression. The barrier and the caps are independent obstructions.

---

## 6. Open questions specific to this document

1. **Predict the density-1/12 shortfall from the singular series.** §5 of the notes measures 19.3% of odd and 0.9% of even values below 1/12. Both engines' availability is computable heuristically; the comparison would test the whole framework of this document rather than any single family.
2. **Is the four-part family ever optimal?** Equivalently, does the triple coincidence of §5 above ever occur? A negative heuristic estimate would be strong evidence for Open Problem 9(a) even without a proof.
3. **The fused family at ω(n) = 2 but bad splitting.** 282 of the 960 ω(n) = 2 values do better with a split than with fusion, which happens when the smallest prime-power cofactor F is large. The distribution of F over ω(n) = 2 integers is classical; predicting the 678/282 division is a clean test.
4. **Efficiency below 1.** §5 of the notes tabulates eff(r,q) = orb(r, qpart(r−1,q))/C(r,2) and finds efficiency 1 at 77% of foreign blocks. The distribution of the largest prime-power divisor of r − 1 over primes r is a shifted-prime question of Erdős type; its known results should be imported here rather than re-derived.
5. **Does the density floor drift as predicted?** The concrete test: extend the table and check whether the floor tracks the thinning of the ω(n) = 2 population. This is the cheapest available check on §4's central claim, and `wide_cert.py` already reaches n = 10⁵ for the collapse question, so the infrastructure exists.
