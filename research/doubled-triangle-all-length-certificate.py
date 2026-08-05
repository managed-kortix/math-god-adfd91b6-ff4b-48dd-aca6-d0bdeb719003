#!/usr/bin/env python3
"""Fail-closed finite audit for the doubled-triangle all-length split.

This checks the physical census, the residue decision table, and rational
Taylor certificates for the two long-path Gram records. The analytic path
monotonicity and structural spectral lemmas remain proof dependencies.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json


PI_HI = F(355, 113)
EXPECTED_SHA256 = "b293eef0d7742da6ecd2c7af35882be14e97811922493121900e65a6705f01e8"
ORBIT_SIZES = (1, 4, 2, 4, 4, 1)
EXPECTED_RESIDUES = {
    (1, 1, "long-dnn"), (1, 3, "long-dnn"),
    (3, 1, "long-dnn"), (3, 3, "long-dnn"),
    (3, 3, "canonical-deletion"),
}
TANGENT_BOUNDS = {
    (1, 12): F(3, 40), (1, 6): F(1, 3), (7, 48): F(1, 4),
    (5, 24): F(3, 5), (1, 8): F(7, 40), (1, 9): F(2, 15),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def alternating_sum(x, powers, last_power):
    total = F(0)
    factorial = 1
    first = min(powers)
    for power in range(last_power + 1):
        if power:
            factorial *= power
        if power in powers:
            sign = -1 if ((power - first) // 2) % 2 else 1
            total += sign * x ** power / factorial
    return total


def tan_sq_upper(numerator, denominator):
    require(0 <= 2 * numerator < denominator, "angle outside [0,pi/2)")
    if numerator == 0:
        return F(0)
    x = F(numerator, denominator) * PI_HI
    sin_upper = alternating_sum(x, {1, 3, 5, 7, 9, 11, 13}, 13)
    cos_lower = alternating_sum(x, {0, 2, 4, 6, 8, 10, 12, 14}, 14)
    require(sin_upper > 0 and cos_lower > 0, "Taylor enclosure lost positivity")
    return (sin_upper / cos_lower) ** 2


def audit_tangent_bound(numerator, denominator, bound):
    require(tan_sq_upper(numerator, denominator) < bound,
            f"tan^2({numerator}pi/{denominator}) bound failed")


def audit_census(orbit_sizes):
    require(2 * sum(orbit_sizes) == 32, "physical census changed")
    dnn = 2 * sum(orbit_sizes) - 4
    require((dnn, 32 - dnn) == (28, 4), "DNN/structural split changed")


def pair_state(even_steps, odd_steps):
    """Pair lengths are (2+2e,1+2o); return residue and long status."""
    require(even_steps >= 0 and odd_steps >= 0, "negative length increment")
    residue = (3 + 2 * (even_steps + odd_steps)) % 4
    long = even_steps > 0 or odd_steps > 0
    if residue == 1:
        require(long, "residue one incorrectly admitted a canonical pair")
    return residue, long


def audit_residue_table(expected):
    seen = set()
    dispositions = set()
    # Parities of the increment counts determine all possible mod-4 states;
    # values 0,1,2 also distinguish canonical from long in residue three.
    for e1, o1, e2, o2 in product(range(3), repeat=4):
        x, long_x = pair_state(e1, o1)
        y, long_y = pair_state(e2, o2)
        seen.add((x, y))
        if long_x or long_y:
            disposition = "long-dnn"
        else:
            require((x, y) == (3, 3), "non-long row outside canonical residue")
            disposition = "canonical-deletion"
        dispositions.add((x, y, disposition))
    require(seen == {(1, 1), (1, 3), (3, 1), (3, 3)},
            "residue table is incomplete")
    require(dispositions == expected, "residue dispositions changed")


def audit_long_certificates(bounds):
    # pi/6 is exact; all other comparisons are strict Taylor enclosures.
    for angle, bound in bounds.items():
        if angle == (1, 6):
            continue
        audit_tangent_bound(*angle, bound)
    even_long = (4 * bounds[(1, 12)] + bounds[(1, 6)] +
                 2 * bounds[(7, 48)] + bounds[(5, 24)] +
                 bounds[(1, 8)])
    odd_long = (2 * bounds[(1, 12)] + 3 * bounds[(1, 9)] +
                3 * bounds[(1, 6)])
    require(even_long == F(229, 120) and even_long < 2,
            "even-long rational certificate changed")
    require(odd_long == F(31, 20) and odd_long < 2,
            "odd-long rational certificate changed")


def certificate_data():
    return {
        "pi_upper": f"{PI_HI.numerator}/{PI_HI.denominator}",
        "orbit_sizes": list(ORBIT_SIZES),
        "residue_dispositions": sorted([list(row) for row in EXPECTED_RESIDUES]),
        "tangent_bounds": sorted([
            [n, d, bound.numerator, bound.denominator]
            for (n, d), bound in TANGENT_BOUNDS.items()
        ]),
    }


def audit(certificate, enforce_digest=True):
    require(certificate["pi_upper"] == "355/113", "pi upper bound changed")
    orbit_sizes = tuple(certificate["orbit_sizes"])
    expected = {tuple(row) for row in certificate["residue_dispositions"]}
    bounds = {(n, d): F(p, q) for n, d, p, q in certificate["tangent_bounds"]}
    require(expected == EXPECTED_RESIDUES, "residue disposition ledger changed")
    require(bounds == TANGENT_BOUNDS, "tangent-bound ledger changed")
    audit_census(orbit_sizes)
    audit_residue_table(expected)
    audit_long_certificates(bounds)
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
    for label in ("orbit", "residue", "tangent"):
        candidate = certificate_data()
        if label == "orbit":
            candidate["orbit_sizes"][0] = 2
        elif label == "residue":
            candidate["residue_dispositions"].pop()
        else:
            candidate["tangent_bounds"][0][2] += 1
        candidates.append((label, candidate))
    for label, candidate in candidates:
        expect_rejected(lambda candidate=candidate: audit(candidate, False), label)
    return len(candidates)


def main():
    digest = audit(certificate_data())
    mutations = hostile_self_checks()
    require(mutations == 3, "hostile mutation count changed")
    print("doubled triangle all-length certificate: exact finite audit passed")
    print("physical rows: 32 = 28 monotone DNN + 4 class-111")
    print("class-111 residues: 4 long-DNN states + 1 canonical-deletion state")
    print("long-path bounds: 229/120 and 31/20, both below 2")
    print(f"certificate_sha256: {digest}")
    print(f"rejected_hostile_mutations: {mutations}")
    print("scope: finite split and tangent bounds only; analytic dependencies not reproved")


if __name__ == "__main__":
    main()
