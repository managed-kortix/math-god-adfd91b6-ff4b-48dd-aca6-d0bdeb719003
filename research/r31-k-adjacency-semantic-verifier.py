#!/usr/bin/env python3
"""Full adjacency-only semantic verifier for the complete physical R31-K lane.

The production API is ``verify(vertices, edges)``.  Its only input is a finite
simple graph represented by a nonempty frozenset of original vertices and a
frozenset of unordered two-vertex frozenset edges.  The verifier reconstructs
all blocks, cuts, physical bridges, rooted block-cut ancestry, side ownership,
piece topology, charges, and the final integer ledger.  It accepts no claimed
profile, packet, owner, charge, rank, threshold, or partition.

This candidate is intentionally scoped to R31-K.  It neither edits nor imports
state from the repository; analytic dependencies are authenticated as pinned
read-only source bytes below.  Its generic adjacency API and finite generated
suite corroborate the implementation but do not by themselves prove the
universal theorem over arbitrary block-cut trees; that proof is external.
"""
from __future__ import annotations

import hashlib
import itertools
import subprocess
import sys
import tempfile
from collections import Counter, deque
from dataclasses import dataclass, replace
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]


class VerifyError(RuntimeError):
    """Fail-closed semantic rejection."""


def require(condition, message):
    if not condition:
        raise VerifyError(message)


def expect_rejection(action, label):
    try:
        action()
    except (VerifyError, KeyError, TypeError, ValueError, IndexError, StopIteration):
        return label
    raise VerifyError(f"hostile mutation accepted: {label}")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    return sha256_bytes(path.read_bytes())


# ---------------------------------------------------------------------------
# Fixed analytic contracts.  No numeric analytic field is accepted through
# verify().  Repeated source paths are deliberate: each semantic use is named
# separately, while audit_sources() independently authenticates the bytes.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Contract:
    source: str
    sha256: str
    claim: str
    floor: int | None
    strict: bool


CONTRACT_SPECS = (
    ("R31K-RESIDUAL-SIEVE-v2", Contract(
        "positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md",
        "3f8bb3a397125782dd6c9cae26ce52f9c6bf826e3136dfee62781048e65c18a5",
        "exact R31-K residual sieve/classification input; not a full-lane theorem", None, False)),
    ("R31K-INDUCED-SUPERADD-v2", Contract(
        "all-tricyclic-graphs/paper.tex",
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
        "positive-square-energy induced superadditivity", None, False)),
    ("R31K-TREE-EXACT-v2", Contract(
        "all-tricyclic-graphs/paper.tex",
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
        "nonempty tree has sigma=-1", -1, False)),
    ("R31K-ODD-UNICYCLIC-LOWER-v2", Contract(
        "all-tricyclic-cacti/paper.tex",
        "d928a56b0257936fcc326ddc2c85e40593117a7749b55502bb42379c805e71e8",
        "odd unicyclic cactus has sigma>-1", -1, True)),
    ("R31K-TRIANGULAR-BLOCK-v2", Contract(
        "packing-two-square-energy/paper.tex",
        "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
        "non-tree triangular block graph has sigma>0", 0, True)),
    ("R31K-CACTUS-RANK2PLUS-v2", Contract(
        "all-nonunicyclic-cacti/paper.tex",
        "26939326e2ad71062617503e106dbd46d99f3d8fe82a98fca858fd3f2f8323f9",
        "connected cactus of rank at least two has sigma>0", 0, True)),
    ("R31K-K4-ROOTED-v2", Contract(
        "packing-two-square-energy/paper.tex",
        "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
        "literal K4 with bridge trees has sigma>2", 2, True)),
    ("R31K-K4-T-SHARED-v2", Contract(
        "packing-two-square-energy/paper.tex",
        "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
        "direct shared-cut literal K4 plus triangle has sigma>3", 3, True)),
)
CONTRACTS = dict(CONTRACT_SPECS)
EXPECTED_CONTRACT_IDS = frozenset(name for name, _ in CONTRACT_SPECS)


def contract_manifest_digest():
    rows = sorted({f"{item.source}\t{item.sha256}" for _, item in CONTRACT_SPECS})
    return sha256_bytes(("\n".join(rows) + "\n").encode())


def audit_contract_table():
    require(frozenset(CONTRACTS) == EXPECTED_CONTRACT_IDS,
            "analytic contract ID set changed")
    canonical = dict(CONTRACT_SPECS)
    require(CONTRACTS == canonical, "analytic contract record changed")
    for contract_id, item in CONTRACTS.items():
        require(type(item) is Contract, f"malformed contract: {contract_id}")
        require(type(item.strict) is bool, f"nonstrict flag malformed: {contract_id}")
        require(item.floor is None or type(item.floor) is int,
                f"contract floor malformed: {contract_id}")


def authenticate_source_blob(blob, expected, label):
    require(sha256_bytes(blob) == expected, f"analytic source changed: {label}")


def audit_sources():
    audit_contract_table()
    require(SOURCE_ROOT.is_dir(), "read-only source repository is absent")
    checked = set()
    for contract_id, item in CONTRACTS.items():
        key = (item.source, item.sha256)
        if key in checked:
            continue
        path = SOURCE_ROOT / item.source
        require(path.is_file(), f"analytic source missing: {contract_id}")
        authenticate_source_blob(path.read_bytes(), item.sha256, contract_id)
        checked.add(key)
    return len(checked)


# ---------------------------------------------------------------------------
# Physical adjacency, Tarjan blocks, and the full block-cut tree.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PhysicalGraph:
    vertices: frozenset
    edges: frozenset


@dataclass(frozen=True)
class Block:
    index: int
    edges: frozenset
    vertices: frozenset
    rank: int
    kind: str
    cycle_length: int | None


@dataclass(frozen=True)
class Inventory:
    graph: PhysicalGraph
    adjacency: dict
    blocks: tuple[Block, ...]
    cuts: frozenset
    tree: dict
    k4: int
    cycles: tuple[int, ...]
    bridge_blocks: tuple[int, ...]
    parent: dict
    depth: dict
    root_order: tuple


@dataclass(frozen=True)
class LocalAnalysis:
    vertices: frozenset
    edges: frozenset
    blocks: tuple[Block, ...]
    rank: int
    positive_ids: tuple[int, ...]
    positive_kinds: tuple[str, ...]
    cycle_lengths: tuple[int, ...]


def edge(left, right):
    require(left != right, "loop in simple adjacency")
    return frozenset((left, right))


def normalize_graph(vertices, edges):
    require(type(vertices) is frozenset and vertices,
            "vertices must be a nonempty frozenset")
    require(type(edges) is frozenset, "edges must be a frozenset")
    normalized = set()
    for current in edges:
        require(type(current) is frozenset and len(current) == 2,
                "malformed unordered edge")
        require(current <= vertices, "edge endpoint outside vertex set")
        normalized.add(current)
    require(len(normalized) == len(edges), "duplicate edge representation")
    return PhysicalGraph(vertices, frozenset(normalized))


def adjacency(vertices, edges):
    graph = {vertex: set() for vertex in vertices}
    for current in edges:
        left, right = tuple(current)
        graph[left].add(right)
        graph[right].add(left)
    return graph


def induced_edges(edges, vertices):
    vertices = set(vertices)
    return frozenset(current for current in edges if current <= vertices)


def components(vertices, edges):
    vertices = frozenset(vertices)
    require(all(current <= vertices for current in edges),
            "component edge escapes supplied vertices")
    graph = adjacency(vertices, edges)
    unseen = set(vertices)
    answer = []
    while unseen:
        root = next(iter(unseen))
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


def connected(vertices, edges):
    return bool(vertices) and len(components(vertices, edges)) == 1


def graph_rank(vertices, edges):
    return len(edges) - len(vertices) + len(components(vertices, edges))


def biconnected_edge_blocks(vertices, edges):
    """Iterative Tarjan edge-stack decomposition.

    Iteration rather than Python recursion is intentional: a physically long
    K2 connector must not change acceptance merely by crossing a recursion
    limit.  Every bridge is returned as its own one-edge block.
    """
    graph = adjacency(vertices, edges)
    discovery = {}
    low = {}
    parent = {}
    parent_edge = {}
    edge_stack = []
    blocks = []
    clock = 0

    for root in vertices:
        if root in discovery:
            continue
        clock += 1
        discovery[root] = low[root] = clock
        frames = [(root, iter(graph[root]))]
        while frames:
            current, iterator = frames[-1]
            try:
                neighbor = next(iterator)
            except StopIteration:
                frames.pop()
                if current in parent:
                    upstream = parent[current]
                    low[upstream] = min(low[upstream], low[current])
                    if low[current] >= discovery[upstream]:
                        boundary = parent_edge[current]
                        current_block = set()
                        while True:
                            require(edge_stack, "Tarjan edge stack underflow")
                            popped = edge_stack.pop()
                            current_block.add(popped)
                            if popped == boundary:
                                break
                        blocks.append(frozenset(current_block))
                else:
                    require(not edge_stack, "Tarjan stack leaked at DFS root")
                continue

            current_edge = edge(current, neighbor)
            if neighbor not in discovery:
                parent[neighbor] = current
                parent_edge[neighbor] = current_edge
                edge_stack.append(current_edge)
                clock += 1
                discovery[neighbor] = low[neighbor] = clock
                frames.append((neighbor, iter(graph[neighbor])))
            elif parent.get(current) != neighbor and discovery[neighbor] < discovery[current]:
                edge_stack.append(current_edge)
                low[current] = min(low[current], discovery[neighbor])

    union = set().union(*blocks) if blocks else set()
    require(union == set(edges), "Tarjan blocks do not exhaust physical edges")
    require(sum(map(len, blocks)) == len(edges), "Tarjan blocks duplicate edges")
    return tuple(blocks)


def classify_block(index, edges):
    require(edges, "empty edge block")
    vertices = frozenset().union(*edges)
    rank = len(edges) - len(vertices) + 1
    degrees = {vertex: sum(vertex in current for current in edges)
               for vertex in vertices}
    if len(edges) == 1:
        require(rank == 0 and len(vertices) == 2, "malformed physical bridge")
        return Block(index, edges, vertices, rank, "bridge", None)
    if (len(vertices) == 4 and len(edges) == 6 and
            all(value == 3 for value in degrees.values())):
        require(rank == 3, "literal K4 rank changed")
        return Block(index, edges, vertices, rank, "K4", None)
    if (len(vertices) >= 3 and len(edges) == len(vertices) and
            all(value == 2 for value in degrees.values())):
        require(rank == 1, "literal cycle rank changed")
        return Block(index, edges, vertices, rank, "cycle", len(vertices))
    raise VerifyError("unsupported positive-rank block type")


def rooted_tree(tree, root):
    require(root in tree, "block-cut root absent")
    parent = {root: None}
    depth = {root: 0}
    order = [root]
    queue = deque([root])
    while queue:
        current = queue.popleft()
        for neighbor in tree[current]:
            if neighbor == parent[current]:
                continue
            require(neighbor not in parent, "block-cut incidence contains a cycle")
            parent[neighbor] = current
            depth[neighbor] = depth[current] + 1
            order.append(neighbor)
            queue.append(neighbor)
    require(set(parent) == set(tree), "block-cut topology disconnected")
    return parent, depth, tuple(order)


def reconstruct(vertices, edges):
    graph = normalize_graph(vertices, edges)
    require(connected(graph.vertices, graph.edges), "input graph disconnected")
    require(graph_rank(graph.vertices, graph.edges) == 7,
            "input graph does not have cyclomatic rank seven")

    raw_blocks = biconnected_edge_blocks(graph.vertices, graph.edges)
    blocks = tuple(classify_block(index, current)
                   for index, current in enumerate(raw_blocks))
    positive = tuple(item for item in blocks if item.rank)
    k4s = tuple(item.index for item in positive if item.kind == "K4")
    cycles = tuple(item.index for item in positive if item.kind == "cycle")
    require(len(k4s) == 1 and len(cycles) == 4 and len(positive) == 5,
            "positive blocks are not one literal K4 and four literal cycles")
    require(sum(item.rank for item in positive) == 7,
            "positive block ranks are not exactly 3+1+1+1+1")

    membership = {vertex: tuple(item.index for item in blocks
                                if vertex in item.vertices)
                  for vertex in graph.vertices}
    cuts = frozenset(vertex for vertex, owners in membership.items()
                     if len(owners) >= 2)
    tree = {("B", item.index): set() for item in blocks}
    for cut in cuts:
        cut_node = ("C", cut)
        tree[cut_node] = set()
        for owner in membership[cut]:
            block_node = ("B", owner)
            tree[cut_node].add(block_node)
            tree[block_node].add(cut_node)
    require(tree, "empty block-cut incidence")
    require(sum(map(len, tree.values())) // 2 == len(tree) - 1,
            "block-cut incidence is not a tree")
    root = ("B", k4s[0])
    parent, depth, order = rooted_tree(tree, root)
    bridges = tuple(item.index for item in blocks if item.kind == "bridge")
    return Inventory(graph, adjacency(graph.vertices, graph.edges), blocks,
                     cuts, tree, k4s[0], cycles, bridges,
                     parent, depth, order)


def block(inventory, index):
    return inventory.blocks[index]


def path_from_root(inventory, node):
    require(node in inventory.parent, "block-cut path target absent")
    result = []
    current = node
    while current is not None:
        result.append(current)
        current = inventory.parent[current]
    result.reverse()
    return tuple(result)


def is_ancestor(inventory, ancestor, descendant, strict=False):
    if strict and ancestor == descendant:
        return False
    current = descendant
    while current is not None and inventory.depth[current] >= inventory.depth[ancestor]:
        if current == ancestor:
            return True
        current = inventory.parent[current]
    return False


def upstream_cut(inventory, block_index):
    node = ("B", block_index)
    require(node != ("B", inventory.k4), "K4 has no upstream articulation")
    parent = inventory.parent[node]
    require(parent is not None and parent[0] == "C",
            "positive block lacks immediate upstream cut")
    cut = parent[1]
    require(cut in block(inventory, block_index).vertices,
            "upstream cut is outside its block")
    return cut


def canonical_subtree_ids(inventory):
    """Exact label-free IDs for rooted colored block-cut subtrees."""
    signatures = {}
    intern = {}
    next_id = 0
    levels = sorted(set(inventory.depth.values()), reverse=True)
    for level in levels:
        keys = {}
        for node in (item for item in inventory.root_order
                     if inventory.depth[item] == level):
            if node[0] == "C":
                color = ("cut",)
            else:
                item = block(inventory, node[1])
                color = ("block", item.kind, item.cycle_length)
            child_ids = tuple(sorted(signatures[child]
                                     for child in inventory.tree[node]
                                     if inventory.parent.get(child) == node))
            keys[node] = (color, child_ids)
        new_keys = sorted({key for key in keys.values() if key not in intern},
                          key=repr)
        for key in new_keys:
            intern[key] = next_id
            next_id += 1
        for node, key in keys.items():
            signatures[node] = intern[key]
    require(set(signatures) == set(inventory.tree),
            "canonical rooted signatures incomplete")
    return signatures


def analyze_piece(inventory, vertices):
    require(type(vertices) is frozenset and vertices,
            "piece is empty or not a frozenset")
    require(vertices <= inventory.graph.vertices, "piece has foreign vertex")
    edges = induced_edges(inventory.graph.edges, vertices)
    require(connected(vertices, edges), "piece is not connected")
    raw = biconnected_edge_blocks(vertices, edges)
    local_blocks = tuple(classify_block(index, current)
                         for index, current in enumerate(raw))
    rank = graph_rank(vertices, edges)
    require(rank == sum(item.rank for item in local_blocks),
            "piece block ranks do not sum to its graph rank")

    local_positive = tuple(item for item in local_blocks if item.rank)
    intact_ids = tuple(sorted(index for index in (inventory.k4, *inventory.cycles)
                              if block(inventory, index).vertices <= vertices))
    local_edge_blocks = frozenset(item.edges for item in local_positive)
    expected_edge_blocks = frozenset(block(inventory, index).edges
                                     for index in intact_ids)
    require(local_edge_blocks == expected_edge_blocks and
            len(local_positive) == len(intact_ids),
            "piece has a split, merged, or newly manufactured positive block")
    kinds = tuple(block(inventory, index).kind for index in intact_ids)
    lengths = tuple(sorted(block(inventory, index).cycle_length
                           for index in intact_ids
                           if block(inventory, index).kind == "cycle"))
    return LocalAnalysis(vertices, edges, local_blocks, rank,
                         intact_ids, kinds, lengths)


def require_cactus(analysis, label):
    require(all(kind == "cycle" for kind in analysis.positive_kinds),
            f"{label} is not a cactus")
    require(analysis.rank == len(analysis.positive_ids),
            f"{label} cactus rank does not equal its cyclic-block count")
    return True


def verify_partition(inventory, target, pieces, label):
    require(type(target) is frozenset and target,
            f"{label} target is malformed")
    require(pieces and all(type(side) is frozenset and side for side in pieces),
            f"{label} contains an empty or malformed piece")
    union = set().union(*pieces)
    require(union == set(target), f"{label} is not exhaustive")
    require(sum(map(len, pieces)) == len(union), f"{label} pieces overlap")
    for side in pieces:
        require(side <= target, f"{label} piece escapes target")
        current_edges = induced_edges(inventory.graph.edges, side)
        require(connected(side, current_edges), f"{label} piece is disconnected")
        # Edges are never supplied with a piece.  They are always recomputed as
        # E(G[side]), so inducedness is constructive rather than a trusted flag.
        require(current_edges == frozenset(current for current in inventory.graph.edges
                                           if current <= side),
                f"{label} piece edge set is not induced")
    return True


# ---------------------------------------------------------------------------
# Residual profile, first bridges, and original-vertex boundary openings.
# ---------------------------------------------------------------------------


def derive_profile(inventory):
    lengths = tuple(sorted(block(inventory, index).cycle_length
                           for index in inventory.cycles))
    require(all(type(length) is int and length >= 3 for length in lengths),
            "cycle length below three")
    if lengths == (3, 3, 3, 3):
        profile = "T4"
    elif lengths[:3] == (3, 3, 3) and lengths[3] >= 5 and lengths[3] % 2 == 1:
        profile = "T3+odd>=5"
    elif lengths == (3, 3, 5, 5):
        profile = "T2+C5+C5"
    else:
        raise VerifyError("adjacency-derived cycle profile is not an R31-K residual")
    h = sum(length != 3 for length in lengths)
    require(h <= 2 and lengths.count(3) == 4 - h,
            "residual nontriangle count is inconsistent")
    return profile, h


def cycle_ids_in(inventory, vertices):
    return tuple(index for index in inventory.cycles
                 if block(inventory, index).vertices <= vertices)


def first_hull_bridges(inventory):
    chosen = set()
    for cycle_index in inventory.cycles:
        route = path_from_root(inventory, ("B", cycle_index))
        bridges = [node[1] for node in route
                   if node[0] == "B" and block(inventory, node[1]).kind == "bridge"]
        if bridges:
            chosen.add(bridges[0])
    result = tuple(sorted(chosen))
    nodes = [("B", index) for index in result]
    for left, right in itertools.permutations(nodes, 2):
        require(not is_ancestor(inventory, left, right, strict=True),
                "deduplicated first physical bridges are not an antichain")
    return result


def bridge_away_component(inventory, bridge_index):
    current = block(inventory, bridge_index)
    require(current.kind == "bridge" and len(current.edges) == 1,
            "away split requested on a nonbridge block")
    physical_edge = next(iter(current.edges))
    sides = components(inventory.graph.vertices,
                       frozenset(inventory.graph.edges - {physical_edge}))
    require(len(sides) == 2, "Tarjan bridge did not split physical adjacency")
    k4_vertices = block(inventory, inventory.k4).vertices
    root_sides = [side for side in sides if k4_vertices <= side]
    require(len(root_sides) == 1, "physical bridge orientation is ambiguous")
    return next(side for side in sides if side != root_sides[0])


def boundary_open(inventory, current_vertices, boundary_index, cut):
    """Return Q-c plus every current descendant owner on original vertices."""
    boundary = block(inventory, boundary_index)
    require(boundary.kind == "cycle", "boundary opening requires a cycle")
    require(boundary.vertices <= current_vertices,
            "boundary cycle is not intact in current territory")
    require(cut in boundary.vertices, "upstream articulation outside boundary")
    current_edges = induced_edges(inventory.graph.edges, current_vertices)
    require(boundary.edges <= current_edges, "boundary edges missing from territory")
    owner_components = components(current_vertices,
                                  frozenset(current_edges - boundary.edges))
    by_vertex = {}
    for side in owner_components:
        hits = side & boundary.vertices
        require(len(hits) == 1,
                "outside owner component meets a cycle at multiple vertices")
        owner = next(iter(hits))
        require(owner not in by_vertex, "cycle vertex has duplicate owner component")
        by_vertex[owner] = side
    require(set(by_vertex) == set(boundary.vertices),
            "cycle owner decomposition omitted a boundary vertex")
    result = frozenset().union(*(by_vertex[vertex]
                                for vertex in boundary.vertices if vertex != cut))
    require(result and cut not in result,
            "opened side is empty or copied its upstream articulation")
    require(boundary.vertices - {cut} <= result,
            "opened side omitted Q-c")
    require(connected(result, induced_edges(inventory.graph.edges, result)),
            "Q-c descendant side is disconnected")
    return result


def ancestor_minimal_cycles(inventory, candidates):
    candidate_set = set(candidates)
    selected = []
    for index in candidates:
        route = path_from_root(inventory, ("B", index))
        earlier = [node[1] for node in route[:-1]
                   if node[0] == "B" and node[1] in candidate_set]
        if not earlier:
            selected.append(index)
    nodes = [("B", index) for index in selected]
    for left, right in itertools.permutations(nodes, 2):
        require(not is_ancestor(inventory, left, right, strict=True),
                "ancestor-minimal cycle boundaries are not an antichain")
    return tuple(sorted(selected))


# ---------------------------------------------------------------------------
# Structural partition plan.  This stage performs no analytic charging.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BridgeSide:
    bridge_block: int
    vertices: frozenset


@dataclass(frozen=True)
class OpenSide:
    boundary_block: int
    upstream_cut: object
    vertices: frozenset


@dataclass(frozen=True)
class PartitionPlan:
    profile: str
    h: int
    phase1: tuple[BridgeSide, ...]
    root_vertices: frozenset
    phase2: tuple[OpenSide, ...]
    core_vertices: frozenset
    anchor_triangle: int | None
    phase3: tuple[OpenSide, ...]
    anchor_vertices: frozenset


def choose_nearest_triangle(inventory, core_triangles):
    require(core_triangles, "nearest triangle requested from triangle-free core")
    minimum = min(inventory.depth[("B", index)] for index in core_triangles)
    nearest = [index for index in core_triangles
               if inventory.depth[("B", index)] == minimum]
    canonical = canonical_subtree_ids(inventory)
    # Do not use Tarjan discovery indices as a semantic tie-break.  Any
    # nearest choice has the same proof contract; canonical subtree ID makes
    # the choice label-free, and equal IDs are deliberately left unordered.
    best_id = min(canonical[("B", index)] for index in nearest)
    return next(index for index in nearest
                if canonical[("B", index)] == best_id)


def construct_plan(inventory, profile, h):
    # Phase 1: simultaneously remove every deduplicated first physical bridge.
    first = first_hull_bridges(inventory)
    phase1 = tuple(BridgeSide(index, bridge_away_component(inventory, index))
                   for index in first)
    away_sets = tuple(item.vertices for item in phase1)
    if away_sets:
        require(sum(map(len, away_sets)) == len(set().union(*away_sets)),
                "first-bridge away components overlap")
        removed_edges = frozenset(next(iter(block(inventory, index).edges))
                                  for index in first)
        simultaneous = components(inventory.graph.vertices,
                                  frozenset(inventory.graph.edges - removed_edges))
        root_matches = [side for side in simultaneous
                        if block(inventory, inventory.k4).vertices <= side]
        require(len(root_matches) == 1, "simultaneous bridge root is ambiguous")
        root_vertices = root_matches[0]
        require(frozenset(simultaneous) == frozenset((root_vertices, *away_sets)),
                "individual first-bridge sides disagree with simultaneous split")
    else:
        root_vertices = inventory.graph.vertices
    verify_partition(inventory, inventory.graph.vertices,
                     (root_vertices, *away_sets), "phase-1 first-bridge partition")
    require(block(inventory, inventory.k4).vertices <= root_vertices,
            "literal K4 escaped the root component")
    for side in phase1:
        require(cycle_ids_in(inventory, side.vertices),
                "selected first bridge has no cycle in its away component")
        analysis = analyze_piece(inventory, side.vertices)
        require_cactus(analysis, "first-bridge away component")
        require(analysis.rank >= 1, "first-bridge away cactus has rank zero")
    for cycle_index in cycle_ids_in(inventory, root_vertices):
        route = path_from_root(inventory, ("B", cycle_index))
        require(not any(node[0] == "B" and
                        block(inventory, node[1]).kind == "bridge"
                        for node in route),
                "a root cycle still has a physical bridge on its K4 route")

    # Phase 2: open every ancestor-minimal nontriangle still in the root.
    root_nontriangles = tuple(index for index in cycle_ids_in(inventory, root_vertices)
                              if block(inventory, index).cycle_length != 3)
    phase2_boundaries = ancestor_minimal_cycles(inventory, root_nontriangles)
    phase2 = tuple(OpenSide(index, upstream_cut(inventory, index),
                            boundary_open(inventory, root_vertices, index,
                                          upstream_cut(inventory, index)))
                   for index in phase2_boundaries)
    phase2_sets = tuple(item.vertices for item in phase2)
    if phase2_sets:
        require(sum(map(len, phase2_sets)) == len(set().union(*phase2_sets)),
                "ancestor-minimal nontriangle sides overlap")
        core_vertices = frozenset(set(root_vertices) - set().union(*phase2_sets))
    else:
        core_vertices = root_vertices
    verify_partition(inventory, root_vertices, (core_vertices, *phase2_sets),
                     "phase-2 nontriangle partition")
    require(block(inventory, inventory.k4).vertices <= core_vertices,
            "nontriangle opening split the literal K4")

    core_analysis = analyze_piece(inventory, core_vertices)
    require(core_analysis.positive_kinds.count("K4") == 1,
            "retained core lost or duplicated its K4")
    require(all(length == 3 for length in core_analysis.cycle_lengths),
            "retained core still has a nontriangle cycle")
    core_triangles = tuple(index for index in inventory.cycles
                           if block(inventory, index).vertices <= core_vertices)
    require(set(core_analysis.positive_ids) == {inventory.k4, *core_triangles},
            "core positive blocks are not K4 plus intact triangles")
    require(core_analysis.rank == 3 + len(core_triangles),
            "K4+kT core rank is incorrect")
    require(len(core_triangles) <= 4 - h,
            "retained triangle count exceeds the global residual count")

    # Phase 3: retain K4 alone when k=0; otherwise retain one nearest direct T.
    if not core_triangles:
        anchor_triangle = None
        phase3 = ()
        anchor_vertices = core_vertices
    else:
        anchor_triangle = choose_nearest_triangle(inventory, core_triangles)
        route = path_from_root(inventory, ("B", anchor_triangle))
        require(len(route) == 3 and route[0] == ("B", inventory.k4) and
                route[1][0] == "C" and route[2] == ("B", anchor_triangle),
                "nearest retained triangle does not share a cut directly with K4")
        shared_cut = route[1][1]
        require(block(inventory, inventory.k4).vertices &
                block(inventory, anchor_triangle).vertices == {shared_cut},
                "purported K4+T anchor does not have one physical shared cut")

        others = tuple(index for index in core_triangles if index != anchor_triangle)
        phase3_boundaries = ancestor_minimal_cycles(inventory, others)
        phase3 = tuple(OpenSide(index, upstream_cut(inventory, index),
                                boundary_open(inventory, core_vertices, index,
                                              upstream_cut(inventory, index)))
                       for index in phase3_boundaries)
        phase3_sets = tuple(item.vertices for item in phase3)
        if phase3_sets:
            require(sum(map(len, phase3_sets)) == len(set().union(*phase3_sets)),
                    "ancestor-minimal triangle sides overlap")
            anchor_vertices = frozenset(set(core_vertices) - set().union(*phase3_sets))
        else:
            anchor_vertices = core_vertices
        verify_partition(inventory, core_vertices,
                         (anchor_vertices, *phase3_sets),
                         "phase-3 triangle partition")
        require(len(phase3) <= len(core_triangles) - 1,
                "more triangle sides than unretained triangles")

    plan = PartitionPlan(profile, h, phase1, root_vertices, phase2,
                         core_vertices, anchor_triangle, phase3, anchor_vertices)
    audit_plan(inventory, plan)
    return plan


def final_piece_sets(plan):
    return (plan.anchor_vertices,
            *(item.vertices for item in plan.phase3),
            *(item.vertices for item in plan.phase2),
            *(item.vertices for item in plan.phase1))


def audit_plan(inventory, plan):
    """Re-derive every boundary and owner set; trust no stored plan claim."""
    profile, h = derive_profile(inventory)
    require((plan.profile, plan.h) == (profile, h),
            "plan profile/nontriangle count is not adjacency-derived")

    expected_first = first_hull_bridges(inventory)
    require(tuple(item.bridge_block for item in plan.phase1) == expected_first,
            "plan first-bridge set changed")
    for item in plan.phase1:
        require(item.vertices == bridge_away_component(inventory, item.bridge_block),
                "stored first-bridge side is not the complete physical component")
    away = tuple(item.vertices for item in plan.phase1)
    expected_root = (inventory.graph.vertices if not away else
                     frozenset(set(inventory.graph.vertices) - set().union(*away)))
    require(plan.root_vertices == expected_root, "stored phase-1 root changed")
    verify_partition(inventory, inventory.graph.vertices,
                     (plan.root_vertices, *away), "audited phase-1 partition")

    root_nontriangles = tuple(index for index in cycle_ids_in(inventory, plan.root_vertices)
                              if block(inventory, index).cycle_length != 3)
    expected_phase2 = ancestor_minimal_cycles(inventory, root_nontriangles)
    require(tuple(item.boundary_block for item in plan.phase2) == expected_phase2,
            "plan nontriangle boundary set changed")
    for item in plan.phase2:
        require(item.upstream_cut == upstream_cut(inventory, item.boundary_block),
                "nontriangle upstream articulation changed")
        require(item.vertices == boundary_open(inventory, plan.root_vertices,
                                               item.boundary_block,
                                               item.upstream_cut),
                "stored nontriangle side is not Q-c plus all descendants")
    phase2_sets = tuple(item.vertices for item in plan.phase2)
    expected_core = (plan.root_vertices if not phase2_sets else
                     frozenset(set(plan.root_vertices) - set().union(*phase2_sets)))
    require(plan.core_vertices == expected_core, "stored K4+kT core changed")
    verify_partition(inventory, plan.root_vertices,
                     (plan.core_vertices, *phase2_sets),
                     "audited phase-2 partition")

    core_triangles = tuple(index for index in inventory.cycles
                           if block(inventory, index).vertices <= plan.core_vertices)
    if not core_triangles:
        require(plan.anchor_triangle is None and not plan.phase3 and
                plan.anchor_vertices == plan.core_vertices,
                "k=0 plan manufactured a triangle anchor or side")
    else:
        expected_anchor = choose_nearest_triangle(inventory, core_triangles)
        require(plan.anchor_triangle == expected_anchor,
                "stored anchor is not the canonical nearest triangle")
        others = tuple(index for index in core_triangles if index != expected_anchor)
        expected_phase3 = ancestor_minimal_cycles(inventory, others)
        require(tuple(item.boundary_block for item in plan.phase3) == expected_phase3,
                "plan triangle boundary set changed")
        for item in plan.phase3:
            require(item.upstream_cut == upstream_cut(inventory, item.boundary_block),
                    "triangle upstream articulation changed")
            require(item.vertices == boundary_open(inventory, plan.core_vertices,
                                                   item.boundary_block,
                                                   item.upstream_cut),
                    "stored triangle side is not Q-c plus all descendants")
        phase3_sets = tuple(item.vertices for item in plan.phase3)
        expected_anchor_vertices = (plan.core_vertices if not phase3_sets else
                                    frozenset(set(plan.core_vertices) -
                                              set().union(*phase3_sets)))
        require(plan.anchor_vertices == expected_anchor_vertices,
                "stored anchor owner set changed")
        verify_partition(inventory, plan.core_vertices,
                         (plan.anchor_vertices, *phase3_sets),
                         "audited phase-3 partition")

    final = final_piece_sets(plan)
    verify_partition(inventory, inventory.graph.vertices, final,
                     "final original-vertex partition")
    for cut in inventory.cuts:
        require(sum(cut in side for side in final) == 1,
                "physical articulation has nonunique final owner")
    return True


# ---------------------------------------------------------------------------
# Independent topology-to-ledger derivation.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PieceReceipt:
    phase: str
    category: str
    vertices: frozenset
    rank: int
    cycle_ids: tuple[int, ...]
    cycle_lengths: tuple[int, ...]
    owned_original_cycles: tuple[int, ...]
    floor: int
    strict: bool
    contract: str
    charge_block: int | None


@dataclass(frozen=True)
class Ledger:
    profile: str
    h: int
    k: int
    anchor_kind: str
    anchor_floor: int
    s: int
    b: int
    value: int
    strict: bool
    receipts: tuple[PieceReceipt, ...]
    charge_blocks: tuple[int, ...]
    contracts: tuple[str, ...]


def side_receipt(inventory, phase, vertices, boundary_block=None):
    analysis = analyze_piece(inventory, vertices)
    require_cactus(analysis, f"{phase} side")

    if phase == "phase1":
        require(analysis.rank >= 1, "phase-1 away side unexpectedly has rank zero")
        if analysis.rank == 1:
            cycle_id = analysis.positive_ids[0]
            length = block(inventory, cycle_id).cycle_length
            require(length % 2 == 1, "phase-1 unicycle is not residual odd")
            if length == 3:
                category = "triangle-positive"
                contract = "R31K-TRIANGULAR-BLOCK-v2"
                floor, strict, charge = 0, True, None
            else:
                category = "charged-odd-unicycle"
                contract = "R31K-ODD-UNICYCLIC-LOWER-v2"
                floor, strict, charge = -1, True, cycle_id
        else:
            category = "cactus-rank>=2-positive"
            contract = "R31K-CACTUS-RANK2PLUS-v2"
            floor, strict, charge = 0, True, None

    elif phase == "phase2":
        require(boundary_block is not None and
                block(inventory, boundary_block).kind == "cycle" and
                block(inventory, boundary_block).cycle_length != 3,
                "phase-2 side lacks its selected original nontriangle")
        if analysis.rank == 0:
            category = "charged-tree"
            contract = "R31K-TREE-EXACT-v2"
            floor, strict, charge = -1, False, boundary_block
        elif analysis.rank == 1:
            cycle_id = analysis.positive_ids[0]
            length = block(inventory, cycle_id).cycle_length
            require(length % 2 == 1, "phase-2 unicycle is not residual odd")
            if length == 3:
                category = "triangle-positive"
                contract = "R31K-TRIANGULAR-BLOCK-v2"
                floor, strict, charge = 0, True, None
            else:
                category = "charged-odd-unicycle"
                contract = "R31K-ODD-UNICYCLIC-LOWER-v2"
                floor, strict, charge = -1, True, boundary_block
        else:
            category = "cactus-rank>=2-positive"
            contract = "R31K-CACTUS-RANK2PLUS-v2"
            floor, strict, charge = 0, True, None

    elif phase == "phase3":
        require(boundary_block is not None and
                block(inventory, boundary_block).kind == "cycle" and
                block(inventory, boundary_block).cycle_length == 3,
                "phase-3 side lacks its selected original triangle")
        require(all(length == 3 for length in analysis.cycle_lengths),
                "phase-3 side is not a triangular block graph/tree")
        if analysis.rank == 0:
            category = "triangle-open-tree"
            contract = "R31K-TREE-EXACT-v2"
            floor, strict, charge = -1, False, None
        else:
            category = "triangular-block-positive"
            contract = "R31K-TRIANGULAR-BLOCK-v2"
            floor, strict, charge = 0, True, None
    else:
        raise VerifyError("unknown ledger phase")

    owned_original_cycles = tuple(index for index in inventory.cycles
                                  if block(inventory, index).edges & analysis.edges)
    return PieceReceipt(phase, category, vertices, analysis.rank,
                        analysis.positive_ids, analysis.cycle_lengths,
                        owned_original_cycles, floor, strict, contract, charge)


def anchor_receipt(inventory, plan):
    analysis = analyze_piece(inventory, plan.anchor_vertices)
    if plan.anchor_triangle is None:
        require(analysis.positive_ids == (inventory.k4,) and analysis.rank == 3,
                "k=0 anchor is not a rooted literal K4 territory")
        contract = "R31K-K4-ROOTED-v2"
        category = "strict-rooted-K4-anchor"
    else:
        require(set(analysis.positive_ids) == {inventory.k4, plan.anchor_triangle} and
                analysis.rank == 4 and analysis.cycle_lengths == (3,),
                "k>=1 anchor is not exactly literal K4 plus one triangle")
        route = path_from_root(inventory, ("B", plan.anchor_triangle))
        require(len(route) == 3 and route[1][0] == "C",
                "K4+T analytic anchor is not a direct shared-cut packet")
        contract = "R31K-K4-T-SHARED-v2"
        category = "strict-shared-K4+T-anchor"
    item = CONTRACTS[contract]
    require(item.floor in (2, 3) and item.strict,
            "anchor contract lost its strict fixed floor")
    owned_original_cycles = tuple(index for index in inventory.cycles
                                  if block(inventory, index).edges & analysis.edges)
    return PieceReceipt("anchor", category, plan.anchor_vertices, analysis.rank,
                        analysis.positive_ids, analysis.cycle_lengths,
                        owned_original_cycles, item.floor, item.strict, contract, None)


def derive_ledger(inventory, plan):
    # This function receives only structural owner sets/boundaries.  It
    # independently reconstructs every induced piece before assigning floors.
    audit_plan(inventory, plan)
    receipts = [anchor_receipt(inventory, plan)]
    receipts.extend(side_receipt(inventory, "phase3", item.vertices,
                                 item.boundary_block)
                    for item in plan.phase3)
    receipts.extend(side_receipt(inventory, "phase2", item.vertices,
                                 item.boundary_block)
                    for item in plan.phase2)
    receipts.extend(side_receipt(inventory, "phase1", item.vertices)
                    for item in plan.phase1)
    receipts = tuple(receipts)

    h = sum(block(inventory, index).cycle_length != 3
            for index in inventory.cycles)
    k = sum(block(inventory, index).vertices <= plan.core_vertices
            for index in inventory.cycles)
    require(all(block(inventory, index).cycle_length == 3
                for index in inventory.cycles
                if block(inventory, index).vertices <= plan.core_vertices),
            "ledger core count includes a nontriangle")
    charges = tuple(item.charge_block for item in receipts
                    if item.charge_block is not None)
    nontriangles = {index for index in inventory.cycles
                    if block(inventory, index).cycle_length != 3}
    require(len(charges) == len(set(charges)),
            "two potentially negative phase-1/2 pieces share a charge")
    require(set(charges) <= nontriangles,
            "a potentially negative piece is charged outside original nontriangles")
    charged_receipts = tuple(item for item in receipts
                             if item.charge_block is not None)
    for item in charged_receipts:
        require(item.charge_block in item.owned_original_cycles,
                "negative piece does not physically own its charged nontriangle")
    for left, right in itertools.combinations(charged_receipts, 2):
        require(not (set(left.owned_original_cycles) &
                     set(right.owned_original_cycles) & nontriangles),
                "two negative pieces physically own the same original nontriangle")

    # Every original positive block must have exactly one final owner even when
    # an opening destroys that block inside the owner's induced subgraph.  The
    # edge-intersection owner relation is derived independently of intact rank.
    positive_originals = (inventory.k4, *inventory.cycles)
    for original in positive_originals:
        owners = [item for item in receipts
                  if block(inventory, original).edges &
                     induced_edges(inventory.graph.edges, item.vertices)]
        require(len(owners) == 1,
                "original positive block has zero or multiple final owners")
    s = len(charges)
    require(s <= h <= 2, "nontriangle charge injection s<=h failed")

    b = sum(item.phase == "phase3" and item.category == "triangle-open-tree"
            for item in receipts)
    phase3_count = sum(item.phase == "phase3" for item in receipts)
    require(b <= phase3_count, "tree-side count exceeds triangle sides")
    if k == 0:
        require(plan.anchor_triangle is None and b == 0,
                "triangle-free core has a K4+T charge")
        anchor_floor = 2
        lower_chain = 2 - h
    else:
        require(plan.anchor_triangle is not None,
                "nonempty triangle core lacks its retained triangle")
        require(phase3_count <= k - 1 and b <= k - 1,
                "b<=k-1 triangle-side injection failed")
        require(k <= 4 - h, "k<=4-h residual injection failed")
        anchor_floor = 3
        lower_chain = 4 - k - h
    require(lower_chain >= 0, "symbolic integer ledger lower chain is negative")

    anchor = receipts[0]
    require(anchor.floor == anchor_floor and anchor.strict,
            "strictness does not come from the authenticated anchor")
    value_from_pieces = sum(item.floor for item in receipts)
    value = anchor_floor - s - b
    require(value_from_pieces == value,
            "piece floors disagree with anchor-s-b ledger")
    require(value >= lower_chain >= 0,
            "exact integer ledger anchor-s-b is negative")

    used_contracts = {
        "R31K-RESIDUAL-SIEVE-v2",
        "R31K-INDUCED-SUPERADD-v2",
        "R31K-TREE-EXACT-v2",
        "R31K-ODD-UNICYCLIC-LOWER-v2",
        "R31K-TRIANGULAR-BLOCK-v2",
        "R31K-CACTUS-RANK2PLUS-v2",
        "R31K-K4-ROOTED-v2",
        "R31K-K4-T-SHARED-v2",
    }
    require(used_contracts == EXPECTED_CONTRACT_IDS,
            "complete R31-K contract manifest changed")
    require(used_contracts <= EXPECTED_CONTRACT_IDS,
            "ledger selected an unknown analytic contract")
    strict = anchor.strict
    require(strict and value >= 0,
            "final positivity is not strict at a nonnegative integer floor")
    ledger = Ledger(plan.profile, h, k, anchor.category, anchor_floor,
                    s, b, value, strict, receipts, charges,
                    tuple(sorted(used_contracts)))
    audit_ledger(inventory, plan, ledger)
    return ledger


def audit_ledger(inventory, plan, ledger):
    """Second arithmetic pass from piece topology, not stored s/b/value."""
    require(ledger.profile == derive_profile(inventory)[0],
            "ledger profile changed")
    anchor = anchor_receipt(inventory, plan)
    fresh = []
    fresh.extend(side_receipt(inventory, "phase3", item.vertices,
                              item.boundary_block) for item in plan.phase3)
    fresh.extend(side_receipt(inventory, "phase2", item.vertices,
                              item.boundary_block) for item in plan.phase2)
    fresh.extend(side_receipt(inventory, "phase1", item.vertices)
                 for item in plan.phase1)
    fresh = tuple(fresh)
    fresh_charges = tuple(item.charge_block for item in fresh
                          if item.charge_block is not None)
    fresh_s = len(fresh_charges)
    fresh_b = sum(item.phase == "phase3" and item.floor == -1 for item in fresh)
    fresh_value = anchor.floor + sum(item.floor for item in fresh)
    require((ledger.anchor_floor, ledger.s, ledger.b, ledger.value) ==
            (anchor.floor, fresh_s, fresh_b, fresh_value),
            "independent ledger replay disagrees")
    require(ledger.charge_blocks == fresh_charges,
            "independent charge replay disagrees")
    require(ledger.receipts == (anchor, *fresh),
            "stored piece receipts disagree with topology replay")
    expected_contracts = tuple(sorted(EXPECTED_CONTRACT_IDS))
    require(ledger.contracts == expected_contracts,
            "independent contract replay disagrees")
    require(ledger.value >= 0 and ledger.strict,
            "replayed strict integer ledger does not prove sigma>0")
    return True


def verify(vertices, edges):
    """Authenticate every analytic contract, then verify one adjacency input."""
    audit_sources()
    inventory = reconstruct(vertices, edges)
    profile, h = derive_profile(inventory)
    plan = construct_plan(inventory, profile, h)
    ledger = derive_ledger(inventory, plan)
    return inventory, plan, ledger


# ---------------------------------------------------------------------------
# Independent adjacency fixture generator.
# ---------------------------------------------------------------------------


def add_clique(edges, vertices):
    edges.update(edge(left, right)
                 for left, right in itertools.combinations(vertices, 2))


def add_cycle(edges, vertices):
    require(len(vertices) >= 3 and len(set(vertices)) == len(vertices),
            "bad generated cycle")
    edges.update(edge(vertices[index], vertices[(index + 1) % len(vertices)])
                 for index in range(len(vertices)))


class Builder:
    def __init__(self):
        self.vertices = set()
        self.edges = set()
        self.serial = 0
        self.cycles = []
        self.routing = []

    def fresh(self, prefix):
        vertex = (prefix, self.serial)
        self.serial += 1
        self.vertices.add(vertex)
        return vertex

    def k4(self):
        vertices = tuple(self.fresh("K") for _ in range(4))
        add_clique(self.edges, vertices)
        return vertices

    def cycle(self, length, port=None):
        vertices = ([port] if port is not None else [])
        vertices += [self.fresh(f"C{length}")
                     for _ in range(length - len(vertices))]
        add_cycle(self.edges, vertices)
        result = tuple(vertices)
        self.cycles.append(result)
        return result

    def bridge_path(self, left, right, length):
        require(type(length) is int and length >= 1,
                "generated bridge length below one")
        internal = [self.fresh("R") for _ in range(length - 1)]
        sequence = (left, *internal, right)
        self.edges.update(edge(a, b) for a, b in zip(sequence, sequence[1:]))
        self.routing.extend(internal)
        return sequence

    def tree_payload(self, root, count):
        require(type(count) is int and count >= 0, "bad payload size")
        made = []
        for index in range(count):
            if index == 0:
                parent = root
            elif index % 4 == 0:
                parent = root
            elif index % 3 == 0:
                parent = made[index // 3 - 1]
            else:
                parent = made[index - 1]
            vertex = self.fresh("P")
            self.edges.add(edge(parent, vertex))
            made.append(vertex)
        return tuple(made)

    def graph(self):
        return frozenset(self.vertices), frozenset(self.edges)


def profile_lengths(profile, odd_length=7):
    require(type(odd_length) is int and odd_length >= 5 and odd_length % 2 == 1,
            "generated odd nontriangle is invalid")
    return {
        "T4": (3, 3, 3, 3),
        "T3+odd>=5": (3, 3, 3, odd_length),
        "T2+C5+C5": (3, 3, 5, 5),
    }[profile]


def fixture(profile, topology, route_length=3, payload_depth=0, odd_length=7):
    lengths = list(profile_lengths(profile, odd_length))
    builder = Builder()
    k4 = builder.k4()

    if topology == "shared-star":
        for length in lengths:
            builder.cycle(length, k4[0])

    elif topology == "repeated-cuts":
        for index, length in enumerate(lengths):
            builder.cycle(length, k4[index // 2])

    elif topology == "nested":
        parent = k4[0]
        for length in lengths:
            current = builder.cycle(length, parent)
            parent = current[1]

    elif topology == "nontriangle-front":
        nontriangles = [length for length in lengths if length != 3]
        require(nontriangles, "nontriangle-front requested for T4")
        remaining = list(lengths)
        first_length = nontriangles[0]
        remaining.remove(first_length)
        current = builder.cycle(first_length, k4[0])
        parent = current[1]
        for length in remaining:
            current = builder.cycle(length, parent)
            parent = current[1]

    elif topology == "four-arms":
        for index, length in enumerate(lengths):
            current = builder.cycle(length)
            builder.bridge_path(k4[index], current[0], route_length + index)

    elif topology == "one-bridge-nest":
        current = builder.cycle(lengths[0])
        builder.bridge_path(k4[0], current[0], route_length)
        parent = current[1]
        for length in lengths[1:]:
            current = builder.cycle(length, parent)
            parent = current[1]

    elif topology == "mixed-bridge-shared":
        triangles = [length for length in lengths if length == 3]
        nontriangles = [length for length in lengths if length != 3]
        if nontriangles:
            detached = builder.cycle(nontriangles.pop())
            builder.bridge_path(k4[0], detached[0], route_length)
        else:
            detached = builder.cycle(triangles.pop())
            builder.bridge_path(k4[0], detached[0], route_length)
        first = builder.cycle(triangles.pop(0), k4[1])
        parent = first[1]
        if triangles:
            nested = builder.cycle(triangles.pop(0), parent)
            parent = nested[1]
        for length in triangles:
            builder.cycle(length, k4[2])
        for length in nontriangles:
            builder.cycle(length, k4[3])

    elif topology == "deep-bridge":
        # A first physical bridge below an already retained positive block.
        first = builder.cycle(3, k4[0])
        lengths.remove(3)
        detached_length = next((length for length in reversed(lengths)
                                if length != 3), lengths[-1])
        lengths.remove(detached_length)
        detached = builder.cycle(detached_length)
        builder.bridge_path(first[1], detached[0], route_length)
        parent = detached[1]
        if lengths:
            nested = builder.cycle(lengths.pop(0), parent)
            parent = nested[1]
        for length in lengths:
            builder.cycle(length, k4[2])

    else:
        raise VerifyError("unknown generated topology")

    if payload_depth:
        builder.tree_payload(k4[2], payload_depth)
        for index, current in enumerate(tuple(builder.cycles)):
            builder.tree_payload(current[-1], min(payload_depth, index + 3))
        for index, current in enumerate(tuple(builder.routing)[:4]):
            builder.tree_payload(current, min(payload_depth, index + 1))
    return builder.graph()


def opaque_relabel(vertices, edges, salt):
    ordered = sorted(vertices, key=repr)
    count = len(ordered)
    permutation = list(reversed(range(count)))
    if count:
        shift = salt % count
        permutation = permutation[shift:] + permutation[:shift]
    mapping = {vertex: ("opaque", salt, 1009 * permutation[index] + 17)
               for index, vertex in enumerate(ordered)}
    return (frozenset(mapping[vertex] for vertex in vertices),
            frozenset(edge(mapping[left], mapping[right])
                      for current in edges for left, right in [tuple(current)]))


def semantic_signature(plan, ledger):
    piece_rows = tuple(sorted((item.phase, item.category, item.rank,
                               item.cycle_lengths, len(item.owned_original_cycles),
                               item.floor)
                              for item in ledger.receipts))
    return (plan.profile, plan.h, len(plan.phase1), len(plan.phase2),
            len(plan.phase3), ledger.k, ledger.anchor_kind,
            ledger.s, ledger.b, ledger.value, piece_rows,
            ledger.contracts)


def expansion_signature(plan, ledger):
    # Vertex counts deliberately do not appear: K2 subdivision and one-root
    # tree growth preserve this semantic receipt.
    return (plan.profile, len(plan.phase1), len(plan.phase2), len(plan.phase3),
            ledger.k, ledger.anchor_kind, ledger.s, ledger.b, ledger.value,
            tuple(sorted((item.phase, item.category, item.rank,
                          item.cycle_lengths)
                         for item in ledger.receipts)))


# ---------------------------------------------------------------------------
# Audits: broad topology coverage, opaque replay, expansion, and mutations.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AuditResult:
    generated: int
    relabeled: int
    profiles: tuple[tuple[str, int], ...]
    anchors: tuple[tuple[str, int], ...]
    categories: tuple[tuple[str, int], ...]
    four_arm_cases: int
    expansion_cases: int
    hostile_rejections: tuple[str, ...]
    rewires_distinguished: int
    source_files: int


def expansion_audit():
    signatures = set()
    sizes = []
    for length, payload in ((1, 0), (2, 4), (9, 11), (41, 19)):
        vertices, edges = fixture("T3+odd>=5", "four-arms",
                                  route_length=length,
                                  payload_depth=payload,
                                  odd_length=9)
        _, plan, ledger = verify(vertices, edges)
        signatures.add(expansion_signature(plan, ledger))
        sizes.append(len(vertices))
    require(len(signatures) == 1 and sizes == sorted(sizes),
            "K2/tree expansion changed the semantic ledger")

    # Explicitly cross the usual recursive-DFS depth to authenticate that the
    # physical verifier itself, not only the theorem prose, handles long K2s.
    vertices, edges = fixture("T4", "one-bridge-nest",
                              route_length=1401, payload_depth=0)
    _, plan, ledger = verify(vertices, edges)
    require(plan.phase1 and ledger.value >= 0,
            "very-long physical connector was not verified")
    return 5


def graph_with_lengths(lengths):
    builder = Builder()
    k4 = builder.k4()
    for length in lengths:
        builder.cycle(length, k4[0])
    return builder.graph()


def hostile_tests():
    global SOURCE_ROOT
    rejected = []
    base_vertices, base_edges = fixture("T2+C5+C5", "shared-star",
                                        payload_depth=7)
    inventory, _, _ = verify(base_vertices, base_edges)
    k4 = block(inventory, inventory.k4)
    c5 = next(block(inventory, index) for index in inventory.cycles
              if block(inventory, index).cycle_length == 5)

    # Chord: no longer a literal cycle block.
    chord = next(edge(left, right)
                 for left, right in itertools.combinations(c5.vertices, 2)
                 if edge(left, right) not in base_edges)
    rejected.append(expect_rejection(
        lambda: verify(base_vertices, frozenset(set(base_edges) | {chord})),
        "cycle chord / unsupported block"))

    # Subdivide one literal K4 edge: rank is preserved, literal topology is not.
    kedge = next(iter(k4.edges))
    left, right = tuple(kedge)
    subdivision = ("hostile-subdivision", 1)
    subdivided_vertices = frozenset(set(base_vertices) | {subdivision})
    subdivided_edges = set(base_edges)
    subdivided_edges.remove(kedge)
    subdivided_edges.update({edge(left, subdivision), edge(subdivision, right)})
    rejected.append(expect_rejection(
        lambda: verify(subdivided_vertices, frozenset(subdivided_edges)),
        "subdivided K4 edge"))

    # Two cross-block ears merge nominal blocks into an unsupported block.
    triangle = next(block(inventory, index) for index in inventory.cycles
                    if block(inventory, index).cycle_length == 3)
    shared = triangle.vertices & k4.vertices
    tprivate = list(triangle.vertices - shared)
    cprivate = list(c5.vertices - k4.vertices - triangle.vertices)
    require(len(tprivate) >= 2 and len(cprivate) >= 2,
            "hostile fixture lacks private endpoints")
    ears = {edge(tprivate[0], cprivate[0]), edge(tprivate[1], cprivate[1])}
    rejected.append(expect_rejection(
        lambda: verify(base_vertices, frozenset(set(base_edges) | ears)),
        "hidden cross-block positive connector"))

    # Delete a payload edge while retaining its endpoint: disconnected input.
    payload_edge = next(current for current in base_edges
                        if any(isinstance(vertex, tuple) and vertex[0] == "P"
                               for vertex in current))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices, frozenset(set(base_edges) - {payload_edge})),
        "omitted rooted payload edge"))

    rejected.append(expect_rejection(
        lambda: verify(base_vertices,
                       frozenset(set(base_edges) | {frozenset({left})})),
        "malformed loop edge"))
    outsider = ("outside", 999)
    rejected.append(expect_rejection(
        lambda: verify(base_vertices,
                       frozenset(set(base_edges) | {frozenset({left, outsider})})),
        "foreign adjacency endpoint"))
    rejected.append(expect_rejection(
        lambda: verify(set(base_vertices), base_edges),
        "mutable vertex-set API injection"))

    for label, lengths in (
        ("even residual cycle", (3, 3, 3, 4)),
        ("nonpentagon residual pair", (3, 3, 5, 7)),
        ("three residual nontriangles", (3, 5, 5, 5)),
        ("four residual nontriangles", (5, 5, 5, 5)),
    ):
        rejected.append(expect_rejection(
            lambda current=lengths: verify(*graph_with_lengths(current)), label))

    rejected.append(expect_rejection(
        lambda: verify(*graph_with_lengths((3, 3, 3, 3, 3))),
        "fifth cycle / rank-eight graph"))

    # The public production entry must authenticate the fixed contract table,
    # rather than relying on main()->audit() to have run first.
    contract_id = "R31K-K4-T-SHARED-v2"
    original = CONTRACTS[contract_id]
    CONTRACTS[contract_id] = replace(
        original, floor=99, claim=original.claim + " [HOSTILE]",
        sha256="0" * 64)
    try:
        rejected.append(expect_rejection(
            lambda: verify(base_vertices, base_edges),
            "public API analytic contract mutation"))
    finally:
        CONTRACTS[contract_id] = original

    # Likewise, direct verify() must reject mutated source bytes.  Build a
    # complete temporary shadow of the five pinned files, mutate one shadow
    # byte stream, and restore SOURCE_ROOT before the directory is removed.
    original_root = SOURCE_ROOT
    with tempfile.TemporaryDirectory(prefix="r31k-hostile-source-") as directory:
        shadow_root = Path(directory)
        for item in {contract.source: contract
                     for contract in CONTRACTS.values()}.values():
            target = shadow_root / item.source
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((original_root / item.source).read_bytes())
        source_contract = CONTRACTS["R31K-RESIDUAL-SIEVE-v2"]
        hostile_source = shadow_root / source_contract.source
        hostile_source.write_bytes(hostile_source.read_bytes() + b"\nHOSTILE")
        SOURCE_ROOT = shadow_root
        try:
            rejected.append(expect_rejection(
                lambda: verify(base_vertices, base_edges),
                "public API analytic source-byte mutation"))
        finally:
            SOURCE_ROOT = original_root

    # The public verifier must not trust a caller-mutated structural plan or
    # independently stored arithmetic receipt.  Replay both from adjacency.
    _, baseline_plan, baseline_ledger = verify(base_vertices, base_edges)
    rejected.append(expect_rejection(
        lambda: audit_plan(inventory, replace(baseline_plan, h=99)),
        "forged structural-plan field"))
    rejected.append(expect_rejection(
        lambda: audit_ledger(inventory, baseline_plan,
                             replace(baseline_ledger, value=99)),
        "forged ledger value"))

    # Four independent arms are now required to pass, not a hostile rejection.
    _, four_plan, four_ledger = verify(*fixture("T2+C5+C5", "four-arms",
                                                route_length=13,
                                                payload_depth=5))
    require(len(four_plan.phase1) == 4 and four_ledger.s == 2 and
            four_ledger.k == 0 and four_ledger.value == 0,
            "four-independent-arm closure was not authenticated")

    # Same profile, physically different bridge topology must remain visible.
    _, star_plan, star_ledger = verify(*fixture("T2+C5+C5", "shared-star"))
    _, arm_plan, arm_ledger = verify(*fixture("T2+C5+C5", "four-arms"))
    require((len(star_plan.phase1), len(star_plan.phase2), star_ledger.k) !=
            (len(arm_plan.phase1), len(arm_plan.phase2), arm_ledger.k),
            "same-profile physical bridge rewire was not distinguished")
    return tuple(rejected), 1


def audit():
    source_files = audit_sources()
    plans = (
        ("T4", "shared-star", 3, 0, 7),
        ("T4", "repeated-cuts", 3, 5, 7),
        ("T4", "nested", 3, 3, 7),
        ("T4", "four-arms", 11, 4, 7),
        ("T4", "one-bridge-nest", 8, 6, 7),
        ("T4", "deep-bridge", 9, 5, 7),
        ("T3+odd>=5", "shared-star", 3, 4, 5),
        ("T3+odd>=5", "repeated-cuts", 3, 5, 7),
        ("T3+odd>=5", "nested", 3, 6, 9),
        ("T3+odd>=5", "nontriangle-front", 3, 7, 11),
        ("T3+odd>=5", "four-arms", 13, 5, 13),
        ("T3+odd>=5", "one-bridge-nest", 7, 4, 9),
        ("T3+odd>=5", "mixed-bridge-shared", 10, 6, 7),
        ("T3+odd>=5", "deep-bridge", 12, 5, 5),
        ("T2+C5+C5", "shared-star", 3, 4, 7),
        ("T2+C5+C5", "repeated-cuts", 3, 6, 7),
        ("T2+C5+C5", "nested", 3, 5, 7),
        ("T2+C5+C5", "nontriangle-front", 3, 7, 7),
        ("T2+C5+C5", "four-arms", 15, 6, 7),
        ("T2+C5+C5", "one-bridge-nest", 9, 5, 7),
        ("T2+C5+C5", "mixed-bridge-shared", 11, 7, 7),
        ("T2+C5+C5", "deep-bridge", 14, 5, 7),
    )
    profile_counts = Counter()
    anchor_counts = Counter()
    category_counts = Counter()
    generated = 0
    relabeled = 0
    four_arm_cases = 0

    for index, (profile, topology, route_length, payload_depth, odd_length) in enumerate(plans):
        vertices, edges = fixture(profile, topology,
                                  route_length=route_length,
                                  payload_depth=payload_depth,
                                  odd_length=odd_length)
        inventory, plan, ledger = verify(vertices, edges)
        require(plan.profile == profile and ledger.profile == profile,
                "generated residual profile misclassified")
        require(sum(block(inventory, item).rank for item in
                    (inventory.k4, *inventory.cycles)) == 7,
                "generated physical block-rank sum changed")
        profile_counts[profile] += 1
        anchor_counts[ledger.anchor_kind] += 1
        category_counts.update(item.category for item in ledger.receipts)
        generated += 1
        if topology == "four-arms":
            require(len(plan.phase1) == 4,
                    "four-arm fixture did not produce four first bridges")
            four_arm_cases += 1

        relabeled_graph = opaque_relabel(vertices, edges, 31 + 17 * index)
        _, relabeled_plan, relabeled_ledger = verify(*relabeled_graph)
        require(semantic_signature(plan, ledger) ==
                semantic_signature(relabeled_plan, relabeled_ledger),
                "opaque relabeling changed the semantic certificate")
        relabeled += 1

    require(set(profile_counts) == {"T4", "T3+odd>=5", "T2+C5+C5"},
            "residual profile coverage incomplete")
    require({"strict-rooted-K4-anchor", "strict-shared-K4+T-anchor"}
            <= set(anchor_counts), "anchor branch coverage incomplete")
    required_categories = {
        "strict-rooted-K4-anchor", "strict-shared-K4+T-anchor",
        "triangle-positive", "charged-odd-unicycle", "charged-tree",
        "cactus-rank>=2-positive", "triangle-open-tree",
        "triangular-block-positive",
    }
    require(required_categories <= set(category_counts),
            "piece/charge category coverage incomplete")
    require(four_arm_cases == 3, "four-independent-arm profile coverage incomplete")

    expansion_cases = expansion_audit()
    rejected, rewires = hostile_tests()
    return AuditResult(generated, relabeled,
                       tuple(sorted(profile_counts.items())),
                       tuple(sorted(anchor_counts.items())),
                       tuple(sorted(category_counts.items())),
                       four_arm_cases, expansion_cases, rejected, rewires,
                       source_files)


def report(result):
    return "\n".join((
        "R31-K full adjacency semantic verifier: finite corroboration passed",
        "scope: complete physical R31-K only; no global/full-multiblock/single-block claim",
        "input: finite simple adjacency only; no supplied profile, topology, owner, charge, threshold, or partition",
        "reconstruction: iterative Tarjan; literal K4 + four literal cycles; full rooted block-cut tree and every K2",
        "ownership: original vertices; induced connected disjoint exhaustive pieces; unique cut/payload owner",
        "strategy: simultaneous first bridges; ancestor-minimal nontriangles; K4 or direct shared-cut K4+T anchor",
        "ledger: finite implementation replay checks integer anchor-s-b>=0; proof strictness comes from the pinned anchor contract",
        f"analytic source files pinned: {result.source_files}; manifest sha256: {contract_manifest_digest()}",
        f"generated adjacency fixtures: {result.generated}; opaque relabel replays: {result.relabeled}",
        "profiles: " + repr(dict(result.profiles)),
        "anchors: " + repr(dict(result.anchors)),
        "piece categories: " + repr(dict(result.categories)),
        f"four-independent-arm cases accepted: {result.four_arm_cases}",
        f"K2/tree expansion probes (including 1401-edge connector): {result.expansion_cases}",
        f"hostile mutations rejected: {len(result.hostile_rejections)}; same-profile rewires distinguished: {result.rewires_distinguished}",
        "analytic contracts: " + repr(tuple(sorted(EXPECTED_CONTRACT_IDS))),
        "verifier sha256: " + file_digest(Path(__file__)),
        "status: finite corroboration/static implementation replay passed; universal proof is external",
    ))


def main():
    result = audit()
    output = report(result)
    if "--optimized-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-child"],
                               check=False, capture_output=True, text=True)
        require(child.returncode == 0,
                "optimized child failed: " + child.stderr)
        require(child.stderr == "", "optimized child wrote stderr")
        require(child.stdout == output + "\n",
                "normal and -O outputs are not byte-identical")
    print(output)


if __name__ == "__main__":
    main()
