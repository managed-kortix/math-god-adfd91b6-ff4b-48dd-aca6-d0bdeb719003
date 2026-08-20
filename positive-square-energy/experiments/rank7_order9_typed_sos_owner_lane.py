#!/usr/bin/env python3
"""Persist the exact scalar/typed SOS union and its order-nine remainder."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import lzma
import os
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
STRATIFIER_PATH = HERE / "rank7_order9_unowned_stratifier.py"
GRAM_PATH = HERE / "rank7_order9_remainder_gram_lanes.py"
OWNER_MANIFEST_PATH = HERE / "rank7_order9_structural_owner_manifest.json"
SCALAR_REPORT_PATH = HERE / "rank7_order9_remainder_gram_lanes.json"
OUTPUT_PATH = HERE / "rank7_order9_typed_sos_owner_manifest.json"
OWNER_STREAM_PATH = HERE / "rank7_order9_typed_sos_owners.jsonl.xz"
REMAINDER_STREAM_PATH = HERE / "rank7_order9_after_sos_remainder.jsonl.xz"
SCHEMA = "rank-seven-order-nine-typed-diagonal-sos-owner-lane-v1"
F = Fraction
_CONTEXT = None


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def pair(value):
    return [value.numerator, value.denominator]


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def strict_json_line(raw, label):
    try:
        payload = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot parse {label}") from error
    require(raw == canonical_bytes(payload), f"noncanonical {label}")
    return payload


def audit_stream(path, expected_total, expected_raw_sha256, expected_artifact_sha256,
                 validator):
    require(file_sha256(path) == expected_artifact_sha256,
            f"artifact digest changed: {path.name}")
    digest = hashlib.sha256()
    total = 0
    try:
        with lzma.open(path, "rb") as rows:
            for raw in rows:
                record = strict_json_line(raw, path.name)
                validator(record, total)
                digest.update(raw)
                total += 1
    except lzma.LZMAError as error:
        raise RuntimeError(f"cannot decompress {path.name}") from error
    require(total == expected_total and digest.hexdigest() == expected_raw_sha256,
            f"stream authentication failed: {path.name}")
    return total


def typed_search(gram, signed, paths, type_ids, candidates, passes, initial):
    matrix = np.asarray(signed, dtype=np.float64)
    endpoints = np.asarray([(row[2], row[3]) for row in paths], dtype=np.int64)
    lengths = np.asarray([row[4] for row in paths], dtype=np.int64)
    type_count = max(type_ids) + 1
    selected = [(F(1), initial)] * type_count
    ids = np.asarray(type_ids)
    eye = np.eye(gram.ORDER)
    values0 = np.asarray([float(value[0]) for value in candidates])
    values1 = np.asarray([float(value[1]) for value in candidates])
    for _ in range(passes):
        changed = False
        for kind in range(type_count):
            diagonal0 = np.broadcast_to(
                np.asarray([float(value[0]) for value in selected]),
                (len(candidates), type_count)).copy()
            diagonal1 = np.broadcast_to(
                np.asarray([float(value[1]) for value in selected]),
                (len(candidates), type_count)).copy()
            diagonal0[:, kind] = values0
            diagonal1[:, kind] = values1
            vertex0 = diagonal0[:, ids]
            vertex1 = diagonal1[:, ids]
            x = eye[None, :, :] * vertex0[:, :, None] + vertex1[:, :, None] * matrix[None, :, :]
            square = x @ np.swapaxes(x, 1, 2)
            normalizer = np.max(np.diagonal(square, axis1=1, axis2=2), axis=1)
            correlations = square[:, endpoints[:, 0], endpoints[:, 1]] / normalizer[:, None]
            correlations[:, (lengths & 1) == 1] *= -1
            with np.errstate(divide="ignore", invalid="ignore"):
                costs = np.sum((1.0 - correlations) /
                               (lengths[None, :] * (1.0 + correlations)), axis=1)
            costs[np.any(correlations <= -1.0, axis=1)] = np.inf
            best = int(np.argmin(costs))
            if selected[kind] != candidates[best]:
                selected[kind] = candidates[best]
                changed = True
        if not changed:
            break
    parameters = tuple(selected)
    return gram.typed_cost(signed, paths, type_ids, parameters), parameters


def worker(record):
    gram, kernels, scalar_candidates, typed_candidates, typed_passes = _CONTEXT
    source_index, global_kernel, order_kernel, raw_row, _ = record
    expected_global, edges = kernels[order_kernel]
    require(global_kernel == expected_global, "remainder kernel changed")
    signed, paths, type_keys, type_ids = gram.matrix_and_paths(edges, tuple(raw_row))
    numerical = gram.numerical_scalar_costs(signed, paths, scalar_candidates)
    coefficient = scalar_candidates[int(np.nanargmin(numerical))]
    scalar_cost = gram.scalar_cost(signed, paths, coefficient)
    scalar_owner = scalar_cost is not None and scalar_cost <= gram.BUDGET
    if scalar_owner:
        return coefficient, scalar_cost, None, None, type_keys
    typed_cost, parameters = typed_search(
        gram, signed, paths, type_ids, typed_candidates, typed_passes, coefficient)
    return coefficient, scalar_cost, typed_cost, parameters, type_keys


def dominant_family(stratifier, edges, row):
    support, parity, graph = stratifier.graph_data(edges, row, 9)
    return {
        "multiplicity_partition": support["multiplicity_partition"],
        "bundle_types": parity["bundle_types"],
        "cycle_rank": graph["cycle_rank"],
        "triangle_total": graph["triangle_total"],
    }


def write_stream(path, rows):
    raw_digest = hashlib.sha256()
    count = 0
    temporary = path.with_name(path.name + ".tmp")
    with lzma.open(temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
        for row in rows:
            raw = canonical_bytes(row)
            output.write(raw)
            raw_digest.update(raw)
            count += 1
    temporary.replace(path)
    return count, raw_digest.hexdigest(), file_sha256(path)


def scan(workers, typed_max_denominator, typed_maximum, typed_passes, progress):
    global _CONTEXT
    stratifier = load("rank7_order9_typed_owner_stratifier", STRATIFIER_PATH)
    gram = load("rank7_order9_typed_owner_gram", GRAM_PATH)
    owner_manifest, owner_manifest_sha256 = stratifier.strict_canonical_json(
        OWNER_MANIFEST_PATH, "structural owner manifest")
    scalar_report, scalar_report_sha256 = stratifier.strict_canonical_json(
        SCALAR_REPORT_PATH, "scalar SOS report")
    require(scalar_report["owner_manifest_sha256"] == owner_manifest_sha256,
            "scalar report references a different owner manifest")
    kernels = stratifier.kernel_dictionary(stratifier.load_scan_engine())
    scalar_candidates = gram.rationals(16, 4)
    typed_ratios = gram.rationals(typed_max_denominator, typed_maximum)
    typed_scales = (F(1, 2), F(2, 3), F(1), F(3, 2), F(2))
    typed_candidates = tuple((scale, scale * ratio)
                             for scale in typed_scales for ratio in typed_ratios)
    _CONTEXT = gram, kernels, scalar_candidates, typed_candidates, typed_passes

    records = stratifier.remainder_records(OWNER_MANIFEST_PATH, owner_manifest)
    if workers == 1:
        results = map(worker, records)
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=workers)
        results = executor.map(worker, records, chunksize=128)

    scalar_digest = hashlib.sha256()
    union_digest = hashlib.sha256()
    family_counts = Counter()
    family_descriptions = {}
    scalar_total = typed_additional_total = scanned = 0
    owner_temp = OWNER_STREAM_PATH.with_name(OWNER_STREAM_PATH.name + ".tmp")
    remainder_temp = REMAINDER_STREAM_PATH.with_name(REMAINDER_STREAM_PATH.name + ".tmp")
    owner_raw = hashlib.sha256()
    remainder_raw = hashlib.sha256()
    first_typed_owner = None
    with lzma.open(owner_temp, "wb", format=lzma.FORMAT_XZ, preset=6) as owner_output, \
            lzma.open(remainder_temp, "wb", format=lzma.FORMAT_XZ, preset=6) as remainder_output:
        source_records = stratifier.remainder_records(OWNER_MANIFEST_PATH, owner_manifest)
        for remainder_index, (record, result) in enumerate(zip(source_records, results, strict=True)):
            source_index, global_kernel, order_kernel, raw_row, orbit_size = record
            coefficient, scalar_cost, typed_cost, parameters, type_keys = result
            scalar_owner = scalar_cost is not None and scalar_cost <= gram.BUDGET
            typed_owner = (not scalar_owner and typed_cost is not None and
                           typed_cost <= gram.BUDGET)
            scalar_total += scalar_owner
            typed_additional_total += typed_owner
            scalar_digest.update(canonical_bytes(
                [source_index, scalar_owner, pair(coefficient),
                 None if scalar_cost is None else pair(scalar_cost)]))
            classification = [
                remainder_index, source_index,
                "scalar-sos" if scalar_owner else ("typed-sos" if typed_owner else None),
                pair(coefficient), None if scalar_cost is None else pair(scalar_cost),
                None if parameters is None else
                [[pair(left), pair(right)] for left, right in parameters],
                None if typed_cost is None else pair(typed_cost),
            ]
            union_digest.update(canonical_bytes(classification))
            if scalar_owner or typed_owner:
                owner_record = [record, classification]
                raw = canonical_bytes(owner_record)
                owner_output.write(raw)
                owner_raw.update(raw)
                if typed_owner and first_typed_owner is None:
                    first_typed_owner = {
                        "remainder_index": remainder_index,
                        "source_index": source_index,
                        "global_kernel": global_kernel,
                        "cost": pair(typed_cost),
                        "parameters": [[pair(left), pair(right)]
                                       for left, right in parameters],
                        "local_types": [[key[0], [list(value) for value in key[1]]]
                                        for key in sorted(set(type_keys))],
                    }
            else:
                raw = canonical_bytes(record)
                remainder_output.write(raw)
                remainder_raw.update(raw)
                edges = kernels[order_kernel][1]
                family = dominant_family(stratifier, edges, tuple(raw_row))
                key = hashlib.sha256(canonical_bytes(family)).hexdigest()[:20]
                family_counts[key] += 1
                family_descriptions[key] = family
            scanned += 1
            if progress and scanned % 25000 == 0:
                print(f"rows={scanned} scalar={scalar_total} typed_additional={typed_additional_total}",
                      flush=True)
    if executor is not None:
        executor.shutdown()
    owner_temp.replace(OWNER_STREAM_PATH)
    remainder_temp.replace(REMAINDER_STREAM_PATH)

    require(scanned == owner_manifest["remainder_orbit_total"], "incomplete SOS scan")
    scalar_lane = scalar_report["scalar_lane"]
    require(scalar_total == scalar_lane["covered_remainder_total"] and
            scalar_digest.hexdigest() == scalar_lane["classification_stream_sha256"],
            "scalar lane did not reproduce")
    remaining = scanned - scalar_total - typed_additional_total
    ranked_families = sorted(family_counts, key=lambda key: (-family_counts[key], key))
    report = {
        "schema": SCHEMA,
        "full_theorem": remaining == 0,
        "scope": "exact finite scalar/typed SOS owner union on the authenticated structural remainder",
        "owner_manifest_sha256": owner_manifest_sha256,
        "scalar_report_sha256": scalar_report_sha256,
        "source_remainder_stream_sha256": owner_manifest["remainder_stream_sha256"],
        "precedence": ["scalar-sos", "typed-sos"],
        "formula": {
            **scalar_report["formula"],
            "typed": "G=(D0+D1*S)(D0+D1*S)^T/M+diag(1-diag((D0+D1*S)(D0+D1*S)^T)/M)",
        },
        "exact_psd_audit": {
            "factorization": "G=XX^T/M+diag(1-diag(XX^T)/M)",
            "normalizer_checked_positive": True,
            "diagonal_completion_checked_nonnegative": True,
            "correlations_checked_in_closed_unit_interval": True,
            "arithmetic": "fractions.Fraction",
        },
        "typed_search": {
            "type_key": "(signed degree, sorted incident (multiplicity,odd-count) pairs)",
            "feature_matrix": "X=D0+D1*S, with D0,D1 constant on exact local types",
            "ratio_maximum_denominator": typed_max_denominator,
            "ratio_range": [pair(typed_ratios[0]), pair(typed_ratios[-1])],
            "ratio_distinct_total": len(typed_ratios),
            "d0_scales": [pair(value) for value in typed_scales],
            "parameter_pair_total": len(typed_candidates),
            "coordinate_passes": typed_passes,
            "initialization": "the exact scalar-grid proposal for the same row",
            "audit": "binary64 coordinate descent proposes one grid tuple; acceptance is replayed with Fraction",
        },
        "scanned_remainder_total": scanned,
        "exclusive_owner_counts": {
            "scalar-sos": scalar_total,
            "typed-sos": typed_additional_total,
        },
        "owned_total": scalar_total + typed_additional_total,
        "owned_target_total": (scalar_total + typed_additional_total) * 16,
        "remaining_total": remaining,
        "remaining_target_total": remaining * 16,
        "partition_identity": f"{scanned} = {scalar_total} + {typed_additional_total} + {remaining}",
        "classification_stream_sha256": union_digest.hexdigest(),
        "first_typed_owner": first_typed_owner,
        "owner_stream": {
            "path": OWNER_STREAM_PATH.name,
            "record_total": scalar_total + typed_additional_total,
            "raw_sha256": owner_raw.hexdigest(),
            "artifact_sha256": file_sha256(OWNER_STREAM_PATH),
        },
        "updated_remainder_stream": {
            "path": REMAINDER_STREAM_PATH.name,
            "record_total": remaining,
            "raw_sha256": remainder_raw.hexdigest(),
            "artifact_sha256": file_sha256(REMAINDER_STREAM_PATH),
        },
        "dominant_updated_remainder_families": [
            {"id": f"f-{key}", "orbit_total": family_counts[key],
             "signature": family_descriptions[key]}
            for key in ranked_families[:20]
        ],
        "claim_boundary": "only rows accepted by exact replay of these finite grids are owned; the updated remainder is unclassified by this lane",
    }
    return report


def audit(output_path):
    stratifier = load("rank7_order9_typed_owner_audit_stratifier", STRATIFIER_PATH)
    gram = load("rank7_order9_typed_owner_audit_gram", GRAM_PATH)
    report, report_sha256 = stratifier.strict_canonical_json(output_path, "typed SOS report")
    owner_manifest, owner_manifest_sha256 = stratifier.strict_canonical_json(
        OWNER_MANIFEST_PATH, "structural owner manifest")
    scalar_report, scalar_report_sha256 = stratifier.strict_canonical_json(
        SCALAR_REPORT_PATH, "scalar SOS report")
    require(report["schema"] == SCHEMA and
            report["owner_manifest_sha256"] == owner_manifest_sha256 and
            report["scalar_report_sha256"] == scalar_report_sha256 and
            report["source_remainder_stream_sha256"] ==
            owner_manifest["remainder_stream_sha256"], "report input authentication changed")
    owner_counts = Counter()
    owner_source_indices = set()

    def validate_owner(record, stream_index):
        require(isinstance(record, list) and len(record) == 2 and
                isinstance(record[0], list) and len(record[0]) == 5 and
                isinstance(record[1], list) and len(record[1]) == 7,
                "malformed owner record")
        source, classification = record
        require(classification[1] == source[0] and
                classification[2] in ("scalar-sos", "typed-sos") and
                source[0] not in owner_source_indices, "owner record identity changed")
        owner_source_indices.add(source[0])
        owner_counts[classification[2]] += 1
        cost = classification[4] if classification[2] == "scalar-sos" else classification[6]
        require(cost is not None and F(*cost) <= gram.BUDGET,
                "owner stream contains a cost above budget")

    owner_info = report["owner_stream"]
    audit_stream(output_path.parent / owner_info["path"], owner_info["record_total"],
                 owner_info["raw_sha256"], owner_info["artifact_sha256"], validate_owner)

    remainder_sources = set()

    def validate_remainder(record, stream_index):
        require(isinstance(record, list) and len(record) == 5 and
                record[0] not in owner_source_indices and
                record[0] not in remainder_sources, "malformed or overlapping remainder record")
        remainder_sources.add(record[0])

    remainder_info = report["updated_remainder_stream"]
    audit_stream(output_path.parent / remainder_info["path"],
                 remainder_info["record_total"], remainder_info["raw_sha256"],
                 remainder_info["artifact_sha256"], validate_remainder)
    expected_counts = report["exclusive_owner_counts"]
    require(dict(owner_counts) == expected_counts and
            len(owner_source_indices) == report["owned_total"] and
            len(remainder_sources) == report["remaining_total"] and
            len(owner_source_indices | remainder_sources) == report["scanned_remainder_total"] ==
            owner_manifest["remainder_orbit_total"], "owner/remainder partition changed")
    return {"report_sha256": report_sha256, "owned_total": report["owned_total"],
            "remaining_total": report["remaining_total"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=max(1, min(8, os.cpu_count() or 1)))
    parser.add_argument("--typed-max-denominator", type=int, default=4)
    parser.add_argument("--typed-maximum", type=int, default=2)
    parser.add_argument("--typed-passes", type=int, default=3)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    require(args.workers > 0 and args.typed_max_denominator > 0 and
            args.typed_maximum > 0 and args.typed_passes > 0, "invalid search bounds")
    require(args.output.parent.is_dir(), "output parent does not exist")
    if args.audit:
        print(json.dumps(audit(args.output), sort_keys=True))
        return
    report = scan(args.workers, args.typed_max_denominator, args.typed_maximum,
                  args.typed_passes, args.progress)
    raw = canonical_bytes(report)
    args.output.write_bytes(raw)
    print(report["partition_identity"])
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
