#!/usr/bin/env python3
"""Verify the universal C4 x S3 orbit count used in Cycle 243."""

from fractions import Fraction
from itertools import permutations, product


PERMS = tuple(permutations(range(3)))


def cycles(perm):
    seen = set()
    lengths = []
    for start in range(3):
        if start in seen:
            continue
        cur = start
        length = 0
        while cur not in seen:
            seen.add(cur)
            length += 1
            cur = perm[cur]
        lengths.append(length)
    return lengths


def burnside_count(n):
    total = 0
    for order in (1, 2, 4, 4):
        for perm in PERMS:
            fixed = 1
            for length in cycles(perm):
                if length % order == 0:
                    fixed *= n
            total += fixed
    result = Fraction(total, 24)
    if result.denominator != 1:
        raise AssertionError("Burnside average is not integral")
    return result.numerator


def act(triple, unit, perm, modulus):
    return tuple((unit * triple[perm[index]]) % modulus for index in range(3))


def brute_count_prime_alphabet(prime):
    # This finite analogue uses all of F_p as the matrix alphabet and its four
    # scalar units. It checks the same cycle calculation for p == 1 mod 4.
    root_i = next(x for x in range(prime) if x * x % prime == prime - 1)
    units = (1, prime - 1, root_i, (-root_i) % prime)
    points = tuple(product(range(prime), repeat=3))
    orbits = set()
    for point in points:
        orbit = tuple(
            sorted(act(point, unit, perm, prime) for unit in units for perm in PERMS)
        )
        orbits.add(orbit)
    expected = burnside_count(prime)
    if len(orbits) != expected:
        raise AssertionError((prime, len(orbits), expected))
    return expected


def main():
    n = 5**18
    expected = (n**3 + 3 * n**2 + 5 * n + 15) // 24
    if burnside_count(n) != expected:
        raise AssertionError("closed formula mismatch")
    small = {prime: brute_count_prime_alphabet(prime) for prime in (5, 13)}
    print("cycle243 F242 symmetry: PASS")
    print(f"matrix alphabet size n = 5^18 = {n}")
    print(f"C4 x S3 orbit count = {expected}")
    print(f"finite-field analogues = {small}")


if __name__ == "__main__":
    main()
