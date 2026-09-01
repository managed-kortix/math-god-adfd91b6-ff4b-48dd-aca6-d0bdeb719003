#!/usr/bin/env python3

import importlib.util
import unittest
from fractions import Fraction
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order10_cycle_leverage_signature_predicate.py")
SPEC = importlib.util.spec_from_file_location("rank7_order10_predicate_tested", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CycleLeverageSignaturePredicateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = MODULE.base.load("predicate_test_source", MODULE.base.weighted.SOURCE)
        cls.projector = MODULE.base.load(
            "predicate_test_projector", MODULE.base.weighted.PROJECTOR)
        cls.kernels = cls.source.kernel_dictionary()
        cls.report, _ = MODULE.strict_json(MODULE.SOURCE_REPORT)
        cls.winners, _, cls.records = MODULE.load_signature_winners(cls.report)

    def test_all_7807_owners_supply_signature_winners(self):
        self.assertEqual(len(self.records), 7807)
        self.assertEqual(len(self.winners), 28)
        self.assertTrue(all(rows for rows in self.winners.values()))

    def test_persisted_owner_replays_algebraic_predicate(self):
        record, _, signature = self.records[0]
        key = MODULE.json.dumps(signature, sort_keys=True, separators=(",", ":"))
        kernel = self.kernels[record[2]]
        accepted, result = MODULE.predicate(
            self.projector, kernel, tuple(record[3]), self.winners[key])
        self.assertTrue(accepted)
        self.assertIsInstance(result[0], Fraction)
        self.assertLessEqual(result[0], MODULE.base.BUDGET)

    def test_winner_profiles_are_nonnegative_resistance_functions(self):
        profiles = {key[3] for rows in self.winners.values() for key in rows}
        self.assertLessEqual(profiles, set(MODULE.base.PROFILES))


if __name__ == "__main__":
    unittest.main()
