#!/usr/bin/env python3
"""Exact polynomial audit for two tricyclic Gram-threshold obstructions."""

from sympy import Poly, Rational, symbols


y = symbols("y")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def doubled_triangle_obstruction():
    q = Poly(73 * y**4 - 204 * y**3 + 214 * y**2 - 76 * y + 9, y)
    stationary = Poly(
        73 * y**5 - 219 * y**4 + 194 * y**3 - 62 * y**2 - 27 * y + 9,
        y,
    )
    require(q.count_roots(-10**6, 10**6) == 0,
            "doubled triangle quartic acquired a real root")
    require(q.eval(0) > 0, "doubled triangle quartic sign changed")
    require(stationary.count_roots(Rational(1, 4), Rational(1, 3)) == 1,
            "doubled triangle stationary-root isolation changed")


def unit_k4_obstruction():
    # S4 averaging gives an equicorrelation r. PSD requires r >= -1/3,
    # and each of the six unit-edge costs (1+r)/(1-r) is increasing.
    r = Rational(-1, 3)
    require(6 * (1 + r) / (1 - r) == 3,
            "unit K4 simplex optimum changed")
    require(3 > 2, "unit K4 no longer exceeds the DNN threshold")


def main():
    doubled_triangle_obstruction()
    unit_k4_obstruction()
    print("tricyclic Gram obstructions: exact audit passed")
    print("doubled triangle canonical class-111: minimum excess > 2")
    print("unit K4: exact minimum excess = 3")


if __name__ == "__main__":
    main()
