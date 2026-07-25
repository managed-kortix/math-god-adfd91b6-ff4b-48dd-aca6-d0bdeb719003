#!/usr/bin/env python3
"""Exact finite-tree obstruction to the bare-C5 pointwise phase comparison."""

import sympy as sp


def main():
    x = sp.symbols("x")
    t = sp.symbols("t", real=True)
    edges = {
        (0, 1), (1, 2), (2, 3), (3, 4), (0, 4),
        (0, 5), (5, 6), (0, 6),
        (1, 7), (7, 8), (1, 8),
        (2, 9),
    }
    adjacency = sp.zeros(10)
    for u, v in edges:
        adjacency[u, v] = adjacency[v, u] = 1

    characteristic = sp.factor(adjacency.charpoly(x).as_expr())
    expected = sp.factor(
        (x + 1) ** 2
        * (x**3 + x**2 - 3*x - 1)
        * (x**5 - 3*x**4 - 3*x**3 + 11*x**2 - x - 3)
    )
    assert sp.expand(characteristic - expected) == 0

    psi = sp.expand(sp.I ** (-10) * characteristic.subs(x, sp.I * t))
    real = sp.re(psi).expand()
    imag = sp.im(psi).expand()
    z5 = t**5 + 5 * t**3 + 5 * t
    cross = sp.factor(2 * real - z5 * imag)
    expected_cross = 2 * (
        2 * t**12 + 24 * t**10 + 110 * t**8 + 233 * t**6
        + 212 * t**4 + 52 * t**2 - 3
    )
    assert sp.expand(cross - expected_cross) == 0
    value = sp.factor(cross.subs(t, sp.Rational(1, 7)))
    assert value == -sp.Rational(51170666676, 13841287201)

    print("characteristic polynomial:", characteristic)
    print("R(t):", real)
    print("I(t):", imag)
    print("2R-Z_C5 I:", cross)
    print("value at t=1/7:", value)
    print("CERTIFIED: the bare-C5 pointwise phase comparison fails")


if __name__ == "__main__":
    main()
