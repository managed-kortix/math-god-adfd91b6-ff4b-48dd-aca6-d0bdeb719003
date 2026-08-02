import json
import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parent


class IndependentScreenTest(unittest.TestCase):
    def test_small_reproducer(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = pathlib.Path(tmp) / "cycle255_screen"
            output = pathlib.Path(tmp) / "screen.json"
            subprocess.run(
                ["g++", "-O2", "-std=c++20", str(ROOT / "cycle255_independent_screen.cpp"),
                 "-o", str(binary)],
                check=True,
            )
            subprocess.run(
                [str(binary), "--n", "16", "--steps-per-unit", "16",
                 "--shortlist", "2", "--report", "2", "--output", str(output)],
                check=True,
            )
            data = json.loads(output.read_text())
            self.assertEqual(data["status"], "NUMERICAL_CANDIDATE_GENERATION_ONLY")
            self.assertFalse(data["pde_certificate"])
            self.assertEqual(data["family"]["profiles"], 781)
            self.assertEqual(data["family"]["shortlist"], 2)
            self.assertAlmostEqual(data["controls"][0]["ratio_at_1_over_16"], 1.0, places=12)
            self.assertLess(data["controls"][0]["rhs_relative_l2"], 1e-12)
            self.assertEqual(len(data["top_results"]), 2)


if __name__ == "__main__":
    unittest.main()
