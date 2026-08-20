#!/usr/bin/env python3
"""Promote high-ownership weighted-cycle signatures by full exact replay."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import lzma
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
WEIGHTED_PATH = HERE / "rank7_order10_weighted_cycle_gram_lane.py"
WEIGHTED_SPEC = importlib.util.spec_from_file_location(
    "rank7_order10_family_weighted", WEIGHTED_PATH)
if WEIGHTED_SPEC is None or WEIGHTED_SPEC.loader is None:
    raise RuntimeError("cannot load weighted-cycle lane")
weighted = importlib.util.module_from_spec(WEIGHTED_SPEC)
WEIGHTED_SPEC.loader.exec_module(weighted)
SOURCE_REPORT = HERE / "rank7_order10_weighted_cycle_gram_lane.json"
SOURCE_OWNERS = HERE / "rank7_order10_weighted_cycle_gram_owners.jsonl.xz"
OUTPUT = HERE / "rank7_order10_weighted_cycle_family_scan.json"
OWNERS = HERE / "rank7_order10_weighted_cycle_family_owners.jsonl.xz"
REMAINDER = HERE / "rank7_order10_after_weighted_cycle_remainder.jsonl.xz"
SCHEMA = "rank-seven-order-ten-weighted-cycle-family-scan-v1"
F = Fraction
_CONTEXT = None


def strict_json(path):
    raw = path.read_bytes()
    payload = json.loads(raw.decode("ascii"))
    weighted.require(raw == weighted.canonical_bytes(payload),
                     f"noncanonical JSON: {path.name}")
    return payload, hashlib.sha256(raw).hexdigest()


def encoded_signature(source, kernel, row):
    return json.dumps(weighted.coarse_signature(source, kernel, row),
                      sort_keys=True, separators=(",", ":"))


def sample_stratification(source, kernels, manifest, source_report):
    sample_size = source_report["sampling"]["tested"]
    owner_indices = set()
    owner_digest = hashlib.sha256()
    owner_count = 0
    with lzma.open(SOURCE_OWNERS, "rb") as rows:
        for raw in rows:
            payload = json.loads(raw.decode("ascii"))
            weighted.require(raw == weighted.canonical_bytes(payload),
                             "noncanonical source owner row")
            owner_digest.update(raw)
            owner_indices.add(payload[0][0])
            owner_count += 1
    owner_info = source_report["owner_stream"]
    weighted.require(
        owner_count == owner_info["record_total"] and
        owner_digest.hexdigest() == owner_info["raw_sha256"] and
        weighted.file_sha256(SOURCE_OWNERS) == owner_info["artifact_sha256"],
        "source owner stream authentication failed")

    counts = Counter()
    owned = Counter()
    descriptions = {}
    for index, record in enumerate(source.remainder_records(manifest)):
        if index >= sample_size:
            break
        kernel = kernels[record[2]]
        key = encoded_signature(source, kernel, tuple(record[3]))
        counts[key] += 1
        owned[key] += record[0] in owner_indices
        descriptions.setdefault(key, json.loads(key))
    weighted.require(sum(counts.values()) == sample_size, "sample ended early")
    weighted.require(sum(owned.values()) == owner_info["record_total"],
                     "sample owner count changed")

    ranked = sorted(counts, key=lambda key: (-owned[key] / counts[key],
                                             -owned[key], -counts[key], key))
    strata = [{"signature": descriptions[key], "tested": counts[key],
               "owned": owned[key], "failed": counts[key] - owned[key],
               "coverage": weighted.pair(F(owned[key], counts[key]))}
              for key in ranked]
    selected = {key for key in counts if owned[key] and owned[key] == counts[key]}
    return strata, selected, owner_indices


def worker(record):
    projector, kernels = _CONTEXT
    source_index, global_kernel, order_kernel, raw_row, orbit_size = record
    kernel = kernels[order_kernel]
    weighted.require(global_kernel == kernel["global_kernel"],
                     "kernel reference changed")
    cost, parameters, normalizer = weighted.search(
        projector, kernel, tuple(raw_row))
    return source_index, orbit_size, cost, parameters, normalizer


def scan(workers=1, progress=False):
    global _CONTEXT
    source = weighted.load("rank7_order10_family_source", weighted.SOURCE)
    projector = weighted.load("rank7_order10_family_projector", weighted.PROJECTOR)
    manifest, manifest_sha256 = source.strict_json(source.MANIFEST)
    source_report, source_report_sha256 = strict_json(SOURCE_REPORT)
    weighted.require(source_report["owner_manifest_sha256"] == manifest_sha256,
                     "source report uses a different remainder")
    kernels = source.kernel_dictionary()
    strata, selected, prior_owner_indices = sample_stratification(
        source, kernels, manifest, source_report)

    targets = []
    target_counts = Counter()
    target_physical = Counter()
    scanned = physical = 0
    source_digest = hashlib.sha256()
    for record in source.remainder_records(manifest):
        kernel = kernels[record[2]]
        key = encoded_signature(source, kernel, tuple(record[3]))
        if key in selected:
            targets.append(record)
            target_counts[key] += 1
            target_physical[key] += record[4]
        source_digest.update(weighted.canonical_bytes(record))
        scanned += 1
        physical += record[4]
        if progress and scanned % 1000000 == 0:
            print(f"stratified={scanned} targets={len(targets)}", flush=True)
    weighted.require(
        (scanned, physical, source_digest.hexdigest()) ==
        (manifest["remainder_orbit_total"], manifest["remainder_physical_total"],
         manifest["remainder_stream_sha256"]),
        "full source remainder authentication failed")

    _CONTEXT = projector, kernels
    if workers == 1:
        results = map(worker, targets)
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=workers)
        results = executor.map(worker, targets, chunksize=16)

    family_results = {}
    classification = hashlib.sha256()
    exact_counts = Counter()
    exact_physical = Counter()
    profile_counts = Counter()
    minimum = None
    for index, (record, result) in enumerate(zip(targets, results, strict=True)):
        source_index, orbit_size, cost, parameters, normalizer = result
        accepted = cost <= weighted.BUDGET
        certificate = [source_index, accepted, weighted.pair(cost),
                       [weighted.pair(value) for value in parameters[:3]] +
                       [parameters[3]], weighted.pair(normalizer)]
        classification.update(weighted.canonical_bytes(certificate))
        kernel = kernels[record[2]]
        key = encoded_signature(source, kernel, tuple(record[3]))
        if accepted:
            exact_counts[key] += 1
            exact_physical[key] += orbit_size
            profile_counts[parameters[3]] += 1
            family_results[source_index] = [record, certificate, json.loads(key)]
        minimum = cost if minimum is None or cost < minimum else minimum
        if progress and (index + 1) % 500 == 0:
            print(f"tested_targets={index + 1} owned={len(family_results)}",
                  flush=True)
    if executor is not None:
        executor.shutdown()

    prior_payloads = {}
    with lzma.open(SOURCE_OWNERS, "rb") as rows:
        for raw in rows:
            payload = json.loads(raw.decode("ascii"))
            prior_payloads[payload[0][0]] = payload
    union_payloads = {**prior_payloads, **family_results}
    weighted.require(prior_owner_indices <= union_payloads.keys(),
                     "prior exact owner was not retained")

    owner_raw = hashlib.sha256()
    owner_physical = 0
    owner_temporary = OWNERS.with_name(OWNERS.name + ".tmp")
    with lzma.open(owner_temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
        for source_index in sorted(union_payloads):
            payload = union_payloads[source_index]
            raw = weighted.canonical_bytes(payload)
            output.write(raw)
            owner_raw.update(raw)
            owner_physical += payload[0][4]
    owner_temporary.replace(OWNERS)

    remainder_raw = hashlib.sha256()
    remainder_total = remainder_physical = 0
    remainder_temporary = REMAINDER.with_name(REMAINDER.name + ".tmp")
    with lzma.open(remainder_temporary, "wb", format=lzma.FORMAT_XZ,
                   preset=6) as output:
        for record in source.remainder_records(manifest):
            if record[0] in union_payloads:
                continue
            raw = weighted.canonical_bytes(record)
            output.write(raw)
            remainder_raw.update(raw)
            remainder_total += 1
            remainder_physical += record[4]
            if progress and remainder_total % 1000000 == 0:
                print(f"remainder={remainder_total}", flush=True)
    remainder_temporary.replace(REMAINDER)
    weighted.require(remainder_total + len(union_payloads) == scanned,
                     "updated remainder partition failed")
    weighted.require(remainder_physical + owner_physical == physical,
                     "updated physical partition failed")

    full_strata = []
    for key in sorted(selected, key=lambda item: (-target_counts[item], item)):
        full_strata.append({
            "signature": json.loads(key), "tested": target_counts[key],
            "owned": exact_counts[key],
            "failed": target_counts[key] - exact_counts[key],
            "physical_total": target_physical[key],
            "owned_physical_total": exact_physical[key],
            "coverage": weighted.pair(F(exact_counts[key], target_counts[key])),
        })
    new_owner_total = len(union_payloads) - len(prior_payloads)
    return {
        "schema": SCHEMA,
        "full_theorem": False,
        "scope": "full exact replay of every coarse signature with 100% ownership in the authenticated 10,000-row pilot",
        "owner_manifest_sha256": manifest_sha256,
        "source_report_sha256": source_report_sha256,
        "source_owner_stream": source_report["owner_stream"],
        "source_remainder": {"record_total": scanned, "physical_total": physical,
                             "raw_sha256": source_digest.hexdigest()},
        "sample_stratification": {
            "tested": source_report["sampling"]["tested"],
            "owned": source_report["result"]["owned_orbit_total"],
            "failed": source_report["result"]["failed_orbit_total"],
            "signature_total": len(strata),
            "selection_rule": "owned=tested and owned>0",
            "selected_signature_total": len(selected),
            "strata": strata,
        },
        "full_family_scan": {
            "tested": len(targets), "owned": sum(exact_counts.values()),
            "failed": len(targets) - sum(exact_counts.values()),
            "coverage": weighted.pair(F(sum(exact_counts.values()), len(targets))),
            "minimum_cost": weighted.pair(minimum),
            "selected_profile_counts": dict(sorted(profile_counts.items())),
            "strata": full_strata,
        },
        "exact_coverage": {
            "prior_owner_total": len(prior_payloads),
            "new_owner_total": new_owner_total,
            "union_owner_total": len(union_payloads),
            "union_owner_physical_total": owner_physical,
            "union_owner_target_total": 17 * len(union_payloads),
            "source_fraction": weighted.pair(F(len(union_payloads), scanned)),
        },
        "classification_stream_sha256": classification.hexdigest(),
        "owner_stream": {"path": OWNERS.name,
                         "record_total": len(union_payloads),
                         "physical_total": owner_physical,
                         "raw_sha256": owner_raw.hexdigest(),
                         "artifact_sha256": weighted.file_sha256(OWNERS)},
        "updated_remainder_stream": {
            "path": REMAINDER.name, "record_total": remainder_total,
            "physical_total": remainder_physical,
            "raw_sha256": remainder_raw.hexdigest(),
            "artifact_sha256": weighted.file_sha256(REMAINDER),
        },
        "claim_boundary": "the union owner stream is exact; every other authenticated source row is persisted in the updated remainder",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    weighted.require(args.workers > 0, "worker count must be positive")
    report = scan(args.workers, args.progress)
    raw = weighted.canonical_bytes(report)
    if args.audit:
        weighted.require(args.output.read_bytes() == raw, "report does not reproduce")
    else:
        args.output.write_bytes(raw)
    print(f"targeted={report['full_family_scan']['tested']} "
          f"owned={report['exact_coverage']['union_owner_total']} "
          f"remaining={report['updated_remainder_stream']['record_total']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
