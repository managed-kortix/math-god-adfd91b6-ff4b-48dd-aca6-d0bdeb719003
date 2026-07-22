#!/usr/bin/env python3
"""Validate and aggregate paired atomic SymPy/PARI chunk certificates."""

from __future__ import annotations

import argparse
import hashlib
import re
from fractions import Fraction
from pathlib import Path


def fields(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if line.startswith("PASS "):
            out.update(re.findall(r"(count|sha256)=([^ ]+)", line))
        elif "=" in line:
            key, value = line.split("=", 1)
            out[key] = value
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--whole-file", type=Path,
                    help="independently verify chunks partition this complete input")
    args = ap.parse_args()
    inputs = sorted(args.data_dir.glob(f"{args.prefix}-chunk-*.g6"))
    if not inputs:
        raise RuntimeError("no chunks")
    total = 0
    global_digest = hashlib.sha256()
    sym_min: tuple[Fraction, str] | None = None
    pari_min: tuple[float, str, str] | None = None
    for inp in inputs:
        raw = inp.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        count = len(raw.splitlines())
        sym = fields(inp.with_suffix(".sympy.out"))
        pari = fields(inp.with_suffix(".pari.out"))
        if int(sym["count"]) != count or int(pari["count"]) != count:
            raise RuntimeError(f"count mismatch {inp}")
        if sym["sha256"] != digest or pari["sha256"] != digest:
            raise RuntimeError(f"hash mismatch {inp}")
        p, q = map(int, sym["minimum_exact_lower"].split("/"))
        sv = Fraction(p, q)
        if sym_min is None or sv < sym_min[0]:
            sym_min = sv, sym["minimum_graph6"]
        pv = float(pari["minimum_slack_80d"])
        if pari_min is None or pv < pari_min[0]:
            pari_min = pv, pari["minimum_graph6"], pari["minimum_slack_80d"]
        total += count
        global_digest.update(raw)
    assert sym_min and pari_min
    whole_digest = None
    if args.whole_file:
        whole_raw = args.whole_file.read_bytes()
        whole_lines = whole_raw.splitlines()
        chunk_lines = []
        for inp in inputs:
            chunk_lines.extend(inp.read_bytes().splitlines())
        if sorted(chunk_lines) != sorted(whole_lines):
            raise RuntimeError("chunks do not form the same graph6 multiset as whole file")
        whole_digest = hashlib.sha256(whole_raw).hexdigest()
    if sym_min[1] != pari_min[1]:
        raise RuntimeError("engines disagree on minimizer")
    print(f"PASS chunks={len(inputs)} count={total} sha256={global_digest.hexdigest()}")
    print(f"minimum_graph6={sym_min[1]}")
    print(f"sympy_minimum_exact_lower={sym_min[0].numerator}/{sym_min[0].denominator}")
    print(f"pari_minimum_slack_80d={pari_min[2]}")
    if whole_digest:
        print(f"whole_input_sha256={whole_digest}")


if __name__ == "__main__":
    main()
