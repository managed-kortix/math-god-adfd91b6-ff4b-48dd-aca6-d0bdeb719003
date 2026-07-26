#!/usr/bin/env python3
"""Compressed exact rank-ten incidence censuses for T^9Q and T^8PP.

This reuses the exhaustively checked color-preserving cycle-leaf recurrence from
the rank-nine census.  All ledger values are fractions.Fraction objects.  The
output is a finite structural experiment, not a theorem checker or theorem
claim.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SPEC = spec_from_file_location(
    "rank_nine_shared_incidence",
    HERE / "nonacyclic-fully-shared-incidence-census.py",
)
BASE = module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("rank-nine census dependency has no import loader")
sys.modules[SPEC.name] = BASE
SPEC.loader.exec_module(BASE)


TRIANGLE_MARGIN = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1, 7: 0, 8: 0}
EXPECTED_TQ = {
    "q=3": {1: 1, 2: 12, 3: 91, 4: 406, 5: 1178, 6: 2115, 7: 2250, 8: 1246, 9: 275},
    "q=4": {1: 1, 2: 12, 3: 91, 4: 412, 5: 1203, 6: 2187, 7: 2361, 8: 1340, 9: 306},
    "q=5": {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2201, 7: 2393, 8: 1372, 9: 321},
    "q=6": {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2204, 7: 2400, 8: 1383, 9: 327},
    "q=7": {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2204, 7: 2402, 8: 1386, 9: 330},
    "q=8": {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2204, 7: 2402, 8: 1387, 9: 331},
    "q=9": {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2204, 7: 2402, 8: 1387, 9: 332},
    "q>=10": {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2204, 7: 2402, 8: 1387, 9: 332},
}
EXPECTED_TPP = {1: 1, 2: 19, 3: 204, 4: 1155, 5: 3990, 6: 8135, 7: 9615, 8: 5843, 9: 1424}


def tq_bound(label, tree, component):
    counts = Counter(tree.colors[cycle] for cycle in component[0])
    triangles, q_count = counts["T"], counts["Q"]
    if q_count not in (0, 1):
        raise RuntimeError("a retained TQ packet contains multiple Q cycles")
    if not q_count:
        return BASE.Bound(
            Fraction(TRIANGLE_MARGIN[triangles]), True, f"A_{triangles}"
        )
    if triangles == 0:
        if label == "q=3":
            return BASE.Bound(Fraction(0), True, "Q=T > 0")
        if label in {"q=4", "q=6", "q=8"}:
            return BASE.Bound(Fraction(0), False, "even Q >= 0")
        return BASE.Bound(Fraction(-1), True, "hostile Q > -1")
    if triangles == 1:
        return BASE.Bound(Fraction(0), True, "TQ > 0")
    if triangles == 2:
        return BASE.Bound(Fraction(0), False, "TTQ >= 0")
    return BASE.Bound(
        Fraction(0), True, f"input lower-rank T^{triangles}Q > 0"
    )


def tpp_bound(tree, component):
    cycles, internal_cuts, adj = component
    triangle_set = {cycle for cycle in cycles if tree.colors[cycle] == "T"}
    triangles = len(triangle_set)
    pentagons = len(cycles) - triangles
    rank = len(cycles)
    if pentagons == 0:
        return BASE.Bound(
            Fraction(TRIANGLE_MARGIN[triangles]), True, f"A_{triangles}"
        )
    if rank == 1:
        return BASE.Bound(Fraction(-1, 4), True, "P > -1/4")
    if (triangles, pentagons) == (1, 1):
        return BASE.Bound(Fraction(3, 4), True, "TP > 3/4")
    if (triangles, pentagons) == (0, 2):
        return BASE.Bound(Fraction(0), True, "PP > 0")
    if (triangles, pentagons) == (2, 1) and any(
        triangle_set <= set(adj[cut]) for cut in internal_cuts
    ):
        return BASE.Bound(Fraction(7, 4), True, "common-cut TTP > 7/4")
    if (triangles, pentagons) == (1, 2):
        return BASE.Bound(Fraction(3, 2), True, "TPP > 3/2")
    if rank == 3:
        return BASE.Bound(Fraction(0), False, "generic rank three >= 0")
    if (triangles, pentagons) == (3, 1) and any(
        len(triangle_set & set(adj[cut])) >= 2 for cut in internal_cuts
    ):
        return BASE.Bound(Fraction(1), True, "shared-pair TTTP > 1")
    if not 4 <= rank <= 8:
        raise RuntimeError(f"unrecognized retained TPP packet of rank {rank}")
    return BASE.Bound(Fraction(0), True, f"input generic rank-{rank} > 0")


def exception_templates(unresolved):
    """Compress exceptions by cut count and sorted colored cut neighborhoods."""
    return Counter((cuts, profile) for cuts, _, profile, _ in unresolved)


def run_case(name, colors, q_cap, bound_function):
    result = BASE.census(colors, q_cap, bound_function)
    BASE.display(name, result)
    print("  exception templates:", dict(sorted(exception_templates(result[-1]).items())))
    return result


def regress_rank_nine():
    cases = (
        (("T",) * 8 + ("Q",), 3, BASE.EXPECTED_TQ["q=3"]),
        (("T",) * 8 + ("Q",), 8, BASE.EXPECTED_TQ["q=8"]),
        (("T",) * 7 + ("P",) * 2, 0, BASE.EXPECTED_TPP),
    )
    for colors, q_cap, expected in cases:
        classes = BASE.enumerate_colors(tuple(sorted(colors)), q_cap)
        BASE.validate_classes(classes, q_cap)
        counts = Counter(BASE.cut_count(tree) for _, tree in classes)
        if counts != Counter(expected):
            raise RuntimeError("rank-nine generator regression failed")


def main():
    regress_rank_nine()
    regimes = (
        ("q=3", 3),
        ("q=4", 4),
        ("q=5", 5),
        ("q=6", 6),
        ("q=7", 7),
        ("q=8", 8),
        ("q=9", 9),
        ("q>=10", 9),
    )
    for label, cap in regimes:
        result = run_case(
            f"T^9Q {label}",
            ("T",) * 9 + ("Q",),
            cap,
            lambda tree, component, label=label: tq_bound(label, tree, component),
        )
        if result[0] != Counter(EXPECTED_TQ[label]):
            raise RuntimeError(f"T^9Q {label} count regression")
        expected_exceptions = Counter({1: 1}) if label in {"q=3", "q=4", "q=6", "q=8"} else Counter({1: 1, 2: 1, 3: 1})
        if Counter(item[0] for item in result[-1]) != expected_exceptions:
            raise RuntimeError(f"T^9Q {label} exception regression")
    result = run_case("T^8PP", ("T",) * 8 + ("P",) * 2, 0, tpp_bound)
    if result[0] != Counter(EXPECTED_TPP):
        raise RuntimeError("T^8PP count regression")
    if Counter(item[0] for item in result[-1]) != Counter({1: 1, 2: 2, 3: 4, 4: 1, 5: 1}):
        raise RuntimeError("T^8PP exception regression")


if __name__ == "__main__":
    main()
