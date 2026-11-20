#!/usr/bin/env python3
"""Dependency-free exhaustive verifier for the total-weight-seven tree lemma.

This program is corroboration, not the mathematical proof.  It enumerates one
representative of every unlabelled *reduced positive-hull tree*, every legal
positive support, and every positive integer weighting of total weight seven.
Reduced means:

* every leaf has positive weight (otherwise it is not in the positive hull);
* every weight-zero degree-two vertex has been suppressed;
* weight-zero vertices of degree at least three are retained.

It verifies the exclusive classification

(A) some edge has side weight in {2,3,4,5}; or
(B) the tree is a star, every leaf has weight one, and the center has the
    remaining weight.

It also expands every checked state by several patterns of weight-zero
subdivision vertices, suppresses them again, and checks that both the weighted
isomorphism type and balanced-edge predicate are invariant.  No third-party
package, numerical eigensolver, randomness, or assertion statement is used, so
normal and ``python -O`` executions have the same checks.
"""

from collections import Counter
from hashlib import sha256
from json import dumps

TOTAL = 7
MAX_REDUCED_VERTICES = 2 * TOTAL - 2


class VerificationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def rooted_tree_codes(max_n):
    """Return canonical AHU codes for rooted unlabelled trees by order."""
    rooted = [set() for _ in range(max_n + 1)]
    forests = [set() for _ in range(max_n)]
    forests[0].add(())
    rooted[1].add(())
    for size in range(1, max_n):
        out = set()
        # A rooted tree is a nondecreasing tuple of rooted child-tree codes.
        for child_size in range(1, size + 1):
            for child in rooted[child_size]:
                for prefix in forests[size - child_size]:
                    if not prefix or prefix[-1] <= child:
                        out.add(prefix + (child,))
        forests[size] = out
        rooted[size + 1] = set(out)
    return rooted


def adjacency_from_rooted_code(code):
    adjacency = []

    def visit(node_code, parent=None):
        vertex = len(adjacency)
        adjacency.append([])
        if parent is not None:
            adjacency[vertex].append(parent)
            adjacency[parent].append(vertex)
        for child_code in node_code:
            visit(child_code, vertex)

    visit(code)
    return tuple(tuple(sorted(neighbours)) for neighbours in adjacency)


def rooted_code(adjacency, vertex, parent):
    return tuple(sorted(rooted_code(adjacency, child, vertex)
                        for child in adjacency[vertex] if child != parent))


def free_code(adjacency):
    return min(rooted_code(adjacency, vertex, -1)
               for vertex in range(len(adjacency)))


def weighted_rooted_code(adjacency, weights, vertex, parent):
    children = tuple(sorted(weighted_rooted_code(adjacency, weights, child,
                                                 vertex)
                            for child in adjacency[vertex]
                            if child != parent))
    return weights[vertex], children


def weighted_free_code(adjacency, weights):
    return min(weighted_rooted_code(adjacency, weights, vertex, -1)
               for vertex in range(len(adjacency)))


def unlabelled_free_trees(max_n):
    """Return one deterministic adjacency representative per free tree."""
    rooted = rooted_tree_codes(max_n)
    free = [dict() for _ in range(max_n + 1)]
    for order in range(1, max_n + 1):
        for code in sorted(rooted[order]):
            adjacency = adjacency_from_rooted_code(code)
            free[order].setdefault(free_code(adjacency), adjacency)
    return free


def positive_compositions(total, parts, prefix=()):
    if parts == 1:
        yield prefix + (total,)
        return
    for first in range(1, total - parts + 2):
        yield from positive_compositions(total - first, parts - 1,
                                         prefix + (first,))


def edges(adjacency):
    return tuple((u, v) for u in range(len(adjacency))
                 for v in adjacency[u] if u < v)


def side_weight(adjacency, weights, start, forbidden):
    stack = [start]
    seen = {forbidden}
    value = 0
    while stack:
        vertex = stack.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        value += weights[vertex]
        stack.extend(adjacency[vertex])
    return value


def has_balanced_edge(adjacency, weights):
    return any(2 <= side_weight(adjacency, weights, u, v) <= 5
               for u, v in edges(adjacency))


def expand_chains(adjacency, weights, subdivision_counts):
    """Replace each edge by a path with the requested zero-weight interiors."""
    old_edges = edges(adjacency)
    require(len(old_edges) == len(subdivision_counts),
            "subdivision pattern has wrong length")
    expanded = [set() for _ in adjacency]
    expanded_weights = list(weights)
    for (u, v), count in zip(old_edges, subdivision_counts):
        require(isinstance(count, int) and count >= 0,
                "invalid subdivision count")
        previous = u
        for _ in range(count):
            new_vertex = len(expanded)
            expanded.append(set())
            expanded_weights.append(0)
            expanded[previous].add(new_vertex)
            expanded[new_vertex].add(previous)
            previous = new_vertex
        expanded[previous].add(v)
        expanded[v].add(previous)
    result = tuple(tuple(sorted(neighbours)) for neighbours in expanded)
    require(len(edges(result)) == len(result) - 1,
            "expanded graph is not a tree")
    return result, tuple(expanded_weights)


def suppress_zero_degree_two(adjacency, weights):
    """Suppress all zero-weight degree-two vertices in a weighted tree."""
    graph = [set(neighbours) for neighbours in adjacency]
    active = set(range(len(graph)))
    while True:
        candidate = next((v for v in sorted(active)
                          if weights[v] == 0 and len(graph[v]) == 2), None)
        if candidate is None:
            break
        left, right = sorted(graph[candidate])
        graph[left].remove(candidate)
        graph[right].remove(candidate)
        graph[candidate].clear()
        active.remove(candidate)
        require(right not in graph[left],
                "suppression would create a parallel edge")
        graph[left].add(right)
        graph[right].add(left)
    old_to_new = {old: new for new, old in enumerate(sorted(active))}
    reduced_adjacency = tuple(
        tuple(sorted(old_to_new[neighbour] for neighbour in graph[old]))
        for old in sorted(active)
    )
    reduced_weights = tuple(weights[old] for old in sorted(active))
    require(len(edges(reduced_adjacency)) == len(reduced_adjacency) - 1,
            "suppressed graph is not a tree")
    return reduced_adjacency, reduced_weights


def audit_chain_expansions(adjacency, weights, serial):
    """Adversarial finite tests for arbitrary K2-chain suppression."""
    edge_count = len(edges(adjacency))
    patterns = [
        (1,) * edge_count,
        tuple((serial + 2 * j) % 4 for j in range(edge_count)),
        tuple(7 if j == serial % edge_count else 0
              for j in range(edge_count)),
    ]
    original_code = weighted_free_code(adjacency, weights)
    original_balanced = has_balanced_edge(adjacency, weights)
    checks = 0
    for pattern in patterns:
        expanded_adjacency, expanded_weights = expand_chains(
            adjacency, weights, pattern)
        require(sum(expanded_weights) == TOTAL,
                "subdivision changed total weight")
        require(has_balanced_edge(expanded_adjacency, expanded_weights)
                == original_balanced,
                "subdivision changed balanced-edge status")
        reduced_adjacency, reduced_weights = suppress_zero_degree_two(
            expanded_adjacency, expanded_weights)
        require(weighted_free_code(reduced_adjacency, reduced_weights)
                == original_code,
                "suppression did not recover weighted tree")
        checks += 1
    return checks


def verify():
    free = unlabelled_free_trees(MAX_REDUCED_VERTICES)
    # Known Otter counts independently guard the tree generator through the
    # largest order that can occur for total positive weight seven.
    expected_free_counts = (1, 1, 1, 2, 3, 6, 11, 23, 47, 106, 235, 551)
    actual_free_counts = tuple(len(free[n]) for n in range(1, 13))
    require(actual_free_counts == expected_free_counts,
            "unlabelled-free-tree count mismatch")

    by_positive_vertices = Counter()
    balanced_by_positive_vertices = Counter()
    exceptional_profiles = Counter()
    states_with_zero_branching = 0
    checked = 0
    chain_expansion_checks = 0

    for order in range(2, MAX_REDUCED_VERTICES + 1):
        for adjacency in free[order].values():
            degree = tuple(map(len, adjacency))
            # In a reduced positive hull every degree-1 or degree-2 vertex is
            # positive.  Degree >= 3 vertices may be zero or positive.
            mandatory = [v for v, d in enumerate(degree) if d <= 2]
            optional = [v for v, d in enumerate(degree) if d >= 3]
            for mask in range(1 << len(optional)):
                support = sorted(mandatory + [
                    optional[j] for j in range(len(optional))
                    if (mask >> j) & 1
                ])
                positive_vertices = len(support)
                if not 2 <= positive_vertices <= TOTAL:
                    continue
                require(order <= 2 * positive_vertices - 2,
                        "reduced-vertex bound failed")

                for values in positive_compositions(TOTAL, positive_vertices):
                    weights = [0] * order
                    for vertex, value in zip(support, values):
                        weights[vertex] = value
                    require(sum(weights) == TOTAL,
                            "weight composition failed")
                    require(all(weights[v] > 0 or degree[v] >= 3
                                for v in range(order)),
                            "unreduced zero-weight vertex survived")

                    balanced = has_balanced_edge(adjacency, weights)
                    exceptional_centers = []
                    for center in range(order):
                        if all(side_weight(adjacency, weights, neighbour,
                                           center) == 1
                               for neighbour in adjacency[center]):
                            exceptional_centers.append(center)
                    exceptional = bool(exceptional_centers)

                    # The two alternatives must be exclusive and exhaustive.
                    require(balanced != exceptional,
                            "classification alternatives failed")
                    checked += 1
                    by_positive_vertices[positive_vertices] += 1
                    if any(weights[v] == 0 and degree[v] >= 3
                           for v in range(order)):
                        states_with_zero_branching += 1

                    chain_expansion_checks += audit_chain_expansions(
                        adjacency, tuple(weights), checked)

                    if balanced:
                        balanced_by_positive_vertices[positive_vertices] += 1
                        continue

                    require(len(exceptional_centers) == 1,
                            "exceptional center is not unique")
                    center = exceptional_centers[0]
                    leaves = list(adjacency[center])
                    # No hidden zero branching, positive nonleaf, or
                    # unsuppressed connector may remain in an exception.
                    require(order == len(leaves) + 1,
                            "exception is not a literal reduced star")
                    require(all(len(adjacency[leaf]) == 1 for leaf in leaves),
                            "exception has a nonleaf arm vertex")
                    require(all(weights[leaf] == 1 for leaf in leaves),
                            "exception has a nonunit leaf")
                    require(weights[center] == TOTAL - len(leaves),
                            "exception has wrong center weight")
                    exceptional_profiles[(positive_vertices,
                                          weights[center],
                                          len(leaves),
                                          order)] += 1

    # The count two in the p=2 row is the two assignments (1,6) and (6,1)
    # on the fixed labelled representative; they are one weighted isomorphism
    # type after designating the rank-six endpoint as the center.
    expected_exceptional_profiles = {
        (2, 6, 1, 2): 2,
        (3, 5, 2, 3): 1,
        (4, 4, 3, 4): 1,
        (5, 3, 4, 5): 1,
        (6, 2, 5, 6): 1,
        (7, 1, 6, 7): 1,
        (7, 0, 7, 8): 1,
    }
    require(dict(exceptional_profiles) == expected_exceptional_profiles,
            "exceptional-profile census mismatch")
    require(set(by_positive_vertices) == set(range(2, 8)),
            "a p=2,...,7 edge case was not exercised")
    require(states_with_zero_branching > 0,
            "zero-weight branching was not exercised")
    require(chain_expansion_checks == 3 * checked,
            "K2-chain expansion suite was incomplete")

    payload = {
        "total_weight": TOTAL,
        "free_tree_counts_orders_1_through_12": actual_free_counts,
        "checked_weighted_states": checked,
        "states_with_zero_weight_branching": states_with_zero_branching,
        "k2_chain_expansion_and_suppression_checks": chain_expansion_checks,
        "states_by_positive_vertices": dict(sorted(by_positive_vertices.items())),
        "balanced_states_by_positive_vertices": dict(
            sorted(balanced_by_positive_vertices.items())),
        "exceptional_profiles_(positive_vertices,center_weight,leaves,order)": {
            str(key): exceptional_profiles[key]
            for key in sorted(exceptional_profiles)
        },
    }
    canonical = dumps(payload, sort_keys=True, separators=(",", ":"))
    print(dumps(payload, sort_keys=True, indent=2))
    print("payload_sha256=" + sha256(canonical.encode()).hexdigest())
    print("weighted-tree classification: PASS")


if __name__ == "__main__":
    verify()
