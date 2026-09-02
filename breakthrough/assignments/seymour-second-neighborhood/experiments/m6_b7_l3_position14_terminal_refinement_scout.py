#!/usr/bin/env python3
"""Scout every B7-l3 position-14 terminal leaf."""

import argparse
import json
import subprocess
import tempfile
import time
from pathlib import Path

import check_m6_b7_l3_position14_terminal_refinement as structural
import m6_b7_l3_position14_terminal_refinement as producer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=30)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    solver = args.solver.resolve(strict=True)
    if producer.identity(solver)[1] != "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292":
        parser.error("solver identity differs")
    structural.audit(regenerate=False)
    leaves = producer.load_leaves()
    manifest = producer.manifest_payload(leaves)
    rows = []
    with tempfile.TemporaryDirectory(prefix="b7-l3-p14-scout-", dir=producer.HERE.parent) as directory:
        cnf_path = Path(directory) / "leaf.cnf"
        for ordinal, leaf in enumerate(leaves):
            producer.write_cnf(cnf_path, ordinal, leaf, *producer.build(leaf), manifest)
            start = time.monotonic_ns()
            try:
                result = subprocess.run([str(solver), "-q", "--restart=false", "--phase=false", "--seed=3",
                                         str(cnf_path)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
                                        timeout=args.seconds)
                status = {10: "SAT", 20: "UNSAT"}.get(result.returncode, f"EXIT-{result.returncode}")
            except subprocess.TimeoutExpired:
                status = "TIMEOUT"
            rows.append({"leaf": ordinal, "key": leaf[0], "parents": len(leaf[-1]),
                         "cnf_bytes": cnf_path.stat().st_size,
                         "cnf_sha256": producer.identity(cnf_path)[1],
                         "nanoseconds": time.monotonic_ns() - start, "status": status})
            print(f"{ordinal:02d} {status}", flush=True)
    payload = {"schema": f"{producer.PREFIX}-scout-v1", "seconds_per_leaf": args.seconds,
               "solver_sha256": producer.identity(solver)[1], "solver_options": ["--restart=false", "--phase=false", "--seed=3"],
               "leaves": len(rows), "unsat": sum(row["status"] == "UNSAT" for row in rows),
               "sat": sum(row["status"] == "SAT" for row in rows),
               "timeout": sum(row["status"] == "TIMEOUT" for row in rows), "rows": rows}
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="ascii")


if __name__ == "__main__":
    main()
