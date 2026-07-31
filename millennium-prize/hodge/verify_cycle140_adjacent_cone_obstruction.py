#!/usr/bin/env python3
"""Cycle 140: exact adjacent-cone obstruction from the Cycle 139 carry.

This dependency-free verifier works over F_32=F_2[t]/(t^5+t^2+1) and
W_2(F_32) in Teichmuller coordinates.  It reconstructs the actual transformed
Fermat carry, contracts the two component Koszul end complexes, and checks the
filtered lower-left transfer for every class in P^1(F_32).
"""

import hashlib
import sys


MOD = 0b100101
MASK = 31
NVARS = 6
ZERO_EXP = (0,) * NVARS
WZERO = (0, 0)
WONE = (1, 0)

EXPECTED_CARRY_SUPPORT = 76
EXPECTED_CARRY_SHA256 = "883504597c5e7284aa84d9742da8c651fc259d6f0abf088d6dca86a38633b69b"
EXPECTED_AGGREGATE_SHA256 = "0f01205954b0393a9136c4ba71b0cf45dc3cf471075951713b74f07857280b57"


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
    result = {}
    for exponent, coefficient in polynomial.items():
        value = neg(coefficient)
        if value != zero:
            result[exponent] = value
    return result


def poly_scale(polynomial, scalar):
    return {
        exponent: value
        for exponent, coefficient in polynomial.items()
        if (value := gf_mul(coefficient, scalar)) != 0
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


def variable(index, coefficient, nvars=NVARS):
    exponent = tuple(1 if index == j else 0 for j in range(nvars))
    return {exponent: coefficient} if coefficient else {}


def linear_polynomial(coefficients, witt=False):
    result = {}
    for index, coefficient in enumerate(coefficients):
        if coefficient:
            exponent = tuple(1 if index == j else 0 for j in range(NVARS))
            result[exponent] = (coefficient, 0) if witt else coefficient
    return result


def build_normal_form(t):
    beta = gf_pow(t, 4) ^ t ^ 1
    gamma = gf_pow(t, 4) ^ t
    a31 = {
        (0, 0, 31, 0, 0, 0): 1,
        (0, 0, 0, 31, 0, 0): 1,
    }
    b32 = {
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
    c32 = {
        (0, 0, 0, 0, 0, 32): 1,
        (1, 0, 0, 0, 0, 31): 1,
        (0, 0, 1, 0, 0, 31): t,
        (0, 0, 0, 1, 0, 31): t ^ 1,
        (32, 0, 0, 0, 0, 0): 1,
        (0, 0, 32, 0, 0, 0): t,
        (0, 0, 0, 32, 0, 0): t ^ 1,
    }
    return a31, b32, c32


def reconstruct_carry():
    t = 2
    gamma = gf_inv(t)
    beta = gf_mul(t ^ 1, gamma)
    inverse = (
        (1, 0, 0, 0, 0, 0),
        (0, 1, 0, 0, 0, 0),
        (gamma, beta, gamma, gamma, 0, 0),
        (beta, gamma, beta, beta, 1, 0),
        (1, 0, t ^ 1, t, 0, 0),
        (1, 0, t, t ^ 1, 0, 1),
    )
    field_add = lambda a, b: a ^ b

    transformed_fermat = {}
    lifted_fermat = {}
    for row in inverse:
        transformed_fermat = poly_add(
            transformed_fermat,
            poly_pow(linear_polynomial(row), 33, field_add, gf_mul, 0, 1),
            field_add,
            0,
        )
        lifted_fermat = poly_add(
            lifted_fermat,
            poly_pow(linear_polynomial(row, True), 33, w_add, w_mul, WZERO, WONE),
            w_add,
            WZERO,
        )

    a31, b32, c32 = build_normal_form(t)
    p = variable(2, 1)
    q = variable(3, 1)
    r = variable(4, 1)
    s = variable(5, 1)
    normal_form = poly_add(
        poly_mul(poly_mul(p, q, field_add, gf_mul, 0), a31, field_add, gf_mul, 0),
        poly_mul(r, b32, field_add, gf_mul, 0),
        field_add,
        0,
    )
    normal_form = poly_add(
        normal_form,
        poly_mul(s, c32, field_add, gf_mul, 0),
        field_add,
        0,
    )
    check(transformed_fermat == normal_form, "characteristic-two normal form failed")

    lifted_normal_form = {
        exponent: (coefficient, 0) for exponent, coefficient in normal_form.items()
    }
    carry = poly_add(
        lifted_fermat,
        poly_neg(lifted_normal_form, w_neg, WZERO),
        w_add,
        WZERO,
    )
    check(len(carry) == EXPECTED_CARRY_SUPPORT, "carry support is not 76")
    check(
        all(first == 0 and second != 0 for first, second in carry.values()),
        "carry is not pure and nonzero",
    )
    certificate = ";".join(
        "%s:%d" % (",".join(str(value) for value in exponent), coefficient[1])
        for exponent, coefficient in sorted(carry.items())
    ).encode("ascii")
    carry_digest = hashlib.sha256(certificate).hexdigest()
    check(carry_digest == EXPECTED_CARRY_SHA256, "Cycle 139 carry hash changed")

    divided_carry = {
        exponent: gf_pow(coefficient[1], 16)
        for exponent, coefficient in carry.items()
    }
    return divided_carry, carry_digest, (a31, b32, c32)


def restrict_to_plane(polynomial, zero_indices):
    keep = tuple(index for index in range(NVARS) if index not in zero_indices)
    return {
        tuple(exponent[index] for index in keep): coefficient
        for exponent, coefficient in polynomial.items()
        if not any(exponent[index] for index in zero_indices)
    }


def sparse_rank(columns):
    pivots = {}
    for column in columns:
        vector = dict(column)
        while vector:
            exponent = min(vector)
            coefficient = vector[exponent]
            if exponent not in pivots:
                pivots[exponent] = poly_scale(vector, gf_inv(coefficient))
                break
            vector = poly_add(
                vector,
                poly_scale(pivots[exponent], coefficient),
                lambda a, b: a ^ b,
                0,
            )
    return len(pivots)


def projective_normalize(left, right):
    check(left != 0 or right != 0, "zero pair has no projective class")
    if left:
        inverse = gf_inv(left)
        return 1, gf_mul(right, inverse)
    return 0, 1


def projective_classes():
    classes = tuple((1, value) for value in range(32)) + ((0, 1),)
    normalized = {
        projective_normalize(left, right)
        for left in range(32)
        for right in range(32)
        if left or right
    }
    check(len(classes) == 33, "P1(F_32) does not have 33 listed classes")
    check(normalized == set(classes), "projective normalization is incomplete")
    return classes


def component_data(label, zero_indices, free_name, carry, factors):
    field_add = lambda a, b: a ^ b
    a31, b32, c32 = factors
    p = variable(2, 1)
    q = variable(3, 1)
    first_partner = poly_mul(p if label == "L" else q, a31, field_add, gf_mul, 0)
    partners = (first_partner, b32, c32)
    restricted_carry = restrict_to_plane(carry, zero_indices)
    restricted_a = restrict_to_plane(a31, zero_indices)
    restricted_partners = tuple(
        restrict_to_plane(partner, zero_indices) for partner in partners
    )
    coordinates = tuple(variable(index, 1, 3) for index in range(3))
    boundaries = [
        poly_mul(partner, coordinate, field_add, gf_mul, 0)
        for partner in restricted_partners
        for coordinate in coordinates
    ]
    check(len(boundaries) == 9, label + " does not have nine boundary columns")
    check(sparse_rank(boundaries) == 9, label + " component boundary rank is not 9")
    check(
        sparse_rank(boundaries + [restricted_carry]) == 10,
        label + " carry lies in the component boundary space",
    )
    check(len(restricted_carry) == 16, label + " carry restriction support is not 16")

    functional_exp = (0, 16, 17)
    check(
        all(column.get(functional_exp, 0) == 0 for column in boundaries),
        label + " functional does not annihilate component boundaries",
    )
    check(
        restricted_carry.get(functional_exp, 0) == 13,
        label + " functional does not evaluate to 13 on the carry",
    )

    z0, z1, free_coordinate = coordinates
    check(free_name in ("p", "q"), "unexpected free-coordinate name")
    records = []
    for left, right in projective_classes():
        phi = poly_add(
            poly_scale(z0, left),
            poly_scale(z1, right),
            field_add,
            0,
        )
        a_phi = poly_mul(restricted_a, phi, field_add, gf_mul, 0)
        transfers = [
            poly_mul(a_phi, base, field_add, gf_mul, 0) for base in (z0, z1)
        ]
        check(
            all(column.get(functional_exp, 0) == 0 for column in transfers),
            label + " functional does not annihilate an extension transfer",
        )
        cone_columns = boundaries + transfers
        rank = sparse_rank(cone_columns)
        augmented_rank = sparse_rank(cone_columns + [restricted_carry])
        check(rank == 11, label + " cone boundary rank is not 11")
        check(augmented_rank == 12, label + " augmented cone rank is not 12")
        records.append(
            "%s:%d,%d:%d,%d:%d"
            % (
                label,
                left,
                right,
                rank,
                augmented_rank,
                restricted_carry[functional_exp],
            )
        )
    check(free_coordinate == variable(2, 1, 3), "free coordinate ordering changed")
    return records


def main():
    t = 2
    check(gf_pow(t, 5) ^ gf_pow(t, 2) ^ 1 == 0, "bad F_32 modulus")
    for value in range(1, 32):
        check(gf_mul(value, gf_inv(value)) == 1, "F_32 inversion failed")
    check(gf_inv(13) == 15, "functional normalization 13^-1 is not 15")

    carry, carry_digest, factors = reconstruct_carry()
    records = []
    records.extend(component_data("L", (3, 4, 5), "p", carry, factors))
    records.extend(component_data("M", (2, 4, 5), "q", carry, factors))
    check(len(records) == 66, "aggregate does not contain 2*33 records")
    aggregate = "\n".join(records).encode("ascii")
    aggregate_digest = hashlib.sha256(aggregate).hexdigest()
    check(
        aggregate_digest == EXPECTED_AGGREGATE_SHA256,
        "aggregate hash changed: got %s" % aggregate_digest,
    )

    print("Cycle 140 adjacent-cone obstruction")
    print("F_32 and W_2(F_32) arithmetic checked exactly")
    print("Cycle 139 carry support = 76")
    print("carry sha256 = %s" % carry_digest)
    print("planes L=(q,r,s), M=(p,r,s): component ranks 9 -> 10")
    print("P1(F_32): 33 normalized classes on each component")
    print("all filtered cone ranks = 11 -> 12")
    print("common functional [z1^16*p^17/q^17]: boundaries/transfers -> 0, carry -> 13")
    print("functional normalization: 13^-1 = 15")
    print("aggregate sha256 = %s" % aggregate_digest)
    print("all exact checks passed")


if __name__ == "__main__":
    main()
