#!/usr/bin/env python3
"""Tests for certified reserve/defect endpoint-prefix analysis."""

import unittest

from flint import arb, ctx

from analyze_endpoint_prefix import (
    analyze_endpoint_prefix, chebyshev_psi_table, drift_free_cell_identity,
)
from analyze_unit_cells import analyze_unit_cells
from mobius_endpoint_surrogate import endpoint_alpha, endpoint_channels


class EndpointPrefixAnalyzerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192

    def test_prime_power_chebyshev_values(self):
        psi = chebyshev_psi_table(10)
        self.assertTrue(psi[1].is_zero())
        self.assertTrue(psi[4].overlaps(psi[3] + psi[2]))
        self.assertTrue(psi[8].overlaps(psi[7] + psi[2]))
        self.assertTrue(psi[9].overlaps(psi[8] + arb(3).log()))

    def test_psi_identity_abel_identity_and_direct_prefix(self):
        for N in (2, 4, 8, 16):
            result = analyze_endpoint_prefix(N, 8 * N)
            self.assertTrue(result.psi_verified)
            self.assertTrue(result.direct_agrees)
            self.assertTrue(result.abel.reconstructed_sum.overlaps(
                result.later_contribution
            ))
            self.assertTrue(result.complete_prefix.overlaps(
                result.reserve + result.later_contribution
            ))
            self.assertTrue(result.drift_free.prefixes_verified)
            self.assertTrue(result.drift_free.reconstructed_sum.overlaps(
                result.complete_prefix
            ))

    def test_drift_free_identity_matches_every_Jk_for_dyadic_N(self):
        for N in (2, 4, 8, 16, 32, 64):
            unit = analyze_unit_cells(N, 1, 4 * N)
            u, d = endpoint_channels(N)
            A = sum((value / a for a, value in enumerate(u, 1)), arb(0))
            D = sum((value / a for a, value in enumerate(d, 1)), arb(0))
            direct = arb(0)
            rebuilt = arb(0)
            for cell in unit.cells:
                identity = drift_free_cell_identity(
                    cell, endpoint_alpha(N), A, D
                )
                self.assertGreater(identity.R.lower(), 0)
                self.assertGreater(identity.V.lower(), 0)
                self.assertGreater(identity.w.lower(), 0)
                self.assertTrue(identity.reconstructed_J.overlaps(cell.J))
                direct += cell.J
                rebuilt += identity.reconstructed_J
                self.assertTrue(direct.overlaps(rebuilt))

    def test_coefficient_and_tail_bounds_are_rigorous(self):
        result = analyze_endpoint_prefix(32, 8 * 32, compare_direct=False)
        drift = result.drift_free
        for cell in drift.cells:
            self.assertLessEqual(
                max(abs(cell.R_coefficient.lower()),
                    abs(cell.R_coefficient.upper())),
                drift.R_coefficient_bound.upper(),
            )
            self.assertLessEqual(
                max(abs(cell.V_coefficient.lower()),
                    abs(cell.V_coefficient.upper())),
                drift.V_coefficient_bound.upper(),
            )
            self.assertLessEqual(
                max(abs(cell.w_coefficient.lower()),
                    abs(cell.w_coefficient.upper())),
                drift.w_coefficient_bound.upper(),
            )
        self.assertTrue(drift.pointwise_tail_radius.overlaps(
            result.tail_radius
        ))
        self.assertGreaterEqual(
            drift.coefficient_tail_radius.lower(),
            drift.pointwise_tail_radius.upper(),
        )

    def test_defect_is_worst_anchored_later_loss(self):
        result = analyze_endpoint_prefix(128, 4 * 128, compare_direct=False)
        self.assertGreater(result.later_defect.lower(), 0)
        self.assertGreaterEqual(result.defect_endpoint, result.N)
        self.assertLessEqual(result.defect_endpoint, result.T)
        self.assertGreater(result.reserve_defect_ratio.lower(), 1)

    def test_tail_radius_has_inverse_horizon_scaling(self):
        near = analyze_endpoint_prefix(16, 8 * 16, compare_direct=False)
        far = analyze_endpoint_prefix(16, 16 * 16, compare_direct=False)
        self.assertTrue(near.tail_radius.overlaps(2 * far.tail_radius))

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            analyze_endpoint_prefix(6, 48)
        with self.assertRaises(ValueError):
            analyze_endpoint_prefix(8, 8)
        with self.assertRaises(ValueError):
            chebyshev_psi_table(0)


if __name__ == "__main__":
    unittest.main()
