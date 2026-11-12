#!/usr/bin/env python3
"""Focused hostile tests for the order-nine master theorem gate.

The suite exercises the master's cheap trust-boundary helpers.  It deliberately
never launches the hour-scale combined structural replay or downstream census.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
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
        self.assertEqual(len(self.master.PYTHON_PINS), 14)
        self.assertEqual(len(self.master.DATA_PINS), 44)
        self.assertEqual(len(self.master.DOCUMENT_PINS), 8)
        registries = tuple(map(set, (self.master.PYTHON_PINS,
                                     self.master.DATA_PINS,
                                     self.master.DOCUMENT_PINS)))
        self.assertTrue(all(registries[left].isdisjoint(registries[right])
                            for left in range(3) for right in range(left + 1, 3)))
        self.assertEqual(frozenset(self.master.DATA_PINS),
                         self.master.EXPECTED_DATA_PATHS)
        observed = self.master.audit_pins()
        self.assertEqual(len(observed), 66)

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

    def test_live_k403_gate_executes_scalar_vector_and_residual_orbits_paths(self):
        receipt = self.master.validate_live_coarse_equivalence()
        self.assertEqual(receipt["fixture"], "real order-nine local kernel K403")
        self.assertEqual(receipt["physical_row_total"], 12_288)
        self.assertEqual(receipt["residual_row_total"], 658)
        self.assertEqual(receipt["decision_sha256"],
                         self.master.K403_DECISION_SHA256)
        self.assertEqual(receipt["decision_receipt_encoding"],
                         "sha256(concatenated canonical ASCII JSON lines "
                         "[403,row,decision] for every physical row in "
                         "mixed-radix product order)")
        self.assertTrue(
            receipt["live_scalar_vector_and_residual_orbits_equivalent"])

    def test_live_k403_gate_rejects_executed_semantic_mutations(self):
        producer = self.master.load_pinned_module(
            self.master.CENSUS_PRODUCER, "rank7_o9_hostile_live_coarse")
        original_scalar = self.master.COARSE_ENGINE.read_text("ascii")
        original_producer = self.master.CENSUS_PRODUCER.read_text("ascii")
        mutations = (
            ("scalar-18-to-17", "18 * multiplicity", "17 * multiplicity", True),
            ("scalar-plus-10", "10 - 13 * odd", "9 - 13 * odd", True),
            ("scalar-minus-13", "10 - 13 * odd", "10 - 12 * odd", True),
            ("scalar-same-color", "if required and color == other_color:",
             "if False and required and color == other_color:", True),
            ("scalar-color-cap", "limit = min(used + 1, 4)",
             "limit = min(used + 1, 3)", True),
            ("producer-superset-to-subset",
             "np.minimum(view[:, :block], view[:, block:], out=view[:, :block])",
             "np.minimum(view[:, block:], view[:, :block], out=view[:, block:])", False),
            ("producer-strict-to-nonstrict", "selected = minimum[support] > threshold",
             "selected = minimum[support] >= threshold", False),
            ("producer-budget", "BUDGET_SCALED = 180", "BUDGET_SCALED = 181", False),
        )
        for label, old, new, scalar_side in mutations:
            with self.subTest(label=label):
                source = original_scalar if scalar_side else original_producer
                hostile = source.replace(old, new, 1)
                self.assertNotEqual(hostile, source)
                if scalar_side:
                    predicate = self.master._load_source_coarse_predicate(hostile)
                    candidate = producer
                else:
                    candidate = mock.Mock(wraps=producer)
                    namespace = dict(producer.__dict__)
                    exec(compile(hostile, str(self.master.CENSUS_PRODUCER), "exec"),
                         namespace)
                    candidate.coarse_sieve = namespace["coarse_sieve"]
                    candidate.residual_orbits = namespace["residual_orbits"]
                    predicate = self.master._load_source_coarse_predicate()
                self.assert_rejected(lambda candidate=candidate, predicate=predicate:
                    self.master.validate_live_coarse_equivalence(
                        producer=candidate, scalar_predicate=predicate))

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

    def test_corrected_switched_ray_dependency_is_forward_only(self):
        source = self.master.SWITCHED_THREE_RAY_NOTE.read_text("ascii")
        self.assertEqual(
            self.master.sha256(source.encode("ascii")),
            self.master.DOCUMENT_PINS[self.master.SWITCHED_THREE_RAY_NOTE])
        self.assertIn("rigorous fixed-parity-monotone bound", source)
        self.assertIn("No converse is claimed for arbitrary switched-three-ray\nGrams", source)
        self.assertIn("forward implication to structural ownership", source)
        self.assertNotIn("This proves both\ndirections", source)
        self.assertNotIn("linear Gram-chain construction has excess", source)

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

    def test_transfer_adapter_is_executed_but_remains_nonpromotional(self):
        receipt = self.master.run_transfer_dependency_adapter()
        self.assertEqual(receipt["source_sha256"],
                         self.master.PYTHON_PINS[
                             self.master.TRANSFER_DEPENDENCY_ADAPTER])
        self.assertEqual(receipt["normal_output_sha256"],
                         self.master.TRANSFER_DEPENDENCY_ADAPTER_OUTPUT_SHA256)
        self.assertEqual(receipt["optimized_output_sha256"],
                         self.master.TRANSFER_DEPENDENCY_ADAPTER_OUTPUT_SHA256)
        self.assertIs(receipt["normal_optimized_byte_identical"], True)
        self.assertEqual(receipt["execution_mode"],
                         "default-registered-unexecuted-finite-gate")
        self.assertEqual(receipt["claim_boundary"],
                         "source-byte-authenticated-nonpromotional-registry-only")
        for field in ("finite_gate_passed", "analytic_dependencies_authenticated",
                      "reviewed_axioms_accepted",
                      "bounded_transfer_implication_discharged",
                      "theorem_eligible", "global_claim"):
            with self.subTest(field=field):
                self.assertIs(receipt[field], False)
        result = receipt["result"]
        self.assertEqual(set(result), {"contract", "hostile_mutations_rejected", "status"})
        self.assertEqual(result["status"], "PASS-NONPROMOTIONAL")
        self.assertEqual(result["hostile_mutations_rejected"], 20)
        contract = result["contract"]
        gate = contract["executed_finite_gates"]
        self.assertEqual(len(gate), 1)
        self.assertEqual(gate[0]["evidence_kind"],
                         "registered-unexecuted-finite-gate")
        self.assertIs(gate[0]["finite_gate_passed"], False)
        self.assertIs(gate[0]["analytic_implication_established"], False)
        self.assertEqual([row["id"] for row in contract["reviewed_analytic_axioms"]],
                         list(self.master.TRANSFER_ADAPTER_AXIOM_IDS))
        self.assertTrue(all(row["status"] == "review-required" and
                            row["semantic_proof_executed"] is False
                            for row in contract["reviewed_analytic_axioms"]))
        for field in ("all_analytic_dependencies_executed",
                      "analytic_dependencies_authenticated",
                      "reviewed_axioms_accepted",
                      "bounded_transfer_implication_discharged",
                      "theorem_eligible", "global_claim"):
            with self.subTest(contract_field=field):
                self.assertIs(contract[field], False)
        self.assertIs(contract["rank_type_exhaustion"]
                      ["analytic_theorem_application_established"], False)

    def test_transfer_adapter_runs_explicit_normal_and_optimized_commands(self):
        real_run = self.master.subprocess.run
        commands = []

        def capture(command, **kwargs):
            commands.append((list(command), dict(kwargs["env"]), kwargs["cwd"]))
            return real_run(command, **kwargs)

        with mock.patch.dict(os.environ, {"PYTHONOPTIMIZE": "2"}, clear=False):
            with mock.patch.object(self.master.subprocess, "run", side_effect=capture):
                self.master.run_transfer_dependency_adapter()
        self.assertEqual(len(commands), 2)
        normal, optimized = commands
        self.assertEqual(normal[0], [sys.executable, "-I", "-S", "-B",
                         str(self.master.TRANSFER_DEPENDENCY_ADAPTER)])
        self.assertEqual(optimized[0], [sys.executable, "-I", "-S", "-B", "-O",
                         str(self.master.TRANSFER_DEPENDENCY_ADAPTER)])
        for command, environment, cwd in commands:
            with self.subTest(command=command):
                self.assertEqual(environment, {})
                self.assertEqual(cwd, self.master.ROOT)

    def test_transfer_adapter_isolated_mode_suppresses_ambient_startup_hook(self):
        with tempfile.TemporaryDirectory() as directory:
            sentinel = Path(directory) / "sitecustomize-executed"
            hook = Path(directory) / "sitecustomize.py"
            hook.write_text(
                "from pathlib import Path\n"
                f"Path({str(sentinel)!r}).write_text('executed', encoding='ascii')\n",
                encoding="ascii",
            )
            with mock.patch.dict(
                    os.environ,
                    {"PYTHONPATH": directory, "PYTHONHOME": directory,
                     "PYTHONSTARTUP": str(hook), "PYTHONINSPECT": "1",
                     "PYTHONOPTIMIZE": "2", "LD_PRELOAD": "/hostile/preload.so",
                     "LD_AUDIT": "/hostile/audit.so", "BASH_ENV": str(hook),
                     "ENV": str(hook), "LOCPATH": directory}, clear=False):
                receipt = self.master.run_transfer_dependency_adapter()
            self.assertFalse(sentinel.exists())
            self.assertEqual(receipt["normal_output_sha256"],
                             self.master.TRANSFER_DEPENDENCY_ADAPTER_OUTPUT_SHA256)
            self.assertEqual(receipt["optimized_output_sha256"],
                             self.master.TRANSFER_DEPENDENCY_ADAPTER_OUTPUT_SHA256)
            self.assertIs(receipt["normal_optimized_byte_identical"], True)

    def test_transfer_adapter_no_site_mode_suppresses_prefix_sitecustomize(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            created = subprocess.run(
                [sys.executable, "-m", "venv", "--without-pip", str(root / "venv")],
                check=False, capture_output=True)
            self.assertEqual(created.returncode, 0, created.stderr.decode())
            venv_python = root / "venv" / "bin" / "python"
            site_packages = (root / "venv" / "lib" /
                             f"python{sys.version_info.major}.{sys.version_info.minor}" /
                             "site-packages")
            site_packages.mkdir(parents=True, exist_ok=True)
            sentinel = root / "prefix-sitecustomize-executed"
            (site_packages / "sitecustomize.py").write_text(
                "from pathlib import Path\n"
                f"Path({str(sentinel)!r}).write_text('executed', encoding='ascii')\n",
                encoding="ascii",
            )
            baseline = subprocess.run(
                [str(venv_python), "-I", "-B", "-c", "pass"],
                check=False, capture_output=True,
                env={"LANG": "C", "LC_ALL": "C",
                     "PYTHONDONTWRITEBYTECODE": "1"})
            self.assertEqual(baseline.returncode, 0, baseline.stderr.decode())
            self.assertTrue(sentinel.is_file())
            sentinel.unlink()
            with mock.patch.object(self.master.sys, "executable", str(venv_python)):
                receipt = self.master.run_transfer_dependency_adapter()
            self.assertFalse(sentinel.exists())
            self.assertEqual(receipt["normal_output_sha256"],
                             self.master.TRANSFER_DEPENDENCY_ADAPTER_OUTPUT_SHA256)
            self.assertEqual(receipt["optimized_output_sha256"],
                             self.master.TRANSFER_DEPENDENCY_ADAPTER_OUTPUT_SHA256)

    def test_transfer_adapter_hostile_promotion_and_gate_schema_rejected(self):
        receipt = self.master.run_transfer_dependency_adapter()
        result = receipt["result"]
        mutations = []
        for field in ("all_analytic_dependencies_executed",
                      "analytic_dependencies_authenticated",
                      "reviewed_axioms_accepted",
                      "bounded_transfer_implication_discharged",
                      "theorem_eligible", "global_claim"):
            hostile = deepcopy(result)
            hostile["contract"][field] = True
            mutations.append(hostile)
        hostile = deepcopy(result)
        hostile["contract"]["executed_finite_gates"][0]["finite_gate_passed"] = True
        mutations.append(hostile)
        hostile = deepcopy(result)
        hostile["contract"]["executed_finite_gates"][0]["extra"] = False
        mutations.append(hostile)
        hostile = deepcopy(result)
        hostile["contract"]["reviewed_analytic_axioms"][0]["status"] = "accepted"
        mutations.append(hostile)
        hostile = deepcopy(result)
        hostile["contract"]["rank_type_exhaustion"][
            "analytic_theorem_application_established"] = True
        mutations.append(hostile)
        for hostile in mutations:
            with self.subTest(hostile=hostile):
                self.assert_rejected(lambda hostile=hostile:
                    self.master.validate_transfer_dependency_adapter(hostile))

    def test_quick_manifest_reports_transfer_review_block_not_authentication(self):
        manifest = self.master.audit(full=False)
        receipt = manifest["transfer_dependency_adapter"]
        self.assertIs(receipt["analytic_dependencies_authenticated"], False)
        self.assertIs(receipt["reviewed_axioms_accepted"], False)
        self.assertIs(receipt["bounded_transfer_implication_discharged"], False)
        self.assertIs(receipt["theorem_eligible"], False)
        self.assertNotIn("adapter_authenticated", receipt)

    def test_run_child_rejects_output_only_forgery_before_validation(self):
        completed = subprocess.CompletedProcess(
            args=[], returncode=0,
            stdout=b'{"status":"passed"}\n', stderr=b"")
        with mock.patch.object(self.master.subprocess, "run", return_value=completed):
            self.assert_rejected(lambda: self.master.run_child(
                "upstream-sos-dominant", self.master.UPSTREAM, (),
                self.master.UPSTREAM_OUTPUT_SHA256, self.master.validate_upstream))

    def test_child_command_and_environment_are_isolated_and_mode_explicit(self):
        self.assertEqual(
            self.master.child_command(self.master.UPSTREAM, (), optimized=False),
            [sys.executable, "-I", "-S", "-B", str(self.master.UPSTREAM)])
        self.assertEqual(
            self.master.child_command(self.master.UPSTREAM, (), optimized=True),
            [sys.executable, "-I", "-S", "-B", "-O", str(self.master.UPSTREAM)])
        with self.assertRaises(TypeError):
            self.master.child_command(self.master.UPSTREAM, ())
        with mock.patch.object(self.master.sys, "executable", "relative-python"):
            self.assert_rejected(lambda: self.master.child_command(
                self.master.UPSTREAM, (), optimized=False))
        with mock.patch.dict(
                os.environ,
                {"PYTHONPATH": "/hostile", "PYTHONHOME": "/hostile",
                 "PYTHONSTARTUP": "/hostile/start.py", "PYTHONINSPECT": "1",
                 "PYTHONOPTIMIZE": "2", "LD_PRELOAD": "/hostile/preload.so",
                 "LD_AUDIT": "/hostile/audit.so", "BASH_ENV": "/hostile/bash-env",
                 "ENV": "/hostile/env", "LOCPATH": "/hostile/locale"}, clear=False):
            environment = self.master.child_environment()
        self.assertEqual(environment, {})
        self.assertTrue(Path(sys.executable).is_absolute())

    def test_run_python_pair_binds_returncode_stderr_and_exact_modes(self):
        ok = subprocess.CompletedProcess(args=[], returncode=0,
                                        stdout=b"same\n", stderr=b"")
        commands = []

        def capture(command, **kwargs):
            commands.append((list(command), dict(kwargs["env"]), kwargs["cwd"]))
            return ok

        with mock.patch.object(self.master.subprocess, "run", side_effect=capture):
            output, receipt = self.master.run_python_pair(
                "synthetic", self.master.UPSTREAM, ("--synthetic",))
        self.assertEqual(output, b"same\n")
        self.assertEqual(set(receipt), self.master.PYTHON_PAIR_RECEIPT_FIELDS)
        self.assertEqual(receipt["schema"], self.master.PYTHON_PAIR_RECEIPT_SCHEMA)
        self.assertEqual(receipt["source_path"], str(self.master.UPSTREAM))
        self.assertEqual(receipt["source_sha256"],
                         self.master.PYTHON_PINS[self.master.UPSTREAM])
        self.assertEqual(receipt["arguments"], ["--synthetic"])
        self.assertEqual(receipt["normal"]["mode"], "normal")
        self.assertEqual(receipt["optimized"]["mode"], "optimized")
        self.assertEqual(receipt["normal"]["command"], commands[0][0])
        self.assertEqual(receipt["optimized"]["command"], commands[1][0])
        self.assertEqual(receipt["normal"]["cwd"], str(self.master.ROOT))
        self.assertEqual(receipt["normal"]["environment"], {})
        self.assertEqual(receipt["normal"]["returncode"], 0)
        self.assertEqual(receipt["normal"]["stderr_sha256"], self.master.EMPTY_SHA256)
        self.assertIs(receipt["normal_optimized_stdout_byte_identical"], True)
        self.assertEqual(commands, [
            ([sys.executable, "-I", "-S", "-B", str(self.master.UPSTREAM),
              "--synthetic"], {}, self.master.ROOT),
            ([sys.executable, "-I", "-S", "-B", "-O", str(self.master.UPSTREAM),
              "--synthetic"], {}, self.master.ROOT),
        ])
        for hostile in (
                subprocess.CompletedProcess(args=[], returncode=1,
                                            stdout=b"same\n", stderr=b""),
                subprocess.CompletedProcess(args=[], returncode=0,
                                            stdout=b"same\n", stderr=b"hostile")):
            with self.subTest(hostile=hostile):
                with mock.patch.object(self.master.subprocess, "run",
                                       return_value=hostile):
                    self.assert_rejected(lambda: self.master.run_python_pair(
                        "synthetic", self.master.UPSTREAM, ()))
        differing = [
            subprocess.CompletedProcess(args=[], returncode=0,
                                        stdout=b"normal\n", stderr=b""),
            subprocess.CompletedProcess(args=[], returncode=0,
                                        stdout=b"optimized\n", stderr=b""),
        ]
        with mock.patch.object(self.master.subprocess, "run", side_effect=differing):
            self.assert_rejected(lambda: self.master.run_python_pair(
                "synthetic", self.master.UPSTREAM, ()))

    def test_noncanonical_or_trailing_child_stdout_is_rejected(self):
        bad_outputs = (
            b'{"status":"passed"}\ntrailing\n',
            b'{ "status":"passed"}\n',
            b'{"status":1.0}\n',
            b'{"status":"passed","status":"passed"}\n',
        )
        for raw in bad_outputs:
            with self.subTest(raw=raw):
                completed = subprocess.CompletedProcess(
                    args=[], returncode=0, stdout=raw, stderr=b"")
                with mock.patch.object(self.master.subprocess, "run",
                                       return_value=completed):
                    self.assert_rejected(lambda: self.master.run_child(
                        "upstream-sos-dominant", self.master.UPSTREAM, (), None,
                        lambda result: None))

    def test_structural_live_key_sink_remains_explicitly_unresolved(self):
        with self.assertRaisesRegex(RuntimeError,
                                    "current-process.*not theorem-eligible"):
            self.master.run_structural_combined_with_keys()

    def test_coarse_atom_runs_explicit_isolated_pair_without_nested_child(self):
        real_run = self.master.subprocess.run
        commands = []

        def capture(command, **kwargs):
            commands.append((list(command), dict(kwargs["env"]), kwargs["cwd"]))
            return real_run(command, **kwargs)

        with mock.patch.object(self.master.subprocess, "run", side_effect=capture):
            receipt = self.master.run_coarse_atom()
        self.assertEqual(receipt["normal_O_byte_identity"],
                         "enforced by isolated master pair")
        execution = receipt["execution"]
        self.assertEqual(execution["normal"]["mode"], "normal")
        self.assertEqual(execution["optimized"]["mode"], "optimized")
        self.assertEqual(execution["normal"]["source_path"],
                         str(self.master.COARSE_ATOM))
        self.assertEqual(execution["normal"]["returncode"], 0)
        self.assertIs(execution["normal"]["stderr_empty"], True)
        self.assertEqual(commands[0][0], [sys.executable, "-I", "-S", "-B",
                         str(self.master.COARSE_ATOM), "--emit"])
        self.assertEqual(commands[1][0], [sys.executable, "-I", "-S", "-B", "-O",
                         str(self.master.COARSE_ATOM), "--emit"])
        for command, environment, cwd in commands:
            with self.subTest(command=command):
                self.assertEqual(environment, {})
                self.assertEqual(cwd, self.master.ROOT)

    def test_quick_manifest_is_never_theorem_eligible(self):
        manifest = self.master.audit(full=False)
        self.assertIs(manifest["theorem_eligible"], False)
        self.assertIs(manifest["global_claim"], False)
        self.assertEqual(manifest["mode"], "quick")
        self.assertEqual(manifest["evidence_kind"],
                         "fail-closed-authentication-only")
        boundary = manifest["runtime_trust_boundary"]
        self.assertIn("already-started parent Python interpreter", boundary)
        self.assertIn("current-process imports", boundary)
        self.assertIn("explicit normal and -O executions", boundary)
        self.assertIn("literal env={}", boundary)
        self.assertIn("structural live key sink remains unresolved", boundary)
        self.assertIn("full/theorem mode is hard-blocked", boundary)

    def test_full_gate_is_explicitly_blocked_before_any_expensive_child(self):
        names = ("run_structural_combined_with_keys", "run_child", "run_cycle",
                 "compose_exact_stage_keys")
        patches = [mock.patch.object(self.master, name) for name in names]
        children = [patch.start() for patch in patches]
        try:
            with self.assertRaisesRegex(
                    RuntimeError, "isolated structural key sink.*authenticated StageLedger"):
                self.master.audit(full=True)
        finally:
            for patch in reversed(patches):
                patch.stop()
        for child in children:
            child.assert_not_called()

    def test_legacy_local_premise_discharge_path_is_deleted(self):
        self.assertFalse(hasattr(self.master, "validate_transfer_analytic_adapter"))
        self.assertFalse(hasattr(self.master, "discharge_finite_premise"))
        self.assertFalse(hasattr(self.master, "full_manifest"))
        source = self.master.Path(self.master.__file__).read_text("ascii")
        self.assertNotIn("validate_transfer_analytic_adapter", source)
        self.assertNotIn("adapter_authenticated", source)
        self.assertNotIn("finite_premise_discharged\": True", source)

    def test_master_and_registered_sources_contain_no_assert_statement(self):
        self.assertEqual(self.master.audit_no_asserts(),
                         len(self.master.PYTHON_PINS) + 1)


if __name__ == "__main__":
    unittest.main()
