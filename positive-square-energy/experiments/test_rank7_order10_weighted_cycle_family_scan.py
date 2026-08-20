#!/usr/bin/env python3

import importlib.util
import json
import unittest
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order10_weighted_cycle_family_scan.py")
SPEC = importlib.util.spec_from_file_location("rank7_order10_family_tested", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class WeightedCycleFamilyScanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = MODULE.weighted.load("family_test_source", MODULE.weighted.SOURCE)
        cls.manifest, _ = cls.source.strict_json(cls.source.MANIFEST)
        cls.kernels = cls.source.kernel_dictionary()
        cls.report, _ = MODULE.strict_json(MODULE.SOURCE_REPORT)

    def test_sample_stratification_recovers_all_pilot_owners(self):
        strata, selected, owners = MODULE.sample_stratification(
            self.source, self.kernels, self.manifest, self.report)
        self.assertEqual(sum(row["tested"] for row in strata), 10000)
        self.assertEqual(sum(row["owned"] for row in strata), 132)
        self.assertEqual(len(owners), 132)
        self.assertEqual(len(selected), 19)
        self.assertTrue(all(json.loads(key) for key in selected))

    def test_selected_signatures_have_exact_sample_ownership(self):
        strata, selected, _ = MODULE.sample_stratification(
            self.source, self.kernels, self.manifest, self.report)
        selected_payloads = {key for key in selected}
        selected_rows = [row for row in strata if json.dumps(
            row["signature"], sort_keys=True, separators=(",", ":"))
            in selected_payloads]
        self.assertTrue(selected_rows)
        self.assertTrue(all(row["owned"] == row["tested"]
                            for row in selected_rows))


if __name__ == "__main__":
    unittest.main()
