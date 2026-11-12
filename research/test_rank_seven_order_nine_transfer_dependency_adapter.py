#!/usr/bin/env python3
"""Hostile tests for the non-promotional transfer dependency adapter."""

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

PATH = Path(__file__).with_name(
    "rank_seven_order_nine_transfer_dependency_adapter.py")


def load_module():
    spec = importlib.util.spec_from_file_location("rank7_o9_transfer_adapter_test", PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load transfer dependency adapter")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TransferDependencyAdapterHostileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load_module()

    def setUp(self):
        self.contract = self.m.build_contract(execute_finite_gate=False)

    def rejected(self, candidate, message=None):
        context = self.assertRaises(RuntimeError) if message is None else \
            self.assertRaisesRegex(RuntimeError, message)
        with context:
            self.m.validate_contract(candidate)

    def test_contract_separates_executed_and_reviewed_evidence(self):
        contract = self.contract
        self.assertEqual(
            contract["executed_finite_gates"][0]["evidence_kind"],
            "registered-unexecuted-finite-gate",
        )
        self.assertFalse(contract["executed_finite_gates"][0]["finite_gate_passed"])
        self.assertFalse(
            contract["executed_finite_gates"][0]["analytic_implication_established"])
        self.assertEqual(len(contract["reviewed_analytic_axioms"]), 5)
        self.assertTrue(all(
            axiom["status"] == "review-required" and
            axiom["semantic_proof_executed"] is False
            for axiom in contract["reviewed_analytic_axioms"]
        ))
        self.assertFalse(contract["all_analytic_dependencies_executed"])
        self.assertFalse(contract["analytic_dependencies_authenticated"])
        self.assertFalse(contract["reviewed_axioms_accepted"])
        self.assertFalse(contract["bounded_transfer_implication_discharged"])
        self.assertFalse(contract["theorem_eligible"])
        self.assertFalse(contract["global_claim"])

    def test_missing_axiom_rejected(self):
        hostile = copy.deepcopy(self.contract)
        hostile["reviewed_analytic_axioms"].pop()
        self.rejected(hostile, "reviewed axiom registry changed")

    def test_extra_axiom_rejected(self):
        hostile = copy.deepcopy(self.contract)
        extra = copy.deepcopy(hostile["reviewed_analytic_axioms"][0])
        extra["id"] = "invented-extra-axiom"
        hostile["reviewed_analytic_axioms"].append(extra)
        self.rejected(hostile, "reviewed axiom registry changed")

    def test_weakened_axiom_hypotheses_rejected(self):
        hostile = copy.deepcopy(self.contract)
        hostile["reviewed_analytic_axioms"][4]["hypotheses"].pop()
        self.rejected(hostile, "reviewed axiom registry changed")

    def test_axiom_status_or_semantic_execution_promotion_rejected(self):
        hostile = copy.deepcopy(self.contract)
        hostile["reviewed_analytic_axioms"][0]["status"] = "executed"
        self.rejected(hostile, "reviewed axiom registry changed")
        hostile = copy.deepcopy(self.contract)
        hostile["reviewed_analytic_axioms"][1]["semantic_proof_executed"] = True
        self.rejected(hostile, "reviewed axiom registry changed")

    def test_false_to_true_child_analytic_flag_rejected(self):
        hostile = copy.deepcopy(self.contract)
        hostile["executed_finite_gates"][0]["analytic_implication_established"] = True
        self.rejected(hostile, "finite gate crossed the analytic boundary")

    def test_any_attempted_aggregate_promotion_rejected(self):
        fields = (
            "all_analytic_dependencies_executed",
            "analytic_dependencies_authenticated",
            "reviewed_axioms_accepted",
            "bounded_transfer_implication_discharged",
            "theorem_eligible",
            "global_claim",
        )
        for field in fields:
            with self.subTest(field=field):
                hostile = copy.deepcopy(self.contract)
                hostile[field] = True
                self.rejected(hostile, "promoted a reviewed axiom or theorem claim")

    def test_bool_as_int_or_non_bool_promotion_rejected(self):
        for value in (0, 1, "false", None):
            with self.subTest(value=value):
                hostile = copy.deepcopy(self.contract)
                hostile["all_analytic_dependencies_executed"] = value
                self.rejected(hostile)

    def test_missing_or_extra_source_pin_rejected(self):
        hostile = copy.deepcopy(self.contract)
        hostile["source_sha256"].pop("all-bicyclic-graphs/paper.tex")
        self.rejected(hostile, "adapter source registry changed")
        hostile = copy.deepcopy(self.contract)
        hostile["source_sha256"]["invented"] = "0" * 64
        self.rejected(hostile, "adapter source registry changed")

    def test_source_hash_cannot_be_laundered_into_semantic_truth(self):
        hostile = copy.deepcopy(self.contract)
        hostile["source_sha256"]["all-tricyclic-graphs/paper.tex"] = "0" * 64
        hostile["analytic_dependencies_authenticated"] = True
        self.rejected(hostile)

    def test_rank_type_omission_and_scope_weakening_rejected(self):
        hostile = copy.deepcopy(self.contract)
        hostile["rank_type_exhaustion"]["types"].pop()
        self.rejected(hostile, "rank-type exhaustion record changed")
        hostile = copy.deepcopy(self.contract)
        hostile["transfer_scope"]["simple_realization_rule"] = "any subdivision"
        self.rejected(hostile)

    def test_child_result_requires_explicit_false_analytic_nonclaim(self):
        hostile = copy.deepcopy(self.m.EXPECTED_TRANSFER)
        hostile["analytic_dependencies_authenticated"] = True
        with self.assertRaisesRegex(RuntimeError, "finite transfer result changed"):
            self.m.validate_transfer_result(hostile)

    def test_exact_reviewed_axiom_ids_and_integer_rank_types(self):
        self.assertEqual(
            [record["id"] for record in self.contract["reviewed_analytic_axioms"]],
            [
                "positive-part-variational-induced-superadditivity",
                "connected-simple-cyclomatic-rank-two-theorem",
                "connected-simple-cyclomatic-rank-three-theorem",
                "connected-simple-cyclomatic-rank-four-theorem",
                "uniform-induced-territory-construction",
            ],
        )
        self.assertEqual(
            self.contract["rank_type_exhaustion"]["types"],
            [
                {"ranks": [4, 2], "crossing_physical_edges": 2},
                {"ranks": [3, 3], "crossing_physical_edges": 2},
                {"ranks": [3, 2], "crossing_physical_edges": 3},
                {"ranks": [2, 2], "crossing_physical_edges": 4},
            ],
        )

    def test_bundled_hostile_ledger_is_exact(self):
        self.assertEqual(self.m.hostile_contract_checks(self.contract), 15)


if __name__ == "__main__":
    unittest.main()
