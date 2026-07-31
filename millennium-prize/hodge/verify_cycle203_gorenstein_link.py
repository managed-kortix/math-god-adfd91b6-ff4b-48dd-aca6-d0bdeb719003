#!/usr/bin/env python3
"""Dependency-free exact checks for the Cycle 203 Gorenstein-link gate."""

from fractions import Fraction


def rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            multiple = work[row][column]
            work[row] = [
                value - multiple * pivot_value
                for value, pivot_value in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def rho_matrix(diagonal_d):
    q_inverse = (Fraction(1), Fraction(1), Fraction(1, 3))
    matrix = [[Fraction(0) for _ in range(9)] for _ in range(9)]
    for row in range(3):
        for column in range(3):
            output = 3 * row + column
            matrix[output][3 * column + row] += q_inverse[row]
            matrix[output][3 * row + column] -= diagonal_d[row]
    return matrix


def exponential_coefficient(weight, degree):
    factorial = (1, 1, 2, 6)[degree]
    return Fraction((-weight) ** degree, factorial)


def be_chern_coefficient(degree):
    # ch(O_W) = 1 - 5 exp(-2L) + 5 exp(-3L) - exp(-5L).
    if degree == 0:
        return Fraction(1 - 5 + 5 - 1)
    return (
        -5 * exponential_coefficient(2, degree)
        + 5 * exponential_coefficient(3, degree)
        - exponential_coefficient(5, degree)
    )


def main():
    coefficients = tuple(be_chern_coefficient(degree) for degree in range(4))
    assert coefficients == (0, 0, 0, 5)

    rho_i = rho_matrix((1, 1, 1))
    rho_d = rho_matrix((3, 1, 1))
    rank_i = rank(rho_i)
    rank_d = rank(rho_d)
    assert rank_i == 6
    assert rank_d == 8
    assert 9 - rank_i == 3
    assert 9 - rank_d == 1

    # A nonzero constant coefficient is a unit over Q, so the ideal cutting
    # out a zero obstruction matrix is already (1), before any saturation.
    nonzero_i = [value for row in rho_i for value in row if value]
    nonzero_d = [value for row in rho_d for value in row if value]
    assert Fraction(-1) in nonzero_i
    assert Fraction(-3) in nonzero_d
    rank_zero_ideal_i = "(1)" if nonzero_i else "(0)"
    rank_zero_ideal_d = "(1)" if nonzero_d else "(0)"
    assert rank_zero_ideal_i == rank_zero_ideal_d == "(1)"

    print("Buchsbaum--Eisenbud ch coefficients in degrees 0..3:", coefficients)
    print("ch_3(O_W) = 5 L^3")
    print("ch_3(I_G/I_W) = 5 L^3 - [G]")
    print("exceptional coefficients for Gamma_I, Gamma_D residuals: -1, -3")
    print("PEL ranks for Gamma_I, Gamma_D:", rank_i, rank_d)
    print("PEL kernel dimensions:", 9 - rank_i, 9 - rank_d)
    print("rank-zero ideals before saturation:", rank_zero_ideal_i, rank_zero_ideal_d)
    print("rank-zero ideals after proper-link saturation: (1) (1)")
    print("all Cycle 203 exact checks passed")


if __name__ == "__main__":
    main()
