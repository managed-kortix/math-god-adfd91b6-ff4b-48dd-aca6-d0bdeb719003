#!/usr/bin/env python3
"""Dependency-free, fail-closed verifier for the Cycle 190 L0 collision."""

import csv
import hashlib
import math
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
P = 7
ELL = 29
CONDUCTOR = 433
PRIMES = (29023, 1499)
O = None
EXPECTED_HASHES = {
    "cycle188_433a1_base_twist_sums.gp":
        "67bb4bc0fb1b666a9100ad5db5e998d02db82c6e9c11ceb5c640530a3930395c",
    "cycle188_base_twist_sums.tsv":
        "bb3e049dd19bd558c83d92560a168fac2d3cbb68e31b8c51bce00fc26bcfca3a",
    "cycle189_base433_symbol_sums.gp":
        "dd212f962025100c412e40c2d70b3020911fedfd4568d0964a7362628f37fcc1",
    "cycle189_base433_symbol_sums.csv":
        "2b4508f39aff3b07a68d781ce04d779549a0167b98a8f57f56ead5c591ad0dbf",
}
EXPECTED_FINITE = {
    29023: {
        "order": 29050,
        "trace": -26,
        "cofactor": 4150,
        "P7": (24326, 16085),
        "Q7": (19138, 16433),
    },
    1499: {
        "order": 1526,
        "trace": -26,
        "cofactor": 218,
        "P7": (1042, 847),
        "Q7": (1463, 497),
    },
}
ACTIVE_A = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14)
WEIGHTS = {
    2: 2, 3: 3, 4: 4, 5: 2, 6: 5, 7: 3,
    8: 6, 9: 6, 10: 4, 11: 1, 13: 1, 14: 5,
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for divisor in range(3, math.isqrt(n) + 1, 2):
        if n % divisor == 0:
            return False
    return True


def legendre(a, prime):
    a %= prime
    if a == 0:
        return 0
    value = pow(a, (prime - 1) // 2, prime)
    require(value in (1, prime - 1), "Euler criterion failed")
    return -1 if value == prime - 1 else 1


def fundamental_discriminant(q):
    return q if q % 4 == 1 else -q


def twist_root_number(q):
    d = fundamental_discriminant(q)
    return (1 if d > 0 else -1) * legendre(d, CONDUCTOR)


def point_count(q):
    # Under X=4x and W=8y+4x, E becomes W^2=X^3+X^2+64.
    squares = bytearray(q)
    for y in range(1, (q + 1) // 2):
        squares[y * y % q] = 1
    character_sum = 0
    for x in range(q):
        value = ((x * x % q) * (x + 1) + 64) % q
        if value:
            character_sum += 1 if squares[value] else -1
    return q + 1 + character_sum


def add(left, right, q):
    if left is O:
        return right
    if right is O:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and (y1 + y2) % q == 0:
        return O
    if left == right:
        if y1 == 0:
            return O
        slope = (3 * x1 * x1 + 2 * x1) * pow(2 * y1, -1, q) % q
    else:
        slope = (y2 - y1) * pow((x2 - x1) % q, -1, q) % q
    x3 = (slope * slope - 1 - x1 - x2) % q
    return x3, (-y1 + slope * (x1 - x3)) % q


def multiply(n, point, q):
    result = O
    while n:
        if n & 1:
            result = add(result, point, q)
        point = add(point, point, q)
        n >>= 1
    return result


def valuation(n, prime):
    result = 0
    while n % prime == 0:
        result += 1
        n //= prime
    return result


def mod7(value):
    require(value.denominator % P != 0, f"non-7-integral value {value}")
    return value.numerator * pow(value.denominator, -1, P) % P


def verify_hashes():
    for name, expected in EXPECTED_HASHES.items():
        path = HERE / name
        require(path.is_file(), f"missing hashed artifact {name}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == expected, f"SHA-256 mismatch for {name}")
        print(f"sha256 {actual}  {name}")


def verify_packet_and_kummer():
    require(PRIMES[0] != PRIMES[1], "collision primes are not distinct")
    require(is_prime(ELL) and is_prime(CONDUCTOR), "fixed primes are not prime")
    for q in PRIMES:
        require(is_prime(q), f"q={q} is composite")
        require(math.gcd(q, 2 * P * ELL * CONDUCTOR) == 1,
                f"q={q} is ramified or excluded")
        require(q % P == 1, f"q={q} is not 1 mod 7")
        require(legendre(q, ELL) == 1, f"q={q} fails (q/29)=1")
        require(twist_root_number(q) == -1, f"q={q} has wrong twist sign")

        expected = EXPECTED_FINITE[q]
        order = point_count(q)
        trace = q + 1 - order
        require(order == expected["order"], f"wrong point count at q={q}")
        require(trace == expected["trace"], f"wrong trace at q={q}")
        require(trace % P == 2 and valuation(order, P) == 1,
                f"q={q} is not in the nonidentity-unipotent packet")
        require(expected["cofactor"] == order // P, f"wrong cofactor at q={q}")

        p7 = multiply(order // P, (0, 8), q)
        q7 = multiply(order // P, (-4 % q, 4), q)
        require(p7 == expected["P7"] and q7 == expected["Q7"],
                f"finite-field witness mismatch at q={q}")
        require(p7 is not O and multiply(P, p7, q) is O,
                f"P witness does not have order seven at q={q}")
        require(q7 == multiply(5, p7, q), f"row is not [1:5] at q={q}")
        print(
            f"q={q} prime #E={order} a_q={trace} v7=1 "
            f"P7={p7} Q7={q7} row=[1:5]"
        )

    # The quotient transport is the unique F_7-linear map taking P7 at q0
    # to P7 at q1; the checked relations show that it also takes Q7 to Q7.
    print("transport: P7(29023)->P7(1499), Q7=5P7->5P7=Q7; row preserved")


def dlogs():
    result = {}
    value = 1
    for exponent in range(28):
        require(value not in result, "eta=2 has order below 28 modulo 29")
        result[value] = exponent
        value = 2 * value % ELL
    require(value == 1 and len(result) == 28, "eta=2 is not primitive mod 29")
    return result


def verify_q1499_symbols(logs):
    path = HERE / "cycle188_base_twist_sums.tsv"
    values = {}
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        require(len(fields) == 8, "bad Cycle 188 TSV schema")
        q, a, log_value, log_mod7 = map(int, fields[:4])
        if q != 1499:
            continue
        u_value, kappa, t_value = map(Fraction, fields[4:7])
        t_mod7 = int(fields[7])
        require(a not in values and 1 <= a < ELL, "duplicate/bad q=1499 row")
        require(log_value == logs[a] and log_mod7 == logs[a] % P,
                "bad discrete logarithm at q=1499")
        require(kappa == 1 and t_value == u_value and mod7(t_value) == t_mod7,
                "bad normalization or reduction at q=1499")
        values[a] = t_value
    require(set(values) == set(range(1, ELL)), "incomplete q=1499 symbol rows")
    full = sum(Fraction(logs[a]) * values[a] for a in values)
    short = sum(Fraction(WEIGHTS[a]) * values[a] for a in ACTIVE_A)
    require(full == Fraction(-150), "wrong q=1499 full modular-symbol sum")
    require(short == Fraction(365, 2), "wrong q=1499 shortened sum")
    require(mod7(full) == 4 and mod7(short) == 4, "wrong q=1499 residue")
    print(f"q=1499 modular sums: full={full} short={short} c=4 NONZERO")


def verify_q29023_symbols():
    path = HERE / "cycle189_base433_symbol_sums.csv"
    rows = []
    with path.open(newline="", encoding="ascii") as source:
        reader = csv.DictReader(source)
        require(reader.fieldnames == [
            "q", "D", "epsilon", "a", "weight", "numerator", "denominator"
        ], "bad Cycle 189 CSV schema")
        for raw in reader:
            row = {key: int(value) for key, value in raw.items()}
            if row["q"] == 29023:
                rows.append(row)
    require(tuple(row["a"] for row in rows) == ACTIVE_A,
            "incomplete or unordered q=29023 rows")
    total = Fraction(0)
    for row in rows:
        require(row["D"] == -29023 and row["epsilon"] == -1,
                "bad q=29023 twist metadata")
        require(row["weight"] == WEIGHTS[row["a"]], "bad q=29023 weight")
        value = Fraction(row["numerator"], row["denominator"])
        require(value.denominator % P != 0, "bad q=29023 denominator")
        total += row["weight"] * value
    require(total == Fraction(77, 2), "wrong q=29023 modular-symbol sum")
    require(mod7(total) == 0, "q=29023 coordinate is not zero")
    print(f"q=29023 modular sum: short={total} c=0 ZERO")


def main():
    verify_hashes()
    verify_packet_and_kummer()
    logs = dlogs()
    verify_q1499_symbols(logs)
    verify_q29023_symbols()
    print("PASS Cycle 190: same L0 class [1:5], but vanishing values differ")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        raise SystemExit(f"FAIL Cycle 190: {error}") from error
