#!/usr/bin/env python3
"""Exact root-isolation checks for bridge-path cycle-closure frontiers."""

from __future__ import annotations

import sympy as sp


def splus_bounds(a: sp.Matrix) -> tuple[sp.Expr, sp.Rational, sp.Rational]:
    x = sp.symbols("x")
    p = sp.Poly(a.charpoly(x).as_expr(), x)
    lo = hi = sp.Rational(0)
    for (left, right), multiplicity in p.intervals(eps=sp.Rational(1, 10**50)):
        if left > 0:
            lo += multiplicity * left**2
            hi += multiplicity * right**2
    return sp.factor(p.as_expr()), lo, hi


def check_pair(a: sp.Matrix, u: int, v: int, expected: str) -> None:
    b = a.copy()
    b[u, v] = b[v, u] = 1
    pa, alo, ahi = splus_bounds(a)
    pb, blo, bhi = splus_bounds(b)
    delta_lo, delta_hi = blo - ahi, bhi - alo
    if expected == "negative":
        assert delta_hi < 0
    else:
        assert delta_lo > 0
    print("before polynomial:", pa)
    print("after polynomial:", pb)
    print("increment interval:", (delta_lo, delta_hi))
    print("increment decimal:", (sp.N(delta_lo, 25), sp.N(delta_hi, 25)))


def main() -> None:
    # Weighted counterexample: a five-vertex bridge path with every path edge
    # of weight 4, closed by a unit edge.
    weighted = sp.zeros(5)
    for i in range(4):
        weighted[i, i + 1] = weighted[i + 1, i] = 4
    print("WEIGHTED P5, PATH WEIGHT 4")
    check_pair(weighted, 0, 4, "negative")

    # Lowest unweighted graph found: a P5 whose final vertex lies in a triangle.
    unweighted = sp.zeros(7)
    for u, v in ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6)):
        unweighted[u, v] = unweighted[v, u] = 1
    print("UNWEIGHTED P5 WITH END TRIANGLE")
    check_pair(unweighted, 0, 4, "positive")
    print("EXACT CERTIFICATE PASSED")


if __name__ == "__main__":
    main()
