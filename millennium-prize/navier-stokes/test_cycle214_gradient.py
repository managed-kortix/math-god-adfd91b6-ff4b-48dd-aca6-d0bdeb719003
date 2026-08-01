import json
import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parent


class GradientScreenTest(unittest.TestCase):
    def test_small_gradient_pipeline(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = pathlib.Path(tmp) / "gradient"
            output = pathlib.Path(tmp) / "screen.json"
            subprocess.run(
                ["g++", "-O2", "-std=c++20", str(ROOT / "cycle214_gradient.cpp"),
                 "-o", str(binary)],
                check=True,
            )
            subprocess.run(
                [str(binary), "--seeds", "2", "--max-wave", "1",
                 "--n32", "8", "--n64", "8", "--steps", "16",
                 "--iterations32", "2", "--iterations64", "1",
                 "--promote", "0.5", "--output", str(output)],
                check=True,
            )
            data = json.loads(output.read_text())
            self.assertEqual(data["status"], "FLOATING_AUTOMATIC_GRADIENT_SCREEN")
            self.assertFalse(data["rigorous_interval_certificate"])
            self.assertEqual(data["method"]["gradient"],
                             "forward_tangent_discrete_rk4")
            self.assertEqual(data["method"]["parameters"], 8)
            self.assertEqual(len(data["candidates"]), 2)
            self.assertEqual(data["counts"]["promoted"], 2)
            self.assertEqual(data["best_resolution_checks"]["seed"],
                             data["candidates"][0]["seed"])
            self.assertGreater(data["best_resolution_checks"]["n8_steps16"], 0.0)
            self.assertGreater(data["best_resolution_checks"]["n8_steps32"], 0.0)
            for candidate in data["candidates"]:
                self.assertGreater(candidate["ratio32"], 0.0)
                self.assertGreater(candidate["ratio64"], 0.0)
                self.assertEqual(len(candidate["coefficients"]), 8)


if __name__ == "__main__":
    unittest.main()
