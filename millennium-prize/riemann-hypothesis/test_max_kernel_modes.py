#!/usr/bin/env python3
"""Tests for max-kernel tridiagonal eigenmode analysis."""

import unittest
from fractions import Fraction
import importlib.util
import math

from analyze_max_kernel_modes import (
    analyze_max_kernel_modes, inverse_tridiagonal, max_kernel,
)


class MaxKernelModeTests(unittest.TestCase):
    def test_exact_inverse_tridiagonal(self):
        for N, M in ((2, 4), (3, 7), (8, 16)):
            kernel = max_kernel(N, M)
            diagonal, off = inverse_tridiagonal(N, M)
            size = M - N
            inverse = [[Fraction(0) for _ in range(size)] for _ in range(size)]
            for i, value in enumerate(diagonal):
                inverse[i][i] = value
            for i, value in enumerate(off):
                inverse[i][i + 1] = inverse[i + 1][i] = value
            for i in range(size):
                for j in range(size):
                    product = sum(kernel[i][k] * inverse[k][j] for k in range(size))
                    self.assertEqual(product, Fraction(i == j))

    @unittest.skipUnless(
        importlib.util.find_spec("numpy") and importlib.util.find_spec("scipy"),
        "optional numpy/scipy eigensolver is unavailable",
    )
    def test_modal_decomposition_and_center_relation(self):
        for N in (2, 4, 8, 16):
            result = analyze_max_kernel_modes(N)
            self.assertAlmostEqual(
                result.quadratic_total + result.linear_total,
                result.tracking_total, places=11,
            )
            for mode in result.modes:
                self.assertAlmostEqual(
                    mode.eigenvalue * mode.center_projection,
                    math.log(N) * mode.linear_target_projection,
                    delta=2e-10 * max(1.0, abs(mode.center_projection)),
                )
                self.assertAlmostEqual(
                    mode.quadratic + mode.linear, mode.tracking,
                    delta=2e-10 * max(1.0, abs(mode.tracking)),
                )

    @unittest.skipUnless(
        importlib.util.find_spec("numpy") and importlib.util.find_spec("scipy"),
        "optional numpy/scipy eigensolver is unavailable",
    )
    def test_explanation_counts_are_valid(self):
        result = analyze_max_kernel_modes(32)
        values = result.explanation.__dict__.values()
        self.assertTrue(all(0 <= value <= 32 for value in values))
        self.assertGreater(result.quadratic_total, 0)
        self.assertLess(result.linear_total, 0)

    @unittest.skipUnless(
        importlib.util.find_spec("numpy") and importlib.util.find_spec("scipy"),
        "optional numpy/scipy eigensolver is unavailable",
    )
    def test_small_arb_certificate(self):
        result = analyze_max_kernel_modes(4, certify=True, bits=160)
        certificate = result.certificate
        self.assertTrue(certificate.eigenvalues_isolated)
        self.assertTrue(certificate.orthonormal)
        self.assertTrue(certificate.quadratic_identity)
        self.assertTrue(certificate.linear_identity)
        self.assertTrue(certificate.tracking_identity)

    def test_validation(self):
        with self.assertRaises(ValueError):
            inverse_tridiagonal(0)
        with self.assertRaises(ValueError):
            inverse_tridiagonal(4, 4)
        if importlib.util.find_spec("numpy") and importlib.util.find_spec("scipy"):
            with self.assertRaises(ValueError):
                analyze_max_kernel_modes(4, 9)
            with self.assertRaises(ValueError):
                analyze_max_kernel_modes(64, certify=True)


if __name__ == "__main__":
    unittest.main()
