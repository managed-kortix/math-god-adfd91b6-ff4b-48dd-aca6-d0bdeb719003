#!/usr/bin/env python3
"""Reproducible pinned CaDiCaL and Kissat scout of all 28 Hall children."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

import m6_b7_l6_exact_pair_timeout_hall_failure_cardinality_split as producer

CADICAL = ("CaDiCaL 1.7.3", 1002216,
           "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292")
KISSAT = ("Kissat 4.0.4", 566856,
          "aa511b55186449eaaa6b421510a8aaa8660d879f50924ce9c45606e7df7ab41f")
CADICAL_OPTIONS = ("--restart=false", "--phase=false", "--seed=3")


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cadical", type=Path, required=True)
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cadical, kissat = args.cadical.resolve(strict=True), args.kissat.resolve(strict=True)
    if identity(cadical) != CADICAL[1:] or identity(kissat) != KISSAT[1:]:
        parser.error("scout solvers are not pinned")
    scope = producer.children()
    manifest = producer.manifest_payload(scope)
    hashes = producer.populate_hashes(scope, manifest)
    rows = []
    with tempfile.TemporaryDirectory(prefix="hall-cardinality-scout-", dir=producer.HERE.parent) as directory:
        path = Path(directory) / "child.cnf"
        for child_position, child in enumerate(scope):
            built = producer.build_child(child)
            producer.write_child(path, child_position, child, *built, manifest)
            if identity(path) != hashes[child_position]:
                raise RuntimeError("scout CNF differs from hash ledger")
            row = {"child": child_position, "membership": child[1][0]["membership"],
                   "cardinality": child[2], "cnf_sha256": hashes[child_position][1]}
            for name, solver, options in (("cadical", cadical, CADICAL_OPTIONS),
                                          ("kissat", kissat, ())):
                start = time.monotonic_ns()
                solved = subprocess.run([str(solver), "-q", *options, str(path)],
                                        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                row[f"{name}_nanoseconds"] = time.monotonic_ns() - start
                row[f"{name}_status"] = {10: "SAT", 20: "UNSAT"}.get(solved.returncode,
                                                                         f"EXIT-{solved.returncode}")
                if row[f"{name}_status"] != "UNSAT":
                    raise RuntimeError(f"{name} did not return UNSAT on child {child_position:03d}")
            rows.append(row)
            print(f"PASS {child_position + 1:02d}/28 membership={row['membership']:03d} "
                  f"k={row['cardinality']} cadical=UNSAT kissat=UNSAT", flush=True)
    payload = {"schema": f"{producer.PREFIX}-scout-v1", "children": 28,
               "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
               "cadical": {"name": CADICAL[0], "bytes": CADICAL[1], "sha256": CADICAL[2],
                            "options": list(CADICAL_OPTIONS)},
               "kissat": {"name": KISSAT[0], "bytes": KISSAT[1], "sha256": KISSAT[2],
                          "options": []}, "rows": rows}
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n",
                           encoding="ascii", newline="\n")


if __name__ == "__main__":
    main()
