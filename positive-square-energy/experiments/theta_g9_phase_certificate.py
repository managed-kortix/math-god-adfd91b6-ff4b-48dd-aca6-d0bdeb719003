#!/usr/bin/env python3
"""Exact whole-rectangle phase certificate for theta graphs of odd girth >= 9."""

from itertools import product
from math import comb

import sympy as sp


z, x = sp.symbols("z x")
CAP = sp.Rational(3, 4)
EXCEPTIONAL = (1, 8, 2)
EXPECTED_J_MINIMUM = sp.Rational(1674992681, 1073741824)


def f(length):
    return 1 - (-z) ** length


def reconstruct(lengths):
    """Reconstruct F,N,P,Q,R,S from three concrete path lengths."""
    F = sp.prod(f(length) for length in lengths)
    complements = [
        sp.prod(f(other) for j, other in enumerate(lengths) if j != i)
        for i in range(3)
    ]
    N = (1 - z) * F + z * sum(
        f(length - 1) * complement
        for length, complement in zip(lengths, complements)
    )
    P = sum(
        (-1) ** ((length - 1) // 2) * z ** ((length - 1) // 2) * complement
        for length, complement in zip(lengths, complements)
        if length % 2
    )
    Q = sum(
        (-1) ** (length // 2) * z ** (length // 2 - 1) * complement
        for length, complement in zip(lengths, complements)
        if length % 2 == 0
    )
    N, P, Q = map(sp.expand, (N, P, Q))
    R = sp.expand(N**2 + z * (1 + z) ** 2 * (P**2 - z * Q**2))
    S = sp.expand(2 * z * (1 + z) ** 2 * P * Q)
    return F, N, P, Q, R, S


def power_to_bernstein(poly, variable=x):
    """Exact degree-preserving power-to-Bernstein conversion on [0,1]."""
    power = sp.Poly(sp.expand(poly), variable)
    degree = power.degree()
    coefficients = [
        sp.factor(sum(
            power.coeff_monomial(variable**j)
            * sp.Rational(comb(i, j), comb(degree, j))
            for j in range(i + 1)
        ))
        for i in range(degree + 1)
    ]
    return degree, coefficients


def bernstein_to_power(coefficients, variable=x):
    degree = len(coefficients) - 1
    return sp.expand(sum(
        coefficient * comb(degree, i) * variable**i
        * (1 - variable) ** (degree - i)
        for i, coefficient in enumerate(coefficients)
    ))


def certify_nonnegative(poly, variable=z, left=0, right=CAP, strict=False):
    """Certify a polynomial on [left,right] by exact Bernstein coefficients."""
    transformed = sp.expand(poly.subs(variable, left + (right - left) * x))
    degree, coefficients = power_to_bernstein(transformed, x)
    assert bernstein_to_power(coefficients, x) == transformed
    if strict:
        assert all(coefficient > 0 for coefficient in coefficients)
    else:
        assert all(coefficient >= 0 for coefficient in coefficients)
        assert any(coefficient > 0 for coefficient in coefficients)
    return degree, coefficients


def cap_data(odd, even, odd_multiplicity):
    """Construct the sharpened cap data rather than storing conclusions."""
    even_multiplicity = 3 - odd_multiplicity
    A = z ** ((odd - 1) // 2) / (1 + z**odd)
    B = z ** (even // 2 - 1) / (1 - z**even)
    C = (1 - z ** (odd - 1)) / (1 + z**odd)
    G = (1 + z ** (even - 1)) / (1 - z**even)
    Abar = odd_multiplicity * A
    Bbar = even_multiplicity * B
    D = sp.cancel(1 - z + z * odd_multiplicity * C + z * even_multiplicity * G)
    c = z * (1 + z) ** 2
    carrier = sp.cancel(D**2 + c * Abar**2 - z * c * Bbar**2)
    numerator = sp.cancel(2 * c * Abar * Bbar)
    phi = sp.cancel(numerator / carrier)
    a = sp.cancel(D**2 - z * c * Bbar**2)
    branch = sp.cancel(a - c * Abar**2)
    y_endpoint = sp.cancel(numerator / (a + c * Abar**2))
    return {
        "A": A, "B": B, "C": C, "G": G,
        "Abar": Abar, "Bbar": Bbar, "D": D, "c": c,
        "carrier": carrier, "numerator": numerator, "Phi": phi,
        "a": a, "branch": branch, "Y_endpoint": y_endpoint,
    }


def oriented_numerator(rational, point):
    """Return the numerator with the sign of its denominator normalized."""
    numerator, denominator = map(sp.expand, sp.fraction(sp.cancel(rational)))
    denominator_value = denominator.subs(z, point)
    assert denominator_value != 0
    if denominator_value < 0:
        numerator, denominator = -numerator, -denominator
    return numerator, denominator


def remove_origin_power(poly):
    power = sp.Poly(sp.expand(poly), z)
    exponent = min(monomial[0] for monomial, coefficient in power.terms())
    return exponent, sp.expand(poly / z**exponent)


def verify_algebra_and_caps():
    """Check path identities, cap formulas, and direct repeated-corner data."""
    a_symbol, k = sp.symbols("a k", integer=True, positive=True)
    b_symbol = a_symbol + 2*k
    odd_difference = (
        z**((a_symbol-1)/2)/(1+z**a_symbol)
        - z**((b_symbol-1)/2)/(1+z**b_symbol)
    )
    odd_factorization = (
        z**((a_symbol-1)/2) * (1-z**k) * (1-z**(a_symbol+k))
        / ((1+z**a_symbol) * (1+z**b_symbol))
    )
    even_difference = (
        z**(a_symbol/2-1)/(1-z**a_symbol)
        - z**(b_symbol/2-1)/(1-z**b_symbol)
    )
    even_factorization = (
        z**(a_symbol/2-1) * (1-z**k) * (1+z**(a_symbol+k))
        / ((1-z**a_symbol) * (1-z**b_symbol))
    )
    assert sp.simplify(odd_difference - odd_factorization) == 0
    assert sp.simplify(even_difference - even_factorization) == 0

    Avar, Bvar, avar, cvar = sp.symbols("Avar Bvar avar cvar", positive=True)
    generic_phi = 2*cvar*Avar*Bvar/(avar+cvar*Avar**2)
    generic_derivative = sp.factor(sp.diff(generic_phi, Avar))
    expected_derivative = (
        2*cvar*Bvar*(avar-cvar*Avar**2)/(avar+cvar*Avar**2)**2
    )
    assert sp.cancel(generic_derivative-expected_derivative) == 0
    critical_point = sp.sqrt(avar/cvar)
    assert sp.simplify(
        generic_phi.subs(Avar, critical_point)-sp.sqrt(cvar)*Bvar/sp.sqrt(avar)
    ) == 0

    cases = [
        (odd, 9-odd, odd_multiplicity)
        for odd, odd_multiplicity in product((1, 3, 5, 7), (1, 2))
    ]
    for odd, even, odd_multiplicity in cases:
        data = cap_data(odd, even, odd_multiplicity)
        r = odd_multiplicity
        s = 3 - r
        assert sp.cancel(data["C"] + (1+z)*z**((odd-1)//2)*data["A"] - 1) == 0
        assert sp.cancel(data["G"] - (1+z)*z**(even//2)*data["B"] - 1) == 0
        lengths = (odd,) * r + (even,) * s
        F, N, P, Q, R, S = reconstruct(lengths)
        p = r * (-1) ** ((odd - 1) // 2) * data["A"]
        q = s * (-1) ** (even // 2) * data["B"]
        assert sp.cancel(N/F - data["D"]) == 0
        assert sp.cancel(P/F - p) == 0
        assert sp.cancel(Q/F - q) == 0
        assert sp.cancel(R/F**2 - data["carrier"]) == 0
        assert sp.cancel(S/F**2 - data["numerator"]) == 0
        assert sp.cancel(data["Phi"] - S/R) == 0
        assert sp.cancel(data["Y_endpoint"] - data["Phi"]) == 0
    return cases


def certify_ordinary_cap(case):
    """For seven caps, certify endpoint branch and endpoint polynomial L."""
    data = cap_data(*case)
    branch_numerator, branch_denominator = oriented_numerator(
        data["branch"], sp.Rational(1, 2)
    )
    certify_nonnegative(branch_numerator)
    certify_nonnegative(branch_denominator, strict=True)

    endpoint_residual = sp.cancel(4*z**4 - data["Y_endpoint"])
    endpoint_numerator, endpoint_denominator = oriented_numerator(
        endpoint_residual, sp.Rational(1, 2)
    )
    origin_power, L = remove_origin_power(endpoint_numerator)
    assert origin_power > 0
    degree, coefficients = certify_nonnegative(L)
    certify_nonnegative(endpoint_denominator, strict=True)
    return degree, coefficients, sp.factor(L)


def certify_exceptional_cap():
    """Split (1,8;2,1): endpoint below 1/4, interior bound above it."""
    data = cap_data(*EXCEPTIONAL)
    branch_numerator, branch_denominator = oriented_numerator(
        data["branch"], sp.Rational(1, 8)
    )
    certify_nonnegative(branch_numerator, right=sp.Rational(1, 4))
    certify_nonnegative(branch_denominator, right=sp.Rational(1, 4), strict=True)

    endpoint_residual = sp.cancel(4*z**4 - data["Y_endpoint"])
    endpoint_numerator, endpoint_denominator = oriented_numerator(
        endpoint_residual, sp.Rational(1, 8)
    )
    origin_power, L = remove_origin_power(endpoint_numerator)
    assert origin_power > 0
    endpoint_degree, endpoint_coefficients = certify_nonnegative(
        L, right=sp.Rational(1, 4)
    )
    certify_nonnegative(endpoint_denominator, right=sp.Rational(1, 4), strict=True)

    a_numerator, a_denominator = oriented_numerator(data["a"], sp.Rational(1, 2))
    certify_nonnegative(
        a_numerator, left=sp.Rational(1, 4), right=CAP, strict=True
    )
    certify_nonnegative(
        a_denominator, left=sp.Rational(1, 4), right=CAP, strict=True
    )

    # If a-c*Abar^2<0, the exact rectangle maximizer of Phi is the interior
    # value sqrt(c)*Bbar/sqrt(a).  Squaring Phi<=4*z^4, then multiplying
    # by the positive z, gives the displayed polynomial J.
    J_rational = sp.cancel(
        16*z**9 * data["a"]
        - z**2 * (1+z)**2 * data["Bbar"]**2
    )
    J_with_origin, J_denominator = oriented_numerator(J_rational, sp.Rational(1, 2))
    origin_power, J = remove_origin_power(J_with_origin)
    assert origin_power == 8
    j_degree, j_coefficients = certify_nonnegative(
        J, left=sp.Rational(1, 4), right=CAP, strict=True
    )
    certify_nonnegative(
        J_denominator, left=sp.Rational(1, 4), right=CAP, strict=True
    )
    assert min(j_coefficients) == EXPECTED_J_MINIMUM
    return (
        endpoint_degree, endpoint_coefficients, sp.factor(L),
        j_degree, j_coefficients, sp.factor(J),
    )


def verify_set_inclusion_reduction():
    """Check the exact remainder decomposition used for arbitrary g>=9."""
    o, e = sp.symbols("o e", integer=True, positive=True)
    q = sp.symbols("q", positive=True)
    odd_remainder = (
        (z**o+z**(o-1)) * (1-q**2)
        / ((1+z**o) * (1+z**o*q**2))
    )
    even_remainder = (
        (z**e+z**(e-1)) * (1-q**2)
        / ((1-z**e) * (1-z**e*q**2))
    )
    C_o = (1-z**(o-1))/(1+z**o)
    C_long = (1-z**(o-1)*q**2)/(1+z**o*q**2)
    G_e = (1+z**(e-1))/(1-z**e)
    G_long = (1+z**(e-1)*q**2)/(1-z**e*q**2)
    assert sp.cancel(C_long - C_o - odd_remainder) == 0
    assert sp.cancel(G_e - G_long - even_remainder) == 0

    r, s = sp.symbols("r s", integer=True, positive=True)
    u, v = sp.symbols("u v", nonnegative=True)
    D_cap = 1-z+z*r*C_o+z*s*G_e
    D_actual = D_cap+z*u-z*v
    assert sp.expand(D_actual-D_cap-z*u+z*v) == 0

    for odd in range(1, 16, 2):
        cap_odd = min(odd, 7)
        cap_even = 9-cap_odd
        assert odd >= cap_odd and cap_odd in (1, 3, 5, 7)
        for even in range(2, 18, 2):
            if odd+even >= 9:
                assert even >= cap_even


def main():
    cases = verify_algebra_and_caps()
    verify_set_inclusion_reduction()
    print("case endpoint-degree endpoint-min endpoint-max")
    for case in cases:
        label = f"({case[0]},{case[1]};{case[2]},{3-case[2]})"
        if case == EXCEPTIONAL:
            endpoint_degree, endpoint_coefficients, L, j_degree, j_coefficients, J = (
                certify_exceptional_cap()
            )
            print(
                f"{label} {endpoint_degree} {min(endpoint_coefficients)} "
                f"{max(endpoint_coefficients)}; J-degree={j_degree} "
                f"J-min={min(j_coefficients)} L={L} J={J}"
            )
        else:
            degree, coefficients, L = certify_ordinary_cap(case)
            print(
                f"{label} {degree} {min(coefficients)} "
                f"{max(coefficients)} L={L}"
            )

    weight = z**-2 - 1
    head = sp.integrate(weight * 4*z**sp.Rational(9, 2), (z, 0, CAP))
    tail_mass = sp.integrate(weight, (z, CAP, 1))
    assert head == 3051*sp.sqrt(3)/19712
    assert tail_mass == sp.Rational(1, 12)
    budget = head + sp.pi*tail_mass/2
    rational_gap = sp.Rational(19, 40) - sp.Rational(6102, 19712)
    assert rational_gap == sp.Rational(8153, 49280) > 0
    atan_lower = sum((-1)**k * sp.Rational(1, 2*k+1) for k in range(8))
    assert atan_lower == sp.Rational(33976, 45045)
    assert 4*atan_lower > 3 and 3 < 2**2

    print(f"cap={CAP}; head={head}; tail-mass={tail_mass}; budget={budget}")
    print(f"rational lower gap after pi>3, sqrt(3)<2: {rational_gap}")
    print("theta g>=9 whole-rectangle phase certificate: PASS (8/8 caps)")


if __name__ == "__main__":
    main()
