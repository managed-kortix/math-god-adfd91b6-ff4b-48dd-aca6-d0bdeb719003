#!/usr/bin/env python3
"""Close the nine order-eleven defect-transport failures by exact shared Grams."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
import math
import random
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import minimize


HERE = Path(__file__).resolve().parent
LANE_PATH = HERE / "rank7_order11_defect_transport_gram_lane.py"
SCAN_PATH = HERE / "rank7_order11_defect_transport_gram_lane.json"
FAILURES_PATH = HERE / "rank7_order11_defect_transport_gram_failures.jsonl.xz"
SOURCE_REMAINDER_PATH = HERE / "rank7_order11_after_defect_transport_remainder.jsonl.xz"
OWNER_PATH = HERE / "rank7_order11_leading_family_closure_owners.json.xz"
REMAINDER_PATH = HERE / "rank7_order11_after_leading_family_closure_remainder.jsonl.xz"
REPORT_PATH = HERE / "rank7_order11_leading_family_closure.json"
SCHEMA = "rank-seven-order-eleven-leading-family-closure-v1"
OWNER_SCHEMA = "rank-seven-order-eleven-leading-family-shared-gram-owners-v1"
EXPECTED_FAILURES = 9
EXPECTED_FAMILY = 319522
DENOMINATORS = (64, 128, 256, 512, 1024, 2048, 4096)
DIMENSION = 11
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


def strict_json(raw, label):
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), f"noncanonical JSON: {label}")
    return payload


def read_json(path, compressed=False):
    stored = path.read_bytes()
    raw = lzma.decompress(stored) if compressed else stored
    return (strict_json(raw, path.name), hashlib.sha256(raw).hexdigest(),
            hashlib.sha256(stored).hexdigest())


def write_json(path, payload, compressed=False):
    raw = canonical_bytes(payload)
    stored = lzma.compress(raw, preset=6) if compressed else raw
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(stored)
    temporary.replace(path)
    return {"path": path.name, "raw_sha256": hashlib.sha256(raw).hexdigest(),
            "artifact_sha256": hashlib.sha256(stored).hexdigest(),
            "bytes": len(stored)}


def load_lane():
    spec = importlib.util.spec_from_file_location("order11_closure_lane", LANE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load Gram lane")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LANE = load_lane()


def read_failures():
    records = []
    digest = hashlib.sha256()
    with lzma.open(FAILURES_PATH, "rb") as stream:
        for raw in stream:
            payload = strict_json(raw, FAILURES_PATH.name)
            require(isinstance(payload, list) and len(payload) == 4 and
                    payload[1][1] is False, "malformed failure record")
            records.append(payload)
            digest.update(raw)
    require(len(records) == EXPECTED_FAILURES, "failure total changed")
    return records, digest.hexdigest()


def collect_kernels(failures):
    wanted = {(item[0][1], item[0][2]) for item in failures}
    manifest, _ = LANE.strict_json(LANE.MANIFEST_PATH)
    wrapper = LANE.load("order11_closure_owner", LANE.OWNER_ENGINE_PATH)
    owner = wrapper.load_owner_engine()
    kernels = {}
    for chunk in manifest["chunks"]:
        header, records, _ = owner.stream_chunk(HERE / chunk["path"])
        for ledger in header["kernels"]:
            key = ledger["global_kernel"], ledger["order_kernel"]
            if key in wanted:
                kernels[key] = LANE.kernel_data(ledger)
        records.close()
    require(set(kernels) == wanted, "failure kernels changed")
    return kernels


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def normalized(vector):
    norm = math.sqrt(dot(vector, vector))
    require(norm > 1e-14, "zero numerical vector")
    return tuple(value / norm for value in vector)


def numerical_cost_gradient(flat, paths):
    raw = flat.reshape(LANE.ORDER, DIMENSION)
    norms = np.linalg.norm(raw, axis=1)
    vectors = raw / norms[:, None]
    total = 0.0
    gradient = np.zeros_like(vectors)
    for _, _, u, v, length in paths:
        correlation = float(vectors[u] @ vectors[v])
        sign = -1.0 if length & 1 else 1.0
        transformed = np.clip(sign * correlation, -1.0 + 1e-12, 1.0 - 1e-12)
        tangent = math.tan(math.acos(transformed) / (2.0 * length))
        total += length * tangent * tangent
        derivative = (-sign * tangent * (1.0 + tangent * tangent) /
                      math.sqrt(1.0 - transformed * transformed))
        gradient[u] += derivative * vectors[v]
        gradient[v] += derivative * vectors[u]
    gradient -= np.sum(gradient * vectors, axis=1)[:, None] * vectors
    gradient /= norms[:, None]
    return total, gradient.ravel()


def optimize(paths, seed, restarts=2, iterations=600):
    best = None
    for restart in range(restarts):
        initial = np.random.default_rng(seed + restart).normal(
            size=(LANE.ORDER, DIMENSION))
        proposal = minimize(
            numerical_cost_gradient, initial.ravel(), args=(paths,), jac=True,
            method="L-BFGS-B",
            options={"maxiter": iterations, "ftol": 1e-13, "gtol": 1e-9},
        )
        if best is None or proposal.fun < best.fun:
            best = proposal
    require(best is not None and best.fun < 6.0, "direct Gram search did not close row")
    return tuple(normalized(tuple(row)) for row in best.x.reshape(LANE.ORDER, DIMENSION))


def rotate_away_from_pole(vectors):
    _, first, sign = max((min(1.0 + sign * row[coordinate] for row in vectors),
                          coordinate, sign)
                         for coordinate in range(DIMENSION) for sign in (-1.0, 1.0))
    order = (first,) + tuple(index for index in range(DIMENSION) if index != first)
    return tuple(tuple((sign if position == 0 else 1.0) * row[coordinate]
                       for position, coordinate in enumerate(order)) for row in vectors)


def stereographic(vector, denominator):
    scale = 1.0 + vector[0]
    require(abs(scale) > 1e-10, "stereographic pole")
    return tuple(F(round(value / scale * denominator), denominator)
                 for value in vector[1:])


def rational_unit(parameters):
    square = dot(parameters, parameters)
    denominator = 1 + square
    return ((1 - square) / denominator,) + tuple(
        2 * value / denominator for value in parameters)


def slerp(left, right, fraction):
    correlation = max(-1.0, min(1.0, dot(left, right)))
    angle = math.acos(correlation)
    if angle < 1e-12:
        return left
    sine = math.sin(angle)
    return normalized(tuple((math.sin((1.0 - fraction) * angle) * x +
                             math.sin(fraction * angle) * y) / sine
                            for x, y in zip(left, right)))


def exact_step_cost(left, right):
    correlation = dot(left, right)
    require(correlation != -1, "antipodal rational step")
    return (1 - correlation) / (1 + correlation)


def exact_path(left, right, exact_left, exact_right, length, denominator):
    parameters = tuple(stereographic(slerp(left, right, step / length), denominator)
                       for step in range(1, length))
    chain = (exact_left,) + tuple(rational_unit(row) for row in parameters) + (exact_right,)
    cost = sum((exact_step_cost(a, b) for a, b in zip(chain, chain[1:])), F())
    return parameters, cost


def pair(value):
    return [value.numerator, value.denominator]


def encode_rows(rows):
    return [[[value.numerator, value.denominator] for value in row] for row in rows]


def decode_rows(rows):
    return tuple(tuple(F(*value) for value in row) for row in rows)


def rationalize(paths, vectors):
    vectors = rotate_away_from_pole(vectors)
    for denominator in DENOMINATORS:
        try:
            branch_parameters = tuple(stereographic(row, denominator) for row in vectors)
            branches = tuple(rational_unit(row) for row in branch_parameters)
            canonical = []
            extended = []
            base_costs = []
            extended_costs = []
            for _, _, u, v, length in paths:
                endpoint = vectors[v] if length % 2 == 0 else tuple(-x for x in vectors[v])
                exact_endpoint = (branches[v] if length % 2 == 0 else
                                  tuple(-x for x in branches[v]))
                inside, cost = exact_path(vectors[u], endpoint, branches[u],
                                          exact_endpoint, length, denominator)
                longer, longer_cost = exact_path(vectors[u], endpoint, branches[u],
                                                 exact_endpoint, length + 2, denominator)
                canonical.append(inside)
                extended.append(longer)
                base_costs.append(cost)
                extended_costs.append(longer_cost)
        except (RuntimeError, ZeroDivisionError):
            continue
        base = sum(base_costs, F())
        costs = (base,) + tuple(base - base_costs[index] + extended_costs[index]
                                for index in range(len(paths)))
        if max(costs) <= LANE.BUDGET:
            return {
                "denominator": denominator,
                "branches": encode_rows(branch_parameters),
                "canonical": [encode_rows(path) for path in canonical],
                "extended": [encode_rows(path) for path in extended],
                "frontier_costs": [pair(cost) for cost in costs],
            }
    raise RuntimeError("exact rationalization did not close row")


def verify_witness(paths, witness):
    denominator = witness["denominator"]
    require(denominator in DENOMINATORS, "unexpected witness denominator")
    branch_parameters = decode_rows(witness["branches"])
    canonical = tuple(decode_rows(path) for path in witness["canonical"])
    extended = tuple(decode_rows(path) for path in witness["extended"])
    require(len(branch_parameters) == LANE.ORDER and
            len(canonical) == len(extended) == LANE.PATH_COUNT,
            "witness dimensions changed")
    branches = tuple(rational_unit(row) for row in branch_parameters)
    costs = []
    for frontier in (None, *range(LANE.PATH_COUNT)):
        total = F()
        for index, ((_, _, u, v, length), base, longer) in enumerate(
                zip(paths, canonical, extended, strict=True)):
            parameters = longer if index == frontier else base
            require(len(parameters) == length - 1 + (2 if index == frontier else 0),
                    "path witness width changed")
            endpoint = branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])
            chain = (branches[u],) + tuple(rational_unit(row) for row in parameters) + (endpoint,)
            total += sum((exact_step_cost(a, b) for a, b in zip(chain, chain[1:])), F())
        require(total <= LANE.BUDGET, "exact frontier cost exceeds six")
        costs.append(pair(total))
    require(costs == witness["frontier_costs"], "stored frontier costs changed")


def make_owners(failures, kernels, progress=False):
    owners = []
    for position, failure in enumerate(failures):
        record = failure[0]
        kernel = kernels[record[1], record[2]]
        _, paths, _, _, family = LANE.paths_types_family(kernel, tuple(record[3]))
        vectors = optimize(paths, 1729 + 1009 * position)
        witness = rationalize(paths, vectors)
        verify_witness(paths, witness)
        owners.append({
            "source_index": record[0], "global_kernel": record[1],
            "order_kernel": record[2], "row": record[3],
            "orbit_size": record[4], "family": LANE.family_payload(family),
            "displaced_method": "defect-transport-typed-sos-gram",
            "owner_method": "direct-shared-rational-correlation-gram",
            "witness": witness,
        })
        if progress:
            print(f"closed={position + 1}/{len(failures)}", flush=True)
    return owners


def verify_owners(owners, failures, kernels):
    require(len(owners) == len(failures) == EXPECTED_FAILURES, "owner total changed")
    for owner, failure in zip(owners, failures, strict=True):
        record = failure[0]
        require([owner[key] for key in ("source_index", "global_kernel", "order_kernel",
                                        "row", "orbit_size")] == record,
                "owner identity changed")
        kernel = kernels[record[1], record[2]]
        _, paths, _, _, family = LANE.paths_types_family(kernel, tuple(record[3]))
        require(owner["family"] == LANE.family_payload(family), "owner family changed")
        verify_witness(paths, owner["witness"])


def write_remainder(owner_indices):
    digest = hashlib.sha256()
    total = physical = removed = removed_physical = 0
    temporary = REMAINDER_PATH.with_name(REMAINDER_PATH.name + ".tmp")
    with lzma.open(SOURCE_REMAINDER_PATH, "rb") as source, lzma.open(
            temporary, "wb", preset=1) as output:
        for raw in source:
            first_comma = raw.find(b",")
            require(raw.startswith(b"[") and first_comma > 1,
                    "malformed source remainder record")
            source_index = int(raw[1:first_comma])
            if source_index in owner_indices:
                record = strict_json(raw, SOURCE_REMAINDER_PATH.name)
                removed += 1
                removed_physical += record[4]
                continue
            output.write(raw)
            digest.update(raw)
            total += 1
    source_report, _, _ = read_json(SCAN_PATH)
    physical = (source_report["remaining_remainder_physical_total"] -
                removed_physical)
    temporary.replace(REMAINDER_PATH)
    require(removed == EXPECTED_FAILURES, "closure rows not found exactly once in remainder")
    return {"path": REMAINDER_PATH.name, "record_total": total,
            "physical_total": physical, "removed_record_total": removed,
            "removed_physical_total": removed_physical,
            "raw_sha256": digest.hexdigest(), "artifact_sha256": file_sha256(REMAINDER_PATH)}


def verify_remainder(owner_indices, expected):
    digest = hashlib.sha256()
    total = physical = removed = removed_physical = 0
    with lzma.open(SOURCE_REMAINDER_PATH, "rb") as source, lzma.open(
            REMAINDER_PATH, "rb") as actual:
        for raw in source:
            first_comma = raw.find(b",")
            require(raw.startswith(b"[") and first_comma > 1,
                    "malformed source remainder record")
            source_index = int(raw[1:first_comma])
            if source_index in owner_indices:
                record = strict_json(raw, SOURCE_REMAINDER_PATH.name)
                removed += 1
                removed_physical += record[4]
                continue
            require(actual.readline() == raw, "persisted closure remainder changed")
            digest.update(raw)
            total += 1
        require(actual.read(1) == b"", "closure remainder has trailing records")
    source_report, _, _ = read_json(SCAN_PATH)
    physical = (source_report["remaining_remainder_physical_total"] -
                removed_physical)
    observed = {"path": REMAINDER_PATH.name, "record_total": total,
                "physical_total": physical, "removed_record_total": removed,
                "removed_physical_total": removed_physical,
                "raw_sha256": digest.hexdigest(),
                "artifact_sha256": file_sha256(REMAINDER_PATH)}
    require(observed == expected, "closure remainder aggregate changed")


def report_payload(scan, scan_raw, failure_raw, failure_xz, owner_artifact,
                   remainder_artifact):
    prior_owned = scan["owned_orbit_total"]
    require(scan["target_family"]["orbit_total"] == EXPECTED_FAMILY and
            scan["remaining_target_family_total"] == EXPECTED_FAILURES and
            scan["updated_remainder_stream"]["artifact_sha256"] ==
            file_sha256(SOURCE_REMAINDER_PATH),
            "defect-transport scan boundary changed")
    return {
        "schema": SCHEMA, "full_theorem": False,
        "status": "leading-family-completely-closed",
        "scope": "all 319522 rows in the leading order-eleven defect-transport family",
        "authenticated_inputs": {
            "defect_transport_scan": {"path": SCAN_PATH.name, "raw_sha256": scan_raw},
            "failure_stream": {"path": FAILURES_PATH.name, "record_total": EXPECTED_FAILURES,
                               "raw_sha256": failure_raw, "artifact_sha256": failure_xz},
            "source_remainder": {"path": SOURCE_REMAINDER_PATH.name,
                                 "artifact_sha256": file_sha256(SOURCE_REMAINDER_PATH)},
        },
        "family_orbit_total": EXPECTED_FAMILY,
        "prior_defect_transport_owner_total": prior_owned,
        "shared_gram_rescue_owner_total": EXPECTED_FAILURES,
        "combined_family_owner_total": prior_owned + EXPECTED_FAILURES,
        "remaining_family_total": 0,
        "owner_precedence": ["defect-transport-typed-sos-gram",
                             "direct-shared-rational-correlation-gram"],
        "rescue_owner_artifact": owner_artifact,
        "updated_remainder_stream": remainder_artifact,
        "theorem_contract": {
            "canonical": "each stored rational path-chain Gram has exact total cost at most six",
            "coordinate_frontiers": "the same rational branch Gram has exact cost at most six after each one-path length-plus-two move",
            "all_length_lift": "canonical-plus-coordinate domination and fixed-parity path-cost monotonicity cover every path length of the prescribed parity",
            "rooted_tree_lift": "one-vertex DNN additivity assigns arbitrary rooted-tree attachments their tree Gram",
        },
        "claim_boundary": "the leading 319522-row family is completely theorem-owned; rows outside this family remain in the exact updated remainder",
    }


def run(audit=False, progress=False, existing_owners=False):
    scan, scan_raw, _ = read_json(SCAN_PATH)
    failures, failure_raw = read_failures()
    failure_xz = file_sha256(FAILURES_PATH)
    kernels = collect_kernels(failures)
    if audit:
        payload, owner_raw, owner_xz = read_json(OWNER_PATH, True)
        require(payload.get("schema") == OWNER_SCHEMA, "wrong owner schema")
        owners = payload.get("owners")
        verify_owners(owners, failures, kernels)
        owner_artifact = {"path": OWNER_PATH.name, "raw_sha256": owner_raw,
                          "artifact_sha256": owner_xz, "bytes": OWNER_PATH.stat().st_size}
        actual_report, _, _ = read_json(REPORT_PATH)
        verify_remainder({owner["source_index"] for owner in owners},
                         actual_report["updated_remainder_stream"])
        expected = report_payload(scan, scan_raw, failure_raw, failure_xz,
                                  owner_artifact, actual_report["updated_remainder_stream"])
        require(actual_report == expected, "closure report changed")
        return expected

    if existing_owners:
        payload, _, _ = read_json(OWNER_PATH, True)
        require(payload.get("schema") == OWNER_SCHEMA, "wrong owner schema")
        owners = payload.get("owners")
    else:
        owners = make_owners(failures, kernels, progress)
    verify_owners(owners, failures, kernels)
    owner_payload = {"schema": OWNER_SCHEMA, "owner_total": len(owners),
                     "owners": owners}
    owner_artifact = write_json(OWNER_PATH, owner_payload, True)
    remainder_artifact = write_remainder({owner["source_index"] for owner in owners})
    report = report_payload(scan, scan_raw, failure_raw, failure_xz,
                            owner_artifact, remainder_artifact)
    write_json(REPORT_PATH, report)
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--existing-owners", action="store_true")
    args = parser.parse_args()
    require(not (args.audit and args.existing_owners),
            "audit does not accept --existing-owners")
    report = run(args.audit, args.progress, args.existing_owners)
    print(json.dumps({"family": report["family_orbit_total"],
                      "rescued": report["shared_gram_rescue_owner_total"],
                      "remaining_family": report["remaining_family_total"],
                      "report_sha256": hashlib.sha256(canonical_bytes(report)).hexdigest()},
                     sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            ZeroDivisionError, lzma.LZMAError, json.JSONDecodeError) as error:
        raise SystemExit(f"order-eleven leading-family closure: FAIL CLOSED: {error}")
