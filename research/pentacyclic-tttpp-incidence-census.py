#!/usr/bin/env python3
"""Exact colored incidence-tree census for the fully shared TTTPP residual."""

from collections import Counter
from itertools import combinations, permutations

TRIANGLES = range(3)
PENTAGONS = range(3, 5)


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


def canonical(edges, cut_count):
    answer = None
    for triangles in permutations(TRIANGLES):
        for pentagons in permutations(PENTAGONS):
            for cuts in permutations(range(cut_count)):
                image = triangles + pentagons + tuple(5 + cut for cut in cuts)
                candidate = tuple(
                    sorted(tuple(sorted((image[left], image[right]))) for left, right in edges)
                )
                if answer is None or candidate < answer:
                    answer = candidate
    return answer


def components_after_cycle_split(edges, cut_count, cycle):
    adjacency = [[] for _ in range(5 + cut_count)]
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)

    seen = {cycle}
    components = []
    for start in adjacency[cycle]:
        stack = [start]
        seen.add(start)
        triangles = pentagons = 0
        while stack:
            vertex = stack.pop()
            triangles += vertex < 3
            pentagons += 3 <= vertex < 5
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        components.append((triangles, pentagons))
    return tuple(sorted(components))


GOOD_AFTER_TRIANGLE_SPLIT = {
    ((0, 2), (2, 0)),
    ((1, 0), (1, 2)),
    ((1, 1), (1, 1)),
    ((0, 1), (0, 1), (2, 0)),
    ((0, 1), (1, 0), (1, 1)),
    ((0, 2), (1, 0), (1, 0)),
}

GOOD_AFTER_PENTAGON_SPLIT = {
    ((0, 1), (3, 0)),
    ((1, 0), (2, 1)),
    ((1, 1), (2, 0)),
    ((0, 1), (1, 0), (2, 0)),
    ((1, 0), (1, 0), (1, 1)),
}


def census():
    trees = set()
    for cut_count in range(1, 5):
        possible_edges = [
            (cycle, 5 + cut)
            for cycle in range(5)
            for cut in range(cut_count)
        ]
        for edges in combinations(possible_edges, cut_count + 4):
            cycle_degrees = [0] * 5
            cut_degrees = [0] * cut_count
            for cycle, cut in edges:
                cycle_degrees[cycle] += 1
                cut_degrees[cut - 5] += 1
            if min(cycle_degrees) < 1 or min(cut_degrees) < 2:
                continue
            if max(cycle_degrees[:3]) > 3 or max(cycle_degrees[3:]) > 5:
                continue
            if not is_tree(edges, 5 + cut_count):
                continue
            trees.add((cut_count, canonical(edges, cut_count)))

    unresolved = []
    resolved = Counter()
    for cut_count, edges in sorted(trees):
        certificate = None
        for cycle in range(5):
            components = components_after_cycle_split(edges, cut_count, cycle)
            good = (
                components in GOOD_AFTER_TRIANGLE_SPLIT
                if cycle < 3
                else components in GOOD_AFTER_PENTAGON_SPLIT
            )
            if len(components) >= 2 and good:
                certificate = cycle, components
                break
        if certificate is None:
            unresolved.append((cut_count, edges))
        else:
            resolved[cut_count] += 1

    assert Counter(cut_count for cut_count, _ in trees) == {1: 1, 2: 7, 3: 18, 4: 14}
    assert resolved == {2: 6, 3: 17, 4: 13}
    expected_unresolved = [
        (1, ((0, 5), (1, 5), (2, 5), (3, 5), (4, 5))),
        (2, ((0, 5), (0, 6), (1, 5), (2, 5), (3, 5), (4, 6))),
        (3, ((0, 5), (0, 6), (1, 5), (1, 7), (2, 5), (3, 6), (4, 7))),
        (
            4,
            (
                (0, 5),
                (1, 6),
                (2, 7),
                (3, 5),
                (3, 6),
                (3, 7),
                (3, 8),
                (4, 8),
            ),
        ),
    ]
    assert unresolved == expected_unresolved
    return trees, unresolved


if __name__ == "__main__":
    all_trees, exceptions = census()
    print("colored trees by cut count:", dict(sorted(Counter(c for c, _ in all_trees).items())))
    print("one-cycle split exceptions:")
    for cut_count, edges in exceptions:
        print(f"  c={cut_count}: {edges}")
