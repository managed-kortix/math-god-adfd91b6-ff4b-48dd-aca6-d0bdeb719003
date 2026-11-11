#!/usr/bin/env python3
"""Hostile ledger and verifier tests for the 26-cell certificate package."""

import tempfile
from pathlib import Path

import verify_m6_b7_l6_early_c_profile_scout_unsat_certificates as verifier


def reject_ledger(data, label):
    with tempfile.TemporaryDirectory(prefix="early-profile-26-hostile-", dir=verifier.ROOT) as directory:
        path = Path(directory) / "ledger.tsv"
        path.write_bytes(data)
        try:
            verifier.load_ledger(path)
            if verifier.canonical_ledger_hash(path) != verifier.LEDGER_CANONICAL_SHA256:
                raise RuntimeError("canonical ledger pin differs")
        except (RuntimeError, UnicodeError):
            return
    raise RuntimeError(f"hostile 26-cell ledger mutation accepted: {label}")


metadata, rows = verifier.load_ledger()
data = verifier.LEDGER.read_bytes()
reject_ledger(data.replace(b"certified-orbits\t26", b"certified-orbits\t25", 1), "count")
reject_ledger(data.replace(rows[0]["artifact"].encode("ascii"), b"certificates/../hostile.xz", 1),
              "artifact-path")
reject_ledger(data.replace(rows[0]["xz-sha256"].encode("ascii"), b"0" * 64, 1), "artifact-hash")
reject_ledger(data + data.splitlines(keepends=True)[-1], "duplicate-row")

with tempfile.TemporaryDirectory(prefix="early-profile-26-verifier-", dir=verifier.ROOT) as directory:
    path = Path(directory) / "verifier.py"
    path.write_bytes(Path(verifier.__file__).read_bytes() + b"\n")
    if verifier.canonical_verifier_hash(path) == metadata["verifier-canonical-sha256"]:
        raise RuntimeError("hostile 26-cell verifier mutation accepted")

print("PASS 26-cell hostile ledger/verifier mutations")
