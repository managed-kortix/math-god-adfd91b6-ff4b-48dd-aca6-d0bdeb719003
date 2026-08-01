#!/usr/bin/env python3
"""Dependency-free hostile tests for the Cycle 212 validation primitives."""

import json
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from validate_cycle212 import (
    CInterval,
    Interval,
    analytic_enstrophy_tail_bound,
    analytic_velocity_bounds,
    check_dissipative_shell_cap,
    check_picard_box,
    geometric_tail_sum,
    load_manifest,
    low_mode_tail_remainder_bound,
    paired_vorticity_coefficient,
    retained_modes,
    sqrt_interval,
    shell_convolution_bound,
    trig_interval,
)


class Cycle212Tests(unittest.TestCase):
    def test_directed_sqrt(self):
        enclosure = sqrt_interval(Interval.point(Fraction(2)))
        self.assertLessEqual(enclosure.lo * enclosure.lo, 2)
        self.assertGreaterEqual(enclosure.hi * enclosure.hi, 2)

    def test_trig_special_values(self):
        self.assertTrue(trig_interval(Fraction(0), "sin").subset(Interval.point(0)))
        self.assertTrue(trig_interval(Fraction(0), "cos").subset(Interval.point(1)))
        sine_quarter = trig_interval(Fraction(1, 4), "sin", 24)
        self.assertLessEqual(sine_quarter.lo, 1)
        self.assertGreaterEqual(sine_quarter.hi, 1)
        cosine_half = trig_interval(Fraction(1, 2), "cos", 24)
        self.assertLessEqual(cosine_half.lo, -1)
        self.assertGreaterEqual(cosine_half.hi, -1)

    def test_geometric_tail(self):
        self.assertEqual(geometric_tail_sum(Fraction(3), Fraction(2), 2), Fraction(3, 2))
        self.assertEqual(geometric_tail_sum(Fraction(1), Fraction(2), 2, 1), Fraction(3, 2))

    def test_analytic_norm_includes_tail(self):
        omega = {
            (1, 0): CInterval.point(1),
            (-1, 0): CInterval.point(1),
        }
        uniform, gradient, tail_component = analytic_velocity_bounds(
            omega, Fraction(1), Fraction(2), 2
        )
        self.assertEqual(tail_component, Fraction(1, 4))
        self.assertGreaterEqual(uniform, Fraction(9, 4))
        self.assertGreaterEqual(gradient, Fraction(5, 2))

    def test_shell_convolution_and_dissipative_cap(self):
        head = {1: Fraction(1, 100), 2: Fraction(1, 100)}
        bound = shell_convolution_bound(4, head, Fraction(1, 1000), Fraction(2), 3)
        self.assertGreater(bound, 0)
        certificate = check_dissipative_shell_cap(
            head,
            Fraction(1, 1000),
            Fraction(2),
            3,
            Fraction(1),
            {3: Fraction(1, 10000), 4: Fraction(1, 20000)},
        )
        self.assertEqual(len(certificate.finite_margins), 3)
        self.assertGreaterEqual(certificate.ray_coefficients[0], 0)

    def test_angular_pairing_cancels_equal_euclidean_shells(self):
        self.assertEqual(paired_vorticity_coefficient((1, 0), (0, 1)), 0)
        self.assertEqual(
            paired_vorticity_coefficient((1, 0), (1, 1)), Fraction(-1, 4)
        )

    def test_analytic_enstrophy_improves_tail_tail_bound(self):
        head = {1: Fraction(1, 100), 2: Fraction(1, 100)}
        cap = Fraction(1)
        rho = Fraction(2)
        coarse = shell_convolution_bound(8, head, cap, rho, 3)
        analytic = shell_convolution_bound(
            8,
            head,
            cap,
            rho,
            3,
            weighted_enstrophy=Fraction(1, 10000),
            analytic_order=2,
        )
        self.assertLess(analytic, coarse)
        self.assertGreater(
            analytic_enstrophy_tail_bound(8, 3, rho, Fraction(1, 10000)), 0
        )
        coarse_ray = check_dissipative_shell_cap(
            head, Fraction(1, 1000), rho, 3, Fraction(1)
        )
        analytic_ray = check_dissipative_shell_cap(
            head,
            Fraction(1, 1000),
            rho,
            3,
            Fraction(1),
            weighted_enstrophy=Fraction(1, 10000),
            analytic_order=2,
        )
        self.assertGreater(
            analytic_ray.ray_coefficients[0], coarse_ray.ray_coefficients[0]
        )

    def test_shell_convolution_dominates_direct_truncation(self):
        head = {1: Fraction(2, 5), 2: Fraction(1, 3)}
        cap = Fraction(1, 7)
        rho = Fraction(3, 2)
        masses = dict(head)
        for index in range(3, 13):
            masses[index] = cap * rho ** (-index)
        for target in range(1, 9):
            direct = Fraction(0)
            for a, mass_a in masses.items():
                for b, mass_b in masses.items():
                    if abs(a - b) <= target <= a + b:
                        direct += 2 * Fraction(b, a) * mass_a * mass_b
            self.assertLessEqual(
                direct, shell_convolution_bound(target, head, cap, rho, 3)
            )

    def test_shell_cap_rejects_outward_face(self):
        head = {1: Fraction(10), 2: Fraction(10)}
        with self.assertRaisesRegex(ValueError, "not inward"):
            check_dissipative_shell_cap(
                head, Fraction(1), Fraction(2), 3, Fraction(1, 1000)
            )

    def test_low_mode_remainder_excludes_retained_pairs(self):
        head = {1: Fraction(1), 2: Fraction(1), 3: Fraction(1)}
        full = shell_convolution_bound(1, head, Fraction(1, 100), Fraction(2), 4)
        remainder = low_mode_tail_remainder_bound(
            1, 2, head, Fraction(1, 100), Fraction(2), 4
        )
        self.assertGreater(full, remainder)
        self.assertGreater(remainder, 0)

    def test_picard_rejects_uncontained_tube(self):
        modes = retained_modes(1)
        entry = {k: CInterval.point(1) for k in modes}
        tiny = {
            k: CInterval(Interval(Fraction(99, 100), Fraction(101, 100)), Interval.point(0))
            for k in modes
        }
        remainder = {k: CInterval.point() for k in modes}
        with self.assertRaises(ValueError):
            check_picard_box(entry, tiny, remainder, Fraction(1), Fraction(1), tiny)

    def test_picard_rejects_bad_endpoint_keys_and_nonreal_remainder(self):
        modes = retained_modes(1)
        zero = {k: CInterval.point() for k in modes}
        wide = {
            k: CInterval(Interval(-1, 1), Interval(-1, 1)) for k in modes
        }
        missing = dict(wide)
        missing.pop(next(iter(modes)))
        with self.assertRaisesRegex(ValueError, "incompatible Picard data"):
            check_picard_box(zero, wide, zero, Fraction(1), Fraction(1, 10), missing)

        nonreal = dict(zero)
        nonreal[(1, 0)] = CInterval.point(0, 1)
        with self.assertRaisesRegex(ValueError, "reality"):
            check_picard_box(zero, wide, nonreal, Fraction(1), Fraction(1, 10), wide)

    def test_full_manifest_fails_closed(self):
        manifest = {
            "format": "cycle212-component-v1",
            "mode": "full",
            "normalization": "T2-2pi-normalized-vorticity-v1",
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps(manifest), encoding="ascii")
            with self.assertRaisesRegex(ValueError, "shell comparison"):
                load_manifest(path)

    def test_unknown_manifest_key_rejected(self):
        manifest = {
            "format": "cycle212-component-v1",
            "mode": "components",
            "normalization": "T2-2pi-normalized-vorticity-v1",
            "unchecked": True,
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps(manifest), encoding="ascii")
            with self.assertRaisesRegex(ValueError, "unknown"):
                load_manifest(path)


if __name__ == "__main__":
    unittest.main()
