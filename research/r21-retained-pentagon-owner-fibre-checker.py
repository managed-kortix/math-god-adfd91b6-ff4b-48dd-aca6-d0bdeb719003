#!/usr/bin/env python3
"""Bounded exact/structural checker for the disputed retained-C5 R21 branch.

This is deliberately NONPROMOTIONAL.  It constructs two materialized
D+T^4+C5 graphs: one in which an actual bridge isolates C5 and one in which
C5 shares a cut vertex with D+4T.  A local Tarjan edge-stack decomposition
checks the positive-rank block inventory.  Deleting the C5 edges then checks
its owner fibres on original vertices.  Integer characteristic polynomials are
computed by the exact Faddeev--LeVerrier recurrence; numerical surplus
is printed only as counterexample-search evidence, never as proof.

The point is scope: a gate requiring an isolating C5 bridge is not exhaustive
for the physical D+T^4+C5 row.  The shared-cut fixture has exactly the claimed
block inventory and a valid retained-pentagon owner-fibre partition, but no
bridge at all.
"""

from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from typing import Hashable


class AuditError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


Vertex = Hashable
Edge = frozenset[Vertex]


def edge(left: Vertex, right: Vertex) -> Edge:
    require(left != right, "loop in a simple graph")
    return frozenset((left, right))


@dataclass(frozen=True)
class Graph:
    vertices: frozenset[Vertex]
    edges: frozenset[Edge]


def adjacency(graph: Graph, edges: frozenset[Edge] | None = None) -> dict[Vertex, set[Vertex]]:
    use = graph.edges if edges is None else edges
    table = {vertex: set() for vertex in graph.vertices}
    for current in use:
        require(type(current) is frozenset and len(current) == 2,
                "edge is not a two-element frozenset")
        left, right = tuple(current)
        require(left in table and right in table, "edge endpoint missing")
        require(right not in table[left], "parallel edge")
        table[left].add(right)
        table[right].add(left)
    return table


def components(vertices: frozenset[Vertex], edges: frozenset[Edge]) -> tuple[frozenset[Vertex], ...]:
    table = adjacency(Graph(vertices, edges))
    unseen = set(vertices)
    answer = []
    while unseen:
        root = min(unseen, key=repr)
        reached = {root}
        queue = deque((root,))
        unseen.remove(root)
        while queue:
            current = queue.popleft()
            for neighbor in table[current]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    reached.add(neighbor)
                    queue.append(neighbor)
        answer.append(frozenset(reached))
    return tuple(answer)


def connected(graph: Graph) -> bool:
    return len(components(graph.vertices, graph.edges)) == 1


def block_vertices(block: frozenset[Edge]) -> frozenset[Vertex]:
    return frozenset(vertex for current in block for vertex in current)


def block_rank(block: frozenset[Edge]) -> int:
    return len(block) - len(block_vertices(block)) + 1


def biconnected_edge_blocks(graph: Graph) -> tuple[frozenset[Edge], ...]:
    """Tarjan edge-stack decomposition; isolated vertices are irrelevant here."""
    table = adjacency(graph)
    discovery: dict[Vertex, int] = {}
    low: dict[Vertex, int] = {}
    parent: dict[Vertex, Vertex | None] = {}
    stack: list[Edge] = []
    blocks: list[frozenset[Edge]] = []
    clock = 0

    def visit(current: Vertex) -> None:
        nonlocal clock
        clock += 1
        discovery[current] = low[current] = clock
        for neighbor in sorted(table[current], key=repr):
            current_edge = edge(current, neighbor)
            if neighbor not in discovery:
                parent[neighbor] = current
                stack.append(current_edge)
                visit(neighbor)
                low[current] = min(low[current], low[neighbor])
                if low[neighbor] >= discovery[current]:
                    block = []
                    while stack:
                        popped = stack.pop()
                        block.append(popped)
                        if popped == current_edge:
                            break
                    require(block, "empty Tarjan block")
                    blocks.append(frozenset(block))
            elif parent.get(current) != neighbor and discovery[neighbor] < discovery[current]:
                stack.append(current_edge)
                low[current] = min(low[current], discovery[neighbor])

    for root in sorted(graph.vertices, key=repr):
        if root not in discovery:
            parent[root] = None
            visit(root)
            require(not stack, "Tarjan stack not empty at component end")
    require(frozenset(current for block in blocks for current in block) == graph.edges,
            "Tarjan blocks do not partition edges")
    return tuple(blocks)


def literal_cycle_length(block: frozenset[Edge]) -> int | None:
    vertices = block_vertices(block)
    degrees = {vertex: 0 for vertex in vertices}
    for current in block:
        left, right = tuple(current)
        degrees[left] += 1
        degrees[right] += 1
    if len(block) == len(vertices) and all(value == 2 for value in degrees.values()):
        return len(vertices)
    return None


def diamond(block: frozenset[Edge]) -> bool:
    vertices = block_vertices(block)
    degrees = {vertex: 0 for vertex in vertices}
    for current in block:
        left, right = tuple(current)
        degrees[left] += 1
        degrees[right] += 1
    return len(vertices) == 4 and len(block) == 5 and sorted(degrees.values()) == [2, 2, 3, 3]


def add_triangle(vertices: set[Vertex], edges: set[Edge], root: Vertex, tag: str) -> None:
    left, right = f"{tag}:u", f"{tag}:v"
    vertices.update((left, right))
    edges.update((edge(root, left), edge(left, right), edge(right, root)))


def fixture(kind: str) -> tuple[Graph, frozenset[Edge]]:
    """Build shared, isolated, or retained-C5-plus-away-group materializations."""
    require(kind in {"shared", "isolated", "root_scoped"}, "unknown fixture kind")
    # D=Theta(1,2,2), with branch vertices x,y and private arm vertices a,p.
    vertices: set[Vertex] = {"x", "y", "a", "p"}
    edges: set[Edge] = {
        edge("x", "y"), edge("x", "a"), edge("a", "y"),
        edge("x", "p"), edge("p", "y"),
    }
    root_triangle_count = 3 if kind == "root_scoped" else 4
    for index in range(root_triangle_count):
        add_triangle(vertices, edges, "x", f"T{index}")
    root = "x" if kind != "isolated" else "w"
    c5_vertices = (root, "c1", "c2", "c3", "c4")
    vertices.update(c5_vertices)
    c5_edges = frozenset(edge(c5_vertices[index], c5_vertices[(index + 1) % 5])
                         for index in range(5))
    edges.update(c5_edges)
    if kind == "isolated":
        edges.add(edge("x", "w"))
    if kind == "root_scoped":
        # T3 lies beyond the first actual bridge x--b.  The C5 is retained at x.
        vertices.add("b")
        edges.add(edge("x", "b"))
        add_triangle(vertices, edges, "b", "T3")
    return Graph(frozenset(vertices), frozenset(edges)), c5_edges


def inventory(graph: Graph) -> dict[str, object]:
    require(connected(graph), "fixture disconnected")
    blocks = biconnected_edge_blocks(graph)
    positive = tuple(block for block in blocks if block_rank(block) > 0)
    bridges = tuple(block for block in blocks if block_rank(block) == 0)
    require(all(len(block) == 1 for block in bridges), "rank-zero block is not K2")
    rank_two = tuple(block for block in positive if block_rank(block) == 2)
    cycles = tuple(block for block in positive if block_rank(block) == 1)
    require(len(rank_two) == 1 and diamond(rank_two[0]), "missing literal diamond")
    lengths = tuple(sorted(literal_cycle_length(block) for block in cycles))
    require(lengths == (3, 3, 3, 3, 5), "wrong cycle inventory")
    require(len(graph.edges) - len(graph.vertices) + 1 == 7, "wrong graph rank")
    return {
        "vertices": len(graph.vertices),
        "edges": len(graph.edges),
        "rank": 7,
        "positive_block_ranks": [2, 1, 1, 1, 1, 1],
        "cycle_lengths": list(lengths),
        "bridge_blocks": len(bridges),
    }


def owner_fibres(graph: Graph, c5_edges: frozenset[Edge]) -> dict[str, object]:
    c5_vertices = block_vertices(c5_edges)
    remainder = graph.edges - c5_edges
    parts = components(graph.vertices, remainder)
    owners = []
    for part in parts:
        meet = part & c5_vertices
        require(len(meet) == 1, "owner component does not meet C5 exactly once")
        owners.append((next(iter(meet)), part))
    require(len(owners) == 5, "C5 did not produce five owner fibres")
    require(frozenset().union(*(part for unused_owner, part in owners)) == graph.vertices,
            "owner fibres not exhaustive")
    upstream = next(part for owner, part in owners if owner == ("x" if "x" in c5_vertices else "w"))
    downstream = graph.vertices - upstream
    # The four nonparent C5 vertices induce a path, linking the four fibres.
    down_edges = frozenset(current for current in graph.edges if current <= downstream)
    require(connected(Graph(downstream, down_edges)), "downstream C5 remnant disconnected")
    require(connected(Graph(upstream, frozenset(current for current in graph.edges if current <= upstream))),
            "upstream owner fibre disconnected")
    crossing = tuple(sorted((tuple(sorted(map(repr, current))) for current in graph.edges
                             if current & upstream and current & downstream)))
    require(len(crossing) == 2, "owner opening should cross two C5 edges")
    return {
        "owner_fibres": len(owners),
        "owner_sizes": sorted(len(part) for unused_owner, part in owners),
        "upstream_vertices": len(upstream),
        "downstream_vertices": len(downstream),
        "crossing_edges": [list(current) for current in crossing],
    }


def matmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    order = len(left)
    return [[sum(left[row][middle] * right[middle][column] for middle in range(order))
             for column in range(order)] for row in range(order)]


def characteristic_polynomial(graph: Graph) -> tuple[int, ...]:
    """Exact integer coefficients of det(lambda I-A), descending order."""
    labels = sorted(graph.vertices, key=repr)
    index = {vertex: position for position, vertex in enumerate(labels)}
    order = len(labels)
    matrix = [[0] * order for unused in range(order)]
    for current in graph.edges:
        left, right = tuple(current)
        matrix[index[left]][index[right]] = matrix[index[right]][index[left]] = 1
    identity = [[int(row == column) for column in range(order)] for row in range(order)]
    previous = [row[:] for row in identity]
    coefficients = [1]
    for step in range(1, order + 1):
        product = matmul(matrix, previous)
        trace = sum(product[index][index] for index in range(order))
        coefficient = Fraction(-trace, step)
        require(coefficient.denominator == 1, "characteristic coefficient nonintegral")
        value = coefficient.numerator
        coefficients.append(value)
        previous = [row[:] for row in product]
        for index in range(order):
            previous[index][index] += value
    return tuple(coefficients)


def numerical_sigma(graph: Graph) -> float | None:
    try:
        import numpy as np
    except ImportError:
        return None
    labels = sorted(graph.vertices, key=repr)
    index = {vertex: position for position, vertex in enumerate(labels)}
    matrix = np.zeros((len(labels), len(labels)), dtype=float)
    for current in graph.edges:
        left, right = tuple(current)
        matrix[index[left], index[right]] = matrix[index[right], index[left]] = 1.0
    eigenvalues = np.linalg.eigvalsh(matrix)
    return float(sum(value * value for value in eigenvalues if value > 1e-9) - len(labels))


def bridge_count(graph: Graph) -> int:
    return sum(block_rank(block) == 0 for block in biconnected_edge_blocks(graph))


def record(kind: str) -> dict[str, object]:
    graph, c5_edges = fixture(kind)
    exact_poly = characteristic_polynomial(graph)
    report = inventory(graph)
    report.update(owner_fibres(graph, c5_edges))
    report.update({
        "fixture": {
            "shared": "shared_cut_retained_c5",
            "isolated": "isolated_c5_bridge",
            "root_scoped": "retained_c5_with_first_bridge_away_triangle",
        }[kind],
        "actual_bridges": bridge_count(graph),
        "has_some_actual_bridge": bridge_count(graph) > 0,
        "charpoly": list(exact_poly),
        "charpoly_sha256": hashlib.sha256(
            (",".join(map(str, exact_poly)) + "\n").encode("ascii")).hexdigest(),
        "numerical_sigma_nonproof": numerical_sigma(graph),
    })
    if kind == "shared":
        require(report["actual_bridges"] == 0,
                "shared-cut witness unexpectedly has a bridge")
        require(report["owner_fibres"] == 5,
                "shared-cut witness lacks retained-C5 owner opening")
    elif kind == "isolated":
        require(report["actual_bridges"] == 1,
                "isolated fixture should have exactly one bridge")
    else:
        require(report["actual_bridges"] == 1,
                "root-scoping fixture should have exactly one bridge")
    return report


def hostile_checks() -> int:
    # Removing one C5 edge destroys the five-fibre owner opening.
    graph, c5_edges = fixture("shared")
    malformed = frozenset(tuple(c5_edges)[1:])
    try:
        owner_fibres(graph, malformed)
    except AuditError:
        pass
    else:
        raise AuditError("partial C5 edge deletion accepted as a five-owner opening")
    # A chord changes the positive-rank block inventory/rank.
    graph, unused = fixture("shared")
    chorded = Graph(graph.vertices, graph.edges | frozenset((edge("c1", "c3"),)))
    try:
        inventory(chorded)
    except AuditError:
        pass
    else:
        raise AuditError("chorded C5 accepted as D+T^4+C5")
    return 2


def root_group_scope_witness() -> dict[str, object]:
    """Show why the retained-C5 opening must run inside the induced root group."""
    graph, c5_edges = fixture("root_scoped")
    bridge = edge("x", "b")
    require(bridge in graph.edges, "root-scoping bridge missing")
    parts = components(graph.vertices, graph.edges - frozenset((bridge,)))
    require(len(parts) == 2, "first bridge did not split the fixture")
    root_vertices = next(part for part in parts if "x" in part)
    away_vertices = next(part for part in parts if "T3:u" in part)
    require(root_vertices.isdisjoint(away_vertices), "root/away groups overlap")
    require(root_vertices | away_vertices == graph.vertices, "root/away split not exhaustive")
    root = Graph(root_vertices,
                 frozenset(current for current in graph.edges if current <= root_vertices))
    root_report = owner_fibres(root, c5_edges)
    full_report = owner_fibres(graph, c5_edges)
    full_x_fibre = next(part for part in components(graph.vertices, graph.edges - c5_edges)
                        if "x" in part)
    root_x_fibre = next(part for part in components(root.vertices, root.edges - c5_edges)
                        if "x" in part)
    require(away_vertices <= full_x_fibre,
            "full-G C5 fibre unexpectedly excludes the first-bridge away group")
    require(away_vertices.isdisjoint(root_x_fibre),
            "R-scoped C5 fibre unexpectedly includes the away group")
    require(len(full_x_fibre) == len(root_x_fibre) + len(away_vertices),
            "full/root fibre size difference is not exactly the away group")
    return {
        "fixture": "retained_c5_with_first_bridge_away_triangle",
        "first_bridge": sorted(map(repr, bridge)),
        "root_group_vertices": len(root_vertices),
        "away_group_vertices": len(away_vertices),
        "full_graph_parent_fibre_vertices": len(full_x_fibre),
        "root_scoped_parent_fibre_vertices": len(root_x_fibre),
        "full_graph_owner_fibres": full_report["owner_fibres"],
        "root_scoped_owner_fibres": root_report["owner_fibres"],
        "witness": (
            "Deleting C5 edges in full G absorbs the already separated away "
            "triangle into F_x; deleting them in induced root group R does not."
        ),
    }


def run() -> dict[str, object]:
    shared = record("shared")
    isolated = record("isolated")
    scoped = record("root_scoped")
    require(shared["cycle_lengths"] == isolated["cycle_lengths"]
            == scoped["cycle_lengths"],
            "the fixtures do not have the same cyclic profile")
    return {
        "status": "NONPROMOTIONAL_SCOPE_WITNESS",
        "isolated": isolated,
        "shared": shared,
        "retained_with_away_group": scoped,
        "root_group_scope": root_group_scope_witness(),
        "hostile_mutations_rejected": hostile_checks(),
        "conclusion": (
            "An actual-bridge-only C5 dispatch omits the legal shared-cut "
            "D+T^4+C5 state.  The retained-C5 opening is valid, but after a "
            "first-bridge split its owner fibres must be computed inside the "
            "induced root group R, not full G."
        ),
    }


def serialized_report() -> str:
    return json.dumps(run(), sort_keys=True, indent=2) + "\n"


def no_asserts() -> None:
    tree = ast.parse(open(__file__, "r", encoding="utf-8").read())
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
            "checker must not depend on Python assert")


def main() -> int:
    no_asserts()
    output = serialized_report()
    if not sys.flags.optimize and "--optimized-child" not in sys.argv:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-child"],
                               check=False, capture_output=True, text=True)
        require(child.returncode == 0, "optimized child failed")
        require(child.stderr == "", "optimized child wrote stderr")
        require(child.stdout == output, "normal/-O output mismatch")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
