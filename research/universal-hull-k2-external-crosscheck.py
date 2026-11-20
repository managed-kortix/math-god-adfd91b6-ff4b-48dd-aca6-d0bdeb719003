#!/usr/bin/env python3
"""Independent NetworkX cross-check for candidate Tarjan/block-cut semantics."""
from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path

import networkx as nx


CANDIDATE = Path(__file__).with_name("universal-hull-k2-verifier.py")
spec = importlib.util.spec_from_file_location("hull_candidate", CANDIDATE)
module = importlib.util.module_from_spec(spec)
if spec.loader is None:
    raise RuntimeError("candidate module has no loader")
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def snapshot_from_nx(graph):
    return module._Snapshot(tuple(graph.nodes), tuple(graph.edges))


def block_edge_sets_candidate(graph):
    normalized = module._normalize_graph(snapshot_from_nx(graph))
    return frozenset(block.edges for block in module._tarjan_blocks(normalized))


def block_edge_sets_nx(graph):
    return frozenset(
        frozenset(frozenset(edge) for edge in component)
        for component in nx.biconnected_component_edges(graph)
    )


def theorem_reference(graph):
    if len(graph) == 0 or not nx.is_connected(graph):
        return None
    blocks = tuple(block_edge_sets_nx(graph))
    vertices = tuple(frozenset(v for edge in block for v in edge) for block in blocks)
    ranks = tuple(len(block) - len(block_vertices) + 1
                  for block, block_vertices in zip(blocks, vertices))
    positive = tuple(i for i, rank in enumerate(ranks) if rank > 0)
    beta = graph.number_of_edges() - graph.number_of_nodes() + 1
    partition = tuple(sorted((ranks[i] for i in positive), reverse=True))
    if beta != 7 or len(positive) != 2 or partition not in ((4, 3), (5, 2)):
        return None
    membership = {v: tuple(i for i, block_vertices in enumerate(vertices)
                           if v in block_vertices) for v in graph}
    cuts = tuple(v for v, indices in membership.items() if len(indices) > 1)
    tree = nx.Graph()
    tree.add_nodes_from(("B", i) for i in range(len(blocks)))
    tree.add_nodes_from(("C", v) for v in cuts)
    for cut in cuts:
        tree.add_edges_from((("C", cut), ("B", i)) for i in membership[cut])
    path = nx.shortest_path(tree, ("B", positive[0]), ("B", positive[1]))
    hull = frozenset(
        next(iter(blocks[node[1]]))
        for node in path
        if node[0] == "B" and ranks[node[1]] == 0 and len(blocks[node[1]]) == 1
    )
    if not hull:
        return None
    return partition, hull


def check_graph(graph, label):
    candidate_blocks = block_edge_sets_candidate(graph)
    reference_blocks = block_edge_sets_nx(graph)
    if candidate_blocks != reference_blocks:
        raise RuntimeError(f"Tarjan mismatch: {label}")
    reference = theorem_reference(graph)
    try:
        receipt = module.verify(tuple(graph.nodes), tuple(graph.edges))
    except module.VerifyError:
        if reference is not None:
            raise RuntimeError(f"candidate rejected reference-valid graph: {label}")
    else:
        if reference is None:
            raise RuntimeError(f"candidate accepted reference-invalid graph: {label}")
        if (receipt.partition, receipt.hull_edges) != reference:
            raise RuntimeError(f"receipt mismatch: {label}")


def random_connected_graph(rng, order, extra):
    graph = nx.random_labeled_tree(order, seed=rng.randrange(1 << 30))
    missing = list(nx.non_edges(graph))
    rng.shuffle(missing)
    graph.add_edges_from(missing[:extra])
    return graph


def main():
    rng = random.Random(4352)
    checked = 0
    # Broad Tarjan comparisons, including trees and arbitrary cyclic graphs.
    for order in range(2, 26):
        for extra in range(0, min(10, order * (order - 1) // 2 - order + 1)):
            for repeat in range(3):
                graph = random_connected_graph(rng, order, extra)
                check_graph(graph, f"random-n{order}-x{extra}-r{repeat}")
                checked += 1
    # Valid universal theorem graphs with randomized internal ranks, connector
    # lengths, off-hull arms, and graph insertion order.
    valid = 0
    for partition in ((4, 3), (5, 2)):
        for repeat in range(30):
            connector = rng.randrange(1, 30)
            payload = rng.randrange(0, 40)
            graph_data, unused = module._bridge_parent(
                partition, connector, payload_length=payload
            )
            graph = nx.Graph()
            edges = [tuple(edge) for edge in graph_data[1]]
            rng.shuffle(edges)
            graph.add_nodes_from(graph_data[0])
            graph.add_edges_from(edges)
            check_graph(graph, f"valid-{partition}-{repeat}")
            valid += 1
    print("external NetworkX cross-check: passed")
    print(f"connected graphs compared: {checked}; valid theorem graphs: {valid}")
    print("comparison: exact maximal-block edge sets, acceptance, partition, hull-edge set")


if __name__ == "__main__":
    main()
