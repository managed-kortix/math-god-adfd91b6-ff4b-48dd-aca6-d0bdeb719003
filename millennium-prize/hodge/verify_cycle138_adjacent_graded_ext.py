#!/usr/bin/env python3
"""Cycle 138: exact graded Ext check for two adjacent plane factorizations.

The symbolic calculation is over the weighted polynomial ring

    F_2[z0,z1,p,q,r,s,A,B,C],

where the first six generators have weight 1, A has weight 31, and B,C
have weight 32.  Thus F=p*q*A+r*B+s*C is the abstract degree-33 normal
form, not a specialization of it.  A separate finite polynomial calculation
over N=F_2[z0,z1,q] computes the degree-zero Ext quotient.

No assertion statement is used, so all checks remain active under python -O.
"""

import sys


NAMES = ("z0", "z1", "p", "q", "r", "s", "A", "B", "C")
WEIGHTS = (1, 1, 1, 1, 1, 1, 31, 32, 32)
NVARS = len(NAMES)
ZERO_EXP = (0,) * NVARS


def fail(message):
    print("FAIL: " + message, file=sys.stderr)
    raise SystemExit(1)


def check(condition, message):
    if not condition:
        fail(message)


# Sparse polynomials over F_2: a polynomial is the set of exponents having
# coefficient one.  Addition is symmetric difference.
def poly_add(left, right):
    return left ^ right


def poly_mul(left, right):
    result = set()
    for a in left:
        for b in right:
            exponent = tuple(x + y for x, y in zip(a, b))
            if exponent in result:
                result.remove(exponent)
            else:
                result.add(exponent)
    return frozenset(result)


ZERO = frozenset()
ONE = frozenset((ZERO_EXP,))


def variable(index):
    exponent = [0] * NVARS
    exponent[index] = 1
    return frozenset((tuple(exponent),))


z0, z1, p, q, r, s, A, B, C = tuple(variable(i) for i in range(NVARS))


def monomial_weight(exponent):
    return sum(e * w for e, w in zip(exponent, WEIGHTS))


def homogeneous_degree(poly):
    check(poly != ZERO, "requested the degree of zero")
    degrees = {monomial_weight(exponent) for exponent in poly}
    check(len(degrees) == 1, "polynomial is not weighted homogeneous")
    return next(iter(degrees))


def zero_matrix(rows, columns):
    return [[ZERO for _ in range(columns)] for _ in range(rows)]


def matrix_add(left, right):
    check(len(left) == len(right), "matrix row mismatch")
    check(not left or len(left[0]) == len(right[0]), "matrix column mismatch")
    return [
        [poly_add(x, y) for x, y in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def matrix_mul(left, right):
    rows = len(left)
    middle = len(right)
    columns = len(right[0]) if right else 0
    check(not left or len(left[0]) == middle, "matrix product shape mismatch")
    result = zero_matrix(rows, columns)
    for i in range(rows):
        for k in range(middle):
            if left[i][k] == ZERO:
                continue
            for j in range(columns):
                if right[k][j] != ZERO:
                    result[i][j] = poly_add(
                        result[i][j], poly_mul(left[i][k], right[k][j])
                    )
    return result


def scalar_identity(size, scalar):
    result = zero_matrix(size, size)
    for i in range(size):
        result[i][i] = scalar
    return result


EVEN = (0, 3, 5, 6)
ODD = (1, 2, 4, 7)
EVEN_INDEX = {mask: i for i, mask in enumerate(EVEN)}
ODD_INDEX = {mask: i for i, mask in enumerate(ODD)}


def operator_matrix(source_masks, target_masks, wedge, contraction):
    """Matrix of sum wedge_i*wedge(e_i) + contraction_i*iota(e_i).

    Exterior signs disappear over F_2.  Masks encode the standard basis of
    Lambda^* F_2^3, so this constructs all entries rather than assuming a
    reduced or rank-one factorization.
    """
    target_index = {mask: i for i, mask in enumerate(target_masks)}
    result = zero_matrix(len(target_masks), len(source_masks))
    for column, mask in enumerate(source_masks):
        for i in range(3):
            bit = 1 << i
            if mask & bit:
                target = mask ^ bit
                coefficient = contraction[i]
            else:
                target = mask | bit
                coefficient = wedge[i]
            row = target_index[target]
            result[row][column] = poly_add(result[row][column], coefficient)
    return result


def factorization(linears, partners):
    d0 = operator_matrix(EVEN, ODD, linears, partners)
    d1 = operator_matrix(ODD, EVEN, linears, partners)
    return d0, d1


def check_matrix_degrees(matrix, source_masks, target_masks, target_twist):
    """Check a degree-zero map into a module with the given internal twist."""
    generator_degree = {
        0: 0,
        1: -1,
        2: -1,
        4: -1,
        3: 31,
        5: 31,
        6: 31,
        7: 30,
    }
    for row, target in enumerate(target_masks):
        for column, source in enumerate(source_masks):
            entry = matrix[row][column]
            if entry == ZERO:
                continue
            expected = (
                generator_degree[source]
                - generator_degree[target]
                + target_twist
            )
            actual = homogeneous_degree(entry)
            check(actual == expected, "graded matrix entry has wrong degree")


def check_symbolic_factorizations_and_chains():
    potential = poly_add(poly_add(poly_mul(poly_mul(p, q), A), poly_mul(r, B)),
                         poly_mul(s, C))
    check(homogeneous_degree(potential) == 33, "F does not have degree 33")

    # L=(q,r,s), M=(p,r,s), with F=q*(pA)+rB+sC
    # and F=p*(qA)+rB+sC, respectively.
    d0_l, d1_l = factorization((q, r, s), (poly_mul(p, A), B, C))
    d0_m, d1_m = factorization((p, r, s), (poly_mul(q, A), B, C))

    for label, d0, d1 in (("L", d0_l, d1_l), ("M", d0_m, d1_m)):
        check(len(d0) == 4 and len(d0[0]) == 4, label + " d0 is not 4 by 4")
        check(len(d1) == 4 and len(d1[0]) == 4, label + " d1 is not 4 by 4")
        check_matrix_degrees(d0, EVEN, ODD, 0)
        check_matrix_degrees(d1, ODD, EVEN, 33)
        check(matrix_mul(d1, d0) == scalar_identity(4, potential),
              label + " d1*d0 is not F times the identity")
        check(matrix_mul(d0, d1) == scalar_identity(4, potential),
              label + " d0*d1 is not F times the identity")

    representatives = []
    for name, a in (("z0", z0), ("z1", z1)):
        Aa = poly_mul(A, a)
        phi0 = operator_matrix(EVEN, ODD, (a, ZERO, ZERO), (Aa, ZERO, ZERO))
        phi1 = operator_matrix(ODD, EVEN, (a, ZERO, ZERO), (Aa, ZERO, ZERO))
        check_matrix_degrees(phi0, EVEN, ODD, 0)
        check_matrix_degrees(phi1, ODD, EVEN, 33)

        even_equation = matrix_add(matrix_mul(d1_m, phi0),
                                   matrix_mul(phi1, d0_l))
        odd_equation = matrix_add(matrix_mul(d0_m, phi1),
                                  matrix_mul(phi0, d1_l))
        check(even_equation == zero_matrix(4, 4),
              "Phi_" + name + " fails the even cocycle equation")
        check(odd_equation == zero_matrix(4, 4),
              "Phi_" + name + " fails the odd cocycle equation")
        representatives.append((phi0, phi1))

    check(representatives[0] != representatives[1],
          "the two chain representatives coincide")
    print("[1] abstract weighted F_2 polynomial calculation")
    print("F = p*q*A + r*B + s*C has weighted degree 33")
    print("K_L and K_M: shifts K^0=S+S(-31)^3, K^1=S(1)^3+S(-30)")
    print("both full differentials are 4 by 4 and square to F*I_4")
    print("Phi_z0 and Phi_z1 have entry degrees 1/32 and satisfy both cocycle equations")


# The following small linear calculation uses monomial keys (a,b,c) for
# z0^a*z1^b*q^c in N=F_2[z0,z1,q].
def n_monomials(degree):
    return tuple(
        (a, b, degree - a - b)
        for a in range(degree + 1)
        for b in range(degree - a + 1)
    )


def n_mul_monomial(left, right):
    return tuple(a + b for a, b in zip(left, right))


def gf2_rank(columns):
    pivots = {}
    for column in columns:
        vector = set(column)
        while vector:
            pivot = min(vector)
            if pivot not in pivots:
                pivots[pivot] = vector
                break
            vector ^= pivots[pivot]
    return len(pivots)


def check_ext_quotient():
    n0 = n_monomials(0)
    n1 = n_monomials(1)
    check(n0 == ((0, 0, 0),), "N_0 basis is wrong")
    check(set(n1) == {(1, 0, 0), (0, 1, 0), (0, 0, 1)},
          "N_1 basis is wrong")

    q_exp = (0, 0, 1)
    b_restriction = (32, 0, 0)  # one valid finite test: B|_M=z0^32
    c_restriction = (0, 32, 0)  # and C|_M=z1^32

    # d1(a,b,c)=(q*b,q*c,0 ; B*b+C*c).  Tagged coordinates keep the
    # three N_2 components and the N_33 hypersurface component disjoint.
    d1_columns = []
    for component in range(3):
        for monomial in n1:
            output = set()
            if component == 1:
                output.add((0, n_mul_monomial(q_exp, monomial)))
                output.add((3, n_mul_monomial(b_restriction, monomial)))
            elif component == 2:
                output.add((1, n_mul_monomial(q_exp, monomial)))
                output.add((3, n_mul_monomial(c_restriction, monomial)))
            d1_columns.append(output)

    domain_dimension = 3 * len(n1)
    rank_d1 = gf2_rank(d1_columns)
    kernel_dimension = domain_dimension - rank_d1
    check(domain_dimension == 9, "degree-one cochain dimension is not 9")
    check(rank_d1 == 6 and kernel_dimension == 3,
          "ker(d1) is not {(a,0,0): a in N_1}")

    # d0(1)=(q,0,0).  Its image has rank one inside that kernel.
    d0_columns = [{(0, q_exp)}]
    rank_d0 = gf2_rank(d0_columns)
    quotient_dimension = kernel_dimension - rank_d0
    check(rank_d0 == 1, "im(d0)=k*q does not have dimension one")
    check(quotient_dimension == 2, "N_1/k*q does not have dimension two")

    q_column = {(0, q_exp)}
    z0_column = {(0, (1, 0, 0))}
    z1_column = {(0, (0, 1, 0))}
    check(gf2_rank([q_column, z0_column, z1_column]) == 3,
          "z0,z1 are not independent modulo k*q")

    print("[2] degree-zero Ext calculation over N=F_2[z0,z1,q]")
    print("dim ker(d1)=3, im(d0)=k*q, dim N_1/k*q=2")
    print("quotient basis = [z0], [z1]")


def main():
    check_symbolic_factorizations_and_chains()
    check_ext_quotient()
    print("all exact checks passed")


if __name__ == "__main__":
    main()
