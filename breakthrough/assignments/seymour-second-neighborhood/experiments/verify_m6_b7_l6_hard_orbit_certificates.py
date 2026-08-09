#!/usr/bin/env python3
"""Strictly regenerate and replay exactly the 14 scout-UNSAT hard-orbit leaves."""

import argparse
import hashlib
import json
import lzma
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGER = HERE / "m6-b7-l6-hard-orbit-certificates.tsv"
LEDGER_IDENTITY = (6987, "cd46a986097405c2d270f15f2525df67e586cc53137e09ef5eafeafd42f2bd02")
FORMAT = "m6-b7-l6-hard-orbit-certificates-v1"
ORDINALS = (7, 9, 10, 18, 20, 21, 22, 26, 27, 28, 29, 34, 35, 38)
SOURCE_PATHS = {
    "orbit-manifest": HERE / "m6-b7-l6-hard-orbits.tsv",
    "orbit-hash-ledger": HERE / "m6-b7-l6-hard-orbit-hashes.tsv",
    "orbit-scout": HERE / "m6-b7-l6-hard-orbit-scout-20s.json",
    "orbit-producer": HERE / "m6_b7_l6_hard_orbits.py",
    "orbit-structural-checker": HERE / "check_m6_b7_l6_hard_orbits.py",
    "state-manifest": HERE / "m6-b7-l6-state-split.tsv",
    "state-hash-ledger": HERE / "m6-b7-l6-state-leaf-hashes.tsv",
    "state-scout": HERE / "m6-b7-l6-state-scout-30s.json",
    "state-certificate-ledger": HERE / "m6-b7-l6-state-certificates.tsv",
    "state-producer": HERE / "m6_b7_l6_state_split.py",
    "state-structural-checker": HERE / "check_m6_b7_l6_state_split.py",
    "clean-parent-manifest": HERE / "m6-clean-sink-selector-groups.tsv",
    "clean-remaining-stream": HERE / "m6-clean-sink-remaining.tsv",
    "clean-partition-manifest": HERE / "m6-clean-sink-manifest.tsv",
    "clean-sink-theorem": ROOT / "attempts" / "tick52-rooted-clean-sink-theorem.md",
    "clean-group-producer": HERE / "m6_clean_sink_group_cnf.py",
    "clean-group-checker": HERE / "check_m6_clean_sink_group_cnf.py",
}
COLUMNS = (
    "leaf-ordinal", "key", "parents", "variables", "clauses", "cnf-bytes",
    "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes", "xz-sha256", "artifact",
)


def identity(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            digest.update(block)
    return path.stat().st_size, digest.hexdigest()


def require_identity(path, size, digest, label):
    actual, expected = identity(path), (int(size), digest)
    if actual != expected:
        raise RuntimeError(f"{label} identity mismatch: expected {expected}, got {actual}")


def load_ledger(path):
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != FORMAT:
        raise RuntimeError("unexpected certificate ledger format")
    metadata, records, columns = {}, [], None
    for line in lines[1:]:
        fields = line.split("\t")
        if fields[0] == "columns":
            if columns is not None or tuple(fields[1].split(",")) != COLUMNS:
                raise RuntimeError("certificate columns changed")
            columns = COLUMNS
        elif columns is None:
            if len(fields) != 2 or fields[0] in metadata:
                raise RuntimeError("malformed certificate metadata")
            metadata[fields[0]] = fields[1]
        else:
            if len(fields) != len(COLUMNS):
                raise RuntimeError("malformed certificate row")
            records.append(dict(zip(COLUMNS, fields)))
    required = {
        "scope": "frozen-B7-l6-hard-orbit-scout-UNSAT-only",
        "solver": "CaDiCaL 1.7.3",
        "solver-source-commit": "38e073b389a877b0a0d3c91136d2443ab95fdeba",
        "solver-binary-sha256": "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292",
        "solver-command": "cadical --lrat --no-binary -q CNF LRAT",
        "solver-required-exit": "20",
        "checker": "lrat-check",
        "checker-source-commit": "2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
        "checker-binary-sha256": "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8",
        "checker-required-output": "c VERIFIED",
        "compression": "xz -3",
        "leaves": "14",
        "parents-incidences": "140",
        "total-lrat-bytes": "517657728",
        "total-xz-bytes": "94639000",
    }
    for name, value in required.items():
        if metadata.get(name) != value:
            raise RuntimeError(f"frozen metadata changed: {name}")
    if columns is None or tuple(int(row["leaf-ordinal"]) for row in records) != ORDINALS:
        raise RuntimeError("ledger is not exactly the 14 frozen scout-UNSAT leaves")
    if sum(int(row["parents"]) for row in records) != 140:
        raise RuntimeError("parent-incidence total changed")
    if sum(int(row["lrat-bytes"]) for row in records) != 517657728:
        raise RuntimeError("LRAT byte total changed")
    if sum(int(row["xz-bytes"]) for row in records) != 94639000:
        raise RuntimeError("compressed byte total changed")
    return metadata, records


def verify_scope(metadata, records):
    scout = json.loads(SOURCE_PATHS["orbit-scout"].read_text(encoding="ascii"))
    if scout.get("schema") != "m6-b7-l6-hard-orbit-scout-v1" or len(scout.get("rows", [])) != 42:
        raise RuntimeError("scout is not the exact frozen 42-leaf record")
    unsat = tuple(row for row in scout["rows"] if row.get("status") == "UNSAT")
    if tuple(row["leaf"] for row in unsat) != ORDINALS or len(unsat) != int(metadata["leaves"]):
        raise RuntimeError("certificate scope differs from the complete scout UNSAT set")
    for scout_row, record in zip(unsat, records):
        expected = (f"{scout_row['leaf']:02d}", scout_row["key"], str(scout_row["parents"]),
                    scout_row["cnf_sha256"])
        actual = (record["leaf-ordinal"], record["key"], record["parents"], record["cnf-sha256"])
        if actual != expected:
            raise RuntimeError("certificate row differs from scout identity")


def run(command, label, **kwargs):
    result = subprocess.run(command, **kwargs)
    if result.returncode:
        raise RuntimeError(f"{label} failed with exit {result.returncode}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    args = parser.parse_args()
    require_identity(args.ledger, *LEDGER_IDENTITY, "certificate ledger")
    metadata, records = load_ledger(args.ledger)
    for name, path in SOURCE_PATHS.items():
        require_identity(path, metadata[f"{name}-bytes"], metadata[f"{name}-sha256"], name)
    if identity(args.checker)[1] != metadata["checker-binary-sha256"]:
        raise RuntimeError("checker binary is not the pinned executable")
    verify_scope(metadata, records)

    with tempfile.TemporaryDirectory(prefix="m6-b7-l6-hard-orbit-verify-", dir=ROOT) as directory:
        work = Path(directory)
        for record in records:
            ordinal = int(record["leaf-ordinal"])
            expected = Path("certificates") / f"m6-b7-l6-hard-orbit-leaf-{ordinal:02d}.lrat.xz"
            if Path(record["artifact"]) != expected:
                raise RuntimeError("artifact path differs from exact safe filename")
            artifact = ROOT / expected
            require_identity(artifact, record["xz-bytes"], record["xz-sha256"], f"leaf {ordinal:02d} xz")
            cnf = work / f"leaf-{ordinal:02d}.cnf"
            run([sys.executable, str(SOURCE_PATHS["orbit-producer"]), "--leaf", str(ordinal),
                 "--output", str(cnf)], f"leaf {ordinal:02d} regeneration", cwd=HERE,
                stdout=subprocess.DEVNULL)
            require_identity(cnf, record["cnf-bytes"], record["cnf-sha256"], f"leaf {ordinal:02d} CNF")
            run([sys.executable, str(SOURCE_PATHS["orbit-structural-checker"]), str(cnf)],
                f"leaf {ordinal:02d} structural check", cwd=HERE, stdout=subprocess.DEVNULL)
            lrat = work / f"leaf-{ordinal:02d}.lrat"
            with lzma.open(artifact, "rb") as source, lrat.open("wb") as target:
                while block := source.read(1 << 20):
                    target.write(block)
            require_identity(lrat, record["lrat-bytes"], record["lrat-sha256"], f"leaf {ordinal:02d} LRAT")
            checked = subprocess.run([str(args.checker), str(cnf), str(lrat)],
                                     capture_output=True, text=True)
            if checked.returncode or metadata["checker-required-output"] not in checked.stdout.splitlines():
                raise RuntimeError(f"leaf {ordinal:02d} LRAT was not accepted by the pinned checker")
            print(f"PASS leaf={ordinal:02d} key={record['key']} parents={record['parents']} xz_bytes={record['xz-bytes']}")
    print(f"PASS leaves=14 parents_incidences=140 total_xz_bytes=94639000")


if __name__ == "__main__":
    main()
