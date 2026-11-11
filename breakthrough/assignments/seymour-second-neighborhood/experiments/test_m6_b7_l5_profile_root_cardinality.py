#!/usr/bin/env python3
"""Regression and hostile tests for the B7-l5 53-profile campaign."""

import tempfile
import unittest
from pathlib import Path

import check_m6_b7_l5_profile_root_cardinality as checker
import m6_b7_l5_profile_root_cardinality as producer
import verify_m6_b7_l5_profile_root_cardinality_certificates as verifier


class B7L5ProfileRootCardinalityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profiles = producer.load_profiles()
        cls.independent = checker.derive()

    def test_exact_census(self):
        self.assertEqual(len(self.profiles), 53)
        self.assertEqual(sum(len(profile[7]) for profile in self.profiles), 3387)
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

    def test_strict_certificate_ledger(self):
        metadata, rows = verifier.load_ledger()
        verifier.verify_bindings(metadata)
        verifier.artifact_paths(rows)
        verifier.verify_artifact_identities(rows)

    def test_rejects_ledger_profile_mutation(self):
        data = verifier.LEDGER.read_text(encoding="ascii")
        mutated = data.replace("00\tp00\t", "01\tp00\t", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.tsv"
            path.write_text(mutated, encoding="ascii", newline="\n")
            with self.assertRaises(RuntimeError):
                verifier.load_ledger(path)

    def test_rejects_noncanonical_artifact_path(self):
        data = verifier.LEDGER.read_text(encoding="ascii")
        mutated = data.replace("certificates/m6-b7-l5-profile-root-cardinality-profile-00.lrat.xz",
                               "certificates/../hostile.lrat.xz", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.tsv"
            path.write_text(mutated, encoding="ascii", newline="\n")
            _, rows = verifier.load_ledger(path)
            with self.assertRaises(RuntimeError):
                verifier.artifact_paths(rows)

    def test_representative_reconstructions(self):
        manifest, _ = checker.load_manifest()
        hashes = checker.load_hashes(manifest)
        with tempfile.TemporaryDirectory() as directory:
            for position in (0, 17, 31, 52):
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
