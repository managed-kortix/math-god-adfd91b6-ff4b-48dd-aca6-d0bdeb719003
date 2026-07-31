#!/usr/bin/env python3
"""Dependency-free exact verifier for the Cycle 189 [1:3] certificate."""

import csv
from fractions import Fraction
from pathlib import Path


P = 7
ACTIVE_A = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14)
WEIGHTS = {2: 2, 3: 3, 4: 4, 5: 2, 6: 5, 7: 3,
           8: 6, 9: 6, 10: 4, 11: 1, 13: 1, 14: 5}
EXPECTED = {
    11831: (-11831, -1, Fraction(74), 4),
    14897: (14897, 1, Fraction(-17, 2), 2),
    48889: (48889, 1, Fraction(-341), 2),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def reduce_mod_7(value: Fraction) -> int:
    require(value.denominator % P != 0, f"non-7-integral rational: {value}")
    return value.numerator * pow(value.denominator, -1, P) % P


path = Path(__file__).with_name("cycle189_base_symbol_sums.csv")
rows_by_q = {q: [] for q in EXPECTED}
with path.open(newline="", encoding="ascii") as source:
    data_lines = (line for line in source if not line.startswith("#"))
    for row in csv.DictReader(data_lines):
        parsed = {key: int(value) for key, value in row.items()}
        q = parsed["q"]
        require(q in rows_by_q, f"unexpected q={q}")
        rows_by_q[q].append(parsed)

statuses = set()
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
    statuses.add(status)
    print(f"q={q} total={total} c(q,29)={residue} status={status}")

require(statuses == {"NONZERO"}, "unexpected zero in [1:3] rows")
print("PASS: all three [1:3] coordinates are nonzero; no zero/nonzero collision")
