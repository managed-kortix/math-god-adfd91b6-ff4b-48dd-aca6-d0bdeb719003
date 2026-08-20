#!/usr/bin/env python3
"""Durable launcher for the full segmented order-eight typed-diagonal replay."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path


HERE = Path(__file__).resolve().parent
VERIFIER_PATH = HERE / "rank7_order8_typed_diagonal_segmented_verifier.py"
RUN_DIRECTORY = HERE / "rank7_order8_typed_diagonal_scheduler"
RECEIPT_DIRECTORY = HERE / "rank7_order8_typed_diagonal_receipts"
TOTAL_ROWS = 492812


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def atomic_json(path, payload):
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="ascii")
    temporary.replace(path)


def load_verifier():
    spec = importlib.util.spec_from_file_location("rank7_order8_typed_scheduler_verifier",
                                                  VERIFIER_PATH)
    require(spec is not None and spec.loader is not None, "cannot load segmented verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare_directories(run_directory, receipt_directory):
    run_directory.mkdir(exist_ok=True)
    receipt_directory.mkdir(exist_ok=True)
    for name in ("locks", "logs", "pids", "state"):
        (run_directory / name).mkdir(exist_ok=True)


def segment_name(start, stop):
    return f"{start:06d}-{stop:06d}"


def paths(run_directory, receipt_directory, start, stop):
    name = segment_name(start, stop)
    return {
        "name": name,
        "receipt": receipt_directory / f"receipt-{name}.json",
        "lock": run_directory / "locks" / f"segment-{name}.lock",
        "log": run_directory / "logs" / f"segment-{name}.log",
        "pid": run_directory / "pids" / f"segment-{name}.pid",
        "state": run_directory / "state" / f"segment-{name}.json",
    }


def process_alive(pid):
    try:
        os.kill(pid, 0)
    except (OSError, ValueError):
        return False
    return True


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="ascii"))
    except (OSError, ValueError, TypeError):
        return {}


def active_lock(path):
    if not path.exists():
        return False
    pid = read_json(path).get("pid")
    if type(pid) is int and process_alive(pid):
        return True
    path.unlink(missing_ok=True)
    return False


def reserve(path, row_range, token):
    payload = json.dumps({"pid": os.getpid(), "range": row_range, "status": "reserved",
                          "token": token, "reserved_at": timestamp()}, sort_keys=True) + "\n"
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        return False
    with os.fdopen(descriptor, "w", encoding="ascii") as stream:
        stream.write(payload)
    return True


def receipt_digest(verifier, receipt_path, census, residuals, start, stop, search):
    if not receipt_path.is_file():
        return None
    payload, digest = verifier.read_canonical(receipt_path, receipt_path.name)
    verifier.validate_receipt(payload, census, residuals)
    require(payload["row_range"] == [start, stop] and payload["search"] == search,
            f"incompatible existing receipt: {receipt_path.name}")
    return digest


def worker(args):
    prepare_directories(args.run_directory, args.receipt_directory)
    job = paths(args.run_directory, args.receipt_directory, args.start, args.stop)
    reserved = read_json(job["lock"])
    require(reserved.get("token") == args.token and reserved.get("status") == "reserved",
            "worker does not own the segment reservation")
    atomic_json(job["lock"], {"pid": os.getpid(), "range": [args.start, args.stop],
                              "status": "running", "started_at": timestamp()})
    atomic_json(job["state"], {"status": "running", "pid": os.getpid(),
                               "range": [args.start, args.stop], "updated_at": timestamp()})
    try:
        command = [sys.executable, "-u", str(VERIFIER_PATH), "verify-segment",
                   "--start", str(args.start), "--stop", str(args.stop),
                   "--output", str(job["receipt"]), "--workers", str(args.workers),
                   "--passes", str(args.passes), "--max-denominator",
                   str(args.max_denominator), "--maximum", str(args.maximum), "--progress"]
        with job["log"].open("a", encoding="utf-8") as stream:
            stream.write(f"[{timestamp()}] exec: {' '.join(command)}\n")
            stream.flush()
            completed = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=stream,
                                       stderr=subprocess.STDOUT, check=False)
            stream.write(f"[{timestamp()}] exit: {completed.returncode}\n")
        require(completed.returncode == 0, f"verifier exited with status {completed.returncode}")
        digest = hashlib.sha256(job["receipt"].read_bytes()).hexdigest()
        result = {"status": "completed", "range": [args.start, args.stop],
                  "receipt": job["receipt"].name, "receipt_sha256": digest,
                  "completed_at": timestamp()}
        atomic_json(job["state"], result)
        return 0
    except Exception as error:
        atomic_json(job["state"], {"status": "failed", "pid": os.getpid(),
                                   "range": [args.start, args.stop], "error": str(error),
                                   "updated_at": timestamp()})
        return 1
    finally:
        job["lock"].unlink(missing_ok=True)


def launch(args):
    require(args.chunk_rows > 0 and args.workers > 0 and args.passes > 0 and
            args.max_denominator > 0 and args.maximum > 0, "invalid launch parameters")
    prepare_directories(args.run_directory, args.receipt_directory)
    verifier = load_verifier()
    _, _, census, residuals = verifier.load_scope(args.census_cache)
    require(len(residuals) == TOTAL_ROWS, "residual stream size changed")
    search = {"maximum_denominator": args.max_denominator, "maximum": args.maximum,
              "coordinate_passes": args.passes,
              "d0_scales": [[1, 2], [2, 3], [1, 1], [3, 2], [2, 1]]}
    jobs = []
    launched = []
    for start in range(0, TOTAL_ROWS, args.chunk_rows):
        stop = min(start + args.chunk_rows, TOTAL_ROWS)
        job = paths(args.run_directory, args.receipt_directory, start, stop)
        digest = receipt_digest(verifier, job["receipt"], census, residuals, start, stop, search)
        pid = None
        if digest is not None:
            status = "completed"
        elif active_lock(job["lock"]):
            status = "running"
            pid = read_json(job["lock"]).get("pid")
        else:
            token = uuid.uuid4().hex
            require(reserve(job["lock"], [start, stop], token),
                    f"could not reserve segment {job['name']}")
            command = [sys.executable, "-u", str(Path(__file__).resolve()), "worker",
                       "--start", str(start), "--stop", str(stop), "--workers",
                       str(args.workers), "--passes", str(args.passes),
                       "--max-denominator", str(args.max_denominator), "--maximum",
                       str(args.maximum), "--census-cache", str(args.census_cache),
                       "--receipt-directory", str(args.receipt_directory),
                       "--run-directory", str(args.run_directory), "--token", token]
            stream = job["log"].open("a", encoding="utf-8")
            process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=stream,
                                       stderr=subprocess.STDOUT, start_new_session=True)
            stream.close()
            pid = process.pid
            job["pid"].write_text(f"{pid}\n", encoding="ascii")
            status = "launched"
            launched.append({"range": [start, stop], "pid": pid})
        jobs.append({"range": [start, stop], "receipt": job["receipt"].name,
                     "receipt_sha256": digest, "status": status, "pid": pid})
    previous = read_json(args.run_directory / "launch.json")
    launch_history = previous.get("launch_history", [])
    if previous.get("launched"):
        event = {"launched": previous["launched"], "recorded_at": previous.get("updated_at")}
        if event not in launch_history:
            launch_history.append(event)
    if launched:
        launch_history.append({"launched": launched, "recorded_at": timestamp()})
    manifest = {"schema": "rank-seven-order-eight-typed-diagonal-launch-v1",
                "scope": [0, TOTAL_ROWS], "chunk_rows": args.chunk_rows,
                "workers_per_segment": args.workers, "search": search,
                "census_cache": str(args.census_cache), "jobs": jobs,
                "launched": launched, "launch_history": launch_history,
                "updated_at": timestamp()}
    atomic_json(args.run_directory / "launch.json", manifest)
    atomic_json(args.run_directory / "initial-receipts.json", {
        "schema": "rank-seven-order-eight-typed-diagonal-initial-receipts-v1",
        "receipts": [{"range": row["range"], "receipt": row["receipt"],
                      "sha256": row["receipt_sha256"]}
                     for row in jobs if row["receipt_sha256"] is not None],
        "recorded_at": timestamp(),
    })
    for row in jobs:
        suffix = f" pid={row['pid']}" if row["pid"] is not None else ""
        print(f"segment={segment_name(*row['range'])} status={row['status']}{suffix}")
    return 0


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    launch_parser = subparsers.add_parser("launch")
    launch_parser.add_argument("--chunk-rows", type=int, default=25000)
    launch_parser.add_argument("--workers", type=int, default=8)
    launch_parser.add_argument("--passes", type=int, default=3)
    launch_parser.add_argument("--max-denominator", type=int, default=8)
    launch_parser.add_argument("--maximum", type=int, default=4)
    launch_parser.add_argument("--census-cache", type=Path,
                               default=HERE / "rank7_order8_rational_search_cache.r7o8c.xz")
    launch_parser.add_argument("--receipt-directory", type=Path, default=RECEIPT_DIRECTORY)
    launch_parser.add_argument("--run-directory", type=Path, default=RUN_DIRECTORY)
    worker_parser = subparsers.add_parser("worker")
    worker_parser.add_argument("--start", type=int, required=True)
    worker_parser.add_argument("--stop", type=int, required=True)
    worker_parser.add_argument("--workers", type=int, required=True)
    worker_parser.add_argument("--passes", type=int, required=True)
    worker_parser.add_argument("--max-denominator", type=int, required=True)
    worker_parser.add_argument("--maximum", type=int, required=True)
    worker_parser.add_argument("--census-cache", type=Path, required=True)
    worker_parser.add_argument("--receipt-directory", type=Path, required=True)
    worker_parser.add_argument("--run-directory", type=Path, required=True)
    worker_parser.add_argument("--token", required=True)
    args = parser.parse_args()
    return launch(args) if args.command == "launch" else worker(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        sys.stderr.write(f"typed-diagonal scheduler: FAIL CLOSED: {error}\n")
        raise SystemExit(1)
