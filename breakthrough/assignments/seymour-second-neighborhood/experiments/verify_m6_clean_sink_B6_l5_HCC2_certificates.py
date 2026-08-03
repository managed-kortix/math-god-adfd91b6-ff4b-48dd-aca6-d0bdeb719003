#!/usr/bin/env python3
"""Strictly regenerate and replay the two frozen B6-l5 H_CC=2 certificates."""

import argparse
import hashlib
import lzma
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGER = HERE / "m6-clean-sink-B6-l5-HCC2-certificates.tsv"
FORMAT = "m6-clean-sink-B6-l5-HCC2-certificates-v1"
LEDGER_IDENTITY = (2057, "8ec58f4193756d57e9e4ed6921c944c1cd876f4ced72b5f67119a2cab508c9a2")
SHARDS = (
    ("02", "B6-l5-q0-c2-s00", "0", "78", "m6-clean-sink-B6-l5-q0-HCC2.lrat.xz"),
    ("05", "B6-l5-q1-c2-s00", "1", "26", "m6-clean-sink-B6-l5-q1-HCC2.lrat.xz"),
)
BOUND_PATHS = {
    "partition-manifest": HERE / "m6-clean-sink-balanced-shards.tsv",
    "partition-theorem": ROOT / "attempts" / "tick53-clean-sink-balanced-shards.md",
    "cnf-hash-ledger": HERE / "m6-clean-sink-balanced-shard-hashes.tsv",
    "producer": HERE / "m6_clean_sink_balanced_shards.py",
    "structural-checker": HERE / "check_m6_clean_sink_balanced_shards.py",
}
METADATA_KEYS = (
    "generated-utc", "scope", "partition-manifest-bytes", "partition-manifest-sha256",
    "partition-theorem-bytes", "partition-theorem-sha256", "cnf-hash-ledger-bytes",
    "cnf-hash-ledger-sha256", "producer-bytes", "producer-sha256",
    "structural-checker-bytes", "structural-checker-sha256", "solver",
    "solver-source-commit", "solver-binary-sha256", "solver-command",
    "solver-required-exit", "checker", "checker-source-commit",
    "checker-binary-sha256", "checker-required-output", "compression",
    "compact-limit-xz-bytes", "shards", "parents", "total-lrat-bytes",
    "total-xz-bytes",
)
COLUMNS = (
    "shard-ordinal", "key", "q", "H_CC", "parents", "variables", "clauses",
    "cnf-bytes", "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes",
    "xz-sha256", "solve-nanoseconds", "check-nanoseconds", "artifact",
)
FIXED = {
    "generated-utc": "2026-08-02",
    "scope": "B6-l5-HCC2-only",
    "partition-manifest-bytes": "8414",
    "partition-manifest-sha256": "20f6d04a9e8ca0662efd011ead7804402d3c0dd21e025311cb4485fae8403fdb",
    "partition-theorem-bytes": "2490",
    "partition-theorem-sha256": "a6aa643ae2cad46349a8a1aee88f837e112532aef2858913c9e19289e8200a87",
    "cnf-hash-ledger-bytes": "5972",
    "cnf-hash-ledger-sha256": "46045d216f32a22b1d618910c4e3fc5528c700b34277be2e17eab89e6ccae125",
    "producer-bytes": "17121",
    "producer-sha256": "4bb4efd995556706e5d5b50fb986d23cf106c4a80e2b0fd6aa53ec8a5c322100",
    "structural-checker-bytes": "16058",
    "structural-checker-sha256": "bfc2fa131a7e3a4f4c270a786ff1b9fc86e68a9ad66d8952d4d64fea36974848",
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
    "compact-limit-xz-bytes": "2000000",
    "shards": "2",
    "parents": "104",
    "total-lrat-bytes": "13470841",
    "total-xz-bytes": "943048",
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
    metadata, records, columns = {}, [], None
    metadata_order = []
    for line in lines[1:]:
        fields = line.split("\t")
        if fields[0] == "columns":
            if columns is not None or tuple(fields[1].split(",")) != COLUMNS:
                raise RuntimeError("certificate columns changed")
            columns = COLUMNS
        elif columns is None:
            if len(fields) != 2 or fields[0] in metadata:
                raise RuntimeError("malformed certificate metadata")
            metadata_order.append(fields[0])
            metadata[fields[0]] = fields[1]
        else:
            if len(fields) != len(COLUMNS):
                raise RuntimeError("malformed certificate record")
            records.append(dict(zip(COLUMNS, fields)))
    if tuple(metadata_order) != METADATA_KEYS or metadata != FIXED or len(records) != 2:
        raise RuntimeError("certificate ledger is not the strict frozen record")
    expected_rows = tuple((row["shard-ordinal"], row["key"], row["q"], row["parents"], Path(row["artifact"]).name)
                          for row in records)
    if expected_rows != SHARDS or any(row["H_CC"] != "2" for row in records):
        raise RuntimeError("ledger does not contain exactly the two requested H_CC=2 shards")
    if sum(int(row["parents"]) for row in records) != 104:
        raise RuntimeError("parent total changed")
    if sum(int(row["lrat-bytes"]) for row in records) != int(metadata["total-lrat-bytes"]):
        raise RuntimeError("LRAT total changed")
    if sum(int(row["xz-bytes"]) for row in records) != int(metadata["total-xz-bytes"]):
        raise RuntimeError("compressed total changed")
    if int(metadata["total-xz-bytes"]) >= int(metadata["compact-limit-xz-bytes"]):
        raise RuntimeError("proof bundle is not compact")
    return metadata, records


def run(command, label, **kwargs):
    result = subprocess.run(command, **kwargs)
    if result.returncode:
        raise RuntimeError(f"{label} failed with exit {result.returncode}")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    args = parser.parse_args()
    require_identity(args.ledger, *LEDGER_IDENTITY, "certificate ledger")
    metadata, records = load_ledger(args.ledger)
    for name, path in BOUND_PATHS.items():
        require_identity(path, metadata[f"{name}-bytes"], metadata[f"{name}-sha256"], name)
    if sha256(args.checker) != metadata["checker-binary-sha256"]:
        raise RuntimeError("checker binary is not the pinned executable")

    with tempfile.TemporaryDirectory(prefix="m6-clean-sink-B6-l5-HCC2-verify-") as directory:
        work = Path(directory)
        for index, record in enumerate(records):
            key = record["key"]
            relative = Path(record["artifact"])
            expected = Path("certificates") / SHARDS[index][4]
            if relative != expected:
                raise RuntimeError(f"{key} artifact path is not the frozen safe path")
            artifact = ROOT / relative
            require_identity(artifact, record["xz-bytes"], record["xz-sha256"], f"{key} compressed LRAT")
            cnf = work / f"{key}.cnf"
            run([sys.executable, str(BOUND_PATHS["producer"]), "--key", key, "--output", str(cnf)],
                f"{key} regeneration", cwd=HERE, stdout=subprocess.DEVNULL)
            require_identity(cnf, record["cnf-bytes"], record["cnf-sha256"], f"{key} CNF")
            run([sys.executable, str(BOUND_PATHS["structural-checker"]), str(cnf)],
                f"{key} structural audit", cwd=HERE, stdout=subprocess.DEVNULL)
            lrat = work / f"{key}.lrat"
            with lzma.open(artifact, "rb") as source, lrat.open("wb") as target:
                while block := source.read(1 << 20):
                    target.write(block)
            require_identity(lrat, record["lrat-bytes"], record["lrat-sha256"], f"{key} LRAT")
            checked = subprocess.run([str(args.checker), str(cnf), str(lrat)], capture_output=True, text=True)
            if checked.returncode or metadata["checker-required-output"] not in checked.stdout.splitlines():
                raise RuntimeError(f"{key} LRAT was not accepted by the pinned checker")
            print(f"PASS shard={record['shard-ordinal']} key={key} parents={record['parents']} xz_bytes={record['xz-bytes']}")
    print(f"PASS shards=2 parents=104 total_xz_bytes={metadata['total-xz-bytes']}")


if __name__ == "__main__":
    main()
