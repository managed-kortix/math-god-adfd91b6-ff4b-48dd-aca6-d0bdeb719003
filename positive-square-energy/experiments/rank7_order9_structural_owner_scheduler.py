#!/usr/bin/env python3
"""Durable per-census-chunk scheduler for the order-nine owner scan."""

from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path


HERE = Path(__file__).resolve().parent
ENGINE = HERE / "rank7_order9_structural_owners.py"
DEFAULT_MANIFEST = HERE / "rank7_order9_exact_residual_census_manifest.json"
DEFAULT_OUTPUT = HERE / "rank7_order9_structural_owner_manifest.json"
RUN_DIRECTORY = HERE / "rank7_order9_structural_owner_scheduler"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def atomic_json(path, payload):
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n",
                         encoding="ascii")
    temporary.replace(path)


def prepare(run_directory):
    run_directory.mkdir(exist_ok=True)
    for name in ("locks", "logs", "pids", "results", "state"):
        (run_directory / name).mkdir(exist_ok=True)


def paths(run_directory, chunk_index):
    name = f"chunk-{chunk_index:02d}"
    return {
        "name": name,
        "result": run_directory / "results" / f"{name}.json",
        "state": run_directory / "state" / f"{name}.json",
        "lock": run_directory / "locks" / f"{name}.lock",
        "log": run_directory / "logs" / f"{name}.log",
        "pid": run_directory / "pids" / f"{name}.pid",
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
    payload = read_json(path)
    if type(payload.get("pid")) is int and process_alive(payload["pid"]):
        return True
    path.unlink(missing_ok=True)
    return False


def reserve(path, chunk_index):
    token = uuid.uuid4().hex
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        return None
    with os.fdopen(descriptor, "w", encoding="ascii") as stream:
        json.dump({"status": "reserved", "pid": os.getpid(), "chunk_index": chunk_index,
                   "token": token, "created_at": timestamp()}, stream, sort_keys=True)
        stream.write("\n")
    return token


def claim(path, chunk_index, token):
    payload = read_json(path)
    if payload.get("status") != "reserved" or payload.get("token") != token:
        return False
    atomic_json(path, {"status": "running", "pid": os.getpid(),
                       "chunk_index": chunk_index, "started_at": timestamp()})
    return True


def manifest_chunks(path):
    payload = json.loads(path.read_text(encoding="ascii"))
    chunks = payload.get("chunks")
    require(type(chunks) is list and chunks, "manifest has no chunks")
    return chunks


def worker(args):
    prepare(args.run_directory)
    item = paths(args.run_directory, args.chunk_index)
    if not claim(item["lock"], args.chunk_index, args.token):
        print(f"chunk={args.chunk_index} claim failed", flush=True)
        return 1
    try:
        atomic_json(item["state"], {"status": "running", "pid": os.getpid(),
                                    "chunk_index": args.chunk_index,
                                    "updated_at": timestamp()})
        command = [sys.executable, "-u", str(ENGINE), "chunk",
                   "--manifest", str(args.manifest), "--chunk-index", str(args.chunk_index),
                   "--output", str(item["result"]), "--progress"]
        with item["log"].open("a", encoding="utf-8") as stream:
            stream.write(f"[{timestamp()}] exec: {' '.join(command)}\n")
            stream.flush()
            completed = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=stream,
                                       stderr=subprocess.STDOUT, check=False)
            stream.write(f"[{timestamp()}] exit: {completed.returncode}\n")
        require(completed.returncode == 0, f"scan exited {completed.returncode}")
        result = read_json(item["result"])
        require(result.get("chunk_index") == args.chunk_index,
                "worker result has wrong chunk identity")
        state = {"status": "completed", "chunk_index": args.chunk_index,
                 "scanned_residual_total": result["scanned_residual_total"],
                 "remainder_orbit_total": result["remainder_orbit_total"],
                 "completed_at": timestamp()}
        atomic_json(item["state"], state)
        print(f"chunk={args.chunk_index} completed", flush=True)
        return 0
    except Exception as error:
        atomic_json(item["state"], {"status": "failed", "pid": os.getpid(),
                                    "chunk_index": args.chunk_index, "error": str(error),
                                    "updated_at": timestamp()})
        print(f"chunk={args.chunk_index} failed: {error}", flush=True)
        return 1
    finally:
        item["lock"].unlink(missing_ok=True)


def launch(args):
    chunks = manifest_chunks(args.manifest)
    prepare(args.run_directory)
    launched = []
    skipped = []
    for chunk_index in range(len(chunks)):
        item = paths(args.run_directory, chunk_index)
        if active_lock(item["lock"]):
            skipped.append((chunk_index, "active"))
            continue
        result = read_json(item["result"])
        if result.get("chunk_index") == chunk_index:
            skipped.append((chunk_index, "completed"))
            continue
        token = reserve(item["lock"], chunk_index)
        if token is None:
            skipped.append((chunk_index, "active"))
            continue
        command = [sys.executable, "-u", str(Path(__file__).resolve()), "worker",
                   "--manifest", str(args.manifest), "--run-directory",
                   str(args.run_directory), "--chunk-index", str(chunk_index),
                   "--token", token]
        stream = item["log"].open("a", encoding="utf-8")
        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=stream,
                                   stderr=subprocess.STDOUT, start_new_session=True)
        stream.close()
        item["pid"].write_text(f"{process.pid}\n", encoding="ascii")
        launched.append((chunk_index, process.pid))
    payload = {
        "schema": "rank-seven-order-nine-structural-owner-scheduler-v1",
        "manifest": str(args.manifest), "run_directory": str(args.run_directory),
        "chunk_total": len(chunks),
        "launched": [{"chunk_index": index, "pid": pid} for index, pid in launched],
        "skipped": [{"chunk_index": index, "reason": reason}
                    for index, reason in skipped],
        "launched_at": timestamp(),
    }
    atomic_json(args.run_directory / "last-launch.json", payload)
    for index, pid in launched:
        print(f"launched chunk={index} pid={pid}")
    for index, reason in skipped:
        print(f"skipped chunk={index} reason={reason}")
    return 0


def aggregate(args):
    chunks = manifest_chunks(args.manifest)
    reports = [paths(args.run_directory, index)["result"] for index in range(len(chunks))]
    require(all(path.is_file() for path in reports), "not all chunk scans are complete")
    command = [sys.executable, "-u", str(ENGINE), "aggregate", "--manifest",
               str(args.manifest), "--output", str(args.output), *map(str, reports)]
    return subprocess.run(command, check=False).returncode


def status(args):
    chunks = manifest_chunks(args.manifest)
    counts = {"completed": 0, "running": 0, "failed": 0, "pending": 0}
    for index in range(len(chunks)):
        item = paths(args.run_directory, index)
        state = read_json(item["state"])
        if read_json(item["result"]).get("chunk_index") == index:
            value = "completed"
        elif active_lock(item["lock"]):
            value = "running"
        elif state.get("status") == "failed":
            value = "failed"
        else:
            value = "pending"
        counts[value] += 1
        print(f"chunk={index} status={value}")
    print(" ".join(f"{key}={value}" for key, value in counts.items()))
    return 0


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("launch", "status", "aggregate"):
        child = subparsers.add_parser(name)
        child.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
        child.add_argument("--run-directory", type=Path, default=RUN_DIRECTORY)
        if name == "aggregate":
            child.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    worker_parser = subparsers.add_parser("worker")
    worker_parser.add_argument("--manifest", required=True, type=Path)
    worker_parser.add_argument("--run-directory", required=True, type=Path)
    worker_parser.add_argument("--chunk-index", required=True, type=int)
    worker_parser.add_argument("--token", required=True)
    args = parser.parse_args()
    return {"launch": launch, "status": status, "aggregate": aggregate,
            "worker": worker}[args.command](args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        sys.stderr.write(f"order-nine structural owner scheduler: FAIL CLOSED: {error}\n")
        raise SystemExit(1)
