#!/usr/bin/env python3
"""Hostile ledger and verifier tests for the remaining five certificates."""

import tempfile
from pathlib import Path

import verify_m6_b7_l6_early_c_profile_remaining_scout_unsat_certificates as verifier


def reject_ledger(data, label):
    with tempfile.TemporaryDirectory(prefix="early-profile-5-hostile-", dir=verifier.ROOT) as directory:
        path = Path(directory) / "ledger.tsv"
        path.write_bytes(data)
        try:
            verifier.load_ledger(path)
            if verifier.canonical_ledger_hash(path) != verifier.LEDGER_CANONICAL_SHA256:
                raise RuntimeError("canonical ledger pin differs")
        except (RuntimeError, UnicodeError):
            return
    raise RuntimeError(f"hostile five-cell ledger mutation accepted: {label}")


metadata, rows = verifier.load_ledger()
data = verifier.LEDGER.read_bytes()
reject_ledger(data.replace(b"certified-orbits\t5", b"certified-orbits\t4", 1), "count")
reject_ledger(data.replace(b"combined-xz-bytes\t90192848", b"combined-xz-bytes\t90192849", 1),
              "combined-total")
reject_ledger(data.replace(rows[0]["artifact"].encode("ascii"), b"certificates/../hostile.xz", 1),
              "artifact-path")
reject_ledger(data.replace(rows[0]["xz-sha256"].encode("ascii"), b"0" * 64, 1), "artifact-hash")
reject_ledger(data + data.splitlines(keepends=True)[-1], "duplicate-row")

with tempfile.TemporaryDirectory(prefix="early-profile-5-verifier-", dir=verifier.ROOT) as directory:
    path = Path(directory) / "verifier.py"
    path.write_bytes(Path(verifier.__file__).read_bytes() + b"\n")
    if verifier.canonical_verifier_hash(path) == metadata["verifier-canonical-sha256"]:
        raise RuntimeError("hostile five-cell verifier mutation accepted")

print("PASS five-cell hostile ledger/verifier mutations")
