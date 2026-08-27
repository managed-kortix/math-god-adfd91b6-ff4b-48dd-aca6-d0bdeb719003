#!/usr/bin/env python3
"""Scout the 33 frozen exact-pair TIMEOUT parents for ten seconds each."""

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import m6_b7_l6_early_c_certificate_residual_exact_pair_singleton_parent as singleton
import m6_b7_l6_exact_pair_timeout_complete_cut as census

SOLVER = "/tmp/opencode/cadical-1.7.3/build/cadical"
SOLVER_IDENTITY = (1002216, "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")
SECONDS = 10
JOBS = 2


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
        parser.error("scout requires the pinned solver, ten seconds, and two jobs")
    semantic_rows = census.records()
    _, memberships = singleton.load_memberships()
    manifest = singleton.manifest_payload(*singleton.load_memberships())

    def job(job_number, directory):
        output = []
        path = Path(directory) / f"job-{job_number}.cnf"
        for position in range(job_number, len(semantic_rows), JOBS):
            semantic = semantic_rows[position]
            ordinal = semantic["membership"]
            member = memberships[ordinal]
            cnf, selectors = singleton.build_membership(member)
            singleton.write_membership(path, ordinal, member, cnf, selectors, manifest)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            start = time.monotonic()
            result = subprocess.run(["timeout", str(SECONDS), str(args.solver), "-q", path],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            elapsed = round(time.monotonic() - start, 3)
            status = {10: "SAT", 20: "UNSAT", 124: "TIMEOUT"}.get(result.returncode)
            if status is None:
                raise RuntimeError(f"unexpected solver exit {result.returncode}")
            print(f"membership={ordinal:03d} status={status} seconds={elapsed}", flush=True)
            output.append({"membership": ordinal, "class": semantic["class"],
                           "status": status, "seconds": elapsed, "job": job_number,
                           "cnf_sha256": digest})
        return output

    rows = []
    with tempfile.TemporaryDirectory(prefix="complete-cut-scout-", dir=singleton.HERE.parent) as directory:
        with ThreadPoolExecutor(max_workers=JOBS) as executor:
            futures = [executor.submit(job, number, directory) for number in range(JOBS)]
            for future in as_completed(futures):
                rows.extend(future.result())
    rows.sort(key=lambda row: row["membership"])
    census_data = census.payload(semantic_rows)
    sequence = "".join({"SAT": "S", "UNSAT": "U", "TIMEOUT": "T"}[row["status"]] for row in rows)
    payload = {"schema": f"{census.PREFIX}-scout-v1", "seconds_per_membership": SECONDS,
               "jobs": JOBS, "solver": SOLVER, "solver_bytes": SOLVER_IDENTITY[0],
               "solver_sha256": SOLVER_IDENTITY[1], "solver_version": SOLVER_IDENTITY[2],
               "census_bytes": len(census_data),
               "census_sha256": hashlib.sha256(census_data).hexdigest(),
               "status_sequence_sha256": hashlib.sha256(sequence.encode("ascii")).hexdigest(),
               "rows": rows}
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="ascii", newline="\n")


if __name__ == "__main__":
    main()
