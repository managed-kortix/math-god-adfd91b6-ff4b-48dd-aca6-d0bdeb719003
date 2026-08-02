import pathlib
import sys
import unittest
from fractions import Fraction


ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from cycle266_3dde1 import euler_rhs
from cycle266_kida_symmetry import (KidaOrbitLayout, c266_profile_field,
                                    profile_reduction_table, stabilizer)
class Cycle266KidaSymmetryTests(unittest.TestCase):
    def test_exact_profile_stabilizers_and_reduction_factors(self):
        rows = profile_reduction_table()
        self.assertEqual([row["group_order"] for row in rows], [96, 32, 96])
        self.assertEqual(rows[0]["levels"][7]["full_modes"], 3374)
        self.assertEqual(rows[0]["levels"][10]["full_modes"], 9260)
        for row in rows:
            for level in row["levels"].values():
                self.assertGreater(level["reduction_factor"], 6.9)

    def test_every_frozen_phase_has_one_of_the_two_orbit_classes(self):
        orders = set()
        for phase_bits in ((x, y, z) for x in range(2) for y in range(2) for z in range(2)):
            field = c266_profile_field(-2, Fraction(1, 4), phase_bits)
            orders.add(len(stabilizer(field)))
        self.assertEqual(orders, {32, 96})

    def test_exact_euler_convolution_is_closed_in_each_orbit_class(self):
        for phase_bits in ((0, 0, 0), (0, 1, 0), (1, 1, 1)):
            field = c266_profile_field(-2, Fraction(1, 4), phase_bits)
            group = set(stabilizer(field))
            self.assertLessEqual(group, set(stabilizer(euler_rhs(field))))

    def test_reduced_convolution_closes_and_matches_dealiased_rhs(self):
        try:
            import numpy as np
            from scout_cycle265_3d_alignment import Galerkin3D
        except ModuleNotFoundError:
            self.skipTest("NumPy is unavailable")

        cutoff = 3
        field = c266_profile_field(-2, 0, (0, 0, 0))
        layout = KidaOrbitLayout(cutoff, stabilizer(field))
        rng = np.random.default_rng(266)
        seed = rng.normal(size=(3, layout.width, layout.width, layout.width)).astype(complex)
        seed += 1j * rng.normal(size=seed.shape)
        seed = 0.5 * (seed + np.conj(seed[:, ::-1, ::-1, ::-1]))
        wave = np.stack(np.meshgrid(*([np.arange(-cutoff, cutoff + 1)] * 3), indexing="ij"))
        wave2 = np.sum(wave * wave, axis=0)
        dot = np.sum(wave * seed, axis=0)
        nonzero = wave2 != 0
        seed[:, nonzero] -= wave[:, nonzero] * dot[nonzero] / wave2[nonzero]
        seed[:, cutoff, cutoff, cutoff] = 0
        invariant = layout.project(seed)
        reduced = layout.compress(invariant)
        np.testing.assert_allclose(layout.expand(reduced), invariant, rtol=2e-12, atol=2e-12)
        reduced_rhs = layout.rhs(reduced)

        solver = Galerkin3D(cutoff)
        full_rhs = solver.rhs(invariant)
        np.testing.assert_allclose(reduced_rhs, layout.compress(full_rhs), rtol=2e-12, atol=2e-12)
        np.testing.assert_allclose(layout.expand(reduced_rhs), full_rhs, rtol=2e-12, atol=2e-12)


if __name__ == "__main__":
    unittest.main()
