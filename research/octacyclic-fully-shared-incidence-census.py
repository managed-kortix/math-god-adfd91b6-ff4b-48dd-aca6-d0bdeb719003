#!/usr/bin/env python3
"""Exact fully shared incidence censuses for octacyclic T^7Q and T^6PP.

The objects are color-preserving bipartite cycle-cut trees.  Generation is by
recursive cycle-leaf extension and canonical tree coding.  The SAFE test uses
only one-cycle interval splits and packet bounds established through rank seven.
It is a finite structural audit, not a theorem checker.
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
TRIANGLE_MARGIN = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1, 7: 0}


def adjacency(tree):
    # A tree has |V|=|E|+1; cycle labels precede all cut labels.
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
    """Add one cycle leaf in both inverse forms and return labelled candidates."""
    old_n = len(tree.colors)
    colors = tree.colors + (new_color,)
    base = tuple(sorted((cycle, cut + 1) for cycle, cut in tree.edges))
    cut_labels = sorted({cut for _, cut in base})

    for cut in cut_labels:
        yield Tree(colors, tuple(sorted(base + ((old_n, cut),))))

    new_cut = max(cut_labels, default=old_n) + 1
    degrees = Counter(cycle for cycle, _ in base)
    for cycle, color in enumerate(tree.colors):
        if degrees[cycle] < color_capacity(color, q_cap):
            yield Tree(
                colors,
                tuple(sorted(base + ((old_n, new_cut), (cycle, new_cut)))),
            )


@lru_cache(maxsize=None)
def enumerate_colors(colors, q_cap):
    """Enumerate color-preserving classes by exhaustive leaf deletion/insertion."""
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
    cycles = component[0]
    return tuple(sorted(Counter(tree.colors[cycle] for cycle in cycles).items()))


def tq_bound(tree, component, q_label):
    counts = Counter(tree.colors[cycle] for cycle in component[0])
    triangles, q_count = counts["T"], counts["Q"]
    assert q_count in (0, 1)
    if not q_count:
        return Bound(Fraction(TRIANGLE_MARGIN[triangles]), True, f"A_{triangles}")
    if triangles == 0:
        if q_label == "q=3":
            return Bound(Fraction(0), True, "Q=T>0")
        if q_label in ("q=4", "q=6", "q=8"):
            return Bound(Fraction(0), False, "even Q>=0")
        return Bound(Fraction(-1), True, "hostile Q>-1")
    if triangles == 1:
        return Bound(Fraction(0), True, "TQ>0")
    if triangles == 2:
        return Bound(Fraction(0), False, "TTQ>=0")
    return Bound(Fraction(0), True, f"rank-{triangles + 1} T^kQ>0")


def tpp_bound(tree, component):
    cycles, internal_cuts, adj = component
    triangle_set = {cycle for cycle in cycles if tree.colors[cycle] == "T"}
    triangles = len(triangle_set)
    pentagons = len(cycles) - triangles
    rank = len(cycles)
    if pentagons == 0:
        return Bound(Fraction(TRIANGLE_MARGIN[triangles]), True, f"A_{triangles}")
    if rank == 1:
        return Bound(Fraction(-1, 4), True, "P>-1/4")
    if (triangles, pentagons) == (1, 1):
        return Bound(Fraction(3, 4), True, "TP>3/4")
    if (triangles, pentagons) == (0, 2):
        return Bound(Fraction(0), True, "PP>0")
    if (triangles, pentagons) == (2, 1):
        if any(triangle_set <= set(adj[cut]) for cut in internal_cuts):
            return Bound(Fraction(7, 4), True, "common-cut TTP>7/4")
    if (triangles, pentagons) == (1, 2):
        return Bound(Fraction(3, 2), True, "TPP>3/2")
    if rank == 3:
        return Bound(Fraction(0), False, "generic tricyclic>=0")
    if (triangles, pentagons) == (3, 1):
        if any(len(triangle_set & set(adj[cut])) >= 2 for cut in internal_cuts):
            return Bound(Fraction(1), True, "shared-pair TTTP>1")
    assert 4 <= rank <= 7
    return Bound(Fraction(0), True, f"generic rank-{rank}>0")


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


def cut_count(tree):
    return len(tree.edges) + 1 - len(tree.colors)


def census(colors, q_cap, bound_function):
    classes = enumerate_colors(tuple(sorted(colors)), q_cap)
    totals = Counter()
    resolved = Counter()
    choices = Counter()
    best_margins = Counter()
    unresolved = []
    support = Counter()
    for sig, tree in classes:
        cuts = cut_count(tree)
        totals[cuts] += 1
        certificates = []
        safe_colors = set()
        for cycle, color in enumerate(tree.colors):
            certificate = split_certificate(tree, cycle, bound_function)
            if certificate is not None:
                certificates.append((cycle, certificate))
                safe_colors.add(color)
        choices[len(certificates)] += 1
        support[tuple(sorted(safe_colors))] += 1
        if certificates:
            resolved[cuts] += 1
            best = max((item[1][2], any(b.strict for b in item[1][1])) for item in certificates)
            best_margins[best] += 1
        else:
            unresolved.append((cuts, sig, tree.edges))
    assert sum(totals.values()) == sum(resolved.values()) + len(unresolved)
    assert sum(choices.values()) == sum(totals.values())
    return totals, resolved, choices, support, best_margins, unresolved


def display(name, result):
    totals, resolved, choices, support, margins, unresolved = result
    print(name)
    print("  colored trees by cut count:", dict(sorted(totals.items())))
    print("  SAFE-resolved by cut count:", dict(sorted(resolved.items())))
    print("  trees by number of SAFE cycles:", dict(sorted(choices.items())))
    print("  SAFE split-color support:", dict(sorted(support.items())))
    print(
        "  best exact rational margins:",
        {(value, strict): count for (value, strict), count in sorted(margins.items())},
    )
    print("  unresolved canonical types:")
    for cuts, sig, edges in unresolved:
        print(f"    c={cuts}: {sig} {edges}")


def assert_rank_seven_regressions():
    cases = (
        (("T",) * 5 + ("P",) * 2, 0, {1: 1, 2: 12, 3: 68, 4: 177, 5: 211, 6: 91}),
        (("T",) * 6 + ("Q",), 3, {1: 1, 2: 8, 3: 33, 4: 71, 5: 74, 6: 29}),
        (("T",) * 6 + ("Q",), 6, {1: 1, 2: 8, 3: 33, 4: 73, 5: 78, 6: 34}),
    )
    for colors, q_cap, expected in cases:
        trees = enumerate_colors(tuple(sorted(colors)), q_cap)
        counts = Counter(cut_count(tree) for _, tree in trees)
        assert counts == Counter(expected)


def main():
    assert_rank_seven_regressions()
    expected_tq = {
        "q=3": {1: 1, 2: 9, 3: 49, 4: 142, 5: 236, 6: 191, 7: 60},
        "q=4": {1: 1, 2: 9, 3: 49, 4: 145, 5: 243, 6: 202, 7: 66},
        "q=5": {1: 1, 2: 9, 3: 49, 4: 145, 5: 245, 6: 205, 7: 69},
        "q=6": {1: 1, 2: 9, 3: 49, 4: 145, 5: 245, 6: 206, 7: 70},
        "q=7": {1: 1, 2: 9, 3: 49, 4: 145, 5: 245, 6: 206, 7: 71},
        "q=8": {1: 1, 2: 9, 3: 49, 4: 145, 5: 245, 6: 206, 7: 71},
        "q>=9": {1: 1, 2: 9, 3: 49, 4: 145, 5: 245, 6: 206, 7: 71},
    }
    for label, cap in (("q=3", 3), ("q=4", 4), ("q=5", 5), ("q=6", 6), ("q=7", 7), ("q=8", 7), ("q>=9", 7)):
        result = census(("T",) * 7 + ("Q",), cap, lambda tree, component, label=label: tq_bound(tree, component, label))
        assert dict(result[0]) == expected_tq[label]
        assert result[1] == Counter({cut: count for cut, count in expected_tq[label].items() if cut != 1})
        assert len(result[-1]) == 1 and result[-1][0][0] == 1
        display(f"T^7Q {label}", result)
    result = census(("T",) * 6 + ("P",) * 2, 0, tpp_bound)
    assert result[0] == Counter({1: 1, 2: 14, 3: 106, 4: 377, 5: 728, 6: 657, 7: 233})
    assert result[1] == Counter({2: 13, 3: 104, 4: 376, 5: 727, 6: 657, 7: 233})
    assert Counter(cuts for cuts, _, _ in result[-1]) == Counter({1: 1, 2: 1, 3: 2, 4: 1, 5: 1})
    display("T^6PP", result)


if __name__ == "__main__":
    main()
