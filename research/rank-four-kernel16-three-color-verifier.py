#!/usr/bin/env python3
"""Fail-closed exact audit of the three-color certificate for kernel 16.

Kernel 16 is K_3,3.  Every physical parity row is regenerated, every one of
the 3^6 color maps is tested, and all arithmetic is integral.  The script
checks the exhaustive census against immutable ledgers and rejects mutations.
"""

from collections import Counter
from copy import deepcopy
from hashlib import sha256
from fractions import Fraction
from itertools import combinations, permutations, product


KERNEL16_CODE = (0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0)
EDGES = tuple((u, v) for u in range(3) for v in range(3, 6))
EXPECTED_PHYSICAL_ROWS = 512
EXPECTED_ORBITS = 26
EXPECTED_SCORE_HISTOGRAM = ((0, 1), (3, 6), (4, 27), (5, 63),
                            (6, 147), (7, 168), (8, 81), (9, 19))
EXPECTED_Q_SCORE_CENSUS = (
    ((0, 0), 1), ((1, 5), 9), ((2, 4), 18), ((2, 6), 18),
    ((3, 3), 6), ((3, 5), 36), ((3, 7), 42), ((4, 4), 9),
    ((4, 6), 81), ((4, 8), 36), ((5, 5), 18), ((5, 7), 108),
    ((6, 6), 48), ((6, 8), 36), ((7, 7), 18), ((7, 9), 18),
    ((8, 8), 9), ((9, 9), 1),
)
EXPECTED_ORBIT_Q_SCORE_CENSUS = (
    ((0, 0), 1), ((1, 5), 1), ((2, 4), 1), ((2, 6), 1),
    ((3, 3), 1), ((3, 5), 1), ((3, 7), 2), ((4, 4), 1),
    ((4, 6), 3), ((4, 8), 1), ((5, 5), 2), ((5, 7), 3),
    ((6, 6), 3), ((6, 8), 1), ((7, 7), 1), ((7, 9), 1),
    ((8, 8), 1), ((9, 9), 1),
)
EXPECTED_PAYLOAD_SHA256 = "cb7e57696bb3667d36fa0f65747b1f26a037ae4a9e506d0a69ebf0525e2d0ec4"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def kernel_edges():
    return tuple(edge for multiplicity, edge in
                 zip(KERNEL16_CODE, combinations(range(6), 2)) if multiplicity)


def color_score(row, colors):
    require(len(row) == 9 and all(type(bit) is int and bit in (0, 1) for bit in row),
            "malformed physical row")
    require(len(colors) == 6
            and all(type(color) is int and color in (0, 1, 2) for color in colors),
            "malformed three-color map")
    for odd, (u, v) in zip(row, EDGES):
        if odd and colors[u] == colors[v]:
            return None
    return sum(row) + 2 * sum(
        not odd and colors[u] != colors[v]
        for odd, (u, v) in zip(row, EDGES))


def optimize_row(row):
    best = None
    witness = None
    for colors in product(range(3), repeat=6):
        score = color_score(row, colors)
        if score is not None and (best is None or score < best):
            best = score
            witness = colors
    require(best is not None and witness is not None,
            "physical row has no proper coloring of its odd-edge graph")
    return best, witness


def automorphisms():
    result = []
    for left in permutations(range(3)):
        for right in permutations(range(3)):
            result.append(tuple(left) + tuple(v + 3 for v in right))
            result.append(tuple(v + 3 for v in left) + tuple(right))
    require(len(result) == 72 and len(set(result)) == 72,
            "K_3,3 automorphism generation failed")
    return tuple(result)


def relabel(row, permutation):
    lookup = dict(zip(EDGES, row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))]
                 for u, v in EDGES)


def canonical_row(row):
    return min(relabel(row, permutation) for permutation in automorphisms())


def payload(records):
    return "".join(
        f"{''.join(map(str, row))}:{score}:{''.join(map(str, colors))}\n"
        for row, score, colors in records)


def audit(expected_rows=EXPECTED_PHYSICAL_ROWS,
          expected_histogram=EXPECTED_SCORE_HISTOGRAM,
          expected_digest=EXPECTED_PAYLOAD_SHA256):
    require(kernel_edges() == EDGES, "kernel-16 code no longer decodes as K_3,3")
    require(sum(KERNEL16_CODE) == 9, "kernel-16 edge ledger changed")
    require(expected_rows == EXPECTED_PHYSICAL_ROWS, "physical-row ledger changed")
    require(expected_histogram == EXPECTED_SCORE_HISTOGRAM,
            "score histogram fixture changed")
    require(expected_digest == EXPECTED_PAYLOAD_SHA256, "payload digest fixture changed")

    rows = tuple(product((0, 1), repeat=len(EDGES)))
    require(len(rows) == expected_rows and len(set(rows)) == expected_rows,
            "physical parity enumeration is not exactly 2^9")
    records = tuple((row,) + optimize_row(row) for row in rows)
    for row, score, colors in records:
        require(color_score(row, colors) == score, "stored witness score changed")
        require(score <= 9, "three-color certificate exceeds rank-four budget")

    histogram = tuple(sorted(Counter(score for _, score, _ in records).items()))
    require(histogram == expected_histogram, "exact score histogram changed")
    q_score = tuple(sorted(Counter((sum(row), score)
                                   for row, score, _ in records).items()))
    require(q_score == EXPECTED_Q_SCORE_CENSUS, "q/score census changed")

    representatives = tuple(sorted({canonical_row(row) for row in rows}))
    require(len(representatives) == EXPECTED_ORBITS, "automorphism-orbit count changed")
    score_by_row = {row: score for row, score, _ in records}
    orbit_census = tuple(sorted(Counter((sum(row), score_by_row[row])
                                        for row in representatives).items()))
    require(orbit_census == EXPECTED_ORBIT_Q_SCORE_CENSUS,
            "automorphism-orbit q/score census changed")
    for row in rows:
        require(score_by_row[row] == score_by_row[canonical_row(row)],
                "score is not invariant under a kernel automorphism")

    digest = sha256(payload(records).encode("ascii")).hexdigest()
    require(digest == expected_digest, "deterministic witness payload changed")
    return records, representatives, histogram, digest


def expect_rejected(action, label):
    try:
        action()
    except (RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    mutations = (
        ("physical-row count", {"expected_rows": 19683}),
        ("score histogram", {"expected_histogram": ((9, 512),)}),
        ("payload digest", {"expected_digest": "0" * 64}),
    )
    for label, changes in mutations:
        expect_rejected(lambda changes=deepcopy(changes): audit(**changes), label)
    malformed = (0,) * 8 + (2,)
    expect_rejected(lambda: optimize_row(malformed), "nonbinary physical row")
    for label, value in (("boolean physical row", True),
                         ("floating physical row", 1.0),
                         ("nonintegral physical row", Fraction(1, 2))):
        expect_rejected(lambda value=value: optimize_row((0,) * 8 + (value,)), label)
    return len(mutations) + 4


def main():
    records, representatives, histogram, digest = audit()
    mutations = hostile_self_checks()
    require(mutations == 7, "hostile mutation count changed")
    print("kernel16 K_3,3 three-color audit: exact exhaustive proof passed")
    print(f"physical_parity_rows: {len(records)} (=2^9; not 3^9)")
    print(f"automorphism_orbits: {len(representatives)}")
    print("minimum_score_histogram: " +
          ",".join(f"{score}:{count}" for score, count in histogram))
    maximum_score = max(score for _, score, _ in records)
    require(maximum_score % 3 == 0, "maximum score does not encode an exact excess")
    print(f"maximum_integer_score: {maximum_score}")
    print(f"maximum_three_color_excess: {maximum_score // 3}")
    print(f"witness_payload_sha256: {digest}")
    print(f"rejected_hostile_mutations: {mutations}")


if __name__ == "__main__":
    main()
