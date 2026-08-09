#!/usr/bin/env python3
"""Strict positive-gain certificate ledger and hostile mutation tests."""

import tempfile
from pathlib import Path

import verify_m6_b7_l6_hard_witness_positive_gain_certificates as verifier


def reject(data, label):
    with tempfile.TemporaryDirectory(prefix="m6-positive-gain-certificate-test-", dir=verifier.ROOT) as directory:
        path = Path(directory) / "ledger.tsv"
        path.write_bytes(data)
        try:
            verifier.load_ledger(path)
        except (RuntimeError, UnicodeError):
            return
    raise RuntimeError(f"hostile certificate ledger mutation accepted: {label}")


metadata, rows = verifier.load_ledger()
verifier.verify_bindings(metadata)
if tuple(int(row["leaf-ordinal"]) for row in rows) != verifier.ORDINALS:
    raise RuntimeError("certificate scope differs")
data = verifier.LEDGER.read_bytes()
reject(data.replace(b"042\to15-w01", b"043\to15-w01", 1), "ordinal")
reject(data.replace(b"leaf-ordinals\t042,095,097", b"leaf-ordinals\t042,095,096", 1), "scope")
reject(data.replace(b"total-xz-bytes\t35233748", b"total-xz-bytes\t35233749", 1), "bound-total")
reject(data.replace(rows[0]["xz-sha256"].encode("ascii"),
                    rows[0]["xz-sha256"].upper().encode("ascii"), 1), "artifact-hash-format")
reject(data + data.splitlines(keepends=True)[-1], "duplicate-row")
print("PASS strict positive-gain certificate bindings and hostile ledger mutations")
