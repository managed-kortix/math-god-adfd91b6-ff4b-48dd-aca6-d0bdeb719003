#!/usr/bin/env python3
"""Exact finite arithmetic for the D=-29023 localization target at 113."""

P = 113
IDENTITY = None
A1, A2, A3 = 1, 1, 1
A4, A6 = -17548636, -24475377572834
G = (85, 7)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def on_curve(point, modulus=P):
    if point is IDENTITY:
        return True
    x, y = point
    return (
        y * y + A1 * x * y + A3 * y
        - x * x * x - A2 * x * x - A4 * x - A6
    ) % modulus == 0


def add(left, right):
    if left is IDENTITY:
        return right
    if right is IDENTITY:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and (y1 + y2 + A1 * x1 + A3) % P == 0:
        return IDENTITY
    if left == right:
        denominator = (2 * y1 + A1 * x1 + A3) % P
        require(denominator, "unexpected vertical tangent")
        slope = (
            3 * x1 * x1 + 2 * A2 * x1 + A4 - A1 * y1
        ) * pow(denominator, -1, P) % P
        nu = (
            -x1 * x1 * x1 + A4 * x1 + 2 * A6 - A3 * y1
        ) * pow(denominator, -1, P) % P
    else:
        denominator = (x2 - x1) % P
        slope = (y2 - y1) * pow(denominator, -1, P) % P
        nu = (y1 * x2 - y2 * x1) * pow(denominator, -1, P) % P
    x3 = (slope * slope + A1 * slope - A2 - x1 - x2) % P
    y3 = (-(slope + A1) * x3 - nu - A3) % P
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


def point_count(modulus):
    return 1 + sum(
        1
        for x in range(modulus)
        for y in range(modulus)
        if on_curve((x, y), modulus)
    )


def main():
    require(point_count(7) == 5, "wrong point count at 7")
    require(point_count(P) == 112, "wrong point count at 113")
    require(on_curve(G), "G is not on the curve")
    require(multiply(112, G) is IDENTITY, "112G is nonzero")
    require(multiply(56, G) is not IDENTITY, "G has no factor 16 in its order")
    require(multiply(16, G) == (53, 42), "wrong order-seven detector")
    require(multiply(7, (53, 42)) is IDENTITY, "detector is not seven-torsion")

    print("Cycle 215 D=-29023 exact localization arithmetic")
    print("#A(F_7)=5; #A(F_113)=112; a_113=2")
    print("G=(85,7) has exact order 112")
    print("16G=(53,42) has exact order 7")
    print("dim_F7 A(F_113)/7A(F_113)=1")
    print("EXACT_ARITHMETIC_STATUS=PASS")


if __name__ == "__main__":
    main()
