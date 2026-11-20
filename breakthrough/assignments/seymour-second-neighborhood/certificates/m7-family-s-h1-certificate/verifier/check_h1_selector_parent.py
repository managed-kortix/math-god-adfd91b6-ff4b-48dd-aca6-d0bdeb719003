#!/usr/bin/env python3
"""Independent fail-closed checker/reconstructor for the family-S h=1 V4 selector parent.

Trust boundary: this file imports neither the production type-row generator nor
any production CNF/parent generator.  It independently enumerates the h=1 rows,
quotients by C-swap and the high swap, reconstructs the complete base clauses,
row stabilizers, unique-T-hole orbit normalizers, selector guards, variable
order, clause order, and exact ASCII DIMACS byte stream.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Sequence

N = 18
W = 0
A = tuple(range(1, 9))
B = tuple(range(9, 16))
C = (16, 17)
HIGHS = frozenset((1, 2))
T = tuple(range(16))
A_TYPES = ((0, 0), (0, 1), (1, 0), (1, 1))
STATES = (("M", 0, 0, 1), ("01", 1, 0, 0), ("10", 0, 1, 0))
SWAP_STATE = {"M": "M", "01": "10", "10": "01"}
EXPECTED = {
    "pre": 6186,
    "fix_c": 0,
    "fix_h": 1490,
    "fix_ch": 0,
    "rows": 1919,
    "base_vars": 23292,
    "base_clauses": 89170,
    "common_units": 28,
    "row_residual_units": 38,
    "hole_guarded": 168584,
    "vars": 25211,
    "clauses": 330705,
    "universe_sha256": "d713ca11b98de20010c923bf1cbe756230d2c9728834ffab51fb65c39068131f",
}

Row = tuple[str, tuple[int, int, int], tuple[int, int, int, int], tuple[int, ...], int]


def fail(message: str) -> None:
    raise RuntimeError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strict_json_load(path: Path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r}")
            result[key] = value
        return result
    return json.loads(
        path.read_text(encoding="ascii"),
        object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"nonfinite JSON {value}")),
    )


def hist(word: Sequence[int], width: int) -> tuple[int, ...]:
    counts = [0] * width
    for symbol in word:
        require(type(symbol) is int and 0 <= symbol < width, "histogram symbol outside range")
        counts[symbol] += 1
    return tuple(counts)


def c_swap(row: Row) -> Row:
    state, distinguished, ac, bc, h = row
    sa = (0, 2, 1, 3)
    return (
        SWAP_STATE[state],
        tuple(sa[t] for t in distinguished),
        tuple(ac[sa[t]] for t in range(4)),
        tuple(bc[3 * (t % 3) + (t // 3)] for t in range(9)),
        h,
    )


def high_swap(row: Row) -> Row:
    state, distinguished, ac, bc, h = row
    return state, (distinguished[0], distinguished[2], distinguished[1]), ac, bc, h


def orbit(row: Row) -> frozenset[Row]:
    return frozenset((row, c_swap(row), high_swap(row), c_swap(high_swap(row))))


def independent_pre_rows() -> tuple[Row, ...]:
    """Construct h=1 rows from sorted words, not weak compositions."""
    u_by_margin: dict[tuple[int, int], list[tuple[tuple[int, ...], tuple[int, ...]]]] = defaultdict(list)
    for distinguished in itertools.product(range(4), repeat=3):
        for ordinary in itertools.combinations_with_replacement(range(4), 6):
            ac = hist(ordinary, 4)
            a0 = sum(A_TYPES[t][0] for t in distinguished) + sum(A_TYPES[t][0] for t in ordinary)
            a1 = sum(A_TYPES[t][1] for t in distinguished) + sum(A_TYPES[t][1] for t in ordinary)
            u_by_margin[a0, a1].append((tuple(distinguished), ac))
    b_by_out: dict[tuple[int, int], list[tuple[int, int, tuple[int, ...]]]] = defaultdict(list)
    for word in itertools.combinations_with_replacement(range(9), 7):
        bc = hist(word, 9)
        out0 = sum(t // 3 == 0 for t in word)
        out1 = sum(t % 3 == 0 for t in word)
        hole0 = sum(t // 3 == 2 for t in word)
        hole1 = sum(t % 3 == 2 for t in word)
        b_by_out[out0, out1].append((hole0, hole1, bc))
    output: list[Row] = []
    for state, d0, d1, c_hole in STATES:
        for (a0, a1), urows in u_by_margin.items():
            required = a0 - 1 - d0, a1 - 1 - d1
            for distinguished, ac in urows:
                for b0, b1, bc in b_by_out.get(required, ()):
                    h = 7 - a0 - a1 - c_hole - b0 - b1
                    if h == 1:
                        output.append((state, distinguished, ac, bc, h))
    return tuple(output)


def row_json(row: Row) -> str:
    return json.dumps(row, separators=(",", ":"))


def universe_bytes(rows: Sequence[Row]) -> bytes:
    return ("m7-family-s-h1-v4-universe-v1\n" + "\n".join(row_json(row) for row in rows) + "\n").encode("ascii")


def independent_rows() -> tuple[Row, ...]:
    pre = independent_pre_rows()
    require(len(pre) == EXPECTED["pre"], f"pre-row count changed: {len(pre)}")
    require(len(set(pre)) == len(pre), "duplicate pre-row")
    pre_set = set(pre)
    require(all(orbit(row) <= pre_set for row in pre), "V4 action leaves h=1 row universe")
    got = (
        sum(c_swap(row) == row for row in pre),
        sum(high_swap(row) == row for row in pre),
        sum(c_swap(high_swap(row)) == row for row in pre),
    )
    require(got == (EXPECTED["fix_c"], EXPECTED["fix_h"], EXPECTED["fix_ch"]), f"fixed counts changed: {got}")
    rows = tuple(sorted({min(orbit(row)) for row in pre}))
    require(len(rows) == EXPECTED["rows"], f"V4 row count changed: {len(rows)}")
    require(all(row == min(orbit(row)) for row in rows), "noncanonical V4 row")
    require(digest(universe_bytes(rows)) == EXPECTED["universe_sha256"], "ordered universe digest changed")
    return rows


class Formula:
    def __init__(self):
        self.names: dict[str, int] = {}
        self.clauses: list[tuple[int, ...]] = []

    def var(self, name: str) -> int:
        require(type(name) is str and name and "\n" not in name and "\r" not in name, "invalid variable name")
        if name not in self.names:
            self.names[name] = len(self.names) + 1
        return self.names[name]

    def add(self, *literals: int) -> None:
        require(all(type(lit) is int and lit != 0 for lit in literals), "invalid literal")
        self.clauses.append(tuple(literals))


def and_gate(formula: Formula, y: int, x: int, z: int) -> None:
    formula.add(-y, x)
    formula.add(-y, z)
    formula.add(y, -x, -z)


def count(formula: Formula, inputs: Sequence[int], tag: str) -> list[int]:
    previous: list[int] = []
    for i, x in enumerate(inputs, 1):
        current: list[int] = []
        for threshold in range(1, i + 1):
            y = formula.var(f"cnt_{tag}_{i}_{threshold}")
            current.append(y)
            old_same = previous[threshold - 1] if threshold <= len(previous) else None
            old_lower: int | bool = previous[threshold - 2] if threshold >= 2 else True
            if old_same is not None:
                formula.add(-old_same, y)
            if old_lower is True:
                formula.add(-x, y)
            else:
                formula.add(-x, -old_lower, y)
            if old_same is None:
                if old_lower is True:
                    formula.add(-y, x)
                else:
                    formula.add(-y, x)
                    formula.add(-y, old_lower)
            elif old_lower is True:
                formula.add(-y, old_same, x)
            else:
                formula.add(-y, old_same, x)
                formula.add(-y, old_same, old_lower)
        previous = current
    return previous


def exact(formula: Formula, literals: Sequence[int], cardinality: int, tag: str) -> None:
    require(0 <= cardinality <= len(literals), "cardinality outside range")
    outputs = count(formula, literals, tag)
    if cardinality:
        formula.add(outputs[cardinality - 1])
    if cardinality < len(literals):
        formula.add(-outputs[cardinality])


def reconstruct_base() -> tuple[Formula, list[list[int]]]:
    formula = Formula()
    arc = [[formula.var(f"a_{i}_{j}") for j in range(N)] for i in range(N)]
    second = [[formula.var(f"q_{i}_{j}") for j in range(N)] for i in range(N)]
    for i in range(N):
        formula.add(-arc[i][i])
        formula.add(-second[i][i])
    for i in range(N):
        for j in range(i + 1, N):
            formula.add(-arc[i][j], -arc[j][i])
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            paths: list[int] = []
            for k in range(N):
                if k in (i, j):
                    continue
                p = formula.var(f"p_{i}_{k}_{j}")
                paths.append(p)
                and_gate(formula, p, arc[i][k], arc[k][j])
            reach = formula.var(f"reach_{i}_{j}")
            for p in paths:
                formula.add(-p, reach)
            formula.add(-reach, *paths)
            formula.add(-second[i][j], reach)
            formula.add(-second[i][j], -arc[i][j])
            formula.add(second[i][j], -reach, arc[i][j])
    for i in range(N):
        exact(formula, [arc[i][j] for j in range(N) if j != i], 9 if i in HIGHS else 8, f"d1_{i}")
        outputs = count(formula, [second[i][j] for j in range(N) if j != i], f"d2_{i}")
        formula.add(-outputs[8 if i in HIGHS else 7])
    holes: list[int] = []
    for i in range(N):
        for j in range(i + 1, N):
            h = formula.var(f"h_{i}_{j}")
            holes.append(h)
            formula.add(-h, -arc[i][j])
            formula.add(-h, -arc[j][i])
            formula.add(h, arc[i][j], arc[j][i])
    exact(formula, holes, 7, "holes")
    for j in range(N):
        formula.add(arc[W][j] if j in A else -arc[W][j])
    for b in B:
        formula.add(*[arc[x][b] for x in A if x != 1])
        formula.add(*[arc[x][b] for x in A if x != 2])
    require((len(formula.names), len(formula.clauses)) == (EXPECTED["base_vars"], EXPECTED["base_clauses"]), "base dimensions changed")
    return formula, arc


def row_units(arc: Sequence[Sequence[int]], row: Row) -> tuple[tuple[int, ...], ...]:
    state, distinguished, ac, bc, _ = row
    ordinary = tuple(t for t, number in enumerate(ac) for _ in range(number))
    atypes = distinguished + ordinary
    require(len(atypes) == 9, "A-side expanded row width")
    units: list[tuple[int, ...]] = []
    for u, typ in zip((0, 1, 2, 3, 4, 5, 6, 7, 8), atypes):
        for k, c in enumerate(C):
            if A_TYPES[typ][k]:
                units.extend(((-arc[u][c],), (-arc[c][u],)))
            else:
                units.extend(((arc[c][u],), (-arc[u][c],)))
    btypes = tuple(t for t, number in enumerate(bc) for _ in range(number))
    require(len(btypes) == 7, "B-side expanded row width")
    for b, typ in zip(B, btypes):
        symbols = typ // 3, typ % 3
        for k, c in enumerate(C):
            symbol = symbols[k]
            if symbol == 0:
                units.extend(((arc[c][b],), (-arc[b][c],)))
            elif symbol == 1:
                units.extend(((arc[b][c],), (-arc[c][b],)))
            else:
                units.extend(((-arc[b][c],), (-arc[c][b],)))
    if state == "M":
        units.extend(((-arc[16][17],), (-arc[17][16],)))
    elif state == "01":
        units.extend(((arc[16][17],), (-arc[17][16],)))
    else:
        units.extend(((arc[17][16],), (-arc[16][17],)))
    require(len(units) == 66 and len(set(units)) == 66, "row units are not 66 unique units")
    return tuple(units)


def stabilizer_blocks(row: Row) -> tuple[tuple[int, ...], ...]:
    """Full C-incidence blocks in T; ordering follows canonical row labels."""
    _, distinguished, ac, bc, _ = row
    blocks: list[tuple[int, ...]] = [(0,)]
    if distinguished[1] == distinguished[2]:
        blocks.append((1, 2))
    else:
        blocks.extend(((1,), (2,)))
    cursor = 3
    for number in ac:
        if number:
            blocks.append(tuple(range(cursor, cursor + number)))
        cursor += number
    require(cursor == 9, "ordinary-A block partition width")
    cursor = 9
    for number in bc:
        if number:
            blocks.append(tuple(range(cursor, cursor + number)))
        cursor += number
    require(cursor == 16, "B block partition width")
    flat = tuple(v for block in blocks for v in block)
    require(sorted(flat) == list(T) and len(flat) == len(set(flat)), "stabilizer blocks do not partition T")
    return tuple(blocks)


def canonical_hole_pairs(row: Row) -> frozenset[tuple[int, int]]:
    blocks = stabilizer_blocks(row)
    representatives: set[tuple[int, int]] = set()
    for index, left in enumerate(blocks):
        if len(left) >= 2:
            representatives.add((left[0], left[1]))
        for right in blocks[index + 1:]:
            representatives.add(tuple(sorted((left[0], right[0]))))
    return frozenset(representatives)


def hole_guard_units(formula: Formula, row: Row) -> tuple[tuple[int, ...], ...]:
    allowed = canonical_hole_pairs(row)
    return tuple(
        (-formula.names[f"h_{u}_{v}"],)
        for u in T for v in T if u < v and (u, v) not in allowed
    )


def reconstruct_parent() -> tuple[Formula, tuple[Row, ...], tuple[int, ...]]:
    rows = independent_rows()
    formula, arc = reconstruct_base()
    all_units = [set(row_units(arc, row)) for row in rows]
    common = set.intersection(*all_units)
    require(len(common) == EXPECTED["common_units"], f"common row unit count changed: {len(common)}")
    for clause in sorted(common):
        formula.add(*clause)
    selectors: list[int] = []
    guarded_row = guarded_hole = 0
    for ordinal, (row, units) in enumerate(zip(rows, all_units)):
        # Selector spelling is part of the proposed production byte contract.
        selector = formula.var(f"sel_{ordinal}")
        selectors.append(selector)
        residual = units - common
        require(len(residual) == EXPECTED["row_residual_units"], f"row {ordinal} residual-unit count changed")
        for unit in sorted(residual):
            formula.add(-selector, *unit)
            guarded_row += 1
        hole_units = hole_guard_units(formula, row)
        for unit in sorted(hole_units):
            formula.add(-selector, *unit)
            guarded_hole += 1
    formula.add(*selectors)
    require(guarded_row == EXPECTED["rows"] * EXPECTED["row_residual_units"], "guarded row total changed")
    require(guarded_hole == EXPECTED["hole_guarded"], f"guarded hole total changed: {guarded_hole}")
    require((len(formula.names), len(formula.clauses)) == (EXPECTED["vars"], EXPECTED["clauses"]),
            f"parent dimensions changed: {(len(formula.names), len(formula.clauses))}")
    return formula, rows, tuple(selectors)


def serialize(formula: Formula) -> bytes:
    output = "".join(f"c var {number} {name}\n" for name, number in formula.names.items())
    output += f"p cnf {len(formula.names)} {len(formula.clauses)}\n"
    output += "".join(" ".join(map(str, clause)) + " 0\n" for clause in formula.clauses)
    return output.encode("ascii")


def parse_canonical_dimacs(raw: bytes) -> tuple[list[str], list[tuple[int, ...]], tuple[int, int]]:
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as error:
        raise RuntimeError(f"non-ASCII DIMACS: {error}") from error
    require(raw.endswith(b"\n"), "DIMACS lacks final newline")
    require(b"\r" not in raw, "DIMACS contains carriage return")
    lines = text.splitlines()
    names: list[str] = []
    seen: set[str] = set()
    clauses: list[tuple[int, ...]] = []
    header: tuple[int, int] | None = None
    phase = "map"
    for line_number, line in enumerate(lines, 1):
        require(line and line == line.strip() and "  " not in line and "\t" not in line, f"noncanonical whitespace line {line_number}")
        if line.startswith("c var "):
            require(phase == "map" and header is None, "variable map after header")
            fields = line.split(" ", 3)
            require(len(fields) == 4 and fields[0:2] == ["c", "var"] and fields[3], "malformed variable map")
            try:
                number = int(fields[2])
            except ValueError as error:
                raise RuntimeError("noninteger variable number") from error
            require(number == len(names) + 1 and fields[3] not in seen, "nonsequential or duplicate variable map")
            names.append(fields[3])
            seen.add(fields[3])
        elif line.startswith("p cnf "):
            require(phase == "map" and header is None, "duplicate or misplaced header")
            fields = line.split(" ")
            require(len(fields) == 4 and fields[:2] == ["p", "cnf"], "malformed header")
            try:
                header = int(fields[2]), int(fields[3])
            except ValueError as error:
                raise RuntimeError("noninteger header") from error
            require(header[0] >= 0 and header[1] >= 0, "negative DIMACS dimension")
            phase = "clauses"
        else:
            require(phase == "clauses" and header is not None, f"unexpected line {line_number}")
            try:
                values = tuple(int(field) for field in line.split(" "))
            except ValueError as error:
                raise RuntimeError(f"noninteger clause line {line_number}") from error
            require(values and values[-1] == 0 and 0 not in values[:-1], f"malformed clause line {line_number}")
            clause = values[:-1]
            require(clause, f"empty clause line {line_number}")
            require(all(abs(literal) <= header[0] for literal in clause), f"literal range line {line_number}")
            clauses.append(clause)
    require(header is not None, "missing DIMACS header")
    require(header == (len(names), len(clauses)), f"DIMACS dimension mismatch: header={header} parsed={(len(names),len(clauses))}")
    return names, clauses, header


def parse_row_payload(value) -> Row:
    require(type(value) is list and len(value) == 5, "row shape")
    state, distinguished, ac, bc, h = value
    require(type(state) is str and state in SWAP_STATE, "row state")
    require(type(distinguished) is list and len(distinguished) == 3 and all(type(x) is int and 0 <= x < 4 for x in distinguished), "row distinguished")
    require(type(ac) is list and len(ac) == 4 and all(type(x) is int and x >= 0 for x in ac) and sum(ac) == 6, "row A counts")
    require(type(bc) is list and len(bc) == 9 and all(type(x) is int and x >= 0 for x in bc) and sum(bc) == 7, "row B counts")
    require(type(h) is int and h == 1, "row h")
    return state, tuple(distinguished), tuple(ac), tuple(bc), h


def check_ledger(path: Path, expected: Sequence[Row]) -> None:
    require(path.is_file() and not path.is_symlink(), "ledger is not a regular nonsymlink file")
    raw = path.read_bytes()
    require(raw.endswith(b"\n") and b"\r" not in raw, "ledger has noncanonical line endings")
    payload = strict_json_load(path)
    require(type(payload) is dict, "ledger root must be the typed envelope object")
    require(set(payload) == {"domain", "ordered_universe_sha256", "row_count", "rows", "schema"},
            "ledger envelope keys")
    require(type(payload["schema"]) is str and payload["schema"] == "m7-family-s-h1-v4-ledger-v1", "ledger schema")
    require(type(payload["domain"]) is str and payload["domain"] == "m7-family-s-h1-v4-universe-v1", "ledger domain")
    require(type(payload["row_count"]) is int and payload["row_count"] == EXPECTED["rows"], "ledger row count")
    require(type(payload["ordered_universe_sha256"]) is str and payload["ordered_universe_sha256"] == EXPECTED["universe_sha256"], "ledger universe digest")
    require(type(payload["rows"]) is list, "ledger rows must be a JSON list")
    canonical = (json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")
    require(raw == canonical, "ledger is not exact canonical compact sorted ASCII JSON")
    got = tuple(parse_row_payload(row) for row in payload["rows"])
    require(len(got) == len(set(got)), "ledger duplicate row")
    require(got == tuple(expected), "ledger is not exact ordered independent universe")


def check_cnf(path: Path, ledger: Path | None) -> None:
    require(path.is_file() and not path.is_symlink(), "CNF is not a regular nonsymlink file")
    formula, rows, _ = reconstruct_parent()
    if ledger is not None:
        check_ledger(ledger, rows)
    expected = serialize(formula)
    raw = path.read_bytes()
    names, clauses, header = parse_canonical_dimacs(raw)
    require(names == list(formula.names), "variable map differs from independent reconstruction")
    require(clauses == formula.clauses, "clause stream differs from independent reconstruction")
    require(raw == expected, "DIMACS bytes differ from canonical independent serialization")
    print(f"PASS independent h1 selector-parent rows={len(rows)} vars={header[0]} clauses={header[1]} bytes={len(raw)} sha256={digest(raw)}")
    print(f"PASS independent h1 V4 pre={EXPECTED['pre']} FixC={EXPECTED['fix_c']} FixH={EXPECTED['fix_h']} FixCH={EXPECTED['fix_ch']} universe_sha256={digest(universe_bytes(rows))}")


def write_reconstruction(path: Path, ledger: Path | None) -> None:
    require(not path.is_symlink(), "refusing to write reconstruction through symlink")
    formula, rows, _ = reconstruct_parent()
    if ledger is not None:
        check_ledger(ledger, rows)
    path.write_bytes(serialize(formula))
    print(f"PASS wrote independent reconstruction vars={len(formula.names)} clauses={len(formula.clauses)} bytes={path.stat().st_size} sha256={digest(path.read_bytes())}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", nargs="?", type=Path)
    parser.add_argument("--ordered-ledger", type=Path)
    parser.add_argument("--write-reconstruction", type=Path)
    args = parser.parse_args()
    require((args.cnf is None) != (args.write_reconstruction is None), "choose exactly one CNF to check or --write-reconstruction")
    if args.write_reconstruction is not None:
        write_reconstruction(args.write_reconstruction, args.ordered_ledger)
    else:
        check_cnf(args.cnf, args.ordered_ledger)


if __name__ == "__main__":
    try:
        main()
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL {error}", file=sys.stderr)
        raise SystemExit(1)
