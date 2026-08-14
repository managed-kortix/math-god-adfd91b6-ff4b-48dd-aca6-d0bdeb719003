import importlib.util
import unittest
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order12_structural_owners.py")
SPEC = importlib.util.spec_from_file_location("order12_owners", PATH)
OWNERS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OWNERS)


class ThreeRayOwnerTests(unittest.TestCase):
    def test_simple_edge_table(self):
        self.assertEqual(OWNERS.three_ray_edge_cost(1, 0, 0, 0), 0)
        self.assertIsNone(OWNERS.three_ray_edge_cost(1, 1, 0, 0))
        self.assertEqual(OWNERS.three_ray_edge_cost(1, 0, 0, 2), 27)
        self.assertEqual(OWNERS.three_ray_edge_cost(1, 1, 0, 2), 6)

    def test_parallel_paths_are_aggregated(self):
        self.assertEqual(OWNERS.three_ray_edge_cost(2, 0, 0, 2), 54)
        self.assertEqual(OWNERS.three_ray_edge_cost(2, 1, 0, 2), 33)
        self.assertEqual(OWNERS.three_ray_edge_cost(2, 2, 0, 2), 8)

    def test_all_cubic_multikernels_are_admitted(self):
        edges = ((0, 1, 2), (0, 2, 1), (1, 3, 1), (2, 3, 2))
        old_order = OWNERS.ORDER
        old_paths = OWNERS.PATH_COUNT
        try:
            OWNERS.ORDER = 4
            OWNERS.PATH_COUNT = 6
            self.assertTrue(OWNERS.cubic_kernel(edges))
            self.assertTrue(OWNERS.signed_three_ray_owner(edges, (0, 0, 0, 0)))
            witness = OWNERS.signed_three_ray_witness(edges, (0, 0, 0, 0))
            self.assertEqual(OWNERS.three_ray_witness_cost(
                edges, (0, 0, 0, 0), witness), 0)
        finally:
            OWNERS.ORDER = old_order
            OWNERS.PATH_COUNT = old_paths

    def test_signed_cut_characterization(self):
        edges = ((0, 1, 2),)
        old_order = OWNERS.ORDER
        old_paths = OWNERS.PATH_COUNT
        try:
            OWNERS.ORDER = 2
            OWNERS.PATH_COUNT = 2
            for odd in range(3):
                witness = OWNERS.generalized_three_ray_witness(edges, (odd,))
                self.assertIsNotNone(witness)
                self.assertLessEqual(OWNERS.three_ray_witness_cost(
                    edges, (odd,), witness), 108)
            self.assertIsNone(OWNERS.three_ray_witness_cost(
                edges, (0,), (0, 1)))
        finally:
            OWNERS.ORDER = old_order
            OWNERS.PATH_COUNT = old_paths

    def test_all_cost_six_atom_profiles_pass_the_filter(self):
        for mixed, optional_counts in OWNERS.ATOM_OPTIONAL_COUNTS.items():
            for optional in optional_counts:
                edges = [(index, index + 1, 2) for index in range(mixed)]
                row = [1] * mixed
                edges.extend((100 + index, 101 + index, 1)
                             for index in range(optional))
                row.extend([1] * optional)
                self.assertTrue(OWNERS.atom_profile_candidate(edges, row))

    def test_report_verifier_checks_partition(self):
        payload = {
            "schema": OWNERS.SCHEMA,
            "full_theorem": False,
            "scope": "test",
            "chunks": [],
            "scanned_residual_total": 1,
            "scanned_target_total": 19,
            "exclusive_owner_row_counts": {lane: int(index == 0)
                                             for index, lane in enumerate(OWNERS.LANES)},
            "cubic_cycle_space_candidate_counts": {},
            "atom_profile_owner_counts": {},
            "recognized_residual_total": 1,
            "recognized_target_total": 19,
            "rational_search_residual_total": 0,
            "rational_search_target_total": 0,
            "rational_search_source_indices_sha256": "0" * 64,
            "rational_search_index_artifact": None,
            "classification_stream_sha256": "0" * 64,
        }
        OWNERS.verify_report(payload)
        payload["recognized_target_total"] = 18
        with self.assertRaises(RuntimeError):
            OWNERS.verify_report(payload)


if __name__ == "__main__":
    unittest.main()
