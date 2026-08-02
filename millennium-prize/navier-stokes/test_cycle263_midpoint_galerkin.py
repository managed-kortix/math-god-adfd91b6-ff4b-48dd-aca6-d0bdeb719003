#!/usr/bin/env python3
import unittest

from verify_cycle263_midpoint_galerkin import GalerkinEuler, synthetic_state, validate


class Cycle263MidpointGalerkinTests(unittest.TestCase):
    def test_conjugate_symmetry_and_rhs_replay(self):
        solver = GalerkinEuler(2)
        state = synthetic_state(solver)
        for mode in solver.representatives:
            value = state[solver.index[mode]]
            reflected = state[solver.index[(-mode[0], -mode[1])]]
            self.assertEqual(reflected, value.conjugate())
        discrepancy = solver.rhs(state) - solver.padded_rhs(state)
        self.assertLess(float(abs(discrepancy).max()), 1.0e-13)

    def test_frozen_validation(self):
        report = validate()
        self.assertTrue(report["passed"], report["failures"])
        self.assertFalse(report["cycle258_family_used"])


if __name__ == "__main__":
    unittest.main()
