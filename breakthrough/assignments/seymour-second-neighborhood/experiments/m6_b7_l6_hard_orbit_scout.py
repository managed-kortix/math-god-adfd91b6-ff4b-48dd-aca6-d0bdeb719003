#!/usr/bin/env python3
"""Run a capped solver scout over all gated B7-l6 hard orbit leaves."""

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from pathlib import Path

import check_m6_b7_l6_hard_orbits as checker
import m6_b7_l6_hard_orbits as producer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=20)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    leaves = producer.load_leaves()
    manifest = producer.manifest_payload(leaves)
    rows = []
    with tempfile.TemporaryDirectory(prefix="m6-b7-l6-hard-scout-", dir=producer.HERE.parent) as directory:
        directory = Path(directory)
        for ordinal, leaf in enumerate(leaves):
            cnf_path, model_path = directory / "leaf.cnf", directory / "model.txt"
            cnf, selectors = producer.build_leaf(leaf)
            producer.write_leaf(cnf_path, ordinal, leaf, cnf, selectors, manifest)
            checker.check(cnf_path)
            start = time.monotonic()
            result = subprocess.run(["timeout", str(args.seconds), str(args.solver), "-q", cnf_path],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
            elapsed = round(time.monotonic() - start, 3)
            status = {10: "SAT", 20: "UNSAT", 124: "TIMEOUT"}.get(result.returncode,
                                                                    f"EXIT_{result.returncode}")
            row = {"leaf": ordinal, "key": leaf[0], "state_leaf": leaf[1], "intersection_t": leaf[4],
                   "parents": len(leaf[6]), "status": status, "seconds": elapsed,
                   "cnf_sha256": hashlib.sha256(cnf_path.read_bytes()).hexdigest()}
            if status == "SAT":
                model_path.write_text(result.stdout, encoding="ascii", newline="\n")
                literals = source_model(model_path)
                _, selected = checker.validate_model(*checker.parse_cnf(cnf_path)[1:3], literals, selectors)
                accepted, cover, _ = leaf[6][selected]
                row.update({"selector": selected, "accepted": accepted, "cover": cover,
                            "model_sha256": hashlib.sha256(model_path.read_bytes()).hexdigest()})
            elif status not in ("UNSAT", "TIMEOUT"):
                row["output"] = result.stdout[-1000:]
            rows.append(row)
            print(f"leaf={ordinal:02d} key={leaf[0]} status={status} seconds={elapsed}")
    solver_data = args.solver.read_bytes()
    payload = {"schema": "m6-b7-l6-hard-orbit-scout-v1", "seconds_per_leaf": args.seconds,
               "solver": str(args.solver), "solver_bytes": len(solver_data),
               "solver_sha256": hashlib.sha256(solver_data).hexdigest(),
               "manifest_sha256": hashlib.sha256(manifest).hexdigest(), "rows": rows}
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="ascii", newline="\n")


def source_model(path):
    literals = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("c ") or line in ("s SATISFIABLE", "SAT"):
            continue
        for token in (line[2:].split() if line.startswith("v ") else line.split()):
            value = int(token)
            if value == 0:
                return literals
            literals.append(value)
    raise RuntimeError("SAT model has no terminator")


if __name__ == "__main__":
    main()
