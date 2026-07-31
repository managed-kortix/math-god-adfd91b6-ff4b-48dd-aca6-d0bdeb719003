#!/usr/bin/env python3
"""Dependency-free replay of the Cycle 188 rational and mod-7 arithmetic."""

import csv
from fractions import Fraction
from pathlib import Path


P = 7
ACTIVE_A = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14)
WEIGHTS = {2: 2, 3: 3, 4: 4, 5: 2, 6: 5, 7: 3,
           8: 6, 9: 6, 10: 4, 11: 1, 13: 1, 14: 5}
EXPECTED = {
    3823: (-3823, -1, Fraction(-90), 1),
    8317: (8317, 1, Fraction(-1413, 2), 4),
}


def reduce_mod_7(value: Fraction) -> int:
    denominator = value.denominator % P
    if denominator == 0:
        raise AssertionError(f"non-7-integral rational: {value}")
    return (value.numerator % P) * pow(denominator, -1, P) % P


path = Path(__file__).with_name("cycle188_base433_symbol_sums.csv")
rows_by_q = {q: [] for q in EXPECTED}
with path.open(newline="", encoding="ascii") as source:
    for row in csv.DictReader(source):
        parsed = {key: int(value) for key, value in row.items()}
        q = parsed["q"]
        if q not in rows_by_q:
            raise AssertionError(f"unexpected q={q}")
        rows_by_q[q].append(parsed)

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
        value = Fraction(row["numerator"], row["denominator"])
        total += row["weight"] * value
    residue = reduce_mod_7(total)
    assert total == expected_total
    assert residue == expected_residue
    print(f"q={q} total={total} c(q,29)={residue} status=NONZERO")

print("PASS: CSV schema, exact rational totals, 7-integrality, and residues verified")
