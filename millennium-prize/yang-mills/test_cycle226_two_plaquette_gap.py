#!/usr/bin/env python3
"""Tests for the two-plaquette shared-link cutoff Ritz certificate."""

import unittest
from fractions import Fraction

from verify_cycle226_two_plaquette_gap import (
    evaluate,
    shared_count_below,
    shared_eigenvalue_interval,
    shared_symmetric_polynomial,
    square_root_interval,
    subtract_intervals,
)


class Cycle226VerifierTests(unittest.TestCase):
    def test_lambda_one_characteristic_polynomial(self):
        polynomial = shared_symmetric_polynomial(Fraction(1))
        expected = tuple(map(Fraction, (4143, -4198, 1354, -176, 8)))
        self.assertEqual(tuple(8 * value for value in polynomial), expected)

    def test_antisymmetric_eigenvalue_is_five(self):
        self.assertEqual(shared_count_below(Fraction(5), Fraction(1)), 2)
        self.assertEqual(shared_count_below(Fraction(5001, 1000), Fraction(1)), 3)

    def test_cutoff_ritz_gap_differs_from_tensor_sum_compression(self):
        tolerance = Fraction(1, 10**10)
        spectrum = tuple(
            shared_eigenvalue_interval(index, Fraction(1), tolerance) for index in range(2)
        )
        gap = subtract_intervals(spectrum[1], spectrum[0])
        product_gap = square_root_interval(Fraction(10), tolerance)
        self.assertLess(gap[1], product_gap[0])
        benchmark = Fraction(31415115147, 10**10)
        self.assertLessEqual(gap[0], benchmark)
        self.assertGreaterEqual(gap[1], benchmark)

    def test_intervals_cross_the_exact_count(self):
        for index in range(2):
            lower, upper = shared_eigenvalue_interval(index, Fraction(1), Fraction(1, 10**9))
            self.assertLessEqual(shared_count_below(lower, Fraction(1)), index)
            self.assertGreater(shared_count_below(upper, Fraction(1)), index)

    def test_polynomial_has_expected_lambda_one_root_signs(self):
        polynomial = shared_symmetric_polynomial(Fraction(1))
        self.assertGreater(evaluate(polynomial, Fraction(18, 10)), 0)
        self.assertLess(evaluate(polynomial, Fraction(19, 10)), 0)


if __name__ == "__main__":
    unittest.main()
