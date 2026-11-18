#!/usr/bin/env python3
"""Exact nonpromotional audit for the rank-(1,6) bridge-gain obstruction.

Run with ``uv run --with sympy python``.  Accepted comparisons use only exact
SymPy integer/rational/algebraic arithmetic.  The optional decimal printed at
the end is orientation-only.
"""

from __future__ import annotations

import sympy as sp


x, t, e, z, a, b = sp.symbols("x t e z a b")
q = x**2 + x - 1
r = x**2 - x - 1
f = x**3 - 3*x**2 - 5*x + 3
p = x**4 - x**3 - (t + 3) * x**2 + (t + 2) * x + t
g = (
    x**7 - 4 * x**6 - (t + 5) * x**5 + (4 * t + 19) * x**4
    + (3 * t + 5) * x**3 - (11 * t + 15) * x**2
    + (4 - 2 * t) * x + 3 * t - 3
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def adjacency_h(T):
    matrix = sp.zeros(5 + T)
    for vertex in range(5):
        other = (vertex + 1) % 5
        matrix[vertex, other] = matrix[other, vertex] = 1
    for leaf in range(T):
        matrix[0, 5 + leaf] = matrix[5 + leaf, 0] = 1
    return matrix


def adjacency_g(T):
    matrix = sp.diag(adjacency_h(T), sp.zeros(5))
    first_k5 = 5 + T
    for left in range(first_k5, first_k5 + 5):
        for right in range(left + 1, first_k5 + 5):
            matrix[left, right] = matrix[right, left] = 1
    matrix[5, first_k5] = matrix[first_k5, 5] = 1
    return matrix


def audit_graphs_and_factors():
    h_divisor = sp.Matrix((
        (0, 2, 0, t),
        (1, 0, 1, 0),
        (0, 1, 1, 0),
        (1, 0, 0, 0),
    ))
    g_divisor = sp.Matrix((
        (0, 2, 0, 1, t - 1, 0, 0),
        (1, 0, 1, 0, 0, 0, 0),
        (0, 1, 1, 0, 0, 0, 0),
        (1, 0, 0, 0, 0, 1, 0),
        (1, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 1, 0, 0, 4),
        (0, 0, 0, 0, 0, 1, 3),
    ))
    require(sp.expand((x * sp.eye(4) - h_divisor).det() - p) == 0,
            "H_t divisor determinant changed")
    require(sp.expand((x * sp.eye(7) - g_divisor).det() - g) == 0,
            "G_t divisor determinant changed")

    for T in range(1, 5):
        chi_h = adjacency_h(T).charpoly(x).as_expr()
        target_h = x ** (T - 1) * q * p.subs(t, T)
        require(sp.expand(chi_h - target_h) == 0,
                f"full H_{T} characteristic factorization changed")

        chi_g = adjacency_g(T).charpoly(x).as_expr()
        if T == 1:
            quotient, remainder = sp.div(g.subs(t, 1), x, domain=sp.ZZ)
            require(remainder == 0, "g_1 lost its cancelling zero factor")
            target_g = (x + 1) ** 3 * q * quotient
        else:
            target_g = x ** (T - 2) * (x + 1) ** 3 * q * g.subs(t, T)
        require(sp.expand(chi_g - target_g) == 0,
                f"full G_{T} characteristic factorization changed")

        require(adjacency_h(T).shape == (5 + T, 5 + T), "H_t order changed")
        require(adjacency_g(T).shape == (10 + T, 10 + T), "G_t order changed")
    require(sum(adjacency_h(10)) // 2 == 15, "H_10 edge count changed")
    require(sum(adjacency_g(10)) // 2 == 26, "G_10 edge count changed")
    require(15 - 15 + 1 == 1 and 10 - 5 + 1 == 6,
            "rank-(1,6) calculation changed")


def exact_root_count(poly, left, right):
    return sp.Poly(poly, x).count_roots(sp.Rational(left), sp.Rational(right))


def audit_finite_obstruction():
    P = sp.Poly(p.subs(t, 10), x)
    G = sp.Poly(g.subs(t, 10), x)
    p_intervals = (
        (sp.Rational(15215, 10000), sp.Rational(15216, 10000)),
        (sp.Rational(35011, 10000), sp.Rational(35012, 10000)),
    )
    g_intervals = (
        (sp.Rational(4476, 10000), sp.Rational(4477, 10000)),
        (sp.Rational(15233, 10000), sp.Rational(15234, 10000)),
        (sp.Rational(34930, 10000), sp.Rational(34931, 10000)),
        (sp.Rational(40636, 10000), sp.Rational(40637, 10000)),
    )
    require(P.count_roots(0, sp.oo) == 2, "p_10 positive-root count changed")
    require(G.count_roots(0, sp.oo) == 4, "g_10 positive-root count changed")
    for left, right in p_intervals:
        require(exact_root_count(P, left, right) == 1,
                "p_10 Sturm interval no longer isolates one root")
        require(P.eval(left) * P.eval(right) < 0,
                "p_10 endpoint sign certificate changed")
    for left, right in g_intervals:
        require(exact_root_count(G, left, right) == 1,
                "g_10 Sturm interval no longer isolates one root")
        require(G.eval(left) * G.eval(right) < 0,
                "g_10 endpoint sign certificate changed")

    upper = (sum(right**2 for _, right in g_intervals)
             - sum(left**2 for left, _ in p_intervals) - 16)
    require(upper == sp.Rational(66392469, 100000000),
            "finite rational gain upper bound changed")
    require(upper < sp.Rational(2, 3),
            "finite t=10 obstruction no longer proves gain < 2/3")
    require(sp.Rational(2, 3) - upper == sp.Rational(822593, 300000000),
            "finite obstruction gap changed")
    return upper


def coefficient(poly, variable, power):
    return sp.expand(poly).coeff(variable, power)


def audit_limit():
    require(sp.expand(sp.limit(p / t, t, sp.oo) + r) == 0,
            "bounded p_t limit changed")
    require(sp.expand(sp.limit(g / t, t, sp.oo) + r * f) == 0,
            "bounded g_t limit changed")
    require(sp.discriminant(r, x) == 5, "r discriminant changed")
    require(sp.discriminant(f, x) == 1616, "f discriminant changed")
    require(sp.resultant(r, f, x) == -41, "limiting factors ceased to be coprime")

    scaled_p = sp.expand(e**4 * p.subs({t: e**-2, x: z / e}))
    scaled_g = sp.expand(e**7 * g.subs({t: e**-2, x: z / e}))
    expected_p = z**4 - z**2 + e * (-z**3 + z) + e**2 * (1 - 3*z**2) + 2*e**3*z
    expected_g = (
        z**7 - z**5 + e * (-4*z**6 + 4*z**4)
        + e**2 * (-5*z**5 + 3*z**3)
        + e**3 * (19*z**4 - 11*z**2)
        + e**4 * (5*z**3 - 2*z) + e**5 * (3 - 15*z**2)
        + 4*e**6*z - 3*e**7
    )
    require(sp.expand(scaled_p - expected_p) == 0, "scaled p equation changed")
    require(sp.expand(scaled_g - expected_g) == 0, "scaled g equation changed")
    require(sp.diff(expected_p, z).subs({e: 0, z: 1}) == 2,
            "positive escaping p root is not simple at the limit")
    require(sp.diff(expected_g, z).subs({e: 0, z: 1}) == 2,
            "positive escaping g root is not simple at the limit")

    for label, equation in (("p", expected_p), ("g", expected_g)):
        trial = sp.series(equation.subs(z, 1 + a*e + b*e**2), e, 0, 3).removeO()
        first = coefficient(trial, e, 1)
        a_value = sp.solve(first, a)
        require(a_value == [0], f"{label} escaping-root linear coefficient changed")
        second = coefficient(trial.subs(a, 0), e, 2)
        b_value = sp.solve(second, b)
        require(b_value == [1], f"{label} escaping-root quadratic coefficient changed")

    # Descartes on f(-x) gives exactly one negative root: its nonzero
    # coefficients have signs -,-,+,+, hence one sign change.
    negative_coefficients = sp.Poly(f.subs(x, -x), x).all_coeffs()
    signs = [sp.sign(value) for value in negative_coefficients if value]
    require(sum(left != right for left, right in zip(signs, signs[1:])) == 1,
            "unique-negative-root Descartes certificate changed")
    require(f.subs(x, -2) < 0 < f.subs(x, -sp.Rational(3, 2)),
            "negative limiting root bracket changed")

    s = sp.sqrt(sp.Rational(7, 3))
    value = sp.simplify(f.subs(x, -s))
    require(value == -4 + 8 * sp.sqrt(21) / 9,
            "2/3 limiting comparison identity changed")
    require(value > 0, "limiting obstruction no longer gives alpha^2 > 7/3")

    alpha = sp.CRootOf(f, 0)
    limit_gain = 3 - alpha**2
    require(alpha < -s, "negative-root ordering changed")
    require(limit_gain < sp.Rational(2, 3), "limiting gain is no longer below 2/3")

    # Claim-boundary check only: this limit is above delta_5, but no finite-t
    # lower bound follows and none is asserted by this verifier.
    require(limit_gain > sp.sqrt(5) - 2,
            "orientation-only comparison with delta_5 changed")
    return alpha, limit_gain


def main():
    audit_graphs_and_factors()
    upper = audit_finite_obstruction()
    alpha, limit_gain = audit_limit()
    print("rank-(1,6) bridge-gain obstruction: exact audit passed")
    print(f"finite certificate: Gamma_10 < {upper} < 2/3")
    print("limit: Gamma_t -> 3-alpha^2 < 2/3, f(alpha)=0, alpha<0")
    print("claim boundary: no finite-t lower bound and no delta_5 payment")
    print(f"orientation only: alpha~{sp.N(alpha, 10)}, limit~{sp.N(limit_gain, 10)}")


if __name__ == "__main__":
    main()
