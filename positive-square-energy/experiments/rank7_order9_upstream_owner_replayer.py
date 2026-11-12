#!/usr/bin/env python3
"""Read-only exact replay of historical order-nine upstream owner payloads.

The numerical producers are deliberately outside this trust boundary.  This
module authenticates the persisted source/report/owner bytes, binds every
owner to its exact source row, and reconstructs each accepted Gram and path
cost using only :class:`fractions.Fraction` arithmetic.  It never searches,
optimizes, imports numerical packages, or writes an artifact.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import lzma
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KERNEL_FIXTURE = ROOT / "research" / "fixtures" / "rank-seven-kernel-frontier-census.json"
STRUCTURAL_MANIFEST = HERE / "rank7_order9_structural_owner_manifest.json"
STRUCTURAL_RESULTS = HERE / "rank7_order9_structural_owner_scheduler" / "results"
SOS_REPORT = HERE / "rank7_order9_typed_sos_owner_manifest.json"
SOS_OWNERS = HERE / "rank7_order9_typed_sos_owners.jsonl.xz"
SOS_REMAINDER = HERE / "rank7_order9_after_sos_remainder.jsonl.xz"
DOMINANT_REPORT = HERE / "rank7_order9_dominant_family_gram_lane.json"
DOMINANT_OWNERS = HERE / "rank7_order9_dominant_family_gram_owners.jsonl.xz"

ORDER = 9
PATH_COUNT = 15
TARGETS_PER_ROW = 16
BUDGET = Fraction(6)
F = Fraction
EXPECTED_KERNEL_SHA256 = "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5"
EXPECTED_KERNEL_COUNTS = (1, 6, 47, 233, 914, 2270, 4015, 4495, 3396, 1391, 365)
EXPECTED_STRUCTURAL_MANIFEST_SHA256 = "8097c55f455cf68e27e29b571ef5cd94e17057290d1f211fb3ecf81949f98366"
EXPECTED_SOS_REPORT_SHA256 = "76e80ac1e1aa5c3277883b8df43ab514fc196c1f8049544d254614a4e4375274"
EXPECTED_DOMINANT_REPORT_SHA256 = "7346c593bd98880ca9599f44ae26c69d20225342d361804740742caccdc75169"
EXPECTED_STRUCTURAL_RECEIPT_SHA256S = (
    "ebc040006305390d28ae4f21b2072a66e2af8ef9cd7933d5e400dba6cc3ff47d",
    "6af96ac219d946e7bf631ccda7410bda3d2a8093711bdb1a43a0f87bd62e29dc",
    "7d109b0d4702e9f654ae9c4312136d88cd8b29aba8de7ad4f8b1d616a2aacb2b",
    "d0cb1f8018cf646c17d322efa2a3b8fdfc9dad452a43d638e9d89aa7c8137374",
    "708c6b03c55c6e47545342746adf86bca91d416ed5ab75b0b576b057e55ecbb5",
    "6cf90f2086bb21cc8d59f73906dab8de53a33837a27f8fd88703cff4f5400985",
    "808e8c663a1d2568a1461d958908e43fd617fe00b1d5a22e6a3e4a4cf2632b6d",
    "1a70dd560c75f92460047c1af93b50832d9db17345118537ef207bff7a20df49",
)
EXPECTED_STRUCTURAL_SOURCE_RANGES = (
    (0, 304033), (304033, 624173), (624173, 963504),
    (963504, 1375315), (1375315, 1704789), (1704789, 2110183),
    (2110183, 2488801), (2488801, 2835895),
)
EXPECTED_SOS_OWNER_KEY_SHA256 = "e79f723c4cfb47dde6a922067c684bb425f8e84422e1973cfefc54ee4ad86465"
EXPECTED_DOMINANT_OWNER_KEY_SHA256 = "2d264fcf673d21f2200fbfddc1833b1f87f6f2351ee220e96b62db21d2ba7c11"
REPLAY_SCHEMA = "rank-seven-order-nine-upstream-owner-replay-v1"
STRUCTURAL_MANIFEST_SCHEMA = "rank-seven-order-nine-structural-owner-coverage-v1"
STRUCTURAL_RECEIPT_SCHEMA = "rank-seven-order-nine-structural-owner-chunk-v1"
SOS_SCHEMA = "rank-seven-order-nine-typed-diagonal-sos-owner-lane-v1"
DOMINANT_SCHEMA = "rank-seven-order-nine-dominant-family-gram-lane-v1"
SOS_COUNTS = {"scalar-sos": 7796, "typed-sos": 105513}
SOS_PHYSICAL_COUNTS = {"scalar-sos": 10958, "typed-sos": 123941}
SOS_SOURCE_TOTAL = 385829
SOS_REMAINDER_TOTAL = 272520
DOMINANT_TOTAL = 1128
DOMINANT_PHYSICAL = 1173
SOS_OWNER_PHYSICAL = sum(SOS_PHYSICAL_COUNTS.values())
UPSTREAM_OWNER_PHYSICAL = SOS_OWNER_PHYSICAL + DOMINANT_PHYSICAL
DOMINANT_TARGET = (
    (2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1), (3, 3, 6), 4, 1,
)

STRUCTURAL_MANIFEST_KEYS = {
    "atom_profile_owner_counts", "atom_recognizer_sha256", "chunks",
    "classification_stream_sha256", "exclusive_owner_orbit_counts",
    "exclusive_owner_physical_counts", "frontiers_per_residual", "full_theorem",
    "manifest_sha256", "order", "owner_engine_sha256", "path_count",
    "payload_free_owned_orbit_total", "payload_free_owned_physical_total",
    "payload_free_owned_target_total", "rank", "remainder_orbit_total",
    "remainder_physical_total", "remainder_stream_sha256", "remainder_target_total",
    "scanned_residual_total", "scanned_target_total", "schema", "scope", "status",
}
STRUCTURAL_MANIFEST_CHUNK_KEYS = {
    "artifact_sha256", "exclusive_owner_orbit_counts",
    "exclusive_owner_physical_counts", "kernel_range", "path",
    "remainder_orbit_total", "remainder_physical_total", "scanned_residual_total",
}
STRUCTURAL_RECEIPT_KEYS = {
    "atom_profile_owner_counts", "atom_recognizer_sha256", "census_artifact_sha256",
    "census_path", "chunk_index", "classification_stream",
    "exclusive_owner_orbit_counts", "exclusive_owner_physical_counts",
    "full_theorem", "kernel_range", "manifest_sha256", "owner_engine_sha256",
    "remainder_orbit_total", "remainder_physical_total", "remainder_stream",
    "scanned_residual_total", "schema", "source_range",
}
STRUCTURAL_STREAM_KEYS = {"artifact_sha256", "path", "sha256"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def _duplicate_safe_pairs(label: str):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"duplicate key in {label}: {key}")
            result[key] = value
        return result
    return pairs


def _reject_json_number(kind: str, label: str):
    def reject(value):
        raise RuntimeError(f"{kind} JSON number in {label}: {value}")
    return reject


def strict_json(raw: bytes, label: str):
    """Parse integral ASCII JSON, rejecting floats and duplicate names."""
    try:
        return json.loads(
            raw.decode("ascii"), object_pairs_hook=_duplicate_safe_pairs(label),
            parse_float=_reject_json_number("floating-point", label),
            parse_constant=_reject_json_number("nonstandard", label),
        )
    except (UnicodeDecodeError, json.JSONDecodeError, OverflowError) as error:
        raise RuntimeError(f"cannot parse {label}") from error


def dominant_json(raw: bytes, label: str):
    """Parse one dominant row, permitting only its finite diagnostic float."""
    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=_duplicate_safe_pairs(label),
            parse_float=float,
            parse_constant=_reject_json_number("nonstandard", label),
        )
    except (UnicodeDecodeError, json.JSONDecodeError, OverflowError) as error:
        raise RuntimeError(f"cannot parse {label}") from error
    require(isinstance(value, list) and len(value) == 4,
            "malformed dominant-family payload")
    diagnostic = value[2]
    require(type(diagnostic) in (int, float) and not isinstance(diagnostic, bool) and
            math.isfinite(diagnostic),
            "malformed dominant-family diagnostic")
    # Integers are permitted throughout the frozen schema.  The sole location
    # in which a parsed binary64 may occur is payload[2].
    def reject_nested_float(item, path=()):
        if type(item) is float:
            require(path == (2,), "floating-point value outside dominant diagnostic")
        elif isinstance(item, list):
            for index, child in enumerate(item):
                reject_nested_float(child, path + (index,))
        elif isinstance(item, dict):
            for key, child in item.items():
                reject_nested_float(child, path + (key,))
    reject_nested_float(value)
    return value


def strict_file(path: Path, expected_sha256: str, label: str,
                *, canonical=True):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == expected_sha256,
            f"{label} identity changed")
    value = strict_json(raw, label)
    if canonical:
        require(raw == canonical_bytes(value), f"noncanonical {label}")
    return value


def exact_int(raw, label: str, *, minimum=None):
    require(type(raw) is int, f"malformed integer: {label}")
    require(minimum is None or raw >= minimum, f"integer out of range: {label}")
    return raw


def rational_pair(raw, label: str, maximum_denominator=None) -> F:
    require(isinstance(raw, list) and len(raw) == 2 and
            all(type(value) is int for value in raw),
            f"malformed rational pair: {label}")
    numerator, denominator = raw
    require(denominator > 0 and math.gcd(abs(numerator), denominator) == 1,
            f"noncanonical rational pair: {label}")
    require(maximum_denominator is None or denominator <= maximum_denominator,
            f"rational denominator exceeds bound: {label}")
    value = F(numerator, denominator)
    require([value.numerator, value.denominator] == raw,
            f"noncanonical rational pair: {label}")
    return value


def load_kernels():
    fixture = strict_file(KERNEL_FIXTURE, EXPECTED_KERNEL_SHA256, "kernel fixture")
    require(isinstance(fixture, dict) and
            tuple(fixture.get("counts_by_order_n2_to_n12", ())) == EXPECTED_KERNEL_COUNTS,
            "kernel fixture ledger changed")
    kernels = {}
    local = 0
    records = fixture.get("kernels")
    require(isinstance(records, list), "malformed kernel fixture")
    for global_index, record in enumerate(records, 1):
        require(isinstance(record, dict) and
                set(record) >= {"n", "code"} and type(record["n"]) is int and
                isinstance(record["code"], list) and
                all(type(value) is int for value in record["code"]),
                "malformed kernel record")
        if record["n"] != ORDER:
            continue
        local += 1
        require(len(record["code"]) == ORDER * (ORDER - 1) // 2 and
                all(value >= 0 for value in record["code"]),
                "malformed order-nine kernel code")
        edges = tuple(
            (u, v, multiplicity)
            for (u, v), multiplicity in zip(
                itertools.combinations(range(ORDER), 2), record["code"], strict=True)
            if multiplicity
        )
        require(sum(edge[2] for edge in edges) == PATH_COUNT,
                "order-nine kernel path count changed")
        kernels[local] = (global_index, edges)
    require(len(kernels) == EXPECTED_KERNEL_COUNTS[ORDER - 2],
            "order-nine kernel total changed")
    return kernels


def validate_source_record(record, kernels, label: str):
    require(isinstance(record, list) and len(record) == 5, f"malformed {label}")
    source_index = exact_int(record[0], f"{label}.source_index", minimum=0)
    global_kernel = exact_int(record[1], f"{label}.global_kernel", minimum=1)
    order_kernel = exact_int(record[2], f"{label}.order_kernel", minimum=1)
    orbit_size = exact_int(record[4], f"{label}.orbit_size", minimum=1)
    require(order_kernel in kernels and kernels[order_kernel][0] == global_kernel,
            f"bad kernel reference: {label}")
    edges = kernels[order_kernel][1]
    row = record[3]
    require(isinstance(row, list) and len(row) == len(edges) and
            all(type(value) is int for value in row) and
            all(0 <= value <= edge[2] for value, edge in zip(row, edges, strict=True)),
            f"malformed parity row: {label}")
    return source_index, orbit_size, edges, tuple(row)


def strict_xz_rows(path: Path, info: dict, validator, *, parser=strict_json):
    require(isinstance(info, dict) and set(info) ==
            {"path", "record_total", "raw_sha256", "artifact_sha256"} and
            info["path"] == path.name and type(info["record_total"]) is int and
            info["record_total"] >= 0 and
            all(isinstance(info[key], str) and len(info[key]) == 64 and
                all(character in "0123456789abcdef" for character in info[key])
                for key in ("raw_sha256", "artifact_sha256")),
            f"malformed stream descriptor: {path.name}")
    require(sha256(path) == info["artifact_sha256"],
            f"artifact digest changed: {path.name}")
    digest = hashlib.sha256()
    total = 0
    try:
        with lzma.open(path, "rb") as stream:
            for raw in stream:
                payload = parser(raw, path.name)
                require(raw == canonical_bytes(payload), f"noncanonical row: {path.name}")
                validator(payload, total)
                digest.update(raw)
                total += 1
    except lzma.LZMAError as error:
        raise RuntimeError(f"cannot decompress {path.name}") from error
    require(total == info["record_total"] and digest.hexdigest() == info["raw_sha256"],
            f"stream identity changed: {path.name}")
    return total


def structural_source(kernels):
    manifest = strict_file(STRUCTURAL_MANIFEST,
                           EXPECTED_STRUCTURAL_MANIFEST_SHA256,
                           "structural owner manifest")
    require(isinstance(manifest, dict) and set(manifest) == STRUCTURAL_MANIFEST_KEYS and
            manifest["schema"] == STRUCTURAL_MANIFEST_SCHEMA and
            manifest["full_theorem"] is False and manifest["rank"] == 7 and
            manifest["order"] == ORDER and manifest["path_count"] == PATH_COUNT and
            manifest["frontiers_per_residual"] == TARGETS_PER_ROW and
            manifest["remainder_orbit_total"] == SOS_SOURCE_TOTAL and
            manifest["scanned_residual_total"] == EXPECTED_STRUCTURAL_SOURCE_RANGES[-1][1] and
            manifest["remainder_stream_sha256"] ==
            "0442d023ca3401f692fcb7866129ad83758753027dcac373a16da3b170c53a3e" and
            isinstance(manifest["chunks"], list) and
            len(manifest["chunks"]) == len(EXPECTED_STRUCTURAL_RECEIPT_SHA256S) and
            all(isinstance(chunk, dict) and set(chunk) == STRUCTURAL_MANIFEST_CHUNK_KEYS
                for chunk in manifest["chunks"]),
            "structural remainder ledger changed")
    records = {}
    digest = hashlib.sha256()
    last_source_index = -1
    for chunk_index, (expected, expected_receipt_sha256, expected_source_range) in enumerate(
            zip(manifest["chunks"], EXPECTED_STRUCTURAL_RECEIPT_SHA256S,
                EXPECTED_STRUCTURAL_SOURCE_RANGES, strict=True)):
        receipt_path = STRUCTURAL_RESULTS / f"chunk-{chunk_index:02d}.json"
        receipt = strict_file(receipt_path, expected_receipt_sha256,
                              f"structural receipt {chunk_index}")
        require(isinstance(receipt, dict) and set(receipt) == STRUCTURAL_RECEIPT_KEYS and
                receipt["schema"] == STRUCTURAL_RECEIPT_SCHEMA and
                receipt["full_theorem"] is False and
                receipt["chunk_index"] == chunk_index and
                tuple(receipt["source_range"]) == expected_source_range and
                receipt["source_range"][1] - receipt["source_range"][0] ==
                receipt["scanned_residual_total"] and
                receipt["manifest_sha256"] == manifest["manifest_sha256"] and
                receipt["owner_engine_sha256"] == manifest["owner_engine_sha256"] and
                receipt["atom_recognizer_sha256"] == manifest["atom_recognizer_sha256"] and
                receipt["census_artifact_sha256"] == expected["artifact_sha256"] and
                receipt["census_path"] == expected["path"] and
                receipt["kernel_range"] == expected["kernel_range"] and
                receipt["scanned_residual_total"] == expected["scanned_residual_total"] and
                receipt["remainder_orbit_total"] == expected["remainder_orbit_total"] and
                receipt["remainder_physical_total"] == expected["remainder_physical_total"] and
                receipt["exclusive_owner_orbit_counts"] == expected["exclusive_owner_orbit_counts"] and
                receipt["exclusive_owner_physical_counts"] == expected["exclusive_owner_physical_counts"],
                f"wrong structural receipt: {receipt_path.name}")
        for descriptor_name in ("classification_stream", "remainder_stream"):
            descriptor = receipt[descriptor_name]
            require(isinstance(descriptor, dict) and set(descriptor) == STRUCTURAL_STREAM_KEYS,
                    f"malformed {descriptor_name} descriptor: {receipt_path.name}")
        stream_info = receipt["remainder_stream"]
        require(stream_info["path"] == f"chunk-{chunk_index:02d}.remainder.jsonl.xz",
                f"wrong structural remainder path: {receipt_path.name}")
        stream_path = STRUCTURAL_RESULTS / stream_info["path"]
        require(stream_path.parent.resolve() == STRUCTURAL_RESULTS.resolve() and
                sha256(stream_path) == stream_info["artifact_sha256"],
                f"structural remainder artifact changed: {stream_path.name}")
        local_digest = hashlib.sha256()
        local_total = 0
        try:
            with lzma.open(stream_path, "rb") as stream:
                for raw in stream:
                    record = strict_json(raw, stream_path.name)
                    require(raw == canonical_bytes(record),
                            f"noncanonical structural row: {stream_path.name}")
                    source_index, _, _, _ = validate_source_record(
                        record, kernels, f"structural[{local_total}]")
                    require(expected_source_range[0] <= source_index < expected_source_range[1] and
                            source_index > last_source_index,
                            "structural source order or range changed")
                    last_source_index = source_index
                    records[source_index] = record
                    local_digest.update(raw)
                    digest.update(raw)
                    local_total += 1
        except lzma.LZMAError as error:
            raise RuntimeError(f"cannot decompress {stream_path.name}") from error
        require(local_total == receipt["remainder_orbit_total"] and
                local_digest.hexdigest() == stream_info["sha256"],
                f"structural remainder stream changed: {stream_path.name}")
    require(len(records) == SOS_SOURCE_TOTAL and
            digest.hexdigest() == manifest["remainder_stream_sha256"],
            "complete structural remainder identity changed")
    return manifest, records


def matrix_and_paths(edges, row):
    signed = [[0] * ORDER for _ in range(ORDER)]
    incident = [[] for _ in range(ORDER)]
    paths = []
    for edge_index, ((u, v, multiplicity), odd) in enumerate(zip(edges, row, strict=True)):
        value = multiplicity - 2 * odd
        signed[u][v] = signed[v][u] = value
        incident[u].append((multiplicity, odd))
        incident[v].append((multiplicity, odd))
        lengths = (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)
        paths.extend((edge_index, occurrence, u, v, length)
                     for occurrence, length in enumerate(lengths))
    require(len(paths) == PATH_COUNT, "physical path total changed")
    type_keys = tuple((sum(signed[u]), tuple(sorted(incident[u]))) for u in range(ORDER))
    dictionary = {key: index for index, key in enumerate(sorted(set(type_keys)))}
    type_ids = tuple(dictionary[key] for key in type_keys)
    return tuple(tuple(row) for row in signed), tuple(paths), type_keys, type_ids


def gram_cost(signed, paths, type_ids, parameters):
    require(len(parameters) == max(type_ids) + 1, "wrong typed parameter count")
    x = [[(parameters[type_ids[u]][0] if u == v else F()) +
          parameters[type_ids[u]][1] * signed[u][v]
          for v in range(ORDER)] for u in range(ORDER)]
    square = [[sum(x[u][w] * x[v][w] for w in range(ORDER))
               for v in range(ORDER)] for u in range(ORDER)]
    normalizer = max(square[u][u] for u in range(ORDER))
    require(normalizer > 0, "zero Gram normalizer")
    completion = tuple(1 - square[u][u] / normalizer for u in range(ORDER))
    require(all(value >= 0 for value in completion), "negative diagonal completion")
    gram = tuple(tuple((square[u][v] / normalizer if u != v else F(1))
                       for v in range(ORDER)) for u in range(ORDER))
    require(all(gram[u][v] == gram[v][u] for u in range(ORDER)
                for v in range(ORDER)) and
            all(gram[u][u] == 1 for u in range(ORDER)),
            "malformed reconstructed correlation Gram")
    total = F()
    for _, _, u, v, length in paths:
        transformed = -gram[u][v] if length & 1 else gram[u][v]
        require(-1 <= transformed <= 1, "Gram correlation escaped [-1,1]")
        if transformed == -1:
            return None, normalizer, completion
        total += (1 - transformed) / (length * (1 + transformed))
    return total, normalizer, completion


def scalar_parameters(type_total, coefficient):
    return tuple((F(1), coefficient) for _ in range(type_total))


def replay_sos_payload(payload, kernels, source_records, owner_seen,
                       *, previous_remainder_index=-1, previous_source_index=-1):
    """Pure exact replay of one SOS owner payload.

    The caller owns stream state and commits the returned key only after this
    function succeeds, which keeps mutation tests independent of disk streams.
    """
    require(isinstance(payload, list) and len(payload) == 2,
            "malformed SOS owner payload")
    record, classification = payload
    source_index, orbit_size, edges, row = validate_source_record(
        record, kernels, "SOS owner payload")
    require(source_records.get(source_index) == record and source_index not in owner_seen and
            source_index > previous_source_index,
            "SOS owner does not match ordered unique structural source row")
    require(isinstance(classification, list) and len(classification) == 7,
            "malformed SOS classification")
    remainder_index = exact_int(classification[0], "SOS remainder index", minimum=0)
    require(remainder_index > previous_remainder_index and
            classification[1] == source_index and type(classification[1]) is int and
            type(classification[2]) is str and
            classification[2] in ("scalar-sos", "typed-sos"),
            "SOS owner identity or precedence changed")
    lane = classification[2]
    coefficient = rational_pair(classification[3], "scalar coefficient", 16)
    stored_scalar_cost = rational_pair(classification[4], "scalar exact cost")
    signed, paths, _, type_ids = matrix_and_paths(edges, row)
    scalar_cost, _, _ = gram_cost(
        signed, paths, type_ids, scalar_parameters(max(type_ids) + 1, coefficient))
    require(scalar_cost is not None and scalar_cost == stored_scalar_cost,
            "scalar SOS exact cost mismatch")
    if lane == "scalar-sos":
        require(scalar_cost <= BUDGET and classification[5] is None and
                classification[6] is None,
                "malformed scalar SOS owner")
        cost = scalar_cost
    else:
        require(scalar_cost > BUDGET and isinstance(classification[5], list),
                "typed SOS precedence changed")
        raw_parameters = classification[5]
        require(len(raw_parameters) == max(type_ids) + 1,
                "typed SOS parameter count changed")
        parameters = []
        for index, values in enumerate(raw_parameters):
            require(isinstance(values, list) and len(values) == 2,
                    "malformed typed SOS parameter")
            parameters.append((
                rational_pair(values[0], f"typed parameter[{index}][0]", 3),
                rational_pair(values[1], f"typed parameter[{index}][1]", 9),
            ))
        stored_cost = rational_pair(classification[6], "typed exact cost")
        cost, _, _ = gram_cost(signed, paths, type_ids, tuple(parameters))
        require(cost is not None and cost == stored_cost and cost <= BUDGET,
                "typed SOS exact cost mismatch")
    return {
        "cost": cost, "lane": lane, "orbit_size": orbit_size,
        "remainder_index": remainder_index, "source_index": source_index,
    }


def family(edges, row):
    kinds = [0, 0, 0]
    adjacency = [set() for _ in range(ORDER)]
    for (u, v, multiplicity), odd in zip(edges, row, strict=True):
        adjacency[u].add(v)
        adjacency[v].add(u)
        kinds[0 if odd == 0 else 2 if odd == multiplicity else 1] += 1
    triangles = sum(len(adjacency[u] & adjacency[v])
                    for u in range(ORDER) for v in adjacency[u] if u < v) // 3
    return (tuple(sorted((edge[2] for edge in edges), reverse=True)), tuple(kinds),
            len(edges) - ORDER + 1, triangles)


def replay_sos(kernels, source_records):
    report = strict_file(SOS_REPORT, EXPECTED_SOS_REPORT_SHA256, "SOS report")
    require(report.get("schema") == SOS_SCHEMA and report.get("full_theorem") is False and
            report.get("owner_manifest_sha256") == EXPECTED_STRUCTURAL_MANIFEST_SHA256 and
            report.get("scanned_remainder_total") == SOS_SOURCE_TOTAL and
            report.get("exclusive_owner_counts") == SOS_COUNTS and
            report.get("precedence") == ["scalar-sos", "typed-sos"] and
            report.get("owned_total") == sum(SOS_COUNTS.values()) and
            report.get("remaining_total") == SOS_REMAINDER_TOTAL and
            report.get("owned_target_total") == sum(SOS_COUNTS.values()) * TARGETS_PER_ROW and
            report.get("remaining_target_total") == SOS_REMAINDER_TOTAL * TARGETS_PER_ROW,
            "SOS report semantics changed")
    owner_seen = set()
    owner_key_digest = hashlib.sha256()
    counts = Counter()
    physical = Counter()
    last_remainder_index = -1
    last_owner_source_index = -1

    def owner(payload, stream_index):
        nonlocal last_remainder_index, last_owner_source_index
        result = replay_sos_payload(
            payload, kernels, source_records, owner_seen,
            previous_remainder_index=last_remainder_index,
            previous_source_index=last_owner_source_index)
        source_index = result["source_index"]
        owner_seen.add(source_index)
        last_remainder_index = result["remainder_index"]
        last_owner_source_index = source_index
        owner_key_digest.update(f"{source_index}\n".encode("ascii"))
        counts[result["lane"]] += 1
        physical[result["lane"]] += result["orbit_size"]

    strict_xz_rows(SOS_OWNERS, report["owner_stream"], owner)
    require(dict(counts) == SOS_COUNTS and dict(physical) == SOS_PHYSICAL_COUNTS,
            "SOS owner counts changed")

    remainder_seen = set()
    remainder_records = {}
    last_remainder_source_index = -1
    def remainder(record, stream_index):
        nonlocal last_remainder_source_index
        source_index, _, _, _ = validate_source_record(
            record, kernels, f"SOS remainder[{stream_index}]")
        require(source_records.get(source_index) == record and
                source_index not in owner_seen and source_index not in remainder_seen and
                source_index > last_remainder_source_index,
                "SOS remainder does not match ordered unique structural source row")
        last_remainder_source_index = source_index
        remainder_seen.add(source_index)
        remainder_records[source_index] = record

    strict_xz_rows(SOS_REMAINDER, report["updated_remainder_stream"], remainder)
    key_sha256 = owner_key_digest.hexdigest()
    require(len(owner_seen) == sum(SOS_COUNTS.values()) and
            len(remainder_seen) == SOS_REMAINDER_TOTAL and
            owner_seen.isdisjoint(remainder_seen) and
            owner_seen | remainder_seen == set(source_records) and
            key_sha256 == EXPECTED_SOS_OWNER_KEY_SHA256,
            "SOS owner/remainder complement changed")
    return (report, owner_seen, remainder_records, counts, physical, key_sha256)


def replay_dominant_payload(payload, kernels, after_sos_records, owners,
                            maximum_denominator, *, previous_source_index=-1):
    """Pure exact replay of one dominant owner; ignore its diagnostic value."""
    require(isinstance(payload, list) and len(payload) == 4,
            "malformed dominant-family payload")
    record, certificate, diagnostic, stored_types = payload
    source_index, orbit_size, edges, row = validate_source_record(
        record, kernels, "dominant owner payload")
    require(after_sos_records.get(source_index) == record and
            source_index not in owners and source_index > previous_source_index,
            "dominant owner is not the exact ordered unique after-SOS source row")
    require(isinstance(certificate, list) and len(certificate) == 4 and
            certificate[0] == source_index and type(certificate[0]) is int and
            certificate[1] is True and
            type(diagnostic) in (int, float) and not isinstance(diagnostic, bool) and
            math.isfinite(diagnostic),
            "malformed dominant-family certificate")
    # The binary64 value is a diagnostic from the absent producer.  It is
    # schema-checked above but deliberately not read below or returned.
    require(family(edges, row) == DOMINANT_TARGET,
            "dominant owner family changed")
    signed, paths, type_keys, type_ids = matrix_and_paths(edges, row)
    expected_types = [[key[0], [list(value) for value in key[1]]]
                      for key in sorted(set(type_keys))]
    require(stored_types == expected_types,
            "dominant owner local types changed")
    raw_parameters = certificate[3]
    require(isinstance(raw_parameters, list) and
            len(raw_parameters) == max(type_ids) + 1,
            "dominant owner parameter count changed")
    parameters = []
    denominators = Counter()
    for index, values in enumerate(raw_parameters):
        require(isinstance(values, list) and len(values) == 2,
                "malformed dominant owner parameter")
        left = rational_pair(values[0], f"dominant parameter[{index}][0]",
                             maximum_denominator)
        right = rational_pair(values[1], f"dominant parameter[{index}][1]",
                              maximum_denominator)
        parameters.append((left, right))
        denominators.update((left.denominator, right.denominator))
    stored_cost = rational_pair(certificate[2], "dominant exact cost")
    cost, normalizer, completion = gram_cost(
        signed, paths, type_ids, tuple(parameters))
    require(cost is not None and cost == stored_cost and cost <= BUDGET,
            "dominant owner exact cost mismatch")
    return {
        "completion": completion, "cost": cost, "denominators": denominators,
        "normalizer": normalizer, "orbit_size": orbit_size,
        "source_index": source_index,
    }


def replay_dominant(kernels, sos_report, after_sos_records):
    # This legacy pinned report sorts its denominator histogram numerically,
    # not by JSON-name lexicographic order.  Its exact bytes and duplicate-key
    # safety are authenticated, but canonical row encoding is required only of
    # the owner stream itself.
    report = strict_file(DOMINANT_REPORT, EXPECTED_DOMINANT_REPORT_SHA256,
                         "dominant-family report", canonical=False)
    require(report.get("schema") == DOMINANT_SCHEMA and
            report.get("full_theorem") is False and
            report.get("source_report_sha256") == EXPECTED_SOS_REPORT_SHA256 and
            report.get("source_stream") == sos_report.get("updated_remainder_stream") and
            report.get("scanned_remainder_total") == SOS_REMAINDER_TOTAL and
            report.get("owned_orbit_total") == DOMINANT_TOTAL and
            report.get("owned_physical_total") == DOMINANT_PHYSICAL and
            report.get("owned_target_total") == DOMINANT_TOTAL * TARGETS_PER_ROW and
            report.get("gram", {}).get("maximum_denominator") == 256,
            "dominant-family report semantics changed")
    maximum_denominator = report["gram"]["maximum_denominator"]
    owners = set()
    owner_key_digest = hashlib.sha256()
    physical = 0
    denominators = Counter()
    last_source_index = -1

    def owner(payload, stream_index):
        nonlocal physical, last_source_index
        result = replay_dominant_payload(
            payload, kernels, after_sos_records, owners, maximum_denominator,
            previous_source_index=last_source_index)
        source_index = result["source_index"]
        owners.add(source_index)
        last_source_index = source_index
        owner_key_digest.update(f"{source_index}\n".encode("ascii"))
        physical += result["orbit_size"]
        denominators.update(result["denominators"])

    strict_xz_rows(DOMINANT_OWNERS, report["owner_stream"], owner,
                   parser=dominant_json)
    key_sha256 = owner_key_digest.hexdigest()
    require(len(owners) == DOMINANT_TOTAL and physical == DOMINANT_PHYSICAL and
            key_sha256 == EXPECTED_DOMINANT_OWNER_KEY_SHA256 and
            report.get("used_denominators") ==
            {str(key): value for key, value in sorted(denominators.items())},
            "dominant owner/report accounting changed")
    return report, owners, key_sha256


def replay():
    kernels = load_kernels()
    _, source_records = structural_source(kernels)
    (sos_report, sos_owners, after_sos, counts, physical,
     sos_owner_key_sha256) = replay_sos(kernels, source_records)
    (_, dominant_owners,
     dominant_owner_key_sha256) = replay_dominant(kernels, sos_report, after_sos)
    result = {
        "arithmetic": "fractions.Fraction",
        "combined_sos_dominant_physical": UPSTREAM_OWNER_PHYSICAL,
        "dominant_family": {
            "owner_key_sha256": dominant_owner_key_sha256,
            "owner_orbits": len(dominant_owners),
            "owner_physical": DOMINANT_PHYSICAL,
            "owner_targets": len(dominant_owners) * TARGETS_PER_ROW,
        },
        "read_only": True,
        "schema": REPLAY_SCHEMA,
        "sos": {
            "after_sos_orbits": len(after_sos),
            "exclusive_owner_orbits": dict(sorted(counts.items())),
            "exclusive_owner_physical": dict(sorted(physical.items())),
            "owner_key_sha256": sos_owner_key_sha256,
            "owner_orbits": len(sos_owners),
            "owner_physical": SOS_OWNER_PHYSICAL,
            "owner_targets": len(sos_owners) * TARGETS_PER_ROW,
            "structural_remainder_orbits": len(source_records),
        },
        "sos_owner_physical": SOS_OWNER_PHYSICAL,
        "status": "exact-upstream-owner-replay-passed",
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.parse_args()
    print(canonical_bytes(replay()).decode("ascii"), end="")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        sys.stderr.write(f"order-nine upstream owner replay: FAIL CLOSED: {error}\n")
        raise SystemExit(1)
