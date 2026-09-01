#!/usr/bin/env python3
"""Exact cached defect-transport Gram scan of the next order-eleven family."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANE_PATH = HERE / "rank7_order11_defect_transport_gram_lane.py"
SOURCE_REPORT = HERE / "rank7_order11_defect_transport_gram_lane.json"
SOURCE_STREAM = HERE / "rank7_order11_after_defect_transport_remainder.jsonl.xz"
PRIOR_SEGMENTS = HERE / "rank7_order11_defect_transport_gram_scan"
PRIOR_SEGMENT_DIRECTORIES = (PRIOR_SEGMENTS,)
EXPECTED_CACHE_SEED_ROWS = 319522
OUTPUT = HERE / "rank7_order11_next_family_defect_transport_gram_lane.json"
OWNERS = HERE / "rank7_order11_next_family_defect_transport_gram_owners.jsonl.xz"
FAILURES = HERE / "rank7_order11_next_family_defect_transport_gram_failures.jsonl.xz"
REMAINDER = HERE / "rank7_order11_after_next_family_defect_transport_remainder.jsonl.xz"
SEGMENTS = HERE / "rank7_order11_next_family_defect_transport_gram_scan"
SCHEMA = "rank-seven-order-eleven-next-family-defect-transport-gram-lane-v1"
SCOPE = "full exact cached defect-transport/cycle Gram replay of the next-largest order-eleven remainder family"
PARAMETER_CACHE_DESCRIPTION = "accepted rational parameters keyed by exact local-type signature, seeded from the complete leading-family scan"
TARGET = ((2,) + (1,) * 15, (6, 1, 9), 6, 1)
EXPECTED_SOURCE_TOTAL = 11075112
EXPECTED_TARGET_TOTAL = 300610
F = Fraction


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LANE = load("order11_next_defect_transport", LANE_PATH)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return LANE.canonical_bytes(payload)


def pair(value):
    return [value.numerator, value.denominator]


def signature(type_keys):
    return json.dumps(
        [[key[0], pair(key[1]), [list(value) for value in key[2]]]
         for key in sorted(set(type_keys))],
        sort_keys=True, separators=(",", ":"))


def family_payload():
    return LANE.family_payload(TARGET)


def segment_path(directory, start, stop):
    return directory / f"rows-{start:06d}-{stop:06d}.json.xz"


def read_segments(directory, identity):
    rows = []
    cursor = 0
    for path in sorted(directory.glob("rows-*.json.xz")):
        with lzma.open(path, "rb") as source:
            raw = source.read()
        payload = json.loads(raw.decode("ascii"))
        require(raw == canonical_bytes(payload), f"noncanonical segment: {path.name}")
        require(payload.get("schema") == SCHEMA + "-segment-v1" and
                payload.get("identity") == identity and
                payload.get("row_range") == [cursor, cursor + len(payload.get("rows", []))],
                f"invalid or noncontiguous segment: {path.name}")
        rows.extend(payload["rows"])
        cursor += len(payload["rows"])
    return rows


def write_segment(directory, start, rows, identity):
    stop = start + len(rows)
    payload = {"schema": SCHEMA + "-segment-v1", "identity": identity,
               "row_range": [start, stop], "rows": rows}
    path = segment_path(directory, start, stop)
    temporary = path.with_name(path.name + ".tmp")
    with lzma.open(temporary, "wb", format=lzma.FORMAT_XZ, preset=3) as output:
        output.write(canonical_bytes(payload))
    temporary.replace(path)


def kernel_dictionary():
    manifest, _ = LANE.strict_json(LANE.MANIFEST_PATH)
    wrapper = LANE.load("order11_next_owner", LANE.OWNER_ENGINE_PATH)
    owner = wrapper.load_owner_engine()
    kernels = {}
    for chunk in manifest["chunks"]:
        header, _, _ = owner.stream_chunk(LANE.MANIFEST_PATH.parent / chunk["path"])
        for row in header["kernels"]:
            kernel = LANE.kernel_data(row)
            prior = kernels.get(row["order_kernel"])
            require(prior is None or prior["edges"] == kernel["edges"],
                    "order-kernel collision")
            kernels[row["order_kernel"]] = kernel
    return kernels


def collect_source():
    source_report, source_report_sha256 = LANE.strict_json(SOURCE_REPORT)
    source_info = source_report["updated_remainder_stream"]
    require(source_info["path"] == SOURCE_STREAM.name and
            source_info["artifact_sha256"] == LANE.file_sha256(SOURCE_STREAM) and
            source_info["record_total"] == EXPECTED_SOURCE_TOTAL,
            "leading-family remainder authentication changed")
    kernels = kernel_dictionary()
    targets = []
    digest = hashlib.sha256()
    scanned = physical = target_physical = 0
    with lzma.open(SOURCE_STREAM, "rb") as source:
        for raw in source:
            record = json.loads(raw.decode("ascii"))
            require(raw == canonical_bytes(record) and len(record) == 5,
                    "noncanonical source remainder row")
            digest.update(raw)
            scanned += 1
            physical += record[4]
            kernel = kernels[record[2]]
            if LANE.row_family(kernel, tuple(record[3])) == TARGET:
                targets.append((record, kernel))
                target_physical += record[4]
    require(scanned == source_info["record_total"] and
            physical == source_info["physical_total"] and
            digest.hexdigest() == source_info["raw_sha256"],
            "source remainder stream changed")
    require(len(targets) == EXPECTED_TARGET_TOTAL, "next-largest family total changed")
    return source_report_sha256, source_info, targets, target_physical


def load_parameter_cache(completed):
    cache = {}
    prior_rows = 0
    for directory in PRIOR_SEGMENT_DIRECTORIES:
        for path in sorted(directory.glob("rows-*.json.xz")):
            with lzma.open(path, "rb") as source:
                payload = json.load(source)
            for row in payload["rows"]:
                prior_rows += 1
                if row[1][1]:
                    encoded = [row[1][4], row[1][5]]
                    bucket = cache.setdefault(row[2], [])
                    if encoded not in bucket:
                        bucket.append(encoded)
    for row in completed:
        if row[1][1]:
            encoded = [row[1][4], row[1][5]]
            bucket = cache.setdefault(row[2], [])
            if encoded not in bucket:
                bucket.append(encoded)
    require(prior_rows == EXPECTED_CACHE_SEED_ROWS,
            "prior-family parameter cache is incomplete")
    return cache, prior_rows


def exact_replay(kernel, row, parameters, cycle_weight):
    signed, paths, type_keys, type_ids, family = LANE.paths_types_family(kernel, row)
    if len(parameters) != max(type_ids) + 1:
        return None
    cost, normalizer = LANE.exact_cost(
        signed, LANE.transport_core(paths), paths, type_ids, parameters, cycle_weight)
    return cost, normalizer, type_keys, family


def scan(max_denominator, checkpoint_rows, directory, progress):
    require(max_denominator > 0 and checkpoint_rows > 0, "invalid scan bounds")
    source_report_sha256, source_info, targets, target_physical = collect_source()
    identity = {"source_report_sha256": source_report_sha256,
                "target_family": family_payload(),
                "max_denominator": max_denominator}
    directory.mkdir(parents=True, exist_ok=True)
    completed = read_segments(directory, identity)
    require(len(completed) <= len(targets), "segments exceed target family")
    cache, seeded_rows = load_parameter_cache(completed)

    pending = []
    cache_hits = optimized = 0
    for position in range(len(completed), len(targets)):
        record, kernel = targets[position]
        row = tuple(record[3])
        _, _, type_keys, _, family = LANE.paths_types_family(kernel, row)
        require(family == TARGET, "target family changed")
        local_signature = signature(type_keys)
        result = None
        for encoded in cache.get(local_signature, ()):
            parameters = tuple((F(*left), F(*right)) for left, right in encoded[0])
            cycle_weight = F(*encoded[1])
            replay = exact_replay(kernel, row, parameters, cycle_weight)
            if replay is not None and replay[0] is not None and replay[0] <= LANE.BUDGET:
                cost, normalizer, keys, result_family = replay
                result = cost, normalizer, parameters, cycle_weight, keys, result_family
                cache_hits += 1
                break
        if result is None:
            result = LANE.search(kernel, row, max_denominator)
            optimized += 1
        cost, normalizer, parameters, cycle_weight, keys, result_family = result
        require(result_family == TARGET, "search family changed")
        accepted = cost is not None and cost <= LANE.BUDGET
        certificate = [record[0], accepted, None if cost is None else pair(cost),
                       pair(normalizer),
                       [[pair(left), pair(right)] for left, right in parameters],
                       pair(cycle_weight)]
        if accepted:
            encoded = [certificate[4], certificate[5]]
            bucket = cache.setdefault(local_signature, [])
            if encoded not in bucket:
                bucket.append(encoded)
        pending.append([record, certificate, local_signature,
                        json.loads(signature(keys))])
        if len(pending) == checkpoint_rows or position + 1 == len(targets):
            write_segment(directory, position + 1 - len(pending), pending, identity)
            completed.extend(pending)
            pending = []
            if progress:
                print(f"target={position + 1}/{len(targets)} "
                      f"owned={sum(row[1][1] for row in completed)} "
                      f"cache_hits={cache_hits} optimized={optimized}", flush=True)

    classification = hashlib.sha256()
    owner_raw = hashlib.sha256()
    failure_raw = hashlib.sha256()
    owner_indices = set()
    owner_physical = failure_physical = 0
    owner_tmp = OWNERS.with_name(OWNERS.name + ".tmp")
    failure_tmp = FAILURES.with_name(FAILURES.name + ".tmp")
    with lzma.open(owner_tmp, "wb", format=lzma.FORMAT_XZ, preset=6) as owner_out, \
            lzma.open(failure_tmp, "wb", format=lzma.FORMAT_XZ, preset=6) as failure_out:
        for record, certificate, _, type_keys in completed:
            classification.update(canonical_bytes(certificate))
            raw = canonical_bytes([record, certificate, type_keys, family_payload()])
            if certificate[1]:
                owner_indices.add(record[0])
                owner_physical += record[4]
                owner_out.write(raw)
                owner_raw.update(raw)
            else:
                failure_physical += record[4]
                failure_out.write(raw)
                failure_raw.update(raw)
    owner_tmp.replace(OWNERS)
    failure_tmp.replace(FAILURES)

    remainder_raw = hashlib.sha256()
    remainder_total = remainder_physical = 0
    remainder_tmp = REMAINDER.with_name(REMAINDER.name + ".tmp")
    with lzma.open(SOURCE_STREAM, "rb") as source, \
            lzma.open(remainder_tmp, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
        for raw in source:
            record = json.loads(raw.decode("ascii"))
            if record[0] in owner_indices:
                continue
            output.write(raw)
            remainder_raw.update(raw)
            remainder_total += 1
            remainder_physical += record[4]
    remainder_tmp.replace(REMAINDER)
    require(remainder_total + len(owner_indices) == source_info["record_total"] and
            remainder_physical + owner_physical == source_info["physical_total"],
            "owner/remainder partition changed")

    report = {
        "schema": SCHEMA, "full_theorem": False,
        "scope": SCOPE,
        "source_report_sha256": source_report_sha256,
        "source_stream": source_info,
        "target_family": {**family_payload(), "orbit_total": len(targets),
                          "physical_total": target_physical},
        "gram": {
            "formula": "H=XX^T+w A P_cycle A^T; G=H/M+diag(1-diag(H)/M)",
            "local_type": "(degree defect,signed degree,sorted incident bundles)",
            "parameter_cache": PARAMETER_CACHE_DESCRIPTION,
            "exact_acceptance": "fresh Fraction projector, Gram, correlation, and path-cost replay on every row, including cache hits; no family extrapolation",
            "maximum_denominator": max_denominator,
        },
        "execution": {"checkpoint_rows": checkpoint_rows,
                      "segment_directory": directory.name,
                      "segment_total": len(list(directory.glob("rows-*.json.xz"))),
                      "cache_seed_row_total": seeded_rows,
                      "cache_signature_total": len(cache)},
        "owned_orbit_total": len(owner_indices),
        "owned_physical_total": owner_physical,
        "owned_target_total": len(owner_indices) * LANE.TARGETS_PER_ROW,
        "remaining_target_family_total": len(targets) - len(owner_indices),
        "remaining_remainder_orbit_total": remainder_total,
        "remaining_remainder_physical_total": remainder_physical,
        "classification_stream_sha256": classification.hexdigest(),
        "owner_stream": {"path": OWNERS.name, "record_total": len(owner_indices),
                         "physical_total": owner_physical,
                         "raw_sha256": owner_raw.hexdigest(),
                         "artifact_sha256": LANE.file_sha256(OWNERS)},
        "failure_stream": {"path": FAILURES.name,
                           "record_total": len(targets) - len(owner_indices),
                           "physical_total": failure_physical,
                           "raw_sha256": failure_raw.hexdigest(),
                           "artifact_sha256": LANE.file_sha256(FAILURES)},
        "updated_remainder_stream": {"path": REMAINDER.name,
                                     "record_total": remainder_total,
                                     "physical_total": remainder_physical,
                                     "raw_sha256": remainder_raw.hexdigest(),
                                     "artifact_sha256": LANE.file_sha256(REMAINDER)},
        "claim_boundary": "only exact accepted owner-stream rows are owned; rejected target rows and all non-target source rows remain persisted",
    }
    OUTPUT.write_bytes(canonical_bytes(report))
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-denominator", type=int, default=128)
    parser.add_argument("--checkpoint-rows", type=int, default=1000)
    parser.add_argument("--segment-directory", type=Path, default=SEGMENTS)
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    report = scan(args.max_denominator, args.checkpoint_rows,
                  args.segment_directory, args.progress)
    print(f"target={report['target_family']['orbit_total']} "
          f"owned={report['owned_orbit_total']} "
          f"remaining={report['remaining_remainder_orbit_total']}")
    print(f"sha256={LANE.file_sha256(OUTPUT)}")


if __name__ == "__main__":
    main()
