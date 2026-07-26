#!/usr/bin/env python3
"""Exact checks for symmetric block multiplicities and Mobius aggregation."""

from fractions import Fraction
from math import gcd


def mobius(n):
    ans = 1
    p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            ans = -ans
            if n % p == 0:
                return 0
            while n % p == 0:
                n //= p
        p += 1
    return -ans if n > 1 else ans


def block_form(c, e, rows, cols):
    return sum(c[i] * e[i][j] * c[j] for i in rows for j in cols)


def check_blocks():
    c = [Fraction(2), Fraction(-3), Fraction(5), Fraction(7)]
    e = [[Fraction((i + 2) * (j + 2) + (i == j)) for j in range(4)]
         for i in range(4)]
    e = [[(e[i][j] + e[j][i]) / 2 for j in range(4)] for i in range(4)]
    a, b = [0, 1], [2, 3]
    dense = block_form(c, e, range(4), range(4))
    stored = block_form(c, e, a, a) + 2 * block_form(c, e, a, b) + block_form(c, e, b, b)
    assert dense == stored


def check_aggregates():
    for N in range(2, 31):
        # Drop the common transcendental factor 1/log N and represent
        # log(N/(qj)) formally by the exponent vector log N-log q-log j.
        for q in range(1, N + 1):
            direct = {}
            for j in range(1, N // q + 1):
                m = mobius(q * j)
                for key, val in ((N, m), (q, -m), (j, -m)):
                    direct[key] = direct.get(key, Fraction(0)) + Fraction(val, j)
            reduced = {}
            if mobius(q) != 0:
                for j in range(1, N // q + 1):
                    if gcd(j, q) == 1:
                        m = mobius(q) * mobius(j)
                        for key, val in ((N, m), (q, -m), (j, -m)):
                            reduced[key] = reduced.get(key, Fraction(0)) + Fraction(val, j)
            assert {k: v for k, v in direct.items() if v} == {k: v for k, v in reduced.items() if v}


if __name__ == "__main__":
    check_blocks()
    check_aggregates()
    print("hierarchical multiplicity and Mobius aggregation checks passed")
