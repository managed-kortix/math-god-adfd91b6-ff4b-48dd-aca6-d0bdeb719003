#!/usr/bin/env python3
"""Scout all exact-pair singleton memberships with pinned CaDiCaL."""

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import m6_b7_l6_early_c_certificate_residual_exact_pair_singleton_parent as producer

SOLVER_PATH = "/tmp/opencode/cadical-1.7.3/build/cadical"
SOLVER_IDENTITY = (1002216, "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")
SECONDS = 5
JOBS = 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=SECONDS)
    parser.add_argument("--jobs", type=int, default=JOBS)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if str(args.solver) != SOLVER_PATH or args.seconds != SECONDS or args.jobs != JOBS:
        parser.error(f"pinned scout requires {SOLVER_PATH}, {SECONDS} seconds, and {JOBS} jobs")
    solver = args.solver.read_bytes()
    version = subprocess.run([str(args.solver), "--version"], capture_output=True,
                             text=True, check=True).stdout.strip()
    if (len(solver), hashlib.sha256(solver).hexdigest(), version) != SOLVER_IDENTITY:
        parser.error("solver is not pinned CaDiCaL 1.7.3")
    cells, memberships = producer.load_memberships()
    manifest = producer.manifest_payload(cells, memberships)
    ledger_path = producer.HERE / f"{producer.PREFIX}-hashes.tsv"
    ledger = ledger_path.read_bytes()
    hashes = {line.split("\t")[1]: line.split("\t")[-1]
              for line in ledger.decode("ascii").splitlines()[5:]}

    def run_job(job, directory):
        rows = []
        path = Path(directory) / f"job-{job}.cnf"
        for ordinal in range(job, len(memberships), args.jobs):
            member = memberships[ordinal]
            cnf, selectors = producer.build_membership(member)
            producer.write_membership(path, ordinal, member, cnf, selectors, manifest)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != hashes.get(producer.membership_key(member)):
                raise RuntimeError(f"membership {ordinal:03d} hash differs before scout")
            start = time.monotonic()
            result = subprocess.run(["timeout", str(args.seconds), str(args.solver), "-q", path],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            status = {10: "SAT", 20: "UNSAT", 124: "TIMEOUT"}.get(result.returncode,
                                                                    f"EXIT_{result.returncode}")
            elapsed = round(time.monotonic() - start, 3)
            if status not in ("SAT", "UNSAT", "TIMEOUT"):
                raise RuntimeError(f"membership {ordinal:03d} solver result {status}: {result.stdout[-500:]}")
            rows.append({"membership": ordinal, "key": producer.membership_key(member),
                         "cell": member[0], "source_child": member[1][0], "parent": member[2],
                         "job": job, "status": status, "seconds": elapsed, "cnf_sha256": digest})
            print(f"membership={ordinal:03d} job={job} status={status} seconds={elapsed}", flush=True)
        return rows

    rows = []
    with tempfile.TemporaryDirectory(prefix="exact-pair-singleton-scout-", dir=producer.HERE.parent) as directory:
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            pending = [executor.submit(run_job, job, directory) for job in range(args.jobs)]
            for future in as_completed(pending):
                rows.extend(future.result())
    rows.sort(key=lambda row: row["membership"])
    statuses = "".join({"SAT": "S", "UNSAT": "U", "TIMEOUT": "T"}[row["status"]] for row in rows)
    payload = {"schema": f"{producer.PREFIX}-scout-v1", "seconds_per_membership": args.seconds,
               "jobs": args.jobs, "solver": str(args.solver), "solver_bytes": len(solver),
               "solver_sha256": hashlib.sha256(solver).hexdigest(), "solver_version": version,
               "manifest_bytes": len(manifest), "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
               "hash_ledger_bytes": len(ledger), "hash_ledger_sha256": hashlib.sha256(ledger).hexdigest(),
               "status_sequence_sha256": hashlib.sha256(statuses.encode("ascii")).hexdigest(), "rows": rows}
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n",
                           encoding="ascii", newline="\n")


if __name__ == "__main__":
    main()
