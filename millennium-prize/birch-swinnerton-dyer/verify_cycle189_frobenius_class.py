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


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


for q, (expected_order, expected_trace) in EXPECTED.items():
    order = point_count(q)
    trace = q + 1 - order
    require(order == expected_order and trace == expected_trace,
            f"wrong point count or trace at q={q}")
    require(legendre(q, 29) == 1, f"q={q} fails (q/29)=1")
    require(twist_root_number(q) == -1, f"q={q} has wrong twist sign")
    require(q % 7 == 1 and trace % 7 == 2 and valuation_7(order) == 1,
            f"q={q} fails the residual packet")
    require(projective_localization_row(q, order) == (1, 3),
            f"q={q} has wrong localization row")
    print(f"q={q} #E(F_q)={order} a_q={trace} class=unipotent(1),[1:3]")

print("PASS: all three primes have the same full L_0 conjugacy class")
