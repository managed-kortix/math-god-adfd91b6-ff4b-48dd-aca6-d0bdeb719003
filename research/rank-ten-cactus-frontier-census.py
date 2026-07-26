#!/usr/bin/env python3
"""Fail-closed exact frontier census for rank-ten cactus residuals.

This program enumerates colored cluster partitions and fully shared bipartite
cycle-cut incidence trees for T^9Q and T^8PP.  Every ledger scalar is a
Fraction.  Frozen totals and exception signatures are checked with explicit
exceptions, so verification remains active under ``python -O``.
"""

from collections import Counter
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = spec_from_file_location(
    "rank_nine_incidence", HERE / "nonacyclic-fully-shared-incidence-census.py"
)
BASE = module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("cannot load rank-nine incidence generator")
SPEC.loader.exec_module(BASE)

TRIANGLE_MARGIN = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1, 7: 0, 8: 0, 9: 0}

EXPECTED_PARTITIONS = {
    "T^9Q": (97, 96, 92, 4),
    "T^8PP": (181, 180, 170, 10),
}

EXPECTED_T9Q = {
    "q=3": {1: 1, 2: 12, 3: 91, 4: 406, 5: 1178, 6: 2115, 7: 2250, 8: 1246, 9: 275},
    "q=4": {1: 1, 2: 12, 3: 91, 4: 412, 5: 1203, 6: 2187, 7: 2361, 8: 1340, 9: 306},
    "q=5": {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2201, 7: 2393, 8: 1372, 9: 321},
    "q=6": {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2204, 7: 2400, 8: 1383, 9: 327},
    "q=7": {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2204, 7: 2402, 8: 1386, 9: 330},
    "q=8": {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2204, 7: 2402, 8: 1387, 9: 331},
    "q>=9": {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2204, 7: 2402, 8: 1387, 9: 332},
}

EXPECTED_T8PP = {
    1: 1, 2: 19, 3: 204, 4: 1155, 5: 3990, 6: 8135,
    7: 9615, 8: 5843, 9: 1424,
}

T9Q_COMMON = "X(Q()T()T()T()T()T()T()T()T()T())"
T9Q_HOSTILE = {
    T9Q_COMMON,
    "T(X(Q())X(T()T()T()T()T()T()T()T()))",
    "T(X(Q())X(T())X(T()T()T()T()T()T()T()))",
}
T8PP_EXCEPTIONS = {
    "X(P()P()T()T()T()T()T()T()T()T())",
    "P(X(P())X(T()T()T()T()T()T()T()T()))",
    "T(X(P())X(P()T()T()T()T()T()T()T()))",
    "P(X(P())X(T())X(T()T()T()T()T()T()T()))",
    "T(X(P())X(P())X(T()T()T()T()T()T()T()))",
    "T(X(P())X(P()T()T()T()T()T()T())X(T()))",
    "X(T()T()T()T()T()T()T(X(P()))T(X(P())))",
    "X(T()T()T()T()T()T(X(P()))T(X(P())X(T())))",
    "X(T()T()T()T()T(X(P())X(T()))T(X(P())X(T())))",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def partitions(triangles, distinguished, minimum=(0, 0)):
    rows = []
    for triangles_here in range(triangles + 1):
        for distinguished_here in range(distinguished + 1):
            part = (triangles_here, distinguished_here)
            if part == (0, 0) or part < minimum:
                continue
            if part == (triangles, distinguished):
                rows.append((part,))
                continue
            for rest in partitions(
                triangles - triangles_here,
                distinguished - distinguished_here,
                part,
            ):
                rows.append((part,) + rest)
    return rows


def triangle_bound(triangles):
    require(triangles in TRIANGLE_MARGIN, f"missing A_{triangles} bound")
    return Fraction(TRIANGLE_MARGIN[triangles]), True


def tq_profile_bound(part):
    triangles, q_count = part
    require(q_count in (0, 1), f"invalid TQ profile {part}")
    if q_count == 0:
        return triangle_bound(triangles)
    if triangles == 0:
        return Fraction(-1), False
    if triangles == 1:
        return Fraction(0), True
    if triangles == 2:
        return Fraction(0), False
    return Fraction(0), True


def tpp_profile_bound(part):
    triangles, pentagons = part
    require(pentagons in (0, 1, 2), f"invalid TPP profile {part}")
    rank = triangles + pentagons
    if pentagons == 0:
        return triangle_bound(triangles)
    if part == (0, 1):
        return Fraction(-1, 4), False
    if part == (1, 1):
        return Fraction(3, 4), True
    if part == (0, 2):
        return Fraction(0), True
    if part == (1, 2):
        return Fraction(3, 2), True
    if rank in (2, 3):
        return Fraction(0), False
    return Fraction(0), True


def partition_audit(triangles, distinguished, bound):
    all_rows = partitions(triangles, distinguished)
    require(len(all_rows) == len(set(all_rows)), "duplicate colored partition")
    proper_rows = [row for row in all_rows if len(row) > 1]
    residual = []
    for row in proper_rows:
        bounds = [bound(part) for part in row]
        total = sum((value for value, _ in bounds), Fraction())
        strict = any(flag for _, flag in bounds)
        if not (total > 0 or (total == 0 and strict)):
            residual.append(row)
    return all_rows, proper_rows, residual


def tq_component_bound(label, tree, component):
    counts = Counter(tree.colors[cycle] for cycle in component[0])
    triangles, q_count = counts["T"], counts["Q"]
    require(q_count in (0, 1), "component contains multiple Q cycles")
    if q_count == 0:
        value, strict = triangle_bound(triangles)
        return BASE.Bound(value, strict, f"A_{triangles}")
    if triangles == 0:
        if label == "q=3":
            return BASE.Bound(Fraction(0), True, "Q=T>0")
        if label in {"q=4", "q=6", "q=8"}:
            return BASE.Bound(Fraction(0), False, "even Q>=0")
        return BASE.Bound(Fraction(-1), True, "hostile Q>-1")
    if triangles == 1:
        return BASE.Bound(Fraction(0), True, "TQ>0")
    if triangles == 2:
        return BASE.Bound(Fraction(0), False, "TTQ>=0")
    require(triangles <= 8, "split unexpectedly retained rank ten")
    return BASE.Bound(Fraction(0), True, f"rank-{triangles + 1}>0")


def tpp_component_bound(tree, component):
    cycles, internal_cuts, adjacency = component
    triangle_set = {cycle for cycle in cycles if tree.colors[cycle] == "T"}
    triangles = len(triangle_set)
    pentagons = len(cycles) - triangles
    rank = len(cycles)
    require(pentagons in (0, 1, 2), "component has invalid pentagon count")
    if pentagons == 0:
        value, strict = triangle_bound(triangles)
        return BASE.Bound(value, strict, f"A_{triangles}")
    if rank == 1:
        return BASE.Bound(Fraction(-1, 4), True, "P>-1/4")
    if (triangles, pentagons) == (1, 1):
        return BASE.Bound(Fraction(3, 4), True, "TP>3/4")
    if (triangles, pentagons) == (0, 2):
        return BASE.Bound(Fraction(0), True, "PP>0")
    if (triangles, pentagons) == (2, 1) and any(
        triangle_set <= set(adjacency[cut]) for cut in internal_cuts
    ):
        return BASE.Bound(Fraction(7, 4), True, "shared-cut TTP>7/4")
    if (triangles, pentagons) == (1, 2):
        return BASE.Bound(Fraction(3, 2), True, "TPP>3/2")
    if rank == 3:
        return BASE.Bound(Fraction(0), False, "rank-3>=0")
    if (triangles, pentagons) == (3, 1) and any(
        len(triangle_set & set(adjacency[cut])) >= 2 for cut in internal_cuts
    ):
        return BASE.Bound(Fraction(1), True, "shared-pair T^3P>1")
    require(4 <= rank <= 9, f"unsupported mixed component rank {rank}")
    return BASE.Bound(Fraction(0), True, f"rank-{rank}>0")


def validate_classes(classes, colors, q_cap):
    signatures = set()
    expected_colors = Counter(colors)
    for signature, tree in classes:
        require(signature not in signatures, f"duplicate signature {signature}")
        signatures.add(signature)
        require(signature == BASE.signature(tree), f"noncanonical representative {signature}")
        require(Counter(tree.colors) == expected_colors, "wrong cycle colors")
        adjacency = BASE.adjacency(tree)
        require(len(tree.edges) == len(adjacency) - 1, "incidence graph is not a tree")
        seen = {0}
        stack = [0]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        require(len(seen) == len(adjacency), "incidence graph is disconnected")
        cycle_count = len(tree.colors)
        for cut in range(cycle_count, len(adjacency)):
            require(len(adjacency[cut]) >= 2, "degree-one cut node")
            require(all(cycle < cycle_count for cycle in adjacency[cut]), "cut-cut edge")
        for cycle, color in enumerate(tree.colors):
            capacity = q_cap if color == "Q" else BASE.CAPACITY[color]
            require(1 <= len(adjacency[cycle]) <= capacity, "cycle capacity violation")
            require(all(cut >= cycle_count for cut in adjacency[cycle]), "cycle-cycle edge")


def exact_census(colors, q_cap, bound_function):
    colors = tuple(sorted(colors))
    classes = BASE.enumerate_colors(colors, q_cap)
    validate_classes(classes, colors, q_cap)
    totals = Counter()
    safe = Counter()
    unresolved = []
    for signature, tree in classes:
        cuts = BASE.cut_count(tree)
        totals[cuts] += 1
        certificates = [
            BASE.split_certificate(tree, cycle, bound_function)
            for cycle in range(len(tree.colors))
        ]
        if any(certificate is not None for certificate in certificates):
            safe[cuts] += 1
        else:
            unresolved.append((cuts, signature, BASE.cut_profile(tree), tree.edges))
    unresolved.sort()
    require(sum(totals.values()) == len(classes), "census total mismatch")
    require(sum(safe.values()) + len(unresolved) == len(classes), "classification mismatch")
    return totals, safe, unresolved


def check_equal(actual, expected, label):
    require(actual == expected, f"{label}: expected {expected!r}, got {actual!r}")


def print_partition_result(name, result):
    all_rows, proper_rows, residual = result
    print(
        f"{name} cluster partitions: total={len(all_rows)} proper={len(proper_rows)} "
        f"direct={len(proper_rows) - len(residual)} structural={len(residual)}"
    )
    for row in residual:
        print("  structural", row)


def print_incidence_result(name, result):
    totals, safe, unresolved = result
    exceptions = Counter(row[0] for row in unresolved)
    print(f"{name} fully shared all:  {dict(sorted(totals.items()))} = {sum(totals.values())}")
    print(f"{name} fully shared SAFE: {dict(sorted(safe.items()))} = {sum(safe.values())}")
    print(f"{name} exceptions: {dict(sorted(exceptions.items()))} = {len(unresolved)}")
    for cuts, signature, profile, _ in unresolved:
        print(f"  c={cuts} cuts={profile} signature={signature}")


def rank_nine_regressions():
    cases = (
        (("T",) * 8 + ("Q",), 3, {1: 1, 2: 11, 3: 68, 4: 253, 5: 572, 6: 742, 7: 493, 8: 127}),
        (("T",) * 8 + ("Q",), 8, {1: 1, 2: 11, 3: 68, 4: 258, 5: 589, 6: 783, 7: 540, 8: 153}),
        (("T",) * 7 + ("P",) * 2, 0, {1: 1, 2: 17, 3: 150, 4: 699, 5: 1856, 6: 2714, 7: 1998, 8: 569}),
    )
    for colors, q_cap, expected in cases:
        classes = BASE.enumerate_colors(tuple(sorted(colors)), q_cap)
        validate_classes(classes, colors, q_cap)
        counts = Counter(BASE.cut_count(tree) for _, tree in classes)
        check_equal(counts, Counter(expected), "rank-nine regression")


def main():
    print("Sharp-DNN rank-ten residuals: T^9Q and T^8PP")
    tq_partitions = partition_audit(9, 1, tq_profile_bound)
    tpp_partitions = partition_audit(8, 2, tpp_profile_bound)
    for name, result in (("T^9Q", tq_partitions), ("T^8PP", tpp_partitions)):
        observed = (
            len(result[0]), len(result[1]), len(result[1]) - len(result[2]), len(result[2])
        )
        check_equal(observed, EXPECTED_PARTITIONS[name], f"{name} partitions")
        print_partition_result(name, result)

    rank_nine_regressions()
    regimes = (("q=3", "q=3", 3), ("q=4", "q=4", 4),
               ("q=5", "q=5", 5), ("q=6", "q=6", 6),
               ("q=7", "capacity 7 (conservative; q=7 is nonhostile)", 7),
               ("q=8", "q=8", 8),
               ("q>=9", "capacity >=9 (conservative hostile ledger)", 9))
    for label, display_label, capacity in regimes:
        result = exact_census(
            ("T",) * 9 + ("Q",),
            capacity,
            lambda tree, component, label=label: tq_component_bound(label, tree, component),
        )
        check_equal(result[0], Counter(EXPECTED_T9Q[label]), f"T^9Q {label} totals")
        # q=7 is actually nonhostile; retaining the hostile ledger there is a
        # conservative weakening that stress-tests the same three repairs.
        expected_signatures = {T9Q_COMMON} if label in {"q=3", "q=4", "q=6", "q=8"} else T9Q_HOSTILE
        check_equal({row[1] for row in result[2]}, expected_signatures, f"T^9Q {label} exceptions")
        print_incidence_result(f"T^9Q {display_label}", result)

    tpp_result = exact_census(("T",) * 8 + ("P",) * 2, 0, tpp_component_bound)
    check_equal(tpp_result[0], Counter(EXPECTED_T8PP), "T^8PP totals")
    check_equal({row[1] for row in tpp_result[2]}, T8PP_EXCEPTIONS, "T^8PP exceptions")
    check_equal(Counter(row[0] for row in tpp_result[2]), Counter({1: 1, 2: 2, 3: 4, 4: 1, 5: 1}), "T^8PP exception cuts")
    print_incidence_result("T^8PP", tpp_result)
    print("PASS: all frozen exact checks succeeded (including under python -O)")


if __name__ == "__main__":
    main()
