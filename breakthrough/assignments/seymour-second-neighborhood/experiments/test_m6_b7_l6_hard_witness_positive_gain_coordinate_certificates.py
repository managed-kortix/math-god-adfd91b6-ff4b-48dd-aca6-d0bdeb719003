#!/usr/bin/env python3
"""Strict coordinate certificate ledger and hostile mutation tests."""

import tempfile
from pathlib import Path

import verify_m6_b7_l6_hard_witness_positive_gain_coordinate_certificates as verifier


def reject(data, label):
    with tempfile.TemporaryDirectory(prefix="m6-coordinate-certificate-test-", dir=verifier.ROOT) as directory:
        path = Path(directory) / "ledger.tsv"
        path.write_bytes(data)
        try:
            verifier.load_ledger(path)
        except (RuntimeError, UnicodeError):
            return
    raise RuntimeError(f"hostile coordinate certificate ledger mutation accepted: {label}")


metadata, rows = verifier.load_ledger()
verifier.verify_bindings(metadata)
if tuple(int(row["leaf-ordinal"]) for row in rows) != verifier.ORDINALS:
    raise RuntimeError("certificate scope differs")
data = verifier.LEDGER.read_bytes()
reject(data.replace(b"020\to03-w01-c17", b"021\to03-w01-c17", 1), "ordinal")
reject(data.replace(b"source-leaf-ordinals\t010,013", b"source-leaf-ordinals\t011,013", 1), "ancestor")
reject(data.replace(b"total-xz-bytes\t3756712", b"total-xz-bytes\t3756713", 1), "bound-total")
reject(data.replace(rows[0]["xz-sha256"].encode("ascii"),
                    rows[0]["xz-sha256"].upper().encode("ascii"), 1), "artifact-hash-format")
reject(data + data.splitlines(keepends=True)[-1], "duplicate-row")
print("PASS strict coordinate certificate bindings and hostile ledger mutations")
