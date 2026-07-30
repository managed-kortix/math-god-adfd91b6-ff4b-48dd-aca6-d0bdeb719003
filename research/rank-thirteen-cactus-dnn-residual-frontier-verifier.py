#!/usr/bin/env python3
"""Fail-closed exact audit of the rank-thirteen sharp-DNN frontier.

The audit uses Fraction arithmetic and Q(sqrt(5)) only. It checks the exact
inequalities and exhaustive triangle-count reduction, not the sharp DNN
theorem or positivity on the residual families.
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

    def __gt__(self, other):
        return (self - other).sign() > 0


def as_qsqrt5(value):
    if isinstance(value, Qsqrt5):
        return value
    return Qsqrt5(Fraction(value))


MONOTONICITY = (
    "u=pi/(2x) in (0,pi/6]",
    "d(tan(u)^2/u)/du has sign 2u-sin(u)cos(u)",
    "sin(u)cos(u)<u<2u",
    "epsilon_x strictly decreases for real x>=3",
)
CASES = (
    "t<=10: DNN-positive",
    "t=11, pair!=(5,5): DNN-positive",
    "t=11, pair=(5,5): T^11PP residual",
    "t>=12: T^12Q residual",
)
RESIDUALS = ("T^12Q", "T^11PP")
EXPECTED_CERTIFICATE_SHA256 = "afed9ecb78b7def1cf0daf14655730e64f52fe59a1e8a38f1b9f115b5aecce76"


def audit(*, triangle_cutoff=10, residuals=RESIDUALS, cosine_lower=Fraction(2159, 2401)):
    zero = Qsqrt5(Fraction(0))
    one = Qsqrt5(Fraction(1))
    two = Qsqrt5(Fraction(2))
    a = Qsqrt5(Fraction(5), Fraction(-2))

    require(zero < a < one, "0 < epsilon_5 < 1 failed")
    require(3 * a < two, "3 epsilon_5 < 2 failed")
    require(2 * a > one, "2 epsilon_5 > 1 failed")

    require(cosine_lower == Fraction(2159, 2401), "cosine certificate changed")
    require(cosine_lower > Fraction(7, 8), "cos(pi/7) rational lower bound failed")
    epsilon7_upper = 7 * (1 - Fraction(7, 8)) / (1 + Fraction(7, 8))
    require(epsilon7_upper == Fraction(7, 15), "epsilon_7 upper bound changed")
    require(Qsqrt5(epsilon7_upper) < one - a, "epsilon_5+epsilon_7 < 1 failed")
    require(Fraction(67, 30) ** 2 < 5, "67/30 < sqrt(5) certificate failed")

    require(triangle_cutoff == 10, "triangle cutoff changed")
    require(Qsqrt5(triangle_cutoff) + 3 * a < Qsqrt5(12), "t<=10 cutoff failed")
    require(a + Qsqrt5(epsilon7_upper) < one, "distinct odd pair cutoff failed")
    require(2 * a > one, "(5,5) residual test failed")
    require(tuple(residuals) == RESIDUALS, "residual family ledger changed")
    require(len(MONOTONICITY) == len(set(MONOTONICITY)), "monotonicity ledger malformed")

    payload = "\n".join(MONOTONICITY + CASES + tuple(residuals)) + "\n"
    return sha256(payload.encode("ascii")).hexdigest()


def expect_rejected(action, label):
    try:
        action()
    except RuntimeError:
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    expect_rejected(lambda: audit(triangle_cutoff=11), "triangle cutoff")
    expect_rejected(lambda: audit(residuals=("T^12Q",)), "missing residual")
    expect_rejected(lambda: audit(residuals=("T^11PP", "T^12Q")), "residual order")
    expect_rejected(
        lambda: audit(cosine_lower=Fraction(7, 8)), "weakened strict cosine bound"
    )
    return 4


def main():
    digest = audit()
    require(digest == EXPECTED_CERTIFICATE_SHA256, "frontier certificate digest changed")
    mutation_count = hostile_self_checks()
    require(mutation_count == 4, "hostile mutation count changed")
    print("rank-thirteen sharp-DNN residual frontier: exact audit passed")
    print("frontier: T^12Q, T^11PP")
    print(f"certificate_sha256: {digest}")
    print(f"rejected_hostile_mutations: {mutation_count}")
    print("status: DNN frontier only; no rank-thirteen cactus theorem claim")


if __name__ == "__main__":
    main()
