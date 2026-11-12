#!/usr/bin/env python3
"""Exact miner for the adaptive favorable-cycle partition residual.

This is a finite-combinatorial classifier only.  It reconstructs the exact
post-three-persisted-Gram-lane, post-rank>=2/rank>=2-partition frontier and
classifies its canonical plus fifteen coordinate targets by whether some
connected branch-vertex bipartition has one side of rank one whose unique
cycle has favorable length (even, or congruent to 3 modulo 4) and the other
side has rank at least two.

The script does not prove the analytic transfer theorem associated with that
criterion and does not claim the residual targets are counterexamples.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import lzma
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIXTURE = HERE / "fixtures/rank-seven-kernel-frontier-census.json"
EXPERIMENTS = ROOT / "positive-square-energy" / "experiments"
SOURCE = EXPERIMENTS / "rank7_order9_after_sos_remainder.jsonl.xz"
LANES = (
    EXPERIMENTS / "rank7_order9_dominant_family_gram_owners.jsonl.xz",
    EXPERIMENTS / "rank7_order9_third_family_cycle_gram_owners.jsonl.xz",
    EXPERIMENTS / "rank7_order9_fourth_family_cycle_gram_owners.jsonl.xz",
)
DEFAULT_OUTPUT = HERE / "rank-seven-order-nine-favorable-cycle-residual.json"

ORDER = 9
FULL_MASK = (1 << ORDER) - 1
PATH_COUNT = 15
EXPECTED = {
    "fixture": "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5",
    "source_xz": "2a45b69d495e65c47d4b3c668572b0b7922e808c905c501c97e513df47d05089",
    "source_raw": "fb28f9f36cafad170995f7dff43fb0d8cd1effa08765dd283461fb011d4cba7b",
    "source_rows": 272520,
    "lanes_xz": (
        "5d41ae256f123a6fa6a31bed226b069ea070e52aaf50199c06d0dbfd0b914de9",
        "9955f46b32f0b714f6c3b6b19778cd93f72bdb05ccd3c6e881a79bab288a77bf",
        "6423fd051a754ba0c810f79a51e83391926c2049ccf20c8cef0ad4c2a4e3867d",
    ),
    "lanes_raw": (
        "f2748ded8f67638f6b44dc5dbdb111edddbbead4fe1be7b47f97edcf1cb744ba",
        "2f35c2a76ce054be0d5b2ed18c0bfd77f163c1429af35ca48b91313ba77d0154",
        "a347d2d7891609156692d0bf0614783d79a9b84c6f4e0902ef6672f1cb4c96f5",
    ),
    "lane_rows": (1128, 631, 1036),
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


def strict_json(raw: bytes, label: str):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    try:
        return json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs,
            parse_constant=lambda value: (_ for _ in ()).throw(
                RuntimeError(f"nonstandard JSON constant in {label}: {value}")),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot parse {label}") from error


def load_kernels():
    require(sha256(FIXTURE) == EXPECTED["fixture"], "kernel fixture changed")
    fixture = strict_json(FIXTURE.read_bytes(), FIXTURE.name)
    kernels = {}
    local = 0
    for global_index, record in enumerate(fixture["kernels"], 1):
        if record["n"] != ORDER:
            continue
        local += 1
        edges = tuple(
            (u, v, multiplicity)
            for (u, v), multiplicity in zip(
                itertools.combinations(range(ORDER), 2), record["code"], strict=True
            )
            if multiplicity
        )
        kernels[local] = (global_index, edges)
    require(len(kernels) == 4495, "order-nine kernel count changed")
    return kernels


def connected_rank(edges, mask: int):
    vertices = {v for v in range(ORDER) if mask >> v & 1}
    require(vertices, "empty induced territory")
    adjacency = {v: set() for v in vertices}
    edge_total = 0
    for u, v, multiplicity in edges:
        if u in vertices and v in vertices:
            adjacency[u].add(v)
            adjacency[v].add(u)
            edge_total += multiplicity
    seen = {min(vertices)}
    pending = list(seen)
    while pending:
        u = pending.pop()
        for v in adjacency[u] - seen:
            seen.add(v)
            pending.append(v)
    return len(seen) == len(vertices), edge_total - len(vertices) + 1


def partition_data(edges):
    partitions = []
    has_rank_two_pair = False
    for mask in range(1, 1 << (ORDER - 1)):
        left_connected, left_rank = connected_rank(edges, mask)
        right_connected, right_rank = connected_rank(edges, FULL_MASK ^ mask)
        if not (left_connected and right_connected):
            continue
        partitions.append((mask, left_rank, right_rank))
        if left_rank >= 2 and right_rank >= 2:
            has_rank_two_pair = True
    return has_rank_two_pair, tuple(partitions)


def load_source(kernels):
    require(sha256(SOURCE) == EXPECTED["source_xz"], "source artifact changed")
    digest = hashlib.sha256()
    rows = []
    by_index = {}
    with lzma.open(SOURCE, "rb") as stream:
        for raw in stream:
            digest.update(raw)
            record = strict_json(raw, SOURCE.name)
            require(raw == canonical_bytes(record), "noncanonical source record")
            require(isinstance(record, list) and len(record) == 5,
                    "malformed source record")
            source_index, global_kernel, local_kernel, row, orbit_size = record
            require(type(source_index) is int and source_index not in by_index,
                    "duplicate or invalid source index")
            require(type(local_kernel) is int and local_kernel in kernels,
                    "invalid local kernel")
            expected_global, edges = kernels[local_kernel]
            require(global_kernel == expected_global, "global/local kernel mismatch")
            require(isinstance(row, list) and len(row) == len(edges) and
                    all(type(value) is int and 0 <= value <= edge[2]
                        for value, edge in zip(row, edges, strict=True)),
                    "invalid source parity row")
            require(type(orbit_size) is int and orbit_size > 0,
                    "invalid physical orbit size")
            require(sum(edge[2] for edge in edges) == PATH_COUNT,
                    "physical path count changed")
            rows.append(record)
            by_index[source_index] = record
    require(len(rows) == EXPECTED["source_rows"], "source row total changed")
    require(digest.hexdigest() == EXPECTED["source_raw"], "source raw bytes changed")
    return rows, by_index


def load_lane_indices(source_by_index):
    excluded = set()
    for position, path in enumerate(LANES):
        require(sha256(path) == EXPECTED["lanes_xz"][position],
                f"{path.name} compressed bytes changed")
        digest = hashlib.sha256()
        count = 0
        with lzma.open(path, "rb") as stream:
            for raw in stream:
                digest.update(raw)
                owner = strict_json(raw, path.name)
                require(raw == canonical_bytes(owner),
                        f"noncanonical owner in {path.name}")
                require(isinstance(owner, list) and len(owner) == 4 and
                        isinstance(owner[0], list) and len(owner[0]) == 5,
                        f"malformed owner in {path.name}")
                source_index = owner[0][0]
                require(source_by_index.get(source_index) == owner[0],
                        f"{path.name} owner is not an exact source row")
                require(source_index not in excluded, "persisted owner lanes overlap")
                excluded.add(source_index)
                count += 1
        require(digest.hexdigest() == EXPECTED["lanes_raw"][position],
                f"{path.name} raw bytes changed")
        require(count == EXPECTED["lane_rows"][position],
                f"{path.name} row count changed")
    require(len(excluded) == 2795, "persisted owner union count changed")
    return excluded


def canonical_paths(edges, row):
    paths = []
    for support, ((u, v, multiplicity), odd_total) in enumerate(
            zip(edges, row, strict=True)):
        lengths = (([1] + [3] * (odd_total - 1)) if odd_total else [])
        lengths += [2] * (multiplicity - odd_total)
        paths.extend((support, occurrence, u, v, length)
                     for occurrence, length in enumerate(lengths))
    require(len(paths) == PATH_COUNT, "path count changed")
    return tuple(paths)


def cycle_length(edges, paths, low_mask: int, frontier: int) -> int:
    """Return the exact unique-cycle length in a connected rank-one side."""
    low_vertices = {v for v in range(ORDER) if low_mask >> v & 1}
    adjacency = {v: set() for v in low_vertices}
    next_vertex = ORDER
    for path_index, (_, _, u, v, base_length) in enumerate(paths):
        if u not in low_vertices or v not in low_vertices:
            continue
        length = base_length + 2 * (path_index == frontier)
        internal = list(range(next_vertex, next_vertex + length - 1))
        next_vertex += length - 1
        sequence = [u, *internal, v]
        for vertex in internal:
            adjacency[vertex] = set()
        for left, right in zip(sequence, sequence[1:]):
            adjacency[left].add(right)
            adjacency[right].add(left)

    alive = set(adjacency)
    leaves = [vertex for vertex in alive if len(adjacency[vertex]) <= 1]
    while leaves:
        vertex = leaves.pop()
        if vertex not in alive:
            continue
        alive.remove(vertex)
        for neighbor in tuple(adjacency[vertex]):
            adjacency[neighbor].discard(vertex)
            if neighbor in alive and len(adjacency[neighbor]) <= 1:
                leaves.append(neighbor)
    require(bool(alive) and all(len(adjacency[v] & alive) == 2 for v in alive),
            "rank-one territory did not reduce to one cycle")
    return len(alive)


def favorable(length: int) -> bool:
    return length % 2 == 0 or length % 4 == 3


def rank_one_options(partitions):
    options = []
    for mask, left_rank, right_rank in partitions:
        if left_rank == 1 and right_rank >= 2:
            options.append((right_rank, mask))
        if right_rank == 1 and left_rank >= 2:
            options.append((left_rank, FULL_MASK ^ mask))
    return tuple(sorted(set(options)))


def analyze(rows, kernels, excluded):
    kernel_partitions = {
        local: partition_data(edges)
        for local, (_, edges) in kernels.items()
    }
    frontier_rows = []
    for record in rows:
        if record[0] in excluded:
            continue
        if not kernel_partitions[record[2]][0]:
            frontier_rows.append(record)
    require(len(frontier_rows) == 1615, "obstruction orbit-row total changed")
    require(sum(record[4] for record in frontier_rows) == 1945,
            "obstruction physical-row total changed")
    require(len({record[2] for record in frontier_rows}) == 115,
            "represented obstruction kernel count changed")

    failures = []
    failed_rows = Counter()
    owned_targets = 0
    canonical_failures = 0
    for record in frontier_rows:
        source_index, global_kernel, local_kernel, row, orbit_size = record
        edges = kernels[local_kernel][1]
        paths = canonical_paths(edges, row)
        require(all(length <= 2 for *_, length in paths),
                "frontier canonical row has a long path")
        options = rank_one_options(kernel_partitions[local_kernel][1])
        require(options, "frontier kernel has no rank-one/rank>=2 partition")
        for target in range(PATH_COUNT + 1):
            frontier = target - 1
            witnesses = []
            observed = []
            for high_rank, low_mask in options:
                length = cycle_length(edges, paths, low_mask, frontier)
                observed.append((high_rank, low_mask, length))
                if favorable(length):
                    witnesses.append((high_rank, low_mask, length))
            if witnesses:
                owned_targets += 1
                continue
            if target == 0:
                canonical_failures += 1
            failed_rows[source_index] += 1
            target_lengths = [length for *_, length in paths]
            support = None
            occurrence = None
            endpoints = None
            multiplicity = None
            odd_total = None
            base_length = None
            if target:
                support, occurrence, u, v, base_length = paths[frontier]
                target_lengths[frontier] += 2
                endpoints = [u, v]
                multiplicity = edges[support][2]
                odd_total = row[support]
            failures.append({
                "key": [source_index, global_kernel, local_kernel, row,
                        orbit_size, frontier],
                "source_record": record,
                "source_index": source_index,
                "global_kernel": global_kernel,
                "order9_kernel": local_kernel,
                "row": row,
                "physical_orbit": orbit_size,
                "canonical_plus_coordinate_target_index": target,
                "frontier_path_index": frontier,
                "frontier_support": support,
                "frontier_occurrence": occurrence,
                "frontier_endpoints": endpoints,
                "frontier_base_length": base_length,
                "frontier_bundle_multiplicity": multiplicity,
                "frontier_bundle_odd_total": odd_total,
                "target_length_vector": target_lengths,
                "physical_occurrence_key": None if target == 0 else [support, occurrence],
                "rank_one_options": [
                    {"high_rank": high_rank, "low_mask": low_mask,
                     "cycle_length": length, "cycle_mod4": length % 4}
                    for high_rank, low_mask, length in observed
                ],
            })

    return {
        "schema": "rank-seven-order-nine-favorable-cycle-residual-v1",
        "full_theorem": False,
        "scope": (
            "finite exact classification of the 1,615-row post-three-stream "
            "induced-rank>=2/rank>=2-partition obstruction frontier"
        ),
        "source": {
            "path": str(SOURCE.relative_to(ROOT)),
            "artifact_sha256": EXPECTED["source_xz"],
            "raw_sha256": EXPECTED["source_raw"],
            "record_total": EXPECTED["source_rows"],
        },
        "excluded_lanes": [
            {"path": str(path.relative_to(ROOT)),
             "artifact_sha256": EXPECTED["lanes_xz"][position],
             "raw_sha256": EXPECTED["lanes_raw"][position],
             "record_total": EXPECTED["lane_rows"][position]}
            for position, path in enumerate(LANES)
        ],
        "frontier": {
            "orbit_rows": len(frontier_rows),
            "physical_rows": sum(record[4] for record in frontier_rows),
            "represented_kernels": len({record[2] for record in frontier_rows}),
            "targets": len(frontier_rows) * (PATH_COUNT + 1),
        },
        "criterion": {
            "partition": (
                "both induced branch-vertex territories connected; one has "
                "rank 1 and the other rank at least 2"
            ),
            "favorable_unique_cycle": "length is even or congruent to 3 modulo 4",
            "target_convention": (
                "canonical_plus_coordinate_target_index 0 is canonical; indices "
                "1..15 increase zero-based frontier_path_index target-1 by two; "
                "the final key field is the zero-based frontier_path_index"
            ),
            "selection": "adaptive existential partition independently per target",
        },
        "owned_targets": owned_targets,
        "residual_targets": len(failures),
        "residual_rows": len(failed_rows),
        "canonical_residual_targets": canonical_failures,
        "residual_targets_per_row_histogram": {
            str(count): multiplicity
            for count, multiplicity in sorted(Counter(failed_rows.values()).items())
        },
        "failures": failures,
        "claim_boundary": (
            "classification only: the script neither authenticates the analytic "
            "partition transfer nor asserts anything about the 80 residual targets"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()

    kernels = load_kernels()
    rows, by_index = load_source(kernels)
    excluded = load_lane_indices(by_index)
    report = analyze(rows, kernels, excluded)
    require(report["owned_targets"] == 25760, "owned target total changed")
    require(report["residual_targets"] == 80, "residual target total changed")
    require(report["residual_rows"] == 39, "residual row total changed")
    require(report["canonical_residual_targets"] == 0,
            "canonical target unexpectedly failed")
    raw = canonical_bytes(report)
    if args.audit:
        require(args.output.read_bytes() == raw, "report does not reproduce byte-for-byte")
    else:
        require(args.output.parent.is_dir(), "output parent does not exist")
        args.output.write_bytes(raw)
    print(
        f"frontier={report['frontier']['orbit_rows']} "
        f"owned={report['owned_targets']} residual={report['residual_targets']} "
        f"rows={report['residual_rows']} canonical_residual="
        f"{report['canonical_residual_targets']}"
    )
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
