#!/usr/bin/env python3
"""Standalone physical-parent gate for the R31-S doubled-C4 residual.

This verifier starts before the historical 110-record stream.  It generates
canonical rooted block forests on the actual distinguished block B and four
external triangle blocks, realizes every accepted parent as a simple graph,
and authenticates the dispatch/partition predicates from reconstructed
adjacency.  It is deliberately independent of theorem/master/state files.

The finite generation is only the positive-rank skeleton.  A parent certificate
also permits recursively nested TREE and BRIDGE_ROUTE payloads.  The checker
validates these by parent pointers and the identities |E|=|V|-1 for every
one-root TREE payload and one bridge per route step.  Induction on the finite
parent tree then covers arbitrary depth: suppressing a leaf payload preserves
all cyclic blocks and rank, and every nonskeleton vertex has one first physical
owner.  Thus TREE symbols are not a bounded decoration sample.
"""

from __future__ import annotations

import itertools
import math
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass


class GateError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise GateError(message)


def edge(left, right):
    require(left != right, "loop requested")
    return frozenset((left, right))


def induced_edges(edges, vertices):
    return {current for current in edges if current <= vertices}


def adjacency(vertices, edges):
    result = {vertex: set() for vertex in vertices}
    for current in edges:
        require(len(current) == 2, "malformed edge")
        left, right = tuple(current)
        require(left in result and right in result, "edge endpoint escaped vertex set")
        result[left].add(right)
        result[right].add(left)
    return result


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
    """Tarjan edge-stack decomposition (bridges are singleton blocks)."""
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

    for root in sorted(vertices, key=repr):
        if root not in discovery:
            visit(root)
            require(not stack, "Tarjan stack leaked between components")
    require((set().union(*blocks) if blocks else set()) == set(edges),
            "Tarjan blocks do not exhaust edges")
    require(sum(map(len, blocks)) == len(edges), "Tarjan blocks duplicate an edge")
    return tuple(blocks)


# Physical doubled-C4 path order a,A,b,c,C,d.
ENDPOINTS = ((0, 1), (0, 1), (1, 2), (2, 3), (2, 3), (3, 0))
DOUBLED = ((0, 1), (3, 4))
CONNECTORS = (2, 5)
BASE_ROW = "010011"
LEGAL_OWNER_COUNT = 6
TRIANGLES = tuple(range(4))


@dataclass(frozen=True)
class Parent:
    """One canonical no-hull-bridge positive-rank parent.

    entries[i]=(parent,slot).  parent=-1 means B and slot is an actual B site;
    otherwise parent is another triangle and slot is one of its two private
    vertices.  A shared owner/cut is represented by repeated equal slots.
    """

    entries: tuple[tuple[int, int], ...]


def all_rooted_parent_functions():
    answer = []
    for parents in itertools.product(range(-1, 4), repeat=4):
        if any(parents[index] == index for index in TRIANGLES):
            continue
        valid = True
        for start in TRIANGLES:
            seen = set()
            current = start
            while current != -1:
                if current in seen:
                    valid = False
                    break
                seen.add(current)
                current = parents[current]
        if valid:
            answer.append(parents)
    require(len(answer) == 125, "rooted labelled tree count changed")
    return tuple(answer)


ROOTED_PARENT_FUNCTIONS = all_rooted_parent_functions()


def canonical_parent(parents, slots, owner_count):
    """Quotient triangle labels and independent reflection of each bare K3."""
    images = []
    for permutation in itertools.permutations(TRIANGLES):  # old -> new
        inverse = {permutation[old]: old for old in TRIANGLES}
        for flips in itertools.product(range(2), repeat=4):
            image = []
            for new in TRIANGLES:
                old = inverse[new]
                parent = parents[old]
                slot = slots[old]
                if parent != -1:
                    slot ^= flips[parent]
                image.append((-1 if parent == -1 else permutation[parent], slot))
            images.append(tuple(image))
    result = min(images)
    require(all((parent == -1 and 0 <= slot < owner_count) or
                (parent in TRIANGLES and slot in (0, 1))
                for parent, slot in result), "canonical parent left its slot domain")
    return Parent(result)


def generate_parents(owner_count):
    """Generate, then canonicalize, every rooted four-triangle block forest."""
    require(type(owner_count) is int and owner_count >= LEGAL_OWNER_COUNT,
            "invalid physical B-site count")
    records = {}
    for parents in ROOTED_PARENT_FUNCTIONS:
        domains = [range(owner_count if parent == -1 else 2) for parent in parents]
        for slots in itertools.product(*domains):
            record = canonical_parent(parents, slots, owner_count)
            records[record.entries] = record
    return tuple(records[key] for key in sorted(records))


def parent_depth(record, node):
    depth = 1
    current = record.entries[node][0]
    seen = {node}
    while current != -1:
        require(current not in seen, "parent cycle")
        seen.add(current)
        depth += 1
        current = record.entries[current][0]
    return depth


def children(record, node):
    return tuple(index for index, (parent, _) in enumerate(record.entries)
                 if parent == node)


def validate_parent_schema(record, owner_count):
    require(isinstance(record, Parent) and len(record.entries) == 4,
            "parent schema has wrong block set")
    for node, (parent, slot) in enumerate(record.entries):
        require(parent == -1 or parent in TRIANGLES, "unknown positive-rank parent")
        require(parent != node, "self-parent triangle")
        require((0 <= slot < owner_count) if parent == -1 else slot in (0, 1),
                "owner slot outside physical parent")
        parent_depth(record, node)
    # Four parent incidences plus B are a rooted tree on five cyclic block nodes.
    require(sum(parent == -1 for parent, _ in record.entries) >= 1,
            "positive-rank parent forest detached from B")
    return True


def deepest_q(record):
    """Deterministic actual maximum block-cut-depth triangle; necessarily a leaf."""
    depths = tuple(parent_depth(record, node) for node in TRIANGLES)
    maximum = max(depths)
    q = min(node for node in TRIANGLES if depths[node] == maximum)
    require(not children(record, q), "maximum-depth Q is not a leaf")
    return q


def retained_parent(record, q):
    remaining = tuple(node for node in TRIANGLES if node != q)
    relabel = {old: new for new, old in enumerate(remaining)}
    entries = []
    for old in remaining:
        parent, slot = record.entries[old]
        entries.append((-1 if parent == -1 else relabel[parent], slot))
    return tuple(entries)


def canonical_retained(entries):
    """Canonical three-block record, under K3 labels and private reflections."""
    images = []
    for permutation in itertools.permutations(range(3)):
        inverse = {permutation[old]: old for old in range(3)}
        for flips in itertools.product(range(2), repeat=3):
            image = []
            for new in range(3):
                old = inverse[new]
                parent, slot = entries[old]
                if parent != -1:
                    slot ^= flips[parent]
                image.append((-1 if parent == -1 else permutation[parent], slot))
            images.append(tuple(image))
    return min(images)


def retained_shape(entries):
    root_count = sum(parent == -1 for parent, _ in entries)
    child_counts = tuple(sum(parent == node for parent, _ in entries)
                         for node in range(3))
    if root_count == 3:
        return "direct3"
    if root_count == 2:
        return "chain2+direct"
    if root_count == 1 and max(child_counts) == 2:
        return "fork"
    require(root_count == 1, "retained parent is not rooted")
    return "chain3"


def retained_oriented_counts(entries):
    """Count retained triangles on the two physical doubled-fibre sides.

    Legal B sites 0,1,4 lie on source side zero and 2,3,5 on side one.
    Every nested block follows the side of its unique top ancestor.  The result
    is derived from the opened parent map, not imported from a 110-row fixture.
    """
    side_by_site = (0, 0, 1, 1, 0, 1)
    counts = [0, 0]
    for node in range(3):
        current = node
        seen = set()
        while entries[current][0] != -1:
            require(current not in seen, "retained parent cycle during side count")
            seen.add(current)
            current = entries[current][0]
        site = entries[current][1]
        require(0 <= site < LEGAL_OWNER_COUNT, "retained top owner is not legal")
        counts[side_by_site[site]] += 1
    require(sum(counts) == 3, "retained side allocation lost a triangle")
    return tuple(counts)


def no_bridge_count(owner_count):
    """Exact coefficient [z^4](1+z+2z^2+5z^3+13z^4)^m."""
    m = owner_count
    return (13 * m + 5 * m * (m - 1) + 4 * math.comb(m, 2)
            + 2 * m * math.comb(m - 1, 2) + math.comb(m, 4))


@dataclass
class PhysicalGraph:
    vertices: set
    edges: set
    b_edges: set
    paths: dict
    intrinsic: tuple
    external: tuple
    owner_sites: tuple


def build_core(even_length=2, odd_length=1):
    require(type(even_length) is int and even_length >= 2 and even_length % 2 == 0,
            "even connector is not positive even")
    require(type(odd_length) is int and odd_length >= 1 and odd_length % 2 == 1,
            "odd connector is not positive odd")
    lengths = [1 if bit == "1" else 2 for bit in BASE_ROW]
    even_connector = next(index for index in CONNECTORS if BASE_ROW[index] == "0")
    odd_connector = next(index for index in CONNECTORS if BASE_ROW[index] == "1")
    lengths[even_connector] = even_length
    lengths[odd_connector] = odd_length
    vertices = {("B", index) for index in range(4)}
    edges = set()
    paths = {}
    for path_index, ((left, right), length) in enumerate(zip(ENDPOINTS, lengths)):
        sequence = ([('B', left)]
                    + [("P", path_index, place) for place in range(1, length)]
                    + [('B', right)])
        paths[path_index] = tuple(sequence)
        vertices.update(sequence)
        edges.update(edge(left_vertex, right_vertex)
                     for left_vertex, right_vertex in zip(sequence, sequence[1:]))
    require(connected(vertices, edges) and graph_rank(vertices, edges) == 3,
            "physical B reconstruction changed")
    b_edges = set(edges)
    intrinsic = []
    legal_sites = [("B", index) for index in range(4)]
    for fibre in DOUBLED:
        even_member = next(index for index in fibre if BASE_ROW[index] == "0")
        odd_member = next(index for index in fibre if BASE_ROW[index] == "1")
        require(len(paths[even_member]) == 3 and len(paths[odd_member]) == 2,
                "doubled member left first-simple scope")
        triangle = frozenset(set(paths[even_member]) | set(paths[odd_member]))
        require(len(triangle) == 3 and
                {edge(left, right) for left, right in itertools.combinations(triangle, 2)} <= edges,
                "doubled fibre is not an actual triangle")
        intrinsic.append(triangle)
        legal_sites.append(paths[even_member][1])
    connector_interiors = tuple(
        vertex for path_index in CONNECTORS for vertex in paths[path_index][1:-1]
    )
    owner_sites = tuple(legal_sites) + connector_interiors
    require(len(owner_sites) == even_length + odd_length + 4,
            "actual B-site formula m=L_even+L_odd+4 changed")
    return PhysicalGraph(vertices, edges, b_edges, paths,
                         tuple(intrinsic), (), owner_sites)


def realize_parent(record, even_length=2, odd_length=1, bridge_routes=None,
                   tree_payloads=None):
    """Reconstruct actual adjacency, including optional routes/payload trees."""
    graph = build_core(even_length, odd_length)
    validate_parent_schema(record, len(graph.owner_sites))
    external = []
    triangle_private = {}
    for node, (parent, slot) in enumerate(record.entries):
        owner = graph.owner_sites[slot] if parent == -1 else triangle_private[parent][slot]
        left, right = ("Q", node, 0), ("Q", node, 1)
        require(owner in graph.vertices, "triangle owner is not yet physical")
        graph.vertices.update((left, right))
        graph.edges.update((edge(owner, left), edge(left, right), edge(right, owner)))
        external.append(frozenset((owner, left, right)))
        triangle_private[node] = (left, right)

    # A BRIDGE_ROUTE is a recursive parent chain replacing one parent incidence.
    # Nonempty routes are on the cyclic hull and must dispatch before residual.
    bridge_routes = {} if bridge_routes is None else bridge_routes
    route_vertices = {}
    for node, length in bridge_routes.items():
        require(node in TRIANGLES and type(length) is int and length >= 1,
                "malformed bridge route")
        triangle = external[node]
        owner = next(vertex for vertex in triangle
                     if vertex not in triangle_private[node])
        # Replace the two owner--private triangle edges by moving the complete
        # triangle to the end of an actual bridge path.  The end becomes its cut.
        left, right = triangle_private[node]
        graph.edges.remove(edge(owner, left))
        graph.edges.remove(edge(owner, right))
        previous = owner
        route = []
        for place in range(length):
            current = ("BR", node, place)
            graph.vertices.add(current)
            graph.edges.add(edge(previous, current))
            route.append(current)
            previous = current
        graph.edges.update((edge(previous, left), edge(previous, right)))
        external[node] = frozenset((previous, left, right))
        route_vertices[node] = tuple(route)

    # TREE payload: arbitrary finite rooted parent tree represented explicitly.
    # payload[root] is a tuple of parent indices; -1 means the physical root.
    tree_payloads = {} if tree_payloads is None else tree_payloads
    payload_vertices = {}
    for root, parent_map in tree_payloads.items():
        require(root in graph.vertices and isinstance(parent_map, tuple),
                "TREE payload has no physical root")
        created = []
        for index, parent_index in enumerate(parent_map):
            require(type(parent_index) is int and -1 <= parent_index < index,
                    "TREE parent order is not well founded")
            vertex = ("TREE", repr(root), index)
            parent = root if parent_index == -1 else created[parent_index]
            graph.vertices.add(vertex)
            graph.edges.add(edge(parent, vertex))
            created.append(vertex)
        owned = frozenset({root, *created})
        require(connected(owned, induced_edges(graph.edges, owned)) and
                len(induced_edges(graph.edges, owned)) == len(owned) - 1,
                "TREE payload is not one-root acyclic material")
        payload_vertices[root] = tuple(created)

    graph.external = tuple(external)
    require(connected(graph.vertices, graph.edges), "realized parent graph disconnected")
    expected_rank = 3 + 4
    require(graph_rank(graph.vertices, graph.edges) == expected_rank,
            "TREE/BRIDGE expansion changed total rank seven")
    return graph, route_vertices, payload_vertices


def clone_graph(graph):
    return PhysicalGraph(set(graph.vertices), set(graph.edges), set(graph.b_edges),
                         dict(graph.paths), tuple(graph.intrinsic),
                         tuple(graph.external), tuple(graph.owner_sites))


def recover_physical_inventory(graph):
    """Recover B, four K3 blocks, cuts, fibres and cyclic-hull bridges.

    No parent-map disposition is trusted here.  Tarjan runs on materialized
    adjacency.  B is authenticated by its exact physical edge set, every other
    cyclic block must be one K3, fibres are components after deleting E(B), and
    a singleton Tarjan block is on the cyclic hull exactly when both sides of
    its deletion contain a cyclic block.
    """
    blocks = biconnected_edge_blocks(graph.vertices, graph.edges)
    require(graph.b_edges in blocks, "physical B is not one maximal Tarjan block")
    other_cyclic = tuple(block for block in blocks
                         if len(block) > 1 and block != graph.b_edges)
    require(len(other_cyclic) == 4 and all(len(block) == 3 for block in other_cyclic),
            "Tarjan inventory is not B plus four K3 blocks")
    external_triangles = tuple(frozenset().union(*block) for block in other_cyclic)
    require(Counter(external_triangles) == Counter(graph.external),
            "Tarjan K3 inventory differs from reconstructed external blocks")

    without_b = graph.edges - graph.b_edges
    fibres = components(graph.vertices, without_b)
    require(all(connected(fibre, induced_edges(without_b, fibre)) for fibre in fibres),
            "B-deletion fibre is not connected")
    fibre_by_vertex = {vertex: fibre for fibre in fibres for vertex in fibre}

    hull_bridges = []
    for block in blocks:
        if len(block) != 1:
            continue
        current = next(iter(block))
        split = components(graph.vertices, graph.edges - {current})
        require(len(split) == 2, "singleton Tarjan block did not split graph")
        cycle_counts = tuple(sum(triangle <= side for triangle in
                                 (*graph.intrinsic, *external_triangles))
                             for side in split)
        if min(cycle_counts) >= 1:
            hull_bridges.append((current, split, cycle_counts))
    return {
        "blocks": blocks,
        "external": external_triangles,
        "fibres": fibres,
        "fibre_by_vertex": fibre_by_vertex,
        "hull_bridges": tuple(hull_bridges),
    }


def triangle_edge_set(triangle):
    return frozenset(edge(left, right)
                     for left, right in itertools.combinations(triangle, 2))


def audit_cyclic_blocks(vertices, edges, expected_triangles):
    blocks = biconnected_edge_blocks(vertices, edges)
    cyclic = {block for block in blocks if len(block) > 1}
    expected = {triangle_edge_set(triangle) for triangle in expected_triangles}
    require(cyclic == expected, "Tarjan cyclic blocks differ from actual triangles")
    require(all(len(block) == 1 or block in expected for block in blocks),
            "hidden nontriangle cyclic block")
    return blocks


def triangle_intersection_connected(triangles):
    if len(triangles) <= 1:
        return bool(triangles)
    vertices = set(range(len(triangles)))
    edges = {edge(left, right) for left, right in itertools.combinations(vertices, 2)
             if triangles[left] & triangles[right]}
    return connected(vertices, edges)


def descendant_nodes(record, root):
    answer = {root}
    changed = True
    while changed:
        changed = False
        for node, (parent, _) in enumerate(record.entries):
            if parent in answer and node not in answer:
                answer.add(node)
                changed = True
    return frozenset(answer)


def classify_parent(record, graph, bridge_routes, payload_vertices):
    """Classify from reconstructed adjacency: A bridge, B fibre, or C residual."""
    del bridge_routes, payload_vertices  # only adjacency may decide disposition.
    inventory = recover_physical_inventory(graph)
    if inventory["hull_bridges"]:
        # Dispatch the first actual hull bridge before any owner/Q choice.  B is
        # intact on its side, so a q-triangle away side leaves rank 7-q.
        current, sides, cycle_counts = min(inventory["hull_bridges"], key=repr)
        b_vertices = frozenset().union(*graph.b_edges)
        away = next(side for side in sides if not b_vertices <= side)
        q = sum(triangle <= away for triangle in inventory["external"])
        complement = set(graph.vertices) - set(away)
        complement_rank = graph_rank(complement, induced_edges(graph.edges, complement))
        require(q in cycle_counts and 1 <= q <= 4,
                "actual hull bridge has no away external triangle")
        require(complement_rank == 7 - q and 3 <= complement_rank <= 6,
                "hull-bridge rank formula 7-q failed")
        return {"case": "bridge", "q": q, "complement_rank": complement_rank,
                "formula": "7-q", "edge": current}

    connector_sites = tuple(vertex for connector in CONNECTORS
                            for vertex in graph.paths[connector][1:-1])
    require(len(connector_sites) == len(set(connector_sites)),
            "connector internal vertex registry overlaps")
    positive_fibres = []
    for site in connector_sites:
        fibre = inventory["fibre_by_vertex"][site]
        # Deleting E(B) leaves site inside its complete external owner fibre;
        # external K3s are wholly contained in that component.
        owned = tuple(triangle for triangle in inventory["external"]
                      if triangle <= fibre)
        if owned:
            positive_fibres.append((site, fibre, owned))
    if positive_fibres:
        # Complete actual B-deletion fibres of every internal vertex of BOTH
        # connectors are inspected; direct-parent metadata is irrelevant.
        site, fibre, owned = min(positive_fibres, key=lambda value: repr(value[0]))
        q = len(owned)
        complement = set(graph.vertices) - set(fibre)
        complement_rank = graph_rank(complement, induced_edges(graph.edges, complement))
        require(1 <= q <= 4 and complement_rank == 6 - q and 2 <= complement_rank <= 5,
                "connector-fibre rank formula 6-q failed")
        return {"case": "connector", "q": q,
                "complement_rank": complement_rank, "formula": "6-q",
                "site": site, "fibre": fibre}
    return {"case": "residual", "inventory": inventory}


def audit_residual(record, even_length=2, odd_length=1, tree_payloads=None):
    graph, routes, payload = realize_parent(
        record, even_length, odd_length, bridge_routes={}, tree_payloads=tree_payloads)
    disposition = classify_parent(record, graph, routes, payload)
    require(disposition["case"] == "residual", "nonclean parent entered residual")

    q = deepest_q(record)
    q_triangle = graph.external[q]
    parent, slot = record.entries[q]
    cut = (graph.owner_sites[slot] if parent == -1
           else next(iter(q_triangle - {("Q", q, 0), ("Q", q, 1)})))
    # S is the complete away component after deleting incidence cut--Q in the
    # block-cut tree, with the upstream cut omitted.  For maximum-depth Q this
    # is Q minus cut plus every TREE payload rooted there.
    s = set(q_triangle - {cut})
    frontier = list(s)
    graph_adj = adjacency(graph.vertices, graph.edges)
    while frontier:
        current = frontier.pop()
        for neighbor in graph_adj[current]:
            if neighbor != cut and neighbor not in s and neighbor not in set().union(*graph.intrinsic):
                # Stay in Q's away component; no other cyclic block can descend
                # from maximum-depth Q, but arbitrary TREE material can.
                if not any(neighbor in triangle and triangle != q_triangle
                           for triangle in graph.external):
                    s.add(neighbor)
                    frontier.append(neighbor)
    s = frozenset(s)
    require(cut not in s and connected(s, induced_edges(graph.edges, s)) and
            len(induced_edges(graph.edges, s)) == len(s) - 1,
            "S is not the cut-deleted complete away tree")

    even_connector = next(index for index in CONNECTORS if BASE_ROW[index] == "0")
    odd_connector = next(index for index in CONNECTORS if BASE_ROW[index] == "1")
    # Check complete F_v for every internal vertex of both connectors before
    # selecting the structural opening.  Residual cleanliness makes each fibre
    # acyclic; a hostile cyclic attachment must have dispatched above.
    fibres = {}
    cyclic_vertices = set().union(*graph.intrinsic, *graph.external)
    for connector in CONNECTORS:
        for vertex in graph.paths[connector][1:-1]:
            owned = {vertex, *payload.get(vertex, ())}
            fibre = frozenset(owned)
            require(connected(fibre, induced_edges(graph.edges, fibre)) and
                    len(induced_edges(graph.edges, fibre)) == len(fibre) - 1,
                    "complete connector fibre is not a tree")
            require(not (set(fibre) & (cyclic_vertices - {vertex})),
                    "connector fibre retained a cyclic descendant")
            fibres[vertex] = fibre
    require(all(vertex in fibres for connector in CONNECTORS
                for vertex in graph.paths[connector][1:-1]),
            "not every even/odd connector internal fibre was tested")
    require(graph.paths[even_connector][1:-1], "even connector has no opening vertex")
    opening = graph.paths[even_connector][1]  # any tested internal vertex works.
    t = fibres[opening]
    require(s.isdisjoint(t), "S and T overlap")

    retained = set(graph.vertices) - set(s) - set(t)
    retained_edges = induced_edges(graph.edges, retained)
    require(connected(retained, retained_edges), "G-(S union T) disconnected before odd cut")
    require(graph_rank(retained, retained_edges) == 5,
            "G-(S union T) does not have rank five")

    odd_edges = tuple(edge(left, right) for left, right in
                      zip(graph.paths[odd_connector], graph.paths[odd_connector][1:]))
    split_results = []
    for cut_edge in odd_edges:
        require(cut_edge in retained_edges, "actual odd-connector edge was deleted early")
        sides = components(retained, retained_edges - {cut_edge})
        require(len(sides) == 2, "actual odd-connector edge is not a bridge after S,T")
        ordered = []
        for intrinsic in graph.intrinsic:
            matches = [side for side in sides if intrinsic <= side]
            require(len(matches) == 1, "intrinsic side is ambiguous")
            ordered.append(matches[0])
        require(ordered[0] != ordered[1], "odd cut failed to separate intrinsic triangles")
        side_data = []
        for side in ordered:
            triangles = tuple(triangle for triangle in (*graph.intrinsic, *graph.external)
                              if triangle <= side)
            require(triangles, "U/V side has no triangle block")
            side_edges = induced_edges(graph.edges, side)
            blocks = audit_cyclic_blocks(side, side_edges, triangles)
            require(triangle_intersection_connected(triangles),
                    "U/V triangles are not one shared-cut cluster")
            rank = graph_rank(side, side_edges)
            require(rank == len(triangles), "U/V rank differs from side triangle count")
            side_data.append((rank, len(blocks)))
        ranks = tuple(rank for rank, _ in side_data)
        require(min(ranks) >= 1 and sum(ranks) == 5,
                "U,V ranks are not positive and summing five")
        split_results.append(ranks)

    require(set().union(s, t, *ordered) == set(graph.vertices) and
            sum(map(len, (s, t, *ordered))) == len(graph.vertices),
            "S,T,U,V are not disjoint and exhaustive")
    return {"q": q, "S": s, "T": t, "ranks": tuple(split_results),
            "retained": canonical_retained(retained_parent(record, q))}


def bridge_case_fixture(record):
    graph, routes, payload = realize_parent(record, bridge_routes={deepest_q(record): 2})
    result = classify_parent(record, graph, routes, payload)
    require(result["case"] == "bridge" and result["formula"] == "7-q",
            "bridge route did not preempt residual")
    return result


def tree_universality_audit():
    """Recursive parent maps witness arbitrary depth without a depth bound."""
    # These are hostile concrete depths only; universality is the well-founded
    # leaf induction checked in realize_parent for an arbitrary supplied tuple.
    probes = ((), (-1,), (-1, 0), (-1, -1, 1, 1, 3),
              tuple([-1] + list(range(0, 31))))
    for parent_map in probes:
        root = ("root", len(parent_map))
        vertices = {root}
        edges = set()
        made = []
        for index, parent_index in enumerate(parent_map):
            require(-1 <= parent_index < index, "symbolic TREE parent not well founded")
            vertex = ("payload", len(parent_map), index)
            parent = root if parent_index == -1 else made[parent_index]
            vertices.add(vertex)
            edges.add(edge(parent, vertex))
            made.append(vertex)
        require(connected(vertices, edges) and len(edges) == len(vertices) - 1,
                "TREE parent invariant failed")
    return len(probes)


def expect_rejection(action, label):
    try:
        action()
    except (GateError, KeyError, IndexError, StopIteration, TypeError, ValueError):
        return label
    raise GateError(f"hostile mutation accepted: {label}")


def exact_connector_owner_hostile_graph():
    """The 15-vertex all-in-one-connector-fibre adjacency mutation."""
    a, b, c, d, x, y, v = "A", "B", "C", "D", "x", "y", "v"
    vertices = {a, b, c, d, x, y, v}
    b_edges = {
        edge(a, b), edge(a, x), edge(x, b),
        edge(c, d), edge(c, y), edge(y, d),
        edge(b, v), edge(v, c), edge(d, a),
    }
    edges = set(b_edges)
    external = []
    for index in range(1, 5):
        left, right = f"p{index}", f"q{index}"
        vertices.update((left, right))
        triangle = frozenset((v, left, right))
        external.append(triangle)
        edges |= set(triangle_edge_set(triangle))
    intrinsic = (frozenset((a, b, x)), frozenset((c, d, y)))
    graph = PhysicalGraph(vertices, edges, b_edges, {
        2: (b, v, c), 5: (d, a),
    }, intrinsic, tuple(external), (a, b, c, d, x, y, v))
    require(len(vertices) == 15 and len(edges) == 21 and graph_rank(vertices, edges) == 7,
            "15-vertex connector hostile graph changed")
    result = classify_parent(None, graph, {}, {})
    require(result["case"] == "connector" and result["q"] == 4 and
            result["complement_rank"] == 2 and result["formula"] == "6-q",
            "exact connector hostile graph escaped Case B")
    return graph, result


def exact_hull_bridge_hostile_graph():
    """The 16-vertex priority mutation with a three-triangle away side."""
    a, b, c, d, x, y, v, z = "A", "B", "C", "D", "x", "y", "v", "z"
    vertices = {a, b, c, d, x, y, v, z}
    b_edges = {
        edge(a, b), edge(a, x), edge(x, b),
        edge(c, d), edge(c, y), edge(y, d),
        edge(b, v), edge(v, c), edge(d, a),
    }
    edges = set(b_edges) | {edge(y, z)}
    triangles = (
        frozenset((z, "a1", "b1")),
        frozenset(("a1", "a2", "b2")),
        frozenset(("b1", "a3", "b3")),
        frozenset((y, "a4", "b4")),
    )
    for triangle in triangles:
        vertices |= set(triangle)
        edges |= set(triangle_edge_set(triangle))
    intrinsic = (frozenset((a, b, x)), frozenset((c, d, y)))
    graph = PhysicalGraph(vertices, edges, b_edges, {
        2: (b, v, c), 5: (d, a),
    }, intrinsic, triangles, (a, b, c, d, x, y, v))
    require(len(vertices) == 16 and len(edges) == 22 and graph_rank(vertices, edges) == 7,
            "16-vertex bridge hostile graph changed")
    result = classify_parent(None, graph, {}, {})
    require(result["case"] == "bridge" and result["q"] == 3 and
            result["complement_rank"] == 4 and result["formula"] == "7-q",
            "exact bridge hostile graph escaped Case A priority")
    return graph, result


def hostile_tests(clean_parent, connector_parent, retained_side_counts):
    labels = []
    labels.append(expect_rejection(
        lambda: validate_parent_schema(Parent(clean_parent.entries + ((-1, 0),)), 6),
        "synthetic fifth triangle"))
    cycle = list(clean_parent.entries)
    cycle[0] = (1, 0)
    cycle[1] = (0, 0)
    labels.append(expect_rejection(
        lambda: validate_parent_schema(Parent(tuple(cycle)), 6), "parent cycle"))
    detached = Parent(tuple((node, 0) for node in TRIANGLES))
    labels.append(expect_rejection(
        lambda: validate_parent_schema(detached, 6), "detached/self parents"))
    labels.append(expect_rejection(
        lambda: realize_parent(clean_parent, tree_payloads={('B', 0): (-1, 2)}),
        "non-well-founded TREE"))

    # Adjacency-level defects are rejected by fresh Tarjan inventory, not by
    # parent metadata: delete a K3 edge; add an inter-block chord; cyclicize a
    # purported TREE payload.
    clean_graph, _, _ = realize_parent(clean_parent)
    missing_edge = clone_graph(clean_graph)
    missing_edge.edges.remove(next(iter(triangle_edge_set(missing_edge.external[0]))))
    labels.append(expect_rejection(
        lambda: recover_physical_inventory(missing_edge),
        "adjacency missing triangle edge"))
    extra_chord = clone_graph(clean_graph)
    left = next(vertex for vertex in extra_chord.external[0]
                if vertex[0] == "Q")
    right = next(vertex for vertex in extra_chord.external[1]
                 if vertex[0] == "Q" and vertex != left)
    extra_chord.edges.add(edge(left, right))
    labels.append(expect_rejection(
        lambda: recover_physical_inventory(extra_chord),
        "adjacency inter-block chord"))
    cyclic_tree, _, tree_vertices = realize_parent(
        clean_parent, tree_payloads={('B', 0): (-1, 0, 0)})
    cyclic_tree.edges.add(edge(tree_vertices[('B', 0)][1],
                               tree_vertices[('B', 0)][2]))
    labels.append(expect_rejection(
        lambda: recover_physical_inventory(cyclic_tree),
        "adjacency cyclic TREE payload"))

    # A connector-attached cyclic fibre must dispatch, not enter residual/T-tree.
    labels.append(expect_rejection(
        lambda: audit_residual(connector_parent), "unconditional connector T-tree"))
    connector_hostile_graph, connector_hostile = exact_connector_owner_hostile_graph()
    labels.append(expect_rejection(
        lambda: require(classify_parent(None, connector_hostile_graph, {}, {})["case"]
                        == "residual", "15-vertex fibre is connector-positive"),
        "15-vertex partial connector fibre"))

    # A real hull bridge must preempt connector/Q handling on reconstructed
    # adjacency; ordinary side connectedness cannot replace shared-cut contact.
    bridge_hostile_graph, bridge_hostile = exact_hull_bridge_hostile_graph()
    labels.append(expect_rejection(
        lambda: require(classify_parent(None, bridge_hostile_graph, {}, {})["case"]
                        != "bridge", "16-vertex hull bridge has priority"),
        "16-vertex skipped hull bridge"))

    # Distinguish the two complement-rank formulas and reject any swap.
    bridge = bridge_case_fixture(clean_parent)
    connector_graph, routes, payload = realize_parent(connector_parent)
    connector = classify_parent(connector_parent, connector_graph, routes, payload)
    require(bridge["complement_rank"] == 7 - bridge["q"] and
            connector["complement_rank"] == 6 - connector["q"] and
            bridge_hostile["complement_rank"] == 7 - bridge_hostile["q"] and
            connector_hostile["complement_rank"] == 6 - connector_hostile["q"],
            "dispatch arithmetic baseline changed")
    labels.append(expect_rejection(
        lambda: require(bridge["complement_rank"] == 6 - bridge["q"],
                        "swapped bridge formula"), "swap bridge rank formula"))
    labels.append(expect_rejection(
        lambda: require(connector["complement_rank"] == 7 - connector["q"],
                        "swapped connector formula"), "swap connector rank formula"))

    # Explicitly reject the historical rank-sum-four assertion.
    result = audit_residual(clean_parent)
    labels.append(expect_rejection(
        lambda: require(sum(result["ranks"][0]) == 4, "rank sum is not four"),
        "rank-sum four"))

    # A one-record side-allocation mutation must fail the derived 110-output
    # 28/27/27/28 census under both normal and optimized execution.
    changed_side_counts = Counter(retained_side_counts)
    changed_side_counts[(3, 0)] -= 1
    changed_side_counts[(2, 1)] += 1
    labels.append(expect_rejection(
        lambda: require(changed_side_counts == Counter({
            (3, 0): 28, (2, 1): 27, (1, 2): 27, (0, 3): 28,
        }), "retained side census changed"), "retained side allocation"))

    # Bridge-separated side triangles are connected as a graph but not a
    # shared-cut cluster; Tarjan/intersection check must reject them.
    a = frozenset((0, 1, 2)); b = frozenset((3, 4, 5))
    vertices = set(a | b)
    edges = set(triangle_edge_set(a) | triangle_edge_set(b)) | {edge(2, 3)}
    labels.append(expect_rejection(
        lambda: require(triangle_intersection_connected((a, b)),
                        "bridge-separated cluster"), "bridge hidden inside U/V"))
    return tuple(labels)


def audit():
    tree_probes = tree_universality_audit()
    generated_counts = {}
    dispatch_counts = {}
    generated_by_m = {}
    parent_sets = {}
    # m=L_even+L_odd+4.  These exact actual-site probes include interiors of
    # both connectors; the generating-function identity supplies arbitrary m.
    for m in (6, 7, 9, 11):
        parents = generate_parents(m)
        parent_sets[m] = parents
        expected = no_bridge_count(m)
        require(len(parents) == expected, f"N({m}) coefficient identity failed")
        clean = tuple(record for record in parents
                      if all(parent != -1 or slot < 6
                             for parent, slot in record.entries))
        connector = tuple(record for record in parents if record not in clean)
        require(len(clean) == 423 and len(connector) == expected - 423,
                f"universal connector dispatch failed at m={m}")
        generated_counts[m] = len(parents)
        dispatch_counts[m] = len(connector)
        generated_by_m[m] = (parents, clean, connector)

    # Exact shortest physical count: L_even=2,L_odd=1 => m=7.
    require(generated_counts[7] == 630 and dispatch_counts[7] == 207,
            "shortest physical 630=207+423 census changed")
    clean = generated_by_m[7][1]
    # Clean parents use only the six length-independent legal sites, so they
    # equal the canonical m=6 records byte-for-byte.
    require({record.entries for record in clean} ==
            {record.entries for record in parent_sets[6]},
            "clean parent set depends on connector length")

    output_preimages = Counter()
    shape_counts = Counter()
    retained_side_counts = Counter()
    retained_shape_side_counts = Counter()
    rank_profiles = Counter()
    residual_audits = 0
    for record in clean:
        result = audit_residual(record)
        output_preimages[result["retained"]] += 1
        residual_audits += 1
        rank_profiles[tuple(sorted(result["ranks"][0]))] += 1
    require(len(output_preimages) == 110, "423 parents do not map onto 110 outputs")
    for retained in output_preimages:
        shape = retained_shape(retained)
        allocation = retained_oriented_counts(retained)
        shape_counts[shape] += 1
        retained_side_counts[allocation] += 1
        retained_shape_side_counts[(shape, allocation)] += 1
    require(shape_counts == Counter({
        "direct3": 56, "chain2+direct": 36, "fork": 12, "chain3": 6,
    }), "derived retained shape census changed")
    require(retained_side_counts == Counter({
        (3, 0): 28, (2, 1): 27, (1, 2): 27, (0, 3): 28,
    }), "derived retained oriented side census changed")
    require(retained_shape_side_counts == Counter({
        ("direct3", (3, 0)): 10, ("direct3", (2, 1)): 18,
        ("direct3", (1, 2)): 18, ("direct3", (0, 3)): 10,
        ("chain2+direct", (3, 0)): 9, ("chain2+direct", (2, 1)): 9,
        ("chain2+direct", (1, 2)): 9, ("chain2+direct", (0, 3)): 9,
        ("fork", (3, 0)): 6, ("fork", (0, 3)): 6,
        ("chain3", (3, 0)): 3, ("chain3", (0, 3)): 3,
    }), "derived retained shape-by-side matrix changed")
    require(Counter(output_preimages.values()) == Counter({
        2: 13, 3: 32, 4: 40, 5: 13, 6: 8, 7: 4,
    }), "423-to-110 preimage multiplicities changed")
    require(sum(output_preimages.values()) == 423, "preimage weights do not sum 423")
    require(rank_profiles == Counter({(2, 3): 226, (1, 4): 197}),
            "physical residual rank profile changed")

    # Every canonical bridge-free parent also has a bridge-route variant.  It
    # must dispatch before connector/residual classification.
    bridge_profiles = Counter()
    for record in parent_sets[6]:
        result = bridge_case_fixture(record)
        bridge_profiles[(result["q"], result["complement_rank"])] += 1
    require(all(complement == 7 - q for q, complement in bridge_profiles),
            "bridge profile used connector arithmetic")

    # Symbolic arbitrary-depth TREE payload on one actual residual parent.
    tree_root = ('B', 0)
    decorated = audit_residual(clean[0], tree_payloads={
        tree_root: (-1, 0, 0, 2, 3, 1, 5, 6),
    })
    require(sum(decorated["ranks"][0]) == 5, "TREE payload changed U,V rank")

    rejected = hostile_tests(clean[0], generated_by_m[7][2][0],
                             retained_side_counts)
    return {
        "generated": generated_counts,
        "connector_dispatch": dispatch_counts,
        "clean": len(clean),
        "residual_audits": residual_audits,
        "outputs": len(output_preimages),
        "shape_counts": shape_counts,
        "retained_side_counts": retained_side_counts,
        "retained_shape_side_counts": retained_shape_side_counts,
        "multiplicities": Counter(output_preimages.values()),
        "rank_profiles": rank_profiles,
        "bridge_profiles": bridge_profiles,
        "tree_probes": tree_probes,
        "rejected": rejected,
    }


def report(result):
    return "\n".join((
        "R31-S physical-parent gate: exact audit passed",
        "scope: full B+4-triangle positive-rank parent trees; shared cuts, repeated cuts, chains and forks",
        "actual adjacency: reconstructed; Tarjan cyclic blocks and triangle-intersection clusters authenticated",
        "no-hull-bridge counts N(m): " + repr(result["generated"]),
        "connector-owner dispatch counts: " + repr(result["connector_dispatch"]),
        "shortest physical census: 630 = 207 connector dispatch + 423 clean residual",
        "arbitrary m identity: N(m)=[z^4](1+z+2z^2+5z^3+13z^4)^m; clean N(6)=423",
        "bridge routes: 423 canonical variants dispatched before residual; complement rank 7-q",
        "connector fibres: every internal vertex of both connectors tested; complement rank 6-q",
        f"clean physical residuals audited: {result['residual_audits']}; S,T,U,V disjoint/exhaustive",
        "residual predicates: Q maximum block-cut depth; S=cut-deleted away tree; T=complete F_v tree; rank(G-S-T)=5",
        "odd connector: every actual edge is a bridge after S,T; U,V are Tarjan-authenticated shared-cut triangle clusters",
        "U,V unordered rank profiles: " + repr(dict(sorted(result["rank_profiles"].items()))),
        "derived retained outputs: 110; shapes=" + repr(dict(result["shape_counts"])),
        "derived oriented retained allocations: " +
        repr(dict(sorted(result["retained_side_counts"].items(), reverse=True))),
        "423-to-110 preimage multiplicities: " + repr(dict(sorted(result["multiplicities"].items()))),
        "retained census scope: retained-record census only; no analytic D3 implication or spectral closure",
        "symbolic universality: recursive TREE/BRIDGE parent invariants; leaf induction, no bridge-depth bound",
        f"hostile mutations rejected: {len(result['rejected'])} " + repr(result["rejected"]),
        "status: standalone combinatorial gate only; no theorem/master/state modification",
    ))


def main():
    result = audit()
    output = report(result)
    if "--optimized-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-child"],
                               check=False, capture_output=True, text=True)
        require(child.returncode == 0, "optimized child failed")
        require(child.stderr == "", "optimized child wrote stderr")
        require(child.stdout.rstrip() == output, "normal/optimized receipts differ")
    print(output)


if __name__ == "__main__":
    main()
