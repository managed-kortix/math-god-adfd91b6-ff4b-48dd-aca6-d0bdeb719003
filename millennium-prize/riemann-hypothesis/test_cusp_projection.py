#!/usr/bin/env python3
"""Tests for the certified piecewise Legendre cusp/projection bounds."""

import unittest
from fractions import Fraction

from flint import arb, ctx

from verify_cusp_projection import (
    cell_means, certify_one_sided, compare_equal_rank, cusp_bilinear,
    dense_kernel_form, diagnostic_vectors, legendre_feature_moments,
    poincare_derivative_bound,
)
from mobius_endpoint_surrogate import (
    aggregate_modes, endpoint_channels, generate_exact_4_to_8_surrogate,
    harmonic_modes,
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
        with self.assertRaisesRegex(ValueError, "positive Fractions or Arb"):
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

    def test_origin_cell_legendre_features_are_finite(self):
        features = legendre_feature_moments(
            Fraction(3), (Fraction(2, 5), Fraction(7, 4)), 3, 3
        )
        for frequency_features in features[0]:
            for feature in frequency_features:
                self.assertTrue(feature.is_finite())

    def test_degrees_zero_through_three_enclose_dense_at_equal_rank(self):
        frequencies, u, d = diagnostic_vectors(8)
        dense, certificates = compare_equal_rank(
            Fraction(8), frequencies, u, d, Fraction(3, 2), 48
        )
        self.assertEqual(tuple(item.degree for item in certificates), (0, 1, 2, 3))
        self.assertTrue(all(item.total_rank == 48 for item in certificates))
        for certificate in certificates:
            self.assertLessEqual(dense.upper(), certificate.upper_bound)

    def test_higher_degree_residual_has_certified_refinement_order(self):
        frequencies, u, d = diagnostic_vectors(6)
        for degree in range(4):
            coarse = certify_one_sided(
                Fraction(5), frequencies, u, d, Fraction(4, 3), 6, degree
            )
            fine = certify_one_sided(
                Fraction(5), frequencies, u, d, Fraction(4, 3), 12, degree
            )
            ratio = coarse.residual_bound / fine.residual_bound
            self.assertTrue(ratio.contains(arb(2 ** (2 * (degree + 1)))))

    def test_harmonic_first_duplicate_aggregation_is_exact(self):
        raw = harmonic_modes(4, 3)
        aggregated = aggregate_modes(raw)
        by_frequency = {frequency: (u, d) for frequency, u, d in aggregated}
        for frequency, (u, d) in by_frequency.items():
            expected_u = sum(
                (mode.u for mode in raw if mode.reduced_frequency == frequency), arb(0)
            )
            expected_d = sum(
                (mode.d for mode in raw if mode.reduced_frequency == frequency), arb(0)
            )
            self.assertTrue(u.contains(expected_u) and expected_u.contains(u))
            self.assertTrue(d.contains(expected_d) and expected_d.contains(d))
        origins = {
            (mode.source, mode.harmonic)
            for mode in raw if mode.reduced_frequency == Fraction(1)
        }
        self.assertEqual(origins, {(1, 1), (2, 2), (3, 3)})
        self.assertEqual(
            tuple(by_frequency),
            tuple(sorted({Fraction(r, a) for a in (1, 2, 3, 5, 6, 7)
                          for r in range(1, 4)})),
        )

    def test_endpoint_channels_match_exact_4_to_8_definitions(self):
        u, d = endpoint_channels(4)
        self.assertTrue(u[0].contains(arb(1)))
        self.assertTrue(d[0].is_zero())
        self.assertTrue(u[3].is_zero())
        self.assertTrue(d[3].is_zero())
        self.assertTrue(u[7].is_zero())
        self.assertTrue(d[7].is_zero())

    def test_mobius_surrogate_projection_certificate(self):
        surrogate = generate_exact_4_to_8_surrogate()
        self.assertEqual(surrogate.alpha, Fraction(1, 3))
        self.assertEqual(surrogate.reduced_frequencies, tuple(sorted(set(
            mode.reduced_frequency for mode in surrogate.raw_modes
        ))))
        dense = dense_kernel_form(
            Fraction(8), surrogate.frequencies, surrogate.u, surrogate.d,
            surrogate.alpha
        )
        certificate = certify_one_sided(
            Fraction(8), surrogate.frequencies, surrogate.u, surrogate.d,
            surrogate.alpha, 64
        )
        self.assertLessEqual(dense.upper(), certificate.upper_bound)


if __name__ == "__main__":
    unittest.main()
