#!/usr/bin/env python3
"""Exact incidence-core and induced-partition search for beta-five block graphs."""

from __future__ import annotations

import itertools
from dataclasses import dataclass

import networkx as nx


@dataclass(frozen=True)
class Core:
    sizes: tuple[int, ...]
    cuts: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class Bound:
    value: int
    strict: bool
    kinds: tuple[str, ...]

    def better_than(self, other: "Bound | None") -> bool:
        return other is None or (self.value, self.strict) > (other.value, other.strict)


def incidence_graph(core: Core) -> nx.Graph:
    graph = nx.Graph()
    for block, size in enumerate(core.sizes):
        graph.add_node(("b", block), kind=f"b{size}")
    for cut, blocks in enumerate(core.cuts):
        graph.add_node(("c", cut), kind="c")
        graph.add_edges_from((("c", cut), ("b", block)) for block in blocks)
    return graph


def same_core(left: Core, right: Core) -> bool:
    return nx.is_isomorphic(
        incidence_graph(left),
        incidence_graph(right),
        node_match=lambda x, y: x["kind"] == y["kind"],
    )


def enumerate_cores(sizes: tuple[int, ...]) -> list[Core]:
    block_count = len(sizes)
    subsets = [
        subset
        for width in range(2, block_count + 1)
        for subset in itertools.combinations(range(block_count), width)
    ]
    cores: list[Core] = []
    for cut_count in range(1, block_count):
        for cuts in itertools.combinations(subsets, cut_count):
            core = Core(sizes, cuts)
            incidence = incidence_graph(core)
            if incidence.number_of_edges() != incidence.number_of_nodes() - 1:
                continue
            if not nx.is_connected(incidence):
                continue
            if any(incidence.degree[("b", i)] > size for i, size in enumerate(sizes)):
                continue
            if any(same_core(core, old) for old in cores):
                continue
            cores.append(core)
    return cores


def realize(core: Core) -> tuple[nx.Graph, tuple[tuple[int, ...], ...], tuple[int, ...]]:
    graph = nx.Graph()
    cut_vertices = tuple(range(len(core.cuts)))
    next_vertex = len(cut_vertices)
    blocks: list[tuple[int, ...]] = []
    for block, size in enumerate(core.sizes):
        vertices = [cut for cut, incident in enumerate(core.cuts) if block in incident]
        private_count = size - len(vertices)
        vertices.extend(range(next_vertex, next_vertex + private_count))
        next_vertex += private_count
        graph.add_edges_from(itertools.combinations(vertices, 2))
        blocks.append(tuple(vertices))
    return graph, tuple(blocks), cut_vertices


def component_bound(graph: nx.Graph) -> Bound:
    n = graph.number_of_nodes()
    m = graph.number_of_edges()
    beta = m - n + 1
    if beta == 0:
        return Bound(n - 1, False, ("tree",))

    blocks = [graph.subgraph(vertices) for vertices in nx.biconnected_components(graph)]
    cyclic = [block for block in blocks if block.number_of_edges() >= block.number_of_nodes()]
    triangular = all(
        block.number_of_nodes() == 3 and block.number_of_edges() == 3 for block in cyclic
    )
    packing = 0
    if triangular:
        triangles = [frozenset(block.nodes) for block in cyclic]
        packing = max(
            (len(chosen) for width in range(len(triangles) + 1)
             for chosen in itertools.combinations(triangles, width)
             if len(set().union(*chosen)) == 3 * width),
            default=0,
        )
    k4_only = (
        len(cyclic) == 1
        and cyclic[0].number_of_nodes() == 4
        and cyclic[0].number_of_edges() == 6
    )

    candidates: list[Bound] = []
    if 1 <= beta <= 4:
        candidates.append(Bound(n, True, (f"rank-{beta}",)))
    if triangular and packing <= 2:
        candidates.append(Bound(m, True, (f"tri-pack-{packing}",)))
    if k4_only:
        candidates.append(Bound(m, True, ("K4-only",)))
    if not candidates:
        return Bound(n - 1, False, ("LTZ",))
    return max(candidates, key=lambda item: (item.value, item.strict))


def subset_bound(graph: nx.Graph, mask: int) -> Bound:
    vertices = [vertex for vertex in graph if mask >> vertex & 1]
    induced = graph.subgraph(vertices)
    value = 0
    strict = False
    kinds: list[str] = []
    for component in nx.connected_components(induced):
        bound = component_bound(induced.subgraph(component))
        value += bound.value
        strict |= bound.strict
        kinds.extend(bound.kinds)
    return Bound(value, strict, tuple(kinds))


def best_partition(graph: nx.Graph) -> tuple[Bound, tuple[int, ...]]:
    full = (1 << graph.number_of_nodes()) - 1
    bounds = [Bound(0, False, ())] + [subset_bound(graph, mask) for mask in range(1, full + 1)]
    best: list[Bound | None] = [None] * (full + 1)
    parts: list[tuple[int, ...]] = [()] * (full + 1)
    best[0] = Bound(0, False, ())
    for mask in range(1, full + 1):
        anchor = mask & -mask
        submask = mask
        while submask:
            if submask & anchor:
                remainder = mask ^ submask
                previous = best[remainder]
                assert previous is not None
                candidate = Bound(
                    previous.value + bounds[submask].value,
                    previous.strict or bounds[submask].strict,
                    previous.kinds + bounds[submask].kinds,
                )
                if candidate.better_than(best[mask]):
                    best[mask] = candidate
                    parts[mask] = parts[remainder] + (submask,)
            submask = (submask - 1) & mask
    assert best[full] is not None
    return best[full], parts[full]


def mask_vertices(mask: int) -> tuple[int, ...]:
    return tuple(vertex for vertex in range(mask.bit_length()) if mask >> vertex & 1)


def describe(core: Core) -> str:
    labels = [f"Q{i}" if size == 4 else f"T{i}" for i, size in enumerate(core.sizes)]
    return " ".join("(" + ",".join(labels[i] for i in cut) + ")" for cut in core.cuts)


def private_breaks(
    graph: nx.Graph, blocks: tuple[tuple[int, ...], ...], target_size: int
) -> tuple[tuple[int, int, Bound], ...]:
    witnesses: list[tuple[int, int, Bound]] = []
    full = (1 << graph.number_of_nodes()) - 1
    for block_index, block in enumerate(blocks):
        if len(block) != target_size:
            continue
        private = [
            vertex
            for vertex in block
            if sum(vertex in other for other in blocks) == 1
        ]
        for vertex in private:
            bound = subset_bound(graph, full ^ (1 << vertex))
            if any(kind.startswith("tri-pack-") for kind in bound.kinds):
                witnesses.append((block_index, vertex, bound))
    return tuple(witnesses)


def main() -> None:
    cases = (((4, 3, 3), 3), ((3, 3, 3, 3, 3), 8))
    for sizes, expected_count in cases:
        cores = enumerate_cores(sizes)
        assert len(cores) == expected_count
        print(f"type={sizes} cores={len(cores)}")
        for index, core in enumerate(cores, 1):
            graph, blocks, cuts = realize(core)
            bound, parts = best_partition(graph)
            assert bound.strict and bound.value >= len(graph)
            breaks = private_breaks(graph, blocks, 4 if 4 in sizes else 3)
            if 4 in sizes:
                assert any(block == 0 for block, _, _ in breaks)
            elif not any(
                kind.startswith("tri-pack-") for kind in component_bound(graph).kinds
            ):
                assert any(witness.value >= len(graph) + 1 for _, _, witness in breaks)
            relation = ">" if bound.strict else ">="
            print(
                f"{index:02d} cuts={describe(core):35s} n={len(graph):2d} "
                f"certificate={bound.value}{relation} parts="
                + " | ".join(str(mask_vertices(mask)) for mask in parts)
                + f" kinds={bound.kinds} blocks={blocks} cutverts={cuts}"
            )


if __name__ == "__main__":
    main()
