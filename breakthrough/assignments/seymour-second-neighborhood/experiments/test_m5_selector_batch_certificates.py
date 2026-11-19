#!/usr/bin/env python3
"""Hostile ledger/artifact tests for the retained m=5 selector pilot."""

import tempfile
from pathlib import Path

import verify_m5_selector_batch_certificates as verifier


def reject(call, label):
    try:
        call()
    except (RuntimeError, UnicodeError, ValueError):
        return
    raise AssertionError(f"hostile mutation accepted: {label}")


metadata, rows = verifier.load_ledger()
assert metadata["scope"] == "retained pilot only; no complete m=5 branch closure"
assert metadata["covered-B6-parents"] == "100"
assert metadata["covered-B7-parents"] == "0"
assert len(rows) == 1
artifact = verifier.ROOT / rows[0]["artifact"]
assert verifier.identity(artifact) == (
    int(rows[0]["xz-bytes"]), rows[0]["xz-sha256"]
)

with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    original = verifier.LEDGER.read_text(encoding="ascii")
    mutations = (
        original.replace("covered-B6-parents\t100", "covered-B6-parents\t4355", 1),
        original.replace("covered-B7-parents\t0", "covered-B7-parents\t3083", 1),
        original.replace(rows[0]["cnf-sha256"], "0" * 64, 1),
        original.replace(rows[0]["xz-sha256"], "0" * 64, 1),
        original.replace(rows[0]["artifact"], "certificates/../hostile.lrat.xz", 1),
        original + original.splitlines()[-1] + "\n",
    )
    for ordinal, text in enumerate(mutations):
        path = root / f"bad-{ordinal}.tsv"
        path.write_text(text, encoding="ascii", newline="\n")
        reject(lambda path=path: verifier.load_ledger(path), f"ledger-{ordinal}")

print("PASS retained_pilot=1 covered_B6=100 covered_B7=0 hostile_mutations=6")
