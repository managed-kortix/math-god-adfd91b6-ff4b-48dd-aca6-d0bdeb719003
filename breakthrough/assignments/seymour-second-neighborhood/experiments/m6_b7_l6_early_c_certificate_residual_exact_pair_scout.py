#!/usr/bin/env python3
"""Run the pinned ten-second scout over 20 residual exact-pair cells."""

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from pathlib import Path

import m6_b7_l6_early_c_certificate_residual_exact_pairs as producer

SOLVER_PATH = "/tmp/opencode/cadical-1.7.3/build/cadical"
SOLVER_IDENTITY = (1002216, "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=10)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if str(args.solver) != SOLVER_PATH or args.seconds != 10:
        parser.error(f"pinned scout requires --solver {SOLVER_PATH} --seconds 10")
    solver = args.solver.read_bytes()
    version = subprocess.run([str(args.solver), "--version"], capture_output=True,
                             text=True, check=True).stdout.strip()
    if (len(solver), hashlib.sha256(solver).hexdigest(), version) != SOLVER_IDENTITY:
        parser.error("solver is not pinned CaDiCaL 1.7.3")
    children = producer.load_children()
    manifest = producer.manifest_payload(children)
    ledger_path = producer.HERE / f"{producer.PREFIX}-hashes.tsv"
    ledger = ledger_path.read_bytes()
    hashes = {line.split("\t")[2]: line.split("\t")[-1]
              for line in ledger.decode("ascii").splitlines()[5:]}
    rows = []
    with tempfile.TemporaryDirectory(prefix="certificate-residual-scout-", dir=producer.HERE.parent) as directory:
        path = Path(directory) / "cell.cnf"
        for cell, record in enumerate(children):
            source_child, child = record
            cnf, selectors = producer.build_child(record)
            producer.write_child(path, cell, record, cnf, selectors, manifest)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != hashes[child[0]]:
                raise RuntimeError(f"cell {cell:03d} hash differs before scout")
            start = time.monotonic()
            result = subprocess.run(["timeout", str(args.seconds), str(args.solver), "-q", path],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            elapsed = round(time.monotonic() - start, 3)
            status = {10: "SAT", 20: "UNSAT", 124: "TIMEOUT"}.get(result.returncode,
                                                                    f"EXIT_{result.returncode}")
            if status not in ("SAT", "UNSAT", "TIMEOUT"):
                raise RuntimeError(f"unexpected scout result {status} for cell {cell}")
            rows.append({"cell": cell, "source_child": source_child, "key": child[0],
                         "profile": child[1], "compatible_parents": len(child[5]),
                         "status": status, "seconds": elapsed, "cnf_sha256": digest})
            print(f"cell={cell:03d} source_child={source_child:03d} status={status} seconds={elapsed}")
    status_sequence = "".join({"SAT": "S", "UNSAT": "U", "TIMEOUT": "T"}[row["status"]]
                              for row in rows)
    payload = {"schema": f"{producer.PREFIX}-scout-v1", "seconds_per_cell": args.seconds,
               "solver": str(args.solver), "solver_bytes": len(solver),
               "solver_sha256": hashlib.sha256(solver).hexdigest(), "solver_version": version,
               "manifest_bytes": len(manifest), "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
               "hash_ledger_bytes": len(ledger), "hash_ledger_sha256": hashlib.sha256(ledger).hexdigest(),
               "status_sequence_sha256": hashlib.sha256(status_sequence.encode("ascii")).hexdigest(),
               "rows": rows}
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n",
                           encoding="ascii", newline="\n")


if __name__ == "__main__":
    main()
