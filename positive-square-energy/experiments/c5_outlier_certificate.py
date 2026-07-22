#!/usr/bin/env python3
"""Exact symbolic certificate for the C5--Cq positive outlier equation."""

from __future__ import annotations

import sympy as s


r, x = s.symbols("r x")
A = r**8-r**7-2*r**6+2*r**5-r**4+r-1
B = r**8-r**7+r**4-2*r**3+2*r**2+r-1


def main() -> None:
    derivative_numerator = s.factor(s.together(s.diff(B/A, r))).as_numer_denom()[0]
    expected = -4*r*(r-1)**2*(r**10+2*r**8+2*r**6+5*r**5+2*r**4+2*r**2+1)
    assert s.expand(derivative_numerator-expected) == 0
    resultant = s.factor(s.resultant(A, r**2-x*r+1, r))
    expected_resultant = -x**8+2*x**7+9*x**6-18*x**5-24*x**4+50*x**3+15*x**2-46*x+17
    assert s.expand(resultant-expected_resultant) == 0
    intervals = s.Poly(A, r).intervals(eps=s.Rational(1, 10**20))
    positive = [(i, m) for i, m in intervals if i[0] > 1]
    assert len(positive) == 1 and positive[0][1] == 1
    assert A.subs(r, s.Rational(5, 3)) < 0
    assert A.subs(r, s.Rational(17, 10)) > 0
    interval=(s.Rational(5,3),s.Rational(17,10))
    assert s.Poly(s.diff(A,r)-41,r).count_roots(*interval)==0
    assert (s.diff(A,r)-41).subs(r,interval[0])>0
    assert s.Poly(34-B,r).count_roots(*interval)==0
    assert (34-B).subs(r,interval[1])>0
    # At r=17/10 the finite equation r^q A-B is positive already for q=10,
    # hence for every q>=727; uniqueness places r_q below 17/10.
    assert (r**10*A-B).subs(r,interval[1])>0
    print("PASS exact C5 outlier identities")
    print("A(r)=" + str(A))
    print("d(B/A)/dr numerator=" + str(expected))
    print("elimination polynomial=" + str(-expected_resultant))
    print("unique_r_gt_1_interval=" + str(positive[0][0]))
    print("PASS pole bracket 5/3 < r_infinity < 17/10")
    print("PASS finite outlier convergence constants A'>41, B<34, r_q<17/10")


if __name__ == "__main__":
    main()
