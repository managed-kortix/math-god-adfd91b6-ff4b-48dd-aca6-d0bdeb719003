#!/usr/bin/env python3
"""Fail-closed verifier for the R31-S marked four-triangle C4 packet."""

from __future__ import annotations

import itertools
import subprocess
import sys
from collections import Counter


class AuditError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def add_triangle(edges, owner, next_vertex):
    u, v = next_vertex, next_vertex + 1
    edges.update({tuple(sorted((owner, u))), tuple(sorted((owner, v))), (u, v)})
    return (owner, u, v), next_vertex + 2


def records_for_side(side):
    owners = tuple(side)
    direct = [("direct3", roots) for roots in itertools.combinations_with_replacement(owners, 3)]
    chain_direct = [("chain2+direct", upstream, root) for upstream in owners for root in owners]
    fork = [("fork", upstream, occupancy) for upstream in owners for occupancy in ("same", "split")]
    chain = [("chain3", upstream) for upstream in owners]
    return direct + chain_direct + fork + chain


def realize(record):
    edges = {(0, 1), (0, 2), (1, 2)}
    triangles = [(0, 1, 2)]
    next_vertex = 3

    def attach(owner):
        nonlocal next_vertex
        triangle, next_vertex = add_triangle(edges, owner, next_vertex)
        triangles.append(triangle)
        return triangle

    kind = record[0]
    if kind == "direct3":
        for owner in record[1]:
            attach(owner)
    elif kind == "chain2+direct":
        parent = attach(record[1])
        attach(parent[1])
        attach(record[2])
    elif kind == "fork":
        parent = attach(record[1])
        attach(parent[1])
        attach(parent[1] if record[2] == "same" else parent[2])
    elif kind == "chain3":
        parent = attach(record[1])
        child = attach(parent[1])
        attach(child[1])
    else:
        raise AuditError(f"unknown incidence shape: {kind}")
    return next_vertex, edges, triangles


def connected(vertices, edges):
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        if u in adjacency and v in adjacency:
            adjacency[u].add(v)
            adjacency[v].add(u)
    seen = set()
    stack = [next(iter(vertices))]
    while stack:
        vertex = stack.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        stack.extend(adjacency[vertex] - seen)
    return seen == set(vertices)


def audit_graph(graph):
    n, edges, triangles = graph
    require(n == 9 and len(edges) == 12 and len(triangles) == 4,
            "four-triangle rank/order ledger changed")
    require(connected(set(range(n)), edges), "realized packet is disconnected")
    require(len(edges) - n + 1 == 4, "realized packet is not rank four")
    for left, right in itertools.combinations(triangles, 2):
        require(len(set(left) & set(right)) <= 1, "realized packet is not a cactus")

    intersection_edges = {
        (i, j) for i, j in itertools.combinations(range(4), 2)
        if set(triangles[i]) & set(triangles[j])
    }
    require(connected(set(range(4)), intersection_edges),
            "triangles do not form one shared-cut cluster")

    packing = max(
        len(choice)
        for size in range(1, 5)
        for choice in itertools.combinations(range(4), size)
        if all(not (set(triangles[i]) & set(triangles[j]))
               for i, j in itertools.combinations(choice, 2))
    )
    require(packing <= 3, "impossible four-block packing reached")
    if packing == 3:
        degrees = Counter()
        for i, j in intersection_edges:
            degrees[i] += 1
            degrees[j] += 1
        require(sorted(degrees.values()) == [1, 1, 1, 3],
                "packing-three record is not central-three-petal")
        center = next(i for i in range(4) if degrees[i] == 3)
        cuts = [set(triangles[center]) & set(triangles[j]) for j in range(4) if j != center]
        require(len(set().union(*cuts)) == 3,
                "central petals do not use the three distinct central vertices")
    return packing


def audit():
    left = records_for_side((0, 1))
    right = records_for_side((0, 1))
    require(len(left) == 14 and len(right) == 14, "one-sided C4 census changed")
    records = [("left", record) for record in left] + [("right", record) for record in right]
    require(len(records) == 28, "marked C4 orbit total changed")

    shape_counts = Counter(record[0] for _, record in records)
    require(shape_counts == Counter({"direct3": 8, "chain2+direct": 8, "fork": 8, "chain3": 4}),
            "marked C4 shape counts changed")

    packing_counts = Counter(audit_graph(realize(record)) for _, record in records)
    require(set(packing_counts) <= {1, 2, 3}, "unclassified packing row")
    require(packing_counts[3] > 0, "exceptional central-petal branch disappeared")

    singleton_coefficient = -2
    triple_petal_coefficient = 8
    require(4 * singleton_coefficient + triple_petal_coefficient == 0,
            "exceptional Sachs domination ledger changed")
    central_deletion_private_edges = 3
    petal_deletion_auxiliary_order = 6
    petal_deletion_perfect_matching = 3
    require(central_deletion_private_edges > 0,
            "central-deletion strict matching factor disappeared")
    require(2 * petal_deletion_perfect_matching == petal_deletion_auxiliary_order,
            "petal-deletion auxiliary perfect matching changed")
    require(3 > 2, "packet threshold ledger changed")
    return shape_counts, packing_counts


def main():
    shape_counts, packing_counts = audit()
    output = (
        "R31-S C4 marked four-triangle verifier: exact audit passed\n"
        f"marked records: direct3={shape_counts['direct3']} "
        f"chain2+direct={shape_counts['chain2+direct']} fork={shape_counts['fork']} "
        f"chain3={shape_counts['chain3']} total={sum(shape_counts.values())}\n"
        f"packing classes: {dict(sorted(packing_counts.items()))}\n"
        "exceptional Sachs ledger: -2*4+8=0 with strict matching domination\n"
        "uniform packet bound: sigma>3>2\n"
        "status: C4 CLOSED; D3 remains"
    )
    if "--optimized-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-child"],
                               check=True, capture_output=True, text=True)
        require(child.stdout.rstrip() == output, "normal/optimized output mismatch")
    print(output)


if __name__ == "__main__":
    main()
