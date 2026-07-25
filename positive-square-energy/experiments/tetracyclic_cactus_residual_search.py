#!/usr/bin/env python3
"""Search residual tetracyclic cactus cores and their massive-star limits."""

from __future__ import annotations

import argparse
import itertools
from collections import defaultdict, deque
from dataclasses import dataclass

import networkx as nx
import numpy as np


RESIDUALS = ((3, 3, 3, 3), (3, 3, 3, 5), (3, 3, 5, 5))


@dataclass(frozen=True)
class Hit:
    slack: float
    cycles: tuple[int, int, int, int]
    topology: str
    detail: str
    graph: nx.Graph
    root: int | None


def positive_square(graph: nx.Graph) -> float:
    matrix = nx.to_numpy_array(graph, nodelist=sorted(graph), dtype=float)
    values = np.linalg.eigvalsh(matrix)
    return float(np.square(values[values > 1e-9]).sum())


def star_limit(graph: nx.Graph, root: int) -> float:
    remainder = graph.copy()
    remainder.remove_node(root)
    return graph.degree(root) + positive_square(remainder) - len(graph)


def rooted_tree_edges(tree: nx.Graph, root: int) -> list[tuple[int, int]]:
    parent = {root: -1}
    queue = deque([root])
    edges: list[tuple[int, int]] = []
    while queue:
        vertex = queue.popleft()
        for child in tree[vertex]:
            if child in parent:
                continue
            parent[child] = vertex
            edges.append((vertex, child))
            queue.append(child)
    return edges


def build_core(
    lengths: tuple[int, int, int, int],
    tree: nx.Graph,
    root: int,
    positions: tuple[int, int, int],
    connectors: tuple[int, int, int],
) -> nx.Graph:
    graph = nx.Graph()
    cycle_vertices: dict[int, list[int]] = {}
    root_cycle = list(range(lengths[root]))
    graph.add_edges_from(
        (root_cycle[index], root_cycle[(index + 1) % lengths[root]])
        for index in range(lengths[root])
    )
    cycle_vertices[root] = root_cycle
    next_vertex = lengths[root]

    for edge_index, (parent, child) in enumerate(rooted_tree_edges(tree, root)):
        attachment = cycle_vertices[parent][positions[edge_index] % lengths[parent]]
        connector = connectors[edge_index]
        for _ in range(connector):
            graph.add_edge(attachment, next_vertex)
            attachment = next_vertex
            next_vertex += 1
        if connector == 0:
            child_cycle = [attachment] + list(
                range(next_vertex, next_vertex + lengths[child] - 1)
            )
            next_vertex += lengths[child] - 1
        else:
            child_cycle = [attachment] + list(
                range(next_vertex, next_vertex + lengths[child] - 1)
            )
            next_vertex += lengths[child] - 1
        graph.add_edges_from(
            (child_cycle[index], child_cycle[(index + 1) % lengths[child]])
            for index in range(lengths[child])
        )
        cycle_vertices[child] = child_cycle
    return nx.convert_node_labels_to_integers(graph)


def add_if_new(
    graph: nx.Graph,
    buckets: dict[str, list[nx.Graph]],
) -> bool:
    digest = nx.weisfeiler_lehman_graph_hash(graph)
    if any(nx.is_isomorphic(graph, old) for old in buckets[digest]):
        return False
    buckets[digest].append(graph)
    return True


def scan(args: argparse.Namespace) -> list[Hit]:
    hits: list[Hit] = []
    for multiset in RESIDUALS:
        buckets: dict[str, list[nx.Graph]] = defaultdict(list)
        length_orders = sorted(set(itertools.permutations(multiset)))
        for tree_index, tree in enumerate(nx.generators.nonisomorphic_trees(4)):
            tree = nx.convert_node_labels_to_integers(tree)
            for lengths in length_orders:
                for root in tree:
                    oriented = rooted_tree_edges(tree, root)
                    position_ranges = [range(lengths[parent]) for parent, _ in oriented]
                    for positions in itertools.product(*position_ranges):
                        for connectors in itertools.product(
                            range(args.max_connector + 1), repeat=3
                        ):
                            if args.shared_only and any(connectors):
                                continue
                            graph = build_core(
                                lengths, tree, root, positions, connectors
                            )
                            if not add_if_new(graph, buckets):
                                continue
                            topology = (
                                f"tree={tree_index} order={lengths} root={root} "
                                f"positions={positions} connectors={connectors}"
                            )
                            hits.append(
                                Hit(
                                    positive_square(graph) - len(graph),
                                    multiset,
                                    topology,
                                    "bare",
                                    graph,
                                    None,
                                )
                            )
                            for star_root in graph:
                                hits.append(
                                    Hit(
                                        star_limit(graph, star_root),
                                        multiset,
                                        topology,
                                        f"star-limit root={star_root} deg={graph.degree(star_root)}",
                                        graph,
                                        star_root,
                                    )
                                )
        print(f"cycles={multiset} nonisomorphic_cores={sum(map(len, buckets.values()))}")
    return hits


def edge_text(graph: nx.Graph) -> str:
    return ",".join(f"{u}-{v}" for u, v in sorted(graph.edges()))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-connector", type=int, default=1)
    parser.add_argument("--shared-only", action="store_true")
    parser.add_argument("--top", type=int, default=30)
    args = parser.parse_args()

    hits = scan(args)
    hits.sort(key=lambda hit: hit.slack)
    print("\nfrontier")
    for hit in hits[: args.top]:
        print(
            f"{hit.slack:.15f} cycles={hit.cycles} {hit.detail} "
            f"{hit.topology} edges={edge_text(hit.graph)}"
        )
    print("\nminimum by multiset")
    for multiset in RESIDUALS:
        hit = min((item for item in hits if item.cycles == multiset), key=lambda item: item.slack)
        print(
            f"{hit.slack:.15f} cycles={multiset} {hit.detail} "
            f"{hit.topology} edges={edge_text(hit.graph)}"
        )


if __name__ == "__main__":
    main()
