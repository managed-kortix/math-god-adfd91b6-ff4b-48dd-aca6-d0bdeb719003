#!/usr/bin/env python3
"""Heuristic search for failure of s+(G)>=n => s+(G+e)>=n.

Discovery only: every reported candidate must later receive exact certification.
"""

from __future__ import annotations

import argparse
import random

import networkx as nx
import numpy as np


def splus(a: np.ndarray) -> float:
    w = np.linalg.eigvalsh(a)
    return float(np.dot(w[w > 0], w[w > 0]))


def scan_graph(g: nx.Graph, best: dict) -> tuple | None:
    n = len(g)
    a = nx.to_numpy_array(g, dtype=float)
    before = splus(a)
    if before < n - 1e-9:
        return None
    for u, v in nx.non_edges(g):
        a[u, v] = a[v, u] = 1
        after = splus(a)
        a[u, v] = a[v, u] = 0
        decrease = before - after
        if decrease > best["decrease"][0]:
            best["decrease"] = (decrease, before - n, after - n,
                                nx.to_graph6_bytes(g, header=False).strip().decode(), u, v)
            print("DECREASE", best["decrease"], flush=True)
        if after < n - 1e-8:
            return (nx.to_graph6_bytes(g, header=False).strip().decode(),
                    u, v, before, after)
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--nmin", type=int, default=8)
    ap.add_argument("--nmax", type=int, default=30)
    ap.add_argument("--seed", type=int, default=20260724)
    ap.add_argument("--sparse", action="store_true")
    args = ap.parse_args()
    rng = random.Random(args.seed)
    best = {"decrease": (-1.0,)}
    for trial in range(args.trials):
        n = rng.randint(args.nmin, args.nmax)
        # Mix sparse threshold-scale graphs and denser graphs where negative
        # positive-part entries are more common.
        if args.sparse:
            m = rng.randint(n + 1, min(n + 10, n * (n - 1) // 2))
            g = nx.gnm_random_graph(n, m, seed=rng.randrange(1 << 63))
        elif trial % 3 == 0:
            p = rng.uniform(2.0 / n, 5.0 / n)
            g = nx.gnp_random_graph(n, p, seed=rng.randrange(1 << 63))
        else:
            p = rng.uniform(0.12, 0.88)
            g = nx.gnp_random_graph(n, p, seed=rng.randrange(1 << 63))
        if not nx.is_connected(g):
            continue
        hit = scan_graph(g, best)
        if hit:
            print("CROSSING", hit, flush=True)
            return
    print("NO_CROSSING", best, flush=True)


if __name__ == "__main__":
    main()
