#!/usr/bin/env python3
"""Cycle 132: exact W2 obstruction for a canonical hyperbolic triple.

This dependency-free verifier works over

    F_32 = F_2[t] / (t^5 + t^2 + 1)

and W_2(F_32), represented in Teichmuller coordinates (a,c)=[a]+2[c].
For z=(1,0,1) and w=(0,1,1), it verifies the complete normal map and
the divided degree-33 Fermat obstruction of L_A union L_Bz union L_Bw.
"""

import sys


MOD = 0b100101
MASK = 31
GZERO = 0
WZERO = (0, 0)
WONE = (1, 0)
ZERO_EXP = (0, 0, 0, 0, 0)


def fail(message):
    print("FAIL: " + message, file=sys.stderr)
    raise SystemExit(1)


def check(condition, message):
    if not condition:
        fail(message)


# F_32 arithmetic; elements are five-bit polynomial representatives.
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


def dot(left, right):
    result = 0
    for a, b in zip(left, right):
        result ^= gf_mul(a, b)
    return result


# Genuine length-two Witt arithmetic in Teichmuller coordinates.
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


# Sparse polynomial arithmetic in (x0,x1,x2,s,r).
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
    for e, a in left.items():
        for f, b in right.items():
            exponent = exp_add(e, f)
            value = add(result.get(exponent, zero), mul(a, b))
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
    exponent = tuple(1 if i == index else 0 for i in range(5))
    return {exponent: coefficient}


def quotient_basis(degree):
    """Normal monomials modulo s(s+U), sr, and r(r+V)."""
    result = []
    for a in range(degree + 1):
        for b in range(degree - a + 1):
            result.append((a, b, degree - a - b, 0, 0))
    for final_index in (3, 4):
        for a in range(degree):
            for b in range(degree - a):
                exponent = [a, b, degree - 1 - a - b, 0, 0]
                exponent[final_index] = 1
                result.append(tuple(exponent))
    return result


def reduce_union(polynomial, U, V, add, mul, zero, one):
    """Reduce by s^2=U*s, s*r=0, and r^2=V*r."""
    max_s = max((e[3] for e in polynomial), default=0)
    max_r = max((e[4] for e in polynomial), default=0)
    powers_u = [{ZERO_EXP: one}]
    powers_v = [{ZERO_EXP: one}]
    for _ in range(max_s):
        powers_u.append(poly_mul(powers_u[-1], U, add, mul, zero))
    for _ in range(max_r):
        powers_v.append(poly_mul(powers_v[-1], V, add, mul, zero))

    result = {}
    for exponent, coefficient in polynomial.items():
        s_degree, r_degree = exponent[3], exponent[4]
        if s_degree and r_degree:
            continue
        if s_degree <= 1 and r_degree <= 1:
            contribution = {exponent: coefficient}
        elif s_degree:
            base = (exponent[0], exponent[1], exponent[2], 1, 0)
            contribution = {
                exp_add(base, e): mul(coefficient, c)
                for e, c in powers_u[s_degree - 1].items()
            }
        else:
            base = (exponent[0], exponent[1], exponent[2], 0, 1)
            contribution = {
                exp_add(base, e): mul(coefficient, c)
                for e, c in powers_v[r_degree - 1].items()
            }
        result = poly_add(result, contribution, add, zero)
    return result


def divide_by_union_ideal(F, U, V):
    """Express a field polynomial exactly as q1*Q1+q2*Q2+q3*Q3."""
    work = dict(F)
    quotients = [{}, {}, {}]
    field_add = lambda a, b: a ^ b

    while work:
        exponent = max(
            work,
            key=lambda e: (e[3] + e[4], e[3], e[4], e[:3]),
        )
        coefficient = work[exponent]
        s_degree, r_degree = exponent[3], exponent[4]

        if s_degree and r_degree:
            generator = 1
            q_exp = (
                exponent[0], exponent[1], exponent[2],
                s_degree - 1, r_degree - 1,
            )
            extra = None
        elif s_degree >= 2:
            generator = 0
            q_exp = (
                exponent[0], exponent[1], exponent[2],
                s_degree - 2, r_degree,
            )
            extra = (U, variable(3, 1))
        elif r_degree >= 2:
            generator = 2
            q_exp = (
                exponent[0], exponent[1], exponent[2],
                s_degree, r_degree - 2,
            )
            extra = (V, variable(4, 1))
        else:
            fail("Fermat restriction has a nonzero union-quotient remainder")

        work = poly_add(work, {exponent: coefficient}, field_add, 0)
        quotients[generator] = poly_add(
            quotients[generator], {q_exp: coefficient}, field_add, 0
        )
        if extra is not None:
            linear, final_variable = extra
            extra_term = poly_mul(
                {q_exp: coefficient},
                poly_mul(linear, final_variable, field_add, gf_mul, 0),
                field_add,
                gf_mul,
                0,
            )
            work = poly_add(work, extra_term, field_add, 0)
    return quotients


def matrix_vector_mul(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def matrix_is_orthogonal(matrix):
    for i in range(3):
        for j in range(3):
            column_i = tuple(matrix[k][i] for k in range(3))
            column_j = tuple(matrix[k][j] for k in range(3))
            if dot(column_i, column_j) != (1 if i == j else 0):
                return False
    return True


def neighbor_matrix(A, direction):
    image = matrix_vector_mul(A, direction)
    return tuple(
        tuple(A[i][j] ^ gf_mul(image[i], direction[j]) for j in range(3))
        for i in range(3)
    )


def dense_rank_and_kernel(columns, row_count):
    """Return field rank, pivot columns, and a basis of the right kernel."""
    column_count = len(columns)
    matrix = [
        [columns[j].get(i, 0) for j in range(column_count)]
        for i in range(row_count)
    ]
    pivots = []
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (i for i in range(pivot_row, row_count) if matrix[i][column]),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
        inverse = gf_inv(matrix[pivot_row][column])
        matrix[pivot_row] = [gf_mul(value, inverse) for value in matrix[pivot_row]]
        for i in range(row_count):
            if i != pivot_row and matrix[i][column]:
                scalar = matrix[i][column]
                matrix[i] = [
                    a ^ gf_mul(scalar, b)
                    for a, b in zip(matrix[i], matrix[pivot_row])
                ]
        pivots.append(column)
        pivot_row += 1

    free_columns = [i for i in range(column_count) if i not in pivots]
    kernel = []
    for free in free_columns:
        vector = [0] * column_count
        vector[free] = 1
        for i, pivot in enumerate(pivots):
            vector[pivot] = matrix[i][free]
        kernel.append(vector)
    return len(pivots), pivots, kernel


def sparse_row_reduce(columns, rows):
    row_index = {exponent: i for i, exponent in enumerate(rows)}
    pivots = {}
    for number, column in enumerate(columns):
        vector = dict(column)
        while vector:
            for exponent in vector:
                if exponent not in row_index:
                    fail("column %d is outside the target quotient basis" % number)
            pivot_exponent = min(vector, key=row_index.__getitem__)
            pivot_row = row_index[pivot_exponent]
            coefficient = vector[pivot_exponent]
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


# The Cycle 118 alpha-coordinate polynomial has these sixteen Lucas terms.
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
    w = (0, 1, 1)
    check(dot(z, z) == 0 and dot(w, w) == 0, "z or w is not isotropic")
    check(dot(z, w) == 1, "z,w are not a hyperbolic pair")
    check(matrix_is_orthogonal(A), "A is not orthogonal")

    u = matrix_vector_mul(A, z)
    v = matrix_vector_mul(A, w)
    Bz = neighbor_matrix(A, z)
    Bw = neighbor_matrix(A, w)
    expected_u = (t ^ 1, gf_pow(t, 2), gf_pow(t, 2) ^ t ^ 1)
    expected_v = (1, t ^ 1, t)
    expected_Bz = ((3, 2, 0), (6, 5, 2), (4, 6, 3))
    expected_Bw = ((0, 3, 2), (2, 6, 5), (3, 4, 6))
    check(u == expected_u and v == expected_v, "incorrect spanning vectors")
    check(Bz == expected_Bz and Bw == expected_Bw, "incorrect neighbor matrices")
    check(matrix_is_orthogonal(Bz), "Bz is not orthogonal")
    check(matrix_is_orthogonal(Bw), "Bw is not orthogonal")

    field_add = lambda a, b: a ^ b
    xg = [variable(i, 1) for i in range(5)]
    xw = [variable(i, WONE) for i in range(5)]
    U = poly_add(xg[0], xg[2], field_add, 0)
    V = poly_add(xg[1], xg[2], field_add, 0)
    Uw = poly_add(xw[0], xw[2], w_add, WZERO)
    Vw = poly_add(xw[1], xw[2], w_add, WZERO)
    s = xg[3]
    r = xg[4]

    q1 = poly_mul(s, poly_add(s, U, field_add, 0), field_add, gf_mul, 0)
    q2 = poly_mul(s, r, field_add, gf_mul, 0)
    q3 = poly_mul(r, poly_add(r, V, field_add, 0), field_add, gf_mul, 0)
    for q in (q1, q2, q3):
        check(
            not reduce_union(q, U, V, field_add, gf_mul, 0, 1),
            "a union-ideal generator does not reduce to zero",
        )
    check([len(quotient_basis(d)) for d in (1, 2, 3, 33)] == [5, 12, 22, 1717],
          "incorrect union quotient Hilbert function")

    yg = []
    yw = []
    for i in range(3):
        field_linear = {}
        witt_linear = {}
        for j in range(3):
            field_linear = poly_add(
                field_linear, poly_scale(xg[j], A[i][j], gf_mul, 0),
                field_add, 0,
            )
            witt_linear = poly_add(
                witt_linear,
                poly_scale(xw[j], w_neg((A[i][j], 0)), w_mul, WZERO),
                w_add,
                WZERO,
            )
        field_linear = poly_add(
            field_linear, poly_scale(xg[3], u[i], gf_mul, 0), field_add, 0
        )
        field_linear = poly_add(
            field_linear, poly_scale(xg[4], v[i], gf_mul, 0), field_add, 0
        )
        witt_linear = poly_add(
            witt_linear, poly_scale(xw[3], (u[i], 0), w_mul, WZERO),
            w_add, WZERO,
        )
        witt_linear = poly_add(
            witt_linear, poly_scale(xw[4], (v[i], 0), w_mul, WZERO),
            w_add, WZERO,
        )
        yg.append(field_linear)
        yw.append(witt_linear)

    Fg = {}
    Fw = {}
    for i in range(3):
        Fg = poly_add(
            Fg, poly_pow(xg[i], 33, field_add, gf_mul, 0, 1), field_add, 0
        )
        Fg = poly_add(
            Fg, poly_pow(yg[i], 33, field_add, gf_mul, 0, 1), field_add, 0
        )
        Fw = poly_add(
            Fw, poly_pow(xw[i], 33, w_add, w_mul, WZERO, WONE),
            w_add, WZERO,
        )
        Fw = poly_add(
            Fw, poly_pow(yw[i], 33, w_add, w_mul, WZERO, WONE),
            w_add, WZERO,
        )

    reduced_witt = reduce_union(Fw, Uw, Vw, w_add, w_mul, WZERO, WONE)
    check(all(c[0] == 0 for c in reduced_witt.values()),
          "W2 Fermat restriction is nonzero modulo 2")
    obstruction = {}
    for exponent, coefficient in reduced_witt.items():
        value = gf_pow(coefficient[1], 16)
        if value:
            obstruction[exponent] = value
    check(len(obstruction) == 215, "unexpected obstruction support")

    raw_quotients = divide_by_union_ideal(Fg, U, V)
    quotients = [
        reduce_union(q, U, V, field_add, gf_mul, 0, 1)
        for q in raw_quotients
    ]
    check([len(q) for q in quotients] == [32, 32, 32],
          "unexpected Fermat quotient supports")

    # Hilbert-Burch relations:
    # r*q1+(s+U)*q2=0 and (r+V)*q2+s*q3=0.
    source = quotient_basis(2)
    relation_rows = [(i, e) for i in range(2) for e in quotient_basis(3)]
    relation_index = {item: i for i, item in enumerate(relation_rows)}
    relation_columns = []
    s_plus_u = poly_add(s, U, field_add, 0)
    r_plus_v = poly_add(r, V, field_add, 0)
    for component in range(3):
        for exponent in source:
            multiplier = {exponent: 1}
            outputs = [{}, {}]
            if component == 0:
                outputs[0] = reduce_union(
                    poly_mul(r, multiplier, field_add, gf_mul, 0),
                    U, V, field_add, gf_mul, 0, 1,
                )
            elif component == 1:
                outputs[0] = reduce_union(
                    poly_mul(s_plus_u, multiplier, field_add, gf_mul, 0),
                    U, V, field_add, gf_mul, 0, 1,
                )
                outputs[1] = reduce_union(
                    poly_mul(r_plus_v, multiplier, field_add, gf_mul, 0),
                    U, V, field_add, gf_mul, 0, 1,
                )
            else:
                outputs[1] = reduce_union(
                    poly_mul(s, multiplier, field_add, gf_mul, 0),
                    U, V, field_add, gf_mul, 0, 1,
                )
            relation_columns.append({
                relation_index[(equation, e)]: c
                for equation in range(2)
                for e, c in outputs[equation].items()
            })

    syzygy_rank, syzygy_pivots, normal_kernel = dense_rank_and_kernel(
        relation_columns, len(relation_rows)
    )
    expected_syzygy_pivots = [
        0, 1, 2, 3, 4, 5, 12, 13, 14,
        15, 16, 17, 18, 19, 20, 24, 27, 29,
    ]
    check(len(relation_rows) == 44 and len(relation_columns) == 36,
          "incorrect normal syzygy matrix dimensions")
    check(syzygy_rank == 18 and len(normal_kernel) == 18,
          "normal syzygy matrix does not have rank 18 and nullity 18")
    check(syzygy_pivots == expected_syzygy_pivots,
          "normal syzygy pivot certificate changed")

    # Rows 1 and 2 of [u v] form an invertible minor, so the remaining
    # ambient normal equation has Fermat gradient y0^32.
    minor = gf_mul(u[1], v[2]) ^ gf_mul(u[2], v[1])
    check(minor != 0, "selected spanning minor is singular")
    gradient = reduce_union(
        poly_pow(yg[0], 32, field_add, gf_mul, 0, 1),
        U, V, field_add, gf_mul, 0, 1,
    )

    def product_reduced(left, right):
        return reduce_union(
            poly_mul(left, right, field_add, gf_mul, 0),
            U, V, field_add, gf_mul, 0, 1,
        )

    normal_columns = [
        product_reduced(gradient, {exponent: 1})
        for exponent in quotient_basis(1)
    ]
    for kernel_vector in normal_kernel:
        column = {}
        for index, coefficient in enumerate(kernel_vector):
            if coefficient:
                component = index // len(source)
                exponent = source[index % len(source)]
                term = product_reduced(quotients[component], {exponent: 1})
                column = poly_add(
                    column, poly_scale(term, coefficient, gf_mul, 0),
                    field_add, 0,
                )
        normal_columns.append(column)

    target = quotient_basis(33)
    normal_pivots = sparse_row_reduce(normal_columns, target)
    augmented_pivots = sparse_row_reduce(normal_columns + [obstruction], target)
    new_pivots = sorted(set(augmented_pivots) - set(normal_pivots))
    expected_pivot = (0, 16, 17, 0, 0)
    check(len(normal_columns) == 23, "normal map does not have 23 columns")
    check(len(normal_pivots) == 23, "normal map does not have rank 23")
    check(len(augmented_pivots) == 24, "augmented map does not have rank 24")
    check(new_pivots == [target.index(expected_pivot)],
          "augmented pivot is not x1^16*x2^17")

    alpha_A = alpha_coefficient(A)
    alpha_Bz = alpha_coefficient(Bz)
    alpha_Bw = alpha_coefficient(Bw)
    alpha_union = alpha_A ^ alpha_Bz ^ alpha_Bw
    check(alpha_A == 14 and alpha_Bz == 29 and alpha_Bw == 15,
          "component alpha coefficients changed")
    check(alpha_union == 28, "triple is not alpha-visible")

    print("Cycle 132 canonical hyperbolic triple obstruction")
    print("F_32 modulus = t^5+t^2+1; all 31 inverses checked")
    print("z = (1,0,1), w = (0,1,1): z.z = w.w = 0, z.w = 1")
    print("u = (3,4,7), v = (1,3,2)")
    print("A = ((0,2,3),(2,5,6),(3,6,4))")
    print("Bz = ((3,2,0),(6,5,2),(4,6,3))")
    print("Bw = ((0,3,2),(2,6,5),(3,4,6))")
    print("union ideal = (s(s+x0+x2), s*r, r(r+x1+x2))")
    print("quotient dimensions d=1,2,3,33: 5,12,22,1717")
    print("normal syzygy matrix = 44 x 36; rank = 18; nullity = 18")
    print("W2 obstruction support = 215")
    print("normal matrix = 1717 x 23; rank(M) = 23")
    print("rank(M | h) = 24; new pivot = x1^16*x2^17")
    print("alpha coefficients A,Bz,Bw = 14,29,15; union = 28 != 0")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
