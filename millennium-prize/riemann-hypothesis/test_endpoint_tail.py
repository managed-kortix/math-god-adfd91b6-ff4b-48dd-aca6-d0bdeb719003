#!/usr/bin/env python3
"""Tests for the direct-breakpoint untruncated endpoint-tail certificate."""

import unittest
from fractions import Fraction

from flint import arb, ctx

from certify_endpoint_tail import (
    affine_cell, certify_endpoint_tail, certify_energy_difference,
    compare_endpoint_to_energy_difference, elementary_remainder_constant,
    finite_endpoint_prefix, finite_energy_difference_prefix,
    integrate_affine_cell,
)
from mobius_endpoint_surrogate import endpoint_alpha, endpoint_channels
from verify_separated_kernel import ball


class EndpointTailTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192
        cls.u, cls.d = endpoint_channels(4)

    def test_affine_coefficients_match_direct_sawtooth_channels(self):
        for k in (8, 9, 14, 31):
            cell = affine_cell(k, self.u, self.d)
            t = Fraction(3 * k + 2, 3)
            direct_f = ball(1) + sum(
                (value * ball(t / a - (k // a))
                 for a, value in enumerate(self.u, 1)), arb(0)
            )
            direct_d = sum(
                (value * ball(t / a - (k // a))
                 for a, value in enumerate(self.d, 1)), arb(0)
            )
            affine_f = cell.f_slope * ball(t) + cell.f_intercept
            affine_d = cell.d_slope * ball(t) + cell.d_intercept
            self.assertTrue(direct_f.overlaps(affine_f))
            self.assertTrue(direct_d.overlaps(affine_d))
            c2, c1, c0 = cell.quadratic
            direct_q = 2 * direct_f * direct_d - ball(Fraction(1, 3)) * direct_d**2
            polynomial_q = c2 * ball(t)**2 + c1 * ball(t) + c0
            self.assertTrue(direct_q.overlaps(polynomial_q))

    def test_finite_prefixes_are_additive_and_cell_exact(self):
        prefix_8_23 = finite_endpoint_prefix(8, 23, self.u, self.d)
        split = (
            finite_endpoint_prefix(8, 13, self.u, self.d)
            + finite_endpoint_prefix(13, 23, self.u, self.d)
        )
        cells = sum(
            (integrate_affine_cell(affine_cell(k, self.u, self.d))
             for k in range(8, 23)), arb(0)
        )
        self.assertTrue(prefix_8_23.overlaps(split))
        self.assertTrue(prefix_8_23.overlaps(cells))

    def test_elementary_remainder_constant_bounds_samples(self):
        constant = elementary_remainder_constant(self.u, self.d)
        for t in (Fraction(25, 3), Fraction(97, 5), Fraction(1001, 7)):
            f = ball(1) + sum(
                (value * ball(t / a - (t.numerator // (t.denominator * a)))
                 for a, value in enumerate(self.u, 1)), arb(0)
            )
            delta = sum(
                (value * ball(t / a - (t.numerator // (t.denominator * a)))
                 for a, value in enumerate(self.d, 1)), arb(0)
            )
            q = 2 * f * delta - ball(Fraction(1, 3)) * delta**2
            self.assertLessEqual(abs(q).upper(), constant.upper())

    def test_full_untruncated_tail_is_strictly_positive(self):
        certificate = certify_endpoint_tail(8, 1024)
        self.assertTrue(certificate.is_positive)
        self.assertGreater(certificate.lower_bound, 0)
        self.assertLess(certificate.lower_bound, certificate.upper_bound)

    def test_independent_finite_difference_has_alpha_factor(self):
        for N in (2, 4, 8, 16):
            u, d = endpoint_channels(N)
            endpoint = finite_endpoint_prefix(
                1, 64, u, d, endpoint_alpha(N)
            )
            direct = finite_energy_difference_prefix(N, 1, 64)
            self.assertTrue((ball(endpoint_alpha(N)) * endpoint).overlaps(direct))

    def test_small_dyadic_complete_functionals_are_positive(self):
        for N in (2, 4, 8, 16):
            comparison = compare_endpoint_to_energy_difference(N, 1, 4096)
            self.assertTrue(comparison.endpoint.is_positive)
            self.assertTrue(comparison.direct_difference.is_positive)
            self.assertTrue(comparison.agrees)

    def test_direct_difference_is_complete_not_just_a_prefix(self):
        certificate = certify_energy_difference(4, 1, 1024)
        self.assertGreater(certificate.remainder_radius, 0)
        self.assertTrue(certificate.is_positive)


if __name__ == "__main__":
    unittest.main()
