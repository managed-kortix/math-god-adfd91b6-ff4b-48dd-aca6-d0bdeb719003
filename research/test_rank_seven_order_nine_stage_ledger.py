#!/usr/bin/env python3
"""Hostile tests for the fail-closed order-nine StageLedger v2 layer."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.runner import TextTestRunner

HERE = Path(__file__).parent
LEDGER_PATH = HERE / "rank_seven_order_nine_stage_ledger.py"
ORACLE_PATH = HERE / "rank_seven_order_nine_target_encoding_oracle.py"
FIXTURE_PATH = HERE / "fixtures" / "rank_seven_order_nine_flat_target_v1.jsonl"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StageLedgerV2HostileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load_module(LEDGER_PATH, "rank7_order9_stage_ledger_v2_test")
        cls.oracle = load_module(ORACLE_PATH, "rank7_order9_target_oracle_test")
        cls.rows = (
            (2, 7487, 1, (1, 1, 1, 1, 1, 1, 1, 1, 0, 0), 1),
            (7, 7487, 1, (1, 1, 1, 1, 1, 1, 1, 0, 1, 0), 2),
            (11, 7487, 1, (1, 1, 1, 1, 0, 1, 1, 1, 1, 0), 1),
            (19, 7487, 1, (1, 1, 0, 1, 1, 1, 1, 1, 1, 0), 3),
            (31, 7487, 1, (1, 1, 1, 1, 1, 1, 1, 1, 1, 0), 1),
        )

    def assert_rejected(self, action, message=None):
        context = self.assertRaises(RuntimeError) if message is None else \
            self.assertRaisesRegex(RuntimeError, message)
        with context:
            action()

    def boundary_pin(self, stage, source, owners, remainder):
        # Test-only pin construction.  Promotional callers must load reviewed
        # committed pins; this helper merely lets hostile tests reach later APIs.
        return self.m._boundary_receipt(stage, source, owners, remainder)[0]

    def advance(self, ledger, stage, owners, remainder):
        pin = self.boundary_pin(stage, ledger.remaining_rows, owners, remainder)
        return ledger.advance(stage, owners, remainder, expected=pin)

    def observation_pin(self, rows, scope):
        identity = self.m._target_identity(tuple(rows), scope)
        return self.m._observation_from_identity(identity)

    def observe_stage(self, ledger, stage, targets=None):
        rows = ledger.owner_rows(stage)
        targets = tuple(self.m.iter_target_keys(rows)) if targets is None else targets
        return ledger.observe_stage_targets(
            stage, targets, expected=self.observation_pin(rows, stage)
        )

    def complete_ledger(self):
        ledger = self.m.StageLedger(self.rows)
        self.advance(ledger, "structural", self.rows[::2], self.rows[1::2])
        self.advance(ledger, "sos", (self.rows[1],), (self.rows[3],))
        self.advance(ledger, "transfer", (self.rows[3],), ())
        return ledger

    def test_independent_fixture_oracle_matches_producer_byte_for_byte(self):
        oracle = self.oracle.verify_fixture()
        producer = b"".join(self.m.iter_target_jsonl((self.rows[0],)))
        fixture = FIXTURE_PATH.read_bytes()
        self.assertEqual(producer, fixture)
        self.assertEqual(len(producer), oracle["fixture_size"])
        self.assertEqual(hashlib.sha256(producer).hexdigest(),
                         oracle["fixture_sha256"])
        self.assertEqual(self.m.TARGET_ENCODING, oracle["schema"])
        first = json.loads(producer.splitlines()[0])
        self.assertIs(type(first), list)
        self.assertEqual(first, [*self.rows[0][:3], list(self.rows[0][3]),
                                 self.rows[0][4], 0])

    def test_encoding_mismatch_nested_target_is_rejected(self):
        ledger = self.m.StageLedger(self.rows)
        self.advance(ledger, "lane", (self.rows[0],), self.rows[1:])
        nested = [[
            [self.rows[0][0], self.rows[0][1], self.rows[0][2],
             list(self.rows[0][3]), self.rows[0][4]], coordinate
        ] for coordinate in range(16)]
        pin = self.observation_pin((self.rows[0],), "lane")
        self.assert_rejected(lambda: ledger.observe_stage_targets(
            "lane", nested, expected=pin), "flat six-field")

    def test_wire_target_indices_are_json_lists(self):
        ledger = self.complete_ledger()
        identity = ledger.stage_target_identity("structural")
        self.assertIs(type(identity["target_indices"]), list)
        self.assertEqual(identity["target_indices"], list(range(16)))
        data = self.m.canonical_bytes(identity)
        self.assertIs(type(json.loads(data)["target_indices"]), list)

    def test_nonconsecutive_full_key_identity_mass_and_generated_nonclaim(self):
        ledger = self.complete_ledger()
        boundary = ledger.boundary("structural")
        self.assertEqual(boundary["source_row_total"], 5)
        self.assertEqual(boundary["source_physical_total"], 8)
        self.assertEqual(boundary["owner_physical_total"], 3)
        self.assertEqual(boundary["remainder_physical_total"], 5)
        identity = ledger.stage_target_identity("structural")
        self.assertEqual(identity["target_total"], 3 * 16)
        self.assertEqual(identity["identity_kind"],
                         "generated-deterministic-row-times-coordinate")
        self.assertFalse(identity["observed_target_stream_validated"])
        self.assertIsNone(ledger.observed_stage_target_receipt("structural"))

    def test_promotional_boundary_and_observation_pins_are_mandatory(self):
        ledger = self.m.StageLedger(self.rows)
        self.assert_rejected(lambda: ledger.advance(
            "lane", self.rows[:1], self.rows[1:]), "expected receipt is required")
        self.assertEqual(ledger.stage_names, ())
        self.advance(ledger, "lane", self.rows[:1], self.rows[1:])
        targets = tuple(self.m.iter_target_keys(self.rows[:1]))
        self.assert_rejected(lambda: ledger.observe_stage_targets(
            "lane", targets), "expected receipt is required")
        self.assertIsNone(ledger.observed_stage_target_receipt("lane"))
        self.assert_rejected(lambda: ledger.observe_universe_targets(
            tuple(self.m.iter_target_keys(self.rows))),
            "expected receipt is required")

    def test_self_derived_wrong_pin_does_not_mutate_state(self):
        ledger = self.m.StageLedger(self.rows)
        pin = self.boundary_pin("lane", self.rows, self.rows[:1], self.rows[1:])
        hostile = copy.deepcopy(pin)
        hostile["owner_row_total"] = 2
        self.assert_rejected(lambda: ledger.advance(
            "lane", self.rows[:1], self.rows[1:], expected=hostile),
            "exact receipt changed")
        self.assertEqual(ledger.stage_names, ())
        self.assertEqual(ledger.remaining_rows, self.rows)

    def test_equal_count_and_mass_swap_rejected_by_exact_pin(self):
        rows = (
            (3, 8000, 2, (0, 1), 2),
            (9, 8000, 2, (1, 0), 2),
            (14, 8000, 2, (1, 1), 2),
            (22, 8000, 2, (2, 0), 2),
        )
        expected = self.boundary_pin("lane", rows,
                                     (rows[0], rows[2]), (rows[1], rows[3]))
        hostile = self.m.StageLedger(rows)
        self.assert_rejected(lambda: hostile.advance(
            "lane", (rows[1], rows[3]), (rows[0], rows[2]), expected=expected),
            "exact receipt changed")

    def test_owner_duplicate_omit_reorder_and_full_key_swap_rejected(self):
        ledger = self.m.StageLedger(self.rows)
        pin = self.boundary_pin("lane", self.rows, self.rows[:1], self.rows[1:])
        self.assert_rejected(lambda: ledger.advance(
            "lane", (self.rows[0], self.rows[0]), self.rows[1:], expected=pin),
            "duplicate full row key")
        self.assert_rejected(lambda: self.m.StageLedger(self.rows).advance(
            "lane", self.rows[:2], self.rows[3:], expected=pin),
            "omits or changes")
        self.assert_rejected(lambda: self.m.StageLedger(self.rows).advance(
            "lane", (self.rows[2], self.rows[0]),
            (self.rows[1], self.rows[3], self.rows[4]), expected=pin),
            "source-index order")
        changed = list(self.rows[0])
        changed[3] = tuple([0] + list(changed[3][1:]))
        self.assert_rejected(lambda: self.m.StageLedger(self.rows).advance(
            "lane", (tuple(changed),), self.rows[1:], expected=pin),
            "full row key")

    def test_semantic_row_cannot_be_reindexed_and_bool_is_not_int(self):
        reindexed = (37, *self.rows[0][1:])
        self.assert_rejected(lambda: self.m.StageLedger((self.rows[0], reindexed)),
                             "duplicate semantic row")
        hostile = list(self.rows[0])
        hostile[0] = True
        self.assert_rejected(lambda: self.m.StageLedger((tuple(hostile),)),
                             "invalid exact integer")

    def test_target_reorder_duplicate_omission_and_surplus_rejected(self):
        ledger = self.m.StageLedger(self.rows)
        self.advance(ledger, "lane", self.rows[:1], self.rows[1:])
        targets = list(self.m.iter_target_keys(self.rows[:1]))
        pin = self.observation_pin(self.rows[:1], "lane")
        cases = []
        duplicate = copy.deepcopy(targets)
        duplicate[7] = duplicate[6]
        cases.append((duplicate, "duplicate, omission, or order"))
        reorder = copy.deepcopy(targets)
        reorder[3], reorder[4] = reorder[4], reorder[3]
        cases.append((reorder, "duplicate, omission, or order"))
        cases.append((targets[:-1], "ended early"))
        cases.append((targets + [targets[-1]], "surplus"))
        for stream, message in cases:
            with self.subTest(message=message):
                self.assert_rejected(lambda stream=stream: ledger.observe_stage_targets(
                    "lane", stream, expected=pin), message)
                self.assertIsNone(ledger.observed_stage_target_receipt("lane"))

    def test_observation_survives_recomputation_and_replay_is_idempotent(self):
        ledger = self.complete_ledger()
        receipt = self.observe_stage(ledger, "structural")
        self.assertTrue(receipt["observed_target_stream_validated"])
        self.assertEqual(receipt["evidence_kind"], "observed-exact-target-stream")
        before = ledger._observed_target_receipts["structural"]
        accounting = ledger.finite_key_accounting()
        self.assertEqual(ledger._observed_target_receipts["structural"], before)
        self.assertEqual(accounting["observed_lane_target_receipts"]["structural"],
                         receipt)
        replay = self.observe_stage(ledger, "structural")
        self.assertEqual(replay, receipt)
        self.assertEqual(ledger._observed_target_receipts["structural"], before)

    def test_generated_identity_cannot_overwrite_or_launder_observation(self):
        ledger = self.complete_ledger()
        observed = self.observe_stage(ledger, "structural")
        stored = ledger._observed_target_receipts["structural"]
        generated = ledger.stage_target_identity("structural")
        self.assertFalse(generated["observed_target_stream_validated"])
        self.assertEqual(ledger._observed_target_receipts["structural"], stored)
        self.assertEqual(ledger.observed_stage_target_receipt("structural"), observed)
        ledger._observed_target_receipts["structural"] = \
            self.m.canonical_bytes(generated)
        self.assert_rejected(lambda: ledger.finite_key_accounting(),
                             "stored receipt schema changed")

    def test_explicit_frontier_cannot_use_generated_identity_as_evidence(self):
        ledger = self.complete_ledger()
        generated = ledger.stage_target_identity("transfer")
        self.assertEqual(generated["identity_kind"],
                         "generated-deterministic-row-times-coordinate")
        self.assertFalse(generated["observed_target_stream_validated"])
        self.assertNotIn("evidence_kind", generated)
        self.assertIsNone(ledger.observed_stage_target_receipt("transfer"))
        accounting = ledger.finite_key_accounting()
        self.assertNotIn("transfer", accounting["observed_lane_target_receipts"])
        self.assertFalse(accounting["all_stage_target_streams_observed"])
        self.assertFalse(accounting["bounded_order_nine_finite_premise_discharged"])

    def test_target_indices_wire_type_mismatch_is_rejected(self):
        ledger = self.m.StageLedger(self.rows)
        # Boundary receipts have no target_indices; the mismatch belongs to an
        # observed-target pin and canonical byte equality must reject tuple/list
        # laundering only at the external mapping type gate.
        self.advance(ledger, "lane", self.rows[:1], self.rows[1:])
        observation = self.observation_pin(self.rows[:1], "lane")
        observation["target_indices"] = tuple(range(16))
        targets = tuple(self.m.iter_target_keys(self.rows[:1]))
        self.assert_rejected(lambda: ledger.observe_stage_targets(
            "lane", targets, expected=observation),
            "target_indices wire type must be a JSON list")
        self.assertIsNone(ledger.observed_stage_target_receipt("lane"))

    def test_observed_receipt_cannot_be_overwritten(self):
        ledger = self.complete_ledger()
        self.observe_stage(ledger, "structural")
        stored = ledger._observed_target_receipts["structural"]
        hostile = bytearray(stored)
        hostile[-2] = ord("x")
        ledger._observed_target_receipts["structural"] = bytes(hostile)
        self.assert_rejected(lambda: ledger.finite_key_accounting(),
                             "stored receipt")

    def test_mutable_stage_state_and_chain_are_recomputed(self):
        ledger = self.complete_ledger()
        state = ledger._stages["structural"]
        decoded = json.loads(state.boundary_bytes)
        decoded["exact_disjoint_union"] = False
        ledger._stages["structural"] = self.m._StageState(
            self.m.canonical_bytes(decoded), state.owners, state.remainder)
        self.assert_rejected(lambda: ledger.finite_key_accounting(),
                             "stored receipt integrity changed")

        ledger = self.complete_ledger()
        wrong = self.m.StageLedger(self.rows)
        self.advance(wrong, "sos", (self.rows[0],), self.rows[1:])
        ledger._stages["sos"] = wrong._stages["sos"]
        self.assert_rejected(lambda: ledger.finite_key_accounting())

        ledger = self.complete_ledger()
        ledger._current = (self.rows[3],)
        self.assert_rejected(lambda: ledger.finite_key_accounting(),
                             "current remainder")

    def test_universe_observation_is_optional_separate_and_preserved(self):
        ledger = self.complete_ledger()
        identity = ledger.universe_target_identity()
        self.assertEqual(identity["scope"], self.m.UNIVERSE_SCOPE)
        self.assertFalse(identity["observed_target_stream_validated"])
        self.assertIsNone(ledger.observed_universe_target_receipt())
        pin = self.observation_pin(self.rows, self.m.UNIVERSE_SCOPE)
        receipt = ledger.observe_universe_targets(
            tuple(self.m.iter_target_keys(self.rows)), expected=pin)
        self.assertEqual(receipt, ledger.observed_universe_target_receipt())
        accounting = ledger.finite_key_accounting()
        self.assertEqual(accounting["observed_universe_target_receipt"], receipt)
        self.assertTrue(accounting["universe_target_stream_observed"])

    def test_accounting_is_generic_nonpromotional_and_has_no_auth_constructor(self):
        ledger = self.complete_ledger()
        accounting = ledger.finite_key_accounting()
        self.assertTrue(accounting["finite_key_accounting_complete"])
        self.assertFalse(accounting["all_stage_target_streams_observed"])
        self.assertFalse(accounting["order_nine_universe_root_authenticated"])
        self.assertFalse(accounting["analytic_lane_ownership_established"])
        self.assertFalse(accounting["bounded_order_nine_finite_premise_discharged"])
        self.assertNotIn("theorem_eligible", accounting)
        self.assertNotIn("global_claim", accounting)
        self.assertFalse(hasattr(ledger, "derive_bounded_premise"))
        self.assertFalse(hasattr(self.m, "implication_record"))
        self.assertNotIn("authenticated", self.m.TARGET_IDENTITY_FIELDS)
        self.assertIn("order-nine root not authenticated", accounting["scope"])

    def test_tiny_synthetic_ledger_never_acquires_order_nine_scope_semantics(self):
        row = (0, 1, 1, (0,), 1)
        ledger = self.m.StageLedger((row,))
        self.advance(ledger, "lane", (row,), ())
        accounting = ledger.finite_key_accounting()
        self.assertEqual(accounting["source_row_total"], 1)
        self.assertFalse(accounting["order_nine_universe_root_authenticated"])
        self.assertFalse(accounting["bounded_order_nine_finite_premise_discharged"])

    def test_no_volatile_transport_fields_in_semantic_receipts(self):
        ledger = self.complete_ledger()
        self.observe_stage(ledger, "structural")
        values = [ledger.boundary("structural"),
                  ledger.stage_target_identity("structural"),
                  ledger.observed_stage_target_receipt("structural")]
        banned = {"path", "pid", "device", "dev", "inode", "cwd", "temporary_path"}
        for value in values:
            self.assertTrue(banned.isdisjoint(value))


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(StageLedgerV2HostileTest)
    detail = io.StringIO()
    result = TextTestRunner(stream=detail, verbosity=0).run(suite)
    if not result.wasSuccessful():
        sys.stderr.write(detail.getvalue())
        raise SystemExit(1)
    print(f"rank-seven order-nine StageLedger v2 hostile tests passed ({result.testsRun})")
