#!/usr/bin/env python3
"""Fresh, checkpointed two-engine reproduction of a complete (n,m) slice."""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def valid_output(path: Path, digest: str) -> bool:
    if not path.exists():
        return False
    text = path.read_text()
    return "PASS " in text and f"sha256={digest}" in text


def run_atomic(command: list[str], output: Path, digest: str) -> None:
    if valid_output(output, digest):
        return
    temporary = output.with_suffix(output.suffix + ".tmp")
    with temporary.open("w") as stream:
        subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, check=True)
    if not valid_output(temporary, digest):
        raise RuntimeError(f"invalid certificate output: {temporary}")
    os.replace(temporary, output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("m", type=int)
    parser.add_argument("--chunks", type=int, default=32)
    parser.add_argument("--parallel", type=int, default=16)
    parser.add_argument("--inner-workers", type=int, default=2)
    parser.add_argument("--digits", type=int, default=6)
    parser.add_argument("--skip-sympy", action="store_true")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    args.output_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"n{args.n}m{args.m}"
    whole = args.output_dir / f"{prefix}.g6"

    # Regenerate from nauty in this process, rather than copying prior input.
    generated = subprocess.run(
        ["nauty-geng", "-cq", str(args.n), f"{args.m}:{args.m}"],
        stdout=subprocess.PIPE, check=True,
    ).stdout
    whole.write_bytes(generated)
    lines = generated.splitlines(keepends=True)
    chunks: list[Path] = []
    for index in range(args.chunks):
        path = args.output_dir / f"{prefix}-chunk-{index:02d}.g6"
        path.write_bytes(b"".join(lines[index::args.chunks]))
        chunks.append(path)

    def sympy_job(path: Path) -> None:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        run_atomic([
            str(Path.home() / "mathenv/bin/python"),
            str(here / "batch_exact_certify.py"), "-f", str(path),
            "--workers", str(args.inner_workers), "--digits", str(args.digits),
        ], path.with_suffix(".sympy.out"), digest)

    if not args.skip_sympy:
        with ThreadPoolExecutor(max_workers=args.parallel) as pool:
            list(pool.map(sympy_job, chunks))
    else:
        missing = [path for path in chunks if not valid_output(
            path.with_suffix(".sympy.out"), hashlib.sha256(path.read_bytes()).hexdigest()
        )]
        if missing:
            raise RuntimeError(f"cannot skip SymPy: {len(missing)} chunk outputs missing")

    def pari_job(path: Path) -> None:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        run_atomic([
            str(Path.home() / "mathenv/bin/python"),
            str(here / "batch_pari_verify.py"), "-f", str(path),
            "--workers", str(args.inner_workers),
        ], path.with_suffix(".pari.out"), digest)

    with ThreadPoolExecutor(max_workers=args.parallel) as pool:
        list(pool.map(pari_job, chunks))

    subprocess.run([
        str(Path.home() / "mathenv/bin/python"),
        str(here / "aggregate_chunk_certificates.py"),
        "--data-dir", str(args.output_dir), "--prefix", prefix,
        "--whole-file", str(whole),
    ], check=True)


if __name__ == "__main__":
    main()
