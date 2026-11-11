#!/usr/bin/env python3
"""Create checked LRATs for exactly 68 frozen exact-pair singleton scout-UNSAT memberships."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time

import check_m6_b7_l6_early_c_certificate_residual_exact_pair_singleton_parent as structural
import m6_b7_l6_early_c_certificate_residual_exact_pair_singleton_parent as producer

SOLVER_SHA256 = "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292"
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
XZ = Path("/usr/bin/xz")
XZ_SHA256 = "b5b163eb273291934556377ab883b4b2a5d4da50bd0dc0a91774ecc234ccd8d0"
LIMIT = 250_000_000
COLUMNS = (
    "membership", "key", "cell", "source-child", "parent", "selector", "variables",
    "clauses", "cnf-bytes", "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes",
    "xz-sha256", "solve-nanoseconds", "check-nanoseconds", "artifact",
)


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
        cells, memberships, manifest = structural.check_cover()
        structural.check_scout()
        scout = json.loads(structural.SCOUT.read_text(encoding="ascii"))
        scope = tuple(row["membership"] for row in scout["rows"] if row["status"] == "UNSAT")
        if len(scope) != 68 or scope != tuple(sorted(set(scope))):
            raise RuntimeError("scope is not exactly 68 ordered frozen scout-UNSAT memberships")
        produced_cells, produced_memberships = producer.load_memberships()
        checked_keys = tuple((member[0], member[1][0], member[1][1][0], member[2])
                             for member in memberships)
        produced_keys = tuple((member[0], member[1][0], member[1][1][0], member[2])
                              for member in produced_memberships)
        if produced_keys != checked_keys:
            raise RuntimeError("producer and independently checked membership universes differ")
        memberships = produced_memberships
        records, total_xz = [], 0
        for position, ordinal in enumerate(scope, 1):
            member = memberships[ordinal]
            cnf_path = args.stage / f"membership-{ordinal:03d}.cnf"
            lrat_path = args.stage / f"membership-{ordinal:03d}.lrat"
            name = f"{producer.PREFIX}-membership-{ordinal:03d}.lrat.xz"
            artifact = artifacts / name
            cnf, selectors = producer.build_membership(member)
            producer.write_membership(cnf_path, ordinal, member, cnf, selectors, manifest)
            structural.check(cnf_path)
            cnf_id = identity(cnf_path)
            solve_start = time.monotonic_ns()
            solved = subprocess.run(
                [str(solver), "--lrat", "--no-binary", "-q", str(cnf_path), str(lrat_path)],
                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
            )
            solve_ns = time.monotonic_ns() - solve_start
            if solved.returncode != 20:
                raise RuntimeError(f"membership {ordinal:03d} solver exit {solved.returncode}, expected 20")
            lrat_id = identity(lrat_path)
            check_start = time.monotonic_ns()
            checked = subprocess.run([str(checker), str(cnf_path), str(lrat_path)],
                                     capture_output=True, text=True)
            check_ns = time.monotonic_ns() - check_start
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError(f"membership {ordinal:03d} LRAT rejected")
            with artifact.open("wb") as output:
                compressed = subprocess.run([str(XZ), "-3", "-c", str(lrat_path)], stdout=output)
            if compressed.returncode:
                raise RuntimeError(f"membership {ordinal:03d} compression failed")
            xz_id = identity(artifact)
            total_xz += xz_id[0]
            if total_xz >= LIMIT:
                raise RuntimeError(f"compressed total {total_xz} is not below {LIMIT}")
            cell, record, parent = member
            variables, clauses = producer.dimensions(member)
            records.append((
                f"{ordinal:03d}", producer.membership_key(member), f"{cell:03d}",
                f"{record[0]:03d}", f"{parent:02d}", str(selectors[parent]), str(variables),
                str(clauses), str(cnf_id[0]), cnf_id[1], str(lrat_id[0]), lrat_id[1],
                str(xz_id[0]), xz_id[1], str(solve_ns), str(check_ns), f"certificates/{name}",
            ))
            cnf_path.unlink()
            lrat_path.unlink()
            print(f"PASS {position:02d}/68 membership={ordinal:03d} xz={xz_id[0]} total={total_xz}",
                  flush=True)
        rows = args.stage / "rows.tsv"
        with rows.open("w", encoding="ascii", newline="\n") as handle:
            handle.write("columns\t" + ",".join(COLUMNS) + "\n")
            for record in records:
                handle.write("\t".join(record) + "\n")
        print(f"PASS memberships=68 total_xz_bytes={total_xz} rows={rows}")
    except BaseException:
        shutil.rmtree(args.stage, ignore_errors=True)
        raise


if __name__ == "__main__":
    main()
