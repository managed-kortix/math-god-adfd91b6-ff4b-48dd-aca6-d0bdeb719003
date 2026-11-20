#!/usr/bin/env python3
"""Optional deterministic reproduction of the retained family-S h=1 DRAT.

This is separate from proof validity.  The default package verifier checks the
retained proof with package-local drat-trim and never invokes this solver.
"""
from __future__ import annotations

import argparse
import hashlib
import lzma
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent.parent
CNF = PACKAGE / "artifacts" / "h1-parent.cnf"
RETAINED = PACKAGE / "artifacts" / "h1-parent.drat.xz"
DEFAULT_SOLVER = PACKAGE / "tools" / "cadical-1.7.3"
EXPECTED_SOLVER = (1_002_216, "ff471d3c6b54fbbc161d65545a5f788d0032ad05b9aff4e2c748d9639400e951")
EXPECTED_CNF = (5_891_576, "31db9866c15372555f9c102b3126fb4e8730f879b5e82ca5f6791318398d4e43")
EXPECTED_RAW = (30_989_483, "32f35d5b3b0458c05f59bcf4467f3bb40103294e0100d7ba8276c2972cfa9de9")
EXPECTED_XZ = (2_471_364, "089e6ded1354db86151092c0603ca1d8aa5397bf7b4b7916c71ad6830375eaba")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def identity(path: Path) -> tuple[int, str]:
    hasher = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            size += len(chunk)
            hasher.update(chunk)
    return size, hasher.hexdigest()


def regular(path: Path, executable: bool = False) -> None:
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and not path.is_symlink(), f"not a regular nonsymlink: {path}")
    if executable:
        require(os.access(path, os.X_OK), f"not executable: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--solver",
        type=Path,
        default=DEFAULT_SOLVER,
        help="path to the exact pinned CaDiCaL binary (defaults to the package-local copy)",
    )
    parser.add_argument("--timeout", type=int, default=300, help="solver timeout in seconds")
    args = parser.parse_args()
    require(type(args.timeout) is int and args.timeout > 0, "timeout must be positive")

    regular(CNF)
    regular(RETAINED)
    regular(args.solver, executable=True)
    require(identity(CNF) == EXPECTED_CNF, "retained CNF identity changed")
    require(identity(args.solver) == EXPECTED_SOLVER, "pinned CaDiCaL identity changed")

    with tempfile.TemporaryDirectory(prefix="h1-proof-reproduce-") as directory:
        raw_path = Path(directory) / "h1-parent.drat"
        result = subprocess.run(
            [str(args.solver.resolve()), "-t", str(args.timeout), str(CNF), str(raw_path)],
            cwd=PACKAGE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="strict",
            timeout=args.timeout + 30,
        )
        require(result.returncode == 20, f"CaDiCaL did not return UNSAT exit 20:\n{result.stdout[-4000:]}")
        require("s UNSATISFIABLE" in result.stdout, "CaDiCaL UNSAT marker absent")
        require(identity(raw_path) == EXPECTED_RAW, "fresh raw DRAT differs from retained identity")
        packed = lzma.compress(raw_path.read_bytes(), format=lzma.FORMAT_XZ, preset=9)
        packed_identity = len(packed), hashlib.sha256(packed).hexdigest()
        require(packed_identity == EXPECTED_XZ, "fresh deterministic XZ-9 proof identity changed")
        require(packed == RETAINED.read_bytes(), "fresh deterministic XZ-9 proof differs bytewise")

    print(
        "PASS optional proof reproduction "
        f"raw_bytes={EXPECTED_RAW[0]} raw_sha256={EXPECTED_RAW[1]}"
    )
    print(
        "PASS deterministic XZ-9 reproduction "
        f"bytes={EXPECTED_XZ[0]} sha256={EXPECTED_XZ[1]}"
    )


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
