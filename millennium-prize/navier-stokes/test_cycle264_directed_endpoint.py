import json
import pathlib
import sys
import unittest

import numpy as np


ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from screen_cycle264_directed_endpoint import PaddedGalerkin, initial_state


class Cycle264DirectedEndpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads(
            (ROOT / "cycle264-variational-centers.json").read_text(encoding="ascii")
        )

    def test_family_is_fresh_and_finite(self):
        self.assertEqual([row["rho"] for row in self.source["candidates"]], [6, 10, 14])
        self.assertEqual(self.source["max_wave"], 4)
        self.assertEqual(len(self.source["candidates"]), 3)

    def test_initial_constraints(self):
        modes = self.source["modes"]
        weights = 0.5 * np.repeat(
            [kx * kx + ky * ky for kx, ky in modes], 2
        )
        k2 = 2.0 * weights
        for candidate in self.source["candidates"]:
            coefficients = np.asarray(candidate["coefficients"])
            energy = np.sum(weights * coefficients**2)
            enstrophy = np.sum(weights * k2 * coefficients**2)
            self.assertAlmostEqual(energy, 1.0, places=12)
            self.assertAlmostEqual(enstrophy / energy, candidate["rho"], places=11)

    def test_one_midpoint_step_residual_and_invariants(self):
        solver = PaddedGalerkin(15)
        state = initial_state(
            solver,
            self.source["modes"],
            self.source["candidates"][0]["coefficients"],
        )
        before = [solver.invariant(state, name) for name in ("energy", "enstrophy")]
        endpoint, _, _, _, _, residual_ratio = solver.midpoint_step(state)
        after = [solver.invariant(endpoint, name) for name in ("energy", "enstrophy")]
        self.assertLessEqual(residual_ratio, 5e-12)
        for left, right in zip(before, after):
            self.assertLess(abs(right / left - 1.0), 1e-10)


if __name__ == "__main__":
    unittest.main()
