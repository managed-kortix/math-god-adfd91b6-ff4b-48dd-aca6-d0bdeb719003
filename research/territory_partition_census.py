#!/usr/bin/env python3
"""Exhaustively test cycle-packing territory partitions on graph6 input."""

import argparse
import itertools
import subprocess
import sys

import networkx as nx


def is_cycle_support(graph, vertices):
    vertices = tuple(vertices)
    if len(vertices) < 3:
        return False
    start = vertices[0]
    rest = vertices[1:]
    for order in itertools.permutations(rest):
        if order[0] > order[-1]:
            continue
        tour = (start,) + order
        if all(graph.has_edge(tour[i], tour[(i + 1) % len(tour)]) for i in range(len(tour))):
            return True
    return False


def cycle_supports(graph):
    nodes = tuple(graph.nodes())
    return [
        frozenset(vertices)
        for size in range(3, len(nodes) + 1)
        for vertices in itertools.combinations(nodes, size)
        if is_cycle_support(graph, vertices)
    ]


def maximum_packings(supports):
    best = []
    maximum = 0

    def visit(start, used, packing):
        nonlocal maximum, best
        if len(packing) > maximum:
            maximum = len(packing)
            best = [tuple(packing)]
        elif len(packing) == maximum:
            best.append(tuple(packing))
        for index in range(start, len(supports)):
            support = supports[index]
            if used.isdisjoint(support):
                visit(index + 1, used | support, packing + [support])

    visit(0, frozenset(), [])
    return maximum, best


def distances(graph, sources):
    result = []
    for source in sources:
        distance = {}
        queue = list(source)
        for vertex in queue:
            distance[vertex] = 0
        for vertex in queue:
            for neighbor in graph[vertex]:
                if neighbor not in distance:
                    distance[neighbor] = distance[vertex] + 1
                    queue.append(neighbor)
        result.append(distance)
    return result


def nearest_options(graph, sources):
    source_distances = distances(graph, sources)
    options = {}
    for vertex in graph:
        values = [distance[vertex] for distance in source_distances]
        minimum = min(values)
        options[vertex] = tuple(index for index, value in enumerate(values) if value == minimum)
    return options


def territories(graph, sources, assignment):
    parts = [set() for _ in sources]
    for vertex, index in assignment.items():
        parts[index].add(vertex)
    return parts


def valid_territories(graph, sources, parts, supports):
    for index, part in enumerate(parts):
        if not sources[index].issubset(part):
            return False
        if any(sources[other] & part for other in range(len(sources)) if other != index):
            return False
        if not nx.is_connected(graph.subgraph(part)):
            return False
        contained = [support for support in supports if support.issubset(part)]
        if any(a.isdisjoint(b) for pos, a in enumerate(contained) for b in contained[pos + 1 :]):
            return False
    return True


def graph_record(graph):
    return nx.to_graph6_bytes(graph, header=False).decode().strip()


def run(order):
    process = subprocess.Popen(
        ["nauty-geng", "-cq", str(order)], stdout=subprocess.PIPE, text=True
    )
    graph_count = 0
    packing_count = 0
    priority_failures = []
    arbitrary_failures = []

    for line in process.stdout:
        graph = nx.from_graph6_bytes(line.strip().encode())
        graph_count += 1
        supports = cycle_supports(graph)
        packing_number, packings = maximum_packings(supports)
        if packing_number == 0:
            continue
        for sources in packings:
            packing_count += 1
            options = nearest_options(graph, sources)
            priority_assignment = {vertex: choices[0] for vertex, choices in options.items()}
            priority_parts = territories(graph, sources, priority_assignment)
            if not valid_territories(graph, sources, priority_parts, supports):
                priority_failures.append((graph_record(graph), sources, priority_assignment))

            if not arbitrary_failures:
                vertices = tuple(graph.nodes())
                for choices in itertools.product(*(options[vertex] for vertex in vertices)):
                    assignment = dict(zip(vertices, choices))
                    parts = territories(graph, sources, assignment)
                    if not valid_territories(graph, sources, parts, supports):
                        arbitrary_failures.append((graph_record(graph), sources, assignment))
                        break

    return {
        "order": order,
        "graphs": graph_count,
        "maximum_packings": packing_count,
        "priority_failures": priority_failures,
        "arbitrary_failure": arbitrary_failures[:1],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=8)
    args = parser.parse_args()
    for order in range(1, args.max_order + 1):
        result = run(order)
        print(result)
        if result["priority_failures"]:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
