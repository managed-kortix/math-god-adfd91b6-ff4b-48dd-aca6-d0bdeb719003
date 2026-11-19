#!/usr/bin/env python3
"""Regression tests for the clean B6-l5 root-cardinality certificate."""

import tempfile
import unittest
from pathlib import Path

import check_m6_clean_sink_B6_l5_root_cardinality as checker
import verify_m6_clean_sink_B6_l5_root_cardinality_certificate as verifier


class CleanB6L5RootCardinalityTest(unittest.TestCase):
    def test_cover(self):
        checker.check_manifest_and_hashes(regenerate=False)

    def test_semantics(self):
        checker.semantic_audit()

    def test_exact_group_dimensions(self):
        members, names, clauses, delta = checker.reconstruct()
        self.assertEqual((len(members), len(names), len(clauses), delta), (1024, 26653, 307308, (2013, 7899)))

    def test_strict_ledger(self):
        metadata, row = verifier.load_ledger()
        verifier.verify_bindings(metadata)
        verifier.artifact_path(row)

    def test_rejects_ledger_group_mutation(self):
        data = verifier.LEDGER.read_text(encoding="ascii").replace("B6-l5\t1024", "B6-l5\t1023", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.tsv"
            path.write_text(data, encoding="ascii", newline="\n")
            with self.assertRaises(RuntimeError):
                verifier.load_ledger(path)


if __name__ == "__main__":
    unittest.main()
