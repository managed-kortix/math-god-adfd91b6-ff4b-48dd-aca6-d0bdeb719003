#!/usr/bin/env python3
"""Regression tests for authoritative all33 cardinality strengthening."""

import tempfile
import unittest
from pathlib import Path

import check_m6_b7_l6_exact_pair_hall_cardinality_strengthening as checker


class CardinalityStrengtheningTest(unittest.TestCase):
    def test_cover(self):
        checker.check_cover(regenerate=False)

    def test_semantics(self):
        checker.semantic_audit()

    def test_fresh_counter_dimensions(self):
        deltas = {checker.reconstruct(record)[5] for record in checker.independent_scope()}
        self.assertEqual(deltas, {(2433, 9571)})

    def test_rejects_counter_clause_mutation(self):
        checker.independent_scope()
        record = checker.producer.scope()[0]
        names, clauses, selectors, universe, support, delta = checker.reconstruct(
            checker.independent_scope()[0])
        manifest = checker.producer.manifest_payload(checker.producer.scope())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.cnf"
            view = checker._CNFView(names, list(clauses))
            view.clauses[-1] = (-view.clauses[-1][0],)
            checker.producer.write_membership(path, 0, record, view, selectors, universe, support,
                                              delta, manifest)
            with self.assertRaises(RuntimeError):
                checker.check(path)


if __name__ == "__main__":
    unittest.main()
