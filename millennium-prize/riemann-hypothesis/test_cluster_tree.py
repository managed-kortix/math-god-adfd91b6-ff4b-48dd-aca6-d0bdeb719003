#!/usr/bin/env python3
"""Tests for the finite certified one-dimensional cluster tree."""

import unittest
from fractions import Fraction

from flint import ctx

from verify_cluster_tree import (
    certify_tree, certify_two_channel_tree, direct_form,
    direct_two_channel_form, finite_realization,
)


class ClusterTreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 160

    def test_mixed_tree_encloses_independent_dense_form(self):
        frequencies, coefficients = finite_realization(24)
        enclosure, stats = certify_tree(
            64, frequencies, coefficients, leaf_size=3, n=3, p=5
        )
        dense = direct_form(64, frequencies, coefficients)
        self.assertTrue(enclosure.contains(dense))
        self.assertGreater(stats.dense_leaves, 0)
        self.assertGreater(stats.compressed_leaves, 0)
        self.assertEqual(stats.ordered_entries, len(frequencies) ** 2)
        self.assertEqual(stats.max_rank, 12)
        self.assertGreater(stats.theorem_radius.lower(), 0)

    def test_all_dense_tree_has_no_theorem_radius(self):
        frequencies, coefficients = finite_realization(12)
        enclosure, stats = certify_tree(
            64,
            frequencies,
            coefficients,
            leaf_size=len(frequencies),
            n=3,
            p=5,
        )
        dense = direct_form(64, frequencies, coefficients)
        self.assertTrue(enclosure.contains(dense))
        self.assertTrue(dense.contains(enclosure))
        self.assertEqual(stats.dense_leaves, 1)
        self.assertEqual(stats.compressed_leaves, 0)
        self.assertTrue(stats.theorem_radius.is_zero())
        self.assertEqual(stats.ordered_entries, len(frequencies) ** 2)

    def test_requires_explicit_rational_data(self):
        with self.assertRaisesRegex(ValueError, "positive Fractions"):
            certify_tree(64, (Fraction(1), 2.0), (Fraction(1), Fraction(1)))
        with self.assertRaisesRegex(ValueError, "coefficients must be Fractions"):
            certify_tree(64, (Fraction(1), Fraction(2)), (Fraction(1), 1))
        with self.assertRaisesRegex(ValueError, "Q>0"):
            certify_tree(-1, (Fraction(1), Fraction(2)), (Fraction(1), Fraction(1)))
        with self.assertRaisesRegex(ValueError, "leaf_size"):
            certify_tree(64, (Fraction(1), Fraction(2)), (Fraction(1), Fraction(1)), leaf_size=0)

    def test_two_channel_shared_error_and_null_direction(self):
        frequencies, u = finite_realization(20)
        d = tuple(Fraction((-1) ** i * (i % 4 + 1), i + 3) for i in range(20))
        alpha = Fraction(3, 2)
        enclosure, stats = certify_two_channel_tree(
            64, frequencies, u, d, alpha, leaf_size=3, n=3, p=5
        )
        dense = direct_two_channel_form(64, frequencies, u, d, alpha)
        self.assertTrue(enclosure.contains(dense))
        self.assertEqual(stats.ordered_entries, len(frequencies) ** 2)

        # For alpha=2 and u=d, the shared kernel coefficient vanishes entrywise.
        zero, zero_stats = certify_two_channel_tree(
            64, frequencies, u, u, Fraction(2), leaf_size=3, n=3, p=5
        )
        self.assertTrue(zero.is_zero())
        self.assertTrue(zero_stats.theorem_radius.is_zero())
        self.assertEqual(zero_stats.rank_sum, 0)

    def test_hand_computed_two_channel_multiplicity(self):
        K = ((Fraction(2), Fraction(3), Fraction(5)),
             (Fraction(3), Fraction(7), Fraction(11)),
             (Fraction(5), Fraction(11), Fraction(13)))
        u = (Fraction(1), Fraction(4), Fraction(-2))
        d = (Fraction(2), Fraction(-1), Fraction(3))
        alpha = Fraction(2)
        direct = sum(
            K[i][j] * (u[i] * d[j] + d[i] * u[j] - alpha * d[i] * d[j])
            for i in range(3) for j in range(3)
        )
        self.assertEqual(direct, -92)
        self.assertEqual(-12 - 390 + 2 * 155, direct)


if __name__ == "__main__":
    unittest.main()
