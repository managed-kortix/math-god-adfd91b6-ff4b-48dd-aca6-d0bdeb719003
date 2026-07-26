#!/usr/bin/env python3
"""Adversarial search for s+(H+uv) < s+(H) on cactus bridge paths.

Every unweighted candidate is represented by an exact symmetric quotient:
stars with t leaves become one leaf joined with weight sqrt(t).  The searched
graph H is a cactus and the unique u-v path consists only of bridges, so adding
uv creates one new cactus cycle.  Floating point output is discovery data.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import dataclass

import networkx as nx
import numpy as np
from scipy.optimize import differential_evolution


def splus(a: np.ndarray) -> float:
    w = np.linalg.eigvalsh(a)
    return float(w[w > 0] @ w[w > 0])


def increment(a: np.ndarray, u: int, v: int) -> float:
    b = a.copy()
    b[u, v] = b[v, u] = 1.0
    return splus(b) - splus(a)


@dataclass
class Quotient:
    matrix: np.ndarray
    graph: nx.Graph
    roots: list[int]
    star_counts: list[int]
    u: int
    v: int
    description: str


def path_c5_core(length: int, masks: list[int]) -> tuple[nx.Graph, list[int]]:
    g = nx.path_graph(length + 1)
    roots = list(range(length + 1))
    nxt = length + 1
    for root, count in enumerate(masks):
        for _ in range(count):
            vertices = [root] + list(range(nxt, nxt + 4))
            nxt += 4
            g.add_edges_from((vertices[i], vertices[(i + 1) % 5]) for i in range(5))
    return g, roots


def add_broom(g: nx.Graph, root: int, stem: int) -> int:
    at = root
    for _ in range(stem):
        new = len(g)
        g.add_edge(at, new)
        at = new
    return at


def quotient(g: nx.Graph, star_roots: list[int], counts: list[int]) -> np.ndarray:
    a = nx.to_numpy_array(g, nodelist=range(len(g)), dtype=float)
    active = [(r, t) for r, t in zip(star_roots, counts) if t]
    q = np.zeros((len(g) + len(active), len(g) + len(active)))
    q[:len(g), :len(g)] = a
    for j, (root, count) in enumerate(active, len(g)):
        q[root, j] = q[j, root] = math.sqrt(count)
    return q


def materialize(q: Quotient) -> nx.Graph:
    g = q.graph.copy()
    for root, count in zip(q.roots, q.star_counts):
        for _ in range(count):
            g.add_edge(root, len(g))
    return g


def random_count(rng: random.Random, maximum: int) -> int:
    if rng.random() < 0.45:
        return 0
    if rng.random() < 0.35:
        return rng.randint(1, min(maximum, 12))
    return max(1, int(round(math.exp(rng.uniform(0, math.log(maximum))))))


def unweighted_search(rng: random.Random, trials: int, max_path: int,
                      max_star: int) -> Quotient:
    best: Quotient | None = None
    best_delta = math.inf
    for _ in range(trials):
        length = rng.randint(2, max_path)
        # Bias toward asymmetric pre-existing pentagons, but permit bouquets.
        masks = [rng.choices((0, 1, 2), weights=(6, 3, 1))[0]
                 for _ in range(length + 1)]
        g, path_roots = path_c5_core(length, masks)
        roots = path_roots.copy()
        if rng.random() < 0.65:
            for __ in range(rng.randint(1, 3)):
                roots.append(add_broom(g, rng.choice(path_roots), rng.randint(1, 8)))
        counts = [random_count(rng, max_star) for _ in roots]
        a = quotient(g, roots, counts)
        delta = increment(a, 0, length)
        if delta < best_delta:
            best_delta = delta
            best = Quotient(a, g, roots, counts, 0, length,
                            f"path={length}, c5_counts={masks}")
    assert best is not None
    return best


def weighted_path_search(length: int, c5_left: int, c5_right: int,
                         seed: int) -> tuple[float, np.ndarray, np.ndarray]:
    masks = [0] * (length + 1)
    masks[0], masks[-1] = c5_left, c5_right
    g, _ = path_c5_core(length, masks)
    base = nx.to_numpy_array(g, nodelist=range(len(g)), dtype=float)
    edges = list(g.edges())

    # Variables are positive edge weights and diagonal vertex potentials.
    # The added closing edge retains weight one.
    def objective(x: np.ndarray) -> float:
        a = np.zeros_like(base)
        for weight, (i, j) in zip(x[:len(edges)], edges):
            a[i, j] = a[j, i] = weight
        np.fill_diagonal(a, x[len(edges):])
        return increment(a, 0, length)

    bounds = [(0.05, 8.0)] * len(edges) + [(-8.0, 8.0)] * len(g)
    result = differential_evolution(objective, bounds, seed=seed, popsize=8,
                                    maxiter=180, polish=True, workers=1,
                                    updating="immediate", tol=1e-9)
    return float(result.fun), result.x, np.array(edges, dtype=int)


def describe(q: Quotient) -> dict[str, object]:
    delta = increment(q.matrix, q.u, q.v)
    graph = materialize(q)
    return {
        "description": q.description,
        "order": len(graph),
        "size_before": graph.number_of_edges(),
        "closure_edge": [q.u, q.v],
        "increment": delta,
        "splus_before": splus(q.matrix),
        "splus_after": splus(q.matrix) + delta,
        "core_edges": sorted([list(e) for e in q.graph.edges()]),
        "star_roots_counts": [[r, t] for r, t in zip(q.roots, q.star_counts) if t],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260725)
    parser.add_argument("--trials", type=int, default=100000)
    parser.add_argument("--max-path", type=int, default=40)
    parser.add_argument("--max-star", type=int, default=10**9)
    parser.add_argument("--weighted", action="store_true")
    args = parser.parse_args()
    rng = random.Random(args.seed)
    best = unweighted_search(rng, args.trials, args.max_path, args.max_star)
    print("UNWEIGHTED_BEST")
    print(json.dumps(describe(best), indent=2))
    if args.weighted:
        for length, left, right in ((2, 0, 0), (3, 0, 0), (4, 1, 0),
                                    (5, 1, 1), (8, 2, 1)):
            value, x, edges = weighted_path_search(length, left, right, args.seed + length)
            print("WEIGHTED", length, left, right, "increment", value)
            print("edge_weights", [(e.tolist(), float(w)) for e, w in zip(edges, x)])
            print("potentials", x[len(edges):].tolist())


if __name__ == "__main__":
    main()
