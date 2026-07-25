#!/usr/bin/env python3
"""Exact phase-monotonicity certificate for a bridge joining two C5s."""

import hashlib

import sympy as s


EXPECTED_TERMS = 4891
EXPECTED_SHA256 = "365e18dedf9032fbcdb88af83d033f0651f02412c796b4f1dfde04152a478af1"


def rooted_cycle(a0, x1, x2, x3, x4):
    deleted_root = x1*x2*x3*x4 + x3*x4 + x1*x4 + x1*x2 + 1
    root_matched = x2*x3*x4 + x2 + x4 + x1*x2*x3 + x1 + x3
    return deleted_root, s.expand(a0*deleted_root + root_matched)


def verify_bare_core_spectrum() -> None:
    x = s.symbols("x")
    adjacency = s.zeros(10)
    edges = [(offset + vertex, offset + (vertex + 1) % 5)
             for offset in (0, 5) for vertex in range(5)]
    edges.append((0, 5))
    for left, right in edges:
        adjacency[left, right] = 1
        adjacency[right, left] = 1

    expected = ((x - 1)*(x**2 - x - 3)*(x**2 + x - 1)**2
                *(x**3 - 4*x + 1))
    assert s.expand(adjacency.charpoly(x).as_expr() - expected) == 0

    rho_polynomial = x**3 - 4*x - 1
    assert rho_polynomial.subs(x, 2) == -1
    assert s.simplify(rho_polynomial.subs(x, s.sqrt(5))) == s.sqrt(5) - 1


def main() -> None:
    verify_bare_core_spectrum()
    t = s.symbols("t")
    y = s.symbols("y0:10")
    variables = (t, *y)

    p, q = rooted_cycle(*(t + value for value in y[:5]))
    u, r = rooted_cycle(*(t + value for value in y[5:]))
    bare_p = t**4 + 3*t**2 + 1
    bare_q = t**5 + 5*t**3 + 5*t
    bare_real = s.expand(bare_q**2 + bare_p**2 - 4)
    weighted_real = s.expand(q*r + p*u - 4)

    certificate = s.Poly(
        s.expand(2*bare_q*weighted_real - (q + r)*bare_real),
        *variables,
        domain=s.ZZ,
    )
    terms = certificate.terms()
    coefficients = [coefficient for _, coefficient in terms]
    assert len(terms) == EXPECTED_TERMS
    assert all(coefficient > 0 for coefficient in coefficients)
    assert all(any(exponent != 0 for exponent in monomial[1:])
               for monomial, _ in terms)
    assert certificate.as_expr().subs(dict.fromkeys(y, 0)) == 0

    payload = "\n".join(
        f"{monomial}:{coefficient}" for monomial, coefficient in terms
    ).encode("ascii")
    digest = hashlib.sha256(payload).hexdigest()
    assert digest == EXPECTED_SHA256

    print("PASS two-C5 bridge phase coefficient certificate")
    print(f"terms={len(terms)} min_coefficient={min(coefficients)} "
          f"max_coefficient={max(coefficients)}")
    print("y_constant=0 all_nonconstant_coefficients_positive=True")
    print(f"sha256={digest}")


if __name__ == "__main__":
    main()
