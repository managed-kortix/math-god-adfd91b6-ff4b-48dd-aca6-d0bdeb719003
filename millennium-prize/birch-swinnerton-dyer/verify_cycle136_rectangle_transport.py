#!/usr/bin/env python3
"""Dependency-free exact checks for Cycle 136 rectangle transport."""

import sys


P = 7
INFINITY = None
GENERATORS = ((0, 1), (-1, 1))
SYMBOL_SUMS = (
    (13, -18, -14, 24, 9, -18, 8),
    (22, -1, -24, -4, 23, -13, -8),
    (4, 30, -16, -10, 12, 2, -24),
    (-9, 13, 11, -24, 11, 13, -9),
    (-24, 2, 12, -10, -16, 30, 4),
    (-8, -13, 23, -4, -24, -1, 22),
    (8, -18, 9, 24, -14, -18, 13),
)
LOCAL_DATA = (
    (29, 5, (1, 1)),
    (113, 4, (7, 32)),
)


class VerificationError(Exception):
    pass


def check(condition, message):
    if not condition:
        raise VerificationError(message)


def delta(matrix):
    return sum(
        i * j * matrix[i][j] for i in range(P) for j in range(P)
    ) % P


def rectangle_center(matrix):
    return tuple(
        tuple(
            (matrix[i][j] - matrix[i][0] - matrix[0][j] + matrix[0][0])
            % P
            for j in range(P)
        )
        for i in range(P)
    )


def transported_matrix(matrix, row_noise, column_noise, unit):
    return tuple(
        tuple(
            (unit * matrix[i][j] + row_noise[i] + column_noise[j]) % P
            for j in range(P)
        )
        for i in range(P)
    )


def verify_rectangle_transport():
    check(len(SYMBOL_SUMS) == P, "symbol matrix does not have seven rows")
    check(all(len(row) == P for row in SYMBOL_SUMS),
          "symbol matrix does not have seven columns")

    centered = rectangle_center(SYMBOL_SUMS)
    check(all(centered[0][j] == 0 for j in range(P)),
          "centered first row is nonzero")
    check(all(centered[i][0] == 0 for i in range(P)),
          "centered first column is nonzero")
    original_delta = delta(SYMBOL_SUMS)
    centered_delta = delta(centered)
    check(original_delta == 3, f"original delta is {original_delta}, expected 3")
    check(centered_delta == original_delta,
          f"rectangle centering changed delta to {centered_delta}")

    examples = (
        ((0, 1, 4, 2, 6, 3, 5), (3, 0, 6, 1, 5, 2, 4), 2),
        ((6, 2, 2, 5, 1, 0, 4), (1, 4, 0, 3, 3, 6, 2), 6),
    )
    for number, (row_noise, column_noise, unit) in enumerate(examples, 1):
        check(unit % P != 0, f"example {number} uses a zero scaling unit")
        check(len(set(row_noise)) > 1 and len(set(column_noise)) > 1,
              f"example {number} has trivial noise")
        transported = transported_matrix(
            SYMBOL_SUMS, row_noise, column_noise, unit
        )
        transported_delta = delta(transported)
        expected_delta = unit * original_delta % P
        check(transported_delta == expected_delta,
              f"example {number} delta is {transported_delta}, "
              f"expected {expected_delta}")
        expected_centered = tuple(
            tuple(unit * value % P for value in row) for row in centered
        )
        check(rectangle_center(transported) == expected_centered,
              f"example {number} rectangle quotient did not scale by {unit}")
    return original_delta, centered_delta, examples


def on_curve(point, prime):
    if point is INFINITY:
        return True
    x, y = point
    return (y * y + x * y - x * x * x - 1) % prime == 0


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
    check(on_curve(left, prime) and on_curve(right, prime),
          f"addition input is off E(F_{prime})")
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
        check(denominator != 0, "unhandled vertical tangent")
        inverse = pow(denominator, -1, prime)
        slope = (3 * x1 * x1 - y1) * inverse % prime
        intercept = (-x1 * x1 * x1 + 2) * inverse % prime

    x3 = (slope * slope + slope - x1 - x2) % prime
    result = x3, (-(slope + 1) * x3 - intercept) % prime
    check(on_curve(result, prime), f"addition output is off E(F_{prime})")
    return result


def scalar_multiply(multiplier, point, prime):
    if multiplier < 0:
        return scalar_multiply(-multiplier, point_neg(point, prime), prime)
    result = INFINITY
    addend = point
    while multiplier:
        if multiplier & 1:
            result = point_add(result, addend, prime)
        addend = point_add(addend, addend, prime)
        multiplier //= 2
    return result


def enumerate_points(prime):
    points = [INFINITY]
    for x in range(prime):
        for y in range(prime):
            point = (x, y)
            if on_curve(point, prime):
                points.append(point)
    return tuple(points)


def verify_localization():
    first, second = GENERATORS
    rows = []
    witnesses = []
    expected_counts = {29: 28, 113: 112}
    for prime, coefficient, witness in LOCAL_DATA:
        points = enumerate_points(prime)
        check(len(points) == expected_counts[prime],
              f"#E(F_{prime})={len(points)}, expected {expected_counts[prime]}")
        check(on_curve(first, prime) and on_curve(second, prime),
              f"rational generators do not reduce to E(F_{prime})")
        check(on_curve(witness, prime),
              f"stored divisibility witness is off E(F_{prime})")

        difference = point_add(
            second, scalar_multiply(-coefficient, first, prime), prime
        )
        check(difference != INFINITY,
              f"local relation at {prime} is exactly zero")
        check(scalar_multiply(P, witness, prime) == difference,
              f"7*witness != Q-{coefficient}P in E(F_{prime})")
        check(scalar_multiply(P, first, prime) == INFINITY
              if prime == 29 else scalar_multiply(P, first, prime) != INFINITY,
              f"unexpected 7-divisibility profile for P at {prime}")
        rows.append((1, coefficient % P))
        witnesses.append((prime, difference, witness))

    check(tuple(rows) == ((1, 5), (1, 4)),
          f"localization matrix is {rows}, expected [[1,5],[1,4]]")
    determinant = (rows[0][0] * rows[1][1]
                   - rows[0][1] * rows[1][0]) % P
    check(determinant == 6,
          f"localization determinant is {determinant}, expected 6")
    check(determinant != 0, "localization determinant vanishes")
    return tuple(rows), determinant, tuple(witnesses)


def main():
    try:
        original_delta, centered_delta, examples = verify_rectangle_transport()
        matrix, determinant, witnesses = verify_localization()
    except (ArithmeticError, VerificationError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print("PASS Cycle 136 rectangle transport and localization checks")
    print(f"rectangle delta: original={original_delta}, centered={centered_delta} mod 7")
    print("noise transport units: " + ", ".join(
        f"u={unit} -> delta={unit * original_delta % P}"
        for _, _, unit in examples
    ))
    print(f"localization matrix mod 7: {matrix}; determinant={determinant}")
    print("divisibility witnesses: " + ", ".join(
        f"ell={prime}: Q-cP={difference}=7*{witness}"
        for prime, difference, witness in witnesses
    ))
    print("scope: exact finite-field arithmetic; no external dependencies")
    return 0


if __name__ == "__main__":
    sys.exit(main())
