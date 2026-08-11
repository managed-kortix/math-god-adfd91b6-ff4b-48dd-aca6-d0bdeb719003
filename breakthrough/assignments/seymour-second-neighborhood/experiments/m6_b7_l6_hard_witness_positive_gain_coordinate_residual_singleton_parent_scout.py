#!/usr/bin/env python3
"""Scout every exact residual membership with pinned CaDiCaL."""

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import m6_b7_l6_hard_witness_positive_gain_coordinate_residual_singleton_parent as producer

SOLVER_IDENTITY = (1002216, "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")
SOLVER_PATH = "/tmp/opencode/cadical-1.7.3/build/cadical"
SECONDS = 5
JOBS = 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=5)
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if str(args.solver) != SOLVER_PATH:
        parser.error(f"the frozen scout requires exactly --solver {SOLVER_PATH}")
    solver = args.solver.read_bytes()
    version = subprocess.run([str(args.solver), "--version"], capture_output=True,
                             text=True, check=True).stdout.strip()
    if (len(solver), hashlib.sha256(solver).hexdigest(), version) != SOLVER_IDENTITY:
        parser.error("solver is not the pinned CaDiCaL 1.7.3 binary")
    if args.seconds != SECONDS or args.jobs != JOBS:
        parser.error(f"the frozen scout requires exactly --seconds {SECONDS} --jobs {JOBS}")
    cover, memberships = producer.load_memberships()
    manifest = producer.manifest_payload(cover, memberships)
    ledger_path = producer.HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-singleton-parent-hashes.tsv"
    hashes = {}
    for line in ledger_path.read_text(encoding="ascii").splitlines()[5:]:
        fields = line.split("\t")
        hashes[fields[1]] = fields[-1]

    def run_job(job, directory):
        rows = []
        path = Path(directory) / f"job-{job}.cnf"
        for ordinal in range(job, len(memberships), args.jobs):
            member = memberships[ordinal]
            cnf, selectors = producer.build_membership(member)
            producer.write_membership(path, ordinal, member, cnf, selectors, manifest)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != hashes.get(producer.membership_key(member)):
                raise RuntimeError(f"generated scout CNF hash differs: {ordinal:04d}")
            start = time.monotonic()
            result = subprocess.run(["timeout", str(args.seconds), str(args.solver), "-q", path],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            status = {10: "SAT", 20: "UNSAT", 124: "TIMEOUT"}.get(
                result.returncode, f"EXIT_{result.returncode}")
            row = {"membership": ordinal, "key": producer.membership_key(member),
                   "residual_leaf": member[0], "parent_ordinal": member[2],
                   "accepted_ordinal": member[3][0], "cover_index": member[3][1],
                   "job": job, "status": status, "seconds": round(time.monotonic() - start, 3),
                   "cnf_sha256": digest}
            if status not in ("SAT", "UNSAT", "TIMEOUT"):
                row["output"] = result.stdout[-1000:]
            rows.append(row)
            print(f"membership={ordinal:04d} job={job} status={status} seconds={row['seconds']}", flush=True)
        return rows

    rows = []
    with tempfile.TemporaryDirectory(prefix="m6-residual-singleton-scout-", dir=producer.HERE.parent) as directory:
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            pending = [executor.submit(run_job, job, directory) for job in range(args.jobs)]
            for future in as_completed(pending):
                rows.extend(future.result())
    rows.sort(key=lambda row: row["membership"])
    ledger = ledger_path.read_bytes()
    payload = {"schema": "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-singleton-parent-scout-v1",
               "seconds_per_membership": args.seconds, "jobs": args.jobs, "solver": str(args.solver),
               "solver_bytes": len(solver), "solver_sha256": hashlib.sha256(solver).hexdigest(),
               "solver_version": version, "manifest_bytes": len(manifest),
               "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
               "hash_ledger_bytes": len(ledger),
               "hash_ledger_sha256": hashlib.sha256(ledger).hexdigest(), "rows": rows}
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n",
                           encoding="ascii", newline="\n")


if __name__ == "__main__":
    main()
