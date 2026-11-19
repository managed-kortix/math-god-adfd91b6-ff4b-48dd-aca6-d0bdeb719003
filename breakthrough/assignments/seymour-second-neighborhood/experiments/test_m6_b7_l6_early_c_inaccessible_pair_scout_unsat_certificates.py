#!/usr/bin/env python3
"""Hostile ledger, status, artifact, and verifier tests for the 172-child package."""

import tempfile
from pathlib import Path

import verify_m6_b7_l6_early_c_inaccessible_pair_scout_unsat_certificates as verifier


def reject_ledger(data, label):
    with tempfile.TemporaryDirectory(prefix="inaccessible-pair-172-hostile-", dir=verifier.ROOT) as directory:
        path = Path(directory) / "ledger.tsv"
        path.write_bytes(data)
        try:
            verifier.load_ledger(path)
            if verifier.canonical_ledger_hash(path) != verifier.LEDGER_CANONICAL_SHA256:
                raise RuntimeError("canonical ledger pin differs")
        except (RuntimeError, UnicodeError):
            return
    raise RuntimeError(f"hostile 172-child ledger mutation accepted: {label}")


metadata, rows = verifier.load_ledger()
data = verifier.LEDGER.read_bytes()
reject_ledger(data.replace(b"certified-children\t172", b"certified-children\t171", 1), "count")
reject_ledger(data.replace(metadata["status-sequence"].encode("ascii"),
                           ("T" + metadata["status-sequence"][1:]).encode("ascii"), 1), "status-sequence")
reject_ledger(data.replace(rows[0]["artifact"].encode("ascii"), b"certificates/../hostile.xz", 1),
              "artifact-path")
reject_ledger(data.replace(rows[0]["xz-sha256"].encode("ascii"), b"0" * 64, 1), "artifact-hash")
reject_ledger(data.replace((rows[0]["child"] + "\t").encode("ascii"), b"001\t", 1), "scope-order")
reject_ledger(data + data.splitlines(keepends=True)[-1], "duplicate-row")
reject_ledger(data.replace(b"total-xz-bytes\t81964720", b"total-xz-bytes\t250000000", 1), "size-cap")

with tempfile.TemporaryDirectory(prefix="inaccessible-pair-172-verifier-", dir=verifier.ROOT) as directory:
    path = Path(directory) / "verifier.py"
    path.write_bytes(Path(verifier.__file__).read_bytes() + b"\n")
    if verifier.canonical_verifier_hash(path) == metadata["verifier-canonical-sha256"]:
        raise RuntimeError("hostile verifier mutation accepted")

print("PASS 172-child hostile ledger/status/artifact/verifier mutations")
