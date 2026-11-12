#!/usr/bin/env python3
"""Hostile tests for the non-promotional transfer dependency adapter."""

from __future__ import annotations

import copy
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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

    def test_optional_transfer_child_commands_are_isolated_and_mode_explicit(self):
        result = copy.deepcopy(self.m.EXPECTED_TRANSFER)
        raw = (self.m.canonical_bytes(result) +
               (self.m.TRANSFER_PASS_LINE + "\n").encode("ascii"))
        self.assertEqual(self.m.sha256_bytes(raw), self.m.TRANSFER_OUTPUT_SHA256)
        completed = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=raw, stderr=b"")
        commands = []

        def capture(command, **kwargs):
            commands.append((list(command), dict(kwargs["env"]), kwargs["cwd"]))
            return completed

        with mock.patch.dict(
                os.environ,
                {"PYTHONOPTIMIZE": "2", "LD_PRELOAD": "/hostile/preload.so",
                 "LD_AUDIT": "/hostile/audit.so", "LOCPATH": "/hostile/locale"},
                clear=False):
            with mock.patch.object(self.m.subprocess, "run", side_effect=capture):
                normal_raw, normal, normal_receipt = \
                    self.m.run_transfer_once(optimized=False)
                optimized_raw, optimized, optimized_receipt = \
                    self.m.run_transfer_once(optimized=True)
        self.assertEqual(normal_raw, raw)
        self.assertEqual(optimized_raw, raw)
        self.assertEqual(normal, result)
        self.assertEqual(optimized, result)
        self.assertEqual(normal_receipt,
                         self.m.expected_execution_receipt(optimized=False))
        self.assertEqual(optimized_receipt,
                         self.m.expected_execution_receipt(optimized=True))
        self.assertEqual(commands[0][0], [sys.executable, "-I", "-S", "-B",
                         str(self.m.TRANSFER_VERIFIER)])
        self.assertEqual(commands[1][0], [sys.executable, "-I", "-S", "-B", "-O",
                         str(self.m.TRANSFER_VERIFIER)])
        for command, environment, cwd in commands:
            with self.subTest(command=command):
                self.assertEqual(environment, {})
                self.assertEqual(cwd, self.m.ROOT)
        self.assertTrue(Path(sys.executable).is_absolute())
        with mock.patch.object(self.m.sys, "executable", "relative-python"):
            with self.assertRaisesRegex(RuntimeError, "not an absolute path"):
                self.m.run_transfer_once(optimized=False)

    def test_adapter_process_isolated_mode_suppresses_ambient_startup_hook(self):
        with tempfile.TemporaryDirectory() as directory:
            sentinel = Path(directory) / "sitecustomize-executed"
            Path(directory, "sitecustomize.py").write_text(
                "from pathlib import Path\n"
                f"Path({str(sentinel)!r}).write_text('executed', encoding='ascii')\n",
                encoding="ascii",
            )
            environment = dict(os.environ)
            environment.update({
                "PYTHONPATH": directory,
                "PYTHONHOME": directory,
                "PYTHONSTARTUP": str(Path(directory, "sitecustomize.py")),
                "PYTHONINSPECT": "1",
                "PYTHONOPTIMIZE": "2",
            })
            outputs = []
            for optimized in (False, True):
                command = [sys.executable, "-I", "-S", "-B"]
                if optimized:
                    command.append("-O")
                command.append(str(PATH))
                completed = subprocess.run(
                    command, cwd=self.m.ROOT, check=False, capture_output=True,
                    env=environment)
                self.assertEqual(completed.returncode, 0)
                self.assertEqual(completed.stderr, b"")
                outputs.append(completed.stdout)
            self.assertFalse(sentinel.exists())
            self.assertEqual(outputs[0], outputs[1])
            self.assertEqual(self.m.sha256_bytes(outputs[0]),
                             "4640bd74f669885d9a848d37c0e278603369df556dbfdf901a52f26cadeebfdd")

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

    def test_default_gate_execution_claim_reproductions_rejected(self):
        hostile = copy.deepcopy(self.contract)
        hostile["executed_finite_gates"][0]["evidence_kind"] = "executed-finite-gate"
        self.rejected(hostile, "executed finite gate schema changed")

        hostile = copy.deepcopy(self.contract)
        hostile["executed_finite_gates"][0]["finite_gate_passed"] = True
        self.rejected(hostile, "registered-unexecuted finite gate receipt values changed")

        hostile = copy.deepcopy(self.contract)
        hostile["executed_finite_gates"][0]["invented_nested_field"] = False
        self.rejected(hostile, "registered-unexecuted finite gate schema changed")

    def test_default_gate_missing_and_cross_mode_fields_rejected(self):
        hostile = copy.deepcopy(self.contract)
        hostile["executed_finite_gates"][0].pop("expected_output_sha256")
        self.rejected(hostile, "registered-unexecuted finite gate schema changed")

        hostile = copy.deepcopy(self.contract)
        hostile["executed_finite_gates"][0]["normal_output_sha256"] = \
            self.m.TRANSFER_OUTPUT_SHA256
        self.rejected(hostile, "registered-unexecuted finite gate schema changed")

    def test_executed_gate_has_exact_closed_schema_and_values(self):
        executed = copy.deepcopy(self.contract)
        executed["executed_finite_gates"] = [self.m.expected_executed_finite_gate()]
        self.m.validate_contract(executed)
        gate = executed["executed_finite_gates"][0]
        self.assertEqual(set(gate), self.m.EXECUTED_FINITE_GATE_FIELDS)
        self.assertEqual(gate["normal_output_sha256"], self.m.TRANSFER_OUTPUT_SHA256)
        self.assertEqual(gate["optimized_output_sha256"], self.m.TRANSFER_OUTPUT_SHA256)
        self.assertIs(gate["normal_optimized_byte_identical"], True)
        self.assertEqual(gate["executions"], [
            self.m.expected_execution_receipt(optimized=False),
            self.m.expected_execution_receipt(optimized=True),
        ])
        self.assertIs(gate["child_analytic_dependencies_authenticated"], False)
        self.assertIs(gate["finite_gate_passed"], True)
        self.assertIs(gate["analytic_implication_established"], False)
        self.assertEqual(gate["applicable_kernels"], 4022)
        self.assertEqual(gate["obstruction_kernels"], 473)
        self.assertEqual(gate["owned_rows"], 268110)
        self.assertEqual(gate["owned_physical_rows"], 302177)
        self.assertEqual(gate["owned_targets"], 4289760)

    def test_executed_gate_hostile_values_missing_extra_and_cross_mode_rejected(self):
        executed = copy.deepcopy(self.contract)
        executed["executed_finite_gates"] = [self.m.expected_executed_finite_gate()]
        mutations = (
            ("normal_output_sha256", "0" * 64),
            ("optimized_output_sha256", "0" * 64),
            ("normal_optimized_byte_identical", False),
            ("executions", []),
            ("child_analytic_dependencies_authenticated", True),
            ("owned_rows", 268109),
            ("finite_gate_passed", False),
            ("analytic_implication_established", True),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                hostile = copy.deepcopy(executed)
                hostile["executed_finite_gates"][0][field] = value
                self.rejected(hostile)

        hostile = copy.deepcopy(executed)
        hostile["executed_finite_gates"][0].pop("optimized_output_sha256")
        self.rejected(hostile, "executed finite gate schema changed")

        hostile = copy.deepcopy(executed)
        hostile["executed_finite_gates"][0]["invented_nested_field"] = False
        self.rejected(hostile, "executed finite gate schema changed")

        hostile = copy.deepcopy(executed)
        hostile["executed_finite_gates"][0]["expected_output_sha256"] = \
            self.m.TRANSFER_OUTPUT_SHA256
        self.rejected(hostile, "executed finite gate schema changed")

        for index, field, value in (
                (0, "mode", "optimized"),
                (0, "command", self.m.transfer_command(optimized=True)),
                (1, "cwd", "/hostile"),
                (1, "environment", {"LD_PRELOAD": "/hostile.so"}),
                (1, "returncode", 1),
                (1, "stderr_sha256", "0" * 64),
                (1, "stdout_sha256", "0" * 64),
                (1, "source_sha256", "0" * 64)):
            with self.subTest(execution=index, field=field):
                hostile = copy.deepcopy(executed)
                hostile["executed_finite_gates"][0]["executions"][index][field] = value
                self.rejected(hostile)

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

    def test_registry_states_exact_theorems_and_oriented_stub_assignment(self):
        axioms = self.contract["reviewed_analytic_axioms"]
        for rank, record in zip((2, 3, 4), axioms[1:4], strict=True):
            self.assertEqual(
                record["statement"],
                f"Every finite simple connected graph H of cyclomatic rank {['zero', 'one', 'two', 'three', 'four'][rank]} satisfies s+(H)>=|V(H)|.",
            )
            self.assertNotIn("attachment", record["statement"])
            self.assertEqual(record["hypotheses"], [
                "H is finite, simple, and connected",
                f"|E(H)|=|V(H)|+{rank - 1}",
            ])
        territory = axioms[4]["statement"]
        self.assertIn("U receives every crossing-path interior as a pendant stub", territory)
        self.assertIn("W receives none", territory)

    def test_bundled_hostile_ledger_is_exact(self):
        self.assertEqual(self.m.hostile_contract_checks(self.contract), 20)
        executed = copy.deepcopy(self.contract)
        executed["executed_finite_gates"] = [self.m.expected_executed_finite_gate()]
        self.assertEqual(self.m.hostile_contract_checks(executed), 20)


if __name__ == "__main__":
    unittest.main()
