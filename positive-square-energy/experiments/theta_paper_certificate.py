#!/usr/bin/env python3
"""Exact symbolic checks for the algebra displayed in paper.tex."""

import sympy as s


def bernstein_coefficients(poly, var, left, right, degree):
    t = s.symbols("t")
    transformed = s.Poly(s.expand(poly.subs(var, left + (right-left)*t)), t)
    power = [transformed.nth(i) for i in range(degree + 1)]
    # t^j = sum_{i=j}^n binom(i,j)/binom(n,j) B_i^n(t)
    return [s.factor(sum(power[j] * s.binomial(i, j) / s.binomial(degree, j)
                         for j in range(i + 1))) for i in range(degree + 1)]


x = s.symbols("x")
C = s.Rational(17, 16)
F = s.expand(16*x**4 - 6*(C-4*(1-x)**2)*(C-2*(1-x)**2))
assert s.expand(F - (-32*x**4+192*x**3-s.Rational(999,4)*x**2
                     +s.Rational(231,2)*x-s.Rational(2115,128))) == 0
for interval in [(s.Rational(15,32), s.Rational(2,3)),
                 (s.Rational(2,3), s.Rational(17,16))]:
    coeffs = bernstein_coefficients(F, x, *interval, 4)
    assert all(c > 0 for c in coeffs), (interval, coeffs)

# Length-three ear cleared ratio identity.
S, a, b = s.symbols("S a b", real=True)
t = s.Rational(1, 3)
U = S + (2+4*a)*t + 2*b*t**2
D = S + (6+8*a+8*b)*t**2 + (1+2*a**2+2*b**2)*t**4
E = s.expand(U**2-(S+1)*D)
target = (-2*S*a**2+144*S*a-2*S*b**2-36*S*b-28*S
          +142*a**2+48*a*b+72*a+2*b**2-48*b-19)/81
assert s.expand(E-target) == 0

# Chord constant is strictly positive.
assert 283**2 > 2*144**2
# Bordered-cycle gain exceeds one.
assert s.simplify(s.Rational(2, 1)/s.sqrt(3)-s.Rational(1,12)-1) > 0

print("PASS exact theta-paper algebra certificate")
