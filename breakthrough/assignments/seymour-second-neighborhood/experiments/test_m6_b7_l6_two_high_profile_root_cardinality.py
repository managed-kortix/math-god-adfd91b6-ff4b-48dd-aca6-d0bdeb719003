#!/usr/bin/env python3
"""Regression tests for exact two-high root-cardinality strengthening."""

import tempfile
import unittest
from pathlib import Path

import check_m6_b7_l6_two_high_profile_root_cardinality as checker
import verify_m6_b7_l6_two_high_profile_root_cardinality_certificates as verifier


class TwoHighRootCardinalityTest(unittest.TestCase):
    def test_exact_scope(self):
        self.assertEqual(checker.SCOPE, (12, 13, 14, 15, 16, 17, 36, 37, 38, 39,
                                         40, 41, 42, 43, 55, 56, 57, 58, 59))

    def test_cover(self):
        checker.check_cover(regenerate=False)

    def test_semantics(self):
        checker.semantic_audit()

    def test_fresh_counter_dimensions(self):
        orbits = checker.independent_scope()
        self.assertEqual({checker.reconstruct(i, orbits)[3] for i in checker.SCOPE}, {(2433, 9571)})

    def test_strict_ledger(self):
        metadata, rows = verifier.load_ledger()
        verifier.verify_bindings(metadata)
        verifier.artifact_paths(rows)

    def test_rejects_ledger_orbit_mutation(self):
        data = verifier.LEDGER.read_text(encoding="ascii")
        mutated = data.replace("00\t12\to12", "00\t13\to12", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.tsv"
            path.write_text(mutated, encoding="ascii", newline="\n")
            with self.assertRaises(RuntimeError):
                verifier.load_ledger(path)

    def test_rejects_counter_mutation(self):
        orbits = checker.independent_scope()
        manifest, _ = checker.load_manifest()
        position, ordinal = 0, checker.SCOPE[0]
        names, clauses, selectors, delta = checker.reconstruct(ordinal, orbits)
        clauses[-1] = (-clauses[-1][0],)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.cnf"
            with path.open("w", encoding="ascii", newline="\n") as handle:
                for name, value in checker.expected_metadata(position, ordinal, orbits[ordinal], manifest,
                                                              selectors, delta):
                    handle.write(f"c {name} {value}\n")
                for number, name in enumerate(names, 1):
                    handle.write(f"c var {number} {name}\n")
                handle.write(f"p cnf {len(names)} {len(clauses)}\n")
                for clause in clauses:
                    handle.write(" ".join(map(str, clause)) + " 0\n")
            with self.assertRaises(RuntimeError):
                checker.check(path)


if __name__ == "__main__":
    unittest.main()
