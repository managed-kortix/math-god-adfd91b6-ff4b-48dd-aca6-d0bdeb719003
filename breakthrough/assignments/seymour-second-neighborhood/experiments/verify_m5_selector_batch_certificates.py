#!/usr/bin/env python3
"""Replay retained LRAT pilots for the exact m=5 selector-batch cover.

This verifier authenticates and replays only rows retained in the certificate
ledger.  It deliberately refuses to turn a partial ledger into a branch-closure
claim.
"""

import argparse
import hashlib
import lzma
import subprocess
import tempfile
from pathlib import Path

import check_m5_selector_batch_cnf as structural
import m5_selector_batch_cnf as producer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGER = HERE / "m5-selector-batch-certificates.tsv"
FORMAT = "m5-selector-batch-certificates-v1"
COLUMNS = (
    "batch-key", "batch-ordinal", "branch", "members", "cnf-bytes",
    "cnf-sha256", "lrat-bytes", "lrat-sha256", "xz-bytes", "xz-sha256",
    "artifact",
)


def identity(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            digest.update(block)
    return path.stat().st_size, digest.hexdigest()


def load_ledger(path=LEDGER):
    data = path.read_bytes()
    lines = data.decode("ascii").splitlines()
    if not lines or lines[0] != FORMAT or data != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("certificate ledger format or framing differs")
    metadata, rows, columns = {}, [], None
    for line in lines[1:]:
        fields = line.split("\t")
        if fields[0] == "columns":
            if columns is not None or tuple(fields[1].split(",")) != COLUMNS:
                raise RuntimeError("certificate columns differ")
            columns = COLUMNS
        elif columns is None:
            if len(fields) != 2 or fields[0] in metadata:
                raise RuntimeError("certificate metadata is malformed or repeated")
            metadata[fields[0]] = fields[1]
        else:
            if len(fields) != len(COLUMNS):
                raise RuntimeError("certificate row has the wrong arity")
            rows.append(dict(zip(COLUMNS, fields)))
    required = {
        "generated-utc": "2026-11-19",
        "scope": "retained pilot only; no complete m=5 branch closure",
        "manifest-format": producer.MANIFEST_FORMAT,
        "manifest-bytes": str(producer.MANIFEST_BYTES),
        "manifest-sha256": producer.MANIFEST_SHA256,
        "solver": "CaDiCaL 1.7.3",
        "solver-binary-sha256": "e2a164ab490c49deb55dab4fb4d2704f7496f7653291106f88d0ddced2f820cd",
        "solver-command": "cadical --lrat --no-binary -q CNF LRAT",
        "solver-required-exit": "20",
        "checker": "lrat-check",
        "checker-binary-sha256": "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8",
        "checker-required-output": "c VERIFIED",
        "compression": "xz -9",
        "artifacts": "1",
        "covered-B6-parents": "100",
        "covered-B7-parents": "0",
    }
    if columns is None or metadata != required or len(rows) != 1:
        raise RuntimeError("certificate metadata or exact retained scope differs")
    row = rows[0]
    expected = {
        "batch-key": "B6-main-P6-00",
        "batch-ordinal": "0",
        "branch": "B6",
        "members": "100",
        "cnf-bytes": "10625508",
        "cnf-sha256": "9d551c0a2f94c57a8fb26f2718b5ea4f0b01fcb6b95adf1e845a24d4f58724d1",
        "lrat-bytes": "6685485",
        "lrat-sha256": "0b4e4558b1b76fdf855909cf65168dd16e6ebebc18ff38ada709aac42727ecfa",
        "xz-bytes": "349896",
        "xz-sha256": "5bb24d655defab83107046abca6635f575a3b4f9e1a4cd3b42a635ad92b215f1",
        "artifact": "certificates/m5-selector-B6-main-P6-00.lrat.xz",
    }
    if row != expected:
        raise RuntimeError("canonical pilot certificate row differs")
    return metadata, rows


def verify(checker):
    metadata, rows = load_ledger()
    manifest = producer.checked_manifest()
    if (len(manifest), hashlib.sha256(manifest).hexdigest()) != (
            int(metadata["manifest-bytes"]), metadata["manifest-sha256"]):
        raise RuntimeError("frozen selector manifest identity differs")
    checker_identity = identity(checker)
    if checker_identity[1] != metadata["checker-binary-sha256"]:
        raise RuntimeError("checker binary differs from the pinned lrat-check")
    with tempfile.TemporaryDirectory(prefix="m5-selector-replay-", dir=ROOT) as directory:
        work = Path(directory)
        for row in rows:
            key = row["batch-key"]
            batch = producer.select_batch(key)
            ordinal = producer.batches().index(batch)
            if (str(ordinal), batch["branch"], str(len(batch["members"]))) != (
                    row["batch-ordinal"], row["branch"], row["members"]):
                raise RuntimeError("ledger row does not identify the frozen batch")
            cnf, selectors = producer.build_batch(batch)
            cnf_path = work / f"{key}.cnf"
            lrat_path = work / f"{key}.lrat"
            producer.write_batch(cnf_path, batch, cnf, selectors, manifest)
            structural.check(cnf_path)
            if identity(cnf_path) != (int(row["cnf-bytes"]), row["cnf-sha256"]):
                raise RuntimeError("regenerated pilot CNF identity differs")
            artifact = ROOT / row["artifact"]
            if artifact.parent != ROOT / "certificates":
                raise RuntimeError("artifact path escapes the certificate directory")
            if identity(artifact) != (int(row["xz-bytes"]), row["xz-sha256"]):
                raise RuntimeError("compressed pilot artifact identity differs")
            with lzma.open(artifact, "rb") as source, lrat_path.open("wb") as target:
                while block := source.read(1 << 20):
                    target.write(block)
            if identity(lrat_path) != (int(row["lrat-bytes"]), row["lrat-sha256"]):
                raise RuntimeError("decompressed pilot LRAT identity differs")
            checked = subprocess.run(
                [str(checker), str(cnf_path), str(lrat_path)],
                capture_output=True, text=True,
            )
            if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
                raise RuntimeError("pilot LRAT was rejected")
            print(
                f"PASS key={key} members={len(batch['members'])} "
                f"cnf_sha256={row['cnf-sha256']} lrat_sha256={row['lrat-sha256']}"
            )
    covered = sum(int(row["members"]) for row in rows)
    if covered != int(metadata["covered-B6-parents"]):
        raise RuntimeError("retained parent count differs from ledger")
    print(
        f"PASS retained_artifacts={len(rows)} covered_B6={covered}/4355 "
        f"covered_B7={metadata['covered-B7-parents']}/3083 "
        f"checker_bytes={checker_identity[0]} checker_sha256={checker_identity[1]}"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path, required=True)
    args = parser.parse_args()
    verify(args.checker.resolve())


if __name__ == "__main__":
    main()
