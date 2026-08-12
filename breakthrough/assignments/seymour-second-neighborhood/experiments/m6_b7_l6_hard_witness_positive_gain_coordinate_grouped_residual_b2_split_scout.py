#!/usr/bin/env python3
"""Run pinned CaDiCaL for 20 seconds on each exact grouped B2 split child."""

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from pathlib import Path

import m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual_b2_split as producer

SOLVER_PATH = "/tmp/opencode/cadical-1.7.3/build/cadical"
SOLVER_IDENTITY = (1002216, "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")
SECONDS = 20


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=SECONDS)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if str(args.solver) != SOLVER_PATH or args.seconds != SECONDS:
        parser.error(f"pinned scout requires --solver {SOLVER_PATH} --seconds {SECONDS}")
    solver = args.solver.read_bytes()
    version = subprocess.run([str(args.solver), "--version"], capture_output=True, text=True, check=True).stdout.strip()
    if (len(solver), hashlib.sha256(solver).hexdigest(), version) != SOLVER_IDENTITY:
        parser.error("solver is not pinned CaDiCaL 1.7.3")
    items = producer.children()
    manifest = producer.manifest_payload(items)
    hash_path = producer.HERE / f"{producer.PREFIX}-hashes.tsv"
    ledger = hash_path.read_bytes()
    hashes = [line.split("\t")[-1] for line in ledger.decode("ascii").splitlines()[5:]]
    rows = []
    with tempfile.TemporaryDirectory(prefix="m6-grouped-b2-scout-", dir=producer.HERE.parent) as directory:
        path = Path(directory) / "child.cnf"
        for ordinal, child in enumerate(items):
            source, branch, _ = child
            cnf, selectors = producer.build_child(child)
            producer.write_child(path, ordinal, child, cnf, selectors, manifest)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != hashes[ordinal]:
                raise RuntimeError(f"child {ordinal:02d} hash differs before scout")
            start = time.monotonic()
            solved = subprocess.run(["timeout", str(SECONDS), str(args.solver), "-q", str(path)],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            elapsed = round(time.monotonic() - start, 3)
            status = {10: "SAT", 20: "UNSAT", 124: "TIMEOUT"}.get(solved.returncode)
            if status is None:
                raise RuntimeError(f"child {ordinal:02d} solver exit {solved.returncode}: {solved.stdout[-500:]}")
            rows.append({"child": ordinal, "source_leaf": source[0], "key": producer.grouped.residual.key(source[1]),
                         "branch": branch, "width": len(selectors), "status": status, "seconds": elapsed,
                         "cnf_sha256": digest})
            print(f"child={ordinal:02d} source={source[0]:03d} branch={branch} status={status} seconds={elapsed}", flush=True)
    payload = {"schema": f"{producer.PREFIX}-scout-v1", "seconds_per_child": SECONDS,
               "solver": str(args.solver), "solver_bytes": len(solver),
               "solver_sha256": hashlib.sha256(solver).hexdigest(), "solver_version": version,
               "manifest_bytes": len(manifest), "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
               "hash_ledger_bytes": len(ledger), "hash_ledger_sha256": hashlib.sha256(ledger).hexdigest(),
               "rows": rows}
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="ascii", newline="\n")


if __name__ == "__main__":
    main()
