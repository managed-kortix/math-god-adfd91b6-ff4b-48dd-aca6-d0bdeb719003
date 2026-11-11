#!/usr/bin/env python3
"""Strict fresh replay of all 28 exact Hall |K| LRAT certificates."""

import argparse
import hashlib
import lzma
from pathlib import Path
import re
import subprocess
import tempfile

import check_m6_b7_l6_exact_pair_timeout_hall_failure_cardinality_split as structural
import m6_b7_l6_exact_pair_timeout_hall_failure_cardinality_split as producer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGER = HERE / f"{producer.PREFIX}-certificates.tsv"
FORMAT = f"{producer.PREFIX}-certificates-v1"
LEDGER_CANONICAL_SHA256 = "28e00f90e24b84b2034c452f28c4a7673fb8852a8ff6979ca419b38d7d46bb5e"
SELF_TOKEN = b'LEDGER_CANONICAL_SHA256 = "' + b"0" * 64 + b'"'
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
LIMIT = 250_000_000
TOTALS = {"cnf-bytes": 291619772, "lrat-bytes": 229856177, "xz-bytes": 17456956}
COLUMNS = ("child", "parent-position", "membership", "key", "cardinality", "variables",
           "clauses", "cnf-bytes", "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes",
           "xz-sha256", "solve-nanoseconds", "check-nanoseconds", "artifact")
BOUND_PATHS = {
    "hall-producer": HERE / "m6_b7_l6_exact_pair_timeout_hall_failure.py",
    "hall-checker": HERE / "check_m6_b7_l6_exact_pair_timeout_hall_failure.py",
    "split-manifest": structural.MANIFEST,
    "split-hash-ledger": structural.HASHES,
    "split-producer": HERE / "m6_b7_l6_exact_pair_timeout_hall_failure_cardinality_split.py",
    "split-checker": HERE / "check_m6_b7_l6_exact_pair_timeout_hall_failure_cardinality_split.py",
    "certificate-producer": HERE / "certify_m6_b7_l6_exact_pair_timeout_hall_failure_cardinality_split.py",
    "scout-producer": HERE / "m6_b7_l6_exact_pair_timeout_hall_failure_cardinality_split_scout.py",
    "scout-ledger": HERE / f"{producer.PREFIX}-scout.json",
    "parent-certificate-ledger": HERE / f"{producer.hall.PREFIX}-scout-unsat-certificates.tsv",
    "parent-certificate-verifier": HERE / f"verify_{producer.hall.PREFIX.replace('-', '_')}_scout_unsat_certificates.py",
    "hostile-tests": HERE / "test_m6_b7_l6_exact_pair_timeout_hall_failure_cardinality_split.py",
}


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
    return hashlib.sha256(data.replace(marker, SELF_TOKEN)).hexdigest()


def canonical_ledger_hash(path=LEDGER):
    lines = path.read_bytes().splitlines(keepends=True)
    prefix = b"verifier-canonical-sha256\t"
    matches = [index for index, line in enumerate(lines) if line.startswith(prefix)]
    if len(matches) != 1:
        raise RuntimeError("ledger verifier pin row changed")
    lines[matches[0]] = prefix + b"0" * 64 + b"\n"
    return hashlib.sha256(b"".join(lines)).hexdigest()


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
    required = {"generated-utc": "2026-08-28", "base-commit": "4846699519960909a03a2af922a578fbd5fe951a",
                "scope": "Frozen-Seymour-Hall-TIMEOUT-memberships-028,054,069,070-exact-|K|-1..7",
                "parents": "4", "children": "28", "partition": "disjoint-and-exhaustive-over-nonempty-K",
                "solver": "CaDiCaL 1.7.3", "solver-source-commit": "38e073b389a877b0a0d3c91136d2443ab95fdeba",
                "solver-binary-sha256": "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292",
                "solver-command": "cadical --lrat --no-binary -q --restart=false --phase=false --seed=3 CNF LRAT",
                "solver-required-exit": "20", "checker": "lrat-check",
                "checker-source-commit": "2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
                "checker-binary-sha256": CHECKER_SHA256, "checker-required-output": "c VERIFIED",
                "compression": "xz -3", "compressed-limit-bytes-exclusive": str(LIMIT),
                "total-cnf-bytes": str(TOTALS["cnf-bytes"]),
                "total-lrat-bytes": str(TOTALS["lrat-bytes"]),
                "total-xz-bytes": str(TOTALS["xz-bytes"]),
                "direct-cadical-default-300s": "TIMEOUT,TIMEOUT,TIMEOUT,TIMEOUT"}
    expected = set(required) | {"verifier-canonical-sha256"} | \
        {f"{name}-{suffix}" for name in BOUND_PATHS for suffix in ("bytes", "sha256")}
    if columns is None or len(rows) != 28 or set(metadata) != expected or any(
            metadata.get(name) != value for name, value in required.items()):
        raise RuntimeError("certificate metadata or exact scope changed")
    scope = producer.children()
    observed = tuple((int(row["child"]), int(row["parent-position"]), int(row["membership"]),
                      row["key"], int(row["cardinality"]), int(row["variables"]),
                      int(row["clauses"]), row["artifact"]) for row in rows)
    expected_rows = tuple(
        (i, child[0], child[1][0]["membership"],
         producer.hall.singleton.membership_key(child[1][1]), child[2],
         *producer.dimensions(child),
         f"certificates/{producer.PREFIX}-child-{i:03d}-membership-"
         f"{child[1][0]['membership']:03d}-k{child[2]}.lrat.xz")
        for i, child in enumerate(scope))
    if observed != expected_rows or any(sum(int(row[name]) for row in rows) != value
                                       for name, value in TOTALS.items()) or TOTALS["xz-bytes"] >= LIMIT:
        raise RuntimeError("certificate order, totals, or cap changed")
    return metadata, rows


def verify_bindings(metadata, checker):
    if canonical_ledger_hash() != LEDGER_CANONICAL_SHA256:
        raise RuntimeError("verifier does not pin canonical ledger")
    if metadata["verifier-canonical-sha256"] != canonical_verifier_hash(Path(__file__)):
        raise RuntimeError("ledger does not pin canonical verifier")
    if not checker.is_absolute() or checker != checker.resolve(strict=True) or \
            identity(checker)[1] != CHECKER_SHA256:
        raise RuntimeError("checker is not explicit pinned lrat-check")
    for name, path in BOUND_PATHS.items():
        if identity(path) != (int(metadata[f"{name}-bytes"]), metadata[f"{name}-sha256"]):
            raise RuntimeError(f"bound artifact changed: {name}")


def artifact_paths(rows):
    expected = {row["artifact"] for row in rows}
    if len(expected) != 28 or any(not path.startswith(f"certificates/{producer.PREFIX}-child-")
                                  for path in expected):
        raise RuntimeError("artifact names are not exact and unique")
    actual = {path.relative_to(ROOT).as_posix() for path in (ROOT / "certificates").glob(
        f"{producer.PREFIX}-child-*.lrat.xz")}
    if actual != expected:
        raise RuntimeError("artifact set differs from ledger")


def verify_artifact_identities(rows, root=ROOT):
    for row in rows:
        artifact = root / row["artifact"]
        if identity(artifact) != (int(row["xz-bytes"]), row["xz-sha256"]):
            raise RuntimeError(f"compressed proof changed: child {int(row['child']):03d}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path, required=True)
    args = parser.parse_args()
    metadata, rows = load_ledger()
    checker = args.checker.resolve(strict=True)
    verify_bindings(metadata, checker)
    artifact_paths(rows)
    verify_artifact_identities(rows)
    structural.check_cover()
    scope = producer.children()
    manifest = producer.manifest_payload(scope)
    with tempfile.TemporaryDirectory(prefix="hall-cardinality-replay-", dir=ROOT) as directory:
        work = Path(directory)
        for count, row in enumerate(rows, 1):
            child_position = int(row["child"])
            child = scope[child_position]
            cnf_path, lrat_path = work / f"c{child_position:03d}.cnf", work / f"c{child_position:03d}.lrat"
            built = producer.build_child(child)
            producer.write_child(cnf_path, child_position, child, *built, manifest)
            structural.check(cnf_path)
            if identity(cnf_path) != (int(row["cnf-bytes"]), row["cnf-sha256"]):
                raise RuntimeError(f"child {child_position:03d} regenerated CNF changed")
            artifact = ROOT / row["artifact"]
            if identity(artifact) != (int(row["xz-bytes"]), row["xz-sha256"]):
                raise RuntimeError(f"child {child_position:03d} compressed proof changed")
            with lzma.open(artifact, "rb") as source, lrat_path.open("wb") as target:
                while block := source.read(1 << 20):
                    target.write(block)
            if identity(lrat_path) != (int(row["lrat-bytes"]), row["lrat-sha256"]):
                raise RuntimeError(f"child {child_position:03d} raw proof changed")
            checked = subprocess.run([str(checker), str(cnf_path), str(lrat_path)],
                                     capture_output=True, text=True)
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError(f"child {child_position:03d} LRAT rejected")
            print(f"PASS {count:02d}/28 membership={row['membership']} k={row['cardinality']}")
    print("PASS children=28 total_cnf_bytes=291619772 total_lrat_bytes=229856177 "
          "total_xz_bytes=17456956 limit_exclusive=250000000")


if __name__ == "__main__":
    main()
