#!/usr/bin/env python3
"""Exact incidence-and-entry census for E2 in the disconnected TTTTPP audit."""

from collections import Counter
from itertools import combinations, permutations

TRIANGLES = range(3)
PENTAGON = 3
CYCLE_COUNT = 4
PENTAGON_LENGTH = 5


def is_tree(edges, order):
    parent = list(range(order))

    def root(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges:
        left, right = root(left), root(right)
        if left == right:
            return False
        parent[left] = right
    return True


def canonical_tree(edges, cut_count):
    answer = None
    for triangles in permutations(TRIANGLES):
        for cuts in permutations(range(cut_count)):
            image = triangles + (PENTAGON,) + tuple(CYCLE_COUNT + cut for cut in cuts)
            candidate = tuple(
                sorted(tuple(sorted((image[left], image[right]))) for left, right in edges)
            )
            if answer is None or candidate < answer:
                answer = candidate
    return answer


def incidence_trees():
    trees = set()
    for cut_count in range(1, 4):
        possible_edges = [
            (cycle, CYCLE_COUNT + cut)
            for cycle in range(CYCLE_COUNT)
            for cut in range(cut_count)
        ]
        for edges in combinations(possible_edges, cut_count + CYCLE_COUNT - 1):
            cycle_degrees = Counter(left for left, _ in edges)
            cut_degrees = Counter(right for _, right in edges)
            if len(cycle_degrees) != CYCLE_COUNT or len(cut_degrees) != cut_count:
                continue
            if min(cut_degrees.values()) < 2:
                continue
            if max(cycle_degrees[triangle] for triangle in TRIANGLES) > 3:
                continue
            if cycle_degrees[PENTAGON] > 5:
                continue
            if not is_tree(edges, CYCLE_COUNT + cut_count):
                continue
            trees.add((cut_count, canonical_tree(edges, cut_count)))
    return trees


def has_intersecting_triangles(edges):
    cut_to_triangles = Counter()
    neighborhoods = {}
    for cycle, cut in edges:
        neighborhoods.setdefault(cut, set()).add(cycle)
    return any(len(neighborhood & set(TRIANGLES)) >= 2 for neighborhood in neighborhoods.values())


def is_three_petal_hub(edges):
    neighborhoods = {}
    for cycle, cut in edges:
        neighborhoods.setdefault(cut, set()).add(cycle)
    return len(neighborhoods) == 3 and {
        frozenset(neighborhood) for neighborhood in neighborhoods.values()
    } == {frozenset((triangle, PENTAGON)) for triangle in TRIANGLES}


def canonical_entry_configuration(petal_marks, triangle_entry, pentagon_entry):
    candidates = []
    for reflection in (1, -1):
        for shift in range(PENTAGON_LENGTH):
            transform = lambda vertex: (reflection * vertex + shift) % PENTAGON_LENGTH
            candidates.append(
                (
                    tuple(sorted(transform(mark) for mark in petal_marks)),
                    transform(triangle_entry),
                    transform(pentagon_entry),
                )
            )
    return min(candidates)


def cyclic_intervals():
    intervals = set()
    for start in range(PENTAGON_LENGTH):
        for length in range(1, PENTAGON_LENGTH):
            intervals.add(
                frozenset((start + offset) % PENTAGON_LENGTH for offset in range(length))
            )
    return sorted(intervals, key=lambda interval: (len(interval), tuple(sorted(interval))))


def packet_type(petal_marks, triangle_entry, pentagon_entry, interval):
    """Return the two packet types when interval owns the external pentagon."""
    if pentagon_entry not in interval:
        return None
    triangles_with_pentagon = sum(mark in interval for mark in petal_marks)
    triangles_with_pentagon += triangle_entry in interval
    return {
        1: "TP + TTT",
        2: "TTP + TT",
    }.get(triangles_with_pentagon)


def entry_orbits():
    configurations = set()
    for petal_marks in combinations(range(PENTAGON_LENGTH), 3):
        for triangle_entry in range(PENTAGON_LENGTH):
            for pentagon_entry in range(PENTAGON_LENGTH):
                configurations.add(
                    canonical_entry_configuration(
                        petal_marks, triangle_entry, pentagon_entry
                    )
                )

    certificates = {}
    for configuration in sorted(configurations):
        petal_marks, triangle_entry, pentagon_entry = configuration
        for interval in cyclic_intervals():
            packet = packet_type(
                petal_marks, triangle_entry, pentagon_entry, interval
            )
            if packet is not None:
                certificates[configuration] = (tuple(sorted(interval)), packet)
                break
        assert configuration in certificates

        interval, _ = certificates[configuration]
        interval = frozenset(interval)
        complement = frozenset(range(PENTAGON_LENGTH)) - interval
        assert interval and complement
        assert interval in cyclic_intervals() and complement in cyclic_intervals()
        assert pentagon_entry in interval
    return configurations, certificates


def census():
    trees = incidence_trees()
    totals = Counter(cut_count for cut_count, _ in trees)
    intersecting = {
        tree for tree in trees if has_intersecting_triangles(tree[1])
    }
    disjoint = trees - intersecting
    assert totals == {1: 1, 2: 3, 3: 4}
    assert len(intersecting) == 7
    assert len(disjoint) == 1
    assert all(is_three_petal_hub(edges) for _, edges in disjoint)

    configurations, certificates = entry_orbits()
    packet_counts = Counter(packet for _, packet in certificates.values())
    assert len(configurations) == 26
    assert packet_counts == {
        "TP + TTT": 20,
        "TTP + TT": 6,
    }
    return totals, intersecting, disjoint, configurations, certificates, packet_counts


if __name__ == "__main__":
    totals, intersecting, disjoint, configurations, certificates, packet_counts = census()
    print("colored TTTP incidence trees by cut count:", dict(sorted(totals.items())))
    print("canonical incidence trees:")
    for cut_count, edges in sorted(intersecting | disjoint):
        classification = "intersecting T pair" if (cut_count, edges) in intersecting else "hub"
        print(f"  c={cut_count} [{classification}]: {edges}")
    print("ordered labelled-entry orbits on the hub:", len(configurations))
    print("certificate types:", dict(sorted(packet_counts.items())))
    for configuration in sorted(configurations):
        interval, packet = certificates[configuration]
        print(f"  {configuration}: interval={interval}, packets={packet}")
