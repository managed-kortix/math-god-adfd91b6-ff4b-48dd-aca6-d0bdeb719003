#!/usr/bin/env python3
"""Generate and check the two compact LRATs for the frozen (3,1) campaign."""

import argparse
import hashlib
import shutil
import subprocess
import time
from pathlib import Path

import check_m6_b7_l6_c_to_b_31_orbits as checker
import m6_b7_l6_c_to_b_31_orbits as producer

SOLVER_SHA256 = "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292"
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
LIMIT = 250_000_000


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
        parser.error("solver is not pinned CaDiCaL 1.7.3")
    if identity(args.checker)[1] != CHECKER_SHA256:
        parser.error("checker is not the pinned lrat-check")
    if args.stage.exists():
        parser.error("stage already exists")
    args.stage.mkdir()
    artifacts = args.stage / "artifacts"
    artifacts.mkdir()
    try:
        all_parents, parents = producer.load_parents()
        manifest = producer.manifest_payload(all_parents, parents)
        records, total = [], 0
        for t in (0, 1):
            cnf_path = args.stage / f"t{t}.cnf"
            lrat_path = args.stage / f"t{t}.lrat"
            artifact = artifacts / f"m6-b7-l6-c-to-b-31-t{t}.lrat.xz"
            cnf, selectors = producer.build_group(t, parents)
            producer.write_group(cnf_path, t, cnf, selectors, manifest, parents)
            checker.check(cnf_path)
            solve_start = time.monotonic_ns()
            solved = subprocess.run([str(args.solver), "--lrat", "--no-binary", "-q",
                                     str(cnf_path), str(lrat_path)], stdout=subprocess.DEVNULL)
            solve_ns = time.monotonic_ns() - solve_start
            if solved.returncode != 20:
                raise RuntimeError(f"t={t} did not solve UNSAT")
            check_start = time.monotonic_ns()
            checked = subprocess.run([str(args.checker), str(cnf_path), str(lrat_path)],
                                     capture_output=True, text=True)
            check_ns = time.monotonic_ns() - check_start
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError(f"t={t} LRAT rejected")
            with artifact.open("wb") as output:
                compressed = subprocess.run(["xz", "-3", "-c", str(lrat_path)], stdout=output)
            if compressed.returncode:
                raise RuntimeError(f"t={t} compression failed")
            total += artifact.stat().st_size
            if total >= LIMIT:
                raise RuntimeError("compressed proof total is not below 250MB")
            records.append((t, identity(cnf_path), identity(lrat_path), identity(artifact), solve_ns, check_ns))
            cnf_path.unlink()
            lrat_path.unlink()
        rows = args.stage / "rows.tsv"
        with rows.open("w", encoding="ascii", newline="\n") as handle:
            handle.write("columns\tt,cnf-bytes,cnf-sha256,lrat-bytes,lrat-sha256,xz-bytes,xz-sha256,solve-nanoseconds,check-nanoseconds,artifact\n")
            for t, cnf_id, lrat_id, xz_id, solve_ns, check_ns in records:
                handle.write(f"{t}\t{cnf_id[0]}\t{cnf_id[1]}\t{lrat_id[0]}\t{lrat_id[1]}\t"
                             f"{xz_id[0]}\t{xz_id[1]}\t{solve_ns}\t{check_ns}\t"
                             f"certificates/m6-b7-l6-c-to-b-31-t{t}.lrat.xz\n")
        print(f"PASS groups=2 total_xz_bytes={total} rows={rows}")
    except BaseException:
        shutil.rmtree(args.stage, ignore_errors=True)
        raise


if __name__ == "__main__":
    main()
