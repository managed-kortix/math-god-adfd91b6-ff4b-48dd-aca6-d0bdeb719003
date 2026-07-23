#!/usr/bin/env python3
"""Exact symbolic checks for the root-congruence witness."""

import sympy as s


def theta(lengths):
    n = sum(lengths) - 1
    A = s.zeros(n)
    nxt = 2
    for length in lengths:
        path = [0] + list(range(nxt, nxt + length - 1)) + [1]
        nxt += length - 1
        for u, v in zip(path, path[1:]):
            A[u, v] = A[v, u] = 1
    return A


def main():
    S, a, q, k = s.symbols("S a q k", real=True)
    U = S - 2 * (1 - k) * q - k**2 * a / 2
    D = S + 2 * (k**2 - 1) * q + (k**2 - 1) ** 2 * a**2
    direct = s.expand(2 * U - D)
    expected = S - 2 * (1 - k) ** 2 * q - k**2 * a - (1 - k**2) ** 2 * a**2
    assert s.expand(direct - expected) == 0

    loss = s.expand(S - direct)
    at_six_sevenths = s.factor(loss.subs(k, s.Rational(6, 7)))
    expected_loss = 2*q/s.Integer(49) + 36*a/s.Integer(49) + 169*a**2/s.Integer(2401)
    assert s.expand(at_six_sevenths - expected_loss) == 0

    derivative = s.factor(s.diff(loss, k) / 2)
    stationary = 2*a**2*k**3 + (2*q + a - 2*a**2)*k - 2*q
    assert s.expand(derivative - stationary) == 0

    x = s.symbols("x")
    expected_charpolys = {
        (2, 3, 3): (x - 1)*(x + 1)*(2*x**5 + x**4 - 14*x**3 - 4*x**2 + 20*x - 7),
        (1, 4, 4): x*(x**2 - 2)*(2*x**5 + x**4 - 14*x**3 - 4*x**2 + 20*x - 6),
        (2, 2, 3): x*(2*x**5 + x**4 - 14*x**3 - 4*x**2 + 18*x - 6),
    }
    for lengths, expected_poly in expected_charpolys.items():
        A = theta(lengths)
        A[0, 0] = -s.Rational(1, 2)
        actual = s.expand(2 * A.charpoly(x).as_expr())
        assert s.expand(actual - expected_poly) == 0

    print("root congruence symbolic certificate: PASS")


if __name__ == "__main__":
    main()
