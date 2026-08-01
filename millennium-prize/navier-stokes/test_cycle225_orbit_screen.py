import json
import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parent


class Cycle225OrbitScreenTest(unittest.TestCase):
    def test_deterministic_floating_protocol_smoke(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = pathlib.Path(tmp) / "cycle225-orbit"
            outputs = [pathlib.Path(tmp) / f"run-{index}.json" for index in range(2)]
            subprocess.run(
                ["g++", "-O2", "-std=c++20", str(ROOT / "cycle225_orbit_screen.cpp"),
                 "-o", str(binary)],
                check=True,
            )
            for output in outputs:
                subprocess.run(
                    [str(binary), "--n", "128", "--steps-per-unit", "16",
                     "--final-time", "0.0625", "--output", str(output)],
                    check=True,
                )

            self.assertEqual(outputs[0].read_bytes(), outputs[1].read_bytes())
            data = json.loads(outputs[0].read_text(encoding="ascii"))
            self.assertEqual(data["status"], "FLOATING_GALERKIN_SCREEN_ONLY")
            self.assertFalse(data["pde_certificate"])
            self.assertEqual(data["floating_label"], "N128 dt1/16 T0.0625")
            self.assertEqual(data["method"], "square_two_thirds_pseudospectral_euler_ab2")
            self.assertEqual(data["n"], 128)
            self.assertEqual(data["dt"], "1/16")
            self.assertEqual(data["checkpoint_spacing"], "1/16")
            self.assertGreater(data["endpoint_l3_ratio"], 0.0)
            self.assertGreaterEqual(data["maximum_checkpoint_l3_ratio"], 1.0)
            self.assertGreaterEqual(data["energy_relative_drift"], 0.0)
            self.assertGreaterEqual(data["enstrophy_relative_drift"], 0.0)


if __name__ == "__main__":
    unittest.main()
