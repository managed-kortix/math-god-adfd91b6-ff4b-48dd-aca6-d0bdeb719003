#!/usr/bin/env python3
"""Tests for the exact/Arb pair-constant residual analyzer."""

import unittest
from fractions import Fraction

from flint import ctx

from analyze_pair_constant_residual import (
    analyze_pair_constant_residual,
    exact_left_null_geometry,
    exact_pair_constant_geometry,
)


class PairConstantResidualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192

    def test_generic_sparse_left_null_basis(self):
        geometry = exact_left_null_geometry(
            ((1, 0), (1, 0), (0, 1)),
            (Fraction(1), Fraction(2), Fraction(3)),
        )
        self.assertEqual(geometry.rank, 2)
        self.assertEqual(geometry.nullity, 1)
        self.assertEqual(geometry.basis, ((Fraction(-1), Fraction(1), Fraction(0)),))
        self.assertEqual(geometry.supports, ((0, 1),))
        self.assertEqual(geometry.weighted_gram, ((Fraction(3, 2),),))
        self.assertTrue(geometry.annihilation_verified)

    def test_coarse_floor_matrix_has_no_left_nullspace_through_128(self):
        for N in (2, 4, 8, 16, 32, 64, 128):
            geometry = exact_pair_constant_geometry(N)
            self.assertEqual(geometry.rank, N // 2)
            self.assertEqual(geometry.nullity, 0)
            self.assertEqual(geometry.basis, ())
            self.assertEqual(geometry.supports, ())
            self.assertTrue(geometry.annihilation_verified)

    def test_unit_lower_triangular_shell_rank_witness(self):
        for N in (2, 4, 8, 16, 32, 64, 128):
            matrix = exact_pair_constant_geometry(N).matrix
            start = N // 2
            for row, k in enumerate(range(start, N)):
                for column, d in enumerate(range(start, N)):
                    self.assertEqual(matrix[row][d - 1], Fraction(d <= k))

    def test_actual_affine_residual_and_prime_comparison_through_128(self):
        for N in (2, 4, 8, 16, 32, 64, 128):
            result = analyze_pair_constant_residual(N)
            self.assertEqual(result.residual_coordinates, ())
            self.assertEqual(result.coordinate_supports, ())
            self.assertEqual(result.residual_support, ())
            self.assertTrue(result.projection_verified)
            self.assertTrue(result.weighted_projection_energy.contains(0))
            self.assertTrue(result.direct_weighted_energy.contains(0))
            self.assertTrue(result.energy_verified)
            self.assertTrue(result.prime_diagonal_positive)

    def test_input_validation(self):
        for N in (1, 3, 256):
            with self.assertRaises(ValueError):
                exact_pair_constant_geometry(N)


if __name__ == "__main__":
    unittest.main()
