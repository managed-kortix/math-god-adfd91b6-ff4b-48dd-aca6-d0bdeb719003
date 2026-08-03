#!/usr/bin/env python3
"""Exact rational replay of the Cycle 272 short-time manifest."""

import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


def frac(value):
    return Fraction(value)


def kappa_upper(q, power, bound):
    n = 1
    while Fraction((n + 1) ** power, n ** power) > q:
        n += 1
    maximum = Fraction(n ** power) / q ** n
    return maximum < bound


def main():
    with (HERE / "cycle272-short-time-manifest.json").open(encoding="ascii") as handle:
        manifest = json.load(handle)

    initial = manifest["initial_intervals"]
    assert frac(initial["L_prime_0"][0]) == Fraction(297, 1_000_000)
    assert frac(initial["L_prime_0"][1]) == Fraction(474, 1_000_000)
    assert frac(initial["L_double_prime_0"][0]) == 3
    assert frac(initial["L_double_prime_0"][1]) == 4
    assert Fraction(15262, 3 * 17090032) > Fraction(297, 1_000_000)

    slab = manifest["analytic_slab"]
    q = frac(slab["Q"])
    assert kappa_upper(q, 1, 18)
    assert kappa_upper(q, 2, 1164)
    assert kappa_upper(q, 3, 133868)

    u = Fraction(600)
    u1 = Fraction(6480000)
    u2 = Fraction(391392000000)
    u3 = Fraction(46322668800000000)
    c_lower = frac(slab["C_lower_bound"])
    c1 = 3 * u * u * u1
    c2 = 6 * u * u1 * u1 + 3 * u * u * u2
    c3 = 12 * u1 ** 3 + 18 * u * u1 * u2 + 3 * u * u * u3
    l3 = c3 / (3 * c_lower) + c1 * c2 / c_lower ** 2
    l3 += 2 * c1 ** 3 / (3 * c_lower ** 3)
    assert c1 == 6998400000000
    assert c2 == 573868800000000000
    assert c3 < 82643000000000000000000
    assert l3 < 62000000000000000

    growth = manifest["certified_short_time_growth"]
    t = frac(growth["t_star"])
    lower = Fraction(297, 1_000_000) * t + Fraction(3, 2) * t ** 2
    lower -= Fraction(62000000000000000, 6) * t ** 3
    derivative_lower = Fraction(297, 1_000_000) + 3 * t
    derivative_lower -= Fraction(62000000000000000, 2) * t ** 2
    assert lower == frac(growth["exact_lower_value"])
    assert lower > frac(growth["simplified_strict_lower_bound"])
    assert derivative_lower == frac(growth["positive_derivative_lower_bound_at_t_star"])
    assert derivative_lower > 0

    factor_two = manifest["factor_two_audit"]
    displacement = Fraction(6480000, 65536)
    relative = displacement / 257
    log_upper = relative / (1 - relative)
    assert displacement == frac(factor_two["L3_norm_displacement_at_T"])
    assert relative == frac(factor_two["relative_displacement_bound"])
    assert log_upper == frac(factor_two["absolute_log_change_upper_bound"])
    assert log_upper == Fraction(50625, 80959)
    assert log_upper < Fraction(2, 3)
    assert factor_two["factor_two_excluded_on_frozen_interval"] is True

    print("Cycle 272 exact short-time replay: PASS")


if __name__ == "__main__":
    main()
