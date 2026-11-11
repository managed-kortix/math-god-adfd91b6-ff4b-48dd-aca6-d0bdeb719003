#!/usr/bin/env python3
"""Hostile tests for the strict position-14 certificate and package ledgers."""

import tempfile
import unittest
from pathlib import Path

import verify_m6_b7_l3_position14_terminal_refinement_certificates as verifier


class Position14CertificateLedgerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.metadata, cls.rows = verifier.load_ledger()

    def mutated(self, path, old, new):
        data = path.read_bytes()
        self.assertIn(old, data)
        target = Path(self.directory) / path.name
        target.write_bytes(data.replace(old, new, 1))
        return target

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = self.temp.name

    def tearDown(self):
        self.temp.cleanup()

    def test_rejects_row_hash_mutation(self):
        bad = self.mutated(verifier.LEDGER, b"8539528062dcbf", b"0539528062dcbf")
        with self.assertRaises(RuntimeError):
            verifier.load_ledger(bad)

    def test_rejects_duplicate_leaf(self):
        bad = self.mutated(verifier.LEDGER, b"\n01\tp14-", b"\n00\tp14-")
        with self.assertRaises(RuntimeError):
            verifier.load_ledger(bad)

    def test_rejects_package_gap(self):
        bad = self.mutated(verifier.PACKAGES, b"15-28", b"16-28")
        with self.assertRaises(RuntimeError):
            verifier.load_packages(self.rows, bad)

    def test_rejects_package_limit(self):
        bad = self.mutated(verifier.PACKAGES, b"146504520", b"150000000")
        with self.assertRaises(RuntimeError):
            verifier.load_packages(self.rows, bad)

    def test_rejects_ledger_reciprocal_pin_mutation(self):
        bad = self.mutated(verifier.LEDGER, b"verifier-canonical-sha256\t", b"verifier-canonical-sha257\t")
        with self.assertRaises(RuntimeError):
            verifier.canonical_ledger_hash(bad)


if __name__ == "__main__":
    unittest.main()
