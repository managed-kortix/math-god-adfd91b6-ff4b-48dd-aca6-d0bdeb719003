#!/usr/bin/env python3
"""Exact census for the rank-seven/order-nine induced-partition transfer.

This verifier proves only finite combinatorial classification statements.  The
spectral implication is proved in the companion note from induced
superadditivity and the completed lower-rank theorems.  Its cubic-vertex
statistics are exploratory incidence data, not a deletion theorem owner.
"""

from __future__ import annotations

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
EXPECTED = {
    "fixture": "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5",
    "source_xz": "2a45b69d495e65c47d4b3c668572b0b7922e808c905c501c97e513df47d05089",
    "source_raw": "fb28f9f36cafad170995f7dff43fb0d8cd1effa08765dd283461fb011d4cba7b",
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
    return (json.dumps(value, separators=(",", ":"), allow_nan=False) + "\n").encode("ascii")


def load_kernels() -> dict[int, tuple[int, tuple[tuple[int, int, int], ...]]]:
    require(sha256(FIXTURE) == EXPECTED["fixture"], "kernel fixture changed")
    payload = json.loads(FIXTURE.read_bytes())
    kernels = {}
    local = 0
    for global_index, record in enumerate(payload["kernels"], 1):
        if record["n"] != 9:
            continue
        local += 1
        edges = tuple(
            (u, v, multiplicity)
            for (u, v), multiplicity in zip(
                itertools.combinations(range(9), 2), record["code"], strict=True
            )
            if multiplicity
        )
        kernels[local] = (global_index, edges)
    require(len(kernels) == 4495, "order-nine kernel count changed")
    return kernels


def connected_rank(edges: tuple[tuple[int, int, int], ...], mask: int) -> tuple[bool, int, int]:
    vertices = {v for v in range(9) if mask >> v & 1}
    require(bool(vertices), "empty induced territory")
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
    return seen == vertices, edge_total - len(vertices) + 1, len(vertices)


def classify_kernels(kernels):
    witnesses = {}
    deletion_vertices = {}
    type_counts = Counter()
    deletion_choice_counts = Counter()
    for local, (_, edges) in kernels.items():
        options = []
        # Exactly one of S and its complement contains vertex 8, so 1 <= S < 2^8
        # enumerates every unordered nontrivial bipartition exactly once.
        for mask in range(1, 1 << 8):
            left = connected_rank(edges, mask)
            right = connected_rank(edges, 511 ^ mask)
            if left[0] and right[0] and left[1] >= 2 and right[1] >= 2:
                crossing = sum(
                    multiplicity
                    for u, v, multiplicity in edges
                    if ((mask >> u) & 1) != ((mask >> v) & 1)
                )
                ranks = tuple(sorted((left[1], right[1]), reverse=True))
                score = (
                    min(ranks), sum(ranks), -crossing,
                    -abs(left[2] - right[2]), -mask,
                )
                options.append((score, mask, ranks, crossing))
        if options:
            witness = max(options)
            witnesses[local] = witness
            type_counts[(witness[2], witness[3])] += 1
            continue

        choices = []
        for vertex in range(9):
            complement = 511 ^ (1 << vertex)
            connected, rank, _ = connected_rank(edges, complement)
            degree = sum(
                multiplicity for u, v, multiplicity in edges
                if vertex in (u, v)
            )
            if connected and rank == 5 and degree == 3:
                incident_supports = tuple(
                    index for index, (u, v, _) in enumerate(edges)
                    if vertex in (u, v)
                )
                choices.append((vertex, incident_supports))
        require(bool(choices), f"kernel {local} has neither transfer nor deletion witness")
        deletion_vertices[local] = tuple(choices)
        deletion_choice_counts[len(choices)] += 1

    require(len(witnesses) == 4022, "partition-applicable kernel count changed")
    require(len(deletion_vertices) == 473, "partition-obstruction kernel count changed")
    require(type_counts == Counter({
        ((4, 2), 2): 811,
        ((3, 3), 2): 400,
        ((3, 2), 3): 1689,
        ((2, 2), 4): 1122,
    }), "canonical transfer-type kernel counts changed")
    require(deletion_choice_counts == Counter({6: 216, 7: 208, 8: 49}),
            "rank-five deletion-choice counts changed")
    return witnesses, deletion_vertices, type_counts, deletion_choice_counts


def load_lane_indices(source_rows: dict[int, list]) -> set[int]:
    indices = set()
    for position, path in enumerate(LANES):
        require(sha256(path) == EXPECTED["lanes_xz"][position],
                f"{path.name} compressed bytes changed")
        digest = hashlib.sha256()
        count = 0
        with lzma.open(path, "rb") as stream:
            for raw in stream:
                digest.update(raw)
                owner = json.loads(raw.decode("ascii"))
                require(raw == canonical_bytes(owner), f"noncanonical owner in {path.name}")
                require(isinstance(owner, list) and len(owner) == 4,
                        f"malformed owner in {path.name}")
                source_record = owner[0]
                require(isinstance(source_record, list) and len(source_record) == 5,
                        f"malformed source key in {path.name}")
                source_index = source_record[0]
                require(source_rows.get(source_index) == source_record,
                        f"{path.name} owner is not an exact source row")
                require(source_index not in indices, "persisted owner lanes overlap")
                indices.add(source_index)
                count += 1
        require(digest.hexdigest() == EXPECTED["lanes_raw"][position],
                f"{path.name} raw bytes changed")
        require(count == EXPECTED["lane_rows"][position],
                f"{path.name} row count changed")
    require(len(indices) == 2795, "persisted owner union count changed")
    return indices


def canonical_paths(edges, raw_row):
    paths = []
    require(len(edges) == len(raw_row), "row width changed")
    for support_index, ((_, _, multiplicity), odd_total) in enumerate(
            zip(edges, raw_row, strict=True)):
        require(type(odd_total) is int and 0 <= odd_total <= multiplicity,
                "invalid odd-count entry")
        if odd_total == 0:
            lengths = [2] * multiplicity
        else:
            lengths = [1] + [3] * (odd_total - 1) + [2] * (multiplicity - odd_total)
        paths.extend((support_index, length) for length in lengths)
    require(len(paths) == 15, "order-nine physical path count changed")
    return paths


def long_incident_cubic_vertex(paths, lengths, deletion_choices):
    for _, support_ids in deletion_choices:
        positions = [i for i, (support, _) in enumerate(paths) if support in support_ids]
        require(len(positions) == 3, "deletion vertex is not cubic in physical edges")
        if any(lengths[i] >= 3 for i in positions):
            return True
    return False


def scan_rows(kernels, witnesses, deletion_vertices):
    require(sha256(SOURCE) == EXPECTED["source_xz"], "source stream changed")
    source_digest = hashlib.sha256()
    rows = []
    source_rows = {}
    with lzma.open(SOURCE, "rb") as stream:
        for raw in stream:
            source_digest.update(raw)
            record = json.loads(raw.decode("ascii"))
            require(raw == canonical_bytes(record), "noncanonical source record")
            require(isinstance(record, list) and len(record) == 5, "malformed source record")
            source_index, global_kernel, local_kernel, raw_row, orbit_size = record
            require(type(source_index) is int and source_index not in source_rows,
                    "duplicate or noninteger source index")
            require(type(local_kernel) is int and local_kernel in kernels,
                    "invalid local kernel")
            require(kernels[local_kernel][0] == global_kernel, "global/local kernel mismatch")
            require(type(orbit_size) is int and orbit_size > 0, "invalid orbit size")
            canonical_paths(kernels[local_kernel][1], raw_row)
            source_rows[source_index] = record
            rows.append(record)
    require(source_digest.hexdigest() == EXPECTED["source_raw"], "source raw bytes changed")
    require(len(rows) == 272520, "source row total changed")

    excluded = load_lane_indices(source_rows)
    orbit_types = Counter()
    physical_types = Counter()
    obstruction_orbits = obstruction_physical = 0
    target_orbits = Counter()
    target_physical = Counter()
    short_per_row = Counter()
    represented_obstruction_kernels = set()

    for record in rows:
        source_index, _, local_kernel, raw_row, orbit_size = record
        if source_index in excluded:
            continue
        if local_kernel in witnesses:
            witness = witnesses[local_kernel]
            transfer_type = (witness[2], witness[3])
            orbit_types[transfer_type] += 1
            physical_types[transfer_type] += orbit_size
            target_orbits["partition"] += 16
            target_physical["partition"] += 16 * orbit_size
            continue

        represented_obstruction_kernels.add(local_kernel)
        obstruction_orbits += 1
        obstruction_physical += orbit_size
        edges = kernels[local_kernel][1]
        paths = canonical_paths(edges, raw_row)
        short_targets = 0
        for frontier in range(16):
            lengths = [length for _, length in paths]
            if frontier:
                lengths[frontier - 1] += 2
            # This is an incidence classification only.  Deleting the branch
            # vertex is not the proved marked physical-edge deletion, which
            # leaves rank six; no target in this branch is theorem-owned here.
            if long_incident_cubic_vertex(
                    paths, lengths, deletion_vertices[local_kernel]):
                target_orbits["cubic-vertex-long-incidence"] += 1
                target_physical["cubic-vertex-long-incidence"] += orbit_size
            else:
                short_targets += 1
                target_orbits["cubic-vertex-short-incidence"] += 1
                target_physical["cubic-vertex-short-incidence"] += orbit_size
        short_per_row[short_targets] += 1

    require(sum(orbit_types.values()) == 268110, "partition-owned orbit count changed")
    require(sum(physical_types.values()) == 302177, "partition-owned physical count changed")
    require(orbit_types == Counter({
        ((4, 2), 2): 88722,
        ((3, 3), 2): 51251,
        ((3, 2), 3): 104224,
        ((2, 2), 4): 23913,
    }), "canonical transfer-type orbit counts changed")
    require(physical_types == Counter({
        ((4, 2), 2): 101324,
        ((3, 3), 2): 57095,
        ((3, 2), 3): 115955,
        ((2, 2), 4): 27803,
    }), "canonical transfer-type physical counts changed")
    require((obstruction_orbits, obstruction_physical, len(represented_obstruction_kernels))
            == (1615, 1945, 115), "represented obstruction counts changed")
    require(target_orbits == Counter({
        "partition": 4289760,
        "cubic-vertex-long-incidence": 22742,
        "cubic-vertex-short-incidence": 3098,
    }), "target-orbit classification changed")
    require(target_physical == Counter({
        "partition": 4834832,
        "cubic-vertex-long-incidence": 27402,
        "cubic-vertex-short-incidence": 3718,
    }), "target-physical classification changed")
    require(short_per_row == Counter({1: 697, 2: 513, 3: 245, 4: 160}),
            "short-target-per-row distribution changed")
    require(sum(target_orbits.values()) == 269725 * 16,
            "target-orbit partition is not exhaustive")
    require(sum(target_physical.values()) == 304122 * 16,
            "target-physical partition is not exhaustive")

    return {
        "kernel_transfer_types": dict(sorted(type_counts_display(orbit_types).items())),
        "partition_owned_orbits": sum(orbit_types.values()),
        "partition_owned_physical": sum(physical_types.values()),
        "obstruction_orbits": obstruction_orbits,
        "obstruction_physical": obstruction_physical,
        "represented_obstruction_kernels": len(represented_obstruction_kernels),
        "target_orbits": dict(sorted(target_orbits.items())),
        "target_physical": dict(sorted(target_physical.items())),
        "short_targets_per_row": dict(sorted(short_per_row.items())),
    }


def type_counts_display(counter):
    return {f"{ranks[0]}-cross-{cross}": count for (ranks, cross), count in counter.items()}


def main() -> None:
    kernels = load_kernels()
    witnesses, deletion_vertices, kernel_types, deletion_counts = classify_kernels(kernels)
    result = scan_rows(kernels, witnesses, deletion_vertices)
    result.update({
        "applicable_kernels": len(witnesses),
        "obstruction_kernels": len(deletion_vertices),
        "canonical_kernel_types": dict(sorted(type_counts_display(kernel_types).items())),
        "deletion_choice_counts": dict(sorted(deletion_counts.items())),
        "post_lane_orbits": 269725,
        "post_lane_physical": 304122,
    })
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    print("rank-seven order-nine induced-partition transfer verifier: PASS")


if __name__ == "__main__":
    main()
