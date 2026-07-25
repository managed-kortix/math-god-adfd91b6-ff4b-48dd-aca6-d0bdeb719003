#!/usr/bin/env python3
"""Enumerate rooted block graphs and test clique-star spanning-tree witnesses."""

from __future__ import annotations

import argparse
import itertools
from collections.abc import Iterator

import networkx as nx
import numpy as np


Rooted = tuple[tuple["Rooted", ...], ...]


def weighted_multisets(
    items: list[tuple[int, object]], total: int, start: int = 0
) -> Iterator[tuple[object, ...]]:
    if total == 0:
        yield ()
        return
    for i in range(start, len(items)):
        weight, item = items[i]
        if weight > total:
            break
        for rest in weighted_multisets(items, total - weight, i):
            yield (item,) + rest


def rooted_objects(max_n: int) -> list[list[Rooted]]:
    roots: list[list[Rooted]] = [[] for _ in range(max_n + 1)]
    roots[1] = [()]
    branches: list[list[tuple[Rooted, ...]]] = [[] for _ in range(max_n)]
    for weight in range(1, max_n):
        root_items = [
            (size, root)
            for size in range(1, weight + 1)
            for root in roots[size]
        ]
        branches[weight] = list(weighted_multisets(root_items, weight))
        branch_items = [
            (size, branch)
            for size in range(1, weight + 1)
            for branch in branches[size]
        ]
        roots[weight + 1] = list(weighted_multisets(branch_items, weight))
    return roots


def realize(root: Rooted) -> tuple[nx.Graph, list[tuple[int, ...]]]:
    graph = nx.Graph()
    blocks: list[tuple[int, ...]] = []

    def visit(obj: Rooted, vertex: int) -> None:
        graph.add_node(vertex)
        for branch in obj:
            clique = [vertex]
            children: list[tuple[Rooted, int]] = []
            for child in branch:
                child_vertex = len(graph)
                graph.add_node(child_vertex)
                clique.append(child_vertex)
                children.append((child, child_vertex))
            graph.add_edges_from(itertools.combinations(clique, 2))
            blocks.append(tuple(clique))
            for child, child_vertex in children:
                visit(child, child_vertex)

    visit(root, 0)
    return graph, blocks


def canonical_key(graph: nx.Graph, blocks: list[tuple[int, ...]]) -> str:
    incidence = nx.Graph()
    incidence.add_nodes_from(("v", vertex) for vertex in graph)
    for index, block in enumerate(blocks):
        block_node = ("b", index)
        incidence.add_node(block_node)
        incidence.add_edges_from((block_node, ("v", vertex)) for vertex in block)

    centers = list(nx.center(incidence))

    def encode(node: tuple[str, int], parent: tuple[str, int] | None) -> str:
        children = sorted(
            encode(child, node) for child in incidence[node] if child != parent
        )
        return node[0] + "(" + "".join(children) + ")"

    return min(encode(center, None) for center in centers)


def positive_part(adjacency: np.ndarray) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh(adjacency)
    return (eigenvectors * np.maximum(eigenvalues, 0.0)) @ eigenvectors.T


def best_star_witness(
    graph: nx.Graph, blocks: list[tuple[int, ...]]
) -> tuple[float, tuple[int, ...]]:
    cyclic = [block for block in blocks if len(block) >= 3]
    fixed = [block for block in blocks if len(block) == 2]
    best = (-1.0, ())
    n = len(graph)
    for centers in itertools.product(*(block for block in cyclic)):
        tree = np.zeros((n, n))
        deleted: list[tuple[int, int]] = []
        for u, v in fixed:
            tree[u, v] = tree[v, u] = 1.0
        for block, center in zip(cyclic, centers):
            for vertex in block:
                if vertex != center:
                    tree[center, vertex] = tree[vertex, center] = 1.0
            deleted.extend(
                (u, v)
                for u, v in itertools.combinations(block, 2)
                if center not in (u, v)
            )
        positive = positive_part(tree)
        value = sum(positive[u, v] for u, v in deleted)
        if value > best[0]:
            best = (value, centers)
    return best


def cyclomatic(blocks: list[tuple[int, ...]]) -> int:
    return sum((len(block) - 1) * (len(block) - 2) // 2 for block in blocks)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=14)
    args = parser.parse_args()
    roots = rooted_objects(args.max_n)
    for n in range(1, args.max_n + 1):
        seen: set[str] = set()
        minimum = (float("inf"), None)
        unique = tested = 0
        for root in roots[n]:
            graph, blocks = realize(root)
            key = canonical_key(graph, blocks)
            if key in seen:
                continue
            seen.add(key)
            unique += 1
            if cyclomatic(blocks) < 2:
                continue
            tested += 1
            value, centers = best_star_witness(graph, blocks)
            if value < minimum[0]:
                minimum = (value, (root, centers, nx.to_graph6_bytes(graph).strip()))
        print(n, len(roots[n]), unique, tested, minimum, flush=True)


if __name__ == "__main__":
    main()
