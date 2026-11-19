#!/usr/bin/env python3
"""Adjacency-only semantic verifier/corroborator for the physical R322 lane.

The production API is exactly ``verify(vertices, edges)``.  Its only input is a
finite simple graph represented by a nonempty frozenset of original vertices
and a frozenset of unordered two-vertex frozenset edges.  No packet label,
block list, route, owner, rank, charge, threshold, or partition is accepted.

The verifier reconstructs physical edge blocks with iterative Tarjan (including
every bridge as a K2 block), authenticates literal K4+D+D and total cyclomatic
rank seven, rebuilds the full block-cut tree, performs the simultaneous
first-K2 split, opens only the ancestor-minimal retained-diamond frontier, and
replays an original-vertex induced connected disjoint exhaustive partition.
Its ledger is the strict bound ``sigma(G) > 2-t >= 0``.

This program is a fail-closed implementation gate and finite corroboration.  It
is not the universal proof and makes no claim about another packet, a
single-block graph, or the global rank-seven problem.  The universal proof is
the separately pinned companion note.
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
PROFILE = "literal-K4+D+D"


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
    ("R322-PACKET-PROOF-v1", Contract(
        "positive-square-energy/heptacyclic-general/r322-complete-physical-closure.md",
        "6a546aecc3e879854a6d178a8a845a9b696bf35528be192283dbf2132d2b2908",
        "reviewed universal proof of the complete physical literal-K4+D+D packet",
        None, False)),
    ("R322-RESIDUAL-SIEVE-v1", Contract(
        "positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md",
        "3f8bb3a397125782dd6c9cae26ce52f9c6bf826e3136dfee62781048e65c18a5",
        "rank-seven debit rule reduces the 3+2+2 row to the exact theta excess predicate",
        None, False)),
    ("R322-THETA-CLASSIFICATION-v1", Contract(
        "positive-square-energy/tricyclic-general/theta-cycle-dnn-reduction.md",
        "b1e40ec3f9f4ba5ecaf1de44284c9fba63d65fc3da59023d05eab488087e7c71",
        "theta excess is uniquely maximal at the literal diamond and every other theta excess above one is below four thirds",
        None, False)),
    ("R322-INDUCED-SUPERADD-v1", Contract(
        "all-tricyclic-graphs/paper.tex",
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
        "positive-square-energy induced superadditivity on vertex partitions",
        None, False)),
    ("R322-TREE-EXACT-v1", Contract(
        "all-tricyclic-graphs/paper.tex",
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
        "every nonempty tree T has sigma(T)=-1",
        -1, False)),
    ("R322-CONNECTED-RANK2-v1", Contract(
        "all-bicyclic-graphs/paper.tex",
        "56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da",
        "every connected rank-two graph has sigma>0",
        0, True)),
    ("R322-CONNECTED-RANK3-v1", Contract(
        "all-tricyclic-graphs/paper.tex",
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
        "every connected rank-three graph has sigma>=0",
        0, False)),
    ("R322-CONNECTED-RANK4-v1", Contract(
        "all-tetracyclic-graphs/paper.tex",
        "70a931c28c8a8817e2c02818200885f73c532d9afe2c065831f2b3884d61160f",
        "every connected rank-four graph has sigma>=0",
        0, False)),
    ("R322-TRIANGLE-UNICYCLIC-v1", Contract(
        "packing-two-square-energy/paper.tex",
        "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
        "a connected graph whose unique positive block is a literal triangle has sigma>0",
        0, True)),
    ("R322-K4-ROOTED-v1", Contract(
        "packing-two-square-energy/paper.tex",
        "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
        "a connected graph whose unique positive block is a literal K4 has sigma>2",
        2, True)),
)

CONTRACTS = dict(CONTRACT_SPECS)

# These values are independent canonical anchors, not values derived from the
# mutable runtime tuple or lookup.  A simultaneous hostile rebind of both views
# therefore still fails the full-record digest check.
EXPECTED_CONTRACT_IDS = frozenset({
    "R322-PACKET-PROOF-v1",
    "R322-RESIDUAL-SIEVE-v1",
    "R322-THETA-CLASSIFICATION-v1",
    "R322-INDUCED-SUPERADD-v1",
    "R322-TREE-EXACT-v1",
    "R322-CONNECTED-RANK2-v1",
    "R322-CONNECTED-RANK3-v1",
    "R322-CONNECTED-RANK4-v1",
    "R322-TRIANGLE-UNICYCLIC-v1",
    "R322-K4-ROOTED-v1",
})
EXPECTED_SOURCE_ROWS = frozenset({
    ("positive-square-energy/heptacyclic-general/r322-complete-physical-closure.md",
     "6a546aecc3e879854a6d178a8a845a9b696bf35528be192283dbf2132d2b2908"),
    ("positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md",
     "3f8bb3a397125782dd6c9cae26ce52f9c6bf826e3136dfee62781048e65c18a5"),
    ("positive-square-energy/tricyclic-general/theta-cycle-dnn-reduction.md",
     "b1e40ec3f9f4ba5ecaf1de44284c9fba63d65fc3da59023d05eab488087e7c71"),
    ("all-tricyclic-graphs/paper.tex",
     "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02"),
    ("all-bicyclic-graphs/paper.tex",
     "56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da"),
    ("all-tetracyclic-graphs/paper.tex",
     "70a931c28c8a8817e2c02818200885f73c532d9afe2c065831f2b3884d61160f"),
    ("packing-two-square-energy/paper.tex",
     "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791"),
})
EXPECTED_FULL_CONTRACT_MANIFEST_SHA256 = (
    "1976483ed5f4cd69a40fb8b01ec97885b441f1425ee04977ad205c63d039b126")
EXPECTED_SOURCE_MANIFEST_SHA256 = (
    "e9100edd1e98f68b124e2c619df966e4742d11c3cca3f03ce3300586bff1b0dc")


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
    payload = {"schema": "r322-contract-manifest-v1", "records": records}
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
    k4: int
    diamonds: tuple[int, int]
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
    if (len(vertices) == 4 and len(edges) == 5 and
            sorted(degrees.values()) == [2, 2, 3, 3]):
        require(rank == 2, "literal diamond rank changed")
        return Block(index, edges, vertices, rank, "diamond", None)
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
    require(set(parent) == set(tree),
            "block-cut topology disconnected")
    return parent, depth, tuple(order)


def reconstruct(vertices, edges):
    graph = normalize_graph(vertices, edges)
    require(connected(graph.vertices, graph.edges),
            "input graph disconnected")
    require(graph_rank(graph.vertices, graph.edges) == 7,
            "input graph does not have cyclomatic rank seven")

    raw_blocks = biconnected_edge_blocks(graph.vertices, graph.edges)
    blocks = tuple(classify_block(index, current)
                   for index, current in enumerate(raw_blocks))
    positive = tuple(current for current in blocks if current.rank)
    k4s = tuple(current.index for current in positive
                if current.kind == "K4")
    diamonds = tuple(current.index for current in positive
                     if current.kind == "diamond")
    require(len(k4s) == 1 and len(diamonds) == 2 and
            len(positive) == 3,
            "positive blocks are not exactly one literal K4 and two literal diamonds")
    require(tuple(sorted(current.rank for current in positive)) == (2, 2, 3),
            "positive block ranks are not exactly 3+2+2")
    require(sum(current.rank for current in positive) == 7,
            "positive block ranks do not sum to seven")

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
    parent, depth, order = rooted_tree(tree, ("B", k4s[0]))
    bridges = tuple(current.index for current in blocks
                    if current.kind == "bridge")
    return Inventory(graph, adjacency(graph.vertices, graph.edges), blocks,
                     cuts, tree, k4s[0], diamonds, bridges,
                     parent, depth, order)


def block(inventory, index):
    require(type(index) is int and 0 <= index < len(inventory.blocks),
            "block index outside inventory")
    return inventory.blocks[index]


def positive_ids(inventory):
    return (inventory.k4, *inventory.diamonds)


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
    if ancestor not in inventory.depth or descendant not in inventory.depth:
        return False
    if strict and ancestor == descendant:
        return False
    current = descendant
    while (current is not None and
           inventory.depth[current] >= inventory.depth[ancestor]):
        if current == ancestor:
            return True
        current = inventory.parent[current]
    return False


def upstream_cut(inventory, block_index):
    node = ("B", block_index)
    require(node != ("B", inventory.k4),
            "literal K4 root has no upstream cut")
    parent = inventory.parent[node]
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


def intact_positive_ids(inventory, vertices):
    edges = induced_edges(inventory.graph.edges, vertices)
    return tuple(index for index in positive_ids(inventory)
                 if block(inventory, index).edges <= edges)


# ---------------------------------------------------------------------------
# First-K2 antichain, ancestor-minimal diamond frontier, and ownership.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BridgeSide:
    bridge_block: int
    deleted_edge: frozenset
    vertices: frozenset
    diamond_count: int
    rank: int


@dataclass(frozen=True)
class OpenSide:
    boundary_block: int
    upstream_cut: object
    vertices: frozenset
    delta: int
    eta: int
    rank: int


@dataclass(frozen=True)
class PartitionPlan:
    profile: str
    phase1: tuple[BridgeSide, ...]
    root_vertices: frozenset
    retained_diamonds: tuple[int, ...]
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
    delta: int | None = None
    eta: int | None = None


@dataclass(frozen=True)
class Ledger:
    profile: str
    branch: str
    frontier_count: int
    tree_debits: int
    anchor_floor: int
    lower_integer: int
    strict: bool
    receipts: tuple[PieceReceipt, ...]
    contracts: tuple[str, ...]


def first_diamond_bridges(inventory):
    chosen = set()
    for diamond in inventory.diamonds:
        route = path_from_root(inventory, ("B", diamond))
        bridge_nodes = tuple(node for node in route
                             if node[0] == "B" and
                             block(inventory, node[1]).kind == "bridge")
        if bridge_nodes:
            chosen.add(bridge_nodes[0][1])
    result = tuple(sorted(chosen))
    nodes = tuple(("B", index) for index in result)
    for left, right in itertools.permutations(nodes, 2):
        require(not is_ancestor(inventory, left, right, strict=True),
                "deduplicated first physical bridges are not an antichain")
    return result


def bridge_away_component(inventory, bridge_index):
    current = block(inventory, bridge_index)
    require(current.kind == "bridge" and len(current.edges) == 1,
            "away split requested on a non-K2 block")
    physical_edge = next(iter(current.edges))
    remaining = frozenset(inventory.graph.edges - {physical_edge})
    sides = components(inventory.graph.vertices, remaining)
    require(len(sides) == 2,
            "Tarjan K2 block did not split physical adjacency")
    k4_vertices = block(inventory, inventory.k4).vertices
    roots = tuple(side for side in sides if k4_vertices <= side)
    require(len(roots) == 1,
            "physical K2 orientation from the K4 is ambiguous")
    away = tuple(side for side in sides if side != roots[0])
    require(len(away) == 1, "physical K2 has no unique away component")
    return away[0]


def ancestor_minimal(inventory, candidates):
    candidates = tuple(candidates)
    candidate_set = set(candidates)
    selected = []
    for index in candidates:
        route = path_from_root(inventory, ("B", index))
        if not any(node[0] == "B" and node[1] in candidate_set
                   for node in route[:-1]):
            selected.append(index)
    result = tuple(sorted(selected))
    nodes = tuple(("B", index) for index in result)
    for left, right in itertools.permutations(nodes, 2):
        require(not is_ancestor(inventory, left, right, strict=True),
                "ancestor-minimal diamond frontier is not an antichain")
    return result


def boundary_open(inventory, current_vertices, boundary_index, cut):
    """Return the induced original-vertex owner X-c and all descendants."""
    boundary = block(inventory, boundary_index)
    require(boundary.kind == "diamond",
            "R322 boundary opening requires a literal diamond")
    require(boundary.vertices <= current_vertices,
            "boundary diamond is not intact in root territory")
    require(cut in boundary.vertices,
            "upstream cut lies outside boundary diamond")
    current_edges = induced_edges(inventory.graph.edges, current_vertices)
    require(boundary.edges <= current_edges,
            "boundary diamond edges are missing from root territory")
    owner_components = components(
        current_vertices, frozenset(current_edges - boundary.edges))
    by_vertex = {}
    for side in owner_components:
        hits = side & boundary.vertices
        require(len(hits) == 1,
                "outside component meets maximal diamond at multiple vertices")
        owner = next(iter(hits))
        require(owner not in by_vertex,
                "diamond vertex has duplicate outside owner component")
        by_vertex[owner] = side
    require(set(by_vertex) == set(boundary.vertices),
            "diamond boundary decomposition omitted a vertex")
    result = frozenset().union(
        *(by_vertex[vertex] for vertex in boundary.vertices
          if vertex != cut))
    require(result and cut not in result,
            "opened diamond side is empty or copied its upstream cut")
    require(boundary.vertices - {cut} <= result,
            "opened diamond side omitted X-c")
    require(connected(result, induced_edges(inventory.graph.edges, result)),
            "opened diamond side is disconnected")
    return result


def diamond_internal_degree(inventory, diamond_index, vertex):
    current = block(inventory, diamond_index)
    require(current.kind == "diamond" and vertex in current.vertices,
            "diamond degree requested outside literal diamond")
    return sum(vertex in physical_edge for physical_edge in current.edges)


def entry_delta(inventory, diamond_index, cut):
    degree = diamond_internal_degree(inventory, diamond_index, cut)
    require(degree in (2, 3),
            "literal diamond entry has impossible internal degree")
    return 0 if degree == 3 else 1


def descendant_diamond_count(inventory, frontier, retained_diamonds):
    count = sum(index != frontier and
                is_ancestor(inventory, ("B", frontier), ("B", index),
                            strict=True)
                for index in retained_diamonds)
    require(count in (0, 1),
            "R322 frontier has impossible descendant diamond count")
    return count


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


def construct_plan(inventory):
    first = first_diamond_bridges(inventory)
    preliminary = tuple((index,
                         next(iter(block(inventory, index).edges)),
                         bridge_away_component(inventory, index))
                        for index in first)
    away_sets = tuple(row[2] for row in preliminary)
    removed_edges = frozenset(row[1] for row in preliminary)
    require(len(removed_edges) == len(preliminary),
            "first-K2 deletion contains a duplicate physical edge")
    simultaneous = components(
        inventory.graph.vertices,
        frozenset(inventory.graph.edges - removed_edges))
    roots = tuple(side for side in simultaneous
                  if block(inventory, inventory.k4).vertices <= side)
    require(len(roots) == 1,
            "simultaneous first-K2 root component is ambiguous")
    root_vertices = roots[0]
    require(frozenset(simultaneous) ==
            frozenset((root_vertices, *away_sets)),
            "individual and simultaneous first-K2 splits disagree")
    verify_partition(inventory, inventory.graph.vertices,
                     (root_vertices, *away_sets),
                     "simultaneous first-K2 partition")

    phase1 = []
    for bridge_index, deleted_edge, vertices in preliminary:
        owned = tuple(index for index in inventory.diamonds
                      if block(inventory, index).edges <=
                      induced_edges(inventory.graph.edges, vertices))
        require(len(owned) in (1, 2),
                "first-K2 away component does not own one or two diamonds")
        analysis = analyze_piece(inventory, vertices)
        require(analysis.rank == 2 * len(owned) and
                analysis.rank in (2, 4),
                "first-K2 away component does not have exact rank 2 or 4")
        require(local_positive_edge_sets(analysis) == frozenset(
                    block(inventory, index).edges for index in owned),
                "away component positive blocks are not exactly its intact diamonds")
        phase1.append(BridgeSide(bridge_index, deleted_edge, vertices,
                                 len(owned), analysis.rank))
    phase1 = tuple(phase1)

    retained = tuple(index for index in inventory.diamonds
                     if block(inventory, index).edges <=
                     induced_edges(inventory.graph.edges, root_vertices))
    require(set(retained) | set(index for side in phase1
                                for index in inventory.diamonds
                                if block(inventory, index).edges <=
                                induced_edges(inventory.graph.edges,
                                              side.vertices)) ==
            set(inventory.diamonds),
            "diamond ownership after first-K2 split is not exhaustive")
    for index in retained:
        route = path_from_root(inventory, ("B", index))
        require(not any(node[0] == "B" and
                        block(inventory, node[1]).kind == "bridge"
                        for node in route),
                "retained diamond still has a K2 on its K4 route")

    frontiers = ancestor_minimal(inventory, retained)
    require(len(frontiers) <= 2,
            "R322 has more than two retained frontier diamonds")
    if retained:
        dominated = set().union(*(
            {index for index in retained
             if is_ancestor(inventory, ("B", frontier), ("B", index))}
            for frontier in frontiers))
        require(dominated == set(retained),
                "frontier does not dominate every retained diamond")
    else:
        require(not frontiers,
                "empty retained inventory has a manufactured frontier")

    opened = []
    for frontier in frontiers:
        cut = upstream_cut(inventory, frontier)
        vertices = boundary_open(inventory, root_vertices, frontier, cut)
        delta = entry_delta(inventory, frontier, cut)
        eta = descendant_diamond_count(inventory, frontier, retained)
        analysis = analyze_piece(inventory, vertices)
        expected_rank = delta + 2 * eta
        require(analysis.rank == expected_rank,
                "opened diamond side rank is not delta+2*eta")
        expected_positive = []
        if delta:
            residual_edges = induced_edges(
                block(inventory, frontier).edges,
                block(inventory, frontier).vertices - {cut})
            require(len(residual_edges) == 3,
                    "degree-two diamond entry did not leave three edges")
            residual_vertices = frozenset().union(*residual_edges)
            residual_degrees = {
                vertex: sum(vertex in current for current in residual_edges)
                for vertex in residual_vertices
            }
            require(len(residual_vertices) == 3 and
                    all(value == 2 for value in residual_degrees.values()),
                    "degree-two diamond entry did not leave a literal triangle")
            expected_positive.append(residual_edges)
        descendants = tuple(index for index in retained
                            if index != frontier and
                            is_ancestor(inventory, ("B", frontier),
                                        ("B", index), strict=True))
        require(len(descendants) == eta,
                "stored eta disagrees with physical descendant diamonds")
        expected_positive.extend(block(inventory, index).edges
                                 for index in descendants)
        require(local_positive_edge_sets(analysis) ==
                frozenset(expected_positive),
                "opened side positive blocks disagree with delta/eta inventory")
        opened.append(OpenSide(frontier, cut, vertices,
                               delta, eta, analysis.rank))
    opened = tuple(opened)
    opened_sets = tuple(item.vertices for item in opened)
    if opened_sets:
        require(sum(len(side) for side in opened_sets) ==
                len(set().union(*opened_sets)),
                "ancestor-minimal opened diamond territories overlap")
    anchor_vertices = (root_vertices if not opened_sets else
                       frozenset(set(root_vertices) -
                                 set().union(*opened_sets)))
    verify_partition(inventory, root_vertices,
                     (anchor_vertices, *opened_sets),
                     "diamond-frontier partition")
    plan = PartitionPlan(PROFILE, phase1, root_vertices, retained,
                         frontiers, opened, anchor_vertices)
    audit_plan(inventory, plan)
    return plan


def final_piece_sets(plan):
    return (plan.anchor_vertices,
            *(item.vertices for item in plan.opened),
            *(item.vertices for item in plan.phase1))


def audit_plan(inventory, plan):
    require(plan.profile == PROFILE, "stored R322 profile changed")
    expected_first = first_diamond_bridges(inventory)
    require(tuple(item.bridge_block for item in plan.phase1) == expected_first,
            "stored first-K2 antichain changed")
    for item in plan.phase1:
        current = block(inventory, item.bridge_block)
        require(current.kind == "bridge" and len(current.edges) == 1 and
                item.deleted_edge == next(iter(current.edges)),
                "stored first-K2 edge is not the exact physical bridge")
        require(item.vertices ==
                bridge_away_component(inventory, item.bridge_block),
                "stored away component is not physically complete")
        analysis = analyze_piece(inventory, item.vertices)
        owned = tuple(index for index in inventory.diamonds
                      if block(inventory, index).edges <= analysis.edges)
        require((item.diamond_count, item.rank) ==
                (len(owned), analysis.rank) and
                item.diamond_count in (1, 2) and
                item.rank == 2 * item.diamond_count,
                "stored away rank/diamond count changed")
    away = tuple(item.vertices for item in plan.phase1)
    expected_root = (inventory.graph.vertices if not away else
                     frozenset(set(inventory.graph.vertices) -
                               set().union(*away)))
    require(plan.root_vertices == expected_root,
            "stored first-K2 root territory changed")
    expected_retained = tuple(index for index in inventory.diamonds
                              if block(inventory, index).edges <=
                              induced_edges(inventory.graph.edges,
                                            expected_root))
    require(plan.retained_diamonds == expected_retained,
            "stored retained-diamond inventory changed")
    expected_frontiers = ancestor_minimal(inventory, expected_retained)
    require(plan.frontiers == expected_frontiers,
            "stored ancestor-minimal frontier changed")
    require(tuple(item.boundary_block for item in plan.opened) ==
            expected_frontiers,
            "stored opened frontier list changed")
    for item in plan.opened:
        cut = upstream_cut(inventory, item.boundary_block)
        require(item.upstream_cut == cut,
                "stored diamond upstream cut changed")
        require(item.vertices == boundary_open(
                    inventory, expected_root, item.boundary_block, cut),
                "stored opened territory is incomplete")
        expected_delta = entry_delta(inventory, item.boundary_block, cut)
        expected_eta = descendant_diamond_count(
            inventory, item.boundary_block, expected_retained)
        analysis = analyze_piece(inventory, item.vertices)
        require((item.delta, item.eta, item.rank) ==
                (expected_delta, expected_eta, analysis.rank) and
                item.rank == item.delta + 2 * item.eta,
                "stored delta/eta/rank tuple changed")
    opened_sets = tuple(item.vertices for item in plan.opened)
    expected_anchor = (expected_root if not opened_sets else
                       frozenset(set(expected_root) -
                                 set().union(*opened_sets)))
    require(plan.anchor_vertices == expected_anchor,
            "stored anchor territory changed")
    final = final_piece_sets(plan)
    verify_partition(inventory, inventory.graph.vertices, final,
                     "final original-vertex partition")
    for cut in inventory.cuts:
        require(sum(cut in side for side in final) == 1,
                "physical articulation has nonunique final owner")
    return True


# ---------------------------------------------------------------------------
# Exact piece receipts and strict integer ledger.
# ---------------------------------------------------------------------------


def anchor_receipt(inventory, plan):
    analysis = analyze_piece(inventory, plan.anchor_vertices)
    require(analysis.rank == 3 and
            local_positive_edge_sets(analysis) ==
            frozenset({block(inventory, inventory.k4).edges}),
            "anchor is not literal-K4-only with bridge trees")
    return PieceReceipt("anchor", "strict-rooted-K4",
                        plan.anchor_vertices, 3, 2, True,
                        "R322-K4-ROOTED-v1")


def open_receipt(inventory, item):
    analysis = analyze_piece(inventory, item.vertices)
    require(analysis.rank == item.delta + 2 * item.eta,
            "opened receipt rank is not delta+2*eta")
    if (item.delta, item.eta) == (0, 0):
        require(analysis.rank == 0 and not analysis.positive_blocks and
                len(analysis.edges) == len(analysis.vertices) - 1,
                "tree debit side is not a nonempty tree")
        category = "tree-debit"
        contract = "R322-TREE-EXACT-v1"
        floor = -1
        strict = False
    elif (item.delta, item.eta) == (1, 0):
        require(analysis.rank == 1 and
                len(analysis.positive_blocks) == 1 and
                analysis.positive_blocks[0].kind == "cycle" and
                analysis.positive_blocks[0].cycle_length == 3,
                "delta-one eta-zero side is not a triangular unicycle")
        category = "triangle-positive"
        contract = "R322-TRIANGLE-UNICYCLIC-v1"
        floor = 0
        strict = True
    elif (item.delta, item.eta) == (0, 1):
        require(analysis.rank == 2,
                "delta-zero eta-one side does not have rank two")
        category = "rank2-descendant-diamond-positive"
        contract = "R322-CONNECTED-RANK2-v1"
        floor = 0
        strict = True
    elif (item.delta, item.eta) == (1, 1):
        require(analysis.rank == 3,
                "delta-one eta-one side does not have rank three")
        category = "rank3-triangle-plus-diamond-nonnegative"
        contract = "R322-CONNECTED-RANK3-v1"
        floor = 0
        strict = False
    else:
        raise VerifyError("opened side has impossible R322 delta/eta pair")
    return PieceReceipt("frontier", category, item.vertices, analysis.rank,
                        floor, strict, contract, item.boundary_block,
                        item.delta, item.eta)


def away_receipt(inventory, item):
    analysis = analyze_piece(inventory, item.vertices)
    require(analysis.rank == item.rank and item.rank in (2, 4) and
            item.rank == 2 * item.diamond_count,
            "away receipt lacks exact rank-two/rank-four authentication")
    contract = f"R322-CONNECTED-RANK{item.rank}-v1"
    require(contract in CONTRACTS and CONTRACTS[contract].floor == 0,
            "away side rank lacks an authenticated nonnegative contract")
    return PieceReceipt("phase1", f"rank{item.rank}-away-nonnegative",
                        item.vertices, item.rank, 0,
                        CONTRACTS[contract].strict, contract)


def derive_ledger(inventory, plan):
    audit_plan(inventory, plan)
    anchor = anchor_receipt(inventory, plan)
    opened = tuple(open_receipt(inventory, item) for item in plan.opened)
    away = tuple(away_receipt(inventory, item) for item in plan.phase1)
    receipts = (anchor, *opened, *away)
    for receipt in receipts:
        require(receipt.contract in CONTRACTS,
                "receipt cites an unknown analytic contract")
        contract = CONTRACTS[receipt.contract]
        require(receipt.floor == contract.floor and
                (not receipt.strict or contract.strict),
                "receipt floor/strictness disagrees with pinned contract")
    tree_debits = sum(item.category == "tree-debit" for item in opened)
    require(0 <= tree_debits <= len(plan.frontiers) <= 2,
            "R322 has more than two frontier tree debits")
    lower_integer = sum(item.floor for item in receipts)
    require(lower_integer == 2 - tree_debits and lower_integer >= 0,
            "strict R322 ledger is not 2-t>=0")
    require(anchor.strict,
            "strict R322 ledger lacks the rooted-K4 strict receipt")
    used = frozenset({
        "R322-PACKET-PROOF-v1",
        "R322-RESIDUAL-SIEVE-v1",
        "R322-THETA-CLASSIFICATION-v1",
        "R322-INDUCED-SUPERADD-v1",
        *(item.contract for item in receipts),
    })
    require(used <= EXPECTED_CONTRACT_IDS,
            "ledger cites a contract outside the immutable manifest")
    ledger = Ledger(PROFILE, "rooted-K4-strict-greater-than-2-minus-t",
                    len(plan.frontiers), tree_debits, anchor.floor,
                    lower_integer, True, receipts, tuple(sorted(used)))
    audit_ledger(inventory, plan, ledger)
    return ledger


def audit_ledger(inventory, plan, ledger):
    anchor = anchor_receipt(inventory, plan)
    opened = tuple(open_receipt(inventory, item) for item in plan.opened)
    away = tuple(away_receipt(inventory, item) for item in plan.phase1)
    receipts = (anchor, *opened, *away)
    tree_debits = sum(item.category == "tree-debit" for item in opened)
    lower_integer = sum(item.floor for item in receipts)
    require(ledger.receipts == receipts,
            "independent receipt replay disagrees")
    require((ledger.profile, ledger.branch, ledger.frontier_count,
             ledger.tree_debits, ledger.anchor_floor,
             ledger.lower_integer, ledger.strict) ==
            (PROFILE, "rooted-K4-strict-greater-than-2-minus-t",
             len(plan.frontiers), tree_debits, anchor.floor,
             lower_integer, True),
            "independent strict integer ledger replay disagrees")
    require(lower_integer == 2 - tree_debits and
            tree_debits <= 2 and anchor.strict,
            "replayed ledger does not prove sigma>2-t>=0")
    fresh_contracts = frozenset({
        "R322-PACKET-PROOF-v1",
        "R322-RESIDUAL-SIEVE-v1",
        "R322-THETA-CLASSIFICATION-v1",
        "R322-INDUCED-SUPERADD-v1",
        *(item.contract for item in receipts),
    })
    require(ledger.contracts == tuple(sorted(fresh_contracts)),
            "replayed graph-specific contract set disagrees")
    return True


def verify(vertices: frozenset, edges: frozenset):
    """Production adjacency-only R322 gate."""
    audit_sources()
    inventory = reconstruct(vertices, edges)
    plan = construct_plan(inventory)
    ledger = derive_ledger(inventory, plan)
    return inventory, plan, ledger


# ---------------------------------------------------------------------------
# Independent adjacency fixture construction and finite corroboration.
# ---------------------------------------------------------------------------


def add_clique(edges, vertices):
    edges.update(edge(left, right)
                 for left, right in itertools.combinations(vertices, 2))


class Builder:
    def __init__(self):
        self.vertices = set()
        self.edges = set()
        self.serial = 0
        self.routing = []
        self.positive = []

    def fresh(self, prefix):
        vertex = (prefix, self.serial)
        self.serial += 1
        self.vertices.add(vertex)
        return vertex

    def k4(self):
        vertices = tuple(self.fresh("K") for _ in range(4))
        add_clique(self.edges, vertices)
        self.positive.append(("K4", vertices))
        return vertices

    def diamond(self, port=None):
        x = port if port is not None else self.fresh("DX")
        if port is not None:
            self.vertices.add(port)
        y = self.fresh("DY")
        a = self.fresh("DA")
        b = self.fresh("DB")
        self.edges.update({edge(x, y), edge(x, a), edge(a, y),
                           edge(x, b), edge(b, y)})
        result = (x, y, a, b)
        self.positive.append(("D", result))
        return result

    def bridge_path(self, left, right, length):
        require(type(length) is int and length >= 1,
                "bridge fixture length must be a positive integer")
        internal = [self.fresh("R") for _ in range(length - 1)]
        sequence = (left, *internal, right)
        self.edges.update(edge(a, b) for a, b in zip(sequence, sequence[1:]))
        self.routing.extend(internal)
        return sequence

    def tree_payload(self, root, count):
        require(type(count) is int and count >= 0,
                "payload count must be a nonnegative integer")
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


def attach_detached_diamond(builder, root, length):
    current = builder.diamond()
    builder.bridge_path(root, current[0], length)
    return current


def fixture(topology, route_length=3, payload_depth=0,
            outer_entry="terminal", nested_entry="terminal"):
    require(route_length >= 1 and payload_depth >= 0,
            "bad R322 fixture expansion parameter")
    require(outer_entry in ("terminal", "internal") and
            nested_entry in ("terminal", "internal"),
            "bad diamond entry orbit")
    builder = Builder()
    k4 = builder.k4()

    def attached_diamond(root, orbit):
        if orbit == "terminal":
            return builder.diamond(root)
        current = builder.diamond()
        old = current[2]  # a degree-two internal vertex
        mapping = {old: root}
        remapped = set()
        for physical_edge in builder.edges:
            left, right = tuple(physical_edge)
            remapped.add(edge(mapping.get(left, left),
                              mapping.get(right, right)))
        builder.edges = remapped
        builder.vertices.discard(old)
        current = tuple(mapping.get(vertex, vertex) for vertex in current)
        builder.positive[-1] = ("D", current)
        return current

    if topology == "direct-separate":
        d1 = attached_diamond(k4[0], outer_entry)
        d2 = builder.diamond(k4[1])

    elif topology == "common-cut":
        d1 = builder.diamond(k4[0])
        d2 = builder.diamond(k4[0])

    elif topology == "nested":
        d1 = attached_diamond(k4[0], outer_entry)
        nested_port = d1[1] if nested_entry == "terminal" else d1[3]
        d2 = builder.diamond(nested_port)

    elif topology == "shared-prefix":
        hub = builder.fresh("HUB")
        builder.bridge_path(k4[0], hub, route_length)
        d1 = builder.diamond(hub)
        d2 = builder.diamond(hub)

    elif topology == "separate-bridges":
        d1 = attach_detached_diamond(builder, k4[0], route_length)
        d2 = attach_detached_diamond(builder, k4[1], route_length + 1)

    elif topology == "one-away-one-root":
        d1 = attach_detached_diamond(builder, k4[0], route_length)
        d2 = builder.diamond(k4[1])

    elif topology == "bridge-after-outer":
        d1 = builder.diamond(k4[0])
        port = d1[1]
        d2 = attach_detached_diamond(builder, port, route_length)

    else:
        raise VerifyError("unknown generated R322 topology")

    if payload_depth:
        builder.tree_payload(k4[3], payload_depth)
        for index, (_, vertices) in enumerate(builder.positive[1:]):
            builder.tree_payload(vertices[-1], min(payload_depth, index + 3))
        for index, current in enumerate(builder.routing[:6]):
            builder.tree_payload(current, min(payload_depth, index + 1))
    graph = builder.graph()
    require(d1 and d2, "generated topology omitted a diamond")
    return graph


def diamond_entry_fixture(entry_orbit, payload_depth=5):
    require(entry_orbit in ("terminal", "internal"),
            "unknown diamond entry orbit fixture")
    return fixture("direct-separate", payload_depth=payload_depth,
                   outer_entry=entry_orbit)


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


def semantic_signature(plan, ledger):
    receipts = tuple(sorted((item.phase, item.category, item.rank,
                             item.floor, item.delta, item.eta)
                            for item in ledger.receipts))
    away = tuple(sorted((item.diamond_count, item.rank)
                        for item in plan.phase1))
    opened = tuple(sorted((item.delta, item.eta, item.rank)
                          for item in plan.opened))
    return (plan.profile, len(plan.phase1), away,
            len(plan.retained_diamonds), len(plan.frontiers), opened,
            ledger.branch, ledger.tree_debits, ledger.anchor_floor,
            ledger.lower_integer, receipts, ledger.contracts)


def expansion_signature(plan, ledger):
    return semantic_signature(plan, ledger)


@dataclass(frozen=True)
class AuditResult:
    generated: int
    relabeled: int
    topologies: tuple[tuple[str, int], ...]
    away_ranks: tuple[tuple[int, int], ...]
    delta_eta: tuple[tuple[tuple[int, int], int], ...]
    categories: tuple[tuple[str, int], ...]
    expansion_cases: int
    long_connector_edges: int
    shared_prefix_cases: int
    hostile_rejections: tuple[str, ...]
    rewires_distinguished: int
    source_files: int
    api_parameters: tuple[str, str]
    no_assert_statements: int


def shared_prefix_audit():
    checked = 0
    for length, payload in ((1, 0), (9, 7), (37, 13)):
        graph = fixture("shared-prefix", route_length=length,
                        payload_depth=payload)
        inventory, plan, ledger = verify(*graph)
        require(len(plan.phase1) == 1 and
                plan.phase1[0].diamond_count == 2 and
                plan.phase1[0].rank == 4 and
                not plan.retained_diamonds and not plan.frontiers,
                "shared-prefix fixture did not produce one rank-four away owner")
        receipt = tuple(item for item in ledger.receipts
                        if item.phase == "phase1")
        require(len(receipt) == 1 and
                receipt[0].contract == "R322-CONNECTED-RANK4-v1",
                "shared-prefix rank-four side got the wrong contract")
        checked += 1
    return checked


def expansion_audit():
    signatures = set()
    for length, payload in ((1, 0), (2, 4), (11, 9), (53, 17)):
        _, plan, ledger = verify(*fixture(
            "one-away-one-root", route_length=length,
            payload_depth=payload))
        signatures.add(expansion_signature(plan, ledger))
    require(len(signatures) == 1,
            "K2/tree expansion changed the semantic R322 certificate")
    long_edges = 1601
    _, plan, ledger = verify(*fixture(
        "shared-prefix", route_length=long_edges, payload_depth=0))
    require(len(plan.phase1) == 1 and plan.phase1[0].rank == 4 and
            ledger.lower_integer == 2,
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


def hostile_tests():
    rejected = []
    base_vertices, base_edges = fixture("common-cut", payload_depth=7)
    inventory, base_plan, base_ledger = verify(base_vertices, base_edges)
    k4 = block(inventory, inventory.k4)
    diamond = block(inventory, inventory.diamonds[0])

    # Physical adjacency mutations.
    kedge = next(iter(k4.edges))
    left, right = tuple(kedge)
    new = ("hostile", "subdivide-k4")
    rejected.append(expect_rejection(
        lambda: verify(frozenset(set(base_vertices) | {new}),
                       frozenset((set(base_edges) - {kedge}) |
                                 {edge(left, new), edge(new, right)})),
        "subdivided literal K4", "unsupported positive-rank block type"))

    dedge = next(iter(diamond.edges))
    left, right = tuple(dedge)
    new = ("hostile", "subdivide-diamond")
    rejected.append(expect_rejection(
        lambda: verify(frozenset(set(base_vertices) | {new}),
                       frozenset((set(base_edges) - {dedge}) |
                                 {edge(left, new), edge(new, right)})),
        "subdivided literal diamond", "unsupported positive-rank block type"))

    missing = next(iter(diamond.edges))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices, frozenset(set(base_edges) - {missing})),
        "diamond edge deletion", "input graph does not have cyclomatic rank seven"))

    private_k = next(iter(k4.vertices - diamond.vertices))
    private_d = next(iter(diamond.vertices - k4.vertices))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices,
                       frozenset(set(base_edges) |
                                 {edge(private_k, private_d)})),
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
                                 {frozenset({private_k})})),
        "malformed loop edge", "malformed unordered edge"))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices,
                       frozenset(set(base_edges) |
                                 {frozenset({private_k, ("outside", 1)})})),
        "foreign endpoint", "edge endpoint outside vertex set"))

    # Wrong physical inventory with rank still seven: K4 + diamond + rank-two
    # theta on five vertices is not literal K4+D+D.
    builder = Builder()
    roots = builder.k4()
    builder.diamond(roots[0])
    x = roots[1]
    y = builder.fresh("TY")
    a = builder.fresh("TA")
    b = builder.fresh("TB")
    c = builder.fresh("TC")
    builder.edges.update({edge(x, y), edge(x, a), edge(a, y),
                          edge(x, b), edge(b, c), edge(c, y)})
    rejected.append(expect_rejection(
        lambda: verify(*builder.graph()),
        "nonliteral rank-two block", "unsupported positive-rank block type"))

    # Runtime contract lookup mutations.
    contract_id = "R322-CONNECTED-RANK4-v1"
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
            ("R322-RESIDUAL-SIEVE-v1", "analytic ledger source-byte mutation"),
            ("R322-THETA-CLASSIFICATION-v1",
             "analytic theta source-byte mutation")):
        source_contract = CONTRACTS[source_contract_id]
        blob = (SOURCE_ROOT / source_contract.source).read_bytes()
        rejected.append(expect_rejection(
            lambda blob=blob, source_contract=source_contract:
                authenticate_source_blob(blob + b"\nHOSTILE",
                                         source_contract.sha256,
                                         "synthetic source mutation"),
            hostile_label, "analytic source changed"))

    source_root_original = globals()["SOURCE_ROOT"]
    globals()["SOURCE_ROOT"] = source_root_original / "absent-r322-sources"
    try:
        rejected.append(expect_rejection(
            lambda: verify(base_vertices, base_edges),
            "public API missing source root",
            "analytic source authentication failed: repository absent"))
    finally:
        globals()["SOURCE_ROOT"] = source_root_original

    # Simultaneously replace both mutable views; immutable manifest hash must
    # still reject altered floor, claim, strictness, and bool-as-int smuggling.
    specs_original = globals()["CONTRACT_SPECS"]
    lookup_original = globals()["CONTRACTS"]
    unused_id = "R322-CONNECTED-RANK4-v1"
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
             replace(unused_original, strict=True),
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

    # The companion proof and its two residual-classification dependencies are
    # authenticated by verify(), not only by a standalone helper.
    mirror_contracts = (
        ("R322-PACKET-PROOF-v1", "companion proof note"),
        ("R322-RESIDUAL-SIEVE-v1", "residual ledger"),
        ("R322-THETA-CLASSIFICATION-v1", "theta classification"),
    )
    with tempfile.TemporaryDirectory(prefix="r322-source-mirror-") as temporary:
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

    # Unexpected implementation exceptions are not hostile-test passes.
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

    # Stored products are untrusted after handoff; replay must reject forgery.
    rejected.append(expect_rejection(
        lambda: audit_plan(inventory,
                           replace(base_plan, frontiers=())),
        "forged frontier set", "stored ancestor-minimal frontier changed"))
    bridge_inventory, bridge_plan, _ = verify(*fixture(
        "shared-prefix", route_length=5))
    genuine = bridge_plan.phase1[0]
    fake_edge = next(current for current in bridge_inventory.graph.edges
                     if current != genuine.deleted_edge)
    rejected.append(expect_rejection(
        lambda: audit_plan(bridge_inventory,
                           replace(bridge_plan,
                                   phase1=(replace(genuine,
                                                   deleted_edge=fake_edge),))),
        "forged selected physical bridge",
        "stored first-K2 edge is not the exact physical bridge"))
    rejected.append(expect_rejection(
        lambda: audit_ledger(inventory, base_plan,
                             replace(base_ledger, lower_integer=99)),
        "forged ledger integer",
        "independent strict integer ledger replay disagrees"))

    # Same inventory, different physical route must produce distinct semantics.
    _, direct_plan, direct_ledger = verify(*fixture("common-cut"))
    _, bridge_plan, bridge_ledger = verify(*fixture(
        "separate-bridges", route_length=8))
    require(semantic_signature(direct_plan, direct_ledger) !=
            semantic_signature(bridge_plan, bridge_ledger),
            "same-inventory direct/bridge rewire was not distinguished")
    return tuple(rejected), 1


def audit():
    source_files = audit_sources()
    api_parameters = api_shape_audit()
    no_assert_statements = no_assert_audit()
    cases = (
        ("direct-separate", 3, 0, "terminal", "terminal"),
        ("direct-separate", 3, 4, "internal", "terminal"),
        ("common-cut", 3, 7, "terminal", "terminal"),
        ("nested", 3, 5, "terminal", "terminal"),
        ("nested", 3, 6, "internal", "terminal"),
        ("shared-prefix", 9, 8, "terminal", "terminal"),
        ("separate-bridges", 11, 9, "terminal", "terminal"),
        ("one-away-one-root", 13, 7, "terminal", "terminal"),
        ("bridge-after-outer", 8, 6, "terminal", "terminal"),
    )
    topologies = Counter()
    away_ranks = Counter()
    delta_eta = Counter()
    categories = Counter()
    generated = relabeled = 0
    for index, (topology, length, payload,
                outer_entry, nested_entry) in enumerate(cases):
        graph = fixture(topology, length, payload,
                        outer_entry, nested_entry)
        inventory, plan, ledger = verify(*graph)
        require(tuple(sorted(block(inventory, current).rank
                             for current in positive_ids(inventory))) ==
                (2, 2, 3),
                "generated R322 block-rank inventory changed")
        require(ledger.lower_integer == 2 - ledger.tree_debits and
                ledger.tree_debits <= 2 and ledger.strict,
                "generated R322 strict ledger changed")
        topologies[topology] += 1
        away_ranks.update(item.rank for item in plan.phase1)
        delta_eta.update((item.delta, item.eta) for item in plan.opened)
        categories.update(item.category for item in ledger.receipts)
        generated += 1
        relabeled_graph = opaque_relabel(*graph, salt=31 + 17 * index)
        _, relabeled_plan, relabeled_ledger = verify(*relabeled_graph)
        require(semantic_signature(plan, ledger) ==
                semantic_signature(relabeled_plan, relabeled_ledger),
                "opaque relabeling changed the R322 semantic certificate")
        relabeled += 1

    require({"direct-separate", "common-cut", "nested", "shared-prefix",
             "separate-bridges", "one-away-one-root",
             "bridge-after-outer"} <= set(topologies),
            "hostile R322 topology coverage incomplete")
    require({2, 4} <= set(away_ranks),
            "away-rank coverage missed rank two or four")
    require({(0, 0), (1, 0), (0, 1), (1, 1)} <= set(delta_eta),
            "delta/eta receipt coverage incomplete")
    require({"strict-rooted-K4", "tree-debit", "triangle-positive",
             "rank2-descendant-diamond-positive",
             "rank3-triangle-plus-diamond-nonnegative",
             "rank2-away-nonnegative", "rank4-away-nonnegative"} <=
            set(categories),
            "R322 piece-category coverage incomplete")
    expansion_cases, long_connector = expansion_audit()
    shared_cases = shared_prefix_audit()
    rejected, rewires = hostile_tests()
    return AuditResult(
        generated, relabeled, tuple(sorted(topologies.items())),
        tuple(sorted(away_ranks.items())),
        tuple(sorted(delta_eta.items())),
        tuple(sorted(categories.items())), expansion_cases,
        long_connector, shared_cases, rejected, rewires,
        source_files, api_parameters, no_assert_statements)


def report(result):
    return "\n".join((
        "R322 adjacency semantic verifier: finite corroboration passed",
        "scope: literal K4+D+D physical R322 only; no global, other-packet, or single-block claim",
        "proof boundary: universal theorem is the pinned companion note; this program is a finite suite plus public adjacency gate",
        "API: verify(vertices:frozenset, edges:frozenset); no supplied profile, block, route, owner, rank, charge, threshold, or partition",
        "reconstruction: iterative Tarjan; physical K2 blocks retained; literal K4+D+D; total rank 7; full block-cut tree",
        "phase 1: deduplicated first-K2 antichain; complete away owners have exact rank 2 or 4",
        "phase 2: ancestor-minimal retained-diamond frontier; boundary-open original-vertex pieces; exact rank delta+2*eta",
        "ownership: every final piece is original-vertex, induced, connected, disjoint, and exhaustive; every cut has one owner",
        "ledger: rooted literal K4 >2; only delta=eta=0 tree sides debit; sigma(G)>2-t>=0 with t<=2",
        f"analytic source files pinned: {result.source_files}; source manifest sha256: {source_manifest_digest()}",
        f"authenticated contract records: {len(EXPECTED_CONTRACT_IDS)}; full manifest sha256: {full_contract_manifest_digest()}",
        f"generated topology fixtures: {result.generated}; opaque relabel replays: {result.relabeled}",
        "topologies: " + repr(dict(result.topologies)),
        "away ranks: " + repr(dict(result.away_ranks)),
        "delta/eta pairs: " + repr(dict(result.delta_eta)),
        "piece categories: " + repr(dict(result.categories)),
        f"K2/tree expansion probes: {result.expansion_cases}; longest connector: {result.long_connector_edges} physical edges",
        f"shared-first-K2-prefix rank-four probes: {result.shared_prefix_cases}",
        f"hostile mutations rejected: {len(result.hostile_rejections)}; same-inventory rewires distinguished: {result.rewires_distinguished}",
        "production API parameters: " + repr(result.api_parameters),
        f"assert statements in verifier AST: {result.no_assert_statements}",
        "analytic contracts: " + repr(tuple(sorted(EXPECTED_CONTRACT_IDS))),
        "companion note sha256: " + CONTRACTS["R322-PACKET-PROOF-v1"].sha256,
        "verifier sha256: " + file_digest(Path(__file__)),
        "status: R322 finite corroboration and independent semantic replay passed",
    ))


def main():
    if sys.argv != [sys.argv[0]]:
        print("R322 verifier: command line arguments are not accepted",
              file=sys.stderr)
        return 2
    print(report(audit()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
