#!/usr/bin/env python3
"""Exact arithmetic packet for the D=-1499 one-prime Kurihara certificate."""

import hashlib
import math
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATA = HERE / "cycle188_base_twist_sums.tsv"
EXPECTED_SHA256 = "bb3e049dd19bd558c83d92560a168fac2d3cbb68e31b8c51bce00fc26bcfca3a"
P = (
    Fraction(399030891253207, 156180668809),
    Fraction(7009131418974188521075, 61722131771310373),
)
MODULUS = 29
IDENTITY = None


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(left, right):
    if left is IDENTITY:
        return right
    if right is IDENTITY:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and (y1 + y2 + x1 + 1) % MODULUS == 0:
        return IDENTITY
    if left == right:
        denominator = (2 * y1 + x1 + 1) % MODULUS
        require(denominator != 0, "unexpected vertical tangent")
        slope = (3 * x1 * x1 - 46813 - y1) * pow(denominator, -1, MODULUS)
        nu = (-x1 ** 3 - 46813 * x1 - 2 * 3372156843 - y1) * pow(
            denominator, -1, MODULUS
        )
    else:
        denominator = (x2 - x1) % MODULUS
        slope = (y2 - y1) * pow(denominator, -1, MODULUS)
        nu = (y1 * x2 - y2 * x1) * pow(denominator, -1, MODULUS)
    slope %= MODULUS
    nu %= MODULUS
    x3 = (slope * slope + slope - x1 - x2) % MODULUS
    y3 = (-(slope + 1) * x3 - nu - 1) % MODULUS
    require(on_curve((x3, y3)), "group law produced an off-curve point")
    return x3, y3


def multiply(n, point):
    result = IDENTITY
    while n:
        if n & 1:
            result = add(result, point)
        point = add(point, point)
        n >>= 1
    return result


def on_curve(point):
    x, y = point
    return (y * y + x * y + y - x ** 3 + 46813 * x + 3372156843) % MODULUS == 0


def mod_fraction(value):
    require(value.denominator % MODULUS != 0, "point has bad denominator at 29")
    return value.numerator * pow(value.denominator, -1, MODULUS) % MODULUS


def point_count():
    return 1 + sum(
        1
        for x in range(MODULUS)
        for y in range(MODULUS)
        if on_curve((x, y))
    )


def discrete_logs():
    result = {}
    value = 1
    for exponent in range(28):
        require(value not in result, "2 is not primitive modulo 29")
        result[value] = exponent
        value = 2 * value % MODULUS
    require(value == 1 and len(result) == 28, "bad discrete-log table")
    return result


def kurihara_value():
    actual_hash = hashlib.sha256(DATA.read_bytes()).hexdigest()
    require(actual_hash == EXPECTED_SHA256, "Cycle 188 data SHA-256 mismatch")
    logs = discrete_logs()
    values = {}
    for line in DATA.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        require(len(fields) == 8, "bad Cycle 188 row")
        q, a, log_value, log_mod7 = map(int, fields[:4])
        if q != 1499:
            continue
        u_value, kappa, twist_value = map(Fraction, fields[4:7])
        require(a not in values, "duplicate q=1499 row")
        require(log_value == logs[a] and log_mod7 == log_value % 7, "bad dlog")
        require(kappa == 1 and twist_value == u_value, "bad period normalization")
        require(twist_value.denominator % 7 != 0, "non-7-integral twist symbol")
        values[a] = twist_value
    require(set(values) == set(range(1, 29)), "incomplete q=1499 symbol table")
    total = sum(Fraction(logs[a]) * values[a] for a in range(1, 29))
    residue = total.numerator * pow(total.denominator, -1, 7) % 7
    require(total == -150 and residue == 4, "wrong Kurihara value")
    return actual_hash, total, residue


def main():
    x, y = P
    require(y * y + x * y + y == x ** 3 - 46813 * x - 3372156843,
            "P is not on the rational curve")
    reduced = mod_fraction(x), mod_fraction(y)
    require(reduced == (0, 11) and on_curve(reduced), "wrong reduction of P at 29")
    require(point_count() == 28, "wrong point count at 29")
    require(multiply(28, reduced) is IDENTITY, "28P is not zero modulo 29")
    for prime_divisor in (2, 7):
        require(multiply(28 // prime_divisor, reduced) is not IDENTITY,
                "P does not have order 28 modulo 29")
    data_hash, total, residue = kurihara_value()

    print("Cycle 209 D=-1499 exact seven-Selmer arithmetic packet")
    print(f"sha256={data_hash}  {DATA.name}")
    print("#E(F_29)=28; P mod 29=(0,11) has exact order 28")
    print("P maps nontrivially to E(F_29)/7E(F_29)")
    print(f"delta_tilde_29={total}; delta_tilde_29 mod 7={residue} (nonzero)")
    print("EXACT_ARITHMETIC_STATUS=PASS")


if __name__ == "__main__":
    main()
