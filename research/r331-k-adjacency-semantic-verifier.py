#!/usr/bin/env python3
"""Adjacency-only semantic gate for the physical R331-K inventory.

The production API is exactly ``verify(vertices, edges)``.  Its only input is a
finite simple graph represented by a nonempty frozenset of original vertices
and a frozenset of unordered two-vertex frozenset edges.  No packet label,
anchor label, block list, route, owner, rank, charge, threshold, or partition
is accepted.

The gate reconstructs every physical edge block with iterative Tarjan,
authenticates exactly two literal K4 blocks and one literal cycle (necessarily
total cyclomatic rank seven), and tries both K4 blocks as the rooted anchor.  It
rebuilds the full block-cut tree including every K2 bridge, opens only the
ancestor-minimal marked frontier among the other K4 and the cycle, and replays
an original-vertex induced connected disjoint exhaustive ownership partition.
Its exact piece ranks are 0, 1, 2, or 3 and its strict integer ledger is
``sigma(G)>2-t>=1>0``, with ``t`` in ``{0,1}`` the number of opened tree
territories.

This program is a fail-closed combinatorial implementation gate and finite
corroboration.  It authenticates source-pinned analytic inputs but does not
turn those pins or the finite fixture suite into a new spectral proof.  It
makes no claim about another packet, a single-block graph, or the global
rank-seven problem.
"""
from __future__ import annotations

import ast
import hashlib
import inspect
import itertools
import json
import shutil
import sys
import tempfile
from collections import Counter, deque
from dataclasses import dataclass, replace
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]
PROFILE = "literal-K4+K4+cycle"


class VerifyError(RuntimeError):
    """Fail-closed semantic rejection."""


def require(condition, message):
    if not condition:
        raise VerifyError(message)


def expect_rejection(action, label, expected_message):
    require(type(expected_message) is str and expected_message,
            f"hostile test lacks an expected rejection reason: {label}")
    try:
        action()
    except VerifyError as error:
        require(expected_message in str(error),
                f"hostile rejection had wrong reason: {label}: {error}")
        return label
    raise VerifyError(f"hostile mutation accepted: {label}")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    return sha256_bytes(path.read_bytes())


# ---------------------------------------------------------------------------
# Immutable analytic manifest anchors.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Contract:
    source: str
    sha256: str
    claim: str
    floor: int | None
    strict: bool


CONTRACT_SPECS = (
    ("R331K-COMBINATORIAL-NOTE-v1", Contract(
        "research/r331-k-adjacency-ownership-note.md",
        "c80c8ae502ed61b8e7e201c302afdcd884dd2775d57892412bdc5cd5a2cf2f11",
        "universal block-cut ownership, exact rank-additivity, and unique-anchor-block proof implemented by this gate",
        None, False)),
    ("R331K-RESIDUAL-SIEVE-v1", Contract(
        "positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md",
        "f45d60cbeefdf523e5aab053af708a388687f05b64a3d569bd1ddda885396ac2",
        "source-pinned registry identifies the physical R331-K residual as two literal K4 blocks plus one odd cycle",
        None, False)),
    ("R331K-INDUCED-SUPERADD-v1", Contract(
        "all-tricyclic-graphs/paper.tex",
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
        "positive-square-energy induced superadditivity on vertex partitions",
        None, False)),
    ("R331K-TREE-EXACT-v1", Contract(
        "all-tricyclic-graphs/paper.tex",
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
        "every nonempty tree T has sigma(T)=-1",
        -1, False)),
    ("R331K-CONNECTED-RANK2-v1", Contract(
        "all-bicyclic-graphs/paper.tex",
        "56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da",
        "every connected rank-two graph has sigma>0",
        0, True)),
    ("R331K-CONNECTED-RANK3-v1", Contract(
        "all-tricyclic-graphs/paper.tex",
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
        "every connected rank-three graph has sigma>=0",
        0, False)),
    ("R331K-TRIANGLE-UNICYCLIC-v1", Contract(
        "packing-two-square-energy/paper.tex",
        "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
        "a connected graph whose unique positive block is a literal triangle has sigma>0",
        0, True)),
    ("R331K-K4-ROOTED-v1", Contract(
        "packing-two-square-energy/paper.tex",
        "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
        "a connected graph whose unique positive block is a literal K4 has sigma>2",
        2, True)),
)

CONTRACTS = dict(CONTRACT_SPECS)

# Independent canonical anchors.  The full-record and source-manifest digests
# below are literal constants filled after this exact encoding is fixed.
EXPECTED_CONTRACT_IDS = frozenset({
    "R331K-COMBINATORIAL-NOTE-v1",
    "R331K-RESIDUAL-SIEVE-v1",
    "R331K-INDUCED-SUPERADD-v1",
    "R331K-TREE-EXACT-v1",
    "R331K-CONNECTED-RANK2-v1",
    "R331K-CONNECTED-RANK3-v1",
    "R331K-TRIANGLE-UNICYCLIC-v1",
    "R331K-K4-ROOTED-v1",
})
EXPECTED_SOURCE_ROWS = frozenset({
    ("research/r331-k-adjacency-ownership-note.md",
     "c80c8ae502ed61b8e7e201c302afdcd884dd2775d57892412bdc5cd5a2cf2f11"),
    ("positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md",
     "f45d60cbeefdf523e5aab053af708a388687f05b64a3d569bd1ddda885396ac2"),
    ("all-tricyclic-graphs/paper.tex",
     "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02"),
    ("all-bicyclic-graphs/paper.tex",
     "56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da"),
    ("packing-two-square-energy/paper.tex",
     "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791"),
})
EXPECTED_FULL_CONTRACT_MANIFEST_SHA256 = (
    "6f97ac8a1bca6ab51f29762ad14ea59dc143ad91fd170e8bf0a2542d4752fcaa")
EXPECTED_SOURCE_MANIFEST_SHA256 = (
    "0764c69830fd50ae478aaade5dccbcba49a3c9cfa7985064e394cf49b6de43ef")


def source_manifest_digest(specs=None):
    specs = CONTRACT_SPECS if specs is None else specs
    rows = sorted({f"{item.source}\t{item.sha256}" for _, item in specs})
    return sha256_bytes(("\n".join(rows) + "\n").encode("utf-8"))


def full_contract_manifest_bytes(specs=None):
    specs = CONTRACT_SPECS if specs is None else specs
    records = []
    for name, item in specs:
        floor = ({"kind": "null"} if item.floor is None else
                 {"kind": "integer", "value": item.floor})
        records.append({
            "id": name,
            "path": item.source,
            "sha256": item.sha256,
            "claim": item.claim,
            "floor": floor,
            "strict": item.strict,
        })
    payload = {"schema": "r331k-contract-manifest-v1", "records": records}
    return json.dumps(payload, ensure_ascii=True,
                      separators=(",", ":")).encode("utf-8")


def full_contract_manifest_digest(specs=None):
    return sha256_bytes(full_contract_manifest_bytes(specs))


def audit_contract_table():
    require(type(CONTRACT_SPECS) is tuple,
            "analytic contract specification container changed")
    require(all(type(row) is tuple and len(row) == 2 and
                type(row[0]) is str and type(row[1]) is Contract
                for row in CONTRACT_SPECS),
            "analytic contract specification row changed")
    require(frozenset(name for name, _ in CONTRACT_SPECS) ==
            EXPECTED_CONTRACT_IDS and
            len(CONTRACT_SPECS) == len(EXPECTED_CONTRACT_IDS),
            "analytic contract ID set changed")
    require(type(CONTRACTS) is dict and
            frozenset(CONTRACTS) == EXPECTED_CONTRACT_IDS,
            "analytic contract lookup changed")
    require(CONTRACTS == dict(CONTRACT_SPECS),
            "analytic contract tuple/lookup disagree")
    for contract_id, item in CONTRACT_SPECS:
        require(type(contract_id) is str and contract_id,
                "malformed contract ID")
        require(type(item.source) is str and item.source,
                f"malformed source path: {contract_id}")
        require(type(item.sha256) is str and len(item.sha256) == 64 and
                all(character in "0123456789abcdef"
                    for character in item.sha256),
                f"malformed source digest: {contract_id}")
        require(type(item.claim) is str and item.claim,
                f"malformed contract claim: {contract_id}")
        require(type(item.strict) is bool,
                f"strict flag malformed: {contract_id}")
        require(item.floor is None or type(item.floor) is int,
                f"contract floor malformed: {contract_id}")
    require(full_contract_manifest_digest() ==
            EXPECTED_FULL_CONTRACT_MANIFEST_SHA256,
            "analytic full contract manifest changed")
    rows = frozenset((item.source, item.sha256)
                     for _, item in CONTRACT_SPECS)
    require(rows == EXPECTED_SOURCE_ROWS,
            "analytic source path/digest manifest changed")
    require(source_manifest_digest() == EXPECTED_SOURCE_MANIFEST_SHA256,
            "analytic source manifest digest changed")


def authenticate_source_blob(blob, expected, label):
    require(sha256_bytes(blob) == expected,
            f"analytic source changed: {label}")


def audit_sources():
    audit_contract_table()
    require(SOURCE_ROOT.is_dir(),
            "analytic source authentication failed: repository absent")
    checked = set()
    for contract_id, item in CONTRACT_SPECS:
        key = (item.source, item.sha256)
        if key in checked:
            continue
        path = SOURCE_ROOT / item.source
        require(path.is_file(),
                f"analytic source authentication failed: missing {contract_id}")
        try:
            blob = path.read_bytes()
        except OSError as error:
            raise VerifyError(
                f"analytic source authentication failed: unreadable {contract_id}") from error
        authenticate_source_blob(blob, item.sha256, contract_id)
        checked.add(key)
    require(checked == set(EXPECTED_SOURCE_ROWS),
            "authenticated source set differs from immutable manifest")
    return len(checked)


# ---------------------------------------------------------------------------
# Physical adjacency and iterative Tarjan reconstruction.
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
    k4s: tuple[int, int]
    cycle: int
    bridge_blocks: tuple[int, ...]


@dataclass(frozen=True)
class Rooting:
    anchor: int
    marked_k4: int
    parent: dict
    depth: dict
    root_order: tuple


@dataclass(frozen=True)
class LocalAnalysis:
    vertices: frozenset
    edges: frozenset
    blocks: tuple[Block, ...]
    rank: int
    positive_blocks: tuple[Block, ...]


def edge(left, right):
    require(left != right, "loop in simple adjacency")
    return frozenset((left, right))


def normalize_graph(vertices, edges):
    require(type(vertices) is frozenset and vertices,
            "vertices must be a nonempty frozenset")
    require(type(edges) is frozenset, "edges must be a frozenset")
    for current in edges:
        require(type(current) is frozenset and len(current) == 2,
                "malformed unordered edge")
        require(current <= vertices, "edge endpoint outside vertex set")
    return PhysicalGraph(vertices, edges)


def adjacency(vertices, edges):
    graph = {vertex: set() for vertex in vertices}
    for current in edges:
        left, right = tuple(current)
        graph[left].add(right)
        graph[right].add(left)
    return graph


def induced_edges(edges, vertices):
    vertices = frozenset(vertices)
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
            for neighbor in graph[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        unseen.difference_update(seen)
        answer.append(frozenset(seen))
    return tuple(answer)


def connected(vertices, edges):
    return bool(vertices) and len(components(vertices, edges)) == 1


def graph_rank(vertices, edges):
    return len(edges) - len(vertices) + len(components(vertices, edges))


def biconnected_edge_blocks(vertices, edges):
    """Iterative edge-stack Tarjan; every physical bridge is a K2 block."""
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
                    require(not edge_stack,
                            "Tarjan edge stack leaked at DFS root")
                continue

            current_edge = edge(current, neighbor)
            if neighbor not in discovery:
                parent[neighbor] = current
                parent_edge[neighbor] = current_edge
                edge_stack.append(current_edge)
                clock += 1
                discovery[neighbor] = low[neighbor] = clock
                frames.append((neighbor, iter(graph[neighbor])))
            elif (parent.get(current) != neighbor and
                  discovery[neighbor] < discovery[current]):
                edge_stack.append(current_edge)
                low[current] = min(low[current], discovery[neighbor])

    union = set().union(*blocks) if blocks else set()
    require(union == set(edges),
            "Tarjan blocks do not exhaust physical edges")
    require(sum(len(current) for current in blocks) == len(edges),
            "Tarjan blocks duplicate physical edges")
    return tuple(blocks)


def classify_block(index, edges):
    require(edges, "empty edge block")
    vertices = frozenset().union(*edges)
    rank = len(edges) - len(vertices) + 1
    degrees = {vertex: sum(vertex in current for current in edges)
               for vertex in vertices}
    if len(edges) == 1:
        require(rank == 0 and len(vertices) == 2,
                "malformed physical bridge")
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
            require(neighbor not in parent,
                    "block-cut incidence contains a cycle")
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
    positive = tuple(current for current in blocks if current.rank)
    k4s = tuple(current.index for current in positive
                if current.kind == "K4")
    cycles = tuple(current.index for current in positive
                   if current.kind == "cycle")
    require(len(k4s) == 2 and len(cycles) == 1 and len(positive) == 3,
            "positive blocks are not exactly two literal K4s and one literal cycle")
    require(tuple(sorted(current.rank for current in positive)) == (1, 3, 3),
            "positive block ranks are not exactly 3+3+1")
    require(sum(current.rank for current in positive) == 7,
            "positive block ranks do not sum to seven")
    cycle = blocks[cycles[0]]
    require(cycle.cycle_length is not None and cycle.cycle_length % 2 == 1,
            "literal cycle is not odd as required by the R331-K residual sieve")

    membership = {
        vertex: tuple(current.index for current in blocks
                      if vertex in current.vertices)
        for vertex in graph.vertices
    }
    cuts = frozenset(vertex for vertex, owners in membership.items()
                     if len(owners) >= 2)
    tree = {("B", current.index): set() for current in blocks}
    for cut in cuts:
        cut_node = ("C", cut)
        tree[cut_node] = set()
        for owner in membership[cut]:
            block_node = ("B", owner)
            tree[cut_node].add(block_node)
            tree[block_node].add(cut_node)
    require(tree, "empty block-cut incidence")
    require(sum(len(neighbors) for neighbors in tree.values()) // 2 ==
            len(tree) - 1,
            "block-cut incidence is not a tree")
    bridges = tuple(current.index for current in blocks
                    if current.kind == "bridge")
    return Inventory(graph, adjacency(graph.vertices, graph.edges), blocks,
                     cuts, tree, tuple(k4s), cycles[0], bridges)


def block(inventory, index):
    require(type(index) is int and 0 <= index < len(inventory.blocks),
            "block index outside inventory")
    return inventory.blocks[index]


def rooting(inventory, anchor):
    require(anchor in inventory.k4s, "root anchor is not one of the literal K4s")
    marked = next(index for index in inventory.k4s if index != anchor)
    parent, depth, order = rooted_tree(inventory.tree, ("B", anchor))
    return Rooting(anchor, marked, parent, depth, order)


def path_from_root(rooted, node):
    require(node in rooted.parent, "block-cut path target absent")
    result = []
    current = node
    while current is not None:
        result.append(current)
        current = rooted.parent[current]
    result.reverse()
    return tuple(result)


def is_ancestor(rooted, ancestor, descendant, strict=False):
    if ancestor not in rooted.depth or descendant not in rooted.depth:
        return False
    if strict and ancestor == descendant:
        return False
    current = descendant
    while (current is not None and
           rooted.depth[current] >= rooted.depth[ancestor]):
        if current == ancestor:
            return True
        current = rooted.parent[current]
    return False


def upstream_cut(inventory, rooted, block_index):
    node = ("B", block_index)
    require(node != ("B", rooted.anchor), "literal K4 root has no upstream cut")
    parent = rooted.parent[node]
    require(parent is not None and parent[0] == "C",
            "positive block lacks an immediate upstream articulation")
    cut = parent[1]
    require(cut in block(inventory, block_index).vertices,
            "upstream articulation lies outside block")
    return cut


def analyze_piece(inventory, vertices):
    require(type(vertices) is frozenset and vertices,
            "piece is empty or not a frozenset")
    require(vertices <= inventory.graph.vertices,
            "piece contains a foreign vertex")
    edges = induced_edges(inventory.graph.edges, vertices)
    require(connected(vertices, edges), "piece is disconnected")
    raw = biconnected_edge_blocks(vertices, edges)
    blocks = tuple(classify_block(index, current)
                   for index, current in enumerate(raw))
    rank = graph_rank(vertices, edges)
    require(rank == sum(current.rank for current in blocks),
            "piece rank is not additive over reconstructed blocks")
    positive = tuple(current for current in blocks if current.rank)
    return LocalAnalysis(vertices, edges, blocks, rank, positive)


def local_positive_edge_sets(analysis):
    return frozenset(current.edges for current in analysis.positive_blocks)


def positive_ids(inventory):
    return (*inventory.k4s, inventory.cycle)


# ---------------------------------------------------------------------------
# Ancestor-minimal marked frontier and exact original-vertex ownership.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OpenSide:
    boundary_block: int
    boundary_kind: str
    upstream_cut: object
    vertices: frozenset
    descendant_mark: int | None
    residual_rank: int
    descendant_rank: int
    rank: int


@dataclass(frozen=True)
class PartitionPlan:
    profile: str
    anchor_block: int
    marked_k4: int
    marked_cycle: int
    mark_relation: str
    frontiers: tuple[int, ...]
    opened: tuple[OpenSide, ...]
    anchor_vertices: frozenset


@dataclass(frozen=True)
class PieceReceipt:
    phase: str
    category: str
    vertices: frozenset
    rank: int
    floor: int
    strict: bool
    contract: str
    boundary_block: int | None = None
    boundary_kind: str | None = None
    descendant_kind: str | None = None


@dataclass(frozen=True)
class Ledger:
    profile: str
    anchor_block: int
    mark_relation: str
    frontier_count: int
    tree_debits: int
    anchor_floor: int
    lower_integer: int
    strict: bool
    receipts: tuple[PieceReceipt, ...]
    contracts: tuple[str, ...]


def mark_relation(rooted, marked_k4, marked_cycle):
    k_node = ("B", marked_k4)
    q_node = ("B", marked_cycle)
    if is_ancestor(rooted, k_node, q_node, strict=True):
        return "K4-before-cycle"
    if is_ancestor(rooted, q_node, k_node, strict=True):
        return "cycle-before-K4"
    return "incomparable"


def ancestor_minimal_marks(rooted, marks):
    marks = tuple(marks)
    mark_set = set(marks)
    selected = []
    for index in marks:
        route = path_from_root(rooted, ("B", index))
        if not any(node[0] == "B" and node[1] in mark_set
                   for node in route[:-1]):
            selected.append(index)
    result = tuple(sorted(selected))
    nodes = tuple(("B", index) for index in result)
    for left, right in itertools.permutations(nodes, 2):
        require(not is_ancestor(rooted, left, right, strict=True),
                "ancestor-minimal marked frontier is not an antichain")
    return result


def boundary_open(inventory, current_vertices, boundary_index, cut):
    """Return X-c plus all physical descendants through X's private vertices."""
    boundary = block(inventory, boundary_index)
    require(boundary.kind in ("K4", "cycle"),
            "R331-K boundary must be a literal K4 or cycle")
    require(boundary.vertices <= current_vertices,
            "boundary block is not intact in current territory")
    require(cut in boundary.vertices,
            "upstream cut lies outside boundary block")
    current_edges = induced_edges(inventory.graph.edges, current_vertices)
    require(boundary.edges <= current_edges,
            "boundary edges are missing from current territory")
    owner_components = components(
        current_vertices, frozenset(current_edges - boundary.edges))
    by_vertex = {}
    for side in owner_components:
        hits = side & boundary.vertices
        require(len(hits) == 1,
                "outside component meets maximal boundary block at multiple vertices")
        owner = next(iter(hits))
        require(owner not in by_vertex,
                "boundary vertex has duplicate outside owner component")
        by_vertex[owner] = side
    require(set(by_vertex) == set(boundary.vertices),
            "boundary decomposition omitted a vertex")
    result = frozenset().union(
        *(by_vertex[vertex] for vertex in boundary.vertices if vertex != cut))
    require(result and cut not in result,
            "opened side is empty or copied its upstream cut")
    require(boundary.vertices - {cut} <= result,
            "opened side omitted X-c")
    require(connected(result, induced_edges(inventory.graph.edges, result)),
            "opened boundary side is disconnected")
    return result


def residual_edges_after_cut(inventory, boundary_index, cut):
    boundary = block(inventory, boundary_index)
    require(cut in boundary.vertices, "residual cut lies outside boundary")
    return induced_edges(boundary.edges, boundary.vertices - {cut})


def residual_rank_after_cut(inventory, boundary_index, cut):
    boundary = block(inventory, boundary_index)
    residual_vertices = boundary.vertices - {cut}
    residual_edges = residual_edges_after_cut(inventory, boundary_index, cut)
    require(connected(residual_vertices, residual_edges),
            "boundary minus its upstream cut is disconnected")
    rank = graph_rank(residual_vertices, residual_edges)
    if boundary.kind == "K4":
        degrees = {vertex: sum(vertex in current for current in residual_edges)
                   for vertex in residual_vertices}
        require(len(residual_vertices) == 3 and len(residual_edges) == 3 and
                all(value == 2 for value in degrees.values()) and rank == 1,
                "literal K4 minus a vertex did not leave a literal triangle")
    else:
        require(boundary.kind == "cycle" and rank == 0 and
                len(residual_edges) == len(residual_vertices) - 1,
                "literal cycle minus a vertex did not leave a path")
    return rank


def verify_partition(inventory, target, pieces, label):
    require(type(target) is frozenset and target,
            f"{label} target is malformed")
    require(type(pieces) is tuple and pieces and
            all(type(side) is frozenset and side for side in pieces),
            f"{label} has an empty or malformed piece")
    union = set().union(*pieces)
    require(union == set(target), f"{label} is not exhaustive")
    require(sum(len(side) for side in pieces) == len(union),
            f"{label} pieces overlap")
    for side in pieces:
        require(side <= target, f"{label} piece escapes target")
        current_edges = induced_edges(inventory.graph.edges, side)
        require(connected(side, current_edges),
                f"{label} piece is disconnected")
        require(current_edges == frozenset(
                    current for current in inventory.graph.edges
                    if current <= side),
                f"{label} piece is not induced")
    return True


def construct_plan(inventory, anchor):
    rooted = rooting(inventory, anchor)
    marks = (rooted.marked_k4, inventory.cycle)
    relation = mark_relation(rooted, *marks)
    frontiers = ancestor_minimal_marks(rooted, marks)
    require(1 <= len(frontiers) <= 2,
            "R331-K frontier does not have one or two marked blocks")

    opened = []
    for frontier in frontiers:
        cut = upstream_cut(inventory, rooted, frontier)
        vertices = boundary_open(inventory, inventory.graph.vertices,
                                 frontier, cut)
        descendants = tuple(index for index in marks
                            if index != frontier and
                            is_ancestor(rooted, ("B", frontier),
                                        ("B", index), strict=True))
        require(len(descendants) <= 1,
                "R331-K frontier has more than one descendant mark")
        descendant = descendants[0] if descendants else None
        residual_rank = residual_rank_after_cut(inventory, frontier, cut)
        descendant_rank = 0 if descendant is None else block(inventory, descendant).rank
        analysis = analyze_piece(inventory, vertices)
        expected_positive = set()
        residual = residual_edges_after_cut(inventory, frontier, cut)
        if residual_rank:
            expected_positive.add(residual)
        if descendant is not None:
            expected_positive.add(block(inventory, descendant).edges)
        require(local_positive_edge_sets(analysis) == frozenset(expected_positive),
                "opened side positive blocks do not equal X-c plus intact descendant mark")
        require(analysis.rank == residual_rank + descendant_rank,
                "opened side rank is not rank(X-c)+sum descendant positive ranks")
        opened.append(OpenSide(frontier, block(inventory, frontier).kind,
                               cut, vertices, descendant, residual_rank,
                               descendant_rank, analysis.rank))
    opened = tuple(opened)
    opened_sets = tuple(item.vertices for item in opened)
    require(sum(len(side) for side in opened_sets) ==
            len(set().union(*opened_sets)),
            "ancestor-minimal marked territories overlap")
    anchor_vertices = frozenset(set(inventory.graph.vertices) -
                                set().union(*opened_sets))
    verify_partition(inventory, inventory.graph.vertices,
                     (anchor_vertices, *opened_sets),
                     "R331-K marked-frontier partition")
    plan = PartitionPlan(PROFILE, anchor, rooted.marked_k4,
                         inventory.cycle, relation, frontiers,
                         opened, anchor_vertices)
    audit_plan(inventory, plan)
    return plan


def final_piece_sets(plan):
    return (plan.anchor_vertices, *(item.vertices for item in plan.opened))


def audit_plan(inventory, plan):
    require(plan.profile == PROFILE, "stored R331-K profile changed")
    rooted = rooting(inventory, plan.anchor_block)
    require((plan.marked_k4, plan.marked_cycle) ==
            (rooted.marked_k4, inventory.cycle),
            "stored marked-block inventory changed")
    relation = mark_relation(rooted, rooted.marked_k4, inventory.cycle)
    require(plan.mark_relation == relation,
            "stored marked-block relation changed")
    marks = (rooted.marked_k4, inventory.cycle)
    frontiers = ancestor_minimal_marks(rooted, marks)
    require(plan.frontiers == frontiers,
            "stored ancestor-minimal frontier changed")
    require(tuple(item.boundary_block for item in plan.opened) == frontiers,
            "stored opened frontier list changed")
    for item in plan.opened:
        boundary = block(inventory, item.boundary_block)
        cut = upstream_cut(inventory, rooted, item.boundary_block)
        vertices = boundary_open(inventory, inventory.graph.vertices,
                                 item.boundary_block, cut)
        descendants = tuple(index for index in marks
                            if index != item.boundary_block and
                            is_ancestor(rooted, ("B", item.boundary_block),
                                        ("B", index), strict=True))
        require(len(descendants) <= 1,
                "audited frontier has more than one descendant mark")
        descendant = descendants[0] if descendants else None
        residual_rank = residual_rank_after_cut(
            inventory, item.boundary_block, cut)
        descendant_rank = (0 if descendant is None else
                           block(inventory, descendant).rank)
        analysis = analyze_piece(inventory, vertices)
        require((item.boundary_kind, item.upstream_cut, item.vertices,
                 item.descendant_mark, item.residual_rank,
                 item.descendant_rank, item.rank) ==
                (boundary.kind, cut, vertices, descendant, residual_rank,
                 descendant_rank, analysis.rank),
                "stored opened territory metadata changed")
        require(item.rank == residual_rank + descendant_rank,
                "audited opened-side rank additivity changed")
    opened_sets = tuple(item.vertices for item in plan.opened)
    expected_anchor = frozenset(set(inventory.graph.vertices) -
                                set().union(*opened_sets))
    require(plan.anchor_vertices == expected_anchor,
            "stored anchor territory changed")
    final = final_piece_sets(plan)
    verify_partition(inventory, inventory.graph.vertices, final,
                     "final original-vertex partition")
    for cut in inventory.cuts:
        require(sum(cut in side for side in final) == 1,
                "physical articulation has nonunique final owner")

    analysis = analyze_piece(inventory, plan.anchor_vertices)
    require(analysis.rank == 3 and
            local_positive_edge_sets(analysis) ==
            frozenset({block(inventory, plan.anchor_block).edges}),
            "anchor is not intact-root-K4-only with bridge trees")
    for original in positive_ids(inventory):
        owners = tuple(side for side in final
                       if block(inventory, original).edges &
                       induced_edges(inventory.graph.edges, side))
        require(len(owners) == 1,
                "original positive block has zero or multiple final owners")
    return True


# ---------------------------------------------------------------------------
# Exact piece receipts and strict integer ledger.
# ---------------------------------------------------------------------------


def anchor_receipt(inventory, plan):
    analysis = analyze_piece(inventory, plan.anchor_vertices)
    require(analysis.rank == 3 and
            local_positive_edge_sets(analysis) ==
            frozenset({block(inventory, plan.anchor_block).edges}),
            "anchor is not literal-K4-only with bridge trees")
    return PieceReceipt("anchor", "strict-rooted-K4",
                        plan.anchor_vertices, 3, 2, True,
                        "R331K-K4-ROOTED-v1")


def open_receipt(inventory, item):
    analysis = analyze_piece(inventory, item.vertices)
    require(analysis.rank == item.residual_rank + item.descendant_rank,
            "opened receipt rank additivity changed")
    descendant_kind = (None if item.descendant_mark is None else
                       block(inventory, item.descendant_mark).kind)
    signature = (item.boundary_kind, descendant_kind, analysis.rank)
    if signature == ("cycle", None, 0):
        require(not analysis.positive_blocks and
                len(analysis.edges) == len(analysis.vertices) - 1,
                "leaf-cycle opened side is not a nonempty tree")
        category = "cycle-open-tree-debit"
        contract = "R331K-TREE-EXACT-v1"
        floor, strict = -1, False
    elif signature == ("K4", None, 1):
        require(len(analysis.positive_blocks) == 1 and
                analysis.positive_blocks[0].kind == "cycle" and
                analysis.positive_blocks[0].cycle_length == 3,
                "leaf-K4 opened side is not a triangular unicycle")
        category = "K4-open-triangle-positive"
        contract = "R331K-TRIANGLE-UNICYCLIC-v1"
        floor, strict = 0, True
    elif signature == ("K4", "cycle", 2):
        category = "K4-open-plus-cycle-rank2-positive"
        contract = "R331K-CONNECTED-RANK2-v1"
        floor, strict = 0, True
    elif signature == ("cycle", "K4", 3):
        category = "cycle-open-plus-K4-rank3-nonnegative"
        contract = "R331K-CONNECTED-RANK3-v1"
        floor, strict = 0, False
    else:
        raise VerifyError("opened side has impossible R331-K physical type")
    return PieceReceipt("frontier", category, item.vertices, analysis.rank,
                        floor, strict, contract, item.boundary_block,
                        item.boundary_kind, descendant_kind)


def derive_ledger(inventory, plan):
    audit_plan(inventory, plan)
    anchor = anchor_receipt(inventory, plan)
    opened = tuple(open_receipt(inventory, item) for item in plan.opened)
    receipts = (anchor, *opened)
    for receipt in receipts:
        require(receipt.contract in CONTRACTS,
                "receipt cites an unknown analytic contract")
        contract = CONTRACTS[receipt.contract]
        require(receipt.floor == contract.floor and
                (not receipt.strict or contract.strict),
                "receipt floor/strictness disagrees with pinned contract")
    tree_debits = sum(item.category == "cycle-open-tree-debit"
                      for item in opened)
    require(0 <= tree_debits <= 1 and tree_debits <= len(plan.frontiers) <= 2,
            "R331-K has an impossible number of tree debits")
    lower_integer = sum(item.floor for item in receipts)
    require(lower_integer == 2 - tree_debits and lower_integer >= 1,
            "strict R331-K ledger is not 2-t with t<=1")
    require(anchor.strict,
            "strict R331-K ledger lacks the rooted-K4 strict receipt")
    used = frozenset({
        "R331K-COMBINATORIAL-NOTE-v1",
        "R331K-RESIDUAL-SIEVE-v1",
        "R331K-INDUCED-SUPERADD-v1",
        *(item.contract for item in receipts),
    })
    require(used <= EXPECTED_CONTRACT_IDS,
            "ledger cites a contract outside the immutable manifest")
    ledger = Ledger(PROFILE, plan.anchor_block, plan.mark_relation,
                    len(plan.frontiers), tree_debits, anchor.floor,
                    lower_integer, True, receipts, tuple(sorted(used)))
    audit_ledger(inventory, plan, ledger)
    return ledger


def audit_ledger(inventory, plan, ledger):
    anchor = anchor_receipt(inventory, plan)
    opened = tuple(open_receipt(inventory, item) for item in plan.opened)
    receipts = (anchor, *opened)
    tree_debits = sum(item.category == "cycle-open-tree-debit"
                      for item in opened)
    lower_integer = sum(item.floor for item in receipts)
    require(ledger.receipts == receipts,
            "independent receipt replay disagrees")
    require((ledger.profile, ledger.anchor_block, ledger.mark_relation,
             ledger.frontier_count, ledger.tree_debits,
             ledger.anchor_floor, ledger.lower_integer, ledger.strict) ==
            (PROFILE, plan.anchor_block, plan.mark_relation,
             len(plan.frontiers), tree_debits, anchor.floor,
             lower_integer, True),
            "independent strict integer ledger replay disagrees")
    require(lower_integer == 2 - tree_debits and
            tree_debits <= 1 and anchor.strict,
            "replayed ledger does not prove the strict integer bound")
    fresh_contracts = frozenset({
        "R331K-COMBINATORIAL-NOTE-v1",
        "R331K-RESIDUAL-SIEVE-v1",
        "R331K-INDUCED-SUPERADD-v1",
        *(item.contract for item in receipts),
    })
    require(ledger.contracts == tuple(sorted(fresh_contracts)),
            "replayed graph-specific contract set disagrees")
    return True


def certificate_signature(plan, ledger):
    return (plan.mark_relation,
            tuple(sorted((item.boundary_kind,
                          None if item.descendant_mark is None else
                          item.descendant_rank,
                          item.rank)
                         for item in plan.opened)),
            ledger.tree_debits, ledger.lower_integer,
            tuple(sorted((item.category, item.rank, item.floor)
                         for item in ledger.receipts)))


def verify(vertices: frozenset, edges: frozenset):
    """Production adjacency-only R331-K gate; replay both unlabeled K4 roots."""
    audit_sources()
    inventory = reconstruct(vertices, edges)
    candidates = []
    failures = []
    for anchor in inventory.k4s:
        try:
            plan = construct_plan(inventory, anchor)
            ledger = derive_ledger(inventory, plan)
            candidates.append((plan, ledger))
        except VerifyError as error:
            failures.append(str(error))
    require(len(candidates) == 2,
            "not every adjacency-derived literal K4 passed as an anchor: " +
            " | ".join(failures))
    return inventory, tuple(candidates)


# ---------------------------------------------------------------------------
# Independent adjacency fixture construction and finite corroboration.
# ---------------------------------------------------------------------------


def add_clique(edges, vertices):
    edges.update(edge(left, right)
                 for left, right in itertools.combinations(vertices, 2))


def add_cycle(edges, vertices):
    require(len(vertices) >= 3 and len(set(vertices)) == len(vertices),
            "generated cycle is malformed")
    edges.update(edge(vertices[index], vertices[(index + 1) % len(vertices)])
                 for index in range(len(vertices)))


class Builder:
    def __init__(self):
        self.vertices = set()
        self.edges = set()
        self.serial = 0
        self.positive = []
        self.routing = []

    def fresh(self, prefix):
        vertex = (prefix, self.serial)
        self.serial += 1
        self.vertices.add(vertex)
        return vertex

    def k4(self, port=None):
        vertices = ([port] if port is not None else [])
        vertices += [self.fresh("K") for _ in range(4 - len(vertices))]
        self.vertices.update(vertices)
        add_clique(self.edges, vertices)
        result = tuple(vertices)
        self.positive.append(("K4", result))
        return result

    def cycle(self, length, port=None):
        require(type(length) is int and length >= 3,
                "generated cycle length below three")
        vertices = ([port] if port is not None else [])
        vertices += [self.fresh(f"C{length}")
                     for _ in range(length - len(vertices))]
        self.vertices.update(vertices)
        add_cycle(self.edges, vertices)
        result = tuple(vertices)
        self.positive.append(("cycle", result))
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
        require(type(count) is int and count >= 0,
                "generated payload size is invalid")
        made = []
        for index in range(count):
            if index == 0 or index % 5 == 0:
                parent = root
            elif index % 3 == 0:
                parent = made[max(0, index // 3 - 1)]
            else:
                parent = made[index - 1]
            vertex = self.fresh("P")
            self.edges.add(edge(parent, vertex))
            made.append(vertex)
        return tuple(made)

    def graph(self):
        return frozenset(self.vertices), frozenset(self.edges)


def attach_k4(builder, root, route_length):
    current = builder.k4()
    builder.bridge_path(root, current[0], route_length)
    return current


def attach_cycle(builder, root, length, route_length):
    current = builder.cycle(length)
    builder.bridge_path(root, current[0], route_length)
    return current


def fixture(topology, route_length=3, payload_depth=0, cycle_length=5):
    require(type(route_length) is int and route_length >= 1 and
            type(payload_depth) is int and payload_depth >= 0 and
            type(cycle_length) is int and cycle_length >= 3 and
            cycle_length % 2 == 1,
            "bad R331-K fixture parameter")
    builder = Builder()
    anchor = builder.k4()

    if topology == "same-cut-siblings":
        marked = builder.k4(anchor[0])
        cycle = builder.cycle(cycle_length, anchor[0])

    elif topology == "separate-direct-arms":
        marked = builder.k4(anchor[0])
        cycle = builder.cycle(cycle_length, anchor[1])

    elif topology == "separate-bridge-arms":
        marked = attach_k4(builder, anchor[0], route_length)
        cycle = attach_cycle(builder, anchor[1], cycle_length,
                             route_length + 1)

    elif topology == "shared-bridge-stem":
        hub = builder.fresh("HUB")
        builder.bridge_path(anchor[0], hub, route_length)
        marked = builder.k4(hub)
        cycle = builder.cycle(cycle_length, hub)

    elif topology == "K4-before-cycle":
        marked = builder.k4(anchor[0])
        cycle = builder.cycle(cycle_length, marked[1])

    elif topology == "K4-before-cycle-bridge":
        marked = attach_k4(builder, anchor[0], route_length)
        cycle = attach_cycle(builder, marked[1], cycle_length,
                             route_length + 2)

    elif topology == "cycle-before-K4":
        cycle = builder.cycle(cycle_length, anchor[0])
        marked = builder.k4(cycle[1])

    elif topology == "cycle-before-K4-bridge":
        cycle = attach_cycle(builder, anchor[0], cycle_length,
                             route_length)
        marked = attach_k4(builder, cycle[max(1, cycle_length // 2)],
                           route_length + 2)

    elif topology == "K4-upstream-cut-sibling":
        marked = builder.k4(anchor[0])
        cycle = builder.cycle(cycle_length, anchor[0])

    elif topology == "cycle-upstream-cut-sibling":
        cycle = builder.cycle(cycle_length, anchor[0])
        marked = builder.k4(anchor[0])

    else:
        raise VerifyError("unknown generated R331-K topology")

    if payload_depth:
        builder.tree_payload(anchor[3], payload_depth)
        builder.tree_payload(marked[-1], max(1, payload_depth // 2))
        builder.tree_payload(cycle[-1], max(1, payload_depth // 3))
        for index, current in enumerate(tuple(builder.routing)[:8]):
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
                      for current in edges
                      for left, right in (tuple(current),)))


def verify_signatures(candidates):
    return tuple(sorted(certificate_signature(plan, ledger)
                        for plan, ledger in candidates))


def semantic_signature(candidates):
    return verify_signatures(candidates)


@dataclass(frozen=True)
class AuditResult:
    generated: int
    relabeled: int
    topologies: tuple[tuple[str, int], ...]
    relations: tuple[tuple[str, int], ...]
    categories: tuple[tuple[str, int], ...]
    expansion_cases: int
    long_connector_edges: int
    hostile_rejections: tuple[str, ...]
    rewires_distinguished: int
    source_files: int
    api_parameters: tuple[str, str]
    no_assert_statements: int


def expansion_audit():
    signatures = set()
    for length, payload in ((1, 0), (2, 4), (11, 9), (53, 17)):
        _, candidates = verify(*fixture(
            "K4-before-cycle-bridge", route_length=length,
            payload_depth=payload, cycle_length=7))
        signatures.add(semantic_signature(candidates))
    require(len(signatures) == 1,
            "K2/tree expansion changed the semantic R331-K certificate")

    long_edges = 1601
    _, candidates = verify(*fixture(
        "shared-bridge-stem", route_length=long_edges,
        payload_depth=0, cycle_length=3))
    require(len(candidates) == 2 and
            all(ledger.lower_integer >= 1
                for _, ledger in candidates),
            "very-long K2 connector failed iterative verification")
    return 5, long_edges


def api_shape_audit():
    signature = inspect.signature(verify)
    parameters = tuple(signature.parameters.values())
    require(tuple(item.name for item in parameters) == ("vertices", "edges") and
            all(item.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD and
                item.default is inspect.Parameter.empty
                for item in parameters),
            "production API is not exactly verify(vertices, edges)")
    annotations = inspect.get_annotations(verify, eval_str=True)
    require(annotations == {"vertices": frozenset, "edges": frozenset},
            "production API lost its frozenset-only annotations")
    return tuple(item.name for item in parameters)


def no_assert_audit():
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    statements = tuple(node for node in ast.walk(tree)
                       if isinstance(node, ast.Assert))
    require(not statements,
            "assert statement found; optimized mode would remove a safety check")
    return len(statements)


def graph_with_inventory(kind):
    builder = Builder()
    root = builder.k4()
    builder.k4(root[0])
    if kind == "even-cycle":
        builder.cycle(4, root[1])
    elif kind == "third-K4":
        builder.k4(root[1])
    elif kind == "two-cycles":
        builder.cycle(3, root[1])
        builder.cycle(3, root[2])
    else:
        raise VerifyError("unknown hostile inventory")
    return builder.graph()


def hostile_tests():
    rejected = []
    base_vertices, base_edges = fixture(
        "same-cut-siblings", payload_depth=7, cycle_length=5)
    inventory, candidates = verify(base_vertices, base_edges)
    base_plan, base_ledger = candidates[0]
    k4 = block(inventory, inventory.k4s[0])
    cycle = block(inventory, inventory.cycle)

    kedge = next(iter(k4.edges))
    left, right = tuple(kedge)
    new = ("hostile", "subdivide-k4")
    rejected.append(expect_rejection(
        lambda: verify(frozenset(set(base_vertices) | {new}),
                       frozenset((set(base_edges) - {kedge}) |
                                 {edge(left, new), edge(new, right)})),
        "subdivided literal K4", "unsupported positive-rank block type"))

    chord = next(edge(left, right)
                 for left, right in itertools.combinations(cycle.vertices, 2)
                 if edge(left, right) not in cycle.edges)
    rejected.append(expect_rejection(
        lambda: verify(base_vertices,
                       frozenset(set(base_edges) | {chord})),
        "cycle chord", "input graph does not have cyclomatic rank seven"))

    cycle_edge = next(iter(cycle.edges))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices,
                       frozenset(set(base_edges) - {cycle_edge})),
        "cycle edge deletion", "input graph does not have cyclomatic rank seven"))

    private_left = next(iter(block(inventory, inventory.k4s[0]).vertices -
                             block(inventory, inventory.k4s[1]).vertices))
    private_right = next(iter(block(inventory, inventory.k4s[1]).vertices -
                              block(inventory, inventory.k4s[0]).vertices))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices,
                       frozenset(set(base_edges) |
                                 {edge(private_left, private_right)})),
        "cross-block ear merger", "input graph does not have cyclomatic rank seven"))

    payload_edge = next(current for current in base_edges
                        if any(isinstance(vertex, tuple) and
                               vertex[0] == "P" for vertex in current))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices,
                       frozenset(set(base_edges) - {payload_edge})),
        "omitted rooted payload edge", "input graph disconnected"))
    rejected.append(expect_rejection(
        lambda: verify(set(base_vertices), base_edges),
        "mutable vertex-set API injection",
        "vertices must be a nonempty frozenset"))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices,
                       frozenset(set(base_edges) |
                                 {frozenset({private_left})})),
        "malformed loop edge", "malformed unordered edge"))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices,
                       frozenset(set(base_edges) |
                                 {frozenset({private_left, ("outside", 1)})})),
        "foreign endpoint", "edge endpoint outside vertex set"))

    rejected.append(expect_rejection(
        lambda: verify(*graph_with_inventory("even-cycle")),
        "even cycle outside residual", "literal cycle is not odd"))
    rejected.append(expect_rejection(
        lambda: verify(*graph_with_inventory("third-K4")),
        "third K4", "input graph does not have cyclomatic rank seven"))
    rejected.append(expect_rejection(
        lambda: verify(*graph_with_inventory("two-cycles")),
        "two cycles", "input graph does not have cyclomatic rank seven"))

    contract_id = "R331K-CONNECTED-RANK2-v1"
    original = CONTRACTS[contract_id]
    for label, replacement in (
            ("analytic floor-table mutation", replace(original, floor=99)),
            ("analytic source-path mutation",
             replace(original, source="all-tricyclic-graphs/paper.tex")),
            ("analytic source-digest mutation",
             replace(original, sha256="0" * 64))):
        CONTRACTS[contract_id] = replacement
        try:
            rejected.append(expect_rejection(
                lambda: verify(base_vertices, base_edges), label,
                "analytic contract tuple/lookup disagree"))
        finally:
            CONTRACTS[contract_id] = original

    for source_contract_id, hostile_label in (
            ("R331K-COMBINATORIAL-NOTE-v1", "combinatorial note source-byte mutation"),
            ("R331K-RESIDUAL-SIEVE-v1", "analytic ledger source-byte mutation")):
        source_contract = CONTRACTS[source_contract_id]
        blob = (SOURCE_ROOT / source_contract.source).read_bytes()
        rejected.append(expect_rejection(
            lambda blob=blob, source_contract=source_contract:
                authenticate_source_blob(blob + b"\nHOSTILE",
                                         source_contract.sha256,
                                         "synthetic source mutation"),
            hostile_label, "analytic source changed"))

    source_root_original = globals()["SOURCE_ROOT"]
    globals()["SOURCE_ROOT"] = source_root_original / "absent-r331k-sources"
    try:
        rejected.append(expect_rejection(
            lambda: verify(base_vertices, base_edges),
            "public API missing source root",
            "analytic source authentication failed: repository absent"))
    finally:
        globals()["SOURCE_ROOT"] = source_root_original

    specs_original = globals()["CONTRACT_SPECS"]
    lookup_original = globals()["CONTRACTS"]
    unused_id = "R331K-CONNECTED-RANK2-v1"
    unused_original = dict(specs_original)[unused_id]

    def rebound_specs(replacement):
        return tuple((name, replacement if name == unused_id else item)
                     for name, item in specs_original)

    for label, replacement, expected in (
            ("simultaneous unused-floor rebind",
             replace(unused_original, floor=99),
             "analytic full contract manifest changed"),
            ("simultaneous unused-claim rebind",
             replace(unused_original, claim="HOSTILE altered claim"),
             "analytic full contract manifest changed"),
            ("simultaneous unused-strict rebind",
             replace(unused_original, strict=False),
             "analytic full contract manifest changed"),
            ("simultaneous boolean-floor rebind",
             replace(unused_original, floor=True),
             "contract floor malformed")):
        mutated = rebound_specs(replacement)
        globals()["CONTRACT_SPECS"] = mutated
        globals()["CONTRACTS"] = dict(mutated)
        try:
            rejected.append(expect_rejection(
                lambda: verify(base_vertices, base_edges), label, expected))
        finally:
            globals()["CONTRACT_SPECS"] = specs_original
            globals()["CONTRACTS"] = lookup_original

    mirror_contracts = (
        ("R331K-COMBINATORIAL-NOTE-v1", "combinatorial proof note"),
        ("R331K-RESIDUAL-SIEVE-v1", "residual ledger"),
    )
    with tempfile.TemporaryDirectory(prefix="r331k-source-mirror-") as temporary:
        mirror = Path(temporary)
        for source, _ in EXPECTED_SOURCE_ROWS:
            target = mirror / source
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE_ROOT / source, target)
        for contract_id, label in mirror_contracts:
            contract = CONTRACTS[contract_id]
            source_path = mirror / contract.source
            original_blob = source_path.read_bytes()
            source_path.unlink()
            globals()["SOURCE_ROOT"] = mirror
            try:
                rejected.append(expect_rejection(
                    lambda: verify(base_vertices, base_edges),
                    f"public API missing {label}",
                    f"analytic source authentication failed: missing {contract_id}"))
            finally:
                globals()["SOURCE_ROOT"] = source_root_original
            source_path.write_bytes(original_blob + b"\nHOSTILE SOURCE MUTATION\n")
            globals()["SOURCE_ROOT"] = mirror
            try:
                rejected.append(expect_rejection(
                    lambda: verify(base_vertices, base_edges),
                    f"public API mutated {label}",
                    f"analytic source changed: {contract_id}"))
            finally:
                globals()["SOURCE_ROOT"] = source_root_original
            source_path.write_bytes(original_blob)

    original_reconstruct = globals()["reconstruct"]

    def unrelated_crash(*_args, **_kwargs):
        raise KeyError("unrelated crash")

    globals()["reconstruct"] = unrelated_crash
    try:
        try:
            expect_rejection(lambda: verify(base_vertices, base_edges),
                             "unrelated implementation crash",
                             "unrelated crash")
        except KeyError as error:
            require(str(error) == "'unrelated crash'",
                    "unrelated implementation exception changed")
        else:
            raise VerifyError("hostile harness masked an unrelated KeyError")
    finally:
        globals()["reconstruct"] = original_reconstruct

    rejected.append(expect_rejection(
        lambda: audit_plan(inventory, replace(base_plan, frontiers=())),
        "forged frontier set", "stored ancestor-minimal frontier changed"))
    rejected.append(expect_rejection(
        lambda: audit_ledger(inventory, base_plan,
                             replace(base_ledger, lower_integer=99)),
        "forged ledger integer",
        "independent strict integer ledger replay disagrees"))

    _, direct_candidates = verify(*fixture("same-cut-siblings"))
    _, bridge_candidates = verify(*fixture(
        "separate-bridge-arms", route_length=8))
    require(semantic_signature(direct_candidates) !=
            semantic_signature(bridge_candidates),
            "same-inventory direct/bridge rewire was not distinguished")
    return tuple(rejected), 1


def audit():
    source_files = audit_sources()
    api_parameters = api_shape_audit()
    no_assert_statements = no_assert_audit()
    cases = (
        ("same-cut-siblings", 3, 0, 3),
        ("separate-direct-arms", 3, 4, 5),
        ("separate-bridge-arms", 11, 9, 7),
        ("shared-bridge-stem", 9, 8, 9),
        ("K4-before-cycle", 3, 5, 3),
        ("K4-before-cycle-bridge", 13, 7, 5),
        ("cycle-before-K4", 3, 6, 7),
        ("cycle-before-K4-bridge", 8, 6, 9),
        ("K4-upstream-cut-sibling", 3, 3, 5),
        ("cycle-upstream-cut-sibling", 3, 3, 7),
    )
    topologies = Counter()
    relations = Counter()
    categories = Counter()
    generated = relabeled = 0
    for index, (topology, length, payload, cycle_length) in enumerate(cases):
        graph = fixture(topology, length, payload, cycle_length)
        inventory, candidates = verify(*graph)
        require(tuple(sorted(block(inventory, current).rank
                             for current in positive_ids(inventory))) ==
                (1, 3, 3),
                "generated R331-K block-rank inventory changed")
        require(len(candidates) == 2,
                "generated graph did not replay both K4 anchors")
        for plan, ledger in candidates:
            require(ledger.lower_integer == 2 - ledger.tree_debits and
                    ledger.tree_debits <= 1 and ledger.strict,
                    "generated R331-K strict ledger changed")
            relations[plan.mark_relation] += 1
            categories.update(item.category for item in ledger.receipts)
        topologies[topology] += 1
        generated += 1
        relabeled_graph = opaque_relabel(*graph, salt=31 + 17 * index)
        _, relabeled_candidates = verify(*relabeled_graph)
        require(semantic_signature(candidates) ==
                semantic_signature(relabeled_candidates),
                "opaque relabeling changed the R331-K semantic certificates")
        relabeled += 1

    require({"same-cut-siblings", "separate-direct-arms",
             "separate-bridge-arms", "shared-bridge-stem",
             "K4-before-cycle", "K4-before-cycle-bridge",
             "cycle-before-K4", "cycle-before-K4-bridge",
             "K4-upstream-cut-sibling", "cycle-upstream-cut-sibling"} <=
            set(topologies),
            "hostile R331-K topology coverage incomplete")
    require({"incomparable", "K4-before-cycle", "cycle-before-K4"} <=
            set(relations),
            "R331-K mark-relation coverage incomplete")
    require({"strict-rooted-K4", "cycle-open-tree-debit",
             "K4-open-triangle-positive",
             "K4-open-plus-cycle-rank2-positive",
             "cycle-open-plus-K4-rank3-nonnegative"} <= set(categories),
            "R331-K piece-category coverage incomplete")
    expansion_cases, long_connector = expansion_audit()
    rejected, rewires = hostile_tests()
    return AuditResult(
        generated, relabeled, tuple(sorted(topologies.items())),
        tuple(sorted(relations.items())), tuple(sorted(categories.items())),
        expansion_cases, long_connector, rejected, rewires,
        source_files, api_parameters, no_assert_statements)


def report(result):
    return "\n".join((
        "R331-K adjacency semantic gate: finite corroboration passed",
        "scope: exactly two literal K4 blocks plus one odd literal cycle; no global, other-packet, or single-block claim",
        "proof boundary: source-pinned analytic inputs plus a finite adjacency gate; no claim that finite fixtures prove a spectral theorem",
        "API: verify(vertices:frozenset, edges:frozenset); no supplied anchor, profile, block, route, owner, rank, charge, threshold, or partition",
        "reconstruction: iterative Tarjan; every physical K2 retained; exact K4+K4+cycle inventory; total rank 7; full block-cut tree",
        "anchors: both adjacency-derived literal K4 choices replayed; no semantic use of labels or Tarjan indices",
        "ownership: ancestor-minimal marked frontier; every final piece original-vertex, induced, connected, disjoint, exhaustive; every cut has one owner",
        "rank lemma: beta(open X)=beta(X-c)+sum beta(intact descendant marks); bridge descendants contribute zero; anchor has unique positive block B",
        "ledger: rooted literal K4 >2; only a leaf-cycle opening is a tree debit; sigma(G)>2-t with t<=1",
        f"analytic source files pinned: {result.source_files}; source manifest sha256: {source_manifest_digest()}",
        f"authenticated contract records: {len(EXPECTED_CONTRACT_IDS)}; full manifest sha256: {full_contract_manifest_digest()}",
        f"generated topology fixtures: {result.generated}; opaque relabel replays: {result.relabeled}",
        "topologies: " + repr(dict(result.topologies)),
        "mark relations across both anchors: " + repr(dict(result.relations)),
        "piece categories: " + repr(dict(result.categories)),
        f"K2/tree expansion probes: {result.expansion_cases}; longest connector: {result.long_connector_edges} physical edges",
        f"hostile mutations rejected: {len(result.hostile_rejections)}; same-inventory rewires distinguished: {result.rewires_distinguished}",
        "production API parameters: " + repr(result.api_parameters),
        f"assert statements in verifier AST: {result.no_assert_statements}",
        "analytic contracts: " + repr(tuple(sorted(EXPECTED_CONTRACT_IDS))),
        "verifier sha256: " + file_digest(Path(__file__)),
        "status: R331-K combinatorial gate and independent semantic replay passed; spectral conclusions remain source-conditional",
    ))


def main():
    if sys.argv != [sys.argv[0]]:
        print("R331-K verifier: command line arguments are not accepted",
              file=sys.stderr)
        return 2
    print(report(audit()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
