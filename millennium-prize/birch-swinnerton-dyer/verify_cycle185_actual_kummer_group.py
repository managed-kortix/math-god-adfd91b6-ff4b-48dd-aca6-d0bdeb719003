#!/usr/bin/env python3
"""Dependency-free finite checks for the Cycle 185 Kummer-group audit."""

import itertools
import sys


P = 7
IDENTITY = (1, 0, 0, 1)
INFINITY = None
RATIONAL_POINTS = ((0, 1), (-1, 1))
LOCAL_DATA = ((29, 5, (1, 1)), (113, 4, (7, 32)))


class VerificationError(Exception):
    pass


def check(condition, message):
    if not condition:
        raise VerificationError(message)


def curve_invariants():
    a1, a2, a3, a4, a6 = 1, 0, 0, 0, 1
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = (a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4
          + a2 * a3 * a3 - a4 * a4)
    c4 = b2 * b2 - 24 * b4
    discriminant = (-b2 * b2 * b8 - 8 * b4**3 - 27 * b6**2
                    + 9 * b2 * b4 * b6)
    check((c4, discriminant) == (1, -433),
          f"unexpected invariants c4={c4}, Delta={discriminant}")
    return c4, discriminant


def on_curve(point, prime):
    if point is INFINITY:
        return True
    x, y = point
    return (y * y + x * y - x**3 - 1) % prime == 0


def point_neg(point, prime):
    if point is INFINITY:
        return INFINITY
    x, y = point
    return x % prime, (-y - x) % prime


def point_add(left, right, prime):
    if left is INFINITY:
        return right
    if right is INFINITY:
        return left
    if right == point_neg(left, prime):
        return INFINITY
    x1, y1 = left
    x2, y2 = right
    if x1 != x2:
        inverse = pow((x2 - x1) % prime, -1, prime)
        slope = (y2 - y1) * inverse % prime
        intercept = (y1 * x2 - y2 * x1) * inverse % prime
    else:
        denominator = (2 * y1 + x1) % prime
        check(denominator, "unhandled vertical tangent")
        inverse = pow(denominator, -1, prime)
        slope = (3 * x1 * x1 - y1) * inverse % prime
        intercept = (-x1**3 + 2) * inverse % prime
    x3 = (slope * slope + slope - x1 - x2) % prime
    result = x3, (-(slope + 1) * x3 - intercept) % prime
    check(on_curve(result, prime), "addition returned an off-curve point")
    return result


def multiply(multiplier, point, prime):
    if multiplier < 0:
        return multiply(-multiplier, point_neg(point, prime), prime)
    result = INFINITY
    addend = point
    while multiplier:
        if multiplier & 1:
            result = point_add(result, addend, prime)
        addend = point_add(addend, addend, prime)
        multiplier //= 2
    return result


def points(prime):
    return [INFINITY] + [
        (x, y) for x in range(prime) for y in range(prime)
        if on_curve((x, y), prime)
    ]


def point_order(point, prime, group_order):
    for divisor in range(1, group_order + 1):
        if group_order % divisor == 0 and multiply(divisor, point, prime) is INFINITY:
            return divisor
    raise VerificationError("point order did not divide the group order")


def mat_mul(left, right):
    a, b, c, d = left
    e, f, g, h = right
    return ((a * e + b * g) % P, (a * f + b * h) % P,
            (c * e + d * g) % P, (c * f + d * h) % P)


def determinant(matrix):
    return (matrix[0] * matrix[3] - matrix[1] * matrix[2]) % P


def mat_inverse(matrix):
    a, b, c, d = matrix
    inverse_det = pow(determinant(matrix), -1, P)
    return (d * inverse_det % P, -b * inverse_det % P,
            -c * inverse_det % P, a * inverse_det % P)


def generated_group(generators):
    generators = tuple(generators) + tuple(mat_inverse(g) for g in generators)
    seen = {IDENTITY}
    pending = [IDENTITY]
    while pending:
        current = pending.pop()
        for generator in generators:
            product = mat_mul(current, generator)
            if product not in seen:
                seen.add(product)
                pending.append(product)
    return seen


def verify_residual_image():
    count3 = len(points(3))
    trace3 = 3 + 1 - count3
    check((count3, trace3 % P, 3 % P) == (6, 5, 3),
          f"bad Frobenius data at 3: count={count3}, trace={trace3}")
    check((trace3 * trace3 - 4 * 3) % P == 6,
          "Frobenius discriminant at 3 is not 6")
    check(6 not in {x * x % P for x in range(P)}, "6 is a square mod 7")

    transvection = (1, 1, 0, 1)
    candidates = []
    generated_orders = set()
    for matrix in itertools.product(range(P), repeat=4):
        if determinant(matrix) == 3 and (matrix[0] + matrix[3]) % P == 5:
            candidates.append(matrix)
            generated_orders.add(len(generated_group((transvection, matrix))))
    gl_order = (P**2 - 1) * (P**2 - P)
    check(len(candidates) == 42, f"found {len(candidates)} Frobenius matrices")
    check(generated_orders == {gl_order},
          f"possible generated subgroup orders are {generated_orders}")
    return count3, trace3, len(candidates), gl_order


def verify_kummer_points():
    first, second = RATIONAL_POINTS
    rows = []
    orders = []
    for prime, coefficient, witness in LOCAL_DATA:
        group_order = len(points(prime))
        check(group_order == prime - 1,
              f"#E(F_{prime})={group_order}, expected {prime - 1}")
        order = point_order(first, prime, group_order)
        expected_order = 7 if prime == 29 else 112
        check(order == expected_order,
              f"P has order {order} at {prime}, expected {expected_order}")
        difference = point_add(second, multiply(-coefficient, first, prime), prime)
        check(multiply(P, witness, prime) == difference,
              f"stored divisibility witness failed at {prime}")
        rows.append((1, coefficient))
        orders.append(order)
    det = (rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]) % P
    check(det == 6, f"localization determinant is {det}, expected 6")
    return tuple(rows), tuple(orders), det


def main():
    try:
        c4, discriminant = curve_invariants()
        count3, trace3, candidate_count, gl_order = verify_residual_image()
        rows, orders, localization_det = verify_kummer_points()
    except (ArithmeticError, VerificationError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    full_order = P**4 * gl_order
    print("PASS Cycle 185 actual Kummer-group finite checks")
    print(f"curve invariants: c4={c4}, Delta={discriminant}, v_433(Delta)=1")
    middle_sign = "+" if trace3 < 0 else "-"
    print(f"F_3: #E={count3}, a_3={trace3}, "
          f"charpoly=X^2{middle_sign}{abs(trace3)}X+3")
    print(f"residual generation: {candidate_count} compatible matrices; "
          f"all generate GL(2,7) of order {gl_order} with a transvection")
    print(f"local rows={rows}, orders(P)={orders}, determinant={localization_det}")
    print(f"certified Galois-group order: 7^4*{gl_order}={full_order}")
    print("scope: finite arithmetic; the accompanying proof supplies inertia, Sah, "
          "and Kummer-theory implications")
    return 0


if __name__ == "__main__":
    sys.exit(main())
