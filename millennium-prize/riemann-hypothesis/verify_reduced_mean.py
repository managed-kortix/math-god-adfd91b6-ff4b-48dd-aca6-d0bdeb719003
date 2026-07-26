#!/usr/bin/env python3
"""Exact rational checks for reduced-frequency/gcd period means."""

from fractions import Fraction
from math import gcd, lcm


def integrate_pair(a, b):
    """Average of beta_a beta_b by exact unit-interval integration."""
    L = lcm(a, b)
    total = Fraction(0)
    for k in range(L):
        ca = -Fraction(k // a, 1) - Fraction(1, 2)
        cb = -Fraction(k // b, 1) - Fraction(1, 2)
        # (t/a+ca)(t/b+cb), integrated from k to k+1.
        total += Fraction((k + 1) ** 3 - k**3, 3 * a * b)
        total += (Fraction(ca, b) + Fraction(cb, a)) * Fraction(2 * k + 1, 2)
        total += ca * cb
    return total / L


def j2(n):
    out = n * n
    p = 2
    x = n
    while p * p <= x:
        if x % p == 0:
            out = out // (p * p) * (p * p - 1)
            while x % p == 0:
                x //= p
        p += 1
    if x > 1:
        out = out // (x * x) * (x * x - 1)
    return out


def gcd_form(u, v):
    M = max(len(u), len(v)) - 1
    return sum(
        u[a] * v[b] * Fraction(gcd(a, b) ** 2, a * b)
        for a in range(1, len(u))
        for b in range(1, len(v))
    )


def divisor_form(u, v):
    M = max(len(u), len(v)) - 1
    total = Fraction(0)
    for d in range(1, M + 1):
        U = sum((u[d * j] / j for j in range(1, (len(u) - 1) // d + 1)), Fraction(0))
        V = sum((v[d * j] / j for j in range(1, (len(v) - 1) // d + 1)), Fraction(0))
        total += Fraction(j2(d), d * d) * U * V
    return total


for a in range(1, 9):
    for b in range(1, 9):
        expected = Fraction(gcd(a, b) ** 2, 12 * a * b)
        assert integrate_pair(a, b) == expected

u = [Fraction(0), Fraction(2, 3), Fraction(-5, 7), Fraction(4, 5), Fraction(0), Fraction(-3, 2)]
v = [Fraction(0), Fraction(-1, 4), Fraction(7, 9), Fraction(0), Fraction(5, 6), Fraction(2, 11)]
assert gcd_form(u, v) == divisor_form(u, v)

# Direct endpoint-functional mean versus reduced divisor frequencies.
c = u
d = v
alpha = Fraction(3, 17)
m = Fraction(5, 13)
n = Fraction(-2, 9)
direct = 2 * m * n - alpha * n * n + Fraction(1, 12) * (
    2 * gcd_form(c, d) - alpha * gcd_form(d, d)
)
reduced = 2 * m * n - alpha * n * n + Fraction(1, 12) * (
    2 * divisor_form(c, d) - alpha * divisor_form(d, d)
)
assert direct == reduced

print("pair correlations, divisor aggregation, and endpoint mean checks passed")
print("endpoint mean =", direct)
