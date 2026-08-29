#!/usr/bin/env python3
r"""
overlay.py

A persistent, per-page refinement layer for constructions.

WHY. gapgen and ordercalc are stateless derivations: each run re-extracts
from the page and rebuilds from scratch. That makes refinement impossible -
there is nowhere to record "S doesn't actually need to be bigger than G, it
just needs to be centerless with no nontrivial homomorphic image embedding
in G" so that it survives the next run. This file is that place. It plays
the same role for constructions that the approved symbols table plays for
the semantic checker.

THREE TIERS, deliberately kept distinct:

    stated    - what the PAGE says. Derived, refreshed from the page on
                every merge, never hand-edited (edits would be lost).
    required  - what the PROOF actually consumes. Usually weaker than
                stated. User- or LLM-supplied and preserved across runs.
    chosen    - the concrete instance used for computation/GAP.

The gap between `stated` and `required` is itself informative. A stated
condition much stronger than what the proof uses is over-restriction: not
wrong, but it hides how general the result is, and it inflates any
computational instantiation. `overlay.py report` surfaces those gaps.

A `case` field records when a stated condition is right for one regime and
loose in another - e.g. "degree exceeding |G|" is exactly the cardinality
argument needed for infinite G, and exponentially wasteful for finite G.
That is a collapsed case split, not an error, and the distinction is worth
keeping rather than silently rewriting.

MERGE SEMANTICS. `init` is re-runnable. Derived fields are refreshed from
the page; user-owned fields (required, chosen, order, notes, case) are
preserved. If a `stated` value changes because the page was edited, the old
value is retained under `stated_previous` and flagged, so a refinement made
against the old wording can be re-checked rather than silently inherited.

Usage:
    python3 overlay.py init page.mediawiki --out page.construction.json
    python3 overlay.py report page.construction.json
    python3 gapgen.py    page.mediawiki --overlay page.construction.json
    python3 ordercalc.py page.mediawiki --overlay page.construction.json
"""

import argparse
import json
import sys
from pathlib import Path

import latex_semantic_scan as sem

USER_FIELDS = ("required", "chosen", "order", "notes", "case")


def blank(stated, sentence, scope):
    return {
        "stated": stated,
        "source_sentence": sentence,
        "scope": list(scope),
        # --- user-owned below; preserved across re-runs ---
        "required": None,
        "chosen": None,
        "order": None,
        "case": None,
        "notes": [],
        "provenance": {"stated": "page", "required": None, "chosen": None},
    }


def extract(text):
    """Symbol -> stated description, from the page as it currently reads."""
    decls = sem.dedupe_declarations(
        sem.extract_declarations(text, sem.DEFAULT_PATTERNS))
    out = {}
    for d in decls:
        # Prefer bindings: a binding introduces the symbol, an assertion
        # merely states a property of it.
        if d["sym"] in out and d.get("kind") != "binding":
            continue
        if d["sym"] not in out or d.get("kind") == "binding":
            out[d["sym"]] = (d["meaning"], d["sentence"], d["scope"])
    return out


def merge(existing, text):
    """Refresh derived fields, preserve user-owned ones."""
    fresh = extract(text)
    merged = {}
    changed, added, gone = [], [], []

    for sym, (stated, sentence, scope) in fresh.items():
        if sym in existing:
            entry = dict(existing[sym])
            if entry.get("stated") != stated:
                entry["stated_previous"] = entry.get("stated")
                entry["stated"] = stated
                entry["source_sentence"] = sentence
                changed.append(sym)
            entry["scope"] = list(scope)
            for f in USER_FIELDS:
                entry.setdefault(f, [] if f == "notes" else None)
            entry.setdefault("provenance",
                             {"stated": "page", "required": None, "chosen": None})
        else:
            entry = blank(stated, sentence, scope)
            added.append(sym)
        merged[sym] = entry

    for sym in existing:
        if sym not in fresh:
            # Keep it: a refinement is worth more than a parse that moved.
            entry = dict(existing[sym])
            entry["orphaned"] = True
            merged[sym] = entry
            gone.append(sym)

    return merged, {"changed": changed, "added": added, "orphaned": gone}


def load(path):
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text())


def resolved_orders(overlay):
    """symbol -> numeric order, for the symbols the user has pinned."""
    return {s: e["order"] for s, e in overlay.items() if e.get("order") is not None}


def resolved_choices(overlay):
    """symbol -> concrete instance string, for gapgen hole-filling."""
    return {s: e["chosen"] for s, e in overlay.items() if e.get("chosen")}


def cmd_init(args):
    existing = load(args.out)
    text = Path(args.file).read_text()
    merged, delta = merge(existing, text)
    Path(args.out).write_text(json.dumps(merged, indent=2, ensure_ascii=False))

    print(f"overlay written to {args.out}: {len(merged)} symbol(s)")
    if delta["added"]:
        print(f"  added:     {', '.join(delta['added'])}")
    if delta["changed"]:
        print(f"  RE-CHECK:  {', '.join(delta['changed'])} - the page's wording "
              f"changed; any refinement was made against the old text "
              f"(kept as 'stated_previous')")
    if delta["orphaned"]:
        print(f"  orphaned:  {', '.join(delta['orphaned'])} - no longer "
              f"extracted from the page; kept, not deleted")
    unfilled = [s for s, e in merged.items() if not e.get("required")]
    if unfilled:
        print(f"  no 'required' yet: {', '.join(sorted(unfilled))}")
    return 0


def cmd_report(args):
    overlay = load(args.overlay)
    if not overlay:
        print(f"{args.overlay} is empty or missing")
        return 1

    gaps, pinned, notes = [], [], []
    for sym, e in sorted(overlay.items()):
        if e.get("required") and e["required"] != e.get("stated"):
            gaps.append((sym, e))
        if e.get("chosen") or e.get("order") is not None:
            pinned.append((sym, e))
        if e.get("notes") or e.get("case"):
            notes.append((sym, e))

    print("=== stated vs required (slack in the page's hypotheses) ===")
    if not gaps:
        print("  (none recorded)")
    for sym, e in gaps:
        print(f"  {sym}")
        print(f"    stated:   {e['stated']}")
        print(f"    required: {e['required']}")
        print(f"    -> the page asks for more than the proof uses; the result "
              f"is more general than stated, and any instantiation built to "
              f"the stated condition is larger than it needs to be")

    print("\n=== case splits recorded ===")
    if not notes:
        print("  (none recorded)")
    for sym, e in notes:
        if e.get("case"):
            print(f"  {sym}: {e['case']}")
        for n in e.get("notes", []):
            print(f"  {sym}: {n}")

    print("\n=== concrete choices ===")
    if not pinned:
        print("  (none recorded)")
    for sym, e in pinned:
        bits = []
        if e.get("chosen"):
            bits.append(f"chosen={e['chosen']}")
        if e.get("order") is not None:
            bits.append(f"order={e['order']}")
        print(f"  {sym}: {', '.join(bits)}")

    stale = [s for s, e in overlay.items() if "stated_previous" in e]
    if stale:
        print(f"\n=== RE-CHECK: page wording changed since refinement ===")
        for s in stale:
            print(f"  {s}: was {overlay[s]['stated_previous']!r}")
    orph = [s for s, e in overlay.items() if e.get("orphaned")]
    if orph:
        print(f"\n=== orphaned (no longer extracted): {', '.join(orph)} ===")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("init", help="Create or MERGE an overlay for a page")
    p1.add_argument("file")
    p1.add_argument("--out", required=True)

    p2 = sub.add_parser("report", help="Show refinements, slack and case splits")
    p2.add_argument("overlay")

    args = ap.parse_args()
    return cmd_init(args) if args.cmd == "init" else cmd_report(args)


if __name__ == "__main__":
    sys.exit(main())
