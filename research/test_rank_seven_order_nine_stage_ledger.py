#!/usr/bin/env python3
"""Hostile tests for the reusable exact order-nine StageLedger."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import unittest
from pathlib import Path

PATH = Path(__file__).with_name("rank_seven_order_nine_stage_ledger.py")


def load_module():
    spec = importlib.util.spec_from_file_location("rank7_order9_stage_ledger_test", PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load StageLedger")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StageLedgerHostileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load_module()
        # Real five-field key shape, deliberately nonconsecutive source indices.
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

    def complete_ledger(self):
        ledger = self.m.StageLedger(self.rows)
        ledger.advance("structural", self.rows[::2], self.rows[1::2])
        ledger.advance("sos", (self.rows[1],), (self.rows[3],))
        ledger.advance("transfer", (self.rows[3],), ())
        return ledger

    def authenticated_registries(self, ledger, *, implication=True,
                                 dependency=True):
        digest = hashlib.sha256(b"authenticated lane contract").hexdigest()
        implications = {}
        dependencies = {}
        for index, stage in enumerate(ledger.stage_names):
            implications[stage] = self.m.implication_record(
                ledger,
                stage,
                "uniform-all-descendant",
                proof_contract_sha256=digest,
                verifier_sha256=digest,
                verification_output_sha256=digest,
                authenticated=True,
                verified=implication,
            )
            dependencies[stage] = {
                "authenticated": dependency,
                "dependency_sha256": (digest,),
            }
        return implications, dependencies

    def test_nonconsecutive_indices_full_key_identity_mass_and_targets(self):
        ledger = self.complete_ledger()
        structural = ledger.boundary("structural")
        self.assertEqual(structural["source_row_total"], 5)
        self.assertEqual(structural["source_physical_total"], 8)
        self.assertEqual(structural["owner_physical_total"], 3)
        self.assertEqual(structural["remainder_physical_total"], 5)
        self.assertTrue(structural["exact_disjoint_union"])
        self.assertFalse(structural["analytic_ownership_established"])

        target = ledger.stage_target_contract("structural")
        self.assertEqual(target["target_indices"], list(range(16)))
        self.assertEqual(target["per_row_target_cardinality"], 16)
        self.assertEqual(target["target_total"], 3 * 16)
        self.assertEqual(target["evidence_kind"],
                         "generated-row-times-target-index-contract")
        self.assertFalse(target["observed_target_stream_validated"])
        self.assertFalse(target["analytic_ownership_established"])

        accounting = ledger.finite_key_accounting()
        self.assertTrue(accounting["finite_key_accounting_complete"])
        self.assertFalse(accounting["analytic_lane_ownership_established"])
        self.assertFalse(accounting["bounded_order_nine_finite_premise_discharged"])
        self.assertIn("finite row/target identities only", accounting["claim_boundary"])

    def test_key_swap_rejected_even_when_counts_and_mass_match(self):
        ledger = self.m.StageLedger(self.rows)
        receipt = ledger.advance("structural", self.rows[:2], self.rows[2:])
        hostile = copy.deepcopy(receipt)
        hostile["owner_key_sha256"], hostile["remainder_key_sha256"] = (
            hostile["remainder_key_sha256"], hostile["owner_key_sha256"])
        replacement = self.m.StageLedger(self.rows)
        self.assert_rejected(
            lambda: replacement.advance("structural", self.rows[:2], self.rows[2:],
                                        expected=hostile),
            "exact receipt changed",
        )

        # A full-key substitution with the same source index and orbit size is
        # rejected independently of every count and physical mass.
        changed = list(self.rows[0])
        changed[3] = tuple([0] + list(changed[3][1:]))
        self.assert_rejected(lambda: self.m.StageLedger(self.rows).advance(
            "structural", (tuple(changed),), self.rows[1:]), "full row key")

    def test_owner_duplicate_and_remainder_omission_rejected(self):
        ledger = self.m.StageLedger(self.rows)
        self.assert_rejected(lambda: ledger.advance(
            "structural", (self.rows[0], self.rows[0]), self.rows[1:]),
            "duplicate full row key")
        self.assert_rejected(lambda: self.m.StageLedger(self.rows).advance(
            "structural", self.rows[:2], self.rows[3:]), "omits or changes")

    def test_owner_and_remainder_must_be_sorted_subsequences(self):
        self.assert_rejected(lambda: self.m.StageLedger(self.rows).advance(
            "structural", (self.rows[2], self.rows[0]),
            (self.rows[1], self.rows[3], self.rows[4])), "source-index order")
        self.assert_rejected(lambda: self.m.StageLedger(self.rows).advance(
            "structural", (self.rows[1],),
            (self.rows[0], self.rows[3], self.rows[2], self.rows[4])),
            "source-index order")

    def test_equal_count_and_physical_mass_swap_needs_exact_receipt(self):
        rows = (
            (3, 8000, 2, (0, 1), 2),
            (9, 8000, 2, (1, 0), 2),
            (14, 8000, 2, (1, 1), 2),
            (22, 8000, 2, (2, 0), 2),
        )
        baseline = self.m.StageLedger(rows)
        expected = baseline.advance("lane", (rows[0], rows[2]), (rows[1], rows[3]))
        hostile = self.m.StageLedger(rows)
        self.assert_rejected(lambda: hostile.advance(
            "lane", (rows[1], rows[3]), (rows[0], rows[2]), expected=expected),
            "exact receipt changed")

    def test_target_duplicate_and_omission_rejected(self):
        ledger = self.m.StageLedger(self.rows)
        ledger.advance("lane", (self.rows[0],), self.rows[1:])
        targets = [[list(self.rows[0][:3]) + [list(self.rows[0][3]), self.rows[0][4]], i]
                   for i in range(16)]
        # Rewrite the nested row to the actual five-field shape.
        targets = [[[self.rows[0][0], self.rows[0][1], self.rows[0][2],
                     list(self.rows[0][3]), self.rows[0][4]], i]
                   for i in range(16)]
        hostile = copy.deepcopy(targets)
        hostile[7] = copy.deepcopy(hostile[6])  # duplicate 6, omit 7
        self.assert_rejected(lambda: ledger.stage_target_contract(
            "lane", targets=hostile), "duplicate, omission, or order")
        self.assert_rejected(lambda: ledger.stage_target_contract(
            "lane", targets=targets[:-1]), "ended early")
        self.assert_rejected(lambda: ledger.stage_target_contract(
            "lane", targets=targets + [targets[-1]]), "surplus")

    def test_supplied_target_stream_is_explicitly_observed_evidence(self):
        ledger = self.m.StageLedger(self.rows)
        ledger.advance("lane", (self.rows[0],), self.rows[1:])
        targets = tuple(self.m.iter_target_keys((self.rows[0],)))
        receipt = ledger.stage_target_contract("lane", targets=targets)
        self.assertEqual(receipt["evidence_kind"], "observed-exact-target-stream")
        self.assertTrue(receipt["observed_target_stream_validated"])

    def test_target_digest_uses_full_row_key_and_exact_index_order(self):
        ledger = self.m.StageLedger(self.rows)
        ledger.advance("lane", (self.rows[0],), self.rows[1:])
        receipt = ledger.stage_target_contract("lane")
        digest = hashlib.sha256()
        for index in range(16):
            digest.update(self.m.canonical_bytes([
                [self.rows[0][0], self.rows[0][1], self.rows[0][2],
                 list(self.rows[0][3]), self.rows[0][4]], index]))
        self.assertEqual(receipt["target_key_sha256"], digest.hexdigest())

    def test_bool_as_int_laundering_is_rejected_everywhere(self):
        hostile_rows = list(self.rows)
        hostile = list(hostile_rows[0])
        hostile[0] = True
        hostile_rows[0] = tuple(hostile)
        self.assert_rejected(lambda: self.m.StageLedger(hostile_rows),
                             "invalid exact integer")
        ledger = self.complete_ledger()
        implications, dependencies = self.authenticated_registries(ledger)
        implications["sos"]["target_total"] = True
        self.assert_rejected(lambda: ledger.derive_bounded_premise(
            implications, dependencies), "invalid exact integer")

    def test_bounded_premise_is_derived_not_literal(self):
        ledger = self.complete_ledger()
        implications, dependencies = self.authenticated_registries(ledger)
        result = ledger.derive_bounded_premise(implications, dependencies)
        self.assertTrue(result["finite_key_accounting_complete"])
        self.assertTrue(result["lane_implication_contracts_authenticated"])
        self.assertTrue(result["lane_implications_verified"])
        self.assertTrue(result["analytic_dependencies_authenticated"])
        self.assertTrue(result["bounded_order_nine_finite_premise_discharged"])
        self.assertFalse(result["global_analytic_child_claim"])
        self.assertNotIn("theorem_eligible", result)
        self.assertNotIn("global_claim", result)

    def test_lane_implication_false_keeps_bounded_premise_false(self):
        ledger = self.complete_ledger()
        implications, dependencies = self.authenticated_registries(
            ledger, implication=False)
        result = ledger.derive_bounded_premise(implications, dependencies)
        self.assertFalse(result["lane_implications_verified"])
        self.assertFalse(result["bounded_order_nine_finite_premise_discharged"])

    def test_implication_authentication_false_keeps_premise_false(self):
        ledger = self.complete_ledger()
        implications, dependencies = self.authenticated_registries(ledger)
        implications["sos"]["authenticated"] = False
        result = ledger.derive_bounded_premise(implications, dependencies)
        self.assertFalse(result["lane_implication_contracts_authenticated"])
        self.assertFalse(result["bounded_order_nine_finite_premise_discharged"])

    def test_transfer_analytic_dependency_false_keeps_premise_false(self):
        ledger = self.complete_ledger()
        implications, dependencies = self.authenticated_registries(ledger)
        dependencies["transfer"]["authenticated"] = False
        result = ledger.derive_bounded_premise(implications, dependencies)
        self.assertFalse(result["analytic_dependencies_authenticated"])
        self.assertFalse(result["bounded_order_nine_finite_premise_discharged"])

    def test_implication_must_bind_exact_lane_rows_and_targets(self):
        ledger = self.complete_ledger()
        implications, dependencies = self.authenticated_registries(ledger)
        implications["structural"]["row_key_sha256"] = "0" * 64
        self.assert_rejected(lambda: ledger.derive_bounded_premise(
            implications, dependencies), "not bound to exact owner rows/targets")
        implications, dependencies = self.authenticated_registries(ledger)
        implications["sos"]["target_indices"] = tuple(range(15))
        self.assert_rejected(lambda: ledger.derive_bounded_premise(
            implications, dependencies), "target-index contract changed")

    def test_registries_are_exact_and_digests_are_authenticated(self):
        ledger = self.complete_ledger()
        implications, dependencies = self.authenticated_registries(ledger)
        implications["extra"] = copy.deepcopy(implications["sos"])
        self.assert_rejected(lambda: ledger.derive_bounded_premise(
            implications, dependencies), "registry is not exact")
        implications, dependencies = self.authenticated_registries(ledger)
        dependencies["sos"]["dependency_sha256"] = ("xyz",)
        self.assert_rejected(lambda: ledger.derive_bounded_premise(
            implications, dependencies), "malformed analytic dependency")

    def test_global_child_must_remain_false_and_bool_exact(self):
        ledger = self.complete_ledger()
        implications, dependencies = self.authenticated_registries(ledger)
        self.assert_rejected(lambda: ledger.derive_bounded_premise(
            implications, dependencies, global_analytic_child_claim=True),
            "requires the global analytic child to remain false")
        self.assert_rejected(lambda: ledger.derive_bounded_premise(
            implications, dependencies, global_analytic_child_claim=0),
            "invalid exact boolean")

    def test_mutable_private_receipts_and_stage_rows_are_recomputed(self):
        def prepared():
            ledger = self.complete_ledger()
            implications, dependencies = self.authenticated_registries(ledger)
            ledger.finite_key_accounting()  # materialize every lazy receipt
            return ledger, implications, dependencies

        cases = []

        ledger, implications, dependencies = prepared()
        forged = "0" * 64
        ledger._stages["structural"].boundary["owner_key_sha256"] = forged
        ledger._target_receipts["structural"]["row_key_sha256"] = forged
        implications["structural"]["row_key_sha256"] = forged
        cases.append(("matching forged row digests", ledger, implications,
                      dependencies))

        ledger, implications, dependencies = prepared()
        ledger._stages["structural"].boundary["exact_disjoint_union"] = False
        cases.append(("false boundary semantic bit", ledger, implications,
                      dependencies))

        ledger, implications, dependencies = prepared()
        ledger._target_receipts["structural"][
            "per_row_cardinality_validated"] = False
        cases.append(("false target semantic bit", ledger, implications,
                      dependencies))

        ledger, implications, dependencies = prepared()
        ledger._universe_target_receipt["target_key_sha256"] = forged
        cases.append(("forged universe target digest", ledger, implications,
                      dependencies))

        ledger, implications, dependencies = prepared()
        state = ledger._stages["structural"]
        ledger._stages["structural"] = self.m._StageState(
            state.boundary, (), ())
        cases.append(("replaced owner and remainder rows", ledger, implications,
                      dependencies))

        ledger, implications, dependencies = prepared()
        wrong_chain = self.m.StageLedger(self.rows)
        wrong_chain.advance("sos", (self.rows[0],), self.rows[1:])
        ledger._stages["sos"] = wrong_chain._stages["sos"]
        cases.append(("later stage no longer consumes prior remainder", ledger,
                      implications, dependencies))

        ledger, implications, dependencies = prepared()
        ledger._current = (self.rows[3],)
        cases.append(("current remainder no longer closes stage chain", ledger,
                      implications, dependencies))

        for label, ledger, implications, dependencies in cases:
            with self.subTest(label=label):
                self.assert_rejected(lambda: ledger.derive_bounded_premise(
                    implications, dependencies))

    def test_failed_expected_pin_does_not_advance_state(self):
        ledger = self.m.StageLedger(self.rows)
        baseline = self.m.StageLedger(self.rows).advance(
            "lane", self.rows[:1], self.rows[1:])
        baseline["owner_row_total"] = 2
        self.assert_rejected(lambda: ledger.advance(
            "lane", self.rows[:1], self.rows[1:], expected=baseline))
        self.assertEqual(ledger.stage_names, ())
        self.assertEqual(ledger.remaining_rows, self.rows)


if __name__ == "__main__":
    unittest.main()
