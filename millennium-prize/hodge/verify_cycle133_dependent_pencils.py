#!/usr/bin/env python3
"""Cycle 133: exact W2 obstruction for all dependent-pencil triples.

This dependency-free verifier works over F_32 = F_2[t]/(t^5+t^2+1)
and genuine length-two Witt vectors in Teichmuller coordinates.  It checks all
30 cross-ratios lambda != 0,1, including the full 1684-by-27 normal maps.
"""

import hashlib
import json
import sys


MOD = 0b100101
MASK = 31
WZERO = (0, 0)
WONE = (1, 0)
ZERO_EXP = (0, 0, 0, 0)
EXPECTED_AGGREGATE_SHA256 = (
    "81903632919c44c3164507ec8ecb2c3af7cc0459b3fe7bf23ef9c7d12e196525"
)
EXPECTED_CLASSES = [
    [2, 3, 18, 19, 28, 29],
    [4, 5, 8, 9, 22, 23],
    [6, 7, 12, 13, 14, 15],
    [10, 11, 16, 17, 24, 25],
    [20, 21, 26, 27, 30, 31],
]


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


def w_neg(x):
    a, c = x
    return a, c ^ gf_mul(a, a)


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


def poly_pow(polynomial, n, add, mul, zero, one):
    result = {ZERO_EXP: one}
    while n:
        if n & 1:
            result = poly_mul(result, polynomial, add, mul, zero)
        polynomial = poly_mul(polynomial, polynomial, add, mul, zero)
        n //= 2
    return result


def variable(index, coefficient):
    return {tuple(1 if index == j else 0 for j in range(4)): coefficient}


def homogeneous_basis(degree):
    result = []
    for a in range(degree + 1):
        for b in range(degree - a + 1):
            for c in range(degree - a - b + 1):
                result.append((a, b, c, degree - a - b - c))
    return result


def quotient_basis(degree):
    return [exponent for exponent in homogeneous_basis(degree) if exponent[3] <= 2]


def reduce_cubic(polynomial, U, mu, add, mul, zero, one):
    linear_coefficient = poly_scale(U, add(mu, one), mul, zero)
    quadratic_coefficient = poly_scale(
        poly_mul(U, U, add, mul, zero), mu, mul, zero
    )
    work = dict(polynomial)
    while True:
        candidates = [exponent for exponent in work if exponent[3] >= 3]
        if not candidates:
            return work
        exponent = max(candidates, key=lambda item: (item[3], item[:3]))
        coefficient = work.pop(exponent)
        quotient_exp = (
            exponent[0], exponent[1], exponent[2], exponent[3] - 3
        )
        leading = {quotient_exp: coefficient}
        first = poly_mul(
            leading,
            poly_mul(
                linear_coefficient, {(0, 0, 0, 2): one}, add, mul, zero
            ),
            add,
            mul,
            zero,
        )
        second = poly_mul(
            leading,
            poly_mul(
                quadratic_coefficient, {(0, 0, 0, 1): one}, add, mul, zero
            ),
            add,
            mul,
            zero,
        )
        work = poly_add(work, first, add, zero)
        work = poly_add(work, second, add, zero)


def divide_by_cubic(F, U, mu):
    field_add = lambda a, b: a ^ b
    linear_coefficient = poly_scale(U, mu ^ 1, gf_mul, 0)
    quadratic_coefficient = poly_scale(
        poly_mul(U, U, field_add, gf_mul, 0), mu, gf_mul, 0
    )
    generator = {(0, 0, 0, 3): 1}
    generator = poly_add(
        generator,
        poly_mul(
            linear_coefficient,
            {(0, 0, 0, 2): 1},
            field_add,
            gf_mul,
            0,
        ),
        field_add,
        0,
    )
    generator = poly_add(
        generator,
        poly_mul(
            quadratic_coefficient,
            {(0, 0, 0, 1): 1},
            field_add,
            gf_mul,
            0,
        ),
        field_add,
        0,
    )
    work = dict(F)
    quotient = {}
    while work:
        exponent = max(work, key=lambda item: (item[3], item[:3]))
        coefficient = work[exponent]
        check(exponent[3] >= 3, "Fermat restriction has nonzero cubic remainder")
        quotient_exp = (
            exponent[0], exponent[1], exponent[2], exponent[3] - 3
        )
        quotient = poly_add(
            quotient, {quotient_exp: coefficient}, field_add, 0
        )
        multiple = poly_scale(
            poly_mul(
                {quotient_exp: 1}, generator, field_add, gf_mul, 0
            ),
            coefficient,
            gf_mul,
            0,
        )
        work = poly_add(work, multiple, field_add, 0)
    return quotient


def sparse_row_reduce(columns, rows):
    row_index = {exponent: i for i, exponent in enumerate(rows)}
    pivots = {}
    for number, column in enumerate(columns):
        vector = dict(column)
        while vector:
            for exponent in vector:
                check(
                    exponent in row_index,
                    "normal column %d is outside the quotient basis" % number,
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
    return pivots


def matrix_vector_mul(matrix, vector):
    return tuple(
        gf_mul(row[0], vector[0])
        ^ gf_mul(row[1], vector[1])
        ^ gf_mul(row[2], vector[2])
        for row in matrix
    )


def matrix_is_orthogonal(matrix):
    for i in range(3):
        for j in range(3):
            value = 0
            for k in range(3):
                value ^= gf_mul(matrix[k][i], matrix[k][j])
            if value != (1 if i == j else 0):
                return False
    return True


def neighbor_matrix(A, direction):
    image = matrix_vector_mul(A, direction)
    return tuple(
        tuple(
            A[i][j] ^ gf_mul(image[i], direction[j])
            for j in range(3)
        )
        for i in range(3)
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


def encode_polynomial(polynomial):
    return [[list(exponent), polynomial[exponent]] for exponent in sorted(polynomial)]


def compute_lambda(lam, A, z, target):
    field_add = lambda a, b: a ^ b
    mu = gf_mul(lam, lam)
    u = matrix_vector_mul(A, z)
    B = neighbor_matrix(A, z)
    scaled_z = tuple(gf_mul(lam, value) for value in z)
    B_lambda = neighbor_matrix(A, scaled_z)
    check(matrix_is_orthogonal(B), "first neighbor is not orthogonal")
    check(matrix_is_orthogonal(B_lambda), "lambda neighbor is not orthogonal")

    xg = [variable(i, 1) for i in range(4)]
    xw = [variable(i, WONE) for i in range(4)]
    U = poly_add(xg[0], xg[2], field_add, 0)
    Uw = poly_add(xw[0], xw[2], w_add, WZERO)
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
                poly_scale(xw[j], w_neg((A[i][j], 0)), w_mul, WZERO),
                w_add,
                WZERO,
            )
        yg.append(
            poly_add(
                field_linear,
                poly_scale(xg[3], u[i], gf_mul, 0),
                field_add,
                0,
            )
        )
        yw.append(
            poly_add(
                witt_linear,
                poly_scale(xw[3], (u[i], 0), w_mul, WZERO),
                w_add,
                WZERO,
            )
        )

    field_fermat = {}
    witt_fermat = {}
    for i in range(3):
        field_fermat = poly_add(
            field_fermat,
            poly_pow(xg[i], 33, field_add, gf_mul, 0, 1),
            field_add,
            0,
        )
        field_fermat = poly_add(
            field_fermat,
            poly_pow(yg[i], 33, field_add, gf_mul, 0, 1),
            field_add,
            0,
        )
        witt_fermat = poly_add(
            witt_fermat,
            poly_pow(xw[i], 33, w_add, w_mul, WZERO, WONE),
            w_add,
            WZERO,
        )
        witt_fermat = poly_add(
            witt_fermat,
            poly_pow(yw[i], 33, w_add, w_mul, WZERO, WONE),
            w_add,
            WZERO,
        )

    reduced_witt = reduce_cubic(
        witt_fermat, Uw, (mu, 0), w_add, w_mul, WZERO, WONE
    )
    check(
        all(coefficient[0] == 0 for coefficient in reduced_witt.values()),
        "W2 Fermat restriction is nonzero modulo 2 for lambda=%d" % lam,
    )
    obstruction = {}
    for exponent, coefficient in reduced_witt.items():
        value = gf_pow(coefficient[1], 16)
        if value:
            obstruction[exponent] = value

    quotient = reduce_cubic(
        divide_by_cubic(field_fermat, U, mu),
        U,
        mu,
        field_add,
        gf_mul,
        0,
        1,
    )
    pivot_coordinate = next((i for i, value in enumerate(u) if value), None)
    check(pivot_coordinate is not None, "the spanning direction vanished")
    gradients = [
        reduce_cubic(
            poly_pow(yg[i], 32, field_add, gf_mul, 0, 1),
            U,
            mu,
            field_add,
            gf_mul,
            0,
            1,
        )
        for i in range(3)
        if i != pivot_coordinate
    ]

    columns = []
    for gradient in gradients:
        for exponent in quotient_basis(1):
            columns.append(
                reduce_cubic(
                    poly_mul(
                        gradient, {exponent: 1}, field_add, gf_mul, 0
                    ),
                    U,
                    mu,
                    field_add,
                    gf_mul,
                    0,
                    1,
                )
            )
    for exponent in quotient_basis(3):
        columns.append(
            reduce_cubic(
                poly_mul(quotient, {exponent: 1}, field_add, gf_mul, 0),
                U,
                mu,
                field_add,
                gf_mul,
                0,
                1,
            )
        )
    check(len(target) == 1684, "degree-33 quotient dimension is not 1684")
    check(len(columns) == 27, "normal map does not have 27 columns")
    normal = sparse_row_reduce(columns, target)
    augmented = sparse_row_reduce(columns + [obstruction], target)
    check(len(normal) == 27, "normal map rank is not 27 for lambda=%d" % lam)
    check(
        len(augmented) == 28,
        "augmented map rank is not 28 for lambda=%d" % lam,
    )

    component_alpha = [
        alpha_coefficient(A), alpha_coefficient(B), alpha_coefficient(B_lambda)
    ]
    alpha = component_alpha[0] ^ component_alpha[1] ^ component_alpha[2]
    record = {
        "lambda": lam,
        "mu": mu,
        "alpha": alpha,
        "component_alpha": component_alpha,
        "h_support": len(obstruction),
        "columns": len(columns),
        "target_dim": len(target),
        "normal_rank": len(normal),
        "augmented_rank": len(augmented),
        "normal_pivots": sorted(normal),
        "new_pivots": sorted(set(augmented) - set(normal)),
    }
    payload = {
        "record": record,
        "h": encode_polynomial(obstruction),
        "normal_reduced": [
            [row, encode_polynomial(normal[row])] for row in sorted(normal)
        ],
    }
    record["certificate_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return record


def anharmonic_class(value):
    return {
        value,
        value ^ 1,
        gf_inv(value),
        gf_inv(value) ^ 1,
        gf_inv(value ^ 1),
        gf_mul(value, gf_inv(value ^ 1)),
    }


def enumerate_classes():
    unseen = set(range(2, 32))
    classes = []
    while unseen:
        representative = min(unseen)
        orbit = sorted(anharmonic_class(representative))
        classes.append(orbit)
        unseen -= set(orbit)
    return classes


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
    z = (1, 0, 1)
    check(matrix_is_orthogonal(A), "Cycle 118 matrix A is not orthogonal")
    check(gf_mul(z[0], z[0]) ^ gf_mul(z[2], z[2]) == 0, "z is not isotropic")
    target = quotient_basis(33)
    records = [compute_lambda(lam, A, z, target) for lam in range(2, 32)]
    classes = enumerate_classes()
    check(classes == EXPECTED_CLASSES, "cross-ratio classes or representatives changed")
    check([orbit[0] for orbit in classes] == [2, 4, 6, 10, 20],
          "class representatives changed")
    alpha_zeros = {record["lambda"] for record in records if record["alpha"] == 0}
    check(alpha_zeros == {9, 24}, "alpha zero set is not exactly {9,24}")
    check(all(record["normal_rank"] == 27 for record in records),
          "normal rank is not uniformly 27")
    check(all(record["augmented_rank"] == 28 for record in records),
          "augmented rank is not uniformly 28")
    summary = {"orbits": classes, "records": records}
    aggregate = hashlib.sha256(
        json.dumps(summary, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    check(aggregate == EXPECTED_AGGREGATE_SHA256,
          "aggregate certificate SHA256 changed: " + aggregate)

    print("Cycle 133 dependent-pencil triple obstruction")
    print("F_32 modulus = t^5+t^2+1; all 31 inverses checked")
    print("lambda values = 30; unordered classes = 5; representatives = 2,4,6,10,20")
    print("normal matrices = 1684 x 27; rank(M) = 27 for all lambda")
    print("rank(M | h) = 28 for all lambda")
    print("alpha zeros = {9,24}")
    print("aggregate SHA256 = " + aggregate)
    print("all exact checks passed")


if __name__ == "__main__":
    main()
