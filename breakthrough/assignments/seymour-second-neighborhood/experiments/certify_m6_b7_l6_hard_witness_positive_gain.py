#!/usr/bin/env python3
"""Create checked LRATs for exactly the three frozen scout-UNSAT gain leaves."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time

import check_m6_b7_l6_hard_witness_positive_gain as structural
import m6_b7_l6_hard_witness_positive_gain as producer

HERE = Path(__file__).resolve().parent
SOLVER_SHA256 = "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292"
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
ORDINALS = (42, 95, 97)
LIMIT = 250_000_000
COLUMNS = (
    "leaf-ordinal", "key", "parents", "variables", "clauses", "cnf-bytes",
    "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes", "xz-sha256",
    "solve-nanoseconds", "check-nanoseconds", "artifact",
)


def identity(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            digest.update(block)
    return path.stat().st_size, digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--stage", type=Path, required=True)
    args = parser.parse_args()
    if identity(args.solver)[1] != SOLVER_SHA256:
        parser.error("solver is not the pinned CaDiCaL 1.7.3 binary")
    if identity(args.checker)[1] != CHECKER_SHA256:
        parser.error("checker is not the pinned lrat-check binary")
    if args.stage.exists():
        parser.error("stage path already exists")
    args.stage.mkdir(parents=False)
    artifacts = args.stage / "artifacts"
    artifacts.mkdir()

    try:
        structural.check_partition()
        scout = structural.check_scout()
        ordinals = tuple(row["leaf"] for row in scout["rows"] if row["status"] == "UNSAT")
        if ordinals != ORDINALS:
            raise RuntimeError("scope is not exactly frozen scout-UNSAT leaves 042,095,097")
        leaves = producer.load_leaves()
        manifest = producer.manifest_payload(leaves)
        records = []
        total_xz = 0
        for position, ordinal in enumerate(ordinals, 1):
            leaf = leaves[ordinal]
            cnf = args.stage / f"leaf-{ordinal:03d}.cnf"
            lrat = args.stage / f"leaf-{ordinal:03d}.lrat"
            artifact_name = f"m6-b7-l6-hard-witness-positive-gain-leaf-{ordinal:03d}.lrat.xz"
            artifact = artifacts / artifact_name
            built, selectors = producer.build_leaf(leaf)
            producer.write_leaf(cnf, ordinal, leaf, built, selectors, manifest)
            structural.check(cnf)
            cnf_id = identity(cnf)
            solve_start = time.monotonic_ns()
            solved = subprocess.run(
                [str(args.solver), "--lrat", "--no-binary", "-q", str(cnf), str(lrat)],
                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False,
            )
            solve_ns = time.monotonic_ns() - solve_start
            if solved.returncode != 20:
                raise RuntimeError(f"leaf {ordinal:03d} solver exit {solved.returncode}, expected 20")
            lrat_id = identity(lrat)
            check_start = time.monotonic_ns()
            checked = subprocess.run(
                [str(args.checker), str(cnf), str(lrat)], capture_output=True, text=True,
            )
            check_ns = time.monotonic_ns() - check_start
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError(f"leaf {ordinal:03d} LRAT rejected")
            with artifact.open("wb") as output:
                compressed = subprocess.run(["xz", "-3", "-c", str(lrat)], stdout=output)
            if compressed.returncode:
                raise RuntimeError(f"leaf {ordinal:03d} compression failed")
            xz_id = identity(artifact)
            total_xz += xz_id[0]
            if total_xz >= LIMIT:
                raise RuntimeError(f"compressed total reached {total_xz} bytes, not below {LIMIT}")
            variables, clauses = producer.dimensions(leaf)
            records.append((
                f"{ordinal:03d}", leaf[0], str(len(leaf[2][6])), str(variables), str(clauses),
                str(cnf_id[0]), cnf_id[1], str(lrat_id[0]), lrat_id[1], str(xz_id[0]),
                xz_id[1], str(solve_ns), str(check_ns), f"certificates/{artifact_name}",
            ))
            cnf.unlink()
            lrat.unlink()
            print(f"PASS {position:02d}/03 leaf={ordinal:03d} key={leaf[0]} xz={xz_id[0]} total={total_xz}", flush=True)
        rows = args.stage / "rows.tsv"
        with rows.open("w", encoding="ascii", newline="\n") as handle:
            handle.write("columns\t" + ",".join(COLUMNS) + "\n")
            for record in records:
                handle.write("\t".join(record) + "\n")
        print(f"PASS leaves=3 total_xz_bytes={total_xz} rows={rows}")
    except BaseException:
        shutil.rmtree(args.stage, ignore_errors=True)
        raise


if __name__ == "__main__":
    main()
