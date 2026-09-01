import importlib.util
import unittest
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order11_leading_family_closure.py")
SPEC = importlib.util.spec_from_file_location("order11_leading_closure", PATH)
CLOSURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLOSURE)


class LeadingFamilyClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.failures, _ = CLOSURE.read_failures()
        cls.kernels = CLOSURE.collect_kernels(cls.failures)
        cls.payload, _, _ = CLOSURE.read_json(CLOSURE.OWNER_PATH, True)

    def test_exact_nine_row_scope(self):
        self.assertEqual(len(self.failures), CLOSURE.EXPECTED_FAILURES)
        self.assertEqual(self.payload["owner_total"], CLOSURE.EXPECTED_FAILURES)

    def test_all_shared_gram_witnesses_replay(self):
        CLOSURE.verify_owners(self.payload["owners"], self.failures, self.kernels)

    def test_family_is_closed(self):
        report, _, _ = CLOSURE.read_json(CLOSURE.REPORT_PATH)
        self.assertEqual(report["combined_family_owner_total"], CLOSURE.EXPECTED_FAMILY)
        self.assertEqual(report["remaining_family_total"], 0)


if __name__ == "__main__":
    unittest.main()
