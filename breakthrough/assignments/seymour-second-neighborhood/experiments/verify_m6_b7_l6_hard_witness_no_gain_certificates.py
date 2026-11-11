#!/usr/bin/env python3
"""Fresh replay of exactly 75 frozen scout-UNSAT no-gain LRAT certificates."""

import argparse
import hashlib
import json
import lzma
from pathlib import Path
import re
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGER = HERE / "m6-b7-l6-hard-witness-no-gain-certificates.tsv"
FORMAT = "m6-b7-l6-hard-witness-no-gain-certificates-v1"
LEDGER_CANONICAL_SHA256 = "69adabb257c2ffc69498fbf04c27c00c2a3807d701db90f98c87ba63f6ffc3c6"
SELF_TOKEN = b'LEDGER_CANONICAL_SHA256 = "' + b"0" * 64 + b'"'
BOUND_PATHS = {
    "no-gain-manifest": HERE / "m6-b7-l6-hard-witness-no-gain.tsv",
    "no-gain-hash-ledger": HERE / "m6-b7-l6-hard-witness-no-gain-hashes.tsv",
    "no-gain-scout": HERE / "m6-b7-l6-hard-witness-no-gain-scout-20s.json",
    "no-gain-producer": HERE / "m6_b7_l6_hard_witness_no_gain.py",
    "no-gain-structural-checker": HERE / "check_m6_b7_l6_hard_witness_no_gain.py",
    "no-gain-scout-source": HERE / "m6_b7_l6_hard_witness_no_gain_scout.py",
    "no-gain-test-source": HERE / "test_m6_b7_l6_hard_witness_no_gain.py",
    "certificate-producer": HERE / "certify_m6_b7_l6_hard_witness_no_gain.py",
}
COLUMNS = (
    "leaf-ordinal", "key", "parents", "variables", "clauses", "cnf-bytes",
    "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes", "xz-sha256",
    "solve-nanoseconds", "check-nanoseconds", "artifact",
)
HEX_COLUMNS = ("cnf-sha256", "lrat-sha256", "xz-sha256")
DECIMAL_COLUMNS = ("leaf-ordinal", "parents", "variables", "clauses", "cnf-bytes",
                   "lrat-bytes", "xz-bytes", "solve-nanoseconds", "check-nanoseconds")
SOLVER_SHA256 = "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292"
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
LIMIT = 250_000_000


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            value.update(block)
    return path.stat().st_size, value.hexdigest()


def canonical_verifier_hash(path):
    data = path.read_bytes()
    marker = b'LEDGER_CANONICAL_SHA256 = "' + LEDGER_CANONICAL_SHA256.encode("ascii") + b'"'
    if data.count(marker) != 1:
        raise RuntimeError("verifier self-pin marker changed")
    return digest(data.replace(marker, SELF_TOKEN))


def canonical_ledger_hash(path):
    lines = path.read_bytes().splitlines(keepends=True)
    prefix = b"verifier-canonical-sha256\t"
    matches = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    if len(matches) != 1:
        raise RuntimeError("ledger verifier self-pin row changed")
    lines[matches[0]] = prefix + b"0" * 64 + b"\n"
    return digest(b"".join(lines))


def load_ledger():
    data = LEDGER.read_bytes()
    lines = data.decode("ascii").splitlines()
    if not lines or lines[0] != FORMAT:
        raise RuntimeError("unexpected certificate ledger format")
    metadata, rows, columns = {}, [], None
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
            row = dict(zip(COLUMNS, fields))
            if any(re.fullmatch(r"[0-9a-f]{64}", row[name]) is None for name in HEX_COLUMNS) or \
                    any(not row[name].isdigit() for name in DECIMAL_COLUMNS):
                raise RuntimeError("noncanonical certificate row value")
            rows.append(row)
    required = {
        "scope": "frozen-B7-l6-hard-witness-no-gain-scout-UNSAT-only",
        "solver": "CaDiCaL 1.7.3",
        "solver-source-commit": "38e073b389a877b0a0d3c91136d2443ab95fdeba",
        "solver-binary-sha256": SOLVER_SHA256,
        "solver-command": "cadical --lrat --no-binary -q CNF LRAT",
        "solver-required-exit": "20",
        "checker": "lrat-check",
        "checker-source-commit": "2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
        "checker-binary-sha256": CHECKER_SHA256,
        "checker-required-output": "c VERIFIED",
        "compression": "xz -3",
        "compressed-limit-bytes-exclusive": str(LIMIT),
        "leaves": "75",
        "parents-incidences": "686",
        "total-lrat-bytes": "583302008",
        "total-xz-bytes": "42951720",
    }
    for name, value in required.items():
        if metadata.get(name) != value:
            raise RuntimeError(f"frozen metadata changed: {name}")
    expected_keys = {
        "generated-utc", "scope", "verifier-canonical-sha256", "solver",
        "solver-source-commit", "solver-binary-sha256", "solver-command",
        "solver-required-exit", "checker", "checker-source-commit",
        "checker-binary-sha256", "checker-required-output", "compression",
        "compressed-limit-bytes-exclusive", "leaves", "parents-incidences",
        "total-lrat-bytes", "total-xz-bytes",
    } | {suffix for name in BOUND_PATHS for suffix in (f"{name}-bytes", f"{name}-sha256")}
    if set(metadata) != expected_keys or metadata["generated-utc"] != "2026-08-09":
        raise RuntimeError("certificate metadata keys or date changed")
    if columns is None or len(rows) != 75:
        raise RuntimeError("ledger does not contain exactly 75 records")
    if sum(int(row["parents"]) for row in rows) != 686:
        raise RuntimeError("parent-incidence total changed")
    if sum(int(row["lrat-bytes"]) for row in rows) != 583302008:
        raise RuntimeError("LRAT byte total changed")
    if sum(int(row["xz-bytes"]) for row in rows) != 42951720:
        raise RuntimeError("compressed byte total changed")
    if int(metadata["total-xz-bytes"]) >= LIMIT:
        raise RuntimeError("compressed total is not below 250MB")
    if data != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("certificate ledger is not canonical ASCII TSV")
    return metadata, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path, required=True)
    args = parser.parse_args()
    metadata, rows = load_ledger()
    if canonical_ledger_hash(LEDGER) != LEDGER_CANONICAL_SHA256:
        raise RuntimeError("verifier does not pin the canonical ledger")
    if metadata.get("verifier-canonical-sha256") != canonical_verifier_hash(Path(__file__)):
        raise RuntimeError("ledger does not pin the canonical verifier")
    for name, path in BOUND_PATHS.items():
        expected = int(metadata[f"{name}-bytes"]), metadata[f"{name}-sha256"]
        if identity(path) != expected:
            raise RuntimeError(f"bound source identity changed: {name}")
    if identity(args.checker)[1] != CHECKER_SHA256:
        raise RuntimeError("checker binary is not pinned lrat-check")
    scout = json.loads(BOUND_PATHS["no-gain-scout"].read_text(encoding="ascii"))
    unsat = tuple(row for row in scout.get("rows", []) if row.get("status") == "UNSAT")
    if len(scout.get("rows", [])) != 117 or len(unsat) != 75:
        raise RuntimeError("scout scope changed")
    for source, record in zip(unsat, rows):
        if (f"{source['leaf']:03d}", source["key"], str(source["parents"]), source["cnf_sha256"]) != \
                (record["leaf-ordinal"], record["key"], record["parents"], record["cnf-sha256"]):
            raise RuntimeError("certificate scope differs from complete scout UNSAT set")

    with tempfile.TemporaryDirectory(prefix="m6-witness-no-gain-replay-", dir=ROOT) as directory:
        work = Path(directory)
        for position, record in enumerate(rows, 1):
            ordinal = int(record["leaf-ordinal"])
            name = f"m6-b7-l6-hard-witness-no-gain-leaf-{ordinal:03d}.lrat.xz"
            if record["artifact"] != f"certificates/{name}":
                raise RuntimeError("artifact path differs from safe exact filename")
            artifact = ROOT / record["artifact"]
            if identity(artifact) != (int(record["xz-bytes"]), record["xz-sha256"]):
                raise RuntimeError(f"leaf {ordinal:03d} compressed identity changed")
            cnf = work / f"leaf-{ordinal:03d}.cnf"
            made = subprocess.run(
                [sys.executable, str(BOUND_PATHS["no-gain-producer"]), "--leaf", str(ordinal),
                 "--output", str(cnf)], cwd=HERE, stdout=subprocess.DEVNULL,
            )
            if made.returncode or identity(cnf) != (int(record["cnf-bytes"]), record["cnf-sha256"]):
                raise RuntimeError(f"leaf {ordinal:03d} CNF regeneration changed")
            checked_structure = subprocess.run(
                [sys.executable, str(BOUND_PATHS["no-gain-structural-checker"]), str(cnf)],
                cwd=HERE, stdout=subprocess.DEVNULL,
            )
            if checked_structure.returncode:
                raise RuntimeError(f"leaf {ordinal:03d} structural check failed")
            lrat = work / f"leaf-{ordinal:03d}.lrat"
            with lzma.open(artifact, "rb") as source, lrat.open("wb") as target:
                while block := source.read(1 << 20):
                    target.write(block)
            if identity(lrat) != (int(record["lrat-bytes"]), record["lrat-sha256"]):
                raise RuntimeError(f"leaf {ordinal:03d} raw LRAT identity changed")
            checked = subprocess.run([str(args.checker), str(cnf), str(lrat)], capture_output=True, text=True)
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError(f"leaf {ordinal:03d} LRAT rejected")
            cnf.unlink()
            lrat.unlink()
            print(f"PASS {position:02d}/75 leaf={ordinal:03d} key={record['key']} xz={record['xz-bytes']}")
    print("PASS leaves=75 parents_incidences=686 total_xz_bytes=42951720 limit_exclusive=250000000")


if __name__ == "__main__":
    main()
