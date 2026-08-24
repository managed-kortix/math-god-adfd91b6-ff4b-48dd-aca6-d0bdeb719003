#!/usr/bin/env python3
"""Create checked LRATs for exactly 172 frozen inaccessible-pair scout-UNSAT children."""

import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import time

import check_m6_b7_l6_early_c_inaccessible_pair_orbits as structural
import m6_b7_l6_early_c_inaccessible_pair_orbits as producer

SOLVER_SHA256 = "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292"
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
XZ = Path("/usr/bin/xz")
XZ_SHA256 = "b5b163eb273291934556377ab883b4b2a5d4da50bd0dc0a91774ecc234ccd8d0"
LIMIT = 250_000_000
COLUMNS = (
    "child", "key", "profile", "parents", "variables", "clauses", "cnf-bytes",
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
    solver, checker = args.solver.resolve(strict=True), args.checker.resolve(strict=True)
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
        children = producer.load_children()
        manifest = producer.manifest_payload(children)
        hashes = structural.load_hashes(manifest)
        structural.check_scout(manifest, hashes)
        scout = __import__("json").loads(structural.SCOUT.read_text(encoding="ascii"))
        scope = tuple(row["child"] for row in scout["rows"] if row["status"] == "UNSAT")
        if len(scope) != 172 or "".join("U" if row["status"] == "UNSAT" else "T"
                                        for row in scout["rows"]) != structural.STATUS_SEQUENCE:
            raise RuntimeError("scope is not exactly the frozen 172-child scout-UNSAT sequence")
        records, total_xz = [], 0
        for position, ordinal in enumerate(scope, 1):
            child = children[ordinal]
            cnf_path = args.stage / f"child-{ordinal:03d}.cnf"
            lrat_path = args.stage / f"child-{ordinal:03d}.lrat"
            name = f"m6-b7-l6-early-c-inaccessible-pair-child-{ordinal:03d}.lrat.xz"
            artifact = artifacts / name
            cnf, selectors = producer.build_child(child)
            producer.write_child(cnf_path, ordinal, child, cnf, selectors, manifest)
            structural.check(cnf_path)
            cnf_id = identity(cnf_path)
            solve_start = time.monotonic_ns()
            solved = subprocess.run(
                [str(solver), "--lrat", "--no-binary", "-q", str(cnf_path), str(lrat_path)],
                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False,
            )
            solve_ns = time.monotonic_ns() - solve_start
            if solved.returncode != 20:
                raise RuntimeError(f"child {ordinal:03d} solver exit {solved.returncode}, expected 20")
            lrat_id = identity(lrat_path)
            check_start = time.monotonic_ns()
            checked = subprocess.run([str(checker), str(cnf_path), str(lrat_path)],
                                     capture_output=True, text=True)
            check_ns = time.monotonic_ns() - check_start
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError(f"child {ordinal:03d} LRAT rejected")
            with artifact.open("wb") as output:
                compressed = subprocess.run([str(XZ), "-3", "-c", str(lrat_path)], stdout=output)
            if compressed.returncode:
                raise RuntimeError(f"child {ordinal:03d} compression failed")
            xz_id = identity(artifact)
            total_xz += xz_id[0]
            if total_xz >= LIMIT:
                raise RuntimeError(f"compressed total {total_xz} is not below {LIMIT}")
            variables, clauses = producer.dimensions(child)
            records.append((
                f"{ordinal:03d}", child[0], f"{child[1]:02d}", str(len(child[5])),
                str(variables), str(clauses), str(cnf_id[0]), cnf_id[1], str(lrat_id[0]),
                lrat_id[1], str(xz_id[0]), xz_id[1], str(solve_ns), str(check_ns),
                f"certificates/{name}",
            ))
            cnf_path.unlink()
            lrat_path.unlink()
            print(f"PASS {position:03d}/172 child={ordinal:03d} xz={xz_id[0]} total={total_xz}",
                  flush=True)
        rows = args.stage / "rows.tsv"
        with rows.open("w", encoding="ascii", newline="\n") as handle:
            handle.write("columns\t" + ",".join(COLUMNS) + "\n")
            for record in records:
                handle.write("\t".join(record) + "\n")
        print(f"PASS children=172 total_xz_bytes={total_xz} rows={rows}")
    except BaseException:
        shutil.rmtree(args.stage, ignore_errors=True)
        raise


if __name__ == "__main__":
    main()
