#!/usr/bin/env python3
"""Exact rational checks for the first KI240 projector toy models."""

from fractions import Fraction as F


Q = (F(1), F(1), F(3))
POWERS = ((1, 0), (2, 1), (3, 4), (2, 11), (-7, 24), (-38, 41), (-117, 44))
COEFFICIENTS = (
    317131927490234375,
    -2073948378906250,
    12564289203125,
    -56707735500,
    27598945,
    3626326,
    -68381,
)


def unit(i, j):
    return [[F((r, s) == (i, j)) for s in range(3)] for r in range(3)]


def rho(norm, b):
    return [[b[j][i] / Q[i] - norm * b[i][j] for j in range(3)] for i in range(3)]


def flatten(a):
    return [a[i][j] for i in range(3) for j in range(3)]


def rank(rows):
    a = [row[:] for row in rows]
    row = 0
    for col in range(len(a[0])):
        pivot = next((r for r in range(row, len(a)) if a[r][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        z = a[row][col]
        a[row] = [x / z for x in a[row]]
        for r in range(len(a)):
            if r != row and a[r][col]:
                z = a[r][col]
                a[r] = [x - z * y for x, y in zip(a[r], a[row])]
        row += 1
    return row


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def main():
    tangent_basis = [unit(i, j) for i in range(3) for j in range(3)]
    ranks = []
    witnesses = []
    for a, b in POWERS:
        norm = a * a + b * b
        rows = [flatten(rho(norm, tangent)) for tangent in tangent_basis]
        ranks.append(rank(rows))
        witnesses.append(next(j for j, row in enumerate(rows) if any(row)))
    assert ranks == [6, 9, 9, 9, 9, 9, 9]
    assert all(COEFFICIENTS)

    # The first actual cross-Hom atom occurs after a shift difference of three.
    # Its degree-zero algebra is the upper triangular 2 by 2 algebra.  Every
    # noncentral idempotent with diagonal (1,0) is a graph projector e_x.
    for x in (F(-7, 3), F(0), F(11, 5)):
        e = [[F(1), x], [F(0), F(0)]]
        assert matmul(e, e) == e
        # Positive self-Ext classes annihilate cross Ext^3, since cross Ext is
        # concentrated in degree three.  Thus e o e keeps the source corner.
        for p in (F(1), F(2, 3), F(-5)):
            o = [[p, F(0)], [F(0), F(0)]]
            assert matmul(matmul(e, o), e)[0][0] == p

    print("Cycle 241 KI240 actual-Ext toy search")
    print(f"graph obstruction ranks over Q = {ranks}")
    print(f"first nonzero tangent indices = {witnesses}")
    print("shift-gap-3 noncentral graph projectors retain the diagonal corner")
    print("all exact rational checks passed")


if __name__ == "__main__":
    main()
