#!/usr/bin/env python3
"""Regenerate and verify the frozen clean-sink B6-l4 LRAT certificate."""

import argparse
import hashlib
import lzma
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGER = HERE / "m6-clean-sink-B6-l4-certificate.tsv"
FORMAT = "m6-clean-sink-B6-l4-certificate-v1"
GROUP = "B6-l4"
IDENTITY_PATHS = {
    "selector-manifest": HERE / "m6-clean-sink-selector-groups.tsv",
    "remaining-stream": HERE / "m6-clean-sink-remaining.tsv",
    "clean-sink-manifest": HERE / "m6-clean-sink-manifest.tsv",
    "clean-sink-theorem": ROOT / "attempts" / "tick52-rooted-clean-sink-theorem.md",
    "producer": HERE / "m6_clean_sink_group_cnf.py",
    "structural-checker": HERE / "check_m6_clean_sink_group_cnf.py",
}
KEYS = (
    "generated-utc", "group", "parents", "solver", "solver-source-commit",
    "solver-binary-sha256", "solver-command", "solver-required-exit", "checker",
    "checker-source-commit", "checker-binary-sha256", "checker-required-output",
    "compression", "selector-manifest-bytes", "selector-manifest-sha256",
    "remaining-stream-bytes", "remaining-stream-sha256", "clean-sink-manifest-bytes",
    "clean-sink-manifest-sha256", "clean-sink-theorem-bytes",
    "clean-sink-theorem-sha256", "producer-bytes", "producer-sha256",
    "structural-checker-bytes", "structural-checker-sha256", "cnf-variables",
    "cnf-clauses", "cnf-bytes", "cnf-sha256", "lrat-bytes", "lrat-sha256",
    "xz-bytes", "xz-sha256", "generate-seconds", "structure-seconds",
    "solve-seconds", "check-seconds", "compress-seconds", "artifact",
)
FIXED = {
    "generated-utc": "2026-08-02",
    "group": GROUP,
    "parents": "2470",
    "solver": "CaDiCaL 1.7.3",
    "solver-source-commit": "38e073b389a877b0a0d3c91136d2443ab95fdeba",
    "solver-binary-sha256": "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292",
    "solver-command": "cadical --lrat --no-binary -q CNF LRAT",
    "solver-required-exit": "20",
    "checker": "lrat-check",
    "checker-source-commit": "2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
    "checker-binary-sha256": "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8",
    "checker-required-output": "c VERIFIED",
    "compression": "xz -3",
    "selector-manifest-bytes": "1838",
    "selector-manifest-sha256": "6e7eee0ddd5b4c7ef02cdf459c9a0647f720513e7ee4987a3a8b0c17af37eeda",
    "remaining-stream-bytes": "2262190",
    "remaining-stream-sha256": "416b7e51a73637784342a374be8e15a1a58032b61fc1140f39f0768d1ff4b642",
    "clean-sink-manifest-bytes": "2104",
    "clean-sink-manifest-sha256": "733e06c8aa9881e0006409efff23729f1bf88d8af7b1a70e8a78fd3775b53217",
    "clean-sink-theorem-bytes": "4156",
    "clean-sink-theorem-sha256": "bd0631529bb4658061663460b718ef2ee3186d02fdc599fb2673d3cff3b94ee2",
    "producer-bytes": "11550",
    "producer-sha256": "9eb6455daf71a2127f76a197012c2e0f4a7c7f42021ddfcfbe244f9f733ed817",
    "structural-checker-bytes": "14918",
    "structural-checker-sha256": "07d2ac0802c8d9fc854e8c5e10ef0e1a67f54dda2c06c1a71bf69465390ee536",
    "cnf-variables": "26086",
    "cnf-clauses": "520647",
    "cnf-bytes": "16535716",
    "cnf-sha256": "f576b3b590135c41ca1cf1eddf11338d3dddc58a9ca9d13bf92283e2def96e19",
    "lrat-bytes": "40592810",
    "lrat-sha256": "736b931b78d2c305f00b3482990cea7769944737eb81a6dd42da18c17d936fa0",
    "xz-bytes": "5185308",
    "xz-sha256": "a532fcbe254ca54922c9c1eb190d547dff948bb61cb6aa55d92ce5546a39f996",
    "artifact": "certificates/m6-clean-sink-B6-l4.lrat.xz",
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def identity(path):
    return path.stat().st_size, sha256(path)


def load_ledger(path):
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != FORMAT or len(lines) != len(KEYS) + 1:
        raise RuntimeError("unexpected certificate ledger format or length")
    metadata = {}
    order = []
    for line in lines[1:]:
        fields = line.split("\t")
        if len(fields) != 2 or fields[0] in metadata:
            raise RuntimeError("malformed or duplicate certificate ledger field")
        order.append(fields[0])
        metadata[fields[0]] = fields[1]
    if tuple(order) != KEYS:
        raise RuntimeError("certificate ledger keys or canonical order changed")
    if any(metadata[name] != value for name, value in FIXED.items()):
        raise RuntimeError("fixed certificate ledger metadata changed")
    for name in ("generate-seconds", "structure-seconds", "solve-seconds",
                 "check-seconds", "compress-seconds"):
        if not float(metadata[name]) >= 0:
            raise RuntimeError(f"invalid timing field: {name}")
    return metadata


def require_identity(path, expected_bytes, expected_hash, label):
    expected = int(expected_bytes), expected_hash
    actual = identity(path)
    if actual != expected:
        raise RuntimeError(f"{label} identity mismatch: expected {expected}, got {actual}")


def run(command, label, **kwargs):
    result = subprocess.run(command, **kwargs)
    if result.returncode:
        raise RuntimeError(f"{label} failed with exit {result.returncode}")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--checker", type=Path, required=True)
    args = parser.parse_args()
    metadata = load_ledger(args.ledger)

    for name, path in IDENTITY_PATHS.items():
        require_identity(path, metadata[f"{name}-bytes"], metadata[f"{name}-sha256"], name)
    if sha256(args.checker) != metadata["checker-binary-sha256"]:
        raise RuntimeError("checker binary is not the pinned executable")

    relative = Path(metadata["artifact"])
    if (relative.is_absolute() or ".." in relative.parts or len(relative.parts) != 2 or
            relative.parts[0] != "certificates"):
        raise RuntimeError("artifact path is outside the certificate directory")
    artifact = ROOT / relative
    require_identity(artifact, metadata["xz-bytes"], metadata["xz-sha256"], "compressed LRAT")

    with tempfile.TemporaryDirectory(prefix="m6-clean-sink-B6-l4-verify-") as directory:
        work = Path(directory)
        cnf = work / "B6-l4.cnf"
        run(
            [sys.executable, str(IDENTITY_PATHS["producer"]), "--group", GROUP,
             "--output", str(cnf)],
            "CNF regeneration", cwd=HERE, stdout=subprocess.DEVNULL,
        )
        require_identity(cnf, metadata["cnf-bytes"], metadata["cnf-sha256"], "CNF")
        run(
            [sys.executable, str(IDENTITY_PATHS["structural-checker"]), str(cnf)],
            "CNF structural check", cwd=HERE, stdout=subprocess.DEVNULL,
        )

        lrat = work / "B6-l4.lrat"
        with lzma.open(artifact, "rb") as source, lrat.open("wb") as target:
            while block := source.read(1 << 20):
                target.write(block)
        require_identity(lrat, metadata["lrat-bytes"], metadata["lrat-sha256"], "LRAT")
        checked = subprocess.run(
            [str(args.checker), str(cnf), str(lrat)], capture_output=True, text=True
        )
        if checked.returncode or metadata["checker-required-output"] not in checked.stdout:
            raise RuntimeError("LRAT was not accepted by the pinned checker")

    print(
        f"PASS group={GROUP} parents={metadata['parents']} cnf_bytes={metadata['cnf-bytes']} "
        f"lrat_bytes={metadata['lrat-bytes']} xz_bytes={metadata['xz-bytes']}"
    )


if __name__ == "__main__":
    main()
