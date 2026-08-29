#!/usr/bin/env python3
r"""
tablecheck.py

Verify a table's summary rows against the rows they summarize.

WHY THIS IS A DIFFERENT ERROR CLASS. arith.py checks identities a page
writes out inside a single math span. This checks arithmetic that is spread
ACROSS a table: a Total row that should equal the column sum, a mean row that
should equal the mean of the column above it. Those are the numbers that go
stale when a row is edited and the summary is not - the classic spreadsheet
failure, and invisible to any per-span check because every individual cell
stays well-formed.

The S3 element-structure page is dense with these:

    | 1 + 1 + 1 || 1 || 1 || 3 || 3 || 0
    | 2 + 1     || 3 || 2 || 1 || 2 || 1
    | 3         || 2 || 3 || 0 || 1 || 2
    | Mean over conjugacy classes || 2 || 2 || 4/3 || 2 || 1
    | Mean over elements          || 7/3 || 13/6 || 1 || 11/6 || 7/6

Two different means over the same columns: the unweighted mean over classes,
and the mean over ELEMENTS, which weights each class by its size. Getting the
weighting wrong is an easy and completely silent error.

CONSERVATIVE BY DESIGN. A column is checked only when every data cell in it
is a bare number and the summary cell is too. Anything with prose, a formula,
or a free variable is skipped rather than guessed at - these tables mix
numeric columns with symbolic ones ("generic q") in the same row.
"""

import re
from fractions import Fraction

TABLE_RE = re.compile(r"^\s*\{\|.*?^\s*\|\}", re.MULTILINE | re.DOTALL)

SUM_LABELS = re.compile(r"^\s*!?\s*total\b", re.IGNORECASE)
MEAN_CLASS_LABELS = re.compile(
    r"^\s*!?\s*mean over (conjugacy classes|classes|rows)\b", re.IGNORECASE)
MEAN_ELEM_LABELS = re.compile(
    r"^\s*!?\s*mean over elements\b", re.IGNORECASE)

# Header of the column that weights a "mean over elements".
WEIGHT_HEADER = re.compile(
    r"number of elements|size of (each )?conjugacy class", re.IGNORECASE)


def _strip(cell):
    c = re.sub(r"<[Mm][Aa][Tt][Hh]>(.*?)</[Mm][Aa][Tt][Hh]>", r"\1", cell,
               flags=re.DOTALL)
    c = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", c)
    c = re.sub(r"\[\[([^\]]*)\]\]", r"\1", c)
    c = re.sub(r"<br\s*/?>", " ", c)
    c = c.replace("'''", "").replace("''", "")
    c = re.sub(r"\\!|\\,|\\;", "", c)
    return c.strip()


def cell_number(cell):
    """Fraction if the cell is a bare number, else None.

    A trailing parenthetical gloss is allowed ("6 (equals 3!, the size of
    the symmetric group)") because these tables routinely annotate a total;
    anything else disqualifies the cell.
    """
    c = _strip(cell)
    c = re.sub(r"\s*\(.*\)\s*$", "", c, flags=re.DOTALL).strip()
    if not c:
        return None
    m = re.fullmatch(r"(-?\d+)\s*/\s*(\d+)", c)
    if m:
        return Fraction(int(m.group(1)), int(m.group(2)))
    m = re.fullmatch(r"\\d?frac\s*\{(-?\d+)\}\s*\{(\d+)\}", c)
    if m:
        return Fraction(int(m.group(1)), int(m.group(2)))
    if re.fullmatch(r"-?\d+", c):
        return Fraction(int(c))
    return None


def parse_tables(text):
    """[{headers, rows, line}] for each wikitable."""
    out = []
    for m in TABLE_RE.finditer(text):
        block = m.group(0)
        line = text.count("\n", 0, m.start()) + 1
        headers, rows, cur = [], [], None
        for raw in block.split("\n"):
            s = raw.strip()
            if s.startswith("{|") or s.startswith("|}"):
                continue
            if s.startswith("!") and not headers:
                headers = [h.strip() for h in re.split(r"\s*!!\s*", s.lstrip("!"))]
                continue
            if s.startswith("|-"):
                if cur is not None:
                    rows.append(cur)
                cur = []
                continue
            if cur is None:
                continue
            if s.startswith("|") or s.startswith("!"):
                body = s[1:] if s.startswith("|") else s.lstrip("!")
                cur.extend(re.split(r"\s*(?:\|\||!!)\s*", body))
        if cur:
            rows.append(cur)
        if headers and rows:
            out.append({"headers": headers, "rows": rows, "line": line})
    return out


def _weight_column(headers):
    for i, h in enumerate(headers):
        if WEIGHT_HEADER.search(_strip(h)):
            return i
    return None


def find_table_inconsistencies(text):
    """Return [(severity, line, message)] for summary rows that don't match."""
    issues = []
    for tbl in parse_tables(text):
        headers, rows, line = tbl["headers"], tbl["rows"], tbl["line"]

        data, summaries = [], []
        for r in rows:
            label = _strip(r[0]) if r else ""
            if SUM_LABELS.match(label):
                summaries.append(("total", r))
            elif MEAN_CLASS_LABELS.match(label):
                summaries.append(("mean_class", r))
            elif MEAN_ELEM_LABELS.match(label):
                summaries.append(("mean_elem", r))
            else:
                if not summaries:      # summary rows end the data block
                    data.append(r)
        if not summaries or len(data) < 2:
            continue

        wcol = _weight_column(headers)
        weights = None
        if wcol is not None:
            ws = [cell_number(r[wcol]) if wcol < len(r) else None for r in data]
            if all(w is not None for w in ws):
                weights = ws

        ncols = max(len(r) for r in rows)
        for kind, srow in summaries:
            for c in range(1, ncols):
                claimed = cell_number(srow[c]) if c < len(srow) else None
                if claimed is None:
                    continue
                vals = [cell_number(r[c]) if c < len(r) else None for r in data]
                if any(v is None for v in vals):
                    continue

                if kind == "total":
                    expect = sum(vals, Fraction(0))
                    what = "column total"
                elif kind == "mean_class":
                    expect = sum(vals, Fraction(0)) / len(vals)
                    what = "mean over classes"
                else:
                    if weights is None or c == wcol:
                        continue
                    tw = sum(weights, Fraction(0))
                    if tw == 0:
                        continue
                    expect = sum(v * w for v, w in zip(vals, weights)) / tw
                    what = "mean over elements (weighted by class size)"

                if claimed != expect:
                    hdr = _strip(headers[c])[:44] if c < len(headers) else f"col {c}"
                    issues.append((
                        "TABLE_INCONSISTENCY", line,
                        f"{what} for column {hdr!r} is stated as {claimed} "
                        f"but the rows above give {expect} "
                        f"(values: {[str(v) for v in vals]})"))
    return issues
