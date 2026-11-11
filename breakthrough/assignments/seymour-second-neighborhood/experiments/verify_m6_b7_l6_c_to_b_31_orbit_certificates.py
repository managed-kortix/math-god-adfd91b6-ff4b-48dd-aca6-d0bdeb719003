#!/usr/bin/env python3
"""Strictly replay the two frozen C-to-B (3,1) LRAT certificates."""

import argparse
import ast
import hashlib
import lzma
import re
import subprocess
import tempfile
from pathlib import Path

import check_m6_b7_l6_c_to_b_31_orbits as structural
import m6_b7_l6_c_to_b_31_orbits as producer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGER = HERE / "m6-b7-l6-c-to-b-31-orbit-certificates.tsv"
FORMAT = "m6-b7-l6-c-to-b-31-orbit-certificates-v2"
LEDGER_CANONICAL_SHA256 = "00a1117004fe452b2d1b675e6cd06cd760dad4e6ce9c94df53ee497dd98f3e6a"
SELF_TOKEN = b'LEDGER_CANONICAL_SHA256 = "' + b"0" * 64 + b'"'
SOLVER_SHA256 = "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292"
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
LIMIT = 250_000_000
BOUND_PATHS = {
    "orbit-manifest": HERE / "m6-b7-l6-c-to-b-31-orbits.tsv",
    "cnf-hash-ledger": HERE / "m6-b7-l6-c-to-b-31-orbits-hashes.tsv",
    "producer": HERE / "m6_b7_l6_c_to_b_31_orbits.py",
    "structural-checker": HERE / "check_m6_b7_l6_c_to_b_31_orbits.py",
    "test-source": HERE / "test_m6_b7_l6_c_to_b_31_orbits.py",
    "certificate-producer": HERE / "certify_m6_b7_l6_c_to_b_31_orbits.py",
}
RUNTIME_SOURCE_NAMES = (
    "check_m6_b7_l6_c_to_b_31_orbits.py",
    "check_m6_clean_sink_group_cnf.py",
    "check_m6_clean_sink_manifest.py",
    "check_m6_parent_cnf.py",
    "m6_b7_l6_c_to_b_31_orbits.py",
    "m6_clean_sink_group_cnf.py",
    "m6_clean_sink_manifest.py",
    "m6_parent_cnf.py",
    "m6_residual_group_cnf.py",
    "snc_cnf.py",
)
for source_name in RUNTIME_SOURCE_NAMES:
    BOUND_PATHS.setdefault(f"runtime-{source_name[:-3].replace('_', '-')}", HERE / source_name)
COLUMNS = ("t", "cnf-bytes", "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes",
           "xz-sha256", "solve-nanoseconds", "check-nanoseconds", "artifact")


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
    local_modules = {path.stem: path for path in HERE.glob("*.py")}
    pending, visited = [Path(__file__).resolve()], set()
    while pending:
        path = pending.pop()
        if path in visited:
            continue
        visited.add(path)
        tree = ast.parse(path.read_text(encoding="ascii"), filename=str(path))
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imports.append(node.module.split(".", 1)[0])
        pending.extend(local_modules[name] for name in imports
                       if name in local_modules and local_modules[name] not in visited)
    visited.remove(Path(__file__).resolve())
    return tuple(sorted(path.name for path in visited))


def load_ledger(path=LEDGER):
    data = path.read_bytes()
    lines = data.decode("ascii").splitlines()
    if not lines or lines[0] != FORMAT or data != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("certificate ledger format or framing differs")
    metadata, order, rows, columns = {}, [], [], None
    for line in lines[1:]:
        fields = line.split("\t")
        if fields[0] == "columns":
            if columns is not None or tuple(fields[1].split(",")) != COLUMNS:
                raise RuntimeError("certificate columns differ")
            columns = COLUMNS
        elif columns is None:
            if len(fields) != 2 or fields[0] in metadata:
                raise RuntimeError("certificate metadata malformed")
            metadata[fields[0]] = fields[1]
            order.append(fields[0])
        else:
            if len(fields) != len(COLUMNS):
                raise RuntimeError("certificate row malformed")
            rows.append(dict(zip(COLUMNS, fields)))
    required = {
        "generated-utc": "2026-08-18", "scope": "frozen-B7-l6-ordered-C-to-B-(3,1)-only",
        "base": "global robust-witness and arc-minimal families; no selected witness units",
        "solver": "CaDiCaL 1.7.3", "solver-binary-sha256": SOLVER_SHA256,
        "solver-command": "cadical --lrat --no-binary -q CNF LRAT", "solver-required-exit": "20",
        "checker": "lrat-check", "checker-binary-sha256": CHECKER_SHA256,
        "checker-required-output": "c VERIFIED", "compression": "xz -3",
        "compressed-limit-bytes-exclusive": str(LIMIT), "groups": "2", "artifacts": "2",
        "total-xz-bytes": "36404128",
    }
    expected_keys = set(required) | {"verifier-canonical-sha256"} | {
        suffix for name in BOUND_PATHS for suffix in (f"{name}-bytes", f"{name}-sha256")
    }
    if columns is None or len(rows) != 2 or set(metadata) != expected_keys or \
            any(metadata.get(key) != value for key, value in required.items()):
        raise RuntimeError("certificate metadata or exact scope differs")
    expected_order = ["generated-utc", "scope", "base"]
    for name in BOUND_PATHS:
        expected_order.extend((f"{name}-bytes", f"{name}-sha256"))
    expected_order.extend(("verifier-canonical-sha256", "solver", "solver-binary-sha256",
                           "solver-command", "solver-required-exit", "checker",
                           "checker-binary-sha256", "checker-required-output", "compression",
                           "compressed-limit-bytes-exclusive", "groups", "artifacts", "total-xz-bytes"))
    if order != expected_order:
        raise RuntimeError("certificate metadata order differs")
    expected_rows = (
        ("0", "10402527", "0c06a73c9308bae4eee1b309362485d24ed6508c7de8e64bf87c647805048b5f", "112111657", "5ea2cb24af68ab9bfd8ad208da63277a2647c4cca50031244e8ef0fce22071c0", "22000348", "9d136d538658ad44326dba02c554fec6cf13ee845e3c8c0d6a0baacc9bab9282", "21196117042", "2331729804", "certificates/m6-b7-l6-c-to-b-31-t0.lrat.xz"),
        ("1", "10402526", "d6bc88cf265db8aaaf5ff6f93160c0ca24bb7c1ba9341ad5704c9f29795eae2a", "77217064", "d40c40103b31cd9798768992f6eaaf09caecf34809adf7d7f7697b45256ad20f", "14403780", "db833fb632b84917217ebd68d98ee7381f8a9332c5620bded2d1c6b928972be3", "10280325285", "1656620000", "certificates/m6-b7-l6-c-to-b-31-t1.lrat.xz"),
    )
    if tuple(tuple(row[name] for name in COLUMNS) for row in rows) != expected_rows:
        raise RuntimeError("canonical certificate rows differ")
    if sum(int(row["xz-bytes"]) for row in rows) != 36404128 or 36404128 >= LIMIT:
        raise RuntimeError("compressed total differs or violates strict bound")
    return metadata, rows


def verify_bindings(metadata):
    if canonical_ledger_hash() != LEDGER_CANONICAL_SHA256:
        raise RuntimeError("verifier does not pin the canonical ledger")
    if metadata["verifier-canonical-sha256"] != canonical_verifier_hash(Path(__file__)):
        raise RuntimeError("ledger does not pin the canonical verifier")
    if runtime_source_closure() != RUNTIME_SOURCE_NAMES:
        raise RuntimeError("verifier runtime Python dependency closure changed")
    for name, path in BOUND_PATHS.items():
        if identity(path) != (int(metadata[f"{name}-bytes"]), metadata[f"{name}-sha256"]):
            raise RuntimeError(f"bound transitive runtime/source changed: {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path, required=True)
    args = parser.parse_args()
    metadata, rows = load_ledger()
    verify_bindings(metadata)
    if identity(args.checker)[1] != CHECKER_SHA256:
        raise RuntimeError("checker binary is not pinned lrat-check")
    all_parents, parents = producer.load_parents()
    manifest = producer.manifest_payload(all_parents, parents)
    with tempfile.TemporaryDirectory(prefix="m6-31-replay-", dir=ROOT) as directory:
        work = Path(directory)
        for t, row in enumerate(rows):
            artifact = ROOT / row["artifact"]
            if identity(artifact) != (int(row["xz-bytes"]), row["xz-sha256"]):
                raise RuntimeError(f"t={t} compressed artifact identity differs")
            cnf_path, lrat_path = work / f"t{t}.cnf", work / f"t{t}.lrat"
            cnf, selectors = producer.build_group(t, parents)
            producer.write_group(cnf_path, t, cnf, selectors, manifest, parents)
            structural.check(cnf_path)
            if identity(cnf_path) != (int(row["cnf-bytes"]), row["cnf-sha256"]):
                raise RuntimeError(f"t={t} regenerated CNF differs")
            with lzma.open(artifact, "rb") as source, lrat_path.open("wb") as target:
                while block := source.read(1 << 20):
                    target.write(block)
            if identity(lrat_path) != (int(row["lrat-bytes"]), row["lrat-sha256"]):
                raise RuntimeError(f"t={t} raw LRAT identity differs")
            checked = subprocess.run([str(args.checker), str(cnf_path), str(lrat_path)],
                                     capture_output=True, text=True)
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError(f"t={t} LRAT rejected")
            print(f"PASS t={t} cnf_sha256={row['cnf-sha256']} lrat_sha256={row['lrat-sha256']} xz_sha256={row['xz-sha256']}")
    print("PASS certificates=2 compatible_parents=10 compressed_bytes=36404128 limit=250000000")


if __name__ == "__main__":
    main()
