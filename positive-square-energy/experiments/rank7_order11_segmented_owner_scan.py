#!/usr/bin/env python3
"""Segmented, resumable structural-owner scan of the complete order-eleven census."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import uuid
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


def finalize(args):
    for chunk in DEFAULT_CHUNKS:
        identifier, _ = CORE.chunk_id(chunk)
        result = CORE.job_paths(args.run_directory, identifier)["result"]
        CORE.require(result.is_file(), f"segmented scan is incomplete: {identifier}")
        CORE.require(CORE.load_json(result).get("status") == "completed",
                     f"segmented result is not complete: {identifier}")
    command = [sys.executable, "-u", str(MANIFEST_TOOL), "build", *map(str, DEFAULT_CHUNKS),
               "--output", str(args.output)]
    return subprocess.run(command, check=False).returncode


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
    args = parser.parse_args()
    if args.command == "launch":
        return launch(args)
    if args.command == "worker":
        return CORE.worker(args)
    if args.command == "finalize":
        return finalize(args)
    return CORE.status(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        sys.stderr.write(f"order-eleven segmented owner scan: FAIL CLOSED: {error}\n")
        raise SystemExit(1)
