#!/usr/bin/env python3
"""Durable four-way structural-owner scan of the order-twelve census.

Each census chunk is one independently resumable job.  A worker streams its
compressed chunk once, writes an atomic summary after every row segment, and
resumes at the first uncommitted segment after interruption.  The finalizer
aggregates those summaries without reopening the residual streams.  Owner
decisions are exact and payload-free: balanced rank one, signed imbalance,
symbolic atoms, then the generalized switched three-ray search.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import uuid
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
OWNER_ENGINE = HERE / "rank7_order12_structural_owners.py"
RUN_DIRECTORY = HERE / "rank7_order12_segmented_owner_scan"
DEFAULT_MANIFEST = HERE / "rank7_order12_exact_owner_remainder_manifest.json"
CHUNK_PATTERN = re.compile(r"rank7_order12_census_(\d{3})_(\d{3})\.json\.xz\Z")
DEFAULT_CHUNKS = tuple(
    HERE / f"rank7_order12_census_{start:03d}_{stop:03d}.json.xz"
    for start, stop in ((0, 92), (92, 183), (183, 274), (274, 365))
)
SCHEMA = "rank-seven-order-twelve-segmented-owner-scan-v1"
SEGMENT_SCHEMA = "rank-seven-order-twelve-owner-segment-v1"
LANES = ("balanced-rank-one", "signed-imbalance-psd", "simplex-mixed-atom",
         "generalized-three-ray")
MANIFEST_SCHEMA = "rank-seven-order-twelve-exact-owner-remainder-manifest-v1"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def atomic_json(path, payload, canonical=False):
    require(path.parent.is_dir(), f"output parent does not exist: {path.parent}")
    temporary = path.with_name(path.name + ".tmp")
    raw = canonical_bytes(payload) if canonical else (
        json.dumps(payload, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("ascii")
    with temporary.open("wb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def load_json(path):
    return json.loads(path.read_text(encoding="ascii"))


def load_owner_engine():
    spec = importlib.util.spec_from_file_location("rank7_order12_segmented_owner_core",
                                                  OWNER_ENGINE)
    require(spec is not None and spec.loader is not None, "cannot load owner engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def chunk_id(path):
    match = CHUNK_PATTERN.fullmatch(path.name)
    require(match is not None, f"noncanonical order-twelve chunk name: {path.name}")
    return f"{match.group(1)}_{match.group(2)}", [int(value) for value in match.groups()]


def prepare_directories(run_directory):
    run_directory.mkdir(exist_ok=True)
    for name in ("locks", "logs", "pids", "results", "segments", "state"):
        (run_directory / name).mkdir(exist_ok=True)


def job_paths(run_directory, identifier):
    return {
        "lock": run_directory / "locks" / f"chunk-{identifier}.lock",
        "log": run_directory / "logs" / f"chunk-{identifier}.log",
        "pid": run_directory / "pids" / f"chunk-{identifier}.pid",
        "result": run_directory / "results" / f"chunk-{identifier}.json",
        "segments": run_directory / "segments" / identifier,
        "state": run_directory / "state" / f"chunk-{identifier}.json",
    }


def process_alive(pid):
    try:
        os.kill(pid, 0)
    except (OSError, ValueError):
        return False
    return True


def active_lock(path):
    if not path.exists():
        return False
    try:
        payload = load_json(path)
    except (OSError, ValueError, TypeError):
        payload = {}
    pid = payload.get("pid")
    if type(pid) is int and process_alive(pid):
        return True
    path.unlink(missing_ok=True)
    return False


def reserve(path, kernel_range, token):
    payload = canonical_bytes({"claimed_at": timestamp(), "pid": os.getpid(),
                               "range": kernel_range, "status": "reserved",
                               "token": token})
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        return False
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(payload)
    return True


def claim(path, kernel_range, token):
    if path.exists():
        try:
            reserved = load_json(path)
        except (OSError, ValueError, TypeError):
            reserved = {}
        if reserved.get("status") == "reserved" and reserved.get("token") == token:
            atomic_json(path, {"claimed_at": timestamp(), "pid": os.getpid(),
                               "range": kernel_range, "status": "running"}, canonical=True)
            return True
    if active_lock(path):
        return False
    return reserve(path, kernel_range, token)


def recognize_exact(owner, atom, edges, row):
    if owner.balanced_rank_one(edges, row):
        return "balanced-rank-one", None
    imbalance = owner.signed_imbalance_certificate(edges, row)
    if imbalance is not None:
        return "signed-imbalance-psd", [imbalance[0], imbalance[1].numerator,
                                         imbalance[1].denominator]
    records = (() if not owner.atom_profile_candidate(edges, row) else
               tuple(record for record in atom.recognize(edges, row)
                     if record["status"] == "exact-equality-owner"))
    if records:
        profiles = sorted({(record["profile"]["mixed"],
                            tuple(record["profile"]["simplex_widths"]))
                           for record in records})
        return "simplex-mixed-atom", [[mixed, list(widths)]
                                       for mixed, widths in profiles]
    witness = owner.generalized_three_ray_witness(edges, row)
    if witness is not None:
        cost = owner.three_ray_witness_cost(edges, row, witness)
        require(cost is not None and cost <= 108, "generalized three-ray witness changed")
        return "generalized-three-ray", [cost, list(witness)]
    return None, None


def segment_path(paths, start, stop):
    return paths["segments"] / f"rows-{start:07d}-{stop:07d}.json"


def validate_segment(payload, identity, expected_start=None):
    require(payload.get("schema") == SEGMENT_SCHEMA, "wrong segment schema")
    require(payload.get("identity") == identity, "segment input identity changed")
    start, stop = payload["row_range"]
    require(type(start) is int and type(stop) is int and start < stop,
            "bad segment row range")
    if expected_start is not None:
        require(start == expected_start, "segment gap or overlap")
    require(set(payload["exclusive_owner_orbit_counts"]) == set(LANES),
            "segment owner lanes changed")
    owned = sum(payload["exclusive_owner_orbit_counts"].values())
    require(owned + payload["remainder_orbit_total"] == stop - start,
            "segment orbit partition changed")
    return stop


def existing_segments(paths, identity):
    paths["segments"].mkdir(exist_ok=True)
    rows = []
    cursor = 0
    for path in sorted(paths["segments"].glob("rows-*.json")):
        payload = load_json(path)
        cursor = validate_segment(payload, identity, cursor)
        require(path == segment_path(paths, *payload["row_range"]),
                "segment filename does not match payload")
        rows.append(payload)
    return rows, cursor


def aggregate_segments(identity, header, segments, complete):
    orbit_counts = Counter({lane: 0 for lane in LANES})
    physical_counts = Counter({lane: 0 for lane in LANES})
    remainder_orbits = remainder_physical = 0
    cursor = 0
    digest = hashlib.sha256()
    summaries = []
    for segment in segments:
        cursor = validate_segment(segment, identity, cursor)
        orbit_counts.update(segment["exclusive_owner_orbit_counts"])
        physical_counts.update(segment["exclusive_owner_physical_counts"])
        remainder_orbits += segment["remainder_orbit_total"]
        remainder_physical += segment["remainder_physical_total"]
        digest.update(bytes.fromhex(segment["classification_stream_sha256"]))
        summaries.append({key: segment[key] for key in (
            "row_range", "exclusive_owner_orbit_counts",
            "exclusive_owner_physical_counts", "remainder_orbit_total",
            "remainder_physical_total", "classification_stream_sha256")})
    if complete:
        require(cursor == header["coarse_residual_total"], "completed scan is short")
    return {
        "schema": SCHEMA,
        "status": "completed" if complete else "running",
        "full_theorem": False,
        "identity": identity,
        "kernel_range": header["kernel_range"],
        "scanned_orbit_total": cursor,
        "coarse_residual_orbit_total": header["coarse_residual_total"],
        "coarse_residual_physical_total": header["coarse_residual_physical_total"],
        "exclusive_owner_orbit_counts": dict(sorted(orbit_counts.items())),
        "exclusive_owner_physical_counts": dict(sorted(physical_counts.items())),
        "owned_orbit_total": sum(orbit_counts.values()),
        "owned_physical_total": sum(physical_counts.values()),
        "remainder_orbit_total": remainder_orbits,
        "remainder_physical_total": remainder_physical,
        "segment_digest_sha256": digest.hexdigest(),
        "segments": summaries,
        "updated_at": timestamp(),
    }


def worker(args):
    prepare_directories(args.run_directory)
    identifier, kernel_range = chunk_id(args.chunk)
    paths = job_paths(args.run_directory, identifier)
    if not claim(paths["lock"], kernel_range, args.token):
        print(f"active chunk retained: {identifier}", flush=True)
        return 0
    try:
        require(args.checkpoint_rows > 0, "checkpoint size must be positive")
        require(args.chunk.is_file(), f"missing census chunk: {args.chunk}")
        owner = load_owner_engine()
        atom = owner.load_atom_recognizer()
        identity = {"atom_recognizer_sha256": file_sha256(owner.ATOM_RECOGNIZER),
                    "chunk_path": str(args.chunk.resolve()),
                    "chunk_sha256": file_sha256(args.chunk),
                    "owner_engine_sha256": file_sha256(OWNER_ENGINE)}
        segments, resume_at = existing_segments(paths, identity)
        header, records, finish = owner.stream_chunk(args.chunk)
        require(header["kernel_range"] == kernel_range, "chunk range/name mismatch")
        kernels = {row["order_kernel"]: tuple(map(tuple, row["edges"]))
                   for row in header["kernels"]}
        segment_start = resume_at
        local_orbits = Counter({lane: 0 for lane in LANES})
        local_physical = Counter({lane: 0 for lane in LANES})
        local_remainder_orbits = local_remainder_physical = 0
        classification = hashlib.sha256()
        stream_digest = hashlib.sha256()
        record_total = physical_total = 0

        def checkpoint(stop):
            nonlocal segment_start, local_orbits, local_physical
            nonlocal local_remainder_orbits, local_remainder_physical, classification
            if stop == segment_start:
                return
            payload = {
                "schema": SEGMENT_SCHEMA, "identity": identity,
                "row_range": [segment_start, stop],
                "exclusive_owner_orbit_counts": dict(sorted(local_orbits.items())),
                "exclusive_owner_physical_counts": dict(sorted(local_physical.items())),
                "remainder_orbit_total": local_remainder_orbits,
                "remainder_physical_total": local_remainder_physical,
                "classification_stream_sha256": classification.hexdigest(),
                "completed_at": timestamp(),
            }
            atomic_json(segment_path(paths, segment_start, stop), payload, canonical=True)
            segments.append(payload)
            atomic_json(paths["state"], aggregate_segments(identity, header, segments, False))
            print(f"[{timestamp()}] chunk={identifier} checkpoint={stop}/"
                  f"{header['coarse_residual_total']}", flush=True)
            segment_start = stop
            local_orbits = Counter({lane: 0 for lane in LANES})
            local_physical = Counter({lane: 0 for lane in LANES})
            local_remainder_orbits = local_remainder_physical = 0
            classification = hashlib.sha256()

        for index, record in enumerate(records):
            stream_digest.update(owner.canonical_bytes(record))
            orbit_size = record["orbit_size"]
            require(type(orbit_size) is int and orbit_size >= 1, "bad orbit size")
            record_total += 1
            physical_total += orbit_size
            if index < resume_at:
                continue
            edges = kernels[record["order_kernel"]]
            row = tuple(record["row"])
            lane, detail = recognize_exact(owner, atom, edges, row)
            classification.update(canonical_bytes(
                [index, record["global_kernel"], record["order_kernel"],
                 record["row"], orbit_size, lane, detail]))
            if lane is None:
                local_remainder_orbits += 1
                local_remainder_physical += orbit_size
            else:
                local_orbits[lane] += 1
                local_physical[lane] += orbit_size
            if index + 1 - segment_start == args.checkpoint_rows:
                checkpoint(index + 1)
        raw_sha256, artifact_sha256 = finish()
        require(stream_digest.hexdigest() == header["residual_stream_sha256"],
                "residual stream digest mismatch")
        require(record_total == header["coarse_residual_total"] and
                physical_total == header["coarse_residual_physical_total"],
                "census totals changed")
        require(artifact_sha256 == identity["chunk_sha256"], "chunk changed during scan")
        checkpoint(record_total)
        result = aggregate_segments(identity, header, segments, True)
        result.update({"artifact_sha256": artifact_sha256, "raw_sha256": raw_sha256,
                       "completed_at": timestamp()})
        atomic_json(paths["result"], result, canonical=True)
        atomic_json(paths["state"], result)
        print(f"[{timestamp()}] chunk={identifier} completed owned="
              f"{result['owned_orbit_total']} remainder={result['remainder_orbit_total']}",
              flush=True)
        return 0
    except Exception as error:
        atomic_json(paths["state"], {"schema": SCHEMA, "status": "failed",
                                     "chunk": str(args.chunk), "pid": os.getpid(),
                                     "error": str(error), "updated_at": timestamp()})
        print(f"[{timestamp()}] chunk={identifier} failed: {error}", flush=True)
        return 1
    finally:
        paths["lock"].unlink(missing_ok=True)


def launch(args):
    require(args.checkpoint_rows > 0, "checkpoint size must be positive")
    require(len(args.chunks) == 4, "the order-twelve launch requires exactly four chunks")
    prepare_directories(args.run_directory)
    jobs = []
    launched = []
    for chunk in sorted(args.chunks, key=lambda path: chunk_id(path)[1]):
        require(chunk.is_file(), f"missing census chunk: {chunk}")
        identifier, kernel_range = chunk_id(chunk)
        paths = job_paths(args.run_directory, identifier)
        status = "pending"
        pid = None
        if paths["result"].is_file():
            status = "completed"
        elif active_lock(paths["lock"]):
            status = "running"
        else:
            token = uuid.uuid4().hex
            require(reserve(paths["lock"], kernel_range, token),
                    f"could not reserve chunk {identifier}")
            command = [sys.executable, "-u", str(Path(__file__).resolve()), "worker",
                       "--chunk", str(chunk), "--checkpoint-rows", str(args.checkpoint_rows),
                       "--run-directory", str(args.run_directory), "--token", token]
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
    manifest = {"schema": "rank-seven-order-twelve-owner-scheduler-v1",
                "checkpoint_rows": args.checkpoint_rows, "jobs": jobs,
                "launched": launched, "updated_at": timestamp()}
    atomic_json(args.run_directory / "scheduler.json", manifest)
    for row in jobs:
        suffix = f" pid={row['pid']}" if row["pid"] is not None else ""
        print(f"chunk={row['chunk']} status={row['status']}{suffix}")
    return 0


def status(args):
    prepare_directories(args.run_directory)
    rows = []
    for chunk in DEFAULT_CHUNKS:
        identifier, kernel_range = chunk_id(chunk)
        paths = job_paths(args.run_directory, identifier)
        payload = load_json(paths["state"]) if paths["state"].is_file() else {}
        state = payload.get("status", "pending")
        if active_lock(paths["lock"]):
            state = "running"
        rows.append({"chunk": identifier, "kernel_range": kernel_range,
                     "status": state, "scanned_orbit_total": payload.get("scanned_orbit_total", 0),
                     "coarse_residual_orbit_total": payload.get("coarse_residual_orbit_total"),
                     "owned_orbit_total": payload.get("owned_orbit_total", 0)})
    atomic_json(args.run_directory / "status.json",
                {"schema": "rank-seven-order-twelve-owner-scheduler-status-v1",
                 "jobs": rows, "updated_at": timestamp()})
    for row in rows:
        total = row["coarse_residual_orbit_total"]
        progress = f"{row['scanned_orbit_total']}/{total}" if total is not None else "0/?"
        print(f"chunk={row['chunk']} status={row['status']} rows={progress} "
              f"owned={row['owned_orbit_total']}")
    return 0


def finalize(args):
    require(args.output.parent.is_dir(), "output parent does not exist")
    owner = load_owner_engine()
    implementation_identity = (file_sha256(OWNER_ENGINE),
                               file_sha256(owner.ATOM_RECOGNIZER))
    owner_orbits = Counter({lane: 0 for lane in LANES})
    owner_physical = Counter({lane: 0 for lane in LANES})
    coarse_orbits = coarse_physical = remainder_orbits = remainder_physical = 0
    classification_digest = hashlib.sha256()
    chunks = []
    expected_start = 0
    shared_identity = None

    for chunk in DEFAULT_CHUNKS:
        identifier, kernel_range = chunk_id(chunk)
        require(kernel_range[0] == expected_start, "chunk ranges have a gap or overlap")
        expected_start = kernel_range[1]
        paths = job_paths(args.run_directory, identifier)
        require(paths["result"].is_file(), f"segmented scan is incomplete: {identifier}")
        result = load_json(paths["result"])
        require(result.get("schema") == SCHEMA and result.get("status") == "completed",
                f"segmented result is not complete: {identifier}")
        require(result.get("full_theorem") is False, f"theorem boundary changed: {identifier}")
        require(result.get("kernel_range") == kernel_range,
                f"result range changed: {identifier}")
        require(set(result["exclusive_owner_orbit_counts"]) == set(LANES) and
                set(result["exclusive_owner_physical_counts"]) == set(LANES),
                f"owner lanes changed: {identifier}")
        identity = result["identity"]
        current_identity = {
            "atom_recognizer_sha256": implementation_identity[1],
            "chunk_path": str(chunk.resolve()),
            "chunk_sha256": file_sha256(chunk),
            "owner_engine_sha256": implementation_identity[0],
        }
        require(identity == current_identity, f"result input identity changed: {identifier}")
        engine_identity = (identity["owner_engine_sha256"],
                           identity["atom_recognizer_sha256"])
        if shared_identity is None:
            shared_identity = engine_identity
        require(engine_identity == shared_identity, "owner implementation changed between chunks")

        local_orbits = Counter({lane: 0 for lane in LANES})
        local_physical = Counter({lane: 0 for lane in LANES})
        local_remainder_orbits = local_remainder_physical = 0
        segment_cursor = 0
        segment_digest = hashlib.sha256()
        for segment in result["segments"]:
            segment_cursor = validate_segment(
                {**segment, "schema": SEGMENT_SCHEMA, "identity": identity},
                identity, segment_cursor)
            local_orbits.update(segment["exclusive_owner_orbit_counts"])
            local_physical.update(segment["exclusive_owner_physical_counts"])
            local_remainder_orbits += segment["remainder_orbit_total"]
            local_remainder_physical += segment["remainder_physical_total"]
            digest = bytes.fromhex(segment["classification_stream_sha256"])
            require(len(digest) == 32, f"bad segment digest: {identifier}")
            segment_digest.update(digest)
        require(segment_cursor == result["coarse_residual_orbit_total"] ==
                result["scanned_orbit_total"], f"incomplete result stream: {identifier}")
        require(dict(sorted(local_orbits.items())) == result["exclusive_owner_orbit_counts"] and
                dict(sorted(local_physical.items())) ==
                result["exclusive_owner_physical_counts"],
                f"segment owner totals changed: {identifier}")
        require(local_remainder_orbits == result["remainder_orbit_total"] and
                local_remainder_physical == result["remainder_physical_total"],
                f"segment remainder totals changed: {identifier}")
        require(segment_digest.hexdigest() == result["segment_digest_sha256"],
                f"segment digest changed: {identifier}")
        require(result["owned_orbit_total"] + result["remainder_orbit_total"] ==
                result["coarse_residual_orbit_total"] and
                result["owned_physical_total"] + result["remainder_physical_total"] ==
                result["coarse_residual_physical_total"],
                f"owner/remainder partition changed: {identifier}")

        owner_orbits.update(local_orbits)
        owner_physical.update(local_physical)
        coarse_orbits += result["coarse_residual_orbit_total"]
        coarse_physical += result["coarse_residual_physical_total"]
        remainder_orbits += local_remainder_orbits
        remainder_physical += local_remainder_physical
        classification_digest.update(bytes.fromhex(result["segment_digest_sha256"]))
        chunks.append({
            "artifact_sha256": result["artifact_sha256"],
            "coarse_residual_orbit_total": result["coarse_residual_orbit_total"],
            "coarse_residual_physical_total": result["coarse_residual_physical_total"],
            "exclusive_owner_orbit_counts": dict(sorted(local_orbits.items())),
            "exclusive_owner_physical_counts": dict(sorted(local_physical.items())),
            "kernel_range": kernel_range,
            "path": os.path.relpath(chunk, args.output.parent),
            "raw_sha256": result["raw_sha256"],
            "remainder_orbit_total": local_remainder_orbits,
            "remainder_physical_total": local_remainder_physical,
            "result_path": os.path.relpath(paths["result"], args.output.parent),
            "result_sha256": file_sha256(paths["result"]),
            "segment_digest_sha256": result["segment_digest_sha256"],
        })

    require(expected_start == 365, "chunks do not exactly cover all order-twelve kernels")
    owned_orbits = sum(owner_orbits.values())
    owned_physical = sum(owner_physical.values())
    require(owned_orbits + remainder_orbits == coarse_orbits and
            owned_physical + remainder_physical == coarse_physical,
            "aggregate owner/remainder partition changed")
    payload = {
        "schema": MANIFEST_SCHEMA,
        "status": "complete-exact-owner-remainder-aggregation",
        "full_theorem": False,
        "scope": "exact segmented residual owner/remainder aggregation only",
        "rank": 7,
        "order": 12,
        "budget": [6, 1],
        "owner_precedence": list(LANES),
        "owner_engine_sha256": shared_identity[0],
        "atom_recognizer_sha256": shared_identity[1],
        "chunks": chunks,
        "coarse_residual_orbit_total": coarse_orbits,
        "coarse_residual_physical_total": coarse_physical,
        "exclusive_owner_orbit_counts": dict(sorted(owner_orbits.items())),
        "exclusive_owner_physical_counts": dict(sorted(owner_physical.items())),
        "owned_orbit_total": owned_orbits,
        "owned_physical_total": owned_physical,
        "remainder_orbit_total": remainder_orbits,
        "remainder_physical_total": remainder_physical,
        "chunk_classification_digest_sha256": classification_digest.hexdigest(),
    }
    atomic_json(args.output, payload, canonical=True)
    print(f"order-twelve owner/remainder manifest built: owned_orbits={owned_orbits} "
          f"remainder_orbits={remainder_orbits} remainder_physical={remainder_physical}")
    print("full_theorem=false")
    return 0


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    launch_parser = subparsers.add_parser("launch")
    launch_parser.add_argument("chunks", nargs="*", type=Path, default=list(DEFAULT_CHUNKS))
    launch_parser.add_argument("--checkpoint-rows", type=int, default=1000)
    launch_parser.add_argument("--run-directory", type=Path, default=RUN_DIRECTORY)
    worker_parser = subparsers.add_parser("worker")
    worker_parser.add_argument("--chunk", required=True, type=Path)
    worker_parser.add_argument("--checkpoint-rows", type=int, default=1000)
    worker_parser.add_argument("--run-directory", type=Path, default=RUN_DIRECTORY)
    worker_parser.add_argument("--token", required=True)
    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--run-directory", type=Path, default=RUN_DIRECTORY)
    finalize_parser = subparsers.add_parser("finalize")
    finalize_parser.add_argument("--run-directory", type=Path, default=RUN_DIRECTORY)
    finalize_parser.add_argument("--output", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    if args.command == "launch":
        return launch(args)
    if args.command == "worker":
        return worker(args)
    if args.command == "finalize":
        return finalize(args)
    return status(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        sys.stderr.write(f"order-twelve segmented owner scan: FAIL CLOSED: {error}\n")
        raise SystemExit(1)
