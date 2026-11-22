#!/usr/bin/env python3
"""Regression and hostile tests for the physical unit-star DNN theorem."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
VERIFIER_PATH = ROOT / "research" / "physical-unit-star-dnn-theorem-verifier.py"


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    if spec.loader is None:
        raise RuntimeError("missing verifier loader")
    spec.loader.exec_module(module)
    return module


v = load_module(VERIFIER_PATH, "physical_unit_star_dnn_theorem_verifier")


def add_edge(adjacency, u, w):
    adjacency.setdefault(u, set()).add(w)
    adjacency.setdefault(w, set()).add(u)


def cycle(adjacency, vertices):
    for index, vertex in enumerate(vertices):
        add_edge(adjacency, vertex, vertices[(index + 1) % len(vertices)])


def complete_bipartite(adjacency, left, right):
    for u in left:
        for w in right:
            add_edge(adjacency, u, w)


def materialize_unit_star(center_rank, cycle_lengths, *, shared_port=False,
                          chain_lengths=None, payload=True):
    """Make a literal theorem instance with many hostile ownership features."""
    adjacency = {}
    next_vertex = 0
    if center_rank == 0:
        center_vertices = [next_vertex]
        adjacency[next_vertex] = set()
        next_vertex += 1
    else:
        # K_{2,c+1} is simple, connected, bridge-free, and has rank c.
        left = [next_vertex, next_vertex + 1]
        next_vertex += 2
        right = list(range(next_vertex, next_vertex + center_rank + 1))
        next_vertex += center_rank + 1
        complete_bipartite(adjacency, left, right)
        center_vertices = left + right
    root_port = center_vertices[0]
    if chain_lengths is None:
        chain_lengths = [1 + (index % 3) for index in range(len(cycle_lengths))]
    for index, (q, length) in enumerate(zip(cycle_lengths, chain_lengths)):
        port = root_port if shared_port else center_vertices[index % len(center_vertices)]
        previous = port
        for _ in range(length):
            internal = next_vertex
            next_vertex += 1
            add_edge(adjacency, previous, internal)
            previous = internal
            if payload:
                leaf = next_vertex
                next_vertex += 1
                add_edge(adjacency, previous, leaf)
        vertices = list(range(next_vertex, next_vertex + q))
        next_vertex += q
        cycle(adjacency, vertices)
        add_edge(adjacency, previous, vertices[index % q])
        if payload:
            arm_leaf = next_vertex
            next_vertex += 1
            add_edge(adjacency, vertices[(index + 2) % q], arm_leaf)
    if payload:
        for port in center_vertices[:min(2, len(center_vertices))]:
            first = next_vertex
            second = next_vertex + 1
            next_vertex += 2
            add_edge(adjacency, port, first)
            add_edge(adjacency, first, second)
    return {vertex: sorted(neighbours) for vertex, neighbours in adjacency.items()}


class PhysicalUnitStarDNNTests(unittest.TestCase):
    def run_script(self, optimized=False):
        command = [sys.executable, "-I", "-B"]
        if optimized:
            command.append("-O")
        command.extend([str(VERIFIER_PATH), "--emit", "--print-manifest"])
        return subprocess.run(command, cwd=ROOT, check=False, capture_output=True)

    def test_normal_and_optimized_receipts_match(self):
        normal = self.run_script()
        optimized = self.run_script(optimized=True)
        self.assertEqual(normal.returncode, 0, normal.stderr)
        self.assertEqual(optimized.returncode, 0, optimized.stderr)
        self.assertEqual(normal.stderr, b"")
        self.assertEqual(normal.stdout, optimized.stdout)
        receipt = v.strict_json_bytes(normal.stdout, "test receipt")
        self.assertEqual(receipt["theorem"], "PHYSICAL-UNIT-STAR-DNN")
        self.assertTrue(receipt["strict"])

    def test_exact_symbolic_certificates(self):
        ledger = v.audit_symbolic_ledger()
        self.assertEqual(ledger["master_coefficients"], [1, 1, 1, 1, 1, 0])
        self.assertIn("19-6sqrt(5)<6", ledger["c_le_4_endpoint"])
        self.assertEqual(ledger["residual_direction"], "5+2epsilon_5>6")

    def test_all_c_le_four_rows_with_arbitrary_payloads(self):
        for center_rank in range(5):
            lengths = [5] * (7 - center_rank)
            graph = materialize_unit_star(center_rank, lengths, shared_port=True)
            receipt = v.check_instance(graph)
            self.assertEqual(receipt["center_rank"], center_rank)
            self.assertEqual(receipt["unit_leaf_count"], 7 - center_rank)
            self.assertEqual(receipt["certificate_status"], "CLOSED")
            self.assertEqual(sum(receipt["edge_ledger"]), receipt["edges"])

    def test_c5_long_arm_and_residual_are_distinguished(self):
        long_arm = v.check_instance(materialize_unit_star(5, [5, 9], shared_port=True))
        self.assertEqual(long_arm["certificate_status"], "CLOSED")
        residual = v.check_instance(materialize_unit_star(5, [5, 5], shared_port=True))
        self.assertEqual(residual["certificate_status"], "OPEN_BY_THIS_CERTIFICATE")

    def test_c6_fails_closed(self):
        with self.assertRaises(v.VerificationError):
            v.check_instance(materialize_unit_star(6, [5]))

    def test_nonhostile_arm_fails_closed(self):
        with self.assertRaises(v.VerificationError):
            v.check_instance(materialize_unit_star(4, [5, 5, 7]))

    def test_extra_positive_component_fails_star_ledger(self):
        graph = materialize_unit_star(4, [5, 5, 5])
        # Rewire a bridge-chain singleton into a triangle while preserving
        # connectivity; total beta rises and is rejected before any ownership.
        start = max(graph) + 1
        graph[start] = [start + 1, start + 2]
        graph[start + 1] = [start, start + 2]
        graph[start + 2] = [start, start + 1, 0]
        graph[0].append(start + 2)
        with self.assertRaises(v.VerificationError):
            v.check_instance(graph)

    def test_disconnected_and_parallel_encoding_fail(self):
        graph = materialize_unit_star(4, [5, 5, 5])
        graph[max(graph) + 1] = []
        with self.assertRaises(v.VerificationError):
            v.check_instance(graph)
        graph = materialize_unit_star(4, [5, 5, 5])
        vertex = min(graph)
        graph[vertex].append(graph[vertex][0])
        with self.assertRaises(v.VerificationError):
            v.check_instance(graph)

    def test_scope_widening_mutations_fail(self):
        manifest = v.load_manifest()
        mutations = []
        candidate = deepcopy(manifest)
        candidate["scope"]["center_rank_rows"].append(6)
        mutations.append(candidate)
        candidate = deepcopy(manifest)
        candidate["residual_rows"][0]["status"] = "CLOSED"
        mutations.append(candidate)
        candidate = deepcopy(manifest)
        candidate["scope"]["reduced_positive_hull"] = "arbitrary"
        mutations.append(candidate)
        candidate = deepcopy(manifest)
        candidate["proof_contract"]["center_bound"] = "kappa(C)<=m_C+c-1"
        mutations.append(candidate)
        for candidate in mutations:
            with self.assertRaises(v.VerificationError):
                v.validate_manifest(candidate)

    def test_strict_parser_rejects_duplicate_nan_and_trailing_bytes(self):
        for raw in (b'{"a":1,"a":2}\n', b'{"a":NaN}\n',
                    b'{"a":1}\ntrailing', b'{ "a":1}\n'):
            with self.assertRaises((v.VerificationError, ValueError)):
                v.strict_json_bytes(raw, "hostile parser")

    def test_built_in_hostile_suite_width(self):
        self.assertEqual(len(v.hostile_self_checks(v.load_manifest())), 12)


if __name__ == "__main__":
    unittest.main()
