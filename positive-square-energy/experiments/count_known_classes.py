#!/usr/bin/env python3
"""Count n=10 census graphs covered by diameter-2 or claw-free theorems."""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path

import numpy as np

from search_geng import graph6_adjacency


def covered(a: np.ndarray) -> tuple[bool, bool]:
    # Connected input has diameter <=2 iff every off-diagonal pair is adjacent
    # or has a common neighbor.
    diameter_two = bool(np.all((a + a @ a + np.eye(len(a))) > 0))
    claw_free = True
    for v in range(len(a)):
        neighbors = np.flatnonzero(a[v])
        for i, j, k in itertools.combinations(neighbors, 3):
            if not (a[i, j] or a[i, k] or a[j, k]):
                claw_free = False
                break
        if not claw_free:
            break
    return diameter_two, claw_free


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", type=Path)
    args = ap.parse_args()
    for path in args.files:
        count = d2 = cf = union = 0
        for raw in path.open("rb"):
            if not raw.strip():
                continue
            a = graph6_adjacency(raw).astype(np.int8)
            is_d2, is_cf = covered(a)
            count += 1
            d2 += is_d2
            cf += is_cf
            union += is_d2 or is_cf
        print(path.name, "count", count, "diameter2", d2, "clawfree", cf,
              "union", union, "uncovered", count - union, flush=True)


if __name__ == "__main__":
    main()
