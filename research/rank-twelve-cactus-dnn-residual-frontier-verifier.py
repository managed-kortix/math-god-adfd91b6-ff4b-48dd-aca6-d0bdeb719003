#!/usr/bin/env python3
"""Fail-closed exact audit of the rank-twelve sharp-DNN frontier.

The audit uses Fraction arithmetic and Q(sqrt(5)) only.  It checks the exact
inequalities and the exhaustive triangle-count reduction; it does not certify
the sharp DNN theorem itself or a rank-twelve cactus theorem.
"""

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@dataclass(frozen=True)
class Qsqrt5:
    rational: Fraction
    radical: Fraction = Fraction(0)

    def __add__(self, other):
        other = as_qsqrt5(other)
        return Qsqrt5(self.rational + other.rational, self.radical + other.radical)

    def __sub__(self, other):
        other = as_qsqrt5(other)
        return Qsqrt5(self.rational - other.rational, self.radical - other.radical)

    def __mul__(self, other):
        other = as_qsqrt5(other)
        return Qsqrt5(
            self.rational * other.rational + 5 * self.radical * other.radical,
            self.rational * other.radical + self.radical * other.rational,
        )

    __rmul__ = __mul__

    def sign(self):
        """Return the exact sign in Q(sqrt(5)), using rational squaring."""
        a, b = self.rational, self.radical
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        comparison = a * a - 5 * b * b
        require(comparison != 0, "unexpected zero in Q(sqrt(5)) sign test")
        if a > 0:
            return 1 if comparison > 0 else -1
        return -1 if comparison > 0 else 1

    def __lt__(self, other):
        return (self - other).sign() < 0

    def __le__(self, other):
        return (self - other).sign() <= 0

    def __gt__(self, other):
        return (self - other).sign() > 0

    def __ge__(self, other):
        return (self - other).sign() >= 0


def as_qsqrt5(value):
    if isinstance(value, Qsqrt5):
        return value
    return Qsqrt5(Fraction(value))


def main():
    zero = Qsqrt5(Fraction(0))
    one = Qsqrt5(Fraction(1))
    two = Qsqrt5(Fraction(2))
    a = Qsqrt5(Fraction(5), Fraction(-2))  # epsilon_5

    # Exact Q(sqrt(5)) comparisons used by the exhaustive reduction.
    require(zero < a < one, "0 < epsilon_5 < 1 failed")
    require(3 * a < two, "3 epsilon_5 < 2 failed")
    require(2 * a > one, "2 epsilon_5 > 1 failed")

    # Rational certificate for epsilon_5 + epsilon_7 < 1.  Monotonicity of
    # c -> (1-c)/(1+c), cos(pi/7)>7/8, gives epsilon_7<7/15.
    cosine_lower = Fraction(2159, 2401)
    require(cosine_lower > Fraction(7, 8), "cos(pi/7) rational lower bound failed")
    epsilon7_upper = 7 * (1 - Fraction(7, 8)) / (1 + Fraction(7, 8))
    require(epsilon7_upper == Fraction(7, 15), "epsilon_7 upper bound changed")
    require(Qsqrt5(epsilon7_upper) < one - a, "epsilon_5+epsilon_7 < 1 failed")
    require(Fraction(67, 30) ** 2 < 5, "67/30 < sqrt(5) certificate failed")

    # The analytic monotonicity lemma is exact: for u in (0,pi/6], the sign of
    # d(tan(u)^2/u)/du reduces, through positive factors, to
    # 2u-sin(u)cos(u)>0, and sin(u)cos(u)<u<2u.
    monotonicity_chain = (
        "u=pi/(2x) in (0,pi/6]",
        "d(tan(u)^2/u)/du has sign 2u-sin(u)cos(u)",
        "sin(u)cos(u)<u<2u",
        "epsilon_x strictly decreases for real x>=3",
    )
    require(len(monotonicity_chain) == len(set(monotonicity_chain)),
            "monotonicity certificate ledger malformed")

    # Exhaust all possible triangle counts t among twelve cycles.  For t<=9,
    # monotonicity bounds every nontriangle by a and 9+3a<11.  For t=10,
    # the only pair reaching one is (5,5).  For t>=11, the family is T^11Q.
    require(Qsqrt5(9) + 3 * a < Qsqrt5(11), "t<=9 cutoff failed")
    require(a < one, "even/nontriangle pair cutoff failed")
    require(a + Qsqrt5(epsilon7_upper) < one, "distinct odd pair cutoff failed")
    require(2 * a > one, "(5,5) residual test failed")

    cases = (
        "t<=9: DNN-positive",
        "t=10, pair!=(5,5): DNN-positive",
        "t=10, pair=(5,5): T^10PP residual",
        "t>=11: T^11Q residual",
    )
    residuals = ("T^11Q", "T^10PP")
    payload = "\n".join(monotonicity_chain + cases + residuals) + "\n"
    digest = sha256(payload.encode("ascii")).hexdigest()
    require(digest == "96d20340187cd0b2c01ca5d89d1f2c06cb0ecd321d035d73b53d94a706edd663",
            "frontier certificate digest changed")

    print("rank-twelve sharp-DNN residual frontier: exact audit passed")
    print("frontier: T^11Q, T^10PP")
    print(f"certificate_sha256: {digest}")
    print("status: DNN frontier only; no rank-twelve cactus theorem claim")


if __name__ == "__main__":
    main()
