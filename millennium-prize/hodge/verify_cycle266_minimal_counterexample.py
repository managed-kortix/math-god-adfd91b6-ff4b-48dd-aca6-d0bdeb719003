#!/usr/bin/env python3
"""Verify the minimal two-cell counterexample to universal H264 survival."""

from collections import defaultdict
from fractions import Fraction
from itertools import combinations


CELLS = (("A", 0), ("B", 1))
ALPHA = (1, 2)
CROSS_DIMENSION = 8


def subsets():
    return [item for size in range(7) for item in combinations(range(1, 7), size)]


def product(left, right):
    if set(left) & set(right):
        return None
    inversions = sum(i > j for i in left for j in right)
    return (-1 if inversions % 2 else 1), tuple(sorted(left + right))


def compose(left, right):
    if right[1] != left[0]:
        return None
    value = product(left[2], right[2])
    if value is None:
        return None
    coefficient, monomial = value
    return coefficient, (right[0], left[1], monomial)


def differential(element, q):
    answer = defaultdict(Fraction)
    for coefficient, term in ((1, compose(q, element)),
                              (-((-1) ** element[3]), compose(element, q))):
        if term is not None:
            term_coefficient, target = term
            answer[target] += coefficient * term_coefficient
    return {target: coefficient for target, coefficient in answer.items() if coefficient}


def matrix_rank(matrix):
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivot_row, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row != pivot_row and matrix[row][column]:
                scale = matrix[row][column]
                matrix[row] = [a - scale * b for a, b in zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
    return pivot_row


def main():
    census = [
        {"kind": "self", "ext_degree": degree, "target_shift": degree - 1,
         "dimension": len(tuple(combinations(range(1, 7), degree)))}
        for degree in range(1, 7)
    ]
    census.append({"kind": "cross", "ext_degree": 3, "target_shift": 2,
                   "dimension": CROSS_DIMENSION})
    assert [(row["ext_degree"], row["target_shift"], row["dimension"])
            for row in census if row["kind"] == "self"] == [
        (1, 0, 6), (2, 1, 15), (3, 2, 20),
        (4, 3, 15), (5, 4, 6), (6, 5, 1),
    ]
    assert census[-1] == {
        "kind": "cross", "ext_degree": 3, "target_shift": 2, "dimension": 8
    }

    basis = []
    for source, source_shift in CELLS:
        for target, target_shift in CELLS:
            for monomial in subsets():
                degree = len(monomial) + source_shift - target_shift
                basis.append((source, target, monomial, degree))
    by_key = {element[:3]: element for element in basis}
    by_degree = defaultdict(list)
    for element in basis:
        by_degree[element[3]].append(element)

    q = by_key[("A", "B", ALPHA)]
    g = by_key[("B", "A", ())]
    assert q[3] == 1 and g[3] == 1
    assert q[2] and compose(q, q) is None
    assert differential(g, q) == {
        ("A", "A", ALPHA): Fraction(1),
        ("B", "B", ALPHA): Fraction(1),
    }

    minimum = min(by_degree)
    maximum = max(by_degree)
    dimensions = {degree: len(by_degree[degree]) for degree in range(minimum, maximum + 1)}
    ranks = {}
    for degree in range(minimum, maximum + 1):
        source = by_degree[degree]
        target = by_degree.get(degree + 1, [])
        rows = {element[:3]: row for row, element in enumerate(target)}
        matrix = [[Fraction(0) for _ in source] for _ in target]
        for column, element in enumerate(source):
            for target_key, coefficient in differential(element, q).items():
                matrix[rows[target_key]][column] = coefficient
        ranks[degree] = matrix_rank([row[:] for row in matrix])

    cohomology = {
        degree: dimensions[degree] - ranks[degree] - ranks.get(degree - 1, 0)
        for degree in range(minimum, maximum + 1)
    }
    assert len(basis) == 256
    assert cohomology[0] == 7
    assert cohomology[2] == 41
    assert any(cohomology.values())

    for element in basis:
        first = differential(element, q)
        second = defaultdict(Fraction)
        for target_key, coefficient in first.items():
            for final_key, final_coefficient in differential(by_key[target_key], q).items():
                second[final_key] += coefficient * final_coefficient
        assert not any(second.values())

    print("Cycle 266 verified: minimal noncontractible packet kills the H264 diagonal class")
    print("two-cell minimal strata: self Ext dimensions 6,15,20,15,6,1; shifted cross Ext3 dimension 8")
    print(f"End(T): dimension={len(basis)}, H^0={cohomology[0]}, H^2={cohomology[2]}")


if __name__ == "__main__":
    main()
