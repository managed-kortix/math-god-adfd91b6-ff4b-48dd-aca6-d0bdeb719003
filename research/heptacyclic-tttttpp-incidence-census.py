#!/usr/bin/env python3
"""Exact fully shared T^5PP incidence census and conservative SAFE ledger.

This is a finite proof-search object, not a theorem checker.  It quotients by
S_5 x S_2 x S_c and accepts only ordinary one-cycle interval splits whose
branch sum follows from established lower-rank packet bounds.
"""

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations


TRIANGLES = tuple(range(5))
PENTAGONS = tuple(range(5, 7))
CYCLE_COUNT = 7
FIRST_CUT = CYCLE_COUNT


@dataclass(frozen=True)
class Bound:
    value: Fraction
    strict: bool
    source: str


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
        for excess in range(1, CYCLE_COUNT)
    }
    for pattern in degree_patterns(CYCLE_COUNT - 1, cut_count):
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


def edges_from_neighborhoods(neighborhoods):
    return tuple(
        (cycle, FIRST_CUT + cut)
        for cut, neighborhood in enumerate(neighborhoods)
        for cycle in neighborhood
    )


def adjacency(edges, cut_count):
    answer = [[] for _ in range(CYCLE_COUNT + cut_count)]
    for left, right in edges:
        answer[left].append(right)
        answer[right].append(left)
    return answer


def is_tree(neighborhoods):
    order = CYCLE_COUNT + len(neighborhoods)
    parent = list(range(order))

    def root(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges_from_neighborhoods(neighborhoods):
        left_root, right_root = root(left), root(right)
        if left_root == right_root:
            return False
        parent[left_root] = right_root
    return True


def color(vertex):
    if vertex in TRIANGLES:
        return "T"
    if vertex in PENTAGONS:
        return "P"
    return "X"


def tree_centers(adj):
    degree = [len(row) for row in adj]
    leaves = [vertex for vertex, value in enumerate(degree) if value <= 1]
    remaining = len(adj)
    while remaining > 2:
        remaining -= len(leaves)
        new_leaves = []
        for leaf in leaves:
            for neighbor in adj[leaf]:
                degree[neighbor] -= 1
                if degree[neighbor] == 1:
                    new_leaves.append(neighbor)
        leaves = new_leaves
    return leaves


def rooted_code(adj, vertex, parent):
    children = sorted(
        rooted_code(adj, neighbor, vertex)
        for neighbor in adj[vertex]
        if neighbor != parent
    )
    return color(vertex) + "(" + "".join(children) + ")"


def canonical_signature(edges, cut_count):
    adj = adjacency(edges, cut_count)
    return min(rooted_code(adj, center, -1) for center in tree_centers(adj))


def canonical_edges(edges, cut_count):
    neighborhoods = [[] for _ in range(cut_count)]
    for cycle, cut in edges:
        neighborhoods[cut - FIRST_CUT].append(cycle)
    answer = None
    for triangles in permutations(TRIANGLES):
        for pentagons in permutations(PENTAGONS):
            image = triangles + pentagons
            transformed = sorted(
                tuple(sorted(image[cycle] for cycle in neighborhood))
                for neighborhood in neighborhoods
            )
            candidate = tuple(
                (cycle, FIRST_CUT + cut)
                for cut, neighborhood in enumerate(transformed)
                for cycle in neighborhood
            )
            if answer is None or candidate < answer:
                answer = candidate
    return answer


def enumerate_trees():
    trees = {}
    for cut_count in range(1, CYCLE_COUNT):
        classes = {}
        for neighborhoods in candidate_neighborhoods(cut_count):
            cycle_degrees = Counter(
                cycle for neighborhood in neighborhoods for cycle in neighborhood
            )
            if len(cycle_degrees) != CYCLE_COUNT:
                continue
            if max(cycle_degrees[cycle] for cycle in TRIANGLES) > 3:
                continue
            if max(cycle_degrees[cycle] for cycle in PENTAGONS) > 5:
                continue
            if not is_tree(neighborhoods):
                continue
            edges = edges_from_neighborhoods(neighborhoods)
            classes.setdefault(canonical_signature(edges, cut_count), edges)
        trees[cut_count] = classes
    return trees


def components_after_cycle_split(edges, cut_count, sacrificed):
    adj = adjacency(edges, cut_count)
    components = []
    seen = {sacrificed}
    for start in adj[sacrificed]:
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        vertices = set()
        cycles = set()
        while stack:
            vertex = stack.pop()
            vertices.add(vertex)
            if vertex < CYCLE_COUNT:
                cycles.add(vertex)
            for neighbor in adj[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        internal_cuts = tuple(
            cut
            for cut in vertices
            if cut >= FIRST_CUT
            and sum(cycle in cycles for cycle in adj[cut]) >= 2
        )
        components.append((tuple(sorted(cycles)), internal_cuts, adj))
    return tuple(components)


def packet_bound(component):
    cycles, internal_cuts, adj = component
    triangle_set = {cycle for cycle in cycles if cycle in TRIANGLES}
    triangles = len(triangle_set)
    pentagons = len(cycles) - triangles
    rank = len(cycles)

    if rank == 1:
        if triangles:
            return Bound(Fraction(0), True, "T > 0")
        return Bound(Fraction(-1, 4), True, "P > -1/4")
    if (triangles, pentagons) == (2, 0):
        return Bound(Fraction(1), True, "TT > 1")
    if (triangles, pentagons) == (1, 1):
        return Bound(Fraction(3, 4), True, "TP > 3/4")
    if (triangles, pentagons) == (0, 2):
        return Bound(Fraction(0), True, "shared PP > 0")
    if (triangles, pentagons) == (3, 0):
        return Bound(Fraction(2), True, "shared TTT > 2")
    if (triangles, pentagons) == (2, 1):
        share_cut = any(triangle_set <= set(adj[cut]) for cut in internal_cuts)
        if share_cut:
            return Bound(Fraction(7, 4), True, "shared-triangle TTP > 7/4")
    if (triangles, pentagons) == (1, 2):
        return Bound(Fraction(3, 2), True, "shared TPP > 3/2")
    if rank == 3:
        return Bound(Fraction(0), False, "generic tricyclic >= 0")
    if (triangles, pentagons) == (4, 0):
        return Bound(Fraction(3), True, "shared TTTT > 3")
    if (triangles, pentagons) == (3, 1):
        share_pair = any(
            len(triangle_set & set(adj[cut])) >= 2 for cut in internal_cuts
        )
        if share_pair:
            return Bound(Fraction(1), True, "shared-pair TTTP > 1")
    if rank == 4:
        return Bound(Fraction(0), True, "generic tetracyclic > 0")
    if (triangles, pentagons) == (5, 0):
        return Bound(Fraction(2), True, "shared TTTTT > 2")
    if rank == 5:
        return Bound(Fraction(0), True, "generic pentacyclic > 0")
    if rank == 6:
        return Bound(Fraction(0), True, "generic hexacyclic > 0")
    raise AssertionError((triangles, pentagons))


def branch_multiset(components):
    return tuple(
        sorted(
            (
                sum(cycle in TRIANGLES for cycle in component[0]),
                sum(cycle in PENTAGONS for cycle in component[0]),
            )
            for component in components
        )
    )


def split_certificate(edges, cut_count, cycle):
    components = components_after_cycle_split(edges, cut_count, cycle)
    if len(components) < 2:
        return None
    bounds = tuple(packet_bound(component) for component in components)
    total = sum((bound.value for bound in bounds), Fraction(0))
    if total > 0 or (total == 0 and any(bound.strict for bound in bounds)):
        return branch_multiset(components), bounds, total
    return None


def structural_class(edges, cut_count):
    adj = adjacency(edges, cut_count)
    cycle_degrees = [len(adj[cycle]) for cycle in range(CYCLE_COUNT)]
    cut_degrees = [len(adj[cut]) for cut in range(FIRST_CUT, FIRST_CUT + cut_count)]
    cycle_leaves = {cycle for cycle in range(CYCLE_COUNT) if cycle_degrees[cycle] == 1}
    if cut_count == 1:
        return "seven-cycle bouquet"
    cut_colors = sorted(
        (
            sum(cycle in TRIANGLES for cycle in adj[cut]),
            sum(cycle in PENTAGONS for cycle in adj[cut]),
        )
        for cut in range(FIRST_CUT, FIRST_CUT + cut_count)
    )
    if cut_colors == [(1, 1), (5, 1)]:
        return "six-cycle common-cut core with TP tail"
    if cut_colors == [(1, 1), (1, 1), (5, 0)]:
        return "five-triangle common-cut core with two P tails"
    if max(cycle_degrees[cycle] for cycle in PENTAGONS) == 5:
        return "saturated pentagon hub"
    if max(cycle_degrees) <= 2 and max(cut_degrees) <= 2 and cycle_leaves == set(PENTAGONS):
        return "pentagon-ended incidence path"
    if cycle_leaves and cycle_leaves <= set(PENTAGONS):
        return "pentagon-leaf core"
    if all(cycle_degrees[cycle] > 1 for cycle in PENTAGONS):
        return "pentagon double hub"
    if max(cut_degrees) >= 3:
        return "multiway-cut core"
    if max(cycle_degrees[cycle] for cycle in TRIANGLES) == 3:
        return "saturated triangle router"
    return "hybrid two-hub core"


def census():
    by_cut_count = enumerate_trees()
    totals = Counter(
        {cut_count: len(classes) for cut_count, classes in by_cut_count.items()}
    )
    resolved = Counter()
    safe_choices = Counter()
    profiles = Counter()
    unresolved = []
    classes = Counter()

    for cut_count, signatures in by_cut_count.items():
        for edges in signatures.values():
            certificates = []
            for cycle in range(CYCLE_COUNT):
                components = components_after_cycle_split(edges, cut_count, cycle)
                certificate = split_certificate(edges, cut_count, cycle)
                profile = (
                    "T" if cycle in TRIANGLES else "P",
                    branch_multiset(components),
                    certificate is not None,
                )
                profiles[profile] += 1
                if certificate is not None:
                    certificates.append((cycle, certificate))
            safe_choices[len(certificates)] += 1
            if certificates:
                resolved[cut_count] += 1
            else:
                canonical = canonical_edges(edges, cut_count)
                label = structural_class(canonical, cut_count)
                unresolved.append((cut_count, canonical, label))
                classes[label] += 1

    unresolved.sort()
    expected_totals = Counter({1: 1, 2: 12, 3: 68, 4: 177, 5: 211, 6: 91})
    expected_resolved = Counter({2: 11, 3: 67, 4: 177, 5: 211, 6: 91})
    expected_safe_choices = Counter({0: 3, 1: 67, 2: 211, 3: 206, 4: 67, 5: 6})
    expected_unresolved = [
        (
            1,
            ((0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)),
            "seven-cycle bouquet",
        ),
        (
            2,
            ((0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (0, 8), (6, 8)),
            "six-cycle common-cut core with TP tail",
        ),
        (
            3,
            (
                (0, 7),
                (1, 7),
                (2, 7),
                (3, 7),
                (4, 7),
                (0, 8),
                (5, 8),
                (1, 9),
                (6, 9),
            ),
            "five-triangle common-cut core with two P tails",
        ),
    ]
    assert totals == expected_totals
    assert resolved == expected_resolved
    assert safe_choices == expected_safe_choices
    assert unresolved == expected_unresolved
    assert sum(totals.values()) == sum(resolved.values()) + len(unresolved)
    assert sum(profiles.values()) == CYCLE_COUNT * sum(totals.values())
    assert sum(count * multiplicity for count, multiplicity in safe_choices.items()) == sum(
        multiplicity for (_, _, safe), multiplicity in profiles.items() if safe
    )
    return totals, resolved, safe_choices, profiles, unresolved, classes


if __name__ == "__main__":
    totals, resolved, safe_choices, profiles, unresolved, classes = census()
    print("colored trees by cut count:", dict(sorted(totals.items())))
    print("SAFE-resolved trees by cut count:", dict(sorted(resolved.items())))
    print("trees by number of SAFE cycle choices:", dict(sorted(safe_choices.items())))
    print("unresolved structural classes:", dict(sorted(classes.items())))
    print("canonical unresolved types:")
    for cut_count, edges, label in unresolved:
        print(f"  c={cut_count} [{label}]: {edges}")
    print("split profiles (color, branch multiset, SAFE):")
    for profile, count in sorted(profiles.items()):
        print(f"  {profile}: {count}")
