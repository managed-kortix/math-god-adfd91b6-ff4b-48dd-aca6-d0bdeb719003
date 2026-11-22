#!/usr/bin/env python3
"""Regression and hostile tests for the narrow physical R61 theorem package."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
VERIFIER_PATH = ROOT / "research" / "r61-physical-single-block-theorem-verifier.py"
REGISTRY_PATH = ROOT / "research" / "r61-rank-six-single-block-owner-registry-verifier.py"


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


v = load_module(VERIFIER_PATH, "r61_physical_single_block_verifier")
r = load_module(REGISTRY_PATH, "r61_rank_six_typed_registry_verifier")


class R61PhysicalSingleBlockTests(unittest.TestCase):
    def run_script(self, path, optimized=False):
        command = [sys.executable, "-I", "-B"]
        if optimized:
            command.append("-O")
        command.extend([str(path), "--emit", "--print-manifest"])
        return subprocess.run(command, cwd=ROOT, check=False, capture_output=True)

    def test_normal_and_optimized_registry_receipts_match(self):
        normal = self.run_script(REGISTRY_PATH)
        optimized = self.run_script(REGISTRY_PATH, optimized=True)
        self.assertEqual(normal.returncode, 0, normal.stderr)
        self.assertEqual(optimized.returncode, 0, optimized.stderr)
        self.assertEqual(normal.stderr, b"")
        self.assertEqual(normal.stdout, optimized.stdout)
        receipt = r.strict_json_bytes(normal.stdout, "test registry receipt")
        self.assertTrue(receipt["registry"]["complete_disjoint_ownership"])
        self.assertEqual(receipt["registry"]["owners"], list(r.OWNERS))

    def test_normal_and_optimized_theorem_receipts_match(self):
        normal = self.run_script(VERIFIER_PATH)
        optimized = self.run_script(VERIFIER_PATH, optimized=True)
        self.assertEqual(normal.returncode, 0, normal.stderr)
        self.assertEqual(optimized.returncode, 0, optimized.stderr)
        self.assertEqual(normal.stderr, b"")
        self.assertEqual(normal.stdout, optimized.stdout)
        receipt = v.strict_json_bytes(normal.stdout, "test theorem receipt")
        self.assertEqual(receipt["theorem"], "R61-PHYSICAL-SINGLE-BLOCK")
        self.assertTrue(receipt["port_blind_structural_selector"])
        self.assertFalse(receipt["strict"])

    def test_strict_parser_rejects_duplicate_nan_and_trailing_bytes(self):
        for raw in (
            b'{"a":1,"a":2}\n',
            b'{"a":NaN}\n',
            b'{"a":1}\ntrailing',
            b'{ "a":1}\n',
        ):
            with self.assertRaises((v.VerificationError, ValueError)):
                v.strict_json_bytes(raw, "hostile parser input")

    def test_scope_widening_is_rejected(self):
        manifest = v.load_manifest()
        hostile = []
        candidate = deepcopy(manifest)
        candidate["scope"]["rank_six_side"]["positive_rank_cyclic_blocks"] = "arbitrary"
        hostile.append(candidate)
        candidate = deepcopy(manifest)
        candidate["scope"]["separator"]["kind"] = "generic-connector"
        hostile.append(candidate)
        candidate = deepcopy(manifest)
        candidate["scope"]["ports"] = "core-only"
        hostile.append(candidate)
        candidate = deepcopy(manifest)
        candidate["conclusion"]["strict"] = True
        hostile.append(candidate)
        for candidate in hostile:
            with self.assertRaises(v.VerificationError):
                v.validate_package(candidate, run_dependencies=False)

    def test_port_blind_selector_has_one_argument(self):
        v.audit_port_blind_contract()
        for family in ("K110-0", "K110-1", "K223"):
            self.assertIsInstance(v.select_structural_partition(family), dict)
        with self.assertRaises(TypeError):
            v.select_structural_partition("K223", 0)

    def test_structural_partitions_and_ledgers(self):
        self.assertEqual(v.audit_k110_0(), ((0, 1, 2, 3), (4,)))
        self.assertEqual(v.audit_k110_1()["ell"], "2h+1, h>=1")
        k223 = v.audit_k223()
        self.assertEqual(k223["fixed_k4"], [0, 3, 4, 5])
        self.assertEqual(k223["fixed_tree"], [1, 2])
        bound = v.audit_strict_ledgers()
        self.assertEqual(bound.floor, 0)
        self.assertTrue(bound.strict)

    def test_k223_bit_flip_fails(self):
        changed = "1" + v.K223_ROW[1:]
        edges = {pair for pair, bit in zip(v.PAIR6, changed) if bit == "1"}
        self.assertNotEqual(edges, v.K223_EDGES)

    def test_registry_owner_mutations_fail(self):
        registry = r.registry_payload()
        candidate = deepcopy(registry)
        candidate["owners"].remove("K110-1")
        with self.assertRaises(r.VerificationError):
            r.validate_registry(candidate)
        candidate = deepcopy(registry)
        candidate["owner_rules"]["K110-1"]["certificate"] = "kappa(R)<=|E(R)|+5"
        with self.assertRaises(r.VerificationError):
            r.validate_registry(candidate)

    def test_built_in_hostile_suites_are_exact(self):
        manifest = v.load_manifest()
        self.assertEqual(len(v.hostile_self_checks(manifest)), 14)
        self.assertEqual(len(r.hostile_self_checks(r.registry_payload())), 7)


if __name__ == "__main__":
    unittest.main()
