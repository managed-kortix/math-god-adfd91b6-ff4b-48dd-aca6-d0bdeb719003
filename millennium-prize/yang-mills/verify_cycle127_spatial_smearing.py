#!/usr/bin/env python3
"""Exact, dependency-free verifier for Cycle 127 spatial smearing constants."""

from fractions import Fraction


class Monomial:
    """A rational coefficient times powers of pi, sigma, and a_tau."""

    SYMBOLS = ("pi", "sigma", "a_tau")

    def __init__(self, coefficient=1, **powers):
        self.coefficient = Fraction(coefficient)
        self.powers = {
            symbol: Fraction(powers.get(symbol, 0)) for symbol in self.SYMBOLS
        }

    def __mul__(self, other):
        if not isinstance(other, Monomial):
            other = Monomial(other)
        return Monomial(
            self.coefficient * other.coefficient,
            **{
                symbol: self.powers[symbol] + other.powers[symbol]
                for symbol in self.SYMBOLS
            },
        )

    __rmul__ = __mul__

    def __pow__(self, exponent):
        exponent = Fraction(exponent)
        if exponent.denominator != 1 and self.coefficient != 1:
            raise ValueError("fractional powers of rational coefficients are not canonical")
        return Monomial(
            self.coefficient ** exponent.numerator,
            **{symbol: power * exponent for symbol, power in self.powers.items()},
        )

    def __neg__(self):
        return Monomial(-self.coefficient, **self.powers)

    def __eq__(self, other):
        return (
            isinstance(other, Monomial)
            and self.coefficient == other.coefficient
            and self.powers == other.powers
        )

    def canonical(self):
        powers = ", ".join(
            f"{symbol}^{power}" for symbol, power in self.powers.items() if power
        )
        return f"coefficient={self.coefficient}" + (f"; {powers}" if powers else "")


ONE = Monomial()
PI = Monomial(pi=1)
SIGMA = Monomial(sigma=1)
A_TAU = Monomial(a_tau=1)


def gamma_exact(argument):
    """Return Gamma(argument) for a positive integer or half-integer exactly."""
    argument = Fraction(argument)
    if argument <= 0 or argument.denominator not in (1, 2):
        raise ValueError("expected a positive integer or half-integer")

    if argument.denominator == 1:
        result = ONE
        for factor in range(1, argument.numerator):
            result *= factor
        return result

    result = PI ** Fraction(1, 2)  # Gamma(1/2) = sqrt(pi)
    current = Fraction(1, 2)
    while current < argument:
        result *= current           # Gamma(x + 1) = x Gamma(x)
        current += 1
    return result


def radial_gaussian(moment):
    r"""Return integral d^3p/(2 pi)^3 p^moment exp(-sigma p^2)."""
    moment = Fraction(moment)
    gamma_argument = (moment + 3) / 2
    # 4 pi/(2 pi)^3 * (1/2) sigma^(-gamma_argument)
    return Fraction(1, 4) * PI ** -2 * gamma_exact(gamma_argument) * (
        SIGMA ** -gamma_argument
    )


def check(label, actual, expected):
    if actual != expected:
        raise AssertionError(
            f"{label}:\n  actual:   {actual.canonical()}\n"
            f"  expected: {expected.canonical()}"
        )
    print(f"PASS: {label}")
    print(f"      canonical identity: {actual.canonical()}")


def main():
    print("Cycle 127 exact spatial-smearing verifier (no floating point)\n")

    print("Gaussian reduction:")
    print("  Integral[d^3p/(2 pi)^3 p^m exp(-sigma p^2)]")
    print("    = Gamma((m+3)/2) / (4 pi^2 sigma^((m+3)/2)).")
    print("  Gamma(3/2) = (1/2) Gamma(1/2) = sqrt(pi)/2.")
    gaussian = radial_gaussian(0)
    gaussian_expected = Fraction(1, 8) * PI ** Fraction(-3, 2) * SIGMA ** Fraction(-3, 2)
    check("m=0 Gaussian = 1/(4 pi sigma)^(3/2)", gaussian, gaussian_expected)

    print("\nTransverse contact term:")
    print("  tr(P_T) = 2, so the Gaussian coefficient is multiplied by 2.")
    contact = 2 * gaussian
    contact_expected = Fraction(1, 4) * PI ** Fraction(-3, 2) * SIGMA ** Fraction(-3, 2)
    check("contact = 2/(4 pi sigma)^(3/2)", contact, contact_expected)

    print("\nSmooth term at tau=0:")
    print("  tr[P_T] times -(p/2) leaves -p under the spatial integral.")
    print("  Gamma(2) = 1, hence -Integral[p exp(-sigma p^2)] is exact.")
    smooth = -radial_gaussian(1)
    smooth_expected = -Fraction(1, 4) * PI ** -2 * SIGMA ** -2
    check("smooth(0) = -1/(4 pi^2 sigma^2)", smooth, smooth_expected)

    print("\nTemporal lattice scaling:")
    print("  delta(tau) maps exactly to delta[n,0]/a_tau.")
    lattice_contact = contact * A_TAU ** -1
    lattice_expected = (
        Fraction(1, 4)
        * PI ** Fraction(-3, 2)
        * SIGMA ** Fraction(-3, 2)
        * A_TAU ** -1
    )
    check("zero-slice contact = contact/a_tau", lattice_contact, lattice_expected)

    print("\nAll exact identities verified using Fraction exponents; no floats used.")


if __name__ == "__main__":
    main()
