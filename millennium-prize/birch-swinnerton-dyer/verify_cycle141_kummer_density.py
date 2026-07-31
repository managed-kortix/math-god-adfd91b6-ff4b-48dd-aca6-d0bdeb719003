#!/usr/bin/env python3
"""Exact finite-group checks for the Cycle 141 Kummer density lemma."""

from fractions import Fraction


P = 7


def matmul(a, b):
    return tuple(
        sum(a[2 * i + k] * b[2 * k + j] for k in range(2)) % P
        for i in range(2) for j in range(2)
    )


def det(a):
    return (a[0] * a[3] - a[1] * a[2]) % P


def rank_a_minus_i(a):
    b = ((a[0] - 1) % P, a[1], a[2], (a[3] - 1) % P)
    if b == (0, 0, 0, 0):
        return 0
    return 2 if det(b) else 1


def main():
    matrices = [
        (a, b, c, d)
        for a in range(P) for b in range(P)
        for c in range(P) for d in range(P)
        if (a * d - b * c) % P
    ]
    gl_size = P * (P - 1) ** 2 * (P + 1)
    assert len(matrices) == gl_size

    identity = (1, 0, 0, 1)
    unipotents = [
        a for a in matrices
        if a != identity
        and matmul(
            ((a[0] - 1) % P, a[1], a[2], (a[3] - 1) % P),
            ((a[0] - 1) % P, a[1], a[2], (a[3] - 1) % P),
        ) == (0, 0, 0, 0)
    ]
    assert len(unipotents) == P * P - 1
    assert all(rank_a_minus_i(a) == 1 for a in unipotents)
    assert Fraction(len(unipotents), gl_size) == Fraction(1, P * (P - 1))

    rows = [(x, y) for x in range(P) for y in range(P)]
    invertible_pairs = sum(
        1 for x in rows for y in rows
        if (x[0] * y[1] - x[1] * y[0]) % P
    )
    assert invertible_pairs == gl_size
    conditional = Fraction(invertible_pairs, P ** 4)
    assert conditional == Fraction((P - 1) * (P * P - 1), P ** 3)
    assert conditional == Fraction(288, 343)

    nonzero = [row for row in rows if row != (0, 0)]
    conditioned_nonzero = Fraction(invertible_pairs, len(nonzero) ** 2)
    assert conditioned_nonzero == Fraction(P, P + 1)
    absolute_pair = Fraction(1, P * (P - 1)) ** 2 * conditional
    assert absolute_pair == Fraction(P + 1, P ** 5) == Fraction(8, 16807)

    print("Cycle 141 finite-group Kummer density checks")
    print("p =", P)
    print("|GL2(F_p)| =", gl_size)
    print("nonidentity unipotents =", len(unipotents))
    print("unipotent prime density = 1/42")
    print("conditional invertible-pair density = 288/343")
    print("nonzero-row conditional density = 7/8")
    print("absolute ordered-pair density = 8/16807")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
