import json
import pathlib
import subprocess
import unittest
import tempfile


ROOT = pathlib.Path(__file__).resolve().parent


class ScreenTest(unittest.TestCase):
    def test_small_screen(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = pathlib.Path(tmp) / "screen"
            output = pathlib.Path(tmp) / "result.json"
            subprocess.run(
                ["g++", "-O2", "-std=c++20", str(ROOT / "cycle212_screen.cpp"), "-o", str(binary)],
                check=True,
            )
            subprocess.run(
                [
                    str(binary),
                    "--proxy-keep", "8",
                    "--candidate-keep", "1",
                    "--coarse-n", "16",
                    "--coarse-steps", "16",
                    "--fine-n", "16",
                    "--fine-steps", "16",
                    "--fine-keep", "1",
                    "--final-time", "0.0625",
                    "--output", str(output),
                ],
                check=True,
            )
            data = json.loads(output.read_text())
            self.assertEqual(data["status"], "NUMERICS_SCREENING_ONLY")
            self.assertFalse(data["rigorous_interval_certificate"])
            self.assertEqual(data["enumeration"]["raw_nonzero"], 5**10 - 1)
            self.assertGreater(data["enumeration"]["nonlinear"], 0)
            self.assertEqual(len(data["coarse_ranked"]), 7)
            self.assertGreater(data["fine_reruns"][0]["max_ratio"], 0)


if __name__ == "__main__":
    unittest.main()
