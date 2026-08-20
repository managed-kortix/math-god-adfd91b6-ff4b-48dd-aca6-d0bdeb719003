#!/usr/bin/env python3
"""Segmented, resumable structural-owner scan of the complete order-eleven census."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
import os
import subprocess
import sys
import uuid
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
SEGMENTED_CORE = HERE / "rank7_order12_segmented_owner_scan.py"
MANIFEST_TOOL = HERE / "rank7_order11_structural_owner_manifest.py"
RUN_DIRECTORY = HERE / "rank7_order11_segmented_owner_scan"
DEFAULT_OUTPUT = HERE / "rank7_order11_structural_owner_manifest.json"
RANGES = ((0, 348), (348, 696), (696, 1044), (1044, 1391))
DEFAULT_CHUNKS = tuple(
    HERE / f"rank7_order11_census_{start:04d}_{stop:04d}.json.xz"
    for start, stop in RANGES
)
LANES = ("balanced-rank-one", "signed-imbalance-psd", "simplex-mixed-atom",
         "cubic-cycle-space-candidate")
FINAL_SCHEMA = "rank-seven-order-eleven-structural-owner-manifest-v2"
SCAN_OWNER_ENGINE_SHA256 = "153451978bedd29cfc39f37ee1cdbcd2eb6789430925774426db9c9b2d29eea8"
TOTAL_KEYS = ("kernel_total", "physical_row_total", "parity_orbit_total",
              "coarse_certified_total", "coarse_residual_total",
              "coarse_residual_physical_total", "frontier_target_total")
SEGMENT_SUMMARY_KEYS = ("row_range", "exclusive_owner_orbit_counts",
                        "exclusive_owner_physical_counts", "remainder_orbit_total",
                        "remainder_physical_total", "classification_stream_sha256")


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load_module("rank7_order11_segmented_core", SEGMENTED_CORE)
MANIFEST = load_module("rank7_order11_manifest_tool", MANIFEST_TOOL)


def configure_core():
    CORE.OWNER_ENGINE = MANIFEST_TOOL
    CORE.RUN_DIRECTORY = RUN_DIRECTORY
    CORE.DEFAULT_CHUNKS = DEFAULT_CHUNKS
    CORE.CHUNK_PATTERN = __import__("re").compile(
        r"rank7_order11_census_(\d{4})_(\d{4})\.json\.xz\Z")
    CORE.SCHEMA = "rank-seven-order-eleven-segmented-owner-scan-v1"
    CORE.SEGMENT_SCHEMA = "rank-seven-order-eleven-owner-segment-v1"
    CORE.LANES = LANES
    CORE.load_owner_engine = MANIFEST.load_owner_engine

    base_atomic_json = CORE.atomic_json
    base_validate_segment = CORE.validate_segment
    base_aggregate_segments = CORE.aggregate_segments

    def atomic_json(path, payload, canonical=False):
        if payload.get("schema") == CORE.SEGMENT_SCHEMA:
            payload["owner_precedence"] = list(LANES)
        base_atomic_json(path, payload, canonical)

    def validate_segment(payload, identity, expected_start=None):
        CORE.require(payload.get("owner_precedence") == list(LANES),
                     "segment owner precedence changed")
        return base_validate_segment(payload, identity, expected_start)

    def aggregate_segments(identity, header, segments, complete):
        return {**base_aggregate_segments(identity, header, segments, complete),
                "owner_precedence": list(LANES)}

    CORE.atomic_json = atomic_json
    CORE.validate_segment = validate_segment
    CORE.aggregate_segments = aggregate_segments

    def recognize_exact(owner, atom, edges, row):
        return owner.recognize_row(atom, edges, row)

    CORE.recognize_exact = recognize_exact


configure_core()


def launch(args):
    CORE.require(args.checkpoint_rows > 0, "checkpoint size must be positive")
    CORE.require(tuple(map(tuple, sorted(CORE.chunk_id(path)[1] for path in args.chunks))) ==
                 RANGES,
                 "launch chunks do not exactly partition all 1391 order-eleven kernels")
    CORE.prepare_directories(args.run_directory)
    jobs = []
    launched = []
    for chunk in sorted(args.chunks, key=lambda path: CORE.chunk_id(path)[1]):
        CORE.require(chunk.is_file(), f"missing census chunk: {chunk}")
        identifier, kernel_range = CORE.chunk_id(chunk)
        paths = CORE.job_paths(args.run_directory, identifier)
        status = "pending"
        pid = None
        if paths["result"].is_file():
            status = "completed"
        elif CORE.active_lock(paths["lock"]):
            status = "running"
        else:
            token = uuid.uuid4().hex
            CORE.require(CORE.reserve(paths["lock"], kernel_range, token),
                         f"could not reserve chunk {identifier}")
            command = [sys.executable, "-u", str(Path(__file__).resolve()), "worker",
                       "--chunk", str(chunk), "--checkpoint-rows",
                       str(args.checkpoint_rows), "--run-directory",
                       str(args.run_directory), "--token", token]
            stream = paths["log"].open("a", encoding="utf-8")
            process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=stream,
                                       stderr=subprocess.STDOUT, start_new_session=True)
            stream.close()
            pid = process.pid
            paths["pid"].write_text(f"{pid}\n", encoding="ascii")
            status = "launched"
            launched.append({"chunk": identifier, "pid": pid})
        jobs.append({"chunk": identifier, "kernel_range": kernel_range,
                     "path": str(chunk), "pid": pid, "status": status})
    payload = {
        "schema": "rank-seven-order-eleven-owner-scheduler-v1",
        "checkpoint_rows": args.checkpoint_rows,
        "manifest_tool": str(MANIFEST_TOOL),
        "owner_precedence": list(LANES),
        "jobs": jobs,
        "launched": launched,
        "updated_at": CORE.timestamp(),
    }
    CORE.atomic_json(args.run_directory / "scheduler.json", payload)
    for row in jobs:
        suffix = f" pid={row['pid']}" if row["pid"] is not None else ""
        print(f"chunk={row['chunk']} status={row['status']}{suffix}")
    return 0


def canonical_payload(path, label):
    raw = path.read_bytes()
    payload = json.loads(raw.decode("ascii"))
    CORE.require(raw == CORE.canonical_bytes(payload), f"noncanonical {label}: {path.name}")
    return payload, raw


def exact_nonnegative(value, label):
    CORE.require(type(value) is int and value >= 0, f"bad {label}")
    return value


def authenticate_census(path, expected_range):
    artifact_sha256 = MANIFEST.file_sha256(path)
    raw_digest = hashlib.sha256()
    marker = b'"residuals":['
    tail_marker = b'],"schema"'
    prefix = bytearray()
    tail = bytearray()
    found_payload = False
    with lzma.open(path, "rb") as stream:
        while block := stream.read(1 << 20):
            raw_digest.update(block)
            if not found_payload:
                position = block.find(marker)
                if position < 0:
                    prefix.extend(block)
                    continue
                prefix.extend(block[:position])
                block = block[position + len(marker):]
                found_payload = True
            tail.extend(block)
            if len(tail) > (1 << 20):
                del tail[:len(tail) - (1 << 20)]
    CORE.require(found_payload, f"missing census residual stream: {path.name}")
    position = tail.rfind(tail_marker)
    CORE.require(position >= 0, f"missing census residual suffix: {path.name}")
    suffix = bytes(tail[position + 1:])
    CORE.require(suffix.endswith(b"\n"), f"missing canonical newline: {path.name}")
    raw_header = bytes(prefix) + b'"residuals":[]' + suffix[:-1]
    header = MANIFEST.load_owner_engine().strict_json(raw_header, path.name)
    header.pop("residuals")
    CORE.require(header.get("kernel_range") == list(expected_range),
                 f"census range/name mismatch: {path.name}")
    MANIFEST.validate_header(header, path)
    return header, {
        "artifact_bytes": path.stat().st_size,
        "artifact_sha256": artifact_sha256,
        "raw_sha256": raw_digest.hexdigest(),
        "residual_stream_sha256": header["residual_stream_sha256"],
    }


def authenticate_result(result_path, segment_directory, census_path, header, artifact):
    result, result_raw = canonical_payload(result_path, "chunk result")
    CORE.require(result.get("schema") == CORE.SCHEMA and
                 result.get("status") == "completed" and
                 result.get("full_theorem") is False,
                 f"incomplete or wrong chunk result: {result_path.name}")
    identity = result["identity"]
    CORE.require(identity.get("chunk_sha256") == artifact["artifact_sha256"] and
                 result.get("artifact_sha256") == artifact["artifact_sha256"] and
                 result.get("raw_sha256") == artifact["raw_sha256"],
                 f"chunk result does not bind census: {result_path.name}")
    CORE.require(Path(identity.get("chunk_path", "")).name == census_path.name,
                 f"chunk result census path changed: {result_path.name}")
    CORE.require(identity.get("atom_recognizer_sha256") ==
                 MANIFEST.file_sha256(MANIFEST.ATOM_RECOGNIZER),
                 f"chunk result atom recognizer changed: {result_path.name}")
    CORE.require(identity.get("owner_engine_sha256") == SCAN_OWNER_ENGINE_SHA256,
                 f"chunk result owner engine changed: {result_path.name}")
    CORE.require(result.get("owner_precedence") == list(LANES) and
                 result.get("kernel_range") == header["kernel_range"],
                 f"chunk result scope changed: {result_path.name}")

    orbit_counts = Counter({lane: 0 for lane in LANES})
    physical_counts = Counter({lane: 0 for lane in LANES})
    remainder_orbits = remainder_physical = cursor = 0
    segment_digest = hashlib.sha256()
    artifact_digest = hashlib.sha256()
    summaries = result["segments"]
    paths = sorted(segment_directory.glob("rows-*.json"))
    CORE.require(len(paths) == len(summaries) and paths,
                 f"segment census differs from result: {result_path.name}")
    for index, (path, summary) in enumerate(zip(paths, summaries, strict=True)):
        segment, raw = canonical_payload(path, "owner segment")
        cursor = CORE.validate_segment(segment, identity, cursor)
        CORE.require(path == CORE.segment_path({"segments": segment_directory},
                                               *segment["row_range"]),
                     f"segment filename does not match payload: {path.name}")
        CORE.require({key: segment[key] for key in SEGMENT_SUMMARY_KEYS} == summary,
                     f"segment/result disagreement: {path.name}")
        for lane in LANES:
            orbit_counts[lane] += exact_nonnegative(
                segment["exclusive_owner_orbit_counts"][lane], f"segment orbit count {index}")
            physical_counts[lane] += exact_nonnegative(
                segment["exclusive_owner_physical_counts"][lane],
                f"segment physical count {index}")
        remainder_orbits += exact_nonnegative(segment["remainder_orbit_total"],
                                              f"segment remainder count {index}")
        remainder_physical += exact_nonnegative(segment["remainder_physical_total"],
                                                f"segment physical remainder {index}")
        classification = segment["classification_stream_sha256"]
        CORE.require(type(classification) is str and len(classification) == 64,
                     f"bad segment classification digest: {path.name}")
        segment_digest.update(bytes.fromhex(classification))
        artifact_digest.update(hashlib.sha256(raw).digest())

    owned_orbits = sum(orbit_counts.values())
    owned_physical = sum(physical_counts.values())
    CORE.require(cursor == header["coarse_residual_total"] and
                 owned_orbits + remainder_orbits == cursor,
                 f"segment orbit partition mismatch: {result_path.name}")
    CORE.require(owned_physical + remainder_physical ==
                 header["coarse_residual_physical_total"],
                 f"segment physical partition mismatch: {result_path.name}")
    expected = {
        "coarse_residual_orbit_total": cursor,
        "coarse_residual_physical_total": header["coarse_residual_physical_total"],
        "exclusive_owner_orbit_counts": dict(sorted(orbit_counts.items())),
        "exclusive_owner_physical_counts": dict(sorted(physical_counts.items())),
        "owned_orbit_total": owned_orbits,
        "owned_physical_total": owned_physical,
        "remainder_orbit_total": remainder_orbits,
        "remainder_physical_total": remainder_physical,
        "scanned_orbit_total": cursor,
        "segment_digest_sha256": segment_digest.hexdigest(),
    }
    CORE.require(all(result.get(key) == value for key, value in expected.items()),
                 f"chunk result aggregate changed: {result_path.name}")
    return {
        **artifact,
        "classification_segment_digest_sha256": segment_digest.hexdigest(),
        "exclusive_owner_orbit_counts": dict(sorted(orbit_counts.items())),
        "exclusive_owner_physical_counts": dict(sorted(physical_counts.items())),
        "kernel_range": header["kernel_range"],
        "remainder_orbit_total": remainder_orbits,
        "remainder_physical_total": remainder_physical,
        "result_artifact_bytes": len(result_raw),
        "result_artifact_sha256": hashlib.sha256(result_raw).hexdigest(),
        "scan_owner_engine_sha256": identity["owner_engine_sha256"],
        "segment_artifacts_sha256": artifact_digest.hexdigest(),
        "segment_total": len(paths),
    }


def build_manifest(sources, output):
    totals = Counter({key: 0 for key in TOTAL_KEYS})
    owner_orbits = Counter({lane: 0 for lane in LANES})
    owner_physical = Counter({lane: 0 for lane in LANES})
    remainder_orbits = remainder_physical = 0
    chunks = []
    global_classification = hashlib.sha256()
    scan_engines = set()
    cursor = 0
    for census_path, result_path, segment_directory in sources:
        _, expected_range = CORE.chunk_id(census_path)
        CORE.require(expected_range[0] == cursor, f"chunk gap or overlap: {census_path.name}")
        header, artifact = authenticate_census(census_path, expected_range)
        chunk = authenticate_result(result_path, segment_directory, census_path,
                                    header, artifact)
        cursor = expected_range[1]
        for key in TOTAL_KEYS:
            totals[key] += header[key]
        owner_orbits.update(chunk["exclusive_owner_orbit_counts"])
        owner_physical.update(chunk["exclusive_owner_physical_counts"])
        remainder_orbits += chunk["remainder_orbit_total"]
        remainder_physical += chunk["remainder_physical_total"]
        global_classification.update(bytes.fromhex(
            chunk["classification_segment_digest_sha256"]))
        scan_engines.add(chunk.pop("scan_owner_engine_sha256"))
        chunk["path"] = os.path.relpath(census_path, output.parent)
        chunk["result_path"] = os.path.relpath(result_path, output.parent)
        chunk["segment_directory"] = os.path.relpath(segment_directory, output.parent)
        chunks.append(chunk)
    CORE.require(cursor == 1391 and len(chunks) == 4, "chunks do not cover order eleven")
    CORE.require(len(scan_engines) == 1, "chunk scans used different owner engines")
    owned_orbits = sum(owner_orbits.values())
    owned_physical = sum(owner_physical.values())
    CORE.require(owned_orbits + remainder_orbits == totals["coarse_residual_total"] and
                 owned_physical + remainder_physical ==
                 totals["coarse_residual_physical_total"],
                 "global owner/remainder partition mismatch")
    return {
        "schema": FINAL_SCHEMA,
        "status": "complete-exact-streaming-aggregation-of-authenticated-segment-scans",
        "full_theorem": False,
        "scope": "exact census and structural-owner aggregation only; no theorem claim",
        "rank": 7,
        "order": 11,
        "budget": [6, 1],
        "path_count": 17,
        "frontiers_per_residual": 18,
        "source_sha256": MANIFEST.SOURCE_SHA256,
        "scan_owner_engine_sha256": scan_engines.pop(),
        "atom_recognizer_sha256": MANIFEST.file_sha256(MANIFEST.ATOM_RECOGNIZER),
        **dict(totals),
        "chunks": chunks,
        "owner_precedence": list(LANES),
        "exclusive_owner_orbit_counts": dict(sorted(owner_orbits.items())),
        "exclusive_owner_physical_counts": dict(sorted(owner_physical.items())),
        "payload_free_owned_orbit_total": owned_orbits,
        "payload_free_owned_physical_total": owned_physical,
        "payload_free_owned_target_total": owned_orbits * 18,
        "remainder_orbit_total": remainder_orbits,
        "remainder_physical_total": remainder_physical,
        "remainder_target_total": remainder_orbits * 18,
        "classification_segment_digest_sha256": global_classification.hexdigest(),
    }


def default_sources(run_directory):
    rows = []
    for chunk in DEFAULT_CHUNKS:
        identifier, _ = CORE.chunk_id(chunk)
        paths = CORE.job_paths(run_directory, identifier)
        rows.append((chunk, paths["result"], paths["segments"]))
    return rows


def print_manifest(payload, prefix):
    print(f"{prefix}: kernels={payload['kernel_total']} "
          f"residual_orbits={payload['coarse_residual_total']} "
          f"residual_physical={payload['coarse_residual_physical_total']}")
    print(f"owned_orbits={payload['payload_free_owned_orbit_total']} "
          f"owned_physical={payload['payload_free_owned_physical_total']} "
          f"remainder_orbits={payload['remainder_orbit_total']} "
          f"remainder_physical={payload['remainder_physical_total']}")
    print("full_theorem=false")


def finalize(args):
    payload = build_manifest(default_sources(args.run_directory), args.output)
    CORE.atomic_json(args.output, payload, canonical=True)
    print_manifest(payload, "order-eleven streaming manifest built")
    return 0


def verify(args):
    expected, raw = canonical_payload(args.manifest, "structural owner manifest")
    CORE.require(expected.get("schema") == FINAL_SCHEMA and
                 expected.get("full_theorem") is False,
                 "wrong manifest schema or theorem boundary")
    sources = [(args.manifest.parent / chunk["path"],
                args.manifest.parent / chunk["result_path"],
                args.manifest.parent / chunk["segment_directory"])
               for chunk in expected["chunks"]]
    actual = build_manifest(sources, args.manifest)
    CORE.require(CORE.canonical_bytes(actual) == raw, "regenerated manifest differs")
    print_manifest(actual, "order-eleven streaming manifest verified")
    return 0


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    launch_parser = subparsers.add_parser("launch")
    launch_parser.add_argument("chunks", nargs="*", type=Path, default=list(DEFAULT_CHUNKS))
    launch_parser.add_argument("--checkpoint-rows", type=int, default=10000)
    launch_parser.add_argument("--run-directory", type=Path, default=RUN_DIRECTORY)
    worker_parser = subparsers.add_parser("worker")
    worker_parser.add_argument("--chunk", required=True, type=Path)
    worker_parser.add_argument("--checkpoint-rows", type=int, default=10000)
    worker_parser.add_argument("--run-directory", type=Path, default=RUN_DIRECTORY)
    worker_parser.add_argument("--token", required=True)
    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--run-directory", type=Path, default=RUN_DIRECTORY)
    finalize_parser = subparsers.add_parser("finalize")
    finalize_parser.add_argument("--run-directory", type=Path, default=RUN_DIRECTORY)
    finalize_parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    if args.command == "launch":
        return launch(args)
    if args.command == "worker":
        return CORE.worker(args)
    if args.command == "finalize":
        return finalize(args)
    if args.command == "verify":
        return verify(args)
    return CORE.status(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        sys.stderr.write(f"order-eleven segmented owner scan: FAIL CLOSED: {error}\n")
        raise SystemExit(1)
