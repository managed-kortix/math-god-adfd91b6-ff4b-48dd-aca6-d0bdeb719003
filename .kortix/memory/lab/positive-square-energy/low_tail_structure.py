#!/usr/bin/env python3
"""Structural fingerprints for a graph6 low tail."""

from __future__ import annotations

import argparse
import itertools

import networkx as nx
import numpy as np

from search_geng import graph6_adjacency


def induced_claw(g: nx.Graph) -> bool:
    for v in g:
        for triple in itertools.combinations(g.neighbors(v), 3):
            if all(not g.has_edge(a, b) for a, b in itertools.combinations(triple, 2)):
                return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph6_file")
    args = parser.parse_args()
    print("graph6\tdiameter\tgirth\ttriangles\tclaw\tinertia\tdegrees")
    for raw in open(args.graph6_file, "rb"):
        g6 = raw.decode().strip()
        a = graph6_adjacency(raw).astype(int)
        g = nx.from_numpy_array(a)
        eig = np.linalg.eigvalsh(a)
        inertia = (sum(eig > 1e-8), sum(abs(eig) <= 1e-8), sum(eig < -1e-8))
        degrees = ",".join(map(str, sorted(dict(g.degree()).values(), reverse=True)))
        triangles = sum(nx.triangles(g).values()) // 3
        print(f"{g6}\t{nx.diameter(g)}\t{nx.girth(g)}\t{triangles}\t"
              f"{int(induced_claw(g))}\t{inertia[0]},{inertia[1]},{inertia[2]}\t{degrees}")


if __name__ == "__main__":
    main()
