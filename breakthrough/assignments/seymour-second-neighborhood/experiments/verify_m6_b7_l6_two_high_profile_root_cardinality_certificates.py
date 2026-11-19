#!/usr/bin/env python3
"""Strict ledger verification and fresh replay of the 19 two-high LRATs."""

import argparse
import ast
import hashlib
import json
import lzma
from pathlib import Path
import re
import subprocess
import tempfile

import check_m6_b7_l6_two_high_profile_root_cardinality as structural
import m6_b7_l6_two_high_profile_root_cardinality as producer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGER = HERE / f"{producer.PREFIX}-certificates.tsv"
FORMAT = f"{producer.PREFIX}-certificates-v1"
LEDGER_CANONICAL_SHA256 = "ad5ac9905db55e69976e8cff95c68016b725299cd11e3c23c76969fc43a7f274"
SELF_TOKEN = b'LEDGER_CANONICAL_SHA256 = "' + b"0" * 64 + b'"'
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
LIMIT = 250_000_000
TOTALS = {"cnf-bytes": 202970329, "lrat-bytes": 217996726, "xz-bytes": 20979196}
COLUMNS = ("position", "orbit", "key", "state-key", "t", "parents", "variables", "clauses",
           "cnf-bytes", "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes", "xz-sha256",
           "solve-nanoseconds", "check-nanoseconds", "artifact")
BOUND_PATHS = {
    "manifest": HERE / f"{producer.PREFIX}.tsv",
    "hash-ledger": HERE / f"{producer.PREFIX}-hashes.tsv",
    "scout": HERE / f"{producer.PREFIX}-scout-30s.json",
    "producer": HERE / "m6_b7_l6_two_high_profile_root_cardinality.py",
    "checker": HERE / "check_m6_b7_l6_two_high_profile_root_cardinality.py",
    "scout-producer": HERE / "m6_b7_l6_two_high_profile_root_cardinality_scout.py",
    "certificate-producer": HERE / "certify_m6_b7_l6_two_high_profile_root_cardinality.py",
    "hostile-tests": HERE / "test_m6_b7_l6_two_high_profile_root_cardinality.py",
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            value.update(block)
    return path.stat().st_size, value.hexdigest()


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
            numeric = set(COLUMNS) - {"key", "state-key", "cnf-sha256", "lrat-sha256", "xz-sha256", "artifact"}
            if any(not row[name].isdigit() for name in numeric) or any(
                    re.fullmatch(r"[0-9a-f]{64}", row[name]) is None
                    for name in ("cnf-sha256", "lrat-sha256", "xz-sha256")):
                raise RuntimeError("noncanonical certificate row")
            rows.append(row)
    required = {"generated-utc": "2026-09-01", "scope": "exact-19-two-high-early-C-profile-root-cardinality",
                "scope-orbits": ",".join(f"{i:02d}" for i in producer.SCOPE), "profiles": "19",
                "scout-unsat": "19", "certified-profiles": "19", "solver": "CaDiCaL 1.7.3",
                "solver-binary-sha256": "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292",
                "solver-command": "cadical --lrat --no-binary -q --restart=false --phase=false --seed=3 CNF LRAT",
                "checker": "lrat-check", "checker-binary-sha256": CHECKER_SHA256,
                "compression": "xz -3", "compressor-binary": "/usr/bin/xz",
                "compressor-binary-sha256": "b5b163eb273291934556377ab883b4b2a5d4da50bd0dc0a91774ecc234ccd8d0",
                "compressed-limit-bytes-exclusive": str(LIMIT),
                "total-cnf-bytes": str(TOTALS["cnf-bytes"]),
                "total-lrat-bytes": str(TOTALS["lrat-bytes"]),
                "total-xz-bytes": str(TOTALS["xz-bytes"])}
    runtime_keys = {f"runtime-{path.name[:-3].replace('_', '-')}-{suffix}"
                    for path in runtime_source_closure() for suffix in ("bytes", "sha256")}
    expected = set(required) | {"verifier-canonical-sha256"} | runtime_keys | \
        {f"{name}-{suffix}" for name in BOUND_PATHS for suffix in ("bytes", "sha256")}
    if columns is None or len(rows) != 19 or set(metadata) != expected or any(
            metadata.get(name) != value for name, value in required.items()):
        raise RuntimeError("certificate metadata or exact scope changed")
    observed = tuple((int(row["position"]), int(row["orbit"])) for row in rows)
    wanted = tuple(enumerate(producer.SCOPE))
    if observed != wanted or any(sum(int(row[key]) for row in rows) != value for key, value in TOTALS.items()) or \
            TOTALS["xz-bytes"] >= LIMIT:
        raise RuntimeError("certificate order, totals, or exclusive cap changed")
    return metadata, rows


def verify_bindings(metadata, checker=None):
    if canonical_ledger_hash() != LEDGER_CANONICAL_SHA256:
        raise RuntimeError("verifier does not pin canonical ledger")
    if metadata["verifier-canonical-sha256"] != canonical_verifier_hash():
        raise RuntimeError("ledger does not pin canonical verifier")
    for name, path in BOUND_PATHS.items():
        if identity(path) != (int(metadata[f"{name}-bytes"]), metadata[f"{name}-sha256"]):
            raise RuntimeError(f"bound artifact changed: {name}")
    for path in runtime_source_closure():
        name = f"runtime-{path.name[:-3].replace('_', '-')}"
        if identity(path) != (int(metadata[f"{name}-bytes"]), metadata[f"{name}-sha256"]):
            raise RuntimeError(f"bound transitive runtime changed: {path.name}")
    scout = json.loads(BOUND_PATHS["scout"].read_text(encoding="ascii"))
    if scout.get("profiles") != 19 or scout.get("unsat") != 19 or scout.get("sat") or scout.get("timeout"):
        raise RuntimeError("scout exact result changed")
    if checker is not None and (not checker.is_absolute() or identity(checker.resolve(strict=True))[1] != CHECKER_SHA256):
        raise RuntimeError("checker path or identity changed")


def artifact_paths(rows):
    expected = {row["artifact"] for row in rows}
    actual = {path.relative_to(ROOT).as_posix() for path in (ROOT / "certificates").glob(
        f"{producer.PREFIX}-orbit-*.lrat.xz")}
    if len(expected) != 19 or actual != expected:
        raise RuntimeError("artifact set differs from ledger")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path)
    parser.add_argument("--no-replay", action="store_true")
    args = parser.parse_args()
    metadata, rows = load_ledger()
    checker = args.checker.resolve(strict=True) if args.checker else None
    verify_bindings(metadata, checker)
    artifact_paths(rows)
    for row in rows:
        artifact = ROOT / row["artifact"]
        if identity(artifact) != (int(row["xz-bytes"]), row["xz-sha256"]):
            raise RuntimeError("compressed artifact identity changed")
    if not args.no_replay:
        if checker is None:
            parser.error("fresh replay requires --checker")
        orbits = producer.scope()
        manifest = producer.manifest_payload(orbits)
        with tempfile.TemporaryDirectory(prefix="two-high-root-replay-", dir=ROOT) as directory:
            work = Path(directory)
            for count, row in enumerate(rows, 1):
                position, ordinal = int(row["position"]), int(row["orbit"])
                cnf_path, lrat_path = work / f"o{ordinal:02d}.cnf", work / f"o{ordinal:02d}.lrat"
                producer.write_cnf(cnf_path, position, ordinal, orbits[ordinal],
                                   *producer.build(ordinal, orbits), manifest)
                structural.check(cnf_path)
                if identity(cnf_path) != (int(row["cnf-bytes"]), row["cnf-sha256"]):
                    raise RuntimeError("regenerated CNF changed")
                with lzma.open(ROOT / row["artifact"], "rb") as source, lrat_path.open("wb") as target:
                    while block := source.read(1 << 20):
                        target.write(block)
                if identity(lrat_path) != (int(row["lrat-bytes"]), row["lrat-sha256"]):
                    raise RuntimeError("raw LRAT changed")
                checked = subprocess.run([str(checker), str(cnf_path), str(lrat_path)], capture_output=True, text=True)
                if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                    raise RuntimeError("LRAT rejected")
                print(f"PASS {count:02d}/19 orbit={ordinal:02d}")
    print(f"PASS profiles=19 total_xz_bytes={TOTALS['xz-bytes']} limit_exclusive={LIMIT}")


if __name__ == "__main__":
    main()
