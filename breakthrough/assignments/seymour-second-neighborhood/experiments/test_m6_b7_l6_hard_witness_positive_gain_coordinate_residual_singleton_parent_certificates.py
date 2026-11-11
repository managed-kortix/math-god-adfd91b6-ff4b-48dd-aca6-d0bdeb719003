#!/usr/bin/env python3
"""Strict singleton certificate ledger and hostile mutation tests."""

import copy
import json
import tempfile
from pathlib import Path

import verify_m6_b7_l6_hard_witness_positive_gain_coordinate_residual_singleton_parent_certificates as verifier


def reject(data, label):
    with tempfile.TemporaryDirectory(prefix="m6-singleton-certificate-test-", dir=verifier.ROOT) as directory:
        path = Path(directory) / "ledger.tsv"
        path.write_bytes(data)
        try:
            verifier.load_ledger(path)
        except (RuntimeError, UnicodeError):
            return
    raise RuntimeError(f"hostile singleton certificate ledger mutation accepted: {label}")


def reject_call(call, label):
    try:
        call()
    except (RuntimeError, UnicodeError):
        return
    raise RuntimeError(f"hostile singleton certificate mutation accepted: {label}")


metadata, rows = verifier.load_ledger()
verifier.verify_bindings(metadata)
data = verifier.LEDGER.read_bytes()
if verifier.runtime_source_closure() != verifier.RUNTIME_SOURCE_NAMES:
    raise RuntimeError("runtime dependency closure is not canonical")
reject(data.replace(b"memberships\t127", b"memberships\t126", 1), "scope")
reject(data.replace(b"total-xz-bytes\t61646844", b"total-xz-bytes\t61646845", 1), "bound-total")
reject(data.replace(rows[0]["xz-sha256"].encode("ascii"),
                    rows[0]["xz-sha256"].upper().encode("ascii"), 1), "artifact-hash-format")
reject(data + data.splitlines(keepends=True)[-1], "duplicate-row")

with tempfile.TemporaryDirectory(prefix="m6-singleton-pin-test-", dir=verifier.ROOT) as directory:
    ledger = Path(directory) / "ledger.tsv"
    ledger.write_bytes(data.replace(b"memberships\t127", b"memberships\t126", 1))
    if verifier.canonical_ledger_hash(ledger) == verifier.LEDGER_CANONICAL_SHA256:
        raise RuntimeError("hostile canonical ledger pin mutation accepted")
    source = Path(directory) / "verifier.py"
    source.write_bytes(Path(verifier.__file__).read_bytes() + b"\n")
    if verifier.canonical_verifier_hash(source) == metadata["verifier-canonical-sha256"]:
        raise RuntimeError("hostile canonical verifier pin mutation accepted")

changed_metadata = dict(metadata)
dependency_key = "runtime-m6-parent-cnf-sha256"
changed_metadata[dependency_key] = "0" * 64
reject_call(lambda: verifier.verify_bindings(changed_metadata), "runtime-dependency-identity")

changed_rows = [dict(row) for row in rows]
changed_rows[0]["artifact"] = changed_rows[1]["artifact"]
reject_call(lambda: verifier.artifact_paths(changed_rows), "artifact-path-and-set")

scout = json.loads(verifier.BOUND_PATHS["singleton-scout"].read_text(encoding="ascii"))
changed_scout = copy.deepcopy(scout)
changed_scout["rows"][int(rows[0]["membership-ordinal"])]["key"] += "-hostile"
reject_call(lambda: verifier.validate_scout_scope(changed_scout, rows), "row-identity")
changed_scout = copy.deepcopy(scout)
changed_scout["rows"][0]["status"], changed_scout["rows"][1]["status"] = \
    changed_scout["rows"][1]["status"], changed_scout["rows"][0]["status"]
reject_call(lambda: verifier.validate_scout_scope(changed_scout, rows), "scout-status-order")
changed_rows = [dict(row) for row in rows]
changed_rows[0]["xz-bytes"] = str(int(changed_rows[0]["xz-bytes"]) + 1)
reject_call(lambda: verifier.validate_compression(changed_rows), "compression-total")
reject_call(lambda: verifier.validate_compression(rows, verifier.TOTALS["xz-bytes"]),
            "compression-exclusive-limit")
print("PASS canonical pins, runtime dependency identity, artifact path/set, row identity, "
      "scout status/order, compression limit")
