#!/usr/bin/env python3
"""Exact partition and ordinary-split censuses for rank-nine cactus residuals."""

from collections import Counter
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = spec_from_file_location(
    "octacyclic_incidence", HERE / "octacyclic-fully-shared-incidence-census.py"
)
BASE = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BASE)

TRIANGLE_MARGIN = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1, 7: 0, 8: 0}


def partitions(triangles, distinguished, minimum=(0, 0)):
    result = []
    for t in range(triangles + 1):
        for d in range(distinguished + 1):
            part = (t, d)
            if t + d == 0 or part < minimum:
                continue
            if part == (triangles, distinguished):
                result.append((part,))
                continue
            for rest in partitions(triangles - t, distinguished - d, part):
                result.append((part,) + rest)
    return result


def triangle_bound(triangles):
    return Fraction(TRIANGLE_MARGIN[triangles]), True


def tq_profile_bound(part):
    triangles, q_count = part
    rank = triangles + q_count
    if q_count == 0:
        return triangle_bound(triangles)
    if triangles == 0:
        return Fraction(-1), False
    if triangles == 1:
        return Fraction(0), True
    if rank in (2, 3):
        return Fraction(0), False
    return Fraction(0), True


def tpp_profile_bound(part):
    triangles, pentagons = part
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
    proper_rows = [row for row in all_rows if len(row) > 1]
    residual = []
    for row in proper_rows:
        bounds = [bound(part) for part in row]
        total = sum((value for value, _ in bounds), Fraction())
        strict = any(flag for _, flag in bounds)
        if not (total > 0 or (total == 0 and strict)):
            residual.append(row)
    return all_rows, proper_rows, residual


def tq_component_bound(tree, component, q_label):
    counts = Counter(tree.colors[cycle] for cycle in component[0])
    triangles, q_count = counts["T"], counts["Q"]
    if q_count == 0:
        return BASE.Bound(Fraction(TRIANGLE_MARGIN[triangles]), True, f"A_{triangles}")
    if triangles == 0:
        if q_label == "q=3":
            return BASE.Bound(Fraction(0), True, "Q=T>0")
        if q_label in ("q=4", "q=6", "q=8"):
            return BASE.Bound(Fraction(0), False, "even Q>=0")
        return BASE.Bound(Fraction(-1), True, "hostile Q>-1")
    if triangles == 1:
        return BASE.Bound(Fraction(0), True, "TQ>0")
    if triangles == 2:
        return BASE.Bound(Fraction(0), False, "TTQ>=0")
    return BASE.Bound(Fraction(0), True, f"rank-{triangles + 1}>0")


def tpp_component_bound(tree, component):
    cycles, internal_cuts, adjacency = component
    triangle_set = {cycle for cycle in cycles if tree.colors[cycle] == "T"}
    triangles = len(triangle_set)
    pentagons = len(cycles) - triangles
    rank = len(cycles)
    if pentagons == 0:
        return BASE.Bound(Fraction(TRIANGLE_MARGIN[triangles]), True, f"A_{triangles}")
    if rank == 1:
        return BASE.Bound(Fraction(-1, 4), True, "P>-1/4")
    if (triangles, pentagons) == (1, 1):
        return BASE.Bound(Fraction(3, 4), True, "TP>3/4")
    if (triangles, pentagons) == (0, 2):
        return BASE.Bound(Fraction(0), True, "PP>0")
    if (triangles, pentagons) == (2, 1):
        if any(triangle_set <= set(adjacency[cut]) for cut in internal_cuts):
            return BASE.Bound(Fraction(7, 4), True, "shared-cut TTP>7/4")
    if (triangles, pentagons) == (1, 2):
        return BASE.Bound(Fraction(3, 2), True, "TPP>3/2")
    if rank == 3:
        return BASE.Bound(Fraction(0), False, "rank-3>=0")
    if (triangles, pentagons) == (3, 1):
        if any(len(triangle_set & set(adjacency[cut])) >= 2 for cut in internal_cuts):
            return BASE.Bound(Fraction(1), True, "shared-pair T^3P>1")
    assert 4 <= rank <= 8
    return BASE.Bound(Fraction(0), True, f"rank-{rank}>0")


def print_partition_result(name, result):
    all_rows, proper_rows, residual = result
    print(f"{name} partitions: {len(all_rows)} total, {len(proper_rows)} proper")
    print(f"{name} direct rows: {len(proper_rows) - len(residual)}")
    print(f"{name} structural rows: {len(residual)}")
    for row in residual:
        print(" ", row)


def print_incidence_result(name, result):
    totals, resolved, _, _, _, unresolved = result
    print(f"{name} incidence totals: {dict(sorted(totals.items()))}")
    print(f"{name} ordinary-split safe: {sum(resolved.values())}/{sum(totals.values())}")
    print(f"{name} exceptions by cut count: {dict(sorted(Counter(x[0] for x in unresolved).items()))}")
    for row in unresolved:
        print(" ", row)


def main():
    tq_partitions = partition_audit(8, 1, tq_profile_bound)
    tpp_partitions = partition_audit(7, 2, tpp_profile_bound)
    assert (len(tq_partitions[0]), len(tq_partitions[1]), len(tq_partitions[2])) == (67, 66, 3)
    assert (len(tpp_partitions[0]), len(tpp_partitions[1]), len(tpp_partitions[2])) == (118, 117, 8)
    print_partition_result("T^8Q", tq_partitions)
    print_partition_result("T^7PP", tpp_partitions)

    expected_tq_totals = {
        3: {1: 1, 2: 11, 3: 68, 4: 253, 5: 572, 6: 742, 7: 493, 8: 127},
        4: {1: 1, 2: 11, 3: 68, 4: 258, 5: 586, 6: 774, 7: 525, 8: 142},
        5: {1: 1, 2: 11, 3: 68, 4: 258, 5: 589, 6: 781, 7: 536, 8: 148},
        6: {1: 1, 2: 11, 3: 68, 4: 258, 5: 589, 6: 783, 7: 539, 8: 151},
        7: {1: 1, 2: 11, 3: 68, 4: 258, 5: 589, 6: 783, 7: 540, 8: 152},
        8: {1: 1, 2: 11, 3: 68, 4: 258, 5: 589, 6: 783, 7: 540, 8: 153},
    }
    for q_label, q_cap in (("q=3", 3), ("q=4", 4), ("q=5", 5), ("q=6", 6), ("q=7", 7), ("q=8+", 8)):
        result = BASE.census(
            ("T",) * 8 + ("Q",),
            q_cap,
            lambda tree, component, label=q_label: tq_component_bound(tree, component, label),
        )
        assert dict(result[0]) == expected_tq_totals[q_cap]
        expected_exceptions = (
            Counter({1: 1}) if q_label in ("q=3", "q=4", "q=6")
            else Counter({1: 1, 2: 1})
        )
        assert Counter(row[0] for row in result[-1]) == expected_exceptions
        print_incidence_result(f"T^8Q {q_label}", result)

    tpp_result = BASE.census(("T",) * 7 + ("P",) * 2, 0, tpp_component_bound)
    assert tpp_result[0] == Counter({1: 1, 2: 17, 3: 150, 4: 699, 5: 1856, 6: 2714, 7: 1998, 8: 569})
    assert Counter(row[0] for row in tpp_result[-1]) == Counter({1: 1, 2: 2, 3: 2, 4: 1, 5: 1})
    print_incidence_result("T^7PP", tpp_result)


if __name__ == "__main__":
    main()
