#!/usr/bin/env python3
"""Exact mod 7^3 certificate for the 433a1 cyclotomic height regulator."""

from fractions import Fraction
from math import isqrt


P = (Fraction(0), Fraction(1))
Q = (Fraction(-1), Fraction(1))


def neg(point):
    x, y = point
    return x, -y - x


def add(left, right):
    if left is None:
        return right
    if right is None:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and y2 == -y1 - x1:
        return None
    if left != right:
        lam = (y2 - y1) / (x2 - x1)
        nu = (y1 * x2 - y2 * x1) / (x2 - x1)
    else:
        lam = (3 * x1 * x1 - y1) / (2 * y1 + x1)
        nu = (-x1 ** 3 + 2) / (2 * y1 + x1)
    x3 = lam * lam + lam - x1 - x2
    y3 = -(lam + 1) * x3 - nu
    result = (x3, y3)
    assert y3 * y3 + x3 * y3 == x3 ** 3 + 1
    return result


def mul(n, point):
    result = None
    while n:
        if n & 1:
            result = add(result, point)
        point = add(point, point)
        n //= 2
    return result


def integral_coordinates(point):
    x, y = point
    d = isqrt(x.denominator)
    assert d * d == x.denominator
    assert y.denominator == d ** 3
    return x.numerator, y.numerator, d


def mod_fraction(value, modulus):
    return value.numerator * pow(value.denominator, -1, modulus) % modulus


def log_unit_mod49(unit):
    # Teichmuller part is killed by u -> u^6; log(1+x)=x mod 49.
    return ((pow(unit, 6, 49) - 1) * pow(6, -1, 49)) % 49


def height_mod49(point):
    alpha, beta, d = integral_coordinates(mul(11, point))
    assert beta % 7
    t = (-d * alpha * pow(beta, -1, 49)) % 49
    # sigma(t)/d = -alpha/beta * (1+t/2+O(t^2)); t^2=0 mod49.
    assert t % 7 == 0
    unit = (-alpha * pow(beta, -1, 49)) % 49
    unit = unit * (1 + t * pow(2, -1, 49)) % 49
    logarithm = log_unit_mod49(unit)
    height = (-2 * pow(121, -1, 49) * logarithm) % 49
    return height, t, unit, logarithm, (alpha, beta, d)


def main():
    assert add(P, Q) == (Fraction(1), Fraction(-2))
    hp = height_mod49(P)
    hq = height_mod49(Q)
    hpq = height_mod49(add(P, Q))
    assert hp[:4] == (42, 28, 44, 7)
    assert hq[:4] == (28, 21, 22, 21)
    assert hpq[:4] == (42, 0, 8, 7)

    cross = ((hpq[0] - hp[0] - hq[0]) * pow(2, -1, 49)) % 49
    assert cross == 35
    # Products of entries known mod 49 and divisible by 7 are known mod 343.
    regulator = (hp[0] * hq[0] - cross * cross) % 343
    assert regulator == 294 == 6 * 49

    print("Cycle 143 exact 433a1 p-adic height certificate")
    print("h(P), h(P,Q), h(Q) mod 49 = 42, 35, 28")
    print("regulator mod 343 = 294 = 6*7^2")
    print("v_7(regulator) = 2; unit mod 7 = 6")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
