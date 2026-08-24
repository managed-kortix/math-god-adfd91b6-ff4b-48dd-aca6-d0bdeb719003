#!/usr/bin/env python3
"""Fresh replay of exactly 172 frozen inaccessible-pair scout-UNSAT LRATs."""

import argparse
import ast
import hashlib
import json
import lzma
from pathlib import Path
import re
import subprocess
import tempfile

import check_m6_b7_l6_early_c_inaccessible_pair_orbits as structural
import m6_b7_l6_early_c_inaccessible_pair_orbits as producer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGER = HERE / "m6-b7-l6-early-c-inaccessible-pair-scout-unsat-certificates.tsv"
FORMAT = "m6-b7-l6-early-c-inaccessible-pair-scout-unsat-certificates-v1"
LEDGER_CANONICAL_SHA256 = "4f2b65a51f1b46d25d54af5af43e382e069b2c529fd96b7987b035dabfb90253"
SELF_TOKEN = b'LEDGER_CANONICAL_SHA256 = "' + b"0" * 64 + b'"'
CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
LIMIT = 250_000_000
COLUMNS = (
    "child", "key", "profile", "parents", "variables", "clauses", "cnf-bytes",
    "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes", "xz-sha256",
    "solve-nanoseconds", "check-nanoseconds", "artifact",
)
BOUND_PATHS = {
    "cover-manifest": HERE / "m6-b7-l6-early-c-inaccessible-pair-orbits.tsv",
    "cover-hash-ledger": HERE / "m6-b7-l6-early-c-inaccessible-pair-hashes.tsv",
    "cover-scout": HERE / "m6-b7-l6-early-c-inaccessible-pair-scout-1s.json",
    "certificate-producer": HERE / "certify_m6_b7_l6_early_c_inaccessible_pair_scout_unsat.py",
    "hostile-tests": HERE / "test_m6_b7_l6_early_c_inaccessible_pair_scout_unsat_certificates.py",
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


def frozen_scope():
    raw = structural.SCOUT.read_bytes()
    scout = json.loads(raw.decode("ascii"))
    rows = scout.get("rows", [])
    statuses = "".join({"UNSAT": "U", "TIMEOUT": "T"}.get(row.get("status"), "?") for row in rows)
    if len(rows) != 192 or statuses != structural.STATUS_SEQUENCE or digest(statuses.encode("ascii")) != \
            structural.STATUS_SEQUENCE_SHA256:
        raise RuntimeError("exact frozen scout status sequence changed")
    scope = tuple(row["child"] for row in rows if row["status"] == "UNSAT")
    if len(scope) != 172:
        raise RuntimeError("frozen scout does not select exactly 172 UNSAT children")
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
                raise RuntimeError("noncanonical certificate row value")
            rows.append(row)
    required = {
        "generated-utc": "2026-08-24",
        "scope": "f47a032-frozen-B7-l6-early-C-inaccessible-pair-exact-scout-UNSAT-only",
        "base-commit": "f47a032c88df5187a99b1895bae50dd363d80959",
        "cover-children": "192", "scout-unsat": "172", "scout-timeout": "20",
        "certified-children": "172", "parent-incidences": "645",
        "status-sequence": structural.STATUS_SEQUENCE,
        "status-sequence-sha256": structural.STATUS_SEQUENCE_SHA256,
        "solver": "CaDiCaL 1.7.3",
        "solver-source-commit": "38e073b389a877b0a0d3c91136d2443ab95fdeba",
        "solver-binary-sha256": "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292",
        "solver-command": "cadical --lrat --no-binary -q CNF LRAT", "solver-required-exit": "20",
        "checker": "lrat-check", "checker-source-commit": "2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
        "checker-binary-sha256": CHECKER_SHA256, "checker-required-output": "c VERIFIED",
        "compression": "xz -3", "compressor-binary": "/usr/bin/xz",
        "compressor-binary-sha256": "b5b163eb273291934556377ab883b4b2a5d4da50bd0dc0a91774ecc234ccd8d0",
        "compressed-limit-bytes-exclusive": str(LIMIT), "total-lrat-bytes": "1226909466",
        "total-xz-bytes": "81964720",
    }
    runtime_keys = {f"runtime-{path.name[:-3].replace('_', '-')}-{suffix}"
                    for path in runtime_source_closure() for suffix in ("bytes", "sha256")}
    expected = set(required) | {"verifier-canonical-sha256"} | runtime_keys | {
        f"{name}-{suffix}" for name in BOUND_PATHS for suffix in ("bytes", "sha256")
    }
    scope = frozen_scope()
    if columns is None or len(rows) != 172 or set(metadata) != expected or \
            any(metadata.get(name) != value for name, value in required.items()):
        raise RuntimeError("certificate metadata or exact scope changed")
    if tuple(int(row["child"]) for row in rows) != scope or len({row["child"] for row in rows}) != 172:
        raise RuntimeError("certificate rows do not equal the ordered complete scout-UNSAT set")
    if sum(int(row["parents"]) for row in rows) != 645 or \
            sum(int(row["lrat-bytes"]) for row in rows) != 1_226_909_466 or \
            sum(int(row["xz-bytes"]) for row in rows) != 81_964_720 or \
            int(metadata["total-xz-bytes"]) >= LIMIT:
        raise RuntimeError("certificate totals differ or compressed total is not below 250MB")
    return metadata, rows


def verify_bindings(metadata, checker):
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
    if checker != checker.resolve(strict=True) or identity(checker)[1] != CHECKER_SHA256:
        raise RuntimeError("checker path or binary is not pinned lrat-check")
    compressor = Path(metadata["compressor-binary"])
    if identity(compressor)[1] != metadata["compressor-binary-sha256"]:
        raise RuntimeError("compressor binary identity changed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path, required=True)
    args = parser.parse_args()
    checker = args.checker.resolve(strict=True)
    metadata, rows = load_ledger()
    verify_bindings(metadata, checker)
    children = producer.load_children()
    manifest = producer.manifest_payload(children)
    hashes = structural.load_hashes(manifest)
    structural.check_scout(manifest, hashes)
    with tempfile.TemporaryDirectory(prefix="inaccessible-pair-172-replay-", dir=ROOT) as directory:
        work = Path(directory)
        for position, row in enumerate(rows, 1):
            ordinal = int(row["child"])
            child = children[ordinal]
            name = f"m6-b7-l6-early-c-inaccessible-pair-child-{ordinal:03d}.lrat.xz"
            if row["artifact"] != f"certificates/{name}" or row["key"] != child[0] or \
                    row["profile"] != f"{child[1]:02d}" or row["parents"] != str(len(child[5])):
                raise RuntimeError("ledger row ancestry or safe artifact name changed")
            artifact = ROOT / row["artifact"]
            if identity(artifact) != (int(row["xz-bytes"]), row["xz-sha256"]):
                raise RuntimeError(f"child {ordinal:03d} compressed identity changed")
            cnf_path, lrat_path = work / f"c{ordinal:03d}.cnf", work / f"c{ordinal:03d}.lrat"
            cnf, selectors = producer.build_child(child)
            producer.write_child(cnf_path, ordinal, child, cnf, selectors, manifest)
            structural.check(cnf_path)
            if identity(cnf_path) != (int(row["cnf-bytes"]), row["cnf-sha256"]):
                raise RuntimeError(f"child {ordinal:03d} regenerated CNF changed")
            with lzma.open(artifact, "rb") as source, lrat_path.open("wb") as target:
                while block := source.read(1 << 20):
                    target.write(block)
            if identity(lrat_path) != (int(row["lrat-bytes"]), row["lrat-sha256"]):
                raise RuntimeError(f"child {ordinal:03d} raw LRAT identity changed")
            checked = subprocess.run([str(checker), str(cnf_path), str(lrat_path)],
                                     capture_output=True, text=True)
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError(f"child {ordinal:03d} LRAT rejected")
            print(f"PASS {position:03d}/172 child={ordinal:03d} xz={row['xz-bytes']}")
    print("PASS children=172 parent_incidences=645 total_xz_bytes=81964720 limit_exclusive=250000000")


if __name__ == "__main__":
    main()
