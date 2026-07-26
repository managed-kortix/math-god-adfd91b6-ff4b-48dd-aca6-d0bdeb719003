#!/usr/bin/env python3
"""Compressed exact rank-nine incidence censuses for T^8Q and T^7PP.

The objects are color-preserving bipartite cycle-cut trees. Generation uses
cycle-leaf deletion/insertion and center-rooted canonical codes. The ordinary
one-cycle split ledger uses fractions.Fraction exclusively. This is a finite
structural experiment, not a theorem checker.
"""

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache


@dataclass(frozen=True)
class Tree:
    colors: tuple[str, ...]
    edges: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class Bound:
    value: Fraction
    strict: bool
    source: str


CAPACITY = {"T": 3, "P": 5}
TRIANGLE_MARGIN = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1, 7: 0, 8: 0}


def adjacency(tree):
    answer = [[] for _ in range(len(tree.edges) + 1)]
    for left, right in tree.edges:
        answer[left].append(right)
        answer[right].append(left)
    return answer


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


def rooted_code(tree, adj, vertex, parent):
    cycle_count = len(tree.colors)
    color = tree.colors[vertex] if vertex < cycle_count else "X"
    children = sorted(
        rooted_code(tree, adj, neighbor, vertex)
        for neighbor in adj[vertex]
        if neighbor != parent
    )
    return color + "(" + "".join(children) + ")"


def signature(tree):
    adj = adjacency(tree)
    return min(rooted_code(tree, adj, center, -1) for center in tree_centers(adj))


def color_capacity(color, q_cap):
    return q_cap if color == "Q" else CAPACITY[color]


def lift(tree, new_color, q_cap):
    """Restore one deleted cycle leaf in the two exhaustive inverse forms."""
    old_cycle_count = len(tree.colors)
    colors = tree.colors + (new_color,)
    base = tuple(sorted((cycle, cut + 1) for cycle, cut in tree.edges))
    cut_labels = sorted({cut for _, cut in base})

    for cut in cut_labels:
        yield Tree(colors, tuple(sorted(base + ((old_cycle_count, cut),))))

    new_cut = max(cut_labels, default=old_cycle_count) + 1
    degrees = Counter(cycle for cycle, _ in base)
    for cycle, color in enumerate(tree.colors):
        if degrees[cycle] < color_capacity(color, q_cap):
            yield Tree(
                colors,
                tuple(sorted(base + ((old_cycle_count, new_cut), (cycle, new_cut)))),
            )


@lru_cache(maxsize=None)
def enumerate_colors(colors, q_cap):
    """Return one representative of every color-preserving incidence class."""
    colors = tuple(colors)
    if len(colors) == 2:
        tree = Tree(colors, ((0, 2), (1, 2)))
        return ((signature(tree), tree),)

    classes = {}
    for new_color in sorted(set(colors)):
        remaining = list(colors)
        remaining.remove(new_color)
        for _, old_tree in enumerate_colors(tuple(remaining), q_cap):
            for tree in lift(old_tree, new_color, q_cap):
                classes.setdefault(signature(tree), tree)
    return tuple(sorted(classes.items()))


def cut_count(tree):
    return len(tree.edges) + 1 - len(tree.colors)


def validate_classes(classes, q_cap):
    seen = set()
    for sig, tree in classes:
        assert sig not in seen and sig == signature(tree)
        seen.add(sig)
        adj = adjacency(tree)
        cycle_count = len(tree.colors)
        assert len(tree.edges) == len(adj) - 1
        assert all(len(adj[cut]) >= 2 for cut in range(cycle_count, len(adj)))
        assert all(
            1 <= len(adj[cycle]) <= color_capacity(color, q_cap)
            for cycle, color in enumerate(tree.colors)
        )


def components_after_split(tree, sacrificed):
    adj = adjacency(tree)
    cycle_count = len(tree.colors)
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
            if vertex < cycle_count:
                cycles.add(vertex)
            for neighbor in adj[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        internal_cuts = tuple(
            cut
            for cut in vertices
            if cut >= cycle_count
            and sum(cycle in cycles for cycle in adj[cut]) >= 2
        )
        components.append((tuple(sorted(cycles)), internal_cuts, adj))
    return tuple(components)


def component_profile(tree, component):
    return tuple(
        sorted(Counter(tree.colors[cycle] for cycle in component[0]).items())
    )


def tq_bound(label, tree, component):
    counts = Counter(tree.colors[cycle] for cycle in component[0])
    triangles, q_count = counts["T"], counts["Q"]
    assert q_count in (0, 1)
    if not q_count:
        return Bound(Fraction(TRIANGLE_MARGIN[triangles]), True, f"A_{triangles}")
    if triangles == 0:
        if label == "q=3":
            return Bound(Fraction(0), True, "Q=T > 0")
        if label in ("q=4", "q=6", "q=8"):
            return Bound(Fraction(0), False, "even Q >= 0")
        return Bound(Fraction(-1), True, "hostile Q > -1")
    if triangles == 1:
        return Bound(Fraction(0), True, "TQ > 0")
    if triangles == 2:
        return Bound(Fraction(0), False, "TTQ >= 0")
    return Bound(Fraction(0), True, f"established rank-{triangles + 1} T^kQ > 0")


def tpp_bound(tree, component):
    cycles, internal_cuts, adj = component
    triangle_set = {cycle for cycle in cycles if tree.colors[cycle] == "T"}
    triangles = len(triangle_set)
    pentagons = len(cycles) - triangles
    rank = len(cycles)
    if pentagons == 0:
        return Bound(Fraction(TRIANGLE_MARGIN[triangles]), True, f"A_{triangles}")
    if rank == 1:
        return Bound(Fraction(-1, 4), True, "P > -1/4")
    if (triangles, pentagons) == (1, 1):
        return Bound(Fraction(3, 4), True, "TP > 3/4")
    if (triangles, pentagons) == (0, 2):
        return Bound(Fraction(0), True, "PP > 0")
    if (triangles, pentagons) == (2, 1):
        if any(triangle_set <= set(adj[cut]) for cut in internal_cuts):
            return Bound(Fraction(7, 4), True, "common-cut TTP > 7/4")
    if (triangles, pentagons) == (1, 2):
        return Bound(Fraction(3, 2), True, "TPP > 3/2")
    if rank == 3:
        return Bound(Fraction(0), False, "generic rank three >= 0")
    if (triangles, pentagons) == (3, 1):
        if any(len(triangle_set & set(adj[cut])) >= 2 for cut in internal_cuts):
            return Bound(Fraction(1), True, "shared-pair TTTP > 1")
    assert 4 <= rank <= 8
    return Bound(Fraction(0), True, f"established generic rank-{rank} > 0")


def split_certificate(tree, cycle, bound_function):
    components = components_after_split(tree, cycle)
    if len(components) < 2:
        return None
    bounds = tuple(bound_function(tree, component) for component in components)
    total = sum((bound.value for bound in bounds), Fraction(0))
    strict = any(bound.strict for bound in bounds)
    if total > 0 or (total == 0 and strict):
        return tuple(component_profile(tree, item) for item in components), bounds, total
    return None


def cut_profile(tree):
    adj = adjacency(tree)
    cycle_count = len(tree.colors)
    return tuple(
        sorted(
            tuple(sorted(Counter(tree.colors[cycle] for cycle in adj[cut]).items()))
            for cut in range(cycle_count, len(adj))
        )
    )


def census(colors, q_cap, bound_function):
    totals = Counter()
    resolved = Counter()
    choices = Counter()
    support = Counter()
    best_margins = Counter()
    unresolved = []
    classes = enumerate_colors(tuple(sorted(colors)), q_cap)
    validate_classes(classes, q_cap)
    for sig, tree in classes:
        cuts = cut_count(tree)
        totals[cuts] += 1
        certificates = []
        safe_colors = set()
        for cycle, color in enumerate(tree.colors):
            certificate = split_certificate(tree, cycle, bound_function)
            if certificate is not None:
                certificates.append(certificate)
                safe_colors.add(color)
        choices[len(certificates)] += 1
        support[tuple(sorted(safe_colors))] += 1
        if certificates:
            resolved[cuts] += 1
            best = max(
                (item[2], any(bound.strict for bound in item[1]))
                for item in certificates
            )
            best_margins[best] += 1
        else:
            unresolved.append((cuts, sig, cut_profile(tree), tree.edges))
    unresolved.sort()
    assert sum(totals.values()) == sum(resolved.values()) + len(unresolved)
    assert sum(choices.values()) == sum(totals.values())
    return totals, resolved, choices, support, best_margins, unresolved


EXPECTED_TQ = {
    "q=3": {1: 1, 2: 11, 3: 68, 4: 253, 5: 572, 6: 742, 7: 493, 8: 127},
    "q=4": {1: 1, 2: 11, 3: 68, 4: 258, 5: 586, 6: 774, 7: 525, 8: 142},
    "q=5": {1: 1, 2: 11, 3: 68, 4: 258, 5: 589, 6: 781, 7: 536, 8: 148},
    "q=6": {1: 1, 2: 11, 3: 68, 4: 258, 5: 589, 6: 783, 7: 539, 8: 151},
    "q=7": {1: 1, 2: 11, 3: 68, 4: 258, 5: 589, 6: 783, 7: 540, 8: 152},
    "q=8": {1: 1, 2: 11, 3: 68, 4: 258, 5: 589, 6: 783, 7: 540, 8: 153},
    "q>=9": {1: 1, 2: 11, 3: 68, 4: 258, 5: 589, 6: 783, 7: 540, 8: 153},
}
EXPECTED_TPP = {
    1: 1,
    2: 17,
    3: 150,
    4: 699,
    5: 1856,
    6: 2714,
    7: 1998,
    8: 569,
}


def compact_counter(counter):
    return dict(sorted(counter.items()))


def display(name, result):
    totals, resolved, choices, support, margins, unresolved = result
    print(name)
    print(
        "  colored trees by cut count:",
        compact_counter(totals),
        "total",
        sum(totals.values()),
    )
    print(
        "  SAFE by cut count:",
        compact_counter(resolved),
        "total",
        sum(resolved.values()),
    )
    exceptions = Counter(item[0] for item in unresolved)
    print("  exceptions by cut count:", compact_counter(exceptions))
    print("  trees by SAFE-cycle count:", compact_counter(choices))
    print("  SAFE color support:", compact_counter(support))
    print("  best exact Fraction ledgers:", compact_counter(margins))
    print("  unresolved canonical types:")
    for cuts, sig, profile, edges in unresolved:
        print(f"    c={cuts} cuts={profile} signature={sig} edges={edges}")


def rank_eight_regressions():
    cases = (
        (
            ("T",) * 7 + ("Q",),
            3,
            {1: 1, 2: 9, 3: 49, 4: 142, 5: 236, 6: 191, 7: 60},
        ),
        (
            ("T",) * 7 + ("Q",),
            7,
            {1: 1, 2: 9, 3: 49, 4: 145, 5: 245, 6: 206, 7: 71},
        ),
        (
            ("T",) * 6 + ("P",) * 2,
            0,
            {1: 1, 2: 14, 3: 106, 4: 377, 5: 728, 6: 657, 7: 233},
        ),
    )
    for colors, q_cap, expected in cases:
        classes = enumerate_colors(tuple(sorted(colors)), q_cap)
        validate_classes(classes, q_cap)
        counts = Counter(cut_count(tree) for _, tree in classes)
        assert counts == Counter(expected)


def main():
    rank_eight_regressions()
    regimes = (
        ("q=3", 3),
        ("q=4", 4),
        ("q=5", 5),
        ("q=6", 6),
        ("q=7", 7),
        ("q=8", 8),
        ("q>=9", 8),
    )
    for label, cap in regimes:
        result = census(
            ("T",) * 8 + ("Q",),
            cap,
            lambda tree, component, label=label: tq_bound(label, tree, component),
        )
        assert result[0] == Counter(EXPECTED_TQ[label])
        if label in {"q=3", "q=4", "q=6", "q=8"}:
            expected_exceptions = Counter({1: 1})
        else:
            expected_exceptions = Counter({1: 1, 2: 1})
        assert Counter(item[0] for item in result[-1]) == expected_exceptions
        display(f"T^8Q {label}", result)

    result = census(("T",) * 7 + ("P",) * 2, 0, tpp_bound)
    assert result[0] == Counter(EXPECTED_TPP)
    assert Counter(item[0] for item in result[-1]) == Counter(
        {1: 1, 2: 2, 3: 2, 4: 1, 5: 1}
    )
    display("T^7PP", result)


if __name__ == "__main__":
    main()
