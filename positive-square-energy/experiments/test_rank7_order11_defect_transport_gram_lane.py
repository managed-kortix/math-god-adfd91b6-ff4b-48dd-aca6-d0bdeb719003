import importlib.util
import unittest
from fractions import Fraction
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order11_defect_transport_gram_lane.py")
SPEC = importlib.util.spec_from_file_location("order11_defect_transport", PATH)
LANE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LANE)


class DefectTransportGramTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest, _ = LANE.strict_json(LANE.MANIFEST_PATH)
        wrapper = LANE.load("order11_defect_test_owner", LANE.OWNER_ENGINE_PATH)
        owner = wrapper.load_owner_engine()
        cls.record, cls.kernel = next(LANE.stream_rows(manifest, owner, exclude_owned=True))

    def test_exact_defect_sequence_and_cycle_rank(self):
        self.assertEqual(sorted(self.kernel["degrees"], reverse=True), [4] + [3] * 10)
        self.assertEqual(sum(edge[2] for edge in self.kernel["edges"]) - LANE.ORDER + 1, 7)

    def test_transport_core_is_exact_psd(self):
        _, paths, _, _, _ = LANE.paths_types_family(
            self.kernel, tuple(self.record[3]))
        core = LANE.transport_core(paths)
        self.assertTrue(all(isinstance(value, Fraction) for row in core for value in row))
        for shift in range(LANE.ORDER):
            vector = [Fraction((index + shift) % 5 - 2) for index in range(LANE.ORDER)]
            quadratic = sum(vector[u] * core[u][v] * vector[v]
                            for u in range(LANE.ORDER) for v in range(LANE.ORDER))
            self.assertGreaterEqual(quadratic, 0)

    def test_search_replays_exact_rational_cost(self):
        cost, normalizer, parameters, cycle_weight, _, _ = LANE.search(
            self.kernel, tuple(self.record[3]), 32)
        self.assertTrue(cost is None or isinstance(cost, Fraction))
        self.assertIsInstance(normalizer, Fraction)
        self.assertTrue(all(isinstance(value, Fraction)
                            for parameter in parameters for value in parameter))
        self.assertIsInstance(cycle_weight, Fraction)


if __name__ == "__main__":
    unittest.main()
