#!/usr/bin/env python3
"""Regression tests for the exact-pair TIMEOUT complete-cut census."""

import tempfile
import unittest
from pathlib import Path

import check_m6_b7_l6_exact_pair_timeout_complete_cut as checker
import m6_b7_l6_exact_pair_timeout_complete_cut as producer


class CompleteCutTest(unittest.TestCase):
    def test_frozen_census(self):
        checker.check()

    def test_frozen_scout(self):
        checker.check_scout()

    def test_rejects_class_mutation(self):
        data = checker.CENSUS.read_bytes().replace(b"epsilon0-b0-chi4", b"epsilon1-b0-chi4", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.tsv"
            path.write_bytes(data)
            with self.assertRaises(RuntimeError):
                checker.check(path)

    def test_all_forced_arcs_are_present(self):
        for row in producer.records():
            self.assertEqual(len(row["forced"]), 16 - sum(row["loads"]))


if __name__ == "__main__":
    unittest.main()
