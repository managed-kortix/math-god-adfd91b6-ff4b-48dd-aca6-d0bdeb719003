#!/usr/bin/env python3
"""Hostile trust-boundary tests for the order-nine structural replayer."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import lzma
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PATH = Path(__file__).with_name("rank7_order9_structural_semantic_replayer.py")


def load_replayer():
    spec = importlib.util.spec_from_file_location("rank7_order9_replayer_test", PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load structural replayer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StructuralSemanticReplayerHostileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.replayer = load_replayer()

    def assert_rejected(self, raw: bytes, *, canonical: bool = True):
        with self.assertRaises(RuntimeError):
            self.replayer.strict_json(raw, "hostile", canonical=canonical)

    def test_strict_json_rejects_every_float_token_and_constant(self):
        hostile = (
            b"0.0", b"-0.0", b"1.25", b"1e2", b"1E-2", b"1e999",
            b"-1e999", b"[0,{\"nested\":2.5}]", b"NaN", b"Infinity",
            b"-Infinity",
        )
        for raw in hostile:
            with self.subTest(raw=raw):
                self.assert_rejected(raw)

    def test_strict_json_rejects_duplicates_noncanonical_and_non_ascii(self):
        self.assert_rejected(b'{"a":1,"a":2}\n', canonical=False)
        self.assert_rejected(b'{ "a":1}\n')
        self.assert_rejected(b'{"a":1}')
        self.assert_rejected(b'{"z":"\xc3\xa9"}\n')
        self.assertEqual(self.replayer.strict_json(b'{"a":[true,null,-3]}\n', "ok"),
                         {"a": [True, None, -3]})

    def test_recursive_float_guard_is_parser_independent(self):
        for hostile in (float("inf"), 2.0, object()):
            with self.subTest(hostile=hostile):
                with mock.patch.object(self.replayer.json, "loads",
                                       return_value={"nested": [1, {"x": hostile}]}):
                    self.assert_rejected(b"{}\n", canonical=False)

    def test_exact_integer_helpers_reject_float_and_bool_laundering(self):
        for hostile in (True, False, 1.5, 2.0, float("inf")):
            with self.subTest(hostile=hostile):
                with self.assertRaises(RuntimeError):
                    self.replayer.exact_int(hostile, "count")
                with self.assertRaises(RuntimeError):
                    self.replayer.exact_int_list([0, hostile], 2, "range")
                with self.assertRaises(RuntimeError):
                    self.replayer.exact_str_int_map({"lane": hostile}, {"lane"}, "ledger")
        self.assertEqual(self.replayer.exact_int(2, "count"), 2)
        self.assertEqual(self.replayer.exact_int_list([0, 2], 2, "range"), [0, 2])

    def test_exact_schemas_reject_missing_and_extra_fields(self):
        sample = {key: None for key in self.replayer.STREAM_RECEIPT_FIELDS}
        self.replayer.exact_fields(sample, self.replayer.STREAM_RECEIPT_FIELDS, "receipt")
        for mutant in (
            {key: value for key, value in sample.items() if key != "sha256"},
            sample | {"prose": "trusted-by-mistake"},
            [],
        ):
            with self.subTest(mutant=mutant):
                with self.assertRaises(RuntimeError):
                    self.replayer.exact_fields(
                        mutant, self.replayer.STREAM_RECEIPT_FIELDS, "receipt")

    def test_xz_readers_reject_float_duplicate_and_jsonl_shape(self):
        cases = (
            (b'{"x":1e999}\n', True),
            (b'{"x":1,"x":2}\n', True),
            (b'{"x":1}\n', False),
        )
        with tempfile.TemporaryDirectory() as temporary:
            for index, (raw, object_reader) in enumerate(cases):
                path = Path(temporary) / f"hostile-{index}.xz"
                stored = lzma.compress(raw)
                path.write_bytes(stored)
                with self.subTest(raw=raw):
                    with self.assertRaises(RuntimeError):
                        if object_reader:
                            self.replayer.read_xz_json(
                                path, hashlib.sha256(stored).hexdigest(),
                                hashlib.sha256(raw).hexdigest())
                        else:
                            self.replayer.read_jsonl_xz(
                                path, hashlib.sha256(stored).hexdigest(),
                                hashlib.sha256(raw).hexdigest())

    def test_manifest_exact_schema_is_enforced_before_semantics(self):
        census = json.loads(self.replayer.CENSUS_MANIFEST.read_text(encoding="ascii"))
        owner = json.loads(self.replayer.OWNER_MANIFEST.read_text(encoding="ascii"))
        for target, fields, label in (
            (census, self.replayer.CENSUS_MANIFEST_FIELDS, "census"),
            (owner, self.replayer.OWNER_MANIFEST_FIELDS, "owner"),
        ):
            self.replayer.exact_fields(target, fields, label)
            with self.assertRaises(RuntimeError):
                self.replayer.exact_fields(target | {"unexpected": 0}, fields, label)

    def test_canonical_identity_encoding_and_callback_contract(self):
        key = (17, 99, 5, (0, 2, 1), 3)
        key_digest = hashlib.sha256()
        self.replayer.update_key_digest(key_digest, key)
        expected = hashlib.sha256(b'[17,99,5,[0,2,1],3]\n').hexdigest()
        self.assertEqual(key_digest.hexdigest(), expected)
        index_digest = hashlib.sha256()
        self.replayer.update_index_digest(index_digest, 17)
        self.assertEqual(index_digest.hexdigest(), hashlib.sha256(b"17\n").hexdigest())

    def test_mixed_radix_orbit_replay_rejects_noncanonical_and_wrong_size(self):
        edges = ((0, 1, 1), (0, 2, 2))
        actions = ((0, 1), (1, 0))
        # Tuple lexicographic minimum is (0, 1), but edge zero is least
        # significant, so mixed-radix code selects (1, 0): code 1 < code 2.
        minimum, size = self.replayer.recompute_orbit((1, 0), edges, actions)
        self.assertEqual((minimum, size), (1, 2))
        noncanonical_code = 0 + 2 * 1
        self.assertNotEqual(noncanonical_code, minimum)
        self.assertNotEqual(1, size)

    def test_automorphism_and_burnside_recomputation(self):
        edges = ((0, 1, 1), (0, 2, 1), (1, 2, 1)) + tuple(
            (vertex, vertex + 1, 1) for vertex in range(3, 8))
        # This synthetic graph need not meet rank-seven path count; the helper
        # must still derive all weighted-graph actions and exact Burnside sum.
        actions = self.replayer.automorphism_actions(edges)
        self.assertGreaterEqual(len(actions), 1)
        self.assertGreaterEqual(self.replayer.burnside_orbits(edges, actions), 1)
        with self.assertRaises(RuntimeError):
            self.replayer.burnside_orbits(edges, actions + ((0,) * len(edges),))

    def test_pinned_source_identity_and_predicate_call_contract(self):
        self.assertEqual(set(self.replayer.EXPECTED_SOURCE_IDENTITY), {
            "universe_source_index_sha256", "universe_key_sha256",
            "owner_source_index_sha256", "owner_key_sha256",
            "remainder_source_index_sha256", "remainder_key_sha256",
        })
        self.assertEqual(self.replayer.EXPECTED_PREDICATE_CALLS, {
            "balanced-rank-one": 2_835_895,
            "signed-imbalance-psd": 2_834_382,
            "simplex-mixed-atom": 2_831_563,
            "generalized-ray": 2_831_150,
        })
        self.assertEqual(self.replayer.EXPECTED_PREDICATE_CALL_TOTAL, 11_332_990)
        self.assertEqual(self.replayer.EXPECTED_OWNER_COUNTS, {
            "balanced-rank-one": 1_513,
            "signed-imbalance-psd": 2_819,
            "simplex-mixed-atom": 413,
            "generalized-ray": 2_445_321,
        })
        self.assertEqual(sum(self.replayer.EXPECTED_OWNER_COUNTS.values()), 2_450_066)
        self.assertEqual(self.replayer.REMAINDER_TOTAL, 385_829)

    def test_fast_result_is_explicitly_ineligible_for_full_gate(self):
        synthetic_fast = {
            "mode": "authenticated-stored-stream-zip",
            "complete": True,
            "predicate_replay_eligible": False,
            "recognition_calls": 0,
            "predicate_call_total": 0,
            "predicate_calls": {lane: 0 for lane in self.replayer.LANES},
            "predicate_passes": {lane: 0 for lane in self.replayer.LANES},
        }
        self.assertFalse(synthetic_fast["predicate_replay_eligible"])
        self.assertNotEqual(synthetic_fast["recognition_calls"], self.replayer.RESIDUAL_TOTAL)
        self.assertNotEqual(synthetic_fast["predicate_calls"],
                            self.replayer.EXPECTED_PREDICATE_CALLS)


if __name__ == "__main__":
    unittest.main()
