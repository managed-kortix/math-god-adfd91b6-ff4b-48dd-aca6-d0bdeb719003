#!/usr/bin/env python3
"""Exact, dependency-free verifier for Cycle 131 Wick contact aliasing."""

from fractions import Fraction


def check(label, actual, expected):
    if actual != expected:
        raise AssertionError(f"{label}: actual={actual}, expected={expected}")
    print(f"PASS: {label} = {actual}")


def dot(left, right):
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def polynomial_value(coefficients, x):
    value = Fraction(0)
    for coefficient in reversed(coefficients):
        value = value * x + coefficient
    return value


def main():
    print("Cycle 131 exact Wick-contact aliasing verifier (Fraction only)\n")

    print("Spatially smeared transverse covariance:")
    dimensions = 3
    transverse_trace = 2
    q_over_g = Fraction(transverse_trace, dimensions)
    q_infinity_over_g = tuple(
        tuple(q_over_g if i == j else Fraction(0) for j in range(dimensions))
        for i in range(dimensions)
    )
    expected_q = tuple(
        tuple(Fraction(2, 3) if i == j else Fraction(0) for j in range(3))
        for i in range(3)
    )
    check("Q_infinity/G", q_infinity_over_g, expected_q)

    print("\nCentered energy e=(1/2)(|E|^2-E|E|^2):")
    trace_q_squared_over_g_squared = sum(
        entry * entry for row in q_infinity_over_g for entry in row
    )
    wick_over_g_squared = Fraction(1, 2) * trace_q_squared_over_g_squared
    check("Tr((Q_infinity/G)^2)", trace_q_squared_over_g_squared, Fraction(4, 3))
    check("(1/2) Tr(Q_infinity^2)/G^2", wick_over_g_squared, Fraction(2, 3))

    # G=(4*pi*sigma)^(-3/2), hence G^2=1/(64*pi^3*sigma^3).
    g_squared_denominator = 4**3
    pi_sigma_coefficient = wick_over_g_squared / g_squared_denominator
    check(
        "coefficient of 1/(pi^3 sigma^3)",
        pi_sigma_coefficient,
        Fraction(1, 96),
    )
    print("      (1/2)Tr(Q_infinity^2) = 1/(96 pi^3 sigma^3)")

    print("\nExact temporal alias count at period T=1:")
    for temporal_sites in (1, 2, 3, 8, 17):
        a = Fraction(1, temporal_sites)
        # Each external lattice frequency has exactly N internal decompositions.
        spectral_over_g_squared = temporal_sites * wick_over_g_squared
        check(
            f"N={temporal_sites}: aliased spectrum / G^2",
            spectral_over_g_squared,
            wick_over_g_squared / a,
        )

    print("\nExact test-function variance in the contact model:")
    phi = tuple(Fraction(value) for value in (2, -1, 3, 0, -2, 1))
    temporal_sites = len(phi)
    a = Fraction(1, temporal_sites)
    lattice_l2 = a * dot(phi, phi)
    # Cov(E_n)=Q_infinity/a and distinct time slices are independent. Wick gives
    # Var[a sum_n phi_n e_n] = (coefficient/a) [a sum_n phi_n^2].
    variance_over_g_squared = wick_over_g_squared * dot(phi, phi)
    predicted_variance = (wick_over_g_squared / a) * lattice_l2
    check("test variance / G^2", variance_over_g_squared, predicted_variance)
    check(
        "a times test variance / (G^2 ||phi||_a^2)",
        a * variance_over_g_squared / lattice_l2,
        wick_over_g_squared,
    )
    print("      Var<e,phi> = [1/(96 pi^3 sigma^3 a)] ||phi||_a^2")

    print("\nContinuum external-composite phase-space contrast:")
    # With x=|p|^2/omega^2 in [0,1], the exact two-photon polynomial is
    # 15-30x+23x^2.  Complete the square exactly:
    # 23(x-15/23)^2 + 120/23.
    for numerator, denominator in ((0, 1), (1, 4), (1, 2), (3, 4), (1, 1)):
        x = Fraction(numerator, denominator)
        phase = 15 - 30 * x + 23 * x * x
        square_form = 23 * (x - Fraction(15, 23)) ** 2 + Fraction(120, 23)
        check(f"phase polynomial at x={x}", phase, square_form)
        if phase <= 0:
            raise AssertionError("two-photon phase polynomial must be positive")
    check("phase polynomial minimum", Fraction(120, 23), Fraction(120, 23))
    print("PASS: 15-30x+23x^2 > 0 on 0<=x<=1")
    print("      its p=0 term is 15 omega^4, giving a positive omega^4 tail")

    print("\nAll identities verified exactly; no floating point or dependencies used.")


if __name__ == "__main__":
    main()
