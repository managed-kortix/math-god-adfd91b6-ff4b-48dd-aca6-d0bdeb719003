#!/usr/bin/env python3
"""Validate the completed B7-l2 stage, move its proofs, and emit strict ledgers."""

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re

import m6_b7_l2_parent_chunk_cover as producer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STEM = producer.PREFIX
ARTIFACT_DIRECTORY = ROOT / "certificates" / f"{STEM}-artifacts"
LEDGER = HERE / f"{STEM}-certificates.tsv"
PACKAGES = HERE / f"{STEM}-packages.tsv"
VERIFIER = HERE / "verify_m6_b7_l2_parent_chunk_certificates.py"
LIMIT = 90_000_000
LEAVES = 652
TOTAL_XZ = 4_409_362_076
BASE_COMMIT = "721249ac550ad173333643d4658e23325af56187"
COLUMNS = ("leaf", "key", "profile", "chunk", "start", "stop", "parents", "variables", "clauses",
           "cnf-bytes", "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes", "xz-sha256", "artifact")
BOUND_PATHS = {
    "manifest": HERE / f"{STEM}.tsv",
    "hash-ledger": HERE / f"{STEM}-hashes.tsv",
    "scout": HERE / f"{STEM}-scout-20s.json",
    "profile-producer": HERE / "m6_b7_l2_profile_root_cardinality.py",
    "producer": HERE / "m6_b7_l2_parent_chunk_cover.py",
    "checker": HERE / "check_m6_b7_l2_parent_chunk_cover.py",
    "scout-producer": HERE / "m6_b7_l2_parent_chunk_cover_scout.py",
    "finalizer": Path(__file__).resolve(),
    "closure-verifier": HERE / "verify_m6_b7_l2_parent_chunk_closure.py",
}


def identity(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            digest.update(block)
    return path.stat().st_size, digest.hexdigest()


def runtime_source_closure():
    local = {path.stem: path.resolve() for path in HERE.glob("*.py")}
    pending, visited = [VERIFIER.resolve()], set()
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
    visited.remove(VERIFIER.resolve())
    return tuple(sorted(visited))


def canonical_verifier_hash():
    data = VERIFIER.read_bytes()
    pattern = rb'LEDGER_CANONICAL_SHA256 = "[0-9a-f]{64}"'
    if len(re.findall(pattern, data)) != 1:
        raise RuntimeError("verifier self-pin marker changed")
    return hashlib.sha256(re.sub(pattern, b'LEDGER_CANONICAL_SHA256 = "' + b"0" * 64 + b'"', data)).hexdigest()


def package_hash(rows):
    payload = "".join("\t".join((row[0], row[13], row[14], row[15])) + "\n" for row in rows)
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def make_packages(rows):
    result, current, size = [], [], 0
    for row in rows:
        item = int(row[13])
        if item >= LIMIT:
            raise RuntimeError(f"leaf {row[0]} alone exceeds package cap")
        if current and size + item >= LIMIT:
            result.append(current)
            current, size = [], 0
        current.append(row)
        size += item
    if current:
        result.append(current)
    return result


def package_payload(packages):
    lines = [f"{STEM}-packages-v1", f"compressed-limit-bytes-exclusive\t{LIMIT}",
             f"packages\t{len(packages)}", f"leaves\t{LEAVES}",
             "artifact-set-hash-format\tsha256(leaf-tab-xz-bytes-tab-xz-sha256-tab-artifact-newline)",
             "columns\tpackage,leaf-range,leaves,xz-bytes,artifact-set-sha256"]
    for number, rows in enumerate(packages):
        total = sum(int(row[13]) for row in rows)
        lines.append(f"{number:02d}\t{rows[0][0]}-{rows[-1][0]}\t{len(rows)}\t{total}\t{package_hash(rows)}")
    return ("\n".join(lines) + "\n").encode("ascii")


def ledger_payload(rows, package_data):
    package_count = len(make_packages(rows))
    bindings = dict(BOUND_PATHS)
    bindings["package-ledger"] = PACKAGES
    lines = [f"{STEM}-certificates-v1", "generated-utc\t2026-09-02",
             "scope\tall-652-frozen-B7-l2-parent-chunk-leaves", f"base-commit\t{BASE_COMMIT}",
             "base-tree\t03f893673ca672c84c6341d48f1c922a23923d44", "profiles\t4", "parents\t8119",
             "profile-parent-incidences\t32476", "leaves\t652", "certified-leaves\t652",
             f"packages\t{package_count}", "cover\tdisjoint-and-exhaustive-within-each-profile",
             "scout-unsat\t652", "solver\tCaDiCaL 1.7.3",
             "solver-source-commit\t38e073b389a877b0a0d3c91136d2443ab95fdeba",
             "solver-binary-sha256\t108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292",
             "solver-command\tcadical --lrat --no-binary -q --restart=false --phase=false --seed=3 CNF LRAT",
             "checker\tlrat-check", "checker-source-commit\t2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
             "checker-binary-sha256\te9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8",
             "compression\txz -3", "compressor-binary\t/usr/bin/xz",
             "compressor-binary-sha256\tb5b163eb273291934556377ab883b4b2a5d4da50bd0dc0a91774ecc234ccd8d0",
             f"compressed-limit-bytes-exclusive\t{LIMIT}",
             f"total-cnf-bytes\t{sum(int(row[9]) for row in rows)}",
             f"total-lrat-bytes\t{sum(int(row[11]) for row in rows)}", f"total-xz-bytes\t{TOTAL_XZ}"]
    for name, path in bindings.items():
        item = identity(path)
        lines.extend((f"{name}-bytes\t{item[0]}", f"{name}-sha256\t{item[1]}"))
    for path in runtime_source_closure():
        name = f"runtime-{path.name[:-3].replace('_', '-')}"
        item = identity(path)
        lines.extend((f"{name}-bytes\t{item[0]}", f"{name}-sha256\t{item[1]}"))
    lines.append(f"verifier-canonical-sha256\t{canonical_verifier_hash()}")
    lines.append("columns\t" + ",".join(COLUMNS))
    lines.extend("\t".join(row) for row in rows)
    return ("\n".join(lines) + "\n").encode("ascii")


def load_stage(stage):
    leaves = producer.load_leaves()
    manifest = producer.manifest_payload(leaves)
    hashes = {}
    for line in (HERE / f"{STEM}-hashes.tsv").read_text(encoding="ascii").splitlines()[5:]:
        fields = line.split("\t")
        hashes[int(fields[0])] = (int(fields[5]), fields[6])
    rows = []
    for leaf in range(LEAVES):
        metadata_path = stage / f"leaf-{leaf:03d}.json"
        artifact = stage / "artifacts" / f"leaf-{leaf:03d}.lrat.xz"
        data = json.loads(metadata_path.read_text(encoding="ascii"))
        if set(data) != {"leaf", "cnf", "lrat", "xz"} or data["leaf"] != leaf or \
                tuple(data["cnf"]) != hashes[leaf] or tuple(data["xz"]) != identity(artifact):
            raise RuntimeError(f"stage identity mismatch at leaf {leaf:03d}")
        if any(not isinstance(data[name][0], int) or re.fullmatch(r"[0-9a-f]{64}", data[name][1]) is None
               for name in ("cnf", "lrat", "xz")):
            raise RuntimeError(f"malformed stage identity at leaf {leaf:03d}")
        description = leaves[leaf]
        cnf, _, _ = producer.build(description)
        artifact_path = f"certificates/{STEM}-artifacts/leaf-{leaf:03d}.lrat.xz"
        rows.append((f"{leaf:03d}", description[0], f"{description[1]:02d}", f"{description[3]:03d}",
                     f"{description[4]:04d}", f"{description[5]:04d}", str(len(description[-1])),
                     str(len(cnf.names)), str(len(cnf.clauses)), str(data["cnf"][0]), data["cnf"][1],
                     str(data["lrat"][0]), data["lrat"][1], str(data["xz"][0]), data["xz"][1], artifact_path))
    if len(list(stage.glob("leaf-*.json"))) != LEAVES or len(list((stage / "artifacts").glob("*.lrat.xz"))) != LEAVES or \
            sum(int(row[13]) for row in rows) != TOTAL_XZ:
        raise RuntimeError("stage set or exact compressed total changed")
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", type=Path, required=True)
    args = parser.parse_args()
    stage = args.stage.resolve(strict=True)
    if ARTIFACT_DIRECTORY.exists() or LEDGER.exists() or PACKAGES.exists():
        parser.error("certificate destination or ledger already exists")
    rows = load_stage(stage)
    packages = make_packages(rows)
    package_data = package_payload(packages)
    PACKAGES.write_bytes(package_data)
    LEDGER.write_bytes(ledger_payload(rows, package_data))
    data = LEDGER.read_bytes()
    prefix = b"verifier-canonical-sha256\t"
    canonical = hashlib.sha256(data.replace(prefix + canonical_verifier_hash().encode("ascii") + b"\n",
                                             prefix + b"0" * 64 + b"\n")).hexdigest()
    verifier_data = VERIFIER.read_bytes()
    verifier_data = re.sub(rb'LEDGER_CANONICAL_SHA256 = "[0-9a-f]{64}"',
                           b'LEDGER_CANONICAL_SHA256 = "' + canonical.encode("ascii") + b'"', verifier_data)
    VERIFIER.write_bytes(verifier_data)
    ARTIFACT_DIRECTORY.parent.mkdir(exist_ok=True)
    os.replace(stage / "artifacts", ARTIFACT_DIRECTORY)
    print(f"PASS leaves={LEAVES} packages={len(packages)} total_xz_bytes={TOTAL_XZ} ledger_canonical_sha256={canonical}")


if __name__ == "__main__":
    main()
