#!/usr/bin/env python3
"""Compact exhaustive SymPy certificate for a graph6 file.

Unlike exact_certify.py, this does not factor or print each characteristic
polynomial. It exact-isolates every real root, rejects any nonpositive lower
bound, and emits a compact summary plus a SHA-256 digest of the ordered input.
"""

from __future__ import annotations

import argparse
import hashlib
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction

import sympy as s

from exact_certify import s_plus_bounds


def certify(g6: str) -> tuple[str, int, int]:
    _, lower, _, _ = s_plus_bounds(g6)
    if lower <= 0:
        raise RuntimeError(f"NONPOSITIVE {g6} {lower}")
    return g6, int(lower.p), int(lower.q)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-file", "-f", required=True)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--chunksize", type=int, default=32)
    args = ap.parse_args()

    with open(args.from_file, "rb") as fh:
        raw = fh.read()
    graphs = [line.decode().strip() for line in raw.splitlines() if line.strip()]
    digest = hashlib.sha256(b"\n".join(g.encode() for g in graphs) + b"\n").hexdigest()

    minimum: tuple[Fraction, str] | None = None
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for g6, p, q in pool.map(certify, graphs, chunksize=args.chunksize):
            value = Fraction(p, q)
            if minimum is None or value < minimum[0]:
                minimum = value, g6

    assert minimum is not None
    value, g6 = minimum
    print(f"PASS count={len(graphs)} sha256={digest}")
    print(f"minimum_graph6={g6}")
    print(f"minimum_exact_lower={value.numerator}/{value.denominator}")
    print(f"minimum_lower_decimal={float(value):.17g}")


if __name__ == "__main__":
    main()
