import json
import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parent


class ScreenTest(unittest.TestCase):
    def test_small_exhaustive_pipeline(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = pathlib.Path(tmp) / "screen"
            output = pathlib.Path(tmp) / "result.json"
            subprocess.run(
                ["g++", "-O2", "-std=c++20", "-pthread", str(ROOT / "cycle213_screen.cpp"),
                 "-o", str(binary)], check=True
            )
            subprocess.run(
                [str(binary), "--max-active", "12", "--threads", "2",
                 "--reduced-n", "8", "--reduced-steps", "16", "--reduced-time", "0.0625",
                 "--reduced-keep", "4", "--candidate-keep", "1", "--coarse-n", "8",
                 "--coarse-steps", "16", "--fine-n", "8", "--fine-steps", "16",
                 "--fine-keep", "1", "--final-time", "0.0625", "--output", str(output)],
                check=True,
            )
            data = json.loads(output.read_text())
            self.assertEqual(data["status"], "FLOATING_FINITE_FAMILY_SCREEN")
            self.assertFalse(data["rigorous_interval_certificate"])
            self.assertEqual(data["enumeration"]["integrated"], 12)
            self.assertEqual(data["method"]["reduced_retained"], 4)
            self.assertEqual(len(data["coarse_ranked"]), 7)
            self.assertIn("floating_maximum", data)


if __name__ == "__main__":
    unittest.main()
