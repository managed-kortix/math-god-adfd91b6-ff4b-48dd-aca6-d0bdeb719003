import pathlib
import sys
import unittest

import numpy as np


ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from scout_cycle265_3d_alignment import FAMILY, Galerkin3D, initial_state


class Cycle265AlignmentTests(unittest.TestCase):
    def test_frozen_family_is_small_and_genuinely_3d(self):
        self.assertEqual(len(FAMILY), 4)
        solver = Galerkin3D(5)
        for member in FAMILY:
            state = initial_state(solver, member)
            self.assertLess(max(solver.defects(state).values()), 2e-12)
            for component in range(3):
                self.assertGreater(np.linalg.norm(state[component]), 1e-3)
            for axis in range(3):
                active = np.any(np.abs(state) > 1e-12, axis=0)
                collapsed = np.any(active, axis=tuple(i for i in range(3) if i != axis))
                self.assertGreater(np.count_nonzero(collapsed), 1)

    def test_rhs_is_tangent_to_energy_and_helicity(self):
        solver = Galerkin3D(5)
        state = initial_state(solver, FAMILY[2])
        tangent = solver.rhs(state)
        energy_tangent = abs(np.real(np.vdot(state, tangent)))
        helicity_tangent = abs(np.real(np.vdot(solver.curl(state), tangent)))
        self.assertLess(energy_tangent, 1e-12)
        self.assertLess(helicity_tangent, 1e-12)

    def test_midpoint_step_preserves_quadratic_invariants(self):
        solver = Galerkin3D(5)
        state = initial_state(solver, FAMILY[0])
        energy0, helicity0 = solver.energy(state), solver.helicity(state)
        endpoint, residual, _ = solver.midpoint_step(state)
        self.assertLessEqual(residual, 1e-11)
        self.assertLess(abs(solver.energy(endpoint) - energy0), 1e-10)
        self.assertLess(abs(solver.helicity(endpoint) - helicity0), 1e-10)


if __name__ == "__main__":
    unittest.main()
