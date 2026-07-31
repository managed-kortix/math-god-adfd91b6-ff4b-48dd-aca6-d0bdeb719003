#!/usr/bin/env python3
"""Exact finite-field verifier that the Cycle 189 primes share class [1:3]."""

from verify_cycle187_small_frobenius_classes import (
    legendre,
    point_count,
    projective_localization_row,
    twist_root_number,
    valuation_7,
)


EXPECTED = {
    11831: (11970, -138),
    14897: (15106, -208),
    48889: (48678, 212),
}

for q, (expected_order, expected_trace) in EXPECTED.items():
    order = point_count(q)
    trace = q + 1 - order
    assert order == expected_order and trace == expected_trace
    assert legendre(q, 29) == 1
    assert twist_root_number(q) == -1
    assert q % 7 == 1 and trace % 7 == 2 and valuation_7(order) == 1
    assert projective_localization_row(q, order) == (1, 3)
    print(f"q={q} #E(F_q)={order} a_q={trace} class=unipotent(1),[1:3]")

print("PASS: all three primes have the same full L_0 conjugacy class")
