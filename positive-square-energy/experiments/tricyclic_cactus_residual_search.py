#!/usr/bin/env python3
"""Targeted quotient search for residual tricyclic cactus cycle triples."""

from __future__ import annotations

import argparse
import itertools
import math
from dataclasses import dataclass

import networkx as nx
import numpy as np


@dataclass(frozen=True)
class Hit:
    slack: float
    family: str
    cycles: tuple[int, int, int]
    detail: str


def add_cycle(g: nx.Graph, length: int, root: int | None = None) -> tuple[int, list[int]]:
    if root is None:
        root = len(g)
        g.add_node(root)
    vertices = [root] + list(range(len(g), len(g) + length - 1))
    g.add_edges_from((vertices[i], vertices[(i + 1) % length]) for i in range(length))
    return root, vertices


def add_path_to_new(g: nx.Graph, root: int, length: int) -> int:
    current = root
    for _ in range(length):
        nxt = len(g)
        g.add_edge(current, nxt)
        current = nxt
    return current


def y_core(cycles: tuple[int, int, int], arms: tuple[int, int, int]) -> nx.Graph:
    g = nx.Graph()
    junction = 0
    g.add_node(junction)
    for length, arm in zip(cycles, arms):
        root = add_path_to_new(g, junction, arm) if arm else junction
        add_cycle(g, length, root)
    return nx.convert_node_labels_to_integers(g)


def chain_core(
    cycles: tuple[int, int, int], left: int, right: int, separation: int
) -> nx.Graph:
    g = nx.Graph()
    middle_root, middle = add_cycle(g, cycles[1])
    right_root = middle[separation % cycles[1]]
    left_tip = add_path_to_new(g, middle_root, left)
    right_tip = add_path_to_new(g, right_root, right)
    add_cycle(g, cycles[0], left_tip)
    add_cycle(g, cycles[2], right_tip)
    return nx.convert_node_labels_to_integers(g)


def adjacency(g: nx.Graph) -> np.ndarray:
    return nx.to_numpy_array(g, nodelist=list(g), dtype=float)


def positive_square(matrix: np.ndarray) -> float:
    values = np.linalg.eigvalsh(matrix)
    return float(np.square(values[values > 1e-9]).sum())


def star_slack(g: nx.Graph, root: int, leaves: int) -> float:
    a = np.zeros((len(g) + 1, len(g) + 1))
    a[:-1, :-1] = adjacency(g)
    a[root, -1] = a[-1, root] = math.sqrt(leaves)
    return positive_square(a) - len(g) - leaves


def broom_slack(g: nx.Graph, root: int, stem: int, leaves: int) -> float:
    h = g.copy()
    hub = add_path_to_new(h, root, stem)
    return star_slack(h, hub, leaves)


def star_limit(g: nx.Graph, root: int) -> float:
    remainder = g.copy()
    remainder.remove_node(root)
    return g.degree(root) + positive_square(adjacency(remainder)) - len(g)


def scan_core(g: nx.Graph, family: str, cycles: tuple[int, int, int], args: argparse.Namespace) -> list[Hit]:
    hits = [Hit(positive_square(adjacency(g)) - len(g), family, cycles, "bare")]
    for root in g:
        hits.append(Hit(star_limit(g, root), family, cycles, f"star-limit root={root} deg={g.degree(root)}"))
        for leaves in args.stars:
            hits.append(Hit(star_slack(g, root, leaves), family, cycles, f"star root={root} t={leaves}"))
        for stem in range(1, args.max_stem + 1):
            for leaves in args.broom_stars:
                hits.append(Hit(broom_slack(g, root, stem, leaves), family, cycles, f"broom root={root} stem={stem} t={leaves}"))
    return hits


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-connector", type=int, default=5)
    parser.add_argument("--max-stem", type=int, default=6)
    parser.add_argument("--stars", type=int, nargs="*", default=[1, 2, 10, 1000, 100000000])
    parser.add_argument("--broom-stars", type=int, nargs="*", default=[10, 1000000])
    parser.add_argument("--top", type=int, default=30)
    args = parser.parse_args()

    triples = [(3, 5, 5)] + [(3, 3, q) for q in range(3, 22, 2)]
    hits: list[Hit] = []
    seen: set[tuple[tuple[int, int, int], str]] = set()
    for cycles in triples:
        for arms in itertools.product(range(args.max_connector + 1), repeat=3):
            if min(arms) != 0:
                continue
            g = y_core(cycles, arms)
            key = (cycles, nx.weisfeiler_lehman_graph_hash(g))
            if key in seen:
                continue
            seen.add(key)
            hits.extend(scan_core(g, f"Y arms={arms}", cycles, args))
        for middle_index in range(3):
            ordered = (cycles[(middle_index + 1) % 3], cycles[middle_index], cycles[(middle_index + 2) % 3])
            for left in range(args.max_connector + 1):
                for right in range(args.max_connector + 1):
                    for separation in range(ordered[1] // 2 + 1):
                        g = chain_core(ordered, left, right, separation)
                        key = (cycles, nx.weisfeiler_lehman_graph_hash(g))
                        if key in seen:
                            continue
                        seen.add(key)
                        hits.extend(scan_core(g, f"chain order={ordered} paths=({left},{right}) sep={separation}", cycles, args))

    hits.sort(key=lambda hit: hit.slack)
    print(f"cores={len(seen)} candidates={len(hits)}")
    for hit in hits[: args.top]:
        print(f"{hit.slack:.15f} cycles={hit.cycles} {hit.family} {hit.detail}")
    print("\nminimum by triple")
    for cycles in triples:
        hit = min((item for item in hits if item.cycles == cycles), key=lambda item: item.slack)
        print(f"{hit.slack:.15f} cycles={cycles} {hit.family} {hit.detail}")


if __name__ == "__main__":
    main()
