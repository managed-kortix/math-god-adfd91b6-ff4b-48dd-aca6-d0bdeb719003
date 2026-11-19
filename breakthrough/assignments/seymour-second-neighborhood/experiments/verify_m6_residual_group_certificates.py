#!/usr/bin/env python3
"""Regenerate and verify the durable checked residual m=6 LRAT artifacts."""

import argparse
import hashlib
import lzma
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGER = HERE / "m6-residual-group-certificates.tsv"
MANIFEST = HERE / "m6-residual-selector-groups.tsv"
GROUPS = ("B6-l4-r0-t2", "B6-l4-r1-t3", "B6-l5-r2-t3", "B7-l6-r3-t0")
MEMBERS = (6679, 6679, 1910, 42)
LEDGER_IDENTITY = (2430, "1785f4d9b0120a0beeccc959a0075e7136379da8579978ab1c95d8fff2f2c7f2")
COLUMNS = (
    "group", "members", "cnf-bytes", "cnf-sha256", "lrat-bytes", "lrat-sha256",
    "xz-bytes", "xz-sha256", "generate-seconds", "structure-seconds",
    "solve-seconds", "check-seconds", "compress-seconds", "artifact",
)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def identity(path):
    return path.stat().st_size, sha256(path)


def load_ledger(path):
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != "m6-residual-group-certificates-v1":
        raise RuntimeError("unexpected certificate ledger format")
    metadata, records, columns = {}, [], None
    seen_columns = False
    for line in lines[1:]:
        fields = line.split("\t")
        if fields[0] == "columns":
            if seen_columns:
                raise RuntimeError("duplicate certificate ledger columns")
            seen_columns = True
            columns = tuple(fields[1].split(","))
            if columns != COLUMNS:
                raise RuntimeError("unexpected certificate ledger columns")
        elif columns is None:
            if len(fields) != 2 or fields[0] in metadata:
                raise RuntimeError("malformed certificate ledger metadata")
            metadata[fields[0]] = fields[1]
        else:
            if len(fields) != len(columns):
                raise RuntimeError("malformed certificate ledger record")
            records.append(dict(zip(columns, fields)))
    expected_metadata = {
        "generated-utc", "timing-clock", "compression", "solver",
        "solver-source-commit", "solver-binary-sha256", "solver-command",
        "solver-required-exit", "checker", "checker-source-commit",
        "checker-binary-sha256", "checker-required-output",
        "group-manifest-bytes", "group-manifest-sha256", "groups",
        "memberships", "total-lrat-bytes", "total-xz-bytes",
    }
    if set(metadata) != expected_metadata or not seen_columns:
        raise RuntimeError("certificate ledger metadata keys changed")
    if tuple(record["group"] for record in records) != GROUPS:
        raise RuntimeError("certificate ledger group order is incomplete")
    if tuple(int(record["members"]) for record in records) != MEMBERS:
        raise RuntimeError("certificate ledger membership counts changed")
    if metadata.get("groups") != "4" or metadata.get("memberships") != str(sum(MEMBERS)):
        raise RuntimeError("certificate ledger dimensions changed")
    totals = {
        "total-lrat-bytes": sum(int(record["lrat-bytes"]) for record in records),
        "total-xz-bytes": sum(int(record["xz-bytes"]) for record in records),
    }
    if any(metadata.get(name) != str(total) for name, total in totals.items()):
        raise RuntimeError("certificate ledger byte totals are inconsistent")
    if totals["total-xz-bytes"] >= 200_000_000:
        raise RuntimeError("durable proof artifacts are not below 200MB")
    return metadata, records


def require_identity(path, expected_bytes, expected_hash, label):
    expected = int(expected_bytes), expected_hash
    actual = identity(path)
    if actual != expected:
        raise RuntimeError(f"{label} identity mismatch: expected {expected}, got {actual}")


def run(command, label, **kwargs):
    result = subprocess.run(command, **kwargs)
    if result.returncode:
        raise RuntimeError(f"{label} failed with exit {result.returncode}")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--keep-cnf", action="store_true")
    args = parser.parse_args()
    require_identity(args.ledger, LEDGER_IDENTITY[0], LEDGER_IDENTITY[1], "certificate ledger")
    metadata, records = load_ledger(args.ledger)
    require_identity(MANIFEST, metadata["group-manifest-bytes"],
                     metadata["group-manifest-sha256"], "residual group manifest")
    if sha256(args.checker) != metadata["checker-binary-sha256"]:
        raise RuntimeError("checker binary is not the pinned executable")

    with tempfile.TemporaryDirectory(prefix="m6-residual-group-verify-") as directory:
        work = Path(directory)
        for record in records:
            group = record["group"]
            relative = Path(record["artifact"])
            if (relative.is_absolute() or ".." in relative.parts or not relative.parts or
                    relative.parts[0] != "certificates"):
                raise RuntimeError(f"{group} artifact path is outside the certificate directory")
            expected_relative = Path("certificates") / f"m6-residual-{group}.lrat.xz"
            if relative != expected_relative:
                raise RuntimeError(f"{group} artifact path differs from the frozen filename")
            artifact = ROOT / relative
            require_identity(artifact, record["xz-bytes"], record["xz-sha256"], f"{group} xz")

            cnf = work / f"{group}.cnf"
            run(
                [sys.executable, str(HERE / "m6_residual_group_cnf.py"), "--group", group,
                 "--output", str(cnf)],
                f"{group} regeneration", cwd=HERE, stdout=subprocess.DEVNULL,
            )
            require_identity(cnf, record["cnf-bytes"], record["cnf-sha256"], f"{group} CNF")
            run(
                [sys.executable, str(HERE / "check_m6_residual_group_cnf.py"), str(cnf)],
                f"{group} structural check", cwd=HERE, stdout=subprocess.DEVNULL,
            )

            lrat = work / f"{group}.lrat"
            with lzma.open(artifact, "rb") as source, lrat.open("wb") as target:
                while block := source.read(1 << 20):
                    target.write(block)
            require_identity(lrat, record["lrat-bytes"], record["lrat-sha256"], f"{group} LRAT")
            checked = subprocess.run(
                [str(args.checker), str(cnf), str(lrat)], capture_output=True, text=True
            )
            if checked.returncode or metadata["checker-required-output"] not in checked.stdout:
                raise RuntimeError(f"{group} LRAT was not accepted by the pinned checker")
            print(
                f"PASS group={group} cnf_bytes={record['cnf-bytes']} "
                f"lrat_bytes={record['lrat-bytes']} xz_bytes={record['xz-bytes']}"
            )
            lrat.unlink()
            if not args.keep_cnf:
                cnf.unlink()
    print(
        f"PASS groups=4 memberships={sum(MEMBERS)} "
        f"total_xz_bytes={metadata['total-xz-bytes']}"
    )


if __name__ == "__main__":
    main()
