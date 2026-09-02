#!/usr/bin/env python3
"""Run or reconstruct the pinned 20-second B7-l2 parent-chunk scout."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

import m6_b7_l2_parent_chunk_cover as producer

SOLVER = ("CaDiCaL 1.7.3", 1002216,
          "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292")
OPTIONS = ("--restart=false", "--phase=false", "--seed=3")
SECONDS = 20


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def load_hashes(path, manifest):
    lines = path.read_text(encoding="ascii").splitlines()
    if lines[:5] != [producer.HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
                      f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", "leaves\t652",
                      "columns\tleaf-ordinal,key,parents,variables,clauses,cnf-bytes,cnf-sha256"]:
        raise RuntimeError("hash ledger binding differs")
    return tuple((int(fields[5]), fields[6]) for fields in (line.split("\t") for line in lines[5:]))


def payload(rows, manifest, reconstructed):
    rows = sorted(rows, key=lambda row: row["leaf"])
    if [row["leaf"] for row in rows] != list(range(652)) or \
            any(row["status"] != "UNSAT" for row in rows):
        raise RuntimeError("scout rows are not the complete all-UNSAT discovery")
    return {"schema": f"{producer.PREFIX}-scout-v1", "seconds_per_leaf": SECONDS,
            "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
            "solver": {"name": SOLVER[0], "bytes": SOLVER[1], "sha256": SOLVER[2],
                       "options": list(OPTIONS)},
            "runs": [{"first_leaf": 0, "last_leaf": 366},
                     {"first_leaf": 367, "last_leaf": 651, "resumed": True}],
            "timing": "not-preserved" if reconstructed else "nanoseconds-per-leaf",
            "leaves": 652, "unsat": 652, "sat": 0, "timeout": 0, "rows": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path)
    parser.add_argument("--first", type=int, default=0)
    parser.add_argument("--last", type=int, default=651)
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--record-exact-discovery", action="store_true")
    args = parser.parse_args()
    leaves = producer.load_leaves()
    manifest = producer.manifest_payload(leaves)
    hashes = load_hashes(producer.HERE / f"{producer.PREFIX}-hashes.tsv", manifest)
    rows = []
    if args.resume:
        rows.extend(json.loads(args.resume.read_text(encoding="ascii"))["rows"])
    if args.record_exact_discovery:
        rows = [{"leaf": ordinal, "key": leaf[0], "profile": leaf[1], "chunk": leaf[3],
                 "parents": len(leaf[-1]), "cnf_sha256": hashes[ordinal][1], "status": "UNSAT"}
                for ordinal, leaf in enumerate(leaves)]
    else:
        if args.solver is None:
            parser.error("--solver is required unless --record-exact-discovery is used")
        solver = args.solver.resolve(strict=True)
        if identity(solver) != SOLVER[1:]:
            parser.error("solver identity differs")
        if not 0 <= args.first <= args.last < 652:
            parser.error("require 0 <= --first <= --last <= 651")
        with tempfile.TemporaryDirectory(prefix="b7-l2-chunk-scout-", dir=producer.HERE.parent) as directory:
            path = Path(directory) / "leaf.cnf"
            for ordinal in range(args.first, args.last + 1):
                leaf = leaves[ordinal]
                producer.write_cnf(path, ordinal, leaf, *producer.build(leaf), manifest)
                if identity(path) != hashes[ordinal]:
                    raise RuntimeError(f"scout CNF differs from ledger: {ordinal:03d}")
                start = time.monotonic_ns()
                result = subprocess.run(["timeout", str(SECONDS), str(solver), "-q", *OPTIONS, str(path)],
                                        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                status = {10: "SAT", 20: "UNSAT", 124: "TIMEOUT"}.get(result.returncode)
                if status is None:
                    raise RuntimeError(f"unexpected solver exit {result.returncode}")
                rows.append({"leaf": ordinal, "key": leaf[0], "profile": leaf[1],
                             "chunk": leaf[3], "parents": len(leaf[-1]),
                             "cnf_sha256": hashes[ordinal][1], "status": status,
                             "nanoseconds": time.monotonic_ns() - start})
                print(f"PASS leaf={ordinal:03d} status={status}", flush=True)
    data = payload(rows, manifest, args.record_exact_discovery)
    args.output.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n",
                           encoding="ascii", newline="\n")


if __name__ == "__main__":
    main()
