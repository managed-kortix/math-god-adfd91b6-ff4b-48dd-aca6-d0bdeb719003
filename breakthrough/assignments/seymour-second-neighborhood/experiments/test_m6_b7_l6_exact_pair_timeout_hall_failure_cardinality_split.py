#!/usr/bin/env python3
"""Regression and hostile tests for the exact Hall |K| split and proofs."""

import tempfile
from pathlib import Path
import shutil
import unittest

import check_m6_b7_l6_exact_pair_timeout_hall_failure_cardinality_split as checker
import verify_m6_b7_l6_exact_pair_timeout_hall_failure_cardinality_split_certificates as verifier
import verify_m6_b7_l6_exact_pair_timeout_hall_failure_all33 as combined


class CardinalitySplitTest(unittest.TestCase):
    def test_cover_and_partition(self):
        checker.check_cover()

    def test_certificate_ledger_and_artifacts(self):
        metadata, rows = verifier.load_ledger()
        verifier.verify_bindings(metadata, Path("/tmp/opencode/seymour-lrat-pilots/drat-trim/lrat-check"))
        verifier.artifact_paths(rows)
        verifier.verify_artifact_identities(rows)

    def test_combined_all33_scope(self):
        all33, direct, split = combined.scope_audit()
        self.assertEqual((len(all33), len(direct), len(split)), (33, 29, 4))

    def test_rejects_cardinality_order_mutation(self):
        data = verifier.LEDGER.read_bytes().replace(b"000\t012\t028\tc007-o25-i17-p01\t1\t",
                                                   b"000\t012\t028\tc007-o25-i17-p01\t2\t", 1)
        with tempfile.TemporaryDirectory(prefix="hall-cardinality-hostile-", dir=verifier.ROOT) as directory:
            path = Path(directory) / "ledger.tsv"
            path.write_bytes(data)
            with self.assertRaises(RuntimeError):
                verifier.load_ledger(path)

    def test_rejects_cap_mutation(self):
        data = verifier.LEDGER.read_bytes().replace(b"total-xz-bytes\t17456956",
                                                   b"total-xz-bytes\t250000000", 1)
        with tempfile.TemporaryDirectory(prefix="hall-cardinality-hostile-", dir=verifier.ROOT) as directory:
            path = Path(directory) / "ledger.tsv"
            path.write_bytes(data)
            with self.assertRaises(RuntimeError):
                verifier.load_ledger(path)

    def test_rejects_row_ancestry_mutations(self):
        data = verifier.LEDGER.read_bytes()
        mutations = (
            data.replace(b"000\t012\t028\t", b"000\t013\t028\t", 1),
            data.replace(b"c007-o25-i17-p01", b"c007-o25-i17-p02", 1),
            data.replace(b"\t23768\t144796\t", b"\t23769\t144796\t", 1),
            data.replace(b"membership-028-k1.lrat.xz", b"membership-028-k2.lrat.xz", 1),
        )
        with tempfile.TemporaryDirectory(prefix="hall-cardinality-ancestry-",
                                         dir=verifier.ROOT) as directory:
            path = Path(directory) / "ledger.tsv"
            for mutation in mutations:
                path.write_bytes(mutation)
                with self.assertRaises(RuntimeError):
                    verifier.load_ledger(path)

    def test_rejects_source_and_pin_mutations(self):
        metadata, _ = verifier.load_ledger()
        changed = dict(metadata)
        changed["hall-producer-sha256"] = "0" * 64
        with self.assertRaises(RuntimeError):
            verifier.verify_bindings(changed,
                                     Path("/tmp/opencode/seymour-lrat-pilots/drat-trim/lrat-check"))
        with tempfile.TemporaryDirectory(prefix="hall-cardinality-pin-",
                                         dir=verifier.ROOT) as directory:
            path = Path(directory) / "verifier.py"
            path.write_bytes(Path(verifier.__file__).read_bytes() + b"\n")
            self.assertNotEqual(verifier.canonical_verifier_hash(path),
                                metadata["verifier-canonical-sha256"])

    def test_rejects_artifact_mutation(self):
        _, rows = verifier.load_ledger()
        row = rows[0]
        with tempfile.TemporaryDirectory(prefix="hall-cardinality-artifact-",
                                         dir=verifier.ROOT) as directory:
            root = Path(directory)
            target = root / row["artifact"]
            target.parent.mkdir()
            shutil.copyfile(verifier.ROOT / row["artifact"], target)
            with target.open("r+b") as handle:
                byte = handle.read(1)
                handle.seek(0)
                handle.write(bytes([byte[0] ^ 1]))
            with self.assertRaises(RuntimeError):
                verifier.verify_artifact_identities([row], root)


if __name__ == "__main__":
    unittest.main()
