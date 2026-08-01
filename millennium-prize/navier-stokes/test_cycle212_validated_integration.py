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
    analytic_velocity_bounds,
    check_picard_box,
    geometric_tail_sum,
    load_manifest,
    retained_modes,
    sqrt_interval,
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
