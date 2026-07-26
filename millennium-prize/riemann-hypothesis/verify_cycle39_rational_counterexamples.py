#!/usr/bin/env python3
"""Exact Fraction verification of the Cycle 39 rational counterexamples."""

from fractions import Fraction as F


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def mat_vec(matrix, vector):
    return [dot(row, vector) for row in matrix]


def quadratic(vector, matrix):
    return dot(vector, mat_vec(matrix, vector))


def check_smallest():
    gram = [[F(1), F(1, 2)], [F(1, 2), F(1)]]
    u2 = [F(1), F(0)]
    u3 = [F(1), F(-1, 2)]
    assert u3 == [u2[i] + F(1, 2) * d for i, d in enumerate([F(0), F(-1)])]
    assert gram[0][0] * gram[1][1] - gram[0][1] ** 2 == F(3, 4)
    p2, p3 = quadratic(u2, gram), quadratic(u3, gram)
    assert (p2, p3) == (F(1), F(3, 4))
    assert p2 - p3 == F(1, 4) < F(1, 2) * p2
    return p2, p3


def check_nested():
    gram = [
        [F(37, 36), F(1, 2), F(0)],
        [F(1, 2), F(5, 18), F(0)],
        [F(0), F(0), F(1, 36)],
    ]
    u2 = [F(1), F(0), F(0)]
    u3 = [F(1), F(-1, 2), F(0)]
    u4 = [F(1), F(-2, 3), F(-1, 3)]

    d2 = [F(0), F(-1), F(0)]
    d3 = [F(0), F(-1), F(-2)]
    assert u3 == [u2[i] + F(1, 2) * d2[i] for i in range(3)]
    assert u4 == [u3[i] + F(1, 6) * d3[i] for i in range(3)]

    # Sylvester minors certify positive definiteness.
    minor2 = gram[0][0] * gram[1][1] - gram[0][1] ** 2
    determinant = minor2 * gram[2][2]
    assert gram[0][0] > 0 and minor2 == F(23, 648) and determinant == F(23, 23328)

    p2, p3, p4 = (quadratic(u, gram) for u in (u2, u3, u4))
    assert (p2, p3, p4) == (F(37, 36), F(43, 72), F(79, 162))
    assert p2 - p3 == F(31, 72) > 0
    assert p3 - p4 == F(71, 648) > 0

    weighted = F(1, 2) * p2 + F(1, 3) * p3
    decrement = p2 - p4
    assert weighted == F(77, 108)
    assert decrement == F(175, 324)
    assert decrement - weighted == F(-14, 81)

    # Rational R^4 realization and exact weighted covariance completion.
    phi0 = [F(1), F(1, 6), F(0), F(0)]
    phi2 = [F(1, 2), F(0), F(1, 6), F(0)]
    phi3 = [F(0), F(0), F(0), F(1, 6)]
    phis = [phi0, phi2, phi3]
    assert [[dot(x, y) for y in phis] for x in phis] == gram
    endpoints = [
        [sum((u[j] * phis[j][i] for j in range(3)), F(0)) for i in range(4)]
        for u in (u2, u3)
    ]
    weights = [F(1, 2), F(1, 3)]
    total_weight = sum(weights, F(0))
    mean = [
        sum((weights[n] * endpoints[n][i] for n in range(2)), F(0)) / total_weight
        for i in range(4)
    ]
    mean_square = total_weight * dot(mean, mean)
    variance = sum(
        (weights[n] * dot([endpoints[n][i] - mean[i] for i in range(4)],
                          [endpoints[n][i] - mean[i] for i in range(4)])
         for n in range(2)),
        F(0),
    )
    assert mean_square == F(151, 216)
    assert variance == F(1, 72) > 0
    assert mean_square + variance == weighted
    return p2, p3, p4, decrement, weighted, variance


def main():
    small = check_smallest()
    nested = check_nested()
    print("PASS Cycle 39 exact rational coefficient-path counterexamples")
    print(f"small P={small}, decrement=1/4, rhs=1/2")
    print(
        "nested P=%s, decrement=%s, rhs=%s, surplus=%s, covariance=%s"
        % (nested[:3], nested[3], nested[4], nested[3] - nested[4], nested[5])
    )


if __name__ == "__main__":
    main()
