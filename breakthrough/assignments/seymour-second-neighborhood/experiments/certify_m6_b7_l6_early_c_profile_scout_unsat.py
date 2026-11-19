#!/usr/bin/env python3
"""Create checked LRATs for exactly 26 selected frozen early-profile cells."""

import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import time

import check_m6_b7_l6_early_c_profile_census as structural
import m6_b7_l6_early_c_profile_census as producer

HERE = Path(__file__).resolve().parent
SOLVER_SHA256 = "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292"
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
XZ = Path("/usr/bin/xz")
XZ_SHA256 = "b5b163eb273291934556377ab883b4b2a5d4da50bd0dc0a91774ecc234ccd8d0"
LIMIT = 250_000_000
SCOPE = (0, 1, 2, 6, 7, 8, 9, 10, 18, 19, 20, 21, 22, 24, 26, 27, 29,
         30, 44, 45, 46, 48, 50, 51, 52, 53)
COLUMNS = (
    "orbit", "key", "parents", "variables", "clauses", "cnf-bytes", "cnf-sha256",
    "lrat-bytes", "lrat-sha256", "xz-bytes", "xz-sha256", "solve-nanoseconds",
    "check-nanoseconds", "artifact",
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
    solver = args.solver.resolve(strict=True)
    checker = args.checker.resolve(strict=True)
    if identity(solver)[1] != SOLVER_SHA256:
        parser.error("solver is not pinned CaDiCaL 1.7.3")
    if identity(checker)[1] != CHECKER_SHA256:
        parser.error("checker is not pinned lrat-check")
    if identity(XZ)[1] != XZ_SHA256:
        parser.error("/usr/bin/xz is not the pinned compressor")
    if args.stage.exists():
        parser.error("stage path already exists")
    args.stage.mkdir(parents=False)
    artifacts = args.stage / "artifacts"
    artifacts.mkdir()
    try:
        orbits = producer.load_orbits()
        manifest = producer.manifest_payload(orbits)
        scout = {ordinal: status for ordinal, status, _, _ in producer.scout_sequence(orbits)}
        if tuple(ordinal for ordinal in SCOPE if scout.get(ordinal) == "UNSAT") != SCOPE:
            raise RuntimeError("scope is not entirely inside the frozen SCOUT-UNSAT set")
        records, total_xz = [], 0
        for position, ordinal in enumerate(SCOPE, 1):
            orbit = orbits[ordinal]
            cnf_path = args.stage / f"orbit-{ordinal:02d}.cnf"
            lrat_path = args.stage / f"orbit-{ordinal:02d}.lrat"
            name = f"m6-b7-l6-early-c-profile-orbit-{ordinal:02d}.lrat.xz"
            artifact = artifacts / name
            cnf, selectors = producer.build_orbit(orbit)
            producer.write_orbit(cnf_path, ordinal, orbit, cnf, selectors, manifest)
            structural.check(cnf_path)
            cnf_id = identity(cnf_path)
            solve_start = time.monotonic_ns()
            solved = subprocess.run(
                [str(solver), "--lrat", "--no-binary", "-q", str(cnf_path), str(lrat_path)],
                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False,
            )
            solve_ns = time.monotonic_ns() - solve_start
            if solved.returncode != 20:
                raise RuntimeError(f"orbit {ordinal:02d} solver exit {solved.returncode}, expected 20")
            lrat_id = identity(lrat_path)
            check_start = time.monotonic_ns()
            checked = subprocess.run(
                [str(checker), str(cnf_path), str(lrat_path)], capture_output=True, text=True,
            )
            check_ns = time.monotonic_ns() - check_start
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError(f"orbit {ordinal:02d} LRAT rejected")
            with artifact.open("wb") as output:
                compressed = subprocess.run([str(XZ), "-3", "-c", str(lrat_path)], stdout=output)
            if compressed.returncode:
                raise RuntimeError(f"orbit {ordinal:02d} compression failed")
            xz_id = identity(artifact)
            total_xz += xz_id[0]
            if total_xz > LIMIT:
                raise RuntimeError(f"compressed total {total_xz} exceeds {LIMIT}")
            variables, clauses = producer.dimensions(len(orbit[7]))
            records.append((
                f"{ordinal:02d}", orbit[0], str(len(orbit[7])), str(variables), str(clauses),
                str(cnf_id[0]), cnf_id[1], str(lrat_id[0]), lrat_id[1], str(xz_id[0]),
                xz_id[1], str(solve_ns), str(check_ns), f"certificates/{name}",
            ))
            cnf_path.unlink()
            lrat_path.unlink()
            print(f"PASS {position:02d}/26 orbit={ordinal:02d} xz={xz_id[0]} total={total_xz}", flush=True)
        rows = args.stage / "rows.tsv"
        with rows.open("w", encoding="ascii", newline="\n") as handle:
            handle.write("columns\t" + ",".join(COLUMNS) + "\n")
            for record in records:
                handle.write("\t".join(record) + "\n")
        print(f"PASS orbits=26 total_xz_bytes={total_xz} rows={rows}")
    except BaseException:
        shutil.rmtree(args.stage, ignore_errors=True)
        raise


if __name__ == "__main__":
    main()
