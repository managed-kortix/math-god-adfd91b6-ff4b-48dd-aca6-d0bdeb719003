#!/usr/bin/env python3
"""NONPROMOTIONAL adjacency scout for the R21 theta owner-fibre split.

This is a semantic fixture test, not the source of the arbitrary-r theorem.
The analytic DNN residual classification supplies the family of physically
given maximal blocks B=Theta(1,2,r), r>=2; the maximal-block owner-fibre lemma
then works uniformly in r.  This executable materializes r=2,3 regression
fixtures, authenticates their Tarjan blocks from adjacency, recovers the three
physical theta path lengths, and constructs complete first-B owner fibres as
components of G-E(B).  The reported split checks connected, induced, disjoint,
exhaustive original-vertex territories.  It makes no spectral or lane-state
claim.
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Hashable


REPO = Path(__file__).resolve().parents[1]
HELPER = REPO / "research/r21-literal-cycle-typing-verifier.py"
spec = importlib.util.spec_from_file_location("r21_literal_helper", HELPER)
assert spec and spec.loader
helper = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = helper
spec.loader.exec_module(helper)

Vertex = Hashable
Edge = frozenset[Vertex]
PhysicalGraph = helper.PhysicalGraph
edge = helper.edge


@dataclass(frozen=True)
class Fixture:
    r: int
    pattern: str
    graph: PhysicalGraph
    designated: str


def theta(r: int) -> tuple[set[Vertex], set[Edge], tuple[str, str, str], tuple[str, ...]]:
    assert isinstance(r, int) and not isinstance(r, bool) and r >= 2
    x, y, a = "B:x", "B:y", "B:a"
    vertices: set[Vertex] = {x, y, a}
    edges: set[Edge] = {edge(x, y), edge(x, a), edge(a, y)}
    previous = x
    internal = []
    for index in range(1, r):
        vertex = f"B:q{index}"
        internal.append(vertex)
        vertices.add(vertex)
        edges.add(edge(previous, vertex))
        previous = vertex
    edges.add(edge(previous, y))
    return vertices, edges, (x, y, a), tuple(internal)


def add_triangle(vertices: set[Vertex], edges: set[Edge], owner: Vertex, label: str) -> None:
    left, right = f"{label}:a", f"{label}:b"
    assert owner in vertices and left not in vertices and right not in vertices
    vertices.update((left, right))
    edges.update((edge(owner, left), edge(left, right), edge(right, owner)))


def build_fixture(r: int, pattern: str) -> Fixture:
    vertices, edges, (x, y, a), internal = theta(r)
    designated = internal[0]
    if pattern == "clean-repeated-owner":
        # Five distinct blocks have the same physical owner x; the designated
        # internal theta fibre stays acyclic.
        for index in range(5):
            add_triangle(vertices, edges, x, f"T{index}")
    elif pattern == "clean-nested-chain":
        # Every triangle after T0 is a nested descendant of the previous one.
        owner: Vertex = x
        for index in range(5):
            add_triangle(vertices, edges, owner, f"T{index}")
            owner = f"T{index}:a"
    elif pattern == "cyclic-designated-fibre":
        # Two triangles share the designated owner while the other three use
        # distinct theta owners.  This exercises the immediate positive-fibre
        # branch rather than miscalling the complete fibre a tree.
        owners = (designated, designated, x, y, a)
        for index, owner in enumerate(owners):
            add_triangle(vertices, edges, owner, f"T{index}")
    else:
        raise AssertionError(f"unknown fixture pattern: {pattern}")
    return Fixture(
        r=r,
        pattern=pattern,
        graph=PhysicalGraph(frozenset(vertices), frozenset(edges)),
        designated=designated,
    )


def cyclic_blocks(graph: PhysicalGraph) -> tuple[frozenset[Edge], ...]:
    return tuple(
        block
        for block in helper.biconnected_edge_blocks(graph.vertices, graph.edges)
        if helper.block_rank(block) > 0
    )


def trace_theta_path(block: frozenset[Edge], start: Vertex, end: Vertex,
                     first: Vertex) -> tuple[Vertex, ...]:
    vertices = helper.block_vertices(block)
    path = [start, first]
    previous, current = start, first
    while current != end:
        choices = [
            vertex for vertex in vertices
            if vertex != current and vertex != previous and edge(current, vertex) in block
        ]
        assert len(choices) == 1
        previous, current = current, choices[0]
        path.append(current)
    return tuple(path)


def authenticate_theta_profile(fixture: Fixture) -> tuple[frozenset[Edge], tuple[tuple[Vertex, ...], ...]]:
    graph = fixture.graph
    helper.adjacency(graph.vertices, graph.edges)
    assert helper.connected(graph.vertices, graph.edges)
    blocks = cyclic_blocks(graph)
    ranks = sorted(helper.block_rank(block) for block in blocks)
    assert ranks == [1, 1, 1, 1, 1, 2]
    triangle_blocks = [block for block in blocks if helper.block_rank(block) == 1]
    assert len(triangle_blocks) == 5
    assert all(helper.authenticate_literal_cycle(block) == 3 for block in triangle_blocks)
    theta_blocks = [block for block in blocks if helper.block_rank(block) == 2]
    assert len(theta_blocks) == 1
    block = theta_blocks[0]
    degrees = helper.block_degrees(block)
    branches = sorted((vertex for vertex, degree in degrees.items() if degree == 3), key=repr)
    assert len(branches) == 2
    start, end = branches
    neighbors = [
        vertex for vertex in helper.block_vertices(block)
        if vertex != start and edge(start, vertex) in block
    ]
    paths = tuple(trace_theta_path(block, start, end, first) for first in neighbors)
    lengths = sorted(len(path) - 1 for path in paths)
    assert lengths == sorted((1, 2, fixture.r))
    designated_paths = [path for path in paths if fixture.designated in path[1:-1]]
    assert len(designated_paths) == 1 and len(designated_paths[0]) - 1 == fixture.r
    assert sum(helper.block_rank(current) for current in blocks) == 7
    return block, tuple(sorted(paths, key=lambda path: (len(path), tuple(map(repr, path)))))


def induced_edges(graph: PhysicalGraph, vertices: frozenset[Vertex]) -> frozenset[Edge]:
    return frozenset(current for current in graph.edges if current <= vertices)


def owner_fibres(graph: PhysicalGraph, block: frozenset[Edge]) -> dict[Vertex, frozenset[Vertex]]:
    # This is deliberately the physical definition: remove all and only edges
    # of the authenticated maximal theta block, then derive components.
    answer: dict[Vertex, frozenset[Vertex]] = {}
    for component in helper.components(graph.vertices, graph.edges - block):
        intersection = component & helper.block_vertices(block)
        assert len(intersection) == 1
        owner = next(iter(intersection))
        assert owner not in answer
        answer[owner] = component
    assert set().union(*(set(part) for part in answer.values())) == set(graph.vertices)
    assert sum(map(len, answer.values())) == len(graph.vertices)
    for owner, fibre in answer.items():
        assert owner in fibre
        assert helper.connected(fibre, induced_edges(graph, fibre))
        complement = graph.vertices - fibre
        assert complement
        assert helper.connected(complement, induced_edges(graph, complement))
    return answer


def triangle_count_inside(graph: PhysicalGraph, vertices: frozenset[Vertex]) -> int:
    return sum(
        helper.block_rank(block) == 1
        and helper.authenticate_literal_cycle(block) == 3
        and helper.block_vertices(block) <= vertices
        for block in cyclic_blocks(graph)
    )


def verify_fixture(fixture: Fixture) -> dict[str, object]:
    block, paths = authenticate_theta_profile(fixture)
    fibres = owner_fibres(fixture.graph, block)
    designated = fixture.designated
    assert designated in fibres
    opened = fibres[designated]
    retained = fixture.graph.vertices - opened
    opened_triangles = triangle_count_inside(fixture.graph, opened)
    retained_triangles = triangle_count_inside(fixture.graph, retained)
    # The intrinsic x-a-y-x triangle is part of the theta block, not one of the
    # five external Tarjan blocks; deleting an internal vertex of the other arm
    # retains it exactly.
    intrinsic = frozenset(("B:x", "B:a", "B:y"))
    assert intrinsic <= retained
    assert all(edge(left, right) in induced_edges(fixture.graph, retained)
               for left, right in (("B:x", "B:a"), ("B:a", "B:y"), ("B:y", "B:x")))
    assert opened_triangles + retained_triangles == 5
    if opened_triangles == 0:
        assert len(induced_edges(fixture.graph, opened)) == len(opened) - 1
        branch = "tree / retained six-triangle cactus"
        assert retained_triangles == 5
    else:
        branch = "cyclic triangular owner fibre / lower-rank complement"
        assert retained_triangles == 5 - opened_triangles
    return {
        "branch": branch,
        "designated": designated,
        "external_triangles_in_opened_fibre": opened_triangles,
        "external_triangles_in_retained_complement": retained_triangles,
        "owner_fibre_sizes": {str(owner): len(vertices) for owner, vertices in sorted(fibres.items(), key=lambda item: repr(item[0]))},
        "pattern": fixture.pattern,
        "r": fixture.r,
        "theta_path_lengths": [len(path) - 1 for path in paths],
    }


def hostile_checks() -> tuple[str, ...]:
    labels = []
    fixture = build_fixture(3, "clean-repeated-owner")
    block, _ = authenticate_theta_profile(fixture)
    # Removing only one arm edge is not G-E(B) and cannot be accepted as the
    # first-block fibre construction: one resulting component meets B many times.
    wrong_components = helper.components(fixture.graph.vertices,
                                         fixture.graph.edges - frozenset((edge("B:x", "B:q1"),)))
    assert any(len(component & helper.block_vertices(block)) > 1 for component in wrong_components)
    labels.append("partial block-edge deletion rejected by owner contract")
    # A symbolic label has no role in any physical dispatch.
    try:
        authenticate_theta_profile(Fixture(3, "label-only", "Theta(1,2,3)+T^5", "B:q1"))  # type: ignore[arg-type]
    except (AttributeError, AssertionError, TypeError):
        labels.append("symbolic profile without adjacency rejected")
    else:
        raise AssertionError("symbolic profile passed adjacency authentication")
    return tuple(labels)


def main() -> None:
    reports = [
        verify_fixture(build_fixture(r, pattern))
        for r in (2, 3)
        for pattern in (
            "clean-repeated-owner",
            "clean-nested-chain",
            "cyclic-designated-fibre",
        )
    ]
    assert len(reports) == 6
    assert sum(report["branch"].startswith("tree") for report in reports) == 4
    assert sum(report["branch"].startswith("cyclic") for report in reports) == 2
    print("NONPROMOTIONAL R21 theta owner-fibre adjacency scout")
    print("authenticated fixtures:", len(reports))
    for report in reports:
        print(report)
    print("hostile rejections:", hostile_checks())
    print("SCOPE: r=2,3 fixtures are semantic regressions only; the uniform theorem assumes a physically given maximal B=Theta(1,2,r) and follows from the maximal-block ear lemma, not fixture extrapolation.")


if __name__ == "__main__":
    main()
