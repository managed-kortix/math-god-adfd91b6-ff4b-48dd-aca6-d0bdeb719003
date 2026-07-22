#!/usr/bin/env python3
"""Exact candidate degree-16 moment minorant for the C5--Cq family."""

from __future__ import annotations

import sympy as s


x = s.symbols("x")
COEFFS = [
    s.Rational(-125923,18247576), s.Rational(2425747,25000000),
    s.Rational(10984041,20000000), s.Rational(73387889,100000000),
    s.Rational(-15034781,100000000), s.Rational(-764437,1250000),
    s.Rational(1396073,6250000), s.Rational(10617087,25000000),
    s.Rational(-18068401,100000000), s.Rational(-18461813,100000000),
    s.Rational(524147,6250000), s.Rational(4743427,100000000),
    s.Rational(-2229999,100000000), s.Rational(-658133,100000000),
    s.Rational(157859,50000000), s.Rational(949,2500000),
    s.Rational(-3689,20000000),
]
P = s.Poly(sum(c*x**i for i, c in enumerate(COEFFS)), x)


def nonpositive_on(poly: s.Poly, left: s.Rational, right: s.Rational) -> bool:
    # A continuous polynomial with no root on the interval has constant sign.
    return poly.count_roots(left, right) == 0 and poly.eval(left) < 0


def main() -> None:
    # Spectral support is conservatively contained in [-11/5, 231/100].
    assert nonpositive_on(P, s.Rational(-11,5), s.Rational(0))
    assert nonpositive_on(P-s.Poly(x**2,x), s.Rational(0), s.Rational(231,100))
    slopes = [s.Rational(1,2),0,1,0,3,0,10,0,35,0,126,0,462,0,1716,0,6435]
    intercepts = [s.Rational(7,2),2,11,8,49,37,236,177,1169,872,5861,4413,
                  29548,22817,149349,119788,755809]
    slope = sum(c*m for c,m in zip(COEFFS,slopes))
    intercept = sum(c*m for c,m in zip(COEFFS,intercepts))
    print("PASS exact candidate minorant")
    print(f"slope={slope} decimal={s.N(slope,18)}")
    print(f"intercept={intercept} decimal={s.N(intercept,18)}")


if __name__ == "__main__":
    main()
