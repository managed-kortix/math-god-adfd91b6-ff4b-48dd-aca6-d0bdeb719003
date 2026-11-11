#!/usr/bin/env python3
"""Hostile canonical ledger, binding, scope, artifact, and cap tests for the 68-proof package."""

import copy
import json
from pathlib import Path
import tempfile

import verify_m6_b7_l6_early_c_certificate_residual_exact_pair_singleton_parent_scout_unsat_certificates as verifier


def reject_ledger(data, label):
    with tempfile.TemporaryDirectory(prefix="exact-pair-singleton-68-hostile-", dir=verifier.ROOT) as directory:
        path = Path(directory) / "ledger.tsv"
        path.write_bytes(data)
        try:
            verifier.load_ledger(path)
            if verifier.canonical_ledger_hash(path) != verifier.LEDGER_CANONICAL_SHA256:
                raise RuntimeError("canonical ledger pin differs")
        except (RuntimeError, UnicodeError):
            return
    raise RuntimeError(f"hostile 68-proof ledger mutation accepted: {label}")


def reject_call(call, label):
    try:
        call()
    except (RuntimeError, UnicodeError):
        return
    raise RuntimeError(f"hostile 68-proof mutation accepted: {label}")


metadata, rows = verifier.load_ledger()
verifier.verify_bindings(metadata)
verifier.artifact_paths(rows)
data = verifier.LEDGER.read_bytes()
reject_ledger(data.replace(b"certified-memberships\t68", b"certified-memberships\t67", 1), "count")
reject_ledger(data.replace(rows[0]["membership"].encode("ascii") + b"\t", b"000\t", 1), "scope-order")
reject_ledger(data.replace(rows[0]["artifact"].encode("ascii"), b"certificates/../hostile.xz", 1),
              "artifact-path")
reject_ledger(data.replace(rows[0]["xz-sha256"].encode("ascii"), b"0" * 64, 1), "artifact-hash")
reject_ledger(data + data.splitlines(keepends=True)[-1], "duplicate-row")
reject_ledger(data.replace(b"total-xz-bytes\t32389520", b"total-xz-bytes\t250000000", 1), "size-cap")

with tempfile.TemporaryDirectory(prefix="exact-pair-singleton-68-pin-", dir=verifier.ROOT) as directory:
    path = Path(directory) / "verifier.py"
    path.write_bytes(Path(verifier.__file__).read_bytes() + b"\n")
    if verifier.canonical_verifier_hash(path) == metadata["verifier-canonical-sha256"]:
        raise RuntimeError("hostile verifier mutation accepted")

changed = dict(metadata)
runtime_key = next(name for name in changed if name.startswith("runtime-m6-parent-cnf-") and
                   name.endswith("sha256"))
changed[runtime_key] = "0" * 64
reject_call(lambda: verifier.verify_bindings(changed), "transitive-runtime")

changed_rows = [dict(row) for row in rows]
changed_rows[0]["artifact"] = changed_rows[1]["artifact"]
reject_call(lambda: verifier.artifact_paths(changed_rows), "artifact-set")

scout = json.loads(verifier.BOUND_PATHS["singleton-scout"].read_text(encoding="ascii"))
changed_scout = copy.deepcopy(scout)
changed_scout["rows"][0]["status"], changed_scout["rows"][1]["status"] = \
    changed_scout["rows"][1]["status"], changed_scout["rows"][0]["status"]
with tempfile.TemporaryDirectory(prefix="exact-pair-singleton-68-scout-", dir=verifier.ROOT) as directory:
    path = Path(directory) / "scout.json"
    path.write_text(json.dumps(changed_scout, sort_keys=True, indent=2) + "\n", encoding="ascii")
    original = verifier.structural.SCOUT
    try:
        verifier.structural.SCOUT = path
        reject_call(verifier.frozen_scope, "equal-total-status-swap")
    finally:
        verifier.structural.SCOUT = original

print("PASS 68-proof canonical pins, transitive runtime, scout order, artifact set, and exclusive cap")
