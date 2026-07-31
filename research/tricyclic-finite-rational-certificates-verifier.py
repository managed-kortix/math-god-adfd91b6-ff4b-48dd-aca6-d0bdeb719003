#!/usr/bin/env python3
"""Fail-closed audit of the finite certificates used for tricyclic kernels.

The audit uses only integer and Fraction arithmetic.  Trigonometric strict
inequalities are proved with rational Taylor enclosures and 333/106 < pi <
355/113.  Planar Gram matrices are PSD by their explicitly checked cosine-Gram
construction.  This file audits the finite tables and representative algebra;
it does not prove the analytic DNN duality, path monotonicity, induced-energy
superadditivity, or the structural reduction to these finite certificates.
"""

from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json


PI_LO = F(333, 106)
PI_HI = F(355, 113)
EXPECTED_SHA256 = "a34ed2d3898c1a244e861ce11ffb51d84d65eb4409066f0745829de5a8ca58b8"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def frac(text):
    if isinstance(text, int):
        return F(text)
    if isinstance(text, F):
        return text
    return F(text)


def ftext(value):
    value = frac(value)
    return f"{value.numerator}/{value.denominator}"


def alternating_sum(x, powers, last_power):
    total = F(0)
    factorial = 1
    for power in range(last_power + 1):
        if power:
            factorial *= power
        if power in powers:
            sign = -1 if ((power - min(powers)) // 2) % 2 else 1
            total += sign * x ** power / factorial
    return total


def tan_sq_upper_pi_multiple(numerator, denominator):
    """Rational upper bound for tan^2(numerator*pi/denominator)."""
    require(isinstance(numerator, int) and isinstance(denominator, int),
            "trigonometric angle is not integral")
    require(0 <= numerator * 2 < denominator, "angle is outside [0,pi/2)")
    if numerator == 0:
        return F(0)
    x = F(numerator, denominator) * PI_HI
    sin_upper = alternating_sum(x, {1, 3, 5, 7, 9, 11, 13}, 13)
    cos_lower = alternating_sum(x, {0, 2, 4, 6, 8, 10, 12, 14}, 14)
    require(0 < cos_lower and 0 < sin_upper, "Taylor enclosure lost positivity")
    return (sin_upper / cos_lower) ** 2


def prove_tan_bound(numerator, denominator, bound, label):
    upper = tan_sq_upper_pi_multiple(numerator, denominator)
    require(upper < frac(bound), f"{label}: rational tangent bound failed")


def determinant3(a, b, c):
    return 1 + 2 * a * b * c - a * a - b * b - c * c


def pair_data(kind, t):
    t = frac(t)
    r = (1 - 6 * t * t + t ** 4) / (1 + t * t) ** 2
    if kind == "EE":
        return r, 4 * t * t
    if kind == "EO":
        require(t != 0, "EO rational parameter is singular")
        return r, ((1 - t * t) / (2 * t)) ** 2 + 2 * t * t
    if kind == "OO":
        require(1 - 3 * t * t != 0, "OO rational parameter is singular")
        q = (3 * t - t ** 3) / (1 - 3 * t * t)
        return -(1 - q * q) / (1 + q * q), q * q + 3 * t * t
    raise RuntimeError(f"unknown doubled-side type: {kind}")


def connector_data(parity, t):
    t = frac(t)
    if parity == "E":
        return (1 - 6 * t * t + t ** 4) / (1 + t * t) ** 2, 2 * t * t
    if parity == "O":
        return (t * t - 1) / (t * t + 1), t * t
    raise RuntimeError(f"unknown connector parity: {parity}")


DT_ROWS = [
    ["EE,EE", "E", ["0", "0", "0"], ["1", "1", "1"], "0", "0"],
    ["EE,EE", "O", ["1/3", "1/3", "1/2"], ["7/25", "7/25", "-3/5"], "41/36", "1216/3125"],
    ["EE,EO", "E", ["0", "1/2", "1/2"], ["1", "-7/25", "-7/25"], "25/16", "0"],
    ["EE,EO", "O", ["1/4", "1/2", "1/3"], ["161/289", "-7/25", "-4/5"], "205/144", "11527191/52200625"],
    ["EE,OO", "E", ["1/4", "1/4", "1/3"], ["161/289", "-495/4913", "7/25"], "2246/1521", "8593933244/15085980625"],
    ["EE,OO", "O", None, ["1", "-1", "-1"], "0", "0"],
    ["EO,EO", "E", None, ["-1/2", "-1/2", "1"], "2", "0"],
    ["EO,EO", "O", None, None, None, None],
    ["EO,OO", "E", ["1/2", "1/5", "1/5"], ["-7/25", "-828/2197", "119/169"], "83009/48400", "1304316959/3016755625"],
    ["EO,OO", "O", ["1/2", "1/5", "1/2"], ["-7/25", "-828/2197", "-3/5"], "91237/48400", "883705599/3016755625"],
    ["OO,OO", "E", None, ["-1", "-1", "1"], "0", "0"],
    ["OO,OO", "O", ["1/5", "1/5", "1/2"], ["-828/2197", "-828/2197", "-3/5"], "16881/12100", "22382224/120670225"],
]

DT_ORBIT_COUNTS = {"EE,EE": 1, "EE,EO": 4, "EE,OO": 2,
                   "EO,EO": 4, "EO,OO": 4, "OO,OO": 1}

DT_CLASS111_LONG_CERTIFICATES = [
    ["parallel-even-long", [[4, 1, 12, "3/40"], [1, 1, 6, "1/3"],
                            [2, 7, 48, "1/4"], [1, 5, 24, "3/5"],
                            [1, 1, 8, "7/40"]], "229/120"],
    ["parallel-odd-long", [[2, 1, 12, "3/40"], [3, 1, 9, "2/15"],
                           [3, 1, 6, "1/3"]], "31/20"],
]


def audit_doubled_triangle(rows, long_certificates):
    require(len(rows) == 12, "doubled triangle: orbit count changed")
    require(len({(row[0], row[1]) for row in rows}) == 12,
            "doubled triangle: duplicate orbit")
    require(sum(DT_ORBIT_COUNTS[row[0]] for row in rows) == 32,
            "doubled triangle: labelled row count is not 32")
    structural = 0
    for index, row in enumerate(rows):
        kinds, parity, parameters, correlations, excess, determinant = row
        label = f"doubled triangle row {index + 1} ({kinds},{parity})"
        if correlations is None:
            require(kinds == "EO,EO" and parity == "O" and
                    parameters is None and excess is None and determinant is None,
                    f"{label}: malformed structural row")
            structural += 1
            continue
        expected_r = tuple(map(frac, correlations))
        if parameters is not None:
            first, second = kinds.split(",")
            r1, e1 = pair_data(first, parameters[0])
            r2, e2 = pair_data(second, parameters[1])
            rc, ec = connector_data(parity, parameters[2])
            require((r1, r2, rc) == expected_r, f"{label}: correlation fraction changed")
            require(e1 + e2 + ec == frac(excess), f"{label}: excess fraction changed")
        else:
            require((kinds, parity, excess) in {
                ("EE,OO", "O", "0"), ("EO,EO", "E", "2"),
                ("OO,OO", "E", "0")}, f"{label}: unknown boundary row")
        r1, r2, rc = expected_r
        require(all(-1 <= value <= 1 for value in expected_r),
                f"{label}: correlation outside [-1,1]")
        actual_det = determinant3(r1, r2, rc)
        require(actual_det == frac(determinant), f"{label}: determinant fraction changed")
        require(actual_det >= 0, f"{label}: Gram determinant is negative")
        require(frac(excess) <= 2, f"{label}: DNN excess exceeds two")
    require(structural == 1, "doubled triangle: structural orbit count changed")
    require(len(long_certificates) == 2,
            "doubled triangle: class-111 long-certificate count changed")
    for label, terms, displayed_sum in long_certificates:
        rational_sum = F(0)
        for coefficient, numerator, denominator, bound in terms:
            require(isinstance(coefficient, int) and coefficient > 0,
                    f"doubled triangle {label}: invalid coefficient")
            exact_tan = exact_simple_tan_sq(numerator, denominator)
            if exact_tan is not None and exact_tan == frac(bound):
                pass
            else:
                prove_tan_bound(numerator, denominator, bound,
                                f"doubled triangle {label} tan^2({numerator}pi/{denominator})")
            rational_sum += coefficient * frac(bound)
        require(rational_sum == frac(displayed_sum),
                f"doubled triangle {label}: rational sum changed")
        require(rational_sum < 2,
                f"doubled triangle {label}: DNN threshold failed")
    dnn_rows = sum(DT_ORBIT_COUNTS[row[0]] for row in rows if row[3] is not None)
    structural_rows = sum(DT_ORBIT_COUNTS[row[0]] for row in rows if row[3] is None)
    require((dnn_rows, structural_rows) == (28, 4),
            "doubled triangle: labelled disposition changed")
    return 11, 1, dnn_rows, structural_rows, len(long_certificates)


C4_CERTIFICATES = [
    [["000000"], [0, 0, 0], "0", None],
    [["001001"], [0, 6, 6], "0", None],
    [["000001"], [11, 8, 7], "3/5", None],
    [["001000"], [1, 8, 9], "3/5", None],
    [["000010", "000100"], [1, 3, 11], "5/4", None],
    [["010000", "100000"], [8, 9, 10], "5/4", None],
    [["000011", "000101"], [1, 2, 6], "9/8", None],
    [["001010", "001100"], [11, 5, 1], "9/8", None],
    [["010001", "100001"], [8, 7, 6], "9/8", None],
    [["011000", "101000"], [8, 2, 1], "9/8", None],
    [["001011", "001101"], [2, 9, 5], "3/2", None],
    [["011001", "101001"], [4, 9, 7], "3/2", None],
    [["010010", "010100", "100010", "100100"], [8, 8, 0], "2", ["2/3", "1/3", "0", "2/3", "1/3", "0"]],
    [["011011", "011101", "101011", "101101"], [4, 10, 6], "2", None],
]

C4_CLASS_COUNTS = {"000": 2, "001": 2, "010": 4, "011": 4,
                   "100": 4, "101": 4, "110": 8, "111": 8}
C4_CLASS_FIRST = {"000": "000000", "001": "000001", "010": "000010",
                  "011": "000011", "100": "010000", "101": "010001",
                  "110": "010010", "111": "010011"}
C4_FAILED = {"010011", "010101", "011010", "011100",
             "100011", "100101", "101010", "101100"}
C4_ENDPOINTS = ((0, 1), (0, 1), (1, 2), (2, 3), (2, 3), (3, 0))


def principal_cos_index(index, period):
    index %= 2 * period
    return min(index, 2 * period - index)


def c4_path_angle_index(bit, ku, kv):
    index = ku - kv
    if bit:
        index += 6
    return principal_cos_index(index, 6)


def exact_simple_tan_sq(numerator, denominator):
    value = F(numerator, denominator)
    if value == 0:
        return F(0)
    if value == F(1, 6):
        return F(1, 3)
    if value == F(1, 4):
        return F(1)
    return None


def c4_contributions(row, k):
    ks = (0, *k)
    values = []
    exact = []
    for bit_text, (u, v) in zip(row, C4_ENDPOINTS):
        bit = int(bit_text)
        length = 1 if bit else 2
        q = c4_path_angle_index(bit, ks[u], ks[v])
        numerator, denominator = q, 12 * length
        values.append(length * tan_sq_upper_pi_multiple(numerator, denominator))
        exact_tan = exact_simple_tan_sq(numerator, denominator)
        exact.append(None if exact_tan is None else length * exact_tan)
    return values, exact


def audit_doubled_c4(certificates):
    require(sum(C4_CLASS_COUNTS.values()) == 36 and
            set(C4_CLASS_COUNTS) == set(C4_CLASS_FIRST),
            "doubled C4: switching census ledger changed")
    simple_rows = {
        f"{bits:06b}" for bits in range(64)
        if not (((bits >> 5) & 1) and ((bits >> 4) & 1))
        and not (((bits >> 2) & 1) and ((bits >> 1) & 1))
    }
    require(len(simple_rows) == 36, "doubled C4: simple canonical row total changed")

    covered = set()
    for rows, k, threshold_text, exact_display in certificates:
        require(len(k) == 3 and all(isinstance(value, int) for value in k),
                "doubled C4: malformed planar Gram angles")
        threshold = frac(threshold_text)
        for row in rows:
            require(len(row) == 6 and set(row) <= {"0", "1"},
                    "doubled C4: malformed parity row")
            require(row not in covered, f"doubled C4: duplicate certificate for {row}")
            require(row not in C4_FAILED, f"doubled C4: failed row was marked DNN")
            upper, exact = c4_contributions(row, k)
            if threshold == 0:
                require(sum(upper) == 0, f"doubled C4: zero bound failed for {row}")
            elif threshold < 2:
                require(sum(upper) < threshold, f"doubled C4: strict bound failed for {row}")
            else:
                require(all(value is not None for value in exact),
                        f"doubled C4: boundary row {row} lacks exact elementary angles")
                require(sum(exact) == 2, f"doubled C4: boundary sum failed for {row}")
                if exact_display is not None:
                    require(sorted(exact) == sorted(map(frac, exact_display)),
                            f"doubled C4: displayed boundary contributions changed for {row}")
            covered.add(row)
    require(covered.isdisjoint(C4_FAILED), "doubled C4: DNN/structural overlap")
    require(covered | C4_FAILED == simple_rows,
            "doubled C4: 36-row DNN/structural partition changed")

    rational_bounds = ((3, 32, "93/1000"), (1, 8, "172/1000"),
                       (1, 16, "40/1000"), (3, 16, "447/1000"))
    for n, d, bound in rational_bounds:
        prove_tan_bound(n, d, bound, f"doubled C4 tan^2({n}pi/{d})")
    require(4 * frac("93/1000") + 3 * frac("172/1000") +
            2 * frac("40/1000") + 2 * frac("447/1000") == frac("1862/1000"),
            "doubled C4: first long-row rational sum changed")
    require(2 * frac("40/1000") + 4 * frac("172/1000") +
            2 * frac("447/1000") == frac("1662/1000"),
            "doubled C4: second long-row rational sum changed")
    require(frac("1862/1000") < 2 and frac("1662/1000") < 2,
            "doubled C4: long-row threshold failed")
    return len(covered), len(C4_FAILED)


K4_TAN_BOUNDS = [
    [5, 48, "7/60"], [1, 8, "7/40"], [3, 16, "9/20"],
]


K4_EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))

K4_ALL_ODD_DISPOSITIONS = {
    "q_ge_3_dnn": 42,
    "q_2_adjacent_dnn": 12,
    "q_2_opposite_dnn": 3,
    "q_1_structural": 6,
    "q_0_packet": 1,
}

# Angles are multiples of pi/3.  Each physical row records the exact number of
# even-path a=2*tan^2(pi/12) terms and odd-path b=tan^2(pi/6) terms.
K4_PHYSICAL_CERTIFICATES = [
    ["001", [2, 4, 4, 0], [
        ["111011", 0, 5], ["101110", 2, 3], ["011101", 2, 3],
        ["001000", 4, 1], ["000011", 3, 2], ["010110", 3, 2],
        ["100101", 3, 2], ["110000", 3, 2],
    ]],
    ["010", [4, 2, 4, 0], [
        ["101111", 0, 5], ["111010", 2, 3], ["001001", 3, 2],
        ["011100", 3, 2], ["010111", 2, 3], ["000010", 4, 1],
        ["110001", 3, 2], ["100100", 3, 2],
    ]],
    ["100", [4, 4, 2, 0], [
        ["011111", 0, 5], ["001010", 3, 2], ["111001", 2, 3],
        ["101100", 3, 2], ["100111", 2, 3], ["110010", 3, 2],
        ["000001", 4, 1], ["010100", 3, 2],
    ]],
    ["011", [2, 4, 3, 0], [
        ["101011", 2, 3], ["111110", 0, 5], ["001101", 3, 2],
        ["011000", 3, 2], ["010011", 3, 2], ["000110", 3, 2],
        ["110101", 2, 3], ["100000", 4, 1],
    ]],
    ["101", [2, 3, 4, 0], [
        ["011011", 2, 3], ["001110", 3, 2], ["111101", 0, 5],
        ["101000", 3, 2], ["100011", 3, 2], ["110110", 2, 3],
        ["000101", 3, 2], ["010000", 4, 1],
    ]],
    ["110", [3, 2, 4, 0], [
        ["001111", 2, 3], ["011010", 3, 2], ["101001", 3, 2],
        ["111100", 2, 3], ["110111", 0, 5], ["100010", 3, 2],
        ["010001", 3, 2], ["000100", 4, 1],
    ]],
    ["111", [3, 3, 3, 0], [
        ["001011", 0, 0], ["011110", 0, 0], ["101101", 0, 0],
        ["111000", 0, 0], ["110011", 0, 0], ["100110", 0, 0],
        ["010101", 0, 0], ["000000", 0, 0],
    ]],
]


def k4_normalize(parities):
    switches = tuple(1 - parities[index] for index in (2, 4, 5)) + (0,)
    normalized = tuple(bit ^ switches[u] ^ switches[v]
                       for bit, (u, v) in zip(parities, K4_EDGES))
    require(normalized[2] == normalized[4] == normalized[5] == 1,
            "K4 physical: normalization failed")
    epsilon = tuple(1 - normalized[index] for index in (0, 1, 3))
    return switches, normalized, epsilon


def audit_k4_physical(certificates):
    require(len(certificates) == 7, "K4 physical: switching-class count changed")
    require([entry[0] for entry in certificates] ==
            ["001", "010", "100", "011", "101", "110", "111"],
            "K4 physical: epsilon-class ledger changed")
    covered = set()
    class_cost_censuses = []
    for epsilon_text, angles, rows in certificates:
        require(len(epsilon_text) == 3 and set(epsilon_text) <= {"0", "1"} and
                epsilon_text != "000", "K4 physical: malformed epsilon word")
        epsilon = tuple(map(int, epsilon_text))
        require(len(angles) == 4 and angles[3] == 0 and
                all(isinstance(value, int) for value in angles),
                f"K4 physical {epsilon_text}: malformed planar angles")
        require(len(rows) == 8, f"K4 physical {epsilon_text}: switch count changed")
        class_counts = []
        seen_switches = set()
        for row_text, displayed_a, displayed_b in rows:
            label = f"K4 physical {epsilon_text}/{row_text}"
            require(len(row_text) == 6 and set(row_text) <= {"0", "1"},
                    f"{label}: malformed parity row")
            require(row_text not in covered, f"{label}: duplicate physical row")
            parities = tuple(map(int, row_text))
            switches, normalized, actual_epsilon = k4_normalize(parities)
            require(actual_epsilon == epsilon, f"{label}: wrong switching class")
            require(switches[:3] not in seen_switches,
                    f"{label}: duplicate physical switch triple")
            seen_switches.add(switches[:3])

            count_a = 0
            count_b = 0
            for bit, normalized_bit, (u, v) in zip(parities, normalized, K4_EDGES):
                physical_u = angles[u] + 3 * switches[u]
                physical_v = angles[v] + 3 * switches[v]
                transformed = principal_cos_index(physical_u - physical_v + 3 * bit, 3)
                normalized_angle = principal_cos_index(
                    angles[u] - angles[v] + 3 * normalized_bit, 3)
                require(transformed == normalized_angle,
                        f"{label}: sign-switch transport failed")
                require(transformed in (0, 1),
                        f"{label}: transformed angle is not zero or pi/3")
                if transformed == 1:
                    if bit:
                        count_b += 1
                    else:
                        count_a += 1
            require((count_a, count_b) == (displayed_a, displayed_b),
                    f"{label}: displayed physical cost changed")
            require(count_a + count_b <= 5, f"{label}: more than six path costs")
            class_counts.append((count_a, count_b))
            covered.add(row_text)
        require(seen_switches == set(product((0, 1), repeat=3)),
                f"K4 physical {epsilon_text}: switch triples are incomplete")
        class_cost_censuses.append(sorted(class_counts))

    all_rows = {f"{mask:06b}" for mask in range(64)}
    all_odd_class = set()
    for row_text in all_rows:
        _, _, epsilon = k4_normalize(tuple(map(int, row_text)))
        if epsilon == (0, 0, 0):
            all_odd_class.add(row_text)
    require(len(covered) == 56 and len(all_odd_class) == 8,
            "K4 physical: 56+8 census changed")
    require(covered.isdisjoint(all_odd_class) and covered | all_odd_class == all_rows,
            "K4 physical: non-all-odd partition changed")

    expected_census = sorted([(0, 5)] + 2 * [(2, 3)] +
                             4 * [(3, 2)] + [(4, 1)])
    require(all(census == expected_census for census in class_cost_censuses[:6]),
            "K4 physical: weight-one/two cost census changed")
    require(class_cost_censuses[6] == 8 * [(0, 0)],
            "K4 physical: weight-three zero-cost census changed")

    # a=14-8*sqrt(3)<1/6 follows from sqrt(3)>83/48.
    require(3 * 48 ** 2 > 83 ** 2 and 14 - 8 * F(83, 48) == F(1, 6),
            "K4 physical: radical bound failed")
    b = F(1, 3)
    require(5 * b == F(5, 3) and
            2 * F(1, 6) + 3 * b < F(5, 3) and
            3 * F(1, 6) + 2 * b < F(5, 3) and
            4 * F(1, 6) + b < F(5, 3) and F(5, 3) < 2,
            "K4 physical: exact excess threshold failed")
    return len(covered), len(all_odd_class)


def audit_k4_all_odd(bounds, expected_dispositions):
    require(bounds == K4_TAN_BOUNDS, "K4: rational tangent ledger changed")
    for n, d, bound in bounds:
        prove_tan_bound(n, d, bound, f"K4 tan^2({n}pi/{d})")
    adjacent = 6 * frac(bounds[0][2]) + frac(bounds[1][2]) + 2 * frac(bounds[2][2])
    require(adjacent == frac("71/40") and adjacent < 2,
            "K4: adjacent-long certificate sum failed")
    prove_tan_bound(1, 8, "1/4", "K4 opposite-long tangent bound")
    require(8 * frac("1/4") == 2, "K4: opposite-long threshold changed")

    # If x=tan(acos(1/3)/6), tan(3 atan x)=1/sqrt(2).
    # At x^2=1/18 the squared triple-angle value is already >1/2.
    y = F(1, 18)
    triple_square = y * (3 - y) ** 2 / (1 - 3 * y) ** 2
    require(triple_square > F(1, 2), "K4: simplex triple-angle certificate failed")
    require(3 * y == F(1, 6), "K4: simplex long-path threshold changed")

    require(set(expected_dispositions) == set(K4_ALL_ODD_DISPOSITIONS),
            "K4: all-odd disposition labels changed")
    dispositions = {key: 0 for key in K4_ALL_ODD_DISPOSITIONS}
    seen = set()
    for mask in range(64):
        long_edges = {index for index in range(6) if mask & (1 << index)}
        q = len(long_edges)
        if q >= 3:
            disposition = "q_ge_3_dnn"
        elif q == 2:
            first, second = sorted(long_edges)
            disposition = ("q_2_opposite_dnn"
                           if set(K4_EDGES[first]).isdisjoint(K4_EDGES[second])
                           else "q_2_adjacent_dnn")
        elif q == 1:
            disposition = "q_1_structural"
        else:
            disposition = "q_0_packet"
        require(mask not in seen, "K4: duplicate long/unit subset")
        seen.add(mask)
        dispositions[disposition] += 1
    require(seen == set(range(64)), "K4: long/unit subset enumeration incomplete")
    require(dispositions == expected_dispositions,
            "K4: all-odd disposition census changed")
    audited = (dispositions["q_ge_3_dnn"] +
               dispositions["q_2_adjacent_dnn"] +
               dispositions["q_2_opposite_dnn"])
    structural = dispositions["q_1_structural"] + dispositions["q_0_packet"]
    require((audited, structural) == (57, 7),
            "K4: audited/structural subset split changed")
    return dispositions, audited, structural


FOUR_PATH_RECORDS = [
    ["no_unit", 0, "right_endpoint", "0"],
    ["no_unit", 1, "right_endpoint_left_derivative_positive", "2"],
    ["no_unit", 2, "left_endpoint_right_derivative_negative", "2"],
    ["no_unit", 3, "left_endpoint", "1"],
    ["no_unit", 4, "left_endpoint", "0"],
    ["one_unit", 0, "right_endpoint", "0"],
    ["one_unit", 1, "pi_over_3_test", "5/3"],
    ["one_unit", 2, "pi_over_3_strict_scaffold", "2"],
    ["one_unit", 3, "symbolic_minimizer", "2"],
]


def audit_four_path(records):
    require(len(records) == 9, "four-path: representative count changed")
    seen = set()
    for family, e, method, displayed in records:
        require(family in {"no_unit", "one_unit"} and isinstance(e, int),
                "four-path: malformed representative")
        require((family, e) not in seen, "four-path: duplicate representative")
        seen.add((family, e))
        value = frac(displayed)
        if family == "no_unit":
            require(0 <= e <= 4, "four-path: invalid no-unit parity count")
            expected = {
                0: ("right_endpoint", F(0)),
                1: ("right_endpoint_left_derivative_positive", F(2)),
                2: ("left_endpoint_right_derivative_negative", F(2)),
                3: ("left_endpoint", F(1)),
                4: ("left_endpoint", F(0)),
            }[e]
            require((method, value) == expected,
                    f"four-path: no-unit e={e} representative changed")
            if e == 1:
                # At the right endpoint only the even term has a nonzero
                # one-sided derivative, and its coefficient is positive.
                derivative_sign = 1
                require(derivative_sign > 0,
                        "four-path: no-unit e=1 derivative sign changed")
            elif e == 2:
                # At the left endpoint only the odd terms have a nonzero
                # one-sided derivative; their arguments decrease with x.
                derivative_sign = -1
                require(derivative_sign < 0,
                        "four-path: no-unit e=2 derivative sign changed")
        else:
            require(0 <= e <= 3, "four-path: invalid one-unit parity count")
            if e == 0:
                require((method, value) == ("right_endpoint", F(0)),
                        "four-path: one-unit e=0 endpoint changed")
            elif e == 1:
                scaffold = F(1, 3) + F(2, 3) + 2 * F(1, 3)
                require(method == "pi_over_3_test" and value == scaffold and value < 2,
                        "four-path: one-unit e=1 representative failed")
                prove_tan_bound(1, 18, "1/9", "four-path e=1 tan^2(pi/18)")
                require(6 * tan_sq_upper_pi_multiple(1, 18) < F(2, 3),
                        "four-path: one-unit e=1 strict odd terms failed")
            elif e == 2:
                scaffold = F(1, 3) + 2 * F(2, 3) + F(1, 3)
                require(method == "pi_over_3_strict_scaffold" and value == scaffold == 2,
                        "four-path: one-unit e=2 scaffold changed")
                prove_tan_bound(1, 18, "1/9", "four-path tan^2(pi/18)")
                require(3 * tan_sq_upper_pi_multiple(1, 18) < F(1, 3),
                        "four-path: one-unit e=2 strict term failed")
            else:
                u2 = F(1, 5)
                symbolic_value = 1 / (4 * u2) - F(1, 2) + 25 * u2 / 4
                require(method == "symbolic_minimizer" and value == symbolic_value == 2 and
                        (5 * u2 - 1) ** 2 == 0,
                        "four-path: exceptional symbolic minimizer failed")
    expected_cases = ({("no_unit", e) for e in range(5)} |
                      {("one_unit", e) for e in range(4)})
    require(seen == expected_cases, "four-path: representative cases incomplete")
    return len(seen)


def canonical_payload(certificate):
    return json.dumps(certificate, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True) + "\n"


def certificate_data():
    return {
        "doubled_triangle": deepcopy(DT_ROWS),
        "doubled_triangle_class111_long": deepcopy(DT_CLASS111_LONG_CERTIFICATES),
        "doubled_c4": deepcopy(C4_CERTIFICATES),
        "k4_physical_certificates": deepcopy(K4_PHYSICAL_CERTIFICATES),
        "k4_tangent_bounds": deepcopy(K4_TAN_BOUNDS),
        "k4_all_odd_dispositions": deepcopy(K4_ALL_ODD_DISPOSITIONS),
        "four_path_representative_records": deepcopy(FOUR_PATH_RECORDS),
    }


def audit(certificate, enforce_digest=True):
    require(isinstance(certificate, dict), "certificate root is not a dictionary")
    require(set(certificate) == {"doubled_triangle", "doubled_triangle_class111_long",
                                 "doubled_c4",
                                 "k4_physical_certificates", "k4_tangent_bounds",
                                 "k4_all_odd_dispositions",
                                 "four_path_representative_records"},
            "certificate sections changed")
    dt_counts = audit_doubled_triangle(
        certificate["doubled_triangle"], certificate["doubled_triangle_class111_long"])
    c4_rows, c4_failed = audit_doubled_c4(certificate["doubled_c4"])
    k4_physical, k4_omitted = audit_k4_physical(certificate["k4_physical_certificates"])
    k4_dispositions, k4_audited, k4_structural = audit_k4_all_odd(
        certificate["k4_tangent_bounds"], certificate["k4_all_odd_dispositions"])
    four_path_cases = audit_four_path(certificate["four_path_representative_records"])
    digest = sha256(canonical_payload(certificate).encode("ascii")).hexdigest()
    if enforce_digest:
        require(digest == EXPECTED_SHA256, "finite certificate digest changed")
    return digest, (dt_counts, c4_rows, c4_failed, k4_physical, k4_omitted,
                    k4_dispositions, k4_audited, k4_structural, four_path_cases)


def expect_rejected(action, label):
    try:
        action()
    except (RuntimeError, ZeroDivisionError, ValueError, TypeError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    mutations = []

    def add(label, mutator):
        candidate = certificate_data()
        mutator(candidate)
        mutations.append((label, candidate))

    add("triangle determinant", lambda c: c["doubled_triangle"][1].__setitem__(5, "1217/3125"))
    add("triangle excess", lambda c: c["doubled_triangle"][4].__setitem__(4, "2247/1521"))
    add("triangle missing orbit", lambda c: c["doubled_triangle"].pop())
    add("triangle class-111 tangent bound", lambda c: c["doubled_triangle_class111_long"][0][1][2].__setitem__(3, "1/5"))
    add("C4 Gram angle", lambda c: c["doubled_c4"][2].__setitem__(1, [0, 0, 0]))
    add("C4 missing row", lambda c: c["doubled_c4"][12][0].pop())
    add("C4 threshold", lambda c: c["doubled_c4"][0].__setitem__(2, "-1/100"))
    add("K4 physical parity", lambda c: c["k4_physical_certificates"][0][2][0].__setitem__(0, "011011"))
    add("K4 physical angle", lambda c: c["k4_physical_certificates"][3][1].__setitem__(0, 0))
    add("K4 physical cost", lambda c: c["k4_physical_certificates"][5][2][0].__setitem__(1, 3))
    add("K4 tangent bound", lambda c: c["k4_tangent_bounds"][0].__setitem__(2, "1/10"))
    add("K4 all-odd disposition", lambda c: c["k4_all_odd_dispositions"].__setitem__("q_1_structural", 5))
    add("four-path e=0 logic", lambda c: c["four_path_representative_records"][5].__setitem__(3, "1"))
    for label, candidate in mutations:
        expect_rejected(lambda candidate=candidate: audit(candidate, enforce_digest=False), label)
    return len(mutations)


def main():
    digest, counts = audit(certificate_data())
    mutations = hostile_self_checks()
    require(mutations == 13, "hostile mutation count changed")
    (dt_counts, c4_rows, c4_failed, k4_physical, k4_omitted,
     k4_dispositions, k4_audited, k4_structural, four_cases) = counts
    dt_dnn_orbits, dt_structural_orbits, dt_dnn_rows, dt_structural_rows, dt_long = dt_counts
    print("tricyclic finite rational certificates: exact audit passed")
    print(f"doubled_triangle: {dt_dnn_orbits} DNN orbit records ({dt_dnn_rows} labelled rows), "
          f"{dt_structural_orbits} structural orbit ({dt_structural_rows} labelled rows), "
          f"{dt_long} audited class-111 long-path DNN records")
    print(f"doubled_c4: {c4_rows} DNN rows, {c4_failed} structural class-111 rows")
    print(f"k4_non_all_odd: {k4_physical} exact physical rows, {k4_omitted} all-odd rows omitted")
    print(f"k4_all_odd: 64/64 long/unit subsets enumerated; {k4_audited} DNN-audited, "
          f"{k4_structural} structural ({k4_dispositions})")
    print(f"four_path: {four_cases} representative symbolic records (not analytic coverage)")
    print(f"certificate_sha256: {digest}")
    print(f"rejected_hostile_mutations: {mutations}")
    print("scope: finite certificate audit only; analytic and structural dependencies are not reproved")


if __name__ == "__main__":
    main()
