#!/usr/bin/env python3
"""Exact certificate for the Cycle 92 seed-fixing quantifier obstruction."""

from fractions import Fraction
from itertools import product


def main() -> None:
    inputs = list(product((0, 1), repeat=3))
    success = {}
    failures = {}
    for x in inputs:
        answer = int(sum(x) >= 2)
        success[x] = Fraction(sum(bit == answer for bit in x), 3)
    for coordinate in range(3):
        failures[coordinate] = [
            x for x in inputs if x[coordinate] != int(sum(x) >= 2)
        ]

    assert min(success.values()) == Fraction(2, 3)
    assert all(len(witnesses) == 2 for witnesses in failures.values())
    assert all(any(x == tuple(int(i == j) for i in range(3))
                   for x in failures[j]) for j in range(3))

    print("minimum randomized success: 2/3")
    for coordinate, witnesses in failures.items():
        print(f"fixed coordinate {coordinate} fails on {witnesses}")


if __name__ == "__main__":
    main()
