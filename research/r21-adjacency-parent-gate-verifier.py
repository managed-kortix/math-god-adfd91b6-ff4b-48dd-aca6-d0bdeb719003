#!/usr/bin/env python3
"""NONPROMOTIONAL adjacency-level parent gate for the two DNN-open R21 rows.

This is a compact prototype, not a theorem claim.  It is the missing semantic
bridge between

  * research/r21-literal-cycle-typing-verifier.py (literal D=Theta(1,2,2) and
    five literal cycles, adjacency authenticated), and
  * research/r21-reduced-block-cut-hull-verifier.py (abstract decorated
    block-cut quotient and its credit ledger).

The gate reconstructs every object from materialized finite simple adjacency:

  1. the Tarjan edge-block decomposition and the graph rank;
  2. an arbitrary rank-two theta block Theta(1,2,r), r>=2, including the
     actual branch vertices and the three arm vertex sequences;
  3. the literal cycle inventory (five C3, or four C3 and one C5);
  4. for the Theta(1,2,r)+T^5 row, an internal long-arm opening and the
     complete physical owner class of the opened vertex;
  5. for the D+T^4+C5 row, the actual bridge that isolates the rank-one C5
     side, the D+4T complement, the first/rootmost cyclic-hull K2 bridges,
     the root shared-cut cluster, the least-depth D+T+T anchor, the cut-closed
     opened territories, and every vertex/rooted payload owner;
  6. the credit ledger under the named analytic packet inputs.

The output is a NONPROMOTIONAL report.  It proves no spectral packet bound and
makes no rank-seven theorem claim.  The only conclusions are conditional on
the explicitly listed analytic inputs, and the gate fails closed for every
physical profile outside the two narrow rows.

The Tarjan/adjacency primitives below are copied verbatim (with the same
require/fail-closed style) from the parent branch's literal-cycle typing gate so
that the prototype can be run without importing a file that is not on this
branch.  The design note records the intended import-once composition.
"""

from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from collections import Counter, deque
from dataclasses import dataclass, replace
from typing import Hashable, Iterable


REPO = Path(__file__).resolve().parents[1]


class GateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


Vertex = Hashable
Edge = frozenset[Vertex]


@dataclass(frozen=True)
class PhysicalGraph:
    vertices: frozenset[Vertex]
    edges: frozenset[Edge]


def edge(left: Vertex, right: Vertex) -> Edge:
    require(left != right, "simple graph cannot contain a loop")
    return frozenset((left, right))


def adjacency(vertices: frozenset[Vertex],
              edges: frozenset[Edge]) -> dict[Vertex, set[Vertex]]:
    require(type(vertices) is frozenset and vertices,
            "vertex set is not a nonempty frozenset")
    require(type(edges) is frozenset, "edge set is not a frozenset")
    graph = {vertex: set() for vertex in vertices}
    for current in edges:
        require(type(current) is frozenset and len(current) == 2,
                "malformed simple edge")
        left, right = tuple(current)
        require(left in graph and right in graph,
                "edge endpoint escaped vertex set")
        require(right not in graph[left], "duplicate simple edge")
        graph[left].add(right)
        graph[right].add(left)
    return graph


def connected(vertices: frozenset[Vertex], edges: frozenset[Edge]) -> bool:
    if not vertices:
        return False
    graph = adjacency(vertices, edges)
    root = min(vertices, key=repr)
    seen = {root}
    stack = [root]
    while stack:
        current = stack.pop()
        for neighbor in graph[current] - seen:
            seen.add(neighbor)
            stack.append(neighbor)
    return seen == set(vertices)


def components(vertices: frozenset[Vertex],
               edges: frozenset[Edge]) -> tuple[frozenset[Vertex], ...]:
    graph = adjacency(vertices, edges)
    unseen = set(vertices)
    answer = []
    while unseen:
        root = min(unseen, key=repr)
        seen = {root}
        stack = [root]
        while stack:
            current = stack.pop()
            for neighbor in graph[current] - seen:
                seen.add(neighbor)
                stack.append(neighbor)
        unseen -= seen
        answer.append(frozenset(seen))
    return tuple(answer)


def graph_rank(vertices: frozenset[Vertex], edges: frozenset[Edge]) -> int:
    return len(edges) - len(vertices) + len(components(vertices, edges))


def block_vertices(block: frozenset[Edge]) -> frozenset[Vertex]:
    require(type(block) is frozenset and block, "empty or malformed edge block")
    return frozenset().union(*block)


def block_rank(block: frozenset[Edge]) -> int:
    return len(block) - len(block_vertices(block)) + 1


def biconnected_edge_blocks(vertices: frozenset[Vertex],
                            edges: frozenset[Edge]) -> tuple[frozenset[Edge], ...]:
    """Tarjan edge-stack decomposition; a bridge is a singleton edge block."""
    graph = adjacency(vertices, edges)
    discovery: dict[Vertex, int] = {}
    low: dict[Vertex, int] = {}
    parent: dict[Vertex, Vertex] = {}
    stack: list[Edge] = []
    blocks: list[frozenset[Edge]] = []
    clock = 0

    def visit(current: Vertex) -> None:
        nonlocal clock
        clock += 1
        discovery[current] = low[current] = clock
        for neighbor in sorted(graph[current], key=repr):
            current_edge = edge(current, neighbor)
            if neighbor not in discovery:
                parent[neighbor] = current
                stack.append(current_edge)
                visit(neighbor)
                low[current] = min(low[current], low[neighbor])
                if low[neighbor] >= discovery[current]:
                    block: set[Edge] = set()
                    while True:
                        require(stack, "Tarjan edge stack underflow")
                        popped = stack.pop()
                        block.add(popped)
                        if popped == current_edge:
                            break
                    blocks.append(frozenset(block))
            elif parent.get(current) != neighbor and discovery[neighbor] < discovery[current]:
                stack.append(current_edge)
                low[current] = min(low[current], discovery[neighbor])

    for root in sorted(vertices, key=repr):
        if root not in discovery:
            visit(root)
            require(not stack, "Tarjan stack leaked between components")
    union = set().union(*blocks) if blocks else set()
    require(union == set(edges), "Tarjan blocks do not exhaust the physical edges")
    require(sum(map(len, blocks)) == len(edges),
            "Tarjan blocks duplicate an edge")
    return tuple(blocks)


def block_degrees(block: frozenset[Edge]) -> dict[Vertex, int]:
    vertices = block_vertices(block)
    return {vertex: sum(vertex in current for current in block) for vertex in vertices}


def authenticate_literal_cycle(block: frozenset[Edge]) -> int:
    vertices = block_vertices(block)
    degrees = block_degrees(block)
    require(len(vertices) >= 3, "cycle block has fewer than three vertices")
    require(len(block) == len(vertices), "rank-one block is not a literal cycle")
    require(all(value == 2 for value in degrees.values()),
            "rank-one block is not internally 2-regular")
    return len(vertices)


# ---------------------------------------------------------------------------
# Arbitrary rank-two theta typing
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ThetaData:
    block: frozenset[Edge]
    branch: tuple[Vertex, Vertex]
    arms: tuple[tuple[Vertex, ...], ...]      # includes both branch endpoints
    lengths: tuple[int, int, int]             # sorted
    long_arm_candidates: tuple[tuple[Vertex, ...], ...]

    @property
    def r(self) -> int:
        return self.lengths[2]


def _walk_path(block: frozenset[Edge], vertices: frozenset[Vertex],
               left: Vertex, right: Vertex) -> tuple[Vertex, ...] | None:
    """Return the unique path from left to right inside the induced block, or None."""
    allowed = frozenset({left, right} | set(vertices))
    graph = adjacency(allowed, frozenset(current for current in block
                                         if current <= allowed))
    if left == right:
        return (left,)
    previous: dict[Vertex, Vertex | None] = {left: None}
    queue = deque([left])
    while queue and right not in previous:
        current = queue.popleft()
        for neighbor in sorted(graph[current], key=repr):
            if neighbor not in previous:
                previous[neighbor] = current
                queue.append(neighbor)
    if right not in previous:
        return None
    answer = []
    current: Vertex | None = right
    while current is not None:
        answer.append(current)
        current = previous[current]
    return tuple(reversed(answer))


def authenticate_theta(block: frozenset[Edge]) -> ThetaData:
    """Authenticate a rank-two block as Theta(1,2,r), r>=2, from adjacency.

    The block must be 2-connected with exactly two degree-three vertices, the
    branch vertices must be joined by a literal unit edge, and deleting the
    branch vertices must leave exactly two path components of sizes one and
    r-1.  No label or symbolic theta type is read.
    """
    vertices = block_vertices(block)
    degrees = block_degrees(block)
    require(len(block) == len(vertices) + 1,
            "rank-two block does not satisfy |E|=|V|+1")
    require(block_rank(block) == 2, "block is not literally rank two")
    branches = tuple(sorted((vertex for vertex, degree in degrees.items() if degree == 3),
                            key=repr))
    require(len(branches) == 2, "theta block does not have exactly two branch vertices")
    require(all(degree in (2, 3) for degree in degrees.values()),
            "theta block has a vertex of degree outside {2,3}")
    x, y = branches
    require(edge(x, y) in block, "theta has no literal unit branch path")
    interiors = vertices - {x, y}
    inner_edges = frozenset(current for current in block
                            if current <= interiors)
    inner_components = components(interiors, inner_edges)
    require(len(inner_components) == 2,
            "deleting theta branch vertices did not leave two arms")
    arms: list[tuple[Vertex, ...]] = [(x, y)]
    sizes = []
    for component in inner_components:
        require(connected(component, inner_edges & frozenset(
            current for current in inner_edges if current <= component)),
            "theta arm is disconnected")
        arm_edges = frozenset(current for current in block if current <= component)
        require(len(arm_edges) == len(component) - 1,
                "theta arm is not a tree path")
        sub_degrees = {vertex: sum(vertex in current for current in arm_edges)
                       for vertex in component}
        require(all(value <= 2 for value in sub_degrees.values()),
                "theta arm has a branch")
        endpoints = tuple(sorted((vertex for vertex, value in sub_degrees.items()
                                  if value <= 1), key=repr))
        require(len(endpoints) == 2 or len(component) == 1,
                "theta arm does not have two endpoints")
        if len(component) == 1:
            only = next(iter(component))
            require(edge(x, only) in block and edge(y, only) in block,
                    "singleton theta arm is not a length-two path")
            arms.append((x, only, y))
            sizes.append(1)
            continue
        # Exactly one endpoint must be adjacent to x and one to y.
        near_x = tuple(vertex for vertex in endpoints if edge(x, vertex) in block)
        near_y = tuple(vertex for vertex in endpoints if edge(y, vertex) in block)
        require(len(near_x) == 1 and len(near_y) == 1 and near_x[0] != near_y[0],
                "theta arm endpoints are not attached to the two branch vertices")
        path = _walk_path(block, component, near_x[0], near_y[0])
        require(path is not None, "theta arm path reconstruction failed")
        require(len(path) == len(component), "theta arm path does not cover the component")
        require(edge(x, path[0]) in block and edge(y, path[-1]) in block,
                "theta arm is not joined to the branch vertices")
        require(all(sum(vertex in current for current in block) == 2
                    for vertex in path),
                "theta arm internal vertex is not degree two")
        arms.append((x, *path, y))
        sizes.append(len(component))
    require(Counter(sizes) == Counter((1, max(sizes))),
            "theta arms are not one length-two arm and one remaining arm")
    lengths = tuple(sorted(len(arm) - 1 for arm in arms))
    require(lengths[0] == 1 and lengths[1] == 2 and lengths[2] >= 2,
            "theta path lengths are not (1,2,r) with r>=2")
    require(sum(len(arm) - 1 for arm in arms) == len(block),
            "theta arm lengths do not account for every block edge")
    long_candidates = tuple(arm for arm in arms if len(arm) - 1 == lengths[2])
    if lengths[2] == 2:
        # The two length-two arms are symmetric; either may be opened.
        long_candidates = tuple(arm for arm in arms if len(arm) - 1 == 2)
    return ThetaData(block, (x, y), tuple(arms), lengths, long_candidates)


# ---------------------------------------------------------------------------
# Block-cut incidence tree
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BlockCutTree:
    blocks: tuple[frozenset[Edge], ...]
    block_index: dict[Edge, int]
    membership: dict[Vertex, tuple[int, ...]]
    graph: dict[tuple[str, object], set[tuple[str, object]]]
    block_node: dict[int, tuple[str, object]]
    cut_node: dict[Vertex, tuple[str, object]]


def build_block_cut_tree(graph: PhysicalGraph) -> BlockCutTree:
    blocks = biconnected_edge_blocks(graph.vertices, graph.edges)
    block_index = {}
    membership_lists: dict[Vertex, list[int]] = {v: [] for v in graph.vertices}
    for index, block in enumerate(blocks):
        for current in block:
            block_index[current] = index
        for vertex in block_vertices(block):
            membership_lists[vertex].append(index)
    membership = {vertex: tuple(sorted(indices))
                  for vertex, indices in membership_lists.items()}
    block_node = {index: ("B", index) for index in range(len(blocks))}
    cut_node = {vertex: ("C", vertex) for vertex, indices in membership.items()
                if len(indices) >= 2}
    incidence: dict[tuple[str, object], set[tuple[str, object]]] = {
        block_node[index]: set() for index in range(len(blocks))
    }
    for vertex, node in cut_node.items():
        incidence[node] = set()
        for index in membership[vertex]:
            block = block_node[index]
            incidence[node].add(block)
            incidence[block].add(node)
    require(connected(frozenset(incidence), frozenset(
        edge(left, right) for left in incidence for right in incidence[left]
        if repr(left) < repr(right))), "block-cut incidence graph is disconnected")
    edge_count = sum(len(neighbors) for neighbors in incidence.values()) // 2
    require(edge_count == len(incidence) - 1,
            "block-cut incidence graph is not a tree")
    return BlockCutTree(blocks, block_index, membership, incidence,
                        block_node, cut_node)


def tree_path(tree: BlockCutTree, start: tuple[str, object],
              finish: tuple[str, object]) -> tuple[tuple[str, object], ...]:
    previous: dict[tuple[str, object], tuple[str, object] | None] = {start: None}
    queue = deque([start])
    while queue and finish not in previous:
        current = queue.popleft()
        for neighbor in sorted(tree.graph[current], key=repr):
            if neighbor not in previous:
                previous[neighbor] = current
                queue.append(neighbor)
    require(finish in previous, "block-cut tree path is disconnected")
    answer = []
    current: tuple[str, object] | None = finish
    while current is not None:
        answer.append(current)
        current = previous[current]
    return tuple(reversed(answer))


def subtree_nodes(tree: BlockCutTree, root: tuple[str, object]) -> set[tuple[str, object]]:
    seen = {root}
    queue = [root]
    while queue:
        current = queue.pop()
        for neighbor in tree.graph[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return seen


# ---------------------------------------------------------------------------
# R21 inventory
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class R21Inventory:
    theta: ThetaData
    theta_block: frozenset[Edge]
    cycles: tuple[frozenset[Edge], ...]
    cycle_lengths: tuple[int, ...]
    bridge_blocks: tuple[frozenset[Edge], ...]
    rank: int

    @property
    def family(self) -> str:
        if self.cycle_lengths == (3, 3, 3, 3, 3):
            return "THETA_PLUS_T5"
        if self.cycle_lengths == (3, 3, 3, 3, 5):
            return "D_PLUS_T4_C5"
        raise GateError("cycle inventory is not one of the two DNN-open rows")


def authenticate_r21(graph: PhysicalGraph) -> R21Inventory:
    require(type(graph) is PhysicalGraph,
            "certificate contains no materialized adjacency")
    adjacency(graph.vertices, graph.edges)
    require(connected(graph.vertices, graph.edges), "physical graph is disconnected")
    require(graph_rank(graph.vertices, graph.edges) == 7,
            "physical graph does not have rank seven")
    blocks = biconnected_edge_blocks(graph.vertices, graph.edges)
    ranks = tuple(block_rank(block) for block in blocks)
    require(all(rank >= 0 for rank in ranks), "Tarjan block has negative rank")
    require(all(len(block) == 1 for block, rank in zip(blocks, ranks) if rank == 0),
            "rank-zero Tarjan block is not a physical bridge")
    cyclic = tuple(block for block, rank in zip(blocks, ranks) if rank > 0)
    cyclic_ranks = tuple(sorted(block_rank(block) for block in cyclic))
    require(cyclic_ranks == (1, 1, 1, 1, 1, 2),
            "positive-rank inventory is not one rank-two plus five rank-one blocks")
    theta_blocks = tuple(block for block in cyclic if block_rank(block) == 2)
    cycle_blocks = tuple(block for block in cyclic if block_rank(block) == 1)
    require(len(theta_blocks) == 1 and len(cycle_blocks) == 5,
            "R21 cyclic block cardinality changed")
    theta = authenticate_theta(theta_blocks[0])
    lengths = tuple(sorted(authenticate_literal_cycle(block) for block in cycle_blocks))
    if lengths != (3, 3, 3, 3, 3) and lengths != (3, 3, 3, 3, 5):
        raise GateError(
            "cycle inventory is DNN-closed or outside the two DNN-open R21 rows")
    return R21Inventory(theta, theta_blocks[0], cycle_blocks, lengths,
                        tuple(block for block, rank in zip(blocks, ranks) if rank == 0),
                        7)


def exact_dnn_witness(inventory: R21Inventory) -> str:
    """Check the exact integer brackets for the two DNN-open rows.

    The radical identities and the Delta-classification are pinned analytic
    inputs; only the final integer brackets are checked here, matching the
    parent literal-cycle typing certificate.
    """
    if inventory.family == "THETA_PLUS_T5":
        if inventory.theta.r == 2:
            require(17 > 9, "exact r=2 witness 17>9 failed")
            return ("Delta(1,2,2)=(sqrt(17)-1)/2>1 because 17>9; "
                    "Delta+5-6>0")
        return ("Delta(1,2,r)>1 for r>=3 by the pinned exact "
                "Delta-classification; Delta+5-6>0")
    require(425 > 361, "exact q=5 witness 425>361 failed")
    return ("literal D: (sqrt(17)+5-4sqrt(5))/2>0 because "
            "sqrt(17)+5>4sqrt(5), squared twice to 425>361")


# ---------------------------------------------------------------------------
# Small deterministic utilities
# ---------------------------------------------------------------------------


def canonical_vertices(vertices: Iterable[Vertex]) -> tuple[Vertex, ...]:
    return tuple(sorted(vertices, key=repr))


def block_label(block: frozenset[Edge]) -> frozenset[Vertex]:
    return block_vertices(block)


def graph_on(graph: PhysicalGraph, vertices: frozenset[Vertex]) -> PhysicalGraph:
    edges = frozenset(current for current in graph.edges if current <= vertices)
    return PhysicalGraph(vertices, edges)


def induced_blocks(graph: PhysicalGraph,
                   vertices: frozenset[Vertex]) -> tuple[frozenset[Edge], ...]:
    return biconnected_edge_blocks(vertices,
                                   frozenset(current for current in graph.edges
                                             if current <= vertices))


def positive_rank_blocks(graph: PhysicalGraph,
                         vertices: frozenset[Vertex]) -> tuple[frozenset[Edge], ...]:
    return tuple(block for block in induced_blocks(graph, vertices)
                 if block_rank(block) > 0)


def all_blocks_triangles(graph: PhysicalGraph, vertices: frozenset[Vertex]) -> int:
    """Return the number of triangle blocks; fail if a cycle block is not C3."""
    count = 0
    for block in induced_blocks(graph, vertices):
        if block_rank(block) == 0:
            require(len(block) == 1, "rank-zero block is not a bridge")
            continue
        require(block_rank(block) == 1, "positive-rank block is not unicyclic")
        length = authenticate_literal_cycle(block)
        require(length == 3, "triangular territory contains a non-triangle cycle")
        count += 1
    return count


def is_tree(graph: PhysicalGraph, vertices: frozenset[Vertex]) -> bool:
    if not vertices:
        return False
    return (connected(vertices, frozenset(c for c in graph.edges if c <= vertices))
            and len([c for c in graph.edges if c <= vertices]) == len(vertices) - 1)


def unique_attachment(graph: PhysicalGraph, vertices: frozenset[Vertex],
                      core: frozenset[Vertex]) -> Vertex:
    """A connected off-core component must meet the core in exactly one vertex."""
    require(vertices and vertices.isdisjoint(core), "malformed off-core component")
    graph_adj = adjacency(graph.vertices, graph.edges)
    neighbors = set()
    for vertex in vertices:
        neighbors.update(graph_adj[vertex] & core)
    require(len(neighbors) == 1,
            "acyclic payload component does not have a unique physical root")
    return next(iter(neighbors))


def fingerprint(vertices: frozenset[Vertex],
                edges: frozenset[Edge]) -> str:
    payload = {
        "vertices": sorted(repr(vertex) for vertex in vertices),
        "edges": sorted(tuple(sorted(repr(endpoint) for endpoint in current))
                        for current in edges),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


# ---------------------------------------------------------------------------
# Physical shared-cut cluster derived from adjacency
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PhysicalCut:
    members: tuple[str, ...]
    ports: tuple[tuple[str, int], ...]
    vertex: Vertex


@dataclass(frozen=True)
class PhysicalCluster:
    root_triangles: tuple[str, ...]
    cuts: tuple[PhysicalCut, ...]
    labels: dict[str, frozenset[Edge]]
    vertices: frozenset[Vertex]
    depths: dict[str, int]


def derive_root_cluster(graph: PhysicalGraph, theta_block: frozenset[Edge],
                        root_triangles: tuple[frozenset[Edge], ...]) -> PhysicalCluster:
    """Derive the physical shared-cut root cluster and its literal port data."""
    blocks = (theta_block, *root_triangles)
    labels: dict[str, frozenset[Edge]] = {"D": theta_block}
    for index, block in enumerate(root_triangles):
        labels[f"T{index}"] = block
    require(len(set(map(block_vertices, blocks))) == len(blocks),
            "root cluster contains a duplicate block")
    block_vertex_sets = {name: block_vertices(block) for name, block in labels.items()}
    cut_vertices = []
    for vertex in graph.vertices:
        members = tuple(sorted(name for name, verts in block_vertex_sets.items()
                               if vertex in verts))
        if len(members) >= 2:
            cut_vertices.append((vertex, members))
    incidence: dict[tuple[str, object], set[tuple[str, object]]] = {
        ("B", name): set() for name in labels
    }
    for vertex, members in cut_vertices:
        node = ("C", vertex)
        incidence[node] = set()
        for name in members:
            incidence[("B", name)].add(node)
            incidence[node].add(("B", name))
    nodes = frozenset(incidence)
    edge_count = sum(len(neighbors) for neighbors in incidence.values()) // 2
    require(edge_count == len(nodes) - 1,
            "physical root-cluster incidence graph is not a tree")
    reached = {("B", "D")}
    queue = list(reached)
    while queue:
        current = queue.pop()
        for neighbor in incidence[current]:
            if neighbor not in reached:
                reached.add(neighbor)
                queue.append(neighbor)
    require(reached == set(nodes), "physical root-cluster incidence graph is disconnected")
    depths: dict[str, int] = {"D": 0}
    queue = deque([("B", "D")])
    depth_by_node = {("B", "D"): 0}
    while queue:
        current = queue.popleft()
        for neighbor in incidence[current]:
            if neighbor not in depth_by_node:
                depth_by_node[neighbor] = depth_by_node[current] + 1
                queue.append(neighbor)
    for name in labels:
        depths[name] = depth_by_node[("B", name)]
    cuts = []
    used_ports: set[tuple[str, int]] = set()
    for vertex, members in sorted(cut_vertices, key=lambda item: repr(item[0])):
        ports = []
        for name in members:
            ordering = canonical_vertices(block_vertex_sets[name])
            port = ordering.index(vertex)
            require((name, port) not in used_ports,
                    "one physical block port was reused by two cut nodes")
            used_ports.add((name, port))
            ports.append((name, port))
        cuts.append(PhysicalCut(members, tuple(ports), vertex))
    cluster_vertices = frozenset().union(*block_vertex_sets.values())
    return PhysicalCluster(tuple(sorted(labels.keys() - {"D"})), tuple(cuts),
                           labels, cluster_vertices, depths)


def select_anchor_pair(cluster: PhysicalCluster) -> tuple[str, str]:
    require(len(cluster.root_triangles) >= 2,
            "DTT anchor selection needs two root triangles")
    pair = tuple(sorted(cluster.root_triangles,
                        key=lambda name: (cluster.depths[name], name))[:2])
    require(len(pair) == 2, "least-depth anchor selection failed")
    return pair  # type: ignore[return-value]


def incident_cuts(cluster: PhysicalCluster, name: str) -> set[Vertex]:
    return {cut.vertex for cut in cluster.cuts if name in cut.members}


def cut_members(cluster: PhysicalCluster, vertex: Vertex) -> tuple[str, ...]:
    for cut in cluster.cuts:
        if cut.vertex == vertex:
            return cut.members
    raise GateError("vertex is not a represented root-cluster cut")


def anchor_hull(cluster: PhysicalCluster, pair: tuple[str, str]) -> set[str]:
    """Retained block labels in the minimal incidence hull of D and the anchors."""
    # Build a small labelled adjacency of block/cut nodes.
    adjacency_nodes: dict[tuple[str, object], set[tuple[str, object]]] = {
        ("B", name): set() for name in cluster.labels
    }
    for cut in cluster.cuts:
        node = ("C", cut.vertex)
        adjacency_nodes[node] = set()
        for name in cut.members:
            adjacency_nodes[("B", name)].add(node)
            adjacency_nodes[node].add(("B", name))

    def path(start, finish):
        previous = {start: None}
        queue = deque([start])
        while queue and finish not in previous:
            current = queue.popleft()
            for neighbor in adjacency_nodes[current]:
                if neighbor not in previous:
                    previous[neighbor] = current
                    queue.append(neighbor)
        require(finish in previous, "root cluster path is disconnected")
        answer = []
        current = finish
        while current is not None:
            answer.append(current)
            current = previous[current]
        return tuple(reversed(answer))

    hull = set(path(("B", "D"), ("B", pair[0])))
    hull |= set(path(("B", "D"), ("B", pair[1])))
    return {node[1] for node in hull if node[0] == "B"}


def cluster_incidence(cluster: PhysicalCluster) -> dict[tuple[str, object], set[tuple[str, object]]]:
    incidence: dict[tuple[str, object], set[tuple[str, object]]] = {
        ("B", name): set() for name in cluster.labels
    }
    for cut in cluster.cuts:
        node = ("C", cut.vertex)
        incidence[node] = set()
        for name in cut.members:
            incidence[("B", name)].add(node)
            incidence[node].add(("B", name))
    return incidence


def derive_opened_groups(graph: PhysicalGraph, cluster: PhysicalCluster,
                         pair: tuple[str, str]) -> tuple[
        frozenset[Vertex],
        tuple[tuple[tuple[str, ...], frozenset[Vertex]], ...],
        tuple[tuple[Vertex, str], ...]]:
    """Return the upstream core, the opened core territories, and the frontier.

    The cut-closed upstream core S contains D, the two least-depth anchor
    triangles, and every represented cut incident with one of those three
    retained blocks.  Every incidence edge from a cut in S to an unselected
    root triangle is cut.  The whole far-side block component, translated to
    original vertices and with the upstream cut removed, is one opened
    territory.  A nested unselected triangle is therefore part of the first
    boundary's territory, never a second independent cut.
    """
    hull = anchor_hull(cluster, pair)
    require(hull == {"D", pair[0], pair[1]},
            "minimal DTT hull contains a third marked triangle")
    retained = {"D", pair[0], pair[1]}
    closure_cuts = set()
    for name in retained:
        closure_cuts.update(incident_cuts(cluster, name))
    unselected = {name for name in cluster.root_triangles if name not in pair}
    incidence = cluster_incidence(cluster)
    upstream = frozenset().union(*(block_vertices(cluster.labels[name])
                                   for name in retained))
    groups: list[tuple[tuple[str, ...], frozenset[Vertex]]] = []
    frontier: list[tuple[Vertex, str]] = []
    covered: set[Vertex] = set()
    for cut_vertex in sorted(closure_cuts, key=repr):
        cut_node = ("C", cut_vertex)
        for block_node in sorted(incidence[cut_node], key=repr):
            if block_node[0] != "B":
                continue
            name = block_node[1]
            if name in retained:
                continue
            require(name in unselected,
                    "closure boundary reached a block outside the root triangles")
            # Explore the far side of the incidence edge (cut, name).
            reached = {block_node}
            queue = [block_node]
            while queue:
                current = queue.pop()
                for neighbor in incidence[current]:
                    if {current, neighbor} == {block_node, cut_node}:
                        continue
                    if neighbor not in reached:
                        reached.add(neighbor)
                        queue.append(neighbor)
            group_blocks = tuple(sorted(node[1] for node in reached
                                        if node[0] == "B"))
            require(set(group_blocks) <= unselected and name in group_blocks,
                    "opened frontier reached a retained block or the D block")
            group_vertices = frozenset().union(
                *(block_vertices(cluster.labels[other]) for other in group_blocks)
            ) - {cut_vertex}
            require(group_vertices and group_vertices.isdisjoint(covered),
                    "opened territories overlap or are empty")
            covered |= group_vertices
            groups.append((group_blocks, group_vertices))
            frontier.append((cut_vertex, name))
    opened_union = frozenset().union(*(group[1] for group in groups)) if groups else frozenset()
    require(opened_union.isdisjoint(upstream),
            "opened core overlaps the upstream core")
    require(opened_union | upstream == cluster.vertices,
            "opened and upstream cores do not cover the root cluster")
    require(Counter(name for group, unused_vertices in groups for name in group)
            == Counter(unselected),
            "opened block groups are not disjoint and exhaustive")
    return upstream, tuple(groups), tuple(frontier)



# ---------------------------------------------------------------------------
# Fixture builders (positive and hostile physical adjacency)
# ---------------------------------------------------------------------------


def theta_core(r: int) -> tuple[set[Vertex], set[Edge], dict[str, Vertex], list[Vertex]]:
    """Build a literal Theta(1,2,r): x,y; arms x-y, x-a-y, x-p1-...-p_{r-1}-y."""
    require(type(r) is int and r >= 2, "theta fixture needs r>=2")
    vertices: set[Vertex] = {"x", "y", "a"}
    edges: set[Edge] = {edge("x", "y"), edge("x", "a"), edge("a", "y")}
    path: list[Vertex] = []
    for index in range(1, r):
        name = f"p{index}"
        vertices.add(name)
        path.append(name)
    sequence = ("x", *path, "y")
    edges.update(edge(left, right) for left, right in zip(sequence, sequence[1:]))
    return vertices, edges, {"x": "x", "y": "y", "a": "a"}, path


def attach_triangle(vertices: set[Vertex], edges: set[Edge], root: Vertex,
                    tag: str) -> tuple[Vertex, Vertex]:
    left, right = f"{tag}:u", f"{tag}:v"
    require(left not in vertices and right not in vertices,
            "triangle fixture label collision")
    vertices.update((left, right))
    edges.update((edge(root, left), edge(left, right), edge(right, root)))
    return left, right


def theta_plus_triangles(r: int,
                         attachments: tuple[tuple[Vertex, int], ...]) -> PhysicalGraph:
    """Attach literal triangles at named theta vertices by shared cuts."""
    vertices, edges, names, path = theta_core(r)
    index = 0
    for root, count in attachments:
        require(root in vertices, "triangle attachment is not a theta vertex")
        for _ in range(count):
            attach_triangle(vertices, edges, root, f"T{index}")
            index += 1
    require(index == 5, "R21 fixture needs five external triangles")
    return PhysicalGraph(frozenset(vertices), frozenset(edges))


def d_plus_t4_c5_isolated(attach_at: Vertex = "x") -> PhysicalGraph:
    """D+T^4 sharing a cut, plus a literal C5 isolated by one actual bridge."""
    vertices, edges, names, path = theta_core(2)
    for index in range(4):
        attach_triangle(vertices, edges, "x", f"T{index}")
    require(attach_at in vertices, "C5 bridge root is not in the D+4T side")
    c5 = ("w", "c1", "c2", "c3", "c4")
    vertices.update(c5)
    edges.update((edge("w", "c1"), edge("c1", "c2"), edge("c2", "c3"),
                  edge("c3", "c4"), edge("c4", "w")))
    edges.add(edge(attach_at, "w"))
    return PhysicalGraph(frozenset(vertices), frozenset(edges))


def d_plus_t4_c5_shared() -> PhysicalGraph:
    """The parent typing gate's own q=5 fixture: C5 shares the D cut."""
    vertices, edges, names, path = theta_core(2)
    for index in range(4):
        attach_triangle(vertices, edges, "x", f"T{index}")
    c5 = ("c1", "c2", "c3", "c4")
    vertices.update(c5)
    edges.update((edge("x", "c1"), edge("c1", "c2"), edge("c2", "c3"),
                  edge("c3", "c4"), edge("c4", "x")))
    return PhysicalGraph(frozenset(vertices), frozenset(edges))


def d_plus_t3_c5_plus_t_isolated() -> PhysicalGraph:
    """C5 side has rank two (C5 plus a triangle), so no rank-one C5 side."""
    vertices, edges, names, path = theta_core(2)
    for index in range(3):
        attach_triangle(vertices, edges, "x", f"T{index}")
    c5 = ("w", "c1", "c2", "c3", "c4")
    vertices.update(c5)
    edges.update((edge("w", "c1"), edge("c1", "c2"), edge("c2", "c3"),
                  edge("c3", "c4"), edge("c4", "w")))
    attach_triangle(vertices, edges, "w", "far")
    edges.add(edge("x", "w"))
    return PhysicalGraph(frozenset(vertices), frozenset(edges))


def d_plus_5t_shared() -> PhysicalGraph:
    """D + five triangles all sharing the D cut vertex x (root cluster k=5)."""
    return theta_plus_triangles(2, (("x", 5),))


def d_plus_5t_chain() -> PhysicalGraph:
    """D with a single bridge chain carrying all five triangles (root k=0)."""
    vertices, edges, names, path = theta_core(2)
    previous = "x"
    for index in range(5):
        cut = f"BC{index}"
        vertices.add(cut)
        edges.add(edge(previous, cut))
        attach_triangle(vertices, edges, cut, f"T{index}")
        previous = f"T{index}:u"
    return PhysicalGraph(frozenset(vertices), frozenset(edges))


def d_plus_5t_two_chains_and_shared() -> PhysicalGraph:
    """D shares one cut with T0; two bridge chains carry the other four."""
    vertices, edges, names, path = theta_core(2)
    attach_triangle(vertices, edges, "x", "T0")
    previous = "x"
    for index in range(1, 3):
        cut = f"BC{index}"
        vertices.add(cut)
        edges.add(edge(previous, cut))
        attach_triangle(vertices, edges, cut, f"T{index}")
        previous = f"T{index}:u"
    previous = "y"
    for index in range(3, 5):
        cut = f"BC{index}"
        vertices.add(cut)
        edges.add(edge(previous, cut))
        attach_triangle(vertices, edges, cut, f"T{index}")
        previous = f"T{index}:u"
    return PhysicalGraph(frozenset(vertices), frozenset(edges))


def d_plus_t4_c5_behind_tree_chain() -> PhysicalGraph:
    """C5 hangs behind a two-bridge tree chain; several isolating bridges exist."""
    vertices, edges, names, path = theta_core(2)
    for index in range(4):
        attach_triangle(vertices, edges, "x", f"T{index}")
    vertices.update(("b1", "t", "w", "c1", "c2", "c3", "c4"))
    edges.update((edge("x", "b1"), edge("b1", "t"), edge("t", "w"),
                  edge("w", "c1"), edge("c1", "c2"), edge("c2", "c3"),
                  edge("c3", "c4"), edge("c4", "w")))
    return PhysicalGraph(frozenset(vertices), frozenset(edges))


def d_plus_5t_nested() -> PhysicalGraph:
    """Five root triangles with one nested chain: D-x-T0-z-{T1,T2}, plus T3,T4 at x."""
    vertices, edges, names, path = theta_core(2)
    attach_triangle(vertices, edges, "x", "T0")
    attach_triangle(vertices, edges, "T0:u", "T1")
    attach_triangle(vertices, edges, "T0:u", "T2")
    attach_triangle(vertices, edges, "x", "T3")
    attach_triangle(vertices, edges, "x", "T4")
    return PhysicalGraph(frozenset(vertices), frozenset(edges))


def d_plus_t4_c5_with_hull_bridge() -> PhysicalGraph:
    """C5 bridge-isolated from an H with D+T0 direct and a bridge chain T1-T2-T3."""
    vertices, edges, names, path = theta_core(2)
    attach_triangle(vertices, edges, "x", "T0")
    previous = "x"
    for index in range(1, 4):
        cut = f"BC{index}"
        vertices.add(cut)
        edges.add(edge(previous, cut))
        attach_triangle(vertices, edges, cut, f"T{index}")
        previous = f"T{index}:u"
    vertices.update(("w", "c1", "c2", "c3", "c4"))
    edges.update((edge("w", "c1"), edge("c1", "c2"), edge("c2", "c3"),
                  edge("c3", "c4"), edge("c4", "w"), edge("a", "w")))
    return PhysicalGraph(frozenset(vertices), frozenset(edges))


def subdivide_edge(graph: PhysicalGraph, target: Edge, name: Vertex) -> PhysicalGraph:
    require(target in graph.edges and name not in graph.vertices,
            "subdivision fixture is malformed")
    left, right = tuple(target)
    edges = set(graph.edges)
    edges.remove(target)
    edges.update((edge(left, name), edge(name, right)))
    return PhysicalGraph(graph.vertices | frozenset((name,)), frozenset(edges))


def add_chord(graph: PhysicalGraph, left: Vertex, right: Vertex) -> PhysicalGraph:
    addition = edge(left, right)
    require(addition not in graph.edges and addition <= graph.vertices,
            "chord fixture is malformed")
    return PhysicalGraph(graph.vertices, graph.edges | frozenset((addition,)))


# ---------------------------------------------------------------------------
# Actual C5-side orientation and first cyclic-hull bridge analysis
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class C5Split:
    c5_block: frozenset[Edge]
    bridge: Edge
    p_side: frozenset[Vertex]
    h_side: frozenset[Vertex]
    h_graph: PhysicalGraph
    p_graph: PhysicalGraph
    candidate_bridges: tuple[Edge, ...] = ()


def orient_c5_side(graph: PhysicalGraph, inventory: R21Inventory) -> C5Split:
    """Find the actual bridge that isolates the rank-one C5 side."""
    require(inventory.cycle_lengths == (3, 3, 3, 3, 5),
            "C5 orientation called on a non-C5 row")
    require(inventory.theta.lengths == (1, 2, 2),
            "the D+T^4+C5 row requires the literal diamond D")
    c5_blocks = tuple(block for block in inventory.cycles
                      if authenticate_literal_cycle(block) == 5)
    require(len(c5_blocks) == 1, "C5 row does not have one literal C5 block")
    c5_block = c5_blocks[0]
    c5_vertex = min(block_vertices(c5_block), key=repr)
    d_vertex = min(block_vertices(inventory.theta_block), key=repr)
    candidates: list[C5Split] = []
    for bridge_block in inventory.bridge_blocks:
        require(len(bridge_block) == 1, "rank-zero block is not a single edge")
        bridge = next(iter(bridge_block))
        remaining = PhysicalGraph(graph.vertices, graph.edges - frozenset((bridge,)))
        parts = components(remaining.vertices, remaining.edges)
        require(len(parts) == 2, "a bridge did not split the graph into two sides")
        p_side = next((part for part in parts if c5_vertex in part), None)
        if p_side is None:
            continue
        h_side = next(part for part in parts if part is not p_side)
        if d_vertex not in h_side:
            continue
        if graph_rank(p_side, frozenset(c for c in remaining.edges if c <= p_side)) != 1:
            continue
        if graph_rank(h_side, frozenset(c for c in remaining.edges if c <= h_side)) != 6:
            continue
        p_blocks = tuple(block for block in biconnected_edge_blocks(
            p_side, frozenset(c for c in graph.edges if c <= p_side))
                         if block_rank(block) > 0)
        require(len(p_blocks) == 1, "C5 side has more than one positive-rank block")
        require(block_vertices(p_blocks[0]) == block_vertices(c5_block)
                and p_blocks[0] == c5_block,
                "C5 side's unique positive-rank block is not the literal C5")
        h_graph = graph_on(graph, h_side)
        h_positive = positive_rank_blocks(h_graph, h_side)
        h_ranks = tuple(sorted(block_rank(block) for block in h_positive))
        require(h_ranks == (1, 1, 1, 1, 2),
                "H side is not one rank-two plus four rank-one blocks")
        require(inventory.theta_block in h_positive,
                "H side does not retain the physical theta block")
        h_cycles = tuple(block for block in h_positive if block_rank(block) == 1)
        require(len(h_cycles) == 4 and
                all(authenticate_literal_cycle(block) == 3 for block in h_cycles),
                "H side's rank-one blocks are not four literal triangles")
        candidates.append(C5Split(c5_block, bridge, p_side, h_side,
                                  h_graph, graph_on(graph, p_side)))
    require(candidates,
            "no actual bridge isolates a rank-one side whose unique cycle is the C5")
    # Several bridges may isolate a rank-one C5 side when the C5 hangs behind a
    # tree chain.  Any of them is a legal oriented split; choose the one whose
    # C5 side is smallest so that the H side keeps the maximal tree payload.
    candidates.sort(key=lambda split: (len(split.p_side),
                                       tuple(sorted(map(repr, split.bridge)))))
    chosen = candidates[0]
    crossing = tuple(c for c in graph.edges
                     if (c & chosen.p_side) and (c & chosen.h_side))
    require(crossing == (chosen.bridge,),
            "C5 and H sides have more than one crossing edge")
    return replace(chosen,
                   candidate_bridges=tuple(split.bridge for split in candidates))


@dataclass(frozen=True)
class HullBridge:
    bridge: Edge
    away_side: frozenset[Vertex]
    triangles: tuple[frozenset[Edge], ...]


@dataclass(frozen=True)
class HullSplit:
    h_graph: PhysicalGraph
    theta_block: frozenset[Edge]
    triangles: tuple[frozenset[Edge], ...]
    root_triangles: tuple[frozenset[Edge], ...]
    bridge_groups: tuple[HullBridge, ...]
    root_side: frozenset[Vertex]


def first_hull_bridges(h_graph: PhysicalGraph, theta_block: frozenset[Edge],
                       triangles: tuple[frozenset[Edge], ...]) -> HullSplit:
    """Cut the first actual K2 bridge on every D-to-triangle cyclic-hull route."""
    tree = build_block_cut_tree(h_graph)
    d_node = ("B", tree.block_index[next(iter(theta_block))])
    require(tree.blocks[tree.block_index[next(iter(theta_block))]] == theta_block,
            "theta block is not a Tarjan block of H")
    t_nodes = []
    for block in triangles:
        require(block in tree.blocks, "external triangle is not a Tarjan block of H")
        t_nodes.append(("B", tree.block_index[next(iter(block))]))
    first: dict[int, list[frozenset[Edge]]] = {}
    root_triangles: list[frozenset[Edge]] = []
    for block, node in zip(triangles, t_nodes):
        path = tree_path(tree, d_node, node)
        first_bridge_index = None
        for item in path:
            if item[0] == "B":
                candidate = tree.blocks[item[1]]
                if block_rank(candidate) == 0:
                    first_bridge_index = item[1]
                    break
        if first_bridge_index is None:
            root_triangles.append(block)
        else:
            first[first_bridge_index] = first.get(first_bridge_index, []) + [block]
    d_vertex = min(block_vertices(theta_block), key=repr)
    groups: list[HullBridge] = []
    away_union: set[Vertex] = set()
    for index, mapped in sorted(first.items()):
        bridge_block = tree.blocks[index]
        require(len(bridge_block) == 1, "first cyclic-hull block is not a bridge")
        bridge = next(iter(bridge_block))
        remaining = PhysicalGraph(h_graph.vertices, h_graph.edges - frozenset((bridge,)))
        parts = components(remaining.vertices, remaining.edges)
        require(len(parts) == 2, "first hull bridge did not split H into two sides")
        away = next(part for part in parts if d_vertex not in part)
        require(not (set(away) & away_union),
                "first-hull-bridge away components overlap")
        away_union |= set(away)
        away_graph = graph_on(h_graph, frozenset(away))
        away_positive = positive_rank_blocks(away_graph, frozenset(away))
        require(tuple(sorted(away_positive,
                             key=lambda b: min(map(repr, block_vertices(b)))))
                == tuple(sorted(mapped,
                                key=lambda b: min(map(repr, block_vertices(b))))),
                "away component's positive-rank blocks are not exactly its mapped triangles")
        require(all(block_rank(block) == 1 and authenticate_literal_cycle(block) == 3
                    for block in away_positive),
                "first-hull-bridge away component is not all-triangle")
        require(not (bridge <= frozenset(away)),
                "first-hull bridge was not cut at the away boundary")
        groups.append(HullBridge(bridge, frozenset(away), tuple(mapped)))
    for outer in groups:
        for inner in groups:
            if outer is inner:
                continue
            require(not (inner.bridge <= outer.away_side),
                    "a first hull bridge lies inside another away component")
    root_side = h_graph.vertices - frozenset(away_union)
    require(connected(root_side, frozenset(c for c in h_graph.edges if c <= root_side)),
            "root side after first-hull-bridge cuts is disconnected")
    require(len(root_triangles) + sum(len(group.triangles) for group in groups)
            == len(triangles),
            "root and first-hull-bridge triangle groups do not partition the triangles")
    require(len(set(root_triangles)) == len(root_triangles),
            "root triangle list contains a duplicate")
    return HullSplit(h_graph, theta_block, triangles, tuple(root_triangles),
                     tuple(groups), frozenset(root_side))


# ---------------------------------------------------------------------------
# Original-vertex territory ownership and conservative credit ledger
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Territory:
    label: str
    kind: str
    vertices: frozenset[Vertex]
    core_blocks: tuple[frozenset[Edge], ...]
    credit: int
    strict: bool


def payload_assignments(graph: PhysicalGraph, root_side: frozenset[Vertex],
                        core_vertices: frozenset[Vertex],
                        core_owner: dict[Vertex, str]) -> dict[str, frozenset[Vertex]]:
    """Assign each maximal acyclic off-core component by its unique root."""
    require(core_vertices <= root_side, "core vertices escaped the root side")
    off_core = root_side - core_vertices
    additions: dict[str, set[Vertex]] = {label: set() for label in set(core_owner.values())}
    if not off_core:
        return {label: frozenset() for label in additions}
    off_edges = frozenset(current for current in graph.edges if current <= off_core)
    graph_adj = adjacency(graph.vertices, graph.edges)
    for component in components(off_core, off_edges):
        require(connected(component, frozenset(c for c in off_edges if c <= component)),
                "off-core payload component is disconnected")
        neighbors = set()
        for vertex in component:
            neighbors.update(graph_adj[vertex] & core_vertices)
        require(len(neighbors) == 1,
                "acyclic payload component does not have a unique physical root")
        owner = core_owner[next(iter(neighbors))]
        additions[owner].update(component)
    return {label: frozenset(vertices) for label, vertices in additions.items()}


def verify_territory(graph: PhysicalGraph, territory: Territory) -> None:
    require(territory.vertices, "empty territory")
    edges = frozenset(current for current in graph.edges
                      if current <= territory.vertices)
    require(connected(territory.vertices, edges),
            f"territory {territory.label} is not connected")
    positive = positive_rank_blocks(graph, territory.vertices)
    actual = tuple(sorted(block_rank(block) for block in positive))
    expected = tuple(sorted(block_rank(block) for block in territory.core_blocks))
    require(actual == expected,
            f"territory {territory.label} positive-rank block inventory changed")


def bridge_free_positive_paths(graph: PhysicalGraph, vertices: frozenset[Vertex],
                               blocks: tuple[frozenset[Edge], ...]) -> None:
    """Every path between the named positive-rank blocks must use no bridge."""
    tree = build_block_cut_tree(graph_on(graph, vertices))
    require(all(block in tree.blocks for block in blocks),
            "named packet block is not a Tarjan block of the territory")
    nodes = [("B", tree.block_index[next(iter(block))]) for block in blocks]
    for left_index in range(len(nodes)):
        for right_index in range(left_index + 1, len(nodes)):
            path = tree_path(tree, nodes[left_index], nodes[right_index])
            for item in path:
                if item[0] == "B":
                    require(block_rank(tree.blocks[item[1]]) > 0,
                            "DTT packet path contains a positive bridge connector")


def build_hull_territories(graph: PhysicalGraph, h_graph: PhysicalGraph,
                           theta_block: frozenset[Edge],
                           triangles: tuple[frozenset[Edge], ...],
                           threshold: int) -> tuple[
        tuple[Territory, ...], tuple[Territory, ...], dict[str, object]]:
    """Derive every H territory from adjacency and check the threshold ledger."""
    require(len(triangles) in (4, 5),
            "hull dispatch is defined only for the four/five-triangle rows")
    hull = first_hull_bridges(h_graph, theta_block, triangles)
    cluster = derive_root_cluster(h_graph, theta_block, hull.root_triangles)
    k = len(cluster.root_triangles)
    opened: tuple[tuple[tuple[str, ...], frozenset[Vertex]], ...] = ()
    upstream_core: frozenset[Vertex]
    pair: tuple[str, str] | None = None
    frontier: tuple[tuple[Vertex, str], ...] = ()
    if k >= 2:
        pair = select_anchor_pair(cluster)
        upstream_core, opened, frontier = derive_opened_groups(h_graph, cluster, pair)
    else:
        upstream_core = frozenset().union(
            *(block_vertices(cluster.labels[name]) for name in cluster.labels))
        require(upstream_core == cluster.vertices,
                "k<2 root cluster has unexpected unselected blocks")
    core_vertices = cluster.vertices
    require(frozenset().union(upstream_core, *(group[1] for group in opened))
            == core_vertices, "opened/upstream core does not cover the root cluster")
    # Build the core-owner map, then fold every acyclic payload component into
    # the unique territory containing its physical root.
    core_owner: dict[Vertex, str] = {}
    for vertex in upstream_core:
        require(vertex not in core_owner, "upstream core vertex is double owned")
        core_owner[vertex] = "upstream"
    for group_index, (group_names, group_vertices) in enumerate(opened):
        label = "opened:" + "+".join(group_names)
        for vertex in group_vertices:
            require(vertex not in core_owner, "opened core vertex is double owned")
            core_owner[vertex] = label
    require(set(core_owner) == set(core_vertices),
            "core-owner map does not cover the root cluster")
    additions = payload_assignments(h_graph, hull.root_side, core_vertices, core_owner)

    if k == 0:
        anchor_names: tuple[str, ...] = ()
    elif k == 1:
        anchor_names = cluster.root_triangles
    else:
        anchor_names = pair or ()
    upstream_blocks = (theta_block,
                       *(cluster.labels[name] for name in anchor_names))
    upstream = Territory("upstream", "upstream",
                         frozenset(upstream_core | additions.get("upstream", frozenset())),
                         upstream_blocks,
                         {0: 1, 1: 2}.get(k, 3), True)
    verify_territory(h_graph, upstream)
    if k >= 2:
        bridge_free_positive_paths(h_graph, upstream.vertices, upstream_blocks)
    if k == 1:
        bridge_free_positive_paths(h_graph, upstream.vertices, upstream_blocks)

    opened_territories = []
    for group_names, group_vertices in opened:
        label = "opened:" + "+".join(group_names)
        vertices = frozenset(group_vertices | additions.get(label, frozenset()))
        # A boundary triangle's upstream cut stays in A0, so the opened
        # territory contains only its private edge; a nested triangle wholly
        # below the boundary can remain a full triangle.  In either case every
        # positive-rank block below the boundary is a literal C3, and the
        # conservative first-boundary credit is -1.
        actual_blocks = positive_rank_blocks(h_graph, vertices)
        require(all(block_rank(block) == 1 and authenticate_literal_cycle(block) == 3
                    for block in actual_blocks),
                "opened territory contains a non-triangle cycle")
        require(all_blocks_triangles(h_graph, vertices) == len(actual_blocks),
                "opened territory block census is inconsistent")
        territory = Territory(label, "opened", vertices,
                              tuple(actual_blocks), -1, False)
        verify_territory(h_graph, territory)
        opened_territories.append(territory)

    bridge_territories = []
    for group in hull.bridge_groups:
        label = "bridge:" + "+".join(
            sorted("T" + str(triangles.index(block)) for block in group.triangles))
        territory = Territory(label, "bridge", group.away_side,
                              tuple(group.triangles), 0, False)
        verify_territory(h_graph, territory)
        require(all_blocks_triangles(h_graph, territory.vertices) == len(group.triangles),
                "first-hull-bridge territory is not all-triangle")
        bridge_territories.append(territory)

    territories = (upstream, *opened_territories, *bridge_territories)
    require(Counter(vertex for territory in territories for vertex in territory.vertices)
            == Counter(h_graph.vertices),
            "H territories are not disjoint and exhaustive")
    ledger_value = sum(territory.credit for territory in territories)
    ledger_strict = any(territory.strict for territory in territories)
    require(ledger_value > threshold or
            (ledger_value == threshold and ledger_strict),
            "H complement ledger is not strictly above its threshold")
    audit = {
        "root_triangle_count": k,
        "anchor_pair": list(pair) if pair else [],
        "opened_frontier": [[repr(vertex), name] for vertex, name in frontier],
        "bridge_groups": [
            {"bridge": sorted(repr(vertex) for vertex in group.bridge),
             "away_vertices": len(group.away_side),
             "triangles": len(group.triangles)}
            for group in hull.bridge_groups
        ],
        "h_vertices": len(h_graph.vertices),
        "h_territories": len(territories),
        "ledger_value": ledger_value,
        "ledger_strict": ledger_strict,
    }
    return territories, (upstream, *opened_territories), audit


def build_c5_hull_territories(graph: PhysicalGraph, split: C5Split,
                              inventory: R21Inventory):
    triangles = tuple(block for block in inventory.cycles
                      if authenticate_literal_cycle(block) == 3)
    require(len(triangles) == 4, "H side does not have four literal triangles")
    return build_hull_territories(graph, split.h_graph, inventory.theta_block,
                                  triangles, 1)



# ---------------------------------------------------------------------------
# Arbitrary Theta(1,2,r)+T^5 opening
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ThetaBranch:
    opening_vertex: Vertex
    r_vertices: frozenset[Vertex]
    h_vertices: frozenset[Vertex]
    r_triangles: int
    h_triangles: int
    r_is_tree: bool
    credit_r: int
    credit_h: int
    strict: bool
    analytic_inputs: tuple[str, ...]


def opening_candidates(theta: ThetaData) -> tuple[Vertex, ...]:
    """Internal vertices of the long arm; both length-two arms when r=2."""
    candidates = []
    for arm in theta.long_arm_candidates:
        require(len(arm) >= 3, "long arm has no internal vertex")
        candidates.extend(arm[1:-1])
    return tuple(dict.fromkeys(candidates))


def verify_theta_branch(graph: PhysicalGraph, inventory: R21Inventory,
                        vertex: Vertex) -> ThetaBranch:
    theta = inventory.theta
    require(vertex in block_vertices(theta.block),
            "opening vertex is not a theta vertex")
    require(vertex in opening_candidates(theta),
            "opening vertex is not internal to the long arm")
    theta_edges = inventory.theta.block
    reduced = PhysicalGraph(graph.vertices, graph.edges - theta_edges)
    # Compute the owner class directly on the graph whose theta edges have
    # already been deleted.
    reduced_adj = adjacency(reduced.vertices, reduced.edges)
    seen = {vertex}
    stack = [vertex]
    while stack:
        current = stack.pop()
        for neighbor in reduced_adj[current] - seen:
            seen.add(neighbor)
            stack.append(neighbor)
    r_vertices = frozenset(seen)
    require(r_vertices & block_vertices(theta.block) == frozenset({vertex}),
            "opened owner class contains a second theta vertex")
    h_vertices = graph.vertices - r_vertices
    require(h_vertices, "opening deleted the whole graph")
    h_graph = graph_on(graph, h_vertices)
    require(connected(h_vertices, h_graph.edges),
            "opened complement is disconnected")
    theta_vertices = block_vertices(theta.block)
    crossing = tuple(current for current in graph.edges
                     if (current & r_vertices) and (current & h_vertices))
    expected_crossing = frozenset(current for current in theta_edges
                                  if vertex in current)
    require(set(crossing) == set(expected_crossing),
            "opened/complement cut edges are not exactly the theta edges at the opening")
    require(len(expected_crossing) == 2,
            "an internal theta vertex does not have two theta edges")
    r_blocks = positive_rank_blocks(graph_on(graph, r_vertices), r_vertices)
    require(all(block_rank(block) == 1 and authenticate_literal_cycle(block) == 3
                for block in r_blocks),
            "opened owner class contains a non-triangle cycle")
    h_positive = positive_rank_blocks(h_graph, h_vertices)
    require(all(block_rank(block) == 1 and authenticate_literal_cycle(block) == 3
                for block in h_positive),
            "opened complement contains a non-triangle cycle")
    r_triangles = len(r_blocks)
    h_triangles = len(h_positive)
    require(r_triangles + h_triangles == 6,
            "opened and complement triangle counts do not sum to six")
    if r_triangles == 0:
        require(is_tree(graph, r_vertices),
                "triangle-free opened owner class is not a tree")
        require(h_triangles == 6,
                "triangle-free opening did not leave a six-triangle cactus")
        credit_r, credit_h = -1, 1
        analytic = ("six-triangle cactus sigma>1",)
    else:
        require(h_triangles >= 1,
                "opened complement lost the intrinsic triangle")
        credit_r, credit_h = 0, 0
        analytic = ("connected triangular block graph sigma>0",)
    ledger_value = credit_r + credit_h
    strict = True
    require(ledger_value > 0 or (ledger_value == 0 and strict),
            "theta opening ledger is not strictly positive")
    require(Counter(r_vertices) + Counter(h_vertices)
            == Counter(graph.vertices),
            "theta opening territories are not disjoint and exhaustive")
    return ThetaBranch(vertex, r_vertices, h_vertices, r_triangles, h_triangles,
                       r_triangles == 0, credit_r, credit_h, strict,
                       tuple(analytic))


def verify_theta_parent(graph: PhysicalGraph, inventory: R21Inventory | None = None,
                        preferred_opening: Vertex | None = None) -> dict[str, object]:
    inventory = inventory or authenticate_r21(graph)
    require(inventory.family == "THETA_PLUS_T5",
            "theta mode requires the Theta(1,2,r)+T^5 row")
    candidates = opening_candidates(inventory.theta)
    require(candidates, "theta has no long-arm internal vertex")
    if preferred_opening is not None:
        require(preferred_opening in candidates,
                "preferred opening is not a legal long-arm internal vertex")
        candidates = (preferred_opening,)
    branches = []
    for vertex in candidates:
        branches.append(verify_theta_branch(graph, inventory, vertex))
    # Prefer a branch whose only analytic input is the connected triangular
    # block graph corollary; otherwise the six-triangle cactus lemma is used.
    branches.sort(key=lambda branch: (branch.r_triangles == 0, repr(branch.opening_vertex)))
    chosen = branches[0]
    return {
        "family": "THETA_PLUS_T5",
        "status": "NONPROMOTIONAL_ADJACENCY_AND_OWNERSHIP_VERIFIED",
        "theta_r": inventory.theta.r,
        "theta_lengths": list(inventory.theta.lengths),
        "exact_dnn_witness": exact_dnn_witness(inventory),
        "theta_branch_vertices": [repr(v) for v in inventory.theta.branch],
        "opening_candidates": [repr(v) for v in candidates],
        "chosen_opening": repr(chosen.opening_vertex),
        "chosen_branch": {
            "r_triangles": chosen.r_triangles,
            "h_triangles": chosen.h_triangles,
            "r_is_tree": chosen.r_is_tree,
            "credit_r": chosen.credit_r,
            "credit_h": chosen.credit_h,
            "ledger_value": chosen.credit_r + chosen.credit_h,
            "strict": chosen.strict,
            "analytic_inputs": list(chosen.analytic_inputs),
        },
        "all_branches": [
            {
                "opening": repr(branch.opening_vertex),
                "r_triangles": branch.r_triangles,
                "h_triangles": branch.h_triangles,
                "ledger": branch.credit_r + branch.credit_h,
                "analytic_inputs": list(branch.analytic_inputs),
            }
            for branch in branches
        ],
        "territories": {
            "opened_owner_class": fingerprint(chosen.r_vertices,
                frozenset(c for c in graph.edges if c <= chosen.r_vertices)),
            "complement": fingerprint(chosen.h_vertices,
                frozenset(c for c in graph.edges if c <= chosen.h_vertices)),
            "opened_vertices": len(chosen.r_vertices),
            "complement_vertices": len(chosen.h_vertices),
        },
        "conclusion": "conditional on the named analytic packet inputs; no theorem claimed",
    }



# ---------------------------------------------------------------------------
# D + T^4 + C5 parent wrapper
# ---------------------------------------------------------------------------


def verify_c5_parent(graph: PhysicalGraph,
                     inventory: R21Inventory | None = None) -> dict[str, object]:
    inventory = inventory or authenticate_r21(graph)
    require(inventory.family == "D_PLUS_T4_C5",
            "C5 mode requires the literal D+T^4+C5 row")
    split = orient_c5_side(graph, inventory)
    territories, anchor_territories, audit = build_c5_hull_territories(
        graph, split, inventory)
    p_positive = positive_rank_blocks(graph_on(graph, split.p_side), split.p_side)
    require(len(p_positive) == 1 and p_positive[0] == split.c5_block,
            "C5 territory's unique positive-rank block changed")
    p_territory = Territory("hostile:C5", "c5", split.p_side,
                            (split.c5_block,), -1, False)
    verify_territory(graph, p_territory)
    require(Counter(vertex for territory in (*territories, p_territory)
                    for vertex in territory.vertices) == Counter(graph.vertices),
            "C5 parent territories are not disjoint and exhaustive")
    h_value = audit["ledger_value"]
    h_strict = audit["ledger_strict"]
    total_value = h_value - 1
    total_strict = h_strict
    require(total_value > 0 or (total_value == 0 and total_strict),
            "C5 parent total ledger is not strictly positive")
    return {
        "family": "D_PLUS_T4_C5",
        "status": "NONPROMOTIONAL_ADJACENCY_AND_OWNERSHIP_VERIFIED",
        "theta_lengths": list(inventory.theta.lengths),
        "cycle_lengths": list(inventory.cycle_lengths),
        "exact_dnn_witness": exact_dnn_witness(inventory),
        "c5_bridge": sorted(repr(vertex) for vertex in split.bridge),
        "c5_side_vertices": len(split.p_side),
        "h_side_vertices": len(split.h_side),
        "c5_side_positive_rank_blocks": len(p_positive),
        "hull": audit,
        "territories": [
            {
                "label": territory.label,
                "kind": territory.kind,
                "vertices": len(territory.vertices),
                "credit": territory.credit,
                "strict": territory.strict,
                "core_block_ranks": [block_rank(block) for block in territory.core_blocks],
                "fingerprint": fingerprint(territory.vertices,
                    frozenset(c for c in graph.edges if c <= territory.vertices)),
            }
            for territory in (*territories, p_territory)
        ],
        "ledger": {
            "h_value": h_value,
            "h_strict": h_strict,
            "p_value": -1,
            "p_strict": False,
            "total_value": total_value,
            "total_strict": total_strict,
        },
        "analytic_inputs": [
            "attached diamond D: sigma>1",
            "attached shared-cut D+T: sigma>2",
            "attached shared-cut D+T+T: sigma>3",
            "connected triangular block graph: sigma>0",
            "two-triangle cactus: sigma>1 (only if grouped by the ledger)",
            "hostile C5 unicycle: sigma>=-delta_5>-1, delta_5=sqrt(5)-2",
        ],
        "conclusion": "conditional on the named analytic packet inputs; no theorem claimed",
    }



# ---------------------------------------------------------------------------
# Pinned analytic sources (change detectors; not adjacency evidence)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SourcePin:
    path: str
    byte_length: int
    sha256: str
    tokens: tuple[str, ...]


SOURCE_PINS = (
    SourcePin("all-tricyclic-graphs/paper.tex", 47532,
              "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
              (r"\Delta(1,2,2)=\frac{\sqrt{17}-1}{2}.",
               r"\Delta(a,b,c)>1", r"(a,b,c)=(1,2,r)")),
    SourcePin("packing-two-square-energy/paper.tex", 44126,
              "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
              ("satisfies $s^+(G)>n$.", r"\label{cor:triangular-block}",
               "Here triangular means that every cyclic block is a triangle")),
    SourcePin("research/five-triangle-shared-cluster-surplus-2026-07-26.md", 10026,
              "08e3e9dd69e57de951ff8941d8a31c0a5c3995a661ecfdd103303e11615b4fae",
              ("Theorem 1 (five triangles in one shared-cut cluster).",
               "while `sigma(A)>2` in all cases.", "Lemma 4 (one leaf opening).")),
    SourcePin("research/arbitrary-r-shared-triangle-uniform-surplus-2026-07-26.md", 9559,
              "42317044cde35dc0e1df6e041e83fa9dd9bc42fdd444f6bc7f16360d5e5748f8",
              ("`sigma(A_r)>7-r`.", "incidence-leaf")),
    SourcePin("positive-square-energy/tricyclic-general/theta-cycle-completion.md", 2949,
              "43153f6e6cecd4bb6ab752c731b6c6c2c763a7c52da76b9f0464ed06eef61b81",
              ("A connected bicyclic cactus whose two cyclic blocks are triangles has",
               "D=s^+-s^->0")),
    SourcePin("positive-square-energy/pentacyclic-general/"
              "doubled-c4-111-two-triangles-retained-packet.md", 10708,
              "4fec746a4cf479b360e5c8692221bf796b6c260a7f9afc2bad37e404574ca00b",
              ("sigma(J)>r-1", "arbitrary one-root tree branches",
               "The scope excludes an acyclic connector meeting several cyclic cores.")),
    SourcePin("positive-square-energy/pentacyclic-general/"
              "diamond-two-triangle-exact-packet.md", 13093,
              "9107ef2821d441da401079982ae8d0b6c98cee17ae7e52268a9b6ad895b8e11b",
              ("sigma(D+T+T)>3.", "one bridge-free block-cut incidence tree",
               "bridge connectors are excluded")),
    SourcePin("all-tricyclic-cacti/paper.tex", 17669,
              "d928a56b0257936fcc326ddc2c85e40593117a7749b55502bb42379c805e71e8",
              (r"\delta_5=\sec(\pi/5)-1=\sqrt5-2",
               r"s^+(U_5)\geq u-\delta_5")),
)


def audit_sources() -> dict[str, dict[str, object]]:
    report: dict[str, dict[str, object]] = {}
    for pin in SOURCE_PINS:
        path = REPO / pin.path
        require(path.is_file(), f"missing pinned analytic source: {pin.path}")
        payload = path.read_bytes()
        require(len(payload) == pin.byte_length,
                f"analytic source byte length changed: {pin.path}")
        require(hashlib.sha256(payload).hexdigest() == pin.sha256,
                f"analytic source SHA-256 changed: {pin.path}")
        text = payload.decode("utf-8")
        for token in pin.tokens:
            require(text.count(token) == 1,
                    f"analytic source token missing or nonunique: {pin.path}: {token!r}")
        report[pin.path] = {
            "bytes": len(payload),
            "sha256": pin.sha256,
            "tokens": len(pin.tokens),
        }
    return report


# ---------------------------------------------------------------------------
# Report and hostile mutation harness
# ---------------------------------------------------------------------------


def expect_rejected(action, label: str) -> str:
    try:
        action()
    except (GateError, TypeError, ValueError, KeyError, IndexError):
        return label
    raise GateError(f"hostile mutation accepted: {label}")


def c5_tree_payload() -> PhysicalGraph:
    graph = d_plus_t4_c5_isolated()
    vertices = set(graph.vertices) | {"c5leaf"}
    edges = set(graph.edges) | {edge("c1", "c5leaf")}
    return PhysicalGraph(frozenset(vertices), frozenset(edges))


def h_tree_payload() -> PhysicalGraph:
    graph = d_plus_t4_c5_isolated(attach_at="a")
    vertices = set(graph.vertices) | {"hleaf"}
    edges = set(graph.edges) | {edge("a", "hleaf")}
    return PhysicalGraph(frozenset(vertices), frozenset(edges))


def extra_cycle_behind_bridge() -> PhysicalGraph:
    graph = d_plus_t4_c5_isolated()
    vertices = set(graph.vertices) | {"extra:b", "extra:u", "extra:v"}
    edges = set(graph.edges) | {
        edge("T0:u", "extra:b"), edge("extra:b", "extra:u"),
        edge("extra:u", "extra:v"), edge("extra:v", "extra:b"),
    }
    return PhysicalGraph(frozenset(vertices), frozenset(edges))


def hostile_checks() -> tuple[str, ...]:
    labels = []
    labels.append(expect_rejected(
        lambda: verify_c5_parent(d_plus_t4_c5_shared()),
        "C5 shares the D cut instead of an actual bridge"))
    labels.append(expect_rejected(
        lambda: verify_c5_parent(d_plus_t3_c5_plus_t_isolated()),
        "C5 side has rank two instead of a rank-one C5 side"))
    labels.append(expect_rejected(
        lambda: verify_c5_parent(add_chord(d_plus_t4_c5_isolated(), "c1", "c3")),
        "chorded nonliteral C5"))
    labels.append(expect_rejected(
        lambda: verify_c5_parent(subdivide_edge(d_plus_t4_c5_isolated(),
                                                edge("T0:u", "T0:v"), "subT")),
        "subdivided required triangle block"))
    labels.append(expect_rejected(
        lambda: verify_c5_parent(extra_cycle_behind_bridge()),
        "extra positive-rank block hidden behind a bridge"))
    labels.append(expect_rejected(
        lambda: verify_c5_parent(add_chord(d_plus_t4_c5_isolated(), "c2", "x")),
        "C5 joined to H by a second edge"))
    # An arbitrary theta in the C5 row is DNN-closed and outside the literal-D
    # reduced-hull theorem.
    vertices, edges, unused_names, unused_path = theta_core(3)
    for index in range(4):
        attach_triangle(vertices, edges, "x", f"T{index}")
    vertices.update(("w", "c1", "c2", "c3", "c4"))
    edges.update((edge("w", "c1"), edge("c1", "c2"), edge("c2", "c3"),
                  edge("c3", "c4"), edge("c4", "w"), edge("x", "w")))
    arbitrary_theta_c5 = PhysicalGraph(frozenset(vertices), frozenset(edges))
    labels.append(expect_rejected(
        lambda: verify_c5_parent(arbitrary_theta_c5),
        "arbitrary theta in the C5 row instead of literal D"))
    # Legal theta openings are internal long-arm vertices only.
    labels.append(expect_rejected(
        lambda: verify_theta_parent(theta_plus_triangles(4, (("x", 5),)),
                                     preferred_opening="x"),
        "theta opening at a branch vertex"))
    labels.append(expect_rejected(
        lambda: verify_theta_parent(theta_plus_triangles(4, (("x", 5),)),
                                     preferred_opening="a"),
        "theta opening on the short length-two arm for r>=3"))
    labels.append(expect_rejected(
        lambda: verify_theta_parent(d_plus_t4_c5_isolated()),
        "C5 row passed to the theta opening mode"))
    # A simple theta with path lengths (2,2,2) is not Theta(1,2,r).
    theta_222_vertices = {"x", "y", "a", "b", "c"}
    theta_222_edges = {edge("x", "a"), edge("a", "y"),
                       edge("x", "b"), edge("b", "y"),
                       edge("x", "c"), edge("c", "y")}
    for index in range(5):
        attach_triangle(theta_222_vertices, theta_222_edges, "x", f"T{index}")
    theta_222 = PhysicalGraph(frozenset(theta_222_vertices),
                              frozenset(theta_222_edges))
    labels.append(expect_rejected(
        lambda: authenticate_r21(theta_222),
        "theta path lengths (2,2,2) instead of (1,2,r)"))
    return tuple(labels)


def run(strict_analytics: bool = False) -> dict[str, object]:
    sources = audit_sources()

    positives = {
        "c5_bridge_isolated": verify_c5_parent(d_plus_t4_c5_isolated()),
        "c5_bridge_isolated_with_c5_tree": verify_c5_parent(c5_tree_payload()),
        "c5_bridge_isolated_with_h_tree": verify_c5_parent(h_tree_payload()),
        "d_plus_5t_shared_k5": build_hull_territories(
            d_plus_5t_shared(), d_plus_5t_shared(),
            authenticate_r21(d_plus_5t_shared()).theta_block,
            tuple(b for b in authenticate_r21(d_plus_5t_shared()).cycles
                  if block_rank(b) == 1), 0)[2],
        "d_plus_5t_chain_k0": build_hull_territories(
            d_plus_5t_chain(), d_plus_5t_chain(),
            authenticate_r21(d_plus_5t_chain()).theta_block,
            tuple(b for b in authenticate_r21(d_plus_5t_chain()).cycles
                  if block_rank(b) == 1), 0)[2],
        "d_plus_5t_nested_k5": build_hull_territories(
            d_plus_5t_nested(), d_plus_5t_nested(),
            authenticate_r21(d_plus_5t_nested()).theta_block,
            tuple(b for b in authenticate_r21(d_plus_5t_nested()).cycles
                  if block_rank(b) == 1), 0)[2],
        "c5_with_hull_bridge_k1": verify_c5_parent(d_plus_t4_c5_with_hull_bridge()),
        "c5_behind_tree_chain": verify_c5_parent(d_plus_t4_c5_behind_tree_chain()),
        "d_plus_5t_two_groups_k1": build_hull_territories(
            d_plus_5t_two_chains_and_shared(), d_plus_5t_two_chains_and_shared(),
            authenticate_r21(d_plus_5t_two_chains_and_shared()).theta_block,
            tuple(b for b in authenticate_r21(
                d_plus_5t_two_chains_and_shared()).cycles if block_rank(b) == 1), 0)[2],
        "theta_rows": [
            verify_theta_parent(theta_plus_triangles(r, (("x", 5),)))
            for r in (2, 3, 4, 5, 7)
        ],
        "theta_owner_triangle": verify_theta_parent(
            theta_plus_triangles(4, (("p2", 1), ("x", 4)))),
    }
    rejected = hostile_checks()
    require(len(rejected) == len(set(rejected)), "hostile labels are not unique")

    prose_only = [
        "connected triangular block graph sigma>0 (packing-two corollary; prose proof, no executable replay)",
        "five-triangle shared cluster sigma>2 (leaf-opening proof note; no executable replay)",
        "six-triangle shared cluster sigma>1 (four-triangle base plus two leaf openings; no executable replay)",
        "two-triangle cactus sigma>1 (Sachs phase note; no executable replay)",
        "D, D+T, D+T+T packet credits (one executable DTT child exists on the parent branch; not replayed here)",
        "hostile C5 delta_5 bound (prose lemma; no executable replay)",
    ]
    if strict_analytics:
        raise GateError(
            "strict analytics requested but the following required inputs are "
            "prose-only or not replayed in this prototype: " + "; ".join(prose_only))
    return {
        "status": "NONPROMOTIONAL_ADJACENCY_AND_OWNERSHIP_VERIFIED",
        "scope": "two DNN-open R21 physical rows only: arbitrary Theta(1,2,r)+T^5 and literal D+T^4+C5",
        "positives": positives,
        "hostile_mutations_rejected": {
            "count": len(rejected),
            "labels": list(rejected),
        },
        "source_receipts": sources,
        "analytic_inputs_not_rederived": prose_only,
        "strict_analytics": strict_analytics,
        "trust_boundary": (
            "Tarjan typing, theta path reconstruction, C5 bridge orientation, "
            "first-hull-bridge selection, root-cluster ports, cut closure, and "
            "original-vertex ownership are adjacency-derived here.  Every "
            "spectral packet credit is an external analytic input.  The gate "
            "does not claim a theorem, does not read labels as evidence, and "
            "does not touch STATE, theorem-master, publication, or lane state."
        ),
        "open_obligations": [
            "No executable replay of the six-triangle cactus >1 lemma; its proof note is pinned by bytes/tokens only.",
            "No executable replay of the connected triangular block graph corollary; pinned by bytes/tokens only.",
            "The DTT packet child is not replayed on this branch; the parent hull verifier owns that replay.",
            "The five-triangle hull dispatch is computed directly per fixture; a 5-triangle decorated-block-cut census is not enumerated here.",
            "The gate does not prove the two analytic packet inequalities; it only composes them after adjacency typing.",
        ],
    }


def serialized_report(strict_analytics: bool = False) -> str:
    return json.dumps(run(strict_analytics), sort_keys=True, indent=2) + "\n"


def audit_no_asserts() -> None:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
            "verifier must not rely on Python assertions")


def main(argv: list[str]) -> int:
    audit_no_asserts()
    strict = "--strict-analytics" in argv
    output = serialized_report(strict)
    if "--optimized-child" not in argv:
        child = subprocess.run(
            [sys.executable, "-O", str(Path(__file__).resolve()),
             "--optimized-child", *(["--strict-analytics"] if strict else [])],
            check=False, capture_output=True, text=True)
        require(child.returncode == 0, "optimized child failed")
        require(child.stderr == "", "optimized child wrote stderr")
        require(child.stdout == output, "normal and optimized outputs differ")
    sys.stdout.write(output)
    return 0


# ---------------------------------------------------------------------------
# Protocol placeholders are completed below in later sections.
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
