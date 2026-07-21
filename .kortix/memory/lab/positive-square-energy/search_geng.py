#!/usr/bin/env python3
"""Stream graph6 graphs from nauty-geng and rank by positive square-energy slack."""

from __future__ import annotations

import argparse
import heapq
import subprocess

import numpy as np


def graph6_adjacency(line: bytes) -> np.ndarray:
    data = [b - 63 for b in line.strip()]
    if not data or data[0] > 62:
        raise ValueError("only graph6 orders <= 62 are supported")
    n = data[0]
    bits = ((x >> shift) & 1 for x in data[1:] for shift in range(5, -1, -1))
    a = np.zeros((n, n), dtype=float)
    # graph6 orders upper-triangle bits by columns: (0,1),(0,2),(1,2),...
    for j in range(1, n):
        for i in range(j):
            a[i, j] = a[j, i] = next(bits)
    return a


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("m", type=int)
    parser.add_argument("--keep", type=int, default=20)
    args = parser.parse_args()

    cmd = ["nauty-geng", "-cq", str(args.n), f"{args.m}:{args.m}"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdout is not None
    heap: list[tuple[float, str, list[float]]] = []  # max-via-negative slack
    count = 0
    for raw in proc.stdout:
        g6 = raw.decode().strip()
        a = graph6_adjacency(raw)
        eig = np.linalg.eigvalsh(a)
        slack = float(np.dot(eig[eig > 0], eig[eig > 0]) - args.n)
        item = (-slack, g6, eig.tolist())
        if len(heap) < args.keep:
            heapq.heappush(heap, item)
        elif item > heap[0]:
            heapq.heapreplace(heap, item)
        count += 1
    stderr = proc.stderr.read().decode() if proc.stderr else ""
    if proc.wait() != 0:
        raise SystemExit(stderr)

    print(f"# n={args.n} m={args.m} count={count} keep={args.keep}")
    for neg_slack, g6, eig in sorted(heap, key=lambda x: -x[0]):
        positives = [x for x in eig if x > 1e-9]
        print(f"{(-neg_slack):.15g}\t{g6}\t{','.join(f'{x:.12g}' for x in positives)}")


if __name__ == "__main__":
    main()
