#!/usr/bin/env python3
"""Exact physical-row audit for switched all-odd Gram templates on kernel 17."""

from collections import Counter
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product


KERNEL17_CODE = (0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0)
EDGES = ((0, 3), (0, 4), (0, 5), (1, 2), (1, 4), (1, 5),
         (2, 3), (2, 5), (3, 4))
ALL_ODD_ANGLES = (0, 1, 5, 2, 4, 3)
TEMPLATE_ANGLES = (
    ALL_ODD_ANGLES,
    (0, 0, 1, 1, 2, 2),
    (0, 1, 0, 2, 1, 2),
    (0, 0, 0, 1, 1, 1),
    (0, 1, 2, 1, 2, 0),
    (0, 0, 1, 2, 2, 1),
    (0, 1, 0, 2, 2, 0),
)
EXPECTED_SINGLE_COVER = 284
EXPECTED_SINGLE_RESIDUAL = 228
EXPECTED_SINGLE_ORBITS = (46, 28)
EXPECTED_TEMPLATE_GAINS = (284, 123, 56, 24, 13, 8, 4)
EXPECTED_COST_HISTOGRAM = (
    ((170, 3, -32), 18), ((57, 1, -32), 36), ((88, 3, -16), 12),
    ((172, 3, -32), 8), ((89, 3, -16), 48), ((2, 1, 0), 2),
    ((30, 1, -16), 66), ((7, 3, 0), 12), ((91, 3, -16), 12),
    ((8, 3, 0), 30), ((3, 1, 0), 40), ((176, 3, -32), 12),
    ((10, 3, 0), 18), ((94, 3, -16), 12), ((95, 3, -16), 36),
    ((4, 1, 0), 3), ((137, 3, -24), 24), ((32, 1, -16), 6),
    ((13, 3, 0), 18), ((55, 3, -8), 12), ((14, 3, 0), 39),
    ((56, 3, -8), 24), ((5, 1, 0), 12), ((6, 1, 0), 3),
    ((19, 3, 0), 6), ((20, 3, 0), 3),
)
EXPECTED_PAYLOAD_SHA256 = "2b32eb2de2e3b3773126b3de96501c0720d25961969acfec05227292bead9f6a"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(left, right):
    if left is None or right is None:
        return None
    return left[0] + right[0], left[1] + right[1]


def compare(left, right):
    """Compare a+b*sqrt(3) exactly."""
    a = left[0] - right[0]
    b = left[1] - right[1]
    if not b:
        return (a > 0) - (a < 0)
    if not a:
        return (b > 0) - (b < 0)
    if (a > 0) == (b > 0):
        return 1 if a > 0 else -1
    square_sign = (a * a > 3 * b * b) - (a * a < 3 * b * b)
    return square_sign if a > 0 else -square_sign


def term(odd, twice_correlation):
    table = {
        (1, -2): (Fraction(0), Fraction(0)),
        (0, -2): (Fraction(2), Fraction(0)),
        (1, -1): (Fraction(1, 3), Fraction(0)),
        (0, -1): (Fraction(2, 3), Fraction(0)),
        (1, 1): (Fraction(3), Fraction(0)),
        (0, 1): (Fraction(14), Fraction(-8)),
        (1, 2): None,
        (0, 2): (Fraction(0), Fraction(0)),
    }
    return table[(odd, twice_correlation)]


def correlations(angles):
    require(len(angles) == 6 and all(a in range(6) for a in angles),
            "malformed pi/3 angle template")
    cosine_twice = (2, 1, -1, -2, -1, 1)
    return tuple(cosine_twice[(angles[u] - angles[v]) % 6] for u, v in EDGES)


def cost(row, angles):
    require(len(row) == 9 and all(bit in (0, 1) for bit in row),
            "malformed physical parity row")
    total = (Fraction(0), Fraction(0))
    for odd, correlation in zip(row, correlations(angles)):
        total = add(total, term(odd, correlation))
    return total


def switch_angles(angles, switch):
    require(len(switch) == 6 and switch[0] == 0 and
            all(bit in (0, 1) for bit in switch), "malformed switch")
    return tuple((angle + 3 * bit) % 6 for angle, bit in zip(angles, switch))


def switched_costs(row, angles):
    return tuple(cost(row, switch_angles(angles, (0,) + tail))
                 for tail in product((0, 1), repeat=5))


def best_switched_cost(row, angles):
    finite = tuple(value for value in switched_costs(row, angles) if value is not None)
    require(finite, "template has no finite switch for physical row")
    best = finite[0]
    for value in finite[1:]:
        if compare(value, best) < 0:
            best = value
    return best


def within_budget(value):
    return value is not None and compare(value, (Fraction(3), Fraction(0))) <= 0


def kernel_edges():
    return tuple(edge for multiplicity, edge in
                 zip(KERNEL17_CODE, combinations(range(6), 2)) if multiplicity)


def automorphisms():
    return tuple(permutation for permutation in permutations(range(6))
                 if {tuple(sorted((permutation[u], permutation[v]))) for u, v in EDGES}
                 == set(EDGES))


def relabel(row, permutation):
    lookup = dict(zip(EDGES, row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))]
                 for u, v in EDGES)


def canonical_row(row):
    return min(relabel(row, permutation) for permutation in automorphisms())


def encode(value):
    return value[0].numerator, value[0].denominator, value[1].numerator


def payload(records):
    return "".join(f"{''.join(map(str, row))}:{encode(value)}\n"
                   for row, value in records)


def audit(expected_digest=EXPECTED_PAYLOAD_SHA256,
          templates=TEMPLATE_ANGLES):
    require(kernel_edges() == EDGES, "kernel-17 edge decoding changed")
    require(sum(KERNEL17_CODE) == 9 and len(set(EDGES)) == 9,
            "kernel-17 edge ledger changed")
    require(len(automorphisms()) == 12, "kernel-17 automorphism group changed")
    require(templates == TEMPLATE_ANGLES, "template fixture changed")

    rows = tuple(product((0, 1), repeat=9))
    require(len(rows) == 512 and len(set(rows)) == 512,
            "physical census is not exactly 2^9")
    records = tuple((row, best_switched_cost(row, ALL_ODD_ANGLES)) for row in rows)
    histogram = Counter(encode(value) for _, value in records)
    require(histogram == Counter(dict(EXPECTED_COST_HISTOGRAM)),
            "single-template cost census changed")
    covered = {row for row, value in records if within_budget(value)}
    residual = set(rows) - covered
    require((len(covered), len(residual)) ==
            (EXPECTED_SINGLE_COVER, EXPECTED_SINGLE_RESIDUAL),
            "single-template cover/residual changed")
    cover_orbits = {canonical_row(row) for row in covered}
    residual_orbits = {canonical_row(row) for row in residual}
    require((len(cover_orbits), len(residual_orbits)) == EXPECTED_SINGLE_ORBITS,
            "single-template orbit census changed")

    remaining = set(rows)
    gains = []
    for angles in templates:
        template_cover = {row for row in rows if within_budget(best_switched_cost(row, angles))}
        gain = remaining & template_cover
        gains.append(len(gain))
        remaining -= template_cover
    require(tuple(gains) == EXPECTED_TEMPLATE_GAINS, "template gain ledger changed")
    require(not remaining and sum(gains) == 512, "template family leaves a residual")

    digest = sha256(payload(records).encode("ascii")).hexdigest()
    require(expected_digest == EXPECTED_PAYLOAD_SHA256, "digest fixture argument changed")
    require(digest == expected_digest, "single-template payload digest changed")
    return records, cover_orbits, residual_orbits, tuple(gains), digest


def expect_rejected(action, label):
    try:
        action()
    except (RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    expect_rejected(lambda: audit(expected_digest="0" * 64), "payload digest")
    changed = list(deepcopy(TEMPLATE_ANGLES))
    changed[-1] = (0, 1, 0, 2, 2, 1)
    expect_rejected(lambda: audit(templates=tuple(changed)), "template fixture")
    expect_rejected(lambda: best_switched_cost((0,) * 8 + (2,), ALL_ODD_ANGLES),
                    "nonbinary physical row")
    return 3


def main():
    records, cover_orbits, residual_orbits, gains, digest = audit()
    mutations = hostile_self_checks()
    print("kernel17 switched all-odd Gram audit: exact physical census passed")
    print(f"physical_parity_rows: {len(records)}")
    print(f"single_matrix_cover_residual: {EXPECTED_SINGLE_COVER}/{EXPECTED_SINGLE_RESIDUAL}")
    print(f"single_matrix_orbit_cover_residual: {len(cover_orbits)}/{len(residual_orbits)}")
    print("seven_template_exact_cover_gains: " + ",".join(map(str, gains)))
    print("seven_template_residual: 0")
    print(f"single_template_payload_sha256: {digest}")
    print(f"rejected_hostile_mutations: {mutations}")


if __name__ == "__main__":
    main()
