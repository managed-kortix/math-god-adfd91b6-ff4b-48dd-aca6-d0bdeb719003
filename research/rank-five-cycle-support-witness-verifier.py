#!/usr/bin/env python3
"""Exact witnesses for rank-five kernel fixture rows 80 and 118."""

from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research" / "fixtures" / "rank-five-kernels.json"
EXPECTED_SOURCE_SHA256 = "027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def determinant(matrix):
    matrix = [list(row) for row in matrix]
    result = F(1)
    for column in range(len(matrix)):
        pivot = next((row for row in range(column, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            result = -result
        value = matrix[column][column]
        result *= value
        for row in range(column + 1, len(matrix)):
            scale = matrix[row][column] / value
            for entry in range(column + 1, len(matrix)):
                matrix[row][entry] -= scale * matrix[column][entry]
    return result


def require_psd(matrix, label):
    require(all(matrix[i][i] == 1 for i in range(len(matrix))),
            f"{label}: non-unit diagonal")
    require(all(matrix[i][j] == matrix[j][i]
                for i in range(len(matrix)) for j in range(len(matrix))),
            f"{label}: nonsymmetric matrix")
    for size in range(1, len(matrix) + 1):
        for indices in itertools.combinations(range(len(matrix)), size):
            minor = [[matrix[i][j] for j in indices] for i in indices]
            require(determinant(minor) >= 0, f"{label}: negative principal minor")


def signed_pullback(base, assignment):
    return [[F(si * sj) * base[i][j] for j, sj in assignment]
            for i, si in assignment]


def step_cost(correlation):
    require(correlation != -1, "antipodal consecutive path vectors")
    return (1 - correlation) / (1 + correlation)


def source_rows():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256,
            "rank-five source fixture digest changed")
    payload = json.loads(raw.decode("ascii"))
    return payload["kernels"][79], payload["kernels"][117]


def support_edges(record):
    pairs = tuple(itertools.combinations(range(record["n"]), 2))
    return {(u, v): multiplicity for (u, v), multiplicity
            in zip(pairs, record["code"]) if multiplicity}


def audit_witness(record, base, assignment, expected_edges, label):
    require(record["code"] == expected_edges, f"{label}: fixture row changed")
    require_psd(base, f"{label} base")
    gram = signed_pullback(base, assignment)
    require_psd(gram, f"{label} branch")
    edges = support_edges(record)
    require(len(edges) == len(assignment), f"{label}: support is not a cycle")
    excess = F(0)
    for (u, v), multiplicity in edges.items():
        correlation = gram[u][v]
        if multiplicity == 1:
            require(correlation == -1, f"{label}: single edge is not antipodal")
            excess += step_cost(-correlation)
        else:
            require(multiplicity == 2, f"{label}: multiplicity exceeds two")
            require(correlation == F(-1, 2),
                    f"{label}: doubled edge correlation changed")
            odd_cost = step_cost(-correlation)
            # The exact even-path midpoint is u+v. Its norm is one when
            # <u,v>=-1/2, and its correlation with either endpoint is 1/2.
            midpoint_norm = 2 + 2 * correlation
            midpoint_step = 1 + correlation
            require(midpoint_norm == 1 and midpoint_step == F(1, 2),
                    f"{label}: invalid exact even midpoint")
            even_cost = 2 * step_cost(midpoint_step)
            require(odd_cost == F(1, 3) and even_cost == F(2, 3),
                    f"{label}: path costs changed")
            excess += odd_cost + even_cost
    require(excess == 4, f"{label}: exact excess is not four")
    return gram, excess


def audit():
    row80, row118 = source_rows()
    row80_base = (
        (F(1), F(0), F(1, 2), F(-1, 2)),
        (F(0), F(1), F(-1, 2), F(-1, 2)),
        (F(1, 2), F(-1, 2), F(1), F(0)),
        (F(-1, 2), F(-1, 2), F(0), F(1)),
    )
    # Branch order is 0,...,6; base-vector order is A,B,C,D.
    row80_assignment = ((0, 1), (1, 1), (2, 1), (2, -1),
                        (1, -1), (0, -1), (3, 1))
    gram80, excess80 = audit_witness(
        row80, row80_base, row80_assignment,
        [0, 0, 0, 0, 1, 2, 0, 0, 1, 0, 2, 1, 0, 2, 0, 2, 0, 0, 0, 0, 0],
        "row 80")

    row118_base = (
        (F(1), F(1, 2), F(0), F(1, 2)),
        (F(1, 2), F(1), F(1, 2), F(0)),
        (F(0), F(1, 2), F(1), F(1, 2)),
        (F(1, 2), F(0), F(1, 2), F(1)),
    )
    row118_assignment = ((0, 1), (0, -1), (3, -1), (2, -1),
                         (1, -1), (2, 1), (3, 1), (1, 1))
    gram118, excess118 = audit_witness(
        row118, row118_base, row118_assignment,
        [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 1, 2, 0, 2, 0, 1, 0, 0, 0],
        "row 118")
    return gram80, excess80, gram118, excess118


def main():
    gram80, excess80, gram118, excess118 = audit()
    print("rank-five cycle-support witnesses: exact audit passed")
    print(f"row80_rank_bound=4 row80_excess={excess80}")
    print(f"row118_rank_bound=3 row118_excess={excess118}")
    print(f"branch_gram_orders={len(gram80)},{len(gram118)}")


if __name__ == "__main__":
    main()
