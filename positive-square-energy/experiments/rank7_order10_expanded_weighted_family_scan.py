#!/usr/bin/env python3
"""Mine and exactly replay expanded weighted-cycle families at order ten."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import lzma
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
WEIGHTED_PATH = HERE / "rank7_order10_weighted_cycle_gram_lane.py"
SPEC = importlib.util.spec_from_file_location("rank7_order10_expanded_base", WEIGHTED_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load weighted-cycle lane")
weighted = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(weighted)

SOURCE_REPORT = HERE / "rank7_order10_weighted_cycle_family_scan.json"
SOURCE_STREAM = HERE / "rank7_order10_after_weighted_cycle_remainder.jsonl.xz"
PRIOR_OWNERS = HERE / "rank7_order10_weighted_cycle_family_owners.jsonl.xz"
OUTPUT = HERE / "rank7_order10_expanded_weighted_family_scan.json"
OWNERS = HERE / "rank7_order10_expanded_weighted_family_owners.jsonl.xz"
REMAINDER = HERE / "rank7_order10_after_expanded_weighted_remainder.jsonl.xz"
SCHEMA = "rank-seven-order-ten-expanded-weighted-family-scan-v1"
F = Fraction
BUDGET = F(6)

PROFILES = (
    "cycle_leverage", "resistance_ratio", "inverse_length", "leverage_length",
    "inverse_length_squared", "leverage_squared", "resistance_length",
    "resistance_length_squared",
)
RATIOS = tuple(F(value) for value in (
    F(1, 16), F(1, 4), 1, 4, 16,
))
DEFECT_SCALES = tuple(F(value) for value in (
    F(1, 2), F(2, 3), 1,
))
PARAMETERS = tuple((F(1), ratio, scale, profile)
                   for profile in PROFILES
                   for scale in DEFECT_SCALES
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


def strict_json(path):
    raw = path.read_bytes()
    payload = json.loads(raw.decode("ascii"))
    require(raw == weighted.canonical_bytes(payload), f"noncanonical JSON: {path.name}")
    return payload, hashlib.sha256(raw).hexdigest()


def encoded_signature(source, kernel, row):
    return json.dumps(weighted.coarse_signature(source, kernel, row),
                      sort_keys=True, separators=(",", ":"))


def metric_weights(paths, cut):
    result = {profile: [] for profile in PROFILES}
    for column, (_, _, _, length) in enumerate(paths):
        resistance = cut[column][column]
        leverage = 1 - resistance
        require(F() < resistance < F(1), "physical path is not cyclic")
        values = {
            "cycle_leverage": leverage,
            "resistance_ratio": leverage / resistance,
            "inverse_length": F(1, length),
            "leverage_length": leverage / length,
            "inverse_length_squared": F(1, length * length),
            "leverage_squared": leverage * leverage,
            "resistance_length": leverage / (resistance * length),
            "resistance_length_squared": leverage / (resistance * length * length),
        }
        for profile in PROFILES:
            result[profile].append(values[profile])
    return result


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
    cut_core = tuple(tuple(sum(x * y for x, y in zip(cut_vectors[u], cut_vectors[v]))
                           for v in range(10)) for u in range(10))
    projected = [[signed[u][column] - sum(
        signed[u][left] * cut[left][column] for left in range(len(paths)))
        for column in range(len(paths))] for u in range(10)]
    cycle_cores = {}
    for profile, weights in metric_weights(paths, cut).items():
        cycle_cores[profile] = tuple(tuple(sum(
            weights[column] * projected[u][column] * projected[v][column]
            for column in range(len(paths))) for v in range(10)) for u in range(10))
    return cut_core, cycle_cores, paths


def gram_cost(cut_core, cycle_core, paths, degrees, parameters):
    _, cycle_weight, defect_scale, _ = parameters
    scales = [F(1) if degree == 3 else defect_scale for degree in degrees]
    core = [[scales[u] * scales[v] *
             (cut_core[u][v] + cycle_weight * cycle_core[u][v])
             for v in range(10)] for u in range(10)]
    normalizer = max(F(1), *(core[u][u] for u in range(10)))
    total = F()
    for _, u, v, length in paths:
        transformed = core[u][v] / normalizer
        if length & 1:
            transformed = -transformed
        if not -1 < transformed <= 1:
            return None, normalizer
        total += (1 - transformed) / (length * (1 + transformed))
    return total, normalizer


def search(projector, kernel, row, parameters=PARAMETERS):
    cut_core, cycle_cores, paths = components(projector, kernel["edges"], row)
    best = None
    for candidate in parameters:
        cost, normalizer = gram_cost(cut_core, cycle_cores[candidate[3]], paths,
                                     kernel["degrees"], candidate)
        if cost is not None and (best is None or cost < best[0]):
            best = cost, candidate, normalizer
    require(best is not None, "expanded weighted family produced no finite exact cost")
    return best


def worker(task):
    projector, kernels = _CONTEXT
    record, parameter_rows = task
    source_index, global_kernel, order_kernel, raw_row, orbit_size = record
    kernel = kernels[order_kernel]
    require(global_kernel == kernel["global_kernel"], "kernel reference changed")
    parameters = PARAMETERS if parameter_rows is None else tuple(
        (F(*row[0]), F(*row[1]), F(*row[2]), row[3]) for row in parameter_rows)
    cost, selected, normalizer = search(projector, kernel, tuple(raw_row), parameters)
    return source_index, orbit_size, cost, selected, normalizer


def parameter_payload(parameters):
    return [weighted.pair(value) for value in parameters[:3]] + [parameters[3]]


def parameter_key(parameters):
    return tuple((value.numerator, value.denominator)
                 for value in parameters[:3]) + (parameters[3],)


def key_payload(key):
    return [list(value) for value in key[:3]] + [key[3]]


def choose_signatures(results, minimum_tested, minimum_precision):
    selected = set()
    for key, row in results.items():
        if (row["tested"] >= minimum_tested and row["owned"] > 0 and
                row["owned"] * minimum_precision.denominator >=
                row["tested"] * minimum_precision.numerator):
            selected.add(key)
    return selected


def authenticated_rows(stream_info):
    digest = hashlib.sha256()
    total = physical = 0
    with lzma.open(SOURCE_STREAM, "rb") as rows:
        for raw in rows:
            record = json.loads(raw.decode("ascii"))
            require(raw == weighted.canonical_bytes(record), "noncanonical source row")
            digest.update(raw)
            total += 1
            physical += record[4]
            yield total - 1, record
    require((total, physical, digest.hexdigest()) ==
            (stream_info["record_total"], stream_info["physical_total"],
             stream_info["raw_sha256"]), "source remainder authentication failed")


def scan(pilot_size=12000, workers=1, minimum_tested=2,
         minimum_precision=F(19, 20), progress=False):
    global _CONTEXT
    require(pilot_size > 10000 and workers > 0 and minimum_tested > 0,
            "invalid expanded scan settings")
    source = load("rank7_order10_expanded_source", weighted.SOURCE)
    projector = load("rank7_order10_expanded_projector", weighted.PROJECTOR)
    manifest, manifest_sha256 = source.strict_json(source.MANIFEST)
    source_report, source_report_sha256 = strict_json(SOURCE_REPORT)
    require(source_report["owner_manifest_sha256"] == manifest_sha256,
            "source report uses another structural remainder")
    stream_info = source_report["updated_remainder_stream"]
    require(weighted.file_sha256(SOURCE_STREAM) == stream_info["artifact_sha256"],
            "source remainder artifact changed")
    require(weighted.file_sha256(PRIOR_OWNERS) ==
            source_report["owner_stream"]["artifact_sha256"], "prior owner artifact changed")
    total = stream_info["record_total"]
    require(pilot_size <= total, "pilot exceeds source remainder")
    kernels = source.kernel_dictionary()

    pilot_positions = {index * total // pilot_size for index in range(pilot_size)}
    pilot_records = []
    pilot_keys = []
    descriptions = {}
    for position, record in authenticated_rows(stream_info):
        if position not in pilot_positions:
            continue
        kernel = kernels[record[2]]
        key = encoded_signature(source, kernel, tuple(record[3]))
        pilot_records.append(record)
        pilot_keys.append(key)
        descriptions.setdefault(key, json.loads(key))
    require(len(pilot_records) == pilot_size, "pilot position count changed")

    _CONTEXT = projector, kernels
    tasks = ((record, None) for record in pilot_records)
    if workers == 1:
        answers = map(worker, tasks)
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=workers)
        answers = executor.map(worker, tasks, chunksize=8)
    pilot_results = defaultdict(lambda: {"tested": 0, "owned": 0})
    winning_parameters = defaultdict(Counter)
    pilot_classification = hashlib.sha256()
    for index, (key, answer) in enumerate(zip(pilot_keys, answers, strict=True)):
        source_index, _, cost, parameters, normalizer = answer
        accepted = cost <= BUDGET
        pilot_results[key]["tested"] += 1
        pilot_results[key]["owned"] += accepted
        if accepted:
            winning_parameters[key][parameter_key(parameters)] += 1
        pilot_classification.update(weighted.canonical_bytes([
            source_index, accepted, weighted.pair(cost), parameter_payload(parameters),
            weighted.pair(normalizer)]))
        if progress and (index + 1) % 1000 == 0:
            print(f"pilot={index + 1} owned={sum(r['owned'] for r in pilot_results.values())}",
                  flush=True)
    if executor is not None:
        executor.shutdown()

    selected = choose_signatures(pilot_results, minimum_tested, minimum_precision)
    require(selected, "expanded pilot selected no signatures")
    grids = {}
    for key in selected:
        winners = winning_parameters[key]
        grids[key] = [key_payload(row) for row, _ in sorted(
            winners.items(), key=lambda item: (-item[1], item[0]))]
        require(grids[key], "selected signature has no owning parameter")

    targets = []
    target_keys = []
    target_counts = Counter()
    for _, record in authenticated_rows(stream_info):
        kernel = kernels[record[2]]
        key = encoded_signature(source, kernel, tuple(record[3]))
        if key in selected:
            targets.append(record)
            target_keys.append(key)
            target_counts[key] += 1
    tasks = ((record, grids[key]) for record, key in zip(targets, target_keys, strict=True))
    if workers == 1:
        answers = map(worker, tasks)
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=workers)
        answers = executor.map(worker, tasks, chunksize=8)

    new_owners = {}
    exact_results = defaultdict(lambda: {"owned": 0, "owned_physical": 0})
    classification = hashlib.sha256()
    for index, (record, key, answer) in enumerate(
            zip(targets, target_keys, answers, strict=True)):
        source_index, orbit_size, cost, parameters, normalizer = answer
        accepted = cost <= BUDGET
        certificate = [source_index, accepted, weighted.pair(cost),
                       parameter_payload(parameters), weighted.pair(normalizer)]
        classification.update(weighted.canonical_bytes(certificate))
        if accepted:
            exact_results[key]["owned"] += 1
            exact_results[key]["owned_physical"] += orbit_size
            new_owners[source_index] = [record, certificate, json.loads(key)]
        if progress and (index + 1) % 1000 == 0:
            print(f"exact={index + 1}/{len(targets)} owned={len(new_owners)}", flush=True)
    if executor is not None:
        executor.shutdown()

    prior = {}
    prior_digest = hashlib.sha256()
    with lzma.open(PRIOR_OWNERS, "rb") as rows:
        for raw in rows:
            payload = json.loads(raw.decode("ascii"))
            require(raw == weighted.canonical_bytes(payload), "noncanonical prior owner")
            prior_digest.update(raw)
            prior[payload[0][0]] = payload
    require((len(prior), prior_digest.hexdigest()) ==
            (source_report["owner_stream"]["record_total"],
             source_report["owner_stream"]["raw_sha256"]), "prior owner stream changed")
    require(not (prior.keys() & new_owners.keys()), "source remainder overlaps prior owners")
    union = {**prior, **new_owners}

    owner_raw = hashlib.sha256()
    owner_physical = 0
    temporary = OWNERS.with_name(OWNERS.name + ".tmp")
    with lzma.open(temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
        for source_index in sorted(union):
            payload = union[source_index]
            raw = weighted.canonical_bytes(payload)
            output.write(raw)
            owner_raw.update(raw)
            owner_physical += payload[0][4]
    temporary.replace(OWNERS)

    remainder_raw = hashlib.sha256()
    remainder_total = remainder_physical = 0
    temporary = REMAINDER.with_name(REMAINDER.name + ".tmp")
    with lzma.open(temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
        for _, record in authenticated_rows(stream_info):
            if record[0] in new_owners:
                continue
            raw = weighted.canonical_bytes(record)
            output.write(raw)
            remainder_raw.update(raw)
            remainder_total += 1
            remainder_physical += record[4]
    temporary.replace(REMAINDER)
    require(remainder_total + len(new_owners) == total, "new remainder partition failed")

    def pilot_stratum(key):
        row = pilot_results[key]
        return {"signature": descriptions[key], **row,
                "failed": row["tested"] - row["owned"],
                "coverage": weighted.pair(F(row["owned"], row["tested"]))}

    ranked = sorted(pilot_results, key=lambda key: (-pilot_results[key]["owned"] /
                                                    pilot_results[key]["tested"],
                                                    -pilot_results[key]["owned"], key))
    exact_strata = []
    for key in sorted(selected, key=lambda item: (-target_counts[item], item)):
        owned = exact_results[key]["owned"]
        exact_strata.append({
            "signature": descriptions[key], "tested": target_counts[key], "owned": owned,
            "failed": target_counts[key] - owned,
            "coverage": weighted.pair(F(owned, target_counts[key])),
            "owned_physical_total": exact_results[key]["owned_physical"],
            "pilot_winning_parameters": grids[key],
        })
    return {
        "schema": SCHEMA, "full_theorem": False,
        "scope": "expanded exact parameter/metric mining on an evenly spaced pilot followed by exact full-family replay",
        "owner_manifest_sha256": manifest_sha256,
        "source_report_sha256": source_report_sha256,
        "source_remainder": stream_info,
        "family": {
            "profiles": list(PROFILES),
            "non_scalar_profile_total": len(PROFILES),
            "ratios": [weighted.pair(value) for value in RATIOS],
            "defect_scales": [weighted.pair(value) for value in DEFECT_SCALES],
            "parameter_total": len(PARAMETERS),
            "selection_replay": "each selected signature replays the union of exact pilot-winning parameter rows for that signature",
        },
        "pilot": {
            "method": "floor(i*N/pilot_size), 0<=i<pilot_size, over the authenticated source remainder",
            "tested": pilot_size, "signature_total": len(pilot_results),
            "owned": sum(row["owned"] for row in pilot_results.values()),
            "minimum_signature_tested": minimum_tested,
            "minimum_precision": weighted.pair(minimum_precision),
            "selected_signature_total": len(selected),
            "classification_stream_sha256": pilot_classification.hexdigest(),
            "strata": [pilot_stratum(key) for key in ranked],
        },
        "full_family_scan": {
            "tested": len(targets), "owned": len(new_owners),
            "failed": len(targets) - len(new_owners),
            "coverage": weighted.pair(F(len(new_owners), len(targets))),
            "classification_stream_sha256": classification.hexdigest(),
            "strata": exact_strata,
        },
        "exact_coverage": {
            "prior_owner_total": len(prior), "new_owner_total": len(new_owners),
            "union_owner_total": len(union),
            "union_owner_physical_total": owner_physical,
            "union_owner_target_total": 17 * len(union),
        },
        "owner_stream": {"path": OWNERS.name, "record_total": len(union),
                         "physical_total": owner_physical,
                         "raw_sha256": owner_raw.hexdigest(),
                         "artifact_sha256": weighted.file_sha256(OWNERS)},
        "updated_remainder_stream": {
            "path": REMAINDER.name, "record_total": remainder_total,
            "physical_total": remainder_physical,
            "raw_sha256": remainder_raw.hexdigest(),
            "artifact_sha256": weighted.file_sha256(REMAINDER),
        },
        "claim_boundary": "the persisted union is exact; every unowned source row is retained byte-for-byte in the updated remainder",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-size", type=int, default=12000)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--minimum-tested", type=int, default=2)
    parser.add_argument("--minimum-precision", type=Fraction, default=F(19, 20))
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    report = scan(args.pilot_size, args.workers, args.minimum_tested,
                  args.minimum_precision, args.progress)
    raw = weighted.canonical_bytes(report)
    if args.audit:
        require(args.output.read_bytes() == raw, "report does not reproduce")
    else:
        args.output.write_bytes(raw)
    print(f"pilot={report['pilot']['tested']} selected={report['pilot']['selected_signature_total']} "
          f"targeted={report['full_family_scan']['tested']} "
          f"new={report['exact_coverage']['new_owner_total']} "
          f"union={report['exact_coverage']['union_owner_total']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
