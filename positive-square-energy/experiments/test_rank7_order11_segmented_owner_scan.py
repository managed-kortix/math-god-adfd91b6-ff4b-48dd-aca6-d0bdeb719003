import importlib.util
import unittest
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order11_segmented_owner_scan.py")
SPEC = importlib.util.spec_from_file_location("order11_segmented", PATH)
SCAN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCAN)


class OrderElevenSegmentedScannerTests(unittest.TestCase):
    def test_complete_kernel_partition_and_precedence(self):
        self.assertEqual(SCAN.RANGES[0][0], 0)
        self.assertEqual(SCAN.RANGES[-1][1], 1391)
        self.assertTrue(all(left[1] == right[0]
                            for left, right in zip(SCAN.RANGES, SCAN.RANGES[1:])))
        self.assertEqual(SCAN.CORE.LANES, SCAN.LANES)

    def test_recognizer_is_manifest_tool_recognizer(self):
        class Owner:
            @staticmethod
            def recognize_row(atom, edges, row):
                return "cubic-cycle-space-candidate", ["test"]

        self.assertEqual(
            SCAN.CORE.recognize_exact(Owner, None, (), ()),
            ("cubic-cycle-space-candidate", ["test"]),
        )

    def test_chunk_names_bind_exact_ranges(self):
        self.assertEqual(
            [SCAN.CORE.chunk_id(path)[1] for path in SCAN.DEFAULT_CHUNKS],
            [list(pair) for pair in SCAN.RANGES],
        )

    def test_checkpoint_binds_owner_precedence(self):
        identity = {"chunk_sha256": "a" * 64}
        payload = {
            "schema": SCAN.CORE.SEGMENT_SCHEMA,
            "identity": identity,
            "owner_precedence": list(SCAN.LANES),
            "row_range": [0, 1],
            "exclusive_owner_orbit_counts": {
                lane: int(lane == SCAN.LANES[0]) for lane in SCAN.LANES
            },
            "exclusive_owner_physical_counts": {
                lane: int(lane == SCAN.LANES[0]) for lane in SCAN.LANES
            },
            "remainder_orbit_total": 0,
            "remainder_physical_total": 0,
            "classification_stream_sha256": "0" * 64,
        }
        self.assertEqual(SCAN.CORE.validate_segment(payload, identity), 1)
        payload["owner_precedence"] = list(reversed(SCAN.LANES))
        with self.assertRaises(RuntimeError):
            SCAN.CORE.validate_segment(payload, identity)


if __name__ == "__main__":
    unittest.main()
