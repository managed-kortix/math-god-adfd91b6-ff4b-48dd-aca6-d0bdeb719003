import pathlib
import sys
import unittest

import numpy as np


ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from scout_cycle259_patch_contours import (
    PeriodicContourSolver,
    diagnostics,
    geometries,
    initial_contours,
    screen,
)


class PatchContourScoutTest(unittest.TestCase):
    def test_deterministic_equal_area_family(self):
        self.assertEqual(len(geometries()), 24)
        for geometry in geometries():
            contours = initial_contours(geometry, 64)
            _, metrics = diagnostics(contours)
            self.assertLess(abs(metrics[0]["area"] / metrics[1]["area"] - 1.0), 1e-12)
            self.assertGreater(metrics[0]["area"], 0.0)

    def test_translation_and_rotation_do_not_change_shape_metrics(self):
        contours = initial_contours(geometries()[0], 64)
        _, before = diagnostics(contours)
        angle = 0.37
        rotation = np.array(
            ((np.cos(angle), -np.sin(angle)), (np.sin(angle), np.cos(angle)))
        )
        transformed = contours @ rotation.T + np.array((0.2, -0.1))
        _, after = diagnostics(transformed)
        for i in range(2):
            self.assertAlmostEqual(
                before[i]["isoperimetric_ratio"], after[i]["isoperimetric_ratio"], places=12
            )
            self.assertAlmostEqual(
                before[i]["normalized_mode3"], after[i]["normalized_mode3"], places=12
            )

    def test_rhs_and_l3_are_finite(self):
        solver = PeriodicContourSolver(24, kernel_grid=128, kernel_cutoff=24, velocity_grid=24)
        contours = initial_contours(geometries()[0], 24)
        self.assertTrue(np.all(np.isfinite(solver.rhs(contours))))
        self.assertGreater(solver.velocity_l3(contours), 0.0)

    def test_tiny_screen_is_deterministic(self):
        first = screen(16, 1.0 / 32.0, 1.0 / 32.0, 1.0 / 32.0, limit=1)
        second = screen(16, 1.0 / 32.0, 1.0 / 32.0, 1.0 / 32.0, limit=1)
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "NUMERICAL_SCOUT_ONLY")
        self.assertFalse(first["pde_certificate"])


if __name__ == "__main__":
    unittest.main()
