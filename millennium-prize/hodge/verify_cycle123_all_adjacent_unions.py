#!/usr/bin/env python3
"""Cycle 123: exhaustive W2 obstruction for all 1023 adjacent planes.

Dependency-free exact computation over

    F_32 = F_2[t] / (t^5 + t^2 + 1)

and its length-two Witt ring W_2(F_32).

For every nonzero isotropic vector z=(a,b,a+b), this verifier constructs

    u = A z,
    B = A(I + z z^T),

the complete reducible union L_A union L_B in its spanning P^3, its full
1156-by-17 embedded normal map, and its divided W2 Fermat obstruction h.

The deterministic certificate stream consists of records

    a,b,a^b:rank(M),rank(M|h)

ordered by a=0,...,31 and then b=0,...,31, omitting (a,b)=(0,0).
"""

import hashlib
import sys
import time


MOD = 0b100101
MASK = 31
ZERO_EXP = (0, 0, 0, 0)
WZERO = (0, 0)
WONE = (1, 0)

EXPECTED_COUNT = 1023
EXPECTED_RANK = 17
EXPECTED_AUGMENTED_RANK = 18
EXPECTED_SHA256 = (
    "c893f4112547e53d50f762167923aa67e17008f7c24cb11bfdaa0f179e9633fe"
)


def fail(message):
    print("FAIL: " + message, file=sys.stderr)
    raise SystemExit(1)


# F_32 arithmetic. Elements are encoded as five-bit integers.
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
    if a == 0:
        fail("attempted inversion of zero in F_32")
    return gf_pow(a, 30)


# W_2(F_32) arithmetic in Teichmuller coordinates (a,c)=[a]+2[c].
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


def exp_add(e, f):
    return tuple(a + b for a, b in zip(e, f))


# Sparse polynomial arithmetic.
def poly_add(p, q, add, zero):
    result = dict(p)
    for exponent, coefficient in q.items():
        value = add(result.get(exponent, zero), coefficient)
        if value == zero:
            result.pop(exponent, None)
        else:
            result[exponent] = value
    return result


def poly_scale(p, scalar, mul, zero):
    result = {}
    for exponent, coefficient in p.items():
        value = mul(coefficient, scalar)
        if value != zero:
            result[exponent] = value
    return result


def poly_mul(p, q, add, mul, zero):
    result = {}
    for e, a in p.items():
        for f, b in q.items():
            exponent = exp_add(e, f)
            value = add(result.get(exponent, zero), mul(a, b))
            if value == zero:
                result.pop(exponent, None)
            else:
                result[exponent] = value
    return result


def poly_pow(p, n, add, mul, zero, one):
    result = {ZERO_EXP: one}
    while n:
        if n & 1:
            result = poly_mul(result, p, add, mul, zero)
        p = poly_mul(p, p, add, mul, zero)
        n //= 2
    return result


def reduce_quad(p, U, add, mul, zero, one):
    """Reduce modulo s^2-U*s, retaining only s-degrees zero and one."""
    max_s_degree = max((e[3] for e in p), default=0)
    powers = [{ZERO_EXP: one}]
    for _ in range(max_s_degree):
        powers.append(poly_mul(powers[-1], U, add, mul, zero))

    result = {}
    for exponent, coefficient in p.items():
        n = exponent[3]
        if n <= 1:
            result = poly_add(
                result, {exponent: coefficient}, add, zero
            )
            continue

        base = (exponent[0], exponent[1], exponent[2], 1)
        contribution = {}
        for power_exponent, power_coefficient in powers[n - 1].items():
            out_exponent = exp_add(base, power_exponent)
            out_coefficient = mul(coefficient, power_coefficient)
            if out_coefficient != zero:
                contribution[out_exponent] = out_coefficient
        result = poly_add(result, contribution, add, zero)

    return result


def divide_by_quad_exact(F, U):
    """Divide an F_32 polynomial exactly by q=s^2-U*s."""
    work = dict(F)
    quotient = {}

    while work:
        max_s_degree = max(e[3] for e in work)
        if max_s_degree < 2:
            break

        leading = [
            (e, c)
            for e, c in work.items()
            if e[3] == max_s_degree
        ]
        for exponent, coefficient in leading:
            work = poly_add(
                work, {exponent: coefficient}, lambda a, b: a ^ b, 0
            )

            q_exponent = (
                exponent[0],
                exponent[1],
                exponent[2],
                max_s_degree - 2,
            )
            quotient = poly_add(
                quotient,
                {q_exponent: coefficient},
                lambda a, b: a ^ b,
                0,
            )

            us_term = poly_mul(
                {
                    (
                        exponent[0],
                        exponent[1],
                        exponent[2],
                        max_s_degree - 1,
                    ): coefficient
                },
                U,
                lambda a, b: a ^ b,
                gf_mul,
                0,
            )
            work = poly_add(work, us_term, lambda a, b: a ^ b, 0)

    if work:
        fail("mod-2 Fermat restriction was not exactly divisible by the quadric")
    return quotient


def section_basis(degree):
    """Basis of H^0(O_Z(degree)) in the quotient by s^2-U*s."""
    result = []

    for a in range(degree + 1):
        for b in range(degree - a + 1):
            result.append((a, b, degree - a - b, 0))

    for a in range(degree):
        for b in range(degree - a):
            result.append((a, b, degree - 1 - a - b, 1))

    return result


def normal_columns(polynomial, multiplier_degree, U):
    """Columns obtained by multiplying by a basis of the requested degree."""
    columns = []
    for exponent in section_basis(multiplier_degree):
        product = poly_mul(
            polynomial,
            {exponent: 1},
            lambda a, b: a ^ b,
            gf_mul,
            0,
        )
        columns.append(
            reduce_quad(
                product,
                U,
                lambda a, b: a ^ b,
                gf_mul,
                0,
                1,
            )
        )
    return columns


def row_reduce(columns, rows):
    """Return normalized sparse pivots for the supplied columns."""
    row_index = {exponent: i for i, exponent in enumerate(rows)}
    pivots = {}

    for column_number, column in enumerate(columns):
        vector = dict(column)

        while vector:
            for exponent in vector:
                if exponent not in row_index:
                    fail(
                        "column %d contains an exponent outside the target basis"
                        % column_number
                    )

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

    return row_index, pivots


def lies_in_span(vector, reduction):
    row_index, pivots = reduction
    work = dict(vector)

    while work:
        for exponent in work:
            if exponent not in row_index:
                fail("obstruction contains an exponent outside the target basis")

        pivot_exponent = min(work, key=row_index.__getitem__)
        pivot_row = row_index[pivot_exponent]
        coefficient = work[pivot_exponent]

        if pivot_row not in pivots:
            return False

        work = poly_add(
            work,
            poly_scale(pivots[pivot_row], coefficient, gf_mul, 0),
            lambda a, b: a ^ b,
            0,
        )

    return True


def matrix_is_orthogonal(matrix):
    for i in range(3):
        for j in range(3):
            value = 0
            for k in range(3):
                value ^= gf_mul(matrix[k][i], matrix[k][j])
            expected = 1 if i == j else 0
            if value != expected:
                return False
    return True


def make_variable(index, coefficient):
    exponent = tuple(1 if j == index else 0 for j in range(4))
    return {exponent: coefficient}


def main():
    start = time.monotonic()

    t = 2
    if gf_pow(t, 5) ^ gf_pow(t, 2) ^ 1:
        fail("the selected element t does not satisfy t^5+t^2+1=0")

    A = (
        (0, t, t ^ 1),
        (t, gf_pow(t, 2) ^ 1, gf_pow(t, 2) ^ t),
        (t ^ 1, gf_pow(t, 2) ^ t, gf_pow(t, 2)),
    )
    if not matrix_is_orthogonal(A):
        fail("Cycle 118 matrix A is not orthogonal")

    xg = [make_variable(i, 1) for i in range(4)]
    xw = [make_variable(i, WONE) for i in range(4)]

    xg_33 = [
        poly_pow(xg[i], 33, lambda a, b: a ^ b, gf_mul, 0, 1)
        for i in range(3)
    ]
    xw_33 = [
        poly_pow(xw[i], 33, w_add, w_mul, WZERO, WONE)
        for i in range(3)
    ]

    target_rows = section_basis(33)
    if len(target_rows) != 1156:
        fail("degree-33 quotient basis does not have dimension 1156")

    certificate_records = []
    rank17_count = 0
    rank18_count = 0
    processed = 0

    for a in range(32):
        for b in range(32):
            z = (a, b, a ^ b)
            if z == (0, 0, 0):
                continue

            processed += 1

            norm_z = 0
            for value in z:
                norm_z ^= gf_mul(value, value)
            if norm_z != 0:
                fail("z=%r is not isotropic" % (z,))

            u = tuple(
                gf_mul(A[i][0], z[0])
                ^ gf_mul(A[i][1], z[1])
                ^ gf_mul(A[i][2], z[2])
                for i in range(3)
            )
            if u == (0, 0, 0):
                fail("u=A*z vanished for z=%r" % (z,))

            B = tuple(
                tuple(
                    A[i][j] ^ gf_mul(u[i], z[j])
                    for j in range(3)
                )
                for i in range(3)
            )
            if not matrix_is_orthogonal(B):
                fail("neighbor B is not orthogonal for z=%r" % (z,))

            # U=z^T*x and the lifted quadric relation s^2=U*s.
            Ug = {}
            Uw = {}
            for i in range(3):
                Ug = poly_add(
                    Ug,
                    poly_scale(xg[i], z[i], gf_mul, 0),
                    lambda x, y: x ^ y,
                    0,
                )
                Uw = poly_add(
                    Uw,
                    poly_scale(xw[i], (z[i], 0), w_mul, WZERO),
                    w_add,
                    WZERO,
                )

            # The spanning P^3 is y=A*x+u*s modulo 2. Over W2 the lifted
            # x-coefficients use -[A_ij], hence the explicit Witt negation.
            yg = []
            yw = []
            for i in range(3):
                field_linear = {}
                witt_linear = {}

                for j in range(3):
                    field_linear = poly_add(
                        field_linear,
                        poly_scale(xg[j], A[i][j], gf_mul, 0),
                        lambda x, y: x ^ y,
                        0,
                    )
                    witt_linear = poly_add(
                        witt_linear,
                        poly_scale(
                            xw[j],
                            w_neg((A[i][j], 0)),
                            w_mul,
                            WZERO,
                        ),
                        w_add,
                        WZERO,
                    )

                yg.append(
                    poly_add(
                        field_linear,
                        poly_scale(xg[3], u[i], gf_mul, 0),
                        lambda x, y: x ^ y,
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

            Fg = {}
            Fw = {}
            for i in range(3):
                Fg = poly_add(Fg, xg_33[i], lambda x, y: x ^ y, 0)
                Fg = poly_add(
                    Fg,
                    poly_pow(
                        yg[i],
                        33,
                        lambda x, y: x ^ y,
                        gf_mul,
                        0,
                        1,
                    ),
                    lambda x, y: x ^ y,
                    0,
                )

                Fw = poly_add(Fw, xw_33[i], w_add, WZERO)
                Fw = poly_add(
                    Fw,
                    poly_pow(yw[i], 33, w_add, w_mul, WZERO, WONE),
                    w_add,
                    WZERO,
                )

            reduced_witt_fermat = reduce_quad(
                Fw, Uw, w_add, w_mul, WZERO, WONE
            )
            for coefficient in reduced_witt_fermat.values():
                if coefficient[0] != 0:
                    fail(
                        "W2 Fermat restriction is nonzero modulo 2 for z=%r"
                        % (z,)
                    )

            # If a reduced Witt coefficient is (0,c), division by 2 followed
            # by inverse Frobenius gives c^(2^(5-1))=c^16 in F_32.
            h = {}
            for exponent, coefficient in reduced_witt_fermat.items():
                value = gf_pow(coefficient[1], 16)
                if value:
                    h[exponent] = value

            quotient = divide_by_quad_exact(Fg, Ug)
            Q = reduce_quad(
                quotient,
                Ug,
                lambda x, y: x ^ y,
                gf_mul,
                0,
                1,
            )

            pivot_coordinate = next(
                (i for i, value in enumerate(u) if value != 0), None
            )
            if pivot_coordinate is None:
                fail("could not select a nonzero coordinate of u")

            remaining_coordinates = [
                i for i in range(3) if i != pivot_coordinate
            ]
            gradients = []
            for i in remaining_coordinates:
                gradients.append(
                    reduce_quad(
                        poly_pow(
                            yg[i],
                            32,
                            lambda x, y: x ^ y,
                            gf_mul,
                            0,
                            1,
                        ),
                        Ug,
                        lambda x, y: x ^ y,
                        gf_mul,
                        0,
                        1,
                    )
                )

            columns = (
                normal_columns(gradients[0], 1, Ug)
                + normal_columns(gradients[1], 1, Ug)
                + normal_columns(Q, 2, Ug)
            )
            if len(columns) != 17:
                fail(
                    "normal map has %d columns rather than 17 for z=%r"
                    % (len(columns), z)
                )

            reduction = row_reduce(columns, target_rows)
            rank_m = len(reduction[1])
            if lies_in_span(h, reduction):
                rank_augmented = rank_m
            else:
                rank_augmented = rank_m + 1

            if rank_m != EXPECTED_RANK:
                fail(
                    "rank(M)=%d rather than 17 for z=%r"
                    % (rank_m, z)
                )
            if rank_augmented != EXPECTED_AUGMENTED_RANK:
                fail(
                    "rank(M|h)=%d rather than 18 for z=%r"
                    % (rank_augmented, z)
                )

            rank17_count += 1
            rank18_count += 1
            certificate_records.append(
                "%d,%d,%d:%d,%d"
                % (z[0], z[1], z[2], rank_m, rank_augmented)
            )

    if processed != EXPECTED_COUNT:
        fail(
            "processed %d neighbors rather than %d"
            % (processed, EXPECTED_COUNT)
        )
    if len(certificate_records) != EXPECTED_COUNT:
        fail("certificate stream does not contain 1023 records")
    if rank17_count != EXPECTED_COUNT:
        fail("not all 1023 normal maps have rank 17")
    if rank18_count != EXPECTED_COUNT:
        fail("not all 1023 augmented maps have rank 18")

    certificate_stream = ";".join(certificate_records).encode("ascii")
    digest = hashlib.sha256(certificate_stream).hexdigest()

    if digest != EXPECTED_SHA256:
        fail(
            "certificate SHA256 mismatch: got %s, expected %s"
            % (digest, EXPECTED_SHA256)
        )

    elapsed = time.monotonic() - start
    print("Cycle 123 exhaustive adjacent-union obstruction")
    print("neighbors processed = %d" % processed)
    print("rank(M) = 17 count = %d" % rank17_count)
    print("rank(M | h) = 18 count = %d" % rank18_count)
    print("liftable pairs = 0")
    print("certificate records = %d" % len(certificate_records))
    print("certificate bytes = %d" % len(certificate_stream))
    print("certificate sha256 = %s" % digest)
    print("expected sha256 = %s" % EXPECTED_SHA256)
    print("elapsed seconds = %.6f" % elapsed)
    print("all exact checks passed")


if __name__ == "__main__":
    main()
