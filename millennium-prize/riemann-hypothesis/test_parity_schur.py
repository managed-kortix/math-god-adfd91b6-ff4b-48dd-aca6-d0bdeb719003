#!/usr/bin/env python3
"""Tests for the exact/Arb weighted parity Schur analyzer."""

import unittest
from fractions import Fraction

from flint import ctx

from analyze_parity_schur import analyze_parity_schur, exact_parity_geometry


class ParitySchurTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192

    def test_small_exact_schur_complement(self):
        geometry = exact_parity_geometry(2)
        self.assertEqual(geometry.weights, (Fraction(1, 6), Fraction(1, 12)))
        self.assertEqual(geometry.coarse_basis_indices, (0,))
        self.assertEqual(geometry.odd_projection, (
            (Fraction(7, 3), Fraction(1, 3)),
        ))
        self.assertEqual(geometry.schur_complement, (
            (Fraction(1, 18), Fraction(1, 18)),
            (Fraction(1, 18), Fraction(1, 18)),
        ))
        self.assertTrue(geometry.schur_verified)
        self.assertTrue(geometry.orthogonality_verified)
        self.assertTrue(geometry.incidence_schur_verified)

    def test_exact_ranks_and_positive_schur_through_64(self):
        for N in (2, 4, 8, 16, 32, 64):
            geometry = exact_parity_geometry(N)
            self.assertEqual(geometry.even_rank, N // 2)
            self.assertEqual(geometry.odd_rank, N)
            self.assertEqual(geometry.fine_rank, N)
            self.assertEqual(geometry.schur_rank, N // 2)
            self.assertTrue(geometry.schur_verified)
            self.assertTrue(geometry.orthogonality_verified)
            self.assertTrue(geometry.incidence_schur_verified)

    def test_actual_mobius_projection_energies_and_cross_terms(self):
        for N in (2, 4, 8, 16, 32, 64):
            energy = analyze_parity_schur(N).energy
            self.assertTrue(energy.projection_verified)
            self.assertTrue(energy.schur_energy_verified)
            self.assertTrue(energy.prime_residual_verified)
            self.assertTrue(energy.residual_energy.overlaps(
                energy.prime_residual_energy
            ))
            self.assertTrue(energy.projected_residual_cross.contains(0))
            self.assertTrue(energy.coarse_residual_cross.contains(0))
            self.assertTrue(energy.odd_energy.overlaps(
                energy.projected_odd_energy + energy.residual_energy
            ))
            self.assertTrue(energy.even_odd_cross.overlaps(
                energy.even_projected_odd_cross
            ))

    def test_direct_fine_energy_cross_check(self):
        for N in (2, 4, 8, 16, 32, 64):
            energy = analyze_parity_schur(N).energy
            direct_from_even_odd = (
                energy.even_energy + 2 * energy.even_odd_cross
                + energy.odd_energy
            )
            self.assertTrue(energy.direct_fine_energy.overlaps(
                direct_from_even_odd
            ))
            self.assertTrue(energy.direct_fine_energy.overlaps(
                energy.decomposed_fine_energy
            ))
            self.assertTrue(energy.direct_energy_verified)

    def test_input_validation(self):
        for N in (1, 3, 128):
            with self.assertRaises(ValueError):
                exact_parity_geometry(N)


if __name__ == "__main__":
    unittest.main()
