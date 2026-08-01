#!/usr/bin/env python3
"""Fail-closed verifier for the non-K5-e order-five rank-five families.

The verifier is intentionally standalone.  It source-locks the kernel census,
tetrahedral census, exploratory exact-result source, and frozen theorem fixture;
reconstructs every key and path ledger; and checks every rational vector and
cost with Fraction arithmetic.  The four K35 equality targets and four K22
structural targets are reconstructed as physical subdivisions and checked as
induced territory partitions rather than accepted as metadata assertions.
"""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KERNEL_SOURCE = ROOT / "research" / "fixtures" / "rank-five-kernels.json"
CENSUS_SOURCE = HERE / "order5-tetra-census.json"
RESULT_SOURCE = HERE / "order5-dim4-rational-gram-results.json"
FIXTURE = HERE / "order5-kernel-family-theorem.json"
EXPECTED_DIGESTS = {
    "kernels": "027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884",
    "census": "27c57079e65f7e484412343b6c0887d3060990fd30fd2d2c7903af971d4f5ff5",
    "results": "9f09889c247d500f5aa0a5906663f5740b89b05239c27567e4b3b553e7eafeff",
    "fixture": "4d8b826b397dc269c7853b8bd386d00bf469282b52720b8dac96d850e9e616d8",
}
PAIRS = tuple(itertools.combinations(range(5), 2))
K5E_KEY = (32, (0, 1, 1, 1, 1, 1, 1, 1, 1, 1))
EXPECTED = {
    "kernels": 24, "physical": 6282, "orbits": 4238,
    "tetra": 4030, "residual": 208, "covered_rows": 207,
    "targets": 2070, "rational": 2062, "symbolic": 4, "structural": 4,
}


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
    require([result.numerator, result.denominator] == value, f"uncanonical {label} fraction")
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
    require(len(paths) == 9, "rank-five path count changed")
    if frontier is not None:
        require(isinstance(frontier, int) and 0 <= frontier < 9, "invalid frontier coordinate")
        edge, occurrence, u, v, length = paths[frontier]
        paths[frontier] = edge, occurrence, u, v, length + 2
    return tuple(paths)


def key(number, row, frontier):
    return number, tuple(row), frontier


def expected_keys(census):
    result = set()
    for number, row in census["search_target_keys"]:
        for frontier in (None, *range(9)):
            result.add(key(number, row, frontier))
    require(len(result) == EXPECTED["targets"], "all-length key universe changed")
    require(all((number, row) != K5E_KEY for number, row, _ in result),
            "excluded all-odd K5-e entered theorem keys")
    return result


def audit_sources(kernels, census, results):
    order_five = tuple(tuple(record["code"]) for record in kernels["kernels"]
                       if record["n"] == 5)
    require(len(order_five) == EXPECTED["kernels"], "order-five kernel source changed")
    require(census["kernel_total"] == EXPECTED["kernels"], "census kernel total changed")
    require(census["physical_total"] == EXPECTED["physical"], "physical total changed")
    require(census["orbit_total"] == EXPECTED["orbits"], "orbit total changed")
    require(census["residual_total"] == EXPECTED["residual"], "residual total changed")
    require(census["orbit_total"] - census["residual_total"] == EXPECTED["tetra"],
            "tetra-certified total changed")
    require(census["search_target_total"] == EXPECTED["covered_rows"],
            "covered residual-row total changed")
    require(census["excluded_target_keys"] == [[K5E_KEY[0], list(K5E_KEY[1])]],
            "excluded key changed")
    require(census["certificate_fixture_frozen"] is False,
            "census experiment was improperly promoted")
    census_codes = tuple(tuple(record["code"]) for record in census["kernels"])
    require(census_codes == order_five, "census kernel selection differs from source")
    require(results["source_census_sha256"] == EXPECTED_DIGESTS["census"],
            "results point to another census")
    require(results["target_total"] == EXPECTED["targets"], "result target total changed")
    require(results["exact_dnn_le_4_total"] == EXPECTED["rational"],
            "result rational total changed")
    require(results["optimized_obstruction_total"] == 8, "result failure total changed")
    require(len(results["records"]) == EXPECTED["targets"], "result record count changed")
    return {number: tuple(record["code"]) for number, record in
            ((row["kernel"], row) for row in census["kernels"])}


def audit_rational(record, source, kernel):
    require(source["exact_dnn_le_4"] is True and source["witness"] is not None,
            "rational fixture points to a failed source target")
    require(record["lengths"] == source["lengths"], "rational path lengths changed")
    witness = record["witness"]
    require(witness == source["witness"], "rational witness differs from fresh result")
    branches_p = tuple(tuple(fraction(x, "branch") for x in row)
                       for row in witness["branches"])
    require(len(branches_p) == 5 and all(len(row) == 3 for row in branches_p),
            "branch stereographic dimensions changed")
    branches = tuple(rational_unit(row) for row in branches_p)
    paths = path_ledger(kernel, tuple(record["row"]), record["frontier"])
    require([path[4] for path in paths] == record["lengths"], "path ledger changed")
    require(len(witness["internals"]) == 9, "internal path ledger changed")
    total = Fraction(0)
    for (_, _, u, v, length), raw_internal in zip(paths, witness["internals"]):
        parameters = tuple(tuple(fraction(x, "internal") for x in row)
                           for row in raw_internal)
        require(len(parameters) == length - 1 and all(len(row) == 3 for row in parameters),
                "internal stereographic dimensions changed")
        vectors = [branches[u], *(rational_unit(row) for row in parameters)]
        vectors.append(branches[v] if length % 2 == 0 else tuple(-x for x in branches[v]))
        total += sum((step_cost(left, right) for left, right in zip(vectors, vectors[1:])),
                     Fraction(0))
    require(total == fraction(witness["cost"], "cost"), "stored rational cost changed")
    require(total < 4, "rational frontier witness is not strict")


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


def connected(vertices, edges):
    if not vertices:
        return False
    seen = {next(iter(vertices))}
    while True:
        reached = seen | {v for edge in edges if edge & seen for v in edge}
        reached &= vertices
        if reached == seen:
            return seen == vertices
        seen = reached


def physical_subdivision(paths):
    branch = tuple(("branch", vertex) for vertex in range(5))
    vertices = set(branch)
    edges = set()
    internals = {}
    for index, (_, _, u, v, length) in enumerate(paths):
        internal = tuple(("internal", index, step) for step in range(1, length))
        internals[index] = internal
        chain = (branch[u], *internal, branch[v])
        vertices.update(internal)
        edges.update(frozenset((left, right)) for left, right in zip(chain, chain[1:]))
    require(all(len(edge) == 2 for edge in edges), "physical subdivision has a loop")
    return branch, vertices, edges, internals


def induced_edges(vertices, edges):
    return {edge for edge in edges if edge <= vertices}


def audit_symbolic(record, kernel):
    require(record["kernel"] == 35, "symbolic target is not K35")
    require(record["template"] in ("coincident_01", "antipodal_01"),
            "unknown K35 symbolic template")
    paths = path_ledger(kernel, tuple(record["row"]), record["frontier"])
    require(record["lengths"] == [path[4] for path in paths], "symbolic lengths changed")
    expected_lengths = {
        "coincident_01": {(2, 1, 2, 1, 2, 1, 2, 1, 2),
                           (4, 1, 2, 1, 2, 1, 2, 1, 2)},
        "antipodal_01": {(1, 1, 2, 1, 2, 1, 2, 1, 2),
                          (3, 1, 2, 1, 2, 1, 2, 1, 2)},
    }
    require(tuple(record["lengths"]) in expected_lengths[record["template"]],
            "K35 equality target does not match template")
    gram = tuple(tuple(fraction(x, "symbolic Gram") for x in row)
                 for row in record["gram"])
    require(len(gram) == 5 and all(len(row) == 5 for row in gram), "bad symbolic Gram size")
    require(all(gram[i][j] == gram[j][i] for i in range(5) for j in range(5)),
            "symbolic Gram is asymmetric")
    require(all(gram[i][i] == 1 for i in range(5)), "symbolic Gram diagonal changed")
    require(all(determinant(tuple(tuple(gram[i][j] for j in indices) for i in indices)) >= 0
                for size in range(1, 6) for indices in itertools.combinations(range(5), size)),
            "symbolic Gram is not PSD")
    edge01 = gram[0][1]
    require(edge01 == (1 if record["template"] == "coincident_01" else -1),
            "K35 01 identity changed")
    required = ((0, 4), (1, 3), (2, 3), (2, 4))
    require(all(gram[u][v] == Fraction(-1, 2) for u, v in required),
            "K35 four-bundle correlations changed")
    require(record["cost_identity"] == "0+4*(1/3+2*(1/3))=4",
            "K35 symbolic cost identity changed")


def audit_structural(record, kernel):
    require(record["kernel"] == 22, "structural target is not K22")
    paths = path_ledger(kernel, tuple(record["row"]), record["frontier"])
    require(record["lengths"] == [path[4] for path in paths], "structural lengths changed")
    structural_targets = {
        ((0, 0, 0, 1, 1, 1, 1, 1, 1, 1), None),
        ((0, 0, 0, 1, 1, 1, 1, 1, 1, 1), 0),
        ((0, 0, 1, 1, 1, 1, 1, 1, 1, 1), None),
        ((0, 0, 1, 1, 1, 1, 1, 1, 1, 1), 0),
    }
    require((tuple(record["row"]), record["frontier"]) in structural_targets,
            "K22 structural key changed")
    require(record["opening"] == {"deleted_branch": 0, "ear_paths": [0, 1, 2],
                                   "retained_clique": [1, 2, 3, 4]},
            "K22 opening data changed")

    branch, vertices, edges, internals = physical_subdivision(paths)
    ear_paths = tuple(record["opening"]["ear_paths"])
    require(tuple((paths[i][2], paths[i][3]) for i in ear_paths) ==
            ((0, 3), (0, 4), (0, 4)), "K22 ear paths were not reconstructed")
    require(set(ear_paths) == {i for i, path in enumerate(paths) if 0 in path[2:4]},
            "K22 opening omits a path at deleted branch")
    deleted_core = {branch[record["opening"]["deleted_branch"]]}
    deleted_core.update(vertex for i in ear_paths for vertex in internals[i])
    retained_core = vertices - deleted_core
    deleted_edges = induced_edges(deleted_core, edges)
    retained_edges = induced_edges(retained_core, edges)
    require(deleted_core and connected(deleted_core, deleted_edges),
            "deleted K22 territory is empty or disconnected")
    require(len(deleted_edges) == len(deleted_core) - 1,
            "deleted K22 territory is not a tree")
    require(connected(retained_core, retained_edges), "K22 complement is disconnected")

    clique = {branch[v] for v in record["opening"]["retained_clique"]}
    clique_edges = {frozenset((branch[u], branch[v]))
                    for u, v in itertools.combinations(record["opening"]["retained_clique"], 2)}
    require(retained_core == clique and retained_edges == clique_edges,
            "K22 complement is not the actual induced K4")

    owner_side = {vertex: "deleted" if vertex in deleted_core else "retained"
                  for vertex in vertices}
    require(set(owner_side) == vertices and all(side in ("deleted", "retained")
                                                for side in owner_side.values()),
            "rooted-tree ownership is not exhaustive")
    # Materialize a nontrivial rooted tree at every branch/internal vertex and
    # reconstruct the induced partition.  An arbitrary rooted tree follows by
    # replacing either representative edge with any tree at the same owner.
    augmented_vertices = set(vertices)
    augmented_edges = set(edges)
    deleted = set(deleted_core)
    retained = set(retained_core)
    for owner, side in owner_side.items():
        first = ("rooted", owner, 1)
        second = ("rooted", owner, 2)
        augmented_vertices.update((first, second))
        augmented_edges.update((frozenset((owner, first)), frozenset((first, second))))
        (deleted if side == "deleted" else retained).update((first, second))
    require(deleted | retained == augmented_vertices and not deleted & retained,
            "rooted-tree territories are not an exhaustive partition")
    deleted_augmented_edges = induced_edges(deleted, augmented_edges)
    retained_augmented_edges = induced_edges(retained, augmented_edges)
    require(connected(deleted, deleted_augmented_edges) and
            len(deleted_augmented_edges) == len(deleted) - 1,
            "owned rooted trees do not preserve the deleted induced tree")
    require(connected(retained, retained_augmented_edges) and
            induced_edges(clique, retained_augmented_edges) == clique_edges,
            "owned rooted trees do not preserve the attached actual K4")


def build_fixture(census, results):
    failures = {key(row["kernel"], row["row"], row["frontier"]): row
                for row in results["records"] if not row["exact_dnn_le_4"]}
    records = []
    coincident = [[1, 1, [-1, 2], [-1, 2], [-1, 2]],
                  [1, 1, [-1, 2], [-1, 2], [-1, 2]],
                  [[-1, 2], [-1, 2], 1, [-1, 2], [-1, 2]],
                  [[-1, 2], [-1, 2], [-1, 2], 1, 1],
                  [[-1, 2], [-1, 2], [-1, 2], 1, 1]]
    antipodal = [[1, -1, 0, [1, 2], [-1, 2]],
                 [-1, 1, 0, [-1, 2], [1, 2]],
                 [0, 0, 1, [-1, 2], [-1, 2]],
                 [[1, 2], [-1, 2], [-1, 2], 1, [1, 2]],
                 [[-1, 2], [1, 2], [-1, 2], [1, 2], 1]]

    def canonical_fraction(value):
        if isinstance(value, int):
            return [value, 1]
        return value

    for source in results["records"]:
        base = {name: source[name] for name in ("kernel", "row", "frontier", "lengths")}
        target = key(source["kernel"], source["row"], source["frontier"])
        if source["exact_dnn_le_4"]:
            base.update({"method": "strict_rational_path_vectors", "witness": source["witness"]})
        elif source["kernel"] == 35:
            template = "coincident_01" if source["row"][0] == 0 else "antipodal_01"
            matrix = coincident if template == "coincident_01" else antipodal
            base.update({
                "method": "symbolic_equality", "template": template,
                "gram": [[canonical_fraction(x) for x in row] for row in matrix],
                "cost_identity": "0+4*(1/3+2*(1/3))=4",
            })
        elif source["kernel"] == 22:
            base.update({
                "method": "structural_attached_k4",
                "opening": {"deleted_branch": 0, "ear_paths": [0, 1, 2],
                            "retained_clique": [1, 2, 3, 4]},
            })
        else:
            raise RuntimeError(f"unclosed failed result {target}")
        records.append(base)
    require(len(failures) == 8, "fresh result failure set changed")
    return {
        "schema": "rank-five-order-five-non-k5e-family-theorem-v2",
        "theorem_scope": "all 24 order-five kernels and physical parity families except all-odd K5-e",
        "excluded_key": [K5E_KEY[0], list(K5E_KEY[1])],
        "source_digests": {name: EXPECTED_DIGESTS[name]
                           for name in ("kernels", "census", "results")},
        "counts": EXPECTED,
        "frontier_policy": "canonical plus all nine one-path length-plus-two frontiers",
        "records": records,
    }


def audit_fixture(fixture, census, results, kernels_by_number):
    require(fixture["schema"] == "rank-five-order-five-non-k5e-family-theorem-v2",
            "fixture schema changed")
    require(fixture["excluded_key"] == [K5E_KEY[0], list(K5E_KEY[1])],
            "fixture exclusion changed")
    require(fixture["counts"] == EXPECTED, "fixture count ledger changed")
    require(fixture["source_digests"] == {name: EXPECTED_DIGESTS[name]
                                         for name in ("kernels", "census", "results")},
            "fixture source locks changed")
    require(fixture == build_fixture(census, results), "fixture differs from fresh output")
    source_records = {key(row["kernel"], row["row"], row["frontier"]): row
                      for row in results["records"]}
    seen = set()
    methods = {"strict_rational_path_vectors": 0, "symbolic_equality": 0,
               "structural_attached_k4": 0}
    for record in fixture["records"]:
        target = key(record["kernel"], record["row"], record["frontier"])
        require(target not in seen, "duplicate theorem key")
        seen.add(target)
        require(target in source_records, "theorem key absent from result source")
        require(record["method"] in methods, "unknown theorem method")
        methods[record["method"]] += 1
        kernel = kernels_by_number[record["kernel"]]
        if record["method"] == "strict_rational_path_vectors":
            audit_rational(record, source_records[target], kernel)
        elif record["method"] == "symbolic_equality":
            audit_symbolic(record, kernel)
        else:
            audit_structural(record, kernel)
    require(seen == expected_keys(census), "all-length frontier cover is incomplete")
    require(methods == {"strict_rational_path_vectors": EXPECTED["rational"],
                        "symbolic_equality": EXPECTED["symbolic"],
                        "structural_attached_k4": EXPECTED["structural"]},
            "certificate partition changed")
    method_by_key = {key(row["kernel"], row["row"], row["frontier"]): row["method"]
                     for row in fixture["records"]}
    k22_rows = ((0, 0, 0, 1, 1, 1, 1, 1, 1, 1),
                (0, 0, 1, 1, 1, 1, 1, 1, 1, 1))
    for row in k22_rows:
        require(all(method_by_key[key(22, row, frontier)] ==
                    ("structural_attached_k4" if frontier in (None, 0)
                     else "strict_rational_path_vectors")
                    for frontier in (None, *range(9))),
                "K22 canonical/frontier descendant cover changed")
    return methods


def hostile_mutations(fixture, census, results, kernels_by_number):
    attacks = []

    def add(name, mutate):
        candidate = copy.deepcopy(fixture)
        mutate(candidate)
        attacks.append((name, candidate))

    add("delete target", lambda x: x["records"].pop())
    add("claim K5-e", lambda x: x.__setitem__("excluded_key", [32, [0] * 10]))
    add("forge count", lambda x: x["counts"].__setitem__("rational", 2063))
    rational_index = next(i for i, row in enumerate(fixture["records"])
                          if row["method"] == "strict_rational_path_vectors")
    symbolic_index = next(i for i, row in enumerate(fixture["records"])
                          if row["method"] == "symbolic_equality")
    structural_index = next(i for i, row in enumerate(fixture["records"])
                            if row["method"] == "structural_attached_k4")
    add("forge rational cost", lambda x: x["records"][rational_index]["witness"].__setitem__("cost", [0, 1]))
    add("change path length", lambda x: x["records"][rational_index]["lengths"].__setitem__(0, 99))
    add("change symbolic Gram", lambda x: x["records"][symbolic_index]["gram"][0].__setitem__(1, [0, 1]))
    add("change symbolic identity", lambda x: x["records"][symbolic_index].__setitem__("cost_identity", "4=4"))
    add("change deleted branch", lambda x: x["records"][structural_index]["opening"].__setitem__("deleted_branch", 1))
    add("omit ear path", lambda x: x["records"][structural_index]["opening"].__setitem__("ear_paths", [0, 1]))
    add("change retained clique", lambda x: x["records"][structural_index]["opening"].__setitem__("retained_clique", [0, 1, 2, 3]))
    add("change source lock", lambda x: x["source_digests"].__setitem__("results", "0" * 64))
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
    payload = build_fixture(census, results)
    require(FIXTURE.parent.is_dir(), "fixture parent missing")
    FIXTURE.write_bytes(canonical_json(payload))
    print(hashlib.sha256(FIXTURE.read_bytes()).hexdigest())


def main():
    if sys.argv[1:] == ["--regenerate"]:
        regenerate()
        return
    require(not sys.argv[1:], "usage: verifier.py [--regenerate]")
    kernels, census, results, fixture = load_sources()
    kernels_by_number = audit_sources(kernels, census, results)
    methods = audit_fixture(fixture, census, results, kernels_by_number)
    attacks = hostile_mutations(fixture, census, results, kernels_by_number)
    print("order-five rank-five non-K5-e kernel-family theorem: exact audit passed")
    print("kernels=24 physical=6282 orbits=4238 tetra_certified=4030 residual=208")
    print("covered_residual_rows=207 all_length_targets=2070 "
          f"rational={methods['strict_rational_path_vectors']} "
          f"symbolic_K35={methods['symbolic_equality']} "
          f"structural_K22={methods['structural_attached_k4']}")
    print(f"hostile_mutations_rejected={attacks}")
    print("excluded_without_claim=K32_all_odd_K5-e")


if __name__ == "__main__":
    main()
