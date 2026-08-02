#!/usr/bin/env python3
"""Fail-closed verifier for the complete order-six rank-five theorem."""

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
CENSUS_SOURCE = HERE / "order6-tetra-census.json"
RESULT_SOURCE = HERE / "order6-dim6-rational-gram-results.json"
FIXTURE = HERE / "order6-kernel-family-theorem.json"
EXPECTED_DIGESTS = {
    "kernels": "027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884",
    "census": "de4278bd890c99fa6c06e62c1641eb2f0ce3a3d4603427d2b80d24c674bb9089",
    "results": "6a46d2acebe60015c0071332f1152bb3da5c9b893e7fc22943a38162db37487e",
    "fixture": "69b236b014aef58c037c610ca01fa62ad82601f7bb34153939ec4ddd3b5f364d",
}
EXPECTED = {
    "kernels": 38, "physical": 23208, "orbits": 12810,
    "tetra": 11312, "residual": 1498, "targets": 16478,
    "rational": 16451, "symbolic": 18, "structural": 9,
}
PAIRS = tuple(itertools.combinations(range(6), 2))
FRONTIERS = (None, *range(10))


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
    require(len(paths) == 10, "rank-five path count changed")
    if frontier is not None:
        require(isinstance(frontier, int) and 0 <= frontier < 10,
                "invalid frontier coordinate")
        edge, occurrence, u, v, length = paths[frontier]
        paths[frontier] = edge, occurrence, u, v, length + 2
    return tuple(paths)


def key(number, row, frontier):
    return number, tuple(row), frontier


def determinant(matrix):
    work = [list(row) for row in matrix]
    result = Fraction(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column]), None)
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
    require(all(determinant(tuple(tuple(matrix[i][j] for j in indices) for i in indices)) >= 0
                for width in range(1, size + 1)
                for indices in itertools.combinations(range(size), width)),
            f"non-PSD {label}")


def expected_keys(census):
    result = {key(record["kernel"], record["row"], frontier)
              for record in census["residuals"] for frontier in FRONTIERS}
    require(len(result) == EXPECTED["targets"], "target key universe changed")
    return result


def audit_sources(kernels, census, results):
    order_six = tuple(tuple(record["code"]) for record in kernels["kernels"]
                      if record["n"] == 6)
    require(len(order_six) == EXPECTED["kernels"], "order-six kernel source changed")
    require(census["kernel_total"] == EXPECTED["kernels"], "census kernel count changed")
    require(census["physical_total"] == EXPECTED["physical"], "physical count changed")
    require(census["orbit_total"] == EXPECTED["orbits"], "orbit count changed")
    require(census["tetra_certified_total"] == EXPECTED["tetra"], "tetra count changed")
    require(census["tetra_residual_total"] == EXPECTED["residual"], "residual count changed")
    require(census["frontier_target_total"] == EXPECTED["targets"], "frontier count changed")
    require(tuple(tuple(row["code"]) for row in census["kernels"]) == order_six,
            "census kernel selection differs from source")
    require(results["source_census_sha256"] == EXPECTED_DIGESTS["census"],
            "results point to another census")
    require(results["complete_source_cover"] is True, "result source cover is incomplete")
    require(results["target_total"] == EXPECTED["targets"], "result target count changed")
    require(results["exact_certificate_total"] == EXPECTED["rational"],
            "result rational count changed")
    require(results["finite_unresolved_total"] == 27, "result failure count changed")
    require(len(results["records"]) == EXPECTED["targets"], "result record count changed")
    return {row["kernel"]: tuple(row["code"]) for row in census["kernels"]}


def audit_rational(source, kernel):
    require(source["exact_dnn_le_4"] is True and source["witness"] is not None,
            "rational target lacks source witness")
    witness = source["witness"]
    branches_p = tuple(tuple(fraction(x, "branch") for x in row)
                       for row in witness["branches"])
    require(len(branches_p) == 6 and all(len(row) == 5 for row in branches_p),
            "branch stereographic dimensions changed")
    branches = tuple(rational_unit(row) for row in branches_p)
    paths = path_ledger(kernel, tuple(source["row"]), source["frontier"])
    require([path[4] for path in paths] == source["lengths"], "rational lengths changed")
    require(len(witness["internals"]) == 10, "internal ledger changed")
    total = Fraction(0)
    for (_, _, u, v, length), raw_internal in zip(paths, witness["internals"]):
        parameters = tuple(tuple(fraction(x, "internal") for x in row)
                           for row in raw_internal)
        require(len(parameters) == length - 1 and all(len(row) == 5 for row in parameters),
                "internal stereographic dimensions changed")
        chain = [branches[u], *(rational_unit(row) for row in parameters)]
        chain.append(branches[v] if length % 2 == 0 else tuple(-x for x in branches[v]))
        total += sum((step_cost(left, right) for left, right in zip(chain, chain[1:])),
                     Fraction(0))
    require(total == fraction(witness["cost"], "cost"), "stored rational cost changed")
    require(total < 4, "rational certificate is not strict")


def parse_gram(record):
    gram = tuple(tuple(fraction(x, "symbolic Gram") for x in row)
                 for row in record["gram"])
    require(len(gram) == 6, "symbolic Gram order changed")
    audit_psd(gram, "symbolic Gram")
    return gram


def audit_symbolic(record, source, kernel):
    require(record["kernel"] in (55, 61), "symbolic target has wrong kernel")
    require(source["exact_dnn_le_4"] is False and source["witness"] is None,
            "symbolic target was not a source obstruction")
    paths = path_ledger(kernel, tuple(record["row"]), record["frontier"])
    require(record["lengths"] == source["lengths"] == [path[4] for path in paths],
            "symbolic path ledger changed")
    gram = parse_gram(record)
    total = Fraction(0)
    for path_index, (_, _, u, v, length) in enumerate(paths):
        transformed = gram[u][v] if length % 2 == 0 else -gram[u][v]
        if transformed == 1:
            path_cost = Fraction(0)
        elif length == 1 and transformed == Fraction(1, 2):
            path_cost = Fraction(1, 3)
        elif length == 2 and transformed == Fraction(-1, 2):
            midpoint_gram = ((Fraction(1), Fraction(1, 2), Fraction(-1, 2)),
                             (Fraction(1, 2), Fraction(1), Fraction(1, 2)),
                             (Fraction(-1, 2), Fraction(1, 2), Fraction(1)))
            audit_psd(midpoint_gram, f"symbolic path {path_index}")
            path_cost = Fraction(2, 3)
        else:
            raise RuntimeError("symbolic path has no verified exact realization")
        total += path_cost
    require(total == 4 and record["cost"] == [4, 1], "symbolic equality cost changed")


def physical_subdivision(paths):
    branches = tuple(("branch", vertex) for vertex in range(6))
    vertices = set(branches)
    edges = set()
    internals = {}
    for index, (_, _, u, v, length) in enumerate(paths):
        internal = tuple(("internal", index, step) for step in range(1, length))
        internals[index] = internal
        chain = (branches[u], *internal, branches[v])
        vertices.update(internal)
        edges.update(frozenset((left, right)) for left, right in zip(chain, chain[1:]))
    require(all(len(edge) == 2 for edge in edges), "physical subdivision has a loop")
    return branches, vertices, edges, internals


def induced_edges(vertices, edges):
    return {edge for edge in edges if edge <= vertices}


def connected(vertices, edges):
    if not vertices:
        return False
    reached = {next(iter(vertices))}
    while True:
        expanded = reached | {vertex for edge in edges if edge & reached for vertex in edge}
        expanded &= vertices
        if expanded == reached:
            return reached == vertices
        reached = expanded


def descendants(parent, root):
    result = {root}
    while True:
        expanded = result | {vertex for vertex, predecessor in parent.items() if predecessor in result}
        if expanded == result:
            return result
        result = expanded


def audit_structural(record, source, kernel):
    require(record["kernel"] == 71, "structural target is not K71")
    require(source["exact_dnn_le_4"] is False and source["witness"] is None,
            "structural target was not a source obstruction")
    paths = path_ledger(kernel, tuple(record["row"]), record["frontier"])
    require(record["lengths"] == source["lengths"] == [path[4] for path in paths],
            "structural path ledger changed")
    require(record["opening"] == {
        "deleted_branches": [1, 2], "deleted_paths": [3, 4, 5, 6],
        "retained_branches": [0, 3, 4, 5], "retained_paths": [0, 1, 2, 7, 8, 9],
    }, "K71 opening changed")
    require(record["frontier"] in (None, 5, 6), "K71 structural descendant is unsafe")

    branches, vertices, edges, internals = physical_subdivision(paths)
    retained_paths = set(record["opening"]["retained_paths"])
    require(all(paths[index][4] == 1 for index in retained_paths),
            "retained K71 K4 path was subdivided")
    retained = {branches[v] for v in record["opening"]["retained_branches"]}
    deleted = vertices - retained
    retained_edges = induced_edges(retained, edges)
    clique_edges = {frozenset((branches[u], branches[v]))
                    for u, v in itertools.combinations(record["opening"]["retained_branches"], 2)}
    require(retained_edges == clique_edges, "K71 retained territory is not an induced actual K4")
    deleted_edges = induced_edges(deleted, edges)
    require(connected(deleted, deleted_edges), "K71 deleted territory is disconnected")
    require(len(deleted_edges) == len(deleted), "K71 deleted territory is not unicyclic")
    require(set(record["opening"]["deleted_paths"]) ==
            {index for index, path in enumerate(paths) if set(path[2:4]) & {1, 2}},
            "K71 opening omits a deleted-branch path")
    cycle_core = {branches[1], branches[2], *internals[4]}
    require(len(cycle_core) == 3 and len(induced_edges(cycle_core, edges)) == 3,
            "K71 favorable triangle was not reconstructed")

    owner_side = {vertex: ("retained" if vertex in retained else "deleted") for vertex in vertices}
    parent = {}
    augmented_vertices = set(vertices)
    augmented_edges = set(edges)
    for owner in sorted(vertices, key=repr):
        width = 2 + (len(repr(owner)) % 3)
        previous = owner
        for depth in range(1, width + 1):
            child = ("rooted", owner, depth)
            parent[child] = previous
            augmented_vertices.add(child)
            augmented_edges.add(frozenset((previous, child)))
            previous = child
    deleted_augmented = set(deleted)
    retained_augmented = set(retained)
    for owner, side in owner_side.items():
        owned = descendants(parent, owner) - vertices
        (retained_augmented if side == "retained" else deleted_augmented).update(owned)
    require(deleted_augmented | retained_augmented == augmented_vertices and
            not deleted_augmented & retained_augmented,
            "owner-exact rooted-tree partition is not exhaustive")
    require(all((child in deleted_augmented) == (predecessor in deleted_augmented)
                for child, predecessor in parent.items()),
            "a rooted-tree descendant crossed its owner's territory")
    require(induced_edges(retained, augmented_edges) == clique_edges,
            "rooted trees changed the actual K4 core")
    deleted_augmented_edges = induced_edges(deleted_augmented, augmented_edges)
    require(connected(deleted_augmented, deleted_augmented_edges) and
            len(deleted_augmented_edges) == len(deleted_augmented),
            "rooted trees changed the favorable unicyclic territory")


def gram_from_groups(groups, matrix):
    return [[[matrix[groups[i]][groups[j]].numerator,
              matrix[groups[i]][groups[j]].denominator] for j in range(6)]
            for i in range(6)]


def closure_record(source):
    base = {name: source[name] for name in ("kernel", "row", "frontier", "lengths")}
    if source["kernel"] in (55, 61):
        s03 = 1 if source["row"][2] == 0 else -1
        s12 = 1 if source["row"][5] == 0 else -1
        matrices = {
            55: {
                (1, 1): ((1, Fraction(-1, 2), Fraction(-1, 2), Fraction(-1, 2)),
                         (Fraction(-1, 2), 1, Fraction(-1, 2), Fraction(-1, 2)),
                         (Fraction(-1, 2), Fraction(-1, 2), 1, 1),
                         (Fraction(-1, 2), Fraction(-1, 2), 1, 1)),
                (1, -1): ((1, Fraction(-1, 2), Fraction(-1, 2), Fraction(-1, 2)),
                          (Fraction(-1, 2), 1, Fraction(1, 2), Fraction(-1, 2)),
                          (Fraction(-1, 2), Fraction(1, 2), 1, 0),
                          (Fraction(-1, 2), Fraction(-1, 2), 0, 1)),
                (-1, -1): ((1, Fraction(-1, 2), Fraction(1, 2), Fraction(-1, 2)),
                           (Fraction(-1, 2), 1, Fraction(1, 2), Fraction(-1, 2)),
                           (Fraction(1, 2), Fraction(1, 2), 1, -1),
                           (Fraction(-1, 2), Fraction(-1, 2), -1, 1)),
            },
            61: {
                (1, 1): ((1, Fraction(-1, 2), Fraction(-1, 2), Fraction(-1, 2)),
                         (Fraction(-1, 2), 1, Fraction(-1, 2), 1),
                         (Fraction(-1, 2), Fraction(-1, 2), 1, Fraction(-1, 2)),
                         (Fraction(-1, 2), 1, Fraction(-1, 2), 1)),
                (1, -1): ((1, Fraction(1, 2), Fraction(-1, 2), Fraction(-1, 2)),
                          (Fraction(1, 2), 1, Fraction(-1, 2), 0),
                          (Fraction(-1, 2), Fraction(-1, 2), 1, Fraction(-1, 2)),
                          (Fraction(-1, 2), 0, Fraction(-1, 2), 1)),
                (-1, -1): ((1, Fraction(-1, 2), Fraction(-1, 2), Fraction(-1, 2)),
                           (Fraction(-1, 2), 1, Fraction(-1, 2), 1),
                           (Fraction(-1, 2), Fraction(-1, 2), 1, Fraction(-1, 2)),
                           (Fraction(-1, 2), 1, Fraction(-1, 2), 1)),
            },
        }
        matrix = tuple(tuple(Fraction(x) for x in row)
                       for row in matrices[source["kernel"]][s03, s12])
        groups = ((0, 1, 1, 0, 2, 3) if source["kernel"] == 55 else
                  (0, 1, 1, 0, 2, 3))
        if s03 == -1 or s12 == -1:
            signs = (1, 1, s12, s03, 1, 1)
            raw = gram_from_groups(groups, matrix)
            gram = [[[Fraction(*raw[i][j]) * signs[i] * signs[j]].pop()
                     for j in range(6)] for i in range(6)]
            base["gram"] = [[[x.numerator, x.denominator] for x in row] for row in gram]
        else:
            base["gram"] = gram_from_groups(groups, matrix)
        base.update({"method": "symbolic_equality", "cost": [4, 1]})
    elif source["kernel"] == 71:
        base.update({
            "method": "structural_triangle_plus_attached_k4",
            "opening": {"deleted_branches": [1, 2], "deleted_paths": [3, 4, 5, 6],
                        "retained_branches": [0, 3, 4, 5],
                        "retained_paths": [0, 1, 2, 7, 8, 9]},
        })
    else:
        raise RuntimeError("unknown unresolved target")
    return base


def build_fixture(census, results):
    unresolved = [row for row in results["records"] if not row["exact_dnn_le_4"]]
    require(len(unresolved) == 27, "unresolved source partition changed")
    return {
        "schema": "rank-five-order-six-kernel-family-theorem-v1",
        "theorem_scope": "all 38 order-six kernels and all physical parity families",
        "source_digests": {name: EXPECTED_DIGESTS[name]
                           for name in ("kernels", "census", "results")},
        "counts": EXPECTED,
        "frontier_policy": "canonical plus all ten one-path length-plus-two frontiers",
        "closure_records": [closure_record(row) for row in unresolved],
    }


def audit_fixture(fixture, census, results, kernels_by_number):
    require(fixture["schema"] == "rank-five-order-six-kernel-family-theorem-v1",
            "fixture schema changed")
    require(fixture["counts"] == EXPECTED, "fixture counts changed")
    require(fixture["source_digests"] == {name: EXPECTED_DIGESTS[name]
                                         for name in ("kernels", "census", "results")},
            "fixture source locks changed")
    require(fixture == build_fixture(census, results), "fixture differs from fresh reconstruction")

    source_records = {}
    duplicates = set()
    for row in results["records"]:
        target = key(row["kernel"], row["row"], row["frontier"])
        if target in source_records:
            duplicates.add(target)
        source_records[target] = row
    target_keys = expected_keys(census)
    require(not duplicates, "duplicate result keys")
    require(set(source_records) == target_keys, "result keys have omissions or extras")
    closure_records = {key(row["kernel"], row["row"], row["frontier"]): row
                       for row in fixture["closure_records"]}
    require(len(closure_records) == len(fixture["closure_records"]), "duplicate closure key")
    missing = target_keys - {target for target, row in source_records.items()
                             if row["exact_dnn_le_4"]}
    require(set(closure_records) == missing, "closure keys differ from exact missing keys")
    require({number: sum(target[0] == number for target in missing) for number in (55, 61, 71)}
            == {55: 9, 61: 9, 71: 9}, "missing-key kernel counts changed")

    methods = {"strict_rational_path_vectors": 0, "symbolic_equality": 0,
               "structural_triangle_plus_attached_k4": 0}
    for target in sorted(target_keys, key=repr):
        source = source_records[target]
        kernel = kernels_by_number[source["kernel"]]
        if source["exact_dnn_le_4"]:
            audit_rational(source, kernel)
            methods["strict_rational_path_vectors"] += 1
        else:
            record = closure_records[target]
            methods[record["method"]] += 1
            if record["method"] == "symbolic_equality":
                audit_symbolic(record, source, kernel)
            else:
                audit_structural(record, source, kernel)
    require(methods == {"strict_rational_path_vectors": EXPECTED["rational"],
                        "symbolic_equality": EXPECTED["symbolic"],
                        "structural_triangle_plus_attached_k4": EXPECTED["structural"]},
            "certificate partition changed")

    method_by_key = {target: ("strict_rational_path_vectors" if source_records[target]["exact_dnn_le_4"]
                              else closure_records[target]["method"])
                     for target in target_keys}
    for record in census["residuals"]:
        number, row = record["kernel"], tuple(record["row"])
        for frontier in range(10):
            require(key(number, row, frontier) in method_by_key,
                    "one-coordinate descendant is uncovered")
        if number == 71 and key(number, row, None) in closure_records:
            require(all(method_by_key[key(number, row, frontier)] ==
                        ("structural_triangle_plus_attached_k4" if frontier in (None, 5, 6)
                         else "strict_rational_path_vectors") for frontier in FRONTIERS),
                    "K71 descendant cover changed")
    return methods, missing


def hostile_mutations(fixture, census, results, kernels_by_number):
    attacks = []

    def add(name, mutate):
        candidate = copy.deepcopy(fixture)
        mutate(candidate)
        attacks.append((name, candidate))

    add("delete closure", lambda x: x["closure_records"].pop())
    add("duplicate closure", lambda x: x["closure_records"].append(copy.deepcopy(x["closure_records"][0])))
    add("forge rational count", lambda x: x["counts"].__setitem__("rational", 16452))
    symbolic = next(i for i, row in enumerate(fixture["closure_records"])
                    if row["method"] == "symbolic_equality")
    structural = next(i for i, row in enumerate(fixture["closure_records"])
                      if row["method"] == "structural_triangle_plus_attached_k4")
    add("change symbolic Gram", lambda x: x["closure_records"][symbolic]["gram"][0].__setitem__(1, [0, 1]))
    add("change symbolic cost", lambda x: x["closure_records"][symbolic].__setitem__("cost", [3, 1]))
    add("change structural frontier", lambda x: x["closure_records"][structural].__setitem__("frontier", 0))
    add("omit deleted path", lambda x: x["closure_records"][structural]["opening"].__setitem__("deleted_paths", [3, 4, 5]))
    add("change retained branch", lambda x: x["closure_records"][structural]["opening"].__setitem__("retained_branches", [0, 2, 4, 5]))
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
    print("order-six rank-five kernel-family theorem: exact audit passed")
    print("kernels=38 physical=23208 orbits=12810 tetra_certified=11312 residual=1498")
    print(f"all_length_targets=16478 rational={methods['strict_rational_path_vectors']} "
          f"symbolic_K55_K61={methods['symbolic_equality']} "
          f"structural_K71={methods['structural_triangle_plus_attached_k4']}")
    print("exact_missing_keys=K55:9,K61:9,K71:9")
    print(f"hostile_mutations_rejected={attacks} verified_missing={len(missing)}")


if __name__ == "__main__":
    main()
