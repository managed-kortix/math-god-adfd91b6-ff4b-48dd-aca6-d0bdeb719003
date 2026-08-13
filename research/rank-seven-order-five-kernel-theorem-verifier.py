#!/usr/bin/env python3
"""Fail-closed exact verifier for rank-seven kernels of order five."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "research" / "fixtures" / "rank-seven-kernel-frontier-census.json"
RESULTS = ROOT / "research" / "fixtures" / "rank-seven-order-five-rational-gram-results.json"
PROOF = ROOT / "positive-square-energy" / "heptacyclic-general" / "rank-seven-order-five-kernel-theorem.md"
K4_PACKET = ROOT / "positive-square-energy" / "tetracyclic-general" / "four-vertex-kernels-dnn.md"
SOURCE_SHA256 = "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5"
RESULTS_SHA256 = "585c46ba7d514fded9031c98e77e61218e5b886ef6a9765eccb3c5833dd00b73"
PROOF_SHA256 = "8f405804831f6c1ec3134a5018d498159d53f6809d8eb6eb5ebb55f0eb2702ef"
K4_PACKET_SHA256 = "06afa6bb5a4f6439842b9edb0f1ea9913b85c1b42aed15668287baa43c0f5213"
BUDGET = Fraction(6)
PAIR_ORDER = tuple(itertools.combinations(range(5), 2))
EXPECTED_KERNELS = 233
EXPECTED_PHYSICAL = 132774
EXPECTED_ORBITS = 109342
EXPECTED_RESIDUALS = 15
FRONTIERS = (None, *range(11))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("ascii")


def locked_json(path, digest, label):
    require(path.is_file(), f"missing {label}")
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == digest, f"{label} digest changed")
    value = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(value), f"{label} is not canonical JSON")
    return value


def exact_int(value, label, minimum=None):
    require(type(value) is int, f"noninteger {label}")
    if minimum is not None:
        require(value >= minimum, f"negative {label}")
    return value


def exact_fraction(value, label):
    require(type(value) is list and len(value) == 2, f"malformed {label}")
    numerator = exact_int(value[0], label)
    denominator = exact_int(value[1], label, 1)
    result = Fraction(numerator, denominator)
    require(value == [result.numerator, result.denominator], f"uncanonical {label}")
    return result


def sparse_edges(code):
    require(type(code) is list and len(code) == 10, "malformed order-five kernel")
    return tuple((u, v, exact_int(value, "multiplicity", 0))
                 for (u, v), value in zip(PAIR_ORDER, code) if value)


def relabel_row(edges, row, permutation):
    edge_index = {(u, v): index for index, (u, v, _) in enumerate(edges)}
    return tuple(row[edge_index[tuple(sorted((permutation[u], permutation[v])))]]
                 for u, v, _ in edges)


def automorphisms(edges):
    multiplicity = {(u, v): value for u, v, value in edges}
    return tuple(permutation for permutation in itertools.permutations(range(5))
                 if all(multiplicity.get(tuple(sorted((permutation[u], permutation[v]))), 0) == value
                        for u, v, value in edges))


def coarse_residual(edges, row):
    adjacency = [[] for _ in range(5)]
    for index, (u, v, multiplicity) in enumerate(edges):
        odd = row[index]
        exact_int(odd, "odd count", 0)
        require(odd <= multiplicity, "odd count exceeds multiplicity")
        weight = 18 * multiplicity + (10 - 13 * odd if odd else 0)
        adjacency[u].append((v, odd != 0, weight))
        adjacency[v].append((u, odd != 0, weight))
    order = sorted(range(5), key=lambda vertex: (
        -sum(required for _, required, _ in adjacency[vertex]), -len(adjacency[vertex]), vertex))
    colors = [-1] * 5
    colors[order[0]] = 0

    def visit(position, used, cost):
        if cost > 180:
            return False
        if position == 5:
            return True
        vertex = order[position]
        for color in range(min(used + 1, 4)):
            added = 0
            for other, required, weight in adjacency[vertex]:
                if colors[other] < 0:
                    continue
                if required and color == colors[other]:
                    break
                if color != colors[other]:
                    added += weight
            else:
                colors[vertex] = color
                if visit(position + 1, max(used, color + 1), cost + added):
                    colors[vertex] = -1
                    return True
                colors[vertex] = -1
        return False

    return not visit(1, 1, 0)


def enumerate_residuals(source):
    require(source["schema"] == "rank-seven-loopless-no-cut-kernels-v2", "source schema changed")
    selected = [(index, sparse_edges(record["code"]))
                for index, record in enumerate(source["kernels"], 1)
                if exact_int(record["n"], "kernel order") == 5]
    require(len(selected) == EXPECTED_KERNELS, "order-five kernel count changed")
    residuals = []
    physical_total = orbit_total = 0
    for kernel, edges in selected:
        require(sum(value for _, _, value in edges) == 11, "physical path count changed")
        group = automorphisms(edges)
        require(group, "empty automorphism group")
        orbit_sizes = {}
        for row in itertools.product(*(range(value + 1) for _, _, value in edges)):
            representative = min(relabel_row(edges, row, permutation) for permutation in group)
            orbit_sizes[representative] = orbit_sizes.get(representative, 0) + 1
        physical_total += sum(orbit_sizes.values())
        orbit_total += len(orbit_sizes)
        residuals.extend((kernel, row, orbit_sizes[row]) for row in sorted(orbit_sizes)
                         if coarse_residual(edges, row))
    require(physical_total == EXPECTED_PHYSICAL, "physical parity total changed")
    require(orbit_total == EXPECTED_ORBITS, "parity orbit total changed")
    require(len(residuals) == EXPECTED_RESIDUALS, "coarse residual total changed")
    return dict(selected), tuple(residuals)


def canonical_lengths(multiplicity, odd):
    require(type(multiplicity) is int and type(odd) is int and 0 <= odd <= multiplicity,
            "invalid canonical row")
    return ((1,) + (3,) * (odd - 1) if odd else ()) + (2,) * (multiplicity - odd)


def path_ledger(edges, row, coordinate=None):
    paths = []
    for edge, ((u, v, multiplicity), odd) in enumerate(zip(edges, row)):
        paths.extend((edge, occurrence, u, v, length)
                     for occurrence, length in enumerate(canonical_lengths(multiplicity, odd)))
    require(len(paths) == 11, "frontier width changed")
    if coordinate is not None:
        exact_int(coordinate, "coordinate", 0)
        require(coordinate < 11, "coordinate out of range")
        edge, occurrence, u, v, length = paths[coordinate]
        paths[coordinate] = edge, occurrence, u, v, length + 2
    return tuple(paths)


def dot(left, right):
    require(len(left) == len(right), "vector dimensions differ")
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def unit(parameters):
    square = dot(parameters, parameters)
    denominator = 1 + square
    return ((1 - square) / denominator,) + tuple(2 * value / denominator for value in parameters)


def step_cost(left, right):
    correlation = dot(left, right)
    require(-1 < correlation <= 1, "invalid Gram step")
    return (1 - correlation) / (1 + correlation)


def audit_rational(record, edges):
    require(record["exact_dnn_le_6"] is True and type(record["witness"]) is dict,
            "missing rational certificate")
    coordinate = record["coordinate"]
    require(coordinate is None or type(coordinate) is int, "malformed coordinate")
    row = tuple(exact_int(value, "parity entry", 0) for value in record["row"])
    paths = path_ledger(edges, row, coordinate)
    require(record["lengths"] == [path[4] for path in paths], "stored lengths changed")
    witness = record["witness"]
    require(set(witness) == {"denominator", "cost", "branches", "internals"},
            "rational witness fields changed")
    exact_int(witness["denominator"], "search denominator", 1)
    branches = tuple(unit(tuple(exact_fraction(value, "branch parameter") for value in raw))
                     for raw in witness["branches"])
    require(len(branches) == 5 and all(len(vector) == 5 for vector in branches),
            "branch Gram dimensions changed")
    require(len(witness["internals"]) == 11, "internal path ledger changed")
    total = Fraction(0)
    for (_, _, u, v, length), raw_path in zip(paths, witness["internals"]):
        parameters = tuple(tuple(exact_fraction(value, "internal parameter") for value in raw)
                           for raw in raw_path)
        require(len(parameters) == length - 1, "internal vector count changed")
        chain = [branches[u], *(unit(raw) for raw in parameters)]
        chain.append(branches[v] if length % 2 == 0 else tuple(-value for value in branches[v]))
        total += sum((step_cost(left, right) for left, right in zip(chain, chain[1:])), Fraction(0))
    require(total == exact_fraction(witness["cost"], "stored cost"), "certificate cost changed")
    require(total <= BUDGET, "rational certificate exceeds six")
    return total


def audit_structural(records, edges):
    require(len(edges) == 10 and sorted(value for _, _, value in edges) == [1] * 9 + [2],
            "K269 is not K5 with one doubled edge")
    doubled_index = next(index for index, edge in enumerate(edges) if edge[2] == 2)
    doubled_paths = [index for index, path in enumerate(path_ledger(edges, records[0][0]))
                     if path[0] == doubled_index]
    require(len(doubled_paths) == 2, "doubled path ledger changed")
    expected = {((1,) * 10, None), ((1,) * 10, doubled_paths[1]),
                ((1,) * 9 + (2,), None), ((1,) * 9 + (2,), doubled_paths[1])}
    actual = {(row, record["coordinate"]) for row, record in records}
    require(actual == expected, "structural K5-plus-path targets changed")
    for row, record in records:
        paths = path_ledger(edges, row, record["coordinate"])
        require(record["lengths"] == [path[4] for path in paths], "structural lengths changed")
        require(record["exact_dnn_le_6"] is False and record["witness"] is None,
                "structural target was mislabeled DNN")
        require(paths[doubled_paths[0]][4] == 1 and paths[doubled_paths[1]][4] >= 2,
                "structural complement is not an actual K5 plus a nonempty path tree")
    # The nonempty internal path and every tree rooted on it form one induced
    # tree (surplus -1). Its induced complement is an attached K5 packet, whose
    # proved surplus is strictly greater than 1. The sum is strictly positive.
    return len(records)


def validate_scope(scope):
    expected = {
        "rank": 7,
        "kernel_order": 5,
        "kernel_count": 233,
        "residual_orbits": 15,
        "frontier": "canonical plus each of 11 physical coordinates",
        "subdivisions": "all simple fixed-parity coordinatewise descendants",
        "attachments": "arbitrary finite rooted trees at branch or subdivision vertices",
        "conclusion": "s+(G)>=|V(G)|",
        "excluded": ["rank-seven kernel orders 6 through 12", "multiple positive-rank blocks",
                     "all connected heptacyclic graphs", "higher-order theorem claims"],
    }
    require(scope == expected, "theorem scope changed or widened")


def scope_manifest():
    return {
        "rank": 7, "kernel_order": 5, "kernel_count": 233, "residual_orbits": 15,
        "frontier": "canonical plus each of 11 physical coordinates",
        "subdivisions": "all simple fixed-parity coordinatewise descendants",
        "attachments": "arbitrary finite rooted trees at branch or subdivision vertices",
        "conclusion": "s+(G)>=|V(G)|",
        "excluded": ["rank-seven kernel orders 6 through 12", "multiple positive-rank blocks",
                     "all connected heptacyclic graphs", "higher-order theorem claims"],
    }


def audit(source_digest=SOURCE_SHA256, results_digest=RESULTS_SHA256, proof_digest=PROOF_SHA256,
          packet_digest=K4_PACKET_SHA256, payload=None, scope=None):
    require(source_digest == SOURCE_SHA256 and results_digest == RESULTS_SHA256,
            "dependency digest policy changed")
    require(proof_digest == PROOF_SHA256, "proof digest policy changed")
    require(packet_digest == K4_PACKET_SHA256, "K4 packet digest policy changed")
    require(hashlib.sha256(PROOF.read_bytes()).hexdigest() == proof_digest, "proof note changed")
    require(hashlib.sha256(K4_PACKET.read_bytes()).hexdigest() == packet_digest,
            "attached-K4 packet proof changed")
    source = locked_json(SOURCE, source_digest, "rank-seven kernel source")
    results = locked_json(RESULTS, results_digest, "Gram results") if payload is None else payload
    validate_scope(scope_manifest() if scope is None else scope)
    kernels, residuals = enumerate_residuals(source)
    residual_keys = {(kernel, row) for kernel, row, _ in residuals}
    require(len(residual_keys) == 15, "residual keys are not unique")
    require(set(results) == {"schema", "status", "source_sha256", "budget", "residual_orbits",
                             "frontiers_per_orbit", "target_total", "exact_dnn_le_6_total",
                             "full_theorem", "records"}, "result fields changed")
    require(results["schema"] == "rank-seven-order-five-rational-gram-search-v1",
            "result schema changed")
    require(results["source_sha256"] == SOURCE_SHA256 and results["budget"] == [6, 1],
            "result dependency or budget changed")
    require(results["residual_orbits"] == 15 and results["frontiers_per_orbit"] == 12
            and results["target_total"] == 180 and results["exact_dnn_le_6_total"] == 176,
            "frontier partition changed")
    require(results["full_theorem"] is False, "fixture improperly claims a theorem")
    records = {}
    for record in results["records"]:
        require(type(record) is dict, "malformed target record")
        require(set(record) == {"kernel", "order_kernel", "row", "coordinate", "lengths",
                                "numerical_cost", "exact_dnn_le_6", "witness"},
                "target record fields changed")
        kernel = exact_int(record["kernel"], "kernel number", 1)
        require(exact_int(record["order_kernel"], "order-local kernel", 1) == kernel - 54,
                "order-local kernel index changed")
        require(type(record["numerical_cost"]) is float and math.isfinite(record["numerical_cost"]),
                "nonfinite search diagnostic")
        row = tuple(exact_int(value, "row entry", 0) for value in record["row"])
        coordinate = record["coordinate"]
        require(coordinate is None or type(coordinate) is int, "malformed frontier coordinate")
        key = kernel, row, coordinate
        require(key not in records, "duplicate target key")
        records[key] = record
    expected = {(kernel, row, coordinate) for kernel, row in residual_keys for coordinate in FRONTIERS}
    require(set(records) == expected, "target keys do not equal residual orbit Cartesian frontier")
    structural = []
    maximum = Fraction(0)
    for (kernel, row, _), record in records.items():
        if record["exact_dnn_le_6"] is True:
            maximum = max(maximum, audit_rational(record, kernels[kernel]))
        else:
            structural.append((row, record))
    require(len(structural) == 4 and all(record["kernel"] == 269 for _, record in structural),
            "structural residual set changed")
    audit_structural(structural, kernels[269])
    return residuals, maximum


def expect_rejected(action, label):
    try:
        action()
    except (KeyError, RuntimeError, TypeError, ValueError, ZeroDivisionError):
        return
    raise RuntimeError(f"hostile mutation accepted: {label}")


def hostile_checks():
    baseline = locked_json(RESULTS, RESULTS_SHA256, "Gram results")
    checks = []

    def mutate(label, action):
        changed = deepcopy(baseline)
        action(changed)
        checks.append((label, lambda changed=changed: audit(payload=changed)))

    mutate("deleted target", lambda value: value["records"].pop())
    mutate("forged exact total", lambda value: value.__setitem__("exact_dnn_le_6_total", 180))
    mutate("promoted fixture theorem", lambda value: value.__setitem__("full_theorem", True))
    mutate("widened budget", lambda value: value.__setitem__("budget", [7, 1]))
    mutate("float numerator", lambda value: value["records"][0]["witness"]["cost"].__setitem__(0, 1.0))
    mutate("zero denominator", lambda value: value["records"][0]["witness"]["cost"].__setitem__(1, 0))
    mutate("forged cost", lambda value: value["records"][0]["witness"].__setitem__("cost", [0, 1]))
    mutate("nonfinite diagnostic", lambda value: value["records"][0].__setitem__("numerical_cost", math.nan))
    mutate("wrong local index", lambda value: value["records"][0].__setitem__("order_kernel", 1))
    mutate("unknown witness field", lambda value: value["records"][0]["witness"].__setitem__("note", 1))
    mutate("structural mislabeled DNN", lambda value: next(
        record for record in value["records"] if not record["exact_dnn_le_6"]).__setitem__(
            "exact_dnn_le_6", True))
    widened = scope_manifest()
    widened["excluded"] = widened["excluded"][:-1]
    checks.append(("higher-order overclaim", lambda: audit(scope=widened)))
    checks.extend((("source digest", lambda: audit(source_digest="0" * 64)),
                   ("results digest", lambda: audit(results_digest="0" * 64)),
                   ("proof digest", lambda: audit(proof_digest="0" * 64)),
                   ("K4 packet digest", lambda: audit(packet_digest="0" * 64))))
    for label, action in checks:
        expect_rejected(action, label)
    return len(checks)


def report(residuals, maximum, mutations):
    orbit_lines = ";".join(f"K{kernel}:{','.join(map(str, row))}:size={size}"
                           for kernel, row, size in residuals)
    return "\n".join((
        "rank-seven order-five kernel theorem: exact fail-closed audit passed",
        "kernels=233 physical_parity_rows=132774 parity_orbits=109342 coarse_residual_orbits=15",
        "residual_orbits=" + orbit_lines,
        "canonical_plus_11_coordinate_targets=180 rational_Gram=176 structural_K269=4",
        f"largest_verified_rational_excess={maximum}",
        "scope=all simple subdivisions; arbitrary rooted trees at branch and subdivision vertices",
        "conclusion=s+(G)>=|V(G)| for rank-seven kernel order five only",
        "nonclaim=orders 6-12, multiblock graphs, all connected heptacyclic graphs, higher orders",
        f"rejected_hostile_mutations={mutations}",
    )) + "\n"


def main():
    residuals, maximum = audit()
    mutations = hostile_checks()
    require(mutations == 16, "hostile mutation count changed")
    output = report(residuals, maximum, mutations)
    if sys.flags.optimize == 0 and "--emit" not in sys.argv:
        completed = subprocess.run((sys.executable, "-O", str(Path(__file__).resolve()), "--emit"),
                                   check=False, capture_output=True, text=True)
        require(completed.returncode == 0, "python -O verifier failed")
        require(completed.stderr == "", "python -O verifier wrote stderr")
        require(completed.stdout == output, "normal and python -O output differ")
    sys.stdout.write(output)


if __name__ == "__main__":
    main()
