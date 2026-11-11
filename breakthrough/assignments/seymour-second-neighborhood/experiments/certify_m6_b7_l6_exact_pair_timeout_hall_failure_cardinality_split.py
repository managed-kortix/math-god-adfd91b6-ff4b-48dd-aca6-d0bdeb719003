#!/usr/bin/env python3
"""Generate and check CaDiCaL LRATs for all 28 exact |K| children."""

import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import time

import check_m6_b7_l6_exact_pair_timeout_hall_failure_cardinality_split as structural
import m6_b7_l6_exact_pair_timeout_hall_failure_cardinality_split as producer

SOLVER_SHA256 = "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292"
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
XZ = Path("/usr/bin/xz")
XZ_SHA256 = "b5b163eb273291934556377ab883b4b2a5d4da50bd0dc0a91774ecc234ccd8d0"
LIMIT = 250_000_000
COLUMNS = ("child", "parent-position", "membership", "key", "cardinality", "variables",
           "clauses", "cnf-bytes", "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes",
           "xz-sha256", "solve-nanoseconds", "check-nanoseconds", "artifact")


def identity(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            value.update(block)
    return path.stat().st_size, value.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--stage", type=Path, required=True)
    args = parser.parse_args()
    solver, checker = args.solver.resolve(strict=True), args.checker.resolve(strict=True)
    if identity(solver)[1] != SOLVER_SHA256 or identity(checker)[1] != CHECKER_SHA256 or \
            identity(XZ)[1] != XZ_SHA256:
        parser.error("solver, checker, or compressor is not pinned")
    if args.stage.exists():
        parser.error("stage path already exists")
    args.stage.mkdir(parents=False)
    artifacts = args.stage / "artifacts"
    artifacts.mkdir()
    try:
        structural.check_cover()
        scope = producer.children()
        manifest = producer.manifest_payload(scope)
        rows, total_xz = [], 0
        for child_position, child in enumerate(scope):
            parent_position, record, cardinality = child
            membership = record[0]["membership"]
            stem = f"child-{child_position:03d}"
            cnf_path, lrat_path = args.stage / f"{stem}.cnf", args.stage / f"{stem}.lrat"
            name = f"{producer.PREFIX}-child-{child_position:03d}-membership-{membership:03d}-k{cardinality}.lrat.xz"
            artifact = artifacts / name
            built = producer.build_child(child)
            producer.write_child(cnf_path, child_position, child, *built, manifest)
            structural.check(cnf_path)
            cnf_id = identity(cnf_path)
            start = time.monotonic_ns()
            solved = subprocess.run([str(solver), "--lrat", "--no-binary", "-q",
                                     "--restart=false", "--phase=false", "--seed=3",
                                     str(cnf_path), str(lrat_path)],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            solve_ns = time.monotonic_ns() - start
            if solved.returncode != 20:
                raise RuntimeError(f"child {child_position:03d} solver exit {solved.returncode}")
            lrat_id = identity(lrat_path)
            start = time.monotonic_ns()
            checked = subprocess.run([str(checker), str(cnf_path), str(lrat_path)],
                                     capture_output=True, text=True)
            check_ns = time.monotonic_ns() - start
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError(f"child {child_position:03d} LRAT rejected")
            with artifact.open("wb") as output:
                compressed = subprocess.run([str(XZ), "-3", "-c", str(lrat_path)], stdout=output)
            if compressed.returncode:
                raise RuntimeError(f"child {child_position:03d} compression failed")
            xz_id = identity(artifact)
            total_xz += xz_id[0]
            if total_xz >= LIMIT:
                raise RuntimeError("compressed certificate package reached exclusive cap")
            variables, clauses = producer.dimensions(child)
            rows.append((f"{child_position:03d}", f"{parent_position:03d}", f"{membership:03d}",
                         producer.hall.singleton.membership_key(record[1]), str(cardinality),
                         str(variables), str(clauses), str(cnf_id[0]), cnf_id[1], str(lrat_id[0]),
                         lrat_id[1], str(xz_id[0]), xz_id[1], str(solve_ns), str(check_ns),
                         f"certificates/{name}"))
            cnf_path.unlink()
            lrat_path.unlink()
            print(f"PASS {child_position + 1:02d}/28 membership={membership:03d} k={cardinality} "
                  f"xz={xz_id[0]} total={total_xz}", flush=True)
        with (args.stage / "rows.tsv").open("w", encoding="ascii", newline="\n") as handle:
            handle.write("columns\t" + ",".join(COLUMNS) + "\n")
            for row in rows:
                handle.write("\t".join(row) + "\n")
        print(f"PASS children=28 total_xz_bytes={total_xz}")
    except BaseException:
        shutil.rmtree(args.stage, ignore_errors=True)
        raise


if __name__ == "__main__":
    main()
