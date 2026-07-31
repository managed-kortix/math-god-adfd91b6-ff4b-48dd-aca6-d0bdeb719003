#!/usr/bin/env python3
"""Exact chartwise obstruction and elimination checks for Cycle 203."""

from fractions import Fraction as F


def zero(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def matmul(left, right):
    out = zero(len(left), len(right[0]))
    for i in range(len(left)):
        for k in range(len(right)):
            for j in range(len(right[0])):
                out[i][j] += left[i][k] * right[k][j]
    return out


def rank(matrix):
    a = [row[:] for row in matrix]
    rows, cols = len(a), len(a[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((i for i in range(pivot_row, rows) if a[i][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        value = a[pivot_row][col]
        a[pivot_row] = [x / value for x in a[pivot_row]]
        for i in range(rows):
            if i != pivot_row and a[i][col]:
                value = a[i][col]
                a[i] = [x - value * y for x, y in zip(a[i], a[pivot_row])]
        pivot_row += 1
    return pivot_row


def determinant3(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def rho_matrix(diagonal):
    """Matrix of B -> Q^-1 B^t - diagonal*B, using row-major order."""
    q_inverse = (F(1), F(1), F(1, 3))
    out = zero(9, 9)
    for i in range(3):
        for j in range(3):
            output = 3 * i + j
            out[output][3 * j + i] += q_inverse[i]
            out[output][3 * i + j] -= diagonal[i]
    return out


def chart_matrix(pivot, values):
    """Ferrand chart map s -> ((s_j-a_j*s_pivot), 2*s_pivot)."""
    other = [j for j in range(3) if j != pivot]
    out = zero(3, 3)
    for row, j in enumerate(other):
        out[row][j] = F(1)
        out[row][pivot] = -values[j]
    out[2][pivot] = F(2)
    return out


def block_left(action):
    """Apply a normal-coordinate action independently in three H^1 directions."""
    out = zero(9, 9)
    for h in range(3):
        for i in range(3):
            for j in range(3):
                out[3 * i + h][3 * j + h] = action[i][j]
    return out


def stack(top, bottom):
    return [row[:] for row in top] + [row[:] for row in bottom]


def main():
    identity = rho_matrix((F(1), F(1), F(1)))
    diagonal = rho_matrix((F(3), F(1), F(1)))
    assert rank(identity) == 6
    assert rank(diagonal) == 8
    assert rank(stack(identity, diagonal)) == 8

    # Check every standard quotient chart at several exact parameter points.
    samples = ((F(0), F(0), F(0)), (F(2), F(-3), F(5)), (F(1, 2), F(7, 3), F(-4)))
    for pivot in range(3):
        for values in samples:
            action = chart_matrix(pivot, values)
            assert rank(action) == 3
            assert abs(determinant3(action)) == 2
            ferrand = block_left(action)
            assert rank(matmul(ferrand, identity)) == 6
            assert rank(matmul(ferrand, diagonal)) == 8
            assert rank(stack(matmul(ferrand, identity), matmul(ferrand, diagonal))) == 8

    # Elimination certificate: det(A_p)=+/-2 is a unit on every chart. Thus
    # A_p R_M=0 implies R_M=0. Each R_M has a displayed nonzero constant entry,
    # so the rank-zero ideal contracts to (1) in the quotient parameters.
    assert identity[0][0] == 0
    assert identity[1][3] == 1
    assert diagonal[0][0] == -2
    for pivot in range(3):
        symbolic_zero_values = (F(0), F(0), F(0))
        assert rank(chart_matrix(pivot, symbolic_zero_values)) == 3

    print("Cycle 203 first Ferrand doubles")
    print("quotient charts checked: 3; det(A_p) = +/-2")
    print("Gamma_I forced block rank/nullity: 6/3")
    print("Gamma_diag(3,1,1) forced block rank/nullity: 8/1")
    print("paired forced block rank/nullity: 8/1")
    print("rank-zero elimination ideal on every quotient chart: (1)")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
