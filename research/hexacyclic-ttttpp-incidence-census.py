#!/usr/bin/env python3
"""Exact colored incidence-tree census for the fully shared TTTTPP residual.

The acceptance test deliberately uses only packet estimates already recorded in
the lower-rank and pentacyclic ledgers.  In particular, a qualitative positive
tetracyclic or pentacyclic packet is never charged against a negative pentagon.
"""

from collections import Counter
from dataclasses import dataclass
from decimal import Decimal, getcontext
from itertools import combinations, combinations_with_replacement, permutations

TRIANGLES = range(4)
PENTAGONS = range(4, 6)
CYCLE_COUNT = 6

getcontext().prec = 40
SQRT5 = Decimal(5).sqrt()
SQRT13 = Decimal(13).sqrt()
DELTA = SQRT5 - 2


@dataclass(frozen=True)
class Bound:
    value: Decimal
    strict: bool
    source: str


def is_tree(cut_neighborhoods):
    order = CYCLE_COUNT + len(cut_neighborhoods)
    parent = list(range(order))

    def root(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for cut, neighborhood in enumerate(cut_neighborhoods, CYCLE_COUNT):
        for cycle in neighborhood:
            left, right = root(cycle), root(cut)
            if left == right:
                return False
            parent[left] = right
    return True


def canonical(cut_neighborhoods):
    answer = None
    for triangles in permutations(TRIANGLES):
        for pentagons in permutations(PENTAGONS):
            image = triangles + pentagons
            neighborhoods = sorted(
                tuple(sorted(image[cycle] for cycle in neighborhood))
                for neighborhood in cut_neighborhoods
            )
            candidate = tuple(
                (cycle, CYCLE_COUNT + cut)
                for cut, neighborhood in enumerate(neighborhoods)
                for cycle in neighborhood
            )
            if answer is None or candidate < answer:
                answer = candidate
    return answer


def neighborhoods_from_edges(edges, cut_count):
    answer = [[] for _ in range(cut_count)]
    for cycle, cut in edges:
        answer[cut - CYCLE_COUNT].append(cycle)
    return tuple(tuple(neighborhood) for neighborhood in answer)


def degree_patterns(total, length, minimum=1):
    if length == 0:
        if total == 0:
            yield ()
        return
    for first in range(minimum, total // length + 1):
        for rest in degree_patterns(total - first, length - 1, first):
            yield (first,) + rest


def candidate_neighborhoods(cut_count):
    by_excess = {
        excess: tuple(combinations(range(CYCLE_COUNT), excess + 1))
        for excess in range(1, 6)
    }
    for pattern in degree_patterns(5, cut_count):
        groups = []
        for excess in sorted(set(pattern)):
            groups.append(
                tuple(
                    combinations_with_replacement(
                        by_excess[excess], pattern.count(excess)
                    )
                )
            )

        def combine(group_index, chosen):
            if group_index == len(groups):
                yield tuple(sorted(chosen))
                return
            for group_choice in groups[group_index]:
                yield from combine(group_index + 1, chosen + group_choice)

        yield from combine(0, ())


def components_after_cycle_split(edges, cut_count, sacrificed):
    adjacency = [[] for _ in range(CYCLE_COUNT + cut_count)]
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)

    components = []
    seen = {sacrificed}
    for start in adjacency[sacrificed]:
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        cycles = set()
        vertices = set()
        while stack:
            vertex = stack.pop()
            vertices.add(vertex)
            if vertex < CYCLE_COUNT:
                cycles.add(vertex)
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        internal_cuts = tuple(
            cut
            for cut in vertices
            if cut >= CYCLE_COUNT
            and sum(cycle in cycles for cycle in adjacency[cut]) >= 2
        )
        components.append((tuple(sorted(cycles)), internal_cuts, adjacency))
    return tuple(components)


def packet_bound(component):
    cycles, internal_cuts, adjacency = component
    triangles = sum(cycle < 4 for cycle in cycles)
    pentagons = len(cycles) - triangles
    rank = len(cycles)

    if rank == 1:
        if triangles:
            return Bound(Decimal(0), True, "T > 0")
        return Bound(-DELTA, False, "P >= -delta")
    if (triangles, pentagons) == (2, 0):
        return Bound(Decimal(1), True, "TT > 1")
    if (triangles, pentagons) == (1, 1):
        return Bound(Decimal(1) - DELTA, True, "TP > 1-delta")
    if (triangles, pentagons) == (0, 2):
        value = Decimal(1) - Decimal(4) / (Decimal(3) * SQRT13)
        return Bound(value, False, "shared PP >= 1-4/(3sqrt(13))")
    if (triangles, pentagons) == (3, 0):
        return Bound(Decimal(2), True, "shared TTT > 2")
    if (triangles, pentagons) == (1, 2):
        return Bound(Decimal(6) - 2 * SQRT5, True, "shared TPP > 6-2sqrt(5)")
    if (triangles, pentagons) == (2, 1):
        triangle_set = {cycle for cycle in cycles if cycle < 4}
        share_cut = any(triangle_set <= set(adjacency[cut]) for cut in internal_cuts)
        if share_cut:
            return Bound(Decimal(2) - DELTA, True, "shared-triangle TTP > 2-delta")
        return Bound(Decimal(0), False, "generic tricyclic >= 0")
    if rank == 3:
        return Bound(Decimal(0), False, "generic tricyclic >= 0")
    if (triangles, pentagons) == (4, 0):
        return Bound(Decimal(3), True, "shared TTTT > 3")
    if (triangles, pentagons) == (3, 1):
        triangle_set = {cycle for cycle in cycles if cycle < 4}
        share_pair = any(
            len(triangle_set & set(adjacency[cut])) >= 2 for cut in internal_cuts
        )
        if share_pair:
            return Bound(Decimal(1), True, "fully shared TTTP with a shared T pair > 1")
    if rank == 4:
        return Bound(Decimal(0), True, "generic tetracyclic > 0")
    if rank == 5:
        return Bound(Decimal(0), True, "generic pentacyclic > 0")
    raise AssertionError((triangles, pentagons))


def split_certificate(edges, cut_count, cycle):
    components = components_after_cycle_split(edges, cut_count, cycle)
    if len(components) < 2:
        return None
    bounds = tuple(packet_bound(component) for component in components)
    total = sum((bound.value for bound in bounds), Decimal(0))
    if total > 0 or (total == 0 and any(bound.strict for bound in bounds)):
        branches = tuple(
            sorted(
                (sum(c < 4 for c in component[0]), sum(c >= 4 for c in component[0]))
                for component in components
            )
        )
        return branches, bounds
    return None


def branch_multiset(components):
    return tuple(
        sorted(
            (sum(c < 4 for c in component[0]), sum(c >= 4 for c in component[0]))
            for component in components
        )
    )


def classify_exception(edges, cut_count):
    neighborhoods = neighborhoods_from_edges(edges, cut_count)
    cycle_degrees = Counter(cycle for neighborhood in neighborhoods for cycle in neighborhood)
    cut_degrees = sorted((len(n) for n in neighborhoods), reverse=True)
    if cut_count == 1:
        return "six-cycle bouquet"
    if any(
        len(neighborhood) == 2
        and sum(cycle < 4 for cycle in neighborhood) == 1
        and sum(cycle >= 4 for cycle in neighborhood) == 1
        for neighborhood in neighborhoods
    ) and sorted(cycle_degrees[cycle] for cycle in PENTAGONS) == [1, 1]:
        return "two pentagon leaves on a triangle core"
    if 5 in cycle_degrees.values():
        hub = next(cycle for cycle, degree in cycle_degrees.items() if degree == 5)
        return "saturated pentagon hub" if hub >= 4 else "multiway triangle hub"
    if cycle_degrees[4] > 1 and cycle_degrees[5] > 1:
        return "pentagon double hub"
    if cut_degrees[0] >= 4:
        return "multiway-cut core"
    return "hybrid core"


def census():
    trees = set()
    for cut_count in range(1, 6):
        for neighborhoods in candidate_neighborhoods(cut_count):
            cycle_degrees = Counter(cycle for n in neighborhoods for cycle in n)
            if len(cycle_degrees) != CYCLE_COUNT:
                continue
            if max(cycle_degrees[cycle] for cycle in TRIANGLES) > 3:
                continue
            if max(cycle_degrees[cycle] for cycle in PENTAGONS) > 5:
                continue
            if not is_tree(neighborhoods):
                continue
            trees.add((cut_count, canonical(neighborhoods)))

    resolved = Counter()
    witnesses = {}
    unresolved = []
    classes = Counter()
    split_profiles = Counter()
    for cut_count, edges in sorted(trees):
        certificate = None
        for cycle in range(CYCLE_COUNT):
            components = components_after_cycle_split(edges, cut_count, cycle)
            safe = split_certificate(edges, cut_count, cycle)
            split_profiles[
                ("T" if cycle < 4 else "P", branch_multiset(components), safe is not None)
            ] += 1
            if certificate is None and safe is not None:
                certificate = safe
                witnesses[(cut_count, edges)] = (cycle, certificate[0])
                resolved[cut_count] += 1
        if certificate is None:
            label = classify_exception(edges, cut_count)
            unresolved.append((cut_count, edges, label))
            classes[label] += 1

    totals = Counter(cut_count for cut_count, _ in trees)
    expected_totals = Counter({1: 1, 2: 9, 3: 40, 4: 62, 5: 38})
    expected_resolved = Counter({2: 9, 3: 40, 4: 62, 5: 37})
    expected_unresolved = [
        (
            1,
            ((0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6)),
            "six-cycle bouquet",
        ),
        (
            5,
            (
                (0, 6),
                (4, 6),
                (1, 7),
                (4, 7),
                (2, 8),
                (4, 8),
                (3, 9),
                (4, 9),
                (4, 10),
                (5, 10),
            ),
            "saturated pentagon hub",
        ),
    ]
    assert totals == expected_totals
    assert resolved == expected_resolved
    assert unresolved == expected_unresolved
    assert sum(totals.values()) == 150
    assert sum(resolved.values()) == 148
    expected_profiles = Counter(
        {
            ("P", ((0, 1), (1, 0), (1, 0), (1, 0), (1, 0)), False): 1,
            ("P", ((0, 1), (1, 0), (1, 0), (2, 0)), True): 2,
            ("P", ((0, 1), (1, 0), (3, 0)), True): 5,
            ("P", ((0, 1), (2, 0), (2, 0)), True): 3,
            ("P", ((0, 1), (4, 0)), True): 13,
            ("P", ((1, 0), (1, 0), (1, 0), (1, 1)), True): 3,
            ("P", ((1, 0), (1, 0), (2, 1)), True): 12,
            ("P", ((1, 0), (1, 1), (2, 0)), True): 6,
            ("P", ((1, 0), (3, 1)), True): 44,
            ("P", ((1, 1), (3, 0)), True): 15,
            ("P", ((2, 0), (2, 1)), True): 24,
            ("P", ((4, 1),), False): 172,
            ("T", ((0, 1), (0, 1), (3, 0)), True): 5,
            ("T", ((0, 1), (1, 0), (2, 1)), False): 3,
            ("T", ((0, 1), (1, 0), (2, 1)), True): 9,
            ("T", ((0, 1), (1, 1), (2, 0)), True): 6,
            ("T", ((0, 1), (3, 1)), False): 3,
            ("T", ((0, 1), (3, 1)), True): 41,
            ("T", ((0, 2), (1, 0), (2, 0)), True): 4,
            ("T", ((0, 2), (3, 0)), True): 10,
            ("T", ((1, 0), (1, 0), (1, 2)), True): 11,
            ("T", ((1, 0), (1, 1), (1, 1)), True): 6,
            ("T", ((1, 0), (2, 2)), True): 60,
            ("T", ((1, 1), (2, 1)), True): 36,
            ("T", ((1, 2), (2, 0)), True): 22,
            ("T", ((3, 2),), False): 384,
        }
    )
    assert split_profiles == expected_profiles
    assert sum(split_profiles.values()) == 6 * sum(totals.values())
    return totals, resolved, unresolved, classes, split_profiles


if __name__ == "__main__":
    totals, resolved, unresolved, classes, split_profiles = census()
    print("colored trees by cut count:", dict(sorted(totals.items())))
    print("SAFE one-cycle packet resolutions:", dict(sorted(resolved.items())))
    print("split branch profiles (cycle, branches, SAFE):")
    for profile, count in sorted(split_profiles.items()):
        print(f"  {profile}: {count}")
    print("unresolved by proposed structural class:", dict(sorted(classes.items())))
    print("canonical exceptions:")
    for cut_count, edges, label in unresolved:
        print(f"  c={cut_count} [{label}]: {edges}")
