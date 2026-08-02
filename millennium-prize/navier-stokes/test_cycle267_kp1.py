import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parent


class Cycle267KP1Tests(unittest.TestCase):
    def test_frozen_manifest_and_outcome(self):
        manifest = json.loads((ROOT / "cycle267-kp1-manifest.json").read_text())
        outcome = json.loads((ROOT / "cycle267-kp1-outcome.json").read_text())
        self.assertEqual(manifest["status"], "FROZEN_BEFORE_TRAJECTORY_COMPUTE")
        self.assertEqual(manifest["profile"]["name"], "K-F(K)/32")
        self.assertEqual([level["cubic_cutoff"] for level in manifest["levels"]], [7, 10])
        self.assertEqual(manifest["integrator"]["method"], "implicit_midpoint")
        self.assertEqual(manifest["resource_policy"]["maximum_cores"], 2)
        self.assertEqual(outcome["status"], "NUMERICAL_ONLY")
        self.assertFalse(outcome["pde_certificate"])
        self.assertTrue(outcome["all_cross_resolution_gates_pass"])
        self.assertEqual(outcome["architecture_signal_promotions"], [])
        self.assertEqual(outcome["certification_promotions"], [])
        for level in outcome["levels"].values():
            self.assertTrue(level["all_local_gates_pass"])
        fine = outcome["levels"]["K10"]["endpoints"]
        maximum = max(row["directed_ratios"]["64"] for row in fine.values())
        self.assertLess(maximum, manifest["promotion"]["architecture_signal_threshold"])


if __name__ == "__main__":
    unittest.main()
