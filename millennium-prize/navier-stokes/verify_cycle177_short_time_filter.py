#!/usr/bin/env python3
"""Exact Laurent/Taylor certificate for the Cycle 177 obstruction."""

from collections import defaultdict
from fractions import Fraction as F


def add(*polynomials):
    result = defaultdict(F)
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] += coefficient
    return {
        exponent: coefficient
        for exponent, coefficient in result.items()
        if coefficient
    }


def scale(value, polynomial):
    return {
        exponent: value * coefficient
        for exponent, coefficient in polynomial.items()
        if value * coefficient
    }


def product(left, right):
    result = defaultdict(F)
    for x, a in left.items():
        for y, b in right.items():
            result[x + y] += a * b
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def derivative(polynomial, order=1):
    return {
        exponent: coefficient * exponent**order
        for exponent, coefficient in polynomial.items()
        if coefficient * exponent**order
    }


def a_polynomial(radius):
    return {-radius: F(1), radius: F(-1)}


def h_polynomial(radius, multiplier):
    return {
        (2 * index - multiplier + 1) * radius: F(1)
        for index in range(multiplier)
    }


def main():
    # R=Y=nu=1, multipliers (2, 4), rail factors {0}, pump factors {1}.
    rail = product(a_polynomial(1), h_polynomial(1, 2))
    pump = h_polynomial(2, 4)
    collision = product(pump, rail)
    assert rail == {-2: F(1), 2: F(-1)}
    assert pump == {-6: F(1), -2: F(1), 2: F(1), 6: F(1)}
    assert collision == a_polynomial(8)

    # Real and imaginary parts of C'(0) from equation (6), with Y=nu=1.
    viscous = scale(
        F(-1),
        add(
            product(derivative(pump, 2), rail),
            product(pump, derivative(rail, 2)),
            collision,
        ),
    )
    nonlinear_imaginary = scale(F(-1), product(pump, collision))

    assert viscous.get(4, F(0)) == -32
    assert nonlinear_imaginary.get(4, F(0)) == 0
    assert viscous.get(6, F(0)) == 0
    assert nonlinear_imaginary.get(6, F(0)) == 1

    # For absent rails with C_r(0)=0, F_r''(0)=-i C_r'(0).
    # Store Gaussian-rational values as (real, imaginary).
    second_derivative_4 = (
        nonlinear_imaginary.get(4, F(0)),
        -viscous.get(4, F(0)),
    )
    second_derivative_6 = (
        nonlinear_imaginary.get(6, F(0)),
        -viscous.get(6, F(0)),
    )
    assert second_derivative_4 == (F(0), F(32))
    assert second_derivative_6 == (F(1), F(0))

    print("Cycle 177 exact short-time Laurent filter")
    print("F*G support:", collision)
    print("C'_4(0): -32")
    print("C'_6(0): i")
    print("F_4(t): 16 i t^2 + O(t^3)")
    print("F_6(t): (1/2) t^2 + O(t^3)")
    print("all exact Laurent and Taylor checks passed")


if __name__ == "__main__":
    main()
