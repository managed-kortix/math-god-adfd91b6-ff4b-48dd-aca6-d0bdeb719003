#!/usr/bin/env python3
"""Dependency-free exact checks for the Cycle 135 433a1 certificate.

The modular-symbol matrix is certificate input.  This program verifies all
of its stated integer and mod-7 consequences, but does not independently
recompute modular symbols from Manin symbols.
"""

import math
import sys


P = 7
CURVE = (1, 0, 0, 0, 1)
AUXILIARY = ((29, 2, 2), (113, 3, 2))  # (ell, primitive root, a_ell)

SYMBOL_SUMS = (
    (13, -18, -14, 24, 9, -18, 8),
    (22, -1, -24, -4, 23, -13, -8),
    (4, 30, -16, -10, 12, 2, -24),
    (-9, 13, 11, -24, 11, 13, -9),
    (-24, 2, 12, -10, -16, 30, 4),
    (-8, -13, 23, -4, -24, -1, 22),
    (8, -18, 9, 24, -14, -18, 13),
)

EXPECTED_CONTRIBUTIONS = (
    (0, 0, 0, 0, 0, 0, 0),
    (0, 6, 1, 2, 1, 5, 1),
    (0, 4, 6, 3, 5, 6, 6),
    (0, 4, 3, 1, 6, 6, 6),
    (0, 1, 5, 6, 3, 5, 5),
    (0, 5, 6, 3, 3, 3, 2),
    (0, 4, 3, 5, 0, 6, 6),
)
EXPECTED_ROW_SUMS = (0, 2, 2, 5, 4, 1, 3)
EXPECTED_COLUMN_SUMS = (0, 3, 3, 6, 4, 3, 5)


class VerificationError(Exception):
    pass


def check(condition, message):
    if not condition:
        raise VerificationError(message)


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def curve_invariants(ainvs):
    a1, a2, a3, a4, a6 = ainvs
    b2 = a1 * a1 + 4 * a2
    b4 = a1 * a3 + 2 * a4
    b6 = a3 * a3 + 4 * a6
    b8 = (a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4
          + a2 * a3 * a3 - a4 * a4)
    c4 = b2 * b2 - 24 * b4
    c6 = -b2 * b2 * b2 + 36 * b2 * b4 - 216 * b6
    discriminant = (-b2 * b2 * b8 - 8 * b4 * b4 * b4
                    - 27 * b6 * b6 + 9 * b2 * b4 * b6)
    return (b2, b4, b6, b8), c4, c6, discriminant


def legendre_symbol(a, prime):
    a %= prime
    if a == 0:
        return 0
    value = pow(a, (prime - 1) // 2, prime)
    check(value in (1, prime - 1), "Euler criterion did not return a sign")
    return 1 if value == 1 else -1


def point_count(prime):
    count = 1  # point at infinity
    for x in range(prime):
        right = (x * x * x + 1) % prime
        for y in range(prime):
            if (y * y + x * y - right) % prime == 0:
                count += 1
    return count


def discrete_log_table(prime, generator):
    table = {}
    value = 1
    for exponent in range(prime - 1):
        check(value not in table, f"generator repeats early modulo {prime}")
        table[value] = exponent
        value = value * generator % prime
    check(value == 1, f"generator does not close modulo {prime}")
    check(set(table) == set(range(1, prime)),
          f"generator is not primitive modulo {prime}")
    for residue, exponent in table.items():
        check(pow(generator, exponent, prime) == residue,
              f"bad discrete log modulo {prime} at residue {residue}")
    return table


def on_curve(point):
    x, y = point
    return y * y + x * y == x * x * x + 1


def verify_curve():
    b, c4, c6, discriminant = curve_invariants(CURVE)
    check(b == (1, 0, 4, 1), f"unexpected b-invariants: {b}")
    check(c4 == 1, f"unexpected c4: {c4}")
    check(c6 == -865, f"unexpected c6: {c6}")
    check(discriminant == -433, f"unexpected discriminant: {discriminant}")
    check(is_prime(433), "433 is not prime")

    # Integral c4 and Delta with v_433(Delta)=1 give a minimal model with
    # multiplicative reduction of conductor exponent one at 433.  Delta is a
    # unit elsewhere, so the conductor is exactly 433.
    check(discriminant % (433 * 433) != 0, "v_433(Delta) is not one")
    check(c4 % 433 != 0, "reduction at 433 is not multiplicative")
    check(legendre_symbol(-c6, 433) == 1,
          "multiplicative reduction at 433 is not split")

    for point in ((0, 1), (-1, 1)):
        check(on_curve(point), f"point {point} is not on E")
    check((0, 1) != (-1, 1), "listed rational points coincide")
    return discriminant


def verify_point_counts():
    expected = {7: -3, 29: 2, 113: 2}
    results = {}
    for prime, expected_trace in expected.items():
        check(is_prime(prime), f"{prime} is not prime")
        count = point_count(prime)
        trace = prime + 1 - count
        check(trace == expected_trace,
              f"a_{prime}={trace}, expected {expected_trace}")
        results[prime] = (count, trace)
    check(results[7][0] % P != 0, "E(F_7) is anomalous")
    check(results[7][1] % P != 0, "reduction at 7 is not ordinary")
    return results


def verify_auxiliary_primes(point_counts):
    log_tables = {}
    for ell, generator, expected_trace in AUXILIARY:
        table = discrete_log_table(ell, generator)
        log_tables[ell] = table
        count, trace = point_counts[ell]
        check(trace == expected_trace, f"stored a_{ell} mismatch")
        check(ell % P == 1, f"{ell} is not 1 modulo {P}")
        check((trace - ell - 1) % P == 0,
              f"a_{ell} is not ell+1 modulo {P}")
        check(math.gcd(ell - 1, count) % P == 0,
              f"cyclotomic ideal at {ell} is not divisible by {P}")
        check(math.gcd(ell - 1, count) % (P * P) != 0,
              f"cyclotomic ideal at {ell} is not exactly {P}Z_{P}")
        check(ell not in (P, 433), f"{ell} divides pN")
    return log_tables


def verify_symbol_certificate():
    check(len(SYMBOL_SUMS) == P, "symbol matrix does not have seven rows")
    check(all(len(row) == P for row in SYMBOL_SUMS),
          "symbol matrix does not have seven columns")
    contributions = tuple(
        tuple((i * j * SYMBOL_SUMS[i][j]) % P for j in range(P))
        for i in range(P)
    )
    check(contributions == EXPECTED_CONTRIBUTIONS,
          "weighted contribution matrix mismatch")
    row_sums = tuple(sum(row) % P for row in contributions)
    column_sums = tuple(
        sum(contributions[i][j] for i in range(P)) % P for j in range(P)
    )
    check(row_sums == EXPECTED_ROW_SUMS, f"row sums mismatch: {row_sums}")
    check(column_sums == EXPECTED_COLUMN_SUMS,
          f"column sums mismatch: {column_sums}")
    check(sum(row_sums) % P == sum(column_sums) % P,
          "row and column totals disagree")
    delta = sum(row_sums) % P
    check(delta == 3, f"normalized Kurihara delta is {delta}, expected 3")
    check(delta != 0, "Kurihara delta vanishes")
    return contributions, row_sums, column_sums, delta


def main():
    try:
        discriminant = verify_curve()
        point_counts = verify_point_counts()
        logs = verify_auxiliary_primes(point_counts)
        _, row_sums, column_sums, delta = verify_symbol_certificate()
    except (ArithmeticError, VerificationError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print("PASS Cycle 135 exact certificate checks for 433a1 at p=7")
    print(f"curve: y^2+xy=x^3+1; Delta={discriminant}; conductor=433")
    print("point counts: " + ", ".join(
        f"#E(F_{prime})={count}, a_{prime}={trace}"
        for prime, (count, trace) in sorted(point_counts.items())
    ))
    print("primitive roots/log tables: " + ", ".join(
        f"g_{ell}={generator} ({len(logs[ell])} entries)"
        for ell, generator, _ in AUXILIARY
    ))
    print(f"row sums mod 7: {row_sums}")
    print(f"column sums mod 7: {column_sums}")
    print(f"normalized delta_29*113={delta} mod 7")
    print("points checked: (0,1), (-1,1); independence is not certified here")
    print("scope: grouped modular-symbol matrix is verified as certificate input")
    return 0


if __name__ == "__main__":
    sys.exit(main())
