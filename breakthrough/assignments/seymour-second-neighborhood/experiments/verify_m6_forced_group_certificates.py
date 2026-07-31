#!/usr/bin/env python3
"""Regenerate and verify every durable m=6 forced-group LRAT artifact."""

import argparse
import hashlib
import lzma
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGER = HERE / "m6-forced-group-certificates.tsv"
GROUPS = ("B6-q0", "B6-q1", "B6-q2", "B6-q3", "B7-q1", "B7-q2", "B7-q3", "B7-q4", "B7-q5")
COLUMNS = (
    "group", "cnf-bytes", "cnf-sha256", "lrat-bytes", "lrat-sha256",
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
    if not lines or lines[0] != "m6-forced-group-certificates-v1":
        raise RuntimeError("unexpected certificate ledger format")
    metadata = {}
    records = []
    columns = None
    for line in lines[1:]:
        fields = line.split("\t")
        if fields[0] == "columns":
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
    if tuple(record["group"] for record in records) != GROUPS:
        raise RuntimeError("certificate ledger group order is incomplete")
    if metadata.get("groups") != "9" or metadata.get("rows") != "31568":
        raise RuntimeError("certificate ledger dimensions changed")
    total = sum(int(record["xz-bytes"]) for record in records)
    if total != int(metadata.get("total-xz-bytes", "-1")):
        raise RuntimeError("certificate ledger compressed total is inconsistent")
    return metadata, records


def require_identity(path, expected_bytes, expected_hash, label):
    actual = identity(path)
    expected = int(expected_bytes), expected_hash
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
    metadata, records = load_ledger(args.ledger)
    proof_source = ROOT / "attempts" / "tick51-b7-q0-human-proof.md"
    if identity(proof_source) != (3055, "506c0750df64f01885f01f7d8674c70a7a9b5d2885b42a7471c8dd1ed5783a71"):
        raise RuntimeError("human-closed B7-q0 proof source identity changed")
    checker_hash = sha256(args.checker)
    if checker_hash != metadata["checker-binary-sha256"]:
        raise RuntimeError("checker binary is not the pinned executable")

    with tempfile.TemporaryDirectory(prefix="m6-forced-group-verify-") as directory:
        work = Path(directory)
        for record in records:
            group = record["group"]
            relative = Path(record["artifact"])
            if relative.is_absolute() or ".." in relative.parts or not relative.parts or relative.parts[0] != "certificates":
                raise RuntimeError(f"{group} artifact path is outside the certificate directory")
            artifact = ROOT / relative
            require_identity(artifact, record["xz-bytes"], record["xz-sha256"], f"{group} xz")

            cnf = work / f"{group}.cnf"
            run(
                [sys.executable, str(HERE / "m6_forced_group_cnf.py"), "--group", group, "--output", str(cnf)],
                f"{group} regeneration",
                cwd=HERE,
                stdout=subprocess.DEVNULL,
            )
            require_identity(cnf, record["cnf-bytes"], record["cnf-sha256"], f"{group} CNF")
            run(
                [sys.executable, str(HERE / "check_m6_forced_group_cnf.py"), str(cnf)],
                f"{group} structural check",
                cwd=HERE,
                stdout=subprocess.DEVNULL,
            )

            lrat = work / f"{group}.lrat"
            with lzma.open(artifact, "rb") as source, lrat.open("wb") as target:
                while block := source.read(1 << 20):
                    target.write(block)
            require_identity(lrat, record["lrat-bytes"], record["lrat-sha256"], f"{group} LRAT")
            checked = subprocess.run(
                [str(args.checker), str(cnf), str(lrat)], capture_output=True, text=True
            )
            if checked.returncode or "c VERIFIED" not in checked.stdout:
                raise RuntimeError(f"{group} LRAT was not accepted by the pinned checker")
            print(
                f"PASS group={group} cnf_bytes={record['cnf-bytes']} "
                f"lrat_bytes={record['lrat-bytes']} xz_bytes={record['xz-bytes']}"
            )
            lrat.unlink()
            if not args.keep_cnf:
                cnf.unlink()
    print(f"PASS groups=9 rows=31568 total_xz_bytes={metadata['total-xz-bytes']}")


if __name__ == "__main__":
    main()
