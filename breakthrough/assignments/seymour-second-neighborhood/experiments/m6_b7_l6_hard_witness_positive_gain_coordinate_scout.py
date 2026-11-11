#!/usr/bin/env python3
"""Run a capped solver scout over all deletion-coordinate children."""

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import check_m6_b7_l6_hard_witness_positive_gain_coordinate as checker
import m6_b7_l6_hard_witness_positive_gain_coordinate as producer

SOLVER_IDENTITY = (1002216, "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=15)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    solver = args.solver.read_bytes()
    version = subprocess.run([str(args.solver), "--version"], capture_output=True,
                             text=True, check=True).stdout.strip()
    if (len(solver), hashlib.sha256(solver).hexdigest(), version) != SOLVER_IDENTITY:
        parser.error("solver is not the pinned CaDiCaL 1.7.3 binary")
    children = producer.load_leaves()
    manifest = producer.manifest_payload(children)
    ledger = producer.HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-hashes.tsv"
    rows = []
    with tempfile.TemporaryDirectory(prefix="m6-positive-coordinate-scout-", dir=producer.HERE.parent) as directory:
        jobs = []
        for ordinal, child in enumerate(children):
            path = Path(directory) / f"leaf-{ordinal:03d}.cnf"
            cnf, selectors = producer.build_leaf(child)
            producer.write_leaf(path, ordinal, child, cnf, selectors, manifest)
            checker.check(path)
            jobs.append((ordinal, child, path))

        def solve(item):
            ordinal, child, path = item
            start = time.monotonic()
            result = subprocess.run(["timeout", str(args.seconds), str(args.solver), "-q", path],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            elapsed = round(time.monotonic() - start, 3)
            status = {10: "SAT", 20: "UNSAT", 124: "TIMEOUT"}.get(result.returncode,
                                                                    f"EXIT_{result.returncode}")
            row = {"leaf": ordinal, "key": producer.child_key(child),
                   "source_leaf": child[0], "source_key": child[4][0],
                   "coordinate": child[1], "deleted": child[2], "witness": child[3],
                   "parents": len(child[4][2][6]), "coordinate_path_literals": 16,
                   "coordinate_path_alo_clauses": 1, "status": status, "seconds": elapsed,
                   "cnf_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            if status not in ("SAT", "UNSAT", "TIMEOUT"):
                row["output"] = result.stdout[-1000:]
            return row

        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            pending = [executor.submit(solve, item) for item in jobs]
            for future in as_completed(pending):
                row = future.result()
                rows.append(row)
                print(f"leaf={row['leaf']:03d} key={row['key']} status={row['status']} "
                      f"seconds={row['seconds']}", flush=True)
        rows.sort(key=lambda row: row["leaf"])
    ledger_data = ledger.read_bytes()
    payload = {"schema": "m6-b7-l6-hard-witness-positive-gain-coordinate-scout-v1",
               "seconds_per_leaf": args.seconds, "solver": str(args.solver),
               "solver_bytes": len(solver), "solver_sha256": hashlib.sha256(solver).hexdigest(),
               "solver_version": version, "manifest_bytes": len(manifest),
               "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
               "hash_ledger_bytes": len(ledger_data),
               "hash_ledger_sha256": hashlib.sha256(ledger_data).hexdigest(), "rows": rows}
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n",
                           encoding="ascii", newline="\n")


if __name__ == "__main__":
    main()
