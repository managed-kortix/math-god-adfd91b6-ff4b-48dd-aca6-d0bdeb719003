#!/usr/bin/env python3
"""Adjacency-only semantic verifier/corroborator for the complete physical R321 lane.

The production API is ``verify(vertices, edges)``.  Its only input is a finite
simple graph represented by a nonempty frozenset of original vertices and a
frozenset of unordered two-vertex frozenset edges.  The verifier reconstructs
all blocks, cuts, physical bridges, rooted block-cut ancestry, side ownership,
piece topology, charges, and the final integer ledger.  It accepts no claimed
profile, packet, owner, charge, rank, threshold, or partition.

This verifier is intentionally scoped to R321.  It neither edits nor imports
state from the repository; analytic dependencies are authenticated as pinned
read-only source bytes below.  Its generic adjacency API and finite generated
suite corroborate the implementation but do not by themselves prove the
universal theorem over arbitrary block-cut trees; that proof is in the
companion packet note.

The returned ``Inventory`` is a diagnostic reconstruction with internal mutable
mapping containers; callers must treat it as untrusted after handoff.  The
immutable ``PartitionPlan`` and ``Ledger`` values are the portable receipt.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import shutil
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
    ("R321-PACKET-PROOF-v1", Contract(
        "positive-square-energy/heptacyclic-general/r321-complete-physical-closure.md",
        "76aef4d8066b9cf58331281318e44b838c4737a7dfb47606c5e1b21f4ce2696c",
        "reviewed universal proof of the complete physical R321 packet", None, False)),
    ("R321-RESIDUAL-SIEVE-v1", Contract(
        "positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md",
        "3f8bb3a397125782dd6c9cae26ce52f9c6bf826e3136dfee62781048e65c18a5",
        "exact R321 residual families K4+Theta(1,2,r)+T2 and K4+D+T+P", None, False)),
    ("R321-INDUCED-SUPERADD-v1", Contract(
        "all-tricyclic-graphs/paper.tex",
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
        "positive-square-energy induced superadditivity", None, False)),
    ("R321-CONNECTED-FLOOR-v1", Contract(
        "tree-equality-square-energy/paper.tex",
        "66370f3cb81546325f0e9a4e19919aa2572f0d147cff6d8baa3f9425e7d82889",
        "every nonempty connected H has sigma(H)>=-1", -1, False)),
    ("R321-CONNECTED-RANK2-v1", Contract(
        "all-bicyclic-graphs/paper.tex",
        "56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da",
        "every connected rank-two graph has sigma>0", 0, True)),
    ("R321-CONNECTED-RANK3-v1", Contract(
        "all-tricyclic-graphs/paper.tex",
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
        "every connected rank-three graph has sigma>=0", 0, False)),
    ("R321-CONNECTED-RANK4-v1", Contract(
        "all-tetracyclic-graphs/paper.tex",
        "70a931c28c8a8817e2c02818200885f73c532d9afe2c065831f2b3884d61160f",
        "every connected rank-four graph has sigma>=0", 0, False)),
    ("R321-TRIANGLE-UNICYCLIC-v1", Contract(
        "packing-two-square-energy/paper.tex",
        "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
        "connected triangular block graph containing a triangle has sigma>0", 0, True)),
    ("R321-K4-ROOTED-v1", Contract(
        "packing-two-square-energy/paper.tex",
        "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
        "literal K4 with bridge trees has sigma>2", 2, True)),
    ("R321-K4-T-SHARED-v1", Contract(
        "packing-two-square-energy/paper.tex",
        "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
        "direct shared-cut literal K4 plus triangle has sigma>3", 3, True)),
)

CONTRACTS = dict(CONTRACT_SPECS)

# Independent canonical anchors.  These do not derive their expected values
# from the mutable runtime tuple/dict.  In particular, simultaneous rebinding
# of CONTRACT_SPECS and CONTRACTS cannot authenticate altered claims or floors.
EXPECTED_CONTRACT_IDS = frozenset({
    "R321-PACKET-PROOF-v1",
    "R321-RESIDUAL-SIEVE-v1",
    "R321-INDUCED-SUPERADD-v1",
    "R321-CONNECTED-FLOOR-v1",
    "R321-CONNECTED-RANK2-v1",
    "R321-CONNECTED-RANK3-v1",
    "R321-CONNECTED-RANK4-v1",
    "R321-TRIANGLE-UNICYCLIC-v1",
    "R321-K4-ROOTED-v1",
    "R321-K4-T-SHARED-v1",
})
EXPECTED_SOURCE_ROWS = frozenset({
    ("positive-square-energy/heptacyclic-general/r321-complete-physical-closure.md",
     "76aef4d8066b9cf58331281318e44b838c4737a7dfb47606c5e1b21f4ce2696c"),
    ("positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md",
     "3f8bb3a397125782dd6c9cae26ce52f9c6bf826e3136dfee62781048e65c18a5"),
    ("all-tricyclic-graphs/paper.tex",
     "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02"),
    ("tree-equality-square-energy/paper.tex",
     "66370f3cb81546325f0e9a4e19919aa2572f0d147cff6d8baa3f9425e7d82889"),
    ("all-bicyclic-graphs/paper.tex",
     "56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da"),
    ("all-tetracyclic-graphs/paper.tex",
     "70a931c28c8a8817e2c02818200885f73c532d9afe2c065831f2b3884d61160f"),
    ("packing-two-square-energy/paper.tex",
     "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791"),
})

# Hard-coded independent anchors for the canonical encodings below.  The full
# encoding is UTF-8 JSON with ensure_ascii=True and compact separators.  It is
# an object {"schema":"r321-contract-manifest-v1","records":[...]} in tuple
# order; every record contains ID, path, SHA-256, exact claim string, an
# explicitly tagged floor ({"kind":"null"} or {"kind":"integer","value":n}),
# and strict as a JSON boolean.
EXPECTED_FULL_CONTRACT_MANIFEST_SHA256 = (
    "200283635516c399fac34c7b81ff04a0fca45051855cb551d99c1e19155f27fe")
EXPECTED_SOURCE_MANIFEST_SHA256 = (
    "49fa7043e940d81119ad1aa91cce3e7e077b8a5412686f293fefe7d1ca82178a")


def source_manifest_digest(specs=None):
    specs = CONTRACT_SPECS if specs is None else specs
    rows = sorted({f"{item.source}\t{item.sha256}" for _, item in specs})
    return sha256_bytes(("\n".join(rows) + "\n").encode())


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
    payload = {"schema": "r321-contract-manifest-v1", "records": records}
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
            EXPECTED_CONTRACT_IDS and len(CONTRACT_SPECS) ==
            len(EXPECTED_CONTRACT_IDS),
            "analytic contract ID set changed")
    require(type(CONTRACTS) is dict and frozenset(CONTRACTS) ==
            EXPECTED_CONTRACT_IDS,
            "analytic contract lookup changed")
    require(CONTRACTS == dict(CONTRACT_SPECS),
            "analytic contract tuple/lookup disagree")
    # Type-check every record before serializing/hashing.  In particular,
    # Python's True == 1 must never blur a Boolean floor with an integer floor.
    for contract_id, item in CONTRACT_SPECS:
        require(type(contract_id) is str and contract_id,
                "malformed contract ID")
        require(type(item.source) is str and item.source,
                f"malformed source path: {contract_id}")
        require(type(item.sha256) is str and len(item.sha256) == 64 and
                all(character in "0123456789abcdef" for character in item.sha256),
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
    require(sha256_bytes(blob) == expected, f"analytic source changed: {label}")


def audit_sources():
    audit_contract_table()
    require(SOURCE_ROOT.is_dir(), "analytic source authentication failed: repository absent")
    checked = set()
    for contract_id, item in CONTRACTS.items():
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
    theta_lengths: tuple[int, int, int] | None = None


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


def _path_between(graph, start, finish):
    previous = {start: None}
    queue = deque([start])
    while queue and finish not in previous:
        current = queue.popleft()
        for neighbor in graph[current]:
            if neighbor not in previous:
                previous[neighbor] = current
                queue.append(neighbor)
    require(finish in previous, "theta arm path is disconnected")
    answer = []
    current = finish
    while current is not None:
        answer.append(current)
        current = previous[current]
    return tuple(reversed(answer))


def authenticate_theta_edges(edges):
    """Return path lengths iff the block is literally Theta(1,2,r), r>=2."""
    vertices = frozenset().union(*edges)
    graph = adjacency(vertices, edges)
    degrees = {vertex: len(graph[vertex]) for vertex in vertices}
    require(len(edges) == len(vertices) + 1, "rank-two block has wrong edge count")
    branches = tuple(vertex for vertex in vertices if degrees[vertex] == 3)
    require(len(branches) == 2 and
            all(value in (2, 3) for value in degrees.values()),
            "rank-two block is not a theta with two cubic terminals")
    x, y = branches
    require(edge(x, y) in edges, "theta lacks its literal length-one arm")
    interiors = vertices - {x, y}
    interior_edges = induced_edges(edges, interiors)
    pieces = components(interiors, interior_edges)
    require(len(pieces) == 2, "theta terminal deletion does not expose two arms")
    lengths = [1]
    for piece in pieces:
        piece_edges = induced_edges(interior_edges, piece)
        require(len(piece_edges) == len(piece) - 1,
                "theta interior arm is not a tree")
        inner_graph = adjacency(piece, piece_edges)
        require(all(len(inner_graph[v]) <= 2 for v in piece),
                "theta interior arm branches")
        if len(piece) == 1:
            only = next(iter(piece))
            require(edge(x, only) in edges and edge(only, y) in edges,
                    "singleton theta arm is not joined to both terminals")
        else:
            ends = tuple(v for v in piece if len(inner_graph[v]) == 1)
            require(len(ends) == 2, "theta interior path lacks two endpoints")
            at_x = tuple(v for v in ends if edge(x, v) in edges)
            at_y = tuple(v for v in ends if edge(y, v) in edges)
            require(len(at_x) == len(at_y) == 1 and at_x[0] != at_y[0],
                    "theta arm endpoints have wrong terminal incidence")
            path = _path_between(inner_graph, at_x[0], at_y[0])
            require(len(path) == len(piece), "theta arm path omits a vertex")
        lengths.append(len(piece) + 1)
    lengths = tuple(sorted(lengths))
    require(lengths[0:2] == (1, 2) and lengths[2] >= 2,
            "rank-two block is not Theta(1,2,r), r>=2")
    require(sum(lengths) == len(edges), "theta paths do not exhaust block edges")
    return lengths


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
    if rank == 2:
        lengths = authenticate_theta_edges(edges)
        return Block(index, edges, vertices, rank, "theta", None, lengths)
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
    thetas = tuple(item.index for item in positive if item.kind == "theta")
    cycles = tuple(item.index for item in positive if item.kind == "cycle")
    require(len(k4s) == 1 and len(thetas) == 1 and len(cycles) == 2 and
            len(positive) == 4,
            "positive blocks are not literal K4 + Theta(1,2,r) + two cycles")
    require(tuple(sorted(item.rank for item in positive)) == (1, 1, 2, 3),
            "positive block ranks are not exactly 3+2+1+1")
    require(sum(item.rank for item in positive) == 7,
            "positive block ranks do not sum to seven")

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
    inventory = Inventory(graph, adjacency(graph.vertices, graph.edges), blocks,
                          cuts, tree, k4s[0], cycles, bridges,
                          parent, depth, order)
    # Keep theta as an adjacency-derived positive block discoverable by kind;
    # the compact Inventory shape is inherited from the generic K4 utility.
    require(len(theta_ids(inventory)) == 1, "theta inventory reconstruction failed")
    return inventory


def theta_ids(inventory):
    return tuple(item.index for item in inventory.blocks if item.kind == "theta")


def external_ids(inventory):
    return (*theta_ids(inventory), *inventory.cycles)


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
                color = ("block", item.kind, item.cycle_length, item.theta_lengths)
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
    originals = (inventory.k4, *external_ids(inventory))
    intact_ids = tuple(sorted(index for index in originals
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




# ---------------------------------------------------------------------------
# R321 profile, first bridges, external frontiers, and exact ledger.
# ---------------------------------------------------------------------------


def derive_profile(inventory):
    theta = block(inventory, theta_ids(inventory)[0])
    require(theta.theta_lengths is not None and theta.theta_lengths[:2] == (1, 2),
            "rank-two block is not authenticated Theta(1,2,r)")
    lengths = tuple(sorted(block(inventory, index).cycle_length
                           for index in inventory.cycles))
    if lengths == (3, 3):
        profile = "K4+Theta(1,2,r)+T2"
    elif theta.theta_lengths == (1, 2, 2) and lengths == (3, 5):
        profile = "K4+D+T+P"
    else:
        raise VerifyError("adjacency-derived profile is not an exact R321 residual")
    triangle = tuple(index for index in inventory.cycles
                     if block(inventory, index).cycle_length == 3)
    require(triangle, "R321 residual has no guaranteed literal triangle")
    return profile, triangle


def first_hull_bridges(inventory):
    chosen = set()
    for external in external_ids(inventory):
        route = path_from_root(inventory, ("B", external))
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
    """Return X-c plus every current descendant owner, on original vertices."""
    boundary = block(inventory, boundary_index)
    require(boundary.rank > 0 and boundary_index != inventory.k4,
            "boundary opening requires an external positive block")
    require(boundary.vertices <= current_vertices,
            "boundary block is not intact in current territory")
    require(cut in boundary.vertices, "upstream articulation outside boundary")
    current_edges = induced_edges(inventory.graph.edges, current_vertices)
    require(boundary.edges <= current_edges, "boundary edges missing from territory")
    owner_components = components(current_vertices,
                                  frozenset(current_edges - boundary.edges))
    by_vertex = {}
    for side in owner_components:
        hits = side & boundary.vertices
        require(len(hits) == 1,
                "outside owner component meets a maximal block at multiple vertices")
        owner = next(iter(hits))
        require(owner not in by_vertex, "block vertex has duplicate owner component")
        by_vertex[owner] = side
    require(set(by_vertex) == set(boundary.vertices),
            "block owner decomposition omitted a boundary vertex")
    result = frozenset().union(*(by_vertex[vertex]
                                for vertex in boundary.vertices if vertex != cut))
    require(result and cut not in result,
            "opened side is empty or copied its upstream articulation")
    require(boundary.vertices - {cut} <= result,
            "opened side omitted X-c")
    require(connected(result, induced_edges(inventory.graph.edges, result)),
            "X-c descendant side is disconnected")
    return result


def ancestor_minimal(inventory, candidates):
    candidates = tuple(candidates)
    candidate_set = set(candidates)
    selected = []
    for index in candidates:
        route = path_from_root(inventory, ("B", index))
        if not any(node[0] == "B" and node[1] in candidate_set
                   for node in route[:-1]):
            selected.append(index)
    nodes = [("B", index) for index in selected]
    for left, right in itertools.permutations(nodes, 2):
        require(not is_ancestor(inventory, left, right, strict=True),
                "ancestor-minimal frontiers are not an antichain")
    return tuple(sorted(selected))


@dataclass(frozen=True)
class BridgeSide:
    bridge_block: int
    deleted_edge: frozenset
    vertices: frozenset


@dataclass(frozen=True)
class OpenSide:
    boundary_block: int
    upstream_cut: object
    vertices: frozenset


@dataclass(frozen=True)
class PartitionPlan:
    profile: str
    phase1: tuple[BridgeSide, ...]
    root_vertices: frozenset
    root_external: tuple[int, ...]
    frontiers: tuple[int, ...]
    anchor_triangle: int | None
    opened: tuple[OpenSide, ...]
    anchor_vertices: frozenset


@dataclass(frozen=True)
class PieceReceipt:
    phase: str
    category: str
    vertices: frozenset
    rank: int
    positive_ids: tuple[int, ...]
    floor: int
    strict: bool
    contract: str


@dataclass(frozen=True)
class Ledger:
    profile: str
    branch: str
    frontier_count: int
    anchor_floor: int
    side_debits: int
    away_positive: int
    value: int
    strict: bool
    receipts: tuple[PieceReceipt, ...]
    contracts: tuple[str, ...]


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
        require(current_edges == frozenset(edge_ for edge_ in inventory.graph.edges
                                           if edge_ <= side),
                f"{label} piece edge set is not induced")
    return True


def choose_triangle(inventory, candidates):
    require(candidates, "triangle anchor candidate set is empty")
    canonical = canonical_subtree_ids(inventory)
    best = min(canonical[("B", index)] for index in candidates)
    # Equal signatures are proof-equivalent: every candidate is a literal C3
    # frontier and yields the same fixed anchor contract.
    return next(index for index in candidates
                if canonical[("B", index)] == best)


def construct_plan(inventory, profile):
    first = first_hull_bridges(inventory)
    phase1 = tuple(BridgeSide(index,
                              next(iter(block(inventory, index).edges)),
                              bridge_away_component(inventory, index))
                   for index in first)
    away = tuple(item.vertices for item in phase1)
    if away:
        require(sum(map(len, away)) == len(set().union(*away)),
                "first-bridge away components overlap")
        removed = frozenset(item.deleted_edge for item in phase1)
        require(len(removed) == len(phase1),
                "simultaneous bridge deletion contains duplicate edges")
        simultaneous = components(inventory.graph.vertices,
                                  frozenset(inventory.graph.edges - removed))
        roots = [side for side in simultaneous
                 if block(inventory, inventory.k4).vertices <= side]
        require(len(roots) == 1, "simultaneous first-bridge root is ambiguous")
        root_vertices = roots[0]
        require(frozenset(simultaneous) == frozenset((root_vertices, *away)),
                "individual and simultaneous first-bridge partitions disagree")
    else:
        root_vertices = inventory.graph.vertices
    verify_partition(inventory, inventory.graph.vertices,
                     (root_vertices, *away), "first-bridge partition")

    for side in phase1:
        current = block(inventory, side.bridge_block)
        require(current.kind == "bridge" and len(current.edges) == 1 and
                side.deleted_edge == next(iter(current.edges)) and
                side.deleted_edge in inventory.graph.edges,
                "first-bridge split did not delete exactly one physical K2 edge")
        analysis = analyze_piece(inventory, side.vertices)
        require(inventory.k4 not in analysis.positive_ids and
                1 <= analysis.rank <= 4,
                "first-bridge away side rank is outside exact R321 range 1..4")
        require(analysis.rank == sum(block(inventory, index).rank
                                     for index in analysis.positive_ids),
                "away rank is not the sum of its owned intact external ranks")
    root_external = tuple(index for index in external_ids(inventory)
                          if block(inventory, index).vertices <= root_vertices)
    for index in root_external:
        route = path_from_root(inventory, ("B", index))
        require(not any(node[0] == "B" and
                        block(inventory, node[1]).kind == "bridge"
                        for node in route),
                "root external block still has a bridge on its K4 route")
    frontiers = ancestor_minimal(inventory, root_external)
    require(len(frontiers) <= 3, "R321 has more than three external frontiers")
    require(set(root_external) == set().union(*(
        {index for index in root_external
         if is_ancestor(inventory, ("B", frontier), ("B", index))}
        for frontier in frontiers)) if frontiers else not root_external,
        "frontiers do not dominate every retained external block")

    frontier_triangles = tuple(index for index in frontiers
                               if block(inventory, index).kind == "cycle" and
                               block(inventory, index).cycle_length == 3)
    negative_p_away = False
    if profile == "K4+D+T+P":
        for side in phase1:
            analysis = analyze_piece(inventory, side.vertices)
            if analysis.rank == 1 and analysis.cycle_lengths == (5,):
                require(not negative_p_away,
                        "more than one singleton pentagon away side")
                negative_p_away = True
    if len(frontiers) == 3:
        require(set(frontiers) == set(root_external) and len(root_external) == 3,
                "three frontiers are not all three external blocks")
        anchor_triangle = choose_triangle(inventory, frontier_triangles)
        route = path_from_root(inventory, ("B", anchor_triangle))
        require(len(route) == 3 and route[1][0] == "C",
                "three-frontier triangle is not direct shared-cut with K4")
        opened_ids = tuple(index for index in frontiers if index != anchor_triangle)
    elif negative_p_away and len(frontiers) == 2:
        # Root contains exactly D and T. Both are minimal and bridge-free, so
        # retain direct T with K4 and open only D; the P away debit is separate.
        require(len(root_external) == 2,
                "P-away/two-frontier branch has extra root external block")
        anchor_triangle = choose_triangle(inventory, frontier_triangles)
        route = path_from_root(inventory, ("B", anchor_triangle))
        require(len(route) == 3 and route[1][0] == "C",
                "P-away root triangle is not direct shared-cut with K4")
        opened_ids = tuple(index for index in frontiers if index != anchor_triangle)
    else:
        anchor_triangle = None
        opened_ids = frontiers

    opened = tuple(OpenSide(index, upstream_cut(inventory, index),
                            boundary_open(inventory, root_vertices, index,
                                          upstream_cut(inventory, index)))
                   for index in opened_ids)
    opened_sets = tuple(item.vertices for item in opened)
    if opened_sets:
        require(sum(map(len, opened_sets)) == len(set().union(*opened_sets)),
                "frontier-opened sides overlap")
        anchor_vertices = frozenset(set(root_vertices) - set().union(*opened_sets))
    else:
        anchor_vertices = root_vertices
    verify_partition(inventory, root_vertices,
                     (anchor_vertices, *opened_sets), "frontier partition")
    plan = PartitionPlan(profile, phase1, root_vertices, root_external,
                         frontiers, anchor_triangle, opened, anchor_vertices)
    audit_plan(inventory, plan)
    return plan


def final_piece_sets(plan):
    return (plan.anchor_vertices,
            *(item.vertices for item in plan.opened),
            *(item.vertices for item in plan.phase1))


def audit_plan(inventory, plan):
    profile, _ = derive_profile(inventory)
    require(plan.profile == profile, "stored R321 profile changed")
    expected_first = first_hull_bridges(inventory)
    require(tuple(item.bridge_block for item in plan.phase1) == expected_first,
            "stored first-bridge set changed")
    for item in plan.phase1:
        current = block(inventory, item.bridge_block)
        require(current.kind == "bridge" and len(current.edges) == 1 and
                item.deleted_edge == next(iter(current.edges)),
                "stored first-bridge edge is not the exact physical K2 edge")
        require(item.vertices == bridge_away_component(inventory, item.bridge_block),
                "stored away side is not its complete physical component")
    away = tuple(item.vertices for item in plan.phase1)
    expected_root = (inventory.graph.vertices if not away else
                     frozenset(set(inventory.graph.vertices) - set().union(*away)))
    require(plan.root_vertices == expected_root, "stored root territory changed")
    expected_external = tuple(index for index in external_ids(inventory)
                              if block(inventory, index).vertices <= expected_root)
    require(plan.root_external == expected_external,
            "stored root external inventory changed")
    expected_frontiers = ancestor_minimal(inventory, expected_external)
    require(plan.frontiers == expected_frontiers, "stored frontier set changed")
    triangles = tuple(index for index in expected_frontiers
                      if block(inventory, index).kind == "cycle" and
                      block(inventory, index).cycle_length == 3)
    negative_p_away = False
    if profile == "K4+D+T+P":
        for item in plan.phase1:
            analysis = analyze_piece(inventory, item.vertices)
            if analysis.rank == 1 and analysis.cycle_lengths == (5,):
                negative_p_away = True
    if len(expected_frontiers) == 3 or (negative_p_away and
                                        len(expected_frontiers) == 2):
        expected_anchor = choose_triangle(inventory, triangles)
        require(plan.anchor_triangle == expected_anchor,
                "stored direct triangle anchor changed")
        opened_ids = tuple(index for index in expected_frontiers
                           if index != expected_anchor)
    else:
        require(plan.anchor_triangle is None,
                "frontier branch manufactured a triangle anchor")
        opened_ids = expected_frontiers
    require(tuple(item.boundary_block for item in plan.opened) == opened_ids,
            "stored opened frontier list changed")
    for item in plan.opened:
        require(item.upstream_cut == upstream_cut(inventory, item.boundary_block),
                "stored frontier cut changed")
        require(item.vertices == boundary_open(inventory, expected_root,
                                               item.boundary_block,
                                               item.upstream_cut),
                "stored frontier side is not complete")
    opened_sets = tuple(item.vertices for item in plan.opened)
    expected_anchor_vertices = (expected_root if not opened_sets else
                                frozenset(set(expected_root) -
                                          set().union(*opened_sets)))
    require(plan.anchor_vertices == expected_anchor_vertices,
            "stored anchor owner changed")
    final = final_piece_sets(plan)
    verify_partition(inventory, inventory.graph.vertices, final,
                     "final original-vertex partition")
    for cut in inventory.cuts:
        require(sum(cut in side for side in final) == 1,
                "physical articulation has nonunique final owner")
    return True


def generic_receipt(inventory, phase, vertices):
    """Authenticate only the universal connected floor on an induced side.

    Frontier opening may cut an original maximal block at an internal
    articulation.  The resulting induced side can contain a residual local
    cycle that is not an intact original block.  That is legal: boundary_open
    authenticates the operation itself, and this receipt makes no local block
    type or original-block bijection claim.
    """
    require(type(vertices) is frozenset and vertices,
            "generic-floor piece is empty or malformed")
    require(vertices <= inventory.graph.vertices,
            "generic-floor piece has a foreign vertex")
    edges = induced_edges(inventory.graph.edges, vertices)
    require(connected(vertices, edges), "generic-floor piece is disconnected")
    touched = tuple(sorted(index for index in
                           (inventory.k4, *external_ids(inventory))
                           if block(inventory, index).edges & edges))
    return PieceReceipt(phase, "connected-generic-floor", vertices,
                        graph_rank(vertices, edges), touched, -1, False,
                        "R321-CONNECTED-FLOOR-v1")


def away_receipt(inventory, vertices):
    analysis = analyze_piece(inventory, vertices)
    if (analysis.rank == 1 and analysis.cycle_lengths == (3,) and
            analysis.positive_kinds == ("cycle",)):
        return PieceReceipt("phase1", "intact-triangle-away-positive", vertices,
                            analysis.rank, analysis.positive_ids, 0, True,
                            "R321-TRIANGLE-UNICYCLIC-v1")
    if analysis.rank in (2, 3, 4):
        # In R321 every first-bridge away component has rank at most four.
        # The completed connected rank-2/3/4 theorems give sigma>=0; authenticate
        # the exact fixed-rank source from the recomputed adjacency rank.
        contract = f"R321-CONNECTED-RANK{analysis.rank}-v1"
        require(contract in CONTRACTS and CONTRACTS[contract].floor == 0,
                "away rank has no authenticated fixed-rank nonnegative contract")
        return PieceReceipt("phase1", "rank>=2-away-nonnegative", vertices,
                            analysis.rank, analysis.positive_ids, 0, False,
                            contract)
    require(analysis.rank == 1 and analysis.cycle_lengths == (5,) and
            plan_profile_for_analysis(inventory) == "K4+D+T+P",
            "rank-one away side is not the unique residual pentagon")
    return generic_receipt(inventory, "phase1", vertices)


def plan_profile_for_analysis(inventory):
    return derive_profile(inventory)[0]


def anchor_receipt(inventory, plan):
    analysis = analyze_piece(inventory, plan.anchor_vertices)
    if plan.anchor_triangle is None:
        require(analysis.positive_ids == (inventory.k4,) and analysis.rank == 3,
                "rooted K4 anchor retains an external positive block")
        return PieceReceipt("anchor", "strict-rooted-K4", plan.anchor_vertices,
                            analysis.rank, analysis.positive_ids, 2, True,
                            "R321-K4-ROOTED-v1")
    require(set(analysis.positive_ids) == {inventory.k4, plan.anchor_triangle} and
            analysis.rank == 4 and analysis.cycle_lengths == (3,),
            "direct anchor is not exactly K4 plus one literal triangle")
    route = path_from_root(inventory, ("B", plan.anchor_triangle))
    require(len(route) == 3 and route[1][0] == "C",
            "K4+T anchor is not direct shared-cut")
    return PieceReceipt("anchor", "strict-shared-K4+T", plan.anchor_vertices,
                        analysis.rank, analysis.positive_ids, 3, True,
                        "R321-K4-T-SHARED-v1")


def derive_ledger(inventory, plan):
    audit_plan(inventory, plan)
    anchor = anchor_receipt(inventory, plan)
    opened = tuple(generic_receipt(inventory, "frontier", item.vertices)
                   for item in plan.opened)
    away = tuple(away_receipt(inventory, item.vertices) for item in plan.phase1)
    receipts = (anchor, *opened, *away)
    for receipt in receipts:
        require(receipt.contract in CONTRACTS,
                "receipt cites an unknown analytic contract")
        contract = CONTRACTS[receipt.contract]
        require(receipt.floor == contract.floor and
                (not receipt.strict or contract.strict),
                "receipt floor/strictness disagrees with pinned contract")

    for original in (inventory.k4, *external_ids(inventory)):
        owners = [item for item in receipts
                  if block(inventory, original).edges &
                     induced_edges(inventory.graph.edges, item.vertices)]
        require(len(owners) == 1,
                "original positive block has zero or multiple final owners")

    generic_away = sum(item.floor == -1 for item in away)
    require(generic_away <= 1,
            "more than one first-bridge away component is potentially negative")
    if generic_away:
        require(plan.profile == "K4+D+T+P",
                "theta-plus-two-triangles has a negative away component")
        negative = next(item for item in away if item.floor == -1)
        require(negative.rank == 1 and
                analyze_piece(inventory, negative.vertices).cycle_lengths == (5,),
                "negative away component is not the singleton pentagon")
    opened_debits = len(opened)
    side_debits = generic_away + opened_debits
    away_positive = len(away) - generic_away
    value = sum(item.floor for item in receipts)

    if len(plan.frontiers) == 3:
        require(not plan.phase1 and plan.anchor_triangle is not None and
                anchor.floor == 3 and opened_debits == 2 and generic_away == 0,
                "three-frontier branch lost direct K4+T/two-side ledger")
        branch = "direct-K4+T-three-frontiers"
    elif generic_away == 1 and len(plan.frontiers) == 2:
        require(plan.anchor_triangle is not None and anchor.floor == 3 and
                opened_debits == 1 and side_debits == 2,
                "P-away/two-frontier branch lost direct K4+T/D/P ledger")
        branch = "direct-K4+T-with-negative-P-away"
    else:
        require(len(plan.frontiers) <= 2 and plan.anchor_triangle is None and
                anchor.floor == 2,
                "small-frontier branch lost rooted K4 anchor")
        if generic_away:
            require(len(plan.frontiers) <= 1,
                    "negative P away permits at most one generic root frontier")
        require(side_debits <= 2,
                "small-frontier branch has more than two generic side debits")
        branch = "rooted-K4-at-most-two-debits"
    require(value >= 0 and anchor.strict,
            "integer ledger is negative or lacks strict anchor")

    # The receipt contracts are graph-specific.  The three universal
    # dependencies below authenticate the residual classification, the packet
    # proof, and the induced-superadditivity step used for every certificate.
    used = frozenset({
        "R321-PACKET-PROOF-v1",
        "R321-RESIDUAL-SIEVE-v1",
        "R321-INDUCED-SUPERADD-v1",
        *(receipt.contract for receipt in receipts),
    })
    require(used <= EXPECTED_CONTRACT_IDS,
            "certificate cites a contract outside the authenticated manifest")
    ledger = Ledger(plan.profile, branch, len(plan.frontiers), anchor.floor,
                    side_debits, away_positive, value, True, receipts,
                    tuple(sorted(used)))
    audit_ledger(inventory, plan, ledger)
    return ledger


def audit_ledger(inventory, plan, ledger):
    anchor = anchor_receipt(inventory, plan)
    opened = tuple(generic_receipt(inventory, "frontier", item.vertices)
                   for item in plan.opened)
    away = tuple(away_receipt(inventory, item.vertices) for item in plan.phase1)
    receipts = (anchor, *opened, *away)
    for receipt in receipts:
        require(receipt.contract in CONTRACTS,
                "replayed receipt cites an unknown analytic contract")
        contract = CONTRACTS[receipt.contract]
        require(receipt.floor == contract.floor and
                (not receipt.strict or contract.strict),
                "replayed receipt disagrees with its pinned contract")
    fresh_debits = sum(item.floor == -1 for item in (*opened, *away))
    fresh_positive = sum(item.floor == 0 for item in away)
    fresh_value = sum(item.floor for item in receipts)
    require(ledger.receipts == receipts, "independent receipt replay disagrees")
    require((ledger.anchor_floor, ledger.side_debits, ledger.away_positive,
             ledger.value, ledger.frontier_count) ==
            (anchor.floor, fresh_debits, fresh_positive, fresh_value,
             len(plan.frontiers)),
            "independent integer ledger replay disagrees")
    require(ledger.value >= 0 and ledger.strict and anchor.strict,
            "replayed ledger does not prove strict positivity")
    fresh_contracts = frozenset({
        "R321-PACKET-PROOF-v1",
        "R321-RESIDUAL-SIEVE-v1",
        "R321-INDUCED-SUPERADD-v1",
        *(receipt.contract for receipt in receipts),
    })
    require(ledger.contracts == tuple(sorted(fresh_contracts)),
            "replayed graph-specific contract set disagrees")
    return True


def verify(vertices, edges):
    # The public gate authenticates immutable contract literals and every pinned
    # source byte on every invocation.  No caller can bypass provenance by
    # importing ``verify`` instead of executing the audit CLI.
    audit_sources()
    inventory = reconstruct(vertices, edges)
    profile, _ = derive_profile(inventory)
    plan = construct_plan(inventory, profile)
    ledger = derive_ledger(inventory, plan)
    return inventory, plan, ledger


# ---------------------------------------------------------------------------
# Independent adjacency fixture generator and finite corroboration.
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
        self.positive = []
        self.routing = []

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

    def cycle(self, length, port=None):
        vertices = ([port] if port is not None else [])
        vertices += [self.fresh(f"C{length}")
                     for _ in range(length - len(vertices))]
        add_cycle(self.edges, vertices)
        result = tuple(vertices)
        self.positive.append((f"C{length}", result))
        return result

    def theta(self, r, port=None):
        require(type(r) is int and r >= 2, "theta fixture requires r>=2")
        x = port if port is not None else self.fresh("DX")
        y = self.fresh("DY")
        a = self.fresh("DA")
        long = [self.fresh("DL") for _ in range(r - 1)]
        self.edges.update({edge(x, y), edge(x, a), edge(a, y)})
        sequence = (x, *long, y)
        self.edges.update(edge(left, right)
                          for left, right in zip(sequence, sequence[1:]))
        result = (x, y, a, *long)
        self.positive.append((f"D{r}", result))
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
            if index == 0 or index % 4 == 0:
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


def fixture(profile, topology, route_length=3, payload_depth=0, theta_r=4):
    require(profile in ("K4+Theta(1,2,r)+T2", "K4+D+T+P"),
            "unknown R321 fixture profile")
    if profile == "K4+D+T+P":
        theta_r = 2
        cycle_lengths = (3, 5)
    else:
        require(theta_r >= 2, "theta residual fixture has r<2")
        cycle_lengths = (3, 3)
    builder = Builder()
    k4 = builder.k4()

    def detached_theta(root, length):
        # Make a theta with a fresh terminal, then bridge to that terminal.
        theta = builder.theta(theta_r)
        builder.bridge_path(root, theta[0], length)
        return theta

    def detached_cycle(root, cycle_length, length):
        current = builder.cycle(cycle_length)
        builder.bridge_path(root, current[0], length)
        return current

    if topology == "direct-three":
        theta = builder.theta(theta_r, k4[0])
        triangle = builder.cycle(cycle_lengths[0], k4[1])
        builder.cycle(cycle_lengths[1], k4[2])

    elif topology == "common-cut":
        theta = builder.theta(theta_r, k4[0])
        triangle = builder.cycle(cycle_lengths[0], k4[0])
        builder.cycle(cycle_lengths[1], k4[0])

    elif topology == "nested-behind-theta":
        theta = builder.theta(theta_r, k4[0])
        triangle = builder.cycle(cycle_lengths[0], theta[1])
        builder.cycle(cycle_lengths[1], k4[1])

    elif topology == "nested-all":
        theta = builder.theta(theta_r, k4[0])
        triangle = builder.cycle(cycle_lengths[0], theta[1])
        builder.cycle(cycle_lengths[1], triangle[1])

    elif topology == "triangle-bridge-two-fronts":
        triangle = detached_cycle(k4[0], cycle_lengths[0], route_length)
        theta = builder.theta(theta_r, k4[1])
        builder.cycle(cycle_lengths[1], k4[2])

    elif topology == "theta-bridge-cycle-front":
        theta = detached_theta(k4[0], route_length)
        triangle = builder.cycle(cycle_lengths[0], k4[1])
        builder.cycle(cycle_lengths[1], triangle[1])

    elif topology == "shared-bridge-prefix":
        # Mandatory countertopology to the rejected minimal-demand dichotomy:
        # all three externals share one rootmost physical bridge, then become
        # incomparable at the downstream cut.  The complete away side owns all
        # three blocks and must be classified by recomputed rank four.
        hub = builder.fresh("HUB")
        builder.bridge_path(k4[0], hub, route_length)
        theta = builder.theta(theta_r, hub)
        triangle = builder.cycle(cycle_lengths[0], hub)
        builder.cycle(cycle_lengths[1], hub)

    elif topology == "pentagon-away-DT-root":
        require(profile == "K4+D+T+P",
                "pentagon-away topology only belongs to D+T+P")
        theta = builder.theta(theta_r, k4[0])
        triangle = builder.cycle(3, k4[1])
        detached_cycle(k4[2], 5, route_length)

    elif topology == "all-one-away":
        theta = detached_theta(k4[0], route_length)
        triangle = builder.cycle(cycle_lengths[0], theta[1])
        builder.cycle(cycle_lengths[1], triangle[1])

    elif topology == "two-away-one-root":
        theta = detached_theta(k4[0], route_length)
        triangle = detached_cycle(k4[1], cycle_lengths[0], route_length + 1)
        builder.cycle(cycle_lengths[1], k4[2])

    elif topology == "three-away":
        theta = detached_theta(k4[0], route_length)
        triangle = detached_cycle(k4[1], cycle_lengths[0], route_length + 1)
        detached_cycle(k4[2], cycle_lengths[1], route_length + 2)

    elif topology == "away-nontriangle-with-triangle":
        # The first bridge group is generic rank>=3 but contains the guaranteed
        # triangle; it is not claimed positive by the narrow triangle contract.
        theta = detached_theta(k4[0], route_length)
        triangle = builder.cycle(cycle_lengths[0], theta[1])
        builder.cycle(cycle_lengths[1], k4[1])

    elif topology == "bridge-below-root-frontier":
        theta = builder.theta(theta_r, k4[0])
        triangle = detached_cycle(theta[1], cycle_lengths[0], route_length)
        builder.cycle(cycle_lengths[1], k4[1])

    else:
        raise VerifyError("unknown generated R321 topology")

    if payload_depth:
        builder.tree_payload(k4[3], payload_depth)
        for index, positive_block in enumerate(tuple(builder.positive)[1:]):
            vertices = positive_block[1]
            builder.tree_payload(vertices[-1], min(payload_depth, index + 2))
        for index, current in enumerate(tuple(builder.routing)[:4]):
            builder.tree_payload(current, min(payload_depth, index + 1))
    return builder.graph()


def theta_entry_fixture(profile, r, entry_orbit, payload_depth=0):
    """Attach K4 to a chosen actual articulation of a maximal theta.

    ``entry_orbit`` is endpoint, short-arm internal, or long-arm internal.
    The chosen vertex is identified with one K4 vertex, so the full-graph
    articulation is recovered from adjacency rather than supplied as metadata.
    """
    require(profile in ("K4+Theta(1,2,r)+T2", "K4+D+T+P"),
            "unknown theta-entry fixture profile")
    require(type(r) is int and r >= 2, "theta-entry fixture requires r>=2")
    require(entry_orbit in ("endpoint", "short-internal", "long-internal"),
            "unknown theta-entry orbit")
    if profile == "K4+D+T+P":
        require(r == 2, "D+T+P theta-entry fixture requires the diamond")
        cycle_lengths = (3, 5)
    else:
        cycle_lengths = (3, 3)

    builder = Builder()
    k4 = builder.k4()
    x = builder.fresh("EX")
    y = builder.fresh("EY")
    short = builder.fresh("ES")
    long = [builder.fresh("EL") for _ in range(r - 1)]
    builder.edges.update({edge(x, y), edge(x, short), edge(short, y)})
    sequence = (x, *long, y)
    builder.edges.update(edge(left, right)
                         for left, right in zip(sequence, sequence[1:]))
    if entry_orbit == "endpoint":
        entry = x
    elif entry_orbit == "short-internal":
        entry = short
    else:
        # For r>2 this is a degree-two internal long-arm vertex; for the
        # diamond it is the other nonterminal orbit.  Identification with K4
        # makes it an actual full-graph articulation without changing its
        # degree inside the maximal theta block.
        entry = long[len(long) // 2]
    mapping = {entry: k4[0]}
    remapped = set()
    for current in builder.edges:
        left, right = tuple(current)
        remapped.add(edge(mapping.get(left, left), mapping.get(right, right)))
    builder.edges = remapped
    builder.vertices.discard(entry)
    builder.cycle(cycle_lengths[0], k4[1])
    builder.cycle(cycle_lengths[1], k4[2])
    if payload_depth:
        builder.tree_payload(k4[3], payload_depth)
        builder.tree_payload(mapping.get(y, y), max(1, payload_depth // 2))
    return builder.graph()


def theta_entry_orbit_audit():
    cases = (
        ("K4+D+T+P", 2, "endpoint"),
        ("K4+D+T+P", 2, "short-internal"),
        ("K4+D+T+P", 2, "long-internal"),
        ("K4+Theta(1,2,r)+T2", 3, "endpoint"),
        ("K4+Theta(1,2,r)+T2", 3, "short-internal"),
        ("K4+Theta(1,2,r)+T2", 3, "long-internal"),
        ("K4+Theta(1,2,r)+T2", 7, "endpoint"),
        ("K4+Theta(1,2,r)+T2", 7, "short-internal"),
        ("K4+Theta(1,2,r)+T2", 7, "long-internal"),
    )
    residual_ranks = set()
    for index, (profile, r, orbit) in enumerate(cases):
        graph = theta_entry_fixture(profile, r, orbit, payload_depth=5)
        inventory, plan, ledger = verify(*graph)
        theta = theta_ids(inventory)[0]
        require(theta in plan.frontiers,
                "theta entry-orbit fixture did not expose theta frontier")
        opened = tuple(item for item in plan.opened
                       if item.boundary_block == theta)
        require(len(opened) == 1,
                "theta entry-orbit fixture did not open theta exactly once")
        item = opened[0]
        require(item.upstream_cut == upstream_cut(inventory, theta) and
                item.upstream_cut in inventory.cuts,
                "theta entry was not reconstructed as its actual articulation")
        require(item.vertices == boundary_open(inventory, plan.root_vertices,
                                               theta, item.upstream_cut),
                "theta entry-orbit opening failed operation replay")
        receipt = tuple(current for current in ledger.receipts
                        if current.phase == "frontier" and
                        current.vertices == item.vertices)
        require(len(receipt) == 1 and
                receipt[0].category == "connected-generic-floor" and
                receipt[0].contract == "R321-CONNECTED-FLOOR-v1",
                "theta residual side received a topology-specific claim")
        residual_ranks.add(receipt[0].rank)
        relabeled = opaque_relabel(*graph, salt=409 + 13 * index)
        _, relabeled_plan, relabeled_ledger = verify(*relabeled)
        require(semantic_signature(plan, ledger) ==
                semantic_signature(relabeled_plan, relabeled_ledger),
                "theta entry-orbit relabel changed semantic certificate")
    require(residual_ranks == {0, 1},
            "theta entry-orbit suite missed tree/cycle residual sides")
    return len(cases), len(cases), tuple(sorted(residual_ranks))


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
    # Positive IDs are Tarjan-local and intentionally excluded from relabel
    # comparison; category/rank/floor is the semantic content.
    pieces = tuple(sorted((item.phase, item.category, item.rank, item.floor)
                          for item in ledger.receipts))
    return (plan.profile, len(plan.phase1), len(plan.root_external),
            len(plan.frontiers), plan.anchor_triangle is not None,
            ledger.branch, ledger.anchor_floor, ledger.side_debits,
            ledger.away_positive, ledger.value, pieces, ledger.contracts)


def expansion_signature(plan, ledger):
    return (plan.profile, len(plan.phase1), len(plan.root_external),
            len(plan.frontiers), plan.anchor_triangle is not None,
            ledger.branch, ledger.anchor_floor, ledger.side_debits,
            ledger.away_positive, ledger.value,
            tuple(sorted((item.phase, item.category, item.rank, item.floor)
                         for item in ledger.receipts)))


@dataclass(frozen=True)
class AuditResult:
    generated: int
    relabeled: int
    profiles: tuple[tuple[str, int], ...]
    branches: tuple[tuple[str, int], ...]
    categories: tuple[tuple[str, int], ...]
    expansion_cases: int
    theta_entry_cases: int
    theta_entry_relabels: int
    theta_residual_ranks: tuple[int, ...]
    shared_first_bridge_cases: int
    hostile_rejections: tuple[str, ...]
    rewires_distinguished: int
    source_files: int


def shared_first_bridge_audit():
    profiles = (("K4+Theta(1,2,r)+T2", 6), ("K4+D+T+P", 2))
    checked = 0
    for index, (profile, theta_r) in enumerate(profiles):
        graph = fixture(profile, "shared-bridge-prefix", route_length=9,
                        payload_depth=7, theta_r=theta_r)
        inventory, plan, ledger = verify(*graph)
        require(len(plan.phase1) == 1 and not plan.root_external and
                not plan.frontiers,
                "shared-prefix countertopology was not split before frontier analysis")
        side = plan.phase1[0]
        analysis = analyze_piece(inventory, side.vertices)
        require(analysis.rank == 4 and
                set(analysis.positive_ids) == set(external_ids(inventory)),
                "shared-prefix away component does not own all externals at rank four")
        receipt = tuple(item for item in ledger.receipts
                        if item.phase == "phase1")
        require(len(receipt) == 1 and receipt[0].rank == 4 and
                receipt[0].category == "rank>=2-away-nonnegative" and
                receipt[0].contract == "R321-CONNECTED-RANK4-v1",
                "shared-prefix rank-four side received wrong analytic contract")
        relabeled = opaque_relabel(*graph, salt=701 + index)
        _, relabeled_plan, relabeled_ledger = verify(*relabeled)
        require(semantic_signature(plan, ledger) ==
                semantic_signature(relabeled_plan, relabeled_ledger),
                "shared-prefix countertopology changed under opaque relabel")
        checked += 1
    return checked


def expansion_audit():
    signatures = set()
    sizes = []
    for length, payload in ((1, 0), (2, 4), (9, 11), (41, 19)):
        vertices, edges = fixture("K4+D+T+P", "triangle-bridge-two-fronts",
                                  route_length=length, payload_depth=payload)
        _, plan, ledger = verify(vertices, edges)
        signatures.add(expansion_signature(plan, ledger))
        sizes.append(len(vertices))
    require(len(signatures) == 1 and sizes == sorted(sizes),
            "K2/tree expansion changed the semantic R321 ledger")
    vertices, edges = fixture("K4+Theta(1,2,r)+T2", "all-one-away",
                              route_length=1401, payload_depth=0, theta_r=9)
    _, plan, ledger = verify(vertices, edges)
    require(plan.phase1 and ledger.value >= 0,
            "very-long connector was not verified")
    return 5


def hostile_tests():
    rejected = []
    base_vertices, base_edges = fixture("K4+D+T+P", "direct-three",
                                        payload_depth=7)
    inventory, base_plan, base_ledger = verify(base_vertices, base_edges)
    k4 = block(inventory, inventory.k4)
    theta = block(inventory, theta_ids(inventory)[0])
    pentagon = next(block(inventory, index) for index in inventory.cycles
                    if block(inventory, index).cycle_length == 5)

    # Subdivide K4: rank preserved, literal root destroyed.
    kedge = next(iter(k4.edges))
    left, right = tuple(kedge)
    new = ("hostile", "subdivide-k4")
    vertices = frozenset(set(base_vertices) | {new})
    edges = set(base_edges) - {kedge}
    edges |= {edge(left, new), edge(new, right)}
    rejected.append(expect_rejection(
        lambda: verify(vertices, frozenset(edges)), "subdivided literal K4",
        "unsupported positive-rank block type"))

    # Chord the pentagon and merge unsupported block structure.
    chord = next(edge(left, right)
                 for left, right in itertools.combinations(pentagon.vertices, 2)
                 if edge(left, right) not in base_edges)
    rejected.append(expect_rejection(
        lambda: verify(base_vertices, frozenset(set(base_edges) | {chord})),
        "chorded residual cycle", "input graph does not have cyclomatic rank seven"))

    # Remove theta's unit arm: no longer Theta(1,2,r).
    x, y = tuple(v for v in theta.vertices
                 if sum(v in current for current in theta.edges) == 3)
    rejected.append(expect_rejection(
        lambda: verify(base_vertices, frozenset(set(base_edges) - {edge(x, y)})),
        "theta unit-arm deletion", "input graph does not have cyclomatic rank seven"))

    # Add a cross ear between K4 and theta private vertices.
    kprivate = next(iter(k4.vertices - theta.vertices))
    dprivate = next(iter(theta.vertices - k4.vertices))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices,
                       frozenset(set(base_edges) | {edge(kprivate, dprivate)})),
        "cross-block ear merger", "input graph does not have cyclomatic rank seven"))

    payload_edge = next(current for current in base_edges
                        if any(isinstance(vertex, tuple) and vertex[0] == "P"
                               for vertex in current))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices, frozenset(set(base_edges) - {payload_edge})),
        "omitted rooted payload edge", "input graph disconnected"))
    rejected.append(expect_rejection(
        lambda: verify(set(base_vertices), base_edges),
        "mutable vertex-set API injection", "vertices must be a nonempty frozenset"))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices,
                       frozenset(set(base_edges) | {frozenset({kprivate})})),
        "malformed loop edge", "malformed unordered edge"))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices,
                       frozenset(set(base_edges) |
                                 {frozenset({kprivate, ("outside", 1)})})),
        "foreign endpoint", "edge endpoint outside vertex set"))

    # Wrong residual profiles.
    # Build K4+Theta(1,2,4)+T+C5 directly: inventory valid, residual invalid.
    builder = Builder(); roots = builder.k4(); builder.theta(4, roots[0]);
    builder.cycle(3, roots[1]); builder.cycle(5, roots[2])
    rejected.append(expect_rejection(lambda: verify(*builder.graph()),
                                     "C5 row with non-diamond theta",
                                     "adjacency-derived profile is not an exact R321 residual"))
    # Build K4+D+C5+C5: no guaranteed triangle.
    builder = Builder(); roots = builder.k4(); builder.theta(2, roots[0]);
    builder.cycle(5, roots[1]); builder.cycle(5, roots[2])
    rejected.append(expect_rejection(lambda: verify(*builder.graph()),
                                     "R321 profile without triangle",
                                     "adjacency-derived profile is not an exact R321 residual"))
    # Unsupported rank-two block Theta(2,2,2), no unit edge.
    builder = Builder(); roots = builder.k4()
    x = roots[0]; y = builder.fresh("UY")
    for tag in range(3):
        a = builder.fresh(f"UA{tag}")
        builder.edges |= {edge(x, a), edge(a, y)}
    builder.cycle(3, roots[1]); builder.cycle(3, roots[2])
    rejected.append(expect_rejection(lambda: verify(*builder.graph()),
                                     "unsupported Theta(2,2,2) block",
                                     "theta lacks its literal length-one arm"))

    # Fixed contract and source-byte mutations.
    contract_id = "R321-K4-T-SHARED-v1"
    original = CONTRACTS[contract_id]
    CONTRACTS[contract_id] = replace(original, floor=99)
    try:
        rejected.append(expect_rejection(audit_contract_table,
                                         "analytic threshold-table mutation",
                                         "analytic contract tuple/lookup disagree"))
    finally:
        CONTRACTS[contract_id] = original
    source_contract_id = "R321-CONNECTED-RANK4-v1"
    source_original = CONTRACTS[source_contract_id]
    CONTRACTS[source_contract_id] = replace(
        source_original, source="all-tricyclic-graphs/paper.tex")
    try:
        rejected.append(expect_rejection(
            audit_contract_table, "analytic source-path table mutation",
            "analytic contract tuple/lookup disagree"))
    finally:
        CONTRACTS[source_contract_id] = source_original
    CONTRACTS[source_contract_id] = replace(
        source_original, sha256="0" * 64)
    try:
        rejected.append(expect_rejection(
            audit_contract_table, "analytic source-digest table mutation",
            "analytic contract tuple/lookup disagree"))
    finally:
        CONTRACTS[source_contract_id] = source_original
    source_contract = CONTRACTS["R321-RESIDUAL-SIEVE-v1"]
    blob = (SOURCE_ROOT / source_contract.source).read_bytes()
    rejected.append(expect_rejection(
        lambda: authenticate_source_blob(blob + b"\nHOSTILE",
                                         source_contract.sha256,
                                         "synthetic source mutation"),
        "analytic source-byte mutation", "analytic source changed"))

    # The production API itself must authenticate the source root and mutable
    # in-memory contract table; calling verify() may not bypass provenance.
    source_root_original = globals()["SOURCE_ROOT"]
    globals()["SOURCE_ROOT"] = source_root_original / "definitely-absent-r321-sources"
    try:
        rejected.append(expect_rejection(
            lambda: verify(base_vertices, base_edges),
            "public API missing source root",
            "analytic source authentication failed: repository absent"))
    finally:
        globals()["SOURCE_ROOT"] = source_root_original
    CONTRACTS[source_contract_id] = replace(
        source_original, source="all-tricyclic-graphs/paper.tex")
    try:
        rejected.append(expect_rejection(
            lambda: verify(base_vertices, base_edges),
            "public API source-path mutation", "analytic contract tuple/lookup disagree"))
    finally:
        CONTRACTS[source_contract_id] = source_original
    CONTRACTS[source_contract_id] = replace(source_original, sha256="0" * 64)
    try:
        rejected.append(expect_rejection(
            lambda: verify(base_vertices, base_edges),
            "public API source-digest mutation", "analytic contract tuple/lookup disagree"))
    finally:
        CONTRACTS[source_contract_id] = source_original
    CONTRACTS[source_contract_id] = replace(source_original, floor=99)
    try:
        rejected.append(expect_rejection(
            lambda: verify(base_vertices, base_edges),
            "public API contract-floor mutation", "analytic contract tuple/lookup disagree"))
    finally:
        CONTRACTS[source_contract_id] = source_original

    # Simultaneously rebinding both mutable runtime views must not bypass the
    # independent full-record digest, even when the changed contract is unused
    # by this graph-specific receipt set and all source path/hash rows survive.
    specs_original = globals()["CONTRACT_SPECS"]
    lookup_original = globals()["CONTRACTS"]
    unused_id = "R321-CONNECTED-RANK4-v1"
    unused_original = dict(specs_original)[unused_id]
    def rebound_specs(replacement):
        return tuple((name, replacement if name == unused_id else item)
                     for name, item in specs_original)
    for label, replacement, expected in (
            ("simultaneous unused-floor rebind",
             replace(unused_original, floor=99),
             "analytic full contract manifest changed"),
            ("simultaneous unused-claim rebind",
             replace(unused_original,
                     claim="HOSTILE altered unused analytic claim"),
             "analytic full contract manifest changed"),
            ("simultaneous unused-strict rebind",
             replace(unused_original, strict=True),
             "analytic full contract manifest changed"),
            ("simultaneous boolean-floor type rebind",
             replace(unused_original, floor=True),
             "contract floor malformed")):
        mutated_specs = rebound_specs(replacement)
        globals()["CONTRACT_SPECS"] = mutated_specs
        globals()["CONTRACTS"] = dict(mutated_specs)
        try:
            rejected.append(expect_rejection(
                lambda: verify(base_vertices, base_edges), label, expected))
        finally:
            globals()["CONTRACT_SPECS"] = specs_original
            globals()["CONTRACTS"] = lookup_original

    # Authenticate the companion universal proof through the production API,
    # not merely through the standalone digest helper.  Build a complete tiny
    # source mirror so the test reaches the note row specifically.
    note_contract = CONTRACTS["R321-PACKET-PROOF-v1"]
    with tempfile.TemporaryDirectory(prefix="r321-source-mirror-") as temporary:
        mirror = Path(temporary)
        for source, _ in EXPECTED_SOURCE_ROWS:
            source_path = SOURCE_ROOT / source
            target_path = mirror / source
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)
        note_path = mirror / note_contract.source
        note_path.unlink()
        globals()["SOURCE_ROOT"] = mirror
        try:
            rejected.append(expect_rejection(
                lambda: verify(base_vertices, base_edges),
                "public API missing companion proof note",
                "analytic source authentication failed: missing R321-PACKET-PROOF-v1"))
        finally:
            globals()["SOURCE_ROOT"] = source_root_original
        shutil.copyfile(source_root_original / note_contract.source, note_path)
        note_path.write_bytes(note_path.read_bytes() + b"\nHOSTILE NOTE MUTATION\n")
        globals()["SOURCE_ROOT"] = mirror
        try:
            rejected.append(expect_rejection(
                lambda: verify(base_vertices, base_edges),
                "public API mutated companion proof note",
                "analytic source changed: R321-PACKET-PROOF-v1"))
        finally:
            globals()["SOURCE_ROOT"] = source_root_original

    # Unexpected implementation exceptions are never counted as hostile PASS.
    original_reconstruct = globals()["reconstruct"]
    def unrelated_crash(*_args, **_kwargs):
        raise KeyError("unrelated crash")
    globals()["reconstruct"] = unrelated_crash
    try:
        try:
            expect_rejection(lambda: verify(base_vertices, base_edges),
                             "unrelated implementation crash", "unrelated crash")
        except KeyError as error:
            require(str(error) == "'unrelated crash'",
                    "unrelated implementation exception changed")
        else:
            raise VerifyError("hostile harness masked an unrelated KeyError")
    finally:
        globals()["reconstruct"] = original_reconstruct

    # Forged plan/ledger fields are independently replayed.
    rejected.append(expect_rejection(
        lambda: audit_plan(inventory, replace(base_plan, frontiers=())),
        "forged frontier set", "stored frontier set changed"))
    bridge_inventory, bridge_cut_plan, _ = verify(*fixture(
        "K4+D+T+P", "shared-bridge-prefix", route_length=5))
    genuine_side = bridge_cut_plan.phase1[0]
    fake_edge = next(current for current in bridge_inventory.graph.edges
                     if current != genuine_side.deleted_edge)
    forged_side = replace(genuine_side, deleted_edge=fake_edge)
    rejected.append(expect_rejection(
        lambda: audit_plan(bridge_inventory,
                           replace(bridge_cut_plan, phase1=(forged_side,))),
        "forged selected physical bridge edge",
        "stored first-bridge edge is not the exact physical K2 edge"))
    rejected.append(expect_rejection(
        lambda: audit_ledger(inventory, base_plan,
                             replace(base_ledger, value=99)),
        "forged ledger value", "independent integer ledger replay disagrees"))

    # Same exact profile, direct vs bridge/nested routing must be distinguished.
    _, direct_plan, direct_ledger = verify(*fixture("K4+D+T+P", "direct-three"))
    _, bridge_plan, bridge_ledger = verify(*fixture(
        "K4+D+T+P", "triangle-bridge-two-fronts", route_length=8))
    require(semantic_signature(direct_plan, direct_ledger) !=
            semantic_signature(bridge_plan, bridge_ledger),
            "same-profile direct/bridge rewire was not distinguished")
    return tuple(rejected), 1


def audit():
    source_files = audit_sources()
    cases = (
        ("K4+Theta(1,2,r)+T2", "direct-three", 3, 0, 2),
        ("K4+Theta(1,2,r)+T2", "common-cut", 3, 5, 3),
        ("K4+Theta(1,2,r)+T2", "nested-behind-theta", 3, 4, 4),
        ("K4+Theta(1,2,r)+T2", "nested-all", 3, 6, 7),
        ("K4+Theta(1,2,r)+T2", "triangle-bridge-two-fronts", 8, 5, 5),
        ("K4+Theta(1,2,r)+T2", "theta-bridge-cycle-front", 7, 3, 6),
        ("K4+Theta(1,2,r)+T2", "all-one-away", 9, 6, 8),
        ("K4+Theta(1,2,r)+T2", "shared-bridge-prefix", 7, 5, 6),
        ("K4+Theta(1,2,r)+T2", "two-away-one-root", 10, 4, 9),
        ("K4+Theta(1,2,r)+T2", "three-away", 11, 5, 10),
        ("K4+Theta(1,2,r)+T2", "away-nontriangle-with-triangle", 6, 3, 4),
        ("K4+Theta(1,2,r)+T2", "bridge-below-root-frontier", 5, 4, 3),
        ("K4+D+T+P", "direct-three", 3, 0, 2),
        ("K4+D+T+P", "common-cut", 3, 6, 2),
        ("K4+D+T+P", "nested-behind-theta", 3, 5, 2),
        ("K4+D+T+P", "nested-all", 3, 7, 2),
        ("K4+D+T+P", "triangle-bridge-two-fronts", 12, 6, 2),
        ("K4+D+T+P", "theta-bridge-cycle-front", 8, 4, 2),
        ("K4+D+T+P", "all-one-away", 10, 5, 2),
        ("K4+D+T+P", "shared-bridge-prefix", 8, 5, 2),
        ("K4+D+T+P", "pentagon-away-DT-root", 9, 6, 2),
        ("K4+D+T+P", "two-away-one-root", 11, 7, 2),
        ("K4+D+T+P", "three-away", 13, 6, 2),
        ("K4+D+T+P", "away-nontriangle-with-triangle", 9, 5, 2),
        ("K4+D+T+P", "bridge-below-root-frontier", 7, 4, 2),
    )
    profiles = Counter(); branches = Counter(); categories = Counter()
    generated = relabeled = 0
    for index, (profile, topology, route_length, payload, theta_r) in enumerate(cases):
        graph = fixture(profile, topology, route_length, payload, theta_r)
        inventory, plan, ledger = verify(*graph)
        require(plan.profile == profile and ledger.profile == profile,
                "generated R321 profile misclassified")
        require(tuple(sorted(block(inventory, i).rank
                             for i in (inventory.k4, *external_ids(inventory)))) ==
                (1, 1, 2, 3), "generated block-rank inventory changed")
        profiles[profile] += 1
        branches[ledger.branch] += 1
        categories.update(item.category for item in ledger.receipts)
        generated += 1
        relabeled_graph = opaque_relabel(*graph, salt=31 + 17 * index)
        _, relabeled_plan, relabeled_ledger = verify(*relabeled_graph)
        require(semantic_signature(plan, ledger) ==
                semantic_signature(relabeled_plan, relabeled_ledger),
                "opaque relabeling changed semantic certificate")
        relabeled += 1
    require(set(profiles) == {"K4+Theta(1,2,r)+T2", "K4+D+T+P"},
            "R321 profile coverage incomplete")
    require({"rooted-K4-at-most-two-debits",
             "direct-K4+T-three-frontiers",
             "direct-K4+T-with-negative-P-away"} <= set(branches),
            "R321 branch coverage incomplete")
    require({"strict-rooted-K4", "strict-shared-K4+T",
             "connected-generic-floor", "intact-triangle-away-positive"}
            <= set(categories), "R321 piece category coverage incomplete")
    expansion_cases = expansion_audit()
    theta_cases, theta_relabels, theta_ranks = theta_entry_orbit_audit()
    shared_cases = shared_first_bridge_audit()
    rejected, rewires = hostile_tests()
    return AuditResult(generated, relabeled, tuple(sorted(profiles.items())),
                       tuple(sorted(branches.items())),
                       tuple(sorted(categories.items())), expansion_cases,
                       theta_cases, theta_relabels, theta_ranks,
                       shared_cases, rejected, rewires, source_files)


def report(result):
    return "\n".join((
        "R321 adjacency semantic verifier: finite corroboration passed",
        "scope: complete physical R321 only; no global/multiblock/single-block claim",
        "proof boundary: universal theorem is in the companion packet note; this program is finite corroboration plus a public adjacency gate",
        "input: finite simple adjacency only; no supplied profile, topology, owner, frontier, charge, threshold, or partition",
        "reconstruction: iterative Tarjan; literal K4 + Theta(1,2,r) + two literal cycles; full block-cut tree including every K2",
        "ownership: original vertices; simultaneous first bridges; grouped ancestor-minimal external frontiers; induced connected disjoint exhaustive replay",
        "ledger: rank>=2 first-bridge away sides are nonnegative; only singleton P may debit; rooted K4 >2 or direct shared-cut K4+C3 >3 pays remaining floors",
        f"analytic source files pinned: {result.source_files}; source manifest sha256: {source_manifest_digest()}",
        f"authenticated contract records: {len(EXPECTED_CONTRACT_IDS)}; full manifest sha256: {full_contract_manifest_digest()}",
        f"generated adjacency fixtures: {result.generated}; opaque relabel replays: {result.relabeled}",
        "profiles: " + repr(dict(result.profiles)),
        "branches: " + repr(dict(result.branches)),
        "piece categories: " + repr(dict(result.categories)),
        f"K2/tree expansion probes (including 1401-edge connector): {result.expansion_cases}",
        f"theta actual-articulation entry orbits: {result.theta_entry_cases}; opaque relabels: {result.theta_entry_relabels}; opened-side ranks: {result.theta_residual_ranks}",
        f"mandatory shared-first-bridge-prefix rank-four cases: {result.shared_first_bridge_cases}",
        f"hostile mutations rejected: {len(result.hostile_rejections)}; same-profile rewires distinguished: {result.rewires_distinguished}",
        "analytic contracts: " + repr(tuple(sorted(EXPECTED_CONTRACT_IDS))),
        "verifier sha256: " + file_digest(Path(__file__)),
        "status: R321 finite corroboration and independent semantic replay passed",
    ))


def main():
    if sys.argv != [sys.argv[0]]:
        print("R321 verifier: command line arguments are not accepted", file=sys.stderr)
        return 2
    print(report(audit()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
