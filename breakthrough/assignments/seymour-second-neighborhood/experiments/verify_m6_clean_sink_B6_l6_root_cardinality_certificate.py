#!/usr/bin/env python3
"""Strictly regenerate and replay the frozen clean B6-l6 grouped LRAT."""

import argparse
import hashlib
import lzma
from pathlib import Path
import re
import subprocess
import tempfile

import check_m6_clean_sink_B6_l6_root_cardinality as structural
import m6_clean_sink_B6_l6_root_cardinality as producer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGER = HERE / f"{producer.PREFIX}-certificate.tsv"
FORMAT = f"{producer.PREFIX}-certificate-v1"
LEDGER_CANONICAL_SHA256 = "edec39edc8b1207ab87ea9c641dba6d613f009f9258042c2159713df5677011b"
SELF_TOKEN = b'LEDGER_CANONICAL_SHA256 = "' + b"0" * 64 + b'"'
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
LIMIT = 250_000_000
COLUMNS = (
    "group", "parents", "variables", "clauses", "cnf-bytes", "cnf-sha256",
    "lrat-bytes", "lrat-sha256", "xz-bytes", "xz-sha256", "solve-nanoseconds",
    "check-nanoseconds", "artifact",
)
BOUND_PATHS = {
    "manifest": HERE / f"{producer.PREFIX}.tsv",
    "hash-ledger": HERE / f"{producer.PREFIX}-hashes.tsv",
    "scout": HERE / f"{producer.PREFIX}-scout-30s.json",
    "producer": HERE / "m6_clean_sink_B6_l6_root_cardinality.py",
    "checker": HERE / "check_m6_clean_sink_B6_l6_root_cardinality.py",
    "scout-producer": HERE / "m6_clean_sink_B6_l6_root_cardinality_scout.py",
    "certificate-producer": HERE / "certify_m6_clean_sink_B6_l6_root_cardinality.py",
    "hostile-tests": HERE / "test_m6_clean_sink_B6_l6_root_cardinality.py",
    "group-source": HERE / "m6_clean_sink_group_cnf.py",
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            value.update(block)
    return path.stat().st_size, value.hexdigest()


def canonical_verifier_hash(path=Path(__file__)):
    data = path.read_bytes()
    marker = b'LEDGER_CANONICAL_SHA256 = "' + LEDGER_CANONICAL_SHA256.encode("ascii") + b'"'
    if data.count(marker) != 1:
        raise RuntimeError("verifier self-pin marker changed")
    return digest(data.replace(marker, SELF_TOKEN))


def canonical_ledger_hash(path=LEDGER):
    lines = path.read_bytes().splitlines(keepends=True)
    prefix = b"verifier-canonical-sha256\t"
    matches = [index for index, line in enumerate(lines) if line.startswith(prefix)]
    if len(matches) != 1:
        raise RuntimeError("ledger reciprocal-pin row changed")
    lines[matches[0]] = prefix + b"0" * 64 + b"\n"
    return digest(b"".join(lines))


def load_ledger(path=LEDGER):
    data = path.read_bytes()
    lines = data.decode("ascii").splitlines()
    if not lines or lines[0] != FORMAT or data != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("certificate ledger is not canonical ASCII TSV")
    metadata, rows, columns = {}, [], None
    for line in lines[1:]:
        fields = line.split("\t")
        if fields[0] == "columns":
            if columns is not None or len(fields) != 2 or tuple(fields[1].split(",")) != COLUMNS:
                raise RuntimeError("certificate columns changed")
            columns = COLUMNS
        elif columns is None:
            if len(fields) != 2 or fields[0] in metadata:
                raise RuntimeError("malformed certificate metadata")
            metadata[fields[0]] = fields[1]
        else:
            if len(fields) != len(COLUMNS):
                raise RuntimeError("malformed certificate row")
            rows.append(dict(zip(COLUMNS, fields)))
    required = {
        "generated-utc": "2026-09-01",
        "scope": "exact-clean-B6-l6-parent-group-root-cardinality",
        "groups": "1", "parents": "220", "certified-groups": "1",
        "scout-unsat": "1", "solver": "CaDiCaL 1.7.3",
        "solver-binary-sha256": "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292",
        "solver-command": "cadical --lrat --no-binary -q --restart=false --phase=false --seed=3 CNF LRAT",
        "checker": "lrat-check", "checker-binary-sha256": CHECKER_SHA256,
        "compression": "xz -3", "compressor-binary": "/usr/bin/xz",
        "compressor-binary-sha256": "b5b163eb273291934556377ab883b4b2a5d4da50bd0dc0a91774ecc234ccd8d0",
        "compressed-limit-bytes-exclusive": str(LIMIT),
    }
    expected = set(required) | {"verifier-canonical-sha256"} | {
        f"{name}-{suffix}" for name in BOUND_PATHS for suffix in ("bytes", "sha256")
    }
    if columns is None or len(rows) != 1 or set(metadata) != expected or any(
            metadata.get(name) != value for name, value in required.items()):
        raise RuntimeError("certificate metadata or exact scope changed")
    row = rows[0]
    numeric = set(COLUMNS) - {"group", "cnf-sha256", "lrat-sha256", "xz-sha256", "artifact"}
    if any(not row[name].isdigit() for name in numeric) or any(
            re.fullmatch(r"[0-9a-f]{64}", row[name]) is None
            for name in ("cnf-sha256", "lrat-sha256", "xz-sha256")):
        raise RuntimeError("noncanonical certificate row")
    if (row["group"], row["parents"], row["variables"], row["clauses"]) != (
            producer.GROUP, "220", "25849", "184296") or int(row["xz-bytes"]) >= LIMIT:
        raise RuntimeError("certificate row scope or exclusive cap changed")
    return metadata, row


def verify_bindings(metadata, checker=None):
    if canonical_ledger_hash() != LEDGER_CANONICAL_SHA256:
        raise RuntimeError("verifier does not pin canonical ledger")
    if metadata["verifier-canonical-sha256"] != canonical_verifier_hash():
        raise RuntimeError("ledger does not pin canonical verifier")
    for name, path in BOUND_PATHS.items():
        if identity(path) != (int(metadata[f"{name}-bytes"]), metadata[f"{name}-sha256"]):
            raise RuntimeError(f"bound artifact changed: {name}")
    if checker is not None and (not checker.is_absolute() or identity(checker)[1] != CHECKER_SHA256):
        raise RuntimeError("checker path or identity changed")


def artifact_path(row):
    relative = Path(row["artifact"])
    expected = Path("certificates") / f"{producer.PREFIX}.lrat.xz"
    if relative != expected:
        raise RuntimeError("artifact path is outside the exact frozen location")
    artifact = ROOT / relative
    if identity(artifact) != (int(row["xz-bytes"]), row["xz-sha256"]):
        raise RuntimeError("compressed artifact identity changed")
    return artifact


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path)
    parser.add_argument("--no-replay", action="store_true")
    args = parser.parse_args()
    metadata, row = load_ledger()
    checker = args.checker.resolve(strict=True) if args.checker else None
    verify_bindings(metadata, checker)
    artifact = artifact_path(row)
    structural.check_manifest_and_hashes()
    structural.semantic_audit()
    if not args.no_replay:
        if checker is None:
            parser.error("fresh replay requires --checker")
        members, cnf, _, delta = producer.build()
        manifest = producer.manifest_payload(members, cnf, delta)
        with tempfile.TemporaryDirectory(prefix="clean-B6-l6-root-replay-", dir=ROOT) as directory:
            work = Path(directory)
            cnf_path, lrat_path = work / "group.cnf", work / "group.lrat"
            producer.write_cnf(cnf_path, cnf, manifest, delta)
            structural.check(cnf_path)
            if identity(cnf_path) != (int(row["cnf-bytes"]), row["cnf-sha256"]):
                raise RuntimeError("regenerated CNF changed")
            with lzma.open(artifact, "rb") as source, lrat_path.open("wb") as target:
                while block := source.read(1 << 20):
                    target.write(block)
            if identity(lrat_path) != (int(row["lrat-bytes"]), row["lrat-sha256"]):
                raise RuntimeError("raw LRAT changed")
            checked = subprocess.run([str(checker), str(cnf_path), str(lrat_path)], capture_output=True, text=True)
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError("LRAT rejected")
    print(f"PASS group={producer.GROUP} parents=220 xz_bytes={row['xz-bytes']} limit_exclusive={LIMIT}")


if __name__ == "__main__":
    main()
