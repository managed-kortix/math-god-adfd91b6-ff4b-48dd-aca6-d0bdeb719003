#!/usr/bin/env python3
"""Streaming payload-free structural-owner scan for rank seven/order nine."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import multiprocessing
import os
import sys
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
OWNER_ENGINE = HERE / "rank7_order12_structural_owners.py"
ATOM_RECOGNIZER = HERE / "rank7_order7_symbolic_atom_recognizer.py"
DEFAULT_MANIFEST = HERE / "rank7_order9_exact_residual_census_manifest.json"
ORDER = 9
RANK = 7
PATH_COUNT = 15
TARGETS_PER_RESIDUAL = 16
KERNEL_TOTAL = 4495
SOURCE_SHA256 = "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5"
CHUNK_SCHEMA = "rank-seven-orders9-12-exact-residual-census-chunk-v1"
MANIFEST_SCHEMA = "rank-seven-orders9-12-exact-residual-census-manifest-v1"
SCHEMA = "rank-seven-order-nine-structural-owner-coverage-v1"
LANES = ("balanced-rank-one", "signed-imbalance-psd", "simplex-mixed-atom",
         "generalized-ray")
WORKER_ENGINE = None
WORKER_ATOM = None


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


def load_engine():
    spec = importlib.util.spec_from_file_location("rank7_order9_owner_core", OWNER_ENGINE)
    require(spec is not None and spec.loader is not None, "cannot load owner engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ORDER = ORDER
    module.RANK = RANK
    module.PATH_COUNT = PATH_COUNT
    module.TARGETS_PER_ROW = TARGETS_PER_RESIDUAL
    module.BUDGET = module.F(RANK - 1)
    return module


def load_manifest(path):
    raw = path.read_bytes()
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), "census manifest is not canonical JSON")
    require(payload.get("schema") == MANIFEST_SCHEMA and
            payload.get("full_theorem") is False, "wrong census manifest")
    require((payload.get("rank"), payload.get("order"), payload.get("path_count"),
             payload.get("frontiers_per_residual"), payload.get("kernel_total"),
             payload.get("source_sha256")) ==
            (RANK, ORDER, PATH_COUNT, TARGETS_PER_RESIDUAL, KERNEL_TOTAL,
             SOURCE_SHA256), "census scope changed")
    return payload, hashlib.sha256(raw).hexdigest()


def recognize_row(engine, atom, edges, row):
    if engine.balanced_rank_one(edges, row):
        return "balanced-rank-one", None
    imbalance = engine.signed_imbalance_certificate(edges, row)
    if imbalance is not None:
        return "signed-imbalance-psd", [imbalance[0], imbalance[1].numerator,
                                         imbalance[1].denominator]
    owners = (() if not engine.atom_profile_candidate(edges, row) else
              tuple(record for record in atom.recognize(edges, row)
                    if record["status"] == "exact-equality-owner"))
    if owners:
        profiles = sorted({(record["profile"]["mixed"],
                            tuple(record["profile"]["simplex_widths"]))
                           for record in owners})
        return "simplex-mixed-atom", [[mixed, list(widths)]
                                       for mixed, widths in profiles]
    if engine.generalized_three_ray_owner(edges, row):
        return "generalized-ray", ["signed-three-ray"]
    return None, None


def initialize_worker():
    global WORKER_ENGINE, WORKER_ATOM
    WORKER_ENGINE = load_engine()
    WORKER_ATOM = WORKER_ENGINE.load_atom_recognizer()


def recognize_task(task):
    record, edges = task
    lane, detail = recognize_row(WORKER_ENGINE, WORKER_ATOM, edges,
                                 tuple(record["row"]))
    return record, lane, detail


def scan(manifest_path, output_path, progress=False, limit=None, jobs=1):
    require(jobs >= 1, "job count must be positive")
    manifest, manifest_sha256 = load_manifest(manifest_path)
    engine = load_engine()
    atom = engine.load_atom_recognizer()
    owner_orbits = Counter({lane: 0 for lane in LANES})
    owner_physical = Counter({lane: 0 for lane in LANES})
    profiles = Counter()
    chunks = []
    classification_digest = hashlib.sha256()
    remainder_digest = hashlib.sha256()
    source_index = 0
    cursor = 0
    stop = False

    pool = None
    if jobs > 1:
        pool = multiprocessing.Pool(jobs, initializer=initialize_worker)
    try:
        for expected in manifest["chunks"]:
            path = (manifest_path.parent / expected["path"]).resolve()
            require(path.parent == manifest_path.parent.resolve(), "chunk path escapes directory")
            header, records, finish = engine.stream_chunk(path)
            start, end = header["kernel_range"]
            require(start == cursor and [start, end] == expected["kernel_range"],
                    f"chunk range changed: {path.name}")
            cursor = end
            kernels = {record["order_kernel"]: record for record in header["kernels"]}
            stream_digest = hashlib.sha256()
            local_orbits = Counter()
            local_physical = Counter()
            local_remainder_orbits = local_remainder_physical = local_count = 0
            submitted = 0
            chunk_source_index = source_index

            def tasks():
                nonlocal stop, submitted
                for record in records:
                    stream_digest.update(canonical_bytes(record))
                    if limit is not None and chunk_source_index + submitted >= limit:
                        stop = True
                        continue
                    kernel = kernels[record["order_kernel"]]
                    require(record["global_kernel"] == kernel["global_kernel"],
                            f"bad kernel reference: {path.name}")
                    submitted += 1
                    yield record, tuple(map(tuple, kernel["edges"]))

            results = (map(lambda task: (task[0],) + recognize_row(
                engine, atom, task[1], tuple(task[0]["row"])), tasks())
                       if pool is None else pool.imap(recognize_task, tasks(), chunksize=256))
            for record, lane, detail in results:
                orbit_size = record["orbit_size"]
                require(type(orbit_size) is int and orbit_size >= 1,
                        f"bad orbit size: {path.name}")
                classification_digest.update(canonical_bytes(
                    [source_index, record["global_kernel"], record["order_kernel"],
                     record["row"], orbit_size, lane, detail]))
                if lane is None:
                    remainder_digest.update(canonical_bytes(
                        [source_index, record["global_kernel"], record["order_kernel"],
                         record["row"], orbit_size]))
                    local_remainder_orbits += 1
                    local_remainder_physical += orbit_size
                else:
                    owner_orbits[lane] += 1
                    owner_physical[lane] += orbit_size
                    local_orbits[lane] += 1
                    local_physical[lane] += orbit_size
                    if lane == "simplex-mixed-atom":
                        profiles.update(f"mixed-{mixed}/simplex-{'-'.join(map(str, widths)) or 'none'}"
                                        for mixed, widths in detail)
                source_index += 1
                local_count += 1

            raw_sha256, artifact_sha256 = finish()
            require(header.get("schema") == CHUNK_SCHEMA and
                    (header.get("rank"), header.get("order"), header.get("path_count"),
                     header.get("source_sha256")) ==
                    (RANK, ORDER, PATH_COUNT, SOURCE_SHA256), f"wrong chunk scope: {path.name}")
            require(stream_digest.hexdigest() == header["residual_stream_sha256"],
                    f"residual digest mismatch: {path.name}")
            require((raw_sha256, artifact_sha256) ==
                    (expected["raw_sha256"], expected["artifact_sha256"]),
                    f"chunk digest changed: {path.name}")
            if not stop:
                require(local_count == expected["coarse_residual_total"],
                        f"chunk residual count changed: {path.name}")
            chunks.append({
                "artifact_sha256": artifact_sha256,
                "exclusive_owner_orbit_counts": dict(sorted(local_orbits.items())),
                "exclusive_owner_physical_counts": dict(sorted(local_physical.items())),
                "kernel_range": [start, end],
                "path": os.path.relpath(path, output_path.parent),
                "remainder_orbit_total": local_remainder_orbits,
                "remainder_physical_total": local_remainder_physical,
                "scanned_residual_total": local_count,
            })
            if progress:
                print(f"chunk={path.name} scanned={source_index} owned={sum(owner_orbits.values())}",
                      flush=True)
            if stop:
                break
    finally:
        if pool is not None:
            pool.close()
            pool.join()

    if limit is None:
        require(cursor == KERNEL_TOTAL and source_index == manifest["coarse_residual_total"],
                "chunks do not cover the exact residual universe")
    owned_orbits = sum(owner_orbits.values())
    owned_physical = sum(owner_physical.values())
    remainder_orbits = source_index - owned_orbits
    remainder_physical = sum(row["remainder_physical_total"] for row in chunks)
    return {
        "schema": SCHEMA,
        "status": "complete-exact-streaming-payload-free-owner-scan",
        "full_theorem": False,
        "scope": "sufficient structural owners only; no rational search",
        "rank": RANK,
        "order": ORDER,
        "path_count": PATH_COUNT,
        "frontiers_per_residual": TARGETS_PER_RESIDUAL,
        "manifest_sha256": manifest_sha256,
        "owner_engine_sha256": file_sha256(OWNER_ENGINE),
        "atom_recognizer_sha256": file_sha256(ATOM_RECOGNIZER),
        "chunks": chunks,
        "scanned_residual_total": source_index,
        "scanned_target_total": source_index * TARGETS_PER_RESIDUAL,
        "exclusive_owner_orbit_counts": dict(sorted(owner_orbits.items())),
        "exclusive_owner_physical_counts": dict(sorted(owner_physical.items())),
        "atom_profile_owner_counts": dict(sorted(profiles.items())),
        "payload_free_owned_orbit_total": owned_orbits,
        "payload_free_owned_physical_total": owned_physical,
        "payload_free_owned_target_total": owned_orbits * TARGETS_PER_RESIDUAL,
        "remainder_orbit_total": remainder_orbits,
        "remainder_physical_total": remainder_physical,
        "remainder_target_total": remainder_orbits * TARGETS_PER_RESIDUAL,
        "classification_stream_sha256": classification_digest.hexdigest(),
        "remainder_stream_sha256": remainder_digest.hexdigest(),
    }


def verify_report(payload):
    require(payload.get("schema") == SCHEMA and payload.get("full_theorem") is False,
            "wrong report schema")
    require(set(payload["exclusive_owner_orbit_counts"]) == set(LANES) and
            set(payload["exclusive_owner_physical_counts"]) == set(LANES),
            "owner lane ledger changed")
    require(sum(payload["exclusive_owner_orbit_counts"].values()) ==
            payload["payload_free_owned_orbit_total"], "owner orbit sum changed")
    require(payload["scanned_residual_total"] ==
            payload["payload_free_owned_orbit_total"] + payload["remainder_orbit_total"],
            "owner/remainder partition changed")
    for source, target in (("scanned_residual_total", "scanned_target_total"),
                           ("payload_free_owned_orbit_total", "payload_free_owned_target_total"),
                           ("remainder_orbit_total", "remainder_target_total")):
        require(payload[target] == TARGETS_PER_RESIDUAL * payload[source],
                f"target arithmetic changed: {target}")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    build = subparsers.add_parser("build")
    build.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    build.add_argument("--output", required=True, type=Path)
    build.add_argument("--progress", action="store_true")
    build.add_argument("--jobs", type=int, default=1)
    build.add_argument("--limit", type=int, help="test-only global row limit")
    verify = subparsers.add_parser("verify")
    verify.add_argument("report", type=Path)
    verify.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    verify.add_argument("--progress", action="store_true")
    verify.add_argument("--jobs", type=int, default=1)
    args = parser.parse_args()
    if args.command == "build":
        require(args.output.parent.is_dir(), "output parent does not exist")
        report = scan(args.manifest, args.output, args.progress, args.limit, args.jobs)
        verify_report(report)
        args.output.write_bytes(canonical_bytes(report))
        print(canonical_bytes(report).decode("ascii"), end="")
        return
    raw = args.report.read_bytes()
    expected = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(expected), "report is not canonical JSON")
    verify_report(expected)
    actual = scan(args.manifest, args.report, args.progress, jobs=args.jobs)
    require(canonical_bytes(actual) == raw, "report differs from exact rescan")
    print(f"audit=passed report_sha256={hashlib.sha256(raw).hexdigest()} "
          f"owned={actual['payload_free_owned_orbit_total']} "
          f"remainder={actual['remainder_orbit_total']}")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        sys.stderr.write(f"order-nine structural owner audit: FAIL CLOSED: {error}\n")
        raise SystemExit(1)
