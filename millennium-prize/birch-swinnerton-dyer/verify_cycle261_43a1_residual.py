#!/usr/bin/env python3
"""Exact finite checks in the Cycle 261 residual-image certificate."""

from fractions import Fraction
from itertools import product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def count_points(p):
    return 1 + sum(
        (y * y + y - x * x * x - x * x) % p == 0
        for x in range(p)
        for y in range(p)
    )


def cubic_discriminant(a, b, c, d):
    return b * b * c * c - 4 * a * c**3 - 4 * b**3 * d - 27 * a * a * d * d + 18 * a * b * c * d


def determinant(a, p):
    return (a[0] * a[3] - a[1] * a[2]) % p


def multiply(a, b, p):
    return tuple(
        sum(a[2 * i + k] * b[2 * k + j] for k in range(2)) % p
        for i in range(2)
        for j in range(2)
    )


def generated_group(generators, p):
    identity = (1, 0, 0, 1)
    group = {identity}
    frontier = [identity]
    while frontier:
        a = frontier.pop()
        for b in generators:
            ab = multiply(a, b, p)
            if ab not in group:
                group.add(ab)
                frontier.append(ab)
    return group


def small_prime_certificate(p, q, trace):
    transvection = (1, 1, 0, 1)
    matrices = [
        a
        for a in product(range(p), repeat=4)
        if determinant(a, p) == q % p and (a[0] + a[3]) % p == trace % p
    ]
    orders = {len(generated_group((transvection, a), p)) for a in matrices}
    expected = (p * p - 1) * (p * p - p)
    require(orders == {expected}, f"small-prime relative-position check failed at p={p}: {orders}")
    return len(matrices), expected


# Completing the square gives Y^2 = 4*x^3+4*x^2+1.  Rational-root
# candidates are all checked, and a separable irreducible cubic with
# nonsquare discriminant has Galois group S_3.
roots = (1, -1, Fraction(1, 2), Fraction(-1, 2), Fraction(1, 4), Fraction(-1, 4))
require(all(4 * x**3 + 4 * x**2 + 1 != 0 for x in roots), "2-division cubic has a rational root")
two_division_discriminant = cubic_discriminant(4, 4, 0, 1)
require(two_division_discriminant == -16 * 43, "wrong 2-division discriminant")

frobenius = {}
for q in (2, 3):
    cardinality = count_points(q)
    trace = q + 1 - cardinality
    frobenius[q] = (trace, trace * trace - 4 * q, cardinality)
require(frobenius == {2: (-2, -4, 5), 3: (-2, -8, 6)}, f"wrong point counts: {frobenius}")

# These nonsquare discriminants rule out invariant lines at the only small odd
# primes not covered by the semistable reducibility lemma plus Mazur torsion.
require(frobenius[2][1] % 3 == 2, "p=3 Frobenius discriminant check failed")
require(frobenius[3][1] % 5 == 2, "p=5 Frobenius discriminant check failed")
require(frobenius[2][1] % 7 == 3, "p=7 Frobenius discriminant check failed")

small = {
    3: small_prime_certificate(3, 2, -2),
    5: small_prime_certificate(5, 3, -2),
}
require(small == {3: (6, 48), 5: (20, 480)}, f"wrong small-image certificate: {small}")

print("MODEL=y^2+y=x^3+x^2")
print("MINIMAL_DISCRIMINANT=-43 VALUATION_AT_43=1")
print(f"TWO_DIVISION_DISCRIMINANT={two_division_discriminant} GALOIS_GROUP=S3")
for q, (trace, disc, cardinality) in frobenius.items():
    print(f"FROBENIUS q={q} a_q={trace} disc={disc} points={cardinality}")
for p, (matrix_count, order) in small.items():
    print(f"SMALL_IMAGE p={p} matrices={matrix_count} generated_order={order}")
print("THEOREM_INPUT=SEMISTABLE_REDUCIBLE_IMPLIES_ISOGENOUS_RATIONAL_p_TORSION_PLUS_MAZUR_TORSION")
print("THEOREM_INPUT=DICKSON_TRANSVECTION_CLASSIFICATION_FOR_p>=7")
print("ALL_PRIME_RESIDUAL_SURJECTIVITY_CERTIFICATE=PASS")
