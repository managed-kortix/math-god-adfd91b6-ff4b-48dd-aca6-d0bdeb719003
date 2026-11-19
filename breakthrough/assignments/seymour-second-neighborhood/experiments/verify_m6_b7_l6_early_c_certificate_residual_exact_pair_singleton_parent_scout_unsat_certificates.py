#!/usr/bin/env python3
"""Strict fresh replay of exactly 68 frozen exact-pair singleton scout-UNSAT LRATs."""

import argparse
import ast
import hashlib
import json
import lzma
from pathlib import Path
import re
import subprocess
import tempfile

import check_m6_b7_l6_early_c_certificate_residual_exact_pair_singleton_parent as structural
import m6_b7_l6_early_c_certificate_residual_exact_pair_singleton_parent as producer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREFIX = producer.PREFIX
LEDGER = HERE / f"{PREFIX}-scout-unsat-certificates.tsv"
FORMAT = f"{PREFIX}-scout-unsat-certificates-v1"
LEDGER_CANONICAL_SHA256 = "17d9a7927bcb912dc550fe571edf1388520fc1daa92b9945581eb7ebaf0a4d18"
SELF_TOKEN = b'LEDGER_CANONICAL_SHA256 = "' + b"0" * 64 + b'"'
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
LIMIT = 250_000_000
TOTALS = {"cnf-bytes": 707414473, "lrat-bytes": 484924019, "xz-bytes": 32389520}
COLUMNS = (
    "membership", "key", "cell", "source-child", "parent", "selector", "variables",
    "clauses", "cnf-bytes", "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes",
    "xz-sha256", "solve-nanoseconds", "check-nanoseconds", "artifact",
)
BOUND_PATHS = {
    "singleton-manifest": HERE / f"{PREFIX}.tsv",
    "singleton-hash-ledger": HERE / f"{PREFIX}-hashes.tsv",
    "singleton-scout": HERE / f"{PREFIX}-scout-5s.json",
    "grouped-manifest": HERE / "m6-b7-l6-early-c-certificate-residual-exact-pair-orbits.tsv",
    "grouped-hash-ledger": HERE / "m6-b7-l6-early-c-certificate-residual-exact-pair-hashes.tsv",
    "inaccessible-certificates": HERE / "m6-b7-l6-early-c-inaccessible-pair-scout-unsat-certificates.tsv",
    "inaccessible-certificate-verifier": HERE / "verify_m6_b7_l6_early_c_inaccessible_pair_scout_unsat_certificates.py",
    "certificate-producer": HERE / f"certify_{PREFIX.replace('-', '_')}_scout_unsat.py",
    "hostile-tests": HERE / f"test_{PREFIX.replace('-', '_')}_scout_unsat_certificates.py",
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
    matches = [index for index, line in enumerate(lines) if line.startswith(prefix)]
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


def frozen_scope():
    structural.check_scout()
    scout = json.loads(structural.SCOUT.read_text(encoding="ascii"))
    rows = scout.get("rows", [])
    scope = tuple(row["membership"] for row in rows if row.get("status") == "UNSAT")
    statuses = "".join({"SAT": "S", "UNSAT": "U", "TIMEOUT": "T"}.get(
        row.get("status"), "?") for row in rows)
    if len(rows) != 101 or len(scope) != 68 or digest(statuses.encode("ascii")) != \
            structural.SCOUT_STATUS_SHA256:
        raise RuntimeError("exact frozen singleton scout scope changed")
    return scope


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
                raise RuntimeError("malformed or duplicate certificate metadata")
            metadata[fields[0]] = fields[1]
        else:
            if len(fields) != len(COLUMNS):
                raise RuntimeError("malformed certificate row")
            row = dict(zip(COLUMNS, fields))
            decimal = set(COLUMNS) - {"key", "cnf-sha256", "lrat-sha256", "xz-sha256", "artifact"}
            if any(not row[name].isdigit() for name in decimal) or any(
                    re.fullmatch(r"[0-9a-f]{64}", row[name]) is None
                    for name in ("cnf-sha256", "lrat-sha256", "xz-sha256")):
                raise RuntimeError("noncanonical certificate row")
            rows.append(row)
    required = {
        "generated-utc": "2026-08-26",
        "base-commit": "6068e283fc21fadc73c1317db1b5625886904cad",
        "scope": "6068e28-exact-pair-singleton-frozen-scout-UNSAT-memberships-only",
        "campaign-memberships": "101", "scout-unsat": "68", "scout-timeout": "33",
        "certified-memberships": "68", "scout-status-sequence-sha256": structural.SCOUT_STATUS_SHA256,
        "solver": "CaDiCaL 1.7.3",
        "solver-source-commit": "38e073b389a877b0a0d3c91136d2443ab95fdeba",
        "solver-binary-sha256": "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292",
        "solver-command": "cadical --lrat --no-binary -q CNF LRAT", "solver-required-exit": "20",
        "checker": "lrat-check", "checker-source-commit": "2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
        "checker-binary-sha256": CHECKER_SHA256, "checker-required-output": "c VERIFIED",
        "compression": "xz -3", "compressor-binary": "/usr/bin/xz",
        "compressor-binary-sha256": "b5b163eb273291934556377ab883b4b2a5d4da50bd0dc0a91774ecc234ccd8d0",
        "compressed-limit-bytes-exclusive": str(LIMIT),
        "total-cnf-bytes": str(TOTALS["cnf-bytes"]),
        "total-lrat-bytes": str(TOTALS["lrat-bytes"]),
        "total-xz-bytes": str(TOTALS["xz-bytes"]),
    }
    runtime_keys = {f"runtime-{path.name[:-3].replace('_', '-')}-{suffix}"
                    for path in runtime_source_closure() for suffix in ("bytes", "sha256")}
    expected = set(required) | {"membership-ordinals", "verifier-canonical-sha256"} | runtime_keys | {
        f"{name}-{suffix}" for name in BOUND_PATHS for suffix in ("bytes", "sha256")}
    scope = frozen_scope()
    if columns is None or len(rows) != 68 or set(metadata) != expected or any(
            metadata.get(name) != value for name, value in required.items()):
        raise RuntimeError("certificate metadata or exact scope changed")
    ordinals = tuple(int(row["membership"]) for row in rows)
    if ordinals != scope or metadata["membership-ordinals"] != ",".join(f"{x:03d}" for x in scope):
        raise RuntimeError("certificate rows do not equal ordered complete scout-UNSAT set")
    if any(sum(int(row[name]) for row in rows) != total for name, total in TOTALS.items()) or \
            TOTALS["xz-bytes"] >= LIMIT:
        raise RuntimeError("certificate totals or exclusive compressed cap changed")
    return metadata, rows


def verify_bindings(metadata, checker=None):
    if canonical_ledger_hash() != LEDGER_CANONICAL_SHA256:
        raise RuntimeError("verifier does not pin canonical ledger")
    if metadata["verifier-canonical-sha256"] != canonical_verifier_hash(Path(__file__)):
        raise RuntimeError("ledger does not pin canonical verifier")
    for name, path in BOUND_PATHS.items():
        if identity(path) != (int(metadata[f"{name}-bytes"]), metadata[f"{name}-sha256"]):
            raise RuntimeError(f"bound artifact changed: {name}")
    for path in runtime_source_closure():
        name = f"runtime-{path.name[:-3].replace('_', '-')}"
        if identity(path) != (int(metadata[f"{name}-bytes"]), metadata[f"{name}-sha256"]):
            raise RuntimeError(f"bound transitive runtime source changed: {path.name}")
    ancestor_lines = BOUND_PATHS["inaccessible-certificates"].read_text(encoding="ascii").splitlines()
    marker = next((index for index, line in enumerate(ancestor_lines) if line.startswith("columns\t")), -1)
    if marker < 0:
        raise RuntimeError("bound ancestor certificate columns absent")
    ancestor_columns = ancestor_lines[marker].split("\t", 1)[1].split(",")
    for line in ancestor_lines[marker + 1:]:
        row = dict(zip(ancestor_columns, line.split("\t")))
        artifact = ROOT / row["artifact"]
        if identity(artifact) != (int(row["xz-bytes"]), row["xz-sha256"]):
            raise RuntimeError(f"bound transitive ancestor artifact changed: {artifact.name}")
    if checker is not None and (checker != checker.resolve(strict=True) or
                                identity(checker)[1] != CHECKER_SHA256):
        raise RuntimeError("checker path or binary is not pinned lrat-check")
    compressor = Path(metadata["compressor-binary"])
    if identity(compressor)[1] != metadata["compressor-binary-sha256"]:
        raise RuntimeError("compressor binary identity changed")


def artifact_paths(rows):
    expected = set()
    for row in rows:
        name = f"{PREFIX}-membership-{int(row['membership']):03d}.lrat.xz"
        if row["artifact"] != f"certificates/{name}" or row["artifact"] in expected:
            raise RuntimeError("artifact path is not unique canonical scoped name")
        expected.add(row["artifact"])
    actual = {path.relative_to(ROOT).as_posix() for path in (ROOT / "certificates").glob(
        f"{PREFIX}-membership-*.lrat.xz")}
    if actual != expected:
        raise RuntimeError("certificate artifact set differs from exact ledger scope")
    return expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path, required=True)
    args = parser.parse_args()
    checker = args.checker.resolve(strict=True)
    metadata, rows = load_ledger()
    verify_bindings(metadata, checker)
    artifact_paths(rows)
    cells, memberships = producer.load_memberships()
    manifest = producer.manifest_payload(cells, memberships)
    with tempfile.TemporaryDirectory(prefix="exact-pair-singleton-68-replay-", dir=ROOT) as directory:
        work = Path(directory)
        for position, row in enumerate(rows, 1):
            ordinal = int(row["membership"])
            member = memberships[ordinal]
            cell, record, parent = member
            cnf_path = work / f"m{ordinal:03d}.cnf"
            lrat_path = work / f"m{ordinal:03d}.lrat"
            cnf, selectors = producer.build_membership(member)
            producer.write_membership(cnf_path, ordinal, member, cnf, selectors, manifest)
            structural.check(cnf_path)
            expected = (producer.membership_key(member), f"{cell:03d}", f"{record[0]:03d}",
                        f"{parent:02d}", str(selectors[parent]))
            observed = tuple(row[name] for name in ("key", "cell", "source-child", "parent", "selector"))
            if observed != expected or identity(cnf_path) != (int(row["cnf-bytes"]), row["cnf-sha256"]):
                raise RuntimeError(f"membership {ordinal:03d} ancestry or regenerated CNF changed")
            artifact = ROOT / row["artifact"]
            if identity(artifact) != (int(row["xz-bytes"]), row["xz-sha256"]):
                raise RuntimeError(f"membership {ordinal:03d} compressed identity changed")
            with lzma.open(artifact, "rb") as source, lrat_path.open("wb") as target:
                while block := source.read(1 << 20):
                    target.write(block)
            if identity(lrat_path) != (int(row["lrat-bytes"]), row["lrat-sha256"]):
                raise RuntimeError(f"membership {ordinal:03d} raw LRAT identity changed")
            checked = subprocess.run([str(checker), str(cnf_path), str(lrat_path)],
                                     capture_output=True, text=True)
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError(f"membership {ordinal:03d} LRAT rejected")
            print(f"PASS {position:02d}/68 membership={ordinal:03d} xz={row['xz-bytes']}")
    print("PASS memberships=68 total_cnf_bytes=707414473 total_lrat_bytes=484924019 "
          "total_xz_bytes=32389520 limit_exclusive=250000000")


if __name__ == "__main__":
    main()
