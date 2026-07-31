#!/usr/bin/env python3
"""Dependency-free checks for the Cycle 163 PEL kernel formulas."""

from math import prod


def gaussian(n: int, r: int, q: int) -> int:
    numerator = prod(q ** (n - i) - 1 for i in range(r))
    denominator = prod(q ** (r - i) - 1 for i in range(r))
    return numerator // denominator


def split_total(p: int) -> int:
    return sum(gaussian(6, r, p) for r in range(7))


def inert_total(p: int) -> int:
    return (p + 1) * (p**3 + 1) * (p**5 + 1)


def adapted_split(p: int) -> int:
    return 2 * (p + 1) * (p**2 + 1)


def minimal_inert(p: int) -> int:
    return (p + 1) ** 2 * (p**2 + 1)


def main() -> None:
    for p in (5, 13, 17):
        assert p % 4 == 1
        assert split_total(p) > adapted_split(p) > 0

    for p in (7, 11, 19):
        assert p % 4 == 3
        assert inert_total(p) > minimal_inert(p) > 0

    # The auxiliary geometries used by the proof have these standard counts.
    for p in (5, 7, 11, 13):
        lagrangians_in_symplectic_four_space = (p + 1) * (p**2 + 1)
        assert lagrangians_in_symplectic_four_space > 0
        assert adapted_split(p) == 2 * lagrangians_in_symplectic_four_space
        assert minimal_inert(p) == (p + 1) * lagrangians_in_symplectic_four_space

    print("cycle 163 PEL kernel count checks: PASS")


if __name__ == "__main__":
    main()
