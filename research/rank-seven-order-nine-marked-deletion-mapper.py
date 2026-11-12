#!/usr/bin/env python3
"""Fail-closed topology/provenance mapper for marked rank-six deletions.

The mapper performs no rank-six owner import and proves no spectral statement.
It authenticates the 1,615-row order-nine frontier, expands physical paths,
deletes a named physical occurrence, computes the exact block decomposition,
and, for a single rank-six block, suppresses degree-two vertices and maps the
result to the canonical rank-six kernel fixture.  Every selected map retains
an explicit isomorphism, oriented physical chains, the two deleted-endpoint
provenance coordinates, finite owner-target selection, and an explicit
zero-cost descendant insertion ledger.

The default pilot is deliberately bounded: the 80 durable favorable-cycle
residual targets plus the two hostile source-78714 deletions (occurrences 1 and
13) in the descendant that lengthens both occurrences.  ``--scope full`` uses
the same schema for all 1,615 rows and all 15 coordinate-frontier deletions.
Multiblock deletions are represented as topology records and are never routed
through a single-block rank-six fixture.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MINER = HERE / "rank-seven-order-nine-favorable-cycle-residual-miner.py"
RESIDUAL = HERE / "rank-seven-order-nine-favorable-cycle-residual.json"
RANK6_FIXTURE = HERE / "fixtures/rank-six-kernels.json"
DEFAULT_OUTPUT = HERE / "rank-seven-order-nine-marked-deletion-pilot-map.json"

ORDER9 = 9
PATH_COUNT9 = 15
# A rank-six kernel of order n has n+5 physical replacement paths.
HOSTILE_SOURCE_INDEX = 78714
HOSTILE_INCREMENT_PATHS = (1, 13)
EXPECTED = {
    "miner": "e0ec83d078390ea7f34d551d017e57ac68640216c96f323a7802e4d42eb239d8",
    "residual": "8a5073c977f7f7b3ca457dee056301e8bdc83e6e0b9974bf171d39b20cdaaac2",
    "rank6_fixture": "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def strict_json(path: Path, expected: str, label: str):
    require(sha256(path) == expected, f"{label} changed")

    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    raw = path.read_bytes()
    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(
                RuntimeError(f"nonstandard JSON constant in {label}: {token}")),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot parse {label}") from error
    return value


def load_module():
    require(sha256(MINER) == EXPECTED["miner"], "frontier miner changed")
    spec = importlib.util.spec_from_file_location("rank7_order9_marked_mapper_miner", MINER)
    require(spec is not None and spec.loader is not None, "cannot load frontier miner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def label_key(label):
    return tuple(label)


def json_label(label):
    if label[0] == "b":
        return ["branch", label[1]]
    require(label[0] == "p" and len(label) == 3, "unknown physical vertex label")
    return ["path", label[1], label[2]]


def pair_index(order: int):
    pairs = tuple(itertools.combinations(range(order), 2))
    return pairs, {pair: index for index, pair in enumerate(pairs)}


def fixture_graph(record):
    pairs, _ = pair_index(record["n"])
    adjacency = [[0] * record["n"] for _ in range(record["n"])]
    for (u, v), multiplicity in zip(pairs, record["code"], strict=True):
        adjacency[u][v] = adjacency[v][u] = multiplicity
    return adjacency


def graph_invariant(adjacency):
    order = len(adjacency)
    weighted = tuple(sorted(sum(row) for row in adjacency))
    unweighted = tuple(sorted(sum(value > 0 for value in row) for row in adjacency))
    multiplicities = tuple(sorted(
        adjacency[u][v] for u in range(order) for v in range(u + 1, order)
        if adjacency[u][v]
    ))
    signatures = tuple(sorted(
        (sum(adjacency[u]), sum(value > 0 for value in adjacency[u]),
         tuple(sorted(value for value in adjacency[u] if value)))
        for u in range(order)
    ))
    return order, weighted, unweighted, multiplicities, signatures


def vertex_signature(adjacency, vertex):
    row = adjacency[vertex]
    return (sum(row), sum(value > 0 for value in row),
            tuple(sorted(value for value in row if value)))


def isomorphisms(left_vertices, left_adjacency, right_adjacency):
    """Enumerate all exact maps from named left vertices to 0..n-1."""
    order = len(left_vertices)
    require(len(left_adjacency) == len(right_adjacency) == order,
            "isomorphism orders differ")
    left_index = {vertex: i for i, vertex in enumerate(left_vertices)}
    candidates = {
        vertex: tuple(
            target for target in range(order)
            if vertex_signature(left_adjacency, left_index[vertex]) ==
               vertex_signature(right_adjacency, target)
        )
        for vertex in left_vertices
    }
    require(all(candidates.values()), "vertex signatures preclude isomorphism")
    search_order = tuple(sorted(
        left_vertices,
        key=lambda vertex: (len(candidates[vertex]),
                            vertex_signature(left_adjacency, left_index[vertex]),
                            label_key(vertex)),
    ))
    mapping = {}
    used = set()
    output = []

    def visit(position):
        if position == order:
            output.append(dict(mapping))
            return
        vertex = search_order[position]
        i = left_index[vertex]
        for target in candidates[vertex]:
            if target in used:
                continue
            if any(left_adjacency[i][left_index[other]] !=
                   right_adjacency[target][mapped]
                   for other, mapped in mapping.items()):
                continue
            mapping[vertex] = target
            used.add(target)
            visit(position + 1)
            used.remove(target)
            del mapping[vertex]

    visit(0)
    return tuple(output)


class RankSixFixtures:
    def __init__(self, rows):
        require(isinstance(rows, list) and len(rows) == 1198,
                "rank-six fixture row count changed")
        self.rows = rows
        self.by_invariant = defaultdict(list)
        for kernel, record in enumerate(rows, 1):
            adjacency = fixture_graph(record)
            self.by_invariant[graph_invariant(adjacency)].append(
                (kernel, record, adjacency)
            )
        self.identification_cache = {}

    @classmethod
    def load(cls):
        payload = strict_json(RANK6_FIXTURE, EXPECTED["rank6_fixture"],
                              "rank-six fixture")
        require(payload.get("beta") == 6 and payload.get("orders") == [2, 10],
                "rank-six fixture scope changed")
        return cls(payload["kernels"])

    def identify(self, branch_vertices, adjacency, chains):
        key = (
            tuple(branch_vertices),
            tuple(tuple(row) for row in adjacency),
        )
        cached = self.identification_cache.get(key)
        if cached is None:
            candidates = []
            for kernel, record, fixture_adjacency in self.by_invariant.get(
                    graph_invariant(adjacency), ()):
                for mapping in isomorphisms(
                        branch_vertices, adjacency, fixture_adjacency):
                    candidates.append((kernel, record, mapping))
            kernel_ids = {kernel for kernel, _, _ in candidates}
            require(candidates, "suppressed rank-six kernel has no fixture isomorphism")
            require(len(kernel_ids) == 1,
                    "suppressed rank-six kernel identity is nonunique")
            cached = tuple(candidates)
            self.identification_cache[key] = cached

        kernel_ids = {kernel for kernel, _, _ in cached}
        require(len(kernel_ids) == 1, "cached fixture identity is nonunique")
        kernel = next(iter(kernel_ids))
        record = cached[0][1]
        pairs, indices = pair_index(record["n"])

        scored = []
        for _, _, mapping in cached:
            parity = [0] * len(pairs)
            for chain in chains:
                endpoints = tuple(sorted((mapping[chain["nodes"][0]],
                                          mapping[chain["nodes"][-1]])))
                parity[indices[endpoints]] += (len(chain["edges"]) & 1)
            require(all(value <= multiplicity for value, multiplicity in
                        zip(parity, record["code"], strict=True)),
                    "mapped parity exceeds fixture multiplicity")
            map_vector = tuple(mapping[vertex] for vertex in branch_vertices)
            scored.append((tuple(parity), map_vector, mapping))
        minimum_parity = min(item[0] for item in scored)
        canonical_parity_maps = [item for item in scored if item[0] == minimum_parity]
        selected = min(canonical_parity_maps, key=lambda item: item[1])
        require(sum(item[1] == selected[1] for item in canonical_parity_maps) == 1,
                "canonical full isomorphism selection is nonunique")
        return {
            "kernel": kernel,
            "record": record,
            "mapping": selected[2],
            "parity": selected[0],
            "isomorphism_count": len(scored),
            "canonical_parity_isomorphism_count": len(canonical_parity_maps),
        }


def validate_target(paths, target_lengths, deletion_index):
    require(isinstance(deletion_index, int) and not isinstance(deletion_index, bool)
            and 0 <= deletion_index < len(paths), "invalid deletion path index")
    require(isinstance(target_lengths, (list, tuple)) and
            len(target_lengths) == len(paths), "target length width changed")
    for index, (path, length) in enumerate(zip(paths, target_lengths, strict=True)):
        base = path[4]
        require(type(length) is int and length >= base and
                (length - base) % 2 == 0,
                f"target length is not a same-parity descendant at path {index}")


def expand_after_deletion(paths, target_lengths, deletion_index):
    validate_target(paths, target_lengths, deletion_index)
    vertices = {("b", vertex) for vertex in range(ORDER9)}
    edges = []
    seen_pairs = set()
    path_data = {}
    for path_index, ((support, occurrence, u, v, _), length) in enumerate(
            zip(paths, target_lengths, strict=True)):
        sequence = [("b", u)]
        sequence.extend(("p", path_index, distance) for distance in range(1, length))
        sequence.append(("b", v))
        path_data[path_index] = {
            "support": support,
            "occurrence": occurrence,
            "u": u,
            "v": v,
            "length": length,
            "nodes": tuple(sequence),
        }
        if path_index == deletion_index:
            continue
        vertices.update(sequence)
        for step, (left, right) in enumerate(zip(sequence, sequence[1:])):
            edge_key = frozenset((left, right))
            require(left != right and edge_key not in seen_pairs,
                    "expanded surviving realization is not simple")
            seen_pairs.add(edge_key)
            edges.append({
                "ends": (left, right),
                "physical_path": path_index,
                "step": step,
            })
    adjacency = {vertex: [] for vertex in vertices}
    for edge_id, edge in enumerate(edges):
        u, v = edge["ends"]
        adjacency[u].append((v, edge_id))
        adjacency[v].append((u, edge_id))
    return vertices, edges, adjacency, path_data


def connected_components(vertices, adjacency):
    unseen = set(vertices)
    components = []
    while unseen:
        start = min(unseen, key=label_key)
        seen = {start}
        pending = [start]
        while pending:
            vertex = pending.pop()
            for neighbor, _ in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    pending.append(neighbor)
        unseen -= seen
        components.append(seen)
    return tuple(components)


def biconnected_edge_components(vertices, edges, adjacency):
    discovery = {}
    low = {}
    clock = 0
    stack = []
    blocks = []

    def visit(vertex, parent_edge=None):
        nonlocal clock
        discovery[vertex] = low[vertex] = clock
        clock += 1
        for neighbor, edge_id in adjacency[vertex]:
            if edge_id == parent_edge:
                continue
            if neighbor not in discovery:
                stack.append(edge_id)
                visit(neighbor, edge_id)
                low[vertex] = min(low[vertex], low[neighbor])
                if low[neighbor] >= discovery[vertex]:
                    block = []
                    while True:
                        popped = stack.pop()
                        block.append(popped)
                        if popped == edge_id:
                            break
                    blocks.append(tuple(block))
            elif discovery[neighbor] < discovery[vertex]:
                stack.append(edge_id)
                low[vertex] = min(low[vertex], discovery[neighbor])

    for vertex in sorted(vertices, key=label_key):
        if vertex not in discovery:
            visit(vertex)
            require(not stack, "biconnected edge stack did not empty")

    ledger = []
    for block in blocks:
        block_vertices = set()
        for edge_id in block:
            block_vertices.update(edges[edge_id]["ends"])
        rank = len(block) - len(block_vertices) + 1
        ledger.append({
            "edge_ids": tuple(sorted(block)),
            "vertices": tuple(sorted(block_vertices, key=label_key)),
            "edge_total": len(block),
            "vertex_total": len(block_vertices),
            "rank": rank,
        })
    ledger.sort(key=lambda row: (-row["rank"], row["vertex_total"],
                                 tuple(label_key(v) for v in row["vertices"])))
    return tuple(ledger)


def trace_suppressed_chains(vertices, edges, adjacency):
    branch_vertices = tuple(sorted(
        (vertex for vertex in vertices if len(adjacency[vertex]) != 2),
        key=label_key,
    ))
    require(branch_vertices, "cannot suppress an all-degree-two component")
    branch_set = set(branch_vertices)
    visited = set()
    chains = []
    for start in branch_vertices:
        for neighbor, first_edge in sorted(
                adjacency[start], key=lambda item: (label_key(item[0]), item[1])):
            if first_edge in visited:
                continue
            nodes = [start, neighbor]
            chain_edges = [first_edge]
            visited.add(first_edge)
            previous_edge = first_edge
            current = neighbor
            while current not in branch_set:
                options = [(vertex, edge_id) for vertex, edge_id in adjacency[current]
                           if edge_id != previous_edge]
                require(len(options) == 1, "degree-two trace is ambiguous")
                next_vertex, next_edge = options[0]
                require(next_edge not in visited, "suppressed trace closed before a branch")
                visited.add(next_edge)
                chain_edges.append(next_edge)
                nodes.append(next_vertex)
                previous_edge = next_edge
                current = next_vertex
            require(nodes[0] != nodes[-1], "suppression produced a loop")
            chains.append({"nodes": tuple(nodes), "edges": tuple(chain_edges)})
    require(len(visited) == len(edges), "suppression omitted surviving edges")

    index = {vertex: i for i, vertex in enumerate(branch_vertices)}
    adjacency_matrix = [[0] * len(branch_vertices) for _ in branch_vertices]
    for chain in chains:
        u = index[chain["nodes"][0]]
        v = index[chain["nodes"][-1]]
        adjacency_matrix[u][v] += 1
        adjacency_matrix[v][u] += 1
    return branch_vertices, adjacency_matrix, tuple(chains)


def original_distance(label, physical_path, path_data):
    row = path_data[physical_path]
    if label == ("b", row["u"]):
        return 0
    if label == ("b", row["v"]):
        return row["length"]
    require(label[0] == "p" and label[1] == physical_path,
            "edge endpoint lacks its physical-path provenance")
    return label[2]


def oriented_chain(chain, mapping, edges, path_data):
    nodes = chain["nodes"]
    edge_ids = chain["edges"]
    mapped_start = mapping[nodes[0]]
    mapped_end = mapping[nodes[-1]]
    require(mapped_start != mapped_end, "mapped chain is a loop")
    if mapped_start > mapped_end:
        nodes = tuple(reversed(nodes))
        edge_ids = tuple(reversed(edge_ids))
        mapped_start, mapped_end = mapped_end, mapped_start

    edge_coordinates = []
    for position, edge_id in enumerate(edge_ids):
        physical_path = edges[edge_id]["physical_path"]
        start_distance = original_distance(nodes[position], physical_path, path_data)
        end_distance = original_distance(nodes[position + 1], physical_path, path_data)
        require(abs(start_distance - end_distance) == 1,
                "physical edge provenance distance changed")
        edge_coordinates.append((physical_path, start_distance, end_distance))

    segments = []
    for physical_path, start, end in edge_coordinates:
        if (segments and segments[-1][0] == physical_path and
                segments[-1][2] == start and
                (segments[-1][2] - segments[-1][1]) * (end - start) > 0):
            segments[-1] = (physical_path, segments[-1][1], end)
        else:
            segments.append((physical_path, start, end))
    return {
        "fixture_endpoints": (mapped_start, mapped_end),
        "nodes": nodes,
        "edge_ids": edge_ids,
        "length": len(edge_ids),
        "segments": tuple(segments),
    }


def assignment_key(chain):
    return tuple(label_key(label) for label in chain["nodes"])


def assign_parallel_chains(chains, base_lengths):
    require(len(chains) == len(base_lengths), "parallel-chain width changed")
    candidates = []

    def visit(slot, remaining, chosen):
        if slot == len(base_lengths):
            candidates.append(tuple(chosen))
            return
        base = base_lengths[slot]
        for position, chain in enumerate(remaining):
            length = chain["length"]
            if length < base or (length - base) % 2:
                continue
            visit(slot + 1, remaining[:position] + remaining[position + 1:],
                  chosen + [chain])

    visit(0, tuple(sorted(chains, key=assignment_key)), [])
    require(candidates, "no parity-preserving physical-chain assignment exists")
    selected = min(candidates, key=lambda rows: tuple(assignment_key(row) for row in rows))
    require(sum(tuple(assignment_key(row) for row in candidate) ==
                tuple(assignment_key(row) for row in selected)
                for candidate in candidates) == 1,
            "canonical parallel-chain assignment is nonunique")
    return selected, len(candidates)


def owner_paths(identification, chains, edges, path_data):
    record = identification["record"]
    mapping = identification["mapping"]
    pairs, indices = pair_index(record["n"])
    groups = defaultdict(list)
    for chain in chains:
        oriented = oriented_chain(chain, mapping, edges, path_data)
        groups[indices[oriented["fixture_endpoints"]]].append(oriented)

    output = []
    assignment_count = 1
    owner_index = 0
    for support, (pair, multiplicity, odd_total) in enumerate(
            zip(pairs, record["code"], identification["parity"], strict=True)):
        if multiplicity == 0:
            require(not groups.get(support), "chain mapped to an absent fixture support")
            continue
        base_lengths = (([1] + [3] * (odd_total - 1)) if odd_total else [])
        base_lengths += [2] * (multiplicity - odd_total)
        assigned, count = assign_parallel_chains(groups[support], base_lengths)
        assignment_count *= count
        for occurrence, (chain, base_length) in enumerate(
                zip(assigned, base_lengths, strict=True)):
            require(chain["fixture_endpoints"] == pair,
                    "oriented chain endpoints changed")
            output.append({
                "owner_path_index": owner_index,
                "fixture_support_index": support,
                "fixture_endpoints": list(pair),
                "fixture_occurrence": occurrence,
                "canonical_length": base_length,
                "actual_length": chain["length"],
                "physical_vertices": [json_label(label) for label in chain["nodes"]],
                "physical_segments": [list(segment) for segment in chain["segments"]],
                "_nodes": chain["nodes"],
            })
            owner_index += 1
    expected_path_count = identification["record"]["n"] + 5
    require(owner_index == expected_path_count and len(output) == expected_path_count,
            "rank-six owner path count changed")
    return output, assignment_count


def target_selection(paths, marked_locations):
    canonical = [row["canonical_length"] for row in paths]
    actual = [row["actual_length"] for row in paths]
    deltas = [length - base for length, base in zip(actual, canonical, strict=True)]
    require(all(delta >= 0 and delta % 2 == 0 for delta in deltas),
            "actual owner lengths do not dominate the canonical target")
    coordinate_candidates = [index + 1 for index, delta in enumerate(deltas) if delta >= 2]
    selected = coordinate_candidates[0] if coordinate_candidates else 0
    selected_lengths = list(canonical)
    if selected:
        selected_lengths[selected - 1] += 2
    extra_pairs = [
        (actual_length - selected_length) // 2
        for actual_length, selected_length in zip(actual, selected_lengths, strict=True)
    ]
    require(all(value >= 0 for value in extra_pairs),
            "selected finite target is not dominated by the actual target")

    # A descendant chain is obtained by expanding selected-target transformed
    # vertices into odd-size runs of identical vectors.  Choose those runs so
    # every marked actual coordinate maps to a distinct selected coordinate;
    # this is the explicit marked lift, rather than an unmarked monotonicity
    # invocation.  Among all valid run ledgers, select lexicographically.
    marks_by_path = defaultdict(list)
    for path_index, distance in marked_locations:
        marks_by_path[path_index].append(distance)
    lift = []
    for index, (selected_length, actual_length) in enumerate(
            zip(selected_lengths, actual, strict=True)):
        extra = actual_length - selected_length
        require(extra >= 0 and extra % 2 == 0, "bad descendant excess")
        candidates = []
        # run lengths are positive odd integers summing to actual_length+1.
        for weak in itertools.product(
                range(extra // 2 + 1), repeat=selected_length + 1):
            if sum(weak) != extra // 2:
                continue
            runs = tuple(1 + 2 * value for value in weak)
            index_map = tuple(
                target_index
                for target_index, run_length in enumerate(runs)
                for _ in range(run_length)
            )
            require(len(index_map) == actual_length + 1,
                    "descendant transformed-index map has wrong width")
            marked_images = [index_map[distance]
                             for distance in marks_by_path.get(index, ())]
            if len(marked_images) != len(set(marked_images)):
                continue
            candidates.append((runs, index_map))
        require(candidates,
                "no explicit zero-cost descendant lift separates marked coordinates")
        runs, index_map = min(candidates)
        lift.append({
            "owner_path_index": index,
            "selected_target_length": selected_length,
            "actual_length": actual_length,
            "selected_transformed_vertex_run_lengths": list(runs),
            "actual_to_selected_transformed_index": list(index_map),
            "inserted_zero_cost_step_pairs": extra // 2,
        })
    return {
        "canonical_length_vector": canonical,
        "actual_length_vector": actual,
        "eligible_finite_target_indices": [0, *coordinate_candidates],
        "selected_finite_target_index": selected,
        "selected_finite_target_length_vector": selected_lengths,
        "selection_rule": (
            "canonical if exact; otherwise the least one-based coordinate whose "
            "canonical length is exceeded by at least two"
        ),
        "descendant_lift": {
            "construction": (
                "replace each selected-target transformed vertex by the recorded "
                "odd run of identical copies; every added adjacent pair has dot "
                "product one and zero exact cost; marked actual coordinates are "
                "required to map to distinct selected coordinates"
            ),
            "paths": lift,
        },
    }


def locate_mark(mark, paths, mapping):
    if mark in mapping:
        return ("branch", mapping[mark])
    locations = []
    for row in paths:
        nodes = row["_nodes"]
        if mark in nodes:
            locations.append(("path", row["owner_path_index"], nodes.index(mark)))
    require(len(locations) == 1, "suppressed marked vertex provenance is nonunique")
    _, owner_index, distance = locations[0]
    require(0 < distance < paths[owner_index]["actual_length"],
            "nonbranch mark was not internal to its surviving chain")
    return locations[0]


def mark_provenance(mark, location, selection):
    if location[0] == "branch":
        fixture_vertex = location[1]
        return {
            "physical_vertex": json_label(mark),
            "provenance_tuple": ["branch", fixture_vertex],
            "kind": "surviving-branch",
            "fixture_vertex": fixture_vertex,
        }
    require(location[0] == "path" and len(location) == 3,
            "unknown marked location kind")
    owner_index, distance = location[1:]
    lift_row = selection["descendant_lift"]["paths"][owner_index]
    target_index = lift_row["actual_to_selected_transformed_index"][distance]
    return {
        "physical_vertex": json_label(mark),
        "provenance_tuple": ["path", owner_index, distance],
        "kind": "suppressed-internal",
        "owner_path_index": owner_index,
        "distance_from_oriented_start": distance,
        "selected_target_transformed_index": target_index,
    }


def block_json(block):
    return {
        "rank": block["rank"],
        "vertex_total": block["vertex_total"],
        "edge_total": block["edge_total"],
        "vertices": [json_label(label) for label in block["vertices"]],
    }


def map_case(case, kernels, fixtures):
    record = case["source_record"]
    source_index, global_kernel, local_kernel, row, orbit_size = record
    require(kernels[local_kernel][0] == global_kernel,
            "case global/local kernel mismatch")
    paths = kernels[local_kernel][1]
    # The miner's canonical path ordering is the authenticated physical ordering.
    miner_paths = case["miner"].canonical_paths(paths, row)
    target_lengths = case["target_length_vector"]
    deletion_index = case["deletion_path_index"]
    vertices, edges, adjacency, path_data = expand_after_deletion(
        miner_paths, target_lengths, deletion_index)
    components = connected_components(vertices, adjacency)
    rank = len(edges) - len(vertices) + len(components)
    require(rank == 6, "physical deletion did not leave rank six")
    blocks = biconnected_edge_components(vertices, edges, adjacency)
    require(sum(block["rank"] for block in blocks) == rank,
            "block ranks do not sum to the graph rank")
    positive = tuple(block for block in blocks if block["rank"] > 0)
    block_profile = [block["rank"] for block in positive]
    deleted = path_data[deletion_index]
    topology = {
        "connected": len(components) == 1,
        "rank": rank,
        "vertex_total": len(vertices),
        "edge_total": len(edges),
        "positive_block_rank_profile": block_profile,
        "blocks": [block_json(block) for block in blocks],
    }
    base_length = miner_paths[deletion_index][4]
    result = {
        "case_id": case["case_id"],
        "case_kind": case["case_kind"],
        "source_record": record,
        "source_index": source_index,
        "global_order9_kernel": global_kernel,
        "local_order9_kernel": local_kernel,
        "source_parity_row": row,
        "source_physical_orbit_size": orbit_size,
        "source_target": {
            "length_vector": list(target_lengths),
            "same_parity_increment_pairs": [
                (length - path[4]) // 2
                for length, path in zip(target_lengths, miner_paths, strict=True)
            ],
        },
        "deleted_physical_path": {
            "path_index": deletion_index,
            "physical_occurrence_key": [deleted["support"], deleted["occurrence"]],
            "stored_endpoints": [deleted["u"], deleted["v"]],
            "canonical_length": base_length,
            "actual_target_length": deleted["length"],
            "restoration_q_queries": {
                "canonical": base_length,
                "coordinate_frontier": base_length + 2,
                "actual_target": deleted["length"],
            },
        },
        "marked_physical_vertices_in_deleted_orientation": [
            json_label(("b", deleted["u"])), json_label(("b", deleted["v"]))
        ],
        "topology": topology,
        "owner_import": {
            "attempted": False,
            "reason": "topology/provenance stage only",
        },
    }

    single_rank_six = (
        len(components) == 1 and len(positive) == 1 and positive[0]["rank"] == 6 and
        set(positive[0]["vertices"]) == vertices and
        positive[0]["edge_total"] == len(edges)
    )
    if not single_rank_six:
        result["mapping_status"] = "multiblock-or-nonsingleblock-rank-six-topology"
        result["rank_six_fixture_mapping"] = None
        return result

    branch_vertices, kernel_adjacency, chains = trace_suppressed_chains(
        vertices, edges, adjacency)
    identification = fixtures.identify(branch_vertices, kernel_adjacency, chains)
    mapped_paths, assignment_count = owner_paths(
        identification, chains, edges, path_data)
    mark_a_label = ("b", deleted["u"])
    mark_b_label = ("b", deleted["v"])
    location_a = locate_mark(mark_a_label, mapped_paths, identification["mapping"])
    location_b = locate_mark(mark_b_label, mapped_paths, identification["mapping"])
    internal_locations = [location[1:] for location in (location_a, location_b)
                          if location[0] == "path"]
    selection = target_selection(mapped_paths, internal_locations)
    mark_a = mark_provenance(mark_a_label, location_a, selection)
    mark_b = mark_provenance(mark_b_label, location_b, selection)
    inverse = [None] * identification["record"]["n"]
    for physical, fixture_vertex in identification["mapping"].items():
        inverse[fixture_vertex] = json_label(physical)
    require(all(value is not None for value in inverse),
            "full fixture isomorphism is not onto")

    public_paths = []
    for row_data in mapped_paths:
        public_paths.append({key: value for key, value in row_data.items()
                             if not key.startswith("_")})
    result["mapping_status"] = "mapped-single-rank-six-kernel"
    result["rank_six_fixture_mapping"] = {
        "fixture_order": identification["record"]["n"],
        "fixture_kernel": identification["kernel"],
        "fixture_code": identification["record"]["code"],
        "dense_canonical_parity_row": list(identification["parity"]),
        "full_isomorphism": {
            "physical_to_fixture": [
                [json_label(vertex), identification["mapping"][vertex]]
                for vertex in branch_vertices
            ],
            "fixture_to_physical": inverse,
            "isomorphism_candidate_count": identification["isomorphism_count"],
            "canonical_parity_isomorphism_candidate_count":
                identification["canonical_parity_isomorphism_count"],
            "selection": (
                "minimum dense parity row, then lexicographically minimum fixture "
                "image vector on sorted surviving physical branch vertices; the "
                "selected concrete full map is unique under this total order even "
                "when the graph has automorphisms"
            ),
        },
        "parallel_chain_assignment_candidate_count": assignment_count,
        "parallel_chain_assignment_selection": (
            "lexicographically minimum oriented physical-vertex sequence among "
            "all parity-preserving assignments that dominate canonical lengths; "
            "the selected concrete occurrence bijection is unique under this total order"
        ),
        "oriented_surviving_chains": public_paths,
        "marked_provenance": [mark_a, mark_b],
        "both_marked_provenance_tuples": [
            mark_a["provenance_tuple"], mark_b["provenance_tuple"]
        ],
        "physical_correlation_recovery": (
            "for internal coordinates (path i,d) and (path j,e), use "
            "(-1)^(d+e) times the dot product of their lifted transformed vectors; "
            "a surviving branch uses its fixture branch vector"
        ),
        "target_selection": selection,
    }
    return result


def load_authenticated_frontier():
    miner = load_module()
    kernels = miner.load_kernels()
    rows, by_index = miner.load_source(kernels)
    excluded = miner.load_lane_indices(by_index)
    partition_cache = {
        local: miner.partition_data(edges)[0]
        for local, (_, edges) in kernels.items()
    }
    frontier = [record for record in rows
                if record[0] not in excluded and not partition_cache[record[2]]]
    require(len(frontier) == 1615 and sum(record[4] for record in frontier) == 1945,
            "authenticated 1,615-row frontier changed")
    require(len({record[2] for record in frontier}) == 115,
            "frontier represented-kernel count changed")
    return miner, kernels, frontier


def pilot_cases(miner, kernels, frontier):
    residual = strict_json(RESIDUAL, EXPECTED["residual"],
                           "favorable-cycle residual artifact")
    require(residual.get("residual_targets") == 80 and
            len(residual.get("failures", [])) == 80,
            "80-target residual scope changed")
    by_index = {record[0]: record for record in frontier}
    cases = []
    for failure in residual["failures"]:
        source = failure["source_record"]
        require(by_index.get(source[0]) == source,
                "residual failure is not an exact frontier source row")
        deletion = failure["frontier_path_index"]
        require(failure["physical_occurrence_key"] ==
                [failure["frontier_support"], failure["frontier_occurrence"]],
                "residual physical occurrence identity changed")
        cases.append({
            "case_id": f"residual-{source[0]}-delete-{deletion}",
            "case_kind": "finite-favorable-cycle-residual-coordinate-target",
            "source_record": source,
            "target_length_vector": failure["target_length_vector"],
            "deletion_path_index": deletion,
            "miner": miner,
        })

    hostile = by_index.get(HOSTILE_SOURCE_INDEX)
    require(hostile == [
        78714, 7662, 176, [1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1], 1
    ], "hostile source 78714 identity changed")
    paths = miner.canonical_paths(kernels[hostile[2]][1], hostile[3])
    lengths = [path[4] for path in paths]
    for path_index in HOSTILE_INCREMENT_PATHS:
        lengths[path_index] += 2
    require(lengths == [1, 3, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 3, 2],
            "hostile descendant length vector changed")
    for deletion in HOSTILE_INCREMENT_PATHS:
        cases.append({
            "case_id": f"hostile-78714-delete-{deletion}",
            "case_kind": "hostile-two-coordinate-descendant-deletion",
            "source_record": hostile,
            "target_length_vector": lengths,
            "deletion_path_index": deletion,
            "miner": miner,
        })
    require(len(cases) == 82 and len({case["case_id"] for case in cases}) == 82,
            "pilot case identity changed")
    return cases


def full_cases(miner, kernels, frontier):
    cases = []
    for source in frontier:
        paths = miner.canonical_paths(kernels[source[2]][1], source[3])
        canonical = [path[4] for path in paths]
        for deletion in range(PATH_COUNT9):
            lengths = list(canonical)
            lengths[deletion] += 2
            cases.append({
                "case_id": f"frontier-{source[0]}-delete-{deletion}",
                "case_kind": "full-frontier-coordinate-deletion",
                "source_record": source,
                "target_length_vector": lengths,
                "deletion_path_index": deletion,
                "miner": miner,
            })
    require(len(cases) == 1615 * PATH_COUNT9,
            "full deletion case count changed")
    return cases


def summarize(records):
    statuses = Counter(record["mapping_status"] for record in records)
    profiles = Counter(
        "+".join(map(str, record["topology"]["positive_block_rank_profile"]))
        for record in records
    )
    fixture_orders = Counter()
    fixture_kernels = Counter()
    mark_kinds = Counter()
    selected_targets = Counter()
    suppressed_mark_cases = 0
    for record in records:
        mapping = record["rank_six_fixture_mapping"]
        if mapping is None:
            continue
        fixture_orders[str(mapping["fixture_order"])] += 1
        fixture_kernels[str(mapping["fixture_kernel"])] += 1
        kinds = [mark["kind"] for mark in mapping["marked_provenance"]]
        mark_kinds.update(kinds)
        suppressed_mark_cases += any(kind == "suppressed-internal" for kind in kinds)
        target = mapping["target_selection"]["selected_finite_target_index"]
        selected_targets[str(target)] += 1
    return {
        "case_total": len(records),
        "mapping_status_counts": dict(sorted(statuses.items())),
        "positive_block_rank_profile_counts": dict(sorted(profiles.items())),
        "fixture_order_counts": dict(sorted(fixture_orders.items())),
        "fixture_kernel_counts": dict(sorted(fixture_kernels.items(),
                                                  key=lambda item: int(item[0]))),
        "marked_provenance_kind_counts": dict(sorted(mark_kinds.items())),
        "cases_with_at_least_one_suppressed_mark": suppressed_mark_cases,
        "selected_finite_target_index_counts": dict(sorted(
            selected_targets.items(), key=lambda item: int(item[0]))),
        "owner_import_attempted": False,
    }


def build(scope: str):
    require(scope in ("pilot", "full"), "unknown mapping scope")
    miner, kernels, frontier = load_authenticated_frontier()
    fixtures = RankSixFixtures.load()
    cases = (pilot_cases(miner, kernels, frontier) if scope == "pilot"
             else full_cases(miner, kernels, frontier))
    records = [map_case(case, kernels, fixtures) for case in cases]
    if scope == "pilot":
        require(all(record["mapping_status"] == "mapped-single-rank-six-kernel"
                    for record in records),
                "pilot contains a deletion without a unique single-block map")
    payload = {
        "schema": "rank-seven-order-nine-marked-deletion-map-v1",
        "scope": scope,
        "proof_semantics": (
            "exact finite topology, suppression, isomorphism, marked provenance, "
            "and descendant-index mapping only; no rank-six Gram owner was imported"
        ),
        "dependencies": {
            "frontier_miner_sha256": EXPECTED["miner"],
            "favorable_cycle_residual_sha256": EXPECTED["residual"],
            "rank_six_fixture_sha256": EXPECTED["rank6_fixture"],
        },
        "source_frontier": {
            "orbit_rows": 1615,
            "physical_rows": 1945,
            "represented_order9_kernels": 115,
            "physical_paths_per_row": PATH_COUNT9,
        },
        "case_convention": (
            "full scope lengthens the selected deletion occurrence by two before "
            "deleting it; each record also retains canonical and coordinate q queries"
        ),
        "summary": summarize(records),
        "records": records if scope == "pilot" else None,
        "full_scope_record_storage": (
            "summary-only deterministic replay; use --scope full --output PATH to "
            "regenerate the 24,225 transient records without committing 163 MB"
            if scope == "full" else "all pilot records embedded"
        ),
        "claim_boundary": [
            "no rank-six rational, coarse, symbolic, or structural owner import",
            "no E or marked correlation r was computed",
            "no E+f_q(r)<=6 decision",
            "no monotone or all-length spectral conclusion",
            "multiblock topology records are not single-block owner records",
        ],
    }
    return payload


def hostile_self_checks():
    checks = 0
    simple_paths = ((0, 0, 0, 1, 1),)
    try:
        validate_target(simple_paths, [2], 0)
    except RuntimeError:
        checks += 1
    else:
        raise RuntimeError("opposite-parity target mutation was accepted")

    fixture = RankSixFixtures.load()
    duplicate = [dict(row) for row in fixture.rows]
    duplicate.append(dict(duplicate[0]))
    try:
        RankSixFixtures(duplicate)
    except RuntimeError:
        checks += 1
    else:
        raise RuntimeError("duplicate fixture-width mutation was accepted")
    require(checks == 2, "hostile self-check count changed")
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", choices=("pilot", "full"), default="pilot")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()

    payload = build(args.scope)
    raw = canonical_bytes(payload)
    if args.audit:
        require(args.output.read_bytes() == raw,
                "committed marked-deletion map does not reproduce byte-for-byte")
    elif not args.emit:
        require(args.output.parent.is_dir(), "output parent does not exist")
        args.output.write_bytes(raw)
    if args.emit:
        print(raw.decode("ascii"), end="")
    digest = hashlib.sha256(raw).hexdigest()
    checks = hostile_self_checks()
    summary = payload["summary"]
    print(
        f"scope={args.scope} cases={summary['case_total']} "
        f"statuses={json.dumps(summary['mapping_status_counts'], sort_keys=True)}"
    )
    print(f"sha256={digest}")
    print(f"hostile_self_checks={checks}")
    print("rank-seven order-nine marked deletion mapper: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
