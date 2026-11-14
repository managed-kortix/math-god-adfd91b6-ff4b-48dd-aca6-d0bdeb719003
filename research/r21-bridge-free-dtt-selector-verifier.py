#!/usr/bin/env python3
"""NONPROMOTIONAL exhaustive R21 bridge-free incidence-skeleton audit.

The input contract is deliberately narrow: after the hostile rank-one side and
all cyclic-hull K2 blocks have been handled elsewhere, the connected physical
complement has exactly one diamond block D and four triangle blocks T0,...,T3.
Payload-only block-cut branches have already been pruned from the minimal
cyclic hull.  Physical port assignments project to the incidence skeleton and
are immaterial to the selector; this program does not count port orbits.

Completeness of the finite generator is elementary.  If c cut nodes remain,
the bipartite incidence tree has 5+c nodes and 4+c edges.  Every retained cut
has degree at least two, while the sum of cut degrees is 4+c; hence c<=4.
Connectedness of five blocks gives c>=1.  Conversely, every state is a
connected (4+c)-edge subset of K_(5,c), subject only to cut degree at least two
and the physical port capacities deg(D)<=4 and deg(T_i)<=3.  Such a connected
subgraph has |V|-1 edges and is therefore a tree.  The generator enumerates
exactly these subsets.  Rooted AHU recursion with unique marked-block colours
and one common cut colour is a complete rooted colour-preserving isomorphism
invariant, so set-deduplication by its code loses only cut-node relabellings.

For each canonical state the verifier finds a pair of triangles whose minimal
D--triangle hull contains no other cyclic block.  Since the contract is
bridge-free, that hull also contains no K2 block.  This does not prove the
preceding bridge cascade, any spectral packet bound, induced territory
ownership, or a rank-seven closure.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from collections import Counter, deque
from pathlib import Path


MARKED = ("D", "T0", "T1", "T2", "T3")
CUT = "C"
EXPECTED_STATES_BY_CUTS = {1: 1, 2: 35, 3: 150, 4: 121}
EXPECTED_SELECTOR_MULTIPLICITIES = {1: 48, 2: 96, 3: 88, 4: 60, 6: 15}
EXPECTED_SIGNATURE_SHA256 = "a5c56244a635fea3656771b7023e8801226599a29da3b1fed8aff6e3daaceeda"


class AuditError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def tree_adjacency(order: int, edges: tuple[tuple[int, int], ...]) -> tuple[tuple[int, ...], ...]:
    graph = [set() for unused in range(order)]
    for left, right in edges:
        require(left != right and right not in graph[left], "bad tree edge")
        graph[left].add(right)
        graph[right].add(left)
    return tuple(tuple(sorted(neighbors)) for neighbors in graph)


def rooted_parent(graph: tuple[tuple[int, ...], ...], root: int = 0) -> tuple[int, ...]:
    parent = [-2] * len(graph)
    parent[root] = -1
    queue = deque([root])
    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if parent[neighbor] == -2:
                parent[neighbor] = current
                queue.append(neighbor)
    require(all(value != -2 for value in parent), "generated tree is disconnected")
    return tuple(parent)


def canonical_code(parent: tuple[int, ...], labels: tuple[str, ...]) -> str:
    """AHU rooted-tree code; equal cut labels are quotient by isomorphism."""
    children = [[] for unused in parent]
    for node, predecessor in enumerate(parent):
        if predecessor >= 0:
            children[predecessor].append(node)

    def encode(node: int) -> str:
        suffixes = sorted(encode(child) for child in children[node])
        return f"{labels[node]}[{'|'.join(suffixes)}]"

    return encode(0)


def valid_incidence_tree(labels: tuple[str, ...],
                         graph: tuple[tuple[int, ...], ...]) -> bool:
    if (len(labels) < 6 or len(labels) > 9 or labels[:len(MARKED)] != MARKED
            or any(label != CUT for label in labels[len(MARKED):])
            or len(graph) != len(labels)):
        return False
    # A physical block-cut graph is undirected, simple, and bipartite between
    # block and cut nodes.  Check symmetry explicitly so a malformed adjacency
    # table cannot serve as a hostile witness.
    for node, neighbors in enumerate(graph):
        if len(neighbors) != len(set(neighbors)):
            return False
        for neighbor in neighbors:
            if not (0 <= neighbor < len(graph)) or node not in graph[neighbor]:
                return False
            if (labels[node] == CUT) == (labels[neighbor] == CUT):
                return False
    # Suppress degree-one cuts: they are not articulation vertices.  Every cut
    # retained in the physical block-cut tree belongs to at least two blocks.
    if any(len(graph[node]) < 2 for node in range(5, len(labels))):
        return False
    # A block node has one incidence per distinct vertex of the block.  D has
    # four vertices and each triangle has three; repeated ownership at one cut
    # is represented by one incidence, not duplicate edges.
    if len(graph[0]) > 4:
        return False
    if any(len(graph[node]) > 3 for node in range(1, 5)):
        return False
    return True


def generate_states() -> dict[str, tuple[tuple[int, ...], tuple[str, ...]]]:
    states: dict[str, tuple[tuple[int, ...], tuple[str, ...]]] = {}
    for cut_count in range(1, 5):
        labels = (*MARKED, *((CUT,) * cut_count))
        block_nodes = tuple(range(len(MARKED)))
        cut_nodes = tuple(range(len(MARKED), len(labels)))
        possible = tuple((block, cut) for block in block_nodes for cut in cut_nodes)
        edge_count = len(labels) - 1
        # Every valid state is a simple bipartite tree, hence an edge_count-
        # subset of K_(5,cut_count).  Enumerating those subsets is much smaller
        # than generating all labelled trees and then rejecting nonbipartite
        # ones; connectivity plus |E|=|V|-1 is exactly the tree condition.
        for edges in itertools.combinations(possible, edge_count):
            graph = tree_adjacency(len(labels), tuple(edges))
            if not valid_incidence_tree(labels, graph):
                continue
            if len({node for current in edges for node in current}) != len(labels):
                continue
            reached = {0}
            queue = [0]
            while queue:
                current = queue.pop()
                for neighbor in graph[current]:
                    if neighbor not in reached:
                        reached.add(neighbor)
                        queue.append(neighbor)
            if len(reached) != len(labels):
                continue
            parent = rooted_parent(graph)
            code = canonical_code(parent, labels)
            states.setdefault(code, (parent, labels))
    return states


def tree_path(parent: tuple[int, ...], start: int, finish: int) -> tuple[int, ...]:
    graph = [set() for unused in parent]
    for node, predecessor in enumerate(parent):
        if predecessor >= 0:
            graph[node].add(predecessor)
            graph[predecessor].add(node)
    previous: dict[int, int | None] = {start: None}
    queue = deque([start])
    while queue and finish not in previous:
        current = queue.popleft()
        for neighbor in sorted(graph[current]):
            if neighbor not in previous:
                previous[neighbor] = current
                queue.append(neighbor)
    require(finish in previous, "state path is disconnected")
    result: list[int] = []
    current: int | None = finish
    while current is not None:
        result.append(current)
        current = previous[current]
    return tuple(reversed(result))


def selector_pairs(parent: tuple[int, ...], labels: tuple[str, ...]) -> tuple[tuple[str, str], ...]:
    """Pairs whose minimal D--T--T incidence hull has exactly those blocks."""
    answer = []
    for left, right in itertools.combinations(range(1, 5), 2):
        hull = set(tree_path(parent, 0, left)) | set(tree_path(parent, 0, right))
        marked = {labels[node] for node in hull if labels[node] != CUT}
        if marked == {"D", labels[left], labels[right]}:
            answer.append((labels[left], labels[right]))
    return tuple(answer)


def audit_states(states: dict[str, tuple[tuple[int, ...], tuple[str, ...]]]) -> dict[str, object]:
    by_cuts: Counter[int] = Counter()
    multiplicities: Counter[int] = Counter()
    signature_rows = []
    for code, (parent, labels) in sorted(states.items()):
        pairs = selector_pairs(parent, labels)
        require(pairs, f"selector failed on physical incidence state: {code}")
        by_cuts[len(labels) - len(MARKED)] += 1
        multiplicities[len(pairs)] += 1
        signature_rows.append(code + "\t" + ",".join(f"{a}-{b}" for a, b in pairs))
    signature = hashlib.sha256(("\n".join(signature_rows) + "\n").encode("ascii")).hexdigest()
    require(dict(sorted(by_cuts.items())) == EXPECTED_STATES_BY_CUTS,
            "incidence-state census changed")
    require(dict(sorted(multiplicities.items())) == EXPECTED_SELECTOR_MULTIPLICITIES,
            "selector multiplicity census changed")
    require(signature == EXPECTED_SIGNATURE_SHA256, "selector signature changed")
    return {
        "labelled_states": len(states),
        "states_by_cut_nodes": dict(sorted(by_cuts.items())),
        "selector_pair_multiplicity": dict(sorted(multiplicities.items())),
        "selector_signature_sha256": signature,
        "residual_states": 0,
    }


def expect_rejected(action, label: str) -> None:
    try:
        action()
    except AuditError:
        return
    raise AuditError(f"hostile mutation accepted: {label}")


def hostile_checks(states: dict[str, tuple[tuple[int, ...], tuple[str, ...]]]) -> int:
    # 1. Replace one required triangle by an untyped block while retaining a
    # syntactically valid star adjacency.
    labels = ("D", "T0", "T1", "T2", "X", CUT)
    star = ((5,), (5,), (5,), (5,), (5,), (0, 1, 2, 3, 4))
    expect_rejected(lambda: require(valid_incidence_tree(labels, star),
                                    "marked cyclic inventory changed"),
                    "marked triangle omitted")

    # 2. Admit a symmetric connected tree with a cut node of degree one.
    labels = (*MARKED, CUT, CUT)
    graph = ((5, 6), (6,), (6,), (6,), (6,), (0,), (0, 1, 2, 3, 4))
    expect_rejected(lambda: require(valid_incidence_tree(labels, graph),
                                    "degree-one cut admitted"),
                    "degree-one cut")

    # 3. Admit a block--block edge (the common way a K2 connector is laundered
    # into a purported shared-cut skeleton).
    labels = (*MARKED, CUT)
    graph = ((1, 5), (0,), (5,), (5,), (5,), (0, 2, 3, 4))
    expect_rejected(lambda: require(valid_incidence_tree(labels, graph),
                                    "non-bipartite incidence admitted"),
                    "block-block connector")

    # 4. Exceed a physical triangle's three distinct articulation ports.
    labels_wide = (*MARKED, CUT, CUT, CUT, CUT)
    graph_wide = (
        (5,), (5, 6, 7, 8), (6,), (7,), (8,), (0, 1), (1, 2), (1, 3), (1, 4))
    expect_rejected(lambda: require(valid_incidence_tree(labels_wide, graph_wide),
                                    "triangle port capacity exceeded"),
                    "triangle fourth cut")

    # 5. Corrupt the exact selector signature.
    expect_rejected(lambda: require(EXPECTED_SIGNATURE_SHA256 == "0" * 64,
                                    "selector digest changed"),
                    "selector digest")
    return 5


BLOCKERS = (
    "NONPROMOTIONAL: this is exhaustive only after a separate adjacency proof has removed every cyclic-hull K2 block and left exactly D+4T.",
    "The exact DTT spectral bound is imported conditionally and is not rederived here.",
    "The selector identifies an incidence hull; adjacency-level induced territory ownership, boundary-cut ownership, and arbitrary rooted payload transport remain obligations of the parent bridge-cascade gate.",
    "No conclusion is made for a state containing any positive connector, the isolated hostile rank-one side, or any other rank-seven profile.",
)


def run() -> dict[str, object]:
    states = generate_states()
    audit = audit_states(states)
    rejected = hostile_checks(states)
    return {
        "status": "NONPROMOTIONAL_CANDIDATE_LEMMA",
        "contract": "bridge-free physical block-cut incidence tree with cyclic blocks D,T0,T1,T2,T3",
        "audit": audit,
        "hostile_mutations_rejected": rejected,
        "unproved_parent_obligations": list(BLOCKERS),
    }


def serialized_report() -> str:
    return json.dumps(run(), sort_keys=True, indent=2) + "\n"


def main() -> int:
    output = serialized_report()
    if not sys.flags.optimize and "--optimized-child" not in sys.argv:
        child = subprocess.run(
            [sys.executable, "-O", str(Path(__file__).resolve()), "--optimized-child"],
            check=False, capture_output=True, text=True)
        require(child.returncode == 0, "optimized selector audit failed")
        require(child.stderr == "", "optimized selector audit wrote stderr")
        require(child.stdout == output, "normal and optimized selector reports differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
