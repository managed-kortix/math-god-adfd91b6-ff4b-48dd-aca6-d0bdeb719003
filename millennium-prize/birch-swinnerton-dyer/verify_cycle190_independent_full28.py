#!/usr/bin/env python3
"""Fail-closed verifier for the Cycle 190 same-backend full-28-row replay."""

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


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def mod7(value: Fraction) -> int:
    require(value.denominator % 7 != 0, f"non-7-integral value {value}")
    return value.numerator * pow(value.denominator, -1, 7) % 7


def discrete_logs() -> dict[int, int]:
    logs = {}
    value = 1
    for exponent in range(28):
        require(value not in logs, "2 has order below 28 modulo 29")
        logs[value] = exponent
        value = 2 * value % 29
    require(value == 1 and len(logs) == 28, "2 is not primitive modulo 29")
    return logs


logs = discrete_logs()
rows: dict[int, dict[int, Fraction]] = {}
with DATA.open(newline="", encoding="ascii") as handle:
    reader = csv.DictReader(handle)
    require(reader.fieldnames == [
        "q", "D", "epsilon", "a", "dlog2", "numerator", "denominator"
    ], "bad CSV schema")
    for record in reader:
        q = int(record["q"])
        a = int(record["a"])
        require(int(record["D"]) == -q and int(record["epsilon"]) == -1,
                f"bad twist metadata at q={q}, a={a}")
        require(a in logs and int(record["dlog2"]) == logs[a],
                f"bad discrete logarithm at q={q}, a={a}")
        value = Fraction(int(record["numerator"]), int(record["denominator"]))
        require(a not in rows.setdefault(q, {}), f"duplicate row q={q}, a={a}")
        rows[q][a] = value

require(set(rows) == set(EXPECTED), "unexpected or missing prime rows")
for q, values in rows.items():
    require(set(values) == set(range(1, 29)), f"incomplete rows at q={q}")
    for a in range(1, 15):
        require(values[a] == values[29 - a], f"pairing failure at q={q}, a={a}")

    full = sum(Fraction(logs[a]) * values[a] for a in range(1, 29))
    paired = sum(Fraction(SHORT_WEIGHTS[a - 1]) * values[a] for a in range(1, 15))
    expected_full, expected_paired, expected_residue = EXPECTED[q]
    require(full == expected_full, f"wrong full lift at q={q}")
    require(paired == expected_paired, f"wrong paired lift at q={q}")
    require(mod7(full) == mod7(paired) == expected_residue,
            f"wrong reduction at q={q}")
    print(
        f"q={q} rows=28 full={full} paired={paired} "
        f"c_mod7={expected_residue} status={'ZERO' if expected_residue == 0 else 'NONZERO'}"
    )

require(mod7(EXPECTED[1499][0]) == 4, "configured q=1499 residue is wrong")
require(mod7(EXPECTED[29023][0]) == 0, "configured q=29023 residue is wrong")
print("Cycle 190 separate same-backend full-28-row replay: PASS")
