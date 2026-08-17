#!/usr/bin/env python3
"""Compute the exact precedence-aware order-eight lane union."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import lzma
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ENGINE_PATH = HERE / "rank7_order8_exact_rational.py"
SCALAR_PATH = HERE / "rank7_order8_parametric_gram_ansatz.py"
TYPED_PATH = HERE / "rank7_order8_typed_diagonal_gram_lane.py"
CACHE_PATH = HERE / "rank7_order8_rational_search_cache.r7o8c.xz"
OUTPUT_PATH = HERE / "rank7_order8_lane_union.json.xz"
PAYLOAD_FREE_TOTAL = 605
COMMITTED_STOP = 21000


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def scalar_owner(scalar, engine, census, source, candidates, values):
    costs = scalar.numerical_costs(engine, census, source, values)
    for position in np.argsort(costs):
        if costs[position] > 6.0 + 1e-10:
            break
        if scalar.exact_cost(engine, census, source, candidates[int(position)]) <= 6:
            return True
    return False


def intervals(indices):
    if not indices:
        return []
    output = []
    start = previous = indices[0]
    for value in indices[1:]:
        if value != previous + 1:
            output.append([start, previous + 1])
            start = value
        previous = value
    output.append([start, previous + 1])
    return output


def verify_committed(engine, census, residuals):
    paths = sorted(HERE.glob("rank7_order8_chunk_*.r7o8g.xz"))
    covered = []
    cursor = 0
    for path in paths:
        raw = lzma.decompress(path.read_bytes(), format=lzma.FORMAT_XZ)
        start, records = engine.base.exact_decode_pack(census, raw, residuals)
        if start >= COMMITTED_STOP:
            continue
        require(start == cursor and start + len(records) <= COMMITTED_STOP,
                "committed packs leave a gap, overlap, or exceed the requested range")
        require(all(mode == engine.base.MODE_SHARED for mode, _ in records),
                "committed range contains a non-shared record")
        covered.extend(range(start, start + len(records)))
        cursor += len(records)
    require(cursor == COMMITTED_STOP, "committed packs do not cover [0,21000)")
    return frozenset(covered)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    require(args.workers > 0, "workers must be positive")

    engine = load("rank7_order8_union_engine", ENGINE_PATH)
    scalar = load("rank7_order8_union_scalar", SCALAR_PATH)
    typed = load("rank7_order8_union_typed", TYPED_PATH)
    census = engine.load_census_module()
    residuals = engine.residual_rows(census, cache_path=CACHE_PATH)

    candidates = scalar.coefficients(32, 4)
    values = np.asarray([float(value) for value in candidates])
    ratios = typed.rationals(8, 4, include_zero=True)
    scales = (Fraction(1, 2), Fraction(2, 3), Fraction(1), Fraction(3, 2), Fraction(2))
    parameter_grid = tuple((float(scale), float(scale * ratio), scale, scale * ratio)
                           for scale in scales for ratio in ratios)
    typed._WORKER_CONTEXT = engine, census, residuals, ratios, parameter_grid, 3
    if args.workers == 1:
        results = map(typed.worker_search, range(len(residuals)))
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=args.workers)
        results = executor.map(typed.worker_search, range(len(residuals)), chunksize=64)

    scalar_indices = []
    typed_indices = []
    for index, (source, result) in enumerate(zip(residuals, results, strict=True)):
        if scalar_owner(scalar, engine, census, source, candidates, values):
            scalar_indices.append(index)
        cost = result[0]
        if cost is not None and cost <= 6:
            typed_indices.append(index)
        if args.progress and (index + 1) % 25000 == 0:
            print(f"rows={index + 1} scalar={len(scalar_indices)} typed={len(typed_indices)}",
                  flush=True)
    if executor is not None:
        executor.shutdown()

    scalar_set = frozenset(scalar_indices)
    typed_set = frozenset(typed_indices)
    rational_set = verify_committed(engine, census, residuals)
    universe = frozenset(range(len(residuals)))
    structural_union = scalar_set | typed_set
    full_union = structural_union | rational_set
    remaining = sorted(universe - full_union)
    structural_remaining = sorted(universe - structural_union)
    source_remaining = [residuals[index][1] for index in remaining]

    atoms = {
        "scalar_only": len(scalar_set - typed_set - rational_set),
        "typed_only": len(typed_set - scalar_set - rational_set),
        "rational_only": len(rational_set - scalar_set - typed_set),
        "scalar_typed_only": len((scalar_set & typed_set) - rational_set),
        "scalar_rational_only": len((scalar_set & rational_set) - typed_set),
        "typed_rational_only": len((typed_set & rational_set) - scalar_set),
        "scalar_typed_rational": len(scalar_set & typed_set & rational_set),
    }
    report = {
        "schema": "rank-seven-order-eight-lane-union-v1",
        "source_stream_sha256": census.SOURCE_SHA256,
        "precedence": ["payload-free", "scalar-sos", "typed-diagonal", "rational-committed"],
        "universe": {
            "coarse_residual_total": len(residuals) + PAYLOAD_FREE_TOTAL,
            "rational_search_total": len(residuals),
            "payload_free_total": PAYLOAD_FREE_TOTAL,
        },
        "raw_lane_counts": {
            "payload-free": PAYLOAD_FREE_TOTAL,
            "scalar-sos": len(scalar_set),
            "typed-diagonal": len(typed_set),
            "rational-committed": len(rational_set),
        },
        "pairwise_overlap_counts": {
            "payload-free+scalar-sos": 0,
            "payload-free+typed-diagonal": 0,
            "payload-free+rational-committed": 0,
            "scalar-sos+typed-diagonal": len(scalar_set & typed_set),
            "scalar-sos+rational-committed": len(scalar_set & rational_set),
            "typed-diagonal+rational-committed": len(typed_set & rational_set),
        },
        "venn_atoms_within_rational_search": atoms,
        "precedence_exclusive_counts": {
            "payload-free": PAYLOAD_FREE_TOTAL,
            "scalar-sos": len(scalar_set),
            "typed-diagonal": len(typed_set - scalar_set),
            "rational-committed": len(rational_set - structural_union),
        },
        "structural_union_count": PAYLOAD_FREE_TOTAL + len(structural_union),
        "structural_residual_count": len(structural_remaining),
        "full_union_count": PAYLOAD_FREE_TOTAL + len(full_union),
        "remaining_count": len(remaining),
        "structural_residual_stream_indices": structural_remaining,
        "remaining_stream_indices": remaining,
        "remaining_stream_intervals": intervals(remaining),
        "remaining_source_indices": source_remaining,
        "remaining_stream_indices_sha256": hashlib.sha256(canonical_bytes(remaining)).hexdigest(),
        "remaining_source_indices_sha256": hashlib.sha256(canonical_bytes(source_remaining)).hexdigest(),
    }
    raw = canonical_bytes(report)
    stored = lzma.compress(raw, format=lzma.FORMAT_XZ, preset=6)
    args.output.write_bytes(stored)
    print(json.dumps({key: report[key] for key in (
        "raw_lane_counts", "pairwise_overlap_counts", "venn_atoms_within_rational_search",
        "precedence_exclusive_counts", "structural_union_count", "structural_residual_count",
        "full_union_count", "remaining_count")}, sort_keys=True, indent=2))
    print(f"raw_sha256={hashlib.sha256(raw).hexdigest()}")
    print(f"xz_sha256={hashlib.sha256(stored).hexdigest()}")


if __name__ == "__main__":
    main()
