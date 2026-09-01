#!/usr/bin/env python3
"""Resumable exact scan of the leading order-eleven defect-transport family."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import lzma
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANE_PATH = HERE / "rank7_order11_defect_transport_gram_lane.py"
OUTPUT = HERE / "rank7_order11_defect_transport_gram_lane.json"
OWNERS = HERE / "rank7_order11_defect_transport_gram_owners.jsonl.xz"
FAILURES = HERE / "rank7_order11_defect_transport_gram_failures.jsonl.xz"
REMAINDER = HERE / "rank7_order11_after_defect_transport_remainder.jsonl.xz"
SEGMENTS = HERE / "rank7_order11_defect_transport_gram_scan"
SCHEMA = "rank-seven-order-eleven-defect-transport-full-family-scan-v1"
TARGET = ((2,) + (1,) * 15, (6, 1, 9), 6, 2)
EXPECTED_TARGET_TOTAL = 319522
F = Fraction


def load_lane():
    spec = importlib.util.spec_from_file_location("order11_defect_transport_lane", LANE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load defect-transport lane")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LANE = load_lane()
_COLLECT_CONTEXT = None


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return LANE.canonical_bytes(payload)


def pair(value):
    return [value.numerator, value.denominator]


def file_sha256(path):
    return LANE.file_sha256(path)


def signature(type_keys):
    return json.dumps(
        [[key[0], pair(key[1]), [list(value) for value in key[2]]]
         for key in sorted(set(type_keys))],
        sort_keys=True, separators=(",", ":"))


def decode(certificate):
    parameters = tuple((F(*left), F(*right)) for left, right in certificate[4])
    return parameters, F(*certificate[5])


def exact_replay(kernel, row, parameters, cycle_weight):
    signed, paths, type_keys, type_ids, family = LANE.paths_types_family(kernel, row)
    require(len(parameters) == max(type_ids) + 1, "parameter/type arity changed")
    cost, normalizer = LANE.exact_cost(
        signed, LANE.transport_core(paths), paths, type_ids, parameters, cycle_weight)
    return cost, normalizer, type_keys, family


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


def collect_chunk(path):
    owner = _COLLECT_CONTEXT
    header, records, finish = owner.stream_chunk(path)
    kernels = {row["order_kernel"]: LANE.kernel_data(row) for row in header["kernels"]}
    targets = []
    digest = hashlib.sha256()
    coarse_total = 0
    for record in records:
        digest.update(canonical_bytes(record))
        kernel = kernels[record["order_kernel"]]
        row = tuple(record["row"])
        source_index = coarse_total
        coarse_total += 1
        if LANE.row_family(kernel, row) != TARGET:
            continue
        packed = [source_index, record["global_kernel"], record["order_kernel"],
                  record["row"], record["orbit_size"]]
        targets.append((packed, kernel))
    finish()
    require(digest.hexdigest() == header["residual_stream_sha256"],
            f"census residual digest changed: {path.name}")
    require(coarse_total == header["coarse_residual_total"],
            f"coarse row total changed: {path.name}")
    return targets, coarse_total


def collect_source(workers):
    global _COLLECT_CONTEXT
    manifest, manifest_sha256 = LANE.strict_json(LANE.MANIFEST_PATH)
    wrapper = LANE.load("order11_defect_full_owner", LANE.OWNER_ENGINE_PATH)
    owner = wrapper.load_owner_engine()
    _COLLECT_CONTEXT = owner
    paths = [LANE.MANIFEST_PATH.parent / row["path"] for row in manifest["chunks"]]
    if workers == 1:
        chunks = map(collect_chunk, paths)
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=min(workers, len(paths)))
        chunks = executor.map(collect_chunk, paths)
    targets = []
    coarse_offset = 0
    for chunk_targets, chunk_coarse_total in chunks:
        for record, kernel in chunk_targets:
            record[0] += coarse_offset
            targets.append((record, kernel))
        coarse_offset += chunk_coarse_total
    if executor is not None:
        executor.shutdown()
    require(len(targets) == EXPECTED_TARGET_TOTAL, "leading family total changed")
    return (manifest, manifest_sha256, owner, targets,
            manifest["remainder_orbit_total"], manifest["remainder_physical_total"])


def scan(max_denominator, checkpoint_rows, directory, progress, workers):
    require(max_denominator > 0 and checkpoint_rows > 0, "invalid scan bounds")
    (manifest, manifest_sha256, owner, targets,
     source_total, source_physical) = collect_source(workers)
    identity = {"source_manifest_sha256": manifest_sha256,
                "target_family": LANE.family_payload(TARGET),
                "max_denominator": max_denominator}
    directory.mkdir(parents=True, exist_ok=True)
    completed = read_segments(directory, identity)
    require(len(completed) <= len(targets), "segments exceed target family")

    cache = {}
    for payload in completed:
        if payload[1][1]:
            encoded = [payload[1][4], payload[1][5]]
            bucket = cache.setdefault(payload[2], [])
            if encoded not in bucket:
                bucket.append(encoded)
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
            cost, normalizer, keys, result_family = exact_replay(
                kernel, row, parameters, cycle_weight)
            if cost is not None and cost <= LANE.BUDGET:
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
    owner_indices = set()
    owner_physical = 0
    temporary = OWNERS.with_name(OWNERS.name + ".tmp")
    with lzma.open(temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
        for record, certificate, _, type_keys in completed:
            classification.update(canonical_bytes(certificate))
            if not certificate[1]:
                continue
            owner_indices.add(record[0])
            owner_physical += record[4]
            raw = canonical_bytes([record, certificate, type_keys,
                                   LANE.family_payload(TARGET)])
            output.write(raw)
            owner_raw.update(raw)
    temporary.replace(OWNERS)

    failure_raw = hashlib.sha256()
    failure_total = failure_physical = 0
    temporary = FAILURES.with_name(FAILURES.name + ".tmp")
    with lzma.open(temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
        for record, certificate, _, type_keys in completed:
            if certificate[1]:
                continue
            raw = canonical_bytes([record, certificate, type_keys,
                                   LANE.family_payload(TARGET)])
            output.write(raw)
            failure_raw.update(raw)
            failure_total += 1
            failure_physical += record[4]
    temporary.replace(FAILURES)

    remainder_raw = hashlib.sha256()
    remainder_total = remainder_physical = 0
    temporary = REMAINDER.with_name(REMAINDER.name + ".tmp")
    with lzma.open(temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
        for record, _ in LANE.stream_rows(manifest, owner, exclude_owned=True):
            if record[0] in owner_indices:
                continue
            raw = canonical_bytes(record)
            output.write(raw)
            remainder_raw.update(raw)
            remainder_total += 1
            remainder_physical += record[4]
    temporary.replace(REMAINDER)
    require(remainder_total + len(owner_indices) == source_total and
            remainder_physical + owner_physical == source_physical,
            "owner/remainder partition changed")

    target_physical = sum(record[4] for record, _ in targets)
    report = {
        "schema": SCHEMA, "full_theorem": False,
        "scope": "full exact Fraction replay of the leading order-eleven defect-transport family",
        "source_manifest_sha256": manifest_sha256,
        "source_remainder_orbit_total": source_total,
        "source_remainder_physical_total": source_physical,
        "target_family": {**LANE.family_payload(TARGET),
                          "orbit_total": len(targets),
                          "physical_total": target_physical},
        "gram": {
            "formula": "H=XX^T+w A P_cycle A^T; G=H/M+diag(1-diag(H)/M)",
            "local_type": "(degree defect,signed degree,sorted incident bundles)",
            "parameter_cache": "accepted rational parameters keyed by exact local-type signature",
            "exact_acceptance": "fresh Fraction projector, Gram, correlation, and path-cost replay on every row, including cache hits; no family extrapolation",
            "maximum_denominator": max_denominator,
        },
        "execution": {"checkpoint_rows": checkpoint_rows,
                       "segment_directory": directory.name,
                       "segment_total": len(list(directory.glob("rows-*.json.xz"))),
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
                          "artifact_sha256": file_sha256(OWNERS)},
        "failure_stream": {"path": FAILURES.name, "record_total": failure_total,
                           "physical_total": failure_physical,
                           "raw_sha256": failure_raw.hexdigest(),
                           "artifact_sha256": file_sha256(FAILURES)},
        "updated_remainder_stream": {
            "path": REMAINDER.name, "record_total": remainder_total,
            "physical_total": remainder_physical,
            "raw_sha256": remainder_raw.hexdigest(),
            "artifact_sha256": file_sha256(REMAINDER)},
        "claim_boundary": "only exact accepted owner-stream rows are owned; rejected target rows and all non-target source rows remain persisted",
    }
    OUTPUT.write_bytes(canonical_bytes(report))
    return report


def audit(directory, workers):
    report, report_sha256 = LANE.strict_json(OUTPUT)
    require(report.get("schema") == SCHEMA and report.get("full_theorem") is False,
            "wrong report schema or theorem boundary")
    (manifest, manifest_sha256, owner, targets,
     source_total, source_physical) = collect_source(workers)
    require(report["source_manifest_sha256"] == manifest_sha256 and
            report["source_remainder_orbit_total"] == source_total and
            report["source_remainder_physical_total"] == source_physical,
            "report source changed")
    identity = {"source_manifest_sha256": manifest_sha256,
                "target_family": LANE.family_payload(TARGET),
                "max_denominator": report["gram"]["maximum_denominator"]}
    completed = read_segments(directory, identity)
    require(len(completed) == EXPECTED_TARGET_TOTAL == len(targets),
            "full target scan is incomplete")

    classification = hashlib.sha256()
    owner_raw = hashlib.sha256()
    failure_raw = hashlib.sha256()
    owner_indices = set()
    owner_physical = failure_physical = 0
    with lzma.open(OWNERS, "rb") as owner_stream, lzma.open(FAILURES, "rb") as failure_stream:
        for position, ((record, certificate, local_signature, type_keys),
                       (expected_record, kernel)) in enumerate(zip(completed, targets, strict=True)):
            require(record == expected_record and certificate[0] == record[0],
                    f"source/segment disagreement at target {position}")
            row = tuple(record[3])
            _, _, expected_keys, _, family = LANE.paths_types_family(kernel, row)
            require(family == TARGET and local_signature == signature(expected_keys) and
                    type_keys == json.loads(signature(expected_keys)),
                    f"type/family disagreement at target {position}")
            parameters, cycle_weight = decode(certificate)
            cost, normalizer, replay_keys, replay_family = exact_replay(
                kernel, row, parameters, cycle_weight)
            accepted = cost is not None and cost <= LANE.BUDGET
            require(replay_family == TARGET and signature(replay_keys) == local_signature and
                    certificate[1] == accepted and
                    certificate[2] == (None if cost is None else pair(cost)) and
                    certificate[3] == pair(normalizer),
                    f"exact certificate replay failed at target {position}")
            classification.update(canonical_bytes(certificate))
            payload = canonical_bytes([record, certificate, type_keys,
                                       LANE.family_payload(TARGET)])
            stream = owner_stream if accepted else failure_stream
            require(stream.readline() == payload,
                    f"persisted {'owner' if accepted else 'failure'} stream changed")
            (owner_raw if accepted else failure_raw).update(payload)
            if accepted:
                owner_indices.add(record[0])
                owner_physical += record[4]
            else:
                failure_physical += record[4]
        require(owner_stream.read(1) == b"" and failure_stream.read(1) == b"",
                "owner or failure stream has trailing records")

    require(classification.hexdigest() == report["classification_stream_sha256"],
            "classification digest changed")
    for path, digest, count, physical, key in (
            (OWNERS, owner_raw, len(owner_indices), owner_physical, "owner_stream"),
            (FAILURES, failure_raw, len(targets) - len(owner_indices), failure_physical,
             "failure_stream")):
        info = report[key]
        require(info == {"path": path.name, "record_total": count,
                         "physical_total": physical, "raw_sha256": digest.hexdigest(),
                         "artifact_sha256": file_sha256(path)},
                f"{key} aggregate changed")

    remainder_raw = hashlib.sha256()
    remainder_total = remainder_physical = 0
    with lzma.open(REMAINDER, "rb") as remainder_stream:
        for record, _ in LANE.stream_rows(manifest, owner, exclude_owned=True):
            if record[0] in owner_indices:
                continue
            raw = canonical_bytes(record)
            require(remainder_stream.readline() == raw,
                    f"persisted remainder changed at source row {record[0]}")
            remainder_raw.update(raw)
            remainder_total += 1
            remainder_physical += record[4]
        require(remainder_stream.read(1) == b"", "remainder stream has trailing records")
    remainder_info = report["updated_remainder_stream"]
    require(remainder_info == {
        "path": REMAINDER.name, "record_total": remainder_total,
        "physical_total": remainder_physical, "raw_sha256": remainder_raw.hexdigest(),
        "artifact_sha256": file_sha256(REMAINDER)},
        "updated remainder aggregate changed")
    require(remainder_total + len(owner_indices) == source_total and
            remainder_physical + owner_physical == source_physical,
            "audited owner/remainder partition changed")
    return report, report_sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-denominator", type=int, default=128)
    parser.add_argument("--checkpoint-rows", type=int, default=1000)
    parser.add_argument("--segment-directory", type=Path, default=SEGMENTS)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    require(args.workers > 0, "worker total must be positive")
    if args.audit:
        report, digest = audit(args.segment_directory, args.workers)
        print(f"audited={report['target_family']['orbit_total']} "
              f"owned={report['owned_orbit_total']} "
              f"failures={report['failure_stream']['record_total']} "
              f"remaining={report['remaining_remainder_orbit_total']}")
        print(f"sha256={digest}")
        return
    report = scan(args.max_denominator, args.checkpoint_rows,
                  args.segment_directory, args.progress, args.workers)
    print(f"target={report['target_family']['orbit_total']} "
          f"owned={report['owned_orbit_total']} "
          f"remaining={report['remaining_remainder_orbit_total']}")
    print(f"sha256={file_sha256(OUTPUT)}")


if __name__ == "__main__":
    main()
