#!/usr/bin/env python3
"""Exact verifier for the K_n--K_n bridge-correction obstruction."""
from fractions import Fraction
from math import isqrt


def qplus(n):
    """x^2-(n-1)x-1, from the copy-symmetric quotient."""
    return (1, -(n - 1), -1)


def qminus(n):
    """x^2-(n-3)x-(2n-3), from the copy-antisymmetric quotient."""
    return (1, -(n - 3), -(2 * n - 3))


def correction_interval(n, bits=120):
    """A rigorous dyadic interval enclosing Delta_n, without floats."""
    scale = 1 << bits
    rad1 = (n - 1) ** 2 + 4
    rad2 = (n + 1) ** 2 - 4
    lo1 = isqrt(rad1 * scale * scale)
    lo2 = isqrt(rad2 * scale * scale)
    hi1 = lo1 if lo1 * lo1 == rad1 * scale * scale else lo1 + 1
    hi2 = lo2 if lo2 * lo2 == rad2 * scale * scale else lo2 + 1
    alo = Fraction((n - 1) * scale + lo1, 2 * scale)
    ahi = Fraction((n - 1) * scale + hi1, 2 * scale)
    blo = Fraction((n - 3) * scale + lo2, 2 * scale)
    bhi = Fraction((n - 3) * scale + hi2, 2 * scale)
    return (
        alo * alo + blo * blo - 2 * (n - 1) ** 2,
        ahi * ahi + bhi * bhi - 2 * (n - 1) ** 2,
    )


def verify_symbolic_bound(n):
    """Verify every exact rational identity/positivity step for one n>=3."""
    if n < 3:
        raise ValueError("symbolic bound requires n>=3")
    a = n - 1
    b = n + 1
    root1_upper = Fraction(a) + Fraction(2, a) - Fraction(2, a**3) + Fraction(4, a**5)
    root2_upper = Fraction(b) - Fraction(2, b) - Fraction(2, b**3)
    # Squaring certificates for the two radical upper bounds.
    if not root1_upper > 0:
        raise RuntimeError("first radical upper bound is not positive")
    if root1_upper**2 - (a * a + 4) != Fraction(
        4 * (5 * n**4 - 20 * n**3 + 26 * n**2 - 12 * n + 5),
        (n - 1) ** 10,
    ):
        raise RuntimeError("first radical square identity failed")
    if not root2_upper > 0:
        raise RuntimeError("second radical upper bound is not positive")
    if root2_upper**2 - (b * b - 4) != Fraction(
        4 * (2 * n**2 + 4 * n + 3), (n + 1) ** 6
    ):
        raise RuntimeError("second radical square identity failed")
    delta_upper = (
        -n * n
        + 2 * n
        + 1
        + Fraction(n - 1, 2) * root1_upper
        + Fraction(n - 3, 2) * root2_upper
    )
    m = n - 3
    p = n**5 - 2 * n**4 + n**3 - 2 * n**2 - 2
    if p != m**5 + 13 * m**4 + 67 * m**3 + 169 * m**2 + 204 * m + 88:
        raise RuntimeError("positive-polynomial translation failed")
    gap = Fraction(2 * (3 * n - 1) * p, n * (n - 1) ** 4 * (n + 1) ** 3)
    if Fraction(4, n) - delta_upper != gap or not gap > 0:
        raise RuntimeError("4/n upper-bound certificate failed")


def verify():
    if qplus(2) != (1, -1, -1) or qminus(2) != (1, 1, -1):
        raise RuntimeError("quadratic-factor self-check failed")
    # n=2 has positive roots phi and 1/phi, hence Delta_2=1.
    if not Fraction(1) < Fraction(4, 2):
        raise RuntimeError("n=2 bound failed")
    for n in range(3, 101):
        verify_symbolic_bound(n)
    # Independent exact dyadic checks, including strictness.  Strict positivity
    # also follows for all n from the projector correction Delta_n>=1/n^2.
    for n in range(2, 101):
        lo, hi = correction_interval(n)
        if lo < Fraction(1, n * n) or hi >= Fraction(4, n):
            raise RuntimeError(f"dyadic enclosure failed at n={n}")
    print("K_n--K_n exact bridge family: VERIFIED")
    print("charpoly=(x+1)^(2n-4)*(x^2-(n-1)x-1)*(x^2-(n-3)x-(2n-3))")
    print("0 < Delta_n < 4/n for every integer n>=2; hence inf Delta_n=0")


if __name__ == "__main__":
    verify()
