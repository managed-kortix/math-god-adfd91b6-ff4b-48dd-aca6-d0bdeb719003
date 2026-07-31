#!/usr/bin/env python3
"""Exact small-prime L0 Frobenius-class search for Cycle 187."""

import argparse
import math
from collections import defaultdict


P = 7
ELL = 29
CONDUCTOR = 433
O = None


def prime_sieve(limit):
    sieve = bytearray(b"\x01") * limit
    if limit:
        sieve[0] = 0
    if limit > 1:
        sieve[1] = 0
    for n in range(2, math.isqrt(limit - 1) + 1):
        if sieve[n]:
            start = n * n
            sieve[start:limit:n] = b"\x00" * (((limit - 1 - start) // n) + 1)
    return sieve


def legendre(a, prime):
    a %= prime
    if not a:
        return 0
    value = pow(a, (prime - 1) // 2, prime)
    return -1 if value == prime - 1 else value


def fundamental_discriminant(q):
    return q if q % 4 == 1 else -q


def twist_root_number(q):
    # E=433a1 has root number +1, and w(E^D)=w(E)*(D/-433).
    d = fundamental_discriminant(q)
    return (1 if d > 0 else -1) * legendre(d, CONDUCTOR)


def point_count(q):
    # E is identified over F_q with W^2=X^3+X^2+64.
    squares = bytearray(q)
    for y in range(1, (q + 1) // 2):
        squares[y * y % q] = 1
    character_sum = 0
    for x in range(q):
        value = ((x * x % q) * (x + 1) + 64) % q
        if value:
            character_sum += 1 if squares[value] else -1
    return q + 1 + character_sum


def inverse(a, q):
    return pow(a % q, -1, q)


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
        slope = (3 * x1 * x1 + 2 * x1) * inverse(2 * y1, q) % q
    else:
        slope = (y2 - y1) * inverse(x2 - x1, q) % q
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


def canonical_row(row):
    x, y = row
    if x == y == 0:
        return "zero"
    if x:
        return (1, y * pow(x, -1, P) % P)
    return (0, 1)


def projective_localization_row(q, order):
    cofactor = order // P
    p_image = multiply(cofactor, (0, 8), q)
    q_image = multiply(cofactor, (-4 % q, 4), q)
    if p_image is O:
        return canonical_row((0, 0 if q_image is O else 1))
    multiple = O
    for scalar in range(P):
        if multiple == q_image:
            return canonical_row((1, scalar))
        multiple = add(multiple, p_image, q)
    raise AssertionError("local images do not span one order-seven line")


def valuation_7(n):
    value = 0
    while n % P == 0:
        value += 1
        n //= P
    return value


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=int, default=200_000)
    return parser.parse_args()


def main():
    args = parse_args()
    if not 3 <= args.bound <= 200_000:
        raise ValueError("bound must lie between 3 and 200000")

    primes = prime_sieve(args.bound)
    classes = defaultdict(list)
    aux_admissible = 0
    sign_admissible = 0
    packet_members = 0

    for q in range(3, args.bound):
        if not primes[q] or q in (P, ELL, CONDUCTOR):
            continue
        if legendre(q, ELL) != 1:
            continue
        aux_admissible += 1
        if twist_root_number(q) != -1:
            continue
        sign_admissible += 1
        if q % P != 1:
            continue

        order = point_count(q)
        trace = q + 1 - order
        if trace % P != 2 or valuation_7(order) != 1:
            continue

        # q=1 and trace=2 mod 7, together with v_7(#E(F_q))=1,
        # certifies the nonidentity-unipotent GL2(F_7) class.
        row = projective_localization_row(q, order)
        class_label = ("unipotent(1)", row)
        classes[class_label].append((q, trace, order))
        packet_members += 1

    repeated = [(label, members) for label, members in classes.items()
                if len(members) >= 2]
    repeated.sort(key=lambda item: (str(item[0][1]), item[1][0][0]))

    print("Cycle 187 exact small-prime Frobenius search")
    print(f"range: 3 <= q < {args.bound}")
    print("packet: (q/29)=1, w(E^Dq)=-1, q=1 mod 7, "
          "a_q=2 mod 7, v_7(#E(F_q))=1")
    print(f"counts: auxiliary={aux_admissible} sign={sign_admissible} "
          f"local_packet={packet_members} classes={len(classes)} "
          f"repeated_classes={len(repeated)}")
    for label, members in repeated:
        data = " ".join(f"{q}[a={trace},N={order}]" for q, trace, order in members)
        print(f"class GL2={label[0]} row={label[1]} count={len(members)}: {data}")
    print("all arithmetic exact; repeated rows are L0 conjugacy classes under Cycle 185 maximality")


if __name__ == "__main__":
    main()
