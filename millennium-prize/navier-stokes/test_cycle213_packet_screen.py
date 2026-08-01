import json
import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parent


class PacketScreenTest(unittest.TestCase):
    def test_bidirectional_packet_screen(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = pathlib.Path(tmp) / "packet-screen"
            output = pathlib.Path(tmp) / "result.json"
            subprocess.run(
                ["g++", "-O2", "-std=c++20", str(ROOT / "cycle213_packet_screen.cpp"),
                 "-o", str(binary)], check=True
            )
            subprocess.run(
                [str(binary), "--samples", "2", "--n", "16", "--steps", "32",
                 "--fine-n", "16", "--fine-steps", "32", "--kmax", "4",
                 "--fine-keep", "1", "--final-time", "0.0625", "--seed", "213",
                 "--output", str(output)], check=True
            )
            data = json.loads(output.read_text())
            self.assertEqual(data["status"], "NUMERICS_SCREENING_ONLY")
            self.assertFalse(data["rigorous_interval_certificate"])
            self.assertEqual(data["method"]["directions"], 2)
            self.assertEqual(len(data["coarse_ranked"]), 4)
            self.assertIn(data["coarse_ranked"][0]["time_direction"], (-1, 1))
            self.assertGreater(data["best_fine_ratio"], 0)


if __name__ == "__main__":
    unittest.main()
