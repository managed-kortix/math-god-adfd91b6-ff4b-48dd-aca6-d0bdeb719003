#!/usr/bin/env python3
"""Scout all 33 unsplit authoritative cardinality strengthenings."""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

import m6_b7_l6_exact_pair_hall_cardinality_strengthening as producer

SOLVER_IDENTITY = (1002216, "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")
OPTIONS = ("--restart=false", "--phase=false", "--seed=3")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=10)
    parser.add_argument("--jobs", type=int, default=8)
    args = parser.parse_args()
    data = args.solver.read_bytes()
    version = subprocess.run([str(args.solver), "--version"], text=True, capture_output=True,
                             check=True).stdout.strip()
    if (len(data), hashlib.sha256(data).hexdigest(), version) != SOLVER_IDENTITY:
        parser.error("solver identity differs from pinned CaDiCaL 1.7.3")
    records = producer.scope()
    manifest = producer.manifest_payload(records)
    hashes = producer.populate_hashes(records, manifest)

    def job(number, directory):
        output = []
        path = Path(directory) / f"job-{number}.cnf"
        for position in range(number, 33, args.jobs):
            built = producer.build_membership(records[position])
            producer.write_membership(path, position, records[position], *built, manifest)
            start = time.monotonic()
            result = subprocess.run(["timeout", str(args.seconds), str(args.solver), "-q", *OPTIONS,
                                     str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            status = {20: "UNSAT", 10: "SAT", 124: "TIMEOUT"}.get(result.returncode)
            if status is None:
                raise RuntimeError(f"unexpected solver exit {result.returncode}")
            row = {"position": position, "membership": records[position][0]["membership"],
                   "status": status, "seconds": round(time.monotonic() - start, 3),
                   "job": number, "cnf_sha256": hashes[position][1]}
            print(row, flush=True)
            output.append(row)
        return output

    rows = []
    with tempfile.TemporaryDirectory(prefix="hall-cardinality-scout-", dir=producer.HERE.parent) as directory:
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            futures = [executor.submit(job, number, directory) for number in range(args.jobs)]
            for future in as_completed(futures):
                rows.extend(future.result())
    rows.sort(key=lambda row: row["position"])
    sequence = "".join({"UNSAT": "U", "SAT": "S", "TIMEOUT": "T"}[row["status"]] for row in rows)
    ledger = producer.hash_payload(records, manifest, hashes)
    payload = {"schema": f"{producer.PREFIX}-scout-v1", "seconds_per_membership": args.seconds,
               "jobs": args.jobs, "solver": str(args.solver), "solver_bytes": SOLVER_IDENTITY[0],
               "solver_sha256": SOLVER_IDENTITY[1], "solver_version": SOLVER_IDENTITY[2],
               "solver_options": list(OPTIONS), "manifest_bytes": len(manifest),
               "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
               "hash_ledger_bytes": len(ledger),
               "hash_ledger_sha256": hashlib.sha256(ledger).hexdigest(),
               "status_sequence_sha256": hashlib.sha256(sequence.encode("ascii")).hexdigest(),
               "rows": rows}
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="ascii")


if __name__ == "__main__":
    main()
