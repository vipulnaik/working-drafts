# Pending checks

*What is left to run or verify. Companion to `orbital-evasiveness-notes.md` and `enumeration-proof.md`. This file is deliberately forward-looking: completed work and its figures live in the two documents, and the session history is in `session-log.md`.*

**Status labels.** *Verified* — an independent computation agreed. *Sound* — an argument was read and found correct, with no independent computation. *Unverified* — neither.

---

## Quick reference: commands

*Flags below are checked against the scripts as they stand. Where a run needs code that does not exist yet, that is said explicitly rather than papered over with a plausible-looking flag.*

**Routine, after any new batch of table values:**

```bash
python3 mu_enumerate.py --nmin 2213 --nmax 2600 --out mu_table_safe_v2.csv   # extend the table (~n^2.9/value)
python3 mu_enumerate.py --nlist ladder_weak.txt --out mu_table_safe_v2.csv   # or: work the weak-value list first
python3 mu_enumerate.py --nmax 2600 --fill-gaps --out mu_table_safe_v2.csv   # then close any gaps a targeted run left
python3 fallback_cert.py mu_table_safe_v2.csv                               # collapse certificate vs the true B(n)
python3 wide_cert.py 100000                                                 # same, from lower bounds; pass 1 cached
python3 check_doc_figures.py mu_table_safe_v2.csv *.md                      # catch prose figures the extension made stale
python3 ladder_verify.py 200000                                             # ladder floor, all 12 classes (87 s)
```

**`ladder_verify.py` — rewritten, and the earlier version was checking too little.** It used to ask a binary question, "does a full-efficiency representation exist near x = 1/3", which (a) skipped every class where full efficiency is locally obstructed — classes 2, 3, 5, 7, 8, 11 mod 12, i.e. half of all n, and the hard half — and (b) used a window that does not contain the balance point of the low-efficiency classes, so a shortfall there was an artefact rather than a finding.

It now computes, for each n and over all twelve classes, the best density the three families achieve, scanning x ∈ [0.10, 0.55] which holds every balance point. That subsumes the old check (representability is "achieved density > 0") and yields the global floor of `arithmetic-of-density.md` §5 directly. Current result to 2·10⁵: **floor 0.02504 at n = 3239, zero values below 0.02**, per-class minima of δ/cap between 0.33 and 0.72.

Cost is O(N²/log N), not linear — 33 s to 10⁵, 190 s to 2.5·10⁵ — so **10⁶ is roughly an hour and is the run worth doing**; 10⁷ is multi-day and not worth it without a further reason. (An earlier note here quoted 193 s for 10⁷; that timing was the old binary check, which scanned a narrow fixed window.)

It also writes **`ladder_weak.txt`** — every n whose computed lower bound falls below the asymptotic constant (5 − 2√6)/2 = 0.050510, which is 2,163 values below 6·10⁴. These are *not* counterexamples: the script computes a lower bound on δ(n), not δ(n), and in particular does not model the fused-plus-foreign shape (F, c) + r\* that the enumeration often prefers. It is a **worklist for `mu_enumerate.py`**: computing the true B(n) at those n would raise the observed global floor of §5 and could replace the loose 1/50 with something near the asymptotic value. Many of the smaller entries (575, 851, 935, 1175, …) are already in the computed table, so the comparison can start immediately without new enumeration.

Since the run is long enough to want watching, it prints a **checkpoint every 10,000** — timestamp, elapsed, throughput, the running floor and its n, a flag if anything has fallen below the floor, and an ETA scaled by N²/log N rather than linearly — and a **cumulative summary every 100,000** giving that block's own minimum alongside the global one. The block minima are worth reading on their own: 0.02504 over the first 10⁵ and 0.04125 over the second, which is the floor-rises-with-n effect of §5 visible as the scan proceeds.

**Run `check_doc_figures.py` after every extension.** Three consecutive extensions each left a *different* subset of the documents behind, because the updates were done by ad-hoc string replacement rather than a sweep. The script recomputes every range-dependent figure the prose quotes — row count, n max, density floor and peak, median, part counts, `certified_K` distribution, the 1/4 and 1/9 shares, the δ ≤ 1/16 tail, the ω(n) = 2 count — and flags occurrences that no longer match. It deliberately does not edit: several of these numbers sit in sentences whose wording has to change with them (the density floor moved off n = 575 at n ≤ 2212, and the surrounding claim that it was "stable rather than eroding" had to go). Some flagged figures are legitimate historical citations — the `mu_fast.py` menu table's row count, a sample size, a "then-N" reference — so the output is a checklist, not a diff.

`mu_enumerate.py` also takes **`--nlist FILE`** (one n per line, extra fields ignored, so `ladder_weak.txt` can be passed straight in) and **`--fill-gaps`**. The two go together: a targeted `--nlist` run leaves holes below its own maximum, and plain resume continues after the *last* row, so those holes would never be filled. `--fill-gaps` rescans from `--nmin` and relies on the already-present check to skip what is done, costing only a loop over n. It also takes `--n` for a single value, `--check` to validate an existing table without extending it, `--quiet`, and `--refined` (the lower endpoint B_refined — see Part C.2 of the proof document before using it). `wide_cert.py` takes `--menu` to add the family-menu lower bound as a cross-check and `--refresh` to discard the cached pass 1. `fallback_cert.py` takes `--verbose` to list every surviving candidate rather than stopping at the first.

**Outstanding one-off runs.** These operate on the GAP battery and read `ckpt_groups.pkl`, `ckpt_catalog.pkl`, `ckpt_order.pkl` from the working directory; `n` is implicit in `groups_out.txt` rather than a flag.

```bash
# A1 + A2  rebuild the n = 12 battery with the corrected dedup key.
#   --maxgroups IS REQUIRED.  It defaults to 200 and silently truncates: the run of
#   2026-07 found 203 distinct Oliver conditions and kept only 200 (see A1 below).
#   Stage-3 VF2 sampling is automatic (--verify, default 3000), so A2 needs no separate run.
#   No manual cleanup: changing any flag changes the selection signature and stage 1
#   deletes ckpt_groups/catalog/order itself.  Do NOT pre-delete them.
#   READ A5 FIRST -- stage 3 at full size is a multi-week run and may not be needed at all.
python3 consume_gap.py --infile groups_out.txt --maxgroups 1000 --maxt 8 --procs 8

# check whether groups_out.txt predates the multi-top-prime change to ark_gap.g:
awk -F'|' '$3 ~ /\+/' groups_out.txt | wc -l     # 0 => either pre-change, or no group has two usable q

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
- **A5** is a design decision about how to compute S at n = 12, not a run — **and it now gates A1**, because it determines whether stage 3 is needed at all.

## Open mathematical questions

Not repeated here. The two arithmetic residues are Open Problem 9 of the notes and Part J items 1–2 of `enumeration-proof.md`; the largest epistemic risk is Part J item 3 — an independent reading of Lemma B′, Lemma C and G.2, none of which has had any. `arithmetic-of-density.md` §6 lists five further questions of its own, all heuristic-vs-measurement comparisons rather than proofs; the cheapest and most informative is whether the observed density floor drifts downward as the ω(n) = 2 population thins, which needs only table extension.

---

## A. Runs pending

**A1. Rebuild the n = 12 battery with the corrected dedup key.** `consume_gap.py`'s stage-1 key was an incomplete invariant that merged inequivalent orbital partitions; the corrected key is a pynauty canonical form on a layered graph. The battery must be rebuilt before any n = 12 verdict is quoted.

*State as of the 2026-07 run (log and checkpoints on file).* Stage 1 rebuilt correctly on the signature change with no manual cleanup, and stage 2 completed: **2,293 raw → 230 distinct (partition, prime) conditions → 227 kept (200 Oliver + 27 p-groups), 2,212 catalogue classes**. μ(12) = 18 survives: m\* = 18 is attained by **3 distinct conditions**, which is the previously reported 8 groups collapsing under the corrected dedup. Stage 3 then reported **1,018,719 of 4,890,732 ordered pairs needing VF2 (20.8%)**.

> **Two problems with that run, both to fix before repeating it.**
>
> **(i) The battery was truncated.** `--maxgroups` defaults to **200** and stage 1 found **203** distinct Oliver conditions, so `sel = ol[:maxgroups] + pg` silently dropped **3**. The sort is `(-mstar, t)`, so the casualties are the lowest-m\* conditions — harmless for μ(12) = 18, which reads off the top, but the battery feeds the Smith/χ computation where every condition is a constraint. Dropping constraints makes the system easier to satisfy, so a negative verdict would survive but a positive one would not be quotable. **Always pass `--maxgroups 1000`.**
>
> **(ii) Stage 3 at full size is a multi-week run.** The old 600-class battery needed 74,213 VF2 pairs; the new 2,212-class battery needs **1,018,719 — 13.7×**. Measured from the logs across three resumed sessions: **2,176 VF2 calls, 30,002 s, 16,061 pairs resolved → 7.4 pairs/call at 13.8 s/call**, with the yield decaying as the easy pairs go first (13.5 → 3.6 → 5.4). Extrapolating: **22 days** at the early rate, **33–41 days** at the late rate. For reference the *old* battery never finished either — four sessions took it from 74,213 to 58,152, about 22% through.
>
> Levers, in order of preference: **settle A5 first**, since the EGF route may make stage 3 unnecessary; failing that, `--maxt 6` drops the t = 7 and t = 8 groups (44 + 58 of 227) and cuts pairs to roughly 30%, still about a week and a weaker battery.

**A2. Stage-3 sample verification at n = 12** — *now automatic, folded into the A1 run.* Now automatic (`--verify`, default 3000 random ordered pairs re-decided by VF2). The n = 10 acceptance test was bit-identical agreement with an archived full-VF2 reference; there is no such reference at any other degree, and roughly 80% of ordered pairs are settled by inference alone. Until this passes, the n = 12 order matrix is an unchecked implementation of checked rules.

**A3. Settle the duality involution empirically.** `probe_backbone.py` now computes the complement class of every forced class and reports violations plus the specific unprobed complements the theorem predicts. Three pressure points exist in the current n = 10 record and all are cheap to close:
- the three forced-OUT classes at 38 edges (393, 401, 405) require three forced-IN classes at 7 edges, and the only 7-edge class probed (**class 108**) came back **free**. If 108 is the complement of any of the three, **the theorem is contradicted**; if not, the partners are unprobed.
- the five forced-IN classes at 8 edges require five forced-OUT at 37 edges; no 37-edge class has been probed.
- the forced-IN class at 2 edges requires a forced-OUT at 43; no 43-edge class has been probed.

The practical corollary of the theorem — probe one representative per complement pair, halving the sweep — is currently being relied on without this check.

**A4. Re-probe the 54 CAP classes at a larger node budget.** They sit at 12–36 edges, concentrated at 24, 28, 30, 33, 34, i.e. through the middle of the free band. A CAP class is *not* free. The log shows `--nodecap` was already raised from 5×10⁶ to 2×10⁷ partway through the sweep, so the earlier CAPs may resolve without a new idea. Until then no statement of the form "the band is free from 11 to 34 edges" is supported.

**A5. Decide how S will be computed at n = 12 before the CSP verdict arrives.** `chi_test.py` enumerates the full down-closure with a canonicalisation per node: 64,333 classes and about 60 s at n = 10, against `--cap 5000000`. At n = 12 the ambient count is 1.65 × 10¹¹ iso classes and the closure of an 18-edge-or-larger generator set may well exceed the cap. The global χ test is the only test that has actually killed anything, so losing it at n = 12 would be a real loss. The alternative is the §8.4 route — exponential formula over signed connected-component weights, two-sort EGF for bipartite components — which computes S without enumerating the closure. This is a design decision, not a bug.

> **Promoted: this now gates A1.** The 2026-07 run showed stage 3 of `consume_gap.py` — the containment-order matrix — projecting to 22–41 days at the corrected battery size. Stage 3 exists to supply that order matrix. So the question is not merely *how* to compute S but **whether the order matrix is needed at all**: if the §8.4 EGF route computes χ without it, weeks of stage 3 are avoidable. Decide this before relaunching A1, and if the EGF route wins, consider whether `consume_gap.py` should gain a `--stop-after 2` flag so the battery can be built without entering stage 3.

**A6. Rerun `fallback_cert.py` whenever the table extends.** It is a per-n check, not a theorem: `python3 fallback_cert.py mu_table_safe_v2.csv` belongs in the routine after every batch of new values. It currently certifies all 1,848 with 0 inconclusive cases, and reports how many are settled by the δ > 1/9 theorem alone (1,390, i.e. 75.2%) versus by the exhaustive search (458, every one of them because δ ≤ 1/9 rather than because a Mersenne cap binds). Two things would retire it: a proof that δ is bounded below (the ladder does this conditionally, which forces s = 1 and lets the Cap(a) argument finish), or a general domination argument for the fallback.

**A7. Verify the dedup-collision audit at n = 10.** The measurement in §8.7′ was made at n = 12 because `groups_out.txt` for n = 12 was to hand. The same audit at n = 10 would say how much the *published* n = 10 SAT was affected, which matters for how the skeleton and the χ kill should be described. Requires the n = 10 `groups_out.txt`.

---

## B. Unchecked assumptions in the scripts

**B1. `Catalog.classify` is a mutating lookup used as a pure query.** In `stage4_fast.py`, `probe_backbone.py` and `chi_test.py` the idiom `x[cat.classify(set())] = 1` assumes the empty graph is already in the catalog. If it were not, `classify` would **append**, silently extending `cat.reps` and desynchronising `V` from the order matrix. The same hazard applies to the complement lookups in the new involution check, which is why that block asserts the catalog did not grow. Status: **unverified, latent.** A `classify_or_fail` variant used everywhere the catalog is meant to be read-only would close it permanently.

**B2. `mono` is only ever called on representatives with the same vertex count.** The complement trick in `ark_intersect.mono` rests on the identity σ(E_H) ⊆ E_G ⟺ σ⁻¹(E_Ḡ) ⊆ E_H̄, which requires σ to be a **bijection** — true when H and G both carry all n vertices, false for a genuine injection. Every catalog representative does carry all n vertices, so the call sites are fine. Status: **sound, but undefended.** An assertion on the vertex counts inside `mono` would make it safe against reuse.

**B3. Purely-foreign configurations are reachable.** `best_with_k` skipped a prime p when no power of p landed in the pruning window, which is justified only for configurations containing a p-characteristic part. Configurations with a trivial bottom layer (all parts foreign) are legitimate Oliver groups, and reaching them relied on some *other* p surviving the skip and happening to make every part foreign — true in practice, unproven in general. Status: **corrected** — an explicit sentinel `p = 0` meaning "trivial bottom layer" is now enumerated and never skipped. The correction did not change B(n) on any of the 85 regression values.

**B4. The refined intra-orbital formula — resolved in range; only the asymptotic statement is open.** Formerly the one place where the code computed something the proof did not license. Now closed: Parts E′–E″ of `enumeration-proof.md` prove the collapse by theorem above density 1/9 and certify it elsewhere out to n = 100,000. **What is pending here is only the routine rerun (A6) and one open case** — s = 2 with c a safe prime and a nonzero leftover, whose two unresolved values below 100,000 are n = 50,817 and n = 89,697. Status: **closed in range, open as an asymptotic statement.** Details in Part J item 2, not repeated here.

**B5. Exhaustiveness of the four GAP stages.** *Partially discharged — read this session, see below.* Only the Oliver-condition test and the emission logic of `ark_gap.g` have been read. `IsOliverTop` is **sound** — taking Γ₂ = `PCore(N,p)` is WLOG since any normal p-subgroup with cyclic quotient lies in O_p(N) and the quotient is then a quotient of a cyclic group; and normality in Γ is automatic because O_p(N) is characteristic in N with N ◁ Γ. What has *not* been checked is whether stages A–D together are exhaustive over the intended families (transitive groups, direct products over partitions, imprimitive wreaths, p-subgroups up to Sylow-conjugacy). The n = 10 and n = 12 exhaustive comparisons are evidence that they are, at those degrees.

> *Read-through, this session.* The four stages are: **A** every transitive group of degree N, by `TransitiveGroup(N,k)` over the full range of k; **B** every partition of N, with each part carrying an independently chosen transitive group, generators embedded blockwise; **B2** every wreath product T(d,k) ≀ T(r,j) with dr = N; **C** for each prime p ≤ N, the conjugacy classes of subgroups of a Sylow p-subgroup of S_N. Two observations. The union is **not** obviously exhaustive over intransitive imprimitive groups: stage B builds direct products of transitive constituents, so an intransitive group whose projections are transitive but which is a *proper subdirect* product — a fibre product over a common quotient — is generated by neither B nor B2, and C only reaches it if it happens to be a p-group. That is the concrete gap to close or refute. Second, stage C's `ConjugacyClassesSubgroups(SylowSubgroup(S_N, 2))` is the expensive step and is explicitly noted in the file as non-checkpointable at N = 10, so any claim of completeness at N = 12 depends on that call having finished, which the logs should be checked for. Status: **stages enumerated and their shapes understood; exhaustiveness still unproved, with subdirect products the identified hole.**

**B6. The lcm strengthening is implemented but unexercised.** `IsOliverTop` now returns every usable top prime as a `+`-separated tag and the solvers enforce χ ≡ 1 mod lcm. Single-prime tags parse identically, so old files behave exactly as before — which also means **the new path has never run**. It needs one GAP re-emission and a check that some group actually receives a multi-prime tag before the strengthening can be claimed.

---

**B7. `TemplateGroup` places the block rotation in the cyclic middle layer, and that is the real template bug.** §2.4's implementation note describes the defect as a spurious gcd(d, k) = 1 filter plus a prime-only k, and both symptoms are visible in `candidate_groups`. They are not the cause. `TemplateGroup`'s own chain model puts the rotation in Γ₁/Γ₂ — its docstring requires d, the foreign primes and s pairwise coprime — and separately enforces k = s with s prime. Theorem 2.4 places the rotation in the top q-group, whence any d | c−1 is admissible and k need only be a prime power. Consequence: the template misses μ(10) = 20 (k = 2, d = 10) and μ(12) = 18 (k = 4).

**Do not repair this in the enumerator alone.** I tried; relaxing the filter builds groups that `TemplateGroup` marks invalid, and an unconditional `break` over the twist candidates then discards the smaller d that had been working — **n = 22 fell from 110 to 55**. The change was reverted and the defect documented in place. The `break` bug is genuine and independent and has been fixed (break only after a valid group is actually produced); with it fixed and the filter restored, the template reproduces Run 1 exactly at n = 6, 10, 12, 15, 18, 21, 22, 26 (6, 10, 10, 30, 36, 28, 110, 78). The real repair is to move the rotation into the top layer inside `TemplateGroup`, updating its Oliver validity check and `desc_parts`, which also changes what `top_prime` parses. Status: **open, deliberately deferred** — the GAP path has no such restriction and supersedes this enumerator, so the value is in correctness of the record rather than in better μ bounds.

