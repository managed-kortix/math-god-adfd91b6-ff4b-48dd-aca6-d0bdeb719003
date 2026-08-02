import pathlib
import sys
import unittest

import numpy as np


ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from scout_cycle257_multiscale_strain import Euler2D, Member, members


class MultiscaleStrainScoutTest(unittest.TestCase):
    def test_family_and_reality(self):
        self.assertEqual(len(members()), 5184)
        solver = Euler2D(32)
        omega = solver.initial(members()[1234])
        physical = np.fft.ifft2(omega)
        self.assertLess(np.max(np.abs(physical.imag)), 1e-12)

    def test_low_frequency_strain_is_self_induced(self):
        solver = Euler2D(32)
        member = Member(1.0, 0.0, 1.0 / 8.0, 0.0, 0, 0, 0)
        omega = solver.initial(member)
        self.assertLess(np.linalg.norm(solver.rhs(omega)), 1e-10)
        member = Member(2.0, 0.5, 1.0 / 8.0, 1.0 / 8.0, 0, 0, 0)
        self.assertGreater(np.linalg.norm(solver.rhs(solver.initial(member))), 1.0)

    def test_short_deterministic_screen(self):
        from scout_cycle257_multiscale_strain import screen

        first = screen(16, 1, 1.0 / 64.0, 1.0 / 32.0, 1.0 / 64.0)
        second = screen(16, 1, 1.0 / 64.0, 1.0 / 32.0, 1.0 / 64.0)
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "NUMERICAL_SCOUT_ONLY")
        self.assertFalse(first["pde_certificate"])


if __name__ == "__main__":
    unittest.main()
