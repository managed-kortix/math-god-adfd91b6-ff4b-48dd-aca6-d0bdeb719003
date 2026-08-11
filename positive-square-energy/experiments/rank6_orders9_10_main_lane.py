#!/usr/bin/env python3
"""Build and audit the strict order-nine and order-ten search-pack manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ORDERS = {
    9: {
        "auditor": HERE / "rank6_order9_pack_auditor.py",
        "directory": HERE / "rank6_order9_search_ckpt",
        "extension": "r9g.xz",
        "manifest": HERE / "rank6_order9_search_manifest.json",
        "replay_option": "--write-chunk-receipt",
        "replay_directory": HERE / "rank6_order9_chunk_replays",
    },
    10: {
        "auditor": HERE / "rank6_order10_pack_auditor.py",
        "directory": HERE / "rank6_order10_search_ckpt",
        "extension": "r10g.xz",
        "manifest": HERE / "rank6_order10_search_manifest.json",
        "replay_option": "--write-chunk-transcript",
        "replay_directory": HERE / "rank6_order10_chunk_replays",
    },
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def strict_json(raw, label):
    def object_pairs(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    def reject_constant(value):
        raise RuntimeError(f"nonstandard constant in {label}: {value}")

    try:
        return json.loads(raw.decode("ascii"), object_pairs_hook=object_pairs,
                          parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{label} is not strict ASCII JSON") from error


def discover_chunks(order, configuration):
    directory = configuration["directory"]
    extension = configuration["extension"]
    require(directory.is_dir(), f"order {order} chunk directory is missing")
    pattern = re.compile(rf"chunk-(\d+)-(\d+)\.{re.escape(extension)}")
    candidates = []
    for path in sorted(directory.glob(f"chunk-*.{extension}"), key=lambda item: item.name):
        require(path.is_file(), f"order {order} candidate is not a file: {path}")
        match = pattern.fullmatch(path.name)
        require(match is not None, f"order {order} malformed chunk name: {path.name}")
        start, stop = (int(value) for value in match.groups())
        require(start < stop, f"order {order} empty or reversed chunk: {path.name}")
        candidates.append((start, stop, path.resolve()))
    require(candidates, f"order {order} has no completed chunks")
    candidates.sort(key=lambda item: (item[0], item[1], item[2].as_posix()))
    previous_stop = None
    for start, stop, path in candidates:
        if previous_stop is not None:
            require(start >= previous_stop,
                    f"order {order} overlapping completed chunks at {path.name}")
        previous_stop = stop
    return candidates


def contiguous_prefix(chunks):
    prefix = []
    cursor = 0
    for chunk in chunks:
        start, stop, _ = chunk
        if start != cursor:
            break
        prefix.append(chunk)
        cursor = stop
    require(prefix, "completed chunks do not begin at residual zero")
    return prefix


def run_checked(command, label, expected_returncodes=(0,)):
    completed = subprocess.run(command, check=False, capture_output=True)
    require(completed.returncode in expected_returncodes,
            f"{label} exited {completed.returncode}: "
            f"{completed.stderr.decode('utf-8', errors='replace').strip()}")
    require(completed.stderr == b"", f"{label} wrote to stderr")
    return completed.stdout


def build_and_digest_audit(order, configuration, chunks):
    auditor = configuration["auditor"].resolve()
    manifest = configuration["manifest"].resolve()
    require(auditor.is_file(), f"order {order} auditor is missing")
    require(manifest.parent.is_dir(), f"order {order} manifest parent is missing")
    temporary = manifest.with_name(manifest.name + ".main-lane.tmp")
    temporary.unlink(missing_ok=True)
    build_command = [
        sys.executable, str(auditor), "--manifest", str(temporary),
        "--build-manifest", *(str(path) for _, _, path in chunks),
    ]
    try:
        run_checked(build_command, f"order {order} manifest build")
        manifest_raw = temporary.read_bytes()
        manifest_payload = strict_json(manifest_raw, f"order {order} manifest")
        require(manifest_raw == canonical_bytes(manifest_payload),
                f"order {order} manifest is not canonical JSON")
        digest_command = [
            sys.executable, str(auditor), "--manifest", str(temporary), "--digest-only",
        ]
        audit_raw = run_checked(
            digest_command, f"order {order} digest audit", expected_returncodes=(1,))
        audit_report = strict_json(audit_raw, f"order {order} digest audit report")
        require(audit_raw == canonical_bytes(audit_report),
                f"order {order} digest audit report is not canonical JSON")
        require(audit_report.get("exact_audit") is False,
                f"order {order} digest audit did not identify its scope")
        require(audit_report.get("manifest_covered_residual_range") ==
                manifest_payload.get("covered_residual_range"),
                f"order {order} digest audit coverage changed")
        os.replace(temporary, manifest)
    finally:
        if temporary.exists():
            temporary.unlink()
    return manifest_payload, audit_report, hashlib.sha256(manifest_raw).hexdigest()


def missing_intervals(chunks, residual_total):
    intervals = []
    cursor = 0
    for start, stop, _ in chunks:
        require(0 <= start < stop <= residual_total, "chunk range exceeds residual census")
        if cursor < start:
            intervals.append([cursor, start])
        cursor = stop
    if cursor < residual_total:
        intervals.append([cursor, residual_total])
    return intervals


def replay_commands(order, configuration, manifest_payload):
    commands = []
    replay_directory = configuration["replay_directory"].resolve()
    replay_directory.mkdir(exist_ok=True)
    auditor = configuration["auditor"].resolve()
    manifest = configuration["manifest"].resolve()
    for index, chunk in enumerate(manifest_payload["chunks"]):
        start, stop = chunk["residual_range"]
        output = replay_directory / f"chunk-{start:05d}-{stop:05d}.json"
        argv = [
            sys.executable, str(auditor), "--manifest", str(manifest),
            "--chunk-index", str(index), configuration["replay_option"], str(output),
        ]
        commands.append({
            "chunk_index": index,
            "residual_range": [start, stop],
            "command": shlex.join(argv),
            "output": str(output),
        })
    return replay_directory, commands


def execute_replays(order, replay_directory, commands):
    replay_directory.mkdir(exist_ok=True)
    for record in commands:
        output = Path(record["output"])
        require(not output.exists(),
                f"order {order} refusing to replace replay output: {output}")
        run_checked(shlex.split(record["command"]),
                    f"order {order} chunk {record['chunk_index']} exact replay")


def process_order(order, execute):
    configuration = ORDERS[order]
    discovered = discover_chunks(order, configuration)
    chunks = contiguous_prefix(discovered)
    manifest, audit, manifest_sha256 = build_and_digest_audit(order, configuration, chunks)
    require(manifest.get("chunks") and len(manifest["chunks"]) == len(chunks),
            f"order {order} manifest omitted a discovered chunk")
    require([chunk["residual_range"] for chunk in manifest["chunks"]] ==
            [[start, stop] for start, stop, _ in chunks],
            f"order {order} embedded chunk ranges differ from filenames")
    residual_total = manifest["residual_total"]
    missing = missing_intervals(discovered, residual_total)
    replay_directory, commands = replay_commands(order, configuration, manifest)
    if execute:
        execute_replays(order, replay_directory, commands)
    return {
        "order": order,
        "manifest": str(configuration["manifest"].resolve()),
        "manifest_sha256": manifest_sha256,
        "digest_audit": "passed",
        "residual_total": residual_total,
        "covered_residual_range": manifest["covered_residual_range"],
        "missing_intervals": missing,
        "discovered_chunks": len(discovered),
        "chunks": len(chunks),
        "replay_mode": "executed" if execute else "scheduled",
        "replay_directory": str(replay_directory),
        "replay_commands": commands,
        "digest_audit_report": audit,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", choices=("9", "10", "both"), default="both")
    parser.add_argument("--execute-replays", action="store_true",
                        help="run every scheduled exact chunk replay sequentially")
    args = parser.parse_args()
    selected = (9, 10) if args.order == "both" else (int(args.order),)
    report = {
        "schema": "rank-six-orders9-10-main-lane-v1",
        "orders": [process_order(order, args.execute_replays) for order in selected],
    }
    sys.stdout.write(canonical_bytes(report).decode("ascii"))


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, TypeError, ValueError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
