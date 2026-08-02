#!/usr/bin/env python3
"""Exact determinant-sector prefilter for the F242 matrix triples."""

import argparse
import itertools
import json
from fractions import Fraction


ZERO = (0, 0)
ONE = (1, 0)
ALPHABET = {"0": ZERO, "1": ONE, "-1": (-1, 0), "i": (0, 1), "-i": (0, -1)}
PERMUTATIONS = tuple(itertools.permutations(range(3)))


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def neg(x):
    return (-x[0], -x[1])


def mul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def conj(x):
    return (x[0], -x[1])


def sign(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(3)
        for j in range(i + 1, 3)
    )
    return -1 if inversions % 2 else 1


def determinant3(matrix):
    answer = ZERO
    for permutation in PERMUTATIONS:
        term = ONE
        for row in range(3):
            term = mul(term, matrix[row][permutation[row]])
        answer = add(answer, term if sign(permutation) == 1 else neg(term))
    return answer


def sum_gaussian(values):
    answer = ZERO
    for value in values:
        answer = add(answer, value)
    return answer


def matrix_add(*matrices):
    return [
        [sum_gaussian(matrix[row][column] for matrix in matrices) for column in range(3)]
        for row in range(3)
    ]


def hermitian_contraction(matrix):
    """Return U conjugate(V)^t for matrix=[U;V]."""
    return [
        [
            sum_gaussian(
                mul(matrix[row][column], conj(matrix[3 + other_row][column]))
                for column in range(3)
            )
            for other_row in range(3)
        ]
        for row in range(3)
    ]


def determinant_coordinate(matrices):
    """Seven-determinant formula for the integral Omega_W coordinate S(L)."""
    h1, h2, h3 = map(hermitian_contraction, matrices)
    positive = sum_gaussian(
        determinant3(matrix)
        for matrix in (matrix_add(h1, h2, h3), h1, h2, h3)
    )
    negative = sum_gaussian(
        determinant3(matrix)
        for matrix in (matrix_add(h1, h2), matrix_add(h1, h3), matrix_add(h2, h3))
    )
    return add(positive, neg(negative))


def direct_coordinate(matrices):
    answer = ZERO
    for columns in itertools.product(range(3), repeat=3):
        upper = [
            [matrices[block][row][columns[block]] for block in range(3)]
            for row in range(3)
        ]
        lower = [
            [matrices[block][row][columns[block]] for block in range(3)]
            for row in range(3, 6)
        ]
        answer = add(answer, mul(determinant3(upper), conj(determinant3(lower))))
    return answer


def exceptional_projection_coordinates(coordinate):
    """Return the Omega_W and Omega_Wbar coefficients after the factor eight."""
    return mul((0, -1), conj(coordinate)), mul((0, 1), coordinate)


def field_rank(matrix):
    work = [[(Fraction(x[0]), Fraction(x[1])) for x in row] for row in matrix]

    def fadd(x, y):
        return (x[0] + y[0], x[1] + y[1])

    def fneg(x):
        return (-x[0], -x[1])

    def fmul(x, y):
        return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])

    def finv(x):
        norm = x[0] * x[0] + x[1] * x[1]
        return (x[0] / norm, -x[1] / norm)

    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column] != ZERO),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = finv(work[pivot_row][column])
        work[pivot_row] = [fmul(inverse, value) for value in work[pivot_row]]
        for row in range(len(work)):
            if row != pivot_row and work[row][column] != ZERO:
                factor = work[row][column]
                work[row] = [
                    fadd(value, fneg(fmul(factor, pivot_value)))
                    for value, pivot_value in zip(work[row], work[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def prefilter(matrices):
    block_ranks = tuple(field_rank(matrix) for matrix in matrices)
    if min(block_ranks) < 2:
        return "REJECT_BLOCK_RANK", block_ranks, None
    combined = [sum((matrix[row] for matrix in matrices), []) for row in range(6)]
    total_rank = field_rank(combined)
    if total_rank < 6:
        return "REJECT_TOTAL_RANK", block_ranks, ZERO
    coordinate = determinant_coordinate(matrices)
    if coordinate == ZERO:
        return "REJECT_WEIL_ZERO", block_ranks, coordinate
    return "KEEP", block_ranks, coordinate


def poly_add(left, right):
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, 0) + coefficient
        if answer[monomial] == 0:
            del answer[monomial]
    return answer


def poly_mul(left, right):
    answer = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] = answer.get(monomial, 0) + left_coefficient * right_coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient}


def poly_determinant(matrix):
    answer = {}
    for permutation in PERMUTATIONS:
        term = {(): sign(permutation)}
        for row in range(3):
            term = poly_mul(term, matrix[row][permutation[row]])
        answer = poly_add(answer, term)
    return answer


def symbolic_identity_check():
    """Compare both formulas as polynomials in 54 independent symbols."""
    x = [[[(r * 9 + row * 3 + column,) for column in range(3)] for row in range(3)] for r in range(3)]
    y = [[[(27 + r * 9 + row * 3 + column,) for column in range(3)] for row in range(3)] for r in range(3)]

    def variable(monomial):
        return {monomial: 1}

    direct = {}
    for columns in itertools.product(range(3), repeat=3):
        upper = [[variable(x[r][row][columns[r]]) for r in range(3)] for row in range(3)]
        lower = [[variable(y[r][row][columns[r]]) for r in range(3)] for row in range(3)]
        direct = poly_add(direct, poly_mul(poly_determinant(upper), poly_determinant(lower)))

    mixed = {}
    for row_sources in itertools.permutations(range(3)):
        matrix = []
        for row, source in enumerate(row_sources):
            matrix_row = []
            for other_row in range(3):
                entry = {}
                for column in range(3):
                    entry = poly_add(
                        entry,
                        poly_mul(variable(x[source][row][column]), variable(y[source][other_row][column])),
                    )
                matrix_row.append(entry)
            matrix.append(matrix_row)
        mixed = poly_add(mixed, poly_determinant(matrix))
    assert mixed == direct
    return len(direct)


WITNESS = [
    [
        [ZERO, ZERO, ZERO], [(0, -1), ZERO, ZERO], [ZERO, ZERO, (0, 1)],
        [(0, 1), ZERO, ZERO], [ZERO, ZERO, ZERO], [ZERO, ZERO, (0, -1)],
    ],
    [
        [ZERO, ZERO, (-1, 0)], [ZERO, ZERO, ZERO], [(0, -1), ZERO, ONE],
        [ZERO, ONE, ZERO], [ONE, ZERO, ZERO], [ZERO, ZERO, (0, 1)],
    ],
    [
        [ZERO, (-1, 0), ZERO], [(-1, 0), ZERO, ZERO], [ZERO, ONE, (-1, 0)],
        [ONE, ZERO, ZERO], [ZERO, ONE, (-1, 0)], [ZERO, ZERO, ZERO],
    ],
]


def parse_candidate(value):
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError("candidate must contain three matrices")
    answer = []
    for matrix in value:
        if not isinstance(matrix, list) or len(matrix) != 6 or any(len(row) != 3 for row in matrix):
            raise ValueError("each matrix must be 6x3")
        answer.append([[ALPHABET[str(entry)] for entry in row] for row in matrix])
    return answer


def format_gaussian(value):
    real, imaginary = value
    if imaginary == 0:
        return str(real)
    if real == 0:
        return "i" if imaginary == 1 else "-i" if imaginary == -1 else f"{imaginary}i"
    return f"{real}{imaginary:+d}i"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", help="JSON file containing one candidate or a list of candidates")
    arguments = parser.parse_args()

    monomial_count = symbolic_identity_check()
    assert direct_coordinate(WITNESS) == determinant_coordinate(WITNESS) == (0, -1)
    assert exceptional_projection_coordinates(determinant_coordinate(WITNESS)) == (ONE, ONE)
    assert prefilter(WITNESS) == ("KEEP", (2, 3, 3), (0, -1))
    print("Cycle 249 F242 exact Weil prefilter")
    print(f"generic determinant identity checked ({monomial_count} nonzero monomials)")
    print("witness ranks = (2,3,3), total rank = 6, S(L) = -i")
    print("witness projection coefficients (Omega_W, Omega_Wbar) = (1, 1)")

    if arguments.json:
        with open(arguments.json, encoding="ascii") as source:
            raw = json.load(source)
        candidates = raw if raw and isinstance(raw[0][0][0], list) else [raw]
        for index, raw_candidate in enumerate(candidates):
            status, ranks, coordinate = prefilter(parse_candidate(raw_candidate))
            printed_coordinate = "-" if coordinate is None else format_gaussian(coordinate)
            print(f"candidate {index}: {status}; block ranks={ranks}; S={printed_coordinate}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
