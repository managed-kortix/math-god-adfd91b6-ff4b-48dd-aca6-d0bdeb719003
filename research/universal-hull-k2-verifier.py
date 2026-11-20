#!/usr/bin/env python3
"""Adjacency-only verifier for the universal beta-seven hull-K2 theorem.

Public API
==========
``verify(vertices, edges) -> Receipt`` accepts only finite simple adjacency.
``audit_receipt(vertices, edges, receipt)`` independently reconstructs and
replays every receipt field from the supplied adjacency and the pinned source
papers.

The accepted theorem lane is deliberately narrow and universal by block rank:
there must be exactly two positive-rank Tarjan maximal blocks, with ranks
(4,3) or (5,2), and their path in the full unsuppressed block--cut tree must
contain at least one physical bridge block K2.  No named kernel family,
fixture, or exact-row label is consulted.

All graph-sized traversals are iterative.  Original vertices may be arbitrary
hashable Python objects whose hash is stable during a call and whose equality
is a stable symmetric relation on distinct labels.  Reflexivity is not
required (persistent NaN- or identity-like labels are supported).  There is no
label ordering key and no promise about Inventory tuple order.
"""
from __future__ import annotations

import ast
import hashlib
import itertools
import tempfile
from collections import deque
from dataclasses import dataclass, replace
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_ROOT = HERE.parent
RECEIPT_SCHEMA = "universal-hull-k2-receipt-v1"
THEOREM_FAMILY = "universal-beta7-two-block-hull-k2"


class VerifyError(RuntimeError):
    """A graph, source, receipt, or self-test predicate failed closed."""


def require(condition, message):
    if not condition:
        raise VerifyError(message)


def sha256_bytes(blob):
    require(type(blob) is bytes, "SHA-256 input is not bytes")
    return hashlib.sha256(blob).hexdigest()


@dataclass(frozen=True, slots=True)
class SourceSpec:
    rank: int
    relative_path: str
    sha256: str
    strict: bool
    markers: tuple[bytes, ...]


# The complete current rank-two through rank-six papers are locked, even
# though the exact hull split uses only ranks 2--5.  The rank-six lock records
# the current lower-rank theorem lineage and the block convention/additivity
# source; it is not silently used to strengthen the (5,2)/(4,3) proof.
SOURCE_SPECS = (
    SourceSpec(
        2,
        "all-bicyclic-graphs/paper.tex",
        "56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da",
        True,
        (
            b"Every finite simple connected graph $G$ with $|V(G)|=n$ and\n$|E(G)|=n+1$ satisfies",
            b"\\boxed{\\splus(G)>n}",
        ),
    ),
    SourceSpec(
        3,
        "all-tricyclic-graphs/paper.tex",
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
        False,
        (
            b"Every finite simple connected graph $G$ with $|V(G)|=n$ and\n$|E(G)|=n+2$ satisfies",
            b"\\boxed{\\splus(G)\\geq n}",
            b"\\begin{lemma}[Induced superadditivity]\\label{lem:super}",
            b"$\\sigma(G)\\geq\\sum_j\\sigma(G[V_j])$.",
            b"with bridges regarded as two-vertex blocks.",
            b"Bridge blocks have\nrank zero, and ranks add over the nontrivial blocks.",
        ),
    ),
    SourceSpec(
        4,
        "all-tetracyclic-graphs/paper.tex",
        "70a931c28c8a8817e2c02818200885f73c532d9afe2c065831f2b3884d61160f",
        False,
        (
            b"Every finite simple connected graph $G$ with $|V(G)|=n$ and\n$|E(G)|=n+3$ satisfies",
            b"\\boxed{\\splus(G)\\geq n}",
        ),
    ),
    SourceSpec(
        5,
        "all-pentacyclic-graphs/paper.tex",
        "8ce140b07dc1428656b4ffd914305f2b14b49a0555cd13a6fc87be0fd4246a18",
        False,
        (
            b"If $G$ is a finite simple connected graph with $|V(G)|=n$ and\n$|E(G)|=n+4$, then",
            b"\\boxed{\\spn(G)\\ge n}",
        ),
    ),
    SourceSpec(
        6,
        "all-hexacyclic-graphs/paper.tex",
        "0e7a2db2932d38a4b4909831c34050553afc0973869fe937eb510cb59421bda7",
        False,
        (
            b"Every finite simple connected graph $G$ with $|V(G)|=n$ and\n$|E(G)|=n+5$ satisfies",
            b"\\boxed{\\spn(G)\\ge n}",
            b"the blocks of a connected graph are its\nmaximal $2$-connected subgraphs together with its bridge copies of $K_2$.",
            b"\\begin{lemma}[Cyclic-block rank additivity]\\label{lem:block-rank}",
            b"The cyclomatic rank of a connected graph is the sum of the cyclomatic ranks of\nits positive-rank cyclic blocks.",
        ),
    ),
)


def _authenticate_sources(root):
    """Read and authenticate every theorem source afresh; no success cache."""
    root = Path(root)
    require(tuple(spec.rank for spec in SOURCE_SPECS) == (2, 3, 4, 5, 6),
            "lower-rank source ledger changed")
    require(tuple(spec.strict for spec in SOURCE_SPECS) ==
            (True, False, False, False, False),
            "lower-rank strictness ledger changed")
    digests = []
    for spec in SOURCE_SPECS:
        path = root / spec.relative_path
        require(path.is_file(), f"missing pinned source for rank {spec.rank}")
        try:
            blob = path.read_bytes()
        except OSError as error:
            raise VerifyError(f"cannot read pinned source for rank {spec.rank}: {error}") from error
        digest = sha256_bytes(blob)
        require(digest == spec.sha256,
                f"pinned source bytes changed for rank {spec.rank}")
        for marker in spec.markers:
            require(marker in blob,
                    f"pinned semantic locator missing for rank {spec.rank}")
        digests.append(digest)
    return tuple(digests)


@dataclass(frozen=True, slots=True)
class Receipt:
    """Minimal replayable evidence; no caller-supplied owner sets are exposed."""
    schema: str
    family: str
    partition: tuple[int, int]
    hull_edges: frozenset
    ledger: tuple[tuple[int, int, bool], ...]


@dataclass(frozen=True, slots=True)
class _Snapshot:
    vertices: tuple
    edges: tuple


@dataclass(frozen=True, slots=True)
class _Graph:
    vertices: frozenset
    edges: frozenset
    adjacency: dict


@dataclass(frozen=True, slots=True)
class _Block:
    vertices: frozenset
    edges: frozenset
    rank: int


@dataclass(frozen=True, slots=True)
class _Inventory:
    graph: _Graph
    blocks: tuple[_Block, ...]
    membership: dict
    cuts: frozenset
    tree: dict
    positive: tuple[int, ...]
    hull_path: tuple


@dataclass(frozen=True, slots=True)
class _Quotient:
    hull_edges: frozenset
    components: tuple[frozenset, ...]
    component_ranks: tuple[int, ...]
    path_order: tuple[int, ...]


def _snapshot_adjacency(vertices, edges):
    try:
        vertex_items = tuple(vertices)
    except (TypeError, RuntimeError) as error:
        raise VerifyError(f"vertices are not a finite iterable: {error}") from error
    edge_items = []
    try:
        iterator = iter(edges)
    except TypeError as error:
        raise VerifyError(f"edges are not iterable: {error}") from error
    try:
        for raw_edge in iterator:
            try:
                pair = tuple(raw_edge)
            except (TypeError, RuntimeError) as error:
                raise VerifyError(f"edge is not a finite endpoint iterable: {error}") from error
            edge_items.append(pair)
    except RuntimeError as error:
        raise VerifyError(f"edge iteration failed: {error}") from error
    return _Snapshot(vertex_items, tuple(edge_items))


def _normalize_graph(snapshot):
    require(type(snapshot) is _Snapshot, "internal adjacency snapshot has wrong type")
    require(snapshot.vertices, "vertex set is empty")
    try:
        vertices = frozenset(snapshot.vertices)
    except (TypeError, ValueError) as error:
        raise VerifyError(f"every original vertex must be hashable: {error}") from error
    require(len(vertices) == len(snapshot.vertices),
            "vertex iterable contains duplicate equal vertices")

    normalized = set()
    for pair in snapshot.edges:
        require(type(pair) is tuple and len(pair) == 2,
                "edge is a loop or is not a two-endpoint pair")
        left, right = pair
        try:
            edge = frozenset((left, right))
        except (TypeError, ValueError) as error:
            raise VerifyError(f"edge endpoint is not hashable: {error}") from error
        require(len(edge) == 2,
                "edge is a loop or is not a two-distinct-vertex pair")
        try:
            endpoints_present = left in vertices and right in vertices
        except (TypeError, ValueError) as error:
            raise VerifyError(f"edge membership test failed: {error}") from error
        require(endpoints_present, "edge endpoint is absent from the vertex set")
        require(edge not in normalized, "parallel or duplicate undirected edge")
        normalized.add(edge)

    adjacency = {vertex: set() for vertex in vertices}
    for edge in normalized:
        left, right = tuple(edge)
        adjacency[left].add(right)
        adjacency[right].add(left)

    start = next(iter(vertices))
    seen = {start}
    queue = deque((start,))
    while queue:
        current = queue.popleft()
        for neighbor in adjacency[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    require(len(seen) == len(vertices), "parent graph is disconnected")
    return _Graph(
        vertices,
        frozenset(normalized),
        {vertex: frozenset(neighbors) for vertex, neighbors in adjacency.items()},
    )


def _tarjan_blocks(graph):
    """Iterative undirected edge-stack Tarjan decomposition.

    A frame is ``(vertex, live-neighbor-iterator)``.  Finishing a frame does
    the low-link update and edge-stack pop that a recursive return would do.
    Neighbor and root iteration are deliberately unordered: labels choose no
    semantic branch, and callers receive no ordering guarantee for blocks.
    """
    discovery = {}
    low = {}
    parent = {}
    parent_edge = {}
    edge_stack = []
    raw_blocks = []
    clock = 0
    roots = 0

    for root in graph.vertices:
        if root in discovery:
            continue
        roots += 1
        clock += 1
        discovery[root] = low[root] = clock
        frames = [(root, iter(graph.adjacency[root]))]
        while frames:
            current, neighbors = frames[-1]
            try:
                neighbor = next(neighbors)
            except StopIteration:
                frames.pop()
                if current in parent:
                    upstream = parent[current]
                    if low[current] < low[upstream]:
                        low[upstream] = low[current]
                    if low[current] >= discovery[upstream]:
                        boundary = parent_edge[current]
                        component_edges = set()
                        while True:
                            require(edge_stack, "Tarjan edge stack underflow")
                            popped = edge_stack.pop()
                            component_edges.add(popped)
                            if popped == boundary:
                                break
                        require(component_edges, "Tarjan emitted an empty block")
                        raw_blocks.append(frozenset(component_edges))
                else:
                    require(not edge_stack, "Tarjan edge stack leaked at a DFS root")
                continue

            current_edge = frozenset((current, neighbor))
            if neighbor not in discovery:
                parent[neighbor] = current
                parent_edge[neighbor] = current_edge
                edge_stack.append(current_edge)
                clock += 1
                discovery[neighbor] = low[neighbor] = clock
                frames.append((neighbor, iter(graph.adjacency[neighbor])))
            elif current in parent and (neighbor is parent[current] or neighbor == parent[current]):
                continue
            elif discovery[neighbor] < discovery[current]:
                edge_stack.append(current_edge)
                if discovery[neighbor] < low[current]:
                    low[current] = discovery[neighbor]

    require(roots == 1 and len(discovery) == len(graph.vertices),
            "Tarjan traversal did not cover one connected component")
    require(not edge_stack, "Tarjan edge stack was not exhausted")

    blocks = []
    for edge_set in raw_blocks:
        block_vertices = frozenset(vertex for edge in edge_set for vertex in edge)
        rank = len(edge_set) - len(block_vertices) + 1
        require(rank >= 0, "Tarjan emitted a negative-rank block")
        if rank == 0:
            require(len(edge_set) == 1 and len(block_vertices) == 2,
                    "rank-zero maximal block is not one physical K2")
        blocks.append(_Block(block_vertices, edge_set, rank))

    reconstructed = frozenset(edge for block in blocks for edge in block.edges)
    require(reconstructed == graph.edges, "Tarjan blocks omit or invent parent edges")
    require(sum(len(block.edges) for block in blocks) == len(graph.edges),
            "Tarjan blocks duplicate parent edges")
    return tuple(blocks)


def _build_inventory(graph):
    blocks = _tarjan_blocks(graph)
    require(blocks, "connected rank-seven graph has no maximal blocks")

    membership_lists = {vertex: [] for vertex in graph.vertices}
    for block_index, block in enumerate(blocks):
        for vertex in block.vertices:
            membership_lists[vertex].append(block_index)
    require(all(membership_lists[vertex] for vertex in graph.vertices),
            "a parent vertex is absent from every maximal block")
    membership = {
        vertex: tuple(indices) for vertex, indices in membership_lists.items()
    }
    cuts = frozenset(
        vertex for vertex, indices in membership.items() if len(indices) > 1
    )

    tree = {("B", index): set() for index in range(len(blocks))}
    tree.update({("C", vertex): set() for vertex in cuts})
    incidence_count = 0
    for cut in cuts:
        indices = membership[cut]
        require(len(indices) >= 2, "block-cut node has fewer than two blocks")
        for block_index in indices:
            block_node = ("B", block_index)
            cut_node = ("C", cut)
            require(cut in blocks[block_index].vertices,
                    "block-cut incidence invents membership")
            tree[block_node].add(cut_node)
            tree[cut_node].add(block_node)
            incidence_count += 1

    for block_index, block in enumerate(blocks):
        expected_cuts = frozenset(block.vertices & cuts)
        actual_cuts = frozenset(node[1] for node in tree[("B", block_index)])
        require(actual_cuts == expected_cuts,
                "full block-cut incidence omitted or invented a cut")
    require(all(node[0] == "B" for cut in cuts
                for node in tree[("C", cut)]),
            "block-cut incidence is not bipartite")

    start_node = next(iter(tree))
    tree_seen = {start_node}
    queue = deque((start_node,))
    while queue:
        node = queue.popleft()
        for neighbor in tree[node]:
            require(node in tree.get(neighbor, ()),
                    "block-cut incidence is asymmetric")
            if neighbor not in tree_seen:
                tree_seen.add(neighbor)
                queue.append(neighbor)
    require(len(tree_seen) == len(tree), "full block-cut incidence is disconnected")
    require(incidence_count == len(tree) - 1 and
            sum(len(neighbors) for neighbors in tree.values()) == 2 * incidence_count,
            "full block-cut incidence is not a tree")

    graph_rank = len(graph.edges) - len(graph.vertices) + 1
    require(graph_rank == 7, "parent graph must have cyclomatic rank seven")
    require(sum(block.rank for block in blocks) == graph_rank,
            "maximal-block ranks do not add to parent rank")
    positive = tuple(
        index for index, block in enumerate(blocks) if block.rank > 0
    )
    require(len(positive) == 2,
            "parent must have exactly two positive-rank maximal blocks")
    partition = tuple(sorted((blocks[index].rank for index in positive), reverse=True))
    require(partition in ((4, 3), (5, 2)),
            "positive block-rank partition must be (4,3) or (5,2)")

    source = ("B", positive[0])
    target = ("B", positive[1])
    previous = {source: None}
    queue = deque((source,))
    while queue and target not in previous:
        node = queue.popleft()
        for neighbor in tree[node]:
            if neighbor not in previous:
                previous[neighbor] = node
                queue.append(neighbor)
    require(target in previous,
            "positive blocks are disconnected in the full block-cut tree")
    reverse_path = []
    node = target
    while node is not None:
        reverse_path.append(node)
        node = previous[node]
    hull_path = tuple(reversed(reverse_path))
    require(hull_path[0] == source and hull_path[-1] == target,
            "positive-block hull has wrong endpoints")
    require(all(hull_path[index + 1] in tree[hull_path[index]]
                for index in range(len(hull_path) - 1)),
            "positive-block hull is not a block-cut path")
    require(all(node[0] == ("B" if index % 2 == 0 else "C")
                for index, node in enumerate(hull_path)),
            "positive-block hull does not alternate block and cut nodes")

    frozen_tree = {
        node: frozenset(neighbors) for node, neighbors in tree.items()
    }
    return _Inventory(
        graph, blocks, membership, cuts, frozen_tree, positive, hull_path
    )


def _simultaneous_hull_quotient(inventory):
    graph = inventory.graph
    hull_block_nodes = tuple(
        node for node in inventory.hull_path if node[0] == "B"
    )
    positive_nodes = frozenset((
        ("B", inventory.positive[0]),
        ("B", inventory.positive[1]),
    ))
    hull_k2_nodes = tuple(
        node for node in hull_block_nodes if node not in positive_nodes
    )
    require(hull_k2_nodes,
            "positive-block path contains no bridge K2; hull lane is closed")

    removed_edges = set()
    removed_neighbors = {}
    for node in hull_k2_nodes:
        block = inventory.blocks[node[1]]
        require(block.rank == 0 and len(block.vertices) == 2 and
                len(block.edges) == 1,
                "hull rank-zero block is not one physical bridge K2")
        physical_edge = next(iter(block.edges))
        require(physical_edge in graph.edges and physical_edge == block.vertices,
                "hull K2 is not an original physical graph edge")
        require(physical_edge not in removed_edges,
                "one physical hull bridge appears more than once")
        removed_edges.add(physical_edge)
        left, right = tuple(physical_edge)
        removed_neighbors.setdefault(left, set()).add(right)
        removed_neighbors.setdefault(right, set()).add(left)

    # Delete all hull bridge edges at once and flood the resulting components.
    # Each vertex and adjacency incidence is processed a constant number of
    # times, irrespective of the number of bridge blocks on the hull.
    component_of = {}
    components = []
    # Scan the frozen vertex set once for component seeds.  Do not repeatedly
    # take the first element of a shrinking set: tombstone scans in that idiom
    # can make a long all-bridge hull superlinear even though each flood is
    # otherwise disjoint.
    for seed in graph.vertices:
        if seed in component_of:
            continue
        component_index = len(components)
        reached = {seed}
        component_of[seed] = component_index
        queue = deque((seed,))
        while queue:
            current = queue.popleft()
            removed_here = removed_neighbors.get(current)
            for neighbor in graph.adjacency[current]:
                if removed_here is not None and neighbor in removed_here:
                    continue
                if neighbor not in component_of:
                    component_of[neighbor] = component_index
                    reached.add(neighbor)
                    queue.append(neighbor)
                else:
                    require(component_of[neighbor] == component_index,
                            "nondeleted edge joins deletion components")
        components.append(frozenset(reached))

    require(len(component_of) == len(graph.vertices),
            "simultaneous deletion omitted parent vertices")
    require(len(components) == len(removed_edges) + 1,
            "hull K2 deletion did not make one component per path interval")

    internal_edge_counts = [0] * len(components)
    quotient = {index: set() for index in range(len(components))}
    quotient_edges = {}
    for physical_edge in graph.edges:
        left, right = tuple(physical_edge)
        left_component = component_of[left]
        right_component = component_of[right]
        if physical_edge in removed_edges:
            require(left_component != right_component,
                    "hull K2 is not a physical bridge")
            component_pair = frozenset((left_component, right_component))
            require(len(component_pair) == 2,
                    "hull K2 has only one quotient endpoint")
            require(component_pair not in quotient_edges,
                    "two hull edges form a quotient multiedge")
            quotient_edges[component_pair] = physical_edge
            quotient[left_component].add(right_component)
            quotient[right_component].add(left_component)
        else:
            require(left_component == right_component,
                    "nondeleted physical edge crosses quotient components")
            internal_edge_counts[left_component] += 1

    require(len(quotient_edges) == len(removed_edges),
            "quotient omitted or invented a hull edge")
    quotient_seen = {next(iter(quotient))}
    queue = deque(quotient_seen)
    while queue:
        component = queue.popleft()
        for neighbor in quotient[component]:
            require(component in quotient[neighbor],
                    "hull quotient adjacency is asymmetric")
            if neighbor not in quotient_seen:
                quotient_seen.add(neighbor)
                queue.append(neighbor)
    require(len(quotient_seen) == len(components),
            "hull quotient is disconnected")
    require(len(quotient_edges) == len(components) - 1,
            "hull quotient is not a tree")
    degrees = tuple(len(quotient[index]) for index in range(len(components)))
    require(all(degree in (1, 2) for degree in degrees) and
            sum(degree == 1 for degree in degrees) == 2,
            "hull quotient is not one simple path")

    positive_components = []
    for block_index in inventory.positive:
        containing = frozenset(
            component_of[vertex]
            for vertex in inventory.blocks[block_index].vertices
        )
        require(len(containing) == 1,
                "positive maximal block was split by a hull K2")
        positive_components.append(next(iter(containing)))
    require(positive_components[0] != positive_components[1],
            "hull K2s do not separate the two positive blocks")
    require(all(degrees[index] == 1 for index in positive_components),
            "positive blocks are not at opposite quotient-path ends")

    # Walk the quotient from one positive block to the other.  A path has one
    # forward choice at each step; no vertex-label ordering is involved.
    path_order = [positive_components[0]]
    path_seen = {positive_components[0]}
    prior = None
    current = positive_components[0]
    while current != positive_components[1]:
        forward = quotient[current] - ({prior} if prior is not None else set())
        require(len(forward) == 1,
                "hull quotient has a missing or branching forward step")
        following = next(iter(forward))
        require(following not in path_seen,
                "hull quotient walk revisits a component")
        path_order.append(following)
        path_seen.add(following)
        prior, current = current, following
    require(len(path_order) == len(components),
            "positive blocks do not span the whole hull quotient path")

    component_ranks = []
    for component, edge_count in zip(components, internal_edge_counts):
        rank = edge_count - len(component) + 1
        require(rank >= 0,
                "connected quotient component has negative cyclomatic rank")
        component_ranks.append(rank)
    require(sum(component_ranks) == 7,
            "quotient component ranks do not sum to parent rank seven")

    # Independently assign every nondeleted maximal block to one quotient
    # component and replay block-rank additivity there.  Deleted hull K2s are
    # exactly the crossing rank-zero blocks.
    removed_block_indices = frozenset(node[1] for node in hull_k2_nodes)
    block_rank_sums = [0] * len(components)
    for block_index, block in enumerate(inventory.blocks):
        containing = frozenset(component_of[vertex] for vertex in block.vertices)
        if block_index in removed_block_indices:
            require(len(containing) == 2 and block.rank == 0 and
                    block.edges <= removed_edges,
                    "deleted hull block has wrong quotient incidence")
        else:
            require(len(containing) == 1,
                    "non-hull maximal block crosses quotient components")
            block_rank_sums[next(iter(containing))] += block.rank
    require(tuple(block_rank_sums) == tuple(component_ranks),
            "quotient side ranks disagree with maximal-block rank sums")

    partition = tuple(sorted(
        (inventory.blocks[index].rank for index in inventory.positive),
        reverse=True,
    ))
    position = {component: index for index, component in enumerate(path_order)}
    require(len(position) == len(path_order),
            "quotient path order repeats a component")
    prefix_rank = 0
    for split_index in range(len(path_order) - 1):
        prefix_rank += component_ranks[path_order[split_index]]
        suffix_rank = 7 - prefix_rank
        side_ranks = tuple(sorted((prefix_rank, suffix_rank), reverse=True))
        require(side_ranks == partition,
                "a hull K2 has wrong exact side-rank sums")
        left_has = tuple(
            position[component] <= split_index
            for component in positive_components
        )
        require(sum(left_has) == 1,
                "a hull K2 does not separate the positive blocks one per side")
        component_pair = frozenset((
            path_order[split_index], path_order[split_index + 1]
        ))
        require(component_pair in quotient_edges and
                quotient_edges[component_pair] in removed_edges,
                "quotient path step lacks its physical hull bridge")

    return _Quotient(
        frozenset(removed_edges),
        tuple(components),
        tuple(component_ranks),
        tuple(path_order),
    )


def _ledger_for(partition):
    strict_by_rank = {spec.rank: spec.strict for spec in SOURCE_SPECS}
    require(set(strict_by_rank) == {2, 3, 4, 5, 6},
            "authenticated lower-rank ledger is incomplete")
    ledger = tuple((rank, 0, strict_by_rank[rank]) for rank in partition)
    require(ledger in (
        ((4, 0, False), (3, 0, False)),
        ((5, 0, False), (2, 0, True)),
    ), "receipt theorem ledger is outside the hull-K2 theorem")
    return ledger


def _derive_receipt(snapshot):
    _authenticate_sources(SOURCE_ROOT)
    graph = _normalize_graph(snapshot)
    inventory = _build_inventory(graph)
    quotient = _simultaneous_hull_quotient(inventory)
    partition = tuple(sorted(
        (inventory.blocks[index].rank for index in inventory.positive),
        reverse=True,
    ))
    return Receipt(
        RECEIPT_SCHEMA,
        THEOREM_FAMILY,
        partition,
        quotient.hull_edges,
        _ledger_for(partition),
    )


def _audit_snapshot(snapshot, receipt):
    """Freshly derive expected evidence, then compare every public field."""
    require(type(receipt) is Receipt, "receipt has wrong record type")
    expected = _derive_receipt(snapshot)

    require(type(receipt.schema) is str and receipt.schema == expected.schema,
            "receipt schema failed independent replay")
    require(type(receipt.family) is str and receipt.family == expected.family,
            "receipt family failed independent replay")
    require(type(receipt.partition) is tuple and
            len(receipt.partition) == 2 and
            all(type(rank) is int for rank in receipt.partition) and
            receipt.partition == expected.partition,
            "receipt partition failed independent replay")
    require(type(receipt.hull_edges) is frozenset and receipt.hull_edges and
            all(type(edge) is frozenset and len(edge) == 2
                for edge in receipt.hull_edges) and
            receipt.hull_edges == expected.hull_edges,
            "receipt hull edges failed independent physical replay")
    require(type(receipt.ledger) is tuple and
            all(type(row) is tuple and len(row) == 3 and
                type(row[0]) is int and type(row[1]) is int and
                type(row[2]) is bool for row in receipt.ledger) and
            receipt.ledger == expected.ledger,
            "receipt ledger failed independent source/theorem replay")
    return True


def verify(vertices, edges):
    """Verify adjacency and return a minimal immutable theorem receipt."""
    snapshot = _snapshot_adjacency(vertices, edges)
    receipt = _derive_receipt(snapshot)
    # Deliberately replay from the adjacency snapshot rather than trusting any
    # intermediate Inventory or quotient object used above.
    _audit_snapshot(snapshot, receipt)
    return receipt


def audit_receipt(vertices, edges, receipt):
    """Independently replay a possibly hostile receipt from adjacency."""
    snapshot = _snapshot_adjacency(vertices, edges)
    return _audit_snapshot(snapshot, receipt)


# ---------------------------------------------------------------------------
# Deterministic self-tests.  Labels and Inventory order never enter stdout.
# ---------------------------------------------------------------------------


class _Builder:
    def __init__(self):
        self.vertices = set()
        self.edges = set()
        self.counter = 0

    def fresh(self, tag="v"):
        vertex = (tag, self.counter)
        self.counter += 1
        self.vertices.add(vertex)
        return vertex

    def edge(self, left, right):
        require(left != right, "test builder attempted a loop")
        self.vertices.update((left, right))
        physical = frozenset((left, right))
        require(len(physical) == 2 and physical not in self.edges,
                "test builder attempted a duplicate edge")
        self.edges.add(physical)

    def path(self, left, right, length, tag="p"):
        require(type(length) is int and length >= 1,
                "test builder path length is invalid")
        chain = [left]
        for unused in range(length - 1):
            chain.append(self.fresh(tag))
        chain.append(right)
        for first, second in zip(chain, chain[1:]):
            self.edge(first, second)
        return tuple(chain)

    def arm(self, root, length, tag="a"):
        current = root
        chain = [root]
        for unused in range(length):
            following = self.fresh(tag)
            self.edge(current, following)
            chain.append(following)
            current = following
        return tuple(chain)

    def multitheta(self, rank, tag="b", shared=None, deep_arm=None):
        require(type(rank) is int and rank >= 1,
                "test positive-block rank is invalid")
        left = shared if shared is not None else self.fresh(tag)
        self.vertices.add(left)
        right = self.fresh(tag)
        lengths = [2] * (rank + 1)
        if deep_arm is not None:
            require(type(deep_arm) is int and deep_arm >= 2,
                    "test deep arm is invalid")
            lengths[0] = deep_arm
        paths = tuple(
            self.path(left, right, length, f"{tag}-arm-{index}")
            for index, length in enumerate(lengths)
        )
        return left, right, paths

    def graph(self):
        return frozenset(self.vertices), frozenset(self.edges)


def _bridge_parent(partition, connector_length, deep_arm=None, payload_length=0):
    builder = _Builder()
    left = builder.multitheta(partition[0], "left", deep_arm=deep_arm)
    right = builder.multitheta(partition[1], "right", deep_arm=deep_arm)
    connector = builder.path(
        left[0], right[0], connector_length, "connector"
    )
    if payload_length:
        builder.arm(left[1], payload_length, "off-hull-payload")
    return builder.graph(), connector


def _shared_cut_parent(payload_length):
    builder = _Builder()
    cut = builder.fresh("shared-cut")
    builder.multitheta(4, "rank4", shared=cut)
    builder.multitheta(3, "rank3", shared=cut)
    builder.arm(cut, payload_length, "off-hull-k2")
    return builder.graph()


def _three_positive_parent():
    builder = _Builder()
    blocks = (
        builder.multitheta(3, "rank3"),
        builder.multitheta(2, "rank2a"),
        builder.multitheta(2, "rank2b"),
    )
    builder.path(blocks[0][0], blocks[1][0], 2, "join1")
    builder.path(blocks[1][1], blocks[2][0], 2, "join2")
    return builder.graph()


def _connector_chord_parent():
    builder = _Builder()
    left = builder.multitheta(3, "left3")
    right = builder.multitheta(3, "right3")
    chain = builder.path(left[0], right[0], 7, "chord-path")
    builder.edge(chain[1], chain[5])
    return builder.graph()


def _wrong_partition_parent():
    builder = _Builder()
    left = builder.multitheta(6, "rank6")
    right = builder.multitheta(1, "rank1")
    builder.path(left[0], right[0], 1, "join")
    return builder.graph()


class _CollidingReprIdentity:
    __slots__ = ("token",)

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return "<same-opaque-repr>"


class _OtherIdentity:
    __slots__ = ("token",)

    def __init__(self, token):
        self.token = token


class _NonReflexiveIdentity:
    """Hashable identity label whose equality relation is deliberately false."""
    __slots__ = ("token",)

    def __init__(self, token):
        self.token = token

    def __hash__(self):
        return 0

    def __eq__(self, other):
        return False

    def __repr__(self):
        return "<non-reflexive-identity>"


def _relabel_graph(graph, mapping):
    vertices, edges = graph
    relabeled_vertices = frozenset(mapping.values())
    relabeled_edges = frozenset(
        frozenset(mapping[vertex] for vertex in edge) for edge in edges
    )
    require(len(relabeled_vertices) == len(vertices) and
            len(relabeled_edges) == len(edges),
            "relabeling collapsed adjacency")
    return relabeled_vertices, relabeled_edges


def _heterogeneous_relabel(graph):
    vertices, edges = graph
    mapping = {}
    for index, vertex in enumerate(vertices):
        if index % 2 == 0:
            label = _CollidingReprIdentity(index)
        elif index == 1:
            label = None
        elif index % 11 == 0:
            label = ("tuple-label", index)
        elif index % 7 == 0:
            label = f"string-label-{index}"
        elif index % 5 == 0:
            label = b"bytes-label-" + str(index).encode("ascii")
        elif index % 3 == 0:
            label = 10_000_000 + index
        else:
            label = _OtherIdentity(index)
        mapping[vertex] = label
    return _relabel_graph(graph, mapping), mapping


def _mapped_edges(edges, mapping):
    return frozenset(
        frozenset(mapping[vertex] for vertex in edge) for edge in edges
    )


def _expect_rejection(action, label, expected_fragment):
    require(type(label) is str and label, "hostile test label is empty")
    require(type(expected_fragment) is str and expected_fragment,
            "hostile test expected reason is empty")
    try:
        action()
    except VerifyError as error:
        require(expected_fragment in str(error),
                f"hostile rejection had wrong reason for {label}: {error}")
        return label
    raise VerifyError(f"hostile mutation was accepted: {label}")


def _module_recursion_audit():
    """Fail if module-level Python functions form a syntactic call cycle."""
    try:
        source = Path(__file__).read_text(encoding="utf-8")
    except OSError as error:
        raise VerifyError(f"cannot read verifier for recursion audit: {error}") from error
    tree = ast.parse(source)
    definitions = {
        node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
    }
    calls = {name: set() for name in definitions}
    recursion_limit_setter = "set" + "recursion" + "limit"
    for name, definition in definitions.items():
        for node in ast.walk(definition):
            if isinstance(node, ast.Call):
                require(not (isinstance(node.func, ast.Attribute) and
                             node.func.attr == recursion_limit_setter),
                        "verifier changes the Python recursion limit")
                if isinstance(node.func, ast.Name) and node.func.id in definitions:
                    calls[name].add(node.func.id)

    # Iterative color DFS over the syntactic module-level call graph.
    color = {name: 0 for name in definitions}
    for root in definitions:
        if color[root] != 0:
            continue
        color[root] = 1
        stack = [(root, iter(calls[root]))]
        while stack:
            current, neighbors = stack[-1]
            try:
                neighbor = next(neighbors)
            except StopIteration:
                color[current] = 2
                stack.pop()
                continue
            require(color[neighbor] != 1,
                    f"module-level recursion cycle reaches {neighbor}")
            if color[neighbor] == 0:
                color[neighbor] = 1
                stack.append((neighbor, iter(calls[neighbor])))
    return len(definitions)


def _self_tests():
    _authenticate_sources(SOURCE_ROOT)
    function_count = _module_recursion_audit()

    connector_lengths = (1, 1401, 10000, 20000)
    connector_cases = 0
    retained_for_relabel = {}
    for partition in ((4, 3), (5, 2)):
        for length in connector_lengths:
            graph, connector = _bridge_parent(partition, length)
            receipt = verify(*graph)
            require(receipt.partition == partition and
                    len(receipt.hull_edges) == length,
                    "connector stress case reconstructed the wrong hull")
            connector_cases += 1
            if length == 1401:
                retained_for_relabel[partition] = (graph, receipt)

    # Two positive blocks each contain a 12,000-edge arm.  This exceeds the
    # ordinary Python call-stack depth without changing the recursion limit.
    deep_graph, unused_connector = _bridge_parent(
        (4, 3), 1, deep_arm=12000
    )
    deep_receipt = verify(*deep_graph)
    require(len(deep_receipt.hull_edges) == 1,
            "deep-arm graph lost its physical hull bridge")

    payload_graph, unused_connector = _bridge_parent(
        (5, 2), 3, payload_length=20000
    )
    payload_receipt = verify(*payload_graph)
    require(len(payload_receipt.hull_edges) == 3,
            "long off-hull payload contaminated the hull")

    # Heterogeneous opaque labels include many default identity-hashed objects
    # with exactly colliding repr strings.  Exact mapped hull-edge sets, not
    # tuple positions, are compared.
    relabel_replays = 0
    for partition in ((4, 3), (5, 2)):
        graph, receipt = retained_for_relabel[partition]
        relabeled, mapping = _heterogeneous_relabel(graph)
        relabeled_receipt = verify(*relabeled)
        require(relabeled_receipt.partition == receipt.partition and
                relabeled_receipt.ledger == receipt.ledger and
                relabeled_receipt.hull_edges ==
                _mapped_edges(receipt.hull_edges, mapping),
                "heterogeneous opaque relabel changed theorem semantics")
        relabel_replays += 1

    # Python hashability does not imply reflexive equality.  The graph code
    # must still honor a persistent object used as one vertex: dict/set lookup
    # recognizes the identical object even when ``x == x`` is false.  Tarjan's
    # parent-edge test therefore uses identity-or-equality.  Exercise both one
    # built-in NaN label and an all-vertex, constant-hash, non-reflexive
    # relabeling so this contract cannot regress silently.
    nonreflexive_replays = 0
    base_graph, base_connector = _bridge_parent((4, 3), 20, payload_length=10)
    connector_internal = base_connector[1]
    persistent_nan = float("nan")
    nan_mapping = {
        vertex: (persistent_nan if vertex is connector_internal else vertex)
        for vertex in base_graph[0]
    }
    nan_graph = _relabel_graph(base_graph, nan_mapping)
    nan_receipt = verify(*nan_graph)
    require(nan_receipt.partition == (4, 3) and
            len(nan_receipt.hull_edges) == 20 and
            audit_receipt(*nan_graph, nan_receipt),
            "persistent NaN relabel changed theorem semantics")
    nonreflexive_replays += 1

    all_nonreflexive_mapping = {
        vertex: _NonReflexiveIdentity(index)
        for index, vertex in enumerate(base_graph[0])
    }
    all_nonreflexive_graph = _relabel_graph(
        base_graph, all_nonreflexive_mapping
    )
    all_nonreflexive_receipt = verify(*all_nonreflexive_graph)
    require(all_nonreflexive_receipt.partition == (4, 3) and
            len(all_nonreflexive_receipt.hull_edges) == 20 and
            audit_receipt(*all_nonreflexive_graph,
                          all_nonreflexive_receipt),
            "all-nonreflexive relabel changed theorem semantics")
    nonreflexive_replays += 1

    # Reversing caller iteration order must leave every receipt field equal.
    order_graph, unused_connector = _bridge_parent((4, 3), 9)
    ordered_vertices = tuple(order_graph[0])
    ordered_edges = tuple(tuple(edge) for edge in order_graph[1])
    forward_receipt = verify(ordered_vertices, ordered_edges)
    reverse_receipt = verify(
        tuple(reversed(ordered_vertices)), tuple(reversed(ordered_edges))
    )
    require(forward_receipt == reverse_receipt,
            "caller iteration order changed the semantic receipt")
    require(audit_receipt(*order_graph, forward_receipt),
            "valid receipt failed public hostile replay")
    order_replays = 1

    hostile = []
    no_hull_graph = _shared_cut_parent(12000)
    hostile.append(_expect_rejection(
        lambda: verify(*no_hull_graph),
        "off-hull K2 payload with shared-cut positives",
        "positive-block path contains no bridge K2",
    ))
    chord_graph = _connector_chord_parent()
    hostile.append(_expect_rejection(
        lambda: verify(*chord_graph), "connector chord",
        "exactly two positive-rank maximal blocks",
    ))
    third_graph = _three_positive_parent()
    hostile.append(_expect_rejection(
        lambda: verify(*third_graph), "third positive block",
        "exactly two positive-rank maximal blocks",
    ))
    wrong_partition_graph = _wrong_partition_parent()
    hostile.append(_expect_rejection(
        lambda: verify(*wrong_partition_graph), "wrong rank partition",
        "partition must be (4,3) or (5,2)",
    ))

    malformed_graph, unused_connector = _bridge_parent((4, 3), 2)
    any_vertex = next(iter(malformed_graph[0]))
    hostile.append(_expect_rejection(
        lambda: verify(malformed_graph[0],
                       tuple(malformed_graph[1]) + ((any_vertex, any_vertex),)),
        "loop", "edge is a loop",
    ))
    one_edge = next(iter(malformed_graph[1]))
    first, second = tuple(one_edge)
    hostile.append(_expect_rejection(
        lambda: verify(malformed_graph[0],
                       tuple(malformed_graph[1]) + ((second, first),)),
        "duplicate edge", "parallel or duplicate undirected edge",
    ))
    extra_left = ("disconnected", 1)
    extra_right = ("disconnected", 2)
    hostile.append(_expect_rejection(
        lambda: verify(malformed_graph[0] | {extra_left, extra_right},
                       malformed_graph[1] | {frozenset((extra_left, extra_right))}),
        "disconnected component", "parent graph is disconnected",
    ))
    isolated = ("isolated", 3)
    hostile.append(_expect_rejection(
        lambda: verify(malformed_graph[0] | {isolated}, malformed_graph[1]),
        "isolated vertex", "parent graph is disconnected",
    ))

    # Authenticate an exact temporary mirror, then mutate and remove sources.
    with tempfile.TemporaryDirectory() as temporary:
        mirror = Path(temporary)
        for spec in SOURCE_SPECS:
            destination = mirror / spec.relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((SOURCE_ROOT / spec.relative_path).read_bytes())
        require(_authenticate_sources(mirror) ==
                tuple(spec.sha256 for spec in SOURCE_SPECS),
                "exact source mirror failed authentication")
        changed = mirror / SOURCE_SPECS[3].relative_path
        changed.write_bytes(changed.read_bytes() + b"\nHOSTILE-SOURCE-MUTATION\n")
        hostile.append(_expect_rejection(
            lambda: _authenticate_sources(mirror), "source byte mutation",
            "pinned source bytes changed for rank 5",
        ))
        changed.write_bytes((SOURCE_ROOT / SOURCE_SPECS[3].relative_path).read_bytes())
        missing = mirror / SOURCE_SPECS[4].relative_path
        missing.unlink()
        hostile.append(_expect_rejection(
            lambda: _authenticate_sources(mirror), "missing source",
            "missing pinned source for rank 6",
        ))

    # A receipt cannot be carried across a mutation of its adjacency source.
    mutable_vertices = list(malformed_graph[0])
    mutable_edges = [tuple(edge) for edge in malformed_graph[1]]
    mutation_receipt = verify(mutable_vertices, mutable_edges)
    mutable_edges.append((mutable_vertices[0], mutable_vertices[0]))
    hostile.append(_expect_rejection(
        lambda: audit_receipt(mutable_vertices, mutable_edges, mutation_receipt),
        "adjacency source mutation", "edge is a loop",
    ))

    # Hostile receipt replay.  No owner field exists; all exposed evidence is
    # recomputed.  Both absent physical edges and real off-hull edges fail.
    receipt_graph, unused_connector = _bridge_parent(
        (4, 3), 3, payload_length=5
    )
    honest = verify(*receipt_graph)
    forged = []
    forged.append(_expect_rejection(
        lambda: audit_receipt(*receipt_graph,
                              replace(honest, schema="forged-schema")),
        "forged schema", "receipt schema",
    ))
    forged.append(_expect_rejection(
        lambda: audit_receipt(*receipt_graph,
                              replace(honest, family="forged-family")),
        "forged family", "receipt family",
    ))
    forged.append(_expect_rejection(
        lambda: audit_receipt(*receipt_graph,
                              replace(honest, partition=(5, 2))),
        "forged partition", "receipt partition",
    ))
    forged.append(_expect_rejection(
        lambda: audit_receipt(*receipt_graph,
                              replace(honest, ledger=((7, 0, False),))),
        "forged ledger", "receipt ledger",
    ))
    forged.append(_expect_rejection(
        lambda: audit_receipt(*receipt_graph,
                              replace(honest, hull_edges=frozenset())),
        "empty hull edges", "receipt hull edges",
    ))
    omitted = frozenset(tuple(honest.hull_edges)[1:])
    forged.append(_expect_rejection(
        lambda: audit_receipt(*receipt_graph,
                              replace(honest, hull_edges=omitted)),
        "omitted physical hull edge", "receipt hull edges",
    ))
    absent_endpoint = _CollidingReprIdentity("absent")
    present_endpoint = next(iter(receipt_graph[0]))
    nonexistent = frozenset((present_endpoint, absent_endpoint))
    forged.append(_expect_rejection(
        lambda: audit_receipt(
            *receipt_graph,
            replace(honest, hull_edges=honest.hull_edges | {nonexistent}),
        ),
        "nonexistent hull edge", "receipt hull edges",
    ))
    off_hull = next(
        edge for edge in receipt_graph[1] if edge not in honest.hull_edges
    )
    forged.append(_expect_rejection(
        lambda: audit_receipt(
            *receipt_graph,
            replace(honest, hull_edges=frozenset((off_hull,))),
        ),
        "real but off-hull edge", "receipt hull edges",
    ))
    forged.append(_expect_rejection(
        lambda: audit_receipt(*receipt_graph, (honest,)),
        "wrong receipt record type", "receipt has wrong record type",
    ))

    require(connector_cases == 8 and relabel_replays == 2 and
            nonreflexive_replays == 2 and order_replays == 1,
            "accepted stress-test census changed")
    require(len(hostile) == 11, "hostile adjacency/source census changed")
    require(len(forged) == 9, "hostile receipt census changed")
    require(function_count >= 20, "recursion audit saw too few module functions")
    return {
        "connector_cases": connector_cases,
        "relabel_replays": relabel_replays,
        "nonreflexive_replays": nonreflexive_replays,
        "order_replays": order_replays,
        "hostile": len(hostile),
        "forged": len(forged),
        "function_count": function_count,
    }


def main():
    stats = _self_tests()
    output = (
        "universal hull-K2 beta-seven theorem: exact audit passed\n"
        "scope: exactly two positive maximal blocks; partitions (4,3) or (5,2); hull K2 required\n"
        "sources: current rank-2..6 papers authenticated; family fixtures/source rows used=0\n"
        "reconstruction: iterative edge-stack Tarjan; full unsuppressed block-cut tree; no label ordering key\n"
        "quotient: all hull K2s deleted simultaneously; physical path and every exact side split replayed\n"
        "stress: connector lengths 1,1401,10000,20000 in both partitions; deep arms=12000; off-hull payload=20000\n"
        f"accepted connector cases: {stats['connector_cases']}; heterogeneous relabel replays: "
        f"{stats['relabel_replays']}; nonreflexive relabel replays: "
        f"{stats['nonreflexive_replays']}; caller-order replays: {stats['order_replays']}\n"
        f"hostile adjacency/source cases rejected: {stats['hostile']}; hostile receipts rejected: "
        f"{stats['forged']}\n"
        "conclusion: partition (4,3) gives sigma>=0; partition (5,2) gives sigma>0\n"
        "status: theorem artifact passed for the universal hull-K2 lane only"
    )
    print(output)


if __name__ == "__main__":
    main()
