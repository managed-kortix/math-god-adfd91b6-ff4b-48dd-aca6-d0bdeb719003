#!/usr/bin/env python3
"""Exact check of the Cycle 204 terminal-receiver linear elimination."""

from fractions import Fraction as F


def rows(terminal, pump, vertical, pump_coefficient, epsilon, delta):
    terminal = F(terminal)
    pump = F(pump)
    vertical = F(vertical)
    coefficient = F(pump_coefficient)

    # Coordinates of w for unit a and unit b, respectively.
    w_a = (
        coefficient * vertical**2,
        coefficient * epsilon * delta * vertical * (pump - terminal),
        F(0),
    )
    w_b = (F(0), F(0), coefficient * delta * vertical)
    tangent = (-delta * vertical, epsilon * (terminal + pump), F(0))

    dot_a = sum(x * y for x, y in zip(tangent, w_a))
    dot_b = sum(x * y for x, y in zip(tangent, w_b))
    e3_a = w_a[2]
    e3_b = w_b[2]

    expected_a = (
        -coefficient
        * delta
        * vertical
        * (vertical**2 + terminal**2 - pump**2)
    )
    assert (dot_a, dot_b) == (expected_a, F(0))
    assert (e3_a, e3_b) == (F(0), coefficient * delta * vertical)
    return expected_a, e3_b


def main():
    terminal, pump, vertical = 8, 6, 1
    determinant = F(1)
    for epsilon in (-1, 1):
        for delta in (-1, 1):
            diagonal = rows(terminal, pump, vertical, 1, epsilon, delta)
            determinant *= diagonal[0] * diagonal[1]

    assert vertical**2 + terminal**2 - pump**2 == 29
    assert determinant != 0
    print("Cycle 204 exact terminal-receiver elimination")
    print("nontrivial scalar: 29")
    print("eight-by-eight determinant:", determinant)
    print("all eight terminal derivative variables vanish")
    print("nonzero terminal normalization is contradictory")


if __name__ == "__main__":
    main()
