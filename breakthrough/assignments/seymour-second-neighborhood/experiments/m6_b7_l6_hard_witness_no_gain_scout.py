#!/usr/bin/env python3
"""Run a capped solver scout over the frozen exact no-gain children."""

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from pathlib import Path

import check_m6_b7_l6_hard_witness_no_gain as checker
import m6_b7_l6_hard_witness_no_gain as producer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=20)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    leaves = producer.load_leaves()
    manifest = producer.manifest_payload(leaves)
    ledger = producer.HERE / "m6-b7-l6-hard-witness-no-gain-hashes.tsv"
    rows = []
    with tempfile.TemporaryDirectory(prefix="m6-witness-no-gain-scout-", dir=producer.HERE.parent) as directory:
        path = Path(directory) / "leaf.cnf"
        for ordinal, leaf in enumerate(leaves):
            cnf, selectors = producer.build_leaf(leaf)
            producer.write_leaf(path, ordinal, leaf, cnf, selectors, manifest)
            checker.check(path)
            start = time.monotonic()
            result = subprocess.run(["timeout", str(args.seconds), str(args.solver), "-q", path],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
            elapsed = round(time.monotonic() - start, 3)
            status = {10: "SAT", 20: "UNSAT", 124: "TIMEOUT"}.get(result.returncode,
                                                                    f"EXIT_{result.returncode}")
            row = {"leaf": ordinal, "key": leaf[0], "parent_orbit": leaf[1],
                   "parent_key": leaf[2][0], "parents": len(leaf[2][6]),
                   "high_c": list(leaf[3]), "ordered_witnesses": list(leaf[4]),
                   "negative_path_units": len(producer.no_gain_paths(leaf)), "status": status,
                   "seconds": elapsed, "cnf_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            if status not in ("UNSAT", "TIMEOUT"):
                row["output"] = result.stdout[-1000:]
            rows.append(row)
            print(f"leaf={ordinal:03d} key={leaf[0]} status={status} seconds={elapsed}", flush=True)
    solver = args.solver.read_bytes()
    version = subprocess.run([str(args.solver), "--version"], capture_output=True,
                             text=True, check=True).stdout.strip()
    ledger_data = ledger.read_bytes()
    payload = {"schema": "m6-b7-l6-hard-witness-no-gain-scout-v1",
                "seconds_per_leaf": args.seconds, "solver": str(args.solver),
                "solver_bytes": len(solver), "solver_sha256": hashlib.sha256(solver).hexdigest(),
                "solver_version": version,
               "manifest_bytes": len(manifest), "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
               "hash_ledger_bytes": len(ledger_data),
               "hash_ledger_sha256": hashlib.sha256(ledger_data).hexdigest(), "rows": rows}
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n",
                           encoding="ascii", newline="\n")


if __name__ == "__main__":
    main()
