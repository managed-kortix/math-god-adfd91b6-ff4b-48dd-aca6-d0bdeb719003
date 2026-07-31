#!/usr/bin/env python3
"""Dependency-free finite checks for the Cycle 191 mod-49 extension."""

import math
import sys


O = None
P = (0, 1)
DATA = {
    1499: {
        "order": 1526,
        "trace": -26,
        "witness": (805, 1292),
        "difference": (1249, 657),
        "projection_p": (1010, 163),
    },
    29023: {
        "order": 29050,
        "trace": -26,
        "witness": (433, 28654),
        "difference": (16289, 21235),
        "projection_p": (20593, 24365),
    },
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


def on_curve(point, prime):
    if point is O:
        return True
    x, y = point
    return (y * y + x * y - x**3 - 1) % prime == 0


def negate(point, prime):
    if point is O:
        return O
    x, y = point
    return x % prime, (-y - x) % prime


def add(left, right, prime):
    if left is O:
        return right
    if right is O:
        return left
    if right == negate(left, prime):
        return O
    x1, y1 = left
    x2, y2 = right
    if x1 != x2:
        inverse = pow((x2 - x1) % prime, -1, prime)
        slope = (y2 - y1) * inverse % prime
        intercept = (y1 * x2 - y2 * x1) * inverse % prime
    else:
        denominator = (2 * y1 + x1) % prime
        require(denominator, "unhandled vertical tangent")
        inverse = pow(denominator, -1, prime)
        slope = (3 * x1 * x1 - y1) * inverse % prime
        intercept = (-x1**3 + 2) * inverse % prime
    x3 = (slope * slope + slope - x1 - x2) % prime
    result = x3, (-(slope + 1) * x3 - intercept) % prime
    require(on_curve(result, prime), "addition produced an off-curve point")
    return result


def multiply(multiplier, point, prime):
    if multiplier < 0:
        return multiply(-multiplier, negate(point, prime), prime)
    result = O
    while multiplier:
        if multiplier & 1:
            result = add(result, point, prime)
        point = add(point, point, prime)
        multiplier >>= 1
    return result


def point_count(prime):
    # With X=4x and W=8y+4x, the equation is W^2=X^3+X^2+64.
    squares = bytearray(prime)
    for value in range(1, (prime + 1) // 2):
        squares[value * value % prime] = 1
    character_sum = 0
    for x in range(prime):
        value = ((x * x % prime) * (x + 1) + 64) % prime
        if value:
            character_sum += 1 if squares[value] else -1
    return prime + 1 + character_sum


def valuation(n, prime):
    result = 0
    while n % prime == 0:
        result += 1
        n //= prime
    return result


def verify_prime(prime, expected):
    require(is_prime(prime), f"q={prime} is composite")
    order = point_count(prime)
    trace = prime + 1 - order
    require((order, trace) == (expected["order"], expected["trace"]),
            f"bad Frobenius data at q={prime}")
    require(valuation(order, 7) == 1, f"v7(#E(F_{prime})) is not one")

    q_point = (-1 % prime, 1)
    difference = add(q_point, multiply(-5, P, prime), prime)
    require(difference == expected["difference"],
            f"bad Q-5P value at q={prime}")
    witness = expected["witness"]
    require(on_curve(witness, prime), f"bad witness at q={prime}")
    require(multiply(49, witness, prime) == difference,
            f"Q-5P is not 49 times the witness at q={prime}")

    projection = multiply(order // 7, P, prime)
    require(projection == expected["projection_p"] and projection is not O,
            f"P does not generate the local 7-primary quotient at q={prime}")
    require(multiply(7, projection, prime) is O,
            f"stored projection is not 7-torsion at q={prime}")

    signature = (prime % 49, trace % 49, "Z/7", "[1:5]")
    print(
        f"q={prime}: #E={order}, a_q={trace}, "
        f"Sigma49_shadow={signature}, 49*{witness}=Q-5P"
    )
    return signature


def main():
    signatures = {q: verify_prime(q, data) for q, data in DATA.items()}
    require(signatures[1499][0] != signatures[29023][0],
            "cyclotomic determinants unexpectedly agree modulo 49")
    require(signatures[1499][1:] == signatures[29023][1:],
            "the expected common trace/local shadow does not agree")
    print("det(Frob_1499)=29 mod 49, det(Frob_29023)=15 mod 49")
    print("PASS Cycle 191: the primes are not conjugate already in Q(E[49])")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        raise SystemExit(f"FAIL Cycle 191: {error}") from error
