#!/usr/bin/env python3
"""Small exact checker independent of PARI and curve databases."""

from fractions import Fraction
from math import gcd


def rhs(x):
    return x**3 + x**2


def on_curve(point):
    x, y = map(Fraction, point)
    return y * y + y == rhs(x)


def count_mod_p(p):
    return 1 + sum(
        1
        for x in range(p)
        for y in range(p)
        if (y * y + y - x**3 - x**2) % p == 0
    )


def discriminant_cubic(poly):
    # poly is a*x^3+b*x^2+c*x+d.
    a, b, c, d = poly
    return b*b*c*c - 4*a*c**3 - 4*b**3*d - 27*a*a*d*d + 18*a*b*c*d


assert on_curve((0, 0))

# Completing the square gives Y^2=4*x^3+4*x^2+1.  Its roots are the
# x-coordinates of nonzero rational 2-torsion.  Rational-root testing leaves
# no root, so E(Q)[2]=0.
two_division = (4, 4, 0, 1)
assert all(4 * Fraction(r) ** 3 + 4 * Fraction(r) ** 2 + 1 for r in (1, -1, Fraction(1, 2), Fraction(-1, 2), Fraction(1, 4), Fraction(-1, 4)))
assert discriminant_cubic(two_division) == -16 * 43

rows = []
torsion_bound = 0
for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 47):
    n = count_mod_p(p)
    a = p + 1 - n
    rows.append((p, a, n))
    if p != 43:
        torsion_bound = gcd(torsion_bound, n)

print("MODEL=y^2+y=x^3+x^2")
print("P=(0,0) ON_CURVE=1")
print("TWO_DIVISION_POLYNOMIAL=4*x^3+4*x^2+1 IRREDUCIBLE_OVER_Q=1")
print("FROBENIUS_COLUMNS=[p,a_p,#E(F_p)]")
for row in rows:
    print(row)
print(f"TORSION_ORDER_DIVIDES_GCD={torsion_bound}")
assert torsion_bound == 1
print("EXACT_ASSERTIONS_PASSED=1")
