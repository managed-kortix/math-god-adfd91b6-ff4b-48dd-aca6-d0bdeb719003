#!/usr/bin/env python3
"""Exact non-scalar weighted-cycle Gram lane for the order-ten remainder."""

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
SOURCE = HERE / "rank7_order10_near_cubic_gram_lane.py"
PROJECTOR = HERE / "rank7_order10_cycle_cut_gram_lane.py"
OUTPUT = HERE / "rank7_order10_weighted_cycle_gram_lane.json"
OWNERS = HERE / "rank7_order10_weighted_cycle_gram_owners.jsonl.xz"
SCHEMA = "rank-seven-order-ten-weighted-cycle-gram-lane-v1"
F = Fraction
BUDGET = F(6)
PROFILES = ("cycle_leverage", "resistance_ratio", "inverse_length",
            "leverage_length")
RATIOS = (F(1, 16), F(1, 8), F(1, 4), F(1, 2), F(1), F(2), F(4), F(8))
DEFECT_SCALES = (F(1, 2), F(2, 3), F(3, 4), F(1))
PARAMETERS = tuple((F(1), ratio, defect, profile)
                   for profile in PROFILES for defect in DEFECT_SCALES
                   for ratio in RATIOS)
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


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def pair(value):
    return [value.numerator, value.denominator]


def weighted_cycle_cores(signed_incidence, paths, cut_projector):
    """Return A P_cycle diag(q) P_cycle A^T for exact path-weight profiles."""
    size = len(paths)
    projected = [[signed_incidence[u][column] - sum(
        signed_incidence[u][left] * cut_projector[left][column]
        for left in range(size)) for column in range(size)]
        for u in range(10)]
    cores = {}
    for profile in PROFILES:
        weights = []
        for column, (_, _, _, length) in enumerate(paths):
            resistance = cut_projector[column][column]
            leverage = 1 - resistance
            require(F() < resistance < F(1), "physical path is not cyclic")
            weights.append({
                "cycle_leverage": leverage,
                "resistance_ratio": leverage / resistance,
                "inverse_length": F(1, length),
                "leverage_length": leverage / length,
            }[profile])
        cores[profile] = tuple(tuple(sum(
            weights[column] * projected[u][column] * projected[v][column]
            for column in range(size)) for v in range(10)) for u in range(10))
    return cores


def components(projector, edges, row):
    paths = projector.physical_paths(edges, row)
    endpoints = tuple((u, v) for _, u, v, _ in paths)
    cut = projector.cut_metric(endpoints)
    signed = [[F() for _ in paths] for _ in range(10)]
    for column, (_, u, v, length) in enumerate(paths):
        signed[u][column] = 1
        signed[v][column] = -1 if length & 1 else 1
    cut_vectors = [[sum(signed[u][left] * cut[left][right]
                        for left in range(len(paths)))
                    for right in range(len(paths))] for u in range(10)]
    cut_core = tuple(tuple(sum(x * y for x, y in zip(cut_vectors[u],
                                                       cut_vectors[v]))
                           for v in range(10)) for u in range(10))
    return cut_core, weighted_cycle_cores(signed, paths, cut), paths


def gram_and_cost(cut_core, cycle_core, paths, degrees, parameters):
    cut_weight, cycle_weight, defect_scale, _ = parameters
    scales = [F(1) if degree == 3 else defect_scale for degree in degrees]
    core = [[scales[u] * scales[v] *
             (cut_weight * cut_core[u][v] + cycle_weight * cycle_core[u][v])
             for v in range(10)] for u in range(10)]
    normalizer = max(F(1), *(core[u][u] for u in range(10)))
    total = F()
    for _, u, v, length in paths:
        correlation = core[u][v] / normalizer
        transformed = -correlation if length & 1 else correlation
        if not -1 < transformed <= 1:
            return None, normalizer
        total += (1 - transformed) / (length * (1 + transformed))
    return total, normalizer


def search(projector, kernel, row):
    cut_core, cycle_cores, paths = components(projector, kernel["edges"], row)
    best = None
    for parameters in PARAMETERS:
        cost, normalizer = gram_and_cost(cut_core, cycle_cores[parameters[3]],
                                         paths, kernel["degrees"], parameters)
        if cost is not None and (best is None or cost < best[0]):
            best = cost, parameters, normalizer
    require(best is not None, "weighted family produced no finite exact cost")
    return best


def coarse_signature(source, kernel, row):
    invariants = source.row_invariants(kernel, row)
    return {
        "degree_partition": list(kernel["degree_partition"]),
        "multiplicity_partition": list(kernel["multiplicity_partition"]),
        "bundle_types": invariants["parity"]["bundle_types"],
        "negative_support_cycle_rank":
            invariants["cycle_cut"]["negative_support_cycle_rank"],
        "odd_support_cycle_rank": invariants["cycle_cut"]["odd_support_cycle_rank"],
        "triangle_total": kernel["triangle_total"],
    }


def worker(record):
    projector, kernels = _CONTEXT
    source_index, global_kernel, order_kernel, raw_row, orbit_size = record
    kernel = kernels[order_kernel]
    require(global_kernel == kernel["global_kernel"], "kernel reference changed")
    cost, parameters, normalizer = search(projector, kernel, tuple(raw_row))
    return source_index, orbit_size, cost, parameters, normalizer


def scan(sample_size=10000, workers=1, progress=False):
    global _CONTEXT
    require(sample_size >= 10000, "representative scan must contain at least 10,000 rows")
    source = load("rank7_order10_weighted_source", SOURCE)
    projector = load("rank7_order10_weighted_projector", PROJECTOR)
    manifest, manifest_sha256 = source.strict_json(source.MANIFEST)
    kernels = source.kernel_dictionary()
    records = []
    signatures = Counter()
    signature_payloads = {}
    for record in source.remainder_records(manifest):
        kernel = kernels[record[2]]
        row = tuple(record[3])
        payload = coarse_signature(source, kernel, row)
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        signatures[encoded] += 1
        signature_payloads.setdefault(encoded, payload)
        records.append(record)
        if len(records) >= sample_size:
            break
    require(len(records) == sample_size, "remainder ended before requested sample")
    _CONTEXT = projector, kernels
    if workers == 1:
        results = map(worker, records)
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=workers)
        results = executor.map(worker, records, chunksize=16)

    classification = hashlib.sha256()
    owner_digest = hashlib.sha256()
    owned = owned_physical = 0
    profile_counts = Counter()
    signature_results = {key: {"tested": count, "owned": 0}
                         for key, count in signatures.items()}
    minimum = None
    temporary = OWNERS.with_name(OWNERS.name + ".tmp")
    with lzma.open(temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
        for index, (record, result) in enumerate(zip(records, results, strict=True)):
            source_index, orbit_size, cost, parameters, normalizer = result
            accepted = cost <= BUDGET
            certificate = [source_index, accepted, pair(cost),
                           [pair(value) for value in parameters[:3]] + [parameters[3]],
                           pair(normalizer)]
            classification.update(canonical_bytes(certificate))
            kernel = kernels[record[2]]
            payload = coarse_signature(source, kernel, tuple(record[3]))
            encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
            signature_results[encoded]["owned"] += accepted
            minimum = cost if minimum is None or cost < minimum else minimum
            if accepted:
                owned += 1
                owned_physical += orbit_size
                profile_counts[parameters[3]] += 1
                raw = canonical_bytes([record, certificate, payload])
                output.write(raw)
                owner_digest.update(raw)
            if progress and (index + 1) % 1000 == 0:
                print(f"tested={index + 1} owned={owned}", flush=True)
    if executor is not None:
        executor.shutdown()
    temporary.replace(OWNERS)

    ranked = sorted(signature_results,
                    key=lambda key: (-signature_results[key]["tested"], key))

    def stratum(key):
        result = signature_results[key]
        return {"signature": signature_payloads[key], **result,
                "coverage": pair(F(result["owned"], result["tested"]))}

    strata = [stratum(key) for key in ranked]
    owner_ranked = sorted((key for key in ranked if signature_results[key]["owned"]),
                          key=lambda key: (-signature_results[key]["owned"],
                                           -signature_results[key]["tested"], key))
    promising = any(row["tested"] >= 100 and row["owned"] * 20 >= row["tested"]
                    for row in strata)
    return {
        "schema": SCHEMA,
        "full_theorem": False,
        "scope": "leading authenticated 10,000-row-or-larger representative scan",
        "owner_manifest_sha256": manifest_sha256,
        "sampling": {"method": "deterministic leading remainder rows",
                     "requested": sample_size, "tested": len(records),
                     "source_index_first": records[0][0],
                     "source_index_last": records[-1][0]},
        "family": {
            "formula": "H=DA(a P_cut+b P_cycle diag(q) P_cycle)A^T D; G=H/M+diag(1-diag(H)/M)",
            "profiles": {
                "cycle_leverage": "q_e=1-R_e",
                "resistance_ratio": "q_e=(1-R_e)/R_e",
                "inverse_length": "q_e=1/L_e",
                "leverage_length": "q_e=(1-R_e)/L_e",
            },
            "effective_resistance": "R_e=(P_cut)_{e,e}",
            "parameter_order": ["cut_weight", "cycle_weight", "defect_scale",
                                "cycle_profile"],
            "parameters": [[pair(value) for value in row[:3]] + [row[3]]
                           for row in PARAMETERS],
            "rational_psd_decomposition": "a(DA P_cut)(DA P_cut)^T+b sum_e q_e(DA P_cycle e_e)(DA P_cycle e_e)^T plus nonnegative diagonal coordinate squares",
            "exact_cost_bound": "sum_p (1-t_p)/(L_p(1+t_p))<=6, t_p=(-1)^L_p G_uv",
        },
        "result": {"owned_orbit_total": owned,
                   "owned_physical_total": owned_physical,
                   "owned_target_total": 17 * owned,
                   "failed_orbit_total": sample_size - owned,
                   "coverage": pair(F(owned, sample_size)),
                   "minimum_cost": pair(minimum),
                    "selected_profile_counts": dict(sorted(profile_counts.items()))},
        "dominant_signatures": strata[:25],
        "dominant_owner_signatures": [stratum(key) for key in owner_ranked[:25]],
        "full_dominant_family_scan": {
            "performed": False,
            "promising_threshold": "at least 5% exact ownership in a signature with at least 100 sampled rows",
            "sample_promising": promising,
            "reason": ("separate full-family scan required" if promising else
                       "no dominant sampled signature met the predeclared coverage threshold"),
        },
        "classification_stream_sha256": classification.hexdigest(),
        "owner_stream": {"path": OWNERS.name, "record_total": owned,
                         "raw_sha256": owner_digest.hexdigest(),
                         "artifact_sha256": file_sha256(OWNERS)},
        "claim_boundary": "only rows persisted in the owner stream are owned; representative coverage is not a full-remainder theorem",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-size", type=int, default=10000)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    require(args.workers > 0, "worker count must be positive")
    report = scan(args.sample_size, args.workers, args.progress)
    raw = canonical_bytes(report)
    if args.audit:
        require(args.output.read_bytes() == raw, "report does not reproduce")
    else:
        args.output.write_bytes(raw)
    print(f"tested={report['sampling']['tested']} "
          f"owned={report['result']['owned_orbit_total']} "
          f"minimum={report['result']['minimum_cost']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
