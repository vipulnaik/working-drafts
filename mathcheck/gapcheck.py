#!/usr/bin/env python3
r"""
gapcheck.py

Cross-check a page's GAP transcript against its own prose claims.

WHY THIS IS POSSIBLE WITHOUT RUNNING GAP. A page like "Normality is not
transitive" states its key facts TWICE: once in prose ("H_1 is not normal in
G") and once as a pasted GAP session ("gap> IsNormal(G,H1); false"). Those
are two independent renderings of one claim, so they can disagree - and a
disagreement is a defect regardless of which side is wrong.

This is the redundancy-as-verification case in its purest form: the check
exists ONLY because the page says the same thing twice. A page carrying just
the prose, or just the transcript, cannot be checked this way at all.

WHAT IT CATCHES. A transcript edited out of step with the prose - a flipped
true/false, a predicate applied to the wrong pair, a claim present in one
layer and absent from the other. What it does NOT catch is a transcript that
is wrong in the same way the prose is wrong: correlated errors are invisible
to any consistency check.

WHAT IT DOES NOT DO. It does not verify that the GAP output is CORRECT - that
needs GAP. It only verifies the two layers agree.
"""

import re

import latex_semantic_scan as sem

# GAP predicate -> (relation name, argument order).
# GAP's convention is Predicate(BIG, SMALL): IsNormal(G,H) asks whether H is
# normal in G, so the subject of the English claim is the SECOND argument.
GAP_PREDICATES = {
    "isnormal": "normal in",
    "issubgroup": "subgroup of",
    "ischaracteristicsubgroup": "characteristic in",
    "issubnormal": "subnormal in",
}

# How the same relation reads in prose. Group 'neg' captures a negation.
PROSE_RELATIONS = {
    "normal in": r"normal(?:\s+subgroup)?\s+(?:in|of)",
    "subgroup of": r"subgroup\s+of",
    "characteristic in": r"characteristic(?:\s+subgroup)?\s+(?:in|of)",
    "subnormal in": r"subnormal\s+(?:in|of)",
}

PRE_RE = re.compile(r"<pre>(.*?)</pre>", re.DOTALL | re.IGNORECASE)
CALL_RE = re.compile(
    r"gap>\s*(?P<pred>\w+)\s*\(\s*(?P<a>[^,()]+?)\s*,\s*(?P<b>[^,()]+?)\s*\)\s*;"
    r"\s*\n\s*(?P<val>true|false)\b",
    re.IGNORECASE)


def _norm(sym):
    """GAP identifiers vs LaTeX: H1 <-> H_1, Gbar <-> \\overline{G}."""
    s = sym.strip()
    s = re.sub(r"\\[a-zA-Z]+|[{}\\$]", "", s)
    s = s.replace("_", "")
    return s.lower()


def gap_claims(text):
    """[(relation, subject, object, truth, line)] from <pre> transcripts."""
    out = []
    for blk in PRE_RE.finditer(text):
        base = text.count("\n", 0, blk.start()) + 1
        body = blk.group(1)
        for m in CALL_RE.finditer(body):
            pred = m.group("pred").lower()
            rel = GAP_PREDICATES.get(pred)
            if not rel:
                continue
            # Predicate(BIG, SMALL) -> "SMALL rel BIG"
            out.append((rel, m.group("b"), m.group("a"),
                        m.group("val").lower() == "true",
                        base + body[:m.start()].count("\n")))
    return out


def prose_claims(text):
    """[(relation, subject, object, truth)] from prose outside <pre>."""
    prose = PRE_RE.sub(" ", text)
    prose = re.sub(r"<math>(.*?)</math>", lambda m: f"\x01{m.group(1)}\x01",
                   prose, flags=re.DOTALL)
    prose = re.sub(r"\[\[[^\]]*\]\]", " ", prose)
    prose = prose.replace("''", "")

    out = []
    for rel, pat in PROSE_RELATIONS.items():
        # Single subject: "H_1 is [not] normal in G".
        # The optional 'coord' group exists to be REJECTED: without it this
        # pattern also matches inside a coordinated construction, so
        # "neither H_1 nor H_2 is normal in G" yields a bogus positive
        # "H_2 is normal in G" - which then sits alongside the correct
        # negative and silently disables the conflict check for that pair.
        rx = re.compile(
            r"(?P<coord>\b(?:and|nor|or)\s+)?"
            r"\x01(?P<subj>[^\x01]+)\x01\s+(?:is|are)\s+(?P<neg>not\s+)?"
            r"(?:an?\s+|the\s+)?" + pat + r"\s+\x01(?P<obj>[^\x01]+)\x01",
            re.IGNORECASE)
        for m in rx.finditer(prose):
            if m.group("coord"):
                continue  # handled by the coordinated pattern below
            out.append((rel, m.group("subj"), m.group("obj"),
                        m.group("neg") is None))

        # Coordinated subjects: "H_1 and H_2 are not normal in G",
        # "neither H_1 nor H_2 is normal in G". The claim distributes over
        # both subjects, and on this kind of page the negative coordinated
        # form carries the main result - missing it loses exactly the claim
        # the transcript exists to corroborate.
        rx2 = re.compile(
            r"(?P<neither>neither\s+)?"
            r"\x01(?P<s1>[^\x01]+)\x01\s*(?:,|and|nor|or)\s*"
            r"\x01(?P<s2>[^\x01]+)\x01\s+(?:is|are)\s+(?:both\s+)?"
            r"(?P<neg>not\s+)?(?:an?\s+|the\s+)?" + pat +
            r"\s+\x01(?P<obj>[^\x01]+)\x01",
            re.IGNORECASE)
        for m in rx2.finditer(prose):
            truth = (m.group("neg") is None) and (m.group("neither") is None)
            for s in (m.group("s1"), m.group("s2")):
                out.append((rel, s, m.group("obj"), truth))
    return out


def prose_claims_scoped(text, skip_exempt=True):
    """prose_claims, restricted to sections that make claims about THIS page.

    Related facts / Facts used tables state conditional conclusions ("if H is
    characteristic in K, then H IS normal in G") that are hypotheses of other
    theorems, not assertions about this page's objects. Counting them makes
    the page look self-contradictory.
    """
    out = []
    for scope, seg in sem.split_into_scopes(text):
        if skip_exempt and sem.is_exempt_scope(scope):
            continue
        out.extend(prose_claims(seg))
    return out


def find_prose_self_conflicts(text):
    """The page asserting BOTH polarities of the same claim.

    Separate from the GAP check because it masks it: a page states its key
    facts several times, so corrupting ONE statement leaves the others
    intact, the key ends up holding both True and False, and every
    comparison against it silently passes. The masking is the reason to
    check for it, but a page contradicting itself is a defect on its own
    terms regardless.
    """
    seen = {}
    for rel, subj, obj, truth in prose_claims_scoped(text):
        seen.setdefault((rel, _norm(subj), _norm(obj)),
                        {"truths": set(), "subj": subj, "obj": obj})
        seen[(rel, _norm(subj), _norm(obj))]["truths"].add(truth)
    out = []
    for (rel, _, _), info in sorted(seen.items()):
        if len(info["truths"]) > 1:
            out.append((
                "PROSE_SELF_CONFLICT", 0,
                f"the page states both that '{info['subj'].strip()} {rel} "
                f"{info['obj'].strip()}' and that it does not. One of the "
                f"statements is stale - and while both stand, any check "
                f"comparing against this claim is disabled"))
    return out


def find_gap_prose_conflicts(text):
    """Return [(severity, line, message)] where transcript and prose differ."""
    issues = []
    gap = gap_claims(text)
    if not gap:
        return issues

    prose = {}
    for rel, subj, obj, truth in prose_claims(text):
        prose.setdefault((rel, _norm(subj), _norm(obj)), set()).add(truth)

    for rel, subj, obj, truth, line in gap:
        key = (rel, _norm(subj), _norm(obj))
        if key not in prose:
            continue  # transcript covers something prose doesn't state
        if truth not in prose[key]:
            issues.append((
                "GAP_PROSE_CONFLICT", line,
                f"GAP says '{subj.strip()} {rel} {obj.strip()}' is "
                f"{str(truth).lower()}, but the prose states the opposite. "
                f"One of the two layers is out of date - the transcript is "
                f"not evidence for a claim it contradicts"))
    return issues
