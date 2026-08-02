#!/usr/bin/env python3
"""Fail-closed verifier for the complete order-seven rank-five theorem."""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KERNEL_SOURCE = ROOT / "research" / "fixtures" / "rank-five-kernels.json"
CENSUS_SOURCE = HERE / "order7-tetra-census.json"
RESULT_SOURCE = HERE / "order7-dim7-rational-gram-results.json"
FIXTURE = HERE / "order7-kernel-family-theorem.json"
EXPECTED_DIGESTS = {
    "kernels": "027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884",
    "census": "a9a05f50cf3db61cf104cd88c966f11064671d7b8027a83d065721e8b395d8b1",
    "results": "7d581bfaa5d02f2ee7642f998371f48c29cdb961c2cebc43d3d2d666632c1a17",
    "fixture": "1de37116d406f72abba33f85678be9f2eba38e71347a79c67bad5f159e2f1c16",
}
EXPECTED = {
    "kernels": 23, "physical": 31112, "orbits": 18026,
    "tetra": 14306, "residual": 3720, "targets": 44640,
    "rational": 44616, "symbolic": 24,
}
PAIRS = tuple(itertools.combinations(range(7), 2))
FRONTIERS = (None, *range(11))
SYMBOLIC_FRONTIERS = (None, 0, 3, 6)
HALF = Fraction(1, 2)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def raw_locked(path, digest, label):
    require(path.is_file(), f"missing {label}")
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == digest, f"{label} digest changed")
    try:
        return raw, json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"invalid ASCII JSON in {label}") from error


def canonical_json(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def fraction(value, label):
    require(isinstance(value, list) and len(value) == 2, f"bad {label} fraction")
    require(all(isinstance(x, int) and not isinstance(x, bool) for x in value),
            f"noninteger {label} fraction")
    require(value[1] > 0, f"nonpositive {label} denominator")
    result = Fraction(value[0], value[1])
    require([result.numerator, result.denominator] == value,
            f"uncanonical {label} fraction")
    return result


def dot(left, right):
    require(len(left) == len(right), "vector dimensions differ")
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def rational_unit(parameters):
    square = dot(parameters, parameters)
    denominator = 1 + square
    return ((1 - square) / denominator,) + tuple(2 * x / denominator for x in parameters)


def step_cost(left, right):
    correlation = dot(left, right)
    require(correlation != -1, "antipodal path step")
    return (1 - correlation) / (1 + correlation)


def canonical_lengths(multiplicity, odd):
    require(isinstance(multiplicity, int) and 0 <= odd <= multiplicity,
            "invalid physical incidence")
    return (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)


def path_ledger(kernel, row, frontier):
    paths = []
    for edge, ((u, v), multiplicity, odd) in enumerate(zip(PAIRS, kernel, row)):
        paths.extend((edge, occurrence, u, v, length)
                     for occurrence, length in enumerate(canonical_lengths(multiplicity, odd)))
    require(len(paths) == 11, "rank-five path count changed")
    if frontier is not None:
        require(isinstance(frontier, int) and 0 <= frontier < 11,
                "invalid frontier coordinate")
        edge, occurrence, u, v, length = paths[frontier]
        paths[frontier] = edge, occurrence, u, v, length + 2
    return tuple(paths)


def key(record):
    return record["kernel"], tuple(record["row"]), record["frontier"]


def determinant(matrix):
    work = [list(row) for row in matrix]
    result = Fraction(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        value = work[column][column]
        result *= value
        for row in range(column + 1, len(work)):
            scale = work[row][column] / value
            for index in range(column, len(work)):
                work[row][index] -= scale * work[column][index]
    return result


def audit_psd(matrix, label):
    size = len(matrix)
    require(size and all(len(row) == size for row in matrix), f"bad {label} size")
    require(all(matrix[i][j] == matrix[j][i] for i in range(size) for j in range(size)),
            f"asymmetric {label}")
    require(all(matrix[i][i] == 1 for i in range(size)), f"bad {label} diagonal")
    for width in range(1, size + 1):
        for indices in itertools.combinations(range(size), width):
            minor = tuple(tuple(matrix[i][j] for j in indices) for i in indices)
            require(determinant(minor) >= 0, f"non-PSD {label}")


def audit_sources(kernels, census, results):
    order_seven = tuple(tuple(record["code"]) for record in kernels["kernels"]
                        if record["n"] == 7)
    require(len(order_seven) == EXPECTED["kernels"], "order-seven kernel source changed")
    checks = (("kernel_total", "kernels"), ("physical_total", "physical"),
              ("orbit_total", "orbits"), ("tetra_certified_total", "tetra"),
              ("tetra_residual_total", "residual"), ("frontier_target_total", "targets"))
    require(all(census[field] == EXPECTED[name] for field, name in checks),
            "order-seven census counts changed")
    require(tuple(tuple(row["code"]) for row in census["kernels"]) == order_seven,
            "census kernel selection differs from source")
    require(results["source_census_sha256"] == EXPECTED_DIGESTS["census"],
            "results point to another census")
    require(results["complete_source_cover"] is True and results["full_theorem"] is False,
            "raw result status changed")
    require(results["target_total"] == EXPECTED["targets"] and
            results["exact_certificate_total"] == EXPECTED["rational"] and
            results["finite_unresolved_total"] == EXPECTED["symbolic"],
            "raw result partition changed")
    require(len(results["records"]) == EXPECTED["targets"], "raw result width changed")
    return {row["kernel"]: tuple(row["code"]) for row in census["kernels"]}


def audit_rational(source, kernel):
    require(source["exact_dnn_le_4"] is True and source["witness"] is not None,
            "rational target lacks source witness")
    witness = source["witness"]
    branch_parameters = tuple(tuple(fraction(x, "branch") for x in row)
                              for row in witness["branches"])
    require(len(branch_parameters) == 7 and all(len(row) == 6 for row in branch_parameters),
            "branch stereographic dimensions changed")
    branches = tuple(rational_unit(row) for row in branch_parameters)
    paths = path_ledger(kernel, tuple(source["row"]), source["frontier"])
    require(source["lengths"] == [path[4] for path in paths], "rational lengths changed")
    require(len(witness["internals"]) == 11, "rational internal ledger changed")
    total = Fraction(0)
    for (_, _, u, v, length), raw_internal in zip(paths, witness["internals"]):
        parameters = tuple(tuple(fraction(x, "internal") for x in row)
                           for row in raw_internal)
        require(len(parameters) == length - 1 and all(len(row) == 6 for row in parameters),
                "internal stereographic dimensions changed")
        chain = [branches[u], *(rational_unit(row) for row in parameters)]
        chain.append(branches[v] if length % 2 == 0 else tuple(-x for x in branches[v]))
        total += sum((step_cost(left, right) for left, right in zip(chain, chain[1:])),
                     Fraction(0))
    require(total == fraction(witness["cost"], "cost") and total < 4,
            "strict rational cost changed")


def cycle_gram(single_signs):
    a, b, c = single_signs
    matrix = [[Fraction(int(i == j)) for j in range(4)] for i in range(4)]
    for u, v, value in ((0, 1, -a * HALF), (1, 2, -b * HALF),
                        (2, 3, -c * HALF), (3, 0, -HALF)):
        matrix[u][v] = matrix[v][u] = value
    return tuple(tuple(row) for row in matrix)


def branch_gram(single_signs):
    a, b, c = single_signs
    base = cycle_gram(single_signs)
    assignment = ((0, 1), (2, c), (1, 1), (1, b), (2, 1), (0, a), (3, 1))
    return tuple(tuple(Fraction(si * sj) * base[i][j] for j, sj in assignment)
                 for i, si in assignment)


def encoded_matrix(matrix):
    return [[[x.numerator, x.denominator] for x in row] for row in matrix]


def closure_record(source):
    signs = tuple(1 if source["row"][edge] == 0 else -1 for edge in (4, 11, 8))
    return {
        "kernel": source["kernel"], "row": source["row"],
        "frontier": source["frontier"], "lengths": source["lengths"],
        "method": "exact_cycle_support_gram",
        "single_edge_order": ["05", "23", "14"],
        "single_signs": list(signs),
        "base_cycle_order": ["05", "23", "14", "6"],
        "base_gram": encoded_matrix(cycle_gram(signs)),
        "branch_gram": encoded_matrix(branch_gram(signs)),
        "cost": [4, 1],
    }


def build_fixture(census, results):
    unresolved = [record for record in results["records"] if not record["exact_dnn_le_4"]]
    require(len(unresolved) == EXPECTED["symbolic"], "unresolved source partition changed")
    return {
        "schema": "rank-five-order-seven-kernel-family-theorem-v1",
        "theorem_scope": "all 23 order-seven kernels and all physical parity families",
        "source_digests": {name: EXPECTED_DIGESTS[name]
                           for name in ("kernels", "census", "results")},
        "counts": EXPECTED,
        "frontier_policy": "canonical plus all eleven one-path length-plus-two frontiers",
        "closure_records": [closure_record(record) for record in unresolved],
    }


def parse_matrix(raw, size, label):
    matrix = tuple(tuple(fraction(x, label) for x in row) for row in raw)
    require(len(matrix) == size and all(len(row) == size for row in matrix),
            f"bad {label} order")
    return matrix


def audit_symbolic(record, source, kernel):
    require(record["kernel"] == 80 and record["frontier"] in SYMBOLIC_FRONTIERS,
            "symbolic key left the K80 cycle-support frontier")
    require(source["exact_dnn_le_4"] is False and source["witness"] is None,
            "symbolic key was not a raw obstruction")
    paths = path_ledger(kernel, tuple(record["row"]), record["frontier"])
    require(record["lengths"] == source["lengths"] == [path[4] for path in paths],
            "symbolic path ledger changed")
    signs = tuple(record["single_signs"])
    require(record["single_edge_order"] == ["05", "23", "14"] and
            record["base_cycle_order"] == ["05", "23", "14", "6"],
            "cycle-support orders changed")
    require(signs == tuple(1 if record["row"][edge] == 0 else -1
                           for edge in (4, 11, 8)), "sign-switch transport changed")
    base = parse_matrix(record["base_gram"], 4, "base Gram")
    gram = parse_matrix(record["branch_gram"], 7, "branch Gram")
    require(base == cycle_gram(signs) and gram == branch_gram(signs),
            "stored cycle-support Gram changed")
    audit_psd(base, "base Gram")
    audit_psd(gram, "branch Gram")

    total = Fraction(0)
    singles = {0, 3, 6}
    for index, (_, _, u, v, length) in enumerate(paths):
        transformed = gram[u][v] if length % 2 == 0 else -gram[u][v]
        if index in singles:
            require(transformed == 1, "single support path is not zero-cost")
            path_cost = Fraction(0)
        elif length & 1:
            require(length == 1 and transformed == HALF, "odd doubled path changed")
            path_cost = Fraction(1, 3)
        else:
            require(length == 2 and transformed == -HALF, "even doubled path changed")
            midpoint = ((Fraction(1), HALF, -HALF),
                        (HALF, Fraction(1), HALF),
                        (-HALF, HALF, Fraction(1)))
            audit_psd(midpoint, f"path {index} midpoint Gram")
            path_cost = Fraction(2, 3)
        total += path_cost
    require(total == 4 and record["cost"] == [4, 1], "symbolic equality cost changed")


def audit_fixture(fixture, census, results, kernels_by_number):
    require(fixture == build_fixture(census, results), "fixture differs from fresh reconstruction")
    require(fixture["counts"] == EXPECTED, "fixture counts changed")
    expected = {(record["kernel"], tuple(record["row"]), frontier)
                for record in census["residuals"] for frontier in FRONTIERS}
    require(len(expected) == EXPECTED["targets"], "exact target universe changed")
    source_records = {}
    for record in results["records"]:
        require(key(record) not in source_records, "duplicate raw result key")
        source_records[key(record)] = record
    require(set(source_records) == expected, "raw keys have omissions or extras")
    closures = {}
    for record in fixture["closure_records"]:
        require(key(record) not in closures, "duplicate symbolic closure key")
        closures[key(record)] = record
    missing = {target for target, record in source_records.items()
               if not record["exact_dnn_le_4"]}
    require(set(closures) == missing, "symbolic keys differ from raw missing keys")
    require({target[2] for target in missing} == set(SYMBOLIC_FRONTIERS),
            "symbolic frontier support changed")
    require(all(sum(target[2] == frontier for target in missing) == 6
                for frontier in SYMBOLIC_FRONTIERS), "symbolic frontier multiplicity changed")

    methods = {"strict_rational_path_vectors": 0, "exact_cycle_support_gram": 0}
    for target in sorted(expected, key=repr):
        source = source_records[target]
        kernel = kernels_by_number[source["kernel"]]
        if source["exact_dnn_le_4"]:
            audit_rational(source, kernel)
            methods["strict_rational_path_vectors"] += 1
        else:
            audit_symbolic(closures[target], source, kernel)
            methods["exact_cycle_support_gram"] += 1
    require(methods == {"strict_rational_path_vectors": EXPECTED["rational"],
                        "exact_cycle_support_gram": EXPECTED["symbolic"]},
            "certificate partition changed")

    for residual in census["residuals"]:
        canonical = (residual["kernel"], tuple(residual["row"]), None)
        require(canonical in source_records, "canonical target is uncovered")
        for frontier in range(11):
            target = (residual["kernel"], tuple(residual["row"]), frontier)
            require(target in source_records, "one-coordinate descendant is uncovered")
        if canonical in closures:
            require(all(((canonical[0], canonical[1], frontier) in closures) ==
                        (frontier in SYMBOLIC_FRONTIERS)
                        for frontier in FRONTIERS),
                    "K80 symbolic/rational descendant cover changed")
    return methods, missing


def hostile_mutations(fixture, census, results, kernels_by_number):
    attacks = []

    def add(name, mutate):
        candidate = copy.deepcopy(fixture)
        mutate(candidate)
        attacks.append((name, candidate))

    add("delete closure", lambda x: x["closure_records"].pop())
    add("duplicate closure", lambda x: x["closure_records"].append(copy.deepcopy(x["closure_records"][0])))
    add("forge rational count", lambda x: x["counts"].__setitem__("rational", 44617))
    add("change parity row", lambda x: x["closure_records"][0]["row"].__setitem__(4, 1))
    add("change frontier", lambda x: x["closure_records"][0].__setitem__("frontier", 1))
    add("change sign transport", lambda x: x["closure_records"][0]["single_signs"].__setitem__(0, -1))
    add("change base Gram", lambda x: x["closure_records"][0]["base_gram"][0].__setitem__(1, [0, 1]))
    add("change branch Gram", lambda x: x["closure_records"][0]["branch_gram"][0].__setitem__(5, [0, 1]))
    add("change path cost", lambda x: x["closure_records"][0].__setitem__("cost", [3, 1]))
    add("change results lock", lambda x: x["source_digests"].__setitem__("results", "0" * 64))
    for name, candidate in attacks:
        try:
            audit_fixture(candidate, census, results, kernels_by_number)
        except (RuntimeError, KeyError, IndexError, TypeError, ZeroDivisionError):
            continue
        raise RuntimeError(f"hostile mutation accepted: {name}")
    return len(attacks)


def load_sources(check_fixture=True):
    _, kernels = raw_locked(KERNEL_SOURCE, EXPECTED_DIGESTS["kernels"], "kernel fixture")
    _, census = raw_locked(CENSUS_SOURCE, EXPECTED_DIGESTS["census"], "tetra census")
    _, results = raw_locked(RESULT_SOURCE, EXPECTED_DIGESTS["results"], "Gram results")
    fixture = None
    if check_fixture:
        _, fixture = raw_locked(FIXTURE, EXPECTED_DIGESTS["fixture"], "theorem fixture")
    return kernels, census, results, fixture


def regenerate():
    kernels, census, results, _ = load_sources(False)
    audit_sources(kernels, census, results)
    FIXTURE.write_bytes(canonical_json(build_fixture(census, results)))
    print(hashlib.sha256(FIXTURE.read_bytes()).hexdigest())


def main():
    if sys.argv[1:] == ["--regenerate"]:
        regenerate()
        return
    require(not sys.argv[1:], "usage: verifier.py [--regenerate]")
    kernels, census, results, fixture = load_sources()
    kernels_by_number = audit_sources(kernels, census, results)
    methods, missing = audit_fixture(fixture, census, results, kernels_by_number)
    attacks = hostile_mutations(fixture, census, results, kernels_by_number)
    print("order-seven rank-five kernel-family theorem: exact audit passed")
    print("kernels=23 physical=31112 orbits=18026 tetra_certified=14306 residual=3720")
    print(f"all_length_targets=44640 rational={methods['strict_rational_path_vectors']} "
          f"symbolic_K80={methods['exact_cycle_support_gram']}")
    print("exact_missing_keys=K80:24 parity_rows=6 frontiers=canonical,0,3,6")
    print(f"hostile_mutations_rejected={attacks} verified_missing={len(missing)}")


if __name__ == "__main__":
    main()
