#!/usr/bin/env python3
"""Deterministic standalone CNF producer for the order-18 m=7 family H.

The two cases are the location of the second high vertex r in the low root's
partition: ``A`` means r in N+(v), and ``B`` means r in N++(v).
The emitted formula exactly encodes the displayed mixed-witness constraints:
exact graph semantics, the order-18 seven-hole degree census, global SNC
badness, the two selected tight deletion-robustness systems, and a proved
within-block status symmetry break.  A family-H candidate maps to a satisfying
assignment, so a checked UNSAT certificate eliminates this family.  The formula
deliberately omits arc-minimality, unrelated deletion-witness selectors, and
strong connectivity: omitting candidate hypotheses is a sound relaxation for
that forward implication.

By default the DIMACS is comment-free.  ``--map-output`` emits the deterministic
one-based variable map as ``number<TAB>name`` records.  ``--map-comments`` also
puts the same map in DIMACS comments; this intentionally changes the file hash.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Sequence

N = 18
V = 0
Q = 1
A = tuple(range(1, 9))
B = tuple(range(9, 16))
C = (16, 17)


class FormulaError(RuntimeError):
    """Raised when deterministic formula construction or writing fails."""


class CNF:
    def __init__(self) -> None:
        self.names: dict[str, int] = {}
        self.clauses: list[tuple[int, ...]] = []
        self.tags: list[str] = []

    def var(self, name: str) -> int:
        if not name or any(ch.isspace() for ch in name):
            raise FormulaError(f"invalid variable name {name!r}")
        old = self.names.get(name)
        if old is not None:
            return old
        number = len(self.names) + 1
        self.names[name] = number
        return number

    def add(self, *literals: int, tag: str) -> None:
        if not tag:
            raise FormulaError("every clause requires a nonempty audit tag")
        clause = tuple(literals)
        if any(type(lit) is not int or lit == 0 for lit in clause):
            raise FormulaError(f"invalid literal in clause {clause!r}")
        if any(abs(lit) > len(self.names) for lit in clause):
            raise FormulaError(f"unallocated variable in clause {clause!r}")
        self.clauses.append(clause)
        self.tags.append(tag)


def equiv_and(cnf: CNF, output: int, left: int, right: int, *, tag: str) -> None:
    cnf.add(-output, left, tag=tag)
    cnf.add(-output, right, tag=tag)
    cnf.add(output, -left, -right, tag=tag)


def threshold(cnf: CNF, inputs: Sequence[int], tag_name: str, *, clause_tag: str) -> list[int]:
    """Return exact unary outputs: output[t-1] iff at least t inputs are true."""
    if not inputs:
        raise FormulaError("threshold requires at least one input")
    if len(set(inputs)) != len(inputs) or any(x <= 0 or x > len(cnf.names) for x in inputs):
        raise FormulaError("threshold inputs must be distinct allocated positive variables")
    previous: list[int] = []
    for index, input_var in enumerate(inputs, 1):
        current: list[int] = []
        for target in range(1, index + 1):
            output = cnf.var(f"cnt_{tag_name}_{index}_{target}")
            current.append(output)
            old_same = previous[target - 1] if target <= len(previous) else None
            old_lower: int | bool = previous[target - 2] if target >= 2 else True
            # output <-> old_same OR (input_var AND old_lower), with constants simplified.
            if old_same is not None:
                cnf.add(-old_same, output, tag=clause_tag)
            if old_lower is True:
                cnf.add(-input_var, output, tag=clause_tag)
            else:
                cnf.add(-input_var, -old_lower, output, tag=clause_tag)
            if old_same is None:
                if old_lower is True:
                    cnf.add(-output, input_var, tag=clause_tag)
                else:
                    cnf.add(-output, input_var, tag=clause_tag)
                    cnf.add(-output, old_lower, tag=clause_tag)
            elif old_lower is True:
                cnf.add(-output, old_same, input_var, tag=clause_tag)
            else:
                cnf.add(-output, old_same, input_var, tag=clause_tag)
                cnf.add(-output, old_same, old_lower, tag=clause_tag)
        previous = current
    return previous


def force_exact(cnf: CNF, inputs: Sequence[int], value: int, tag_name: str, *, clause_tag: str) -> list[int]:
    if type(value) is not int or not 0 <= value <= len(inputs):
        raise FormulaError(f"invalid exact cardinality {value} for width {len(inputs)}")
    outputs = threshold(cnf, inputs, tag_name, clause_tag=clause_tag)
    if value:
        cnf.add(outputs[value - 1], tag=clause_tag)
    if value < len(inputs):
        cnf.add(-outputs[value], tag=clause_tag)
    return outputs


def case_data(case: str) -> tuple[int, tuple[int, ...], tuple[int, ...]]:
    if case == "A":
        return 2, tuple(range(3, 9)), tuple(range(9, 16))
    if case == "B":
        return 9, tuple(range(2, 9)), tuple(range(10, 16))
    raise FormulaError(f"case must be A or B, got {case!r}")


def build_formula(case: str, *, badness_vertices: Sequence[int] | None = None) -> CNF:
    """Build one deterministic forward-sound family-H formula.

    ``badness_vertices=None`` is the production formula and imposes global
    badness.  A specified subset exists only for documented clause-necessity
    scouts; q's selected-witness tightness remains exact independently.
    """
    r_vertex, group_one, group_two = case_data(case)
    high_vertices = {Q, r_vertex}
    if badness_vertices is None:
        badness = set(range(N))
    else:
        badness = set(badness_vertices)
        if any(type(vertex) is not int or not 0 <= vertex < N for vertex in badness):
            raise FormulaError(f"badness vertex outside 0..{N - 1}: {badness_vertices!r}")
    cnf = CNF()
    arc = [[cnf.var(f"a_{i}_{j}") for j in range(N)] for i in range(N)]
    second = [[cnf.var(f"q_{i}_{j}") for j in range(N)] for i in range(N)]
    path: dict[tuple[int, int, int], int] = {}

    for i in range(N):
        cnf.add(-arc[i][i], tag="oriented")
        cnf.add(-second[i][i], tag="distance_two")
    for i in range(N):
        for j in range(i + 1, N):
            cnf.add(-arc[i][j], -arc[j][i], tag="oriented")

    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            paths: list[int] = []
            for middle in range(N):
                if middle in (i, j):
                    continue
                variable = cnf.var(f"p_{i}_{middle}_{j}")
                path[i, middle, j] = variable
                paths.append(variable)
                equiv_and(cnf, variable, arc[i][middle], arc[middle][j], tag="distance_two")
            reach = cnf.var(f"r_{i}_{j}")
            for variable in paths:
                cnf.add(-variable, reach, tag="distance_two")
            cnf.add(-reach, *paths, tag="distance_two")
            cnf.add(-second[i][j], reach, tag="distance_two")
            cnf.add(-second[i][j], -arc[i][j], tag="distance_two")
            cnf.add(second[i][j], -reach, arc[i][j], tag="distance_two")

    for i in range(N):
        out_vars = [arc[i][j] for j in range(N) if j != i]
        degree = 9 if i in high_vertices else 8
        force_exact(cnf, out_vars, degree, f"d1_{i}", clause_tag="degree")
        second_vars = [second[i][j] for j in range(N) if j != i]
        second_counts = threshold(cnf, second_vars, f"d2_{i}", clause_tag="distance_two_count")
        # q is the selected tight witness for deleting r: d++(q)=8.  Its
        # upper bound is kept in this group, rather than borrowed from global
        # badness, so badness-deletion scouts do not weaken witness tightness.
        if i == Q:
            cnf.add(second_counts[7], tag="mixed_tightness")
            cnf.add(-second_counts[8], tag="mixed_tightness")
        elif i in badness:
            # Strict badness: high rows have d++ <= 8, low rows d++ <= 7.
            cnf.add(-second_counts[degree - 1], tag=f"global_badness:{i}")

    hole_vars: list[int] = []
    for i in range(N):
        for j in range(i + 1, N):
            hole = cnf.var(f"h_{i}_{j}")
            hole_vars.append(hole)
            cnf.add(-hole, -arc[i][j], tag="hole_semantics")
            cnf.add(-hole, -arc[j][i], tag="hole_semantics")
            cnf.add(hole, arc[i][j], arc[j][i], tag="hole_semantics")
    force_exact(cnf, hole_vars, 7, "holes", clause_tag="seven_holes")

    a_set = set(A)
    b_set = set(B)
    for j in range(N):
        cnf.add(arc[V][j] if j in a_set else -arc[V][j], tag="low_root_first")
        cnf.add(second[V][j] if j in b_set else -second[V][j], tag="low_root_second")
    for b_vertex in B:
        cnf.add(*(arc[a_vertex][b_vertex] for a_vertex in A), tag="low_root_support")
    for a_vertex in A:
        for c_vertex in C:
            cnf.add(-arc[a_vertex][c_vertex], tag="low_root_no_C")

    cnf.add(arc[Q][r_vertex], tag="mixed_chain")

    # Since q has 9 first and 8 exact-second neighbors, those layers exhaust
    # V\{q}.  The arcs v->q and q in A_v (hence q !-> C_v) force these units.
    for endpoint in (V, *C):
        cnf.add(second[Q][endpoint], tag="high_root_exhaustion")

    # v's exact second endpoints must survive deletion of q.
    for b_vertex in B:
        cnf.add(
            *(arc[a_vertex][b_vertex] for a_vertex in A if a_vertex != Q),
            tag="robust_v_delete_q",
        )

    # Every old exact second endpoint of q must retain a two-walk avoiding r.
    for endpoint in range(N):
        if endpoint in (Q, r_vertex):
            continue
        alternatives = [
            path[Q, middle, endpoint]
            for middle in range(N)
            if middle not in (Q, r_vertex, endpoint)
        ]
        cnf.add(-second[Q][endpoint], *alternatives, tag="robust_q_delete_r")

    # Canonical O<I<H order for q-pair statuses in each uniform block.
    for group in (group_one, group_two, C):
        for left, right in zip(group, group[1:]):
            cnf.add(-arc[Q][right], arc[Q][left], tag="status_symmetry")
            cnf.add(
                -arc[right][Q], arc[Q][left], arc[left][Q],
                tag="status_symmetry",
            )

    if len(cnf.clauses) != len(cnf.tags):
        raise FormulaError("internal tag/clause length mismatch")
    return cnf


def dimacs_bytes(cnf: CNF, *, map_comments: bool = False) -> bytes:
    chunks: list[str] = []
    if map_comments:
        chunks.extend(f"c var {number} {name}\n" for name, number in cnf.names.items())
    chunks.append(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
    chunks.extend(" ".join(map(str, clause)) + " 0\n" for clause in cnf.clauses)
    return "".join(chunks).encode("ascii")


def map_bytes(cnf: CNF) -> bytes:
    return "".join(f"{number}\t{name}\n" for name, number in cnf.names.items()).encode("ascii")


def write_new(path: Path, payload: bytes) -> None:
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as error:
        raise FormulaError(f"refusing to overwrite existing path: {path}") from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=("A", "B"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--map-output", type=Path)
    parser.add_argument("--map-comments", action="store_true")
    args = parser.parse_args()
    if args.map_output is not None and args.map_output == args.output:
        parser.error("--map-output must differ from --output")
    try:
        formula = build_formula(args.case)
        payload = dimacs_bytes(formula, map_comments=args.map_comments)
        write_new(args.output, payload)
        if args.map_output is not None:
            write_new(args.map_output, map_bytes(formula))
    except (FormulaError, OSError) as error:
        parser.exit(2, f"ERROR: {error}\n")
    print(
        f"PASS case={args.case} vars={len(formula.names)} clauses={len(formula.clauses)} "
        f"bytes={len(payload)} sha256={hashlib.sha256(payload).hexdigest()}"
    )
    if args.map_output is not None:
        mapping = map_bytes(formula)
        print(
            f"PASS map_bytes={len(mapping)} "
            f"map_sha256={hashlib.sha256(mapping).hexdigest()}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
