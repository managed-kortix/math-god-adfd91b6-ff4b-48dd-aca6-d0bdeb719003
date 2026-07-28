#!/usr/bin/env python3

import unittest

from verify_cycle70_fermat_quartic import (
    bounded_monomials,
    exact_rank,
    incidence_monomial_matrix,
    jacobian_multiplication_matrix,
    normalized_plane_class,
    verify,
)


class Cycle70FermatQuarticTests(unittest.TestCase):
    def test_jacobian_ring_dimensions_and_multiplication_rank(self):
        matrix, r4_basis, r10_basis = jacobian_multiplication_matrix()
        self.assertEqual(len(r4_basis), 90)
        self.assertEqual(len(r10_basis), 21)
        self.assertEqual((len(matrix), len(matrix[0])), (21, 90))
        self.assertEqual(exact_rank(matrix), 6)

    def test_diagonally_normalized_plane_class(self):
        plane_class = normalized_plane_class()
        self.assertEqual(len(plane_class), 27)
        self.assertEqual(set(plane_class.values()), {1})
        self.assertTrue(all(sum(exponent) == 6 for exponent in plane_class))

    def test_incidence_monomial_map_rank(self):
        matrix, quartics_on_plane = incidence_monomial_matrix()
        self.assertEqual(len(quartics_on_plane), 15)
        self.assertEqual((len(matrix), len(matrix[0])), (15, 9))
        self.assertEqual(exact_rank(matrix), 9)

    def test_public_verification_record(self):
        result = verify()
        self.assertEqual(
            (
                result.r4_dimension,
                result.r10_dimension,
                result.jacobian_multiplication_rank,
                result.incidence_monomial_rank,
            ),
            (90, 21, 6, 9),
        )

    def test_exact_rank_validation(self):
        self.assertEqual(exact_rank([]), 0)
        with self.assertRaises(ValueError):
            exact_rank([[1, 0], [1]])
        with self.assertRaises(ValueError):
            bounded_monomials(0, 4, 2)


if __name__ == "__main__":
    unittest.main()
