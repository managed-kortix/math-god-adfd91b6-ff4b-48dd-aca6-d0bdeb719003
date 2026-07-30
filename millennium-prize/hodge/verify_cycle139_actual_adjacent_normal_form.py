#!/usr/bin/env python3
"""Cycle 139: actual adjacent-pair normal form and genuine W2 carry audit.

This dependency-free verifier works over F_32 = F_2[t]/(t^5+t^2+1)
and W_2(F_32) in Teichmuller coordinates.  It uses the Cycle 122 matrix A
and z=(1,t+1,t), verifies the explicit six-variable coordinate change and
the sparse characteristic-two normal form, then compares its coefficientwise
Teichmuller lift with the standard Fermat polynomial transformed using the
Teichmuller-lifted inverse linear forms.
"""

import hashlib
import sys


MOD = 0b100101
MASK = 31
NVARS = 6
ZERO_EXP = (0,) * NVARS
WZERO = (0, 0)
WONE = (1, 0)

# Filled by the exact audit below and pinned to make the carry certificate
# reproducible rather than merely checking that some discrepancy exists.
EXPECTED_CARRY_SUPPORT = 76
EXPECTED_CARRY_SHA256 = "883504597c5e7284aa84d9742da8c651fc259d6f0abf088d6dca86a38633b69b"


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
    check(a != 0, "attempted inversion of zero in F_32")
    return gf_pow(a, 30)


def w_add(left, right):
    a, c = left
    b, d = right
    return a ^ b, c ^ d ^ gf_mul(a, b)


def w_neg(value):
    a, c = value
    return a, c ^ gf_mul(a, a)


def w_mul(left, right):
    a, c = left
    b, d = right
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


def poly_neg(polynomial, neg, zero):
    return {
        exponent: value
        for exponent, coefficient in polynomial.items()
        if (value := neg(coefficient)) != zero
    }


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


def monomial(exponent, coefficient):
    return {exponent: coefficient} if coefficient else {}


def variable(index, coefficient):
    exponent = [0] * NVARS
    exponent[index] = 1
    return monomial(tuple(exponent), coefficient)


def linear_polynomial(coefficients, one):
    result = {}
    for index, coefficient in enumerate(coefficients):
        if coefficient:
            result[tuple(1 if index == j else 0 for j in range(NVARS))] = (
                coefficient if one == 1 else (coefficient, 0)
            )
    return result


def matrix_mul(left, right):
    return [
        [
            _field_sum(gf_mul(left[i][k], right[k][j]) for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def matrix_vector_mul(matrix, vector):
    return tuple(
        _field_sum(gf_mul(coefficient, value) for coefficient, value in zip(row, vector))
        for row in matrix
    )


def _field_sum(values):
    result = 0
    for value in values:
        result ^= value
    return result


def determinant(matrix):
    work = [list(row) for row in matrix]
    result = 1
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            return 0
        work[column], work[pivot] = work[pivot], work[column]
        value = work[column][column]
        result = gf_mul(result, value)
        inverse = gf_inv(value)
        work[column] = [gf_mul(inverse, entry) for entry in work[column]]
        for row in range(column + 1, len(work)):
            value = work[row][column]
            if value:
                work[row] = [
                    entry ^ gf_mul(value, pivot_entry)
                    for entry, pivot_entry in zip(work[row], work[column])
                ]
    return result


def substitute_linear(form, parametrization):
    return tuple(
        _field_sum(gf_mul(form[i], parametrization[i][j]) for i in range(6))
        for j in range(3)
    )


def build_sparse_normal_form(t):
    beta = gf_pow(t, 4) ^ t ^ 1
    gamma = gf_pow(t, 4) ^ t

    A31 = {
        (0, 0, 31, 0, 0, 0): 1,
        (0, 0, 0, 31, 0, 0): 1,
    }
    B32 = {
        (0, 0, 0, 0, 32, 0): 1,
        (1, 0, 0, 0, 31, 0): beta,
        (0, 1, 0, 0, 31, 0): gamma,
        (0, 0, 1, 0, 31, 0): beta,
        (0, 0, 0, 1, 31, 0): beta,
        (32, 0, 0, 0, 0, 0): beta,
        (0, 32, 0, 0, 0, 0): gamma,
        (0, 0, 32, 0, 0, 0): beta,
        (0, 0, 0, 32, 0, 0): beta,
    }
    C32 = {
        (0, 0, 0, 0, 0, 32): 1,
        (1, 0, 0, 0, 0, 31): 1,
        (0, 0, 1, 0, 0, 31): t,
        (0, 0, 0, 1, 0, 31): t ^ 1,
        (32, 0, 0, 0, 0, 0): 1,
        (0, 0, 32, 0, 0, 0): t,
        (0, 0, 0, 32, 0, 0): t ^ 1,
    }
    return A31, B32, C32


def main():
    t = 2
    t2 = gf_mul(t, t)
    gamma = gf_inv(t)
    beta = gf_mul(t ^ 1, gamma)
    check(gamma == gf_pow(t, 4) ^ t, "t inverse formula changed")
    check(beta == gf_pow(t, 4) ^ t ^ 1, "beta formula changed")

    A = (
        (0, t, t ^ 1),
        (t, t2 ^ 1, t2 ^ t),
        (t ^ 1, t2 ^ t, t2),
    )
    z = (1, t ^ 1, t)
    u = matrix_vector_mul(A, z)
    check(u == (0, 1, 1), "Az is not (0,1,1)")
    B = tuple(
        tuple(A[i][j] ^ gf_mul(u[i], z[j]) for j in range(3))
        for i in range(3)
    )

    # Rows map old coordinates (x0,x1,x2,y0,y1,y2) to
    # new coordinates (z0,z1,p,q,r,s).
    transform = (
        (1, 0, 0, 0, 0, 0),
        (0, 1, 0, 0, 0, 0),
        (t ^ 1, t2 ^ t, t2, 0, 1, 0),
        (t, t2 ^ 1, t2 ^ t, 0, 1, 0),
        (0, t, t ^ 1, 1, 0, 0),
        (1, t ^ 1, t, 0, 1, 1),
    )
    inverse = (
        (1, 0, 0, 0, 0, 0),
        (0, 1, 0, 0, 0, 0),
        (gamma, beta, gamma, gamma, 0, 0),
        (beta, gamma, beta, beta, 1, 0),
        (1, 0, t ^ 1, t, 0, 0),
        (1, 0, t, t ^ 1, 0, 1),
    )
    identity = [[1 if i == j else 0 for j in range(6)] for i in range(6)]
    check(determinant(transform) == t, "coordinate-transform determinant is not t")
    check(matrix_mul(transform, inverse) == identity, "T*T^-1 is not identity")
    check(matrix_mul(inverse, transform) == identity, "T^-1*T is not identity")

    # Parametrizations have rows indexed by old x,y coordinates and columns x0,x1,x2.
    plane_A = tuple(identity[:3]) + A
    plane_B = tuple(identity[:3]) + B
    pulled_A = tuple(substitute_linear(row, plane_A) for row in transform)
    pulled_B = tuple(substitute_linear(row, plane_B) for row in transform)
    check(pulled_A[2] == z, "p restricted to L_A is not z^T*x")
    check(pulled_A[3:] == ((0, 0, 0),) * 3, "L_A is not (q,r,s)")
    check(pulled_B[3] == z, "q restricted to L_B is not z^T*x")
    check(
        (pulled_B[2], pulled_B[4], pulled_B[5]) == ((0, 0, 0),) * 3,
        "L_B is not (p,r,s)",
    )

    field_add = lambda a, b: a ^ b
    old_forms = [linear_polynomial(row, 1) for row in inverse]
    fermat = {}
    for form in old_forms:
        fermat = poly_add(
            fermat, poly_pow(form, 33, field_add, gf_mul, 0, 1), field_add, 0
        )

    A31, B32, C32 = build_sparse_normal_form(t)
    p = variable(2, 1)
    q = variable(3, 1)
    r = variable(4, 1)
    s = variable(5, 1)
    normal_form = poly_add(
        poly_mul(poly_mul(p, q, field_add, gf_mul, 0), A31, field_add, gf_mul, 0),
        poly_mul(r, B32, field_add, gf_mul, 0),
        field_add,
        0,
    )
    normal_form = poly_add(
        normal_form, poly_mul(s, C32, field_add, gf_mul, 0), field_add, 0
    )
    check(len(A31) == 2, "A31 support is not 2")
    check(len(B32) == 9, "B32 support is not 9")
    check(len(C32) == 7, "C32 support is not 7")
    check(len(normal_form) == 18, "normal-form support is not 18")
    check(fermat == normal_form, "standard Fermat identity in characteristic two failed")

    # Lift the already-expanded characteristic-two decomposition coefficientwise.
    lifted_normal_form = {
        exponent: (coefficient, 0) for exponent, coefficient in normal_form.items()
    }
    lifted_fermat = {}
    for row in inverse:
        form = linear_polynomial(row, WONE)
        lifted_fermat = poly_add(
            lifted_fermat,
            poly_pow(form, 33, w_add, w_mul, WZERO, WONE),
            w_add,
            WZERO,
        )
    carry = poly_add(
        lifted_fermat,
        poly_neg(lifted_normal_form, w_neg, WZERO),
        w_add,
        WZERO,
    )
    check(carry, "W2 carry discrepancy unexpectedly vanished")
    check(
        all(coefficient[0] == 0 and coefficient[1] != 0 for coefficient in carry.values()),
        "W2 discrepancy is not a nonzero pure carry polynomial",
    )
    certificate = ";".join(
        "%s:%d" % (",".join(str(value) for value in exponent), coefficient[1])
        for exponent, coefficient in sorted(carry.items())
    ).encode("ascii")
    digest = hashlib.sha256(certificate).hexdigest()
    check(
        len(carry) == EXPECTED_CARRY_SUPPORT,
        "W2 carry support changed: got %d, expected %d"
        % (len(carry), EXPECTED_CARRY_SUPPORT),
    )
    check(
        digest == EXPECTED_CARRY_SHA256,
        "W2 carry SHA256 changed: got %s, expected %s"
        % (digest, EXPECTED_CARRY_SHA256),
    )

    print("Cycle 139 actual adjacent normal form")
    print("A*z = (0,1,1); B = A*(I+z*z^T)")
    print("det(T) = t; explicit inverse verified on both sides")
    print("L_A = (q,r,s); L_B = (p,r,s)")
    print("supports A31,B32,C32,F = 2,9,7,18")
    print("A31 = p^31+q^31")
    print(
        "B32 = r^32+beta*(z0+p+q)*r^31+gamma*z1*r^31"
        "+beta*(z0^32+p^32+q^32)+gamma*z1^32"
    )
    print(
        "C32 = s^32+(z0+t*p+(t+1)*q)*s^31"
        "+z0^32+t*p^32+(t+1)*q^32"
    )
    print("beta = t^4+t+1; gamma = t^4+t")
    print("F = p*q*A31+r*B32+s*C32 exactly over F_32")
    print("W2 coefficientwise lift differs from lifted-inverse Fermat")
    print("nonzero carry support = %d" % len(carry))
    print("carry sha256 = %s" % digest)
    print("all exact checks passed")


if __name__ == "__main__":
    main()
