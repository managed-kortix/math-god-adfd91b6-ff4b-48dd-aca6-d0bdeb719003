#!/usr/bin/env python3
"""Exact rational audit of generic dyadic floor-transform claims."""

from fractions import Fraction


def dot(left, right):
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def weighted_dot(left, right, weights):
    return sum((w * x * y for w, x, y in zip(weights, left, right)), Fraction(0))


def certificate(N):
    if N < 2:
        raise ValueError("the normalized Z_N transform requires N >= 2")
    weights = tuple(Fraction(1, k * (k + 1)) for k in range(N, 2 * N))
    old = tuple(Fraction(k) for k in range(N, 2 * N))
    if N == 2:
        increment = tuple(Fraction(k // 2, 2) for k in range(N, 2 * N))
    else:
        increment = None
    if increment is None:
        return {"N": N, "rational_power_taper_certificate": False}
    old_norm = weighted_dot(old, old, weights)
    cross = weighted_dot(old, increment, weights)
    increment_norm = weighted_dot(increment, increment, weights)
    difference = (
        (Fraction(0), -cross),
        (-cross, -increment_norm),
    )
    determinant = difference[0][0] * difference[1][1] - difference[0][1] ** 2
    values = {}
    fine_norms = {}
    for sign in (Fraction(1), Fraction(-1)):
        vector = (Fraction(1), sign)
        values[sign] = dot(vector, tuple(dot(row, vector) for row in difference))
        fine = tuple(x + sign * y for x, y in zip(old, increment))
        fine_norms[sign] = weighted_dot(fine, fine, weights)
    return {
        "N": N,
        "weights": weights,
        "old": old,
        "increment": increment,
        "old_norm": old_norm,
        "cross": cross,
        "increment_norm": increment_norm,
        "difference": difference,
        "determinant": determinant,
        "values": values,
        "fine_norms": fine_norms,
    }


def main():
    item = certificate(2)
    assert item["determinant"] < 0
    assert item["values"][Fraction(1)] < 0 < item["values"][Fraction(-1)]
    print("minimal admissible certificate")
    for key, value in item.items():
        print(f"{key} = {value}")


if __name__ == "__main__":
    main()
