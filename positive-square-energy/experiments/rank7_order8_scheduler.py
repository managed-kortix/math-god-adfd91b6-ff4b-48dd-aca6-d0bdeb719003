#!/usr/bin/env python3
"""Durable launcher for exact rank-seven/order-eight witness shards."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path


HERE = Path(__file__).resolve().parent
ENGINE = HERE / "rank7_order8_exact_rational.py"
DEFAULT_CACHE = HERE / "rank7_order8_rational_search_cache.r7o8c.xz"
RUN_DIRECTORY = HERE / "rank7_order8_scheduler"
LEGACY_FRAGMENT_DIRECTORY = HERE / "rank7_order8_chunk_005000_010000.r7o8g.xz.fragments"
TOTAL_ROWS = 492812
FRAGMENT_PATTERN = re.compile(r"fragment-(\d+)-(\d+)\.r7o8g\.xz\Z")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def atomic_json(path, payload):
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="ascii")
    temporary.replace(path)


def shard_name(start, stop):
    return f"{start:06d}_{stop:06d}"


def shard_paths(run_directory, start, stop):
    name = shard_name(start, stop)
    output = HERE / f"rank7_order8_chunk_{name}.r7o8g.xz"
    return {
        "name": name,
        "output": output,
        "fragments": output.with_name(output.name + ".fragments"),
        "log": run_directory / "logs" / f"shard-{name}.log",
        "lock": run_directory / "locks" / f"shard-{name}.lock",
        "state": run_directory / "state" / f"shard-{name}.json",
        "result": run_directory / "results" / f"shard-{name}.json",
        "pid": run_directory / "pids" / f"shard-{name}.pid",
    }


def prepare_directories(run_directory):
    run_directory.mkdir(exist_ok=True)
    for name in ("locks", "logs", "pids", "results", "state"):
        (run_directory / name).mkdir(exist_ok=True)


def process_alive(pid):
    try:
        os.kill(pid, 0)
    except (OSError, ValueError):
        return False
    return True


def read_lock(path):
    try:
        return json.loads(path.read_text(encoding="ascii"))
    except (OSError, ValueError, TypeError):
        return {}


def active_lock(path):
    if not path.exists():
        return False
    payload = read_lock(path)
    pid = payload.get("pid")
    if type(pid) is int and process_alive(pid):
        return True
    path.unlink(missing_ok=True)
    return False


def claim(path, start, stop, token=None):
    if token is not None and path.exists():
        reserved = read_lock(path)
        if reserved.get("token") == token and reserved.get("status") == "reserved":
            atomic_json(path, {"pid": os.getpid(), "range": [start, stop],
                               "status": "running", "claimed_at": timestamp()})
            return True
    payload = json.dumps({"pid": os.getpid(), "range": [start, stop], "claimed_at": timestamp()},
                         sort_keys=True) + "\n"
    while True:
        try:
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        except FileExistsError:
            if active_lock(path):
                return False
            continue
        with os.fdopen(descriptor, "w", encoding="ascii") as stream:
            stream.write(payload)
        return True


def run_logged(command, log_path):
    with log_path.open("a", encoding="utf-8") as stream:
        stream.write(f"[{timestamp()}] exec: {' '.join(map(str, command))}\n")
        stream.flush()
        completed = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=stream,
                                   stderr=subprocess.STDOUT, check=False)
        stream.write(f"[{timestamp()}] exit: {completed.returncode}\n")
        stream.flush()
    require(completed.returncode == 0, f"command failed with exit status {completed.returncode}")


def prepare_cache(cache, run_directory):
    if cache.is_file():
        return
    require(cache.parent.is_dir(), "cache parent does not exist")
    baseline = HERE / "rank7_order8_chunk_000000_005000.r7o8g.xz"
    log = run_directory / "cache.log"
    run_logged([sys.executable, "-u", str(ENGINE), "--verify-pack", str(baseline),
                "--census-cache", str(cache)], log)
    require(cache.is_file(), "engine did not persist the census cache")


def adopt_legacy_fragments(destination, start, stop):
    destination.mkdir(exist_ok=True)
    if not LEGACY_FRAGMENT_DIRECTORY.is_dir():
        return 0
    adopted = 0
    for source in sorted(LEGACY_FRAGMENT_DIRECTORY.glob("fragment-*.r7o8g.xz")):
        match = FRAGMENT_PATTERN.fullmatch(source.name)
        if match is None:
            continue
        fragment_start, fragment_stop = map(int, match.groups())
        if fragment_start < start or fragment_stop > stop:
            continue
        target = destination / source.name
        if target.exists():
            require(target.read_bytes() == source.read_bytes(),
                    f"conflicting fragment already exists: {target.name}")
            continue
        try:
            os.link(source, target)
        except OSError:
            shutil.copy2(source, target)
        adopted += 1
    return adopted


def worker(args):
    prepare_directories(args.run_directory)
    paths = shard_paths(args.run_directory, args.start, args.stop)
    if not claim(paths["lock"], args.start, args.stop, args.token):
        print(f"active shard retained: {paths['name']}", flush=True)
        return 0
    try:
        atomic_json(paths["state"], {"status": "running", "pid": os.getpid(),
                                     "range": [args.start, args.stop], "updated_at": timestamp()})
        adopted = adopt_legacy_fragments(paths["fragments"], args.start, args.stop)
        print(f"[{timestamp()}] shard={paths['name']} adopted_fragments={adopted}", flush=True)
        run_logged([
            sys.executable, "-u", str(ENGINE),
            "--output", str(paths["output"]),
            "--fragment-directory", str(paths["fragments"]),
            "--census-cache", str(args.cache),
            "--start", str(args.start), "--count", str(args.stop - args.start),
            "--checkpoint-rows", str(args.checkpoint_rows), "--progress",
        ], paths["log"])
        run_logged([sys.executable, "-u", str(ENGINE), "--verify-pack", str(paths["output"]),
                    "--census-cache", str(args.cache)], paths["log"])
        digest = hashlib.sha256(paths["output"].read_bytes()).hexdigest()
        result = {"schema": "rank-seven-order-eight-shard-result-v1", "status": "completed",
                  "range": [args.start, args.stop], "rows": args.stop - args.start,
                  "output": paths["output"].name, "output_sha256": digest,
                  "exact_audit": True, "completed_at": timestamp()}
        atomic_json(paths["result"], result)
        atomic_json(paths["state"], result)
        print(f"[{timestamp()}] shard={paths['name']} exact_audit=true sha256={digest}", flush=True)
        return 0
    except Exception as error:
        atomic_json(paths["state"], {"status": "failed", "pid": os.getpid(),
                                     "range": [args.start, args.stop], "error": str(error),
                                     "updated_at": timestamp()})
        print(f"[{timestamp()}] shard={paths['name']} failed: {error}", flush=True)
        return 1
    finally:
        paths["lock"].unlink(missing_ok=True)


def launch(args):
    require(0 <= args.start < args.stop <= TOTAL_ROWS, "invalid launch range")
    require(args.shard_rows > 0 and args.checkpoint_rows > 0, "row widths must be positive")
    require((args.stop - args.start) % args.shard_rows == 0,
            "launch range must be an exact number of shards")
    prepare_directories(args.run_directory)
    prepare_cache(args.cache, args.run_directory)
    launched = []
    skipped = []
    for start in range(args.start, args.stop, args.shard_rows):
        stop = min(start + args.shard_rows, args.stop)
        paths = shard_paths(args.run_directory, start, stop)
        if active_lock(paths["lock"]):
            skipped.append((paths["name"], "active"))
            continue
        if paths["result"].is_file() and paths["output"].is_file():
            skipped.append((paths["name"], "completed"))
            continue
        token = uuid.uuid4().hex
        try:
            descriptor = os.open(paths["lock"], os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        except FileExistsError:
            skipped.append((paths["name"], "active"))
            continue
        with os.fdopen(descriptor, "w", encoding="ascii") as lock_stream:
            json.dump({"pid": os.getpid(), "range": [start, stop], "status": "reserved",
                       "token": token, "claimed_at": timestamp()}, lock_stream, sort_keys=True)
            lock_stream.write("\n")
        command = [sys.executable, "-u", str(Path(__file__).resolve()), "worker",
                   "--start", str(start), "--stop", str(stop),
                   "--checkpoint-rows", str(args.checkpoint_rows),
                   "--cache", str(args.cache), "--run-directory", str(args.run_directory),
                   "--token", token]
        stream = paths["log"].open("a", encoding="utf-8")
        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=stream,
                                   stderr=subprocess.STDOUT, start_new_session=True)
        stream.close()
        paths["pid"].write_text(f"{process.pid}\n", encoding="ascii")
        launched.append((paths["name"], process.pid))
    manifest = {"schema": "rank-seven-order-eight-scheduler-launch-v1",
                "range": [args.start, args.stop], "shard_rows": args.shard_rows,
                "checkpoint_rows": args.checkpoint_rows, "cache": str(args.cache),
                "launched": [{"shard": name, "pid": pid} for name, pid in launched],
                "skipped": [{"shard": name, "reason": reason} for name, reason in skipped],
                "launched_at": timestamp()}
    atomic_json(args.run_directory / "last-launch.json", manifest)
    for name, pid in launched:
        print(f"launched shard={name} pid={pid}")
    for name, reason in skipped:
        print(f"skipped shard={name} reason={reason}")
    return 0


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    launch_parser = subparsers.add_parser("launch")
    launch_parser.add_argument("--start", type=int, default=5000)
    launch_parser.add_argument("--stop", type=int, default=9000)
    launch_parser.add_argument("--shard-rows", type=int, default=1000)
    launch_parser.add_argument("--checkpoint-rows", type=int, default=500)
    launch_parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    launch_parser.add_argument("--run-directory", type=Path, default=RUN_DIRECTORY)
    worker_parser = subparsers.add_parser("worker")
    worker_parser.add_argument("--start", type=int, required=True)
    worker_parser.add_argument("--stop", type=int, required=True)
    worker_parser.add_argument("--checkpoint-rows", type=int, default=500)
    worker_parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    worker_parser.add_argument("--run-directory", type=Path, default=RUN_DIRECTORY)
    worker_parser.add_argument("--token")
    args = parser.parse_args()
    return launch(args) if args.command == "launch" else worker(args)


if __name__ == "__main__":
    raise SystemExit(main())
