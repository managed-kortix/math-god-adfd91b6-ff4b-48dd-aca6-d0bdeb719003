#!/usr/bin/env python3
"""Tests for the certified weighted drift-free g_k tail decomposition."""

import unittest
from flint import arb, ctx

from analyze_weighted_g_tail import (
    analyze_weighted_g_tail, mobius_table, truncated_mobius_transform,
)


class WeightedGTailTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192

    def test_exact_mobius_table(self):
        self.assertEqual(
            mobius_table(12),
            (0, 1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0),
        )

    def test_truncated_transform_definition(self):
        N = 8
        values = truncated_mobius_transform(N, 16)
        self.assertTrue(values[8].is_zero())
        log_N = arb(N).log()
        expected_10 = (arb(8) / 10).log() / log_N
        self.assertTrue(values[9].is_zero())
        self.assertTrue(values[10].overlaps(expected_10))

    def test_reconstructs_every_drift_free_cell_and_prefix(self):
        for N in (2, 4, 8, 16, 32, 64):
            result = analyze_weighted_g_tail(N)
            self.assertEqual(result.horizons[0].stop, 2 * N)
            for cell in result.cells:
                self.assertTrue(cell.identities_verified)
                self.assertTrue(cell.reconstructed_g.overlaps(cell.drift_free_g))
                self.assertTrue(cell.weighted_reconstruction.overlaps(
                    cell.weighted_baseline
                    + cell.weighted_linear
                    + cell.weighted_quadratic
                ))
            horizon = result.horizons[0]
            self.assertTrue(horizon.cells_verified)
            self.assertTrue(horizon.prefixes_verified)
            self.assertTrue(horizon.reconstructed_sum.overlaps(
                horizon.drift_free_sum
            ))
            self.assertTrue(horizon.baseline_sum.overlaps(
                horizon.baseline_slope_sum
                + horizon.baseline_cross_sum
                + horizon.baseline_psi_square_sum
            ))

    def test_configurable_horizons_are_nested_prefixes(self):
        N = 32
        result = analyze_weighted_g_tail(N, (40, 48, 64))
        self.assertEqual(
            tuple(horizon.stop for horizon in result.horizons),
            (40, 48, 64),
        )
        for horizon in result.horizons:
            direct = sum(
                (cell.weighted_reconstruction for cell in result.cells
                 if cell.k < horizon.stop),
                result.cells[0].weight * 0,
            )
            self.assertTrue(horizon.reconstructed_sum.overlaps(direct))

    def test_term_coefficients_and_certified_signs(self):
        for N in (8, 16, 32, 64):
            result = analyze_weighted_g_tail(N)
            horizon = result.horizons[0]
            self.assertLess(horizon.linear_sum.upper(), 0)
            self.assertGreater(horizon.quadratic_sum.lower(), 0)
            for cell in result.cells:
                self.assertGreaterEqual(cell.quadratic.lower(), 0)

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            analyze_weighted_g_tail(6)
        with self.assertRaises(ValueError):
            analyze_weighted_g_tail(8, (8,))
        with self.assertRaises(ValueError):
            analyze_weighted_g_tail(8, (17,))
        with self.assertRaises(ValueError):
            truncated_mobius_transform(8, 17)


if __name__ == "__main__":
    unittest.main()
