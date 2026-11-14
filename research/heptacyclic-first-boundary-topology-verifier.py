#!/usr/bin/env python3
"""NONPROMOTIONAL adjacency-level first-boundary replay.

This standalone diagnostic checks a small set of representative physical
R21/R31-K/R321/R41 cases.  It does not enumerate all reduced block-cut hulls.
Routing words are outputs of Tarjan reconstruction; no channel or disposition
field occurs in the physical-case schema.
"""

from __future__ import annotations

import itertools
import json
import subprocess
import sys
from collections import deque
from copy import deepcopy
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable


Vertex = str
Edge = tuple[Vertex, Vertex]
Node = tuple[str, object]


class AuditError(RuntimeError):
    """A physical or ownership claim was not reconstructed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def edge(left: Vertex, right: Vertex) -> Edge:
    require(left != right, "loops are not allowed")
    return (left, right) if left < right else (right, left)


def induced_edges(edges: Iterable[Edge], vertices: Iterable[Vertex]) -> frozenset[Edge]:
    chosen = frozenset(vertices)
    return frozenset(current for current in edges
                     if current[0] in chosen and current[1] in chosen)


def adjacency(vertices: Iterable[Vertex], edges: Iterable[Edge]) -> dict[Vertex, set[Vertex]]:
    answer = {vertex: set() for vertex in vertices}
    for left, right in edges:
        require(left in answer and right in answer, "edge endpoint is absent")
        require(right not in answer[left], "duplicate edge")
        answer[left].add(right)
        answer[right].add(left)
    return answer


def components(vertices: Iterable[Vertex], edges: Iterable[Edge]) -> tuple[frozenset[Vertex], ...]:
    remaining = set(vertices)
    graph = adjacency(remaining, edges)
    answer: list[frozenset[Vertex]] = []
    while remaining:
        start = min(remaining)
        reached = {start}
        queue = [start]
        while queue:
            current = queue.pop()
            for neighbor in graph[current]:
                if neighbor not in reached:
                    reached.add(neighbor)
                    queue.append(neighbor)
        remaining -= reached
        answer.append(frozenset(reached))
    return tuple(sorted(answer, key=lambda part: tuple(sorted(part))))


def connected(vertices: Iterable[Vertex], edges: Iterable[Edge]) -> bool:
    chosen = frozenset(vertices)
    return bool(chosen) and len(components(chosen, edges)) == 1


def graph_rank(vertices: Iterable[Vertex], edges: Iterable[Edge]) -> int:
    chosen = frozenset(vertices)
    chosen_edges = frozenset(edges)
    return len(chosen_edges) - len(chosen) + len(components(chosen, chosen_edges))


def edge_blocks(vertices: Iterable[Vertex], edges: Iterable[Edge]) -> tuple[frozenset[Edge], ...]:
    """Tarjan edge-stack reconstruction of all biconnected edge blocks."""
    chosen = frozenset(vertices)
    chosen_edges = frozenset(edges)
    graph = adjacency(chosen, chosen_edges)
    discovery: dict[Vertex, int] = {}
    low: dict[Vertex, int] = {}
    parent: dict[Vertex, Vertex | None] = {}
    stack: list[Edge] = []
    blocks: list[frozenset[Edge]] = []
    clock = 0

    def visit(current: Vertex) -> None:
        nonlocal clock
        discovery[current] = clock
        low[current] = clock
        clock += 1
        for neighbor in sorted(graph[current]):
            current_edge = edge(current, neighbor)
            if neighbor not in discovery:
                parent[neighbor] = current
                stack.append(current_edge)
                visit(neighbor)
                low[current] = min(low[current], low[neighbor])
                if low[neighbor] >= discovery[current]:
                    block: set[Edge] = set()
                    while stack:
                        popped = stack.pop()
                        block.add(popped)
                        if popped == current_edge:
                            break
                    require(block and current_edge in block,
                            "Tarjan edge stack lost a tree edge")
                    blocks.append(frozenset(block))
            elif parent.get(current) != neighbor and discovery[neighbor] < discovery[current]:
                stack.append(current_edge)
                low[current] = min(low[current], discovery[neighbor])

    for start in sorted(chosen):
        if start not in discovery:
            parent[start] = None
            visit(start)
            require(not stack, "Tarjan edge stack was not drained")
    require(set().union(*blocks) == set(chosen_edges) if chosen_edges else not blocks,
            "Tarjan blocks do not exhaust the edge set")
    require(sum(map(len, blocks)) == len(chosen_edges),
            "Tarjan blocks duplicate an edge")
    return tuple(sorted(blocks, key=lambda block: tuple(sorted(block))))


@dataclass(frozen=True)
class BlockMark:
    name: str
    kind: str
    vertices: frozenset[Vertex]
    opening: Vertex | None = None


@dataclass(frozen=True)
class PhysicalCase:
    name: str
    profile: str
    vertices: frozenset[Vertex]
    edges: frozenset[Edge]
    marks: tuple[BlockMark, ...]
    root_mark: str
    hostile_mark: str
    payload_groups: tuple[frozenset[Vertex], ...]


@dataclass(frozen=True)
class Block:
    index: int
    edges: frozenset[Edge]
    vertices: frozenset[Vertex]
    rank: int


@dataclass(frozen=True)
class BlockCutModel:
    vertices: frozenset[Vertex]
    edges: frozenset[Edge]
    blocks: tuple[Block, ...]
    cut_vertices: frozenset[Vertex]
    tree: tuple[tuple[Node, Node], ...]
    mark_to_block: tuple[tuple[str, int], ...]

    def block_for(self, mark: str) -> Block:
        lookup = dict(self.mark_to_block)
        require(mark in lookup, f"mark is absent from block-cut model: {mark}")
        return self.blocks[lookup[mark]]


@dataclass(frozen=True)
class Territory:
    name: str
    vertices: frozenset[Vertex]
    edges: frozenset[Edge]
    rank: int


@dataclass(frozen=True)
class OpeningRecord:
    root_mark: str
    target_mark: str
    cut: Vertex
    vertices: frozenset[Vertex]


@dataclass(frozen=True)
class Bound:
    value: int
    strict: bool

    def __add__(self, other: "Bound") -> "Bound":
        return Bound(self.value + other.value, self.strict or other.strict)

    def above(self, target: int) -> bool:
        return self.value > target or (self.value == target and self.strict)


@dataclass(frozen=True)
class ReplayCertificate:
    case_name: str
    profile: str
    branch: str
    topology: tuple[object, ...]
    hostile_bridge: Edge
    hostile_vertices: frozenset[Vertex]
    selected_marks: tuple[str, ...]
    details: tuple[tuple[str, str], ...]
    openings: tuple[OpeningRecord, ...]
    territories: tuple[Territory, ...]
    ledger: tuple[tuple[str, str], ...]


class Builder:
    def __init__(self) -> None:
        self.vertices: set[Vertex] = set()
        self.edges: set[Edge] = set()
        self.marks: list[BlockMark] = []
        self.payload_groups: list[frozenset[Vertex]] = []

    def add_edge(self, left: Vertex, right: Vertex) -> None:
        current = edge(left, right)
        require(current not in self.edges, f"duplicate builder edge: {current}")
        self.vertices.update(current)
        self.edges.add(current)

    def add_mark(self, name: str, kind: str, vertices: Iterable[Vertex],
                 opening: Vertex | None = None) -> None:
        chosen = frozenset(vertices)
        require(name not in {mark.name for mark in self.marks},
                f"duplicate mark: {name}")
        self.vertices |= set(chosen)
        self.marks.append(BlockMark(name, kind, chosen, opening))

    def add_payload_leaf(self, root: Vertex, leaf: Vertex) -> None:
        self.add_edge(root, leaf)
        self.payload_groups.append(frozenset({leaf}))

    def finish(self, name: str, profile: str, root: str, hostile: str) -> PhysicalCase:
        return PhysicalCase(
            name=name,
            profile=profile,
            vertices=frozenset(self.vertices),
            edges=frozenset(self.edges),
            marks=tuple(self.marks),
            root_mark=root,
            hostile_mark=hostile,
            payload_groups=tuple(self.payload_groups),
        )


def add_k4(builder: Builder, name: str, prefix: str) -> tuple[Vertex, ...]:
    vertices = tuple(f"{prefix}{index}" for index in range(4))
    for left, right in itertools.combinations(vertices, 2):
        builder.add_edge(left, right)
    builder.add_mark(name, "K4", vertices)
    return vertices


def add_diamond(builder: Builder, name: str, vertices: tuple[Vertex, Vertex, Vertex, Vertex],
                missing: tuple[Vertex, Vertex]) -> None:
    missing_edge = edge(*missing)
    for left, right in itertools.combinations(vertices, 2):
        if edge(left, right) != missing_edge:
            builder.add_edge(left, right)
    builder.add_mark(name, "D", vertices)


def add_shared_cycle(builder: Builder, name: str, kind: str, cut: Vertex,
                     length: int) -> tuple[Vertex, ...]:
    require(length >= 3, "cycle is too short")
    vertices = (cut, *(f"{name}:{index}" for index in range(1, length)))
    for left, right in zip(vertices, vertices[1:] + vertices[:1]):
        builder.add_edge(left, right)
    builder.add_mark(name, kind, vertices)
    return vertices


def add_free_cycle(builder: Builder, name: str, kind: str, length: int) -> tuple[Vertex, ...]:
    vertices = tuple(f"{name}:{index}" for index in range(length))
    for left, right in zip(vertices, vertices[1:] + vertices[:1]):
        builder.add_edge(left, right)
    builder.add_mark(name, kind, vertices)
    return vertices


def add_hostile_connector(builder: Builder, root: Vertex, name: str, kind: str = "P") -> None:
    cycle = add_free_cycle(builder, name, kind, 5)
    middle = f"{name}:connector"
    builder.add_edge(root, middle)
    builder.add_edge(middle, cycle[0])
    builder.add_payload_leaf(middle, f"{name}:payload")


def build_r21(name: str = "r21-dtt", bridge_t1: bool = False,
               split_repeated_cut: bool = False) -> PhysicalCase:
    builder = Builder()
    diamond = ("r21:d0", "r21:d1", "r21:d2", "r21:d3")
    add_diamond(builder, "D", diamond, (diamond[2], diamond[3]))
    add_shared_cycle(builder, "T0", "T", diamond[0], 3)
    if bridge_t1:
        cycle = add_free_cycle(builder, "T1", "T", 3)
        builder.add_edge(diamond[1], cycle[0])
    else:
        add_shared_cycle(builder, "T1", "T", diamond[1], 3)
    add_shared_cycle(builder, "T2", "T", diamond[2], 3)
    cut_t3 = diamond[3] if split_repeated_cut else diamond[2]
    add_shared_cycle(builder, "T3", "T", cut_t3, 3)
    add_hostile_connector(builder, diamond[3], "P")
    return builder.finish(name, "R21", "D", "P")


def build_r31(name: str, nested_t0: bool, nested_t1: bool) -> PhysicalCase:
    builder = Builder()
    k4 = add_k4(builder, "K4", "r31:k")
    nontriangle = add_shared_cycle(builder, "N1", "N", k4[1], 5)
    add_shared_cycle(builder, "T0", "T", nontriangle[2] if nested_t0 else k4[0], 3)
    add_shared_cycle(builder, "T1", "T", nontriangle[3] if nested_t1 else k4[2], 3)
    add_hostile_connector(builder, k4[3], "N0", "N")
    return builder.finish(name, "R31-K", "K4", "N0")


def build_r321(name: str, entry_degree: int, direct_triangle: bool) -> PhysicalCase:
    require(entry_degree in (2, 3), "diamond entry orbit must have degree two or three")
    builder = Builder()
    k4 = add_k4(builder, "K4", "r321:k")
    diamond = (k4[0], "r321:d1", "r321:d2", "r321:d3")
    missing = (diamond[0], diamond[1]) if entry_degree == 2 else (diamond[2], diamond[3])
    add_diamond(builder, "D", diamond, missing)
    add_shared_cycle(builder, "T", "T", k4[2] if direct_triangle else diamond[2], 3)
    add_hostile_connector(builder, k4[3], "P")
    return builder.finish(name, "R321", "K4", "P")


def build_r41(name: str, owner_triangles: int) -> PhysicalCase:
    require(owner_triangles in (0, 1, 2), "invalid S4 owner count")
    builder = Builder()
    core = tuple(f"r41:k{index}" for index in range(4))
    for left, right in itertools.combinations(core, 2):
        builder.add_edge(left, right)
    opening = "r41:v"
    builder.add_edge(core[0], opening)
    builder.add_edge(opening, core[1])
    builder.add_mark("S4", "S4", (*core, opening), opening)
    add_shared_cycle(builder, "T0", "T", opening if owner_triangles >= 1 else core[2], 3)
    add_shared_cycle(builder, "T1", "T", opening if owner_triangles >= 2 else core[3], 3)
    builder.add_payload_leaf(opening, "r41:owner-payload")
    add_hostile_connector(builder, core[0], "P")
    return builder.finish(name, "R41", "S4", "P")


def block_vertices(block_edges: Iterable[Edge]) -> frozenset[Vertex]:
    return frozenset(vertex for current in block_edges for vertex in current)


def shape_of_block(vertices: frozenset[Vertex], edges: frozenset[Edge]) -> str:
    degrees = sorted(len(adjacency(vertices, edges)[vertex]) for vertex in vertices)
    if len(vertices) == 3 and len(edges) == 3 and degrees == [2, 2, 2]:
        return "T"
    if len(vertices) >= 4 and len(edges) == len(vertices) and all(value == 2 for value in degrees):
        return "N"
    if len(vertices) == 4 and len(edges) == 5 and degrees == [2, 2, 3, 3]:
        return "D"
    if len(vertices) == 4 and len(edges) == 6 and degrees == [3, 3, 3, 3]:
        return "K4"
    return "OTHER"


def validate_mark_shape(mark: BlockMark, block: Block) -> None:
    require(mark.vertices == block.vertices, f"{mark.name} vertex set is not its Tarjan block")
    shape = shape_of_block(block.vertices, block.edges)
    if mark.kind == "P":
        require(shape == "N" and len(block.vertices) == 5,
                f"{mark.name} is not a pentagon block")
    elif mark.kind == "N":
        require(shape == "N", f"{mark.name} is not a nontriangle cycle block")
    elif mark.kind in {"T", "D", "K4"}:
        require(shape == mark.kind, f"{mark.name} physical block kind changed")
    elif mark.kind == "S4":
        require(len(block.vertices) == 5 and len(block.edges) == 8 and block.rank == 4,
                "S4 representative block has wrong order/size/rank")
        require(mark.opening in block.vertices, "S4 opening is absent")
        retained = block.vertices - {mark.opening}
        retained_edges = induced_edges(block.edges, retained)
        require(shape_of_block(retained, retained_edges) == "K4",
                "S4 opening does not retain its physical K4")
        require(len(adjacency(block.vertices, block.edges)[mark.opening]) == 2,
                "S4 opening is not the ear interior")
    else:
        raise AuditError(f"unknown physical block kind: {mark.kind}")


def tree_edge(left: Node, right: Node) -> tuple[Node, Node]:
    return (left, right) if repr(left) < repr(right) else (right, left)


def analyze(vertices: Iterable[Vertex], edges: Iterable[Edge],
            marks: Iterable[BlockMark], *, require_all_cyclic_typed: bool = True) -> BlockCutModel:
    chosen_vertices = frozenset(vertices)
    chosen_edges = frozenset(edges)
    require(connected(chosen_vertices, chosen_edges), "physical graph is disconnected")
    raw = edge_blocks(chosen_vertices, chosen_edges)
    blocks = tuple(Block(index, current, block_vertices(current),
                         graph_rank(block_vertices(current), current))
                   for index, current in enumerate(raw))
    membership: dict[Vertex, list[int]] = {vertex: [] for vertex in chosen_vertices}
    for block in blocks:
        for vertex in block.vertices:
            membership[vertex].append(block.index)
    cuts = frozenset(vertex for vertex, owners in membership.items() if len(owners) > 1)
    incidence = tuple(sorted(
        (tree_edge(("B", block.index), ("C", vertex))
         for block in blocks for vertex in block.vertices if vertex in cuts),
        key=repr,
    ))
    tree_nodes = {node for current in incidence for node in current}
    tree_nodes |= {("B", block.index) for block in blocks}
    require(len(incidence) == len(tree_nodes) - 1,
            "Tarjan block-cut incidence is not a tree")

    mark_map: list[tuple[str, int]] = []
    used: set[int] = set()
    marks_tuple = tuple(marks)
    for mark in marks_tuple:
        candidates = [block for block in blocks if block.vertices == mark.vertices and block.rank > 0]
        require(len(candidates) == 1, f"{mark.name} is not one recovered cyclic block")
        block = candidates[0]
        require(block.index not in used, "two marks claim one cyclic block")
        validate_mark_shape(mark, block)
        used.add(block.index)
        mark_map.append((mark.name, block.index))
    cyclic = {block.index for block in blocks if block.rank > 0}
    if require_all_cyclic_typed:
        require(cyclic == used, "untyped cyclic block reconstructed from adjacency")
    return BlockCutModel(chosen_vertices, chosen_edges, blocks, cuts, incidence,
                         tuple(sorted(mark_map)))


def validate_payloads(case: PhysicalCase) -> None:
    seen: set[Vertex] = set()
    for payload in case.payload_groups:
        require(payload and not (seen & set(payload)), "payload groups overlap")
        seen |= set(payload)
        payload_edges = induced_edges(case.edges, payload)
        require(connected(payload, payload_edges) and graph_rank(payload, payload_edges) == 0,
                "payload is not an induced tree")
        outside = {neighbor for vertex in payload
                   for neighbor in adjacency(case.vertices, case.edges)[vertex]
                   if neighbor not in payload}
        require(len(outside) == 1, "payload does not have one physical owner root")


def validate_profile(case: PhysicalCase) -> BlockCutModel:
    require(case.profile in {"R21", "R31-K", "R321", "R41"},
            "unknown representative profile")
    require(len(case.vertices) == len(set(case.vertices)), "duplicate vertex")
    require(all(current == edge(*current) for current in case.edges),
            "edge is not canonical")
    require(len({mark.name for mark in case.marks}) == len(case.marks),
            "duplicate mark name")
    marks = {mark.name: mark for mark in case.marks}
    require(case.root_mark in marks and case.hostile_mark in marks,
            "root or hostile mark is absent")
    model = analyze(case.vertices, case.edges, case.marks)
    kinds = sorted(mark.kind for mark in case.marks)
    expected = {
        "R21": sorted(["D", "T", "T", "T", "T", "P"]),
        "R31-K": sorted(["K4", "N", "N", "T", "T"]),
        "R321": sorted(["K4", "D", "T", "P"]),
        "R41": sorted(["S4", "T", "T", "P"]),
    }[case.profile]
    require(kinds == expected, "typed positive-block inventory changed")
    require(sum(model.block_for(mark.name).rank for mark in case.marks) == 7,
            "marked block ranks do not sum to seven")
    require(marks[case.hostile_mark].kind in {"N", "P"},
            "hostile selected block is not nontriangular")
    validate_payloads(case)
    return model


def tree_adjacency(model: BlockCutModel) -> dict[Node, set[Node]]:
    nodes = {("B", block.index) for block in model.blocks}
    nodes |= {("C", vertex) for vertex in model.cut_vertices}
    answer = {node: set() for node in nodes}
    for left, right in model.tree:
        answer[left].add(right)
        answer[right].add(left)
    return answer


def tree_path(model: BlockCutModel, start: Node, finish: Node) -> tuple[Node, ...]:
    graph = tree_adjacency(model)
    require(start in graph and finish in graph, "block-cut path endpoint is absent")
    previous: dict[Node, Node | None] = {start: None}
    queue = deque([start])
    while queue and finish not in previous:
        current = queue.popleft()
        for neighbor in sorted(graph[current], key=repr):
            if neighbor not in previous:
                previous[neighbor] = current
                queue.append(neighbor)
    require(finish in previous, "block-cut path is disconnected")
    path: list[Node] = []
    current: Node | None = finish
    while current is not None:
        path.append(current)
        current = previous[current]
    return tuple(reversed(path))


def mark_lookup(case: PhysicalCase) -> dict[str, BlockMark]:
    return {mark.name: mark for mark in case.marks}


def subcase_model(case: PhysicalCase, vertices: frozenset[Vertex]) -> BlockCutModel:
    marks = tuple(mark for mark in case.marks if mark.vertices <= vertices)
    return analyze(vertices, induced_edges(case.edges, vertices), marks)


def first_bridge_to(model: BlockCutModel, root_mark: str, target_mark: str) -> tuple[Edge, frozenset[Vertex]]:
    root_node = ("B", model.block_for(root_mark).index)
    target_node = ("B", model.block_for(target_mark).index)
    path = tree_path(model, root_node, target_node)
    bridges = [model.blocks[node[1]] for node in path
               if node[0] == "B" and len(model.blocks[node[1]].edges) == 1]
    require(bridges, f"no actual bridge separates {target_mark}")
    bridge = next(iter(bridges[0].edges))
    sides = components(model.vertices, model.edges - {bridge})
    require(len(sides) == 2, "Tarjan K2 block is not an actual bridge")
    target_vertices = model.block_for(target_mark).vertices
    away = [side for side in sides if target_vertices <= side]
    require(len(away) == 1, "target block is not wholly on one bridge side")
    return bridge, away[0]


def boundary_open(model: BlockCutModel, root_mark: str,
                  target_mark: str) -> tuple[Vertex, frozenset[Vertex]]:
    root_node = ("B", model.block_for(root_mark).index)
    target_node = ("B", model.block_for(target_mark).index)
    path = tree_path(model, root_node, target_node)
    require(len(path) >= 3 and path[-2][0] == "C",
            "target has no rooted entry cut")
    cut = path[-2][1]
    incidence = tree_edge(path[-2], path[-1])
    remaining_tree = tuple(current for current in model.tree if current != incidence)
    graph = tree_adjacency(replace(model, tree=remaining_tree))
    reached = {target_node}
    queue = [target_node]
    while queue:
        current = queue.pop()
        for neighbor in graph[current]:
            if neighbor not in reached:
                reached.add(neighbor)
                queue.append(neighbor)
    vertices: set[Vertex] = set()
    for node in reached:
        if node[0] == "B":
            vertices |= set(model.blocks[node[1]].vertices)
        else:
            vertices.add(node[1])
    vertices.discard(cut)
    opened = frozenset(vertices)
    opened_edges = induced_edges(model.edges, opened)
    require(opened and connected(opened, opened_edges),
            "boundary opening is not one connected away territory")
    return cut, opened


def topology_signature(model: BlockCutModel) -> tuple[object, ...]:
    marked = {index: name for name, index in model.mark_to_block}
    records = []
    for block in model.blocks:
        label = marked.get(block.index, "K2" if len(block.edges) == 1 else "UNTYPED")
        records.append((label, tuple(sorted(block.edges)),
                        tuple(sorted(block.vertices & model.cut_vertices))))
    return tuple(records)


def split_hostile(case: PhysicalCase, model: BlockCutModel) -> tuple[Edge, frozenset[Vertex], frozenset[Vertex]]:
    bridge, hostile = first_bridge_to(model, case.root_mark, case.hostile_mark)
    complement = case.vertices - hostile
    hostile_edges = induced_edges(case.edges, hostile)
    complement_edges = induced_edges(case.edges, complement)
    require(connected(hostile, hostile_edges) and graph_rank(hostile, hostile_edges) == 1,
            "hostile side is not a connected unicycle")
    require(connected(complement, complement_edges) and graph_rank(complement, complement_edges) == 6,
            "hostile complement is not connected rank six")
    hostile_marks = [mark.name for mark in case.marks if mark.vertices <= hostile]
    require(hostile_marks == [case.hostile_mark],
            "hostile side contains the wrong marked cyclic inventory")
    return bridge, hostile, complement


def marked_path(model: BlockCutModel, root_mark: str, target_mark: str) -> tuple[str, ...]:
    reverse = {index: name for name, index in model.mark_to_block}
    path = tree_path(model, ("B", model.block_for(root_mark).index),
                     ("B", model.block_for(target_mark).index))
    return tuple(reverse[node[1]] for node in path
                 if node[0] == "B" and node[1] in reverse)


def path_has_bridge(model: BlockCutModel, root_mark: str, target_mark: str) -> bool:
    path = tree_path(model, ("B", model.block_for(root_mark).index),
                     ("B", model.block_for(target_mark).index))
    return any(node[0] == "B" and len(model.blocks[node[1]].edges) == 1
               for node in path)


def make_territory(case: PhysicalCase, name: str,
                   vertices: Iterable[Vertex]) -> Territory:
    chosen = frozenset(vertices)
    chosen_edges = induced_edges(case.edges, chosen)
    return Territory(name, chosen, chosen_edges, graph_rank(chosen, chosen_edges))


def cyclic_shapes(vertices: frozenset[Vertex], edges: frozenset[Edge]) -> tuple[str, ...]:
    shapes = []
    for current in edge_blocks(vertices, edges):
        block_vertices_set = block_vertices(current)
        if graph_rank(block_vertices_set, current) > 0:
            shapes.append(shape_of_block(block_vertices_set, current))
    return tuple(sorted(shapes))


def cyclic_hull_contains_bridge(vertices: frozenset[Vertex], edges: frozenset[Edge]) -> bool:
    model = analyze(vertices, edges, (), require_all_cyclic_typed=False)
    cyclic_nodes = [("B", block.index) for block in model.blocks if block.rank > 0]
    if len(cyclic_nodes) <= 1:
        return False
    hull: set[Node] = set()
    for target in cyclic_nodes[1:]:
        hull |= set(tree_path(model, cyclic_nodes[0], target))
    return any(node[0] == "B" and len(model.blocks[node[1]].edges) == 1
               for node in hull)


BOUND_TABLE = {
    "DTT": Bound(3, True),
    "K4T": Bound(3, True),
    "K4": Bound(2, True),
    "F": Bound(2, True),
    "TREE": Bound(-1, False),
    "TRIANGULAR": Bound(0, True),
    "RANK_GE_2": Bound(0, False),
    "UNICYCLE": Bound(-1, True),
}


def validate_bound_tag(territory: Territory, tag: str) -> None:
    require(tag in BOUND_TABLE, f"unknown conditional packet tag: {tag}")
    require(connected(territory.vertices, territory.edges),
            f"territory is disconnected: {territory.name}")
    shapes = cyclic_shapes(territory.vertices, territory.edges)
    if tag == "DTT":
        require(shapes == ("D", "T", "T") and territory.rank == 4,
                "DTT anchor does not have its physical cyclic inventory")
        require(not cyclic_hull_contains_bridge(territory.vertices, territory.edges),
                "DTT narrow anchor contains a positive connector")
    elif tag == "K4T":
        require(shapes == ("K4", "T") and territory.rank == 4,
                "K4T anchor does not have its physical cyclic inventory")
        require(not cyclic_hull_contains_bridge(territory.vertices, territory.edges),
                "K4T narrow anchor contains a positive connector")
    elif tag in {"K4", "F"}:
        require(shapes == ("K4",) and territory.rank == 3,
                f"{tag} representative is not one retained K4 packet")
    elif tag == "TREE":
        require(territory.rank == 0 and len(territory.edges) == len(territory.vertices) - 1,
                "tree debit is not an induced tree")
    elif tag == "TRIANGULAR":
        require(territory.rank >= 1 and shapes and set(shapes) == {"T"},
                "triangular territory contains a nontriangle cyclic block")
    elif tag == "RANK_GE_2":
        require(2 <= territory.rank <= 6, "lower-rank territory is outside ranks two through six")
    elif tag == "UNICYCLE":
        require(territory.rank == 1, "unicycle tag has wrong rank")


def tag_for_side(territory: Territory) -> str:
    if territory.rank == 0:
        return "TREE"
    shapes = cyclic_shapes(territory.vertices, territory.edges)
    if territory.rank == 1 and shapes and set(shapes) == {"T"}:
        return "TRIANGULAR"
    if territory.rank == 1:
        return "UNICYCLE"
    return "RANK_GE_2"


def component_pieces(case: PhysicalCase, universe: frozenset[Vertex],
                     fixed: tuple[tuple[str, frozenset[Vertex]], ...],
                     model: BlockCutModel, root_mark: str,
                     candidate_marks: tuple[str, ...]) -> tuple[tuple[Territory, ...], tuple[OpeningRecord, ...]]:
    occupied = set().union(*(vertices for _, vertices in fixed))
    require(sum(len(vertices) for _, vertices in fixed) == len(occupied),
            "fixed semantic pieces overlap")
    remainder = universe - occupied
    remainder_edges = induced_edges(case.edges, remainder)
    parts = components(remainder, remainder_edges) if remainder else ()
    territories = [make_territory(case, name, vertices) for name, vertices in fixed]
    openings: list[OpeningRecord] = []
    used_marks: set[str] = set()
    for index, part in enumerate(parts):
        matched_openings = []
        for mark in candidate_marks:
            if mark in used_marks:
                continue
            try:
                cut, opened = boundary_open(model, root_mark, mark)
            except AuditError:
                continue
            if opened == part:
                matched_openings.append((mark, cut))
        if matched_openings:
            mark, cut = min(matched_openings)
            used_marks.add(mark)
            openings.append(OpeningRecord(root_mark, mark, cut, part))
            label = f"opened:{mark}"
        else:
            bridge_matches = []
            for mark in candidate_marks:
                if mark in used_marks:
                    continue
                try:
                    unused_bridge, away = first_bridge_to(model, root_mark, mark)
                except AuditError:
                    continue
                if away == part:
                    bridge_matches.append(mark)
            require(bridge_matches, f"remainder component {index} has no physical first boundary")
            mark = min(bridge_matches)
            used_marks.add(mark)
            label = f"bridged:{mark}"
        territories.append(make_territory(case, label, part))
    require(set().union(*(territory.vertices for territory in territories)) == universe,
            "component pieces do not exhaust their universe")
    return tuple(territories), tuple(sorted(openings, key=lambda item: item.target_mark))


def derive_r21(case: PhysicalCase, complement: frozenset[Vertex],
               hostile: Territory) -> tuple[str, tuple[str, ...], tuple[tuple[str, str], ...],
                                              tuple[Territory, ...], tuple[OpeningRecord, ...],
                                              tuple[tuple[str, str], ...]]:
    model = subcase_model(case, complement)
    root = model.block_for("D")
    bridge_edges = {next(iter(block.edges)) for block in model.blocks if len(block.edges) == 1}
    bridge_free = components(complement, model.edges - bridge_edges)
    root_component = next(part for part in bridge_free if root.vertices <= part)
    triangle_names = tuple(sorted(mark.name for mark in case.marks if mark.kind == "T"))
    root_triangles = tuple(name for name in triangle_names
                           if model.block_for(name).vertices <= root_component)
    require(len(root_triangles) >= 2, "representative R21 root cluster has fewer than two triangles")
    selected = None
    for pair in itertools.combinations(root_triangles, 2):
        hull: set[Node] = set()
        for name in pair:
            hull |= set(tree_path(model, ("B", root.index),
                                  ("B", model.block_for(name).index)))
        triangle_nodes = {("B", model.block_for(name).index) for name in triangle_names}
        if hull & triangle_nodes == {("B", model.block_for(name).index) for name in pair}:
            if not any(node[0] == "B" and len(model.blocks[node[1]].edges) == 1
                       for node in hull):
                selected = pair
                break
    require(selected is not None, "no physical bridge-free DTT hull was selected")
    marks = mark_lookup(case)
    anchor_vertices = marks["D"].vertices | marks[selected[0]].vertices | marks[selected[1]].vertices
    fixed = (("anchor", anchor_vertices),)
    pieces, openings = component_pieces(case, complement, fixed, model, "D",
                                        tuple(name for name in triangle_names if name not in selected))
    anchor = pieces[0]
    ledger = [(anchor.name, "DTT")]
    ledger.extend((territory.name, tag_for_side(territory)) for territory in pieces[1:])
    details = (("root_cluster_triangles", str(len(root_triangles))),)
    return (f"dtt-root-k{len(root_triangles)}", tuple(selected), details,
            (hostile, *pieces), openings, tuple(ledger))


def derive_r31(case: PhysicalCase, complement: frozenset[Vertex],
               hostile: Territory) -> tuple[str, tuple[str, ...], tuple[tuple[str, str], ...],
                                              tuple[Territory, ...], tuple[OpeningRecord, ...],
                                              tuple[tuple[str, str], ...]]:
    model = subcase_model(case, complement)
    marks = mark_lookup(case)
    triangles = tuple(sorted(mark.name for mark in case.marks if mark.kind == "T"))
    nontriangle = next(mark.name for mark in case.marks
                       if mark.kind == "N" and mark.name != case.hostile_mark)
    direct = tuple(name for name in triangles
                   if not path_has_bridge(model, "K4", name)
                   and marked_path(model, "K4", name) == ("K4", name))
    if direct:
        chosen = direct[0]
        anchor_vertices = marks["K4"].vertices | marks[chosen].vertices
        pieces, openings = component_pieces(
            case, complement, (("anchor", anchor_vertices),), model, "K4",
            tuple(name for name in (nontriangle, *triangles) if name != chosen))
        ledger = [(pieces[0].name, "K4T")]
        ledger.extend((territory.name, tag_for_side(territory)) for territory in pieces[1:])
        return ("direct-T", (chosen,), (), (hostile, *pieces), openings, tuple(ledger))

    paths = {name: marked_path(model, "K4", name) for name in triangles}
    require(all(path[:2] == ("K4", nontriangle) for path in paths.values()),
            "R31 representative has neither direct T nor one intermediate N")
    cut, opened = boundary_open(model, "K4", nontriangle)
    anchor_vertices = marks["K4"].vertices
    require(complement == anchor_vertices | opened and not (anchor_vertices & opened),
            "intermediate-N opening does not partition the complement")
    anchor = make_territory(case, "anchor", anchor_vertices)
    downstream = make_territory(case, f"opened:{nontriangle}", opened)
    opening = OpeningRecord("K4", nontriangle, cut, opened)
    ledger = ((anchor.name, "K4"), (downstream.name, tag_for_side(downstream)))
    return ("intermediate-N", (nontriangle,), (), (hostile, anchor, downstream),
            (opening,), ledger)


def diamond_entry_degree(case: PhysicalCase, cut: Vertex) -> int:
    mark = mark_lookup(case)["D"]
    block_edges = induced_edges(case.edges, mark.vertices)
    return len(adjacency(mark.vertices, block_edges)[cut])


def derive_r321(case: PhysicalCase, complement: frozenset[Vertex],
                hostile: Territory) -> tuple[str, tuple[str, ...], tuple[tuple[str, str], ...],
                                               tuple[Territory, ...], tuple[OpeningRecord, ...],
                                               tuple[tuple[str, str], ...]]:
    model = subcase_model(case, complement)
    marks = mark_lookup(case)
    path = marked_path(model, "K4", "T")
    if path == ("K4", "D", "T") and not path_has_bridge(model, "K4", "T"):
        cut, opened = boundary_open(model, "K4", "D")
        anchor = make_territory(case, "anchor", marks["K4"].vertices)
        downstream = make_territory(case, "opened:D", opened)
        require(complement == anchor.vertices | downstream.vertices
                and not (anchor.vertices & downstream.vertices),
                "intermediate-D opening does not partition the complement")
        entry = diamond_entry_degree(case, cut)
        require(entry in (2, 3), "diamond entry orbit was not reconstructed")
        opening = OpeningRecord("K4", "D", cut, opened)
        ledger = ((anchor.name, "K4"), (downstream.name, tag_for_side(downstream)))
        return ("intermediate-D", ("D",), (("D_entry_degree", str(entry)),),
                (hostile, anchor, downstream), (opening,), ledger)

    require(path == ("K4", "T") and not path_has_bridge(model, "K4", "T"),
            "R321 representative has no direct or intermediate triangle route")
    anchor_vertices = marks["K4"].vertices | marks["T"].vertices
    pieces, openings = component_pieces(case, complement, (("anchor", anchor_vertices),),
                                        model, "K4", ("D",))
    ledger = [(pieces[0].name, "K4T")]
    ledger.extend((territory.name, tag_for_side(territory)) for territory in pieces[1:])
    return ("direct-T", ("T",), (), (hostile, *pieces), openings, tuple(ledger))


def structural_owner(case: PhysicalCase, complement: frozenset[Vertex]) -> tuple[frozenset[Vertex], frozenset[Vertex], int]:
    marks = mark_lookup(case)
    structural = marks["S4"]
    require(structural.opening is not None, "S4 opening was not supplied")
    structural_edges = induced_edges(case.edges, structural.vertices)
    deleted = induced_edges(case.edges, complement) - structural_edges
    owner = next(part for part in components(complement, deleted)
                 if structural.opening in part)
    retained = complement - owner
    require(connected(owner, induced_edges(case.edges, owner)),
            "computed S4 owner fibre is disconnected")
    require(connected(retained, induced_edges(case.edges, retained)),
            "computed S4 retained side is disconnected")
    retained_core = structural.vertices - {structural.opening}
    require(retained_core <= retained and shape_of_block(
        retained_core, induced_edges(case.edges, retained_core)) == "K4",
        "computed S4 retained core is not its physical K4")
    q = sum(mark.kind == "T" and mark.vertices <= owner for mark in case.marks)
    return owner, retained, q


def derive_r41(case: PhysicalCase, complement: frozenset[Vertex],
               hostile: Territory) -> tuple[str, tuple[str, ...], tuple[tuple[str, str], ...],
                                              tuple[Territory, ...], tuple[OpeningRecord, ...],
                                              tuple[tuple[str, str], ...]]:
    model = subcase_model(case, complement)
    marks = mark_lookup(case)
    owner, unused_retained, q = structural_owner(case, complement)
    opening = marks["S4"].opening
    require(opening is not None, "S4 opening is absent")
    f_core = marks["S4"].vertices - {opening}
    owner_piece = make_territory(case, "structural-owner", owner)
    triangles = tuple(sorted(mark.name for mark in case.marks if mark.kind == "T"))
    outside = tuple(name for name in triangles if not marks[name].vertices <= owner)
    if q == 0:
        direct = tuple(name for name in outside
                       if marked_path(model, "S4", name) == ("S4", name)
                       and not path_has_bridge(model, "S4", name))
        require(direct, "R41 representative has no direct retained-side triangle")
        chosen = direct[0]
        anchor_vertices = f_core | marks[chosen].vertices
        pieces, openings = component_pieces(
            case, complement,
            ((owner_piece.name, owner_piece.vertices), ("anchor", anchor_vertices)),
            model, "S4", tuple(name for name in outside if name != chosen))
        require(pieces[0] == owner_piece, "structural owner piece changed")
        ledger = [(owner_piece.name, "TREE"), (pieces[1].name, "K4T")]
        ledger.extend((territory.name, tag_for_side(territory)) for territory in pieces[2:])
        return ("retained-direct-T", (chosen,), (("owner_triangles", "0"),),
                (hostile, *pieces), openings, tuple(ledger))
    if q == 1:
        require(len(outside) == 1, "one-owner R41 does not leave one triangle")
        anchor = make_territory(case, "anchor", f_core)
        pieces, openings = component_pieces(
            case, complement,
            ((owner_piece.name, owner_piece.vertices), (anchor.name, anchor.vertices)),
            model, "S4", outside)
        ledger = [(owner_piece.name, "TRIANGULAR"), (anchor.name, "F")]
        ledger.extend((territory.name, tag_for_side(territory)) for territory in pieces[2:])
        return ("opened-owner-one-T", tuple(name for name in triangles
                                             if marks[name].vertices <= owner),
                (("owner_triangles", "1"),), (hostile, *pieces), openings, tuple(ledger))
    require(q == 2 and not outside, "two-owner R41 owner census changed")
    anchor = make_territory(case, "anchor", f_core)
    require(complement == owner_piece.vertices | anchor.vertices
            and not (owner_piece.vertices & anchor.vertices),
            "two-owner R41 pieces do not partition the complement")
    ledger = ((owner_piece.name, "RANK_GE_2"), (anchor.name, "F"))
    return ("opened-owner-two-T", triangles, (("owner_triangles", "2"),),
            (hostile, owner_piece, anchor), (), ledger)


def verify_partition(case: PhysicalCase, territories: tuple[Territory, ...]) -> None:
    require(territories and len({territory.name for territory in territories}) == len(territories),
            "territory names are not unique")
    union = set().union(*(territory.vertices for territory in territories))
    require(union == set(case.vertices), "territories omit a physical vertex")
    require(sum(len(territory.vertices) for territory in territories) == len(union),
            "territories duplicate a physical vertex")
    for territory in territories:
        expected_edges = induced_edges(case.edges, territory.vertices)
        require(territory.edges == expected_edges, f"{territory.name} is not induced")
        require(territory.rank == graph_rank(territory.vertices, territory.edges),
                f"{territory.name} rank was not recomputed")
        require(connected(territory.vertices, territory.edges),
                f"{territory.name} is disconnected")
    for payload in case.payload_groups:
        owners = [territory.name for territory in territories if payload <= territory.vertices]
        require(len(owners) == 1, "rooted payload does not follow one physical owner")


def verify_certificate_core(case: PhysicalCase, certificate: ReplayCertificate) -> None:
    model = validate_profile(case)
    require(certificate.case_name == case.name and certificate.profile == case.profile,
            "certificate belongs to another physical case")
    require(certificate.topology == topology_signature(model),
            "block-cut topology changed under an old routing receipt")
    bridge, hostile, complement = split_hostile(case, model)
    require(certificate.hostile_bridge == bridge and certificate.hostile_vertices == hostile,
            "hostile actual-bridge split changed")
    verify_partition(case, certificate.territories)
    hostile_pieces = [territory for territory in certificate.territories
                      if territory.vertices == hostile]
    require(len(hostile_pieces) == 1, "hostile side is not one complete territory")
    complement_model = subcase_model(case, complement)
    for opening in certificate.openings:
        cut, vertices = boundary_open(complement_model, opening.root_mark,
                                      opening.target_mark)
        require((cut, vertices) == (opening.cut, opening.vertices),
                "boundary-opening receipt is not the complete rooted away side")
        require(cut not in vertices, "boundary cut was copied downstream")
        owners = [territory for territory in certificate.territories
                  if cut in territory.vertices]
        require(len(owners) == 1, "boundary cut is not upstream-only")
    territory_by_name = {territory.name: territory for territory in certificate.territories}
    require(len(certificate.ledger) == len(territory_by_name) - 1,
            "conditional ledger does not cover exactly the hostile complement")
    ledger_names = {name for name, unused_tag in certificate.ledger}
    require(ledger_names == set(territory_by_name) - {hostile_pieces[0].name},
            "conditional ledger omits or charges a complement territory twice")
    total = Bound(0, False)
    for name, tag in certificate.ledger:
        validate_bound_tag(territory_by_name[name], tag)
        total += BOUND_TABLE[tag]
    require(total.above(1), "representative hostile complement did not reconstruct a >1 ledger")


def derive_certificate(case: PhysicalCase) -> ReplayCertificate:
    model = validate_profile(case)
    bridge, hostile_vertices, complement = split_hostile(case, model)
    hostile = make_territory(case, "hostile", hostile_vertices)
    if case.profile == "R21":
        branch, selected, details, territories, openings, ledger = derive_r21(
            case, complement, hostile)
    elif case.profile == "R31-K":
        branch, selected, details, territories, openings, ledger = derive_r31(
            case, complement, hostile)
    elif case.profile == "R321":
        branch, selected, details, territories, openings, ledger = derive_r321(
            case, complement, hostile)
    elif case.profile == "R41":
        branch, selected, details, territories, openings, ledger = derive_r41(
            case, complement, hostile)
    else:
        raise AuditError("profile dispatch escaped validation")
    certificate = ReplayCertificate(
        case_name=case.name,
        profile=case.profile,
        branch=branch,
        topology=topology_signature(model),
        hostile_bridge=bridge,
        hostile_vertices=hostile_vertices,
        selected_marks=selected,
        details=details,
        openings=openings,
        territories=territories,
        ledger=ledger,
    )
    verify_certificate_core(case, certificate)
    return certificate


def verify_old_receipt(case: PhysicalCase, certificate: ReplayCertificate) -> None:
    verify_certificate_core(case, certificate)
    fresh = derive_certificate(case)
    require(fresh == certificate, "physical replay derives a different semantic receipt")


def representative_cases() -> tuple[PhysicalCase, ...]:
    return (
        build_r21(),
        build_r31("r31-direct", False, False),
        build_r31("r31-intermediate", True, True),
        build_r321("r321-intermediate", 3, False),
        build_r321("r321-direct", 3, True),
        build_r41("r41-retained", 0),
        build_r41("r41-owner-one", 1),
        build_r41("r41-owner-two", 2),
    )


def expect_rejected(action, label: str) -> None:
    try:
        action()
    except (AuditError, KeyError, ValueError):
        return
    raise AuditError(f"same-label laundering rewire was accepted: {label}")


def hostile_rewire_checks(certificates: dict[str, ReplayCertificate]) -> int:
    # 1. Insert a positive K2 connector into the T1 member of the old DTT anchor.
    expect_rejected(
        lambda: verify_old_receipt(build_r21(bridge_t1=True), certificates["r21-dtt"]),
        "K2 inserted into narrow DTT anchor")

    # 2. Move the old direct T0 behind the nontriangle boundary block.
    expect_rejected(
        lambda: verify_old_receipt(build_r31("r31-direct", True, False),
                                   certificates["r31-direct"]),
        "triangle moved behind nontriangle")

    # 3. Move a retained-side R41 triangle into the computed opening fibre.
    expect_rejected(
        lambda: verify_old_receipt(build_r41("r41-retained", 1),
                                   certificates["r41-retained"]),
        "R41 triangle moved from retained port to opening vertex")

    # 4. Split a repeated physical cut while preserving all block names and kinds.
    expect_rejected(
        lambda: verify_old_receipt(build_r21(split_repeated_cut=True),
                                   certificates["r21-dtt"]),
        "repeated cut split")

    # 5. Keep the shared cut but swap its diamond orbit from degree three to two.
    expect_rejected(
        lambda: verify_old_receipt(build_r321("r321-intermediate", 2, False),
                                   certificates["r321-intermediate"]),
        "diamond entry orbit swapped")

    # 6. Copy one connector payload into a second territory in the old receipt.
    baseline = build_r21()
    certificate = certificates["r21-dtt"]
    payload_vertex = next(iter(next(group for group in baseline.payload_groups
                                   if "P:payload" in group)))
    territories = list(certificate.territories)
    anchor_index = next(index for index, territory in enumerate(territories)
                        if territory.name == "anchor")
    changed_vertices = territories[anchor_index].vertices | {payload_vertex}
    territories[anchor_index] = make_territory(baseline, "anchor", changed_vertices)
    duplicated = replace(certificate, territories=tuple(territories))
    expect_rejected(lambda: verify_old_receipt(baseline, duplicated),
                    "connector payload duplicated")
    return 6


BLOCKERS = (
    "NONPROMOTIONAL: only eight explicit representative physical cases are replayed; no reduced-hull isomorphism generator has been audited.",
    "No contraction/expansion invariance proof covers arbitrary positive K2-chain lengths, cycle segment lengths, or every rooted-tree payload placement.",
    "The S4 replay authenticates one K4-plus-ear opening only; transport from every structural rank-four state and every physical port orbit is unproved.",
    "The numeric packet tags DTT, K4T, K4/F, triangular, and ranks two through six are conditional imported bounds, not rederived by this diagnostic.",
)


def run() -> dict[str, object]:
    cases = representative_cases()
    certificates = {case.name: derive_certificate(case) for case in cases}
    require(len(certificates) == len(cases), "representative case names collide")
    require({certificate.profile for certificate in certificates.values()}
            == {"R21", "R31-K", "R321", "R41"},
            "representative profile coverage changed")
    rejected = hostile_rewire_checks(certificates)
    return {
        "candidate_replays": len(certificates),
        "laundering_mutations_rejected": rejected,
        "unproved_completeness_blockers": list(BLOCKERS),
    }


def serialized_report() -> str:
    return json.dumps(run(), sort_keys=True, indent=2) + "\n"


def main() -> int:
    output = serialized_report()
    if not sys.flags.optimize and "--optimized-child" not in sys.argv:
        child = subprocess.run(
            [sys.executable, "-O", str(Path(__file__).resolve()), "--optimized-child"],
            check=False, capture_output=True, text=True)
        require(child.returncode == 0, "optimized candidate replay failed")
        require(child.stderr == "", "optimized candidate replay wrote stderr")
        require(child.stdout == output, "normal and optimized candidate reports differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
