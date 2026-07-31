#!/usr/bin/env python3
"""Dependency-free exact verifier for the Cycle 189 raw-sum certificate."""

import csv
from fractions import Fraction
from pathlib import Path


P = 7
KNOWN_Q1499_RESIDUE = 4
ACTIVE_A = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14)
WEIGHTS = {2: 2, 3: 3, 4: 4, 5: 2, 6: 5, 7: 3,
           8: 6, 9: 6, 10: 4, 11: 1, 13: 1, 14: 5}
EXPECTED = {
    7589: (7589, 1, Fraction(359, 2), 1),
    14071: (-14071, -1, Fraction(1243, 2), 2),
    29023: (-29023, -1, Fraction(77, 2), 0),
}


def mod7(value: Fraction) -> int:
    if value.denominator % P == 0:
        raise AssertionError(f"non-7-integral rational: {value}")
    return value.numerator * pow(value.denominator, -1, P) % P


path = Path(__file__).with_name("cycle189_base433_symbol_sums.csv")
rows_by_q = {q: [] for q in EXPECTED}
with path.open(newline="", encoding="ascii") as source:
    reader = csv.DictReader(source)
    assert reader.fieldnames == [
        "q", "D", "epsilon", "a", "weight", "numerator", "denominator"
    ]
    for source_row in reader:
        row = {key: int(value) for key, value in source_row.items()}
        q = row["q"]
        if q not in rows_by_q:
            raise AssertionError(f"unexpected q={q}")
        rows_by_q[q].append(row)

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
    residue = mod7(total)
    assert total == expected_total and residue == expected_residue
    status = "ZERO" if residue == 0 else "NONZERO"
    print(f"q={q} total={total} c(q,29)={residue} status={status}")

assert KNOWN_Q1499_RESIDUE != 0 and EXPECTED[29023][3] == 0
print("PASS: exact raw sums, rational totals, and mod-7 zero are verified")
