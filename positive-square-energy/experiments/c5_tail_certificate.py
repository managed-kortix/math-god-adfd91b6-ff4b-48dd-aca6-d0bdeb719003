#!/usr/bin/env python3
"""Exact constants certificate for the C5--Cq phase-quadrature tail (q>=727)."""

import sympy as s


def main() -> None:
    # a=q/2-delta' is at least q/2-10.  With pi<22/7, inverse
    # differentiation and |delta''|<60 give this uniform bound for F''.
    a = s.symbols("a", positive=True)
    p = s.Rational(22, 7)
    M = 8*p**2/a**2 + 240*p**2/a**3

    # There are at most (q+7)/4=(2a+27)/4 midpoint cells.  Their union ends
    # at L+1/2, whereas b=q/4+1-atan(1/4)/pi.  In either residue class the
    # terminal discrepancy has length <1/3 (use 1/13<atan(1/4)/pi<1/12).
    # Because F(b)=F'(b)=0, its integral is at most M(1/3)^3/6.
    error = s.factor((2*a+27)*M/96 + M/s.Integer(162))
    derivative = s.factor(s.diff(error, a))
    assert derivative < 0
    error727 = s.factor(error.subs(a, s.Rational(707, 2)))
    assert error727 < s.Rational(1, 100)

    # r_q exceeds the limiting pole alpha>5/3, so its positive eigenvalue
    # x_q=r_q+r_q^-1 exceeds 34/15.  Use sqrt(5)<161/72 in the target.
    margin = (
        s.Rational(34, 15)**2 + 2
        - (s.Rational(161, 72) + s.Rational(9, 2))
    )
    assert s.Rational(161, 72)**2 > 5
    assert margin - error727 > 0

    # beta=atan(1/4)/pi lies in (1/13,1/12).  The upper bound uses
    # atan(x)<x and pi>3; the lower uses atan(x)>x-x^3/3 and pi<22/7.
    atan_lower = s.Rational(1, 4) - s.Rational(1, 3*4**3)
    assert atan_lower / p > s.Rational(1, 13)
    assert s.Rational(1, 4) / 3 < s.Rational(1, 12) or s.Rational(1, 4) / 3 == s.Rational(1, 12)

    # The finite outlier equation has A(r_q)=B(r_q)/r_q^q.  B is positive
    # on r>1 because B(1+t) has all positive coefficients.
    r, t = s.symbols("r t")
    B = r**8-r**7+r**4-2*r**3+2*r**2+r-1
    shifted = s.Poly(s.expand(B.subs(r, 1+t)), t)
    assert all(coefficient > 0 for coefficient in shifted.all_coeffs())

    print("PASS exact q>=727 quadrature constants")
    print(f"midpoint_plus_endpoint_error_at_727={error727} < 1/100")
    print(f"energy_margin_using_sqrt5_upper_bound={margin}")
    print(f"remaining_margin={s.factor(margin-error727)}")
    print("PASS 1/13 < atan(1/4)/pi < 1/12 and B(r)>0 for r>1")


if __name__ == "__main__":
    main()
