#!/usr/bin/env python3
"""Dependency-free verifier for the Cycle 190 full-28-row certificate."""

import csv
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATA = HERE / "cycle190_independent_full28_base433.csv"
EXPECTED = {
    1499: (Fraction(-150), Fraction(365, 2), 4),
    29023: (Fraction(-3108), Fraction(77, 2), 0),
}
SHORT_WEIGHTS = [0, 2, 3, 4, 2, 5, 3, 6, 6, 4, 1, 0, 1, 5]


def mod7(value: Fraction) -> int:
    assert value.denominator % 7
    return value.numerator * pow(value.denominator, -1, 7) % 7


def discrete_logs() -> dict[int, int]:
    logs = {}
    value = 1
    for exponent in range(28):
        assert value not in logs
        logs[value] = exponent
        value = 2 * value % 29
    assert value == 1 and len(logs) == 28
    return logs


logs = discrete_logs()
rows: dict[int, dict[int, Fraction]] = {}
with DATA.open(newline="", encoding="ascii") as handle:
    reader = csv.DictReader(handle)
    assert reader.fieldnames == [
        "q", "D", "epsilon", "a", "dlog2", "numerator", "denominator"
    ]
    for record in reader:
        q = int(record["q"])
        a = int(record["a"])
        assert int(record["D"]) == -q and int(record["epsilon"]) == -1
        assert int(record["dlog2"]) == logs[a]
        value = Fraction(int(record["numerator"]), int(record["denominator"]))
        assert a not in rows.setdefault(q, {})
        rows[q][a] = value

assert set(rows) == set(EXPECTED)
for q, values in rows.items():
    assert set(values) == set(range(1, 29))
    for a in range(1, 15):
        assert values[a] == values[29 - a]

    full = sum(Fraction(logs[a]) * values[a] for a in range(1, 29))
    paired = sum(Fraction(SHORT_WEIGHTS[a - 1]) * values[a] for a in range(1, 15))
    expected_full, expected_paired, expected_residue = EXPECTED[q]
    assert full == expected_full
    assert paired == expected_paired
    assert mod7(full) == mod7(paired) == expected_residue
    print(
        f"q={q} rows=28 full={full} paired={paired} "
        f"c_mod7={expected_residue} status={'ZERO' if expected_residue == 0 else 'NONZERO'}"
    )

assert mod7(EXPECTED[1499][0]) == 4
assert mod7(EXPECTED[29023][0]) == 0
print("Cycle 190 independent full-28-row certificate: PASS")
