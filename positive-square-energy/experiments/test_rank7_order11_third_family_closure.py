import importlib.util
import unittest
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order11_third_family_closure.py")
SPEC = importlib.util.spec_from_file_location("order11_third_closure", PATH)
CLOSURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLOSURE)
CLOSURE.configure()
ENGINE = CLOSURE.closure


class ThirdFamilyClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.failures, _ = ENGINE.read_failures()
        cls.kernels = ENGINE.collect_kernels(cls.failures)
        cls.payload, _, _ = ENGINE.read_json(ENGINE.OWNER_PATH, True)

    def test_exact_two_row_scope(self):
        self.assertEqual(len(self.failures), ENGINE.EXPECTED_FAILURES)
        self.assertEqual(self.payload["owner_total"], ENGINE.EXPECTED_FAILURES)

    def test_stronger_rational_grams_replay_exactly(self):
        ENGINE.verify_owners(self.payload["owners"], self.failures, self.kernels)

    def test_family_and_global_remainder_are_closed(self):
        report, _, _ = ENGINE.read_json(ENGINE.REPORT_PATH)
        self.assertEqual(report["combined_family_owner_total"], ENGINE.EXPECTED_FAMILY)
        self.assertEqual(report["remaining_family_total"], 0)
        self.assertEqual(report["updated_remainder_stream"]["record_total"], 10477105)
        self.assertEqual(report["updated_remainder_stream"]["physical_total"], 15035535)


if __name__ == "__main__":
    unittest.main()
