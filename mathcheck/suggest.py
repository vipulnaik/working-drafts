#!/usr/bin/env python3
r"""
suggest.py

"What is MISSING from this page" — a third, separate kind of check.

The other tools ask whether what's written is wrong (`check`, `diff`) or
whether it needs a human's eye (`characterize`). This one asks whether the
page lacks a kind of content that pages like it usually carry.

WHY IT IS A SEPARATE COMMAND. Absence checks are judged against an
expectation rather than against the page itself, so they are inherently the
noisiest kind. Mixed into `check` they would drown the findings that are
actually about correctness. Run this when you are deliberately deciding what
to add, not on every edit.

CALIBRATION. Every suggestion here is gated on evidence FROM THE PAGE - a
detected infinite domain, an unexhibited input, a derivable order. Nothing
fires merely because a section is absent. When in doubt the rule is to stay
quiet: a suggestion list people learn to ignore is worse than no list.

Output is meant as a reminder and a starting point, NOT as text to paste.
Derived orders and GAP snippets need a human pass before they go on a wiki.
"""

import re

import latex_semantic_scan as sem


# Page-type templates Groupprops already carries. These gate suggestions so
# a norm is only applied to pages it actually fits.
PAGE_TYPES = {
    "definition equivalence": "definition-equivalence",
    "subgroup property non-implication": "non-implication",
    "subgroup property implication": "implication",
    "tabular proof format": "tabular-proof",
}


def page_types(text):
    found = set()
    for m in re.finditer(r"\{\{([^|}]+)", text):
        name = m.group(1).strip().lower()
        for key, label in PAGE_TYPES.items():
            if name.startswith(key):
                found.add(label)
    return found


def _has_finiteness_caveat(text):
    """Does the page say anywhere that no finite example exists?"""
    for sent in re.split(r"(?<=[.!?])\s+", text):
        low = sent.lower()
        if "finite" not in low:
            continue
        if re.search(r"\b(no|not|cannot|can't|never|impossible|must be "
                     r"infinite|every finite)\b", low):
            return True
    return False


def suggest(text, source="page"):
    """Return a list of {id, title, why, evidence, action} dicts."""
    out = []
    types = page_types(text)

    # --- 1. finiteness caveat -------------------------------------------
    infinite = sem.find_infinite_domain(text)
    if infinite and not _has_finiteness_caveat(text):
        out.append({
            "id": "finiteness-caveat",
            "title": "State that no finite example exists",
            "why": ("The constructions here are inherently infinite, but the "
                    "page never says a finite example is impossible. A reader "
                    "may reasonably wonder whether a small example exists and "
                    "waste time looking."),
            "evidence": infinite[0][2],
            "action": ("Add a sentence giving the general reason, e.g. why "
                       "the property in question holds automatically in the "
                       "finite case."),
        })

    # --- 2. unexhibited inputs ------------------------------------------
    try:
        import gapgen
        model = gapgen.build(text, None)
    except Exception:
        model = None

    if model and model["inputs"] and not infinite:
        # Does the page exhibit ANY concrete instance?
        concrete = re.search(
            r"\b(for instance|for example|e\.g\.|such as|explicitly, "
            r"take|particular example)\b", text, re.IGNORECASE)
        seen = set()
        unexhibited = []
        for e in model["inputs"]:
            if not e.get("meaning") or "never constructed" in e["meaning"]:
                continue
            if e["sym"] in seen:
                continue
            seen.add(e["sym"])
            unexhibited.append(e["sym"])
        if unexhibited and not concrete:
            out.append({
                "id": "worked-example",
                "title": "Exhibit a concrete instance",
                "why": ("The proof assumes objects exist without showing one, "
                        "so a reader cannot check the construction against "
                        "anything. The page has finite models, so a smallest "
                        "example is available."),
                "evidence": f"assumed but never exhibited: {', '.join(unexhibited)}",
                "action": ("Give one smallest instance. Minimise the quantity "
                           "that actually drives the size (often an index, not "
                           "a group order)."),
            })

    # --- 3. derivable orders --------------------------------------------
    if not infinite:
        try:
            import ordercalc
            results, _, _ = ordercalc.analyse(text)
        except Exception:
            results = []
        determined = [r for r in results if r["inferrable"]]
        # "size" is the commoner word in practice - the Wedderburn page
        # discusses orders throughout and never once says "order".
        states_order = re.search(
            r"\b(order|cardinality|size|index)\b|\|\s*[A-Z]\s*\|",
            text, re.IGNORECASE)
        if determined and not states_order:
            out.append({
                "id": "order-computation",
                "title": "State the orders of the constructed groups",
                "why": ("The page's own equations determine these, but it "
                        "never says them. Stated orders give a reader a "
                        "cheap sanity check and make the construction's cost "
                        "visible."),
                "evidence": "; ".join(sorted({
                    f"|{r['symbol']}| = {r['order']}" for r in determined})[:4]),
                "action": ("Add the formulas. Once stated they become a "
                           "checkable layer - ordercalc can verify the page's "
                           "figures against its own derivation, which a "
                           "derived-only calculation cannot do."),
            })

    # --- 4. GAP verification --------------------------------------------
    if not infinite and model and model["checks"]:
        if not re.search(r"\bGAP\b", text):
            out.append({
                "id": "gap-verification",
                "title": "Add a GAP verification snippet",
                "why": ("This page's assertions are mechanically checkable "
                        "and it has finite models, but no verification code "
                        "is offered."),
                "evidence": "checkable assertions: " + "; ".join(
                    c["meaning"] for c in model["checks"][:3]),
                "action": ("Run gapgen.py, fill the holes, verify it runs, "
                           "then include the working snippet. Do not paste "
                           "the scaffold unedited."),
            })

    # --- 5. uncited Given (structural, tabular pages only) ---------------
    if "tabular-proof" in types:
        for _, ln, msg in sem.find_uncited_givens(text):
            out.append({
                "id": "given-citation",
                "title": "Record where a hypothesis is first used",
                "why": ("The tabular format's 'Given data used' column is a "
                        "machine-checkable claim about dependencies; leaving "
                        "it blank forfeits that."),
                "evidence": f"line {ln}: {msg}",
                "action": "Cite the Given in the row that first consumes it.",
            })

    return out


def render(items, source):
    if not items:
        return (f"# expansion suggestions for {source}\n\n"
                "No suggestions. (This is a low bar, not a compliment: "
                "suggestions only fire on positive evidence from the page.)")
    L = [f"# expansion suggestions for {source}", ""]
    for i, s in enumerate(items, 1):
        L.append(f"{i}. {s['title']}  [{s['id']}]")
        L.append(f"   why:      {s['why']}")
        L.append(f"   evidence: {s['evidence']}")
        L.append(f"   action:   {s['action']}")
        L.append("")
    L.append(f"-- {len(items)} suggestion(s). These are reminders and starting "
             f"points, not text to paste. --")
    return "\n".join(L)
