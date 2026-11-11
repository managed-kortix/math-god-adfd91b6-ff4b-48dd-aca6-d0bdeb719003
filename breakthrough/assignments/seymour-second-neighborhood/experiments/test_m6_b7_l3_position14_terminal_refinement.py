#!/usr/bin/env python3
"""Regression and hostile tests for the B7-l3 position-14 refinement."""

import tempfile
import unittest
from pathlib import Path

import check_m6_b7_l3_position14_terminal_refinement as checker
import m6_b7_l3_position14_terminal_refinement as producer


class Position14TerminalRefinementTest(unittest.TestCase):
    def test_exact_cover(self):
        self.assertEqual(len(producer.load_leaves()), 60)
        checker.audit(regenerate=False)

    def test_manifest_and_hashes(self):
        leaves = producer.load_leaves()
        manifest = producer.manifest_payload(leaves)
        self.assertEqual(manifest, checker.MANIFEST.read_bytes())
        self.assertEqual(len(checker.load_hashes(manifest)), 60)

    def test_representative_reconstruction(self):
        leaves = producer.load_leaves()
        manifest, _ = checker.load_manifest()
        with tempfile.TemporaryDirectory() as directory:
            for ordinal in (0, 14, 29, 44, 59):
                path = Path(directory) / f"leaf-{ordinal}.cnf"
                producer.write_cnf(path, ordinal, leaves[ordinal], *producer.build(leaves[ordinal]), manifest)
                checker.check(path)

    def test_rejects_clause_mutation(self):
        leaves = producer.load_leaves()
        manifest, _ = checker.load_manifest()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.cnf"
            producer.write_cnf(path, 0, leaves[0], *producer.build(leaves[0]), manifest)
            data = path.read_bytes()
            marker = b"-26411 0\n"
            self.assertIn(marker, data)
            path.write_bytes(data.replace(marker, b"26411 0\n", 1))
            with self.assertRaises(RuntimeError):
                checker.check(path)


if __name__ == "__main__":
    unittest.main()
