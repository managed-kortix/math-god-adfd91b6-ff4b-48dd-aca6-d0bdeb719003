#!/usr/bin/env python3
"""Tests for the certified piecewise-constant cusp/projection bound."""

import unittest
from fractions import Fraction

from flint import arb, ctx

from verify_cusp_projection import (
    cell_means, certify_one_sided, cusp_bilinear, dense_kernel_form,
    diagnostic_vectors, poincare_derivative_bound,
)
from verify_separated_kernel import ball


class CuspProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192

    def test_suffix_cusp_matches_quadratic_double_sum(self):
        frequencies = (Fraction(1, 5), Fraction(2, 3), Fraction(7, 4))
        x = (Fraction(2, 3), Fraction(-5, 7), Fraction(4, 9))
        y = (Fraction(-3, 8), Fraction(6, 5), Fraction(1, 2))
        dense = sum(
            x[i] * y[j] * min(frequencies[i], frequencies[j])
            for i in range(3) for j in range(3)
        )
        self.assertEqual(cusp_bilinear(frequencies, x, y), dense)

    def test_first_cell_mean_is_origin_safe_and_exact_si_formula(self):
        Q, w = Fraction(3, 2), Fraction(7, 5)
        means = cell_means(Q, (w,), 1)
        expected = ball(w * Q).si() / ball(Q)
        self.assertTrue(means[0][0].contains(expected))
        self.assertTrue(expected.contains(means[0][0]))
        self.assertTrue(means[0][0] < ball(w))
        self.assertTrue(means[0][0] > 0)

    def test_one_sided_bound_dominates_dense_rational_form(self):
        frequencies, u, d = diagnostic_vectors(9)
        alpha, Q = Fraction(3, 2), Fraction(8)
        dense = dense_kernel_form(Q, frequencies, u, d, alpha)
        certificate = certify_one_sided(Q, frequencies, u, d, alpha, 24)
        self.assertLessEqual(dense.upper(), certificate.upper_bound)
        self.assertGreater(certificate.poincare_remainder.lower(), 0)

    def test_poincare_remainder_has_quadratic_cell_scaling(self):
        frequencies, u, d = diagnostic_vectors(7)
        args = (Fraction(6), frequencies, u, d, Fraction(5, 4))
        coarse = certify_one_sided(*args, 10)
        fine = certify_one_sided(*args, 20)
        ratio = coarse.poincare_remainder / fine.poincare_remainder
        self.assertTrue(ratio.contains(arb(4)))
        self.assertLessEqual(
            dense_kernel_form(*args[:-1], args[-1]).upper(), coarse.upper_bound
        )
        self.assertLessEqual(
            dense_kernel_form(*args[:-1], args[-1]).upper(), fine.upper_bound
        )

    def test_cancellation_direction_has_zero_adverse_remainder(self):
        frequencies, u, _ = diagnostic_vectors(8)
        alpha = Fraction(2)
        d = tuple(ui / alpha for ui in u)
        certificate = certify_one_sided(
            Fraction(5), frequencies, u, d, alpha, 12
        )
        self.assertTrue(certificate.derivative_energy_bound.is_zero())
        self.assertTrue(certificate.poincare_remainder.is_zero())
        dense = dense_kernel_form(Fraction(5), frequencies, u, d, alpha)
        self.assertLessEqual(dense.upper(), certificate.upper_bound)

    def test_input_contract(self):
        with self.assertRaisesRegex(ValueError, "positive Fractions"):
            certify_one_sided(Fraction(1), (1.0,), (Fraction(1),),
                              (Fraction(1),), Fraction(1), 2)
        with self.assertRaisesRegex(ValueError, "positive Fraction"):
            certify_one_sided(Fraction(1), (Fraction(1),), (Fraction(1),),
                              (Fraction(1),), Fraction(0), 2)

    def test_suffix_derivative_profile_preserves_cancellation(self):
        frequencies = (Fraction(9), Fraction(10))
        z = (Fraction(1), Fraction(-1))
        energy, _ = poincare_derivative_bound(Fraction(2), frequencies, z, 4)
        self.assertTrue(energy.contains(ball(Fraction(2) * Fraction(19, 2) ** 2)))
        crude = Fraction(2) * Fraction(9 * 9 + 10 * 10, 2) ** 2
        self.assertLess(energy.upper(), ball(crude).lower())


if __name__ == "__main__":
    unittest.main()
