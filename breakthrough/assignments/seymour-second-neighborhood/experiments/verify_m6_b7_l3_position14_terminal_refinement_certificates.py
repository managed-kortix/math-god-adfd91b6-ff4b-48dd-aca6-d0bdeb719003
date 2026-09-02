#!/usr/bin/env python3
"""Strictly verify the frozen 60-certificate B7-l3 position-14 refinement."""

import argparse
import ast
import hashlib
import lzma
from pathlib import Path
import re
import subprocess
import tempfile

import check_m6_b7_l3_position14_terminal_refinement as structural
import m6_b7_l3_position14_terminal_refinement as producer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STEM = producer.PREFIX
LEDGER = HERE / f"{STEM}-certificates.tsv"
PACKAGES = HERE / f"{STEM}-packages.tsv"
FORMAT = f"{STEM}-certificates-v1"
LEDGER_CANONICAL_SHA256 = "2070e5624e5af6846219a442581dc171c64fcbfd4559e096814254abe8fe53cb"
SELF_TOKEN = b'LEDGER_CANONICAL_SHA256 = "' + b"0" * 64 + b'"'
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
LIMIT = 150_000_000
LEAVES = tuple(range(60))
TOTALS = {"cnf-bytes": 652486326, "lrat-bytes": 3598116209, "xz-bytes": 604092780}
COLUMNS = ("leaf", "key", "shard", "q", "chunk", "high-A", "parents", "variables", "clauses",
           "cnf-bytes", "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes", "xz-sha256",
           "solve-nanoseconds", "check-nanoseconds", "artifact")
BOUND_PATHS = {
    "manifest": HERE / f"{STEM}.tsv",
    "hash-ledger": HERE / f"{STEM}-hashes.tsv",
    "package-ledger": PACKAGES,
    "producer": HERE / "m6_b7_l3_position14_terminal_refinement.py",
    "checker": HERE / "check_m6_b7_l3_position14_terminal_refinement.py",
    "certificate-producer": HERE / "certify_m6_b7_l3_position14_terminal_refinement_60.py",
    "hostile-tests": HERE / "test_m6_b7_l3_position14_terminal_refinement.py",
    "certificate-hostile-tests": HERE / "test_m6_b7_l3_position14_terminal_refinement_certificates.py",
    "composition-verifier": HERE / "verify_m6_b7_l3_profile_root_cardinality_all19_closure.py",
    "eighteen-profile-ledger": HERE / "m6-b7-l3-profile-root-cardinality-except-position14-certificates.tsv",
    "eighteen-profile-packages": HERE / "m6-b7-l3-profile-root-cardinality-except-position14-packages.tsv",
    "eighteen-profile-verifier": HERE / "verify_m6_b7_l3_profile_root_cardinality_except_position14_certificates.py",
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
    payload = "".join("\t".join((row["leaf"], row["xz-bytes"], row["xz-sha256"],
                                  row["artifact"])) + "\n" for row in rows)
    return digest(payload.encode("ascii"))


def load_packages(rows, path=PACKAGES):
    data = path.read_bytes()
    lines = data.decode("ascii").splitlines()
    expected = [f"{STEM}-packages-v1", "compressed-limit-bytes-exclusive\t150000000",
                "packages\t5", "leaves\t60",
                "artifact-set-hash-format\tsha256(leaf-tab-xz-bytes-tab-xz-sha256-tab-artifact-newline)",
                "columns\tpackage,leaf-range,leaves,xz-bytes,artifact-set-sha256"]
    if data != ("\n".join(lines) + "\n").encode("ascii") or lines[:6] != expected or len(lines) != 11:
        raise RuntimeError("package ledger is not canonical")
    by_leaf = {int(row["leaf"]): row for row in rows}
    covered = []
    for package, line in enumerate(lines[6:]):
        fields = line.split("\t")
        if len(fields) != 5 or re.fullmatch(r"[0-9a-f]{64}", fields[4]) is None:
            raise RuntimeError("malformed package row")
        endpoints = fields[1].split("-")
        if len(endpoints) != 2 or any(not value.isdigit() for value in endpoints):
            raise RuntimeError("malformed package range")
        leaves = tuple(range(int(endpoints[0]), int(endpoints[1]) + 1))
        if any(leaf not in by_leaf for leaf in leaves):
            raise RuntimeError("package references unknown leaf")
        selected = [by_leaf[leaf] for leaf in leaves]
        size = sum(int(row["xz-bytes"]) for row in selected)
        expected_fields = [f"{package:02d}", f"{leaves[0]:02d}-{leaves[-1]:02d}", str(len(leaves)),
                           str(size), package_hash(selected)]
        if fields != expected_fields or size >= LIMIT:
            raise RuntimeError("package row differs")
        covered.extend(leaves)
    if tuple(covered) != LEAVES:
        raise RuntimeError("package cover differs")


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
            row = dict(zip(COLUMNS, fields))
            text = {"key", "shard", "cnf-sha256", "lrat-sha256", "xz-sha256", "artifact"}
            if any(not row[name].isdigit() for name in set(COLUMNS) - text) or any(
                    re.fullmatch(r"[0-9a-f]{64}", row[name]) is None
                    for name in ("cnf-sha256", "lrat-sha256", "xz-sha256")):
                raise RuntimeError("noncanonical certificate row")
            rows.append(row)
    required = {
        "generated-utc": "2026-09-02", "scope": "B7-l3-position14-terminal-refinement",
        "parent-profile-position": "14", "parent-profile-key": "p14", "parents": "1269",
        "parent-high-A-assignments": "5076", "leaves": "60", "packages": "5",
        "cover": "disjoint-and-exhaustive", "solver": "CaDiCaL 1.7.3",
        "solver-source-commit": "38e073b389a877b0a0d3c91136d2443ab95fdeba",
        "solver-binary-sha256": "108d1042b38ceae5cb71e4a806870c4f4d8ffdb48a124f2e1fb7b23d3a8292",
        "solver-command": "cadical --lrat --no-binary -q --restart=false --phase=false --seed=3 CNF LRAT",
        "checker": "lrat-check", "checker-source-commit": "2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
        "checker-binary-sha256": CHECKER_SHA256, "compression": "xz -3", "compressor-binary": "/usr/bin/xz",
        "compressor-binary-sha256": "b5b163eb273291934556377ab883b4b2a5d4da50bd0dc0a91774ecc234ccd8d0",
        "compressed-limit-bytes-exclusive": str(LIMIT), "total-cnf-bytes": str(TOTALS["cnf-bytes"]),
        "total-lrat-bytes": str(TOTALS["lrat-bytes"]), "total-xz-bytes": str(TOTALS["xz-bytes"]),
    }
    runtime_keys = {f"runtime-{path.name[:-3].replace('_', '-')}-{suffix}"
                    for path in runtime_source_closure() for suffix in ("bytes", "sha256")}
    expected_keys = set(required) | {"verifier-canonical-sha256"} | runtime_keys | {
        f"{name}-{suffix}" for name in BOUND_PATHS for suffix in ("bytes", "sha256")}
    if columns is None or len(rows) != 60 or set(metadata) != expected_keys or any(
            metadata.get(name) != value for name, value in required.items()):
        raise RuntimeError("certificate metadata or exact scope changed")
    expected_order = tuple((f"{leaf:02d}", producer.load_leaves()[leaf][0]) for leaf in LEAVES)
    if tuple((row["leaf"], row["key"]) for row in rows) != expected_order or any(
            sum(int(row[name]) for row in rows) != total for name, total in TOTALS.items()):
        raise RuntimeError("certificate order or totals changed")
    load_packages(rows)
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
    if checker is not None and (not checker.is_absolute() or identity(checker.resolve(strict=True))[1] != CHECKER_SHA256):
        raise RuntimeError("checker path or identity changed")


def artifact_paths(rows):
    expected = {row["artifact"] for row in rows}
    actual = {path.relative_to(ROOT).as_posix() for path in (ROOT / "certificates").glob(f"{STEM}-leaf-*.lrat.xz")}
    if len(expected) != 60 or actual != expected:
        raise RuntimeError("artifact set differs from exact 60-leaf ledger")


def verify_payloads(rows, checker=None, selected=None):
    leaves = producer.load_leaves()
    manifest = producer.manifest_payload(leaves)
    chosen = set(LEAVES if selected is None else selected)
    if not chosen <= set(LEAVES):
        raise RuntimeError("selected leaf outside exact scope")
    with tempfile.TemporaryDirectory(prefix="b7-l3-p14-cert-verify-", dir=ROOT) as directory:
        work = Path(directory)
        for leaf in sorted(chosen):
            row, description = rows[leaf], leaves[leaf]
            built = producer.build(description)
            cnf = built[0]
            expected = {"key": description[0], "shard": description[2], "q": str(description[3]),
                        "chunk": str(description[5]), "high-A": str(description[6]),
                        "parents": str(len(description[-1])), "variables": str(len(cnf.names)),
                        "clauses": str(len(cnf.clauses))}
            if any(row[name] != value for name, value in expected.items()):
                raise RuntimeError("ledger row does not describe regenerated leaf")
            cnf_path = work / f"leaf-{leaf:02d}.cnf"
            lrat_path = work / f"leaf-{leaf:02d}.lrat"
            producer.write_cnf(cnf_path, leaf, description, *built, manifest)
            structural.check(cnf_path)
            if identity(cnf_path) != (int(row["cnf-bytes"]), row["cnf-sha256"]):
                raise RuntimeError("regenerated CNF changed")
            artifact = ROOT / row["artifact"]
            if identity(artifact) != (int(row["xz-bytes"]), row["xz-sha256"]):
                raise RuntimeError("compressed artifact identity changed")
            if checker is None:
                raw_id = decompress_identity(artifact, int(row["lrat-bytes"]))
            else:
                with lrat_path.open("wb") as target:
                    raw_id = decompress_identity(artifact, int(row["lrat-bytes"]), target)
            if raw_id != (int(row["lrat-bytes"]), row["lrat-sha256"]):
                raise RuntimeError("raw LRAT changed")
            if checker is not None:
                checked = subprocess.run([str(checker), str(cnf_path), str(lrat_path)], capture_output=True, text=True)
                if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                    raise RuntimeError("LRAT rejected")
            print(f"PASS {leaf + 1:02d}/60 leaf={leaf:02d}")


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
    if not args.no_replay and checker is None:
        parser.error("fresh replay requires --checker")
    selected = (0, 14, 29, 44, 59) if args.representative else None
    verify_payloads(rows, None if args.no_replay else checker, selected)
    print(f"PASS leaves=60 parents=1269 packages=5 total_xz_bytes={TOTALS['xz-bytes']}")


if __name__ == "__main__":
    main()
