#!/usr/bin/env python3
"""Scout the 33 frozen exact-pair Hall-failure memberships."""

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import m6_b7_l6_exact_pair_timeout_hall_failure as hall

SOLVER = "/tmp/opencode/cadical-1.7.3/build/cadical"
SOLVER_IDENTITY = (1002216, "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")
SECONDS = 180
JOBS = 2
SOLVER_OPTIONS = ("--restart=false", "--phase=false", "--seed=3")
POSITION_OPTIONS = {10: ("--restart=false",)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=SECONDS)
    parser.add_argument("--jobs", type=int, default=JOBS)
    args = parser.parse_args()
    solver_data = args.solver.read_bytes()
    version = subprocess.run([str(args.solver), "--version"], text=True, capture_output=True,
                             check=True).stdout.strip()
    if str(args.solver) != SOLVER or args.seconds != SECONDS or args.jobs != JOBS or \
            (len(solver_data), hashlib.sha256(solver_data).hexdigest(), version) != SOLVER_IDENTITY:
        parser.error("scout requires the pinned solver, 180 seconds, and two jobs")
    records = hall.scope()
    manifest = hall.manifest_payload(records)
    hashes = hall.populate_hashes(records, manifest)

    def job(job_number, directory):
        output = []
        path = Path(directory) / f"job-{job_number}.cnf"
        for position in range(job_number, len(records), JOBS):
            row, _ = records[position]
            cnf, selectors, universe, support = hall.build_membership(records[position])
            hall.write_membership(path, position, records[position], cnf, selectors, universe, support,
                                  manifest)
            if hall.identity(path) != hashes[position]:
                raise RuntimeError("scout CNF differs from generated hash")
            start = time.monotonic()
            options = POSITION_OPTIONS.get(position, SOLVER_OPTIONS)
            result = subprocess.run(["timeout", str(SECONDS), str(args.solver), "-q", *options, path],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            elapsed = round(time.monotonic() - start, 3)
            status = {10: "SAT", 20: "UNSAT", 124: "TIMEOUT"}.get(result.returncode)
            if status is None:
                raise RuntimeError(f"unexpected solver exit {result.returncode}")
            print(f"position={position:03d} membership={row['membership']:03d} "
                  f"status={status} seconds={elapsed}", flush=True)
            output.append({"position": position, "membership": row["membership"],
                           "status": status, "seconds": elapsed, "job": job_number,
                           "solver_options": list(options), "cnf_sha256": hashes[position][1]})
        return output

    rows = []
    with tempfile.TemporaryDirectory(prefix="hall-failure-scout-", dir=hall.HERE.parent) as directory:
        with ThreadPoolExecutor(max_workers=JOBS) as executor:
            futures = [executor.submit(job, number, directory) for number in range(JOBS)]
            for future in as_completed(futures):
                rows.extend(future.result())
    rows.sort(key=lambda row: row["position"])
    sequence = "".join({"SAT": "S", "UNSAT": "U", "TIMEOUT": "T"}[row["status"]] for row in rows)
    ledger = hall.hash_payload(records, manifest, hashes)
    payload = {"schema": f"{hall.PREFIX}-scout-v1", "seconds_per_membership": SECONDS,
               "jobs": JOBS, "solver": SOLVER, "solver_bytes": SOLVER_IDENTITY[0],
               "solver_sha256": SOLVER_IDENTITY[1], "solver_version": SOLVER_IDENTITY[2],
               "default_solver_options": list(SOLVER_OPTIONS),
               "position_options": {str(key): list(value) for key, value in POSITION_OPTIONS.items()},
               "manifest_bytes": len(manifest), "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
               "hash_ledger_bytes": len(ledger), "hash_ledger_sha256": hashlib.sha256(ledger).hexdigest(),
               "status_sequence_sha256": hashlib.sha256(sequence.encode("ascii")).hexdigest(),
               "rows": rows}
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n",
                           encoding="ascii", newline="\n")


if __name__ == "__main__":
    main()
