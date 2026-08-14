#!/usr/bin/env python3
"""Memory-bounded order-eleven aggregation and payload-free owner audit."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
OWNER_ENGINE = HERE / "rank7_order12_structural_owners.py"
ATOM_RECOGNIZER = HERE / "rank7_order7_symbolic_atom_recognizer.py"
ORDER = 11
RANK = 7
PATH_COUNT = 17
TARGETS_PER_RESIDUAL = 18
KERNEL_TOTAL = 1391
SOURCE_SHA256 = "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5"
CHUNK_SCHEMA = "rank-seven-orders9-12-exact-residual-census-chunk-v1"
SCHEMA = "rank-seven-order-eleven-structural-owner-manifest-v1"
LANES = ("balanced-rank-one", "signed-imbalance-psd", "simplex-mixed-atom",
         "cubic-cycle-space-candidate")
TOTAL_KEYS = ("kernel_total", "physical_row_total", "parity_orbit_total",
              "coarse_certified_total", "coarse_residual_total",
              "coarse_residual_physical_total", "frontier_target_total")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def load_owner_engine():
    spec = importlib.util.spec_from_file_location("rank7_order11_owner_core", OWNER_ENGINE)
    require(spec is not None and spec.loader is not None, "cannot load owner engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ORDER = ORDER
    module.RANK = RANK
    module.PATH_COUNT = PATH_COUNT
    module.TARGETS_PER_ROW = TARGETS_PER_RESIDUAL
    module.SCHEMA = SCHEMA
    module.LANES = LANES
    return module


def validate_header(header, path):
    label = path.name
    require(header.get("schema") == CHUNK_SCHEMA, f"wrong schema: {label}")
    require(header.get("full_theorem") is False, f"theorem flag changed: {label}")
    require((header.get("rank"), header.get("order"), header.get("budget")) ==
            (RANK, ORDER, [RANK - 1, 1]), f"wrong scope: {label}")
    require((header.get("path_count"), header.get("frontiers_per_residual")) ==
            (PATH_COUNT, TARGETS_PER_RESIDUAL), f"wrong frontier scope: {label}")
    require(header.get("source_sha256") == SOURCE_SHA256, f"source pin changed: {label}")
    start, stop = header["kernel_range"]
    require(0 <= start < stop <= KERNEL_TOTAL, f"bad kernel range: {label}")
    kernels = header["kernels"]
    require(header["kernel_total"] == stop - start == len(kernels),
            f"incomplete kernel ledger: {label}")
    order_kernel_indices = [row["order_kernel"] for row in kernels]
    require(len(set(order_kernel_indices)) == len(order_kernel_indices) and
            order_kernel_indices == sorted(order_kernel_indices),
            f"kernel ledger is not strictly ordered: {label}")
    sums = {
        "physical_row_total": sum(row["physical_rows"] for row in kernels),
        "parity_orbit_total": sum(row["parity_orbits"] for row in kernels),
        "coarse_certified_total": sum(row["coarse_certified_orbits"] for row in kernels),
        "coarse_residual_total": sum(row["coarse_residual_orbits"] for row in kernels),
        "coarse_residual_physical_total": sum(
            row["coarse_residual_physical_rows"] for row in kernels),
    }
    require(all(header[key] == value for key, value in sums.items()),
            f"chunk totals disagree with kernel ledger: {label}")
    require(header["coarse_certified_total"] + header["coarse_residual_total"] ==
            header["parity_orbit_total"], f"coarse partition mismatch: {label}")
    require(header["frontier_target_total"] ==
            TARGETS_PER_RESIDUAL * header["coarse_residual_total"],
            f"frontier total mismatch: {label}")


def scan(paths, output):
    owner = load_owner_engine()
    atom = owner.load_atom_recognizer()
    totals = Counter({key: 0 for key in TOTAL_KEYS})
    owner_orbits = Counter({lane: 0 for lane in LANES})
    owner_physical = Counter({lane: 0 for lane in LANES})
    chunks = []
    classification_digest = hashlib.sha256()
    cursor = 0
    source_index = 0

    for path in paths:
        header, records, finish = owner.stream_chunk(path)
        start, stop = header["kernel_range"]
        require(type(start) is int and type(stop) is int and
                0 <= start < stop <= KERNEL_TOTAL, f"bad kernel range: {path.name}")
        require(start == cursor, f"chunk gap, overlap, or wrong order at {path.name}")
        cursor = stop
        kernels = {row["order_kernel"]: row for row in header["kernels"]}
        stream_digest = hashlib.sha256()
        local_orbits = Counter()
        local_physical = Counter()
        local_remainder_orbits = 0
        local_remainder_physical = 0
        previous = None
        record_count = 0
        physical_count = 0

        for record in records:
            encoded = canonical_bytes(record)
            stream_digest.update(encoded)
            ledger = kernels.get(record.get("order_kernel"))
            require(ledger is not None and record.get("global_kernel") ==
                    ledger["global_kernel"], f"bad residual kernel reference: {path.name}")
            row = record.get("row")
            edges = tuple(map(tuple, ledger["edges"]))
            require(type(row) is list and len(row) == len(edges) and
                    all(type(value) is int and 0 <= value <= edge[2]
                        for value, edge in zip(row, edges, strict=True)),
                    f"nonphysical residual row: {path.name}")
            orbit_size = record.get("orbit_size")
            require(type(orbit_size) is int and orbit_size >= 1 and
                    ledger["automorphisms"] % orbit_size == 0,
                    f"bad residual orbit size: {path.name}")
            code = 0
            stride = 1
            for value, edge in zip(row, edges, strict=True):
                code += value * stride
                stride *= edge[2] + 1
            key = record["order_kernel"], code
            require(previous is None or previous < key,
                    f"residual stream is not strictly ordered: {path.name}")
            previous = key

            lane, detail = owner.recognize_row(atom, edges, tuple(row))
            classification_digest.update(canonical_bytes(
                [source_index, record["global_kernel"], record["order_kernel"],
                 row, orbit_size, lane, detail]))
            source_index += 1
            record_count += 1
            physical_count += orbit_size
            if lane is None:
                local_remainder_orbits += 1
                local_remainder_physical += orbit_size
            else:
                local_orbits[lane] += 1
                local_physical[lane] += orbit_size
                owner_orbits[lane] += 1
                owner_physical[lane] += orbit_size

        raw_sha256, artifact_sha256 = finish()
        validate_header(header, path)
        require(stream_digest.hexdigest() == header["residual_stream_sha256"],
                f"residual digest mismatch: {path.name}")
        require(record_count == header["coarse_residual_total"] and
                physical_count == header["coarse_residual_physical_total"],
                f"residual totals mismatch: {path.name}")
        for key in TOTAL_KEYS:
            totals[key] += header[key]
        chunks.append({
            "artifact_bytes": path.stat().st_size,
            "artifact_sha256": artifact_sha256,
            "coarse_residual_physical_total": physical_count,
            "coarse_residual_total": record_count,
            "exclusive_owner_orbit_counts": dict(sorted(local_orbits.items())),
            "exclusive_owner_physical_counts": dict(sorted(local_physical.items())),
            "kernel_range": [start, stop],
            "path": os.path.relpath(path, output.parent),
            "raw_sha256": raw_sha256,
            "remainder_orbit_total": local_remainder_orbits,
            "remainder_physical_total": local_remainder_physical,
        })

    require(cursor == KERNEL_TOTAL, "chunks do not exactly cover order eleven")
    owned_orbits = sum(owner_orbits.values())
    owned_physical = sum(owner_physical.values())
    remainder_orbits = totals["coarse_residual_total"] - owned_orbits
    remainder_physical = totals["coarse_residual_physical_total"] - owned_physical
    require(sum(row["remainder_orbit_total"] for row in chunks) == remainder_orbits and
            sum(row["remainder_physical_total"] for row in chunks) == remainder_physical,
            "owner/remainder partition mismatch")
    return {
        "schema": SCHEMA,
        "status": "complete-exact-aggregation-with-payload-free-owner-scan",
        "full_theorem": False,
        "scope": "exact census aggregation and sufficient payload-free owner coverage only",
        "rank": RANK,
        "order": ORDER,
        "budget": [RANK - 1, 1],
        "path_count": PATH_COUNT,
        "frontiers_per_residual": TARGETS_PER_RESIDUAL,
        "source_sha256": SOURCE_SHA256,
        "owner_engine_sha256": file_sha256(OWNER_ENGINE),
        "atom_recognizer_sha256": file_sha256(ATOM_RECOGNIZER),
        **dict(totals),
        "chunks": chunks,
        "exclusive_owner_orbit_counts": dict(sorted(owner_orbits.items())),
        "exclusive_owner_physical_counts": dict(sorted(owner_physical.items())),
        "payload_free_owned_orbit_total": owned_orbits,
        "payload_free_owned_physical_total": owned_physical,
        "payload_free_owned_target_total": owned_orbits * TARGETS_PER_RESIDUAL,
        "remainder_orbit_total": remainder_orbits,
        "remainder_physical_total": remainder_physical,
        "remainder_target_total": remainder_orbits * TARGETS_PER_RESIDUAL,
        "classification_stream_sha256": classification_digest.hexdigest(),
    }


def ordered_paths(paths):
    return sorted(paths, key=lambda path: path.name)


def print_totals(payload, prefix):
    print(f"{prefix}: kernels={payload['kernel_total']} physical={payload['physical_row_total']} "
          f"orbits={payload['parity_orbit_total']}")
    print(f"residual_orbits={payload['coarse_residual_total']} "
          f"residual_physical={payload['coarse_residual_physical_total']} "
          f"targets={payload['frontier_target_total']}")
    print(f"payload_free_owned_orbits={payload['payload_free_owned_orbit_total']} "
          f"remainder_orbits={payload['remainder_orbit_total']} "
          f"remainder_physical={payload['remainder_physical_total']}")
    print("full_theorem=false")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    build = subparsers.add_parser("build")
    build.add_argument("chunks", nargs="+", type=Path)
    build.add_argument("--output", required=True, type=Path)
    verify = subparsers.add_parser("verify")
    verify.add_argument("manifest", type=Path)
    args = parser.parse_args()

    if args.command == "build":
        require(args.output.parent.is_dir(), "output parent does not exist")
        payload = scan(ordered_paths(args.chunks), args.output)
        args.output.write_bytes(canonical_bytes(payload))
        print_totals(payload, "order-eleven manifest built")
        return 0

    raw = args.manifest.read_bytes()
    expected = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(expected), "manifest is not canonical ASCII JSON")
    require(expected.get("schema") == SCHEMA and expected.get("full_theorem") is False,
            "wrong manifest schema or theorem boundary")
    paths = [args.manifest.parent / row["path"] for row in expected["chunks"]]
    actual = scan(paths, args.manifest)
    require(canonical_bytes(actual) == raw, "regenerated manifest differs")
    print_totals(actual, "order-eleven manifest verified")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        sys.stderr.write(f"order-eleven structural owner audit: FAIL CLOSED: {error}\n")
        raise SystemExit(1)
