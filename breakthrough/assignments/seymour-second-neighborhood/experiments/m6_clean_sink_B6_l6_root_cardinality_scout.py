#!/usr/bin/env python3
"""Reproduce the exact clean B6-l6 root-cardinality scout."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

import m6_clean_sink_B6_l6_root_cardinality as producer

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
    members, cnf, _, delta = producer.build()
    manifest = producer.manifest_payload(members, cnf, delta)
    with tempfile.TemporaryDirectory(prefix="clean-B6-l6-scout-", dir=producer.HERE.parent) as directory:
        path = Path(directory) / "group.cnf"
        producer.write_cnf(path, cnf, manifest, delta)
        start = time.monotonic_ns()
        result = subprocess.run(["timeout", str(args.seconds), str(solver), "-q", *OPTIONS, str(path)],
                                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        elapsed = time.monotonic_ns() - start
        status = {10: "SAT", 20: "UNSAT", 124: "TIMEOUT"}.get(result.returncode)
        if status is None:
            raise RuntimeError(f"unexpected solver exit {result.returncode}")
        size, digest = identity(path)
    payload = {"schema": f"{producer.PREFIX}-scout-v1", "seconds": args.seconds,
               "solver_bytes": identity(solver)[0], "solver_sha256": SOLVER_SHA256,
               "solver_version": "1.7.3", "solver_options": list(OPTIONS), "groups": 1,
               "parents": len(members), "unsat": int(status == "UNSAT"),
               "sat": int(status == "SAT"), "timeout": int(status == "TIMEOUT"),
               "rows": [{"group": producer.GROUP, "parents": len(members), "cnf_bytes": size,
                         "cnf_sha256": digest, "status": status, "nanoseconds": elapsed}]}
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="ascii", newline="\n")
    print(f"PASS group={producer.GROUP} parents={len(members)} status={status}")


if __name__ == "__main__":
    main()
