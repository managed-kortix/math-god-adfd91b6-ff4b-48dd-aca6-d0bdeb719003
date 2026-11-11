#!/usr/bin/env python3
"""Strict fresh replay of exactly 127 frozen singleton-scout UNSAT LRATs."""

import argparse
import ast
import hashlib
import json
import lzma
from pathlib import Path
import re
import subprocess
import tempfile

import check_m6_b7_l6_hard_witness_positive_gain_coordinate_residual_singleton_parent as structural
import m6_b7_l6_hard_witness_positive_gain_coordinate_residual_singleton_parent as producer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGER = HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-singleton-parent-certificates.tsv"
FORMAT = "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-singleton-parent-certificates-v1"
LEDGER_CANONICAL_SHA256 = "1c811d372a2c630faec84a25291bdb6ae8f489b1268c21fb8808dbbbeabe8389"
SELF_TOKEN = b'LEDGER_CANONICAL_SHA256 = "' + b"0" * 64 + b'"'
PREFIX = "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-singleton-parent"
BOUND_PATHS = {
    "singleton-manifest": HERE / f"{PREFIX}.tsv",
    "singleton-hash-ledger": HERE / f"{PREFIX}-hashes.tsv",
    "singleton-scout": HERE / f"{PREFIX}-scout-5s.json",
    "singleton-producer": HERE / f"{PREFIX.replace('-', '_')}.py",
    "singleton-structural-checker": HERE / f"check_{PREFIX.replace('-', '_')}.py",
    "singleton-scout-source": HERE / f"{PREFIX.replace('-', '_')}_scout.py",
    "singleton-test-source": HERE / f"test_{PREFIX.replace('-', '_')}.py",
    "certificate-producer": HERE / f"certify_{PREFIX.replace('-', '_')}.py",
    "certificate-test-source": HERE / f"test_{PREFIX.replace('-', '_')}_certificates.py",
    "residual-manifest": HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-cover.tsv",
    "residual-hash-ledger": HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-cover-hashes.tsv",
    "residual-scout": HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-cover-scout-15s.json",
    "residual-producer": HERE / "m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover.py",
    "residual-structural-checker": HERE / "check_m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover.py",
    "residual-scout-source": HERE / "m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover_scout.py",
    "residual-test-source": HERE / "test_m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover.py",
    "coordinate-certificates": HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-certificates.tsv",
    "coordinate-certificate-verifier": HERE / "verify_m6_b7_l6_hard_witness_positive_gain_coordinate_certificates.py",
    "positive-gain-certificates": HERE / "m6-b7-l6-hard-witness-positive-gain-certificates.tsv",
    "positive-gain-certificate-verifier": HERE / "verify_m6_b7_l6_hard_witness_positive_gain_certificates.py",
    "no-gain-certificates": HERE / "m6-b7-l6-hard-witness-no-gain-certificates.tsv",
    "no-gain-certificate-verifier": HERE / "verify_m6_b7_l6_hard_witness_no_gain_certificates.py",
    "witness-orbit-certificates": HERE / "m6-b7-l6-hard-orbit-certificates.tsv",
    "state-certificates": HERE / "m6-b7-l6-state-certificates.tsv",
}
RUNTIME_SOURCE_NAMES = (
    "check_m6_b7_l6_hard_orbits.py",
    "check_m6_b7_l6_hard_witness_orbits.py",
    "check_m6_b7_l6_hard_witness_positive_gain.py",
    "check_m6_b7_l6_hard_witness_positive_gain_coordinate.py",
    "check_m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover.py",
    "check_m6_b7_l6_hard_witness_positive_gain_coordinate_residual_singleton_parent.py",
    "check_m6_b7_l6_state_split.py",
    "check_m6_clean_sink_group_cnf.py",
    "check_m6_clean_sink_manifest.py",
    "check_m6_parent_cnf.py",
    "m6_b7_l6_hard_orbits.py",
    "m6_b7_l6_hard_witness_orbits.py",
    "m6_b7_l6_hard_witness_positive_gain.py",
    "m6_b7_l6_hard_witness_positive_gain_coordinate.py",
    "m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover.py",
    "m6_b7_l6_hard_witness_positive_gain_coordinate_residual_singleton_parent.py",
    "m6_b7_l6_state_split.py",
    "m6_clean_sink_group_cnf.py",
    "m6_clean_sink_manifest.py",
    "m6_parent_cnf.py",
    "m6_residual_group_cnf.py",
    "snc_cnf.py",
)
for source_name in RUNTIME_SOURCE_NAMES:
    BOUND_PATHS[f"runtime-{source_name[:-3].replace('_', '-')}"] = HERE / source_name
COLUMNS = (
    "membership-ordinal", "key", "residual-leaf-ordinal", "residual-key",
    "parent-ordinal", "accepted-ordinal", "cover-index", "parent-fingerprint",
    "selector", "variables", "clauses", "cnf-bytes", "cnf-sha256", "lrat-bytes",
    "lrat-sha256", "xz-bytes", "xz-sha256", "solve-nanoseconds",
    "check-nanoseconds", "artifact",
)
HEX_COLUMNS = ("parent-fingerprint", "cnf-sha256", "lrat-sha256", "xz-sha256")
DECIMAL_COLUMNS = (
    "membership-ordinal", "residual-leaf-ordinal", "parent-ordinal", "accepted-ordinal",
    "cover-index", "selector", "variables", "clauses", "cnf-bytes", "lrat-bytes",
    "xz-bytes", "solve-nanoseconds", "check-nanoseconds",
)
SOLVER_SHA256 = "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292"
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
LIMIT = 250_000_000
TOTALS = {"cnf-bytes": 1320445141, "lrat-bytes": 909397178, "xz-bytes": 61646844}


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
        "generated-utc": "2026-08-11",
        "base-commit": "b7cdeff6816fd29eedc9633aea7d7adb949d55a5",
        "scope": "frozen-B7-singleton-parent-scout-UNSAT-memberships-only",
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
        "scout-status-sequence-sha256": "1c820b0de4e79a0ac355e9603566eca4a77eedf84f15989a124bdccbb30fbf82",
        "scout-status-totals": "SAT=0,UNSAT=127,TIMEOUT=1255",
        "memberships": "127",
        "artifacts": "127",
        "total-cnf-bytes": str(TOTALS["cnf-bytes"]),
        "total-lrat-bytes": str(TOTALS["lrat-bytes"]),
        "total-xz-bytes": str(TOTALS["xz-bytes"]),
    }
    if any(metadata.get(name) != value for name, value in required.items()):
        raise RuntimeError("frozen certificate metadata changed")
    expected_keys = set(required) | {"membership-ordinals", "verifier-canonical-sha256"} | {
        suffix for name in BOUND_PATHS for suffix in (f"{name}-bytes", f"{name}-sha256")
    }
    if set(metadata) != expected_keys or columns is None or len(rows) != 127:
        raise RuntimeError("certificate ledger framing or scope changed")
    ordinals = tuple(int(row["membership-ordinal"]) for row in rows)
    if ordinals != tuple(sorted(set(ordinals))) or metadata["membership-ordinals"] != ",".join(
            f"{ordinal:04d}" for ordinal in ordinals):
        raise RuntimeError("ordered membership scope changed")
    if any(sum(int(row[name]) for row in rows) != total for name, total in TOTALS.items()):
        raise RuntimeError("certificate totals changed")
    if TOTALS["xz-bytes"] >= LIMIT or data != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("compressed bound or canonical ledger encoding changed")
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
            raise RuntimeError(f"bound transitive source changed: {name}")
    for name in ("coordinate-certificates", "positive-gain-certificates",
                 "no-gain-certificates", "witness-orbit-certificates", "state-certificates"):
        lines = BOUND_PATHS[name].read_text(encoding="ascii").splitlines()
        marker = next((i for i, line in enumerate(lines) if line.startswith("columns\t")), -1)
        if marker < 0:
            raise RuntimeError(f"bound certificate columns absent: {name}")
        columns = lines[marker].split("\t", 1)[1].split(",")
        for line in lines[marker + 1:]:
            row = dict(zip(columns, line.split("\t")))
            artifact = ROOT / row["artifact"]
            if identity(artifact) != (int(row["xz-bytes"]), row["xz-sha256"]):
                raise RuntimeError(f"bound transitive certificate artifact changed: {artifact.name}")


def validate_scout_scope(scout, rows):
    scout_rows = scout.get("rows", [])
    unsat = tuple(row for row in scout_rows if row.get("status") == "UNSAT")
    statuses = tuple(row.get("status") for row in scout_rows)
    encoded = "".join({"SAT": "S", "UNSAT": "U", "TIMEOUT": "T"}.get(status, "?")
                      for status in statuses)
    if len(scout_rows) != 1382 or len(unsat) != 127 or \
            hashlib.sha256(encoded.encode("ascii")).hexdigest() != \
            "1c820b0de4e79a0ac355e9603566eca4a77eedf84f15989a124bdccbb30fbf82":
        raise RuntimeError("singleton scout status scope or order changed")
    for source, record in zip(unsat, rows):
        observed = (f"{source['membership']:04d}", source["key"], f"{source['residual_leaf']:03d}",
                    f"{source['parent_ordinal']:02d}", f"{source['accepted_ordinal']:05d}",
                    f"{source['cover_index']:06d}", source["cnf_sha256"])
        expected = tuple(record[name] for name in (
            "membership-ordinal", "key", "residual-leaf-ordinal", "parent-ordinal",
            "accepted-ordinal", "cover-index", "cnf-sha256",
        ))
        if observed != expected:
            raise RuntimeError("certificate row identity differs from ordered scout UNSAT row")


def artifact_paths(rows):
    paths = []
    for record in rows:
        ordinal = int(record["membership-ordinal"])
        expected = f"certificates/{PREFIX}-membership-{ordinal:04d}.lrat.xz"
        if record["artifact"] != expected:
            raise RuntimeError("artifact path differs from safe exact filename")
        paths.append(record["artifact"])
    if len(paths) != len(set(paths)):
        raise RuntimeError("duplicate singleton certificate artifact path")
    return set(paths)


def validate_compression(rows, limit=LIMIT):
    total = sum(int(row["xz-bytes"]) for row in rows)
    if total != TOTALS["xz-bytes"] or total >= limit:
        raise RuntimeError("compressed artifact total is not the frozen strict bound")
    return total


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path, required=True)
    args = parser.parse_args()
    metadata, rows = load_ledger()
    verify_bindings(metadata)
    if identity(args.checker)[1] != CHECKER_SHA256:
        raise RuntimeError("checker binary is not pinned lrat-check")
    scout = json.loads(BOUND_PATHS["singleton-scout"].read_text(encoding="ascii"))
    validate_scout_scope(scout, rows)
    expected_artifacts = artifact_paths(rows)
    actual_artifacts = {path.relative_to(ROOT).as_posix() for path in
                        (ROOT / "certificates").glob(f"{PREFIX}-membership-*.lrat.xz")}
    if actual_artifacts != expected_artifacts:
        raise RuntimeError("singleton certificate artifact set is not exactly ledger scope")
    validate_compression(rows)

    cover, memberships = producer.load_memberships()
    manifest = producer.manifest_payload(cover, memberships)
    with tempfile.TemporaryDirectory(prefix="m6-singleton-replay-", dir=ROOT) as directory:
        work = Path(directory)
        for position, record in enumerate(rows, 1):
            ordinal = int(record["membership-ordinal"])
            name = f"{PREFIX}-membership-{ordinal:04d}.lrat.xz"
            artifact = ROOT / record["artifact"]
            if identity(artifact) != (int(record["xz-bytes"]), record["xz-sha256"]):
                raise RuntimeError(f"membership {ordinal:04d} compressed identity changed")
            cnf = work / f"membership-{ordinal:04d}.cnf"
            member = memberships[ordinal]
            built, selectors = producer.build_membership(member)
            producer.write_membership(cnf, ordinal, member, built, selectors, manifest)
            if identity(cnf) != (int(record["cnf-bytes"]), record["cnf-sha256"]):
                raise RuntimeError(f"membership {ordinal:04d} CNF regeneration changed")
            structural.check(cnf)
            lrat = work / f"membership-{ordinal:04d}.lrat"
            with lzma.open(artifact, "rb") as source, lrat.open("wb") as target:
                while block := source.read(1 << 20):
                    target.write(block)
            if identity(lrat) != (int(record["lrat-bytes"]), record["lrat-sha256"]):
                raise RuntimeError(f"membership {ordinal:04d} raw LRAT identity changed")
            checked = subprocess.run([str(args.checker), str(cnf), str(lrat)], capture_output=True, text=True)
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError(f"membership {ordinal:04d} LRAT rejected")
            print(f"PASS {position:03d}/127 membership={ordinal:04d} xz={record['xz-bytes']}")
    print("PASS memberships=127 artifacts=127 total_xz_bytes=61646844 limit_exclusive=250000000")


if __name__ == "__main__":
    main()
