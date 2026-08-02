import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from cycle266_kida_direction import report


class Cycle266KidaDirectionTests(unittest.TestCase):
    def test_exact_tangent_and_positive_direction(self):
        data = report()
        self.assertEqual(data["coefficient_a_in_cycle265_parameterization"], -2)
        self.assertEqual(data["coefficient_b_in_cycle265_parameterization"], 0)
        for value in data["kida_constraint_variations_along_minus_F"].values():
            self.assertLess(abs(value), 1e-12)
        for row in data["grids"]:
            self.assertGreater(row["directional_derivative_at_kida_along_minus_F"], 1.12)
            self.assertGreater(row["candidate_l3_cube_derivative"], 0.035)
            self.assertGreater(row["candidate_log_l3_derivative"], 0.012)
        values = [row["candidate_l3_cube_derivative"] for row in data["grids"]]
        self.assertLess(max(values) - min(values), 2e-5)


if __name__ == "__main__":
    unittest.main()
