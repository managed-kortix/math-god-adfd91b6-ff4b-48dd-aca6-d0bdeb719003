import unittest
from fractions import Fraction

from verify_cycle206_canonical_small_n import certificate, xi_disk_bound


class CanonicalSmallNTest(unittest.TestCase):
    def test_published_certificate(self):
        values = certificate()
        self.assertEqual(values["target_value_bound"], Fraction(203, 266))
        self.assertEqual(values["target_derivative_bound"], Fraction(221, 190))
        self.assertEqual(values["target_kernel_bound"], Fraction(44863, 151620))
        self.assertEqual(values["endpoint_kernel_bound"], Fraction(1, 6))
        self.assertEqual(values["uniform_error_bound"], Fraction(70133, 151620))
        self.assertLess(values["uniform_error_bound"], Fraction(1, 2))

    def test_bound_rejects_failed_exponential_decay(self):
        with self.assertRaises(ValueError):
            xi_disk_bound(Fraction(1), Fraction(9, 2))
        with self.assertRaises(ValueError):
            xi_disk_bound(Fraction(1), Fraction(5))

    def test_bound_rejects_invalid_domain(self):
        with self.assertRaises(ValueError):
            xi_disk_bound(Fraction(0), Fraction(1))
        with self.assertRaises(ValueError):
            xi_disk_bound(Fraction(1), Fraction(-1))

    def test_error_is_exact_sum_of_component_bounds(self):
        values = certificate()
        self.assertEqual(
            values["uniform_error_bound"],
            values["target_kernel_bound"] + values["endpoint_kernel_bound"],
        )


if __name__ == "__main__":
    unittest.main()
