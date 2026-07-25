#!/usr/bin/env python3
"""Exact coefficient certificate for the shared-vertex C3+C5 phase bound."""

import hashlib

import sympy as s


EXPECTED_TERMS = 293
EXPECTED_SHA256 = "07af9b8b357dc505ada2e47ecd633f085ce16f49077262475bdb4dd09f80086c"


def triangle_partitions(u1, u2):
    """Return the root-deleted and root-matched triangle partitions."""
    return u1*u2 + 1, u1 + u2


def pentagon_partitions(x1, x2, x3, x4):
    """Return the root-deleted and root-matched pentagon partitions."""
    A = x1*x2*x3*x4 + x3*x4 + x1*x4 + x1*x2 + 1
    B = x2*x3*x4 + x2 + x4 + x1*x2*x3 + x1 + x3
    return A, B


def main() -> None:
    t, y0, y31, y32, y51, y52, y53, y54 = s.symbols(
        "t y0 y31 y32 y51 y52 y53 y54"
    )
    y_variables = (y0, y31, y32, y51, y52, y53, y54)
    variables = (t, *y_variables)

    A3, B3 = triangle_partitions(t + y31, t + y32)
    A5, B5 = pentagon_partitions(
        t + y51, t + y52, t + y53, t + y54
    )
    R = (t + y0)*A3*A5 + B3*A5 + A3*B5
    Z5 = t**5 + 5*t**3 + 5*t

    # Since Psi/K = R + 2*i*(A3-A5), this is exactly the cleared
    # denominator form of arg(Psi) <= atan(2/Z5).
    Q = s.Poly(s.expand(R - Z5*(A3 - A5)), *variables, domain=s.ZZ)
    terms = Q.terms()
    coefficients = [coefficient for _, coefficient in terms]

    assert len(terms) == EXPECTED_TERMS
    assert all(coefficient > 0 for coefficient in coefficients)
    assert s.factor(Q.as_expr().subs(dict.fromkeys(y_variables, 0))) == (
        t*(t**4 + 3*t**2 + 1)*(t**4 + 5*t**2 + 7)
    )

    payload = "\n".join(
        f"{monomial}:{coefficient}" for monomial, coefficient in terms
    ).encode("ascii")
    digest = hashlib.sha256(payload).hexdigest()
    assert digest == EXPECTED_SHA256

    print("PASS shared-vertex C3+C5 phase coefficient certificate")
    print(
        f"terms={len(terms)} min_coefficient={min(coefficients)} "
        f"max_coefficient={max(coefficients)}"
    )
    print("all_coefficients_positive=True")
    print("y_constant=t*(t^4+3*t^2+1)*(t^4+5*t^2+7)")
    print(f"sha256={digest}")


if __name__ == "__main__":
    main()
