#!/usr/bin/env python3
"""Dependency-free exact cross-audit for the final rank-(1,6) countersearch.

This verifier checks the rational inequalities newly consolidated in
``open-audits/rank-one-six-unit-star-countersearch-final-2026-11-20.md``.
The two companion verifiers audit the graph characteristic polynomials,
projector-residue formulas, and Sturm root counts.  No floating point and no
``assert`` statements are used here.
"""

from fractions import Fraction as F


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def poly_eval_desc(coefficients, value):
    out = F(0)
    for coefficient in coefficients:
        out = out * value + coefficient
    return out


def audit_projector_obstruction():
    cubic = [F(1), F(0), F(-4), F(-1)]
    at_upper = poly_eval_desc(cubic, F(423, 200))
    require(at_upper == F(6967, 8_000_000),
            "B_1 cubic endpoint identity changed")
    require(at_upper > 0, "B_1 positive-root upper bracket changed")

    # sqrt(5)>559/250 is certified after squaring positive quantities.
    require(5 * 250**2 - 559**2 == 19,
            "sqrt(5) rational lower certificate changed")

    debit_lower = (F(7) + F(559, 250)) / 2 - F(423, 200) ** 2
    require(debit_lower == F(5791, 40000),
            "hostile-debit rational lower bound changed")
    require(F(1, 24) < F(1, 7) < debit_lower,
            "projector/debit comparison changed")


def audit_finite_gain_obstruction():
    p_intervals = (
        (F(15215, 10000), F(15216, 10000)),
        (F(35011, 10000), F(35012, 10000)),
    )
    g_intervals = (
        (F(4476, 10000), F(4477, 10000)),
        (F(15233, 10000), F(15234, 10000)),
        (F(34930, 10000), F(34931, 10000)),
        (F(40636, 10000), F(40637, 10000)),
    )
    lower = (sum(left * left for left, _ in g_intervals)
             - sum(right * right for _, right in p_intervals) - 16)
    upper = (sum(right * right for _, right in g_intervals)
             - sum(left * left for left, _ in p_intervals) - 16)
    require(lower == F(66101461, 100000000),
            "finite gain rational lower bound changed")
    require(upper == F(66392469, 100000000),
            "finite gain rational upper bound changed")
    require(F(3, 5) < lower < upper < F(2, 3),
            "finite gain interval no longer lies in (3/5,2/3)")
    require(F(2, 3) - upper == F(822593, 300000000),
            "finite gain 2/3 gap changed")


def audit_limit_obstruction():
    # f(x)=x^3-3x^2-5x+3.
    f = [F(1), F(-3), F(-5), F(3)]
    require(poly_eval_desc(f, F(-77, 50)) == F(-8383, 125000),
            "negative-root lower endpoint identity changed")
    require(poly_eval_desc(f, F(-3, 2)) == F(3, 8),
            "negative-root upper endpoint identity changed")
    require(F(3) - F(77, 50) ** 2 == F(1571, 2500),
            "limit lower rational comparison changed")
    require(F(1571, 2500) > F(3, 5),
            "limit lower bound no longer exceeds 3/5")

    # -4+8*sqrt(21)/9>0 follows by squaring positive sides:
    # 8*sqrt(21)>36 iff 64*21>36^2.
    require(64 * 21 - 36**2 == 48,
            "sqrt(7/3) sign certificate changed")
    require(poly_eval_desc(f, F(-2)) == -7,
            "negative-root comparison at -2 changed")


def main():
    audit_projector_obstruction()
    audit_finite_gain_obstruction()
    audit_limit_obstruction()
    print("PASS final rank-(1,6) / unit-star countersearch cross-audit")
    print("exact obstruction only: no sigma(G)<0 graph counterexample claimed")
    print("projector product < 1/24 < 1/7 < hostile B_1 debit")
    print("66101461/100000000 < Gamma_10 < 66392469/100000000 < 2/3")
    print("3/5 < lim Gamma_t < 2/3")


if __name__ == "__main__":
    main()
