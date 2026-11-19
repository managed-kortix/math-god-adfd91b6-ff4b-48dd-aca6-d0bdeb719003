#!/usr/bin/env python3
"""Strict fresh replay of exactly eight frozen coordinate-scout UNSAT LRATs."""

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
LEDGER = HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-certificates.tsv"
FORMAT = "m6-b7-l6-hard-witness-positive-gain-coordinate-certificates-v1"
LEDGER_CANONICAL_SHA256 = "3aae87713d43ec3bf754beae9ec8b65020f4d3185b9e0a5bf83bce8f9a3c3a3f"
SELF_TOKEN = b'LEDGER_CANONICAL_SHA256 = "' + b"0" * 64 + b'"'
BOUND_PATHS = {
    "coordinate-manifest": HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate.tsv",
    "coordinate-hash-ledger": HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-hashes.tsv",
    "coordinate-scout": HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-scout-15s.json",
    "coordinate-producer": HERE / "m6_b7_l6_hard_witness_positive_gain_coordinate.py",
    "coordinate-structural-checker": HERE / "check_m6_b7_l6_hard_witness_positive_gain_coordinate.py",
    "coordinate-scout-source": HERE / "m6_b7_l6_hard_witness_positive_gain_coordinate_scout.py",
    "coordinate-test-source": HERE / "test_m6_b7_l6_hard_witness_positive_gain_coordinate.py",
    "certificate-producer": HERE / "certify_m6_b7_l6_hard_witness_positive_gain_coordinate.py",
    "certificate-test-source": HERE / "test_m6_b7_l6_hard_witness_positive_gain_coordinate_certificates.py",
    "ancestor-manifest": HERE / "m6-b7-l6-hard-witness-positive-gain.tsv",
    "ancestor-hash-ledger": HERE / "m6-b7-l6-hard-witness-positive-gain-hashes.tsv",
    "ancestor-scout": HERE / "m6-b7-l6-hard-witness-positive-gain-scout-20s.json",
    "ancestor-certificates": HERE / "m6-b7-l6-hard-witness-positive-gain-certificates.tsv",
    "ancestor-certificate-verifier": HERE / "verify_m6_b7_l6_hard_witness_positive_gain_certificates.py",
    "complement-manifest": HERE / "m6-b7-l6-hard-witness-no-gain.tsv",
    "complement-hash-ledger": HERE / "m6-b7-l6-hard-witness-no-gain-hashes.tsv",
    "complement-scout": HERE / "m6-b7-l6-hard-witness-no-gain-scout-20s.json",
    "complement-certificates": HERE / "m6-b7-l6-hard-witness-no-gain-certificates.tsv",
    "complement-certificate-verifier": HERE / "verify_m6_b7_l6_hard_witness_no_gain_certificates.py",
    "base-snc-cnf": HERE / "snc_cnf.py",
    "base-parent-producer": HERE / "m6_parent_cnf.py",
    "base-parent-checker": HERE / "check_m6_parent_cnf.py",
    "base-residual-producer": HERE / "m6_residual_group_cnf.py",
    "base-clean-manifest-producer": HERE / "m6_clean_sink_manifest.py",
    "base-clean-manifest-checker": HERE / "check_m6_clean_sink_manifest.py",
    "base-clean-group-producer": HERE / "m6_clean_sink_group_cnf.py",
    "base-clean-group-checker": HERE / "check_m6_clean_sink_group_cnf.py",
    "base-state-producer": HERE / "m6_b7_l6_state_split.py",
    "base-state-checker": HERE / "check_m6_b7_l6_state_split.py",
    "base-hard-orbit-producer": HERE / "m6_b7_l6_hard_orbits.py",
    "base-hard-orbit-checker": HERE / "check_m6_b7_l6_hard_orbits.py",
    "base-witness-orbit-producer": HERE / "m6_b7_l6_hard_witness_orbits.py",
    "base-witness-orbit-checker": HERE / "check_m6_b7_l6_hard_witness_orbits.py",
    "ancestor-producer": HERE / "m6_b7_l6_hard_witness_positive_gain.py",
    "ancestor-structural-checker": HERE / "check_m6_b7_l6_hard_witness_positive_gain.py",
    "ancestor-scout-source": HERE / "m6_b7_l6_hard_witness_positive_gain_scout.py",
    "ancestor-test-source": HERE / "test_m6_b7_l6_hard_witness_positive_gain.py",
    "ancestor-certificate-producer": HERE / "certify_m6_b7_l6_hard_witness_positive_gain.py",
    "ancestor-certificate-test-source": HERE / "test_m6_b7_l6_hard_witness_positive_gain_certificates.py",
    "complement-producer": HERE / "m6_b7_l6_hard_witness_no_gain.py",
    "complement-structural-checker": HERE / "check_m6_b7_l6_hard_witness_no_gain.py",
    "complement-scout-source": HERE / "m6_b7_l6_hard_witness_no_gain_scout.py",
    "complement-test-source": HERE / "test_m6_b7_l6_hard_witness_no_gain.py",
    "complement-certificate-producer": HERE / "certify_m6_b7_l6_hard_witness_no_gain.py",
}
COLUMNS = (
    "leaf-ordinal", "key", "source-leaf-ordinal", "source-key", "coordinate",
    "deleted", "witness", "parents", "variables", "clauses", "cnf-bytes",
    "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes", "xz-sha256",
    "solve-nanoseconds", "check-nanoseconds", "artifact",
)
HEX_COLUMNS = ("cnf-sha256", "lrat-sha256", "xz-sha256")
DECIMAL_COLUMNS = (
    "leaf-ordinal", "source-leaf-ordinal", "coordinate", "deleted", "witness",
    "parents", "variables", "clauses", "cnf-bytes", "lrat-bytes", "xz-bytes",
    "solve-nanoseconds", "check-nanoseconds",
)
ORDINALS = (20, 26, 96, 102, 172, 178, 215, 217)
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


def canonical_ledger_hash(path=LEDGER):
    lines = path.read_bytes().splitlines(keepends=True)
    prefix = b"verifier-canonical-sha256\t"
    matches = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    if len(matches) != 1:
        raise RuntimeError("ledger verifier self-pin row changed")
    lines[matches[0]] = prefix + b"0" * 64 + b"\n"
    return digest(b"".join(lines))


def load_ledger(path=LEDGER):
    data = path.read_bytes()
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
        "generated-utc": "2026-08-09",
        "scope": "frozen-B7-l6-hard-witness-positive-gain-coordinate-scout-UNSAT-only-020,026,096,102,172,178,215,217",
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
        "leaves": "8",
        "leaf-ordinals": "020,026,096,102,172,178,215,217",
        "source-leaf-ordinals": "010,013,051,054,090,093,115,116",
        "parents-incidences": "72",
        "total-cnf-bytes": "83200933",
        "total-lrat-bytes": "56828147",
        "total-xz-bytes": "3756712",
        "ancestor-certificate-scope": "042,095,097",
        "complement-certificate-scope": "75-scout-UNSAT-leaves",
    }
    if any(metadata.get(name) != value for name, value in required.items()):
        raise RuntimeError("frozen certificate metadata changed")
    expected_keys = set(required) | {"verifier-canonical-sha256"} | {
        suffix for name in BOUND_PATHS for suffix in (f"{name}-bytes", f"{name}-sha256")
    }
    if set(metadata) != expected_keys or columns is None:
        raise RuntimeError("certificate metadata keys changed")
    if tuple(int(row["leaf-ordinal"]) for row in rows) != ORDINALS:
        raise RuntimeError("ledger scope is not exactly the eight ordered scout UNSAT leaves")
    totals = {"parents": 72, "cnf-bytes": 83200933, "lrat-bytes": 56828147, "xz-bytes": 3756712}
    if any(sum(int(row[name]) for row in rows) != value for name, value in totals.items()):
        raise RuntimeError("certificate totals changed")
    if totals["xz-bytes"] >= LIMIT or data != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("compressed bound or canonical ledger encoding changed")
    return metadata, rows


def load_certificate_artifacts(path):
    lines = path.read_text(encoding="ascii").splitlines()
    marker = next((i for i, line in enumerate(lines) if line.startswith("columns\t")), -1)
    if marker < 0:
        raise RuntimeError(f"certificate columns absent: {path.name}")
    columns = lines[marker].split("\t", 1)[1].split(",")
    result = []
    for line in lines[marker + 1:]:
        row = dict(zip(columns, line.split("\t")))
        artifact = ROOT / row["artifact"]
        if identity(artifact) != (int(row["xz-bytes"]), row["xz-sha256"]):
            raise RuntimeError(f"bound certificate artifact changed: {artifact.name}")
        result.append(artifact)
    return set(result)


def verify_bindings(metadata):
    if canonical_ledger_hash() != LEDGER_CANONICAL_SHA256:
        raise RuntimeError("verifier does not pin the canonical ledger")
    if metadata["verifier-canonical-sha256"] != canonical_verifier_hash(Path(__file__)):
        raise RuntimeError("ledger does not pin the canonical verifier")
    for name, path in BOUND_PATHS.items():
        expected = int(metadata[f"{name}-bytes"]), metadata[f"{name}-sha256"]
        if identity(path) != expected:
            raise RuntimeError(f"bound source identity changed: {name}")
    ancestor = load_certificate_artifacts(BOUND_PATHS["ancestor-certificates"])
    complement = load_certificate_artifacts(BOUND_PATHS["complement-certificates"])
    if len(ancestor) != 3 or len(complement) != 75:
        raise RuntimeError("ancestor/complement certificate scope changed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path, required=True)
    args = parser.parse_args()
    metadata, rows = load_ledger()
    verify_bindings(metadata)
    if identity(args.checker)[1] != CHECKER_SHA256:
        raise RuntimeError("checker binary is not pinned lrat-check")
    scout = json.loads(BOUND_PATHS["coordinate-scout"].read_text(encoding="ascii"))
    unsat = tuple(row for row in scout.get("rows", []) if row.get("status") == "UNSAT")
    if len(scout.get("rows", [])) != 219 or tuple(row["leaf"] for row in unsat) != ORDINALS:
        raise RuntimeError("coordinate scout scope changed")
    for source, record in zip(unsat, rows):
        observed = (f"{source['leaf']:03d}", source["key"], f"{source['source_leaf']:03d}",
                    source["source_key"], str(source["coordinate"]), str(source["deleted"]),
                    str(source["witness"]), str(source["parents"]), source["cnf_sha256"])
        expected = tuple(record[name] for name in (
            "leaf-ordinal", "key", "source-leaf-ordinal", "source-key", "coordinate",
            "deleted", "witness", "parents", "cnf-sha256",
        ))
        if observed != expected:
            raise RuntimeError("certificate scope differs from complete coordinate scout UNSAT set")
    expected_artifacts = {ROOT / row["artifact"] for row in rows}
    actual_artifacts = set((ROOT / "certificates").glob(
        "m6-b7-l6-hard-witness-positive-gain-coordinate-leaf-*.lrat.xz"
    ))
    if actual_artifacts != expected_artifacts:
        raise RuntimeError("coordinate artifact set is not exactly ledger scope")

    with tempfile.TemporaryDirectory(prefix="m6-positive-coordinate-replay-", dir=ROOT) as directory:
        work = Path(directory)
        for position, record in enumerate(rows, 1):
            ordinal = int(record["leaf-ordinal"])
            name = f"m6-b7-l6-hard-witness-positive-gain-coordinate-leaf-{ordinal:03d}.lrat.xz"
            if record["artifact"] != f"certificates/{name}":
                raise RuntimeError("artifact path differs from safe exact filename")
            artifact = ROOT / record["artifact"]
            if identity(artifact) != (int(record["xz-bytes"]), record["xz-sha256"]):
                raise RuntimeError(f"leaf {ordinal:03d} compressed identity changed")
            cnf = work / f"leaf-{ordinal:03d}.cnf"
            made = subprocess.run(
                [sys.executable, str(BOUND_PATHS["coordinate-producer"]), "--leaf", str(ordinal),
                 "--output", str(cnf)], cwd=HERE, stdout=subprocess.DEVNULL,
            )
            if made.returncode or identity(cnf) != (int(record["cnf-bytes"]), record["cnf-sha256"]):
                raise RuntimeError(f"leaf {ordinal:03d} CNF regeneration changed")
            checked_structure = subprocess.run(
                [sys.executable, str(BOUND_PATHS["coordinate-structural-checker"]), str(cnf)],
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
            print(f"PASS {position:02d}/08 leaf={ordinal:03d} key={record['key']} xz={record['xz-bytes']}")
    print("PASS leaves=8 ordinals=020,026,096,102,172,178,215,217 parents_incidences=72 total_xz_bytes=3756712 limit_exclusive=250000000")


if __name__ == "__main__":
    main()
