#!/usr/bin/env python3
"""Focused hostile tests for the order-nine master theorem gate.

The suite exercises the master's cheap trust-boundary helpers.  It deliberately
never launches the hour-scale combined structural replay or downstream census.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock

PATH = Path(__file__).with_name("rank-seven-order-nine-kernel-theorem-verifier.py")


def load_master():
    spec = importlib.util.spec_from_file_location("rank7_order9_master_test", PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load order-nine master")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OrderNineMasterHostileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.master = load_master()

    def assert_rejected(self, action):
        with self.assertRaises((KeyError, OSError, RuntimeError, TypeError, ValueError)):
            action()

    def test_strict_json_rejects_float_duplicate_bool_integer_and_noncanonical(self):
        for raw in (b'{"x":1.0}\n', b'{"x":1e999}\n', b'{"x":NaN}\n',
                    b'{"x":1,"x":2}\n', b'{ "x":1}\n', b'{"x":1}'):
            with self.subTest(raw=raw):
                self.assert_rejected(lambda raw=raw: self.master.strict_json(raw, "hostile"))
        for value in (True, False, 1.0, -1):
            with self.subTest(value=value):
                self.assert_rejected(lambda value=value:
                                     self.master.exact_int(value, "integer"))

    def test_dependency_registry_is_exact_complete_and_disjoint(self):
        self.assertEqual(len(self.master.PYTHON_PINS), 13)
        self.assertEqual(len(self.master.DATA_PINS), 44)
        self.assertEqual(len(self.master.DOCUMENT_PINS), 7)
        registries = tuple(map(set, (self.master.PYTHON_PINS,
                                     self.master.DATA_PINS,
                                     self.master.DOCUMENT_PINS)))
        self.assertTrue(all(registries[left].isdisjoint(registries[right])
                            for left in range(3) for right in range(left + 1, 3)))
        self.assertEqual(frozenset(self.master.DATA_PINS),
                         self.master.EXPECTED_DATA_PATHS)
        observed = self.master.audit_pins()
        self.assertEqual(len(observed), 64)

    def test_partition_rejects_gap_overlap_physical_and_type_laundering(self):
        mutations = []
        gap = deepcopy(self.master.PARTITION_ORBITS)
        gap["gram"] -= 1
        mutations.append((gap, self.master.PARTITION_PHYSICAL))
        overlap = deepcopy(self.master.PARTITION_ORBITS)
        overlap["gram"] += 1
        mutations.append((overlap, self.master.PARTITION_PHYSICAL))
        wrong_precedence = deepcopy(self.master.PARTITION_ORBITS)
        wrong_precedence["sos"] += 1
        wrong_precedence["transfer"] -= 1
        mutations.append((wrong_precedence, self.master.PARTITION_PHYSICAL))
        physical = deepcopy(self.master.PARTITION_PHYSICAL)
        physical["gram"] -= 1
        mutations.append((self.master.PARTITION_ORBITS, physical))
        boolean = deepcopy(self.master.PARTITION_ORBITS)
        boolean["obstruction"] = True
        mutations.append((boolean, self.master.PARTITION_PHYSICAL))
        for orbits, masses in mutations:
            with self.subTest(orbits=orbits, masses=masses):
                self.assert_rejected(lambda orbits=orbits, masses=masses:
                                     self.master.validate_partition(orbits, masses))

    def test_coarse_atom_and_order_nine_application_are_separate_exact_contracts(self):
        contract = self.master.audit_coarse_source_contract()
        self.assertEqual(contract["atom_proof_scope"],
                         "47 order-four kernels; reusable exact tetrahedral inequalities only")
        self.assertEqual(contract["application_scope"],
                         "all 4,495 order-nine kernels and their parity orbits")
        atom = self.master.run_coarse_atom()
        self.assertEqual(atom["application_scope"], "not an order-nine row scan")
        application = self.master.validate_coarse_application_chunks()
        self.assertEqual(application["kernel_total"], 4495)
        self.assertEqual(application["coarse_owner_orbits"], 62_331_675)
        self.assertTrue(application["per_kernel_complements_validated"])
        self.assertFalse(application["coarse_owner_keys_materialized"])

    def test_coarse_semantic_constant_and_retained_gram_mutations_fail(self):
        mutations = (
            lambda x: x["different_color_scaled_cost"].__setitem__(
                "odd_positive", "18*m-10-13*o"),
            lambda x: x["different_color_scaled_cost"].__setitem__(
                "odd_positive", "18*m+10+13*o"),
            lambda x: x.__setitem__("budget_scaled", 181),
            lambda x: x.__setitem__("same_color_legal_iff", "any o"),
            lambda x: x.__setitem__("owner_semantics", "canonical target only"),
        )
        for mutate in mutations:
            hostile = deepcopy(self.master.COARSE_ATOM_CONTRACT)
            mutate(hostile)
            self.assert_rejected(
                lambda hostile=hostile: self.master.audit_coarse_source_contract(hostile))

    def test_coarse_source_constant_mutations_fail_independently_of_counts(self):
        producer = self.master.CENSUS_PRODUCER.read_text("ascii")
        for old, new in (
                ("- 10 * np.bitwise_count(support)",
                 "+ 10 * np.bitwise_count(support)"),
                ("+ 13 * odd_sum", "- 13 * odd_sum"),
                ("BUDGET_SCALED = 180", "BUDGET_SCALED = 181")):
            hostile = producer.replace(old, new, 1)
            self.assertNotEqual(hostile, producer)
            self.assert_rejected(lambda hostile=hostile:
                                 self.master.audit_coarse_source_contract(
                                     producer_source=hostile))
        atom = self.master.COARSE_ATOM.read_text("ascii")
        hostile = atom.replace("if odd:\n                return None",
                               "if False:\n                return None", 1)
        self.assertNotEqual(hostile, atom)
        self.assert_rejected(lambda:
                             self.master.audit_coarse_source_contract(
                                 atom_source=hostile))

    def test_target_equivalent_is_bookkeeping_not_materialized_keys(self):
        accounting = self.master.validate_target_accounting()
        self.assertEqual(accounting["coarse_target_equivalent"], 997_306_800)
        self.assertEqual(accounting["residual_frontier_targets"], 45_374_320)
        self.assertEqual(accounting["parity_target_equivalent"], 1_042_681_120)
        self.assertIsNone(accounting["coarse_owner_key_digest"])
        self.assertIn("bookkeeping only", accounting["semantics"])
        self.assert_rejected(lambda:
            self.master.validate_target_accounting(
                self.master.COARSE_ORBITS - 1, self.master.RESIDUAL_ORBITS + 1))

    def test_structural_validator_rejects_fast_substitution_and_counter_laundering(self):
        result = json.loads(Path("/tmp/struct-fast-current.json").read_text()) \
            if Path("/tmp/struct-fast-current.json").is_file() else None
        if result is None:
            completed = subprocess.run(
                [sys.executable, "-B", str(self.master.STRUCTURAL)],
                check=False, capture_output=True,
                env={"PYTHONDONTWRITEBYTECODE": "1"})
            self.assertEqual(completed.returncode, 0, completed.stderr.decode())
            self.assertEqual(completed.stderr, b"")
            result = json.loads(completed.stdout)
        self.master.validate_structural(result, predicates=False, census=False)
        self.assert_rejected(lambda:
            self.master.validate_structural(result, predicates=True, census=True))

        hostile = deepcopy(result)
        hostile["predicate_replay_eligible"] = True
        hostile["census_reconstruction"] = True
        hostile["census_reconstruction_requested"] = True
        hostile["census_reconstruction_eligible"] = True
        hostile["combined_replay_eligible"] = True
        hostile["mode"] = "fresh-census-plus-fresh-full-predicate-replay"
        self.assert_rejected(lambda:
            self.master.validate_structural(hostile, predicates=True, census=True))

    def test_structural_validator_rejects_extra_missing_bool_and_wrong_vectors(self):
        fields = {key: None for key in self.master.STRUCTURAL_FIELDS}
        fields["unexpected"] = 0
        self.assert_rejected(lambda:
            self.master.validate_structural(fields, predicates=True, census=True))
        missing = {key: None for key in self.master.STRUCTURAL_FIELDS
                   if key != "predicate_calls"}
        self.assert_rejected(lambda:
            self.master.validate_structural(missing, predicates=True, census=True))

    def test_exact_downstream_schemas_reject_partial_extra_and_bool(self):
        bad_values = (
            (self.master.validate_upstream,
             {"schema": "rank-seven-order-nine-upstream-owner-replay-v1"}),
            (self.master.validate_cycle,
             {"third": {"record_total": 631}, "fourth": {"record_total": 1036}}),
            (self.master.validate_transfer,
             {"source_orbits_recomputed": 272_520, "extra": 0}),
            (self.master.validate_obstruction,
             {"frontier_rows": True}),
        )
        for validator, payload in bad_values:
            with self.subTest(validator=validator.__name__):
                self.assert_rejected(lambda validator=validator, payload=payload:
                                     validator(payload))

    def test_run_child_rejects_output_only_forgery_before_validation(self):
        completed = subprocess.CompletedProcess(
            args=[], returncode=0,
            stdout=b'{"status":"passed"}\n', stderr=b"")
        with mock.patch.object(self.master.subprocess, "run", return_value=completed):
            self.assert_rejected(lambda: self.master.run_child(
                "upstream-sos-dominant", self.master.UPSTREAM, (),
                self.master.UPSTREAM_OUTPUT_SHA256, self.master.validate_upstream))

    def test_child_command_propagates_optimizer_mode_and_disables_bytecode(self):
        command = self.master.child_command(self.master.UPSTREAM, ())
        self.assertEqual(command[0], sys.executable)
        self.assertIn("-B", command)
        if sys.flags.optimize:
            self.assertIn("-O", command)
        else:
            self.assertNotIn("-O", command)

    def test_quick_manifest_is_never_theorem_eligible(self):
        manifest = self.master.audit(full=False)
        self.assertIs(manifest["theorem_eligible"], False)
        self.assertIs(manifest["global_claim"], False)
        self.assertEqual(manifest["mode"], "quick")
        self.assertEqual(manifest["evidence_kind"],
                         "fail-closed-authentication-only")

    def test_full_gate_is_explicitly_blocked_before_any_expensive_child(self):
        with mock.patch.object(self.master, "run_structural_combined_with_keys") as child:
            with self.assertRaisesRegex(
                    RuntimeError, "authenticated StageLedger receipts"):
                self.master.audit(full=True)
            child.assert_not_called()

    def test_legacy_local_premise_discharge_cannot_promote(self):
        with self.assertRaisesRegex(RuntimeError, "discharge disabled"):
            self.master.discharge_finite_premise({}, {}, {}, {}, {}, {})

    def test_master_and_registered_sources_contain_no_assert_statement(self):
        self.assertEqual(self.master.audit_no_asserts(),
                         len(self.master.PYTHON_PINS) + 1)


if __name__ == "__main__":
    unittest.main()
