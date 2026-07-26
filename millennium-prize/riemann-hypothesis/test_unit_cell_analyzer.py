#!/usr/bin/env python3
"""Tests for the divisor-sieve endpoint unit-cell analyzer."""

import unittest

from flint import arb, ctx

from analyze_unit_cells import (
    analyze_unit_cells, contiguous_block_diagnostic, divisor_impulses,
    fixed_lag_pairing_diagnostic, search_block_lengths,
)
from certify_endpoint_tail import certify_endpoint_tail, finite_endpoint_prefix
from mobius_endpoint_surrogate import endpoint_alpha, endpoint_channels


class UnitCellAnalyzerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192

    def test_divisor_sieve_matches_direct_divisor_sums(self):
        coefficients = tuple(arb(value) for value in (1, -2, 3, 0, 5))
        impulses = divisor_impulses(coefficients, 20)
        for n in range(1, 21):
            direct = sum(
                (coefficient for a, coefficient in enumerate(coefficients, 1)
                 if n % a == 0),
                arb(0),
            )
            self.assertTrue(impulses[n].overlaps(direct))

    def test_sieved_cells_and_prefix_match_direct_certificate(self):
        for N in (2, 4, 8, 16):
            analysis = analyze_unit_cells(N, 1, 96)
            u, d = endpoint_channels(N)
            direct = finite_endpoint_prefix(1, 96, u, d, endpoint_alpha(N))
            certificate = certify_endpoint_tail(1, 96, N)
            self.assertTrue(analysis.finite_prefix.overlaps(direct))
            self.assertTrue(analysis.finite_prefix.overlaps(certificate.finite_prefix))

    def test_nontrivial_start_prefix_matches_direct_certificate(self):
        analysis = analyze_unit_cells(8, 17, 80)
        u, d = endpoint_channels(8)
        direct = finite_endpoint_prefix(17, 80, u, d, endpoint_alpha(8))
        self.assertTrue(analysis.finite_prefix.overlaps(direct))
        self.assertEqual(analysis.cells[0].k, 17)
        self.assertFalse(analysis.cells[0].prefix.overlaps(analysis.finite_prefix))

    def test_known_negative_cell_and_runs_are_found(self):
        analysis = analyze_unit_cells(8, 1, 64)
        negative_indices = {
            cell.k for cell in analysis.cells if cell.sign == "negative"
        }
        run_indices = {
            k for run in analysis.negative_runs for k in range(run.start, run.end + 1)
        }
        self.assertIn(35, negative_indices)
        self.assertEqual(run_indices, negative_indices)

    def test_block_and_pairing_diagnostics_are_decisive(self):
        analysis = analyze_unit_cells(8, 1, 64)
        singletons = contiguous_block_diagnostic(analysis.cells, 1)
        self.assertEqual(singletons.status, "failure")
        self.assertGreater(singletons.negative_windows, 0)
        _, first_success = search_block_lengths(analysis.cells, 8)
        self.assertIsNotNone(first_success)
        self.assertEqual(first_success.status, "success")
        self.assertLessEqual(first_success.length, 8)
        diagnostics = [
            fixed_lag_pairing_diagnostic(analysis.cells, lag)
            for lag in (-2, -1, 1, 2)
        ]
        self.assertTrue(all(item.status in {"success", "failure"} for item in diagnostics))
        self.assertTrue(all(item.negative_cells > 0 for item in diagnostics))

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            analyze_unit_cells(6, 1, 10)
        with self.assertRaises(ValueError):
            divisor_impulses((arb(1),), 0)
        analysis = analyze_unit_cells(4, 1, 10)
        with self.assertRaises(ValueError):
            contiguous_block_diagnostic(analysis.cells, 20)
        with self.assertRaises(ValueError):
            fixed_lag_pairing_diagnostic(analysis.cells, 0)


if __name__ == "__main__":
    unittest.main()
