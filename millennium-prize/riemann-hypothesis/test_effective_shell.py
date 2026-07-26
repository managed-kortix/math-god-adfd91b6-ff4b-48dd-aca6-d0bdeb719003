#!/usr/bin/env python3
"""Tests for the exact/Arb effective-shell analyzer."""

import unittest
from fractions import Fraction

from flint import ctx

from analyze_effective_shell import (
    analyze_effective_shell,
    exact_shell_first_differences,
    exact_shell_reconstruction,
)


class EffectiveShellTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192

    def test_exact_first_difference_inverse(self):
        values = (Fraction(2, 3), Fraction(-1, 5), Fraction(7, 4))
        coefficients = exact_shell_first_differences(values)
        self.assertEqual(coefficients, (
            Fraction(2, 3), Fraction(-13, 15), Fraction(39, 20)
        ))
        self.assertEqual(exact_shell_reconstruction(coefficients), values)

    def test_effective_coefficients_reconstruct_pair_average(self):
        for N in (2, 4, 8, 32, 128):
            result = analyze_effective_shell(N)
            self.assertTrue(result.first_difference_verified)
            self.assertTrue(result.pair_average_verified)
            self.assertEqual(len(result.effective_coefficients), N)
            self.assertEqual(len(result.first_difference_coefficients), N // 2)

    def test_discrepancy_reconstructs_image_difference(self):
        for N in (2, 8, 32, 128, 512):
            result = analyze_effective_shell(N)
            for effective, preceding, discrepancy in zip(
                    result.reconstructed_pair_average,
                    result.preceding_image,
                    self._discrepancy_image(result)):
                self.assertTrue(effective.overlaps(preceding + discrepancy))

    @staticmethod
    def _discrepancy_image(result):
        zero = result.discrepancy[0] * 0
        return tuple(
            sum((coefficient * (k // d) for d, coefficient in
                 enumerate(result.discrepancy, 1)), zero)
            for k in range(result.N // 2, result.N)
        )

    def test_affine_jump_is_direct_fine_pair_jump(self):
        for N in (2, 8, 32, 128):
            result = analyze_effective_shell(N)
            for offset, jump in enumerate(result.pair_jumps):
                even = result.fine_completed_vector[2 * offset]
                odd = result.fine_completed_vector[2 * offset + 1]
                self.assertTrue(jump.overlaps(odd - even))

    def test_complete_fine_energy_decomposition_through_8192(self):
        for N in (2, 8, 32, 128, 512, 2048, 8192):
            result = analyze_effective_shell(N)
            self.assertTrue(result.fine_energy_verified)
            self.assertTrue(result.complete_fine_energy.overlaps(
                result.weighted_coarse_energy + result.affine_jump_energy
            ))
            self.assertTrue(result.polarization_verified)
            self.assertTrue(result.coarse_minus_fine.overlaps(
                -2 * result.preceding_discrepancy_correlation
                - result.pair_average_discrepancy_energy
                - result.affine_jump_energy
            ))

    def test_preceding_completed_vector_uses_affine_center(self):
        for N in (8, 32, 128):
            result = analyze_effective_shell(N)
            self.assertTrue(any(
                not raw.overlaps(completed)
                for raw, completed in zip(result.preceding_image,
                                          result.preceding_completed_vector)
            ))
            for pair, old, delta in zip(
                    result.reconstructed_pair_average,
                    result.preceding_completed_vector,
                    result.pair_average_discrepancy):
                self.assertTrue(pair.overlaps(old + delta))

    def test_input_validation(self):
        for N in (1, 3, 16384):
            with self.assertRaises(ValueError):
                analyze_effective_shell(N)
        with self.assertRaises(ValueError):
            exact_shell_first_differences(())


if __name__ == "__main__":
    unittest.main()
