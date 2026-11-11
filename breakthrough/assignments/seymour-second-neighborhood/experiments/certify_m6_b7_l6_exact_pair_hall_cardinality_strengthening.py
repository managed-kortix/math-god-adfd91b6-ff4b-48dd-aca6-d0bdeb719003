#!/usr/bin/env python3
"""Generate, check, and compress LRATs for all 33 unsplit cardinality CNFs."""

import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import time

import check_m6_b7_l6_exact_pair_hall_cardinality_strengthening as structural
import m6_b7_l6_exact_pair_hall_cardinality_strengthening as producer

SOLVER_SHA256 = "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292"
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
XZ_SHA256 = "b5b163eb273291934556377ab883b4b2a5d4da50bd0dc0a91774ecc234ccd8d0"
LIMIT = 250_000_000
COLUMNS = ("position", "membership", "key", "cell", "parent", "selector", "hall-U", "hall-S",
           "variables", "clauses", "cnf-bytes", "cnf-sha256", "lrat-bytes", "lrat-sha256",
           "xz-bytes", "xz-sha256", "solve-nanoseconds", "check-nanoseconds", "artifact")


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
    solver, checker, xz = args.solver.resolve(strict=True), args.checker.resolve(strict=True), Path("/usr/bin/xz")
    if identity(solver)[1] != SOLVER_SHA256 or identity(checker)[1] != CHECKER_SHA256 or \
            identity(xz)[1] != XZ_SHA256:
        parser.error("solver, checker, or compressor identity differs")
    if args.stage.exists():
        parser.error("stage path already exists")
    args.stage.mkdir()
    artifacts = args.stage / "artifacts"
    artifacts.mkdir()
    try:
        structural.check_cover(regenerate=False)
        records = producer.scope()
        manifest = producer.manifest_payload(records)
        rows, total_xz = [], 0
        for position, record in enumerate(records):
            membership = record[0]["membership"]
            cnf_path, lrat_path = args.stage / f"p{position:03d}.cnf", args.stage / f"p{position:03d}.lrat"
            name = f"{producer.PREFIX}-position-{position:03d}-membership-{membership:03d}.lrat.xz"
            artifact = artifacts / name
            built = producer.build_membership(record)
            producer.write_membership(cnf_path, position, record, *built, manifest)
            structural.check(cnf_path)
            cnf_id = identity(cnf_path)
            start = time.monotonic_ns()
            solved = subprocess.run([str(solver), "--lrat", "--no-binary", "-q", "--restart=false",
                                     "--phase=false", "--seed=3", str(cnf_path), str(lrat_path)],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            solve_ns = time.monotonic_ns() - start
            if solved.returncode != 20:
                raise RuntimeError(f"position {position:03d} solver exit {solved.returncode}")
            lrat_id = identity(lrat_path)
            start = time.monotonic_ns()
            checked = subprocess.run([str(checker), str(cnf_path), str(lrat_path)], capture_output=True, text=True)
            check_ns = time.monotonic_ns() - start
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError(f"position {position:03d} LRAT rejected")
            with artifact.open("wb") as output:
                if subprocess.run([str(xz), "-3", "-c", str(lrat_path)], stdout=output).returncode:
                    raise RuntimeError("compression failed")
            xz_id = identity(artifact)
            total_xz += xz_id[0]
            if total_xz >= LIMIT:
                raise RuntimeError("compressed package reached exclusive cap")
            row, member = record
            cnf, selectors, universe, support, _ = built
            rows.append((f"{position:03d}", f"{membership:03d}", producer.hall.singleton.membership_key(member),
                         f"{member[0]:03d}", f"{member[2]:02d}", str(selectors[member[2]]),
                         ",".join(map(str, universe)), ",".join(map(str, support)), str(len(cnf.names)),
                         str(len(cnf.clauses)), str(cnf_id[0]), cnf_id[1], str(lrat_id[0]), lrat_id[1],
                         str(xz_id[0]), xz_id[1], str(solve_ns), str(check_ns), f"certificates/{name}"))
            cnf_path.unlink()
            lrat_path.unlink()
            print(f"PASS {position + 1:02d}/33 position={position:03d} xz={xz_id[0]} total={total_xz}", flush=True)
        with (args.stage / "rows.tsv").open("w", encoding="ascii", newline="\n") as handle:
            handle.write("columns\t" + ",".join(COLUMNS) + "\n")
            for row in rows:
                handle.write("\t".join(row) + "\n")
        print(f"PASS memberships=33 total_xz_bytes={total_xz}")
    except BaseException:
        shutil.rmtree(args.stage, ignore_errors=True)
        raise


if __name__ == "__main__":
    main()
