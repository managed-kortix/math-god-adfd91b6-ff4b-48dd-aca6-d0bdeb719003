#!/usr/bin/env python3
"""Dependency-free exact verifier for the Cycle 188 rational certificate."""

from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATA = HERE / "cycle188_base_twist_sums.tsv"
EXPECTED = {
    1499: (Fraction(-150), Fraction(365, 2), 4),
    6287: (Fraction(-1616), Fraction(-733, 2), 1),
}
SHORT_WEIGHTS = {2: 2, 3: 3, 4: 4, 5: 2, 6: 5, 7: 3,
                 8: 6, 9: 6, 10: 4, 11: 1, 13: 1, 14: 5}


def mod7(x: Fraction) -> int:
    if x.denominator % 7 == 0:
        raise AssertionError(f"non-7-integral rational: {x}")
    return x.numerator * pow(x.denominator, -1, 7) % 7


def dlogs() -> dict[int, int]:
    out = {}
    x = 1
    for j in range(28):
        assert x not in out
        out[x] = j
        x = 2 * x % 29
    assert x == 1 and len(out) == 28
    return out


logs = dlogs()
rows: dict[int, dict[int, Fraction]] = {}
for line in DATA.read_text(encoding="ascii").splitlines():
    if not line or line.startswith("#"):
        continue
    fields = line.split("\t")
    assert len(fields) == 8
    q, a, dl, dl7 = map(int, fields[:4])
    U, kappa, T = map(Fraction, fields[4:7])
    t7 = int(fields[7])
    assert dl == logs[a] and dl7 == dl % 7
    assert kappa == 1 and T == kappa * U and t7 == mod7(T)
    assert a not in rows.setdefault(q, {})
    rows[q][a] = T

assert set(rows) == set(EXPECTED)
for q, values in rows.items():
    assert set(values) == set(range(1, 29))
    for a in range(1, 15):
        assert values[a] == values[29 - a]

    full = sum(Fraction(logs[a]) * values[a] for a in range(1, 29))
    short = sum(Fraction(weight) * values[a] for a, weight in SHORT_WEIGHTS.items())
    full_expected, short_expected, residue_expected = EXPECTED[q]
    assert full == full_expected
    assert short == short_expected
    assert mod7(full) == residue_expected
    assert mod7(short) == residue_expected
    print(
        f"q={q} rows=28 raw_full_sum={full} "
        f"raw_short_sum={short} c_mod7={residue_expected} nonzero"
    )

print("Cycle 188 certificate: PASS")
