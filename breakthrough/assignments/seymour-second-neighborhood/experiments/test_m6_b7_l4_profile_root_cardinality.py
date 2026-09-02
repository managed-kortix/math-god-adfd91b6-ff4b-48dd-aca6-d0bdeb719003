#!/usr/bin/env python3
"""Regression and hostile tests for the B7-l4 40-profile campaign."""

import tempfile
import unittest
from pathlib import Path

import check_m6_b7_l4_profile_root_cardinality as checker
import m6_b7_l4_profile_root_cardinality as producer


class B7L5ProfileRootCardinalityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profiles = producer.load_profiles()
        cls.independent = checker.derive()

    def test_exact_census(self):
        self.assertEqual(len(self.profiles), 40)
        self.assertEqual(sum(len(profile[7]) for profile in self.profiles), 14464)
        self.assertEqual([(x[1], x[2], x[3], x[4], x[6], len(x[7])) for x in self.profiles],
                         [(x[1], x[2], x[3], x[4], x[6], len(x[7])) for x in self.independent])

    def test_manifest(self):
        manifest = producer.manifest_payload(self.profiles)
        self.assertEqual(manifest, checker.MANIFEST.read_bytes())
        self.assertIn(b"certificate-status\tnot-started\n", manifest)

    def test_cover_without_regeneration(self):
        checker.check_cover(regenerate=False)

    def test_semantics(self):
        checker.semantic_audit()

    def test_representative_reconstructions(self):
        manifest, _ = checker.load_manifest()
        hashes = checker.load_hashes(manifest)
        with tempfile.TemporaryDirectory() as directory:
            for position in (0, 13, 26, 39):
                path = Path(directory) / f"p{position:02d}.cnf"
                producer.write_cnf(path, position, self.profiles[position],
                                   *producer.build(self.profiles[position]), manifest)
                self.assertEqual(producer.identity(path), hashes[position])
                checker.check(path)

    def test_rejects_counter_mutation(self):
        manifest, _ = checker.load_manifest()
        position = 0
        names, clauses, selectors, delta = checker.reconstruct(self.independent[position])
        clauses[-1] = (-clauses[-1][0],)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.cnf"
            with path.open("w", encoding="ascii", newline="\n") as handle:
                for name, value in checker.metadata(position, self.independent[position], manifest,
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
