#!/usr/bin/env python3
"""Recover and exactly verify one completed order-eight R8G2 Gram owner."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import lzma
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PIPELINE = HERE / "rank6_order8_sparse_pipeline.py"
MANIFEST = HERE / "rank6_order8_search_manifest.json"
CHUNK = HERE / "rank6_order8_search_ckpt/chunk-00000-20000.r8g.xz"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def fraction_pair(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def load_pipeline():
    spec = importlib.util.spec_from_file_location("rank6_order8_sparse_pipeline_recovery", PIPELINE)
    require(spec is not None and spec.loader is not None, "cannot load order-eight pipeline")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    pipeline = load_pipeline()
    manifest = json.loads(MANIFEST.read_bytes().decode("ascii"))
    chunk_record = manifest["chunks"][0]
    require(chunk_record["path"].endswith(CHUNK.name), "manifest first chunk changed")
    compressed = CHUNK.read_bytes()
    require(len(compressed) == chunk_record["compressed_bytes"] and
            hashlib.sha256(compressed).hexdigest() == chunk_record["compressed_sha256"],
            "first compressed chunk changed")
    raw = lzma.decompress(compressed)
    require(len(raw) == chunk_record["raw_bytes"] and
            hashlib.sha256(raw).hexdigest() == chunk_record["raw_sha256"],
            "first raw chunk changed")

    residual_rows = []
    for kernel in pipeline.source_kernels():
        _, local = pipeline.kernel_census(kernel, True)
        residual_rows.extend(local)
        if len(residual_rows) >= chunk_record["residual_range"][1]:
            break
    require(len(residual_rows) >= chunk_record["residual_range"][1],
            "did not regenerate enough residual rows")
    start, attempts, records = pipeline.decode_search(raw, residual_rows)
    require([start, start + attempts] == chunk_record["residual_range"],
            "decoded range disagrees with manifest")
    engine = pipeline.load_engine()

    for offset, (mode, witness) in enumerate(records):
        if mode != pipeline.MODE_SHARED:
            continue
        source_index = start + offset
        costs = pipeline.verify_witness(engine, residual_rows[source_index], witness)
        branch_vectors = tuple(engine.rational_unit(parameters) for parameters in witness[1])
        branch_gram = tuple(tuple(sum((x * y for x, y in zip(left, right)), Fraction())
                                  for right in branch_vectors)
                            for left in branch_vectors)
        result = {
            "schema": "rank-six-order-eight-marked-owner-recovery-example-v1",
            "source_index": source_index,
            "source": residual_rows[source_index],
            "record_mode": "shared",
            "canonical_excess": fraction_pair(costs[0]),
            "branch_gram": [[fraction_pair(value) for value in row] for row in branch_gram],
        }
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return
    raise RuntimeError("first chunk has no shared record")


if __name__ == "__main__":
    main()
