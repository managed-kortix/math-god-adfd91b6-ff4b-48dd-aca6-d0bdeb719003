#!/usr/bin/env python3
"""Strict fresh replay of the frozen grouped residual leaf 129 LRAT."""

import argparse
import ast
import hashlib
import lzma
from pathlib import Path
import re
import subprocess
import tempfile

import check_m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual as structural
import m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual as producer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREFIX = "m6-b7-l6-hard-witness-positive-gain-coordinate-grouped-residual"
LEDGER = HERE / f"{PREFIX}-leaf-129-certificate.tsv"
FORMAT = f"{PREFIX}-leaf-129-certificate-v1"
LEDGER_CANONICAL_SHA256 = "d4259dab9513c47fc6aef12df9751529774249633b838519011747d58535f3cd"
SELF_TOKEN = b'LEDGER_CANONICAL_SHA256 = "' + b"0" * 64 + b'"'
ARTIFACT = ROOT / "certificates" / f"{PREFIX}-leaf-129.lrat.xz"
BOUND_PATHS = {
    "grouped-manifest": HERE / f"{PREFIX}.tsv",
    "grouped-hash-ledger": HERE / f"{PREFIX}-hashes.tsv",
    "grouped-scout": HERE / f"{PREFIX}-scout-20s.json",
    "grouped-producer": HERE / "m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual.py",
    "grouped-structural-checker": HERE / "check_m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual.py",
    "grouped-test-source": HERE / "test_m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual.py",
    "certificate-test-source": HERE / "test_m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual_leaf_129_certificate.py",
    "singleton-certificate-ledger": HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-singleton-parent-certificates.tsv",
    "singleton-certificate-verifier": HERE / "verify_m6_b7_l6_hard_witness_positive_gain_coordinate_residual_singleton_parent_certificates.py",
}
RUNTIME_SOURCE_NAMES = (
    "check_m6_b7_l6_hard_orbits.py",
    "check_m6_b7_l6_hard_witness_orbits.py",
    "check_m6_b7_l6_hard_witness_positive_gain.py",
    "check_m6_b7_l6_hard_witness_positive_gain_coordinate.py",
    "check_m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual.py",
    "check_m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover.py",
    "check_m6_b7_l6_state_split.py",
    "check_m6_clean_sink_group_cnf.py",
    "check_m6_clean_sink_manifest.py",
    "check_m6_parent_cnf.py",
    "m6_b7_l6_hard_orbits.py",
    "m6_b7_l6_hard_witness_orbits.py",
    "m6_b7_l6_hard_witness_positive_gain.py",
    "m6_b7_l6_hard_witness_positive_gain_coordinate.py",
    "m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual.py",
    "m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover.py",
    "m6_b7_l6_state_split.py",
    "m6_clean_sink_group_cnf.py",
    "m6_clean_sink_manifest.py",
    "m6_parent_cnf.py",
    "m6_residual_group_cnf.py",
    "snc_cnf.py",
)
for source_name in RUNTIME_SOURCE_NAMES:
    key = f"runtime-{source_name[:-3].replace('_', '-')}"
    BOUND_PATHS.setdefault(key, HERE / source_name)
SOLVER_SHA256 = "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292"
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
COLUMNS = ("leaf-ordinal", "key", "width", "surviving-memberships", "variables", "clauses",
           "cnf-bytes", "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes", "xz-sha256",
           "artifact")


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
    pending = [Path(__file__).resolve()]
    visited = set()
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
        raise RuntimeError("certificate ledger format or framing changed")
    metadata, metadata_order, row, columns = {}, [], None, None
    for line in lines[1:]:
        fields = line.split("\t")
        if fields[0] == "columns":
            if columns is not None or tuple(fields[1].split(",")) != COLUMNS:
                raise RuntimeError("certificate columns changed")
            columns = COLUMNS
        elif columns is None:
            if len(fields) != 2 or fields[0] in metadata:
                raise RuntimeError("certificate metadata malformed")
            metadata[fields[0]] = fields[1]
            metadata_order.append(fields[0])
        else:
            if row is not None or len(fields) != len(COLUMNS):
                raise RuntimeError("certificate scope is not exactly one row")
            row = dict(zip(COLUMNS, fields))
    if columns is None or row is None:
        raise RuntimeError("certificate row absent")
    required = {
        "generated-utc": "2026-08-12",
        "scope": "frozen-grouped-residual-leaf-129-only",
        "grouped-campaign": "153-leaf/1255-selector singleton-certified residual",
        "singleton-ancestry": "exactly the bound 127-row checked singleton certificate ledger/verifier",
        "solver": "CaDiCaL 1.7.3",
        "solver-binary-sha256": SOLVER_SHA256,
        "solver-command": "cadical --lrat --no-binary -q CNF LRAT",
        "checker": "lrat-check",
        "checker-binary-sha256": CHECKER_SHA256,
        "checker-required-output": "c VERIFIED",
        "compression": "xz -3",
    }
    expected_keys = set(required) | {"verifier-canonical-sha256"} | {
        suffix for name in BOUND_PATHS for suffix in (f"{name}-bytes", f"{name}-sha256")
    }
    if any(metadata.get(name) != value for name, value in required.items()) or set(metadata) != expected_keys:
        raise RuntimeError("certificate metadata changed")
    expected_order = ["generated-utc", "scope", "grouped-campaign", "singleton-ancestry"]
    for name in BOUND_PATHS:
        expected_order.extend((f"{name}-bytes", f"{name}-sha256"))
    expected_order.extend(("verifier-canonical-sha256", "solver", "solver-binary-sha256",
                           "solver-command", "checker", "checker-binary-sha256",
                           "checker-required-output", "compression"))
    if metadata_order != expected_order:
        raise RuntimeError("certificate metadata order changed")
    for name, value in metadata.items():
        if name.endswith("-bytes") and (not value.isdigit() or str(int(value)) != value):
            raise RuntimeError(f"certificate byte field is noncanonical: {name}")
        if name.endswith("-sha256") and re.fullmatch(r"[0-9a-f]{64}", value) is None:
            raise RuntimeError(f"certificate hash field is noncanonical: {name}")
    expected_row = {
        "leaf-ordinal": "129", "key": "o37-w01-c16", "width": "2",
        "surviving-memberships": "1142,1144", "variables": "23618", "clauses": "143056",
        "cnf-bytes": "10382345", "cnf-sha256": "e89b0f74972ee8f76f0cda2227523516933f10b13b914b18193beec97ccc664f",
        "lrat-bytes": "79502883", "lrat-sha256": "747540b5714e32e4164ae41dd852ae1ab360c36f3001abde4824ad2ca862b23e",
        "xz-bytes": "15420984", "xz-sha256": "f4387b4de1e4968f17d4031fc73e8286224145cb0ff00b66acae6c3a2088dcec",
        "artifact": f"certificates/{PREFIX}-leaf-129.lrat.xz",
    }
    if row != expected_row:
        raise RuntimeError("leaf 129 certificate row changed")
    return metadata, row


def verify_bindings(metadata):
    if canonical_ledger_hash() != LEDGER_CANONICAL_SHA256:
        raise RuntimeError("verifier does not pin the canonical ledger")
    if metadata["verifier-canonical-sha256"] != canonical_verifier_hash(Path(__file__)):
        raise RuntimeError("ledger does not pin the canonical verifier")
    if runtime_source_closure() != RUNTIME_SOURCE_NAMES:
        raise RuntimeError("leaf 129 verifier runtime Python dependency closure changed")
    for name, path in BOUND_PATHS.items():
        expected = int(metadata[f"{name}-bytes"]), metadata[f"{name}-sha256"]
        if identity(path) != expected:
            raise RuntimeError(f"bound campaign or ancestry input changed: {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path, required=True)
    args = parser.parse_args()
    metadata, row = load_ledger()
    verify_bindings(metadata)
    if identity(args.checker)[1] != CHECKER_SHA256:
        raise RuntimeError("checker binary is not pinned lrat-check")
    if identity(ARTIFACT) != (int(row["xz-bytes"]), row["xz-sha256"]):
        raise RuntimeError("compressed leaf 129 artifact identity changed")
    groups = producer.load_groups()
    manifest = producer.manifest_payload(groups)
    group = groups[129]
    with tempfile.TemporaryDirectory(prefix="m6-grouped-leaf-129-replay-", dir=ROOT) as directory:
        work = Path(directory)
        cnf_path = work / "leaf-129.cnf"
        cnf, selectors = producer.build_group(group)
        producer.write_group(cnf_path, group, cnf, selectors, manifest)
        if identity(cnf_path) != (int(row["cnf-bytes"]), row["cnf-sha256"]):
            raise RuntimeError("fresh leaf 129 CNF identity changed")
        structural.check(cnf_path)
        lrat_path = work / "leaf-129.lrat"
        with lzma.open(ARTIFACT, "rb") as source, lrat_path.open("wb") as target:
            while block := source.read(1 << 20):
                target.write(block)
        if identity(lrat_path) != (int(row["lrat-bytes"]), row["lrat-sha256"]):
            raise RuntimeError("decompressed leaf 129 LRAT identity changed")
        checked = subprocess.run([str(args.checker), str(cnf_path), str(lrat_path)],
                                 capture_output=True, text=True)
        if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
            raise RuntimeError("leaf 129 LRAT rejected")
    print(f"PASS grouped-leaf=129 key={row['key']} width=2 xz_bytes={row['xz-bytes']} "
          f"xz_sha256={row['xz-sha256']}")


if __name__ == "__main__":
    main()
