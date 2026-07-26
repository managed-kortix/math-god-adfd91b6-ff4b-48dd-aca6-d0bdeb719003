#!/usr/bin/env python3
"""Exact color-preserving incidence-tree census for fully shared TTTTTQ."""

from collections import Counter
from itertools import combinations, permutations, product


TRIANGLES = tuple(range(5))
Q_NODE = 5
CYCLES = TRIANGLES + (Q_NODE,)
FIRST_CUT = 6
Q_CAPS = {"q=3": 3, "q=4": 4, "q>=5": 5}
EXPECTED_COUNTS = {
    "q=3": {1: 1, 2: 6, 3: 20, 4: 27, 5: 14},
    "q=4": {1: 1, 2: 6, 3: 20, 4: 28, 5: 15},
    "q>=5": {1: 1, 2: 6, 3: 20, 4: 28, 5: 16},
}
EXPECTED_SUPPORT = {
    "q=3": {(True, False): 36, (False, True): 4, (True, True): 27, (False, False): 1},
    "q=4": {(True, False): 36, (False, True): 5, (True, True): 28, (False, False): 1},
    "q>=5": {(True, False): 36, (False, True): 6, (True, True): 28, (False, False): 1},
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


def color(vertex):
    if vertex < 5:
        return "T"
    if vertex == Q_NODE:
        return "Q"
    return "X"


def rooted_code(adj, vertex, parent):
    children = sorted(
        rooted_code(adj, neighbor, vertex)
        for neighbor in adj[vertex]
        if neighbor != parent
    )
    return color(vertex) + "(" + "".join(children) + ")"


def canonical_signature(edges, cut_count):
    adj = adjacency(edges, FIRST_CUT + cut_count)
    return min(rooted_code(adj, center, -1) for center in tree_centers(adj))


def canonical_edges(edges, cut_count):
    """Return the lexicographically least edge set under T and cut permutations."""
    best = None
    for triangle_image in permutations(TRIANGLES):
        for cut_image in permutations(range(cut_count)):
            image = triangle_image + (Q_NODE,) + tuple(
                FIRST_CUT + cut for cut in cut_image
            )
            candidate = tuple(sorted((image[cycle], image[cut]) for cycle, cut in edges))
            if best is None or candidate < best:
                best = candidate
    return best


def enumerate_trees(q_cap):
    by_cut_count = {}
    for cut_count in range(1, 6):
        classes = {}
        edge_count = cut_count + 5
        for cut_degrees in positive_compositions(edge_count, cut_count):
            neighborhood_choices = [
                tuple(combinations(CYCLES, degree)) for degree in cut_degrees
            ]
            for neighborhoods in product(*neighborhood_choices):
                cycle_degrees = [0] * 6
                edges = []
                for cut_offset, neighborhood in enumerate(neighborhoods):
                    cut = FIRST_CUT + cut_offset
                    for cycle in neighborhood:
                        cycle_degrees[cycle] += 1
                        edges.append((cycle, cut))
                if min(cycle_degrees) == 0:
                    continue
                if max(cycle_degrees[:5]) > 3 or cycle_degrees[Q_NODE] > q_cap:
                    continue
                if not is_tree(edges, FIRST_CUT + cut_count):
                    continue
                signature = canonical_signature(edges, cut_count)
                classes.setdefault(signature, tuple(sorted(edges)))
        by_cut_count[cut_count] = classes
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


def safe_split(edges, cut_count, cycle):
    """Test only the packet implications explicitly recorded in existing ledgers."""
    branches = branches_after_split(edges, cut_count, cycle)
    if len(branches) < 2:
        return None

    if cycle == Q_NODE:
        # Every branch is a nonempty connected all-triangle packet.  Singleton
        # T is strict; TT, TTT, TTTT, and pentacyclic TTTTT are established.
        assert all(triangles >= 1 and not has_q for triangles, has_q in branches)
        reason = "all-triangle branches are positive"
    else:
        q_branch = next(branch for branch in branches if branch[1])
        q_triangles = q_branch[0]
        if q_triangles == 0:
            # Q may contribute -delta_q.  Since deg(T)<=3, the other four
            # triangles occupy at most two branches, one containing TT or more;
            # sigma(TT)>1>delta_q (uniformly q>=5), while q=3,4 are no worse.
            other_sizes = [triangles for triangles, has_q in branches if not has_q]
            assert max(other_sizes) >= 2
            reason = "TT credit > 1 absorbs singleton Q loss < 1"
        elif q_triangles == 1:
            reason = "TQ and every remaining triangle branch are positive"
        elif q_triangles == 2:
            # Generic tricyclic TTQ is nonnegative.  A different branch exists
            # and is a nonempty all-triangle packet, hence is strictly positive.
            assert any(not has_q for _, has_q in branches)
            reason = "TTQ is nonnegative and another triangle branch is positive"
        else:
            reason = "tetracyclic/pentacyclic T^kQ branch and remaining branches are positive"
    return tuple(packet_symbol(branch) for branch in branches), reason


def census_category(label, q_cap):
    by_cut_count = enumerate_trees(q_cap)
    resolved = Counter()
    split_support = Counter()
    exceptions = []
    profiles = Counter()

    for cut_count, classes in by_cut_count.items():
        for edges in classes.values():
            certificates = []
            has_t_split = has_q_split = False
            for cycle in CYCLES:
                certificate = safe_split(edges, cut_count, cycle)
                if certificate is None:
                    continue
                certificates.append((cycle, certificate))
                has_t_split |= cycle in TRIANGLES
                has_q_split |= cycle == Q_NODE
                profiles[("Q" if cycle == Q_NODE else "T", certificate[0])] += 1
            split_support[(has_t_split, has_q_split)] += 1
            if certificates:
                resolved[cut_count] += 1
            else:
                exceptions.append((cut_count, canonical_edges(edges, cut_count)))

    counts = Counter({cut_count: len(classes) for cut_count, classes in by_cut_count.items()})
    assert len(exceptions) == 1
    assert exceptions[0] == (
        1,
        ((0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6)),
    )
    assert counts == EXPECTED_COUNTS[label]
    assert split_support == EXPECTED_SUPPORT[label]
    assert sum(counts.values()) == sum(resolved.values()) + len(exceptions)
    return {
        "label": label,
        "counts": counts,
        "resolved": resolved,
        "split_support": split_support,
        "exceptions": exceptions,
        "profiles": profiles,
    }


def census():
    return [census_category(label, cap) for label, cap in Q_CAPS.items()]


if __name__ == "__main__":
    for result in census():
        print(result["label"])
        print("  colored trees by cut count:", dict(sorted(result["counts"].items())))
        print("  safe one-cycle split by cut count:", dict(sorted(result["resolved"].items())))
        support = {
            "T only": result["split_support"][(True, False)],
            "Q only": result["split_support"][(False, True)],
            "both": result["split_support"][(True, True)],
            "neither": result["split_support"][(False, False)],
        }
        print("  trees supporting safe split types:", support)
        print("  unresolved canonical edge sets:")
        for cut_count, edges in result["exceptions"]:
            print(f"    c={cut_count}: {edges}")
