#!/usr/bin/env python3
"""Regression tests for the certificate-relative binary all-different layer."""

import json
from pathlib import Path
import tempfile
import unittest

import check_m6_b7_l6_exact_pair_hall_binary_alldifferent as checker


class BinaryAllDifferentTest(unittest.TestCase):
    def test_cover_and_reconstruction(self):
        checker.check_cover(regenerate=False)

    def test_exhaustive_small_domains(self):
        checker.semantic_audit()

    def test_rejects_forbidden_value_seven_shortcut(self):
        checker.excluded_value_counterexample()

    def test_scout(self):
        checker.check_scout()

    def test_exact_dimensions(self):
        for record in checker.independent_scope():
            names, clauses, _, _, _, _ = checker.reconstruct(record)
            base_variables, base_clauses = checker.hall_check.base.producer.dimensions(record[1])
            self.assertEqual((len(names) - base_variables, len(clauses) - base_clauses), (84, 336))

    def test_rejects_manifest_mutation(self):
        data = checker.MANIFEST.read_bytes().replace(b"value i selected", b"value j selected", 1)
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
        data["rows"][0]["status"] = "UNSAT"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "swapped.json"
            path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="ascii")
            with self.assertRaises(RuntimeError):
                checker.check_scout(path, require_identity=False)

    def test_channel_and_disequality_mutations_change_reconstruction(self):
        names, clauses, _, universe, support, bits = checker.reconstruct(checker.independent_scope()[0])
        channel = (*tuple(bits[universe[0]]), names.index(f"a_{support[0]}_{universe[0]}") + 1)
        self.assertIn(channel, clauses)
        pair = universe[:2]
        diff = names.index(f"hall_match_diff_{pair[0]}_{pair[1]}_0") + 1
        self.assertIn((-diff, bits[pair[0]][0], bits[pair[1]][0]), clauses)


if __name__ == "__main__":
    unittest.main()
