#!/usr/bin/env python3
"""Tests for exact harmonic completions and approximate mode diagnostics."""

import importlib.util
import math
import unittest

from verify_harmonic_completions import (
    Polynomial, compare_low_modes, completed_polynomial_moments,
    convolution_residual, cumulative_convolution_residual,
    direct_cumulative_convolution_residual,
    direct_convolution_residual, direct_harmonic_completion,
    generalized_von_mangoldt, harmonic_completion, verify_exact_identities,
)


class ExactHarmonicCompletionTests(unittest.TestCase):
    def test_degrees_zero_through_three_are_formally_exact(self):
        result = verify_exact_identities(80, cutoffs=(0, 1, 3, 8, 20))
        self.assertEqual(result.completion_checks, 4 * 80)
        self.assertEqual(result.residual_checks, 4 * 80 * 5)
        self.assertEqual(result.cumulative_checks, 4 * 80 * 5)

    def test_completion_examples_include_prime_power_log_relations(self):
        L = Polynomial.variable("L")
        for n in (1, 2, 4, 6, 12, 30):
            for degree in range(4):
                self.assertEqual(
                    harmonic_completion(degree, n, L),
                    direct_harmonic_completion(degree, n, L),
                )
        self.assertEqual(generalized_von_mangoldt(1, 0), Polynomial.constant(1))
        self.assertEqual(generalized_von_mangoldt(6, 0), Polynomial.constant(0))

    def test_residual_is_exact_for_edge_cutoffs(self):
        for degree in range(4):
            for n in range(1, 33):
                for cutoff in (0, 1, n // 2, n, n + 1):
                    self.assertEqual(
                        convolution_residual(degree, n, cutoff),
                        direct_convolution_residual(degree, n, cutoff),
                    )
                    self.assertEqual(
                        cumulative_convolution_residual(degree, n, cutoff),
                        direct_cumulative_convolution_residual(degree, n, cutoff),
                    )

    def test_numerical_completed_moments_only_have_roundoff_residual(self):
        moments, discrepancies = completed_polynomial_moments(32)
        self.assertEqual(len(moments), 4)
        self.assertTrue(all(abs(value) < 2e-12 for value in discrepancies))

    def test_validation(self):
        with self.assertRaises(ValueError):
            harmonic_completion(4, 2)
        with self.assertRaises(ValueError):
            generalized_von_mangoldt(2, -1)
        with self.assertRaises(ValueError):
            convolution_residual(1, 2, -1)
        with self.assertRaises(ValueError):
            verify_exact_identities(0)


@unittest.skipUnless(
    importlib.util.find_spec("numpy") and importlib.util.find_spec("scipy"),
    "optional numpy/scipy numerical stack is unavailable",
)
class NumericalModeComparisonTests(unittest.TestCase):
    def test_low_modes_are_finite_and_continuum_projection_tracks_discrete_mode(self):
        comparisons = compare_low_modes(128, modes=3)
        self.assertEqual(len(comparisons), 3)
        for item in comparisons:
            values = (
                item.beta, item.eigenvalue, item.modal_projection,
                item.mellin_projection, item.mellin_minus_modal,
                *item.completed_polynomial_projections, *item.completion_roundoff,
            )
            self.assertTrue(all(math.isfinite(value) for value in values))
            self.assertGreater(item.beta, 0)
            self.assertGreater(item.eigenvalue, 0)
            self.assertLess(abs(item.mellin_minus_modal), 0.03)
            self.assertTrue(all(abs(value) < 2e-10 for value in item.completion_roundoff))

    def test_numerical_validation(self):
        with self.assertRaises(ValueError):
            compare_low_modes(1)
        with self.assertRaises(ValueError):
            compare_low_modes(4, 5)


if __name__ == "__main__":
    unittest.main()
