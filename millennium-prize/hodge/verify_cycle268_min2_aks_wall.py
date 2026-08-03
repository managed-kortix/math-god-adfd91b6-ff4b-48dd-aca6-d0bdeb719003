#!/usr/bin/env python3
"""Verify every exact assertion available before the H268 transfer wall."""

from fractions import Fraction as F
from itertools import combinations
from math import comb


Q = (F(1), F(1), F(3))


def unit(i, j):
    return [[F((r, s) == (i, j)) for s in range(3)] for r in range(3)]


def rho(norm, b):
    return [[b[j][i] / Q[i] - norm * b[i][j] for j in range(3)]
            for i in range(3)]


def flatten(matrix):
    return [matrix[i][j] for i in range(3) for j in range(3)]


def rank(rows):
    matrix = [row[:] for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next((r for r in range(pivot_row, len(matrix))
                      if matrix[r][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row != pivot_row and matrix[row][column]:
                scale = matrix[row][column]
                matrix[row] = [left - scale * right for left, right in
                               zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
    return pivot_row


def wedge(left, right):
    if set(left) & set(right):
        return None
    inversions = sum(i > j for i in left for j in right)
    return (-1 if inversions % 2 else 1), tuple(sorted(left + right))


def wedge_map_rank(q, right_degree):
    source = list(combinations(range(1, 7), right_degree))
    target = list(combinations(range(1, 7), len(q) + right_degree))
    rows = {monomial: row for row, monomial in enumerate(target)}
    matrix = [[F(0) for _ in source] for _ in target]
    for column, monomial in enumerate(source):
        value = wedge(q, monomial)
        if value is not None:
            coefficient, product = value
            matrix[rows[product]][column] = F(coefficient)
    return rank(matrix)


def main():
    dimensions = [comb(6, degree) for degree in range(7)]
    assert dimensions == [1, 6, 15, 20, 15, 6, 1]
    assert [(degree, degree - 1, dimensions[degree])
            for degree in range(1, 7)] == [
        (1, 0, 6), (2, 1, 15), (3, 2, 20),
        (4, 3, 15), (5, 4, 6), (6, 5, 1),
    ]

    tangent_basis = [unit(i, j) for i in range(3) for j in range(3)]
    ranks = []
    for k in range(7):
        rows = [flatten(rho(F(5 ** k), b)) for b in tangent_basis]
        ranks.append(rank(rows))
    assert ranks == [6, 9, 9, 9, 9, 9, 9]

    # Under the explicitly non-geometric strict-formality prefilter, a reverse
    # degree-one block has exterior degree 2-e.
    reverse_degrees = {degree: 2 - degree for degree in range(1, 7)}
    assert reverse_degrees == {1: 1, 2: 0, 3: -1, 4: -2, 5: -3, 6: -4}
    assert wedge_map_rank((1,), 1) == 5
    assert wedge_map_rank((1, 2), 0) == 1

    mandatory_q = (1, 2)
    assert len(mandatory_q) == 2
    assert wedge(mandatory_q, ()) == (1, mandatory_q)

    print("Cycle 268 H268-MIN2-AKS exact input audit verified")
    print(f"self-arrow dimensions e=1..6: {dimensions[1:]}")
    print(f"vertex rho ranks k=0..6: {ranks}")
    print("mandatory q=a1a2 included; actual transfer matrices are absent")
    print("terminal output: MIN2-AKS-WALL")


if __name__ == "__main__":
    main()
