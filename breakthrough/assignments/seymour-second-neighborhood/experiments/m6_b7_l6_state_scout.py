#!/usr/bin/env python3
"""Run a capped solver scout over every gated B7-l6 state leaf."""

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from pathlib import Path

import check_m6_b7_l6_state_split as checker
import m6_b7_l6_state_split as producer

SCHEMA = "m6-b7-l6-state-scout-v1"


def solver_identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=30)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.seconds <= 0 or not args.solver.is_file():
        parser.error("solver must be a file and seconds must be positive")
    leaves = producer.load_leaves()
    manifest = producer.manifest_payload(leaves)
    rows = []
    with tempfile.TemporaryDirectory(prefix="m6-b7-l6-scout-", dir=producer.HERE.parent) as directory:
        directory = Path(directory)
        for ordinal, leaf in enumerate(leaves):
            cnf_path, model_path = directory / "leaf.cnf", directory / "model.txt"
            cnf, shapes, selectors = producer.build_leaf(leaf[1], leaf[2])
            producer.write_leaf(cnf_path, ordinal, leaf, cnf, shapes, selectors, manifest)
            checker.check(cnf_path)
            start = time.monotonic()
            result = subprocess.run(["timeout", str(args.seconds), str(args.solver), "-q", cnf_path],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    text=True, check=False)
            elapsed = round(time.monotonic() - start, 3)
            status = {10: "SAT", 20: "UNSAT", 124: "TIMEOUT"}.get(result.returncode,
                                                                    f"EXIT_{result.returncode}")
            row = {"leaf": ordinal, "key": leaf[0], "parents": len(leaf[2]),
                   "status": status, "seconds": elapsed,
                   "cnf_sha256": hashlib.sha256(cnf_path.read_bytes()).hexdigest()}
            if status == "SAT":
                model_path.write_text(result.stdout, encoding="ascii", newline="\n")
                _, _, members, checked_selectors = checker.check(cnf_path, model_path)
                literals = checker.read_model(model_path)
                _, selected = checker.validate_model(*checker.parse_cnf(cnf_path)[1:3], literals,
                                                     checked_selectors)
                accepted, cover_index, _ = members[selected]
                row.update({"selector": selected, "accepted": accepted, "cover": cover_index,
                            "model_sha256": hashlib.sha256(model_path.read_bytes()).hexdigest()})
            elif status not in ("UNSAT", "TIMEOUT"):
                row["output"] = result.stdout[-1000:]
            rows.append(row)
            print(f"leaf={ordinal:02d} key={leaf[0]} status={status} seconds={elapsed}")
    payload = {"schema": SCHEMA, "seconds_per_leaf": args.seconds,
               "solver": str(args.solver), "solver_bytes": solver_identity(args.solver)[0],
               "solver_sha256": solver_identity(args.solver)[1],
               "manifest_sha256": hashlib.sha256(manifest).hexdigest(), "rows": rows}
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="ascii", newline="\n")


if __name__ == "__main__":
    main()
