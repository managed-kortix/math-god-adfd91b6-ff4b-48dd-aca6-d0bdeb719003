#!/usr/bin/env python3
"""Exact local tests for :mod:`m7_family_h_cnf`.

This test has no SAT-solver dependency.  It independently evaluates one fixed
family-H local graph, checks its exact neighborhoods and deletion robustness,
and then checks the generator's graph-semantic variables/clauses.  The graph is
a negative control: it satisfies the census and both selected robust-witness
systems but is not globally bad, so it must satisfy the formula only after the
global-badness clauses are omitted.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any

HERE = Path(__file__).resolve().parent
GENERATOR = HERE / "m7_family_h_cnf.py"
SPEC = importlib.util.spec_from_file_location("m7_family_h_cnf", GENERATOR)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {GENERATOR}")
h = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(h)

# Case A: v=0, q=1, r=2.  Each tuple is the exact out-neighborhood.
ROWS = (
    (1, 2, 3, 4, 5, 6, 7, 8),
    (2, 3, 9, 10, 11, 12, 13, 14, 15),
    (3, 4, 5, 6, 7, 8, 9, 10, 11),
    (4, 5, 6, 7, 8, 9, 10, 11),
    (1, 5, 6, 7, 8, 9, 10, 11),
    (1, 6, 7, 8, 9, 10, 11, 12),
    (1, 7, 8, 9, 10, 11, 12, 13),
    (1, 8, 9, 10, 11, 12, 13, 14),
    (1, 9, 10, 11, 12, 13, 14, 15),
    (0, 10, 12, 13, 14, 15, 16, 17),
    (0, 11, 12, 13, 14, 15, 16, 17),
    (0, 9, 12, 13, 14, 15, 16, 17),
    (0, 2, 3, 4, 13, 14, 15, 16),
    (0, 2, 3, 4, 5, 14, 15, 16),
    (0, 2, 3, 4, 5, 6, 15, 16),
    (0, 2, 3, 4, 5, 6, 7, 16),
    (0, 2, 3, 4, 5, 6, 7, 8),
    (0, 2, 3, 4, 5, 6, 7, 8),
)
EXPECTED_HASHES = {
    "A": (
        1_572_702,
        "22f8107f8dc0d3fd9ce03ea4e7b2995a8b749457d721dc0ee16e40ac10e8e012",
    ),
    "B": (
        1_572_685,
        "4686ccca33f81749c8b88cccfd06a566323ee7a0e8bd83726778a76a8eb35b60",
    ),
}
MAP_SIZE = 456_630
MAP_HASH = "01643ce36c1daaa7eb3e28c7ac9a87303e58e279e15b39efa2d8d9e79025e7c2"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def first(vertex: int, rows: tuple[tuple[int, ...], ...] = ROWS) -> set[int]:
    return set(rows[vertex])


def second(vertex: int, rows: tuple[tuple[int, ...], ...] = ROWS) -> set[int]:
    first_layer = first(vertex, rows)
    reached = {endpoint for middle in first_layer for endpoint in rows[middle]}
    return reached - first_layer - {vertex}


def delete_vertex(deleted: int) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(x for x in row if x != deleted) if i != deleted else () for i, row in enumerate(ROWS))


def graph_checks() -> None:
    require(len(ROWS) == h.N, "wrong row count")
    for i, row in enumerate(ROWS):
        require(len(row) == len(set(row)), f"duplicate endpoint in row {i}")
        require(i not in row, f"loop in row {i}")
        require(all(0 <= j < h.N for j in row), f"endpoint outside graph in row {i}")
    for i in range(h.N):
        for j in range(i + 1, h.N):
            require(not (j in ROWS[i] and i in ROWS[j]), f"digon on {i},{j}")

    holes = {(i, j) for i in range(h.N) for j in range(i + 1, h.N)
             if j not in ROWS[i] and i not in ROWS[j]}
    require(holes == {(1, 16), (1, 17), (12, 17), (13, 17),
                      (14, 17), (15, 17), (16, 17)}, f"wrong holes: {sorted(holes)}")
    require(tuple(map(len, ROWS)) == (8, 9, 9) + (8,) * 15, "wrong outdegree census")
    require(first(h.V) == set(h.A), "wrong low-root first layer")
    require(second(h.V) == set(h.B), "wrong low-root exact-second layer")
    require(2 in first(h.Q), "missing q->r")
    require(first(h.Q) == {2, 3, 9, 10, 11, 12, 13, 14, 15}, "wrong q first layer")
    require(second(h.Q) == {0, 4, 5, 6, 7, 8, 16, 17}, "wrong q second layer")
    require(second(h.V, delete_vertex(h.Q)) == second(h.V), "v is not robust after deleting q")
    require(second(h.Q, delete_vertex(2)) == second(h.Q), "q is not robust after deleting r")

    pairs = tuple((len(first(i)), len(second(i))) for i in range(h.N))
    require(pairs == ((8, 7), (9, 8), (9, 8), (8, 8)) + ((8, 9),) * 8 + ((8, 8),) * 6,
            f"unexpected degree pairs: {pairs}")
    seymour = {i for i in range(h.N) if len(second(i)) >= len(first(i))}
    require(seymour == set(range(3, 18)), f"negative control unexpectedly globally bad: {seymour}")


def graph_assignment(formula: Any) -> dict[int, bool]:
    arc = {(i, j): j in ROWS[i] for i in range(h.N) for j in range(h.N)}
    sec = {(i, j): j in second(i) for i in range(h.N) for j in range(h.N)}
    values: dict[int, bool] = {}
    for name, number in formula.names.items():
        fields = name.split("_")
        if fields[0] == "a":
            values[number] = arc[int(fields[1]), int(fields[2])]
        elif fields[0] == "q":
            values[number] = sec[int(fields[1]), int(fields[2])]
        elif fields[0] == "p":
            i, middle, j = map(int, fields[1:])
            values[number] = arc[i, middle] and arc[middle, j]
        elif fields[0] == "r":
            i, j = map(int, fields[1:])
            values[number] = any(arc[i, middle] and arc[middle, j]
                                 for middle in range(h.N) if middle not in (i, j))
        elif fields[0] == "h":
            i, j = map(int, fields[1:])
            values[number] = not arc[i, j] and not arc[j, i]
        elif fields[0] == "cnt":
            # cnt_TAG_index_target.  Recover the target and evaluate each exact
            # sequential-counter family from its already semantic input list.
            target = int(fields[-1])
            index = int(fields[-2])
            tag = "_".join(fields[1:-2])
            if tag.startswith("d1_"):
                vertex = int(tag.split("_")[1])
                inputs = [arc[vertex, j] for j in range(h.N) if j != vertex]
            elif tag.startswith("d2_"):
                vertex = int(tag.split("_")[1])
                inputs = [sec[vertex, j] for j in range(h.N) if j != vertex]
            elif tag == "holes":
                inputs = [not arc[i, j] and not arc[j, i]
                          for i in range(h.N) for j in range(i + 1, h.N)]
            else:
                raise RuntimeError(f"unknown counter family {tag!r}")
            values[number] = sum(inputs[:index]) >= target
        else:
            raise RuntimeError(f"unknown variable kind {name!r}")
    return values


def clause_true(clause: tuple[int, ...], values: dict[int, bool]) -> bool:
    return any(values[abs(literal)] == (literal > 0) for literal in clause)


def formula_checks() -> None:
    relaxed = h.build_formula("A", badness_vertices=())
    values = graph_assignment(relaxed)
    failures = [(index + 1, tag) for index, (clause, tag) in enumerate(zip(relaxed.clauses, relaxed.tags))
                if not clause_true(clause, values)]
    require(not failures, f"negative control fails relaxed formula: {failures[:10]}")

    full = h.build_formula("A")
    full_values = graph_assignment(full)
    failures = [(index + 1, tag) for index, (clause, tag) in enumerate(zip(full.clauses, full.tags))
                if not clause_true(clause, full_values)]
    expected_failures = [(25_634 + 1_159 * (vertex - 3), f"global_badness:{vertex}")
                         for vertex in range(3, 18)]
    require(failures == expected_failures,
            f"wrong full-formula negative-control failures: {failures}")

    for case in "AB":
        formula = h.build_formula(case)
        payload = h.dimacs_bytes(formula)
        mapping = h.map_bytes(formula)
        require((len(payload), hashlib.sha256(payload).hexdigest()) == EXPECTED_HASHES[case],
                f"formula hash drift in case {case}")
        require((len(mapping), hashlib.sha256(mapping).hexdigest()) == (MAP_SIZE, MAP_HASH),
                f"map hash drift in case {case}")
        require(len(formula.names) == 23_292 and len(formula.clauses) == 89_249,
                f"dimension drift in case {case}")

    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "new"
        h.write_new(output, b"first")
        require(output.read_bytes() == b"first", "atomic write payload mismatch")
        try:
            h.write_new(output, b"second")
        except h.FormulaError:
            pass
        else:
            raise RuntimeError("write_new overwrote an existing path")
        require(output.read_bytes() == b"first", "failed overwrite changed existing path")



def cli_checks() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for case in "AB":
            output = root / f"{case}.cnf"
            mapping = root / f"{case}.map"
            result = subprocess.run(
                [sys.executable, "-B", str(GENERATOR), "--case", case,
                 "--output", str(output), "--map-output", str(mapping)],
                check=False, capture_output=True, text=True,
            )
            require(result.returncode == 0, f"generator CLI failed: {result.stderr!r}")
            require((output.stat().st_size, hashlib.sha256(output.read_bytes()).hexdigest())
                    == EXPECTED_HASHES[case], f"CLI formula mismatch in case {case}")
            require((mapping.stat().st_size, hashlib.sha256(mapping.read_bytes()).hexdigest())
                    == (MAP_SIZE, MAP_HASH), f"CLI map mismatch in case {case}")
            overwrite = subprocess.run(
                [sys.executable, "-B", str(GENERATOR), "--case", case,
                 "--output", str(output)], check=False, capture_output=True, text=True,
            )
            require(overwrite.returncode == 2 and "refusing to overwrite" in overwrite.stderr,
                    f"CLI did not reject overwrite: {overwrite.returncode}, {overwrite.stderr!r}")


def main() -> int:
    graph_checks()
    formula_checks()
    cli_checks()
    print("PASS exact family-H local semantics and negative control")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
