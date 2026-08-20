#!/usr/bin/env python3
"""Exact defect-transport/cycle-space/typed-SOS lane for order eleven."""

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
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.optimize import minimize


HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / "rank7_order11_structural_owner_manifest.json"
OWNER_ENGINE_PATH = HERE / "rank7_order11_structural_owner_manifest.py"
OUTPUT_PATH = HERE / "rank7_order11_defect_transport_gram_lane.json"
OWNER_STREAM_PATH = HERE / "rank7_order11_defect_transport_gram_owners.jsonl.xz"
SCHEMA = "rank-seven-order-eleven-defect-transport-typed-sos-gram-lane-v1"
ORDER = 11
PATH_COUNT = 17
TARGETS_PER_ROW = 18
BUDGET = Fraction(6)
F = Fraction
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


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def strict_json(path):
    raw = path.read_bytes()
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), f"noncanonical JSON: {path.name}")
    return payload, hashlib.sha256(raw).hexdigest()


def pair(value):
    return [value.numerator, value.denominator]


def inverse(matrix):
    size = len(matrix)
    work = [[F(value) for value in row] + [F(i == j) for j in range(size)]
            for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        require(pivot is not None, "singular reduced Laplacian")
        work[column], work[pivot] = work[pivot], work[column]
        divisor = work[column][column]
        work[column] = [value / divisor for value in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [left - multiplier * right
                         for left, right in zip(work[row], work[column])]
    return tuple(tuple(row[size:]) for row in work)


def kernel_data(ledger):
    edges = tuple(map(tuple, ledger["edges"]))
    degrees = [0] * ORDER
    adjacency = [set() for _ in range(ORDER)]
    for u, v, multiplicity in edges:
        degrees[u] += multiplicity
        degrees[v] += multiplicity
        adjacency[u].add(v)
        adjacency[v].add(u)
    require(sorted(degrees, reverse=True) == [4] + [3] * 10,
            "order-eleven kernel is not defect two")
    return {
        "global_kernel": ledger["global_kernel"], "edges": edges,
        "degrees": tuple(degrees), "defect_vertex": degrees.index(4),
        "multiplicity_partition": tuple(sorted((edge[2] for edge in edges), reverse=True)),
        "support_cycle_rank": len(edges) - ORDER + 1,
        "triangle_total": sum(len(adjacency[u] & adjacency[v])
                              for u in range(ORDER) for v in adjacency[u]
                              if u < v) // 3,
    }


def paths_types_family(kernel, row):
    signed = [[F() for _ in range(ORDER)] for _ in range(ORDER)]
    incident = [[] for _ in range(ORDER)]
    paths = []
    kinds = [0, 0, 0]
    for edge_index, ((u, v, multiplicity), odd) in enumerate(
            zip(kernel["edges"], row, strict=True)):
        value = multiplicity - 2 * odd
        signed[u][v] = signed[v][u] = value
        incident[u].append((multiplicity, odd))
        incident[v].append((multiplicity, odd))
        kinds[0 if odd == 0 else 2 if odd == multiplicity else 1] += 1
        lengths = (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)
        paths.extend((edge_index, occurrence, u, v, length)
                     for occurrence, length in enumerate(lengths))
    require(len(paths) == PATH_COUNT, "physical path count changed")
    signed_degrees = [sum(values) for values in signed]
    keys = [(kernel["degrees"][u] - 3, signed_degrees[u],
             tuple(sorted(incident[u], reverse=True))) for u in range(ORDER)]
    dictionary = {key: index for index, key in enumerate(sorted(set(keys)))}
    family = (kernel["multiplicity_partition"], tuple(kinds),
              kernel["support_cycle_rank"], kernel["triangle_total"])
    return (tuple(tuple(values) for values in signed), tuple(paths), tuple(keys),
            tuple(dictionary[key] for key in keys), family)


def row_family(kernel, row):
    kinds = [0, 0, 0]
    for (_, _, multiplicity), odd in zip(kernel["edges"], row, strict=True):
        kinds[0 if odd == 0 else 2 if odd == multiplicity else 1] += 1
    return (kernel["multiplicity_partition"], tuple(kinds),
            kernel["support_cycle_rank"], kernel["triangle_total"])


@lru_cache(maxsize=None)
def cycle_projector(endpoints):
    columns = len(endpoints)
    incidence = [[F() for _ in range(columns)] for _ in range(ORDER - 1)]
    for column, (u, v) in enumerate(endpoints):
        if u < ORDER - 1:
            incidence[u][column] = 1
        if v < ORDER - 1:
            incidence[v][column] = -1
    laplacian = [[sum(incidence[u][edge] * incidence[v][edge]
                       for edge in range(columns))
                  for v in range(ORDER - 1)] for u in range(ORDER - 1)]
    laplacian_inverse = inverse(laplacian)
    cut = [[sum(incidence[u][left] * laplacian_inverse[u][v] * incidence[v][right]
                for u in range(ORDER - 1) for v in range(ORDER - 1))
            for right in range(columns)] for left in range(columns)]
    return tuple(tuple(F(left == right) - cut[left][right]
                       for right in range(columns)) for left in range(columns))


def transport_core(paths):
    projector = cycle_projector(tuple((u, v) for _, _, u, v, _ in paths))
    signed_incidence = [[F() for _ in paths] for _ in range(ORDER)]
    for column, (_, _, u, v, length) in enumerate(paths):
        signed_incidence[u][column] = 1
        signed_incidence[v][column] = -1 if length & 1 else 1
    projected = [[sum(signed_incidence[u][left] * projector[left][right]
                      for left in range(len(paths)))
                  for right in range(len(paths))] for u in range(ORDER)]
    return tuple(tuple(sum(x * y for x, y in zip(projected[u], projected[v]))
                       for v in range(ORDER)) for u in range(ORDER))


def exact_cost(signed, transport, paths, type_ids, parameters, cycle_weight):
    x = [[(parameters[type_ids[u]][0] if u == v else F()) +
          parameters[type_ids[u]][1] * signed[u][v]
          for v in range(ORDER)] for u in range(ORDER)]
    core = [[sum(x[u][w] * x[v][w] for w in range(ORDER)) +
             cycle_weight * transport[u][v]
             for v in range(ORDER)] for u in range(ORDER)]
    normalizer = max(core[u][u] for u in range(ORDER))
    require(normalizer > 0, "zero Gram normalizer")
    total = F()
    for _, _, u, v, length in paths:
        correlation = core[u][v] / normalizer
        transformed = -correlation if length & 1 else correlation
        require(-1 <= transformed <= 1, "Gram correlation escaped unit interval")
        if transformed == -1:
            return None, normalizer
        total += (1 - transformed) / (length * (1 + transformed))
    return total, normalizer


def numerical_cost(values, signed, transport, paths, type_ids):
    type_total = (len(values) - 1) // 2
    ids = np.asarray(type_ids)
    diagonal = np.exp(values[:type_total])[ids]
    coefficient = values[type_total:2 * type_total][ids]
    x = np.eye(ORDER) * diagonal[:, None] + coefficient[:, None] * signed
    core = x @ x.T + np.exp(values[-1]) * transport
    normalizer = np.max(np.diag(core))
    total = 0.0
    for _, _, u, v, length in paths:
        transformed = core[u, v] / normalizer
        if length & 1:
            transformed = -transformed
        if transformed <= -1.0 + 1e-12:
            return 1e9
        total += (1.0 - transformed) / (length * (1.0 + transformed))
    return total


def search(kernel, row, max_denominator=128):
    signed, paths, type_keys, type_ids, family = paths_types_family(kernel, row)
    transport = transport_core(paths)
    type_total = max(type_ids) + 1
    initial = np.concatenate((np.zeros(type_total), np.full(type_total, 0.35), [-2.0]))
    proposal = minimize(
        numerical_cost, initial,
        args=(np.asarray(signed, dtype=np.float64),
              np.asarray(transport, dtype=np.float64), paths, type_ids),
        method="Powell",
        bounds=[(-2.0, 2.0)] * type_total +
               [(-4.0, 4.0)] * type_total + [(-9.0, 4.0)],
        options={"ftol": 1e-8, "maxiter": 220},
    )
    parameters = tuple(
        (F(float(np.exp(proposal.x[index]))).limit_denominator(max_denominator),
         F(float(proposal.x[type_total + index])).limit_denominator(max_denominator))
        for index in range(type_total))
    cycle_weight = F(float(np.exp(proposal.x[-1]))).limit_denominator(max_denominator)
    cost, normalizer = exact_cost(signed, transport, paths, type_ids,
                                  parameters, cycle_weight)
    return cost, normalizer, parameters, cycle_weight, type_keys, family


def existing_owner(owner, atom, edges, row):
    return owner.recognize_row(atom, edges, row)[0] is not None


def stream_rows(manifest, owner, exclude_owned=False):
    atom = owner.load_atom_recognizer() if exclude_owned else None
    source_index = 0
    for chunk_row in manifest["chunks"]:
        path = MANIFEST_PATH.parent / chunk_row["path"]
        header, records, finish = owner.stream_chunk(path)
        kernels = {row["order_kernel"]: kernel_data(row) for row in header["kernels"]}
        stream_digest = hashlib.sha256()
        for record in records:
            stream_digest.update(canonical_bytes(record))
            kernel = kernels[record["order_kernel"]]
            row = tuple(record["row"])
            if not exclude_owned or not existing_owner(owner, atom, kernel["edges"], row):
                yield [source_index, record["global_kernel"], record["order_kernel"],
                       record["row"], record["orbit_size"]], kernel
            source_index += 1
        finish()
        require(stream_digest.hexdigest() == header["residual_stream_sha256"],
                "census residual digest changed")


def family_payload(family):
    return {"multiplicity_partition": list(family[0]),
            "bundle_types": list(family[1]), "cycle_rank": family[2],
            "triangle_total": family[3]}


def family_key(family):
    return json.dumps(family_payload(family), sort_keys=True, separators=(",", ":"))


def worker(item):
    max_denominator = _CONTEXT
    record, kernel = item
    result = search(kernel, tuple(record[3]), max_denominator)
    return record, result


def scan(top_families=12, representatives_per_family=8, max_denominator=128,
         workers=1, progress=False, persist=True, full_families=True):
    global _CONTEXT
    require(top_families > 0 and representatives_per_family > 0 and
            max_denominator > 0 and workers > 0, "invalid scan bounds")
    manifest, manifest_sha256 = strict_json(MANIFEST_PATH)
    owner_wrapper = load("rank7_order11_defect_transport_owner", OWNER_ENGINE_PATH)
    owner = owner_wrapper.load_owner_engine()
    atom = owner.load_atom_recognizer()
    counts = Counter()
    physical_counts = Counter()
    descriptions = {}
    representatives = {}
    remainder_digest = hashlib.sha256()
    scanned = physical = 0
    for record, kernel in stream_rows(manifest, owner):
        family = row_family(kernel, tuple(record[3]))
        key = family_key(family)
        counts[key] += 1
        physical_counts[key] += record[4]
        descriptions[key] = family_payload(family)
        bucket = representatives.setdefault(key, [])
        if len(bucket) < representatives_per_family:
            bucket.append((record, kernel))
        remainder_digest.update(canonical_bytes(record))
        scanned += 1
        physical += record[4]
        if progress and scanned % 1000000 == 0:
            print(f"stratified={scanned}", flush=True)
    require((scanned, physical) == (manifest["coarse_residual_total"],
                                    manifest["coarse_residual_physical_total"]),
            "coarse residual totals changed")
    ranked = sorted(counts, key=lambda key: (-counts[key], -physical_counts[key], key))
    selected = set(ranked[:top_families])
    pilot_items = [item for key in ranked[:top_families] for item in representatives[key]
                   if not existing_owner(owner, atom, item[1]["edges"], tuple(item[0][3]))]

    _CONTEXT = max_denominator
    if workers == 1:
        pilot_results = map(worker, pilot_items)
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=workers)
        pilot_results = executor.map(worker, pilot_items, chunksize=4)
    pilot_owned = Counter()
    pilot_tested = Counter()
    pilot_rows = []
    pilot_owner_payloads = []
    for position, (record, result) in enumerate(pilot_results, 1):
        cost, normalizer, parameters, cycle_weight, type_keys, family = result
        key = family_key(family)
        accepted = cost is not None and cost <= BUDGET
        pilot_tested[key] += 1
        pilot_owned[key] += accepted
        certificate = [record[0], accepted, None if cost is None else pair(cost),
                       pair(normalizer),
                       [[pair(left), pair(right)] for left, right in parameters],
                       pair(cycle_weight)]
        pilot_rows.append([record[0], accepted, None if cost is None else pair(cost)])
        if accepted:
            pilot_owner_payloads.append([
                record, certificate,
                [[type_key[0], pair(type_key[1]), [list(value) for value in type_key[2]]]
                 for type_key in sorted(set(type_keys))], descriptions[key]])
        if progress and position % 20 == 0:
            print(f"pilot={position}/{len(pilot_items)} owned={sum(pilot_owned.values())}",
                  flush=True)
    if executor is not None:
        executor.shutdown()
    promoted = {key for key in selected if pilot_owned[key] > 0}

    targets = []
    if full_families:
        for record, kernel in stream_rows(manifest, owner):
            family = row_family(kernel, tuple(record[3]))
            if (family_key(family) in promoted and
                    not existing_owner(owner, atom, kernel["edges"], tuple(record[3]))):
                targets.append((record, kernel))
    if workers == 1:
        results = map(worker, targets)
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=workers)
        results = executor.map(worker, targets, chunksize=8)

    owners = [] if full_families else pilot_owner_payloads
    classification = hashlib.sha256()
    full_tested = Counter()
    full_owned = Counter()
    full_physical = Counter()
    for position, (record, result) in enumerate(results, 1):
        cost, normalizer, parameters, cycle_weight, type_keys, family = result
        key = family_key(family)
        accepted = cost is not None and cost <= BUDGET
        certificate = [record[0], accepted, None if cost is None else pair(cost),
                       pair(normalizer),
                       [[pair(left), pair(right)] for left, right in parameters],
                       pair(cycle_weight)]
        classification.update(canonical_bytes(certificate))
        full_tested[key] += 1
        full_owned[key] += accepted
        full_physical[key] += record[4] * accepted
        if accepted:
            owners.append([record, certificate,
                           [[key[0], pair(key[1]), [list(value) for value in key[2]]]
                            for key in sorted(set(type_keys))], descriptions[key]])
        if progress and position % 1000 == 0:
            print(f"family_scan={position}/{len(targets)} owned={len(owners)}", flush=True)
    if executor is not None:
        executor.shutdown()

    owner_raw = hashlib.sha256()
    if persist:
        temporary = OWNER_STREAM_PATH.with_name(OWNER_STREAM_PATH.name + ".tmp")
        with lzma.open(temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
            for payload in owners:
                raw = canonical_bytes(payload)
                output.write(raw)
                owner_raw.update(raw)
        temporary.replace(OWNER_STREAM_PATH)
    strata = [{"signature": descriptions[key], "orbit_total": counts[key],
               "physical_total": physical_counts[key],
               "pilot_tested": pilot_tested[key], "pilot_owned": pilot_owned[key],
               "promoted": key in promoted,
               "full_tested": full_tested[key], "full_owned": full_owned[key],
               "full_owned_physical": full_physical[key]}
              for key in ranked[:top_families]]
    return {
        "schema": SCHEMA, "full_theorem": False,
        "scope": "exact full structural-remainder stratification, representative scan of dominant families, and full exact replay of pilot-positive dominant families",
        "source_manifest_sha256": manifest_sha256,
        "source_coarse_residual_orbit_total": scanned,
        "source_coarse_residual_physical_total": physical,
        "source_coarse_residual_stream_sha256": remainder_digest.hexdigest(),
        "exact_structural_remainder_orbit_total": manifest["remainder_orbit_total"],
        "exact_structural_remainder_physical_total": manifest["remainder_physical_total"],
        "degree_sequence": [4] + [3] * 10,
        "degree_defect_identity": "sum_v(deg(v)-3)=1; handshake defect from cubic is two",
        "failure_analysis": {
            "cubic_cycle_lane": "requires degree sequence 3^12 and therefore rejects every order-eleven kernel before searching",
            "generalized_three_ray": "not in order-eleven precedence; its six states quantize correlations and cannot transport the unique degree-four hub defect continuously",
            "signed_imbalance": "uses only local signed bundle imbalance and discards cycle-space transport",
            "simplex_atom": "requires sparse equality profiles and does not fit the broad mixed near-cubic remainder",
        },
        "gram": {
            "formula": "H=XX^T+w A P_cycle A^T; G=H/M+diag(1-diag(H)/M)",
            "typed_sos": "X=D0+D1*S with local type (degree defect,signed degree,sorted incident bundles)",
            "defect_transport": "A P_cycle carries signed endpoint mass through the seven-dimensional physical cycle space away from the unique degree-four hub",
            "cycle_projector": "P_cycle=I-B^T(BB^T)^-1B",
            "psd_proof": "XX^T and w(A P_cycle)(A P_cycle)^T are exact rational Gram squares; diagonal completion is nonnegative",
            "exact_cost": "sum_p (1-t_p)/(L_p(1+t_p))<=6 with t_p=(-1)^L G_uv",
            "max_denominator": max_denominator,
        },
        "family_selection": {"top_family_total": top_families,
                             "representatives_per_family": representatives_per_family,
                             "promotion_rule": "at least one exact pilot owner",
                             "promoted_family_total": len(promoted),
                             "full_family_replay": full_families},
        "dominant_families": strata,
        "pilot": {"tested": len(pilot_items), "owned": sum(pilot_owned.values()),
                  "classification": pilot_rows},
        "full_family_scan": {"performed": full_families,
                             "tested": len(targets), "owned": len(owners),
                             "owned_physical": sum(row[0][4] for row in owners)},
        "owned_target_total": len(owners) * TARGETS_PER_ROW,
        "remaining_remainder_total": manifest["remainder_orbit_total"] - len(owners),
        "classification_stream_sha256": classification.hexdigest(),
        "owner_stream": None if not persist else {
            "path": OWNER_STREAM_PATH.name, "record_total": len(owners),
            "raw_sha256": owner_raw.hexdigest(),
            "artifact_sha256": file_sha256(OWNER_STREAM_PATH)},
        "claim_boundary": "only exact accepted records in the owner stream are owned; when full-family replay is false these are representative owners only; all other structural remainder rows remain unclassified by this lane",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--top-families", type=int, default=12)
    parser.add_argument("--representatives-per-family", type=int, default=8)
    parser.add_argument("--max-denominator", type=int, default=128)
    parser.add_argument("--workers", type=int, default=max(1, min(8, os.cpu_count() or 1)))
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--pilot-only", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    report = scan(args.top_families, args.representatives_per_family,
                  args.max_denominator, args.workers, args.progress,
                  persist=True, full_families=not args.pilot_only)
    raw = canonical_bytes(report)
    if args.audit:
        require(args.output.read_bytes() == raw, "report does not reproduce")
    else:
        args.output.write_bytes(raw)
    print(f"remainder={report['exact_structural_remainder_orbit_total']} "
          f"pilot_owned={report['pilot']['owned']} "
          f"family_owned={report['full_family_scan']['owned']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
