#!/usr/bin/env python3
"""Regenerate and independently replay the exact k4 simultaneous-source package.

The verifier fails closed.  It checks the frozen ledger schema and totals, all
source/artifact identities, the exact finite orbit cover, deterministic CNF
regeneration, producer-independent structural reconstruction, raw LRAT identity
while streaming decompression, and one successful ``c VERIFIED`` from the
pinned proof checker for every retained branch.
"""

from __future__ import annotations

import argparse
import hashlib
import lzma
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGER = HERE / "k4-simsrc-certificates.tsv"
FORMAT = "k4-simsrc-certificates-v1"
COLUMNS = (
    "case", "p", "source", "pair", "parent_source", "parent_pair",
    "orbit_size", "variables", "clauses", "cnf_bytes", "cnf_sha256",
    "lrat_bytes", "lrat_sha256", "xz_bytes", "xz_sha256", "artifact",
)
SOURCE_PATHS = {
    "generator": HERE / "k4_simsrc_cnf.py",
    "structural_checker": HERE / "check_k4_simsrc_cnf.py",
    "split_checker": HERE / "k4_simsrc_split.py",
}
EXPECTED_METADATA = {
    "scope": "conditional-rooted-m8-k4-simultaneous-source-T-projection-p6-p7",
    "format": FORMAT,
    "generator": "experiments/k4_simsrc_cnf.py",
    "structural_checker": "experiments/check_k4_simsrc_cnf.py",
    "split_checker": "experiments/k4_simsrc_split.py",
    "proof_checker": "lrat-check",
    "checker_source_commit": "2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
    "checker_source_sha256": "bf07c2ac96b9035da1ebcc578cb95e956a2b795629d613154cdb307f8a8f4a95",
    "checker_binary_bytes": "22064",
    "checker_binary_sha256": "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8",
    "solver": "CaDiCaL-1.7.3",
    "solver_source_commit": "38e073b389a877b0a0d3c91136d2443ab95fdeba",
    "solver_command": "cadical --lrat --no-binary -q CNF LRAT",
    "solver_required_exit": "20",
    "checker_required_exit": "0",
    "checker_required_output": "one-literal-c-VERIFIED",
    "compression": "xz-stream-retained",
    "generator_sha256": "04dab677b19f07a006a606f9f6461ab04f5814b4304519c12a3ce991bce69f5f",
    "structural_checker_sha256": "0fcaf5039c804ff33c1667cc7d9eb46d618320b4f828535166ba6b852e73fc01",
    "split_checker_sha256": "6e327e7febe4aa60a8ab0ace60f610f052f34a6f273e13b6da816229be020915",
    "rows": "45",
    "p6_rows": "17",
    "p7_direct_rows": "11",
    "p7_refined_rows": "17",
    "p6_total_xz_bytes": "58140108",
    "p7_total_xz_bytes": "230672140",
    "all_total_xz_bytes": "288812248",
}


def identity(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            size += len(block)
            digest.update(block)
    return size, digest.hexdigest()


def require_identity(path: Path, size: str | int, digest: str, label: str) -> None:
    expected = int(size), digest
    actual = identity(path)
    if actual != expected:
        raise RuntimeError(f"{label} identity mismatch: expected {expected}, got {actual}")


def load_ledger(path: Path):
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != FORMAT:
        raise RuntimeError("unexpected certificate ledger format")
    metadata: dict[str, str] = {}
    rows: list[dict[str, str]] = []
    columns = None
    for line in lines[1:]:
        fields = line.split("\t")
        if fields[0] == "columns":
            if columns is not None or len(fields) != 2 or tuple(fields[1].split(",")) != COLUMNS:
                raise RuntimeError("certificate columns changed")
            columns = COLUMNS
        elif columns is None:
            if len(fields) != 2 or fields[0] in metadata:
                raise RuntimeError("malformed or duplicate ledger metadata")
            metadata[fields[0]] = fields[1]
        else:
            if len(fields) != len(COLUMNS):
                raise RuntimeError("malformed certificate row")
            rows.append(dict(zip(COLUMNS, fields)))
    if metadata != EXPECTED_METADATA:
        mismatches = {
            key: {"expected": value, "actual": metadata.get(key)}
            for key, value in EXPECTED_METADATA.items()
            if metadata.get(key) != value
        }
        extra = {key: value for key, value in metadata.items() if key not in EXPECTED_METADATA}
        raise RuntimeError(f"frozen metadata changed: mismatches={mismatches}, extra={extra}")
    if columns is None or len(rows) != 45:
        raise RuntimeError("ledger does not contain the exact 45 certificate rows")
    return metadata, rows


def parse_pair(text: str) -> tuple[int, int]:
    values = tuple(map(int, text.split(",")))
    if len(values) != 2 or values[0] >= values[1]:
        raise RuntimeError("malformed canonical pair")
    return values


def expected_rows_from_split():
    sys.path.insert(0, str(HERE))
    import k4_simsrc_split as split

    split.audit()
    expected = []
    for index, pair, orbit in split.p6_orbits():
        expected.append(("p6-first", 6, 2, pair, None, None, len(orbit), index))
    for index, pair, orbit in split.p7_first_orbits():
        if index != split.P7_REFINED_PARENT_INDEX:
            expected.append(("p7-first", 7, 2, pair, None, None, len(orbit), index))
    parent = split.allowed_pairs(2)[split.P7_REFINED_PARENT_INDEX]
    for index, pair, orbit in split.p7_suborbits():
        expected.append(("p7-refined", 7, 3, pair, 2, parent, len(orbit), index))
    return expected


def verify_scope(rows) -> None:
    expected = expected_rows_from_split()
    if len(expected) != len(rows):
        raise RuntimeError("split and ledger row counts differ")
    seen_artifacts: set[str] = set()
    for record, item in zip(rows, expected):
        case, p, source, pair, parent_source, parent_pair, orbit_size, index = item
        actual = (
            record["case"], int(record["p"]), int(record["source"]), parse_pair(record["pair"]),
            None if record["parent_source"] == "-" else int(record["parent_source"]),
            None if record["parent_pair"] == "-" else parse_pair(record["parent_pair"]),
            int(record["orbit_size"]),
        )
        if actual != item[:-1]:
            raise RuntimeError(f"ledger row differs from split: expected {item[:-1]}, got {actual}")
        if case == "p6-first":
            artifact = f"certificates/k4-simsrc-p6-orbit-{index:03d}.lrat.xz"
        elif case == "p7-first":
            artifact = f"certificates/k4-simsrc-p7-orbit-{index:03d}.lrat.xz"
        else:
            artifact = f"certificates/k4-simsrc-p7-orbit-014-suborbit-{index:03d}.lrat.xz"
        if record["artifact"] != artifact or artifact in seen_artifacts:
            raise RuntimeError("artifact name is unsafe, duplicate, or differs from the exact split")
        seen_artifacts.add(artifact)

    sums = {
        "p6_total_xz_bytes": sum(int(row["xz_bytes"]) for row in rows if row["p"] == "6"),
        "p7_total_xz_bytes": sum(int(row["xz_bytes"]) for row in rows if row["p"] == "7"),
        "all_total_xz_bytes": sum(int(row["xz_bytes"]) for row in rows),
    }
    if any(str(value) != EXPECTED_METADATA[key] for key, value in sums.items()):
        raise RuntimeError("compressed-byte totals changed")
    # The convention applies per logical package: p=6 and p=7 are separate.
    if sums["p6_total_xz_bytes"] >= 250_000_000 or sums["p7_total_xz_bytes"] >= 250_000_000:
        raise RuntimeError("a logical certificate package exceeds 250,000,000 bytes")


def run(command, label: str, **kwargs) -> subprocess.CompletedProcess:
    result = subprocess.run(command, **kwargs)
    if result.returncode:
        raise RuntimeError(f"{label} failed with exit {result.returncode}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", required=True, type=Path)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--identity-only", action="store_true",
                        help="check ledger, cover, tools, and artifact hashes without replaying LRATs")
    args = parser.parse_args()

    metadata, rows = load_ledger(args.ledger)
    for label, path in SOURCE_PATHS.items():
        if not path.is_file():
            raise RuntimeError(f"missing {label}: {path}")
        if identity(path)[1] != metadata[f"{label}_sha256"]:
            raise RuntimeError(f"{label} source identity changed")
    require_identity(
        args.checker,
        metadata["checker_binary_bytes"],
        metadata["checker_binary_sha256"],
        "proof checker",
    )
    verify_scope(rows)

    for record in rows:
        artifact = ROOT / record["artifact"]
        require_identity(artifact, record["xz_bytes"], record["xz_sha256"], record["artifact"])
    if args.identity_only:
        print("PASS identity-only rows=45 p6_xz_bytes=58140108 p7_xz_bytes=230672140")
        return

    temporary_root = Path(os.environ.get("TMPDIR", "/tmp"))
    with tempfile.TemporaryDirectory(prefix="k4-simsrc-verify-", dir=temporary_root) as directory:
        work = Path(directory)
        for ordinal, record in enumerate(rows):
            p = int(record["p"])
            source = int(record["source"])
            pair = record["pair"]
            selections = [f"{source}:{pair}"]
            if record["parent_source"] != "-":
                selections.insert(0, f"{record['parent_source']}:{record['parent_pair']}")
            stem = f"leaf-{ordinal:02d}"
            cnf, variable_map, lrat = work / f"{stem}.cnf", work / f"{stem}.map", work / f"{stem}.lrat"

            producer_command = [sys.executable, str(SOURCE_PATHS["generator"]), str(p), str(cnf), "--map", str(variable_map)]
            checker_command = [sys.executable, str(SOURCE_PATHS["structural_checker"]), str(p), str(cnf), str(variable_map)]
            for selection in selections:
                producer_command += ["--select", selection]
                checker_command += ["--select", selection]
            run(producer_command, f"row {ordinal} CNF regeneration", cwd=HERE, stdout=subprocess.DEVNULL)
            require_identity(cnf, record["cnf_bytes"], record["cnf_sha256"], f"row {ordinal} regenerated CNF")
            run(checker_command, f"row {ordinal} structural check", cwd=HERE, stdout=subprocess.DEVNULL)

            digest = hashlib.sha256()
            raw_size = 0
            with lzma.open(ROOT / record["artifact"], "rb") as source_handle, lrat.open("wb") as target:
                while block := source_handle.read(1 << 20):
                    raw_size += len(block)
                    digest.update(block)
                    target.write(block)
            if (raw_size, digest.hexdigest()) != (int(record["lrat_bytes"]), record["lrat_sha256"]):
                raise RuntimeError(f"row {ordinal} decompressed LRAT identity mismatch")

            checked = run([str(args.checker), str(cnf), str(lrat)], f"row {ordinal} LRAT check",
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            if checked.stdout.splitlines().count("c VERIFIED") != 1:
                raise RuntimeError(f"row {ordinal} checker did not emit exactly one literal c VERIFIED")
            lrat.unlink()
            print(f"PASS row={ordinal:02d} case={record['case']} p={p} selections={';'.join(selections)}")

    print("PASS full-replay rows=45 p6_xz_bytes=58140108 p7_xz_bytes=230672140")


if __name__ == "__main__":
    main()
