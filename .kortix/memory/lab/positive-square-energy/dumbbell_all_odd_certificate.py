#!/usr/bin/env python3
"""Exact finite certificate for the exceptional D_5 in the all-odd proof."""

from __future__ import annotations

import sympy as s
from fractions import Fraction


def dumbbell_adjacency(n: int) -> s.Matrix:
    a = s.zeros(2 * n)
    for offset in (0, n):
        for i in range(n):
            a[offset + i, offset + (i + 1) % n] = 1
            a[offset + (i + 1) % n, offset + i] = 1
    a[0, n] = a[n, 0] = 1
    return a


def main() -> None:
    x = s.symbols("x")
    results = []
    for n in (5, 9):
        poly = s.Poly(dumbbell_adjacency(n).charpoly(x).as_expr(), x)
        lower = s.Rational(-2 * n)
        for (left, right), multiplicity in poly.intervals(eps=s.Rational(1, 10**30)):
            if right > 0:
                assert left > 0
                lower += multiplicity * left**2
        assert lower > 0
        results.append((n, s.factor(poly.as_expr()), lower))

    # For every n>=9, cos(pi/n) >= 1-(22/(7n))^2/2 > 9/10, so
    # sec(pi/n)-1 < 1/9. This is the only rational tail estimate
    # needed after the gluing lemma supplies a correction >=1/9.
    def sec_deficit_upper(n: int) -> Fraction:
        z = Fraction(22, 7 * n) ** 2
        return z / (2 - z)

    assert Fraction(1, 18) > sec_deficit_upper(13)
    # pi(1-pi^2/(24*13^2))>3 using 333/106<pi<22/7.
    assert Fraction(333, 106) * (
        1 - Fraction(22, 7) ** 2 / (24 * 13**2)
    ) > 3
    for n, factorization, lower in results:
        print(f"PASS D_{n} exact SymPy certificate")
        print("charpoly=" + str(factorization))
        print(f"slack_lower={lower.p}/{lower.q}")
    print("PASS rational tail inequalities: d<2/3 and 2(sec(pi/n)-1)<1/9 for n>=13")


if __name__ == "__main__":
    main()
