import json
import pathlib
import sys
import unittest

import numpy as np


ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from scout_cycle258_integrated_l3 import (
    Euler2D,
    compare_reports,
    frozen_family,
    screen,
)


class Cycle258IntegratedL3Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads(
            (ROOT / "cycle257-initial-l3-candidates.json").read_text(encoding="ascii")
        )

    def test_frozen_family_constraints(self):
        modes, family = frozen_family(self.source)
        self.assertEqual(len(family), 45)
        weights = 0.5 * np.repeat(
            [kx * kx + ky * ky for kx, ky in modes], 2
        )
        k2 = 2.0 * weights
        for label, x in family:
            energy = np.sum(weights * x * x)
            enstrophy = np.sum(weights * k2 * x * x)
            self.assertAlmostEqual(energy, 1.0, places=12)
            self.assertAlmostEqual(enstrophy / energy, label.rho, places=11)

    def test_real_initial_field(self):
        modes, family = frozen_family(self.source)
        solver = Euler2D(64)
        omega = solver.initial(modes, family[-1][1])
        self.assertLess(np.max(np.abs(np.fft.ifft2(omega).imag)), 1e-12)

    def test_short_integral_identity_and_determinism(self):
        kwargs = dict(n=64, dt=1.0 / 64.0, final_time=1.0 / 32.0,
                      sample_dt=1.0 / 64.0, limit=1)
        first = screen(self.source, **kwargs)
        second = screen(self.source, **kwargs)
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "NUMERICAL_SCOUT_ONLY")
        self.assertFalse(first["pde_certificate"])
        self.assertLess(
            first["results"][0]["max_integral_identity_discrepancy"], 1e-5
        )

    def test_cross_resolution_comparison(self):
        kwargs = dict(dt=1.0 / 64.0, final_time=1.0 / 64.0,
                      sample_dt=1.0 / 64.0, limit=1)
        coarse = screen(self.source, n=64, **kwargs)
        fine = screen(self.source, n=128, **kwargs)
        comparison = compare_reports(coarse, fine)
        self.assertEqual(comparison["family_size"], 1)
        self.assertFalse(comparison["pde_certificate"])
        self.assertEqual(comparison["comparisons"][0]["family_index"], 0)


if __name__ == "__main__":
    unittest.main()
