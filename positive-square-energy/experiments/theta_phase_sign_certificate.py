#!/usr/bin/env python3
"""Exact algebra checks for theta phase signs and safe short-base limits."""

import sympy as s


def main():
    z = s.symbols("z", positive=True)
    a, b = s.symbols("a b", integer=True, positive=True)

    # Difference identities behind strict shorter-path domination.  Here
    # b=a+2r, so r=(b-a)/2 is a positive integer.
    r = s.symbols("r", integer=True, positive=True)
    b_expr = a + 2*r
    odd_diff = (
        z**((a-1)/2)/(1+z**a)
        - z**((b_expr-1)/2)/(1+z**b_expr)
    )
    odd_factored = (
        z**((a-1)/2)*(1-z**r)*(1-z**(a+r))
        / ((1+z**a)*(1+z**(a+2*r)))
    )
    assert s.simplify(odd_diff-odd_factored) == 0

    even_diff = (
        z**(a/2-1)/(1-z**a)
        - z**(b_expr/2-1)/(1-z**b_expr)
    )
    even_factored = (
        z**(a/2-1)*(1-z**r)*(1+z**(a+r))
        / ((1-z**a)*(1-z**(a+2*r)))
    )
    assert s.simplify(even_diff-even_factored) == 0

    # Exact limiting carriers after removal of positive real factors.
    D23 = 1 + 2*z - z**2
    D14 = 1 + 2*z - z**2 + z**3 - z**4
    assert s.expand(D23-(1+z)-z*(1-z)) == 0
    assert s.expand(D14-(1+z)-z*(1-z)*(1+z**2)) == 0

    # The arctan majorant integrates exactly to 8/15.
    majorant_integrand = s.simplify((z**-2-1)*2*z**s.Rational(5, 2)/(1+z))
    assert s.simplify(majorant_integrand-2*s.sqrt(z)*(1-z)) == 0
    integral = s.integrate(2*s.sqrt(z)*(1-z), (z, 0, 1))
    assert integral == s.Rational(8, 15)
    assert s.Rational(8, 15) < s.Rational(3, 5)

    print("theta phase sign/limit certificate: PASS")


if __name__ == "__main__":
    main()
