#!/usr/bin/env python3
"""Exact arithmetic audit for the all-odd K4-subdivision proof."""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from numbers import Number


EXPECTED_SHA256 = "b0c4ed64a12ccabe0a8a38cb9fdb85622d8f7c2d07bdf53f75eb1700a684fa39"
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
ADJACENT_TESTS = (
    (Q(5, 24), Q(7, 60), 8858386029377237523769),
    (Q(1, 4), Q(7, 40), 287162942936656949),
    (Q(3, 8), Q(9, 20), 831220125392302623),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def validate_payload_types(value, path="certificate") -> None:
    """Admit only exact JSON-like values; in particular reject bool and float."""
    if value is None or isinstance(value, str) or type(value) is int:
        return
    if isinstance(value, Number):
        raise RuntimeError(f"{path}: non-integral numeric value is forbidden")
    if type(value) is list:
        for index, item in enumerate(value):
            validate_payload_types(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        require(all(isinstance(key, str) for key in value),
                f"{path}: dictionary keys must be strings")
        for key, item in value.items():
            validate_payload_types(item, f"{path}.{key}")
        return
    raise RuntimeError(f"{path}: forbidden payload type {type(value).__name__}")


def cosine_lower_at_rational_pi(multiplier: Q) -> Q:
    """Lower bound 1-y^2/2+y^4/24-y^6/720 at y<=multiplier*355/113."""
    y = multiplier * Q(355, 113)
    return Q(1) - y * y / 2 + y**4 / 24 - y**6 / 720


def determinant(matrix) -> Q:
    """Exact determinant by fraction-preserving Gaussian elimination."""
    work = [[Q(entry) for entry in row] for row in matrix]
    value = Q(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column] != 0), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            value = -value
        diagonal = work[column][column]
        value *= diagonal
        for row in range(column + 1, len(work)):
            multiplier = work[row][column] / diagonal
            for entry in range(column + 1, len(work)):
                work[row][entry] -= multiplier * work[column][entry]
    return value


def verify_three_even_cut_gram(gram, displayed_total) -> None:
    expected = (
        (Q(1), Q(1, 6), Q(1, 6), Q(1, 6)),
        (Q(1, 6), Q(1), Q(-11, 24), Q(-11, 24)),
        (Q(1, 6), Q(-11, 24), Q(1), Q(-11, 24)),
        (Q(1, 6), Q(-11, 24), Q(-11, 24), Q(1)),
    )
    require(gram == expected, "three-even-cut Gram changed")
    expected_minors = {
        1: sorted([Q(1)] * 4),
        2: sorted([Q(35, 36)] * 3 + [Q(455, 576)] * 3),
        3: sorted([Q(1225, 1728)] * 3 + [Q(1225, 6912)]),
        4: [Q(0)],
    }
    for order in range(1, 5):
        minors = []
        for indices in combinations(range(4), order):
            principal = [[gram[row][column] for column in indices]
                         for row in indices]
            minors.append(determinant(principal))
        require(sorted(minors) == expected_minors[order],
                f"three-even-cut order-{order} principal minors changed")
        require(all(value >= 0 for value in minors),
                f"three-even-cut Gram is not PSD at order {order}")
    kernel = (Q(-1), Q(2), Q(2), Q(2))
    require(all(sum(gram[row][column] * kernel[column] for column in range(4)) == 0
                for row in range(4)), "three-even-cut Gram kernel changed")

    # Derive the displayed radical total from the Gram, rather than trusting a
    # second unbound ledger.  For an even path of length two and correlation r,
    # f_2(r)=2(1-s)/(1+s), where s^2=(1+r)/2.  Here s=sqrt(21)/6, so rationalizing
    # gives (38-8*sqrt(21))/5.  An odd unit of correlation t costs (1+t)/(1-t).
    cut = (gram[0][1], gram[0][2], gram[0][3])
    triangle = (gram[1][2], gram[1][3], gram[2][3])
    require(len(set(cut)) == len(set(triangle)) == 1,
            "three-even-cut correlations lost orbit symmetry")
    r, t = cut[0], triangle[0]
    square = (1 + r) / 2
    require(square == Q(21, 36), "three-even-cut half-angle square changed")
    radical, root_denominator = 21, 6
    denominator = root_denominator**2 - radical
    even_constant = 2 * Q(root_denominator**2 + radical, denominator)
    even_radical = -4 * Q(root_denominator, denominator)
    odd_cost = (1 + t) / (1 - t)
    require((even_constant, even_radical, odd_cost) ==
            (Q(38, 5), Q(-8, 5), Q(13, 35)),
            "three-even-cut path costs changed")
    total_constant = 3 * even_constant + 3 * odd_cost
    total_radical = 3 * even_radical
    common_denominator = total_constant.denominator
    radical_coefficient = -total_radical * common_denominator
    require(radical_coefficient.denominator == 1,
            "three-even-cut radical coefficient is not integral")
    derived_total = [total_constant.numerator, radical_coefficient.numerator,
                     radical, common_denominator]
    require(all(type(value) is int for value in derived_total) and
            derived_total == displayed_total == [837, 168, 21, 35],
            "three-even-cut radical total is not derived from the Gram")
    numerator, coefficient, radicand, total_denominator = derived_total
    gap = numerator - 2 * total_denominator
    require(coefficient > 0 and gap > 0 and
            coefficient**2 * radicand - gap**2 == 4415 > 0,
            "three-even-cut strict radical comparison failed")

    # Hostile regression gates: the former regular-simplex assertion was false.
    # Its length-two cost exceeds 1/6, and the condition it actually needed is
    # 2/3>(11/13)^2 rather than the unrelated true comparison 8/9>(11/13)^2.
    require(59**2 - 24**2 * 6 == 25 > 0,
            "former simplex countercheck changed")
    require(2 * 169 - 3 * 121 == -25 < 0,
            "former half-angle countercheck changed")


def verify_simplex(gram, displayed_total) -> None:
    # At t=1/(3 sqrt(2)), tan(3 arctan t)=53/(45 sqrt(2)) > 1/sqrt(2).
    require(Q(53, 45) > 1, "simplex triple-angle comparison failed")
    require(Q(6 - 3, 2) + Q(3, 6) == 2, "three-long budget failed")
    require(Q(2, 3) > Q(7, 9) ** 2, "even length-two simplex bound failed")
    require(Q(6 - 4, 2) + Q(4, 4) == 2, "four-long budget failed")
    verify_three_even_cut_gram(gram, displayed_total)


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
    cut_sizes = {0: 0, 3: 0, 4: 0}
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
        if even_count == 3:
            even_edges = [edges[index] for index, value in enumerate(parity) if value == 0]
            common = set(even_edges[0]).intersection(*map(set, even_edges[1:]))
            require(len(common) == 1,
                    "three-edge switching cut is not a relabelled star")
        cut_sizes[even_count] += 1
        rows.append(parity)
    require(len(set(rows)) == 8, "switching orbit does not contain eight rows")
    require(rows[0] == (1, 1, 1, 1, 1, 1), "all-odd representative missing")
    require(cut_sizes == {0: 1, 3: 4, 4: 3},
            "switching rows do not split as one constant, four three-cuts, three four-cuts")


def certificate_data():
    return {
        "edges": [list(edge) for edge in EDGES],
        "adjacent_tests": [
            [m.numerator, m.denominator, b.numerator, b.denominator, expected]
            for m, b, expected in ADJACENT_TESTS
        ],
        "simplex_constants": [53, 45, 7, 9],
        "three_even_cut_gram": [
            [[1, 1], [1, 6], [1, 6], [1, 6]],
            [[1, 6], [1, 1], [-11, 24], [-11, 24]],
            [[1, 6], [-11, 24], [1, 1], [-11, 24]],
            [[1, 6], [-11, 24], [-11, 24], [1, 1]],
        ],
        "three_even_cut_total": [837, 168, 21, 35],
        "opposite_radical": [11, 8],
    }


def audit(certificate, enforce_digest=True):
    require(isinstance(certificate, dict), "certificate root is not a dictionary")
    validate_payload_types(certificate)
    require(set(certificate) == {"edges", "adjacent_tests", "simplex_constants",
                                 "three_even_cut_gram", "three_even_cut_total",
                                 "opposite_radical"},
            "certificate sections changed")
    require(certificate["edges"] == [list(edge) for edge in EDGES],
            "K4 endpoint ledger changed")
    require(certificate["simplex_constants"] == [53, 45, 7, 9],
            "simplex constant ledger changed")
    require(certificate["three_even_cut_total"] == [837, 168, 21, 35],
            "three-even-cut total ledger changed")
    require(certificate["opposite_radical"] == [11, 8],
            "opposite radical ledger changed")
    tests = tuple((Q(a, b), Q(c, d), expected)
                  for a, b, c, d, expected in certificate["adjacent_tests"])
    require(tests == ADJACENT_TESTS, "adjacent tangent ledger changed")
    gram = tuple(tuple(Q(numerator, denominator) for numerator, denominator in row)
                 for row in certificate["three_even_cut_gram"])
    verify_simplex(gram, certificate["three_even_cut_total"])
    verify_opposite()
    verify_adjacent(tests)
    verify_switching_rows(tuple(map(tuple, certificate["edges"])))
    payload = json.dumps(certificate, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=True, allow_nan=False) + "\n"
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
    for label in ("edge", "tangent", "simplex", "three-even Gram", "three-even total",
                  "extra section", "boolean numerator", "tuple array"):
        candidate = certificate_data()
        if label == "edge":
            candidate["edges"][0][1] = 2
        elif label == "tangent":
            candidate["adjacent_tests"][0][2] = 8
        elif label == "simplex":
            candidate["simplex_constants"][0] = 52
        elif label == "three-even Gram":
            candidate["three_even_cut_gram"][0][1] = [1, 5]
        elif label == "three-even total":
            candidate["three_even_cut_total"][0] = 838
        elif label == "extra section":
            candidate["junk"] = 0
        elif label == "boolean numerator":
            candidate["three_even_cut_gram"][0][0][0] = True
        else:
            candidate["three_even_cut_gram"] = tuple(candidate["three_even_cut_gram"])
        candidates.append((label, candidate))
    for label, candidate in candidates:
        expect_rejected(lambda candidate=candidate: audit(candidate, False), label)
    return len(candidates)


def main() -> None:
    digest = audit(certificate_data())
    mutations = hostile_self_checks()
    require(mutations == 8, "hostile mutation count changed")
    print("all-odd K4 exact audit passed: 4 cases, 8 switching rows, 3 Taylor bounds")
    print(f"certificate_sha256: {digest}")
    print(f"rejected_hostile_mutations: {mutations}")


if __name__ == "__main__":
    main()
