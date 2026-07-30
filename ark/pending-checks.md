# Pending checks

*What is left to run or verify. Companion to `orbital-evasiveness-notes.md` and `enumeration-proof.md`. This file is deliberately forward-looking: completed work and its figures live in the two documents, and the session history is in `session-log.md`.*

**Status labels.** *Verified* — an independent computation agreed. *Sound* — an argument was read and found correct, with no independent computation. *Unverified* — neither.

---

## Quick reference: commands

*Flags below are checked against the scripts as they stand. Where a run needs code that does not exist yet, that is said explicitly rather than papered over with a plausible-looking flag.*

**Routine, after any new batch of table values:**

```bash
python3 mu_enumerate.py --nmin 2008 --nmax 2500 --out mu_table_safe_v2.csv   # extend the table (~n^2.9/value)
python3 fallback_cert.py mu_table_safe_v2.csv                               # collapse certificate vs the true B(n)
python3 wide_cert.py 100000                                                 # same, from lower bounds; pass 1 cached
```

`mu_enumerate.py` also takes `--n` for a single value, `--check` to validate an existing table without extending it, `--quiet`, and `--refined` (the lower endpoint B_refined — see Part C.2 of the proof document before using it). `wide_cert.py` takes `--menu` to add the family-menu lower bound as a cross-check and `--refresh` to discard the cached pass 1. `fallback_cert.py` takes `--verbose` to list every surviving candidate rather than stopping at the first.

**Outstanding one-off runs.** These operate on the GAP battery and read `ckpt_groups.pkl`, `ckpt_catalog.pkl`, `ckpt_order.pkl` from the working directory; `n` is implicit in `groups_out.txt` rather than a flag.

```bash
# A1 + A2  rebuild the n = 12 battery with the corrected dedup key.
#          Stage-3 VF2 sampling is automatic (--verify, default 3000), so A2 needs no separate run.
python3 consume_gap.py --infile groups_out.txt --maxt 8 --procs 8

# A3  involution pressure points. Needs the complements of 393, 401, 405 (38 edges) and of the
#     five 8-edge forced-IN classes; 108 is the only 7-edge class probed so far and came back free.
python3 probe_backbone.py --classes 393,401,405,108,437,439,457,493

# A4  the 54 CAP classes at a larger budget. --auto N probes the N highest-value unprobed classes;
#     there is no flag that selects "the CAP classes", so the list must be passed explicitly.
python3 probe_backbone.py --classes <the 54 CAP ids> --nodecap 20000000
```

**Needs code that does not exist:**

- **A7** (dedup-collision audit at n = 10) has no CLI entry point — the n = 12 measurement was ad hoc. It also needs `groups_out.txt` for n = 10, which is not in the working set.
- **A4**'s class list is not recorded anywhere machine-readable; it must be re-extracted from the probe record before the command above can be run.
- **A5** is a design decision about how to compute S at n = 12, not a run.

## Open mathematical questions

Not repeated here. The two arithmetic residues are Open Problem 9 of the notes and Part J items 1–2 of `enumeration-proof.md`; the largest epistemic risk is Part J item 3 — an independent reading of Lemma B′, Lemma C and G.2, none of which has had any.

---

## A. Runs pending

**A1. Rebuild the n = 12 battery with the corrected dedup key.** `consume_gap.py`'s stage-1 key was an incomplete invariant used to discard groups; it is now a canonical form of the orbital partition. Because the selection signature changes, a bare rerun will detect the mismatch and rebuild stages 1–3 automatically. Expected effect at n = 12: the battery grows from 381 to 425 distinct (partition, prime) conditions, and at `--maxt 8` from 205 to 230. Cost: stage 2 and stage 3 rerun. **Nothing downstream of the old key should be quoted as a verdict until this has run**, because a dropped condition can only turn a real UNSAT into SAT.

**A2. Stage-3 sample verification at n = 12** — *now automatic, folded into the A1 run.* Now automatic (`--verify`, default 3000 random ordered pairs re-decided by VF2). The n = 10 acceptance test was bit-identical agreement with an archived full-VF2 reference; there is no such reference at any other degree, and roughly 80% of ordered pairs are settled by inference alone. Until this passes, the n = 12 order matrix is an unchecked implementation of checked rules.

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

## B. Unchecked assumptions in the scripts

**B1. `Catalog.classify` is a mutating lookup used as a pure query.** In `stage4_fast.py`, `probe_backbone.py` and `chi_test.py` the idiom `x[cat.classify(set())] = 1` assumes the empty graph is already in the catalog. If it were not, `classify` would **append**, silently extending `cat.reps` and desynchronising `V` from the order matrix. The same hazard applies to the complement lookups in the new involution check, which is why that block asserts the catalog did not grow. Status: **unverified, latent.** A `classify_or_fail` variant used everywhere the catalog is meant to be read-only would close it permanently.

**B2. `mono` is only ever called on representatives with the same vertex count.** The complement trick in `ark_intersect.mono` rests on the identity σ(E_H) ⊆ E_G ⟺ σ⁻¹(E_Ḡ) ⊆ E_H̄, which requires σ to be a **bijection** — true when H and G both carry all n vertices, false for a genuine injection. Every catalog representative does carry all n vertices, so the call sites are fine. Status: **sound, but undefended.** An assertion on the vertex counts inside `mono` would make it safe against reuse.

**B3. Purely-foreign configurations are reachable.** `best_with_k` skipped a prime p when no power of p landed in the pruning window, which is justified only for configurations containing a p-characteristic part. Configurations with a trivial bottom layer (all parts foreign) are legitimate Oliver groups, and reaching them relied on some *other* p surviving the skip and happening to make every part foreign — true in practice, unproven in general. Status: **corrected** — an explicit sentinel `p = 0` meaning "trivial bottom layer" is now enumerated and never skipped. The correction did not change B(n) on any of the 85 regression values.

**B4. The refined intra-orbital formula — resolved in range; only the asymptotic statement is open.** Formerly the one place where the code computed something the proof did not license. Now closed: Parts E′–E″ of `enumeration-proof.md` prove the collapse by theorem above density 1/9 and certify it elsewhere out to n = 100,000. **What is pending here is only the routine rerun (A6) and one open case** — s = 2 with c a safe prime and a nonzero leftover, whose two unresolved values below 100,000 are n = 50,817 and n = 89,697. Status: **closed in range, open as an asymptotic statement.** Details in Part J item 2, not repeated here.

**B5. Exhaustiveness of the four GAP stages.** Only the Oliver-condition test and the emission logic of `ark_gap.g` have been read. `IsOliverTop` is **sound** — taking Γ₂ = `PCore(N,p)` is WLOG since any normal p-subgroup with cyclic quotient lies in O_p(N) and the quotient is then a quotient of a cyclic group; and normality in Γ is automatic because O_p(N) is characteristic in N with N ◁ Γ. What has *not* been checked is whether stages A–D together are exhaustive over the intended families (transitive groups, direct products over partitions, imprimitive wreaths, p-subgroups up to Sylow-conjugacy). The n = 10 and n = 12 exhaustive comparisons are evidence that they are, at those degrees.

**B6. The lcm strengthening is implemented but unexercised.** `IsOliverTop` now returns every usable top prime as a `+`-separated tag and the solvers enforce χ ≡ 1 mod lcm. Single-prime tags parse identically, so old files behave exactly as before — which also means **the new path has never run**. It needs one GAP re-emission and a check that some group actually receives a multi-prime tag before the strengthening can be claimed.

---

**B7. `TemplateGroup` places the block rotation in the cyclic middle layer, and that is the real template bug.** §2.4's implementation note describes the defect as a spurious gcd(d, k) = 1 filter plus a prime-only k, and both symptoms are visible in `candidate_groups`. They are not the cause. `TemplateGroup`'s own chain model puts the rotation in Γ₁/Γ₂ — its docstring requires d, the foreign primes and s pairwise coprime — and separately enforces k = s with s prime. Theorem 2.4 places the rotation in the top q-group, whence any d | c−1 is admissible and k need only be a prime power. Consequence: the template misses μ(10) = 20 (k = 2, d = 10) and μ(12) = 18 (k = 4).

**Do not repair this in the enumerator alone.** I tried; relaxing the filter builds groups that `TemplateGroup` marks invalid, and an unconditional `break` over the twist candidates then discards the smaller d that had been working — **n = 22 fell from 110 to 55**. The change was reverted and the defect documented in place. The `break` bug is genuine and independent and has been fixed (break only after a valid group is actually produced); with it fixed and the filter restored, the template reproduces Run 1 exactly at n = 6, 10, 12, 15, 18, 21, 22, 26 (6, 10, 10, 30, 36, 28, 110, 78). The real repair is to move the rotation into the top layer inside `TemplateGroup`, updating its Oliver validity check and `desc_parts`, which also changes what `top_prime` parses. Status: **open, deliberately deferred** — the GAP path has no such restriction and supersedes this enumerator, so the value is in correctness of the record rather than in better μ bounds.

