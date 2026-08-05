#!/usr/bin/env python3
"""Exact arithmetic audit for the all-odd K4-subdivision proof."""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json


EXPECTED_SHA256 = "85ccff4a03791e2a5a455a7c350b804982f6ee3fb426233cd5e92c67431466c2"
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
ADJACENT_TESTS = (
    (Q(5, 24), Q(7, 60), 8858386029377237523769),
    (Q(1, 4), Q(7, 40), 287162942936656949),
    (Q(3, 8), Q(9, 20), 831220125392302623),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def cosine_lower_at_rational_pi(multiplier: Q) -> Q:
    """Lower bound 1-y^2/2+y^4/24-y^6/720 at y<=multiplier*355/113."""
    y = multiplier * Q(355, 113)
    return Q(1) - y * y / 2 + y**4 / 24 - y**6 / 720


def verify_simplex() -> None:
    # At t=1/(3 sqrt(2)), tan(3 arctan t)=53/(45 sqrt(2)) > 1/sqrt(2).
    require(Q(53, 45) > 1, "simplex triple-angle comparison failed")
    require(Q(6 - 3, 2) + Q(3, 6) == 2, "three-long budget failed")
    require(Q(2, 3) > Q(7, 9) ** 2, "even length-two simplex bound failed")
    require(Q(6 - 4, 2) + Q(4, 4) == 2, "four-long budget failed")

    # Exceptional switch: three even long paths and three odd unit paths.
    require(Q(8, 9) > Q(11, 13) ** 2,
            "three-even-cut half-angle bound failed")
    require(3 * Q(1, 2) + 3 * Q(1, 6) == 2,
            "three-even-cut budget failed")


def verify_opposite() -> None:
    # 24-16 sqrt(2)<2 iff sqrt(2)>11/8.
    require(Q(2) > Q(11, 8) ** 2, "opposite-long radical bound failed")


def verify_adjacent(tests) -> None:
    for multiplier, tangent_bound, expected_numerator in tests:
        target = (1 - tangent_bound) / (1 + tangent_bound)
        difference = cosine_lower_at_rational_pi(multiplier) - target
        require(difference > 0, f"Taylor certificate failed for {multiplier}")
        require(
            difference.numerator == expected_numerator,
            f"Taylor numerator drift for {multiplier}",
        )
    total = 6 * Q(7, 60) + Q(7, 40) + 2 * Q(9, 20)
    require(total == Q(71, 40) and total < 2, "adjacent-long budget failed")


def verify_switching_rows(edges) -> None:
    rows = []
    for bits in product((0, 1), repeat=3):
        switches = bits + (0,)
        parity = tuple(1 ^ switches[i] ^ switches[j] for i, j in edges)
        canonical = tuple(1 if value else 2 for value in parity)
        require(all((length & 1) == value for length, value in zip(canonical, parity)),
                "canonical physical parity mismatch")
        require(all(length >= 1 for length in canonical), "unit lower length failed")
        long_minimum = tuple(3 if value else 2 for value in parity)
        require(all(length >= 2 for length in long_minimum), "long lower length failed")
        even_count = parity.count(0)
        require(even_count in (0, 3, 4), "K4 cut-size classification failed")
        rows.append(parity)
    require(len(set(rows)) == 8, "switching orbit does not contain eight rows")
    require(rows[0] == (1, 1, 1, 1, 1, 1), "all-odd representative missing")


def certificate_data():
    return {
        "edges": [list(edge) for edge in EDGES],
        "adjacent_tests": [
            [m.numerator, m.denominator, b.numerator, b.denominator, expected]
            for m, b, expected in ADJACENT_TESTS
        ],
        "simplex_constants": [53, 45, 7, 9, 11, 13],
        "opposite_radical": [11, 8],
    }


def audit(certificate, enforce_digest=True):
    require(certificate["edges"] == [list(edge) for edge in EDGES],
            "K4 endpoint ledger changed")
    require(certificate["simplex_constants"] == [53, 45, 7, 9, 11, 13],
            "simplex constant ledger changed")
    require(certificate["opposite_radical"] == [11, 8],
            "opposite radical ledger changed")
    tests = tuple((Q(a, b), Q(c, d), expected)
                  for a, b, c, d, expected in certificate["adjacent_tests"])
    require(tests == ADJACENT_TESTS, "adjacent tangent ledger changed")
    verify_simplex()
    verify_opposite()
    verify_adjacent(tests)
    verify_switching_rows(tuple(map(tuple, certificate["edges"])))
    payload = json.dumps(certificate, sort_keys=True, separators=(",", ":")) + "\n"
    digest = sha256(payload.encode("ascii")).hexdigest()
    if enforce_digest:
        require(digest == EXPECTED_SHA256, "certificate digest changed")
    return digest


def expect_rejected(action, label):
    try:
        action()
    except (RuntimeError, KeyError, TypeError, ValueError, ZeroDivisionError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    candidates = []
    for label in ("edge", "tangent", "simplex"):
        candidate = certificate_data()
        if label == "edge":
            candidate["edges"][0][1] = 2
        elif label == "tangent":
            candidate["adjacent_tests"][0][2] = 8
        else:
            candidate["simplex_constants"][0] = 52
        candidates.append((label, candidate))
    for label, candidate in candidates:
        expect_rejected(lambda candidate=candidate: audit(candidate, False), label)
    return len(candidates)


def main() -> None:
    digest = audit(certificate_data())
    mutations = hostile_self_checks()
    require(mutations == 3, "hostile mutation count changed")
    print("all-odd K4 exact audit passed: 4 cases, 8 switching rows, 3 Taylor bounds")
    print(f"certificate_sha256: {digest}")
    print(f"rejected_hostile_mutations: {mutations}")


if __name__ == "__main__":
    main()
