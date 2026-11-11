#!/usr/bin/env python3
"""Reproduce the canonical 19-profile B7-l3 root-cardinality scout."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

import m6_b7_l3_profile_root_cardinality as producer

SOLVER_SHA256 = "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292"
OPTIONS = ("--restart=false", "--phase=false", "--seed=3")


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=30)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    solver = args.solver.resolve(strict=True)
    if identity(solver)[1] != SOLVER_SHA256:
        parser.error("solver identity differs")
    profiles = producer.load_profiles()
    manifest = producer.manifest_payload(profiles)
    rows = []
    with tempfile.TemporaryDirectory(prefix="b7-l3-root-scout-", dir=producer.HERE.parent) as directory:
        path = Path(directory) / "profile.cnf"
        for position, profile in enumerate(profiles):
            producer.write_cnf(path, position, profile, *producer.build(profile), manifest)
            start = time.monotonic_ns()
            result = subprocess.run(["timeout", str(args.seconds), str(solver), "-q", *OPTIONS, str(path)],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            elapsed = time.monotonic_ns() - start
            status = {10: "SAT", 20: "UNSAT", 124: "TIMEOUT"}.get(result.returncode)
            if status is None:
                raise RuntimeError(f"unexpected solver exit {result.returncode}")
            size, digest = identity(path)
            rows.append({"position": position, "key": profile[0], "cnf_bytes": size,
                         "cnf_sha256": digest, "status": status, "nanoseconds": elapsed})
            print(f"PASS {position + 1:02d}/19 profile={profile[0]} status={status}", flush=True)
    payload = {"schema": f"{producer.PREFIX}-scout-v1", "seconds_per_profile": args.seconds,
               "solver_bytes": identity(solver)[0], "solver_sha256": SOLVER_SHA256,
               "solver_version": "1.7.3", "solver_options": list(OPTIONS), "profiles": 19,
               "unsat": sum(row["status"] == "UNSAT" for row in rows),
               "sat": sum(row["status"] == "SAT" for row in rows),
               "timeout": sum(row["status"] == "TIMEOUT" for row in rows), "rows": rows}
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="ascii", newline="\n")


if __name__ == "__main__":
    main()
