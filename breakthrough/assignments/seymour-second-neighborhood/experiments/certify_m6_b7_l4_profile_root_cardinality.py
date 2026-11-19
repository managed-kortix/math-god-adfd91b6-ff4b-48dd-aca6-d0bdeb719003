#!/usr/bin/env python3
"""Generate, check, and compress LRATs for all 40 B7-l4 profiles."""

import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import time

import check_m6_b7_l4_profile_root_cardinality as structural
import m6_b7_l4_profile_root_cardinality as producer

SOLVER_SHA256 = "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292"
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
XZ_SHA256 = "b5b163eb273291934556377ab883b4b2a5d4da50bd0dc0a91774ecc234ccd8d0"
COLUMNS = ("position", "key", "state-key", "t", "parents", "variables", "clauses", "cnf-bytes",
           "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes", "xz-sha256", "solve-nanoseconds",
           "check-nanoseconds", "artifact")


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
    xz = Path("/usr/bin/xz")
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
        profiles = producer.load_profiles()
        manifest = producer.manifest_payload(profiles)
        rows, total_xz = [], 0
        for position, profile in enumerate(profiles):
            cnf_path = args.stage / f"p{position:02d}.cnf"
            lrat_path = args.stage / f"p{position:02d}.lrat"
            name = f"{producer.PREFIX}-profile-{position:02d}.lrat.xz"
            artifact = artifacts / name
            built = producer.build(profile)
            producer.write_cnf(cnf_path, position, profile, *built, manifest)
            structural.check(cnf_path)
            cnf_id = identity(cnf_path)
            start = time.monotonic_ns()
            solved = subprocess.run([str(solver), "--lrat", "--no-binary", "-q", "--restart=false",
                                     "--phase=false", "--seed=3", str(cnf_path), str(lrat_path)],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            solve_ns = time.monotonic_ns() - start
            if solved.returncode != 20:
                raise RuntimeError(f"profile {position:02d} solver exit {solved.returncode}")
            lrat_id = identity(lrat_path)
            start = time.monotonic_ns()
            checked = subprocess.run([str(checker), str(cnf_path), str(lrat_path)],
                                     capture_output=True, text=True)
            check_ns = time.monotonic_ns() - start
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError(f"profile {position:02d} LRAT rejected")
            with artifact.open("wb") as output:
                subprocess.run([str(xz), "-3", "-c", str(lrat_path)], stdout=output, check=True)
            xz_id = identity(artifact)
            total_xz += xz_id[0]
            cnf = built[0]
            rows.append((f"{position:02d}", profile[0], profile[2], str(profile[4]), str(len(profile[7])),
                         str(len(cnf.names)), str(len(cnf.clauses)), str(cnf_id[0]), cnf_id[1],
                         str(lrat_id[0]), lrat_id[1], str(xz_id[0]), xz_id[1], str(solve_ns),
                         str(check_ns), f"certificates/{name}"))
            cnf_path.unlink()
            lrat_path.unlink()
            print(f"PASS {position + 1:02d}/40 profile={profile[0]} xz={xz_id[0]} total={total_xz}",
                  flush=True)
        with (args.stage / "rows.tsv").open("w", encoding="ascii", newline="\n") as handle:
            handle.write("columns\t" + ",".join(COLUMNS) + "\n")
            for row in rows:
                handle.write("\t".join(row) + "\n")
        print(f"PASS profiles=40 total_xz_bytes={total_xz}")
    except BaseException:
        shutil.rmtree(args.stage, ignore_errors=True)
        raise


if __name__ == "__main__":
    main()
