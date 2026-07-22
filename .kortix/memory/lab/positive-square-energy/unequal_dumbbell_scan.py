#!/usr/bin/env python3
"""Numerical scan of bridges between unequal odd cycles."""

from __future__ import annotations

import argparse
import numpy as np


def adjacency(p: int, q: int) -> np.ndarray:
    a = np.zeros((p + q, p + q))
    for offset, n in ((0, p), (p, q)):
        for i in range(n):
            a[offset + i, offset + (i + 1) % n] = 1
            a[offset + (i + 1) % n, offset + i] = 1
    a[0, p] = a[p, 0] = 1
    return a


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cycle", type=int, default=101)
    args = parser.parse_args()
    minimum = (float("inf"), 0, 0)
    count = 0
    for p in range(3, args.max_cycle + 1, 2):
        for q in range(p, args.max_cycle + 1, 2):
            eig = np.linalg.eigvalsh(adjacency(p, q))
            slack = float(np.dot(eig[eig > 0], eig[eig > 0]) - p - q)
            minimum = min(minimum, (slack, p, q))
            count += 1
    print(f"pairs={count} max_cycle={args.max_cycle}")
    print(f"minimum_slack={minimum[0]:.17g} p={minimum[1]} q={minimum[2]}")


if __name__ == "__main__":
    main()
