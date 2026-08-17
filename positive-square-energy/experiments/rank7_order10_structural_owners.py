#!/usr/bin/env python3
"""Chunkable order-ten scan using the structural owner's exact precedence."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
CORE_PATH = HERE / "rank7_order9_structural_owners.py"
DEFAULT_MANIFEST = HERE / "rank7_order10_exact_residual_census_manifest.json"
SOURCE_SHA256 = "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5"


def load_core():
    spec = importlib.util.spec_from_file_location("rank7_order10_owner_scan_core", CORE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load chunked structural owner core")
    core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(core)
    core.DEFAULT_MANIFEST = DEFAULT_MANIFEST
    core.ORDER = 10
    core.RANK = 7
    core.PATH_COUNT = 16
    core.TARGETS_PER_RESIDUAL = 17
    core.KERNEL_TOTAL = 3396
    core.SOURCE_SHA256 = SOURCE_SHA256
    core.SCHEMA = "rank-seven-order-ten-structural-owner-coverage-v1"
    core.CHUNK_RESULT_SCHEMA = "rank-seven-order-ten-structural-owner-chunk-v1"
    core.LANES = ("balanced-rank-one", "signed-imbalance-psd", "simplex-mixed-atom",
                  "cubic-cycle-space-candidate")

    def recognize_row(engine, atom, edges, row):
        # This call preserves the owner's declared first-match precedence exactly.
        return engine.recognize_row(atom, edges, row)

    core.recognize_row = recognize_row
    return core


def build_census_manifest(core, paths, output):
    engine = core.load_engine()
    chunks = []
    totals = {
        key: 0 for key in ("kernel_total", "physical_row_total", "parity_orbit_total",
                           "coarse_certified_total", "coarse_residual_total",
                           "coarse_residual_physical_total", "frontier_target_total")
    }
    cursor = 0
    for path in sorted(paths, key=lambda item: item.name):
        header, records, finish = engine.stream_chunk(path)
        start, stop = header["kernel_range"]
        core.require(start == cursor, f"chunk gap, overlap, or wrong order: {path.name}")
        digest = hashlib.sha256()
        count = 0
        for record in records:
            digest.update(core.canonical_bytes(record))
            count += 1
        raw_sha256, artifact_sha256 = finish()
        core.require((header.get("schema"), header.get("rank"), header.get("order"),
                      header.get("path_count"), header.get("frontiers_per_residual"),
                      header.get("source_sha256")) ==
                     (core.CHUNK_SCHEMA, core.RANK, core.ORDER, core.PATH_COUNT,
                      core.TARGETS_PER_RESIDUAL, SOURCE_SHA256),
                     f"wrong census scope: {path.name}")
        core.require(count == header["coarse_residual_total"] and
                     digest.hexdigest() == header["residual_stream_sha256"],
                     f"incomplete census stream: {path.name}")
        for key in totals:
            totals[key] += header[key]
        chunks.append({
            "artifact_sha256": artifact_sha256,
            "coarse_residual_total": count,
            "kernel_range": [start, stop],
            "path": os.path.relpath(path, output.parent),
            "raw_sha256": raw_sha256,
        })
        cursor = stop
    core.require(cursor == core.KERNEL_TOTAL, "chunks do not cover order ten")
    payload = {
        "schema": core.MANIFEST_SCHEMA,
        "status": "complete-exact-residual-orbit-decomposition",
        "full_theorem": False,
        "rank": core.RANK,
        "order": core.ORDER,
        "budget": [core.RANK - 1, 1],
        "path_count": core.PATH_COUNT,
        "frontiers_per_residual": core.TARGETS_PER_RESIDUAL,
        "source_sha256": SOURCE_SHA256,
        **totals,
        "chunks": chunks,
    }
    output.write_bytes(core.canonical_bytes(payload))
    return payload


def main():
    core = load_core()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    census = subparsers.add_parser("census-manifest")
    census.add_argument("chunks", nargs="+", type=Path)
    census.add_argument("--output", type=Path, default=DEFAULT_MANIFEST)
    chunk = subparsers.add_parser("chunk")
    chunk.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    chunk.add_argument("--chunk-index", required=True, type=int)
    chunk.add_argument("--output", required=True, type=Path)
    chunk.add_argument("--progress", action="store_true")
    aggregate = subparsers.add_parser("aggregate")
    aggregate.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    aggregate.add_argument("--output", required=True, type=Path)
    aggregate.add_argument("chunks", nargs="+", type=Path)
    args = parser.parse_args()
    if args.command == "census-manifest":
        core.require(args.output.parent.is_dir(), "output parent does not exist")
        payload = build_census_manifest(core, args.chunks, args.output)
        print(f"census_chunks={len(payload['chunks'])} "
              f"residuals={payload['coarse_residual_total']}")
        return 0
    core.require(args.output.parent.is_dir(), "output parent does not exist")
    if args.command == "chunk":
        report = core.scan_census_chunk(args.manifest, args.chunk_index, args.output,
                                        args.progress)
        print(f"chunk={args.chunk_index} scanned={report['scanned_residual_total']} "
              f"remainder={report['remainder_orbit_total']}")
        return 0
    report = core.aggregate_chunks(args.manifest, args.chunks, args.output)
    print(f"aggregated={len(args.chunks)} scanned={report['scanned_residual_total']} "
          f"remainder={report['remainder_orbit_total']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        sys.stderr.write(f"order-ten structural owner scan: FAIL CLOSED: {error}\n")
        raise SystemExit(1)
