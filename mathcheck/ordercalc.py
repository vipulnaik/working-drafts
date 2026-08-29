#!/usr/bin/env python3
r"""
ordercalc.py

Symbolic order arithmetic for constructive proofs.

IDEA. A construction like "A = \mathbb{F}_p[G] \rtimes G" determines |A|
completely in terms of |G| and p, even when nothing about G is known. So:
assign a free symbol to each order that is NOT inferrable (the given groups,
the chosen prime), then propagate known order formulas through every
construction the page defines, and report a closed form for each.

This is deliberately NOT parsed from prose. The prose forms ("the restricted
wreath product of S and G, where G acts via the regular action of G/H") are
ambiguous about which set indexes the power, which is exactly the operand
gapgen has to leave as a TODO. The LaTeX equation forms on the same pages
("A = \mathbb{F}_p[G] \rtimes G", "V = S^{G/H}") are an expression grammar
already, and are what this reads.

ORDER FORMULAS USED
    X \times Y, X \rtimes Y, X \ltimes Y      |X| * |Y|
    X^{Y}   (direct power indexed by a set)   |X| ^ |Y|
    X / Y   (quotient)                        |X| / |Y|
    \mathbb{F}_p[G]  (additive group)         p ^ |G|
    \langle ... \rangle, N_A(B), C_K(V)       NOT inferrable -> free symbol

The last line matters: a normalizer, centralizer or join has no order
formula in general, so this introduces a fresh symbol rather than guessing.
Where the PROSE separately identifies such a subgroup with a construction
(the pages say N_A(B) = \mathbb{F}_p[G] \rtimes H), that equation is picked
up like any other and the order follows.

Usage:
    python3 ordercalc.py page.mediawiki
    python3 ordercalc.py page.mediawiki --json
"""

import argparse
import json
import re
import sys
from pathlib import Path

import sympy as sp

import latex_semantic_scan as sem
import overlay as ov


# --------------------------------------------------------------------------
# Tokenizing / parsing construction expressions
# --------------------------------------------------------------------------

def strip_math(s):
    s = s.strip()
    s = re.sub(r"^\\!\s*", "", s)
    s = re.sub(r"\s+", " ", s)
    return s


def split_top(expr, ops):
    """Split on the first top-level occurrence of any operator in `ops`
    (a list of literal strings), respecting {} [] () nesting."""
    depth = 0
    i = 0
    while i < len(expr):
        c = expr[i]
        if c in "{[(":
            depth += 1
        elif c in "}])":
            depth -= 1
        elif depth == 0:
            for op in ops:
                if expr.startswith(op, i):
                    return expr[:i], op, expr[i + len(op):]
        i += 1
    return None


class Unknown(Exception):
    """The expression has no general order formula."""


def order_of(expr, env, fresh):
    """Return a sympy expression for the order of the group denoted by
    `expr`. `env` maps symbol name -> sympy order expression. `fresh`
    mints a new free symbol for anything not inferrable."""
    expr = strip_math(expr)

    # Strip one layer of redundant outer braces/parens
    while (expr.startswith("{") and expr.endswith("}")) or \
          (expr.startswith("(") and expr.endswith(")")):
        inner = expr[1:-1]
        if split_top(inner, ["}", ")"]) is None:
            expr = inner.strip()
        else:
            break

    # Product-like operators: order multiplies.
    part = split_top(expr, [r"\rtimes", r"\ltimes", r"\times", r"\wr"])
    if part:
        a, op, b = part
        if op == r"\wr":
            # X wr Y needs the index set; not determined by the expression
            raise Unknown(f"wreath product {expr!r} needs its index set")
        return order_of(a, env, fresh) * order_of(b, env, fresh)

    # Quotient
    part = split_top(expr, ["/"])
    if part:
        a, _, b = part
        return order_of(a, env, fresh) / order_of(b, env, fresh)

    # Group algebra F_p[G]: additive group is elementary abelian of rank |G|
    m = re.fullmatch(r"\\mathbb\{F\}_\{?(\w+)\}?\s*\[\s*(.+?)\s*\]", expr)
    if m:
        p, base = m.group(1), m.group(2)
        p_sym = env.get(p) or fresh(p)
        return p_sym ** order_of(base, env, fresh)

    # Direct power X^{Y} : |X|^|Y| where Y indexes the copies
    part = split_top(expr, ["^"])
    if part:
        a, _, b = part
        return order_of(a, env, fresh) ** order_of(b, env, fresh)

    # Join / generated subgroup: no formula
    if expr.startswith(r"\langle"):
        raise Unknown(f"join {expr!r} has no general order formula")

    # Set-builder {x | condition}: the order depends on the condition, which
    # is prose. Must NOT fall through to the bare-symbol case below, which
    # would mint a free symbol named after the whole expression and then
    # report it as "determined".
    if expr.startswith(r"\{") or expr.startswith("{"):
        raise Unknown(f"set-builder {expr[:40]!r} has no order formula "
                      f"(depends on the defining condition)")

    # Normalizer / centralizer notation: no formula
    if re.fullmatch(r"[NC]_\{?\w+\}?\s*\(.*\)", expr):
        raise Unknown(f"{expr!r} (normalizer/centralizer) has no general "
                      f"order formula")

    # A bare symbol
    name = expr.strip()
    if name in env:
        return env[name]
    # A genuine bare symbol (G, H_1, \R, \mathbb{Q}) gets a free symbol.
    # A compound expression must not: naming a free symbol after a whole
    # expression disguises "we have no idea" as "determined".
    if re.fullmatch(r"[A-Za-z]\w*(_\{?\w+\}?)?", name) or \
       re.fullmatch(r"\\[a-zA-Z]+(\{\w+\})?(\^\S+)?", name):
        return fresh(name)
    raise Unknown(f"cannot interpret {expr!r}")


# --------------------------------------------------------------------------
# Harvesting definitional equations from the page
# --------------------------------------------------------------------------

DEF_RE = re.compile(
    r"^\s*(?P<lhs>[A-Za-z](?:_\{[^{}]*\}|_\w)?"          # B, C_1, V
    r"|[NC]_\{?\w+\}?\s*\([^)]*\))"                       # N_A(B)
    r"\s*=\s*(?P<rhs>.+?)\s*$"
)


def harvest(text):
    """Return [(lhs, rhs, scope)] for every definitional equation in a math
    span. Chained definitions separated by commas are split, so
    'C_1 = ..., C_2 = ...' yields two."""
    out = []
    for scope_path, seg in sem.split_into_scopes(text):
        seg = sem.strip_wiki_markup(seg)
        _, spans = sem.desugar(seg)
        for content in spans:
            for piece in re.split(r",\s*(?=[A-Za-z][\w_]*\s*=)", content):
                m = DEF_RE.match(strip_math(piece))
                if m:
                    out.append((m.group("lhs").strip(),
                                m.group("rhs").strip(),
                                scope_path))
    return out


# Prose-defined constructions. Some pages define a group only in words
# ("Let K be the semidirect product of V and G") with no equation anywhere,
# so the equation harvester never sees it. This recovers the narrow case
# where BOTH operands appear as math spans joined by "and". Deliberately
# limited: the wreath-product prose form does not say which set indexes the
# power, so it stays out - that ambiguity is real, not a parsing shortfall.
PROSE_DEFS = [
    (re.compile(
        r"SYM\((?P<lhs>[^)]+)\)\s+(?:is|be)\s+the\s+semidirect product of\s+"
        r"(?:the\s+[\w -]+\s+)?SYM\((?P<a>[^)]+)\)\s+and\s+SYM\((?P<b>[^)]+)\)",
        re.IGNORECASE), r"{a} \rtimes {b}"),
    (re.compile(
        r"SYM\((?P<lhs>[^)]+)\)\s+(?:is|be)\s+the\s+direct product of\s+"
        r"(?:the\s+[\w -]+\s+)?SYM\((?P<a>[^)]+)\)\s+and\s+SYM\((?P<b>[^)]+)\)",
        re.IGNORECASE), r"{a} \times {b}"),
]


def harvest_prose(text):
    """[(lhs, rhs, scope, 'prose')] for constructions stated only in words."""
    out = []
    for scope_path, seg in sem.split_into_scopes(text):
        seg = sem.strip_wiki_markup(seg)
        desugared, _ = sem.desugar(seg)
        for rx, tmpl in PROSE_DEFS:
            for m in rx.finditer(desugared):
                g = m.groupdict()
                lhs = g["lhs"].strip()
                # An operand may itself carry its definition ("V = S^{G/H}");
                # keep only the symbol being named.
                a = g["a"].split("=")[0].strip()
                b = g["b"].split("=")[0].strip()
                out.append((lhs, tmpl.format(a=a, b=b), scope_path))
    return out


def analyse(text):
    # (text is needed for scalar detection below)
    env = {}
    free = {}
    notes = []

    # Symbols appearing as the subscript of \mathbb{F}_p are field sizes -
    # scalars, not group orders - so they must not be printed as |p|.
    display = {}
    scalars = set(re.findall(r"\\mathbb\{F\}_\{?(\w+)\}?", text))

    # Symbol NAMES must round-trip through sympify so a caller can feed the
    # emitted formulas back into a solver; "|G|" does not parse. Use ord_G
    # internally and carry a display map for human output.
    def fresh(name):
        key = re.sub(r"[^\w]", "", name) or "x"
        if key not in free:
            if key in scalars:
                sym = sp.Symbol(key, positive=True)
                display[str(sym)] = key
            else:
                sym = sp.Symbol(f"ord_{key}", positive=True)
                display[str(sym)] = f"|{name}|"
            free[key] = sym
        return free[key]

    results = []
    for lhs, rhs, scope in harvest(text) + harvest_prose(text):
        try:
            val = sp.simplify(order_of(rhs, env, fresh))
            env[lhs] = val
            results.append({
                "symbol": lhs,
                "expression": rhs,
                "order": sp.sstr(val),
                "scope": list(scope),
                "inferrable": True,
            })
        except Unknown as e:
            sym = fresh(lhs)
            env[lhs] = sym
            results.append({
                "symbol": lhs,
                "expression": rhs,
                "order": sp.sstr(sym),
                "scope": list(scope),
                "inferrable": False,
                "reason": str(e),
            })
    return results, free, display


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--assume", action="append", default=[], metavar="SYM=VAL",
                    help="Supply a known order, e.g. --assume G=8 --assume H=2. "
                         "Use the bare symbol name; |G| is written G.")
    ap.add_argument("--overlay", default=None,
                    help="Persisted refinement overlay (see overlay.py). "
                         "Supplies orders without retyping --assume; "
                         "explicit --assume still wins.")
    ap.add_argument("--minimal", action="store_true",
                    help="Fill unsupplied scalars with their smallest legal "
                         "value (prime -> 2, odd prime -> 3). Group orders are "
                         "NOT guessed: there is no canonical smallest group.")
    args = ap.parse_args()

    text = Path(args.file).read_text()
    results, free, display = analyse(text)

    if args.json:
        print(json.dumps({"orders": results,
                          "free_symbols": sorted(str(s) for s in free.values()),
                          "display_names": display},
                         indent=2, ensure_ascii=False))
        return 0

    # Substitution. Group orders must be supplied explicitly - unlike a
    # prime, a group has no canonical smallest instance, and the pages'
    # constraints ("2-subnormal but not normal") are not expressible here.
    subs = {}
    # Overlay first, so an explicit --assume on the command line overrides it.
    if args.overlay:
        for k, v in ov.resolved_orders(ov.load(args.overlay)).items():
            target = free.get(re.sub(r"[^\w]", "", k))
            if target is not None:
                subs[target] = sp.sympify(v)
    for a in args.assume:
        if "=" not in a:
            print(f"bad --assume {a!r}, expected SYM=VALUE", file=sys.stderr)
            return 2
        k, v = a.split("=", 1)
        k, v = k.strip(), v.strip()
        target = free.get(k)
        if target is None:
            print(f"# warning: no symbol {k!r} on this page "
                  f"(known: {', '.join(sorted(free))})", file=sys.stderr)
            continue
        subs[target] = sp.sympify(v)

    if args.minimal:
        for k, sym in free.items():
            if sym in subs or str(sym).startswith("ord_"):
                continue
            lowered = k.lower()
            if "oddprime" in lowered or lowered in ("q",):
                subs.setdefault(sym, sp.Integer(3))
            else:
                subs.setdefault(sym, sp.Integer(2))

    inf = sem.find_infinite_domain(text)
    if inf:
        print(f"# NOT FINITELY INSTANTIABLE")
        for _, ln, msg in inf:
            print(f"#   line {ln}: {msg}")
        print(f"#   Orders below are formal only - every quantity is "
              f"infinite, so numeric substitution is meaningless here.\n")

    print(f"# order analysis of {args.file}\n")
    def show(expr_str):
        for k, v in sorted(display.items(), key=lambda kv: -len(kv[0])):
            expr_str = expr_str.replace(k, v)
        return expr_str

    print("Free symbols (orders not determined by the page):")
    for k in sorted(free):
        print(f"    {display.get(str(free[k]), str(free[k]))}")
    print()
    if subs:
        print("Assumed:")
        for k, v in subs.items():
            print(f"    {display.get(str(k), str(k))} = {v}")
        print()

    for r in results:
        sc = r["scope"][-1] if r["scope"] else "top"
        mark = "" if r["inferrable"] else "   [not inferrable]"
        print(f"[{sc}] {r['symbol']} = {r['expression']}")
        print(f"        |{r['symbol']}| = {show(r['order'])}{mark}")
        if subs and r["inferrable"]:
            val = sp.simplify(sp.sympify(r["order"],
                                         locals={str(x): x for x in free.values()}).subs(subs))
            if val.free_symbols:
                print(f"          with assumptions: {show(sp.sstr(val))}")
            else:
                print(f"          = {val}")
        if not r["inferrable"]:
            print(f"        reason: {r['reason']}")
    print(f"\n-- {sum(1 for r in results if r['inferrable'])} of "
          f"{len(results)} order(s) determined --")
    return 0


if __name__ == "__main__":
    sys.exit(main())
