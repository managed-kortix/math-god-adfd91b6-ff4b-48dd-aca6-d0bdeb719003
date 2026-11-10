#!/usr/bin/env python3
"""Fail-closed global shared-packet lane for the post-XII order-eight remainder.

Generation runs numerical descent only to propose witnesses, then accepts each
owner solely by exact ``Fraction`` replay.  ``--audit`` is a separate read-only
path: it regenerates the complete rational-search census, authenticates every
six-field source row, replays every persisted packet exactly, and verifies that
the persisted remainder is the ordered byte-for-byte source complement.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import lzma
import math
import sys
import time
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ENGINE_PATH = HERE / "rank7_order8_exact_rational.py"
CACHE_PATH = HERE / "rank7_order8_rational_search_cache.r7o8c.xz"
SOURCE_REPORT = HERE / "rank7_order8_twelfth_induced_packet_gram_family.json"
SOURCE_STREAM = HERE / "rank7_order8_after_twelfth_induced_packet_gram_family_remainder.jsonl.xz"
OUTPUT = HERE / "rank7_order8_post_xii_shared_packet_lane.json"
OWNERS = HERE / "rank7_order8_post_xii_shared_packet_owners.jsonl.xz"
REMAINDER = HERE / "rank7_order8_after_post_xii_shared_packet_remainder.jsonl.xz"
SCHEMA = "rank-seven-order-eight-post-xii-global-shared-packet-lane-v1"
SOURCE_SCHEMA = "rank-seven-order-eight-twelfth-induced-packet-gram-family-v1"
SOURCE_TOTAL = 54598
TARGETS_PER_ROW = 15
DENOMINATORS = (256, 1024, 4096, 16384, 65536)
EXPECTED_REPORT_SHA256 = (
    "2d94c557a8a74845098d5ced351acb474e6f950ffb9072919db11e95e7b3cdb0"
)
EXPECTED_OWNER_ARTIFACT_SHA256 = (
    "9e50f7eb752f1a03eedf395550328c755216346badb5df77ae1b0fe03ef411e0"
)
EXPECTED_OWNER_RAW_SHA256 = (
    "8ae95c887177a0c4a3db346e063249518f876e16a06f11fcf07d1e0ea3b84e07"
)
EXPECTED_REMAINDER_ARTIFACT_SHA256 = (
    "bbadc801837908ada49cdb53a83fb1afa46a5a240a77ecb18c66fbb0a06a6340"
)
EXPECTED_REMAINDER_RAW_SHA256 = (
    "619ec23ae2435f06140ff94a98b56acc16571c71206fab132c71cdecc950229b"
)
EXPECTED_SOURCE_REPORT_SHA256 = (
    "dc4e868dae60db6b9504b2288f983ef1d98cbfa36245178e95f778fa277293c5"
)
EXPECTED_SOURCE_STREAM_SHA256 = (
    "de3fa584558684d6ffd8485b31707fc20f2fdb550d68c4a91116feda6b4464e6"
)
EXPECTED_SOURCE_STREAM_RAW_SHA256 = (
    "a6fb784238ae4d04b9e90d34939dc7658724684a9262eb7237f2197cc686c918"
)
EXPECTED_WORKERS = 2
EXPECTED_RESTARTS = 2
EXPECTED_ITERATIONS = 300
SCOPE = "complete authenticated post-XII order-eight remainder"
CLAIM_BOUNDARY = (
    "only persisted exact shared-packet accepts and their proved same-parity "
    "all-length/rooted-tree lifts are owned; the exact complement remains "
    "unresolved and no order-eight theorem is claimed"
)
CERTIFICATE_CONTRACT = {
    "kind": "full shared rational waypoint packet",
    "branch_psd": "eight exact rational stereographic unit vectors give G=XX^T",
    "path_psd": "every canonical and extended path is an explicit rational vector chain",
    "frontiers": "canonical plus each of fourteen one-coordinate length-plus-two targets",
    "all_length": "retain an accepted branch Gram and use fixed-parity optimized path-cost monotonicity",
    "rooted_trees": "attach each tree vertex as the negative of its parent vector, adding exact excess zero",
}
SEARCH_CONTRACT = {
    "kind": "unchanged shared rational waypoint packet search",
    "seed": 1729,
    "restarts": EXPECTED_RESTARTS,
    "iterations": EXPECTED_ITERATIONS,
    "workers": EXPECTED_WORKERS,
    "denominators": list(DENOMINATORS),
    "numerical_role": "proposal only",
    "exact_acceptance": "Fraction replay of one common branch Gram and all canonical/coordinate waypoint chains at cost at most six",
}
OWNER_FIELDS = {
    "global_kernel", "numerical_canonical_cost", "orbit_size", "source_index",
    "stream_index", "witness",
}
WITNESS_FIELDS = {"denominator", "branches", "canonical", "extended"}
_CONTEXT = None


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def exact_int(value, label, minimum=None):
    require(type(value) is int, f"{label} is not an exact integer")
    if minimum is not None:
        require(value >= minimum, f"{label} is below {minimum}")
    return value


def exact_string(value, label):
    require(type(value) is str and value, f"{label} is not a nonempty string")
    return value


def exact_mapping(value, label):
    require(type(value) is dict and all(type(key) is str for key in value),
            f"{label} is not a string-keyed object")
    return value


def exact_list(value, label):
    require(type(value) is list, f"{label} is not a list")
    return value


def strict_json(raw, label):
    def no_duplicate_pairs(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key in {label}: {key}")
            result[key] = value
        return result

    try:
        text = raw.decode("ascii")
        return json.loads(
            text,
            object_pairs_hook=no_duplicate_pairs,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError(f"non-finite JSON constant {value}")),
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(f"invalid JSON in {label}") from error


def strict_canonical(raw, label):
    payload = strict_json(raw, label)
    require(raw == canonical_bytes(payload), f"{label} is not canonical JSON")
    return payload


def load_engine():
    spec = importlib.util.spec_from_file_location("rank7_order8_post_xii_engine", ENGINE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load exact witness engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def integer_rows(rows, denominator):
    result = []
    for row in rows:
        require(all(denominator % value.denominator == 0 for value in row),
                "non-shared witness denominator")
        result.append([value.numerator * (denominator // value.denominator)
                       for value in row])
    return result


def encode_witness(witness):
    denominator, branches, canonical, extended = witness
    return {
        "denominator": denominator,
        "branches": integer_rows(branches, denominator),
        "canonical": [integer_rows(path, denominator) for path in canonical],
        "extended": [integer_rows(path, denominator) for path in extended],
    }


def authenticated_source_report():
    raw = SOURCE_REPORT.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_REPORT_SHA256,
            "pinned XII source report changed")
    report = strict_canonical(raw, SOURCE_REPORT.name)
    require(type(report) is dict and report.get("schema") == SOURCE_SCHEMA and
            report.get("full_theorem") is True and
            exact_int(report.get("remaining_remainder_total"),
                      "source report remaining_remainder_total", 0) == SOURCE_TOTAL,
            "XII source report is not the complete accepted closure")
    info = exact_mapping(report.get("reduced_remainder_stream"),
                         "source report reduced_remainder_stream")
    require(info == {
                "path": SOURCE_STREAM.name,
                "record_total": SOURCE_TOTAL,
                "raw_sha256": EXPECTED_SOURCE_STREAM_RAW_SHA256,
                "artifact_sha256": EXPECTED_SOURCE_STREAM_SHA256,
            } and
            file_sha256(SOURCE_STREAM) == EXPECTED_SOURCE_STREAM_SHA256,
            "pinned post-XII source stream identity changed")
    return raw, report, info


def validate_source_record(record, residuals, census, label):
    record = exact_list(record, label)
    require(len(record) == 6, f"{label} is not a six-field source row")
    stream_index = exact_int(record[0], f"{label}.stream_index", 0)
    require(stream_index < len(residuals), f"{label}.stream_index is out of range")
    source_index = exact_int(record[1], f"{label}.source_index", 0)
    global_kernel = exact_int(record[2], f"{label}.global_kernel", 0)
    edges_raw = exact_list(record[3], f"{label}.edges")
    row_raw = exact_list(record[4], f"{label}.row")
    orbit_size = exact_int(record[5], f"{label}.orbit_size", 1)

    edges = []
    for position, edge_raw in enumerate(edges_raw):
        edge = exact_list(edge_raw, f"{label}.edges[{position}]")
        require(len(edge) == 3, f"{label}.edges[{position}] is not a triple")
        u = exact_int(edge[0], f"{label}.edges[{position}][0]", 0)
        v = exact_int(edge[1], f"{label}.edges[{position}][1]", 0)
        multiplicity = exact_int(edge[2], f"{label}.edges[{position}][2]", 1)
        require(u < v < 8, f"{label}.edges[{position}] has invalid endpoints")
        edges.append((u, v, multiplicity))
    require(all(left < right for left, right in zip(edges, edges[1:])),
            f"{label}.edges are not strictly ordered")
    row = tuple(exact_int(value, f"{label}.row[{position}]", 0)
                for position, value in enumerate(row_raw))
    require(len(row) == len(edges) and
            all(odd <= edge[2] for edge, odd in zip(edges, row, strict=True)),
            f"{label}.row is not physical")

    pair_index = {edge: index for index, edge in enumerate(census.PAIRS)}
    support = tuple(pair_index[(u, v)] for u, v, _ in edges)
    rebuilt = (global_kernel, source_index, support,
               tuple(multiplicity for _, _, multiplicity in edges), row, orbit_size)
    residual = residuals[stream_index]
    require(residual[:6] == rebuilt and residual[6] is None and residual[7] is False,
            f"{label} differs from the authenticated residual census")
    return stream_index, residual


def read_source(residuals, census):
    _, _, info = authenticated_source_report()
    digest = hashlib.sha256()
    records = []
    seen = set()
    try:
        with lzma.open(SOURCE_STREAM, "rb") as stream:
            for position, raw in enumerate(stream):
                record = strict_canonical(raw, f"source row {position}")
                stream_index, residual = validate_source_record(
                    record, residuals, census, f"source row {position}")
                require(stream_index not in seen, "source stream index is duplicated")
                if records:
                    require(records[-1][0][0] < stream_index,
                            "source stream indices are not strictly increasing")
                seen.add(stream_index)
                digest.update(raw)
                records.append((record, raw, residual))
    except lzma.LZMAError as error:
        raise RuntimeError("post-XII source is not a valid XZ stream") from error
    require(len(records) == SOURCE_TOTAL and
            digest.hexdigest() == info.get("raw_sha256"),
            "post-XII source raw identity changed")
    return records


def fraction_rows(value, denominator, label):
    rows = []
    for row_index, row_raw in enumerate(exact_list(value, label)):
        row = exact_list(row_raw, f"{label}[{row_index}]")
        require(len(row) == 7, f"{label}[{row_index}] has wrong dimension")
        rows.append(tuple(Fraction(exact_int(item,
                                             f"{label}[{row_index}][{column}]") ,
                                   denominator)
                          for column, item in enumerate(row)))
    return tuple(rows)


def decode_witness(value, label):
    witness = exact_mapping(value, label)
    require(set(witness) == WITNESS_FIELDS, f"{label} fields changed")
    denominator = exact_int(witness.get("denominator"), f"{label}.denominator", 1)
    require(denominator in DENOMINATORS, f"{label}.denominator is not permitted")
    branches = fraction_rows(witness.get("branches"), denominator,
                             f"{label}.branches")
    canonical_raw = exact_list(witness.get("canonical"), f"{label}.canonical")
    extended_raw = exact_list(witness.get("extended"), f"{label}.extended")
    require(len(branches) == 8 and
            len(canonical_raw) == len(extended_raw) == 14,
            f"{label} packet dimensions changed")
    canonical = tuple(fraction_rows(path, denominator,
                                    f"{label}.canonical[{index}]")
                      for index, path in enumerate(canonical_raw))
    extended = tuple(fraction_rows(path, denominator,
                                   f"{label}.extended[{index}]")
                     for index, path in enumerate(extended_raw))
    return denominator, branches, canonical, extended


def worker(record):
    engine, census, residuals, restarts, iterations = _CONTEXT

    class Arguments:
        symbolic_fast_lane = False
        seed = 1729
        fallback_restarts = 0
        fallback_iterations = 0

    Arguments.restarts = restarts
    Arguments.iterations = iterations
    stream_index = record[0]
    result, numerical, shared, _ = engine.base.search_record(
        Arguments, census, residuals[stream_index], stream_index, DENOMINATORS)
    if result[0] != engine.base.MODE_SHARED or shared is None:
        return stream_index, numerical, None
    engine.base.verify_shared(census, residuals[stream_index], shared)
    return stream_index, numerical, encode_witness(shared)


def scan(workers, restarts, iterations, progress=False):
    global _CONTEXT
    started = time.perf_counter()
    source_report_raw, _, source_info = authenticated_source_report()
    engine = load_engine()
    census = engine.load_census_module()
    residuals = engine.residual_rows(census, cache_path=CACHE_PATH)
    records = read_source(residuals, census)
    source_load_seconds = time.perf_counter() - started
    _CONTEXT = engine, census, residuals, restarts, iterations

    if workers == 1:
        results = map(worker, (record for record, _, _ in records))
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=workers)
        results = executor.map(worker, (record for record, _, _ in records), chunksize=8)

    scan_started = time.perf_counter()
    owners = []
    owner_indices = set()
    classification = hashlib.sha256()
    denominator_histogram = {}
    for position, ((record, _, _), result) in enumerate(
            zip(records, results, strict=True), 1):
        stream_index, numerical, witness = result
        require(stream_index == record[0], "worker result escaped source order")
        accepted = witness is not None
        classification.update(canonical_bytes([stream_index, record[1], accepted]))
        if accepted:
            require(type(numerical) is float and math.isfinite(numerical),
                    "accepted numerical provenance is malformed")
            require(stream_index not in owner_indices, "generated owner is duplicated")
            owner_indices.add(stream_index)
            denominator = witness["denominator"]
            denominator_histogram[str(denominator)] = (
                denominator_histogram.get(str(denominator), 0) + 1)
            owners.append({
                "stream_index": stream_index,
                "source_index": record[1],
                "global_kernel": record[2],
                "orbit_size": record[5],
                "numerical_canonical_cost": numerical,
                "witness": witness,
            })
        if progress and position % 1000 == 0:
            print(f"rows={position}/{len(records)} owned={len(owners)}", flush=True)
    if executor is not None:
        executor.shutdown()
    scan_seconds = time.perf_counter() - scan_started

    owner_raw_digest = hashlib.sha256()
    owner_tmp = OWNERS.with_name(OWNERS.name + ".tmp")
    with lzma.open(owner_tmp, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
        for owner in owners:
            raw = canonical_bytes(owner)
            output.write(raw)
            owner_raw_digest.update(raw)
    owner_tmp.replace(OWNERS)

    remainder_raw_digest = hashlib.sha256()
    remainder_total = remainder_physical = 0
    remainder_tmp = REMAINDER.with_name(REMAINDER.name + ".tmp")
    with lzma.open(remainder_tmp, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
        for record, raw, _ in records:
            if record[0] not in owner_indices:
                output.write(raw)
                remainder_raw_digest.update(raw)
                remainder_total += 1
                remainder_physical += record[5]
    remainder_tmp.replace(REMAINDER)

    owner_physical = sum(owner["orbit_size"] for owner in owners)
    source_physical = sum(record[0][5] for record in records)
    require(len(owners) + remainder_total == SOURCE_TOTAL and
            owner_physical + remainder_physical == source_physical,
            "generated owner/remainder partition is incomplete")

    report = {
        "schema": SCHEMA,
        "full_theorem": False,
        "scan_complete": True,
        "scope": SCOPE,
        "source_report": {
            "path": SOURCE_REPORT.name,
            "sha256": hashlib.sha256(source_report_raw).hexdigest(),
        },
        "source_stream": source_info,
        "source_orbit_total": SOURCE_TOTAL,
        "source_physical_total": source_physical,
        "targets_per_row": TARGETS_PER_ROW,
        "search": SEARCH_CONTRACT,
        "certificate": CERTIFICATE_CONTRACT,
        "owned_orbit_total": len(owners),
        "owned_physical_total": owner_physical,
        "owned_target_total": len(owners) * TARGETS_PER_ROW,
        "remaining_orbit_total": remainder_total,
        "remaining_physical_total": remainder_physical,
        "remaining_target_total": remainder_total * TARGETS_PER_ROW,
        "partition_identity": f"{SOURCE_TOTAL} = {len(owners)} + {remainder_total}",
        "classification_stream_sha256": classification.hexdigest(),
        "accepted_denominator_histogram": dict(sorted(denominator_histogram.items(),
                                                       key=lambda item: int(item[0]))),
        "owner_stream": {
            "path": OWNERS.name,
            "record_total": len(owners),
            "raw_sha256": owner_raw_digest.hexdigest(),
            "artifact_sha256": file_sha256(OWNERS),
        },
        "reduced_remainder_stream": {
            "path": REMAINDER.name,
            "record_total": remainder_total,
            "raw_sha256": remainder_raw_digest.hexdigest(),
            "artifact_sha256": file_sha256(REMAINDER),
        },
        "generation_runtime": {
            "source_load_seconds": source_load_seconds,
            "search_seconds": scan_seconds,
            "total_seconds": time.perf_counter() - started,
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    raw = canonical_bytes(report)
    output_tmp = OUTPUT.with_name(OUTPUT.name + ".tmp")
    output_tmp.write_bytes(raw)
    output_tmp.replace(OUTPUT)
    return report, raw


def audit(*, hostile=False):
    started = time.perf_counter()
    report_raw = OUTPUT.read_bytes()
    require(hashlib.sha256(report_raw).hexdigest() == EXPECTED_REPORT_SHA256,
            "pinned post-XII report changed")
    report = strict_canonical(report_raw, OUTPUT.name)
    require(type(report) is dict and set(report) == {
        "accepted_denominator_histogram", "certificate", "claim_boundary",
        "classification_stream_sha256", "full_theorem", "generation_runtime",
        "owned_orbit_total", "owned_physical_total", "owned_target_total",
        "owner_stream", "partition_identity", "reduced_remainder_stream",
        "remaining_orbit_total", "remaining_physical_total", "remaining_target_total",
        "scan_complete", "schema", "scope", "search", "source_orbit_total",
        "source_physical_total", "source_report", "source_stream", "targets_per_row",
    }, "report fields changed")
    require(report.get("schema") == SCHEMA and report.get("full_theorem") is False and
            report.get("scan_complete") is True and
            report.get("scope") == SCOPE and
            report.get("claim_boundary") == CLAIM_BOUNDARY and
            report.get("certificate") == CERTIFICATE_CONTRACT and
            report.get("search") == SEARCH_CONTRACT and
            exact_int(report.get("source_orbit_total"),
                      "source_orbit_total", 0) == SOURCE_TOTAL and
            exact_int(report.get("targets_per_row"),
                      "targets_per_row", 1) == TARGETS_PER_ROW,
            "report scope, search, certificate, or claim boundary changed")
    runtime = exact_mapping(report.get("generation_runtime"), "generation_runtime")
    require(set(runtime) == {"source_load_seconds", "search_seconds", "total_seconds"} and
            all(type(value) is float and math.isfinite(value) and value >= 0
                for value in runtime.values()),
            "generation runtime provenance is malformed")

    source_report_raw, _, source_info = authenticated_source_report()
    source_report_link = exact_mapping(report.get("source_report"), "source_report")
    require(source_report_link == {
        "path": SOURCE_REPORT.name,
        "sha256": hashlib.sha256(source_report_raw).hexdigest(),
    } and report.get("source_stream") == source_info,
            "report is not pinned to the authenticated XII source")

    engine = load_engine()
    census = engine.load_census_module()
    # Deliberately regenerate from source chunks; audit never trusts the convenience cache.
    residuals = engine.materialize_residuals(census)
    records = read_source(residuals, census)
    source_by_index = {record[0][0]: record for record in records}
    require(len(source_by_index) == SOURCE_TOTAL,
            "authenticated source indices are not unique")

    owner_info = exact_mapping(report.get("owner_stream"), "owner_stream")
    require(owner_info == {
                "path": OWNERS.name,
                "record_total": 54597,
                "raw_sha256": EXPECTED_OWNER_RAW_SHA256,
                "artifact_sha256": EXPECTED_OWNER_ARTIFACT_SHA256,
            } and file_sha256(OWNERS) == EXPECTED_OWNER_ARTIFACT_SHA256,
            "pinned owner artifact identity changed")
    owner_expected = exact_int(owner_info.get("record_total"),
                               "owner_stream.record_total", 0)
    owner_digest = hashlib.sha256()
    owner_indices = []
    owner_physical = 0
    denominator_histogram = {}
    previous = -1
    try:
        with lzma.open(OWNERS, "rb") as stream:
            for position, raw in enumerate(stream):
                owner = strict_canonical(raw, f"owner row {position}")
                owner = exact_mapping(owner, f"owner row {position}")
                require(set(owner) == OWNER_FIELDS,
                        f"owner row {position} fields changed")
                stream_index = exact_int(owner.get("stream_index"),
                                         f"owner row {position}.stream_index", 0)
                require(stream_index > previous and stream_index in source_by_index,
                        "owners are not unique and in strict source order")
                previous = stream_index
                source_record, _, residual = source_by_index[stream_index]
                require(exact_int(owner.get("source_index"),
                                  f"owner row {position}.source_index", 0) ==
                        source_record[1] and
                        exact_int(owner.get("global_kernel"),
                                  f"owner row {position}.global_kernel", 0) ==
                        source_record[2] and
                        exact_int(owner.get("orbit_size"),
                                  f"owner row {position}.orbit_size", 1) ==
                        source_record[5],
                        "owner metadata differs from its six-field source row")
                numerical = owner.get("numerical_canonical_cost")
                require(type(numerical) is float and math.isfinite(numerical),
                        "owner numerical provenance is malformed")
                witness = decode_witness(owner.get("witness"),
                                         f"owner row {position}.witness")
                engine.base.verify_shared(census, residual, witness)
                denominator_histogram[str(witness[0])] = (
                    denominator_histogram.get(str(witness[0]), 0) + 1)
                owner_digest.update(raw)
                owner_indices.append(stream_index)
                owner_physical += source_record[5]
    except lzma.LZMAError as error:
        raise RuntimeError("owner stream is not a valid XZ stream") from error
    require(len(owner_indices) == owner_expected and
            owner_digest.hexdigest() == owner_info.get("raw_sha256"),
            "owner raw stream identity changed")

    owner_set = set(owner_indices)
    remainder_info = exact_mapping(report.get("reduced_remainder_stream"),
                                   "reduced_remainder_stream")
    require(remainder_info == {
                "path": REMAINDER.name,
                "record_total": 1,
                "raw_sha256": EXPECTED_REMAINDER_RAW_SHA256,
                "artifact_sha256": EXPECTED_REMAINDER_ARTIFACT_SHA256,
            } and file_sha256(REMAINDER) == EXPECTED_REMAINDER_ARTIFACT_SHA256,
            "pinned remainder artifact identity changed")
    remainder_expected = exact_int(remainder_info.get("record_total"),
                                   "remainder_stream.record_total", 0)
    remainder_digest = hashlib.sha256()
    remainder_total = remainder_physical = 0
    expected = ((record, raw) for record, raw, _ in records
                if record[0] not in owner_set)
    try:
        with lzma.open(REMAINDER, "rb") as stream:
            for position, ((expected_record, expected_raw), actual_raw) in enumerate(
                    zip(expected, stream, strict=True)):
                actual_record = strict_canonical(actual_raw, f"remainder row {position}")
                validate_source_record(actual_record, residuals, census,
                                       f"remainder row {position}")
                require(actual_raw == expected_raw and actual_record == expected_record,
                        "remainder is not the ordered byte-for-byte source complement")
                remainder_digest.update(actual_raw)
                remainder_total += 1
                remainder_physical += actual_record[5]
    except lzma.LZMAError as error:
        raise RuntimeError("remainder stream is not a valid XZ stream") from error
    require(remainder_total == remainder_expected and
            remainder_digest.hexdigest() == remainder_info.get("raw_sha256"),
            "remainder raw stream identity changed")

    classification = hashlib.sha256()
    for record, _, _ in records:
        classification.update(canonical_bytes(
            [record[0], record[1], record[0] in owner_set]))
    source_physical = sum(record[0][5] for record in records)
    require(len(owner_indices) + remainder_total == SOURCE_TOTAL and
            owner_physical + remainder_physical == source_physical and
            report.get("source_physical_total") == source_physical and
            report.get("owned_orbit_total") == len(owner_indices) and
            report.get("owned_physical_total") == owner_physical and
            report.get("owned_target_total") == TARGETS_PER_ROW * len(owner_indices) and
            report.get("remaining_orbit_total") == remainder_total and
            report.get("remaining_physical_total") == remainder_physical and
            report.get("remaining_target_total") == TARGETS_PER_ROW * remainder_total and
            report.get("partition_identity") ==
            f"{SOURCE_TOTAL} = {len(owner_indices)} + {remainder_total}" and
            report.get("classification_stream_sha256") == classification.hexdigest() and
            report.get("accepted_denominator_histogram") ==
            dict(sorted(denominator_histogram.items(), key=lambda item: int(item[0]))),
            "report counts, partition, or classification digest changed")
    for field in (
            "source_physical_total", "owned_orbit_total", "owned_physical_total",
            "owned_target_total", "remaining_orbit_total", "remaining_physical_total",
            "remaining_target_total"):
        exact_int(report.get(field), field, 0)
    require(report_raw == OUTPUT.read_bytes(),
            "read-only audit changed the report")

    hostile_rejections = 0
    if hostile:
        import copy

        def rejected(action, label):
            nonlocal hostile_rejections
            try:
                action()
            except (RuntimeError, ZeroDivisionError, ValueError):
                hostile_rejections += 1
                return
            raise RuntimeError(f"hostile mutation accepted: {label}")

        with lzma.open(OWNERS, "rb") as stream:
            first_owner = strict_canonical(next(stream), "first hostile owner")
        real_witness = first_owner["witness"]
        hostile_mutations = []
        changed = copy.deepcopy(real_witness)
        changed["denominator"] = 0
        hostile_mutations.append((changed, "zero denominator"))
        changed = copy.deepcopy(real_witness)
        changed["branches"][0] = changed["branches"][0][:-1]
        hostile_mutations.append((changed, "short branch vector"))
        changed = copy.deepcopy(real_witness)
        changed["canonical"] = changed["canonical"][:-1]
        hostile_mutations.append((changed, "short canonical packet list"))
        changed = copy.deepcopy(real_witness)
        changed["extended"][0] = changed["extended"][0][:-1]
        hostile_mutations.append((changed, "wrong extended path width"))
        changed = copy.deepcopy(real_witness)
        changed["extra"] = 1
        hostile_mutations.append((changed, "extra witness field"))
        changed = copy.deepcopy(real_witness)
        changed["branches"][0][0] = True
        hostile_mutations.append((changed, "boolean numerator"))
        for changed, label in hostile_mutations:
            rejected(lambda changed=changed, label=label:
                     engine.base.verify_shared(
                         census, residuals[first_owner["stream_index"]],
                         decode_witness(changed, label)), label)

        first_source = records[0][0]
        changed = copy.deepcopy(first_source)
        changed[0] = True
        rejected(lambda: validate_source_record(changed, residuals, census,
                                                "boolean stream index"),
                 "boolean source stream index")
        changed = copy.deepcopy(first_source)
        changed[5] += 1
        rejected(lambda: validate_source_record(changed, residuals, census,
                                                "changed orbit size"),
                 "changed source orbit size")
        changed = copy.deepcopy(first_source)
        changed[3][0][2] += 1
        rejected(lambda: validate_source_record(changed, residuals, census,
                                                "changed multiplicity"),
                 "changed source multiplicity")
        rejected(lambda: strict_canonical(b'{"a":1,"a":2}\n', "duplicate key"),
                 "duplicate JSON key")
        rejected(lambda: strict_canonical(json.dumps(report, indent=2).encode("ascii"),
                                          "pretty report"),
                 "noncanonical JSON")
        require(report_raw == OUTPUT.read_bytes(),
                "hostile read-only audit changed the report")

    return {
        "hostile_mutations_rejected": hostile_rejections,
        "audit_seconds": time.perf_counter() - started,
        "owned": len(owner_indices),
        "remaining": remainder_total,
        "report_sha256": hashlib.sha256(report_raw).hexdigest(),
        "owner_artifact_sha256": file_sha256(OWNERS),
        "remainder_artifact_sha256": file_sha256(REMAINDER),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=EXPECTED_WORKERS)
    parser.add_argument("--restarts", type=int, default=EXPECTED_RESTARTS)
    parser.add_argument("--iterations", type=int, default=EXPECTED_ITERATIONS)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--hostile", action="store_true")
    args = parser.parse_args()
    require((args.workers, args.restarts, args.iterations) ==
            (EXPECTED_WORKERS, EXPECTED_RESTARTS, EXPECTED_ITERATIONS),
            "generation parameters differ from the frozen search contract")
    require(not args.hostile or args.audit,
            "--hostile is available only on the read-only --audit path")
    if args.audit:
        result = audit(hostile=args.hostile)
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return
    report, raw = scan(args.workers, args.restarts, args.iterations, args.progress)
    print(f"scanned={report['source_orbit_total']} owned={report['owned_orbit_total']} "
          f"remaining={report['remaining_orbit_total']}")
    print(f"report_sha256={hashlib.sha256(raw).hexdigest()}")
    print(f"owner_artifact_sha256={report['owner_stream']['artifact_sha256']}")
    print(f"remainder_artifact_sha256={report['reduced_remainder_stream']['artifact_sha256']}")
    print(f"generation_seconds={report['generation_runtime']['total_seconds']:.6f}")


if __name__ == "__main__":
    main()
