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
from hashlib import sha256
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
FIXED_CAPACITY = {"T": 3, "P": 5}
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
EXPECTED_CLASS_DIGESTS = {
    ("TQ", 3): "78cfe00c5dd739abf40e0b9a3430e2ac2eca3e01869b3ecec650dabbfb25bb4d",
    ("TQ", 4): "22d7529cf9eb828f0622bd0db6d3035f7f9d738d8df7e4342879e5e7c8d9e74d",
    ("TQ", 5): "59a1fea893b7962abb40a84b7a8761702f68316d05462c57454c5fa0086ef8ad",
    ("TQ", 6): "98e14a529fb8bb085acfaf1cc053348ce601772f113e327591f0d33b49c2f495",
    ("TQ", 7): "3bf10013f3a249b05a3480a8d0aff5c25336de38037cc4208d9ecc5b0b99119d",
    ("TQ", 8): "f32dbdcd744b374b287d29f2d3780a28f723fa2e7fe4bf8993c95189dda6fad2",
    ("TQ", 9): "7ebb60de1db8245229b982f66b7695fdcbfcc69924d158e273058ac3a6cb83eb",
    ("TPP", 0): "9aa6813cb87e1db0748faf441b8941145fbedb5af55386404bd9cfcbe10a6e3b",
}
EXPECTED_RESIDUAL_DIGESTS = {
    "small": "e78f3397dec51558412e2185b74aff1317b3836881bd320c91a5cc2cb8b3cd49",
    "hostile": "ac33b61aa7fc00e499cac468d282ed7c12ffd5ab56f328399a7d2f3c6557617f",
    "TPP": "461351660aa2d8e23d36ca54441275acfd022ebfec80ba599698ffcbb86cb35a",
}
EXPECTED_RANK_NINE_DIGESTS = {
    ("TQ", 3): "ab1b56bb87453b119d47b5b7243834a774411be790418096e831be3ac9454302",
    ("TQ", 8): "6d208a1638f5107327547cb304fe5480e04df57f8337e4487f2ad89c14d57e32",
    ("TPP", 0): "29b8e8525bf1d0ac4609e177b95b19d4dda095c569cb0a4dfe506d3243e4e0c2",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def signature_digest(signatures):
    return sha256(("\n".join(signatures) + "\n").encode("ascii")).hexdigest()


def color_capacity(color, q_cap):
    if color == "Q":
        return q_cap
    require(color in FIXED_CAPACITY, f"unknown cycle color {color!r}")
    return FIXED_CAPACITY[color]


def canonical_signature(tree, adj):
    """Compute the center-rooted code locally, independently of the dependency."""
    degrees = [len(row) for row in adj]
    leaves = [vertex for vertex, degree in enumerate(degrees) if degree <= 1]
    remaining = len(adj)
    while remaining > 2:
        require(leaves, "tree center search stalled")
        remaining -= len(leaves)
        next_leaves = []
        for leaf in leaves:
            for neighbor in adj[leaf]:
                degrees[neighbor] -= 1
                if degrees[neighbor] == 1:
                    next_leaves.append(neighbor)
        leaves = next_leaves

    cycle_count = len(tree.colors)

    def rooted(vertex, parent):
        color = tree.colors[vertex] if vertex < cycle_count else "X"
        children = sorted(
            rooted(neighbor, vertex) for neighbor in adj[vertex] if neighbor != parent
        )
        return color + "(" + "".join(children) + ")"

    return min(rooted(center, -1) for center in leaves)


def validate_classes(classes, colors, q_cap, expected_counts, expected_digest):
    """Fail-closed structural, canonical, completeness, and digest audit."""
    require(classes, "canonical generator returned no classes")
    require(tuple(sig for sig, _ in classes) == tuple(sorted(sig for sig, _ in classes)),
            "canonical classes are not signature-sorted")
    require(len({sig for sig, _ in classes}) == len(classes),
            "duplicate canonical signature")
    counts = Counter()
    expected_colors = Counter(colors)
    for stored_signature, tree in classes:
        cycle_count = len(tree.colors)
        cut_total = len(tree.edges) + 1 - cycle_count
        vertex_count = cycle_count + cut_total
        require(Counter(tree.colors) == expected_colors, "canonical row has incorrect colors")
        require(cut_total >= 1 and len(tree.edges) == vertex_count - 1,
                "canonical row has invalid tree size")
        require(len(set(tree.edges)) == len(tree.edges), "canonical row repeats an edge")
        adj = [[] for _ in range(vertex_count)]
        for cycle, cut in tree.edges:
            require(0 <= cycle < cycle_count and cycle_count <= cut < vertex_count,
                    "canonical row has a non-incidence edge or invalid vertex")
            adj[cycle].append(cut)
            adj[cut].append(cycle)
        require(all(len(adj[cut]) >= 2 for cut in range(cycle_count, vertex_count)),
                "canonical row contains a redundant cut leaf")
        require(all(1 <= len(adj[cycle]) <= color_capacity(color, q_cap)
                    for cycle, color in enumerate(tree.colors)),
                "canonical row violates cycle capacity")
        seen = {0}
        stack = [0]
        while stack:
            vertex = stack.pop()
            for neighbor in adj[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        require(len(seen) == vertex_count, "canonical row is disconnected")
        require(stored_signature == canonical_signature(tree, adj),
                "stored signature is not the independent canonical code")
        counts[cut_total] += 1
    require(counts == Counter(expected_counts), "canonical cut-count census changed")
    actual_digest = signature_digest(sig for sig, _ in classes)
    require(actual_digest == expected_digest, "canonical signature digest changed")
    return actual_digest


def validate_result(result, expected_counts, expected_exceptions, residual_digest):
    totals, resolved, choices, support, margins, unresolved = result
    total = sum(totals.values())
    require(totals == Counter(expected_counts), "incidence count regression")
    require(sum(resolved.values()) + len(unresolved) == total,
            "resolved/unresolved ledger is incomplete")
    require(sum(choices.values()) == total, "SAFE-choice ledger is incomplete")
    require(sum(support.values()) == total, "SAFE-support ledger is incomplete")
    require(sum(margins.values()) == sum(resolved.values()),
            "best-margin ledger is incomplete")
    require(Counter(item[0] for item in unresolved) == expected_exceptions,
            "exception census changed")
    require(signature_digest(item[1] for item in unresolved) == residual_digest,
            "canonical residual digest changed")


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


def run_case(name, colors, q_cap, bound_function, expected_counts, class_digest):
    classes = BASE.enumerate_colors(tuple(sorted(colors)), q_cap)
    actual_digest = validate_classes(
        classes, colors, q_cap, expected_counts, class_digest
    )
    result = BASE.census(colors, q_cap, bound_function)
    BASE.display(name, result)
    print("  independent canonical sha256:", actual_digest)
    print("  exception templates:", dict(sorted(exception_templates(result[-1]).items())))
    return result


def regress_rank_nine():
    cases = (
        (("T",) * 8 + ("Q",), 3, BASE.EXPECTED_TQ["q=3"], ("TQ", 3)),
        (("T",) * 8 + ("Q",), 8, BASE.EXPECTED_TQ["q=8"], ("TQ", 8)),
        (("T",) * 7 + ("P",) * 2, 0, BASE.EXPECTED_TPP, ("TPP", 0)),
    )
    for colors, q_cap, expected, digest_key in cases:
        classes = BASE.enumerate_colors(tuple(sorted(colors)), q_cap)
        validate_classes(
            classes,
            colors,
            q_cap,
            expected,
            EXPECTED_RANK_NINE_DIGESTS[digest_key],
        )


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
            EXPECTED_TQ[label],
            EXPECTED_CLASS_DIGESTS[("TQ", cap)],
        )
        expected_exceptions = Counter({1: 1}) if label in {"q=3", "q=4", "q=6", "q=8"} else Counter({1: 1, 2: 1, 3: 1})
        residual_key = "small" if len(expected_exceptions) == 1 else "hostile"
        validate_result(
            result,
            EXPECTED_TQ[label],
            expected_exceptions,
            EXPECTED_RESIDUAL_DIGESTS[residual_key],
        )
    result = run_case(
        "T^8PP",
        ("T",) * 8 + ("P",) * 2,
        0,
        tpp_bound,
        EXPECTED_TPP,
        EXPECTED_CLASS_DIGESTS[("TPP", 0)],
    )
    validate_result(
        result,
        EXPECTED_TPP,
        Counter({1: 1, 2: 2, 3: 4, 4: 1, 5: 1}),
        EXPECTED_RESIDUAL_DIGESTS["TPP"],
    )


if __name__ == "__main__":
    main()
