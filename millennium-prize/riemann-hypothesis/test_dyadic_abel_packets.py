#!/usr/bin/env python3
"""Tests for consecutive-scale Abel packet certification."""

import unittest
from fractions import Fraction

from flint import ctx

from analyze_dyadic_abel_packets import (
    analyze_dyadic_abel_packets,
    detect_sign_pattern,
    exact_abel_square_energy,
)


class DyadicAbelPacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192

    def test_exact_abel_energy(self):
        values = (Fraction(2, 3), Fraction(-1, 5), Fraction(7, 4))
        boundary, cumulative = exact_abel_square_energy(values, 6, 4)
        expected = sum((
            Fraction(6, k * (k + 1)) * value ** 2
            for k, value in enumerate(values, 4)
        ), Fraction(0))
        self.assertEqual(sum(boundary + cumulative, Fraction(0)), expected)

    def test_sign_pattern_runs(self):
        pattern = detect_sign_pattern((Fraction(1), Fraction(2),
                                       Fraction(-1), Fraction(-3),
                                       Fraction(4)))
        self.assertEqual(pattern.compact, "++--+")
        self.assertEqual(pattern.runs, (
            ("+", 0, 2), ("-", 2, 4), ("+", 4, 5)
        ))
        self.assertEqual(pattern.transition_indices, (2, 4))
        self.assertTrue(pattern.certified)

    def test_full_consecutive_telescope_through_8192(self):
        result = analyze_dyadic_abel_packets(2, 13)
        self.assertEqual(result.scales[-1], 8192)
        self.assertTrue(result.shell_packet_recombination_verified)
        self.assertTrue(result.boundary_telescope_verified)
        self.assertTrue(result.cumulative_telescope_verified)
        self.assertTrue(result.total_telescope_verified)
        self.assertTrue(result.interior_boundary_residual.contains(0))
        self.assertTrue(result.interior_cumulative_residual.contains(0))
        self.assertTrue(result.direct_sum.overlaps(
            result.exterior_boundary + result.exterior_cumulative
        ))
        self.assertTrue(result.decrement_sign_pattern.certified)
        self.assertTrue(result.boundary_sign_pattern.certified)
        self.assertTrue(result.cumulative_sign_pattern.certified)

    def test_base_and_depth_validation(self):
        for base, depth in ((1, 1), (3, 1), (2, 0), (4, -1), (4, 13)):
            with self.assertRaises(ValueError):
                analyze_dyadic_abel_packets(base, depth)
        result = analyze_dyadic_abel_packets(128, 7)
        self.assertEqual(result.scales, (128, 256, 512, 1024,
                                         2048, 4096, 8192))

    def test_exact_input_validation(self):
        with self.assertRaises(ValueError):
            exact_abel_square_energy((), 1, 1)
        with self.assertRaises(ValueError):
            exact_abel_square_energy((1,), 1, 0)


if __name__ == "__main__":
    unittest.main()
