#!/usr/bin/env python3
"""Counterexample-oriented search for bicyclic cacti with 1 mod 4 cycles.

Pendant stars are compressed exactly to one weighted leaf per occupied root.
The omitted leaf-difference eigenvalues are zero, so the reported square
energy is the square energy of the full unweighted graph up to roundoff.
"""

from __future__ import annotations

import argparse
import itertools
import math
import random
from dataclasses import dataclass

import networkx as nx
import numpy as np


@dataclass(order=True)
class Hit:
    slack: float
    family: str
    cycles: tuple[int, int]
    connector: int
    stars: tuple[int, ...]
    order: int


def cycle_pair(p: int, q: int, connector: int) -> tuple[nx.Graph, str]:
    """connector=0 is a shared vertex; connector>=1 is a joining path length."""
    if connector == 0:
        g = nx.cycle_graph(p)
        second = [0] + list(range(p, p + q - 1))
        g.add_edges_from((second[i], second[(i + 1) % q]) for i in range(q))
        return g, "figure8"
    g = nx.disjoint_union(nx.cycle_graph(p), nx.cycle_graph(q))
    left, right = 0, p
    previous = left
    for _ in range(connector - 1):
        vertex = len(g)
        g.add_node(vertex)
        g.add_edge(previous, vertex)
        previous = vertex
    g.add_edge(previous, right)
    return g, "path"


def compressed_matrix(core: nx.Graph, stars: tuple[int, ...]) -> np.ndarray:
    occupied = [i for i, count in enumerate(stars) if count]
    a = np.zeros((len(core) + len(occupied), len(core) + len(occupied)))
    for u, v in core.edges():
        a[u, v] = a[v, u] = 1.0
    for j, root in enumerate(occupied, len(core)):
        a[root, j] = a[j, root] = math.sqrt(stars[root])
    return a


def evaluate(core: nx.Graph, family: str, p: int, q: int, connector: int,
             stars: tuple[int, ...]) -> Hit:
    eig = np.linalg.eigvalsh(compressed_matrix(core, stars))
    positive = eig[eig > 1e-10]
    order = len(core) + sum(stars)
    return Hit(float(positive @ positive - order), family, (p, q), connector,
               stars, order)


def allocations(parts: int, budget: int):
    if parts == 1:
        yield (budget,)
        return
    for first in range(budget + 1):
        for rest in allocations(parts - 1, budget - first):
            yield (first,) + rest


def structured_stars(core: nx.Graph, max_leaves: int, rng: random.Random,
                     random_samples: int):
    n = len(core)
    yield (0,) * n
    distinguished = sorted(set(
        [v for v, degree in core.degree() if degree != 2]
        + [0, max(core.nodes())]
        + [v for v in core if core.degree(v) == 2][:4]
    ))
    sizes = sorted(set(range(min(max_leaves, 16) + 1)) | {
        min(max_leaves, x) for x in (24, 32, 64, 128, 256, 512, 1024,
                                     4096, 16384, 65536, 10**6)
    } | {max_leaves})
    for root in range(n):
        for size in sizes[1:]:
            stars = [0] * n
            stars[root] = size
            yield tuple(stars)
    for u, v in itertools.combinations_with_replacement(distinguished, 2):
        for total in sizes[1:]:
            for left in sorted(set([0, 1, total // 4, total // 2, 3 * total // 4,
                                    max(0, total - 1), total])):
                stars = [0] * n
                stars[u] += left
                stars[v] += total - left
                yield tuple(stars)
    if n <= 13:
        for total in range(min(max_leaves, 20) + 1):
            for roots in itertools.combinations(range(n), min(3, n)):
                for values in allocations(len(roots), total):
                    stars = [0] * n
                    for root, value in zip(roots, values):
                        stars[root] = value
                    yield tuple(stars)
    scale = math.log1p(max_leaves)
    for _ in range(random_samples):
        stars = [0] * n
        occupied = rng.randint(1, min(6, n))
        for root in rng.sample(range(n), occupied):
            stars[root] = min(max_leaves, int(math.expm1(rng.random() * scale)))
        yield tuple(stars)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cycle", type=int, default=17)
    parser.add_argument("--max-connector", type=int, default=12)
    parser.add_argument("--max-leaves", type=int, default=1024)
    parser.add_argument("--random-samples", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260725)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    lengths = list(range(5, args.max_cycle + 1, 4))
    best: list[Hit] = []
    count = 0
    for p in lengths:
        for q in lengths:
            if q < p:
                continue
            for connector in range(args.max_connector + 1):
                core, family = cycle_pair(p, q, connector)
                seen = set()
                for stars in structured_stars(core, args.max_leaves, rng,
                                              args.random_samples):
                    if stars in seen:
                        continue
                    seen.add(stars)
                    hit = evaluate(core, family, p, q, connector, stars)
                    best.append(hit)
                    best.sort()
                    del best[20:]
                    count += 1
    print(f"evaluated={count}")
    for hit in best:
        occupied = [(i, x) for i, x in enumerate(hit.stars) if x]
        print(f"slack={hit.slack:.17g} n={hit.order} family={hit.family} "
              f"cycles={hit.cycles} connector={hit.connector} stars={occupied}")


if __name__ == "__main__":
    main()
