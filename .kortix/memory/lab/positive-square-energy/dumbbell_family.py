#!/usr/bin/env python3
"""Exact certificates for equal odd-cycle dumbbells.

D_n is formed from two copies of C_n by adding one bridge between chosen
vertices.  The script uses the proved Chebyshev factorization of its
characteristic polynomial and rational root isolation, never floating point,
to certify s^+(D_n)-2n > 0 for a requested finite range.
"""

from __future__ import annotations

import argparse
from fractions import Fraction

import sympy as s


x = s.symbols("x")


def factors(n: int) -> tuple[s.Poly, s.Poly, s.Poly]:
    assert n >= 3 and n % 2 == 1
    k = (n - 1) // 2
    uk = s.chebyshevu(k, x / 2)
    ukm1 = s.chebyshevu(k - 1, x / 2)
    r = s.Poly(uk + ukm1, x)
    a = s.Poly((x - 2) * (uk + ukm1) - (uk - ukm1), x)
    b = s.Poly((x - 2) * (uk + ukm1) + (uk - ukm1), x)
    return r, a, b


def exact_lower(n: int, digits: int) -> s.Rational:
    r, a, b = factors(n)
    lower = s.Rational(-2 * n)
    eps = s.Rational(1, 10**digits)
    for poly, outer_mult in ((r, 2), (a, 1), (b, 1)):
        for (left, right), root_mult in poly.intervals(eps=eps):
            if right <= 0:
                continue
            if left <= 0:
                raise RuntimeError(f"interval straddles zero: n={n} {(left, right)}")
            lower += outer_mult * root_mult * left**2
    if lower <= 0:
        raise RuntimeError(f"NONPOSITIVE n={n}: {lower}")
    return lower


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-n", type=int, default=101)
    ap.add_argument("--digits", type=int, default=12)
    args = ap.parse_args()
    minimum: tuple[Fraction, int] | None = None
    count = 0
    for n in range(3, args.max_n + 1, 2):
        lower = exact_lower(n, args.digits)
        value = Fraction(int(lower.p), int(lower.q))
        if minimum is None or value < minimum[0]:
            minimum = value, n
        count += 1
    assert minimum is not None
    print(f"PASS odd_n_count={count} max_n={args.max_n} digits={args.digits}")
    print(f"minimum_n={minimum[1]}")
    print(f"minimum_exact_lower={minimum[0].numerator}/{minimum[0].denominator}")
    print(f"minimum_lower_decimal={float(minimum[0]):.17g}")


if __name__ == "__main__":
    main()
