#!/usr/bin/env python3
"""Tests for the exact/Arb two-scale completed-square analyzer."""

import unittest
from fractions import Fraction

from flint import arb, ctx

from analyze_two_scale_completion import (
    analyze_two_scale_completion, exact_rank, floor_matrix, nullspace_basis,
)
from search_cross_scale_sources import certificate


class TwoScaleCompletionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192

    def test_floor_matrix_rank_and_nullspace_are_exact(self):
        matrix = floor_matrix(4, 8, 4)
        self.assertEqual(matrix[0], (4, 2, 1, 1))
        self.assertEqual(exact_rank(matrix), 3)
        basis = nullspace_basis(matrix)
        self.assertEqual(len(basis), 1)
        for vector in basis:
            for row in matrix:
                self.assertEqual(
                    sum((a * b for a, b in zip(row, vector)), Fraction(0)), 0
                )

    def test_completed_identity_and_weighted_g_cross_check(self):
        for N in (2, 4, 8, 16, 32):
            result = analyze_two_scale_completion(N)
            self.assertTrue(result.z_2N_psi_verified)
            self.assertTrue(result.completed_cells_verified)
            self.assertTrue(result.weighted_g_verified)
            self.assertTrue(result.completed_total.overlaps(
                result.scaled_weighted_g_total
            ))
            self.assertTrue(result.scaled_weighted_g_total.overlaps(
                arb(result.alpha.numerator) / result.alpha.denominator
                * result.weighted_g_total
            ))

    def test_joint_kernel_is_exact_direct_sum(self):
        for N in (2, 4, 8, 16):
            result = analyze_two_scale_completion(N)
            self.assertTrue(result.joint_kernel_verified)
            self.assertEqual(
                len(result.joint_kernel_basis),
                len(result.kernel_N) + len(result.kernel_2N),
            )
            self.assertEqual(len(result.joint_kernel_basis), result.inertia.zero)

    def test_finite_N_signed_gram_inertia(self):
        for N in (2, 4, 8, 16, 32):
            result = analyze_two_scale_completion(N)
            inertia = result.inertia
            self.assertTrue(result.inertia_verified)
            self.assertEqual(inertia.positive, exact_rank(result.floor_N))
            self.assertEqual(inertia.negative, exact_rank(result.floor_2N))
            self.assertEqual(
                inertia.positive + inertia.negative + inertia.zero,
                inertia.dimension,
            )
            self.assertEqual(inertia.dimension, 3 * N)

    def test_actual_mobius_sources_are_projected_not_surrogates(self):
        for N in (4, 8, 16):
            result = analyze_two_scale_completion(N)
            for projection in (result.projection_N, result.projection_2N):
                self.assertTrue(projection.decomposition_verified)
                self.assertTrue(projection.kernel_verified)
                self.assertTrue(projection.image_verified)
                self.assertEqual(projection.rank + projection.nullity,
                                 projection.columns)
                self.assertTrue(any(not value.is_zero()
                                    for value in projection.source))
                self.assertTrue(all(value.contains(0)
                                    for value in projection.kernel_image))

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            analyze_two_scale_completion(6)
        with self.assertRaises(ValueError):
            floor_matrix(4, 4, 4)

    def test_minimal_generic_cross_scale_counterexample(self):
        item = certificate(2)
        self.assertLess(item["determinant"], 0)
        self.assertLess(item["values"][Fraction(1)], 0)
        self.assertGreater(item["values"][Fraction(-1)], 0)
        self.assertNotEqual(item["cross"], 0)


if __name__ == "__main__":
    unittest.main()
