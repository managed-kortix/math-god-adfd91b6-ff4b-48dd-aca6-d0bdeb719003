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


def reduce_mod_7(value: Fraction) -> int:
    if value.denominator % P == 0:
        raise AssertionError(f"non-7-integral rational: {value}")
    return value.numerator * pow(value.denominator, -1, P) % P


path = Path(__file__).with_name("cycle189_base_symbol_sums.csv")
rows_by_q = {q: [] for q in EXPECTED}
with path.open(newline="", encoding="ascii") as source:
    data_lines = (line for line in source if not line.startswith("#"))
    for row in csv.DictReader(data_lines):
        parsed = {key: int(value) for key, value in row.items()}
        q = parsed["q"]
        if q not in rows_by_q:
            raise AssertionError(f"unexpected q={q}")
        rows_by_q[q].append(parsed)

statuses = set()
for q, rows in rows_by_q.items():
    expected_D, expected_epsilon, expected_total, expected_residue = EXPECTED[q]
    assert len(rows) == len(ACTIVE_A)
    assert tuple(row["a"] for row in rows) == ACTIVE_A
    total = Fraction(0)
    for row in rows:
        assert row["D"] == expected_D
        assert row["epsilon"] == expected_epsilon
        assert row["weight"] == WEIGHTS[row["a"]]
        assert row["denominator"] > 0 and row["denominator"] % P
        total += row["weight"] * Fraction(row["numerator"], row["denominator"])
    residue = reduce_mod_7(total)
    assert total == expected_total
    assert residue == expected_residue
    status = "ZERO" if residue == 0 else "NONZERO"
    statuses.add(status)
    print(f"q={q} total={total} c(q,29)={residue} status={status}")

assert statuses == {"NONZERO"}
print("PASS: all three [1:3] coordinates are nonzero; no zero/nonzero collision")
