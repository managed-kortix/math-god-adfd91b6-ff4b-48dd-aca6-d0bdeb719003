#!/usr/bin/env python3
"""Dependency-free replay of the Cycle 189 [0:1] rational certificates."""

import csv
from fractions import Fraction
from pathlib import Path


P = 7
ACTIVE_A = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14)
WEIGHTS = {
    2: 2, 3: 3, 4: 4, 5: 2, 6: 5, 7: 3,
    8: 6, 9: 6, 10: 4, 11: 1, 13: 1, 14: 5,
}
EXPECTED = {
    8191: (-8191, -1, Fraction(-1230), 2),
    10949: (10949, 1, Fraction(-125), 1),
    19559: (-19559, -1, Fraction(1381), 2),
    31963: (-31963, -1, Fraction(-391), 1),
    34679: (-34679, -1, Fraction(401), 2),
    39439: (-39439, -1, Fraction(-2530), 4),
    45053: (45053, 1, Fraction(-97), 1),
    66179: (-66179, -1, Fraction(-418), 2),
    77617: (77617, 1, Fraction(870), 2),
    99709: (99709, 1, Fraction(1261), 1),
    103811: (-103811, -1, Fraction(-3177, 2), 4),
    109789: (109789, 1, Fraction(-1354), 4),
    114311: (-114311, -1, Fraction(3311), 0),
}
FILES = (
    "cycle189_0_1_base433_symbol_sums.csv",
    "cycle189_0_1_base433_symbol_sums_continuation.csv",
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def reduce_mod_7(value: Fraction) -> int:
    denominator = value.denominator % P
    require(denominator != 0, f"non-7-integral rational: {value}")
    return value.numerator % P * pow(denominator, -1, P) % P


rows_by_q = {q: [] for q in EXPECTED}
base = Path(__file__).parent
for filename in FILES:
    with (base / filename).open(newline="", encoding="ascii") as source:
        for row in csv.DictReader(source):
            parsed = {key: int(value) for key, value in row.items()}
            q = parsed["q"]
            require(q in rows_by_q, f"unexpected q={q}")
            rows_by_q[q].append(parsed)

for q, rows in rows_by_q.items():
    expected_D, expected_epsilon, expected_total, expected_residue = EXPECTED[q]
    require(len(rows) == len(ACTIVE_A), f"wrong row count at q={q}")
    require(tuple(row["a"] for row in rows) == ACTIVE_A,
            f"incomplete or unordered rows at q={q}")
    total = Fraction(0)
    for row in rows:
        require(row["D"] == expected_D, f"wrong D at q={q}, a={row['a']}")
        require(row["epsilon"] == expected_epsilon,
                f"wrong epsilon at q={q}, a={row['a']}")
        require(row["weight"] == WEIGHTS[row["a"]],
                f"wrong weight at q={q}, a={row['a']}")
        require(row["denominator"] > 0 and row["denominator"] % P,
                f"bad denominator at q={q}, a={row['a']}")
        total += row["weight"] * Fraction(row["numerator"], row["denominator"])
    residue = reduce_mod_7(total)
    require(total == expected_total, f"wrong total at q={q}")
    require(residue == expected_residue, f"wrong residue at q={q}")
    status = "ZERO" if residue == 0 else "NONZERO"
    print(f"q={q} total={total} c(q,29)={residue} status={status}")

require(EXPECTED[8191][3] != 0 and EXPECTED[114311][3] == 0,
        "configured comparison is not zero/nonzero")
print("PASS: exact [0:1] symbol values differ at q=8191 and q=114311")
