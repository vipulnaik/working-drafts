# mathcheck — deterministic sanity checks for mathematical prose

A set of scripts for catching mechanically-detectable errors in wiki-style
mathematical writing, so human review can focus on the mathematics.

Everything is pure Python plus (optionally) `sympy`. **No LaTeX installation
is required.** No network access, no LLM calls.

---

## Files

Put all of these in one directory; they import each other as modules.

| File | Role |
| --- | --- |
| `mathcheck.py` | Front door for the two checking layers |
| `latex_var_scan.py` | Syntactic layer — which symbols exist |
| `latex_semantic_scan.py` | Semantic layer — what each symbol means |
| `gapgen.py` | GAP scaffold generator for constructive proofs |
| `ordercalc.py` | Symbolic order arithmetic (needs `sympy`) |
| `overlay.py` | Persistent per-page refinements |
| `regression_test.py` | Test suite for the tools themselves |
| `probe.py` | Exploratory mutation harness |

---

## The two checking layers

**Syntactic** (`latex_var_scan.py`) knows which symbols exist. Its state is a
`registry.json` — a flat set of variable names.

**Semantic** (`latex_semantic_scan.py`) knows what each symbol means. Its state
is a per-page `<page>.symbols.json` — a table you review by hand.

They catch different things and neither subsumes the other. A symbol swapped
for one that appears nowhere else on the page is caught by the registry diff;
a symbol swapped for one already in scope can only be caught semantically.

---

## Workflows

### Writing a new page

```bash
# 1. draft the page

# 2. extract a semantic table
python3 mathcheck.py semantic-extract MyPage.mediawiki --out MyPage.symbols.json

# 3. HAND-EDIT MyPage.symbols.json — fix misparses, delete junk.
#    This step is not optional and not skimmable.

# 4. check against your corrected table
python3 mathcheck.py check MyPage.mediawiki --approved MyPage.symbols.json
```

Don't pass `--registry` here; on a new page every symbol is new.

### Auditing an existing corpus

```bash
# Pass A — census. No registry, so read the UNKNOWN-MACRO and
# MALFORMED_MATH_TAG lines; those need no baseline and are pure signal.
python3 mathcheck.py syntax-batch ./wiki-export/ --glob '*.mediawiki'

# Pass B — semantic tables, one per page
for f in wiki-export/*.mediawiki; do
  python3 mathcheck.py semantic-extract "$f" --out "${f%.mediawiki}.symbols.json"
done
```

Expect to spend Pass A growing `KNOWN_OPERATORS` / `KNOWN_FUNCTIONS` /
`DECORATION_MACROS` in `latex_var_scan.py` until the unknown-macro list is
genuinely unknown rather than merely unlisted.

### Checking an edit (the main workflow)

```bash
python3 mathcheck.py diff old.mediawiki new.mediawiki --approved MyPage.symbols.json
```

`diff` reports **only what the edit introduced** — pre-existing problems stay
quiet, so an edit is judged on what it changed. The registry is built from the
old revision in memory, so there's no registry file to forget to update.

Exit code: `1` if the edit introduced anything gating, `0` otherwise. Enough
for a pre-commit hook today.

### Suggesting what to add

```bash
python3 mathcheck.py suggest MyPage.mediawiki
python3 mathcheck.py suggest MyPage.mediawiki --json
```

A third kind of check, and deliberately a **separate command**. `check` and
`diff` ask whether what's written is wrong; `characterize` asks what needs a
human's eye; `suggest` asks whether the page lacks content that pages like it
usually carry — a finiteness caveat, a worked example, stated orders, a GAP
snippet, a Given citation.

Absence is judged against an expectation rather than against the page, so this
is inherently the noisiest kind of check and would drown correctness findings
if mixed into `check`. Run it when you're deciding what to add, not on every
edit.

Every suggestion fires on positive evidence from the page (a detected infinite
domain, an unexhibited input, a derivable order) — never merely because a
section is absent. Suggestions are gated on the page-type templates
(`{{tabular proof format}}` and friends) where a norm only applies to some
page types. Expect 0–3 per page; the test suite has a volume guard.

**Output is a reminder and a starting point, not text to paste.** Derived
orders and GAP snippets need a human pass first.

### Reviewing characterizations

```bash
python3 mathcheck.py characterize MyPage.mediawiki
python3 mathcheck.py characterize MyPage.mediawiki --json   # for an LLM
```

Not an error report — a checklist. Resolve everything `check` flags as a
problem first, then walk this list confirming each set of characterizations
picks out the same object. `VERIFY-EQUIVALENCE` items are explicitly asserted
equivalent by the text (an "in other words", "equivalently"), so a mismatch
there is a real defect; plain `characterizations` are accumulated independent
properties and are usually fine.

This catches the dropped-qualifier failure — "the largest normal subgroup of
`G` containing `H`" where the proof needs "...containing `H` **as a normal
subgroup**". Where the first characterization is implicit (a symbol sitting in
a chain like `H < K < G`), the raw antecedent sentence is shown unparsed for
you to compare by eye.

---

## Registry scoping — decide this early

`registry.json` is a **flat global set of names**. For a per-page edit diff
that's exactly right: use one registry per page.

`syntax-batch --update-registry` builds one registry across every file, which
for a large corpus is close to meaningless — `G` on one page has nothing to do
with `G` on another. After a few hundred pages the "new variable" signal goes
to zero.

**Recommendation: per-page registries only.** Use the shared/global registry
for finding unknown *macros* (where a common vocabulary genuinely is correct),
never for variable novelty.

---

## Severities

Gating (fail a pipeline):

- `REDEFINITION` — a symbol re-bound to a conflicting meaning
- `SELF_REFERENCE` — a symbol defined in terms of itself
- `MALFORMED_MATH_TAG` — empty, unbalanced, or crossed `<math>` delimiters;
  these corrupt span detection and turn prose into phantom variables

Advisory (reported, never gates):

- `MATH_TAG_CASE` — `<matH>` instead of `<math>`. Cosmetic: MediaWiki matches
  tag case insensitively, so it renders identically
- `DRIFT` — meaning differs from the approved table. Compares against a table
  that goes stale, so it's noisy on real edits
- `UNDECLARED_REFERENT` — a symbol used only as an "of X" target
- `POSSIBLE_ALIAS` — two symbols with near-identical meanings
- `AMBIGUOUS_ATTACHMENT` — the parse is correct, but the phrasing can mislead
  a reader too; add commas or parentheses
- `UNCITED_GIVEN` — a tabular proof states a Given but never cites it in the
  "Given data used" column, so the step where the hypothesis is first consumed
  is unrecorded. A conjunctive Given ("a division ring `K` of finite size") is
  split into its components and each is checked separately, so dropping one
  citation isn't masked by the other still being present

Lists live at the top of `mathcheck.py` (`GATING_SEVERITIES`,
`ADVISORY_SEVERITIES`) if you want to move something.

---

## Constructive proofs

### GAP scaffolds

```bash
python3 gapgen.py page.mediawiki --section "hard direction"
python3 gapgen.py page.mediawiki --json      # holes, for an LLM to fill
```

A **scaffolding generator with typed holes**, not a synthesizer. It guarantees
skeleton completeness, not mathematical correctness: every symbol appears
either as real GAP or as a labelled hole, and nothing is referenced without
being defined or declared an input.

Holes are expected, not failures — constructive proofs lean on results stated
elsewhere ("a nontrivial 2-subnormal subgroup that is not normal"), and naming
those is better than guessing.

Output will generally need editing before it runs. `SemidirectProduct` always
needs a hand-written action homomorphism, and anything infinite must be
instantiated at a concrete finite example first. **Nothing emitted has been
executed** — check signatures against the GAP reference manual on first use.

Extend coverage by editing the `CONSTRUCTIONS` table at the top of the file.

### When a page has no finite model

Both `gapgen` and `ordercalc` lead with a **NOT FINITELY INSTANTIABLE** banner
when a page's constructions live over the reals, rationals or complexes. Some
results have no finite counterexample by nature — every finite subgroup is
powering-invariant, so a counterexample to powering-invariance is necessarily
infinite. For those pages the computational tools aren't short of data, they're
structurally inapplicable, and filling the TODOs won't help.

Detection is deliberately narrow: only inherently-infinite objects count. A
page that merely mentions "finitary" or "infinite" in passing may still have
perfectly good finite examples.

### Order arithmetic

```bash
python3 ordercalc.py page.mediawiki
python3 ordercalc.py page.mediawiki --assume p=2 --assume G=8 --assume H=2
python3 ordercalc.py page.mediawiki --minimal     # primes -> 2, odd primes -> 3
python3 ordercalc.py page.mediawiki --json
```

Assigns a free symbol to each order the page doesn't determine, then
propagates order formulas through every construction: `\rtimes`/`\times` →
product, `X^Y` → power, `X/Y` → quotient, `\mathbb{F}_p[G]` → `p^|G|`.

It reads the **LaTeX equation forms**, not the prose — `A = \mathbb{F}_p[G]
\rtimes G` is an expression grammar already, whereas the prose form doesn't say
which set indexes a power. A narrow prose bridge handles "X is the semidirect
product of A and B".

Things with no general order formula (joins `\langle ... \rangle`,
normalizers, centralizers) are reported **not inferrable** rather than guessed.

Partial substitution works: unsupplied symbols stay in the formula
(`256*|H_1|`). Emitted formulas round-trip through `sympify` (internally
`ord_G`, displayed `|G|`), so you can feed them to a solver.

`--minimal` fills scalars only. Group orders are never guessed — a prime has a
canonical smallest instance, a group does not.

---

## Refinement overlays

```bash
python3 overlay.py init page.mediawiki --out page.construction.json   # re-runnable
python3 overlay.py report page.construction.json

python3 ordercalc.py page.mediawiki --overlay page.construction.json
python3 gapgen.py    page.mediawiki --overlay page.construction.json
```

Makes refinement **cumulative** — without it, every run rebuilds from the page
and any tightening you did is lost.

Three tiers per symbol:

- `stated` — what the page says. Derived; refreshed each `init`. Don't
  hand-edit, your edits will be overwritten.
- `required` — what the proof actually consumes, usually weaker. Yours.
- `chosen` — the concrete instance, plus `order`.

Also `case` and `notes`, for recording things like "this recipe is exactly
right for infinite `G` and loose by an exponential factor for finite `G`".

`overlay.py report` surfaces the `stated` vs `required` gap, which is a page
quality signal in itself: a stated hypothesis much stronger than what the proof
uses means the result is more general than advertised, and any computational
instantiation is bigger than it needs to be.

**Merge semantics.** `init` is re-runnable. User fields survive. If the page
wording changed, the old text is kept as `stated_previous` and flagged
`RE-CHECK` — your refinement was made against text that no longer exists.
Symbols that stop being extracted are marked `orphaned`, not deleted.

`gapgen` fills holes from `chosen` and prints `ACTUALLY REQUIRED` above the
page's stated condition. `ordercalc` picks up orders without retyping
`--assume` (an explicit flag still wins).

---

## Testing the tools

```bash
python3 regression_test.py     # exit 0 = pass, 2 = missing sample files
python3 probe.py               # exploratory mutation battery
```

Run from a directory containing the scripts and the sample `.mediawiki` files.

The suite checks both directions: clean pages stay at or below recorded
baselines (false positives), and injected errors are still caught (false
negatives). Several cases are sabotage-verified — deliberately breaking the
feature fails exactly that case.

**Baselines are intentional.** If a change pushes an issue count up, that's
either new signal or new noise, and the diff tells you which. Don't relax a
baseline without deciding which it was.

`probe.py` is for discovery, not regression: it runs many subtle mutations and
reports what's caught. Findings worth keeping get promoted into
`regression_test.py`.

---

## Known limits

- **Symbol confusion between two symbols already in scope** is the main blind
  spot. Swapping `d` for `r` where both exist and the sentence stays internally
  consistent is not mechanically detectable.
- **Staleness.** Nothing notices when a statement was true two edits ago and
  no longer is. `DRIFT` gestures at it but is too noisy to gate on.
- **`required` is free text.** Nothing verifies that a weakened condition
  actually suffices for the proof — the overlay records that judgment, it
  doesn't validate it.
- **Overlays are per-page.** A refinement to a shared notion must be repeated
  on each page that uses it.
- Prose patterns are tuned to Groupprops idiom. Other corpora will need
  additions to `DEFAULT_PATTERNS` in `latex_semantic_scan.py`.
