#!/usr/bin/env python3
"""Exact coefficient certificate for the two-C5 shared-root inequality."""

import hashlib

import sympy as s


EXPECTED_TERMS = 1290
EXPECTED_SHA256 = "4c436cac772395d2a8edfdd81408ffe426759d3e94d66df2e4ab0235a3343110"


class CertificateError(RuntimeError):
    """Raised when an exact coefficient certificate invariant fails."""


def require(condition, message):
    if not condition:
        raise CertificateError(message)


def path_and_root_matched(x1, x2, x3, x4):
    A = x1*x2*x3*x4 + x3*x4 + x1*x4 + x1*x2 + 1
    B = x2*x3*x4 + x2 + x4 + x1*x2*x3 + x1 + x3
    return A, B


def main() -> None:
    t, y0 = s.symbols("t y0")
    y11, y12, y13, y14, y21, y22, y23, y24 = s.symbols(
        "y11 y12 y13 y14 y21 y22 y23 y24"
    )
    y = (y11, y12, y13, y14, y21, y22, y23, y24)
    variables = (t, y0, *y)

    A1, B1 = path_and_root_matched(*(t + value for value in y[:4]))
    A2, B2 = path_and_root_matched(*(t + value for value in y[4:]))
    a0 = t + y0

    R = a0*A1*A2 + B1*A2 + A1*B2
    P = s.Poly(
        s.expand(2*R - t*(t**4 + 7*t**2 + 9)*(A1 + A2)),
        *variables,
        domain=s.ZZ,
    )

    terms = P.terms()
    coefficients = [coefficient for _, coefficient in terms]
    require(P.domain == s.ZZ, f"coefficient domain is {P.domain}, not ZZ")
    require(len(terms) == EXPECTED_TERMS,
            f"expected {EXPECTED_TERMS} terms, got {len(terms)}")
    require(bool(coefficients), "coefficient stream is empty")
    require(all(coefficient.is_Integer for coefficient in coefficients),
            "coefficient stream contains a non-integer")
    require(all(coefficient >= 0 for coefficient in coefficients),
            "coefficient stream contains a negative coefficient")
    require(all(coefficient > 0 for coefficient in coefficients),
            "canonical sparse term stream contains a nonpositive coefficient")
    require(P.as_expr().subs(dict.fromkeys((y0, *y), 0)) == 0,
            "polynomial has a nonzero y-constant part")
    require(all(any(exponent != 0 for exponent in monomial[1:])
                for monomial, _ in terms),
            "a canonical term is independent of every y variable")

    payload = "\n".join(
        f"{monomial}:{coefficient}" for monomial, coefficient in terms
    ).encode("ascii")
    digest = hashlib.sha256(payload).hexdigest()
    require(digest == EXPECTED_SHA256,
            f"coefficient digest mismatch: expected {EXPECTED_SHA256}, got {digest}")

    print("PASS two-C5 bouquet matching coefficient certificate")
    print(f"terms={len(terms)} min_coefficient={min(coefficients)} "
          f"max_coefficient={max(coefficients)}")
    print("y_constant=0 all_coefficients_nonnegative=True")
    print(f"sha256={digest}")


if __name__ == "__main__":
    main()
