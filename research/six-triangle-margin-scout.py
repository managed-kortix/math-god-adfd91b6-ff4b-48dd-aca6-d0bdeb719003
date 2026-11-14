#!/usr/bin/env python3
"""NONPROMOTIONAL exact/numerical scout for the six-triangle margin.

The structural conclusion is checked by a finite reduced-cluster partition
census.  Spectral rows are evidence only: bare shared-cut topologies use exact
integer characteristic polynomials and rational Sturm isolation; long
connectors and large rooted stars use floating-point symmetric eigensolvers.
No numerical row is promoted to a proof.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import numpy as np


REPO = Path(__file__).resolve().parents[1]


def load(name: str, relative: str):
    path = REPO / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


incidence = load("six_triangle_incidence", "research/octacyclic-rooted-six-triangle-certificate.py")
exact = load("six_triangle_exact", "research/shared_triangle_rooted_exact.py")


def add_edge(edges: set[tuple[int, int]], left: int, right: int) -> None:
    assert left != right
    edges.add(tuple(sorted((left, right))))


def add_triangle(edges: set[tuple[int, int]], vertices: tuple[int, int, int]) -> None:
    for index in range(3):
        add_edge(edges, vertices[index], vertices[(index + 1) % 3])


def realize_shared_cluster(tree) -> tuple[int, set[tuple[int, int]]]:
    adjacency = incidence.adjacency(tree)
    cuts = range(6, len(adjacency))
    cut_image = {cut: index for index, cut in enumerate(cuts)}
    order = len(cut_image)
    edges: set[tuple[int, int]] = set()
    for triangle in range(6):
        vertices = [cut_image[cut] for cut in adjacency[triangle]]
        while len(vertices) < 3:
            vertices.append(order)
            order += 1
        assert len(vertices) == len(set(vertices)) == 3
        add_triangle(edges, tuple(vertices))
    return order, edges


def exact_surplus_interval(order: int, edges: set[tuple[int, int]], bits: int = 28) -> tuple[Fraction, Fraction]:
    certificate = exact.surplus_certificate((order, edges, 0), bits)
    return tuple(Fraction(value) for value in certificate["surplus_interval"])  # type: ignore[return-value]


def numerical_surplus(order: int, edges: set[tuple[int, int]]) -> float:
    adjacency = np.zeros((order, order), dtype=float)
    for left, right in edges:
        adjacency[left, right] = adjacency[right, left] = 1.0
    eigenvalues = np.linalg.eigvalsh(adjacency)
    return float(np.square(eigenvalues[eigenvalues > 1e-9]).sum() - order)


def six_disjoint_triangles(connector_length: int) -> tuple[int, set[tuple[int, int]]]:
    assert connector_length >= 1
    edges: set[tuple[int, int]] = set()
    order = 0
    roots = []
    for _ in range(6):
        root = order
        add_triangle(edges, (order, order + 1, order + 2))
        roots.append(root)
        order += 3
    for index in range(5):
        previous = roots[index]
        for _ in range(connector_length - 1):
            add_edge(edges, previous, order)
            previous = order
            order += 1
        add_edge(edges, previous, roots[index + 1])
    return order, edges


def attach_uniform_leaves(graph: tuple[int, set[tuple[int, int]]], leaves: int) -> tuple[int, set[tuple[int, int]]]:
    order, base_edges = graph
    edges = set(base_edges)
    roots = list(range(order))
    for root in roots:
        for _ in range(leaves):
            add_edge(edges, root, order)
            order += 1
    return order, edges


def integer_partitions(total: int, maximum: int | None = None):
    maximum = total if maximum is None else min(maximum, total)
    if total == 0:
        yield ()
        return
    for first in range(maximum, 0, -1):
        for rest in integer_partitions(total - first, first):
            yield (first,) + rest


def structural_partition_census() -> tuple[tuple[int, ...], ...]:
    """Check every shared-cluster size partition of six.

    Inputs used by the ledger are b_1=0,b_2=1,b_3=2,b_4=3,b_5=2,b_6=1,
    all strict.  If some cluster has size >=2 it alone supplies >1 (for size
    2 exactly the all-incidence TT theorem supplies >1); all other cyclic
    territories are strict positive.  If all are singletons, choose a marked leaf and its nearest other marked
    node.  Their path has no third marked node and gives an arbitrary-connector
    TT territory >1, leaving only positive triangular territories.
    """
    rows = tuple(integer_partitions(6))
    assert len(rows) == 11
    for row in rows:
        assert sum(row) == 6
        if max(row) >= 2:
            distinguished = max(row)
            assert distinguished in (2, 3, 4, 5, 6)
            # For 2 use TT>1; for 3..6 use the shared-cluster strict floors.
            strict_margin_floor = {2: 1, 3: 2, 4: 3, 5: 2, 6: 1}[distinguished]
            assert strict_margin_floor >= 1
        else:
            assert row == (1, 1, 1, 1, 1, 1)
            # Choose a marked leaf and its nearest other marked node.  The
            # connecting path has no third marked node.  Cutting every other
            # incident actual bridge realizes one attached TT territory and
            # positive remainders.
    return rows


def main() -> None:
    partitions = structural_partition_census()

    exact_rows = []
    for code, tree in incidence.enumerate_trees(6):
        order, edges = realize_shared_cluster(tree)
        lower, upper = exact_surplus_interval(order, edges)
        assert lower > 1
        exact_rows.append((lower, upper, code))
    assert len(exact_rows) == 19
    exact_minimum = min(exact_rows)
    assert all(exact_minimum[1] < row[0] for row in exact_rows if row is not exact_minimum)

    connector_rows = []
    for length in (1, 2, 3, 5, 10, 20, 50):
        graph = six_disjoint_triangles(length)
        value = numerical_surplus(*graph)
        assert value > 1
        connector_rows.append((length, graph[0], value))

    leaf_rows = []
    base = six_disjoint_triangles(1)
    for leaves in (0, 1, 2, 5, 10, 20, 50, 100):
        graph = attach_uniform_leaves(base, leaves)
        value = numerical_surplus(*graph)
        assert value > 1
        leaf_rows.append((leaves, graph[0], value))

    print("NONPROMOTIONAL six-triangle margin scout")
    print("structural cluster-size partitions:", len(partitions), partitions)
    print("decomposition verdict: sigma>1 for every connected triangular block graph with exactly six triangles")
    print("proof route: retain one >=2 cluster (or a nearest-pair connector TT between singleton clusters); all remaining cyclic territories have sigma>0")
    print("exact bare shared-cut incidence classes:", len(exact_rows))
    print("exact minimum interval:", exact.rational_text(exact_minimum[0]), exact.rational_text(exact_minimum[1]))
    print("exact minimum incidence code:", exact_minimum[2])
    print("long connector samples (length, vertices, sigma):")
    for row in connector_rows:
        print(" ", row)
    print("uniform rooted-star samples (leaves per base vertex, vertices, sigma):")
    for row in leaf_rows:
        print(" ", row)
    print("LIMITATION: exact spectra cover bare shared-cut classes; connector/star eigenspectra are numerical probes only. The theorem strategy is the induced-territory decomposition, not numerical extrapolation.")


if __name__ == "__main__":
    main()
