#!/usr/bin/env python3

import importlib.util
import itertools
import unittest
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order8_payload_free_lanes.py")
SPEC = importlib.util.spec_from_file_location("payload_free", PATH)
lanes = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lanes)


class PayloadFreeLaneTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atom = lanes.load_atom_recognizer()

    def test_balanced_rank_one(self):
        edges = tuple((i, (i + 1) % 7, 2) for i in range(7))
        self.assertTrue(lanes.balanced_rank_one(edges, (0,) * 7))
        self.assertFalse(lanes.balanced_rank_one(edges, (1,) + (0,) * 6))

    def test_signed_imbalance_dd_certificate(self):
        edges = tuple((i, (i + 1) % 7, 2) for i in range(7))
        certificate = lanes.signed_imbalance_certificate(edges, (0,) * 7)
        self.assertIsNotNone(certificate)
        denominator, targets = certificate
        self.assertGreaterEqual(denominator, 1)
        self.assertEqual(len(targets), 15)
        self.assertLessEqual(max(targets), lanes.BUDGET)

    def test_regular_k5_atom_at_order_eight(self):
        edges = [(u, v, 1) for u, v in itertools.combinations(range(5), 2)]
        edges += [(5, 6, 2), (6, 7, 2)]
        row = (1,) * 10 + (0, 0)
        owners = lanes.atom_owners(self.atom, tuple(edges), row)
        self.assertTrue(any(record["geometry"] == "regular-simplex-K5"
                            for record in owners))

    def test_report_arithmetic_rejects_mutation(self):
        report = {
            "schema": lanes.SCHEMA, "full_theorem": False, "scope": "test",
            "manifest_sha256": "0" * 64, "selected_chunks": [0],
            "scanned_residual_total": 1, "scanned_target_total": 15,
            "raw_lane_row_counts": {lane: int(lane == lanes.LANES[0]) for lane in lanes.LANES},
            "exclusive_owner_row_counts": {lane: int(lane == lanes.LANES[0])
                                           for lane in lanes.LANES},
            "overlap_row_counts": {}, "atom_profile_owner_counts": {},
            "recognized_residual_total": 1, "recognized_target_total": 15,
            "rational_search_residual_total": 0, "rational_search_target_total": 0,
            "classification_stream_sha256": "1" * 64,
        }
        lanes.verify_report(report)
        report["recognized_target_total"] = 14
        with self.assertRaises(RuntimeError):
            lanes.verify_report(report)


if __name__ == "__main__":
    unittest.main()
