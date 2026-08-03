import json
import pathlib
import subprocess
import unittest
from copy import deepcopy
from fractions import Fraction

from flint import arb, ctx

import certify_p3_admission as p3


ROOT = pathlib.Path(__file__).resolve().parent


class P3AdmissionCertificateTest(unittest.TestCase):
    def test_genuine_3d_example_is_certified_positive(self):
        completed = subprocess.run(
            ["uv", "run", "--with", "python-flint", "python",
             str(ROOT / "certify_p3_admission.py"), "--example",
             "--subdivisions", "2", "--precision", "96"],
            check=True,
            text=True,
            capture_output=True,
        )
        self.assertIn('"proved_positive": true', completed.stdout)

    def test_pressure_sign_and_exact_zero_mode(self):
        velocity = p3.fourier_coefficients(p3.EXAMPLE["modes"])
        pressure = p3.pressure_coefficients(velocity)
        for wave, coefficient in pressure.items():
            wave2 = sum(value * value for value in wave)
            recovered = (Fraction(0), Fraction(0))
            for left_wave, left_vector in velocity.items():
                right_wave = tuple(wave[i] - left_wave[i] for i in range(3))
                if right_wave not in velocity:
                    continue
                for i in range(3):
                    for j in range(3):
                        recovered = p3.add_complex(
                            recovered,
                            p3.scale_complex(
                                p3.mul_complex(left_vector[i], velocity[right_wave][j]),
                                Fraction(-wave[i] * wave[j], wave2),
                            ),
                        )
            self.assertEqual(coefficient, recovered)

        result = p3.enclose(p3.EXAMPLE, 1, 96, "1/1024")
        self.assertEqual(result["exact_unweighted_u_dot_grad_p_integral"], "0")
        self.assertEqual(result["normalized_box_mass"], "1.000000000000000000000000000000000000000")

    def test_binomial_remainder_contains_higher_degree_reference(self):
        low = p3.enclose(p3.EXAMPLE, 1, 128, "1/1024")
        high_data = deepcopy(p3.EXAMPLE)
        high_data["positive_speed_polynomial"]["degree"] = 10
        high = p3.enclose(high_data, 1, 128, "1/1024")
        self.assertTrue(arb(low["polynomial_P3"]).contains(arb(high["polynomial_P3"])))

    def test_tail_radius_is_nonnegative_and_can_close_admission(self):
        tailed = deepcopy(p3.EXAMPLE)
        tailed["analytic_tail"] = {"velocity_l1": "1", "gradient_l1": "1"}
        result = p3.enclose(tailed, 1, 96, "1/1024")
        self.assertGreater(arb(result["fourier_tail_error_bound"]).lower(), 0)
        self.assertFalse(result["proved_positive"])

    def test_malformed_bounds_fail_closed(self):
        cases = []
        negative_tail = deepcopy(p3.EXAMPLE)
        negative_tail["analytic_tail"]["velocity_l1"] = "-1"
        cases.append(negative_tail)
        nan_rho = deepcopy(p3.EXAMPLE)
        nan_rho["positive_speed_polynomial"]["relative_perturbation_bound"] = "nan"
        cases.append(nan_rho)
        zero_center = deepcopy(p3.EXAMPLE)
        zero_center["positive_speed_polynomial"]["speed_squared_center"] = "0"
        cases.append(zero_center)
        for data in cases:
            with self.subTest(data=data), self.assertRaises((ValueError, ArithmeticError)):
                p3.enclose(data, 1, 96, "1/1024")

    def test_serialized_arb_encloses_original(self):
        ctx.prec = 128
        value = arb(1) / 3
        encoded = p3.arb_text(value)
        self.assertTrue(arb(encoded).contains(value))

    def test_checked_in_certificate_reproduces(self):
        with open(ROOT / "cycle-272-p3-certificate.json", encoding="ascii") as handle:
            certificate = json.load(handle)
        result = p3.enclose(p3.EXAMPLE, 1, certificate["precision_bits"], certificate["epsilon"])
        for key in (
            "format", "normalization", "pressure_fourier_sign", "polynomial_P3",
            "fourier_tail_error_bound", "certified_lower_endpoint", "proved_positive",
        ):
            self.assertEqual(result[key], certificate[key])


if __name__ == "__main__":
    unittest.main()
