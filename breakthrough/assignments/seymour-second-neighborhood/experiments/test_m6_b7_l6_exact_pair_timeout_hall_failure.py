#!/usr/bin/env python3
"""Regression tests for the exact-pair Hall-failure extension."""

import tempfile
import unittest
import json
from pathlib import Path

import check_m6_b7_l6_exact_pair_timeout_hall_failure as checker
import m6_b7_l6_exact_pair_timeout_hall_failure as producer


class HallFailureTest(unittest.TestCase):
    def test_frozen_cover(self):
        checker.check_cover()

    def test_tiny_truth_table(self):
        checker.truth_table_audit()

    def test_frozen_scout(self):
        checker.check_scout()

    def test_exact_dimensions(self):
        for record in producer.scope():
            cnf, _, _, _ = producer.build_membership(record)
            base_variables, base_clauses = producer.singleton.dimensions(record[1])
            self.assertEqual((len(cnf.names) - base_variables, len(cnf.clauses) - base_clauses),
                             (142, 480))

    def test_rejects_manifest_mutation(self):
        data = checker.MANIFEST.read_bytes().replace(b"|Gamma(K)|<|K|", b"|Gamma(K)|>|K|", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.tsv"
            path.write_bytes(data)
            original = checker.MANIFEST
            try:
                checker.MANIFEST = path
                with self.assertRaises(RuntimeError):
                    checker.check_cover(regenerate=False)
            finally:
                checker.MANIFEST = original

    def test_rejects_equal_total_status_swap(self):
        data = json.loads(checker.SCOUT.read_text(encoding="ascii"))
        unsat = next(index for index, row in enumerate(data["rows"]) if row["status"] == "UNSAT")
        timeout = next(index for index, row in enumerate(data["rows"]) if row["status"] == "TIMEOUT")
        data["rows"][unsat]["status"], data["rows"][timeout]["status"] = \
            data["rows"][timeout]["status"], data["rows"][unsat]["status"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "swapped.json"
            path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="ascii")
            with self.assertRaises(RuntimeError):
                checker.check_scout(path)

    def test_compact_cnf_rejects_wrong_semantics(self):
        edges, chosen, clauses = checker.tiny_hall_cnf(2, 2)
        complete = [literal for row in edges for literal in row]
        select_both = list(chosen)
        self.assertFalse(checker.locally_satisfiable(clauses, complete + select_both))
        empty = [-literal for row in edges for literal in row]
        self.assertTrue(checker.locally_satisfiable(clauses, empty + select_both))


if __name__ == "__main__":
    unittest.main()
