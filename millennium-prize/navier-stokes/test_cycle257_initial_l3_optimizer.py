import json
import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parent


class Cycle257InitialL3OptimizerTest(unittest.TestCase):
    def test_exact_gradient_and_constraints(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = pathlib.Path(tmp) / "optimizer"
            output = pathlib.Path(tmp) / "candidate.json"
            subprocess.run(
                ["g++", "-O2", "-std=c++20", "-Wall", "-Wextra", "-pedantic",
                 str(ROOT / "cycle257_initial_l3_optimizer.cpp"), "-o", str(binary)],
                check=True,
            )
            subprocess.run(
                [str(binary), "--max-wave", "3", "--grid", "32", "--starts", "2",
                 "--iterations", "4", "--rho", "5", "--output", str(output)],
                check=True,
            )
            data = json.loads(output.read_text(encoding="ascii"))
            self.assertEqual(data["status"], "FLOATING_CANDIDATE_BOXES_ONLY")
            self.assertFalse(data["pde_certificate"])
            candidate = data["candidates"][0]
            self.assertEqual(candidate["rho"], 5)
            self.assertLess(candidate["directional_gradient_relative_error"], 1e-6)
            self.assertLess(
                abs(candidate["objective"] - candidate["double_grid_objective"]),
                5e-4,
            )


if __name__ == "__main__":
    unittest.main()
