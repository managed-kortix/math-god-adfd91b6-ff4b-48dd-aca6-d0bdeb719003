#!/usr/bin/env python3
"""Dependency-free exact progression and local-row screen for Cycle 185."""

import argparse
import math


P = 7
ELL = 29
CONDUCTOR = 433
MODULUS = 8 * P * CONDUCTOR * ELL
ANCHOR = 1289
TARGET_ROW = (1, 1)
O = None


def is_prime(n):
    if n < 2:
        return False
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % prime == 0:
            return n == prime
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    # Deterministic for n < 2^64.
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % n == 0:
            continue
        x = pow(base, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def legendre(a, q):
    a %= q
    if a == 0:
        return 0
    value = pow(a, (q - 1) // 2, q)
    if value == q - 1:
        return -1
    assert value == 1
    return 1


def point_count(q):
    # The integral change X=4x, W=4(2y+x) identifies E mod q with
    # W^2=X^3+X^2+64. It is valid because every screened q is odd.
    character_sum = sum(legendre((x * x % q) * (x + 1) + 64, q)
                        for x in range(q))
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
    y3 = (-y1 + slope * (x1 - x3)) % q
    return x3, y3


def multiply(n, point, q):
    result = O
    addend = point
    while n:
        if n & 1:
            result = add(result, addend, q)
        addend = add(addend, addend, q)
        n >>= 1
    return result


def canonical_row(row):
    x, y = row
    if x == y == 0:
        return None
    if x:
        scale = pow(x, -1, P)
        return 1, y * scale % P
    return 0, 1


def local_row(q, order):
    if order % P or order % (P * P) == 0:
        return None
    cofactor = order // P
    p_image = multiply(cofactor, (0, 8), q)
    q_image = multiply(cofactor, (-4 % q, 4), q)
    if p_image is O:
        return canonical_row((0, 0 if q_image is O else 1))
    value = O
    for scalar in range(P):
        if value == q_image:
            return canonical_row((1, scalar))
        value = add(value, p_image, q)
    raise AssertionError("local quotient images do not lie in one order-7 line")


def admissible_twist_at_ell(q):
    d_sign = 1 if q % 4 == 1 else -1
    return legendre(d_sign * q, ELL) == 1


def screen(q):
    order = point_count(q)
    trace = q + 1 - order
    row = local_row(q, order)
    return order, trace, row


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=int, default=7,
                        help="number of progression terms k to inspect")
    parser.add_argument("--start", type=int, default=1,
                        help="first positive k in q=1289+k*703192")
    parser.add_argument("--prime-limit", type=int, default=1,
                        help="stop after this many prime terms are locally screened")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.start < 1 or args.terms < 1 or args.prime_limit < 1:
        raise ValueError("start, terms, and prime-limit must be positive")
    assert MODULUS == 703192
    assert math.gcd(ANCHOR, MODULUS) == 1
    assert is_prime(ANCHOR)
    anchor_order, anchor_trace, anchor_row = screen(ANCHOR)
    assert (anchor_order, anchor_trace, anchor_row) == (1330, -40, TARGET_ROW)

    print("modulus=", MODULUS, " residue=", ANCHOR, sep="")
    print("anchor q=1289 order=1330 trace=-40 row=(1,1)")
    screened = 0
    stop = args.start + args.terms
    for k in range(args.start, stop):
        q = ANCHOR + k * MODULUS
        if q >= 1 << 64:
            raise ValueError("deterministic primality range exceeded")
        if not is_prime(q):
            continue
        assert q % MODULUS == ANCHOR
        assert admissible_twist_at_ell(q) == admissible_twist_at_ell(ANCHOR)
        order, trace, row = screen(q)
        status = "MATCH" if trace % P == ANCHOR % P + 1 and row == TARGET_ROW else "reject"
        print(f"k={k} q={q} order={order} trace={trace} "
              f"trace_mod_7={trace % P} row={row} {status}")
        screened += 1
        if screened >= args.prime_limit:
            break
    if not screened:
        print("no prime progression terms screened")


if __name__ == "__main__":
    main()
