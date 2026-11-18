#!/usr/bin/env python3
"""Dependency-free exact audit for the C5-bouquet projector counterfamily.

No floating point and no assert statements are used.  Polynomial coefficient
lists are low-to-high.  The verifier checks representative graph matrices,
the symbolic divisor identities by polynomial arithmetic over Q[r], exact
rational isolating brackets, and the sign identities used in the note.
"""
from fractions import Fraction as F
from itertools import permutations
from math import isqrt


def trim(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def add(a, b):
    out = [F(0)] * max(len(a), len(b))
    for i, z in enumerate(a):
        out[i] += z
    for i, z in enumerate(b):
        out[i] += z
    return trim(out)


def sub(a, b):
    return add(a, [-z for z in b])


def mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, z in enumerate(a):
        for j, w in enumerate(b):
            out[i + j] += z * w
    return trim(out)


def scale(a, q):
    return trim([F(q) * z for z in a])


def evaluate(a, q):
    out = F(0)
    for z in reversed(a):
        out = out * q + z
    return out


def parity(p):
    inv = sum(p[i] > p[j] for i in range(len(p))
              for j in range(i + 1, len(p)))
    return -1 if inv & 1 else 1


def charpoly_low(matrix):
    """Exact det(xI-M) by the Leibniz formula (small matrices only)."""
    n = len(matrix)
    out = [F(0)]
    for p in permutations(range(n)):
        term = [F(parity(p))]
        for i, j in enumerate(p):
            factor = [-F(matrix[i][j]), F(1)] if i == j else [-F(matrix[i][j])]
            term = mul(term, factor)
        out = add(out, term)
    return out


def determinant(matrix):
    """Exact fraction-free Bareiss determinant."""
    M = [list(map(int, row)) for row in matrix]
    n = len(M)
    sign = 1
    previous = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            pivot = next((i for i in range(k + 1, n) if M[i][k]), None)
            if pivot is None:
                return 0
            M[k], M[pivot] = M[pivot], M[k]
            sign *= -1
        pivot = M[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = M[i][j] * pivot - M[i][k] * M[k][j]
                if numerator % previous:
                    raise SystemExit("Bareiss exact division failed")
                M[i][j] = numerator // previous
        previous = pivot
        for i in range(k + 1, n):
            M[i][k] = 0
    return sign * M[-1][-1]


def charpoly_faddeev(matrix):
    """Exact det(xI-A), low-to-high, by Faddeev--LeVerrier."""
    n = len(matrix)
    A = [[F(z) for z in row] for row in matrix]
    B = [[F(i == j) for j in range(n)] for i in range(n)]
    high = [F(1)]
    for k in range(1, n + 1):
        AB = [[sum(A[i][z] * B[z][j] for z in range(n))
               for j in range(n)] for i in range(n)]
        ck = -sum(AB[i][i] for i in range(n)) / k
        high.append(ck)
        B = [[AB[i][j] + (ck if i == j else 0)
              for j in range(n)] for i in range(n)]
    return trim(list(reversed(high)))


def graph_matrix(r):
    """Adjacency matrix of r C5 petals sharing vertex 0, plus leaf 4r+1."""
    n = 4 * r + 2
    A = [[0] * n for _ in range(n)]
    z = 1
    for _ in range(r):
        cycle = [0] + list(range(z, z + 4))
        z += 4
        for i in range(5):
            a, b = cycle[i], cycle[(i + 1) % 5]
            A[a][b] = A[b][a] = 1
    A[0][z] = A[z][0] = 1
    return A


def audit_rank(r):
    # Nonsymmetric equitable divisor.  It is diagonally similar to the
    # symmetric quotient, hence has the same real spectrum.
    D = [[0, 2*r, 0, 1],
         [1, 0, 1, 0],
         [0, 1, 1, 0],
         [1, 0, 0, 0]]
    quotient = charpoly_low(D)
    cubic = [F(-1), F(-(2*r+2)), F(0), F(1)]
    expected_quotient = mul([-1, 1], cubic)
    if quotient != expected_quotient:
        raise SystemExit(f"quotient polynomial mismatch at r={r}: {quotient}")

    minor = [row[:3] for row in D[:3]]
    g = charpoly_low(minor)
    expected_g = list(map(F, [2*r, -(2*r+1), -1, 1]))
    if g != expected_g:
        raise SystemExit(f"rooted minor polynomial mismatch at r={r}: {g}")

    # Rational isolation of the unique positive cubic root.  Descartes gives
    # at most one; f(0)<0 and the upper bracket is positive.
    q = isqrt(2*r+2)
    lo = F(q)
    hi = F(q+1)
    while evaluate(cubic, lo) >= 0:
        lo -= 1
    if not (evaluate(cubic, lo) < 0 < evaluate(cubic, hi)):
        raise SystemExit(f"positive-root bracket failed at r={r}")
    if lo < 2:
        # For r=1 the sharper exact check f(2)=-1 and f(3)>0 applies.
        lo = F(2)
    if evaluate(cubic, F(2)) >= 0:
        raise SystemExit(f"lambda_r>2 sign check failed at r={r}")

    # At a cubic root, these two polynomial identities are exactly the
    # numerators of p_r-1/(r+2) and p_r-1/(2r+2), after clearing their positive
    # denominators.  We check their factorizations in Z[x] coefficientwise.
    # Counterexample identity: negative of five positive factors for x>2.
    counter_factors = ([-1, 1], [-1, -1, 1], [1, 2, 3, 1])
    counter_numerator = scale(mul(mul(*counter_factors[:2]), counter_factors[2]), -1)
    expected_counter = list(map(F, [-1, -2, -1, 2, 4, -1, -1]))
    if counter_numerator != expected_counter:
        raise SystemExit("counterexample factor identity failed")
    if not (evaluate(counter_numerator, F(2)) < 0):
        raise SystemExit("counterexample sign audit failed")

    lower_numerator = [-1, -1, 1]  # x^2-x-1
    if evaluate(lower_numerator, F(2)) <= 0:
        raise SystemExit("comparison with 1/(2r+2) failed")

    # Exact graph-level checks at representative ranks independently bind the
    # family construction to the factored characteristic polynomial.
    if r <= 3:
        A = graph_matrix(r)
        n, m = len(A), sum(map(sum, A)) // 2
        if (n, m, m-n+1) != (4*r+2, 5*r+1, r):
            raise SystemExit(f"graph count failed at r={r}")
        actual = charpoly_faddeev(A)
        expected = mul(mul(mul([-1, 1],
                               polynomial_power([-1, 1, 1], r)),
                           polynomial_power([-1, -1, 1], r-1)), cubic)
        if actual != expected:
            raise SystemExit(f"full characteristic polynomial failed at r={r}")
        if determinant(A) != -1:
            raise SystemExit(f"nonsingularity determinant failed at r={r}")


def polynomial_power(a, k):
    out = [F(1)]
    for _ in range(k):
        out = mul(out, a)
    return out


def symbolic_identity_audit():
    # Work in Z[x].  Put a=(x^3-1)/x=2r+2.  The displayed p_r formula and
    # each comparison are checked after clearing denominators.
    # p numerator P and denominator Q.
    P = [1, 2, 3, 3]                         # 3x^3+3x^2+2x+1
    Q = mul([1, 0, 0, 2], [1, 1, 1])        # (2x^3+1)(x^2+x+1)

    # p-1/(r+2): denominator after substitution is positive, and numerator is
    # -(x-1)(x^2-x-1)(x^3+3x^2+2x+1).
    neg = scale(mul(mul([-1, 1], [-1, -1, 1]), [1, 2, 3, 1]), -1)
    # Directly clear p - 2/(a+2), with a=(x^3-1)/x:
    # P*(x^3+2x-1) - 2x*Q.
    direct = sub(mul(P, [-1, 2, 0, 1]), mul([0, 2], Q))
    if direct != neg:
        raise SystemExit(f"strict-counterexample identity mismatch: {direct} != {neg}")

    # p-1/a = (x^2-x-1)/((x-1)(2x^3+1)).  Cross multiplication:
    # P*(x^3-1) - x*Q = (x^2-x-1)(x^2+x+1)^2.
    direct_lower = sub(mul(P, [-1, 0, 0, 1]), mul([0, 1], Q))
    expected_lower = mul([-1, -1, 1], mul([1, 1, 1], [1, 1, 1]))
    if direct_lower != expected_lower:
        raise SystemExit("lower-comparison identity mismatch")


def main():
    symbolic_identity_audit()
    for r in (1, 2, 3, 6, 7, 20, 101):
        audit_rank(r)
    print("PASS nonnegative-projector C5-bouquet counterfamily")
    print("chi=(x-1)(x^2-x-1)^(r-1)(x^2+x-1)^r(x^3-(2r+2)x-1)")
    print("det(A)=-1, so Pi_{>=0}=Pi_+")
    print("1/(2r+2) < projector leaf diagonal < 1/(r+2) for every r>=1")


if __name__ == "__main__":
    main()
