#!/usr/bin/env python3
r"""
latex_var_scan.py

Deterministic, no-dependency sanity scanner for math expressions written in
LaTeX / MediaWiki-math-flavored LaTeX. Does NOT typeset or fully parse LaTeX;
it tokenizes math-mode content into "atoms" and classifies each atom as:

    OPERATOR   - known relation/operator macro (\sum, \in, \to, ...)
    FUNCTION   - known named function (\log, \gcd, \dim, ...)
    VARIABLE   - a bare or decorated symbol (x, n, \alpha, x_i, \hat{G}, ...)
    UNKNOWN    - a macro not in any known list (likely typo or needs adding)

Intended use: run over a .md/.wiki/.tex file, extract math spans, list all
VARIABLE atoms, and diff against a registry of "already declared" variables
to flag NEW variables per section/file. This is a *recall-biased* tool:
it is tuned to over-flag ambiguous tokens as variables rather than miss them,
since the human reviewer's job is to skim the flagged list, not trust it blindly.

No LaTeX installation required - pure Python stdlib regex/tokenizing.
"""

import re
import json
import sys
import argparse
from pathlib import Path

# --------------------------------------------------------------------------
# 1. Known symbol tables (extend these freely - this is the main lever for
#    reducing false positives, and it's meant to be edited per-project).
# --------------------------------------------------------------------------

KNOWN_OPERATORS = {
    "sum", "prod", "int", "oint", "bigcup", "bigcap", "bigoplus",
    "in", "notin", "subset", "subseteq", "supset", "supseteq",
    "cup", "cap", "setminus", "times", "otimes", "oplus",
    "forall", "exists", "nexists",
    "to", "mapsto", "implies", "iff", "Rightarrow", "Leftrightarrow",
    "leq", "geq", "neq", "approx", "equiv", "sim", "simeq", "cong",
    "le", "ge", "ll", "gg",
    "partial", "nabla", "infty",
    "wedge", "vee", "neg", "lnot",
    "leftarrow", "rightarrow", "longrightarrow", "longleftarrow",
    "quad", "qquad", "cdot", "cdots", "ldots", "vdots", "ddots",
    "left", "right", "big", "Big", "bigg", "Bigg",
    "text", "mathrm", "operatorname",  # these wrap prose/labels, not vars
}

KNOWN_FUNCTIONS = {
    "log", "ln", "exp", "sin", "cos", "tan", "sec", "csc", "cot",
    "gcd", "lcm", "dim", "deg", "det", "ker", "im", "rank",
    "min", "max", "sup", "inf", "lim", "limsup", "liminf",
    "Aut", "Inn", "Hom", "End", "Gal", "Spec",
}

# Macros that denote a *set/space* constant rather than a free variable
# (\mathbb{R}, \mathbb{Z}, etc.) - still worth listing separately since
# they're not "new variables" but also not operators.
KNOWN_CONSTANTS = {
    "mathbb",  # handled specially: \mathbb{X} -> constant if X in {R,Z,N,Q,C,F,S}
    "emptyset", "varnothing",
}

# Decoration macros that wrap a *core* variable: \hat{x}, \bar{n}, \tilde{G}, ...
DECORATION_MACROS = {
    "hat", "bar", "tilde", "dot", "ddot", "vec", "overline", "underline",
    "widehat", "widetilde", "boldsymbol", "mathbf", "mathcal", "mathfrak",
    "mathscr",
}

GREEK_LETTERS = {
    "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta",
    "eta", "theta", "vartheta", "iota", "kappa", "lambda", "mu", "nu",
    "xi", "pi", "rho", "sigma", "varsigma", "tau", "upsilon", "phi",
    "varphi", "chi", "psi", "omega",
    "Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi", "Sigma", "Upsilon",
    "Phi", "Psi", "Omega",
}

# --------------------------------------------------------------------------
# 2. Tokenizer
# --------------------------------------------------------------------------

TOKEN_RE = re.compile(r"""
    (?P<macro>\\[a-zA-Z]+)          # \command
  | (?P<lbrace>\{)
  | (?P<rbrace>\})
  | (?P<sub>_)
  | (?P<sup>\^)
  | (?P<num>\d+(\.\d+)?)
  | (?P<letter>[a-zA-Z])
  | (?P<other>\S)
""", re.VERBOSE)


class Atom:
    __slots__ = ("kind", "name", "raw")

    def __init__(self, kind, name, raw):
        self.kind = kind      # OPERATOR | FUNCTION | CONSTANT | VARIABLE | UNKNOWN
        self.name = name      # normalized display name, e.g. "x_i", "alpha", "hat{G}"
        self.raw = raw        # original substring

    def __repr__(self):
        return f"{self.kind}:{self.name}"


def tokenize(expr):
    """Yield raw regex match tokens for a math-mode string."""
    return list(TOKEN_RE.finditer(expr))


def classify(expr):
    """
    Walk the token stream and produce a list of Atom objects.
    This is a shallow, greedy parser: good enough for sanity-checking,
    not a full LaTeX grammar. Nesting depth for sub/superscripts is
    handled but arbitrary macro expansion is not.
    """
    tokens = tokenize(expr)
    atoms = []
    i = 0
    n = len(tokens)

    def read_group(i):
        """If tokens[i] is '{', consume the balanced group and return
        (inner_string, next_index). Otherwise treat tokens[i] as a
        single-token group."""
        if tokens[i].group("lbrace"):
            depth = 1
            j = i + 1
            start = tokens[j].start()
            while j < n and depth > 0:
                if tokens[j].group("lbrace"):
                    depth += 1
                elif tokens[j].group("rbrace"):
                    depth -= 1
                j += 1
            end = tokens[j - 1].start()
            return expr[start:end], j
        else:
            return tokens[i].group(0), i + 1

    while i < n:
        tok = tokens[i]

        if tok.group("macro"):
            name = tok.group("macro")[1:]  # strip backslash

            if name in KNOWN_OPERATORS:
                atoms.append(Atom("OPERATOR", name, tok.group(0)))
                i += 1
                continue

            if name in KNOWN_FUNCTIONS:
                atoms.append(Atom("FUNCTION", name, tok.group(0)))
                i += 1
                continue

            if name == "mathbb":
                inner, i = read_group(i + 1)
                if inner.strip() in {"R", "Z", "N", "Q", "C", "F", "S"}:
                    atoms.append(Atom("CONSTANT", f"mathbb{{{inner.strip()}}}", tok.group(0)))
                else:
                    atoms.append(Atom("VARIABLE", f"mathbb{{{inner.strip()}}}", tok.group(0)))
                continue

            if name in KNOWN_CONSTANTS:
                atoms.append(Atom("CONSTANT", name, tok.group(0)))
                i += 1
                continue

            if name in GREEK_LETTERS:
                base = name
                i += 1
                base, i = _absorb_subscript(base, tokens, i, n, expr, read_group)
                atoms.append(Atom("VARIABLE", base, tok.group(0)))
                continue

            if name in DECORATION_MACROS:
                inner, j = read_group(i + 1)
                core = f"{name}{{{inner}}}"
                i = j
                core, i = _absorb_subscript(core, tokens, i, n, expr, read_group)
                atoms.append(Atom("VARIABLE", core, tok.group(0)))
                continue

            # Unrecognized macro - flag it
            atoms.append(Atom("UNKNOWN", name, tok.group(0)))
            i += 1
            continue

        if tok.group("letter"):
            base = tok.group(0)
            i += 1
            base, i = _absorb_subscript(base, tokens, i, n, expr, read_group)
            atoms.append(Atom("VARIABLE", base, tok.group(0)))
            continue

        # numbers, braces (stray), sub/sup without preceding var, other
        # punctuation: not variables, skip silently.
        i += 1

    return atoms


def _absorb_subscript(base, tokens, i, n, expr, read_group):
    """Given we just consumed a core symbol, greedily absorb a following
    _{...} / _x and ^{...} / ^x so `x_i`, `G_i^{(n)}` become one atom."""
    changed = True
    while changed and i < n:
        changed = False
        if i < n and tokens[i].group("sub"):
            inner, j = read_group(i + 1)
            base = f"{base}_{{{inner}}}"
            i = j
            changed = True
        if i < n and tokens[i].group("sup"):
            inner, j = read_group(i + 1)
            base = f"{base}^{{{inner}}}"
            i = j
            changed = True
    return base, i


# --------------------------------------------------------------------------
# 3. Extracting math spans from surrounding prose
# --------------------------------------------------------------------------

MATH_SPAN_RE = re.compile(
    r"(?<!\\)\$\$(.+?)(?<!\\)\$\$"       # $$ ... $$
    r"|(?<!\\)\$(.+?)(?<!\\)\$"          # $ ... $
    r"|\\\((.+?)\\\)"                    # \( ... \)
    r"|\\\[(.+?)\\\]"                    # \[ ... \]
    r"|<math>(.+?)</math>",              # MediaWiki <math> tags
    re.DOTALL,
)


def extract_math_spans(text):
    spans = []
    for m in MATH_SPAN_RE.finditer(text):
        content = next(g for g in m.groups() if g is not None)
        spans.append((m.start(), content))
    return spans


# --------------------------------------------------------------------------
# 4. Registry diffing (new vs. previously-declared variables)
# --------------------------------------------------------------------------

def load_registry(path):
    p = Path(path)
    if p.exists():
        return set(json.loads(p.read_text()))
    return set()


def save_registry(path, names):
    Path(path).write_text(json.dumps(sorted(names), indent=2))


# --------------------------------------------------------------------------
# 5. CLI
# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="Markdown/wiki/tex file to scan")
    ap.add_argument("--registry", default=None, help="Path to JSON registry of known variables")
    ap.add_argument("--update-registry", action="store_true", help="Add all found variables into the registry")
    ap.add_argument("--show-unknown", action="store_true", help="List UNKNOWN (unrecognized) macros too")
    args = ap.parse_args()

    text = Path(args.file).read_text()
    spans = extract_math_spans(text)

    known = load_registry(args.registry) if args.registry else set()
    all_vars = set()
    all_unknown = set()
    new_vars = set()

    for pos, content in spans:
        line = text.count("\n", 0, pos) + 1
        for atom in classify(content):
            if atom.kind == "VARIABLE":
                all_vars.add(atom.name)
                if atom.name not in known:
                    new_vars.add(atom.name)
                    print(f"line {line}: NEW variable  '{atom.name}'   (in: {content.strip()[:60]})")
            elif atom.kind == "UNKNOWN" and args.show_unknown:
                all_unknown.add(atom.name)
                print(f"line {line}: UNKNOWN macro '\\{atom.name}' (in: {content.strip()[:60]})")

    print(f"\n--- summary ---")
    print(f"math spans scanned: {len(spans)}")
    print(f"distinct variables found: {len(all_vars)}")
    print(f"new (not in registry): {len(new_vars)}")
    if args.show_unknown:
        print(f"unrecognized macros: {len(all_unknown)}  {sorted(all_unknown)}")

    if args.registry and args.update_registry:
        save_registry(args.registry, known | all_vars)
        print(f"registry updated: {args.registry}")


if __name__ == "__main__":
    main()
