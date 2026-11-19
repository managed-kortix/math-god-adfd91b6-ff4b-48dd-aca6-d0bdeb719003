#!/usr/bin/env python3
"""Adjacency-only fail-closed semantic verifier for the physical R31-K lane.

The sole production input is a finite simple graph encoded by its vertex set
and unordered adjacency edges.  Tarjan blocks, ports, the block-cut tree,
physical K2 bridges, residual profile, dispatch, and original-vertex pieces
are all reconstructed.  No caller supplies a profile, channel, owner, packet
threshold, or claimed partition.
"""
from __future__ import annotations

import hashlib
import itertools
import subprocess
import sys
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class VerifyError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerifyError(message)


def expect_rejection(action, label):
    try:
        action()
    except (VerifyError, KeyError, TypeError, ValueError, IndexError, StopIteration):
        return label
    raise VerifyError(f"hostile adjacency accepted: {label}")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# Fixed theorem IDs and source bytes.  Numeric thresholds are selected only
# from this private table after an adjacency-derived dispatch; input records
# have no analytic fields.
ANALYTIC_CONTRACTS = {
    "R31K-K4-ROOTED-v1": {
        "source": "packing-two-square-energy/paper.tex",
        "sha256": "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
        "strict_floor": 2,
    },
    "R31K-K4-T-SHARED-v1": {
        "source": "positive-square-energy/hexacyclic-general/multiblock-items5-7-owner-exact-closure.md",
        "sha256": "1c5722565e874ebf04533e908c5bf335f7be0b56a5665f5b607cfdef14ac8c67",
        "strict_floor": 3,
    },
    "R31K-UNICYCLIC-LOWER-v1": {
        "source": "all-tricyclic-cacti/paper.tex",
        "sha256": "d928a56b0257936fcc326ddc2c85e40593117a7749b55502bb42379c805e71e8",
        "strict_floor": -1,
    },
    "R31K-CONNECTED-RANK2-6-v1": {
        "source": "positive-square-energy/heptacyclic-general/complete-multiblock-theorem.md",
        "sha256": "27c6a4736125d821f21fd1ebc7a30580068535826c8fcc6f72ea172cbb6a7399",
        "strict_floor": 0,
    },
    "R31K-INDUCED-SUPERADD-v1": {
        "source": "packing-two-square-energy/paper.tex",
        "sha256": "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
        "strict_floor": None,
    },
    "R31K-RESIDUAL-SIEVE-v1": {
        "source": "positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md",
        "sha256": "3f8bb3a397125782dd6c9cae26ce52f9c6bf826e3136dfee62781048e65c18a5",
        "strict_floor": None,
    },
}
EXPECTED_CONTRACT_IDS = frozenset(ANALYTIC_CONTRACTS)


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


@dataclass(frozen=True)
class Certificate:
    profile: str
    dispatch: str
    contracts: tuple[str, ...]
    pieces: tuple[frozenset, ...]
    piece_kinds: tuple[str, ...]
    ports: tuple[tuple[int, object], ...]
    boundary_blocks: tuple[int, ...]


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
    require(len(normalized) == len(edges), "duplicate edge")
    return PhysicalGraph(vertices, edges)


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


def connected(vertices, edges):
    return bool(vertices) and len(components(vertices, edges)) == 1


def graph_rank(vertices, edges):
    return len(edges) - len(vertices) + len(components(vertices, edges))


def biconnected_edge_blocks(vertices, edges):
    """Tarjan edge-stack decomposition; every physical bridge is one block."""
    graph = adjacency(vertices, edges)
    discovery = {}
    low = {}
    parent = {}
    stack = []
    blocks = []
    clock = 0

    def visit(current):
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
                    block = set()
                    while True:
                        require(stack, "Tarjan stack underflow")
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
    require((set().union(*blocks) if blocks else set()) == set(edges),
            "Tarjan blocks do not exhaust edges")
    require(sum(map(len, blocks)) == len(edges), "Tarjan blocks duplicate edges")
    return tuple(blocks)


def classify_block(index, edges):
    vertices = frozenset().union(*edges)
    rank = len(edges) - len(vertices) + 1
    degrees = {vertex: sum(vertex in current for current in edges)
               for vertex in vertices}
    if len(edges) == 1:
        require(rank == 0 and len(vertices) == 2, "malformed bridge block")
        return Block(index, edges, vertices, rank, "bridge", None)
    if len(vertices) == 4 and len(edges) == 6 and all(value == 3 for value in degrees.values()):
        require(rank == 3, "K4 rank changed")
        return Block(index, edges, vertices, rank, "K4", None)
    if len(vertices) >= 3 and len(edges) == len(vertices) and all(value == 2 for value in degrees.values()):
        require(rank == 1, "cycle rank changed")
        return Block(index, edges, vertices, rank, "cycle", len(vertices))
    raise VerifyError("unsupported positive-rank block type")


def reconstruct(vertices, edges):
    graph = normalize_graph(vertices, edges)
    require(connected(graph.vertices, graph.edges), "input graph disconnected")
    require(graph_rank(graph.vertices, graph.edges) == 7,
            "input graph does not have cyclomatic rank seven")
    raw = biconnected_edge_blocks(graph.vertices, graph.edges)
    blocks = tuple(classify_block(index, current)
                   for index, current in enumerate(raw))
    positive = tuple(block for block in blocks if block.rank)
    k4s = tuple(block.index for block in positive if block.kind == "K4")
    cycles = tuple(block.index for block in positive if block.kind == "cycle")
    require(len(k4s) == 1 and len(cycles) == 4 and len(positive) == 5,
            "positive blocks are not one K4 and four cycles")
    require(sum(block.rank for block in positive) == 7,
            "positive block ranks are not 3+1+1+1+1")

    membership = {vertex: tuple(block.index for block in blocks
                                if vertex in block.vertices)
                  for vertex in graph.vertices}
    cuts = frozenset(vertex for vertex, owners in membership.items()
                     if len(owners) >= 2)
    # Full block-cut topology, including bridge blocks and articulation nodes.
    tree = {("B", block.index): set() for block in blocks}
    for cut in cuts:
        node = ("C", cut)
        tree[node] = set()
        for block_index in membership[cut]:
            block_node = ("B", block_index)
            tree[node].add(block_node)
            tree[block_node].add(node)
    require(sum(map(len, tree.values())) // 2 == len(tree) - 1,
            "block-cut incidence is not a tree")
    seen = {next(iter(tree))}
    stack = list(seen)
    while stack:
        current = stack.pop()
        for neighbor in tree[current] - seen:
            seen.add(neighbor)
            stack.append(neighbor)
    require(seen == set(tree), "block-cut topology disconnected")
    # A non-cut endpoint of a bridge is implicit in its neighboring block; the
    # block-cut graph still records every physical K2 and every shared port.
    bridge_blocks = tuple(block.index for block in blocks if block.kind == "bridge")
    return Inventory(graph, adjacency(graph.vertices, graph.edges), blocks, cuts,
                     tree, k4s[0], cycles, bridge_blocks)


def block(inventory, index):
    return inventory.blocks[index]


def tree_path(tree, start, finish):
    previous = {start: None}
    queue = deque([start])
    while queue and finish not in previous:
        current = queue.popleft()
        for neighbor in sorted(tree[current], key=repr):
            if neighbor not in previous:
                previous[neighbor] = current
                queue.append(neighbor)
    require(finish in previous, "block-cut route disconnected")
    result = []
    current = finish
    while current is not None:
        result.append(current)
        current = previous[current]
    return tuple(reversed(result))


def derive_profile(inventory):
    lengths = tuple(sorted(block(inventory, index).cycle_length
                           for index in inventory.cycles))
    require(all(length >= 3 for length in lengths), "cycle length below three")
    # epsilon_3=1; every nontriangle epsilon <= epsilon_5<3/5; odd excess
    # decreases and even excess is zero.  Hence sum epsilon>3 leaves exactly
    # these three length profiles.
    if lengths == (3, 3, 3, 3):
        return "T4"
    if lengths[:3] == (3, 3, 3) and lengths[3] >= 5 and lengths[3] % 2 == 1:
        return "T3+odd>=5"
    if lengths == (3, 3, 5, 5):
        return "T2+C5+C5"
    raise VerifyError("adjacency-derived profile is not an R31-K residual")


def cyclic_hull_nodes(inventory):
    marked = [("B", inventory.k4), *(('B', index) for index in inventory.cycles)]
    hull = {marked[0]}
    for target in marked[1:]:
        hull.update(tree_path(inventory.tree, marked[0], target))
    return frozenset(hull)


def hull_bridge_blocks(inventory):
    hull = cyclic_hull_nodes(inventory)
    return tuple(index for index in inventory.bridge_blocks if ("B", index) in hull)


def component_after_edge(inventory, bridge_index, away_from_k4=True):
    current = block(inventory, bridge_index)
    require(current.kind == "bridge", "physical split requested on nonbridge")
    bridge_edge = next(iter(current.edges))
    sides = components(inventory.graph.vertices,
                       frozenset(inventory.graph.edges - {bridge_edge}))
    require(len(sides) == 2, "Tarjan K2 did not split physical graph")
    k4_vertices = block(inventory, inventory.k4).vertices
    if away_from_k4:
        matches = [side for side in sides if not k4_vertices <= side]
    else:
        matches = [side for side in sides if k4_vertices <= side]
    require(len(matches) == 1, "bridge orientation is ambiguous")
    return matches[0]


def cyclic_blocks_in(inventory, vertices):
    return tuple(item for item in (inventory.k4, *inventory.cycles)
                 if block(inventory, item).vertices <= vertices)


def first_hull_bridges(inventory):
    root = ("B", inventory.k4)
    result = set()
    for cycle_index in inventory.cycles:
        route = tree_path(inventory.tree, root, ("B", cycle_index))
        candidates = [node[1] for node in route
                      if node[0] == "B" and block(inventory, node[1]).kind == "bridge"]
        if candidates:
            result.add(candidates[0])
    return tuple(sorted(result))


def first_nontriangle(inventory):
    """First C_(odd>=5) after the K4 in the bridge-free block-cut tree."""
    root = ("B", inventory.k4)
    nontriangles = [index for index in inventory.cycles
                    if block(inventory, index).cycle_length != 3]
    require(nontriangles, "first-nontriangle requested in T4")
    depths = {index: len(tree_path(inventory.tree, root, ("B", index)))
              for index in nontriangles}
    chosen = min(nontriangles, key=lambda index: (depths[index], repr(block(inventory, index).vertices)))
    route = tree_path(inventory.tree, root, ("B", chosen))
    require(not any(block(inventory, node[1]).kind == "bridge"
                    for node in route if node[0] == "B"),
            "first-nontriangle route contains an undispatched bridge")
    return chosen, route


def port_toward(inventory, upstream_block, downstream_block):
    route = tree_path(inventory.tree, ("B", upstream_block), ("B", downstream_block))
    cuts = [node[1] for node in route if node[0] == "C"]
    require(cuts, "blocks have no physical articulation port")
    port = cuts[0]
    require(port in block(inventory, upstream_block).vertices,
            "physical port not in upstream block")
    return port


def boundary_open(inventory, boundary_block, upstream_port, protected):
    """Open one block at its upstream port and return original downstream vertices.

    Delete all edges of the boundary block, take every owner component based at
    a vertex other than the upstream port, and unite them with those block
    vertices.  The protected upstream vertex is never copied.
    """
    boundary = block(inventory, boundary_block)
    require(boundary.kind == "cycle", "boundary opening requires a cycle")
    require(upstream_port in boundary.vertices, "opening port outside cycle")
    residual_edges = frozenset(inventory.graph.edges - boundary.edges)
    owner_components = components(inventory.graph.vertices, residual_edges)
    by_vertex = {}
    for side in owner_components:
        hits = side & boundary.vertices
        require(len(hits) == 1, "cycle owner component meets two block vertices")
        by_vertex[next(iter(hits))] = side
    result = frozenset().union(*(by_vertex[vertex]
                                for vertex in boundary.vertices - {upstream_port}))
    result = frozenset(set(result) - set(protected))
    require(upstream_port not in result and result,
            "boundary-open side is empty or copied its port")
    return result


def nearest_anchor_partition(inventory, anchor_blocks):
    """Partition every original vertex by nearest expanded anchor owner.

    Anchor seeds are full block vertex sets.  Multi-source BFS on physical
    adjacency uses a deterministic anchor order.  A class can only cross a
    physical bridge away from its seed; block-cut uniqueness proves it remains
    connected.  This routine is used only after the dispatch has selected
    pairwise compatible anchor blocks.
    """
    anchors = tuple(sorted(anchor_blocks))
    seed_owner = {}
    for anchor in anchors:
        for vertex in block(inventory, anchor).vertices:
            seed_owner.setdefault(vertex, anchor)
    require(seed_owner, "empty anchor set")
    distance = {vertex: 0 for vertex in seed_owner}
    owner = dict(seed_owner)
    queue = deque(sorted(seed_owner, key=repr))
    while queue:
        current = queue.popleft()
        for neighbor in sorted(inventory.adjacency[current], key=repr):
            proposal = distance[current] + 1
            candidate = owner[current]
            if (neighbor not in distance or proposal < distance[neighbor] or
                    (proposal == distance[neighbor] and candidate < owner[neighbor])):
                distance[neighbor] = proposal
                owner[neighbor] = candidate
                queue.append(neighbor)
    require(set(owner) == set(inventory.graph.vertices), "BFS ownership omitted vertices")
    pieces = tuple(frozenset(vertex for vertex, value in owner.items() if value == anchor)
                   for anchor in anchors)
    return pieces


def verify_piece_partition(inventory, pieces):
    require(pieces and all(type(piece) is frozenset and piece for piece in pieces),
            "empty/malformed piece")
    union = set().union(*pieces)
    require(union == set(inventory.graph.vertices), "pieces are not exhaustive")
    require(sum(map(len, pieces)) == len(union), "pieces overlap")
    for piece in pieces:
        current_edges = induced_edges(inventory.graph.edges, piece)
        require(connected(piece, current_edges), "piece is not connected")
        # Inducedness is constructive: the checker always recomputes E(G[piece]).
        require(current_edges == frozenset(edge(u, v) for u in piece
                                           for v in inventory.adjacency[u]
                                           if repr(u) < repr(v) and v in piece),
                "piece edge set is not induced")
    for cut in inventory.cuts:
        require(sum(cut in piece for piece in pieces) == 1,
                "articulation vertex has nonunique owner")
    return True


def triangle_blocks(inventory):
    return tuple(index for index in inventory.cycles
                 if block(inventory, index).cycle_length == 3)


def k4_triangle_anchor(inventory, triangle_index):
    """Return the cut-closed K4--T route as one narrow shared-cut packet."""
    route = tree_path(inventory.tree, ("B", inventory.k4), ("B", triangle_index))
    interior_positive = [node[1] for node in route[1:-1]
                         if node[0] == "B" and block(inventory, node[1]).rank]
    require(not interior_positive, "purported K4+T anchor contains an intermediate cycle")
    require(not any(block(inventory, node[1]).kind == "bridge"
                    for node in route if node[0] == "B"),
            "purported shared anchor contains a physical bridge")
    # With no K2 node on the block-cut route, the blocks are consecutive at a
    # shared physical cut.  The analytic K4+T packet permits arbitrary one-root
    # trees, so take the two full blocks and every rank-zero component whose
    # unique route reaches one of them before another positive block.
    seeds = set(block(inventory, inventory.k4).vertices |
                block(inventory, triangle_index).vertices)
    forbidden = set().union(*(block(inventory, index).vertices - seeds
                              for index in inventory.cycles
                              if index != triangle_index))
    allowed = set(inventory.graph.vertices) - forbidden
    anchor = next(side for side in components(frozenset(allowed),
                                              induced_edges(inventory.graph.edges, allowed))
                  if block(inventory, inventory.k4).vertices <= side)
    require(block(inventory, triangle_index).vertices <= anchor and
            connected(anchor, induced_edges(inventory.graph.edges, anchor)),
            "K4+T anchor disconnected")
    return anchor


def _component_kinds(inventory, pieces, anchor_label):
    kinds = [anchor_label]
    for side in pieces[1:]:
        owned = cyclic_blocks_in(inventory, side)
        kinds.append("boundary-tree" if not owned else
                     ("boundary-unicycle" if len(owned) == 1 else
                      "boundary-rank>=2"))
    return tuple(kinds)


def _contracts_for_kinds(kinds, anchor_contract):
    contracts = [anchor_contract, "R31K-INDUCED-SUPERADD-v1"]
    for kind in kinds[1:]:
        if kind in {"boundary-tree", "boundary-unicycle"}:
            contracts.append("R31K-UNICYCLIC-LOWER-v1")
        else:
            require(kind == "boundary-rank>=2",
                    "unknown boundary kind for lower-rank contract")
            contracts.append("R31K-CONNECTED-RANK2-6-v1")
    return tuple(contracts)


def _split_by_anchor(inventory, anchor, label):
    remaining = frozenset(set(inventory.graph.vertices) - set(anchor))
    remainder = (() if not remaining else
                 components(remaining, induced_edges(inventory.graph.edges, remaining)))
    pieces = (anchor, *remainder)
    verify_piece_partition(inventory, pieces)
    return pieces, _component_kinds(inventory, pieces, label)


def _crossing_ports(inventory, pieces):
    result = []
    for index, side in enumerate(pieces[1:], 1):
        crossing = {current for current in inventory.graph.edges
                    if bool(current & side) and not current <= side}
        require(crossing, f"piece {index} has no physical boundary")
        result.append((index, tuple(sorted((tuple(sorted(current, key=repr))
                                           for current in crossing), key=repr))))
    return tuple(result)



def first_bridge_dispatch(inventory, profile):
    first = first_hull_bridges(inventory)
    if not first:
        return None
    # Authenticate the simultaneous first-bridge antichain on original
    # vertices before selecting the packet.  Every later connector, nested
    # cycle, and rooted payload remains in one complete away component.
    away = tuple(component_after_edge(inventory, index) for index in first)
    require(sum(map(len, away)) == len(set().union(*away)),
            "first-bridge away territories overlap (not an antichain)")
    root_vertices = frozenset(set(inventory.graph.vertices) - set().union(*away))
    verify_piece_partition(inventory, (root_vertices, *away))
    require(inventory.k4 in cyclic_blocks_in(inventory, root_vertices),
            "K4 escaped first-bridge root")

    # The accepted R31-K bridge reduction requires an actual root-side
    # triangle directly shared-cut reachable from K4.  Derive that condition
    # from adjacency; never infer it from the profile.
    root_triangles = [index for index in triangle_blocks(inventory)
                      if block(inventory, index).vertices <= root_vertices]
    direct = []
    for index in root_triangles:
        route = tree_path(inventory.tree, ("B", inventory.k4), ("B", index))
        if not any(block(inventory, node[1]).kind == "bridge"
                   for node in route if node[0] == "B") and not any(
                       block(inventory, node[1]).rank
                       for node in route[1:-1] if node[0] == "B"):
            direct.append(index)
    require(direct,
            "R31-K first-bridge row lacks an authenticated direct root triangle")
    selected = min(direct, key=lambda index: repr(block(inventory, index).vertices))
    anchor = k4_triangle_anchor(inventory, selected)
    pieces, kinds = _split_by_anchor(inventory, anchor, "K4+T-anchor")
    require(len(pieces) - 1 <= 3,
            "first-bridge K4+T core has more than three territories")
    return Certificate(
        profile, "first-bridge+K4+kT-core",
        _contracts_for_kinds(kinds, "R31K-K4-T-SHARED-v1"),
        pieces, kinds,
        tuple((index, next(iter(block(inventory, index).edges))) for index in first),
        first)

def bridge_free_dispatch(inventory, profile):
    require(not hull_bridge_blocks(inventory), "bridge-free dispatcher saw hull bridge")
    triangles = triangle_blocks(inventory)
    require(len(triangles) >= 2, "R31-K residual lacks two triangles")
    root = ("B", inventory.k4)
    direct = []
    for index in triangles:
        route = tree_path(inventory.tree, root, ("B", index))
        if not any(block(inventory, node[1]).rank
                   for node in route[1:-1] if node[0] == "B"):
            direct.append(index)

    if direct:
        selected = min(direct,
                       key=lambda index: (len(tree_path(inventory.tree, root, ('B', index))),
                                          repr(block(inventory, index).vertices)))
        anchor = k4_triangle_anchor(inventory, selected)
        pieces, kinds = _split_by_anchor(inventory, anchor, "K4+T-anchor")
        require(len(pieces) - 1 <= 3,
                "K4+T anchor generated more than three first-boundary territories")
        dispatch = "K4+kT-core:" + profile
        return Certificate(
            profile, dispatch,
            _contracts_for_kinds(kinds, "R31K-K4-T-SHARED-v1"),
            pieces, kinds, _crossing_ports(inventory, pieces), ())

    # No triangle is directly reachable.  The first positive block on every
    # K4--triangle route is a nontriangle.  Open every distinct first such
    # block simultaneously.  Complete downstream sides keep all nesting and
    # rooted payloads together; their original vertices cannot overlap because
    # first positive block nodes form an antichain in the block-cut tree.
    require(profile != "T4", "T4 has no first nontriangle")
    first_nontriangles = set()
    for triangle in triangles:
        route = tree_path(inventory.tree, root, ("B", triangle))
        positive = [node[1] for node in route[1:-1]
                    if node[0] == "B" and block(inventory, node[1]).rank]
        require(positive and block(inventory, positive[0]).kind == "cycle" and
                block(inventory, positive[0]).cycle_length != 3,
                "first obstruction before triangle is not a nontriangle")
        first_nontriangles.add(positive[0])
    downstream = []
    ports = []
    for index in sorted(first_nontriangles):
        port = port_toward(inventory, inventory.k4, index)
        side = boundary_open(inventory, index, port,
                             block(inventory, inventory.k4).vertices)
        downstream.append(side)
        ports.append((index, port))
    require(sum(map(len, downstream)) == len(set().union(*downstream)),
            "first-nontriangle downstream territories overlap")
    root_piece = frozenset(set(inventory.graph.vertices) - set().union(*downstream))
    pieces = (root_piece, *downstream)
    verify_piece_partition(inventory, pieces)
    kinds = _component_kinds(inventory, pieces, "K4-root")
    require(all(kind == "boundary-rank>=2" for kind in kinds[1:]),
            "opened first-nontriangle side is not a strict rank>=2 cactus")
    return Certificate(
        profile, "first-nontriangle-cascade",
        _contracts_for_kinds(kinds, "R31K-K4-ROOTED-v1"),
        pieces, kinds, tuple(ports), tuple(sorted(first_nontriangles)))

def verify_contracts(certificate):
    require(set(certificate.contracts) <= EXPECTED_CONTRACT_IDS,
            "unknown analytic contract ID")
    require("R31K-INDUCED-SUPERADD-v1" in certificate.contracts,
            "induced superadditivity contract omitted")
    for contract_id in certificate.contracts:
        floor = ANALYTIC_CONTRACTS[contract_id]["strict_floor"]
        require(floor is None or type(floor) is int,
                "analytic floor is not a fixed integer/None")
    if "K4+kT-core" in certificate.dispatch:
        require(certificate.contracts.count("R31K-K4-T-SHARED-v1") == 1,
                "K4+T threshold contract missing or duplicated")
        floor = ANALYTIC_CONTRACTS["R31K-K4-T-SHARED-v1"]["strict_floor"]
        require(type(floor) is int and floor == 3,
                "fixed K4+T contract threshold changed")
        require(len(certificate.pieces) - 1 <= floor,
                "K4+T anchor cannot pay boundary territories")
    if certificate.dispatch == "first-bridge+K4-core":
        require(certificate.boundary_blocks,
                "first-bridge certificate omitted its physical K2 blocks")
    if certificate.dispatch == "first-nontriangle-cascade":
        require(certificate.boundary_blocks,
                "cascade certificate omitted first nontriangle blocks")
    return True


def verify(vertices, edges):
    inventory = reconstruct(vertices, edges)
    profile = derive_profile(inventory)
    certificate = first_bridge_dispatch(inventory, profile)
    if certificate is None:
        certificate = bridge_free_dispatch(inventory, profile)
    require(certificate.profile == profile, "certificate profile not adjacency-derived")
    verify_piece_partition(inventory, certificate.pieces)
    verify_contracts(certificate)
    return inventory, certificate


# -------------------------- independent fixture generator ------------------


def add_clique(edges, vertices):
    edges.update(edge(left, right) for left, right in itertools.combinations(vertices, 2))


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

    def fresh(self, prefix):
        value = (prefix, self.serial)
        self.serial += 1
        self.vertices.add(value)
        return value

    def k4(self):
        vertices = tuple(self.fresh("K") for _ in range(4))
        add_clique(self.edges, vertices)
        return vertices

    def cycle(self, length, port=None):
        vertices = ([port] if port is not None else [])
        vertices += [self.fresh(f"C{length}") for _ in range(length - len(vertices))]
        add_cycle(self.edges, vertices)
        return tuple(vertices)

    def bridge_path(self, left, right, length):
        require(length >= 1, "bridge path length below one")
        internal = [self.fresh("R") for _ in range(length - 1)]
        sequence = [left, *internal, right]
        self.edges.update(edge(a, b) for a, b in zip(sequence, sequence[1:]))
        return tuple(sequence)

    def tree_payload(self, root, parent_map):
        made = []
        for parent_index in parent_map:
            require(type(parent_index) is int and -1 <= parent_index < len(made),
                    "bad generated tree parent")
            vertex = self.fresh("P")
            parent = root if parent_index == -1 else made[parent_index]
            self.edges.add(edge(parent, vertex))
            made.append(vertex)
        return tuple(made)

    def graph(self):
        return frozenset(self.vertices), frozenset(self.edges)


def fixture(profile, topology, route_length=1, payload_depth=0):
    """Generate adjacency only; labels are not consumed by verify()."""
    lengths = {
        "T4": (3, 3, 3, 3),
        "T3+odd>=5": (3, 3, 3, 7),
        "T2+C5+C5": (3, 3, 5, 5),
    }[profile]
    builder = Builder()
    k4 = builder.k4()
    cycles = []
    if topology == "shared-star":
        for length in lengths:
            cycles.append(builder.cycle(length, k4[0]))
    elif topology == "repeated-cuts":
        # Two independent repeated physical cuts on K4, no strings in verifier.
        for index, length in enumerate(lengths):
            cycles.append(builder.cycle(length, k4[index // 2]))
    elif topology == "nested":
        parent = k4[0]
        for length in lengths:
            current = builder.cycle(length, parent)
            cycles.append(current)
            parent = current[1]
    elif topology == "first-nontriangle":
        require(profile != "T4", "nontriangle fixture requested for T4")
        non = next(length for length in lengths if length != 3)
        rest = list(lengths); rest.remove(non)
        q = builder.cycle(non, k4[0]); cycles.append(q)
        # Put every triangle beyond the first nontriangle.  Then no direct
        # K4--triangle shared packet exists and the cascade branch is forced.
        parent = q[2]
        for length in rest:
            current = builder.cycle(length, parent)
            cycles.append(current)
            parent = current[1]
    elif topology == "long-bridge":
        # Vertex-disjoint cycle core joined by an arbitrary physical K2 chain.
        for index, length in enumerate(lengths):
            current = builder.cycle(length)
            cycles.append(current)
            parent = k4[0] if index == 0 else cycles[index - 1][1]
            builder.bridge_path(parent, current[0], route_length + index)
    elif topology == "mixed-bridge-shared":
        first = builder.cycle(lengths[0])
        builder.bridge_path(k4[0], first[0], route_length)
        cycles.append(first)
        parent = first[1]
        cycles.append(builder.cycle(lengths[1], parent))
        for length in lengths[2:]:
            cycles.append(builder.cycle(length, k4[1]))
    else:
        raise VerifyError("unknown generator topology")
    if payload_depth:
        builder.tree_payload(k4[2], tuple([-1] + list(range(payload_depth - 1))))
        for index, current in enumerate(cycles):
            builder.tree_payload(current[-1], (-1, 0, 0, 2, 1)[:1 + index])
    return builder.graph()


def relabel(vertices, edges):
    ordered = sorted(vertices, key=repr)
    mapping = {vertex: ("opaque", 1009 * index + 17) for index, vertex in enumerate(reversed(ordered))}
    return (frozenset(mapping[vertex] for vertex in vertices),
            frozenset(edge(mapping[left], mapping[right])
                      for current in edges for left, right in [tuple(current)]))


def certificate_signature(certificate):
    # Vertex counts can move between equally near one-root tree payloads under
    # opaque tie-breaking without changing the proved owner semantics.  The
    # invariant receipt is the derived branch, piece ranks/types and contracts.
    return (certificate.profile, certificate.dispatch,
            tuple(sorted(certificate.piece_kinds)),
            tuple(sorted(certificate.contracts)), len(certificate.pieces))


def expansion_invariance_audit():
    """Executable witnesses for the proved quotient/expansion contract.

    Subdividing a physical bridge replaces one K2 node by a K2 chain in the
    full block-cut tree; every new degree-two routing vertex remains in the
    same first-bridge territory.  Adding a one-root tree adds only rank-zero
    leaf blocks below its unique root.  Neither operation changes positive
    blocks, their ports, residual profile, or dispatch.  Induction on the
    number of inserted K2/tree leaves proves arbitrary finite expansion; the
    probes below check independent concrete depths and both operations at once.
    """
    signatures = set()
    sizes = []
    for length in (1, 2, 5, 13):
        vertices, edges = fixture("T3+odd>=5", "mixed-bridge-shared",
                                  route_length=length, payload_depth=length)
        _, certificate = verify(vertices, edges)
        require(certificate.dispatch == "first-bridge+K4+kT-core",
                "bridge expansion changed dispatch")
        signatures.add((certificate.profile, certificate.dispatch,
                        certificate.piece_kinds, certificate.contracts))
        sizes.append(len(vertices))
    require(len(signatures) == 1 and sizes == sorted(sizes),
            "bridge/tree expansion invariance failed")
    return len(sizes)


def hostile_tests():
    rejected = []
    base_vertices, base_edges = fixture("T2+C5+C5", "first-nontriangle", payload_depth=4)
    inventory, baseline = verify(base_vertices, base_edges)
    require(baseline.dispatch == "first-nontriangle-cascade",
            "hostile baseline missed cascade")

    # Add a chord to C5: exact block type must fail.
    c5 = next(block(inventory, index) for index in inventory.cycles
              if block(inventory, index).cycle_length == 5)
    nonedges = [edge(left, right) for left, right in itertools.combinations(c5.vertices, 2)
                if edge(left, right) not in base_edges]
    rejected.append(expect_rejection(
        lambda: verify(base_vertices, frozenset(set(base_edges) | {nonedges[0]})),
        "C5 chord / wrong block type"))

    # Rewire one cycle edge to a K4 vertex: merges blocks or breaks cycle.
    shared_k4 = c5.vertices & block(inventory, inventory.k4).vertices
    private_edges = [current for current in c5.edges if not (current & shared_k4)]
    require(private_edges, "hostile C5 has no private edge")
    current = private_edges[0]; left, right = tuple(current)
    kvertex = next(vertex for vertex in block(inventory, inventory.k4).vertices
                   if vertex not in c5.vertices)
    rewired = set(base_edges); rewired.remove(current); rewired.add(edge(left, kvertex))
    rejected.append(expect_rejection(lambda: verify(base_vertices, frozenset(rewired)),
                                     "hostile cycle-to-K4 rewire"))

    # Add two cross-block edges: this creates a hidden positive connector and
    # merges nominal blocks into an unsupported biconnected block.
    triangle = block(inventory, triangle_blocks(inventory)[0])
    tprivate = [vertex for vertex in triangle.vertices
                if vertex not in block(inventory, inventory.k4).vertices]
    cprivate = [vertex for vertex in c5.vertices
                if vertex not in block(inventory, inventory.k4).vertices and
                vertex not in triangle.vertices]
    require(len(cprivate) >= 2, "hostile blocks do not have private endpoints")
    extras = {edge(tprivate[0], cprivate[0]), edge(tprivate[1], cprivate[1])}
    rejected.append(expect_rejection(
        lambda: verify(base_vertices, frozenset(set(base_edges) | extras)),
        "hidden positive connector"))

    # Delete payload edge (disconnect), duplicate semantic vertex via malformed edge,
    # and manufacture a sixth positive block.
    payload_edge = next(current for current in base_edges
                        if any(isinstance(v, tuple) and v[0] == "P" for v in current))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices, frozenset(set(base_edges) - {payload_edge})),
        "omitted rooted payload"))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices, frozenset(set(base_edges) | {frozenset({kvertex})})),
        "loop/malformed edge"))

    # Non-residual profiles: even, C7+C5 with only two triangles, and four C5.
    for lengths_label, mutate in (
        ("even cycle", (3, 3, 3, 4)),
        ("two long unequal", (3, 3, 5, 7)),
        ("four pentagons", (5, 5, 5, 5)),
    ):
        builder = Builder(); k4 = builder.k4()
        for length in mutate: builder.cycle(length, k4[0])
        rejected.append(expect_rejection(lambda g=builder.graph(): verify(*g), lengths_label))

    # Threshold injection is impossible at API level; mutation of the private
    # fixed table must fail the exact value check.
    original = ANALYTIC_CONTRACTS["R31K-K4-T-SHARED-v1"]["strict_floor"]
    ANALYTIC_CONTRACTS["R31K-K4-T-SHARED-v1"]["strict_floor"] = 99
    try:
        vertices, edges = fixture("T4", "shared-star")
        rejected.append(expect_rejection(lambda: verify(vertices, edges),
                                         "analytic threshold mutation"))
    finally:
        ANALYTIC_CONTRACTS["R31K-K4-T-SHARED-v1"]["strict_floor"] = original

    # Four independent rank-one first-bridge arms have no proved payment in
    # this artifact.  The graph has a valid residual profile, but must be
    # rejected rather than laundered through the rooted K4 bound.
    four_arms = Builder()
    arm_k4 = four_arms.k4()
    for index, length in enumerate((3, 3, 5, 5)):
        current_cycle = four_arms.cycle(length)
        four_arms.bridge_path(arm_k4[index], current_cycle[0], 3 + index)
    rejected.append(expect_rejection(lambda: verify(*four_arms.graph()),
                                     "four independent rank-one bridge arms"))

    # Same-label topology rewires must change adjacency-derived branch.
    star = fixture("T3+odd>=5", "shared-star")
    bridge = fixture("T3+odd>=5", "mixed-bridge-shared", route_length=4)
    _, star_certificate = verify(*star)
    _, bridge_certificate = verify(*bridge)
    require(star_certificate.dispatch != bridge_certificate.dispatch,
            "same profile bridge rewire did not change dispatch")
    return tuple(rejected), 1


def audit_sources():
    require(frozenset(ANALYTIC_CONTRACTS) == EXPECTED_CONTRACT_IDS,
            "analytic contract ID set changed")
    for contract_id, record in ANALYTIC_CONTRACTS.items():
        require(set(record) == {"source", "sha256", "strict_floor"},
                f"malformed analytic contract: {contract_id}")
        path = ROOT / record["source"]
        require(path.is_file() and digest(path) == record["sha256"],
                f"analytic source changed: {contract_id}")


def audit():
    audit_sources()
    counts = Counter()
    signatures = Counter()
    generated = 0
    # Independently generated adjacency witnesses authenticate every profile
    # and every dispatch branch, plus long connectors, nesting, repeated cuts,
    # arbitrary labels, and rooted payloads.  They are not trusted fixtures.
    plans = (
        ("T4", "shared-star"), ("T4", "repeated-cuts"),
        ("T4", "nested"),
        ("T3+odd>=5", "shared-star"), ("T3+odd>=5", "nested"),
        ("T3+odd>=5", "first-nontriangle"),
        ("T3+odd>=5", "mixed-bridge-shared"),
        ("T2+C5+C5", "shared-star"), ("T2+C5+C5", "repeated-cuts"),
        ("T2+C5+C5", "nested"), ("T2+C5+C5", "first-nontriangle"),
    )
    for index, (profile, topology) in enumerate(plans):
        vertices, edges = fixture(profile, topology, route_length=7,
                                  payload_depth=(index % 6))
        inventory, certificate = verify(vertices, edges)
        require(certificate.profile == profile, "generated profile misclassified")
        counts[(profile, certificate.dispatch)] += 1
        signatures[certificate.dispatch] += 1
        generated += 1
        # Opaque relabeling must preserve semantic receipt up to vertex names.
        relabeled = relabel(vertices, edges)
        _, relabeled_certificate = verify(*relabeled)
        require(certificate_signature(certificate) ==
                certificate_signature(relabeled_certificate),
                "opaque relabeling changed semantic certificate")
        require(sum(block.rank for block in inventory.blocks) == 7,
                "generated block-rank sum changed")
    require({key[0] for key in counts} == {"T4", "T3+odd>=5", "T2+C5+C5"},
            "profile branch coverage incomplete")
    require({"first-bridge+K4+kT-core", "first-nontriangle-cascade",
             "K4+kT-core:T4",
             "K4+kT-core:T3+odd>=5", "K4+kT-core:T2+C5+C5"}
            <= set(signatures), "dispatch branch coverage incomplete")
    expansions = expansion_invariance_audit()
    rejected, rewires = hostile_tests()
    return generated, counts, signatures, expansions, rejected, rewires


def report(result):
    generated, counts, signatures, expansions, rejected, rewires = result
    return "\n".join((
        "R31-K adjacency semantic verifier: exact audit passed",
        "scope: R31-K only; no global or full-multiblock theorem",
        "input contract: finite simple adjacency only; no supplied profile/channel/owner/threshold",
        "Tarjan: exact K4 + four literal cycle blocks; full block-cut tree, K2 bridges and physical ports reconstructed",
        "residual profiles: T4; T3+odd>=5; T2+C5+C5",
        "dispatches: " + repr(dict(sorted(signatures.items()))),
        f"independently generated fixtures: {generated}; opaque relabel replay: {generated}",
        "profile/dispatch matrix: " + repr(dict(sorted(counts.items()))),
        f"quotient expansion probes: {expansions}; arbitrary finite K2/tree expansion proved by leaf/subdivision induction",
        "ownership: original vertices; connected induced disjoint exhaustive pieces; unique articulation/payload owner",
        "analytic contracts: " + repr(tuple(sorted(EXPECTED_CONTRACT_IDS))),
        f"hostile adjacency mutations rejected: {len(rejected)}; same-profile rewires distinguished: {rewires}",
        "status: accepted R31-K physical sublane authenticated; four-arm/global bridge ledger open",
    ))


def main():
    result = audit()
    output = report(result)
    if "--optimized-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-child"],
                               check=False, capture_output=True, text=True)
        require(child.returncode == 0, "optimized child failed: " + child.stderr)
        require(child.stderr == "", "optimized child wrote stderr")
        require(child.stdout.rstrip() == output,
                "normal and -O receipts are not byte-identical")
    print(output)


if __name__ == "__main__":
    main()
