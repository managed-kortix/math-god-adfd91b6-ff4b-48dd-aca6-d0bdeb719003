#!/usr/bin/env python3
"""Pure exact verifier for the rank-seven/order-eight packet chain IV--XII.

The verifier is deliberately independent of NumPy, SciPy, numerical search,
and the producer modules.  It authenticates the census chunks and selected
residual indices, reconstructs the 492,812-row rational-search stream, forms
the *virtual* lane-IV complement inside the lane-III source, and then verifies
lanes V--XII.  Every persisted packet is decoded as ``Fraction`` data and
replayed exactly.  Every materialized remainder is required to be the ordered,
byte-for-byte complement of its source.

This module contains no file-writing operation.  Its public functions accept a
root directory so hostile tests can audit mutated private copies.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import math
import sys
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping, NoReturn, Sequence, TypeGuard

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ORDER = 8
PATH_COUNT = 14
TARGETS_PER_ROW = 15
BUDGET = Fraction(6)
DENOMINATORS = (256, 1024, 4096, 16384, 65536)
MANIFEST_NAME = "rank7_order8_exact_residual_census_manifest.json"
INDICES_NAME = "rank7_order8_rational_search_indices.json"
EXPECTED_MANIFEST_SHA256 = "5d41e78a2f688f4c3064cb88f1d6d475008d36c84f892edc4cba28ade424fe98"
EXPECTED_INDICES_SHA256 = "245cceaab164ba9c2a604d0db8b09a65598fd52084b1df2363911c6d1d4d3a59"
EXPECTED_SELECTED_TOTAL = 492812

Json = Any
Family = tuple[tuple[int, ...], tuple[int, int, int], int, int]
Residual = tuple[int, int, tuple[int, ...], tuple[int, ...], tuple[int, ...], int]
Record = list[Json]
Witness = tuple[
    int,
    tuple[tuple[Fraction, ...], ...],
    tuple[tuple[tuple[Fraction, ...], ...], ...],
    tuple[tuple[tuple[Fraction, ...], ...], ...],
]

OWNER_FIELDS = frozenset({
    "global_kernel", "numerical_canonical_cost", "orbit_size", "source_index",
    "stream_index", "witness",
})
WITNESS_FIELDS = frozenset({"denominator", "branches", "canonical", "extended"})
STREAM_FIELDS = frozenset({"path", "record_total", "raw_sha256", "artifact_sha256"})


@dataclass(frozen=True)
class LaneSpec:
    ordinal: str
    report_name: str
    report_sha256: str
    schema: str
    source_report_name: str
    source_stream_name: str
    owner_stream_name: str
    remainder_stream_name: str | None
    source_total: int
    owner_total: int
    remainder_total: int
    target: Family
    target_physical: int
    dominance_rank: int
    virtual_closed_total: int = 0
    virtual_closed_target: Family | None = None


LANES = (
    LaneSpec(
        "IV", "rank7_order8_induced_packet_gram_family.json",
        "e71c8fa8e315ff5015de8f821612814eb36fce8f8d37579b54a34359928ad099",
        "rank-seven-order-eight-induced-packet-gram-family-v1",
        "rank7_order8_third_structural_cycle_gram_lane.json",
        "rank7_order8_after_third_structural_cycle_gram_remainder.jsonl.xz",
        "rank7_order8_induced_packet_gram_family_owners.jsonl.xz", None,
        83611, 2928, 80683,
        ((2, 2, 2, 2, 1, 1, 1, 1, 1, 1), (2, 4, 4), 3, 1), 3060, 4,
    ),
    LaneSpec(
        "V", "rank7_order8_fifth_induced_packet_gram_family.json",
        "800901fe6d227f0304c651f898b33f84698c21e868275b935593120b114c44c5",
        "rank-seven-order-eight-fifth-induced-packet-gram-family-v1",
        "rank7_order8_induced_packet_gram_family.json",
        "rank7_order8_after_third_structural_cycle_gram_remainder.jsonl.xz",
        "rank7_order8_fifth_induced_packet_gram_family_owners.jsonl.xz",
        "rank7_order8_after_fifth_induced_packet_gram_family_remainder.jsonl.xz",
        80683, 2571, 78112,
        ((2, 2, 2, 2, 1, 1, 1, 1, 1, 1), (1, 3, 6), 3, 1), 2694, 5,
        2928, ((2, 2, 2, 2, 1, 1, 1, 1, 1, 1), (2, 4, 4), 3, 1),
    ),
    LaneSpec(
        "VI", "rank7_order8_sixth_induced_packet_gram_family.json",
        "d396cc1070fde5422a5a07640314c4fcbe3ee970ade479d5c2bec781ba51f0e6",
        "rank-seven-order-eight-sixth-induced-packet-gram-family-v1",
        "rank7_order8_fifth_induced_packet_gram_family.json",
        "rank7_order8_after_fifth_induced_packet_gram_family_remainder.jsonl.xz",
        "rank7_order8_sixth_induced_packet_gram_family_owners.jsonl.xz",
        "rank7_order8_after_sixth_induced_packet_gram_family_remainder.jsonl.xz",
        78112, 2027, 76085,
        ((2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), (3, 2, 7), 5, 3), 2192, 6,
    ),
    LaneSpec(
        "VII", "rank7_order8_seventh_induced_packet_gram_family.json",
        "d29bd297b7e9945ef59a578bf66445375695af4a26188f8524287c082c6cf1fe",
        "rank-seven-order-eight-seventh-induced-packet-gram-family-v1",
        "rank7_order8_sixth_induced_packet_gram_family.json",
        "rank7_order8_after_sixth_induced_packet_gram_family_remainder.jsonl.xz",
        "rank7_order8_seventh_induced_packet_gram_family_owners.jsonl.xz",
        "rank7_order8_after_seventh_induced_packet_gram_family_remainder.jsonl.xz",
        76085, 6817, 69268,
        ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1), (2, 3, 6), 4, 2), 7492, 1,
    ),
    LaneSpec(
        "VIII", "rank7_order8_eighth_induced_packet_gram_family.json",
        "318c607aa4114c049c7689ea00c9e635def0ef31933053411dae81d012111b05",
        "rank-seven-order-eight-eighth-induced-packet-gram-family-v1",
        "rank7_order8_seventh_induced_packet_gram_family.json",
        "rank7_order8_after_seventh_induced_packet_gram_family_remainder.jsonl.xz",
        "rank7_order8_eighth_induced_packet_gram_family_owners.jsonl.xz",
        "rank7_order8_after_eighth_induced_packet_gram_family_remainder.jsonl.xz",
        69268, 4219, 65049,
        ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1), (3, 3, 5), 4, 2), 4656, 1,
    ),
    LaneSpec(
        "IX", "rank7_order8_ninth_induced_packet_gram_family.json",
        "38f87fbe6a76c6ea59945e7befda3c04b6d6ffdfaaac123e144f93ffe26c9f38",
        "rank-seven-order-eight-ninth-induced-packet-gram-family-v1",
        "rank7_order8_eighth_induced_packet_gram_family.json",
        "rank7_order8_after_eighth_induced_packet_gram_family_remainder.jsonl.xz",
        "rank7_order8_ninth_induced_packet_gram_family_owners.jsonl.xz",
        "rank7_order8_after_ninth_induced_packet_gram_family_remainder.jsonl.xz",
        65049, 3765, 61284,
        ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1), (2, 3, 6), 4, 1), 3916, 1,
    ),
    LaneSpec(
        "X", "rank7_order8_tenth_induced_packet_gram_family.json",
        "7f758edbd9f4a24d342f9e2dc87068e01f6ea6ee608a1dc086b02dd1415ea33b",
        "rank-seven-order-eight-tenth-induced-packet-gram-family-v1",
        "rank7_order8_ninth_induced_packet_gram_family.json",
        "rank7_order8_after_ninth_induced_packet_gram_family_remainder.jsonl.xz",
        "rank7_order8_tenth_induced_packet_gram_family_owners.jsonl.xz",
        "rank7_order8_after_tenth_induced_packet_gram_family_remainder.jsonl.xz",
        61284, 2731, 58553,
        ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1), (1, 3, 7), 4, 2), 2968, 1,
    ),
    LaneSpec(
        "XI", "rank7_order8_eleventh_induced_packet_gram_family.json",
        "7fa3e0fd480e23a8140f628124e39db3a19f56406281d9549d37118c8f55282b",
        "rank-seven-order-eight-eleventh-induced-packet-gram-family-v1",
        "rank7_order8_tenth_induced_packet_gram_family.json",
        "rank7_order8_after_tenth_induced_packet_gram_family_remainder.jsonl.xz",
        "rank7_order8_eleventh_induced_packet_gram_family_owners.jsonl.xz",
        "rank7_order8_after_eleventh_induced_packet_gram_family_remainder.jsonl.xz",
        58553, 2167, 56386,
        ((2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), (2, 2, 8), 5, 3), 2275, 1,
    ),
    LaneSpec(
        "XII", "rank7_order8_twelfth_induced_packet_gram_family.json",
        "dc4e868dae60db6b9504b2288f983ef1d98cbfa36245178e95f778fa277293c5",
        "rank-seven-order-eight-twelfth-induced-packet-gram-family-v1",
        "rank7_order8_eleventh_induced_packet_gram_family.json",
        "rank7_order8_after_eleventh_induced_packet_gram_family_remainder.jsonl.xz",
        "rank7_order8_twelfth_induced_packet_gram_family_owners.jsonl.xz",
        "rank7_order8_after_twelfth_induced_packet_gram_family_remainder.jsonl.xz",
        56386, 1788, 54598,
        ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1), (2, 3, 6), 4, 3), 1958, 1,
    ),
)


@dataclass(frozen=True)
class StreamEntry:
    record: Record
    raw: bytes
    residual: Residual


@dataclass(frozen=True)
class LaneReceipt:
    ordinal: str
    source_total: int
    owner_total: int
    remainder_total: int
    physical_total: int
    frontier_total: int


@dataclass(frozen=True)
class ChainReceipt:
    selected_residual_total: int
    lanes: tuple[LaneReceipt, ...]


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def is_exact_int(value: object) -> TypeGuard[int]:
    return type(value) is int


def exact_int(value: object, label: str, *, minimum: int | None = None) -> int:
    if not is_exact_int(value):
        fail(f"{label}: expected exact integer")
    if minimum is not None and value < minimum:
        fail(f"{label}: expected integer at least {minimum}")
    return value


def exact_string(value: object, label: str) -> str:
    if type(value) is not str or not value:
        fail(f"{label}: expected nonempty string")
    return value


def exact_list(value: object, label: str) -> list[Json]:
    if type(value) is not list:
        fail(f"{label}: expected array")
    return value


def exact_mapping(value: object, label: str) -> dict[str, Json]:
    if type(value) is not dict or not all(type(key) is str for key in value):
        fail(f"{label}: expected object with string keys")
    return value


def exact_float(value: object, label: str) -> float:
    if type(value) is not float or not math.isfinite(value):
        fail(f"{label}: expected finite JSON float")
    return value


def hex_digest(value: object, label: str) -> str:
    text = exact_string(value, label)
    require(len(text) == 64 and all(character in "0123456789abcdef" for character in text),
            f"{label}: expected lowercase SHA-256")
    return text


def strict_json(raw: bytes, label: str) -> Json:
    def pairs(items: list[tuple[str, Json]]) -> dict[str, Json]:
        result: dict[str, Json] = {}
        for key, value in items:
            require(key not in result, f"{label}: duplicate key {key}")
            result[key] = value
        return result

    def reject_constant(value: str) -> NoReturn:
        fail(f"{label}: nonstandard JSON constant {value}")

    try:
        return json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                          parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{label}: invalid strict ASCII JSON") from error


def canonical_bytes(value: Json) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def safe_path(root: Path, name: object, expected: str, label: str) -> Path:
    text = exact_string(name, f"{label}.path")
    require(Path(text).name == text and text == expected, f"{label}: unsafe or wrong path")
    root_resolved = root.resolve()
    path = (root / text).resolve()
    require(path.parent == root_resolved and path.is_file(), f"{label}: artifact missing")
    return path


def parse_report(root: Path, spec: LaneSpec) -> tuple[bytes, dict[str, Json]]:
    path = safe_path(root, spec.report_name, spec.report_name, f"lane {spec.ordinal} report")
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == spec.report_sha256,
            f"lane {spec.ordinal}: pinned report digest changed")
    report = exact_mapping(strict_json(raw, spec.report_name), spec.report_name)
    require(raw == canonical_bytes(report), f"lane {spec.ordinal}: report is noncanonical")
    require(report.get("schema") == spec.schema and report.get("full_theorem") is True,
            f"lane {spec.ordinal}: theorem report identity changed")
    return raw, report


def validate_stream_info(info_value: object, expected_path: str, expected_total: int,
                         label: str) -> tuple[dict[str, Json], str, str]:
    info = exact_mapping(info_value, label)
    require(set(info) == STREAM_FIELDS, f"{label}: metadata fields changed")
    require(exact_string(info.get("path"), f"{label}.path") == expected_path,
            f"{label}: path changed")
    require(exact_int(info.get("record_total"), f"{label}.record_total", minimum=0) ==
            expected_total, f"{label}: record total changed")
    return (info, hex_digest(info.get("raw_sha256"), f"{label}.raw_sha256"),
            hex_digest(info.get("artifact_sha256"), f"{label}.artifact_sha256"))


def source_record(value: object, residuals: Sequence[Residual], label: str) -> tuple[Record, Residual]:
    record = exact_list(value, label)
    require(len(record) == 6, f"{label}: source row must have six fields")
    stream_index = exact_int(record[0], f"{label}.stream_index", minimum=0)
    require(stream_index < len(residuals), f"{label}: stream index out of range")
    source_index = exact_int(record[1], f"{label}.source_index", minimum=0)
    global_kernel = exact_int(record[2], f"{label}.global_kernel", minimum=0)
    edges_value = exact_list(record[3], f"{label}.edges")
    odds_value = exact_list(record[4], f"{label}.odd_counts")
    orbit_size = exact_int(record[5], f"{label}.orbit_size", minimum=1)
    require(len(edges_value) == len(odds_value), f"{label}: edge/parity widths differ")
    edges: list[tuple[int, int, int]] = []
    for index, edge_value in enumerate(edges_value):
        edge = exact_list(edge_value, f"{label}.edges[{index}]")
        require(len(edge) == 3, f"{label}.edges[{index}]: expected triple")
        u = exact_int(edge[0], f"{label}.edges[{index}][0]", minimum=0)
        v = exact_int(edge[1], f"{label}.edges[{index}][1]", minimum=0)
        multiplicity = exact_int(edge[2], f"{label}.edges[{index}][2]", minimum=1)
        require(u < v < ORDER, f"{label}.edges[{index}]: invalid endpoints")
        edges.append((u, v, multiplicity))
    require(all(left < right for left, right in zip(edges, edges[1:])),
            f"{label}: edges are not strictly ordered")
    odds = tuple(exact_int(value, f"{label}.odd_counts[{index}]", minimum=0)
                 for index, value in enumerate(odds_value))
    require(all(odd <= edge[2] for edge, odd in zip(edges, odds, strict=True)) and
            sum(edge[2] for edge in edges) == PATH_COUNT,
            f"{label}: nonphysical path multiplicities")
    support = tuple(u * (2 * ORDER - u - 1) // 2 + v - u - 1 for u, v, _ in edges)
    rebuilt: Residual = (global_kernel, source_index, support,
                         tuple(edge[2] for edge in edges), odds, orbit_size)
    residual = residuals[stream_index]
    require(rebuilt == residual, f"{label}: row differs from regenerated census residual")
    adjacency = [set() for _ in range(ORDER)]
    for u, v, _ in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    reached = {0}
    frontier = [0]
    for vertex in frontier:
        for neighbor in adjacency[vertex]:
            if neighbor not in reached:
                reached.add(neighbor)
                frontier.append(neighbor)
    require(len(reached) == ORDER, f"{label}: support is disconnected")
    return record, residual


def read_source_stream(root: Path, path_name: str, info_value: object, expected_total: int,
                       residuals: Sequence[Residual], label: str) -> tuple[StreamEntry, ...]:
    info, expected_raw, expected_artifact = validate_stream_info(
        info_value, path_name, expected_total, label)
    path = safe_path(root, info.get("path"), path_name, label)
    require(sha256_file(path) == expected_artifact, f"{label}: compressed digest changed")
    digest = hashlib.sha256()
    entries: list[StreamEntry] = []
    seen_stream: set[int] = set()
    seen_source: set[int] = set()
    try:
        with lzma.open(path, "rb") as stream:
            for position, raw in enumerate(stream):
                value = strict_json(raw, f"{label} row {position}")
                record, residual = source_record(value, residuals, f"{label} row {position}")
                require(raw == canonical_bytes(record), f"{label} row {position}: noncanonical")
                stream_index, source_index = record[0], record[1]
                require(stream_index not in seen_stream and source_index not in seen_source,
                        f"{label} row {position}: duplicate identity")
                seen_stream.add(stream_index)
                seen_source.add(source_index)
                digest.update(raw)
                entries.append(StreamEntry(record, raw, residual))
    except (lzma.LZMAError, EOFError) as error:
        raise RuntimeError(f"{label}: invalid XZ stream") from error
    require(len(entries) == expected_total and digest.hexdigest() == expected_raw,
            f"{label}: count or raw digest changed")
    return tuple(entries)


def family(record: Record) -> Family:
    edges = tuple(tuple(edge) for edge in record[3])
    odds = tuple(record[4])
    kinds = [0, 0, 0]
    adjacency = [set() for _ in range(ORDER)]
    for (u, v, multiplicity), odd in zip(edges, odds, strict=True):
        adjacency[u].add(v)
        adjacency[v].add(u)
        kinds[0 if odd == 0 else 2 if odd == multiplicity else 1] += 1
    triangles = sum(len(adjacency[u] & adjacency[v])
                    for u in range(ORDER) for v in adjacency[u] if u < v) // 3
    return (tuple(sorted((edge[2] for edge in edges), reverse=True)), tuple(kinds),
            len(edges) - ORDER + 1, triangles)


def family_object(key: Family, orbit_total: int, physical_total: int) -> dict[str, Json]:
    return {
        "multiplicity_partition": list(key[0]),
        "bundle_types": list(key[1]),
        "cycle_rank": key[2],
        "triangle_total": key[3],
        "orbit_total": orbit_total,
        "physical_total": physical_total,
    }


def family_census(entries: Sequence[StreamEntry]) -> tuple[Counter[Family], Counter[Family], tuple[Family, ...]]:
    orbits: Counter[Family] = Counter()
    physical: Counter[Family] = Counter()
    for entry in entries:
        key = family(entry.record)
        orbits[key] += 1
        physical[key] += entry.record[5]
    ranked = tuple(sorted(orbits, key=lambda key: (-orbits[key], -physical[key], key)))
    return orbits, physical, ranked


def fraction_rows(value: object, denominator: int, label: str) -> tuple[tuple[Fraction, ...], ...]:
    rows_value = exact_list(value, label)
    rows: list[tuple[Fraction, ...]] = []
    for row_index, row_value in enumerate(rows_value):
        row = exact_list(row_value, f"{label}[{row_index}]")
        require(len(row) == ORDER - 1, f"{label}[{row_index}]: wrong dimension")
        rows.append(tuple(Fraction(exact_int(item, f"{label}[{row_index}][{column}]"),
                                            denominator)
                          for column, item in enumerate(row)))
    return tuple(rows)


def decode_witness(value: object, label: str) -> Witness:
    payload = exact_mapping(value, label)
    require(set(payload) == WITNESS_FIELDS, f"{label}: witness fields changed")
    denominator = exact_int(payload.get("denominator"), f"{label}.denominator", minimum=1)
    require(denominator in DENOMINATORS, f"{label}: denominator not permitted")
    branches = fraction_rows(payload.get("branches"), denominator, f"{label}.branches")
    canonical_value = exact_list(payload.get("canonical"), f"{label}.canonical")
    extended_value = exact_list(payload.get("extended"), f"{label}.extended")
    require(len(branches) == ORDER and len(canonical_value) == len(extended_value) == PATH_COUNT,
            f"{label}: packet dimensions changed")
    canonical = tuple(fraction_rows(item, denominator, f"{label}.canonical[{index}]")
                      for index, item in enumerate(canonical_value))
    extended = tuple(fraction_rows(item, denominator, f"{label}.extended[{index}]")
                     for index, item in enumerate(extended_value))
    return denominator, branches, canonical, extended


def dot(left: Sequence[Fraction], right: Sequence[Fraction]) -> Fraction:
    require(len(left) == len(right), "internal vector dimensions differ")
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction())


def rational_unit(parameters: Sequence[Fraction]) -> tuple[Fraction, ...]:
    require(len(parameters) == ORDER - 1, "stereographic parameter dimension changed")
    square = dot(parameters, parameters)
    denominator = 1 + square
    require(denominator > 0, "stereographic denominator is not positive")
    vector = ((1 - square) / denominator,) + tuple(2 * value / denominator
                                                   for value in parameters)
    require(dot(vector, vector) == 1, "rational-unit identity failed")
    return vector


def exact_step_cost(left: Sequence[Fraction], right: Sequence[Fraction]) -> Fraction:
    correlation = dot(left, right)
    require(-1 < correlation <= 1, "packet step has invalid or antipodal correlation")
    cost = (1 - correlation) / (1 + correlation)
    require(cost >= 0, "packet step cost is negative")
    return cost


def path_ledger(record: Record) -> tuple[tuple[int, int, int, int, int], ...]:
    paths: list[tuple[int, int, int, int, int]] = []
    for edge_index, (edge_value, odd) in enumerate(zip(record[3], record[4], strict=True)):
        u, v, multiplicity = edge_value
        lengths = (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)
        paths.extend((edge_index, occurrence, u, v, length)
                     for occurrence, length in enumerate(lengths))
    require(len(paths) == PATH_COUNT, "packet path ledger width changed")
    return tuple(paths)


def replay_witness(record: Record, witness: Witness, label: str) -> None:
    denominator, branch_parameters, canonical, extended = witness
    require(denominator in DENOMINATORS, f"{label}: denominator escaped contract")
    branches = tuple(rational_unit(row) for row in branch_parameters)
    paths = path_ledger(record)
    base_costs: list[Fraction] = []
    extended_costs: list[Fraction] = []
    for index, ((_, _, u, v, length), base, longer) in enumerate(
            zip(paths, canonical, extended, strict=True)):
        endpoint = branches[v] if length % 2 == 0 else tuple(-value for value in branches[v])
        require(len(base) == length - 1 and len(longer) == length + 1,
                f"{label}: path {index} packet widths changed")
        costs: list[Fraction] = []
        for parameters in (base, longer):
            chain = (branches[u], *(rational_unit(row) for row in parameters), endpoint)
            costs.append(sum((exact_step_cost(left, right)
                              for left, right in zip(chain, chain[1:])), Fraction()))
        base_costs.append(costs[0])
        extended_costs.append(costs[1])
    base_total = sum(base_costs, Fraction())
    require(base_total <= BUDGET, f"{label}: canonical exact Fraction cost exceeds six")
    require(all(base_total - old + new <= BUDGET
                for old, new in zip(base_costs, extended_costs, strict=True)),
            f"{label}: exact Fraction frontier cost exceeds six")


def read_owner_stream(root: Path, spec: LaneSpec, info_value: object,
                      source_by_index: Mapping[int, StreamEntry]) -> tuple[set[int], int]:
    label = f"lane {spec.ordinal} owners"
    info, expected_raw, expected_artifact = validate_stream_info(
        info_value, spec.owner_stream_name, spec.owner_total, label)
    path = safe_path(root, info.get("path"), spec.owner_stream_name, label)
    require(sha256_file(path) == expected_artifact, f"{label}: compressed digest changed")
    digest = hashlib.sha256()
    owners: set[int] = set()
    physical = 0
    try:
        with lzma.open(path, "rb") as stream:
            for position, raw in enumerate(stream):
                owner = exact_mapping(strict_json(raw, f"{label} row {position}"),
                                      f"{label} row {position}")
                require(raw == canonical_bytes(owner), f"{label} row {position}: noncanonical")
                require(set(owner) == OWNER_FIELDS, f"{label} row {position}: fields changed")
                stream_index = exact_int(owner.get("stream_index"),
                                         f"{label} row {position}.stream_index", minimum=0)
                require(stream_index not in owners and stream_index in source_by_index,
                        f"{label} row {position}: duplicate or foreign stream index")
                source = source_by_index[stream_index]
                require(exact_int(owner.get("source_index"),
                                  f"{label} row {position}.source_index", minimum=0) ==
                        source.record[1] and
                        exact_int(owner.get("global_kernel"),
                                  f"{label} row {position}.global_kernel", minimum=0) ==
                        source.record[2] and
                        exact_int(owner.get("orbit_size"),
                                  f"{label} row {position}.orbit_size", minimum=1) ==
                        source.record[5],
                        f"{label} row {position}: metadata differs from source")
                exact_float(owner.get("numerical_canonical_cost"),
                            f"{label} row {position}.numerical_canonical_cost")
                require(family(source.record) == spec.target,
                        f"{label} row {position}: owner lies outside target family")
                witness = decode_witness(owner.get("witness"), f"{label} row {position}.witness")
                replay_witness(source.record, witness, f"{label} row {position}")
                digest.update(raw)
                owners.add(stream_index)
                physical += source.record[5]
    except (lzma.LZMAError, EOFError) as error:
        raise RuntimeError(f"{label}: invalid XZ stream") from error
    require(len(owners) == spec.owner_total and digest.hexdigest() == expected_raw,
            f"{label}: count or raw digest changed")
    return owners, physical


def exact_target_report(report: Mapping[str, Json], spec: LaneSpec,
                        orbit_total: int, physical_total: int) -> None:
    target = exact_mapping(report.get("target_family"), f"lane {spec.ordinal}.target_family")
    expected = family_object(spec.target, orbit_total, physical_total)
    expected["scanned_total"] = spec.owner_total
    if spec.ordinal != "IV":
        expected["dominance_rank"] = spec.dominance_rank
    require(target == expected, f"lane {spec.ordinal}: target-family report changed")


def exact_dominant_report(report: Mapping[str, Json], spec: LaneSpec,
                          entries: Sequence[StreamEntry]) -> None:
    if spec.ordinal == "IV":
        require("dominant_families" not in report,
                "lane IV: unexpected dominant-family table")
        return
    orbits, physical, ranked = family_census(entries)
    expected = [family_object(key, orbits[key], physical[key]) for key in ranked]
    require(report.get("dominant_families") == expected,
            f"lane {spec.ordinal}: exact dominant-family census changed")
    require(spec.target in orbits and ranked[spec.dominance_rank - 1] == spec.target,
            f"lane {spec.ordinal}: declared dominance rank changed")


def classification_digest(entries: Sequence[StreamEntry], target: Family,
                          owners: set[int]) -> str:
    digest = hashlib.sha256()
    for entry in entries:
        if family(entry.record) == target:
            digest.update(canonical_bytes([entry.record[0], entry.record[1],
                                           entry.record[0] in owners]))
    return digest.hexdigest()


def verify_remainder(root: Path, spec: LaneSpec, report: Mapping[str, Json],
                     expected: Sequence[StreamEntry], residuals: Sequence[Residual]) -> tuple[StreamEntry, ...]:
    require(spec.remainder_stream_name is not None, "internal materialized remainder error")
    remainder = read_source_stream(
        root, spec.remainder_stream_name, report.get("reduced_remainder_stream"),
        spec.remainder_total, residuals, f"lane {spec.ordinal} remainder")
    require(len(expected) == len(remainder), f"lane {spec.ordinal}: remainder width changed")
    for position, (wanted, observed) in enumerate(zip(expected, remainder, strict=True)):
        require(wanted.raw == observed.raw and wanted.record == observed.record,
                f"lane {spec.ordinal}: remainder row {position} is not byte complement")
    return remainder


def verify_lane(root: Path, spec: LaneSpec, source: Sequence[StreamEntry],
                source_info: Mapping[str, Json], residuals: Sequence[Residual]) -> tuple[tuple[StreamEntry, ...], LaneReceipt, Mapping[str, Json]]:
    report_raw, report = parse_report(root, spec)
    source_report = exact_mapping(report.get("source_report"), f"lane {spec.ordinal}.source_report")
    require(set(source_report) == {"path", "sha256"} and
            source_report.get("path") == spec.source_report_name,
            f"lane {spec.ordinal}: source-report link changed")
    source_report_path = safe_path(root, source_report.get("path"), spec.source_report_name,
                                   f"lane {spec.ordinal}.source_report")
    require(source_report.get("sha256") == hashlib.sha256(source_report_path.read_bytes()).hexdigest(),
            f"lane {spec.ordinal}: source-report digest changed")
    report_source = exact_mapping(report.get("source_stream"), f"lane {spec.ordinal}.source_stream")
    require(report_source == source_info,
            f"lane {spec.ordinal}: source-stream metadata does not chain exactly")
    require(len(source) == spec.source_total,
            f"lane {spec.ordinal}: source total differs from contract")

    orbits, physical, _ = family_census(source)
    require(orbits[spec.target] == spec.owner_total and physical[spec.target] == spec.target_physical,
            f"lane {spec.ordinal}: target census changed")
    exact_target_report(report, spec, orbits[spec.target], physical[spec.target])
    exact_dominant_report(report, spec, source)
    source_by_index = {entry.record[0]: entry for entry in source}
    require(len(source_by_index) == len(source), f"lane {spec.ordinal}: duplicate source index")
    owners, owned_physical = read_owner_stream(
        root, spec, report.get("owner_stream"), source_by_index)
    target_indices = {entry.record[0] for entry in source if family(entry.record) == spec.target}
    require(owners == target_indices, f"lane {spec.ordinal}: owners are not exactly target family")
    require(owned_physical == spec.target_physical,
            f"lane {spec.ordinal}: owner physical total changed")
    require(report.get("classification_stream_sha256") ==
            classification_digest(source, spec.target, owners),
            f"lane {spec.ordinal}: classification digest changed")
    require(exact_int(report.get("owned_orbit_total"), f"lane {spec.ordinal}.owned_orbit_total") ==
            spec.owner_total and
            exact_int(report.get("owned_physical_total"), f"lane {spec.ordinal}.owned_physical_total") ==
            spec.target_physical and
            exact_int(report.get("owned_target_total"), f"lane {spec.ordinal}.owned_target_total") ==
            TARGETS_PER_ROW * spec.owner_total and
            exact_int(report.get("remaining_target_family_total"),
                      f"lane {spec.ordinal}.remaining_target_family_total") == 0,
            f"lane {spec.ordinal}: owner accounting changed")

    remainder = tuple(entry for entry in source if entry.record[0] not in owners)
    require(len(remainder) == spec.remainder_total and
            spec.source_total == spec.owner_total + spec.remainder_total,
            f"lane {spec.ordinal}: partition arithmetic changed")
    if spec.ordinal == "IV":
        # Lane IV predates a materialized reduced stream.  This in-memory,
        # order-preserving complement is the authenticated topology consumed
        # virtually by lane V from the same lane-III source artifact.
        require("reduced_remainder_stream" not in report,
                "lane IV: unexpected materialized remainder")
    else:
        require(exact_int(report.get("scanned_remainder_total"),
                          f"lane {spec.ordinal}.scanned_remainder_total") == spec.source_total and
                exact_int(report.get("remaining_remainder_total"),
                          f"lane {spec.ordinal}.remaining_remainder_total") == spec.remainder_total,
                f"lane {spec.ordinal}: remainder accounting changed")
        remainder = verify_remainder(root, spec, report, remainder, residuals)
    require(report_raw == safe_path(root, spec.report_name, spec.report_name,
                                    f"lane {spec.ordinal} report readback").read_bytes(),
            f"lane {spec.ordinal}: report changed during read-only audit")
    receipt = LaneReceipt(spec.ordinal, spec.source_total, spec.owner_total,
                          spec.remainder_total, spec.target_physical,
                          spec.owner_total * TARGETS_PER_ROW)
    return remainder, receipt, report


def verify_fifth_virtual_topology(spec: LaneSpec, report: Mapping[str, Json],
                                  full_lane_iv_source: Sequence[StreamEntry],
                                  virtual_iv_remainder: Sequence[StreamEntry]) -> None:
    require(spec.ordinal == "V" and spec.virtual_closed_target is not None,
            "internal lane-V topology error")
    closed = spec.virtual_closed_target
    closed_indices = {entry.record[0] for entry in full_lane_iv_source if family(entry.record) == closed}
    require(len(closed_indices) == spec.virtual_closed_total and
            len(virtual_iv_remainder) == spec.source_total and
            tuple(entry for entry in full_lane_iv_source
                  if entry.record[0] not in closed_indices) == tuple(virtual_iv_remainder),
            "lane V: virtual lane-IV complement topology changed")
    require(exact_int(report.get("closed_source_family_total"),
                      "lane V.closed_source_family_total") == spec.virtual_closed_total,
            "lane V: virtual closed-source count changed")


def load_manifest_residuals(root: Path) -> tuple[Residual, ...]:
    manifest_path = safe_path(root, MANIFEST_NAME, MANIFEST_NAME, "residual manifest")
    manifest_raw = manifest_path.read_bytes()
    require(hashlib.sha256(manifest_raw).hexdigest() == EXPECTED_MANIFEST_SHA256,
            "residual manifest digest changed")
    manifest = exact_mapping(strict_json(manifest_raw, MANIFEST_NAME), MANIFEST_NAME)
    require(manifest_raw == canonical_bytes(manifest), "residual manifest is noncanonical")
    require(manifest.get("schema") ==
            "rank-seven-order-eight-exact-residual-census-manifest-v1" and
            manifest.get("order") == ORDER and manifest.get("path_count") == PATH_COUNT and
            manifest.get("coarse_residual_total") == 493417,
            "residual manifest contract changed")

    indices_path = safe_path(root, INDICES_NAME, INDICES_NAME, "rational-search indices")
    indices_raw = indices_path.read_bytes()
    require(hashlib.sha256(indices_raw).hexdigest() == EXPECTED_INDICES_SHA256,
            "rational-search index digest changed")
    indices = exact_mapping(strict_json(indices_raw, INDICES_NAME), INDICES_NAME)
    require(indices_raw == canonical_bytes(indices) and set(indices) == {
        "schema", "manifest_sha256", "selected_chunks", "source_indices"
    } and indices.get("schema") == "rank-seven-order-eight-rational-search-indices-v1" and
        indices.get("manifest_sha256") == EXPECTED_MANIFEST_SHA256 and
        indices.get("selected_chunks") == list(range(8)),
        "rational-search index contract changed")
    wanted_value = exact_list(indices.get("source_indices"), "source_indices")
    wanted = tuple(exact_int(value, f"source_indices[{index}]", minimum=0)
                   for index, value in enumerate(wanted_value))
    require(len(wanted) == EXPECTED_SELECTED_TOTAL and
            all(left < right for left, right in zip(wanted, wanted[1:])),
            "selected residual indices changed")

    residuals: list[Residual] = []
    wanted_position = 0
    source_offset = 0
    chunks = exact_list(manifest.get("chunks"), "manifest.chunks")
    require(len(chunks) == 8, "residual chunk count changed")
    for chunk_index, chunk_info_value in enumerate(chunks):
        chunk_info = exact_mapping(chunk_info_value, f"manifest.chunks[{chunk_index}]")
        chunk_name = exact_string(chunk_info.get("path"), f"manifest.chunks[{chunk_index}].path")
        path = safe_path(root, chunk_name, chunk_name, f"residual chunk {chunk_index}")
        require(sha256_file(path) == hex_digest(chunk_info.get("artifact_sha256"),
                                                f"chunk {chunk_index}.artifact_sha256"),
                f"residual chunk {chunk_index}: compressed digest changed")
        try:
            raw = lzma.decompress(path.read_bytes(), format=lzma.FORMAT_XZ)
        except lzma.LZMAError as error:
            raise RuntimeError(f"residual chunk {chunk_index}: invalid XZ") from error
        require(hashlib.sha256(raw).hexdigest() == hex_digest(
            chunk_info.get("raw_sha256"), f"chunk {chunk_index}.raw_sha256"),
            f"residual chunk {chunk_index}: raw digest changed")
        chunk = exact_mapping(strict_json(raw, chunk_name), chunk_name)
        require(raw == canonical_bytes(chunk), f"residual chunk {chunk_index}: noncanonical")
        kernels: dict[int, tuple[tuple[int, int, int], ...]] = {}
        for kernel_position, kernel_value in enumerate(exact_list(chunk.get("kernels"),
                                                                  f"chunk {chunk_index}.kernels")):
            kernel = exact_mapping(kernel_value, f"chunk {chunk_index}.kernels[{kernel_position}]")
            order_kernel = exact_int(kernel.get("order_kernel"), "order_kernel", minimum=0)
            global_kernel = exact_int(kernel.get("global_kernel"), "global_kernel", minimum=0)
            edges: list[tuple[int, int, int]] = []
            for edge_position, edge_value in enumerate(exact_list(kernel.get("edges"), "kernel.edges")):
                edge = exact_list(edge_value, f"kernel.edges[{edge_position}]")
                require(len(edge) == 3, "kernel edge is not a triple")
                u = exact_int(edge[0], "kernel edge.u", minimum=0)
                v = exact_int(edge[1], "kernel edge.v", minimum=0)
                multiplicity = exact_int(edge[2], "kernel edge.multiplicity", minimum=1)
                require(u < v < ORDER, "kernel edge endpoints changed")
                edges.append((u, v, multiplicity))
            require(order_kernel not in kernels and
                    all(left < right for left, right in zip(edges, edges[1:])),
                    "kernel ordering or identity changed")
            kernels[order_kernel] = tuple(edges)
            require(global_kernel >= 0, "global kernel changed")
        residual_values = exact_list(chunk.get("residuals"), f"chunk {chunk_index}.residuals")
        expected_chunk_total = exact_int(chunk_info.get("coarse_residual_total"),
                                         f"chunk {chunk_index}.coarse_residual_total", minimum=0)
        require(len(residual_values) == expected_chunk_total,
                f"residual chunk {chunk_index}: record total changed")
        for local_index, source_value in enumerate(residual_values):
            source_index = source_offset + local_index
            if wanted_position == len(wanted) or wanted[wanted_position] != source_index:
                continue
            source = exact_mapping(source_value, f"chunk {chunk_index}.residuals[{local_index}]")
            order_kernel = exact_int(source.get("order_kernel"), "residual.order_kernel", minimum=0)
            require(order_kernel in kernels, "residual references an unknown order kernel")
            edges = kernels[order_kernel]
            row_value = exact_list(source.get("row"), "residual.row")
            row = tuple(exact_int(value, f"residual.row[{position}]", minimum=0)
                        for position, value in enumerate(row_value))
            require(len(row) == len(edges) and
                    all(odd <= edge[2] for edge, odd in zip(edges, row, strict=True)),
                    "residual parity row changed")
            support = tuple(u * (2 * ORDER - u - 1) // 2 + v - u - 1
                            for u, v, _ in edges)
            residuals.append((
                exact_int(source.get("global_kernel"), "residual.global_kernel", minimum=0),
                source_index, support, tuple(edge[2] for edge in edges), row,
                exact_int(source.get("orbit_size"), "residual.orbit_size", minimum=1),
            ))
            wanted_position += 1
        source_offset += expected_chunk_total
    require(source_offset == 493417 and wanted_position == len(wanted) and
            len(residuals) == EXPECTED_SELECTED_TOTAL,
            "selected residual stream reconstruction changed")
    return tuple(residuals)


def verify_chain(root: Path = HERE, *, report_hashes: Mapping[str, str] | None = None) -> ChainReceipt:
    root = root.resolve()
    residuals = load_manifest_residuals(root)
    specs = LANES
    if report_hashes is not None:
        specs = tuple(LaneSpec(**{**spec.__dict__,
                                 "report_sha256": report_hashes.get(spec.report_name,
                                                                    spec.report_sha256)})
                      for spec in LANES)

    lane_iv = specs[0]
    _, iv_report = parse_report(root, lane_iv)
    iv_source_info = exact_mapping(iv_report.get("source_stream"), "lane IV.source_stream")
    full_source = read_source_stream(root, lane_iv.source_stream_name, iv_source_info,
                                     lane_iv.source_total, residuals, "lane IV source")
    remainder, receipt, previous_report = verify_lane(
        root, lane_iv, full_source, iv_source_info, residuals)
    receipts = [receipt]
    source_info: Mapping[str, Json] = iv_source_info

    for spec in specs[1:]:
        _, report = parse_report(root, spec)
        report_source_info = exact_mapping(report.get("source_stream"),
                                           f"lane {spec.ordinal}.source_stream")
        if spec.ordinal == "V":
            require(report_source_info == iv_source_info,
                    "lane V: physical source must be the lane-IV source artifact")
            verify_fifth_virtual_topology(spec, report, full_source, remainder)
        else:
            source_info = exact_mapping(previous_report.get("reduced_remainder_stream"),
                                        f"lane {spec.ordinal} predecessor remainder")
            require(report_source_info == source_info,
                    f"lane {spec.ordinal}: predecessor metadata changed")
        remainder, lane_receipt, previous_report = verify_lane(
            root, spec, remainder, report_source_info, residuals)
        receipts.append(lane_receipt)

    return ChainReceipt(len(residuals), tuple(receipts))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=HERE,
                        help="artifact directory (default: verifier directory)")
    args = parser.parse_args(argv)
    receipt = verify_chain(args.root)
    for lane in receipt.lanes:
        print(f"{lane.ordinal}: source={lane.source_total} owners={lane.owner_total} "
              f"remainder={lane.remainder_total} physical={lane.physical_total}")
    print(f"rank7 order8 packet chain IV--XII: PASS "
          f"(residuals={receipt.selected_residual_total}, "
          f"owners={sum(lane.owner_total for lane in receipt.lanes)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
