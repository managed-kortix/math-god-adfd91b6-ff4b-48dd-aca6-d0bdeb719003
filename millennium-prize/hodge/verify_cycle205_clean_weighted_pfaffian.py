#!/usr/bin/env python3
"""Exact certificate for clean effective coordinate-weight Pfaffian cubics."""

from itertools import product


def scalar_coefficient(weights):
    total = sum(weights) // 2
    assert 2 * total == sum(weights)
    numerator = (
        sum(weight**3 for weight in weights)
        - sum((total - weight) ** 3 for weight in weights)
        + total**3
    )
    assert numerator % 6 == 0
    return numerator // 6


def xxy_coefficient(left, right):
    left_total = sum(left) // 2
    right_total = sum(right) // 2
    numerator = (
        sum(left[i] ** 2 * right[i] for i in range(5))
        - sum(
            (left_total - left[i]) ** 2 * (right_total - right[i])
            for i in range(5)
        )
        + left_total**2 * right_total
    )
    assert numerator % 2 == 0
    return numerator // 2


def xyz_coefficient(x_weights, y_weights, z_weights):
    totals = tuple(sum(weights) // 2 for weights in (x_weights, y_weights, z_weights))
    return (
        sum(x_weights[i] * y_weights[i] * z_weights[i] for i in range(5))
        - sum(
            (totals[0] - x_weights[i])
            * (totals[1] - y_weights[i])
            * (totals[2] - z_weights[i])
            for i in range(5)
        )
        + totals[0] * totals[1] * totals[2]
    )


def effective(weights):
    if sum(weights) % 2:
        return False
    total = sum(weights) // 2
    return all(
        total - weights[i] - weights[j] >= 0
        for i in range(5)
        for j in range(i + 1, 5)
    )


def zero_ray(weights):
    positive = [weight for weight in weights if weight]
    return not positive or (len(positive) == 4 and len(set(positive)) == 1)


def positive_normal_form(p, q, r, z, u):
    return (
        p**2 * q + 2 * p**2 * r + p**2 * z + 2 * p**2 * u
        + 3 * p * q**2 + 10 * p * q * r + 5 * p * q * z + 9 * p * q * u
        + 8 * p * r**2 + 8 * p * r * z + 14 * p * r * u
        + 2 * p * z**2 + 7 * p * z * u + 6 * p * u**2
        + 2 * q**3 + 10 * q**2 * r + 5 * q**2 * z + 9 * q**2 * u
        + 16 * q * r**2 + 16 * q * r * z + 28 * q * r * u
        + 4 * q * z**2 + 14 * q * z * u + 12 * q * u**2
        + 8 * r**3 + 12 * r**2 * z + 21 * r**2 * u
        + 6 * r * z**2 + 21 * r * z * u + 18 * r * u**2
        + z**3 + 5 * z**2 * u + 9 * z * u**2 + 5 * u**3
    )


def check_positive_normal_form():
    checked = 0
    for p, q, r, z, u in product(range(4), repeat=5):
        x = q + 2 * r + z + 2 * u
        weights = (x, x + p, x + p + q, x + p + q + r, x + p + q + r + z)
        assert effective(weights)
        assert scalar_coefficient(weights) == positive_normal_form(p, q, r, z, u)
        checked += 1
    return checked


def bounded_zero_ray_check(max_sum):
    checked = 0
    for weights in product(range(max_sum // 2 + 1), repeat=5):
        if sum(weights) > max_sum or not effective(weights):
            continue
        checked += 1
        assert (scalar_coefficient(weights) == 0) == zero_ray(weights)
    return checked


def main():
    # The note gives an all-weight positive-polynomial proof. This finite search
    # independently checks the classification through a substantial bound.
    normal_form_checks = check_positive_normal_form()
    checked = bounded_zero_ray_check(30)

    rays = [tuple(0 if i == missing else 1 for i in range(5)) for missing in range(5)]
    for i, left in enumerate(rays):
        assert scalar_coefficient(left) == 0
        for j, right in enumerate(rays):
            expected = 0 if i == j else 1
            assert xxy_coefficient(left, right) == expected
            assert xxy_coefficient(right, left) == expected
            for k, third in enumerate(rays):
                if i == j and j == k:
                    assert xyz_coefficient(left, right, third) == 0

    print("positive normal-form evaluations:", normal_form_checks)
    print("effective scalar vectors checked through total 30:", checked)
    print("zero-pure-cubic vectors: exactly multiples of permutations of (0,1,1,1,1)")
    print("distinct zero rays create contaminating pair-mixed cubics")
    print("one zero ray has zero XYZ coefficient")
    print("no clean effective coordinate-weight identity C(N)=kXYZ for nonzero k")
    print("all Cycle 205 exact checks passed")


if __name__ == "__main__":
    main()
