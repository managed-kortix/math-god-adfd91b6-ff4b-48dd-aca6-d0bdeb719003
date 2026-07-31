#!/usr/bin/env python3
"""Standalone fail-closed audit of the four-vertex rank-four theorem ledger.

All proposed DNN certificates are accepted only after exact Fraction checks.
The final two rows are handled by an exhaustive monotone all-odd-K4 class
ledger.  The ledger contains valid DNN and structural classes, but it exposes
the actual-K4 branch required by the reduction and exits with a blocker because
that branch has no encoded proof of the required unit surplus.
"""

import hashlib
import importlib.util
import json
from copy import deepcopy
from fractions import Fraction
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    require(spec is not None and spec.loader is not None,
            f"cannot load proof component {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


BASE = load("rank_four_four_vertex_base",
            "rank-four-four-vertex-dnn-verifier.py")
PATCH = load("rank_four_four_vertex_patch",
             "rank-four-four-vertex-exact-row-patch.py")


UNRESOLVED_RECORDS = (
    {
        "key": (4, (1, 1, 1, 1, 1, 1)),
        "status": "unresolved",
        "gram": None,
        "numerical_excess": None,
        "predicates": (
            "k4_support_with_doubled_23",
            "five_singleton_bundles_odd",
            "doubled_23_has_one_odd_one_even",
            "choose_odd_23_path_for_k4_support",
            "other_23_path_even_hence_has_internal_vertex",
            "induced_complement_is_all_odd_k4_packet",
        ),
        "ownership": (
            "deleted_path_internal_vertices_and_their_rooted_trees_form_nonempty_tree",
            "deleted_tree_has_sigma_minus_one",
            "remaining_vertices_induce_the_all_odd_k4_packet",
            "induced_vertex_sets_are_disjoint_and_exhaustive",
        ),
        "reduction": "induced_superadditivity",
        "required_all_odd_k4_sigma": 1,
    },
    {
        "key": (4, (1, 1, 1, 1, 1, 2)),
        "status": "unresolved",
        "gram": None,
        "numerical_excess": None,
        "predicates": (
            "k4_support_with_doubled_23",
            "five_singleton_bundles_odd",
            "doubled_23_has_two_odd",
            "choose_one_odd_23_path_for_k4_support",
            "simplicity_forces_other_odd_23_path_to_have_internal_vertex",
            "induced_complement_is_all_odd_k4_packet",
        ),
        "ownership": (
            "deleted_path_internal_vertices_and_their_rooted_trees_form_nonempty_tree",
            "deleted_tree_has_sigma_minus_one",
            "remaining_vertices_induce_the_all_odd_k4_packet",
            "induced_vertex_sets_are_disjoint_and_exhaustive",
        ),
        "reduction": "induced_superadditivity",
        "required_all_odd_k4_sigma": 1,
    },
)


# Canonical all-odd K4 branch lengths are 1 (unit) or 3 (long).  The regular
# simplex gives unit cost 1/2 and long cost strictly below 1/6.  These are the
# four proposed monotone DNN bounds; the verifier derives each rational bound.
PROPOSED_DNN_CERTIFICATES = (
    {
        "name": "three_long_simplex",
        "long_paths": 3,
        "claimed_bound": Fraction(2),
    },
    {
        "name": "four_long_simplex",
        "long_paths": 4,
        "claimed_bound": Fraction(5, 3),
    },
    {
        "name": "five_long_simplex",
        "long_paths": 5,
        "claimed_bound": Fraction(4, 3),
    },
    {
        "name": "six_long_simplex",
        "long_paths": 6,
        "claimed_bound": Fraction(1),
    },
)


ALL_ODD_K4_CLASS_COUNTS = {
    "q_ge_3_dnn": 42,
    "q_2_adjacent_dnn": 12,
    "q_2_opposite_dnn": 3,
    "q_1_structural": 6,
    "actual_k4_packet": 1,
}


def base_failures():
    fixture = {
        (i, row): (parameters if parameters[0] == "x" else
                   tuple(Fraction(x) for x in parameters))
        for i, row, parameters in BASE.CERTIFICATES
    }
    failures = set()
    universe = set()
    for i, kernel in enumerate(BASE.KERNELS):
        for row in BASE.physical_rows(kernel):
            key = (i, row)
            universe.add(key)
            representative, bits, permutation = BASE.orbit_transport(kernel, row)
            parameters = fixture[(i, representative)]
            failed = parameters[0] == "x" and row != representative
            if not failed:
                try:
                    failed = BASE.transported_cost(
                        kernel, row, parameters, bits, permutation) > 3
                except RuntimeError:
                    failed = True
            if failed:
                failures.add(key)
    return universe, failures


def patch_coverage(failures):
    rational = {(i, row) for i, row, unused in PATCH.ROW_CERTIFICATES}
    boundary = {(i, row) for i, row, unused_matrix, unused_cost
                in PATCH.BOUNDARY_CERTIFICATES}
    canonical_patch = rational | boundary
    return {key for key in failures
            if (key[0], PATCH.aut_canonical(BASE.KERNELS[key[0]], key[1]))
            in canonical_patch}


def exact_psd(matrix):
    return all(BASE.determinant(BASE.principal_submatrix(matrix, indices)) >= 0
               for size in range(1, 5)
               for indices in combinations(range(4), size))


def validate_dnn_certificate(record):
    required = {"name", "long_paths", "claimed_bound"}
    require(set(record) == required, "proposed DNN certificate schema changed")
    q = record["long_paths"]
    require(q in (3, 4, 5, 6), "proposed simplex class is not one of 3,4,5,6")

    matrix = tuple(tuple(Fraction(1) if i == j else Fraction(-1, 3)
                         for j in range(4)) for i in range(4))
    require(exact_psd(matrix),
            f"{record['name']}: proposed Gram matrix is not exactly PSD")

    # If y=x^2 and x=tan(acos(1/3)/6), tan(3 atan x)=1/sqrt(2).
    # At y=1/18 the squared triple-angle is already greater than 1/2;
    # monotonicity of tan(3 atan x) on this interval proves x^2<1/18,
    # hence a length-three path costs 3x^2<1/6.
    y = Fraction(1, 18)
    triple_square = y * (3 - y) ** 2 / (1 - 3 * y) ** 2
    require(triple_square > Fraction(1, 2),
            f"{record['name']}: exact long-path comparison failed")
    require(3 * y == Fraction(1, 6),
            f"{record['name']}: rational long-path upper bound changed")
    derived_bound = (6 - q) * Fraction(1, 2) + q * Fraction(1, 6)
    require(derived_bound == record["claimed_bound"],
            f"{record['name']}: claimed rational upper bound changed")
    return derived_bound


def reject_false_simplex():
    square = Fraction(1, 3)
    correlation = (1 - 6 * square + square * square) / (1 + square) ** 2
    require(correlation == Fraction(-1, 2),
            "quarter-angle algebra changed at t^2=1/3")
    require(correlation != Fraction(-1, 3),
            "false regular-simplex parameter was accepted")

    polynomial = lambda x: x * x - 4 * x + 1
    require(polynomial(square) != 0,
            "false simplex square solves the regular-simplex equation")
    require(polynomial(Fraction(2)) < 0 and polynomial(Fraction(1)) < 0 and
            polynomial(Fraction(0)) > 0,
            "regular-simplex root isolation changed")

    false_parameters = ("x",) + (Fraction(1, 3),) * 6
    try:
        unused_cost, matrix = BASE.certificate_cost(
            BASE.KERNELS[4], (1, 1, 1, 1, 1, 1), false_parameters)
        require(exact_psd(matrix), "false simplex Gram matrix is indefinite")
    except RuntimeError:
        return
    raise RuntimeError("false regular-simplex residual certificate was accepted")


def classify_long_edges(long_edges):
    q = len(long_edges)
    if q >= 3:
        return "q_ge_3_dnn"
    if q == 2:
        first, second = sorted(long_edges)
        return ("q_2_opposite_dnn"
                if set(BASE.pairs()[first]).isdisjoint(BASE.pairs()[second])
                else "q_2_adjacent_dnn")
    if q == 1:
        return "q_1_structural"
    return "actual_k4_packet"


def audit_all_odd_k4_classes():
    counts = {name: 0 for name in ALL_ODD_K4_CLASS_COUNTS}
    seen = set()
    for mask in range(64):
        long_edges = frozenset(i for i in range(6) if mask & (1 << i))
        require(long_edges not in seen, "duplicate all-odd K4 long-edge subset")
        seen.add(long_edges)
        counts[classify_long_edges(long_edges)] += 1
    require(len(seen) == 64, "all-odd K4 long/unit subsets are incomplete")
    require(counts == ALL_ODD_K4_CLASS_COUNTS,
            "all-odd K4 monotone class census changed")

    for long_edges in seen:
        disposition = classify_long_edges(long_edges)
        if disposition.endswith("_dnn"):
            require(len(long_edges) >= 2, "DNN class lost its long-path premise")
        elif disposition == "q_1_structural":
            require(len(long_edges) == 1,
                    "one-long structural class predicate changed")
        else:
            require(not long_edges,
                    "actual-K4 class contains a subdivided branch path")
    return counts


def validate_actual_k4_branch(record):
    required = {"status", "core", "unit_edges", "required_sigma",
                "proof_artifact"}
    require(set(record) == required, "actual-K4 branch schema changed")
    require(record["core"] == "actual_K4" and record["unit_edges"] == 6,
            "actual-K4 branch does not identify the unsubdivided graph")
    require(record["required_sigma"] == 1,
            "actual-K4 branch weakened the required surplus")
    require(record["status"] == "unresolved" and
            record["proof_artifact"] is None,
            "actual-K4 branch was marked proved without an exact artifact")


ACTUAL_K4_BRANCH = {
    "status": "unresolved",
    "core": "actual_K4",
    "unit_edges": 6,
    "required_sigma": 1,
    "proof_artifact": None,
}


def validate_unresolved_record(record):
    required_fields = {"key", "status", "gram", "numerical_excess",
                       "predicates", "ownership", "reduction",
                       "required_all_odd_k4_sigma"}
    require(set(record) == required_fields, "unresolved record schema changed")
    require(record["status"] == "unresolved",
            "residual was falsely reclassified as proved")
    require(record["gram"] is None and record["numerical_excess"] is None,
            "unresolved residual contains a false numerical certificate")
    require(record["reduction"] == "induced_superadditivity",
            "wrong residual reduction")
    require(record["required_all_odd_k4_sigma"] == 1,
            "required all-odd K4 margin changed")

    kernel_index, row = record["key"]
    require(kernel_index == 4, "unresolved row has the wrong kernel")
    require(BASE.KERNELS[kernel_index] == (1, 1, 1, 1, 1, 2),
            "unresolved kernel multiplicities changed")
    require(row[:5] == (1, 1, 1, 1, 1),
            "singleton all-odd predicate is false")
    require(row[5] in (1, 2), "doubled-bundle parity count is not residual")

    predicates = set(record["predicates"])
    common = {
        "k4_support_with_doubled_23",
        "five_singleton_bundles_odd",
        "induced_complement_is_all_odd_k4_packet",
    }
    expected = set(common)
    if row[5] == 1:
        expected.update({
            "doubled_23_has_one_odd_one_even",
            "choose_odd_23_path_for_k4_support",
            "other_23_path_even_hence_has_internal_vertex",
        })
    else:
        expected.update({
            "doubled_23_has_two_odd",
            "choose_one_odd_23_path_for_k4_support",
            "simplicity_forces_other_odd_23_path_to_have_internal_vertex",
        })
    require(predicates == expected, "unresolved predicate ledger is not exact")

    require(set(record["ownership"]) == {
        "deleted_path_internal_vertices_and_their_rooted_trees_form_nonempty_tree",
        "deleted_tree_has_sigma_minus_one",
        "remaining_vertices_induce_the_all_odd_k4_packet",
        "induced_vertex_sets_are_disjoint_and_exhaustive",
    }, "residual partition ownership is not exact")


def audit(records=UNRESOLVED_RECORDS):
    BASE.audit()
    PATCH.audit()
    universe, failures = base_failures()
    base = universe - failures
    patch = patch_coverage(failures)

    require(len(universe) == 342, "physical universe changed")
    require(len(base) == 270, "base physical coverage changed")
    require(len(failures) == 72, "base failure frontier changed")
    require(len(patch) == 70, "patch physical coverage changed")
    require(base.isdisjoint(patch), "base and patch coverage overlap")

    require(isinstance(records, tuple), "unresolved fixture is not immutable")
    for record in records:
        validate_unresolved_record(record)
    unresolved = {record["key"] for record in records}
    require(len(records) == len(unresolved) == 2,
            "unresolved count or uniqueness changed")
    require(unresolved == failures - patch,
            "unresolved records do not equal the exact residual frontier")
    require(base | patch | unresolved == universe,
            "physical status ledger is not exhaustive")
    require(not (base & unresolved) and not (patch & unresolved),
            "status classes are not disjoint")

    reject_false_simplex()
    simplex_bounds = tuple(validate_dnn_certificate(record)
                           for record in PROPOSED_DNN_CERTIFICATES)
    require(simplex_bounds == (Fraction(2), Fraction(5, 3),
                               Fraction(4, 3), Fraction(1)),
            "four-certificate simplex ledger changed")
    class_counts = audit_all_odd_k4_classes()
    validate_actual_k4_branch(ACTUAL_K4_BRANCH)

    serial = json.dumps(records, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(serial.encode("ascii")).hexdigest()
    return digest, unresolved, class_counts


def expect_rejected(records, label):
    try:
        audit(records)
    except (RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    mutations = []

    def mutate(label, action):
        records = deepcopy(UNRESOLVED_RECORDS)
        records = [dict(record) for record in records]
        action(records)
        mutations.append((label, tuple(records)))

    mutate("deleted residual", lambda rows: rows.pop())
    mutate("duplicated residual", lambda rows: rows.append(dict(rows[0])))
    mutate("wrong physical row", lambda rows: rows[0].__setitem__(
        "key", (4, (1, 1, 1, 1, 0, 1))))
    mutate("numerical Gram smuggled in", lambda rows: rows[0].__setitem__(
        "gram", ((1,),)))
    mutate("numerical excess smuggled in", lambda rows: rows[0].__setitem__(
        "numerical_excess", Fraction(3)))
    mutate("status changed to proved", lambda rows: rows[0].__setitem__(
        "status", "proved"))
    mutate("parity predicate deleted", lambda rows: rows[0].__setitem__(
        "predicates", rows[0]["predicates"][:-1]))
    mutate("ownership split", lambda rows: rows[1].__setitem__(
        "ownership", rows[1]["ownership"][:-1]))
    mutate("required margin weakened", lambda rows: rows[0].__setitem__(
        "required_all_odd_k4_sigma", 0))

    for label, records in mutations:
        expect_rejected(records, label)

    false_simplex = deepcopy(PROPOSED_DNN_CERTIFICATES[-1])
    false_simplex["claimed_bound"] = Fraction(9, 10)
    try:
        validate_dnn_certificate(false_simplex)
    except RuntimeError:
        pass
    else:
        raise RuntimeError("hostile false-simplex mutation was accepted")
    return len(mutations) + 1


def main():
    digest, unresolved, class_counts = audit()
    mutations = hostile_self_checks()
    require(mutations == 10, "hostile mutation count changed")
    print("four-vertex rank-four ledger audit passed; theorem remains unresolved")
    print("physical_rows: 342 = 270 base + 70 exact_patch + 2 unresolved")
    print("all_odd_k4_classes: " + ",".join(
        f"{name}={class_counts[name]}" for name in ALL_ODD_K4_CLASS_COUNTS))
    print("false_simplex_certificate: rejected by exact quarter-angle algebra")
    print("unresolved_rows: kernel4/111111,kernel4/111112")
    print("structural_branch: actual K4 requires an exact attached-packet sigma >= 1 proof")
    print(f"unresolved_records_sha256: {digest}")
    print(f"rejected_hostile_mutations: {mutations}")
    if unresolved:
        print("BLOCKER: two physical rows require the unproved all-odd K4 sigma>=1 lemma")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
