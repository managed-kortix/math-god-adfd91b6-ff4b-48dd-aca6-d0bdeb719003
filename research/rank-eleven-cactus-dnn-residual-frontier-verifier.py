#!/usr/bin/env python3
"""Exact arithmetic audit for the rank-eleven sharp-DNN frontier note.

This checks the rational and quadratic integer certificates used in the
symbolic reduction. It does not evaluate transcendental functions, enumerate
cacti, or prove a graph theorem.
"""

from fractions import Fraction


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    # Squaring certificates for a=5-2*sqrt(5).
    require(20 < 25, "a>0 certificate failed")
    require(4 < 5, "a<1 certificate failed")
    require(169 < 180, "3a<2 certificate failed")
    require(80 < 81, "2a>1 certificate failed")

    # cos(pi/7)>2159/2401>7/8 and the induced epsilon_7<7/15.
    cosine_lower = Fraction(2159, 2401)
    require(cosine_lower > Fraction(7, 8), "cosine rational bound failed")
    epsilon7_upper = 7 * (1 - Fraction(7, 8)) / (1 + Fraction(7, 8))
    require(epsilon7_upper == Fraction(7, 15), "epsilon_7 bound reduction failed")

    # 7/15<2*sqrt(5)-4 is certified by (67/30)^2<5.
    require(Fraction(67, 30) ** 2 < 5, "epsilon_5+epsilon_7 certificate failed")
    require(4489 < 4500, "cleared-denominator certificate failed")

    residuals = ("T^10Q (q>=3, including q=3)", "T^9PP")
    print("rank-eleven sharp-DNN residual frontier: exact arithmetic audit passed")
    for residual in residuals:
        print(f"  {residual}")
    print("status: DNN failure-set classification only; no cactus theorem claim")


if __name__ == "__main__":
    main()
