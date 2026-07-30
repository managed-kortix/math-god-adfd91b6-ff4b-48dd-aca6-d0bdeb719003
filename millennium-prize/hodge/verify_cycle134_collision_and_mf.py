#!/usr/bin/env python3
"""Cycle 134: collision containment and unrestricted Koszul MF lift gates.

This dependency-free verifier uses F_32 = F_2[t]/(t^5+t^2+1) and genuine
length-two Witt vectors in Teichmuller coordinates.  It checks the nonreduced
collision s(s+U)^2 in characteristic two and the unrestricted graded 4|4
Koszul matrix-factorization lifting obstruction for the Cycle 118 plane L_A.
"""

import math
import sys


MOD = 0b100101
MASK = 31
WZERO = (0, 0)
WONE = (1, 0)


def fail(message):
    print("FAIL: " + message, file=sys.stderr)
    raise SystemExit(1)


def check(condition, message):
    if not condition:
        fail(message)


def gf_mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 32:
            a ^= MOD
    return result & MASK


def gf_pow(a, n):
    result = 1
    while n:
        if n & 1:
            result = gf_mul(result, a)
        a = gf_mul(a, a)
        n //= 2
    return result


def gf_inv(a):
    if not a:
        fail("attempted inversion of zero in F_32")
    return gf_pow(a, 30)


def w_add(x, y):
    a, c = x
    b, d = y
    return a ^ b, c ^ d ^ gf_mul(a, b)


def w_mul(x, y):
    a, c = x
    b, d = y
    return (
        gf_mul(a, b),
        gf_mul(gf_mul(a, a), d) ^ gf_mul(gf_mul(b, b), c),
    )


def exp_add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def poly_add(left, right, add, zero):
    result = dict(left)
    for exponent, coefficient in right.items():
        value = add(result.get(exponent, zero), coefficient)
        if value == zero:
            result.pop(exponent, None)
        else:
            result[exponent] = value
    return result


def poly_scale(polynomial, scalar, mul, zero):
    result = {}
    for exponent, coefficient in polynomial.items():
        value = mul(coefficient, scalar)
        if value != zero:
            result[exponent] = value
    return result


def poly_mul(left, right, add, mul, zero):
    result = {}
    for left_exp, left_coefficient in left.items():
        for right_exp, right_coefficient in right.items():
            exponent = exp_add(left_exp, right_exp)
            value = add(
                result.get(exponent, zero),
                mul(left_coefficient, right_coefficient),
            )
            if value == zero:
                result.pop(exponent, None)
            else:
                result[exponent] = value
    return result


def poly_pow(polynomial, n, add, mul, zero, one, variables):
    result = {(0,) * variables: one}
    while n:
        if n & 1:
            result = poly_mul(result, polynomial, add, mul, zero)
        polynomial = poly_mul(polynomial, polynomial, add, mul, zero)
        n //= 2
    return result


def variable(index, coefficient, variables):
    return {
        tuple(1 if index == j else 0 for j in range(variables)): coefficient
    }


def matrix_vector_mul(matrix, vector):
    return tuple(
        gf_mul(row[0], vector[0])
        ^ gf_mul(row[1], vector[1])
        ^ gf_mul(row[2], vector[2])
        for row in matrix
    )


ALPHA_TERMS = (
    (18, 0, 17, 4, 0, 8, 0, 19),
    (18, 0, 1, 4, 16, 24, 0, 3),
    (18, 0, 16, 4, 1, 9, 0, 18),
    (18, 0, 0, 4, 17, 25, 0, 2),
    (2, 16, 17, 4, 0, 8, 16, 3),
    (2, 16, 1, 20, 0, 24, 0, 3),
    (2, 16, 16, 4, 1, 9, 16, 2),
    (2, 16, 0, 20, 1, 25, 0, 2),
    (16, 2, 17, 4, 0, 8, 2, 17),
    (16, 2, 1, 4, 16, 24, 2, 1),
    (16, 2, 16, 4, 1, 9, 2, 16),
    (16, 2, 0, 4, 17, 25, 2, 0),
    (0, 18, 17, 4, 0, 8, 18, 1),
    (0, 18, 1, 20, 0, 24, 2, 1),
    (0, 18, 16, 4, 1, 9, 18, 0),
    (0, 18, 0, 20, 1, 25, 2, 0),
)


def alpha_coefficient(matrix):
    values = (
        matrix[0][1], matrix[0][2], matrix[1][0], matrix[1][1],
        matrix[1][2], matrix[2][0], matrix[2][1], matrix[2][2],
    )
    result = 0
    for exponents in ALPHA_TERMS:
        term = 1
        for value, exponent in zip(values, exponents):
            term = gf_mul(term, gf_pow(value, exponent))
        result ^= term
    return result


def reduce_collision_cubic(polynomial, U):
    """Reduce modulo s(s+U)^2 = s^3+s*U^2 in characteristic two."""
    field_add = lambda a, b: a ^ b
    U_squared = poly_mul(U, U, field_add, gf_mul, 0)
    work = dict(polynomial)
    while True:
        candidates = [exponent for exponent in work if exponent[3] >= 3]
        if not candidates:
            return work
        exponent = max(candidates, key=lambda item: (item[3], item[:3]))
        coefficient = work.pop(exponent)
        quotient_exp = exponent[:3] + (exponent[3] - 3,)
        replacement = poly_mul(
            {quotient_exp[:3] + (quotient_exp[3] + 1,): coefficient},
            U_squared,
            field_add,
            gf_mul,
            0,
        )
        work = poly_add(work, replacement, field_add, 0)


def collision_section(A):
    field_add = lambda a, b: a ^ b
    z = (1, 0, 1)
    u = matrix_vector_mul(A, z)
    x = [variable(i, 1, 4) for i in range(4)]
    U = poly_add(x[0], x[2], field_add, 0)
    y = []
    for i in range(3):
        linear = {}
        for j in range(3):
            linear = poly_add(
                linear, poly_scale(x[j], A[i][j], gf_mul, 0), field_add, 0
            )
        y.append(
            poly_add(
                linear, poly_scale(x[3], u[i], gf_mul, 0), field_add, 0
            )
        )

    fermat = {}
    for linear in x[:3] + y:
        fermat = poly_add(
            fermat,
            poly_pow(linear, 33, field_add, gf_mul, 0, 1, 4),
            field_add,
            0,
        )
    remainder = reduce_collision_cubic(fermat, U)
    expected = {(32, 0, 0, 1): 1, (0, 0, 32, 1): 1}
    expected.update({(j, 0, 31 - j, 2): 1 for j in range(32)})
    check(remainder == expected, "collision remainder is not the stated 34 terms")
    check(len(remainder) == 34, "collision remainder support is not 34")
    check(remainder, "collision cubic unexpectedly contains the Fermat restriction")

    neighbor = tuple(
        tuple(
            A[i][j] ^ gf_mul(u[i], z[j]) for j in range(3)
        )
        for i in range(3)
    )
    alpha_A = alpha_coefficient(A)
    alpha_neighbor = alpha_coefficient(neighbor)
    check(alpha_A == 14, "P_alpha(A) changed")
    check(alpha_neighbor == 29, "P_alpha(B_z) changed")
    check(alpha_A != 0, "the collision fundamental cycle is alpha-invisible mod 2")

    print("[1] collision cubic containment")
    print("generator = s(s+U)^2 = s^3+s*U^2; U = x0+x2")
    print("remainder = s*U^32 + s^2*sum_{j=0}^{31} x0^j*x2^(31-j)")
    print("remainder support = 34 != 0; mod-2 containment fails")
    print("alpha coefficients P_A,P_Bz = 14,29; collision is alpha-visible")


def sparse_rank(columns, rows):
    row_index = {exponent: i for i, exponent in enumerate(rows)}
    pivots = {}
    for number, column in enumerate(columns):
        vector = dict(column)
        while vector:
            for exponent in vector:
                check(
                    exponent in row_index,
                    "column %d is outside the degree-33 target" % number,
                )
            pivot_exp = min(vector, key=row_index.__getitem__)
            pivot_row = row_index[pivot_exp]
            coefficient = vector[pivot_exp]
            if pivot_row not in pivots:
                pivots[pivot_row] = poly_scale(
                    vector, gf_inv(coefficient), gf_mul, 0
                )
                break
            vector = poly_add(
                vector,
                poly_scale(pivots[pivot_row], coefficient, gf_mul, 0),
                lambda a, b: a ^ b,
                0,
            )
    return len(pivots)


def check_koszul_4_by_4():
    """Check d^2=sum(l_i*g_i) on Lambda^* F_2^3, split 4|4."""
    even = [mask for mask in range(8) if mask.bit_count() % 2 == 0]
    odd = [mask for mask in range(8) if mask.bit_count() % 2 == 1]
    check(len(even) == len(odd) == 4, "Koszul parity ranks are not 4|4")
    images = {}
    for mask in range(8):
        image = {}
        for i in range(3):
            if mask & (1 << i):
                target = mask ^ (1 << i)
                image[target] = poly_add(
                    image.get(target, {}), variable(i + 3, 1, 6),
                    lambda a, b: a ^ b, 0,
                )
            else:
                target = mask | (1 << i)
                image[target] = poly_add(
                    image.get(target, {}), variable(i, 1, 6),
                    lambda a, b: a ^ b, 0,
                )
        images[mask] = image
    potential = {}
    for i in range(3):
        potential[(0,) * i + (1,) + (0,) * (2 - i)
                  + (0,) * i + (1,) + (0,) * (2 - i)] = 1
    for source in range(8):
        square = {}
        for middle, first_coefficient in images[source].items():
            for target, second_coefficient in images[middle].items():
                product = poly_mul(
                    first_coefficient, second_coefficient,
                    lambda a, b: a ^ b, gf_mul, 0,
                )
                square[target] = poly_add(
                    square.get(target, {}), product,
                    lambda a, b: a ^ b, 0,
                )
        square = {target: value for target, value in square.items() if value}
        check(square == {source: potential}, "Koszul differential does not square to F")


def mf_section(A):
    field_add = lambda a, b: a ^ b
    check_koszul_4_by_4()
    xg = [variable(i, 1, 3) for i in range(3)]
    xw = [variable(i, WONE, 3) for i in range(3)]
    yg = []
    yw = []
    for i in range(3):
        field_linear = {}
        witt_linear = {}
        for j in range(3):
            field_linear = poly_add(
                field_linear,
                poly_scale(xg[j], A[i][j], gf_mul, 0),
                field_add,
                0,
            )
            witt_linear = poly_add(
                witt_linear,
                poly_scale(xw[j], (A[i][j], 0), w_mul, WZERO),
                w_add,
                WZERO,
            )
        yg.append(field_linear)
        yw.append(witt_linear)

    field_fermat = {}
    witt_fermat = {}
    for linear in xg + yg:
        field_fermat = poly_add(
            field_fermat,
            poly_pow(linear, 33, field_add, gf_mul, 0, 1, 3),
            field_add,
            0,
        )
    for linear in xw + yw:
        witt_fermat = poly_add(
            witt_fermat,
            poly_pow(linear, 33, w_add, w_mul, WZERO, WONE, 3),
            w_add,
            WZERO,
        )
    check(not field_fermat, "L_A is not contained in the Fermat reduction")
    check(
        all(coefficient[0] == 0 for coefficient in witt_fermat.values()),
        "W2 Fermat restriction is nonzero modulo 2",
    )
    obstruction = {
        exponent: gf_pow(coefficient[1], 16)
        for exponent, coefficient in witt_fermat.items()
        if gf_pow(coefficient[1], 16)
    }

    columns = []
    for linear in yg:
        gradient = poly_pow(linear, 32, field_add, gf_mul, 0, 1, 3)
        for coordinate in xg:
            columns.append(poly_mul(gradient, coordinate, field_add, gf_mul, 0))
    target = [
        (a, b, 33 - a - b)
        for a in range(34)
        for b in range(34 - a)
    ]
    expected_middle = {
        (0, 16, 17): 25,
        (0, 17, 16): 25,
        (16, 0, 17): 7,
        (16, 1, 16): 22,
        (16, 16, 1): 16,
        (16, 17, 0): 24,
        (17, 0, 16): 17,
        (17, 16, 0): 8,
    }
    middle = {
        exponent: coefficient
        for exponent, coefficient in obstruction.items()
        if max(exponent) < 32
    }
    check(len(target) == math.comb(35, 2) == 595, "target dimension is not 595")
    check(len(columns) == 9, "contracted membership matrix does not have 9 columns")
    check(len(obstruction) == 17, "W2 obstruction support is not 17")
    check(middle == expected_middle, "middle-exponent obstruction terms changed")
    normal_rank = sparse_rank(columns, target)
    augmented_rank = sparse_rank(columns + [obstruction], target)
    check(normal_rank == 9, "contracted membership matrix rank is not 9")
    check(augmented_rank == 10, "augmented membership matrix rank is not 10")

    print("[2] unrestricted graded 4|4 Koszul MF W2 lift")
    print("Koszul differential: parity ranks 4|4 and d^2 = sum l_i*g_i")
    print("contraction: h in span{x_j*(A*x)_i^32 : 0<=i,j<=2}")
    print("membership matrix = 595 x 9; rank(M) = 9; rank(M | h) = 10")
    print("middle monomials (exponent: coefficient) =")
    for exponent in sorted(middle):
        print("  %s: %d" % (exponent, middle[exponent]))


def main():
    t = 2
    check(gf_pow(t, 5) ^ gf_pow(t, 2) ^ 1 == 0, "bad F_32 modulus")
    for value in range(1, 32):
        check(gf_mul(value, gf_inv(value)) == 1, "F_32 inverse check failed")
    A = (
        (0, t, t ^ 1),
        (t, gf_pow(t, 2) ^ 1, gf_pow(t, 2) ^ t),
        (t ^ 1, gf_pow(t, 2) ^ t, gf_pow(t, 2)),
    )
    collision_section(A)
    mf_section(A)
    print("all exact checks passed")


if __name__ == "__main__":
    main()
