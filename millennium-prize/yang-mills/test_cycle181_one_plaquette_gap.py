#!/usr/bin/env python3
"""Tests for the Cycle 181 finite-cutoff certificate; safe under python -O."""

import unittest
from fractions import Fraction

from verify_cycle181_one_plaquette_gap import (
    eigenvalue_interval,
    finite_matrix,
    half_line_count_bounds,
    half_line_low_spectrum,
    low_spectrum_intervals,
    sturm_count,
    subtract_intervals,
    tail_resolvent_bounds,
)


class Cycle181VerifierTests(unittest.TestCase):
    def test_zero_coupling_has_exact_diagonal_counts(self):
        diagonal, off_diagonal = finite_matrix(Fraction(0), 4)
        self.assertEqual(sturm_count(Fraction(0), diagonal, off_diagonal), 0)
        self.assertEqual(sturm_count(Fraction(1), diagonal, off_diagonal), 1)
        self.assertEqual(sturm_count(Fraction(3), diagonal, off_diagonal), 1)
        self.assertEqual(sturm_count(Fraction(4), diagonal, off_diagonal), 2)

    def test_intervals_certify_count_jump(self):
        diagonal, off_diagonal = finite_matrix(Fraction(1, 10), 8)
        for index in range(3):
            lower, upper = eigenvalue_interval(
                index, diagonal, off_diagonal, Fraction(1, 10**9)
            )
            self.assertLessEqual(upper - lower, Fraction(1, 10**9))
            self.assertLessEqual(sturm_count(lower, diagonal, off_diagonal), index)
            self.assertGreater(sturm_count(upper, diagonal, off_diagonal), index)

    def test_zero_coupling_gap_interval_contains_three(self):
        spectrum = low_spectrum_intervals(Fraction(0), 5, Fraction(1, 10**10))
        gap = subtract_intervals(spectrum[1], spectrum[0])
        self.assertLessEqual(gap[0], Fraction(3))
        self.assertGreaterEqual(gap[1], Fraction(3))

    def test_tail_resolvent_bounds_follow_operator_order(self):
        lower, upper = tail_resolvent_bounds(Fraction(2), Fraction(1), 3)
        self.assertEqual(lower, Fraction(1, 23))
        self.assertEqual(upper, Fraction(1, 22))

    def test_half_line_count_bounds_are_ordered(self):
        for point in (Fraction(0), Fraction(1), Fraction(3), Fraction(4)):
            lower, upper = half_line_count_bounds(point, Fraction(1), 8)
            self.assertLessEqual(lower, upper)

    def test_lambda_one_half_line_gap_is_certified(self):
        spectrum = half_line_low_spectrum(Fraction(1), 12, Fraction(1, 10**10))
        gap = subtract_intervals(spectrum[1], spectrum[0])
        benchmark = Fraction(311386381151, 10**11)
        self.assertLessEqual(gap[0], benchmark)
        self.assertGreaterEqual(gap[1], benchmark)
        self.assertGreater(gap[0], Fraction(3))
        self.assertLess(gap[1] - gap[0], Fraction(1, 10**8))

    def test_rejects_invalid_inputs_without_assert_statements(self):
        with self.assertRaises(ValueError):
            finite_matrix(Fraction(-1), 3)
        with self.assertRaises(ValueError):
            finite_matrix(Fraction(1), -1)
        diagonal, off_diagonal = finite_matrix(Fraction(1), 2)
        with self.assertRaises(ValueError):
            eigenvalue_interval(3, diagonal, off_diagonal)
        with self.assertRaises(ValueError):
            eigenvalue_interval(0, diagonal, off_diagonal, Fraction(0))
        with self.assertRaises(ValueError):
            tail_resolvent_bounds(Fraction(15), Fraction(1), 2)


if __name__ == "__main__":
    unittest.main()
