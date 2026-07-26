#!/usr/bin/env python3
"""Exact color-preserving incidence-tree census for fully shared T^6 Q.

The generation is compressed: every seven-cycle tree has a leaf T, and
deleting that leaf gives a six-cycle T^5 Q tree.  We extend the established
rank-six census in the two inverse ways and canonicalize the results.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product


TRIANGLES = tuple(range(6))
Q_NODE = 6
CYCLES = TRIANGLES + (Q_NODE,)
FIRST_CUT = 7
Q_CAPS = {"q=3": 3, "q=4": 4, "q=5": 5, "q=6": 6, "q>=7": 6}
EXPECTED_COUNTS = {
    "q=3": {1: 1, 2: 8, 3: 33, 4: 71, 5: 74, 6: 29},
    "q=4": {1: 1, 2: 8, 3: 33, 4: 73, 5: 77, 6: 32},
    "q=5": {1: 1, 2: 8, 3: 33, 4: 73, 5: 78, 6: 33},
    "q=6": {1: 1, 2: 8, 3: 33, 4: 73, 5: 78, 6: 34},
    "q>=7": {1: 1, 2: 8, 3: 33, 4: 73, 5: 78, 6: 34},
}
EXPECTED_SUPPORT = {
    "q=3": {(True, False): 110, (False, True): 6, (True, True): 99, (False, False): 1},
    "q=4": {(True, False): 110, (False, True): 8, (True, True): 105, (False, False): 1},
    "q=5": {(True, False): 110, (False, True): 9, (True, True): 106, (False, False): 1},
    "q=6": {(True, False): 110, (False, True): 10, (True, True): 106, (False, False): 1},
    "q>=7": {(True, False): 110, (False, True): 10, (True, True): 106, (False, False): 1},
}


def positive_compositions(total, length, minimum=2, maximum=6):
    if length == 0:
        if total == 0:
            yield ()
        return
    for first in range(minimum, maximum + 1):
        rest = total - first
        if minimum * (length - 1) <= rest <= maximum * (length - 1):
            for suffix in positive_compositions(rest, length - 1, minimum, maximum):
                yield (first,) + suffix


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


def adjacency(edges, order):
    answer = [[] for _ in range(order)]
    for left, right in edges:
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


def color(vertex, q_node, first_cut):
    if vertex < q_node:
        return "T"
    if vertex == q_node:
        return "Q"
    assert vertex >= first_cut
    return "X"


def rooted_code(adj, vertex, parent, q_node, first_cut):
    children = sorted(
        rooted_code(adj, neighbor, vertex, q_node, first_cut)
        for neighbor in adj[vertex]
        if neighbor != parent
    )
    return color(vertex, q_node, first_cut) + "(" + "".join(children) + ")"


def canonical_signature(edges, order, q_node, first_cut):
    adj = adjacency(edges, order)
    return min(
        rooted_code(adj, center, -1, q_node, first_cut)
        for center in tree_centers(adj)
    )


def enumerate_rank_six(q_cap):
    """Generate T^5 Q classes used as the compressed rank-seven seeds."""
    triangles = tuple(range(5))
    q_node = 5
    cycles = triangles + (q_node,)
    first_cut = 6
    by_cut_count = {}
    for cut_count in range(1, 6):
        classes = {}
        edge_count = cut_count + 5
        for cut_degrees in positive_compositions(edge_count, cut_count):
            choices = [tuple(combinations(cycles, degree)) for degree in cut_degrees]
            for neighborhoods in product(*choices):
                cycle_degrees = [0] * 6
                edges = []
                for offset, neighborhood in enumerate(neighborhoods):
                    cut = first_cut + offset
                    for cycle in neighborhood:
                        cycle_degrees[cycle] += 1
                        edges.append((cycle, cut))
                if min(cycle_degrees) == 0:
                    continue
                if max(cycle_degrees[:5]) > 3 or cycle_degrees[q_node] > q_cap:
                    continue
                if not is_tree(edges, first_cut + cut_count):
                    continue
                signature = canonical_signature(
                    edges, first_cut + cut_count, q_node, first_cut
                )
                classes.setdefault(signature, tuple(sorted(edges)))
        by_cut_count[cut_count] = classes
    return by_cut_count


def lift_rank_six_edges(edges):
    """Insert the sixth T before Q and shift every old cut by one."""
    lifted = []
    for cycle, cut in edges:
        lifted_cycle = Q_NODE if cycle == 5 else cycle
        lifted.append((lifted_cycle, cut + 1))
    return tuple(sorted(lifted))


def enumerate_rank_seven(q_cap):
    """Extend at one T leaf, quotienting after extension.

    The inverse operations are exhaustive.  The leaf either meets an old cut,
    or it meets a degree-two cut whose other neighbor is an old cycle.
    """
    by_cut_count = {cut_count: {} for cut_count in range(1, 7)}
    rank_six = enumerate_rank_six(q_cap)
    expected_rank_six_total = {3: 68, 4: 70, 5: 71, 6: 71}[q_cap]
    assert sum(map(len, rank_six.values())) == expected_rank_six_total
    for old_cut_count, old_classes in rank_six.items():
        for old_edges in old_classes.values():
            base = lift_rank_six_edges(old_edges)

            for cut in range(FIRST_CUT, FIRST_CUT + old_cut_count):
                edges = tuple(sorted(base + ((5, cut),)))
                signature = canonical_signature(
                    edges, FIRST_CUT + old_cut_count, Q_NODE, FIRST_CUT
                )
                by_cut_count[old_cut_count].setdefault(signature, edges)

            new_cut = FIRST_CUT + old_cut_count
            for cycle in TRIANGLES[:5] + (Q_NODE,):
                if cycle == Q_NODE:
                    q_degree = sum(left == Q_NODE for left, _ in base)
                    if q_degree == q_cap:
                        continue
                else:
                    triangle_degree = sum(left == cycle for left, _ in base)
                    if triangle_degree == 3:
                        continue
                edges = tuple(sorted(base + ((5, new_cut), (cycle, new_cut))))
                signature = canonical_signature(
                    edges, FIRST_CUT + old_cut_count + 1, Q_NODE, FIRST_CUT
                )
                by_cut_count[old_cut_count + 1].setdefault(signature, edges)
    return by_cut_count


def branches_after_split(edges, cut_count, cycle):
    adj = adjacency(edges, FIRST_CUT + cut_count)
    branches = []
    for start in adj[cycle]:
        stack = [(start, cycle)]
        triangles = 0
        contains_q = False
        while stack:
            vertex, parent = stack.pop()
            triangles += vertex in TRIANGLES
            contains_q |= vertex == Q_NODE
            for neighbor in adj[vertex]:
                if neighbor != parent and neighbor != cycle:
                    stack.append((neighbor, vertex))
        branches.append((triangles, contains_q))
    return tuple(sorted(branches))


def packet_symbol(branch):
    triangles, contains_q = branch
    return "T" * triangles + ("Q" if contains_q else "")


def packet_margin(branch, label):
    """Return (rational lower bound, strict, cited packet class)."""
    triangles, contains_q = branch
    if not contains_q:
        margins = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1}
        return Fraction(margins[triangles]), True, f"T^{triangles}"
    if triangles == 0:
        if label == "q=3":
            return Fraction(0), True, "Q=T"
        if label in ("q=4", "q=6"):
            return Fraction(0), False, "nonhostile Q"
        return Fraction(-1), True, "Q>-1"
    if triangles == 1:
        return Fraction(0), True, "TQ>0"
    if triangles == 2:
        return Fraction(0), False, "generic TTQ>=0"
    return Fraction(0), True, f"established T^{triangles}Q>0"


def safe_split(edges, cut_count, cycle, label):
    branches = branches_after_split(edges, cut_count, cycle)
    if len(branches) < 2:
        return None
    packets = [packet_margin(branch, label) for branch in branches]
    lower = sum((packet[0] for packet in packets), Fraction(0))
    strict = any(packet[1] for packet in packets)
    if lower > 0 or (lower == 0 and strict):
        return {
            "symbols": tuple(packet_symbol(branch) for branch in branches),
            "lower": lower,
            "strict": strict,
            "ledger": tuple(packet[2] for packet in packets),
        }
    return None


def census_category(label, q_cap):
    by_cut_count = enumerate_rank_seven(q_cap)
    counts = Counter({c: len(classes) for c, classes in by_cut_count.items()})
    resolved = Counter()
    split_support = Counter()
    profiles = Counter()
    best_margins = Counter()
    exceptions = []

    for cut_count, classes in by_cut_count.items():
        for signature, edges in classes.items():
            certificates = []
            has_t_split = has_q_split = False
            for cycle in CYCLES:
                certificate = safe_split(edges, cut_count, cycle, label)
                if certificate is None:
                    continue
                certificates.append((cycle, certificate))
                has_t_split |= cycle in TRIANGLES
                has_q_split |= cycle == Q_NODE
                profile = ("Q" if cycle == Q_NODE else "T", certificate["symbols"])
                profiles[profile] += 1
            split_support[(has_t_split, has_q_split)] += 1
            if certificates:
                resolved[cut_count] += 1
                best = max(
                    (certificate["lower"], certificate["strict"])
                    for _, certificate in certificates
                )
                best_margins[best] += 1
            else:
                exceptions.append((cut_count, signature, edges))

    assert sum(counts.values()) == sum(resolved.values()) + len(exceptions)
    assert counts == EXPECTED_COUNTS[label]
    assert split_support == EXPECTED_SUPPORT[label], (label, split_support)
    assert len(exceptions) == 1
    cut_count, _, edges = exceptions[0]
    assert cut_count == 1
    assert len(edges) == 7 and len({cut for _, cut in edges}) == 1
    return {
        "label": label,
        "counts": counts,
        "resolved": resolved,
        "split_support": split_support,
        "profiles": profiles,
        "best_margins": best_margins,
        "exceptions": exceptions,
    }


def census():
    return [census_category(label, cap) for label, cap in Q_CAPS.items()]


if __name__ == "__main__":
    for result in census():
        print(result["label"])
        print("  colored trees by cut count:", dict(sorted(result["counts"].items())))
        print("  safe one-cycle splits by cut count:", dict(sorted(result["resolved"].items())))
        support = {
            "T only": result["split_support"][(True, False)],
            "Q only": result["split_support"][(False, True)],
            "both": result["split_support"][(True, True)],
            "neither": result["split_support"][(False, False)],
        }
        print("  trees supporting safe split colors:", support)
        margins = {
            (f">{lower}" if strict else f">={lower}"): count
            for (lower, strict), count in sorted(result["best_margins"].items())
        }
        print("  best certified rational lower margins:", margins)
        print("  unresolved canonical signatures:")
        for cut_count, signature, _ in result["exceptions"]:
            print(f"    c={cut_count}: {signature}")
