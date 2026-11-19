#!/usr/bin/env python3
"""Strictly regenerate and replay the 11 scout-UNSAT B7-l6 state leaves."""

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
LEDGER = HERE / "m6-b7-l6-state-certificates.tsv"
LEDGER_IDENTITY = (5030, "037a4a6e51ef5cd76dc070bd461481ef90ac5520a875c0a96973c60f991172c7")
FORMAT = "m6-b7-l6-state-certificates-v1"
BOUND_PATHS = {
    "state-manifest": HERE / "m6-b7-l6-state-split.tsv",
    "cnf-hash-ledger": HERE / "m6-b7-l6-state-leaf-hashes.tsv",
    "scout": HERE / "m6-b7-l6-state-scout-30s.json",
    "producer": HERE / "m6_b7_l6_state_split.py",
    "structural-checker": HERE / "check_m6_b7_l6_state_split.py",
}
ORDINALS = (0, 2, 4, 6, 8, 10, 14, 16, 18, 22, 26)
METADATA_KEYS = (
    "generated-utc", "scope", "timing-clock", "state-manifest-bytes",
    "state-manifest-sha256", "cnf-hash-ledger-bytes", "cnf-hash-ledger-sha256",
    "scout-bytes", "scout-sha256", "producer-bytes", "producer-sha256",
    "structural-checker-bytes", "structural-checker-sha256", "verifier-bytes",
    "verifier-sha256", "solver", "solver-source-commit", "solver-binary-sha256",
    "solver-command", "solver-required-exit", "checker", "checker-source-commit",
    "checker-binary-sha256", "checker-required-output", "compression",
    "compact-limit-xz-bytes", "leaves", "parents-incidences", "total-lrat-bytes",
    "total-xz-bytes",
)
COLUMNS = (
    "leaf-ordinal", "key", "parents", "variables", "clauses", "cnf-bytes",
    "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes", "xz-sha256",
    "solve-nanoseconds", "check-nanoseconds", "artifact",
)
FIXED = {
    "generated-utc": "2026-08-05",
    "scope": "frozen-B7-l6-scout-UNSAT-only",
    "timing-clock": "Python time.monotonic_ns",
    "state-manifest-bytes": "4382",
    "state-manifest-sha256": "a3b8f9d17b50dbfccd5f00740b33c6e90f6f10d26a3854dd627a45681e5c890e",
    "cnf-hash-ledger-bytes": "3163",
    "cnf-hash-ledger-sha256": "eec464838f7d01e6cf053c7cbf8fa1442068d78738f4bd2772b15a8417543ae4",
    "scout-bytes": "6948",
    "scout-sha256": "69c1d56145ec2544702717b252bd1e3796c882c68ca95023488b959e2af2f763",
    "producer-bytes": "15948",
    "producer-sha256": "544de152f692fc9f2b781f81de320e1d35a24a38d3225147212aa5d9609d2d1f",
    "structural-checker-bytes": "14637",
    "structural-checker-sha256": "a21959f914193fdb15f56f9b92ab4cddb2fed7cf6386a5ecc8c852c148925bb3",
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
    "compact-limit-xz-bytes": "100000000",
    "leaves": "11",
    "parents-incidences": "90",
    "total-lrat-bytes": "194427307",
    "total-xz-bytes": "25946740",
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def identity(path):
    return path.stat().st_size, sha256(path)


def require_identity(path, size, digest, label):
    expected = int(size), digest
    actual = identity(path)
    if actual != expected:
        raise RuntimeError(f"{label} identity mismatch: expected {expected}, got {actual}")


def load_ledger(path):
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != FORMAT:
        raise RuntimeError("unexpected certificate ledger format")
    metadata, order, records, columns = {}, [], [], None
    for line in lines[1:]:
        fields = line.split("\t")
        if fields[0] == "columns":
            if columns is not None or tuple(fields[1].split(",")) != COLUMNS:
                raise RuntimeError("certificate columns changed")
            columns = COLUMNS
        elif columns is None:
            if len(fields) != 2 or fields[0] in metadata:
                raise RuntimeError("malformed certificate metadata")
            order.append(fields[0])
            metadata[fields[0]] = fields[1]
        else:
            if len(fields) != len(COLUMNS):
                raise RuntimeError("malformed certificate row")
            records.append(dict(zip(COLUMNS, fields)))
    if tuple(order) != METADATA_KEYS or columns is None:
        raise RuntimeError("certificate metadata order changed")
    for name, value in FIXED.items():
        if metadata.get(name) != value:
            raise RuntimeError(f"frozen metadata changed: {name}")
    if tuple(int(row["leaf-ordinal"]) for row in records) != ORDINALS:
        raise RuntimeError("ledger is not exactly the 11 frozen scout-UNSAT leaves")
    if sum(int(row["parents"]) for row in records) != int(metadata["parents-incidences"]):
        raise RuntimeError("parent-incidence total changed")
    for field in ("lrat-bytes", "xz-bytes"):
        expected = int(metadata[f"total-{field}"])
        if sum(int(row[field]) for row in records) != expected:
            raise RuntimeError(f"{field} total changed")
    if int(metadata["total-xz-bytes"]) >= int(metadata["compact-limit-xz-bytes"]):
        raise RuntimeError("compressed proof bundle is not below 100MB")
    return metadata, records


def verify_scope(metadata, records):
    scout = json.loads(BOUND_PATHS["scout"].read_text(encoding="ascii"))
    if scout.get("schema") != "m6-b7-l6-state-scout-v1" or len(scout.get("rows", [])) != 30:
        raise RuntimeError("scout is not the exact 30-leaf frozen record")
    unsat = tuple(row for row in scout["rows"] if row.get("status") == "UNSAT")
    if tuple(row["leaf"] for row in unsat) != ORDINALS or len(unsat) != int(metadata["leaves"]):
        raise RuntimeError("certificate scope differs from scout UNSAT set")
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
    for name, path in BOUND_PATHS.items():
        require_identity(path, metadata[f"{name}-bytes"], metadata[f"{name}-sha256"], name)
    # The verifier pins the immutable ledger.  Do not make the ledger and
    # verifier recursively pin one another; the recorded verifier identity is
    # provenance for the generation run.
    if sha256(args.checker) != metadata["checker-binary-sha256"]:
        raise RuntimeError("checker binary is not the pinned executable")
    verify_scope(metadata, records)

    with tempfile.TemporaryDirectory(prefix="m6-b7-l6-state-verify-") as directory:
        work = Path(directory)
        for record in records:
            ordinal = int(record["leaf-ordinal"])
            expected = Path("certificates") / f"m6-b7-l6-state-leaf-{ordinal:02d}.lrat.xz"
            relative = Path(record["artifact"])
            if relative != expected:
                raise RuntimeError("artifact path differs from exact safe filename")
            artifact = ROOT / relative
            require_identity(artifact, record["xz-bytes"], record["xz-sha256"], f"leaf {ordinal:02d} xz")
            cnf = work / f"leaf-{ordinal:02d}.cnf"
            run([sys.executable, str(BOUND_PATHS["producer"]), "--leaf", str(ordinal),
                 "--output", str(cnf)], f"leaf {ordinal:02d} regeneration", cwd=HERE,
                stdout=subprocess.DEVNULL)
            require_identity(cnf, record["cnf-bytes"], record["cnf-sha256"], f"leaf {ordinal:02d} CNF")
            run([sys.executable, str(BOUND_PATHS["structural-checker"]), str(cnf)],
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
    print(f"PASS leaves={metadata['leaves']} parents_incidences={metadata['parents-incidences']} total_xz_bytes={metadata['total-xz-bytes']}")


if __name__ == "__main__":
    main()
