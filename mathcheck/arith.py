#!/usr/bin/env python3
r"""
arith.py

Evaluate the arithmetic a page states about itself.

WHY THIS PAGE TYPE IS DIFFERENT. The proof pages carry their redundancy in
prose: a symbol characterized twice, a hypothesis cited in a column. A
"specific information" page carries it in NUMBERS. The S3 element-structure
page computes the order 6 five different ways, the number of conjugacy
classes three ways, and writes out each evaluation in full:

    3! = 3 \cdot 2 \cdot 1 = 6
    (2^2 - 1)(2^2 - 2) = (3)(2) = 6
    q(q - 1) = 3(3 - 1) = 3(2) = 6

Every one of those is a claim that can simply be checked. No parsing of
English, no judgment: evaluate both sides and compare. This is the highest
density of mechanically verifiable content anywhere in the corpus, and none
of the earlier tooling touches it - the declaration machinery finds barely
any declarations on such a page.

WHAT IT DOES. Split each math span on '=', evaluate every segment that is
purely numeric, and require them all to agree. Segments containing free
variables (q(q-1), n!) are skipped rather than guessed at - a chain like
"q(q - 1) = 3(3 - 1) = 3(2) = 6" is checked on its last three terms, which
is exactly the part the page is asserting is arithmetic.

WHAT IT DOES NOT DO. It does not check that the FORMULA is right for the
family - that q(q-1) really is the order of GA(1,q). It checks that the
page's own evaluation of its own formula is self-consistent.
"""

import re

import sympy as sp

# LaTeX shorthands -> something sympify understands.
REPLACEMENTS = [
    (r"\\!", ""),
    (r"\\,", ""),
    (r"\\;", ""),
    (r"\\cdot", "*"),
    (r"\\times", "*"),
    (r"\\left", ""),
    (r"\\right", ""),
    (r"\\displaystyle", ""),
]

FRAC_RE = re.compile(r"\\d?frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}")


def latex_to_expr(s):
    """Best-effort conversion of a simple arithmetic LaTeX fragment."""
    for pat, rep in REPLACEMENTS:
        s = re.sub(pat, rep, s)
    # \frac{a}{b} -> (a)/(b), repeatedly for nesting
    prev = None
    while prev != s:
        prev = s
        s = FRAC_RE.sub(r"((\1)/(\2))", s)
    s = s.replace("{", "(").replace("}", ")")
    # factorial: 3! -> factorial(3)
    s = re.sub(r"(\d+)\s*!", r"factorial(\1)", s)
    # implicit multiplication: (3)(2) -> (3)*(2), 3(2) -> 3*(2), 2(3-1)
    s = re.sub(r"\)\s*\(", ")*(", s)
    s = re.sub(r"(\d)\s*\(", r"\1*(", s)
    s = re.sub(r"\)\s*(\d)", r")*\1", s)
    s = s.replace("^", "**")
    return s.strip()


NUMERIC_RE = re.compile(r"^[\d\s+\-*/().!^]*$")


def numeric_value(segment):
    """Value of a segment if it is purely numeric, else None."""
    expr = latex_to_expr(segment)
    # A segment with any letter left in it refers to a free variable
    # (or an unconverted command) - not something to evaluate.
    probe = expr.replace("factorial", "")
    if re.search(r"[A-Za-z\\]", probe):
        return None
    if not probe.strip():
        return None
    try:
        val = sp.sympify(expr, rational=True)
        if val.free_symbols:
            return None
        return sp.nsimplify(val)
    except Exception:
        return None


MATH_RE = re.compile(r"<[Mm][Aa][Tt][Hh]>(.+?)</[Mm][Aa][Tt][Hh]>", re.DOTALL)


def find_arithmetic_errors(text):
    """Return [(severity, line, message)] for stated identities that fail."""
    issues = []
    for m in MATH_RE.finditer(text):
        content = m.group(1)
        # Only equality chains; skip congruences, inequalities, definitions
        # involving relations we are not evaluating.
        if "=" not in content:
            continue
        if re.search(r"\\(le|ge|neq|equiv|pmod|cong|approx|sim|mapsto|in)\b",
                     content):
            continue
        if re.search(r"[<>]", content):
            continue
        segments = [s for s in content.split("=") if s.strip()]
        if len(segments) < 2:
            continue

        vals = []
        for seg in segments:
            v = numeric_value(seg)
            if v is not None:
                vals.append((seg.strip(), v))
        if len(vals) < 2:
            continue
        first = vals[0][1]
        for seg, v in vals[1:]:
            if sp.simplify(v - first) != 0:
                line = text.count("\n", 0, m.start()) + 1
                issues.append((
                    "ARITHMETIC_ERROR", line,
                    f"stated identity does not hold: {content.strip()[:70]!r} "
                    f"- '{vals[0][0]}' evaluates to {first} but '{seg}' "
                    f"evaluates to {v}"))
                break
    return issues


def summarize(text):
    """(checked, skipped) counts, for calibration."""
    checked = skipped = 0
    for m in MATH_RE.finditer(text):
        c = m.group(1)
        if "=" not in c:
            continue
        segs = [s for s in c.split("=") if s.strip()]
        vals = [numeric_value(s) for s in segs]
        if sum(v is not None for v in vals) >= 2:
            checked += 1
        else:
            skipped += 1
    return checked, skipped
