#!/usr/bin/env python3
"""Strict identity verification and selected fresh replay of 652 B7-l2 LRATs."""

import argparse
import ast
import hashlib
import json
import lzma
from pathlib import Path
import re
import subprocess
import tempfile

import check_m6_b7_l2_parent_chunk_cover as structural
import m6_b7_l2_parent_chunk_cover as producer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STEM = producer.PREFIX
LEDGER = HERE / f"{STEM}-certificates.tsv"
PACKAGES = HERE / f"{STEM}-packages.tsv"
FORMAT = f"{STEM}-certificates-v1"
LEDGER_CANONICAL_SHA256 = "9539163a66b783452983e2d9e3f34c8720a456d96da23457d25f07c20aa6459c"
SELF_TOKEN = b'LEDGER_CANONICAL_SHA256 = "' + b"0" * 64 + b'"'
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
LIMIT = 90_000_000
LEAVES = tuple(range(652))
TOTAL_XZ = 4_409_362_076
COLUMNS = ("leaf", "key", "profile", "chunk", "start", "stop", "parents", "variables", "clauses",
           "cnf-bytes", "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes", "xz-sha256", "artifact")
BOUND_PATHS = {
    "manifest": HERE / f"{STEM}.tsv", "hash-ledger": HERE / f"{STEM}-hashes.tsv",
    "scout": HERE / f"{STEM}-scout-20s.json", "package-ledger": PACKAGES,
    "profile-producer": HERE / "m6_b7_l2_profile_root_cardinality.py",
    "producer": HERE / "m6_b7_l2_parent_chunk_cover.py",
    "checker": HERE / "check_m6_b7_l2_parent_chunk_cover.py",
    "scout-producer": HERE / "m6_b7_l2_parent_chunk_cover_scout.py",
    "finalizer": HERE / "finalize_m6_b7_l2_parent_chunk_certificates.py",
    "closure-verifier": HERE / "verify_m6_b7_l2_parent_chunk_closure.py",
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            value.update(block)
    return path.stat().st_size, value.hexdigest()


def decompress_identity(path, expected_bytes, output=None):
    value, size = hashlib.sha256(), 0
    with lzma.open(path, "rb") as source:
        while block := source.read(1 << 20):
            size += len(block)
            if size > expected_bytes:
                raise RuntimeError("decompressed LRAT exceeds ledger size")
            value.update(block)
            if output is not None:
                output.write(block)
    return size, value.hexdigest()


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


def package_hash(rows):
    payload = "".join("\t".join((row["leaf"], row["xz-bytes"], row["xz-sha256"], row["artifact"])) + "\n"
                      for row in rows)
    return digest(payload.encode("ascii"))


def load_packages(rows):
    data = PACKAGES.read_bytes()
    lines = data.decode("ascii").splitlines()
    prefix = [f"{STEM}-packages-v1", f"compressed-limit-bytes-exclusive\t{LIMIT}"]
    if data != ("\n".join(lines) + "\n").encode("ascii") or lines[:2] != prefix or len(lines) < 7:
        raise RuntimeError("package ledger is not canonical")
    package_count = int(lines[2].split("\t")[1])
    if lines[3:6] != ["leaves\t652",
            "artifact-set-hash-format\tsha256(leaf-tab-xz-bytes-tab-xz-sha256-tab-artifact-newline)",
            "columns\tpackage,leaf-range,leaves,xz-bytes,artifact-set-sha256"] or len(lines) != 6 + package_count:
        raise RuntimeError("package ledger header changed")
    by_leaf, covered = {int(row["leaf"]): row for row in rows}, []
    for number, line in enumerate(lines[6:]):
        fields = line.split("\t")
        endpoints = fields[1].split("-") if len(fields) == 5 else []
        if len(endpoints) != 2 or any(not item.isdigit() for item in endpoints):
            raise RuntimeError("malformed package range")
        selected = [by_leaf[leaf] for leaf in range(int(endpoints[0]), int(endpoints[1]) + 1)]
        size = sum(int(row["xz-bytes"]) for row in selected)
        expected = [f"{number:02d}", f"{selected[0]['leaf']}-{selected[-1]['leaf']}", str(len(selected)),
                    str(size), package_hash(selected)]
        if fields != expected or size >= LIMIT:
            raise RuntimeError("package identity or exclusive cap changed")
        covered.extend(int(row["leaf"]) for row in selected)
    if tuple(covered) != LEAVES:
        raise RuntimeError("packages do not exactly cover all leaves")
    return package_count


def load_ledger():
    data = LEDGER.read_bytes()
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
            row = dict(zip(COLUMNS, fields))
            text = {"key", "cnf-sha256", "lrat-sha256", "xz-sha256", "artifact"}
            if any(not row[name].isdigit() for name in set(COLUMNS) - text) or any(
                    re.fullmatch(r"[0-9a-f]{64}", row[name]) is None
                    for name in ("cnf-sha256", "lrat-sha256", "xz-sha256")):
                raise RuntimeError("noncanonical certificate row")
            rows.append(row)
    required = {"generated-utc": "2026-09-02", "scope": "all-652-frozen-B7-l2-parent-chunk-leaves",
                "base-commit": "721249ac550ad173333643d4658e23325af56187",
                "base-tree": "03f893673ca672c84c6341d48f1c922a23923d44", "profiles": "4", "parents": "8119",
                "profile-parent-incidences": "32476", "leaves": "652", "certified-leaves": "652",
                "cover": "disjoint-and-exhaustive-within-each-profile", "scout-unsat": "652",
                "checker-binary-sha256": CHECKER_SHA256, "compressed-limit-bytes-exclusive": str(LIMIT),
                "total-xz-bytes": str(TOTAL_XZ)}
    runtime_keys = {f"runtime-{path.name[:-3].replace('_', '-')}-{suffix}"
                    for path in runtime_source_closure() for suffix in ("bytes", "sha256")}
    expected_keys = set(required) | runtime_keys | {"packages", "solver", "solver-source-commit",
        "solver-binary-sha256", "solver-command", "checker", "checker-source-commit", "compression",
        "compressor-binary", "compressor-binary-sha256", "total-cnf-bytes", "total-lrat-bytes",
        "verifier-canonical-sha256"} | {f"{name}-{suffix}" for name in BOUND_PATHS for suffix in ("bytes", "sha256")}
    if columns is None or len(rows) != 652 or set(metadata) != expected_keys or any(
            metadata.get(name) != value for name, value in required.items()):
        raise RuntimeError("certificate metadata or exact scope changed")
    if tuple(int(row["leaf"]) for row in rows) != LEAVES or sum(int(row["xz-bytes"]) for row in rows) != TOTAL_XZ:
        raise RuntimeError("certificate order or total changed")
    if int(metadata["packages"]) != load_packages(rows):
        raise RuntimeError("package count changed")
    return metadata, rows


def verify_bindings(metadata, checker=None):
    if canonical_ledger_hash() != LEDGER_CANONICAL_SHA256:
        raise RuntimeError("verifier does not pin canonical ledger")
    if metadata["verifier-canonical-sha256"] != canonical_verifier_hash():
        raise RuntimeError("ledger does not pin canonical verifier")
    for name, path in BOUND_PATHS.items():
        if identity(path) != (int(metadata[f"{name}-bytes"]), metadata[f"{name}-sha256"]):
            raise RuntimeError(f"bound input changed: {name}")
    for path in runtime_source_closure():
        name = f"runtime-{path.name[:-3].replace('_', '-')}"
        if identity(path) != (int(metadata[f"{name}-bytes"]), metadata[f"{name}-sha256"]):
            raise RuntimeError(f"bound transitive runtime changed: {path.name}")
    scout = json.loads(BOUND_PATHS["scout"].read_text(encoding="ascii"))
    if scout.get("leaves") != 652 or scout.get("unsat") != 652 or scout.get("sat") or scout.get("timeout"):
        raise RuntimeError("frozen scout result changed")
    if checker is not None and (not checker.is_absolute() or identity(checker.resolve(strict=True))[1] != CHECKER_SHA256):
        raise RuntimeError("checker path or identity changed")


def artifact_paths(rows):
    expected = {row["artifact"] for row in rows}
    directory = ROOT / "certificates" / f"{STEM}-artifacts"
    actual = {path.relative_to(ROOT).as_posix() for path in directory.glob("*.lrat.xz")}
    if len(expected) != 652 or actual != expected:
        raise RuntimeError("artifact set differs from exact ledger")


def verify_identities(rows):
    for count, row in enumerate(rows, 1):
        artifact = ROOT / row["artifact"]
        if identity(artifact) != (int(row["xz-bytes"]), row["xz-sha256"]):
            raise RuntimeError(f"compressed identity changed at leaf {row['leaf']}")
        if decompress_identity(artifact, int(row["lrat-bytes"])) != (int(row["lrat-bytes"]), row["lrat-sha256"]):
            raise RuntimeError(f"raw LRAT identity changed at leaf {row['leaf']}")
        if count % 25 == 0 or count == 652:
            print(f"PASS identities={count:03d}/652", flush=True)


def replay(rows, checker, selected):
    leaves = producer.load_leaves()
    manifest = producer.manifest_payload(leaves)
    with tempfile.TemporaryDirectory(prefix="b7-l2-certificate-replay-", dir=ROOT) as directory:
        work = Path(directory)
        for leaf in selected:
            row, description = rows[leaf], leaves[leaf]
            built = producer.build(description)
            cnf = built[0]
            expected = {"key": description[0], "profile": f"{description[1]:02d}",
                        "chunk": f"{description[3]:03d}", "start": f"{description[4]:04d}",
                        "stop": f"{description[5]:04d}", "parents": str(len(description[-1])),
                        "variables": str(len(cnf.names)), "clauses": str(len(cnf.clauses))}
            if any(row[name] != value for name, value in expected.items()):
                raise RuntimeError("ledger row does not describe regenerated leaf")
            cnf_path, lrat_path = work / f"leaf-{leaf:03d}.cnf", work / f"leaf-{leaf:03d}.lrat"
            producer.write_cnf(cnf_path, leaf, description, *built, manifest)
            structural.check(cnf_path)
            if identity(cnf_path) != (int(row["cnf-bytes"]), row["cnf-sha256"]):
                raise RuntimeError("regenerated CNF changed")
            with lrat_path.open("wb") as target:
                raw = decompress_identity(ROOT / row["artifact"], int(row["lrat-bytes"]), target)
            if raw != (int(row["lrat-bytes"]), row["lrat-sha256"]):
                raise RuntimeError("raw LRAT changed")
            checked = subprocess.run([str(checker), str(cnf_path), str(lrat_path)], capture_output=True, text=True)
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError(f"LRAT rejected at leaf {leaf:03d}")
            print(f"PASS replay leaf={leaf:03d} profile={description[1]:02d}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path)
    parser.add_argument("--no-replay", action="store_true")
    parser.add_argument("--representative", action="store_true")
    args = parser.parse_args()
    metadata, rows = load_ledger()
    checker = args.checker.resolve(strict=True) if args.checker else None
    verify_bindings(metadata, checker)
    artifact_paths(rows)
    verify_identities(rows)
    if not args.no_replay:
        if checker is None:
            parser.error("replay requires --checker")
        selected = (0, 162, 163, 325, 326, 488, 489, 651) if args.representative else LEAVES
        replay(rows, checker, selected)
    print(f"PASS leaves=652 profiles=4 parents=8119 packages={metadata['packages']} total_xz_bytes={TOTAL_XZ} limit_exclusive={LIMIT}")


if __name__ == "__main__":
    main()
