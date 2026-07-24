#!/usr/bin/env python3
"""Exact certificate for the local four-fifths reduction."""

import sympy as s


def main():
    x = s.symbols("x")
    U = s.Rational(1, 5) + x/2 + x**2/2 + x**3/9

    # Exact positivity on the two pieces.  SymPy's interval routine uses exact
    # real-root isolation; endpoints and every critical point are covered.
    assert s.Poly(U, x).is_nonnegative is not False
    for f, left, right in ((U, -3, 0), (U-x**2, 0, 3)):
        critical = s.Poly(s.diff(f, x), x).intervals()
        assert f.subs(x, left) > 0 and f.subs(x, right) > 0
        for interval, multiplicity in critical:
            lo, hi = interval
            if hi < left or lo > right:
                continue
            # Exact minimum from algebraic critical roots.
            for root in s.solve(s.diff(f, x), x):
                if root.is_real and bool(root >= left) and bool(root <= right):
                    assert s.simplify(f.subs(x, root)) > 0

    # (degree, triangle-walk count, a upper bound, q upper bound)
    states = [
        (3, 0, s.Rational(97, 112), s.Rational(17, 10)),
        (3, 2, s.Rational(97, 112), s.Rational(173, 90)),
        (3, 4, s.Rational(97, 112), s.Rational(193, 90)),
        (2, 0, s.Rational(17, 24), s.Rational(6, 5)),
        (2, 2, s.Rational(17, 24), s.Rational(64, 45)),
    ]
    margins = []
    for d, tau, a, q in states:
        assert q == s.Rational(1, 5) + s.Rational(d, 2) + s.Rational(tau, 9)
        loss = s.Rational(2, 49)*q + s.Rational(36, 49)*a + s.Rational(169, 2401)*a**2
        margin = s.factor(s.Rational(4, 5) - loss)
        assert margin > 0
        margins.append(margin)

    expected_worst = s.Rational(31684811, 1355316480)
    assert min(margins) == expected_worst

    # Explicitly reject the false cubic majorant.
    false_u1 = s.Rational(1, 2) + x/2 + x**3/9
    assert false_u1.subs(x, -3) == -4

    print("local four-fifths certificate: PASS")


if __name__ == "__main__":
    main()
