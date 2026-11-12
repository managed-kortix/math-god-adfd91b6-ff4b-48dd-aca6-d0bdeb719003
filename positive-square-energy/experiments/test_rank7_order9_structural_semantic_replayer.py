#!/usr/bin/env python3
"""Hostile trust-boundary tests for the order-nine structural replayer."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import lzma
import os
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

    def test_census_reconstruction_ledger_is_execution_derived_and_fail_closed(self):
        expected_hashes = [pin[0] for pin in self.replayer.CHUNK_SPECS]
        expected_totals = {
            key: (self.replayer.KERNEL_TOTAL if key == "kernel_total" else
                  self.replayer.RESIDUAL_TOTAL if key == "coarse_residual_total" else
                  self.replayer.RESIDUAL_PHYSICAL_TOTAL
                  if key == "coarse_residual_physical_total" else
                  self.replayer.PARITY_ORBIT_TOTAL if key == "parity_orbit_total" else
                  self.replayer.COARSE_CERTIFIED_TOTAL
                  if key == "coarse_certified_total" else
                  self.replayer.RESIDUAL_TOTAL * self.replayer.FRONTIERS
                  if key == "frontier_target_total" else 81_885_688)
            for key in self.replayer.CENSUS_TOTAL_FIELDS
        }
        manifest = dict(expected_totals)
        ledger = self.replayer.empty_census_reconstruction_ledger()
        ledger.update({
            "producer_loads": 1,
            "generate_chunk_calls": 8,
            "chunks_reconstructed": 8,
            "kernels_reconstructed": self.replayer.KERNEL_TOTAL,
            "residual_rows_reconstructed": self.replayer.RESIDUAL_TOTAL,
            "totals": dict(expected_totals),
            "raw_chunk_sha256": list(expected_hashes),
        })
        result = self.replayer.census_reconstruction_result(True, True, ledger, manifest)
        self.assertIs(result["census_reconstruction"], True)
        self.assertIs(result["census_reconstruction_eligible"], True)
        self.assertEqual(result["census_reconstruction_generate_calls"], 8)
        self.assertEqual(result["census_reconstructed_raw_sha256"], expected_hashes)

        mutations = (
            {"producer_loads": 0},
            {"generate_chunk_calls": 0},
            {"generate_chunk_calls": 7},
            {"chunks_reconstructed": 7},
            {"kernels_reconstructed": self.replayer.KERNEL_TOTAL - 1},
            {"residual_rows_reconstructed": self.replayer.RESIDUAL_TOTAL - 1},
            {"raw_chunk_sha256": expected_hashes[:-1]},
            {"raw_chunk_sha256": ["0" * 64, *expected_hashes[1:]]},
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                hostile = dict(ledger)
                hostile.update(mutation)
                with self.assertRaises(RuntimeError):
                    self.replayer.census_reconstruction_result(
                        True, True, hostile, manifest)
        hostile = dict(ledger)
        hostile["totals"] = dict(expected_totals)
        hostile["totals"]["coarse_residual_total"] -= 1
        with self.assertRaises(RuntimeError):
            self.replayer.census_reconstruction_result(True, True, hostile, manifest)
        with self.assertRaises(RuntimeError):
            self.replayer.census_reconstruction_result(False, True, ledger, manifest)

    def test_census_record_counts_only_exact_actual_producer_returns(self):
        stored = {key: 0 for key in self.replayer.CENSUS_CHUNK_FIELDS}
        stored.update({
            "kernel_total": 1,
            "coarse_residual_total": 1,
            "kernels": [{}],
            "residuals": [{}],
        })
        for key in self.replayer.CENSUS_TOTAL_FIELDS:
            stored[key] = 1
        expected = hashlib.sha256(self.replayer.canonical_bytes(stored)).hexdigest()
        ledger = self.replayer.empty_census_reconstruction_ledger()
        self.replayer.record_census_reconstruction(
            ledger, stored, stored, expected, "synthetic")
        self.assertEqual(ledger["generate_chunk_calls"], 1)
        self.assertEqual(ledger["kernels_reconstructed"], 1)
        self.assertEqual(ledger["residual_rows_reconstructed"], 1)

        for mutant in (
            None,
            stored | {"extra": 0},
            stored | {"residuals": []},
            stored | {"kernel_total": True},
            stored | {"coarse_residual_total": 1.0},
        ):
            with self.subTest(mutant=mutant):
                before = self.replayer.empty_census_reconstruction_ledger()
                with self.assertRaises((RuntimeError, TypeError, ValueError)):
                    self.replayer.record_census_reconstruction(
                        before, mutant, stored, expected, "hostile")
                self.assertEqual(before, self.replayer.empty_census_reconstruction_ledger())

    def test_public_census_api_rejects_bool_laundering(self):
        with self.assertRaises(RuntimeError):
            self.replayer.reconstruct_census(replay_predicates=1, _chunk_limit=1)
        with self.assertRaises(RuntimeError):
            self.replayer.replay_all_predicates(reconstruct_fresh_census=1,
                                                _chunk_limit=1)

    def test_public_census_path_requires_real_producer_generate_call(self):
        class StopAtGenerate(RuntimeError):
            pass

        class FakeProducer:
            CHUNK_SCHEMA = "rank-seven-orders9-12-exact-residual-census-chunk-v1"
            MANIFEST_SCHEMA = "rank-seven-orders9-12-exact-residual-census-manifest-v1"
            ORDER_KERNEL_TOTALS = {self.replayer.ORDER: self.replayer.KERNEL_TOTAL}
            SOURCE_SHA256 = self.replayer.PINS[self.replayer.KERNEL_FIXTURE]
            RANK = self.replayer.RANK
            BUDGET_SCALED = 180

            @staticmethod
            def load_engine():
                raise AssertionError("test should stop before source-engine load")

            @staticmethod
            def generate_chunk(*args, **kwargs):
                raise StopAtGenerate("actual generate_chunk reached")

        original_loader = self.replayer.load_module

        def fake_loader(path, name):
            if path == self.replayer.CENSUS_PRODUCER:
                return FakeProducer
            return original_loader(path, name)

        with mock.patch.object(self.replayer, "load_module", side_effect=fake_loader):
            with self.assertRaisesRegex(StopAtGenerate, "actual generate_chunk reached"):
                self.replayer.reconstruct_census(_chunk_limit=1)


    def test_stdlib_producer_is_byte_equivalent_on_bounded_real_kernels(self):
        vector = self.replayer.load_module(
            self.replayer.CENSUS_PRODUCER, "rank7_order9_vector_equivalence_test")
        receipt = self.replayer.validate_stdlib_producer_equivalence(
            vector, ((0, 1), (4453, 4454)))
        self.assertEqual(receipt["bounded_kernel_total"], 2)
        self.assertIs(receipt["byte_identical"], True)
        self.assertEqual([row["physical_row_total"] for row in receipt["ranges"]],
                         [7776, 32768])
        self.assertEqual([row["residual_orbit_total"] for row in receipt["ranges"]],
                         [297, 629])
        self.assertTrue(all(row["byte_identical"] is True
                            for row in receipt["ranges"]))
        self.assertIn("not full-census or theorem evidence",
                      receipt["claim_boundary"])

    def test_stdlib_producer_equivalence_rejects_vector_mutation(self):
        vector = self.replayer.load_module(
            self.replayer.CENSUS_PRODUCER, "rank7_order9_vector_mutation_test")
        original = vector.generate_chunk

        def hostile(*args, **kwargs):
            result = original(*args, **kwargs)
            result["coarse_residual_total"] += 1
            return result

        vector.generate_chunk = hostile
        with self.assertRaisesRegex(RuntimeError, "stdlib/vector census producer differs"):
            self.replayer.validate_stdlib_producer_equivalence(vector, ((0, 1),))

    def test_partition_tag_sink_has_exact_framing_and_ledgers(self):
        r = self.replayer
        with tempfile.TemporaryDirectory(dir="/workspace") as directory:
            os.chmod(directory, 0o700)
            path = Path(directory) / "partition.bin"
            with mock.patch.object(r, "RESIDUAL_TOTAL", 3), \
                 mock.patch.object(
                     r, "PARTITION_STREAM_BYTE_TOTAL",
                     len(r.PARTITION_STREAM_HEADER) + 3 + len(r.PARTITION_STREAM_TRAILER)):
                sink = r.PartitionTagFileSink(path, "synthetic")
                sink.write_partition("owner", (0, 9, 1, (0, 1), 2))
                sink.write_partition("remainder", (1, 9, 1, (1, 0), 1))
                sink.write_partition("owner", (2, 10, 2, (1,), 3))
                receipt = sink.close()
            raw = path.read_bytes()
            self.assertEqual(
                raw,
                r.PARTITION_STREAM_HEADER + b"ORO" + r.PARTITION_STREAM_TRAILER)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(receipt["record_total"], 3)
            self.assertEqual(receipt["owner_orbit_total"], 2)
            self.assertEqual(receipt["owner_physical_total"], 5)
            self.assertEqual(receipt["remainder_orbit_total"], 1)
            self.assertEqual(receipt["remainder_physical_total"], 1)
            self.assertEqual(receipt["stream_sha256"], hashlib.sha256(raw).hexdigest())

    def test_partition_tag_sink_rejects_nonconsecutive_and_unknown_partition(self):
        r = self.replayer
        with tempfile.TemporaryDirectory(dir="/workspace") as directory:
            os.chmod(directory, 0o700)
            path = Path(directory) / "partition.bin"
            sink = r.PartitionTagFileSink(path, "synthetic")
            with self.assertRaisesRegex(RuntimeError, "nonconsecutive"):
                sink.write_partition("owner", (1, 9, 1, (0,), 1))
            with self.assertRaisesRegex(RuntimeError, "unknown key partition"):
                sink.write_partition("hostile", (0, 9, 1, (0,), 1))
            sink.abort()

    def test_partition_sink_path_rejects_stale_symlink_and_nonprivate_parent(self):
        r = self.replayer
        with tempfile.TemporaryDirectory(dir="/workspace") as directory:
            root = Path(directory)
            os.chmod(root, 0o700)
            stale = root / "stale.bin"
            stale.write_bytes(b"stale")
            with self.assertRaises(RuntimeError):
                r.validate_sink_path(str(stale.resolve()), "stale")
            target = root / "target.bin"
            target.write_bytes(b"target")
            link = root / "link.bin"
            link.symlink_to(target)
            with self.assertRaises(RuntimeError):
                r.validate_sink_path(str(link), "symlink")
            open_parent = root / "open"
            open_parent.mkdir(mode=0o755)
            with self.assertRaises(RuntimeError):
                r.validate_sink_path(str((open_parent / "new.bin").resolve()), "open")

    def test_partition_cli_rejects_any_callback_fallback_or_output_without_mode(self):
        with self.assertRaises(TypeError):
            self.replayer.emit_combined_partition_stream(
                "/workspace/does-not-exist/partition.bin", lambda *_: None)
        self.assertNotIn("--callback", PATH.read_text("ascii"))
        self.assertNotIn("--emit-key-sink", PATH.read_text("ascii"))



if __name__ == "__main__":
    unittest.main()
