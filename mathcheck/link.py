#!/usr/bin/env python3
r"""
link.py

Chain one page's construction onto another page's worked example.

THE PROBLEM. A constructive page assumes inputs it does not exhibit: the
3-subnormal page needs "a nontrivial 2-subnormal subgroup H of G that is not
normal" and never produces one. Another page - "Normality is not transitive"
- exhibits exactly that in D8. Chaining them turns an unrunnable scaffold
into a concrete instance.

WHY NAME MATCHING IS THE WRONG APPROACH, using these two pages:

    page A (3-subnormal)          H  = the 2-subnormal non-normal subgroup
    page B (normality)            H  = an arbitrary building-block group
    page B                        H_1 = the 2-subnormal non-normal subgroup

So A.H corresponds to B.H_1, NOT to B.H. Matching on the name would bind A.H
to B.H - and because in the smallest case both happen to have order 2, the
order arithmetic would come out RIGHT while the correspondence was wrong.
A coincidence that produces a correct number is the worst possible failure,
because nothing downstream can detect it.

WHAT THIS DOES INSTEAD. Match on PROPERTIES. Derive what each symbol on the
supplying page is known to satisfy, parse what the consuming page requires,
and bind only where the properties agree. The name is then reported as
corroborating or CONFLICTING evidence - never as the basis of the match.

DERIVATION. Subnormal depth comes from chains of normality: if X is normal
in Y and Y is normal in Z, then X is 2-subnormal in Z. That is the one
inference rule here, and it is the one the pages actually rely on.

SCOPE. This proposes bindings for a human or LLM to approve; it does not
apply them. Approved bindings belong in the consuming page's overlay, where
they persist with provenance.
"""

import re

import gapcheck
import latex_semantic_scan as sem


# --------------------------------------------------------------------------
# What a page PROVIDES
# --------------------------------------------------------------------------

# Sections that state a theorem rather than exhibit an object. A symbol
# there is a BOUND VARIABLE of the statement ("suppose H is normal in K..."),
# not a witness you can substitute into another page's construction. It will
# satisfy every required property by construction - that is what the theorem
# says - while denoting nothing concrete.
ABSTRACT_SECTIONS = {"statement", "partial truth", "corollaries", "analysis",
                     "definition", "related facts", "facts used"}


def _is_abstract(scope):
    return bool(scope) and scope[0].strip().lower() in ABSTRACT_SECTIONS


def relations(text):
    """{(subject, object, abstract): {relation: truth}} from a page's prose,
    tagged by whether the claim sits in an abstract or a worked section."""
    rel = {}
    for scope, seg in sem.split_into_scopes(text):
        abstract = _is_abstract(scope)
        for r, subj, obj, truth in gapcheck.prose_claims(seg):
            key = (subj.strip(), obj.strip(), abstract)
            rel.setdefault(key, {})
            # A negative claim is never overwritten by a positive one: pages
            # state "H_1 is normal in K" and "H_1 is NOT normal in G", and
            # losing the negative loses the point of the example.
            if r in rel[key] and rel[key][r] is False:
                continue
            rel[key][r] = truth
    return rel


def subnormal_depths(rel):
    """{(subject, object): depth} from chains of normality.

    depth 1 = normal. depth 2 = normal in something normal in the target.
    Only the single rule the pages use; no attempt at a general closure.
    """
    normal_in = {(a, b, ab) for (a, b, ab), rs in rel.items()
                 if rs.get("normal in") is True}
    depth = {pair: 1 for pair in normal_in}
    for (x, y, ab) in list(normal_in):
        for (y2, z, ab2) in normal_in:
            if y2 == y and ab2 == ab and (x, z, ab) not in depth:
                depth[(x, z, ab)] = 2
    return depth


def provides(text):
    """[{symbol, ambient, properties}] - what each symbol is known to satisfy."""
    rel = relations(text)
    depth = subnormal_depths(rel)
    out = {}
    for (subj, obj, ab), rs in rel.items():
        e = out.setdefault((subj, obj, ab), {"symbol": subj, "ambient": obj,
                                             "abstract": ab,
                                             "properties": set()})
        for r, truth in rs.items():
            e["properties"].add(("" if truth else "not ") + r)
    for (subj, obj, ab), d in depth.items():
        e = out.setdefault((subj, obj, ab), {"symbol": subj, "ambient": obj,
                                             "abstract": ab,
                                             "properties": set()})
        e["properties"].add(f"{d}-subnormal in")
    return list(out.values())


# --------------------------------------------------------------------------
# What a page REQUIRES
# --------------------------------------------------------------------------

REQUIREMENT_PATTERNS = [
    (r"(?P<k>\d)-subnormal", lambda m: f"{m.group('k')}-subnormal in"),
    (r"\bnot\s+normal\b", lambda m: "not normal in"),
    (r"\bnormal\b(?!.*\bnot\b)", lambda m: "normal in"),
    (r"\bcharacteristic\b", lambda m: "characteristic in"),
]


def requires(description):
    """Parse a requirement description into a set of property strings."""
    props = set()
    low = description.lower()
    # "not normal" must be tested before the bare "normal" pattern.
    if re.search(r"\bnot\s+normal\b", low):
        props.add("not normal in")
    m = re.search(r"(?P<k>\d)-subnormal", low)
    if m:
        props.add(f"{m.group('k')}-subnormal in")
    if re.search(r"\bcharacteristic\b", low):
        props.add("characteristic in")
    return props


# --------------------------------------------------------------------------
# Matching
# --------------------------------------------------------------------------

def match(consumer_symbol, requirement, supplier_text, supplier_name="supplier"):
    """Propose bindings for `consumer_symbol` from the supplying page.

    Returns a list of candidate dicts, best first.
    """
    needed = requires(requirement)
    cands = []
    for p in provides(supplier_text):
        have = p["properties"]
        missing = needed - have
        if missing:
            continue
        cands.append({
            "consumer_symbol": consumer_symbol,
            "supplier_symbol": p["symbol"],
            "supplier_ambient": p["ambient"],
            "supplier_page": supplier_name,
            "required": sorted(needed),
            "satisfied_by": sorted(have),
            "name_matches": p["symbol"].strip() == consumer_symbol.strip(),
            "abstract": p["abstract"],
        })

    # A name-based match that the PROPERTIES reject is the dangerous case:
    # it is what a naive matcher would pick, and it can yield a correct
    # number from a wrong correspondence.
    name_twin = [p for p in provides(supplier_text)
                 if p["symbol"].strip() == consumer_symbol.strip()]
    decoys = [p for p in name_twin
              if not needed <= p["properties"]
              and p["symbol"] not in {c["supplier_symbol"] for c in cands}]

    # Concrete witnesses first. A name match is corroboration, never the
    # basis of a binding, so it only breaks ties among equally concrete
    # candidates.
    cands.sort(key=lambda c: (c["abstract"], not c["name_matches"]))
    return cands, decoys


def render(consumer_symbol, requirement, cands, decoys, supplier_name):
    L = [f"# binding '{consumer_symbol}' from {supplier_name}",
         f"#   required: {requirement}", ""]
    if not cands:
        L.append("No symbol on the supplying page satisfies the requirement.")
    for c in cands:
        L.append(f"CANDIDATE  {consumer_symbol}  :=  {c['supplier_symbol']} "
                 f"(in {c['supplier_ambient']})")
        L.append(f"    satisfies: {', '.join(c['required'])}")
        L.append(f"    known to be: {', '.join(c['satisfied_by'])}")
        L.append("    name match: " + ("yes (corroborating only)"
                                        if c["name_matches"]
                                        else "NO - matched on properties alone"))
        if c["abstract"]:
            L.append("    ABSTRACT: this symbol is a bound variable of a "
                     "theorem statement, not an exhibited object - it "
                     "satisfies the requirement by hypothesis, so it is not "
                     "a witness")
        L.append("")
    for d in decoys:
        L.append(f"!! NAME DECOY: the supplying page also has a symbol named "
                 f"'{d['symbol']}', which is what a name-based matcher would "
                 f"pick - but it does NOT satisfy the requirement.")
        L.append(f"    it is only known to be: "
                 f"{', '.join(sorted(d['properties'])) or '(nothing relevant)'}")
        L.append(f"    binding to it could still produce plausible numbers, "
                 f"so a correct-looking result is not evidence the "
                 f"correspondence is right.")
        L.append("")
    return "\n".join(L)


# --------------------------------------------------------------------------
# Concrete orders stated on the supplying page
# --------------------------------------------------------------------------

_NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                 "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                 "twelve": 12, "sixteen": 16, "twenty-four": 24}


def stated_orders(text):
    """{symbol: order} for orders the supplying page states in prose.

    Pages give the smallest case in words - "H_1 a group of order two, and G
    a group of order eight" - so a digit-only scan finds nothing.
    """
    out = {}
    pat = re.compile(
        r"<math>(?P<sym>[^<]+)</math>\s+(?:a|an|the)?\s*group of order\s+"
        r"(?P<ord>\w+)", re.IGNORECASE)
    for m in pat.finditer(text):
        raw = m.group("ord").lower()
        val = _NUMBER_WORDS.get(raw)
        if val is None and raw.isdigit():
            val = int(raw)
        if val is not None:
            out[m.group("sym").strip()] = val
    return out


def build_substitution(bindings, supplier_text):
    """Given approved {consumer_symbol: supplier_symbol}, return the orders
    to feed into ordercalc, keyed by the CONSUMER page's names."""
    orders = stated_orders(supplier_text)
    subs, unresolved = {}, []
    for consumer, supplier in bindings.items():
        if supplier in orders:
            subs[consumer] = orders[supplier]
        else:
            unresolved.append((consumer, supplier))
    return subs, unresolved
