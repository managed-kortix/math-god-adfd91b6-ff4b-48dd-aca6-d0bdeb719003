#!/usr/bin/env python3
"""Enumerate shared-cut C3,C3,C3,Cq cores and audit 2R-Zq I."""

from __future__ import annotations

import argparse
import itertools
import random
from collections import defaultdict
from fractions import Fraction

import networkx as nx


def rooted_edges(tree: nx.Graph, root: int) -> list[tuple[int, int]]:
    result = []
    seen = {root}
    queue = [root]
    while queue:
        parent = queue.pop(0)
        for child in tree[parent]:
            if child not in seen:
                seen.add(child)
                queue.append(child)
                result.append((parent, child))
    return result


def build(lengths, tree, root, positions):
    graph = nx.Graph()
    cycles = {}
    vertices = list(range(lengths[root]))
    cycles[root] = vertices
    graph.add_edges_from((vertices[i], vertices[(i + 1) % len(vertices)]) for i in range(len(vertices)))
    next_vertex = len(vertices)
    for edge_index, (parent, child) in enumerate(rooted_edges(tree, root)):
        cut = cycles[parent][positions[edge_index] % lengths[parent]]
        vertices = [cut] + list(range(next_vertex, next_vertex + lengths[child] - 1))
        next_vertex += lengths[child] - 1
        cycles[child] = vertices
        graph.add_edges_from((vertices[i], vertices[(i + 1) % len(vertices)]) for i in range(len(vertices)))
    return nx.convert_node_labels_to_integers(graph)


def cores(q: int):
    buckets = defaultdict(list)
    result = []
    for lengths in sorted(set(itertools.permutations((3, 3, 3, q)))):
        for tree in nx.generators.nonisomorphic_trees(4):
            tree = nx.convert_node_labels_to_integers(tree)
            for root in tree:
                ranges = [range(lengths[parent]) for parent, _ in rooted_edges(tree, root)]
                for positions in itertools.product(*ranges):
                    graph = build(lengths, tree, root, positions)
                    digest = nx.weisfeiler_lehman_graph_hash(graph)
                    if any(nx.is_isomorphic(graph, old) for old in buckets[digest]):
                        continue
                    buckets[digest].append(graph)
                    result.append(graph)
    return result


def cycle_blocks(graph: nx.Graph):
    blocks = [frozenset(block) for block in nx.biconnected_components(graph) if len(block) >= 3]
    triangles = [block for block in blocks if len(block) == 3]
    long_cycle = next(block for block in blocks if len(block) != 3)
    return triangles, long_cycle


def matching_partition(graph: nx.Graph, activities, deleted=frozenset()):
    available = frozenset(graph) - deleted
    cache = {}

    def visit(vertices):
        if not vertices:
            return activities[0] * 0 + 1
        if vertices in cache:
            return cache[vertices]
        vertex = min(vertices)
        remainder = vertices - {vertex}
        total = activities[vertex] * visit(remainder)
        for neighbor in graph[vertex]:
            if neighbor in remainder:
                total += visit(remainder - {neighbor})
        cache[vertices] = total
        return total

    return visit(available)


def z_cycle(q, t):
    graph = nx.cycle_graph(q)
    return matching_partition(graph, [t] * q)


def certificate(graph, activities, t):
    triangles, long_cycle = cycle_blocks(graph)
    cycles = triangles + [long_cycle]
    factors = [-2j, -2j, -2j, 2j]
    real = matching_partition(graph, activities)
    imag = real * 0
    for mask in range(1, 1 << 4):
        chosen = [index for index in range(4) if mask & (1 << index)]
        if any(cycles[i] & cycles[j] for i, j in itertools.combinations(chosen, 2)):
            continue
        deleted = frozenset().union(*(cycles[index] for index in chosen))
        factor = 1
        for index in chosen:
            factor *= factors[index]
        term = matching_partition(graph, activities, deleted)
        real += int(factor.real) * term
        imag += int(factor.imag) * term
    value = 2 * real - z_cycle(len(long_cycle), t) * imag
    return real, imag, value


def edge_text(graph):
    return ",".join(f"{u}-{v}" for u, v in sorted(graph.edges()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=650)
    parser.add_argument("--binary", action="store_true")
    args = parser.parse_args()
    rng = random.Random(args.seed)
    for q in (5, 9):
        graphs = cores(q)
        best = None
        for core_index, graph in enumerate(graphs):
            if args.binary:
                tests = []
                for t in (Fraction(1, 100), Fraction(1, 10), Fraction(1)):
                    for high in (Fraction(1), Fraction(10), Fraction(100)):
                        if high < t:
                            continue
                        tests.extend(
                            (t, [high if mask & (1 << vertex) else t for vertex in graph])
                            for mask in range(1 << len(graph))
                        )
            else:
                tests = [(1.0, [1.0] * len(graph))]
                tests.extend(
                    (10 ** rng.uniform(-3, 3), None)
                    for _ in range(args.samples)
                )
            for t, activities in tests:
                if activities is None:
                    activities = [t + 10 ** rng.uniform(-3, 5) for _ in graph]
                real, imag, value = certificate(graph, activities, t)
                normalized = value / max(1.0, 2 * abs(real), abs(z_cycle(q, t) * imag))
                hit = (normalized, value, core_index, graph, activities, t, real, imag)
                if best is None or normalized < best[0]:
                    best = hit
                if normalized <= 0:
                    break
            if best[0] <= 0:
                break
        normalized, value, core_index, graph, activities, t, real, imag = best
        print(f"q={q} core_types={len(graphs)} normalized={normalized} value={value} core={core_index} t={t} R={real} I={imag}")
        print(f"edges={edge_text(graph)}")
        print("activities=" + ",".join(f"{i}:{activity}" for i, activity in enumerate(activities)))


if __name__ == "__main__":
    main()
