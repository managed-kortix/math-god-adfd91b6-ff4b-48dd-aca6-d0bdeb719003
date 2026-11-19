#!/usr/bin/env python3
"""Hostile parser and transitive-binding tests for the leaf 129 certificate."""

import tempfile
from pathlib import Path

import verify_m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual_leaf_129_certificate as verifier


def reject(call, label):
    try:
        call()
    except (RuntimeError, ValueError, UnicodeError):
        return
    raise RuntimeError(f"hostile leaf 129 certificate mutation accepted: {label}")


metadata, row = verifier.load_ledger()
verifier.verify_bindings(metadata)
if verifier.runtime_source_closure() != verifier.RUNTIME_SOURCE_NAMES:
    raise RuntimeError("leaf 129 runtime closure is not exact")

with tempfile.TemporaryDirectory(prefix="m6-grouped-leaf-129-hostile-", dir=verifier.ROOT) as directory:
    work = Path(directory)
    original = verifier.LEDGER.read_text(encoding="ascii")

    def mutate(label, old, new):
        if original.count(old) != 1:
            raise RuntimeError(f"hostile fixture is not unique: {label}")
        path = work / f"bad-{label}.tsv"
        path.write_text(original.replace(old, new), encoding="ascii", newline="\n")
        reject(lambda: verifier.load_ledger(path), label)

    mutate("metadata-order", "generated-utc\t2026-08-12\nscope\tfrozen-grouped-residual-leaf-129-only",
           "scope\tfrozen-grouped-residual-leaf-129-only\ngenerated-utc\t2026-08-12")
    mutate("metadata-hash", "grouped-manifest-sha256\t188e", "grouped-manifest-sha256\t188G")
    mutate("metadata-bytes", "grouped-manifest-bytes\t12775", "grouped-manifest-bytes\t012775")
    mutate("row-cnf-hash", row["cnf-sha256"], "0" * 64)
    mutate("row-field", "\t23618\t143056\t", "\t23619\t143056\t")
    mutate("artifact", row["artifact"], "certificates/../hostile.lrat.xz")
    row_line = original.rstrip("\n").split("\n")[-1]
    mutate("extra-row", row_line + "\n", row_line + "\n" + row_line + "\n")

    source_key = "runtime-snc-cnf"
    original_path = verifier.BOUND_PATHS[source_key]
    bad_source = work / "snc_cnf.py"
    bad_source.write_bytes(original_path.read_bytes() + b"\n")
    verifier.BOUND_PATHS[source_key] = bad_source
    try:
        reject(lambda: verifier.verify_bindings(metadata), "transitive-runtime-source")
    finally:
        verifier.BOUND_PATHS[source_key] = original_path

print("PASS leaf 129 certificate hostile canonical-row and transitive-runtime mutations")
