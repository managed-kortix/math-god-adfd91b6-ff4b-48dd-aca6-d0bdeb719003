#!/usr/bin/env python3
"""OPEN exact hostile audit of the physical induced topology behind R31-S.

This is deliberately not an authoritative theorem verifier.  It pins the
committed transport/cactus sources, independently realizes every transported
record, performs the actual vertex opening and edge cut, and checks the
resulting induced vertex territories.  Connector paths are reduced through the
complete five-by-five symbolic remnant classes; arbitrary additional vertices
are subdivisions of one-root path remnants and cannot change a cyclic block,
cyclomatic rank, or owner.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    "transport": (
        ROOT / "research/r31-s-doubled-c4-marked-cut-verifier.py",
        "b14e7544bd8f5298fd425c68228e5fb4f5c49071dd3a7ec773ee5de610630c71",
    ),
    "d3_diagnostic": (
        ROOT / "research/r31-s-d3-diamond-packet-verifier.py",
        "f0b799d5fc7734749335bb6b344c58357bab69668b0dae40c5149146c66e9993",
    ),
    "four_triangle_verifier": (
        ROOT / "research/r31-s-c4-marked-four-triangle-verifier.py",
        "d405f644467ab59e615a4cf6fdf5ada1a3ba8c21eadcd1ee7035b3fa37d159e0",
    ),
    "four_triangle_theorem": (
        ROOT / "positive-square-energy/heptacyclic-general"
        / "r31-s-c4-marked-four-triangle-theorem.md",
        "78344337226ae5c5b42645dd563390eec9eb462824e78fd4e42d7fa54051309d",
    ),
    "packing_two_theorem": (
        ROOT / "packing-two-square-energy/paper.tex",
        "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
    ),
    "frontier": (
        ROOT / "positive-square-energy/heptacyclic-general"
        / "r31-s-doubled-c4-three-triangle-frontier.md",
        "ef6f646a0a4416a161dae588940c271a73104c6e86a243baba22928234a082d6",
    ),
    "upstream_owner_rules": (
        ROOT / "positive-square-energy/heptacyclic-general"
        / "complete-multiblock-theorem.md",
        "f7a3e009b9b617b0ea5f245702e7e93d2f74116ef7d388d65222069cb06ac347",
    ),
    "upstream_nested_reduction": (
        ROOT / "positive-square-energy/heptacyclic-general"
        / "nested-induced-piece-packet-theorem.md",
        "79b44180ff2d3ca44b5537e2913709fa6c2334b2e475990b34508475592a000b",
    ),
    "owner_ledger": (
        ROOT / "research/fixtures/heptacyclic-multiblock-owner-ledger.json",
        "0630cd96fd341b9017b31d6a36341cfead0c6bca64517c1073797ffc14747f42",
    ),
    "pentacyclic_owner_model": (
        ROOT / "positive-square-energy/pentacyclic-general"
        / "four-residual-owner-exact-closure.md",
        "b182d37b472808cc2c000e61958471bc6c998ade17e02ec8ea14f7329653cd46",
    ),
}

# If a path is opened at an internal vertex, its two retained endpoint
# remnants have edge lengths a,b >= 0 with a+b even.  If an odd path is cut
# at an edge, its two retained remnants have edge lengths c,d >= 0 with c+d
# even.  Up to subdivision, the following are all possibilities: both empty;
# one empty and the other positive even; or both positive of common odd/even
# parity.  They are canonical representatives, not a bounded-length sample.
REMNANT_CASES = ((0, 0), (0, 2), (2, 0), (1, 1), (2, 2))


class AuditError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_sources():
    for label, (path, expected) in SOURCES.items():
        require(path.is_file(), f"missing pinned source: {label}")
        require(digest(path) == expected, f"pinned source changed: {label}")


def load_transport_module():
    path = SOURCES["transport"][0]
    spec = importlib.util.spec_from_file_location("marked_transport", path)
    require(spec is not None and spec.loader is not None,
            "cannot load marked transport verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


M = load_transport_module()


def edge(left, right):
    require(left != right, "loop introduced")
    return frozenset((left, right))


def endpoints(current):
    require(len(current) == 2, "malformed undirected edge")
    return tuple(current)


def adjacency(vertices, edges):
    result = {vertex: set() for vertex in vertices}
    for current in edges:
        left, right = endpoints(current)
        require(left in result and right in result, "edge escaped vertex set")
        result[left].add(right)
        result[right].add(left)
    return result


def components(vertices, edges):
    graph = adjacency(vertices, edges)
    unseen = set(vertices)
    result = []
    while unseen:
        seed = min(unseen, key=repr)
        unseen.remove(seed)
        component = {seed}
        stack = [seed]
        while stack:
            current = stack.pop()
            for neighbor in graph[current] & unseen:
                unseen.remove(neighbor)
                component.add(neighbor)
                stack.append(neighbor)
        result.append(frozenset(component))
    return tuple(result)


def induced_edges(edges, vertices):
    return {current for current in edges if current <= vertices}


def graph_rank(vertices, edges):
    return len(edges) - len(vertices) + len(components(vertices, edges))


def connected(vertices, edges):
    return bool(vertices) and len(components(vertices, edges)) == 1


def is_tree(vertices, edges):
    return connected(vertices, edges) and len(edges) == len(vertices) - 1


def biconnected_edge_blocks(vertices, edges):
    """Tarjan edge stacks: one block per bridge or maximal 2-connected piece."""
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
                        popped = stack.pop()
                        block.add(popped)
                        if popped == current_edge:
                            break
                    blocks.append(frozenset(block))
            elif parent.get(current) != neighbor and discovery[neighbor] < discovery[current]:
                stack.append(current_edge)
                low[current] = min(low[current], discovery[neighbor])

    for seed in sorted(vertices, key=repr):
        if seed not in discovery:
            visit(seed)
            require(not stack, "biconnected edge stack did not empty")
    require(set().union(*blocks) == set(edges) if blocks else not edges,
            "biconnected blocks do not exhaust edges")
    require(sum(map(len, blocks)) == len(edges),
            "biconnected blocks duplicate an edge")
    return tuple(blocks)


def independent_records():
    owners = tuple(M.OWNER_LABELS)
    direct = {("direct3", roots)
              for roots in itertools.combinations_with_replacement(owners, 3)}
    chain_direct = {("chain2+direct", upstream, direct_root)
                    for upstream in owners for direct_root in owners}
    fork = {("fork", upstream, occupancy)
            for upstream in owners for occupancy in ("same", "split")}
    chain = {("chain3", upstream) for upstream in owners}
    records = direct | chain_direct | fork | chain
    require(len(records) == 110, "independent three-block record census changed")
    require(Counter(record[0] for record in records) == Counter({
        "direct3": 56, "chain2+direct": 36, "fork": 12, "chain3": 6,
    }), "independent incidence-shape census changed")
    return records


def canonical_remnant_pair(left, right):
    """Normalize every admissible arbitrary remnant pair to REMNANT_CASES."""
    require(type(left) is int and type(right) is int and left >= 0 and right >= 0,
            "remnant length is not a nonnegative integer")
    require((left - right) % 2 == 0, "remnant parities differ")
    if left == right == 0:
        return (0, 0)
    if left == 0:
        require(right % 2 == 0, "one-empty remnant is not even")
        return (0, 2)
    if right == 0:
        require(left % 2 == 0, "one-empty remnant is not even")
        return (2, 0)
    return (1, 1) if left % 2 else (2, 2)


def audit_symbolic_remnant_reduction():
    require(tuple(canonical_remnant_pair(*pair) for pair in REMNANT_CASES) ==
            REMNANT_CASES, "canonical remnant representatives are not fixed")
    # Exact formulas.  For opening remnants a,b, L=a+b+2 and j=a+1;
    # for cut remnants c,d, M=c+d+1 and k=c.
    for left, right in REMNANT_CASES:
        open_length = left + right + 2
        open_position = left + 1
        require(open_length >= 2 and open_length % 2 == 0,
                "open connector representative is not positive even")
        require(1 <= open_position < open_length,
                "open position is not internal")
        cut_length = left + right + 1
        cut_position = left
        require(cut_length >= 1 and cut_length % 2 == 1,
                "cut connector representative is not positive odd")
        require(0 <= cut_position < cut_length,
                "cut position is not an actual edge")
    # Hostile long values exercise the total normalizer; the proof of
    # exhaustiveness is the zero/nonzero and common-parity case split above.
    long_pairs = ((0, 18), (20, 0), (1, 17), (7, 9), (2, 18), (14, 8))
    require(set(canonical_remnant_pair(*pair) for pair in long_pairs) ==
            {(0, 2), (2, 0), (1, 1), (2, 2)},
            "long remnant normalizer lost a class")


def build_core(row, connector_lengths):
    target = M.target_geometry(row)
    lengths = list(M.first_simple_lengths(row))
    require(set(connector_lengths) == set(M.CONNECTORS),
            "connector length assignment is incomplete")
    for path_index, length in connector_lengths.items():
        require(type(length) is int and length >= 1,
                "connector length is not positive integral")
        require(length % 2 == int(row[path_index]),
                "connector parity changed")
        lengths[path_index] = length
    vertices = {("branch", index) for index in range(4)}
    edges = set()
    paths = {}
    for path_index, ((left, right), length) in enumerate(zip(M.ENDPOINTS, lengths)):
        sequence = (
            [("branch", left)]
            + [("path", path_index, place) for place in range(1, length)]
            + [("branch", right)]
        )
        paths[path_index] = tuple(sequence)
        vertices.update(sequence)
        edges.update(edge(u, v) for u, v in zip(sequence, sequence[1:]))
    require(connected(vertices, edges), "physical doubled-C4 core is disconnected")
    require(graph_rank(vertices, edges) == 3, "physical core rank changed")
    return vertices, edges, paths, target


def add_triangle(vertices, edges, triangles, owner, label):
    left = ("triangle", label, 0)
    right = ("triangle", label, 1)
    require(owner in vertices and left not in vertices and right not in vertices,
            "triangle attachment is not a one-cut extension")
    triangle = frozenset((owner, left, right))
    vertices.update((left, right))
    edges.update((edge(owner, left), edge(left, right), edge(right, owner)))
    triangles.append(triangle)
    return left, right


def realize(row, record, connector_lengths):
    vertices, edges, paths, target = build_core(row, connector_lengths)
    triangles = []
    intrinsic = []

    # Each physical doubled fibre has one direct odd member and one two-edge
    # even member.  Their union is exactly one K3, never Theta(1,2,2).
    for fibre in M.DOUBLED_FIBRES:
        even_member = next(index for index in fibre if row[index] == "0")
        odd_member = next(index for index in fibre if row[index] == "1")
        require(len(paths[even_member]) == 3 and len(paths[odd_member]) == 2,
                "doubled fibre left first-simple {2,1} scope")
        left, right = paths[odd_member]
        interior = paths[even_member][1]
        require(set(paths[even_member][::2]) == {left, right},
                "parallel members have incompatible endpoints")
        triangle = frozenset((left, right, interior))
        triangle_edges = {edge(u, v) for u, v in itertools.combinations(triangle, 2)}
        require(triangle_edges <= edges,
                "first-simple doubled fibre is not an actual K3")
        triangles.append(triangle)
        intrinsic.append(triangle)

    label_to_token = {label: token for token, label in target["token_to_label"].items()}

    def physical_owner(label):
        kind, index = label_to_token[label]
        if kind == "branch":
            return ("branch", index)
        require(kind == "interior" and len(paths[index]) == 3,
                "legal interior owner is not unique")
        return paths[index][1]

    serial = iter(range(3))
    kind = record[0]
    top_owner_vertices = []
    if kind == "direct3":
        for root in record[1]:
            owner = physical_owner(root)
            top_owner_vertices.append(owner)
            add_triangle(vertices, edges, triangles, owner, next(serial))
    elif kind == "chain2+direct":
        upstream = physical_owner(record[1])
        direct = physical_owner(record[2])
        top_owner_vertices.extend((upstream, direct))
        first, _ = add_triangle(vertices, edges, triangles, upstream, next(serial))
        add_triangle(vertices, edges, triangles, first, next(serial))
        add_triangle(vertices, edges, triangles, direct, next(serial))
    elif kind == "fork":
        upstream = physical_owner(record[1])
        top_owner_vertices.append(upstream)
        first, second = add_triangle(
            vertices, edges, triangles, upstream, next(serial)
        )
        child_roots = (first, first) if record[2] == "same" else (first, second)
        add_triangle(vertices, edges, triangles, child_roots[0], next(serial))
        add_triangle(vertices, edges, triangles, child_roots[1], next(serial))
    elif kind == "chain3":
        upstream = physical_owner(record[1])
        top_owner_vertices.append(upstream)
        first, _ = add_triangle(vertices, edges, triangles, upstream, next(serial))
        second, _ = add_triangle(vertices, edges, triangles, first, next(serial))
        add_triangle(vertices, edges, triangles, second, next(serial))
    else:
        raise AuditError(f"unknown incidence record {record!r}")
    require(len(triangles) == 5 and len(intrinsic) == 2,
            "realized cycle-block count changed")
    return vertices, edges, paths, target, tuple(triangles), tuple(intrinsic), tuple(top_owner_vertices)


def add_rooted_owner_witnesses(vertices, edges):
    """Attach a nontrivial one-root tree at every current physical vertex."""
    physical = tuple(sorted(vertices, key=repr))
    owner_classes = {}
    for root in physical:
        child = ("owned-tree", root, 0)
        grandchild = ("owned-tree", root, 1)
        require(child not in vertices and grandchild not in vertices,
                "rooted owner witness collision")
        vertices.update((child, grandchild))
        edges.update((edge(root, child), edge(child, grandchild)))
        owner_classes[root] = frozenset((root, child, grandchild))
    require(set().union(*owner_classes.values()) == vertices,
            "rooted owner classes omit a witness vertex")
    require(sum(map(len, owner_classes.values())) == len(vertices),
            "rooted owner classes duplicate a witness vertex")
    return owner_classes


def triangle_edges(triangle):
    return frozenset(edge(left, right)
                     for left, right in itertools.combinations(triangle, 2))


def validate_shared_cut_side(side, all_edges, side_triangles):
    side_edges = induced_edges(all_edges, side)
    require(connected(side, side_edges), "induced side is disconnected")
    require(side_triangles, "side has no cyclic block")
    require(len(set(side_triangles)) == len(side_triangles),
            "cycle block was duplicated")
    for left, right in itertools.combinations(side_triangles, 2):
        require(len(left & right) <= 1, "two triangle blocks share an edge")

    expected_blocks = {triangle_edges(triangle) for triangle in side_triangles}
    blocks = biconnected_edge_blocks(side, side_edges)
    cyclic_blocks = {block for block in blocks if len(block) > 1}
    require(cyclic_blocks == expected_blocks,
            "side has an omitted, invented, or nontriangular cyclic block")
    require(all(len(block) == 1 or block in expected_blocks for block in blocks),
            "side has a non-cycle non-bridge block")

    intersection = set()
    for first, second in itertools.combinations(range(len(side_triangles)), 2):
        if side_triangles[first] & side_triangles[second]:
            intersection.add(edge(first, second))
    cycle_nodes = set(range(len(side_triangles)))
    require(connected(cycle_nodes, intersection) if len(cycle_nodes) > 1 else True,
            "triangle intersection graph is disconnected")
    rank = graph_rank(side, side_edges)
    require(rank == len(side_triangles),
            "side rank is not its exact triangle-block count")
    return {
        "rank": rank,
        "cycles": len(side_triangles),
        "cycle_lengths": (3,) * len(side_triangles),
        "shared_cut_cluster": True,
        "blocks": blocks,
    }


def transported_remnants(row, vertex_map, edge_map, open_pair, cut_pair):
    symbolic = M.transport_symbolic_paths(row, vertex_map, edge_map)
    source_geometry = M.target_geometry(M.BASE)
    result = {}
    for source_edge, pair in (
        (source_geometry["open_connector"], open_pair),
        (source_geometry["cut_connector"], cut_pair),
    ):
        ledger = symbolic[source_edge]
        target_pair = pair if ledger["orientation"] == "forward" else tuple(reversed(pair))
        result[ledger["role"]] = (ledger["target_edge"], target_pair)
    require(set(result) == {"open", "cut"},
            "transported remnant roles are incomplete")
    return result


def physical_split(row, record, vertex_map, edge_map, source_open_pair, source_cut_pair):
    remnants = transported_remnants(
        row, vertex_map, edge_map, source_open_pair, source_cut_pair
    )
    open_edge, open_pair = remnants["open"]
    cut_edge_index, cut_pair = remnants["cut"]
    open_length = sum(open_pair) + 2
    cut_length = sum(cut_pair) + 1
    connector_lengths = {open_edge: open_length, cut_edge_index: cut_length}
    (vertices, edges, paths, target, triangles, intrinsic,
     top_owner_vertices) = realize(row, record, connector_lengths)

    open_position = open_pair[0] + 1
    cut_position = cut_pair[0]
    opened_vertex = paths[open_edge][open_position]
    actual_cut_edge = edge(
        paths[cut_edge_index][cut_position],
        paths[cut_edge_index][cut_position + 1],
    )
    expected_open_cross = {
        edge(opened_vertex, paths[open_edge][open_position - 1]),
        edge(opened_vertex, paths[open_edge][open_position + 1]),
    }
    require(actual_cut_edge in edges and expected_open_cross <= edges,
            "prescribed physical cut/open incidence is absent")

    owner_classes = add_rooted_owner_witnesses(vertices, edges)
    opened_territory = set(owner_classes[opened_vertex])
    opened_edges = induced_edges(edges, opened_territory)
    require(is_tree(opened_territory, opened_edges),
            "opened owner territory is not a nonempty induced tree")

    retained_vertices = set(vertices) - opened_territory
    retained_edges = induced_edges(edges, retained_vertices)
    require(connected(retained_vertices, retained_edges),
            "opening did not leave the odd connector as the unique sector route")
    require(graph_rank(vertices, edges) == 6,
            "retained R31-S graph H lost rank six")
    require(graph_rank(retained_vertices, retained_edges) == 5,
            "physical opening did not lower rank six to rank five")
    require(actual_cut_edge in retained_edges,
            "odd-connector cut edge was lost with the opening territory")

    separated_edges = retained_edges - {actual_cut_edge}
    sides = components(retained_vertices, separated_edges)
    require(len(sides) == 2,
            "cutting an actual odd-connector edge did not make exactly two sectors")
    side_zero = next(side for side in sides if ("branch", 0) in side)
    side_one = next(side for side in sides if ("branch", 2) in side)
    require(side_zero != side_one and
            {("branch", 0), ("branch", 1)} <= side_zero and
            {("branch", 2), ("branch", 3)} <= side_one,
            "doubled-fibre endpoint sectors changed")

    territories = (frozenset(opened_territory), side_zero, side_one)
    require(set().union(*territories) == vertices,
            "induced territories omit a vertex")
    require(sum(map(len, territories)) == len(vertices),
            "induced territories duplicate a vertex")
    for owner, owner_class in owner_classes.items():
        containing = [territory for territory in territories if owner in territory]
        require(len(containing) == 1 and owner_class <= containing[0],
                "a rooted owner class was split, omitted, or duplicated")

    cross_edges = {
        current for current in edges
        if sum(bool(current <= territory) for territory in territories) == 0
    }
    require(cross_edges == expected_open_cross | {actual_cut_edge},
            "territory boundary has an omitted or invented cross-edge")
    require(sum(any(endpoint in side_zero for endpoint in current)
                for current in expected_open_cross) == 1 and
            sum(any(endpoint in side_one for endpoint in current)
                for current in expected_open_cross) == 1,
            "even-connector remnants do not attach one per endpoint sector")
    require(any(endpoint in side_zero for endpoint in actual_cut_edge) and
            any(endpoint in side_one for endpoint in actual_cut_edge),
            "odd cut edge does not cross the two induced sectors")

    side_triangles = []
    for side in (side_zero, side_one):
        current = tuple(triangle for triangle in triangles if triangle <= side)
        require(all(sum(bool(triangle <= territory) for territory in territories) == 1
                    for triangle in current),
                "a side triangle is not uniquely owned")
        side_triangles.append(current)
    require(sum(map(len, side_triangles)) == len(triangles),
            "a physical triangle block was split or omitted")
    profiles = tuple(
        validate_shared_cut_side(side, edges, current)
        for side, current in zip((side_zero, side_one), side_triangles)
    )
    # Physical certificate that every connector remnant and owner-witness
    # branch is forest material, never an inter-cluster route: all nontriangle
    # blocks are bridges, while connectedness of the triangle-intersection graph
    # above is witnessed solely by actual shared vertices of triangle blocks.
    for side, profile, current in zip(
            (side_zero, side_one), profiles, side_triangles):
        side_edges = induced_edges(edges, side)
        cyclic_edges = set().union(*(triangle_edges(triangle) for triangle in current))
        bridge_edges = set().union(*(block for block in profile["blocks"]
                                     if len(block) == 1), set())
        require(cyclic_edges.isdisjoint(bridge_edges),
                "cyclic edge was also classified as a bridge")
        require(cyclic_edges | bridge_edges == side_edges,
                "triangle and bridge blocks do not exhaust the induced side")
        require(all(len(block) == 1 for block in profile["blocks"]
                    if block.isdisjoint(cyclic_edges)),
                "noncyclic side material is not a forest of bridge blocks")
    require(sum(profile["rank"] for profile in profiles) == 5,
            "side ranks do not exhaust the opened rank-five graph")

    # Every top-level owner and all nested descendants must follow one sector.
    require(all(owner in side_zero or owner in side_one for owner in top_owner_vertices),
            "top-level triangle owner escaped both sectors")
    oriented_rank_pair = tuple(profile["rank"] for profile in profiles)
    actual_rank_pair = tuple(sorted(oriented_rank_pair))
    actual_class = "balanced-2+3" if actual_rank_pair == (2, 3) else "one-sided-1+4"
    require(oriented_rank_pair in {(1, 4), (2, 3), (3, 2), (4, 1)},
            "unexpected physical side-rank profile")

    old_label = M.source_classification(record)
    if old_label == "balanced":
        require(actual_class == "balanced-2+3",
                "old balanced label does not realize two shared-cut clusters")
    else:
        require(actual_class == "one-sided-1+4",
                "old one-sided label does not realize rank 1+4")

    # The analytic scope check is label-independent.  Every rank-four side,
    # whether formerly called C4 or D3, must satisfy the *statement-level*
    # hypotheses at theorem lines 7--16: a cactus with exactly four actual
    # triangle blocks in one shared-cut cluster, plus only bridge/tree blocks.
    # This deliberately does not rely on the narrower branch-owner census of
    # the old C4 verifier.
    if 4 in actual_rank_pair:
        rank_four = next(index for index, profile in enumerate(profiles)
                         if profile["rank"] == 4)
        rank_four_side = (side_zero, side_one)[rank_four]
        rank_four_triangles = side_triangles[rank_four]
        require(len(rank_four_triangles) == 4 and
                profiles[rank_four]["cycles"] == 4 and
                profiles[rank_four]["cycle_lengths"] == (3, 3, 3, 3),
                "rank-four side is not exactly four actual triangle blocks")
        require(profiles[rank_four]["shared_cut_cluster"],
                "rank-four triangle intersection graph is disconnected")
        require(all(len(block) in {1, 3} for block in profiles[rank_four]["blocks"]),
                "rank-four side contains a hidden diamond/noncactus block")
        require(sum(len(block) == 3 for block in profiles[rank_four]["blocks"]) == 4,
                "rank-four side cyclic-block multiplicity changed")

    if old_label == "D3":
        interior_top_owners = {
            owner for owner in top_owner_vertices
            if type(owner) is tuple and owner and owner[0] == "path" and
            owner[1] in target["doubled_even"]
        }
        require(interior_top_owners and interior_top_owners <= rank_four_side,
                "D3 label lost its physical interior top owner")

    return {
        "profiles": profiles,
        "oriented_rank_pair": oriented_rank_pair,
        "actual_class": actual_class,
        "old_label": old_label,
        "record_shape": record[0],
        "triangles": triangles,
        "intrinsic": intrinsic,
        "territories": territories,
        "edges": edges,
        "paths": paths,
        "target": target,
        "opened_vertex": opened_vertex,
        "cut_edge": actual_cut_edge,
    }


def audit_pinned_counterexample():
    identity = ((0, 1, 2, 3), (0, 1, 2, 3, 4, 5))
    record = ("direct3", ("x", "x", "x"))
    require(M.source_classification(record) == "D3",
            "pinned direct3(x,x,x) record lost D3 label")
    result = physical_split(M.BASE, record, *identity, (0, 0), (0, 0))
    rank_four_index = next(index for index, profile in enumerate(result["profiles"])
                           if profile["rank"] == 4)
    rank_four_side = result["territories"][rank_four_index + 1]
    core = frozenset({("branch", 0), ("branch", 1), ("path", 0, 1)})
    exact_core_edges = {edge(left, right) for left, right in itertools.combinations(core, 2)}
    require(core <= rank_four_side and exact_core_edges <= result["edges"],
            "pinned owner-side intrinsic K3 changed")
    require(not any(vertex == ("branch", "z") for vertex in rank_four_side),
            "invented diamond vertex entered pinned physical side")
    expected_cycles = {core}
    for label in range(3):
        expected_cycles.add(frozenset({
            ("path", 0, 1), ("triangle", label, 0), ("triangle", label, 1),
        }))
    actual_cycles = {triangle for triangle in result["triangles"] if triangle <= rank_four_side}
    require(actual_cycles == expected_cycles,
            "pinned direct3(x,x,x) exact cycle listing changed")
    return result


def expect_rejection(action, label):
    try:
        action()
    except (AuditError, KeyError, StopIteration, TypeError, ValueError):
        return
    raise AuditError(f"hostile mutation accepted: {label}")


def hostile_topology_tests():
    rejected = 0

    # A physical K3 plus an invented second A-B two-edge route is a diamond;
    # it must not pass the registered-triangle block audit.
    vertices = {"A", "B", "x", "z"}
    edges = {edge("A", "B"), edge("A", "x"), edge("B", "x"),
             edge("A", "z"), edge("B", "z")}
    expect_rejection(
        lambda: validate_shared_cut_side(
            frozenset(vertices), edges, (frozenset(("A", "B", "x")),)
        ),
        "invented diamond vertex",
    )
    rejected += 1

    # Two triangular cyclic blocks joined only by a bridge are a connected
    # cactus but not one shared-cut cluster.
    vertices = {0, 1, 2, 3, 4, 5}
    triangles = (frozenset((0, 1, 2)), frozenset((3, 4, 5)))
    edges = set().union(*(triangle_edges(triangle) for triangle in triangles))
    edges.add(edge(2, 3))
    expect_rejection(
        lambda: validate_shared_cut_side(frozenset(vertices), edges, triangles),
        "bridge-separated triangles",
    )
    rejected += 1

    expect_rejection(lambda: canonical_remnant_pair(0, 3),
                     "opposite-parity remnant pair")
    rejected += 1
    expect_rejection(lambda: canonical_remnant_pair(-1, 1),
                     "negative remnant length")
    rejected += 1

    # A one-sided cycle list with one omitted block must fail exact block equality.
    vertices = {0, 1, 2, 3, 4}
    triangles = (frozenset((0, 1, 2)), frozenset((0, 3, 4)))
    edges = set().union(*(triangle_edges(triangle) for triangle in triangles))
    expect_rejection(
        lambda: validate_shared_cut_side(
            frozenset(vertices), edges, (triangles[0],)
        ),
        "omitted physical triangle block",
    )
    rejected += 1
    return rejected


def audit():
    audit_sources()
    audit_symbolic_remnant_reduction()
    independent = independent_records()
    imported, imported_shapes = M.base_records()
    require(independent == imported,
            "committed record universe differs from independent regeneration")
    require(imported_shapes == Counter(record[0] for record in independent),
            "committed record shape counts differ from independent regeneration")

    automorphisms = M.genuine_kernel_automorphisms()
    require(len(automorphisms) == 16, "genuine automorphism count changed")
    profile_counts = Counter()
    old_label_counts = Counter()
    actual_counts = Counter()
    d3_shape_counts = Counter()
    oriented_base_rank_counts = Counter()
    oriented_transport_rank_counts = Counter()
    audits = 0

    identity = ((0, 1, 2, 3), (0, 1, 2, 3, 4, 5))
    for record in sorted(independent, key=repr):
        baseline = physical_split(M.BASE, record, *identity, (0, 0), (0, 0))
        oriented_base_rank_counts[baseline["oriented_rank_pair"]] += 1
    require(oriented_base_rank_counts == Counter({
        (1, 4): 28, (2, 3): 27, (3, 2): 27, (4, 1): 28,
    }), "oriented 110-record base rank ledger changed")

    for row in M.EXPECTED_ANCHORS:
        witnesses = tuple(
            witness for witness in automorphisms
            if M.act_on_row(M.BASE, witness[1]) == row
        )
        require(len(witnesses) == 2, f"{row}: witness count changed")
        for vertex_map, edge_map in witnesses:
            owner_map, _, _ = M.owner_transport(row, vertex_map, edge_map)
            for source_record in sorted(independent, key=repr):
                transported_record = M.transport_record(source_record, owner_map)
                for open_pair in REMNANT_CASES:
                    for cut_pair in REMNANT_CASES:
                        result = physical_split(
                            row, transported_record, vertex_map, edge_map,
                            open_pair, cut_pair,
                        )
                        ranks = tuple(sorted(profile["rank"]
                                             for profile in result["profiles"]))
                        clusters = tuple(sorted(profile["shared_cut_cluster"]
                                                for profile in result["profiles"]))
                        key = (result["old_label"], ranks, clusters)
                        profile_counts[key] += 1
                        old_label_counts[result["old_label"]] += 1
                        actual_counts[result["actual_class"]] += 1
                        oriented_transport_rank_counts[result["oriented_rank_pair"]] += 1
                        if result["old_label"] == "D3":
                            d3_shape_counts[result["record_shape"]] += 1
                        audits += 1

    multiplier = 16 * len(REMNANT_CASES) ** 2
    require(audits == 8 * 2 * 110 * 25,
            "parametric transported physical split count changed")
    require(old_label_counts == Counter({
        "balanced": 54 * multiplier,
        "C4": 28 * multiplier,
        "D3": 28 * multiplier,
    }), "transported old-label totals changed")
    require(actual_counts == Counter({
        "balanced-2+3": 54 * multiplier,
        "one-sided-1+4": 56 * multiplier,
    }), "actual induced-topology totals changed")
    require(oriented_transport_rank_counts == Counter({
        (1, 4): 28 * multiplier, (2, 3): 27 * multiplier,
        (3, 2): 27 * multiplier, (4, 1): 28 * multiplier,
    }), "oriented transported rank-pair ledger changed")
    require(profile_counts == Counter({
        ("balanced", (2, 3), (True, True)): 54 * multiplier,
        ("C4", (1, 4), (True, True)): 28 * multiplier,
        ("D3", (1, 4), (True, True)): 28 * multiplier,
    }), "physical induced-side profile changed")
    require(d3_shape_counts == Counter({
        "direct3": 12 * multiplier,
        "chain2+direct": 10 * multiplier,
        "fork": 4 * multiplier,
        "chain3": 2 * multiplier,
    }), "D3 repeated/nested shape coverage changed")

    pinned = audit_pinned_counterexample()
    rejected = hostile_topology_tests()
    return {
        "audits": audits,
        "old": old_label_counts,
        "actual": actual_counts,
        "profiles": profile_counts,
        "d3_shapes": d3_shape_counts,
        "oriented_base_ranks": oriented_base_rank_counts,
        "oriented_transport_ranks": oriented_transport_rank_counts,
        "pinned": pinned,
        "rejected": rejected,
    }


def report(result):
    lines = [
        "R31-S OPEN induced-topology hostile audit: physical audit passed; closure BLOCKED",
        "pinned sources: transport/D3/C4 executables + packing-two/C4 theorems + frontier/upstream owner prose",
        "symbolic connector remnants: 5 open classes * 5 cut classes; arbitrary positive segments are one-root path subdivisions",
        f"physical split audits: {result['audits']} = 8 anchors * 2 witnesses * 110 records * 25 remnant classes",
        "old labels: balanced=21600 C4=11200 D3=11200",
        "110 base records, oriented ranks: (1,4)=28 (2,3)=27 (3,2)=27 (4,1)=28; no forced 4+1 claim",
        "44,000 transported/remnant probes: unordered ranks (2,3)=21600; (1,4)=22400",
        "former D3 shapes: direct3=4800 chain2+direct=4000 fork=1600 chain3=800",
        "every split: H rank 6; opened complement rank 5; induced sides exhaustive; opened owner territory is a nonempty tree",
        "every side: exact triangular biconnected blocks; connected actual triangle-intersection graph; all other blocks are bridges",
        "pinned direct3(x,x,x): cyclic hull edges AB,Ax,Bx and x-ui,ui-vi,vi-x (i=1,2,3); cycles K3 plus three x-petals",
        "semantic verdict: D3 diamond vertex z has no physical preimage; the old C4/D3 distinction is not an induced-topology distinction",
        f"hostile topology/remnant mutations rejected: {result['rejected']}",
        "conditional ledger only: if upstream derives distinct induced trees S,T, then side sum >3 gives sigma(H)>2 and sigma(G)>1",
        "blocker: this checker models T and imports S from prose; it does not derive either owner class from the full parent graph",
        "status: OPEN physical audit; BLOCKED as R31-S closure; no theorem/ledger promotion",
    ]
    return "\n".join(lines)


def main():
    result = audit()
    output = report(result)
    if "--optimized-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run(
            [sys.executable, "-O", __file__, "--optimized-child"],
            check=False, capture_output=True, text=True,
        )
        require(child.returncode == 0, "optimized hostile audit failed")
        require(child.stderr == "", "optimized hostile audit wrote stderr")
        require(child.stdout.rstrip() == output,
                "normal/optimized hostile audit receipts differ")
    print(output)


if __name__ == "__main__":
    main()
