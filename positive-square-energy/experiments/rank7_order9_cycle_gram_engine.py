#!/usr/bin/env python3
"""Exact verifier for historical order-nine cycle-space Gram witnesses.

The historical numerical producer is absent from the repository.  This module
therefore authenticates the surviving source, reports, and witness streams and
replays every accepted certificate over :class:`fractions.Fraction`; it does
not claim to reproduce the missing optimizer or its rejected classifications.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
import math
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "rank7_order9_unowned_stratifier.py"
SOURCE_REPORT = HERE / "rank7_order9_typed_sos_owner_manifest.json"
SOURCE_STREAM = HERE / "rank7_order9_after_sos_remainder.jsonl.xz"
ORDER = 9
PATH_COUNT = 15
TARGETS_PER_ROW = 16
BUDGET = Fraction(6)
F = Fraction


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


def pair(value):
    return [value.numerator, value.denominator]


def strict_json(raw, label):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    try:
        return json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(
                              RuntimeError(f"nonstandard constant in {label}: {value}")))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot parse {label}") from error


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


@lru_cache(maxsize=None)
def exact_cycle_projector(endpoints):
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


def paths_and_types(edges, row):
    signed = [[F() for _ in range(ORDER)] for _ in range(ORDER)]
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
    signed_degrees = [sum(row) for row in signed]
    keys = [(signed_degrees[u], tuple(sorted(incident[u], reverse=True)))
            for u in range(ORDER)]
    dictionary = {key: index for index, key in enumerate(sorted(set(keys)))}
    return (tuple(tuple(row) for row in signed), tuple(paths), tuple(keys),
            tuple(dictionary[key] for key in keys))


def exact_cycle_core(paths):
    projector = exact_cycle_projector(tuple((u, v) for _, _, u, v, _ in paths))
    incidence = [[F() for _ in paths] for _ in range(ORDER)]
    for column, (_, _, u, v, length) in enumerate(paths):
        incidence[u][column] = 1
        incidence[v][column] = -1 if length & 1 else 1
    projected = [[sum(incidence[u][left] * projector[left][right]
                      for left in range(len(paths)))
                  for right in range(len(paths))] for u in range(ORDER)]
    return tuple(tuple(sum(x * y for x, y in zip(projected[u], projected[v]))
                       for v in range(ORDER)) for u in range(ORDER))



def canonical_type(key):
    signed_degree, incident = key
    return int(signed_degree), tuple(sorted(incident))


def historical_type_ids(type_keys):
    canonical = sorted({canonical_type(key) for key in type_keys})
    dictionary = {key: index for index, key in enumerate(canonical)}
    return tuple(dictionary[canonical_type(key)] for key in type_keys)


def serialized_types(type_keys):
    """Return the canonical local-type order used by the stored witnesses."""
    canonical = sorted({canonical_type(key) for key in type_keys})
    return [[signed_degree, [list(value) for value in incident]]
            for signed_degree, incident in canonical]


def exact_cost(signed, cycle_core, paths, type_ids, parameters, cycle_weight):
    x = [[(parameters[type_ids[u]][0] if u == v else F()) +
          parameters[type_ids[u]][1] * signed[u][v]
          for v in range(ORDER)] for u in range(ORDER)]
    core = [[sum(x[u][w] * x[v][w] for w in range(ORDER)) +
             cycle_weight * cycle_core[u][v]
             for v in range(ORDER)] for u in range(ORDER)]
    normalizer = max(core[u][u] for u in range(ORDER))
    require(normalizer > 0, "zero Gram normalizer")
    total = F()
    for _, _, u, v, length in paths:
        correlation = core[u][v] / normalizer
        transformed = -correlation if length & 1 else correlation
        require(-1 <= transformed <= 1, "exact correlation escaped [-1,1]")
        if transformed == -1:
            return None, normalizer
        total += (1 - transformed) / (length * (1 + transformed))
    return total, normalizer


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


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rational_pair(raw, label, maximum_denominator=None):
    require(isinstance(raw, list) and len(raw) == 2 and
            all(type(value) is int for value in raw),
            f"malformed rational pair: {label}")
    numerator, denominator = raw
    require(denominator > 0 and
            (maximum_denominator is None or denominator <= maximum_denominator) and
            math.gcd(abs(numerator), denominator) == 1,
            f"noncanonical rational pair: {label}")
    value = F(numerator, denominator)
    require(pair(value) == raw, f"noncanonical rational pair: {label}")
    return value


def authenticate_source():
    """Authenticate the complete after-SOS stream and index every exact row."""
    base = load("rank7_order9_cycle_source", BASE_PATH)
    report, report_sha = base.strict_canonical_json(SOURCE_REPORT,
                                                     "SOS owner report")
    source_info = report["updated_remainder_stream"]
    require(source_info["path"] == SOURCE_STREAM.name and
            file_sha256(SOURCE_STREAM) == source_info["artifact_sha256"],
            "after-SOS source artifact changed")
    digest = hashlib.sha256()
    records = {}
    physical = 0
    with lzma.open(SOURCE_STREAM, "rb") as stream:
        for raw in stream:
            record = strict_json(raw, SOURCE_STREAM.name)
            require(raw == canonical_bytes(record) and len(record) == 5 and
                    type(record[0]) is int and record[0] not in records and
                    type(record[4]) is int and record[4] > 0,
                    "noncanonical or duplicate after-SOS source row")
            records[record[0]] = record
            physical += record[4]
            digest.update(raw)
    require(len(records) == source_info["record_total"] and
            digest.hexdigest() == source_info["raw_sha256"],
            "after-SOS source identity changed")
    kernels = base.kernel_dictionary(base.load_scan_engine())
    strata = Counter()
    physical_strata = Counter()
    for record in records.values():
        expected_global, edges = kernels[record[2]]
        require(record[1] == expected_global,
                "after-SOS source kernel reference changed")
        key = family(edges, tuple(record[3]))
        strata[key] += 1
        physical_strata[key] += record[4]
    return (base, kernels, report_sha, source_info, records, physical,
            strata, physical_strata)


def replay_owner_stream(path, target, expected, expected_report,
                        authenticated_source=None):
    """Authenticate and exactly replay one historical witness stream."""
    if authenticated_source is None:
        authenticated_source = authenticate_source()
    (_, kernels, source_report_sha, source_info, source_records,
     source_physical, strata, physical_strata) = authenticated_source
    report_raw = expected_report.read_bytes()
    report = strict_json(report_raw, expected_report.name)
    require(hashlib.sha256(report_raw).hexdigest() == expected["report_sha256"],
            "historical report identity changed")
    require(report["schema"] == expected["schema"] and
            report["full_theorem"] is False and
            report["source_report_sha256"] == source_report_sha and
            report["source_stream"] == source_info and
            report["scanned_remainder_total"] == len(source_records) and
            report["scanned_remainder_physical_total"] == source_physical and
            report["target_family"] == expected["target_family"] and
            strata[target] == expected["target_family"]["orbit_total"] and
            physical_strata[target] ==
            expected["target_family"]["physical_total"] and
            report["gram"] == HISTORICAL_GRAM and
            report["claim_boundary"] == HISTORICAL_CLAIM_BOUNDARY,
            "historical report semantics changed")

    maximum_denominator = report["gram"]["maximum_denominator"]
    require(type(maximum_denominator) is int and maximum_denominator > 0,
            "invalid historical denominator bound")
    digest = hashlib.sha256()
    total = physical = 0
    seen = set()
    denominators = Counter()
    with lzma.open(path, "rb") as stream:
        for raw in stream:
            payload = strict_json(raw, path.name)
            require(raw == canonical_bytes(payload) and len(payload) == 4,
                    "noncanonical owner payload")
            record, certificate, numerical, stored_types = payload
            require(len(record) == 5 and source_records.get(record[0]) == record,
                    "owner record does not match authenticated source")
            require(record[0] not in seen and len(certificate) == 5 and
                    certificate[0] == record[0] and certificate[1] is True,
                    "duplicate owner or bad owner schema")
            require(type(numerical) in (int, float) and not isinstance(numerical, bool)
                    and math.isfinite(numerical),
                    "invalid numerical diagnostic")
            seen.add(record[0])
            expected_global, edges = kernels[record[2]]
            require(expected_global == record[1] and
                    family(edges, tuple(record[3])) == target,
                    "owner kernel or family changed")
            signed, paths, type_keys, _ = paths_and_types(edges,
                                                            tuple(record[3]))
            type_ids = historical_type_ids(type_keys)
            require(serialized_types(type_keys) == stored_types,
                    "owner local types changed")
            require(isinstance(certificate[3], list) and
                    len(certificate[3]) == max(type_ids) + 1,
                    "invalid owner Gram parameter count")
            parameters = tuple(
                (rational_pair(values[0], f"parameter[{index}][0]",
                               maximum_denominator),
                 rational_pair(values[1], f"parameter[{index}][1]",
                               maximum_denominator))
                for index, values in enumerate(certificate[3])
                if isinstance(values, list) and len(values) == 2)
            require(len(parameters) == len(certificate[3]),
                    "malformed owner Gram parameters")
            cycle_weight = rational_pair(certificate[4], "cycle weight",
                                         maximum_denominator)
            require(cycle_weight >= 0, "negative cycle weight")
            stored_cost = rational_pair(certificate[2], "exact cost")
            cost, _ = exact_cost(signed, exact_cycle_core(paths), paths,
                                 type_ids, parameters, cycle_weight)
            require(cost is not None and cost <= BUDGET and cost == stored_cost,
                    "owner exact cost mismatch")
            denominators.update([cycle_weight.denominator] +
                                [value.denominator for values in parameters
                                 for value in values])
            digest.update(raw)
            total += 1
            physical += record[4]

    require(total == expected["owner_total"], "owner total changed")
    result = {"record_total": total, "physical_total": physical,
              "target_total": total * TARGETS_PER_ROW,
              "raw_sha256": digest.hexdigest(),
              "artifact_sha256": file_sha256(path)}
    require(result == expected["owner_stream"] and
            report["owner_stream"] == {"path": path.name,
                                       "record_total": total,
                                       "raw_sha256": result["raw_sha256"],
                                       "artifact_sha256": result["artifact_sha256"]} and
            report["owned_orbit_total"] == total and
            report["owned_physical_total"] == physical and
            report["owned_target_total"] == total * TARGETS_PER_ROW and
            report["remaining_target_family_total"] ==
            expected["target_family"]["orbit_total"] - total and
            report["used_denominators"] ==
            {str(key): value for key, value in sorted(denominators.items())},
            "owner/report accounting changed")
    return result


HISTORICAL_GRAM = {
    "cycle_projector": "P_cycle=I-B^T(BB^T)^-1B on physical-path coordinates",
    "exact_replay": "all typed entries and w are rounded to bounded rational fractions before exact projector and cost acceptance",
    "formula": "H=XX^T+w A P_cycle A^T; G=H/M+diag(1-diag(H)/M)",
    "local_type": "(signed degree, sorted incident (multiplicity,odd-count) pairs)",
    "maximum_denominator": 256,
    "proposal": "one deterministic binary64 Powell start at D0=1,D1=1/2,w=exp(-2)",
    "psd_proof": "XX^T and w(A P_cycle)(A P_cycle)^T are Gram squares for w>=0; diagonal completion is a nonnegative coordinate-square sum",
    "signed_incidence": "A has entries 1 and (-1)^L at physical-path endpoints",
    "typed_feature": "X=D0+D1*S, with D0,D1 constant on exact local types",
}
HISTORICAL_CLAIM_BOUNDARY = (
    "only records persisted in the owner stream are theorem-owned; all other "
    "records remain unclassified"
)
HISTORICAL_LANES = {
    "third": {
        "target": ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1),
                   (3, 3, 6), 4, 2),
        "owners": HERE / "rank7_order9_third_family_cycle_gram_owners.jsonl.xz",
        "report": HERE / "rank7_order9_third_family_cycle_gram_lane.json",
        "schema": "rank-seven-order-nine-third-family-cycle-gram-lane-v1",
        "report_sha256": "af5a3ae40631936c8b7360cd376838c340e62e0c55d01734f110072f20b83585",
        "owner_total": 631,
        "target_family": {
            "bundle_types": [3, 3, 6], "cycle_rank": 4,
            "multiplicity_partition": [2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            "orbit_total": 17507, "physical_total": 20496,
            "triangle_total": 2,
        },
        "owner_stream": {
            "artifact_sha256": "9955f46b32f0b714f6c3b6b19778cd93f72bdb05ccd3c6e881a79bab288a77bf",
            "physical_total": 748,
            "raw_sha256": "2f35c2a76ce054be0d5b2ed18c0bfd77f163c1429af35ca48b91313ba77d0154",
            "record_total": 631, "target_total": 10096,
        },
    },
    "fourth": {
        "target": ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1),
                   (4, 3, 5), 4, 2),
        "owners": HERE / "rank7_order9_fourth_family_cycle_gram_owners.jsonl.xz",
        "report": HERE / "rank7_order9_fourth_family_cycle_gram_lane.json",
        "schema": "rank-seven-order-nine-fourth-family-cycle-gram-lane-v1",
        "report_sha256": "3f5d3c168b7b13ec58321063de52f0e387fd2b1ae6fbd919ee5aecfbba4404ce",
        "owner_total": 1036,
        "target_family": {
            "bundle_types": [4, 3, 5], "cycle_rank": 4,
            "multiplicity_partition": [2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            "orbit_total": 16183, "physical_total": 19053,
            "triangle_total": 2,
        },
        "owner_stream": {
            "artifact_sha256": "6423fd051a754ba0c810f79a51e83391926c2049ccf20c8cef0ad4c2a4e3867d",
            "physical_total": 1283,
            "raw_sha256": "a347d2d7891609156692d0bf0614783d79a9b84c6f4e0902ef6672f1cb4c96f5",
            "record_total": 1036, "target_total": 16576,
        },
    },
}


def audit_historical(names):
    authenticated_source = authenticate_source()
    result = {}
    all_indices = set()
    third_report_hash = HISTORICAL_LANES["third"]["report_sha256"]
    for name in names:
        lane = HISTORICAL_LANES[name]
        replay = replay_owner_stream(lane["owners"], lane["target"], lane,
                                     lane["report"], authenticated_source)
        report = strict_json(lane["report"].read_bytes(), lane["report"].name)
        if name == "third":
            require(report["prior_lane"] == {
                        "owned_orbit_total": 1018,
                        "remainder_total": 270374,
                        "report_sha256": "79a0fd27298125d9ac1a776b9b144f5cafb3e55e03d0c4615eb5c0d3f026b921",
                    } and report["remaining_remainder_total"] == 269743,
                    "third report historical metadata changed")
        elif name == "fourth":
            require(report["prior_lane"] == {
                        "owned_orbit_total": 631,
                        "remainder_total": 269743,
                        "report_sha256": third_report_hash,
                    } and report["remaining_remainder_total"] == 268707,
                    "fourth report chain metadata changed")
        indices = set()
        with lzma.open(lane["owners"], "rb") as stream:
            for raw in stream:
                record = strict_json(raw, lane["owners"].name)[0]
                require(record[0] not in indices and record[0] not in all_indices,
                        "historical owner streams overlap")
                indices.add(record[0])
        all_indices.update(indices)
        result[name] = replay
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-historical", nargs="*",
                        choices=sorted(HISTORICAL_LANES),
                        help="exact-replay committed historical witness streams")
    args = parser.parse_args()
    require(args.audit_historical is not None,
            "this reconstruction is a verifier; use --audit-historical")
    names = args.audit_historical or sorted(HISTORICAL_LANES)
    result = audit_historical(names)
    print(canonical_bytes(result).decode("ascii"), end="")


if __name__ == "__main__":
    main()
