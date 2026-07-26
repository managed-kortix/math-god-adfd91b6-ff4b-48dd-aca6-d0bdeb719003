#!/usr/bin/env python3
"""Algebra-only tests for finite-zero shell decomposition bookkeeping."""

import unittest
from fractions import Fraction

from reconnoiter_finite_zero_shell import decompose_shell_vectors


class FiniteZeroShellAlgebraTests(unittest.TestCase):
    def test_affine_gram_and_remainder_recombine_exactly(self):
        weights = (Fraction(2, 3), Fraction(5, 7), Fraction(11, 13))
        d0 = (Fraction(1, 2), Fraction(-2, 5), Fraction(7, 3))
        d1 = (Fraction(-1, 4), Fraction(3, 8), Fraction(5, 6))
        zero0 = (Fraction(2, 9), Fraction(4, 11), Fraction(-3, 7))
        zero1 = (Fraction(5, 12), Fraction(-1, 10), Fraction(8, 15))
        remainder0 = (Fraction(1, 17), Fraction(-2, 19), Fraction(3, 23))
        remainder1 = (Fraction(-4, 29), Fraction(5, 31), Fraction(1, 37))
        jump = Fraction(7, 41)

        result = decompose_shell_vectors(
            weights, d0, d1, zero0, zero1, remainder0, remainder1, jump
        )
        self.assertEqual(
            result.affine_constant + result.affine_zero_linear
            + result.zero_quadratic,
            result.truncated_gram,
        )
        self.assertEqual(
            result.truncated_gram + result.arithmetic_remainder_correction,
            result.recombined_total,
        )
        self.assertEqual(result.recombined_total, result.direct_total)

    def test_zero_remainder_reduces_to_finite_gram(self):
        weights = (Fraction(1, 3), Fraction(2, 5))
        d0 = (Fraction(2), Fraction(-1))
        d1 = (Fraction(1, 2), Fraction(3, 2))
        z0 = (Fraction(-1, 3), Fraction(4, 7))
        z1 = (Fraction(2, 9), Fraction(-5, 8))
        zeros = (Fraction(0), Fraction(0))
        result = decompose_shell_vectors(
            weights, d0, d1, z0, z1, zeros, zeros, Fraction(3, 11)
        )
        self.assertEqual(result.arithmetic_remainder_correction, 0)
        self.assertEqual(result.truncated_gram, result.direct_total)

    def test_vector_lengths_are_validated(self):
        with self.assertRaises(ValueError):
            decompose_shell_vectors((1,), (1,), (1,), (), (1,), (1,), (1,), 0)
        with self.assertRaises(ValueError):
            decompose_shell_vectors((), (), (), (), (), (), (), 0)


if __name__ == "__main__":
    unittest.main()
