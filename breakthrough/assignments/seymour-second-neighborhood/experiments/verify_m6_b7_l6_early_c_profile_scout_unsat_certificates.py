#!/usr/bin/env python3
"""Fresh replay of exactly 26 frozen early-profile SCOUT-UNSAT LRATs."""

import argparse
import ast
import hashlib
import lzma
from pathlib import Path
import re
import subprocess
import tempfile

import check_m6_b7_l6_early_c_profile_census as structural
import m6_b7_l6_early_c_profile_census as producer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGER = HERE / "m6-b7-l6-early-c-profile-scout-unsat-certificates.tsv"
FORMAT = "m6-b7-l6-early-c-profile-scout-unsat-certificates-v1"
LEDGER_CANONICAL_SHA256 = "1bb88e4b16e9d2ae39a3308141be7a7232412e35f14e23f857ac3b6b221ca0fd"
SELF_TOKEN = b'LEDGER_CANONICAL_SHA256 = "' + b"0" * 64 + b'"'
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
LIMIT = 250_000_000
SCOPE = (0, 1, 2, 6, 7, 8, 9, 10, 18, 19, 20, 21, 22, 24, 26, 27, 29,
         30, 44, 45, 46, 48, 50, 51, 52, 53)
COLUMNS = (
    "orbit", "key", "parents", "variables", "clauses", "cnf-bytes", "cnf-sha256",
    "lrat-bytes", "lrat-sha256", "xz-bytes", "xz-sha256", "solve-nanoseconds",
    "check-nanoseconds", "artifact",
)
BOUND_PATHS = {
    "census-manifest": HERE / "m6-b7-l6-early-c-profile-census.tsv",
    "census-hash-ledger": HERE / "m6-b7-l6-early-c-profile-hashes.tsv",
    "census-scout": HERE / "m6-b7-l6-early-c-profile-scout.json",
    "census-provenance": HERE / "m6-b7-l6-early-c-profile-provenance.tsv",
    "certificate-producer": HERE / "certify_m6_b7_l6_early_c_profile_scout_unsat.py",
    "census-documentation": ROOT / "attempts/frozen-b7-l6-early-c-profile-census.md",
    "experiments-documentation": HERE / "README.md",
    "notebook": ROOT / "notebook.md",
}


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


def runtime_source_closure():
    local = {path.stem: path.resolve() for path in HERE.glob("*.py")}
    pending, visited = [Path(__file__).resolve()], set()
    while pending:
        path = pending.pop()
        if path in visited:
            continue
        visited.add(path)
        tree = ast.parse(path.read_text(encoding="ascii"), filename=str(path))
        names = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.extend(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names.append(node.module.split(".", 1)[0])
        pending.extend(local[name] for name in names if name in local)
    visited.remove(Path(__file__).resolve())
    return tuple(sorted(visited))


def load_ledger(path=LEDGER):
    data = path.read_bytes()
    lines = data.decode("ascii").splitlines()
    if not lines or lines[0] != FORMAT or data != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("certificate ledger is not canonical ASCII TSV")
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
            if any(re.fullmatch(r"[0-9a-f]{64}", row[name]) is None
                   for name in ("cnf-sha256", "lrat-sha256", "xz-sha256")):
                raise RuntimeError("noncanonical certificate row hash")
            rows.append(row)
    required = {
        "generated-utc": "2026-08-23",
        "scope": "frozen-B7-l6-early-C-profile-selected-26-SCOUT-UNSAT-orbits-only",
        "base-commit": "3e176b4675a4d4676cae9eeab8399a74ef19f265",
        "scope-orbits": ",".join(f"{value:02d}" for value in SCOPE),
        "census-orbits": "60", "census-scout-unsat": "31", "certified-orbits": "26",
        "solver": "CaDiCaL 1.7.3",
        "solver-binary-sha256": "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292",
        "solver-command": "cadical --lrat --no-binary -q CNF LRAT", "solver-required-exit": "20",
        "checker": "lrat-check", "checker-binary-sha256": CHECKER_SHA256,
        "checker-required-output": "c VERIFIED", "compression": "xz -3",
        "compressor-binary": "/usr/bin/xz",
        "compressor-binary-sha256": "b5b163eb273291934556377ab883b4b2a5d4da50bd0dc0a91774ecc234ccd8d0",
        "compressed-limit-bytes": str(LIMIT), "total-lrat-bytes": "197309757",
        "total-xz-bytes": "13906564",
    }
    runtime_keys = {f"runtime-{path.name[:-3].replace('_', '-')}-{suffix}"
                    for path in runtime_source_closure() for suffix in ("bytes", "sha256")}
    expected = set(required) | {"verifier-canonical-sha256"} | runtime_keys | {
        f"{name}-{suffix}" for name in BOUND_PATHS for suffix in ("bytes", "sha256")
    }
    if columns is None or len(rows) != len(SCOPE) or set(metadata) != expected or \
            any(metadata.get(name) != value for name, value in required.items()):
        raise RuntimeError("certificate metadata or exact scope changed")
    if tuple(int(row["orbit"]) for row in rows) != SCOPE:
        raise RuntimeError("certificate row scope or order changed")
    if sum(int(row["lrat-bytes"]) for row in rows) != 197_309_757 or \
            sum(int(row["xz-bytes"]) for row in rows) != 13_906_564 or \
            int(metadata["total-xz-bytes"]) > LIMIT:
        raise RuntimeError("proof byte total differs or exceeds 250MB")
    return metadata, rows


def verify_bindings(metadata, checker):
    if canonical_ledger_hash() != LEDGER_CANONICAL_SHA256:
        raise RuntimeError("verifier does not pin canonical ledger")
    if metadata["verifier-canonical-sha256"] != canonical_verifier_hash(Path(__file__)):
        raise RuntimeError("ledger does not pin canonical verifier")
    for name, path in BOUND_PATHS.items():
        if identity(path) != (int(metadata[f"{name}-bytes"]), metadata[f"{name}-sha256"]):
            raise RuntimeError(f"bound census provenance/artifact changed: {name}")
    for path in runtime_source_closure():
        name = f"runtime-{path.name[:-3].replace('_', '-')}"
        if identity(path) != (int(metadata[f"{name}-bytes"]), metadata[f"{name}-sha256"]):
            raise RuntimeError(f"bound transitive runtime source changed: {path.name}")
    if checker != checker.resolve(strict=True):
        raise RuntimeError("checker path is not explicit and canonical")
    if identity(checker)[1] != CHECKER_SHA256:
        raise RuntimeError("checker binary is not pinned lrat-check")
    if identity(Path(metadata["compressor-binary"]))[1] != metadata["compressor-binary-sha256"]:
        raise RuntimeError("compressor binary identity changed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path, required=True)
    args = parser.parse_args()
    checker = args.checker.resolve(strict=True)
    metadata, rows = load_ledger()
    verify_bindings(metadata, checker)
    orbits = producer.load_orbits()
    manifest = producer.manifest_payload(orbits)
    scout = {ordinal: status for ordinal, status, _, _ in producer.scout_sequence(orbits)}
    if len(orbits) != 60 or tuple(i for i in SCOPE if scout.get(i) == "UNSAT") != SCOPE:
        raise RuntimeError("scope differs from committed 60-orbit census SCOUT-UNSAT rows")
    with tempfile.TemporaryDirectory(prefix="early-profile-replay-", dir=ROOT) as directory:
        work = Path(directory)
        for position, row in enumerate(rows, 1):
            ordinal = int(row["orbit"])
            name = f"m6-b7-l6-early-c-profile-orbit-{ordinal:02d}.lrat.xz"
            if row["artifact"] != f"certificates/{name}":
                raise RuntimeError("artifact path differs from exact safe filename")
            artifact = ROOT / row["artifact"]
            if identity(artifact) != (int(row["xz-bytes"]), row["xz-sha256"]):
                raise RuntimeError(f"orbit {ordinal:02d} compressed identity changed")
            cnf_path, lrat_path = work / f"o{ordinal:02d}.cnf", work / f"o{ordinal:02d}.lrat"
            cnf, selectors = producer.build_orbit(orbits[ordinal])
            producer.write_orbit(cnf_path, ordinal, orbits[ordinal], cnf, selectors, manifest)
            structural.check(cnf_path)
            if identity(cnf_path) != (int(row["cnf-bytes"]), row["cnf-sha256"]):
                raise RuntimeError(f"orbit {ordinal:02d} regenerated CNF changed")
            with lzma.open(artifact, "rb") as source, lrat_path.open("wb") as target:
                while block := source.read(1 << 20):
                    target.write(block)
            if identity(lrat_path) != (int(row["lrat-bytes"]), row["lrat-sha256"]):
                raise RuntimeError(f"orbit {ordinal:02d} raw LRAT identity changed")
            checked = subprocess.run([str(checker), str(cnf_path), str(lrat_path)],
                                     capture_output=True, text=True)
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError(f"orbit {ordinal:02d} LRAT rejected")
            print(f"PASS {position:02d}/26 orbit={ordinal:02d} xz={row['xz-bytes']}")
    print("PASS orbits=26 total_xz_bytes=13906564 limit_bytes=250000000")


if __name__ == "__main__":
    main()
