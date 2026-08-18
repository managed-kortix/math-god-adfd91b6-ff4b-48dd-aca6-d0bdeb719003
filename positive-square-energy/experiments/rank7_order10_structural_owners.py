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
TOTAL_KEYS = ("kernel_total", "physical_row_total", "parity_orbit_total",
              "coarse_certified_total", "coarse_residual_total",
              "coarse_residual_physical_total", "frontier_target_total")


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


def validate_census_header(core, header, path):
    label = path.name
    core.require(header.get("schema") == core.CHUNK_SCHEMA,
                 f"wrong census schema: {label}")
    core.require(header.get("full_theorem") is False,
                 f"census theorem flag changed: {label}")
    core.require((header.get("rank"), header.get("order"), header.get("budget")) ==
                 (core.RANK, core.ORDER, [core.RANK - 1, 1]),
                 f"wrong census scope: {label}")
    core.require((header.get("path_count"), header.get("frontiers_per_residual"),
                  header.get("source_sha256")) ==
                 (core.PATH_COUNT, core.TARGETS_PER_RESIDUAL, SOURCE_SHA256),
                 f"wrong census source or frontier scope: {label}")
    start, stop = header["kernel_range"]
    core.require(type(start) is int and type(stop) is int and
                 0 <= start < stop <= core.KERNEL_TOTAL,
                 f"bad census kernel range: {label}")
    kernels = header["kernels"]
    core.require(type(kernels) is list and
                 header["kernel_total"] == stop - start == len(kernels),
                 f"incomplete census kernel ledger: {label}")
    indices = [row["order_kernel"] for row in kernels]
    core.require(indices == list(range(start + 1, stop + 1)),
                 f"census kernel ledger is not contiguous: {label}")
    sums = {
        "physical_row_total": sum(row["physical_rows"] for row in kernels),
        "parity_orbit_total": sum(row["parity_orbits"] for row in kernels),
        "coarse_certified_total": sum(row["coarse_certified_orbits"] for row in kernels),
        "coarse_residual_total": sum(row["coarse_residual_orbits"] for row in kernels),
        "coarse_residual_physical_total": sum(
            row["coarse_residual_physical_rows"] for row in kernels),
    }
    core.require(all(header[key] == value for key, value in sums.items()),
                 f"census totals disagree with kernel ledger: {label}")
    core.require(header["coarse_certified_total"] + header["coarse_residual_total"] ==
                 header["parity_orbit_total"],
                 f"census coarse partition mismatch: {label}")
    core.require(header["frontier_target_total"] ==
                 core.TARGETS_PER_RESIDUAL * header["coarse_residual_total"],
                 f"census frontier total mismatch: {label}")


def scan_census_chunks(core, paths, output):
    engine = core.load_engine()
    chunks = []
    totals = {key: 0 for key in TOTAL_KEYS}
    cursor = 0
    for path in sorted(paths, key=lambda item: item.name):
        path = path.resolve()
        core.require(path.parent == output.parent.resolve(),
                     f"census chunk is not scheduler-local: {path}")
        header, records, finish = engine.stream_chunk(path)
        start, stop = header["kernel_range"]
        core.require(start == cursor, f"chunk gap, overlap, or wrong order: {path.name}")
        kernels = {row["order_kernel"]: row for row in header["kernels"]}
        digest = hashlib.sha256()
        count = 0
        physical_count = 0
        previous = None
        for record in records:
            digest.update(core.canonical_bytes(record))
            ledger = kernels.get(record.get("order_kernel"))
            core.require(ledger is not None and record.get("global_kernel") ==
                         ledger["global_kernel"],
                         f"bad residual kernel reference: {path.name}")
            row = record.get("row")
            edges = ledger["edges"]
            core.require(type(row) is list and len(row) == len(edges) and
                         all(type(value) is int and 0 <= value <= edge[2]
                             for value, edge in zip(row, edges, strict=True)),
                         f"nonphysical residual row: {path.name}")
            orbit_size = record.get("orbit_size")
            core.require(type(orbit_size) is int and orbit_size >= 1 and
                         ledger["automorphisms"] % orbit_size == 0,
                         f"bad residual orbit size: {path.name}")
            code = 0
            stride = 1
            for value, edge in zip(row, edges, strict=True):
                code += value * stride
                stride *= edge[2] + 1
            key = record["order_kernel"], code
            core.require(previous is None or previous < key,
                         f"residual stream is not strictly ordered: {path.name}")
            previous = key
            count += 1
            physical_count += orbit_size
        raw_sha256, artifact_sha256 = finish()
        validate_census_header(core, header, path)
        core.require(count == header["coarse_residual_total"] and
                     physical_count == header["coarse_residual_physical_total"] and
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
    return payload


def build_census_manifest(core, paths, output):
    payload = scan_census_chunks(core, paths, output)
    core.atomic_bytes(output, core.canonical_bytes(payload))
    return payload


def verify_census_manifest(core, manifest_path):
    raw = manifest_path.read_bytes()
    expected = json.loads(raw.decode("ascii"))
    core.require(raw == core.canonical_bytes(expected),
                 "census manifest is not canonical ASCII JSON")
    core.require(expected.get("schema") == core.MANIFEST_SCHEMA and
                 expected.get("full_theorem") is False,
                 "wrong census manifest schema or theorem boundary")
    chunks = expected.get("chunks")
    core.require(type(chunks) is list and chunks, "census manifest has no chunks")
    paths = [manifest_path.parent / row["path"] for row in chunks]
    actual = scan_census_chunks(core, paths, manifest_path)
    core.require(core.canonical_bytes(actual) == raw,
                 "regenerated census manifest differs")
    return actual


def main():
    core = load_core()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    census = subparsers.add_parser("census-manifest")
    census.add_argument("chunks", nargs="+", type=Path)
    census.add_argument("--output", type=Path, default=DEFAULT_MANIFEST)
    verify_census = subparsers.add_parser("verify-census-manifest")
    verify_census.add_argument("manifest", type=Path, nargs="?", default=DEFAULT_MANIFEST)
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
    if args.command == "verify-census-manifest":
        payload = verify_census_manifest(core, args.manifest)
        print(f"census_chunks={len(payload['chunks'])} "
              f"residuals={payload['coarse_residual_total']} status=verified")
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
