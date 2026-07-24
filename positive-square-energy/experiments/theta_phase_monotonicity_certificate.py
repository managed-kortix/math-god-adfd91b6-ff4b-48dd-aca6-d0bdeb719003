#!/usr/bin/env python3
"""Exact c -> c+4 theta phase-monotonicity certificate.

The only dependency is SymPy.  All arithmetic used by the checks is exact.
"""

from itertools import product
from math import comb

import sympy as sp


z, q = sp.symbols("z q")


def f(length):
    """The checked-in path factor f_l=1-(-z)^l."""
    return 1 - (-z) ** length


def interpolated_phase(a, b, c0):
    """Reconstruct N,P,Q,R,T for c=c0+4k, with q=z^k."""
    fc = 1 - (-1) ** c0 * z**c0 * q**4
    fcm1 = 1 - (-1) ** (c0 - 1) * z ** (c0 - 1) * q**4
    F = f(a) * f(b) * fc
    N = (1 - z) * F + z * (
        f(a - 1) * f(b) * fc
        + f(b - 1) * f(a) * fc
        + fcm1 * f(a) * f(b)
    )
    P = sp.S.Zero
    Q = sp.S.Zero
    for length, complement in ((a, f(b) * fc), (b, f(a) * fc)):
        if length % 2:
            P += (-1) ** ((length - 1) // 2) * z ** ((length - 1) // 2) * complement
        else:
            Q += (-1) ** (length // 2) * z ** (length // 2 - 1) * complement
    complement = f(a) * f(b)
    if c0 % 2:
        P += (-1) ** ((c0 - 1) // 2) * z ** ((c0 - 1) // 2) * q**2 * complement
    else:
        Q += (-1) ** (c0 // 2) * z ** (c0 // 2 - 1) * q**2 * complement
    N, P, Q = map(sp.expand, (N, P, Q))
    R = sp.expand(N**2 + z * (1 + z) ** 2 * (P**2 - z * Q**2))
    T = sp.expand(2 * z * (1 + z) ** 2 * P * Q)
    return N, P, Q, R, T


def direct_phase(a, b, c):
    """Independently reconstruct N,P,Q,R,T at one integer c."""
    lengths = (a, b, c)
    F = sp.prod(f(length) for length in lengths)
    N = (1 - z) * F + z * sum(
        f(length - 1) * sp.prod(f(other) for j, other in enumerate(lengths) if j != i)
        for i, length in enumerate(lengths)
    )
    P = sum(
        (-1) ** ((length - 1) // 2)
        * z ** ((length - 1) // 2)
        * sp.prod(f(other) for j, other in enumerate(lengths) if j != i)
        for i, length in enumerate(lengths)
        if length % 2
    )
    Q = sum(
        (-1) ** (length // 2)
        * z ** (length // 2 - 1)
        * sp.prod(f(other) for j, other in enumerate(lengths) if j != i)
        for i, length in enumerate(lengths)
        if not length % 2
    )
    N, P, Q = map(sp.expand, (N, P, Q))
    R = sp.expand(N**2 + z * (1 + z) ** 2 * (P**2 - z * Q**2))
    T = sp.expand(2 * z * (1 + z) ** 2 * P * Q)
    return N, P, Q, R, T


def power_to_bernstein(poly, variables=(z, q)):
    """Convert an exact multivariate power polynomial on [0,1]^d."""
    power = sp.Poly(sp.expand(poly), *variables)
    degrees = tuple(power.degree(variable) for variable in variables)
    coefficients = {}
    for index in product(*(range(degree + 1) for degree in degrees)):
        value = sp.S.Zero
        for exponent in product(*(range(i + 1) for i in index)):
            weight = sp.prod(
                sp.Rational(comb(i, e), comb(degree, e))
                for i, e, degree in zip(index, exponent, degrees)
            )
            value += power.coeff_monomial(sp.prod(v**e for v, e in zip(variables, exponent))) * weight
        coefficients[index] = sp.factor(value)
    return degrees, coefficients


def bernstein_to_power(degrees, coefficients, variables=(z, q)):
    """Inverse expansion, used to audit the conversion itself."""
    answer = sp.S.Zero
    for index, value in coefficients.items():
        basis = sp.prod(
            comb(degree, i) * variable**i * (1 - variable) ** (degree - i)
            for variable, degree, i in zip(variables, degrees, index)
        )
        answer += value * basis
    return sp.expand(answer)


RESIDUALS = {
    ("23", 0): "q^4*z^12+q^4*z^11-q^4*z^10-q^4*z^9+2*q^4*z^8+q^2*z^9+q^2*z^8-q^2*z^7+2*q^2*z^6-q^2*z^5+q^2*z^4+q^2*z^3+2*z^4-z^3-z^2+z+1",
    ("23", 1): "z^4+z^3-2*z^2+z+1",
    ("23", 2): "q^4*z^14+q^4*z^13-q^4*z^12-q^4*z^11+2*q^4*z^10-q^2*z^10-q^2*z^9+q^2*z^8-2*q^2*z^7+q^2*z^6-q^2*z^5-q^2*z^4+2*z^4-z^3-z^2+z+1",
    ("23", 3): "z^4+z^3-2*z^2+z+1",
    ("14", 0): "q^4*z^14+q^4*z^13-2*q^4*z^12+3*q^4*z^11-3*q^4*z^10+3*q^4*z^9-2*q^4*z^8+q^4*z^7-q^2*z^10-q^2*z^8-q^2*z^6-q^2*z^4+z^7-2*z^6+3*z^5-3*z^4+3*z^3-2*z^2+z+1",
    ("14", 1): "q^4*z^12+q^4*z^10-q^4*z^9+q^4*z^8+q^2*z^9+q^2*z^7+q^2*z^5+q^2*z^3+z^4-z^3+z^2+1",
    ("14", 2): "q^4*z^16+q^4*z^15-2*q^4*z^14+3*q^4*z^13-3*q^4*z^12+3*q^4*z^11-2*q^4*z^10+q^4*z^9+q^2*z^11+q^2*z^9+q^2*z^7+q^2*z^5+z^7-2*z^6+3*z^5-3*z^4+3*z^3-2*z^2+z+1",
    ("14", 3): "q^4*z^14+q^4*z^12-q^4*z^11+q^4*z^10-q^2*z^10-q^2*z^8-q^2*z^6-q^2*z^4+z^4-z^3+z^2+1",
}


EXPECTED_STATS = {
    ("23", 0): ((12, 4), 65, 65, 0, sp.Integer(1), sp.Integer(8)),
    ("23", 1): ((4, 0), 5, 5, 0, sp.Integer(1), sp.Integer(2)),
    ("23", 2): ((14, 4), 75, 72, 3, sp.Integer(0), sp.Integer(2)),
    ("23", 3): ((4, 0), 5, 5, 0, sp.Integer(1), sp.Integer(2)),
    ("14", 0): ((14, 4), 75, 72, 3, sp.Integer(0), sp.Integer(2)),
    ("14", 1): ((12, 4), 65, 65, 0, sp.Integer(1), sp.Integer(8)),
    ("14", 2): ((16, 4), 85, 85, 0, sp.Integer(1), sp.Integer(8)),
    ("14", 3): ((14, 4), 75, 72, 3, sp.Integer(0), sp.Integer(2)),
}


def expected_prefactor(name, residue):
    common = 2 * q**2 * (z - 1) ** 3 * (z + 1) ** 10
    if name == "14":
        common *= (z**2 + 1) ** 2
    else:
        common *= (z**2 - z + 1) ** 2
    data = {
        ("23", 0): -z**3 * (q*z-1)*(q*z+1)*(q*z**2-1)*(q*z**2+1)*(q**2*z**2+1)*(q**2*z**4+1),
        ("23", 1): -z**3 * (q*z**2-1)*(q*z**2+1)*(q*z**3-1)*(q*z**3+1)*(q**4*z**5+1)*(q**4*z**9+1),
        ("23", 2): z**4 * (q**2*z**3-1)*(q**2*z**3+1)*(q**2*z**5-1)*(q**2*z**5+1),
        ("23", 3): z**4 * (q**2*z**5+1)*(q**2*z**7+1)*(q**4*z**7+1)*(q**4*z**11+1),
        ("14", 0): z**2 * (q*z-1)*(q*z+1)*(q*z**2-1)*(q*z**2+1)*(q**2*z**2+1)*(q**2*z**4+1),
        ("14", 1): z**4 * (q**4*z**5+1)*(q**4*z**9+1),
        ("14", 2): -z**3 * (q**2*z**3-1)*(q**2*z**3+1)*(q**2*z**5-1)*(q**2*z**5+1),
        ("14", 3): -z**5 * (q**4*z**7+1)*(q**4*z**11+1),
    }
    return sp.expand(common * data[(name, residue)])


def main():
    cases = {"23": (2, 3), "14": (1, 4)}
    directions = {"23": (1, 1, -1, -1), "14": (-1, -1, 1, 1)}
    print("family residue direction degree count positive zero min max")
    for name, (a, b) in cases.items():
        for residue in range(4):
            c0 = 4 + residue
            N, P, Q, R, T = interpolated_phase(a, b, c0)
            Rq, Tq = R.subs(q, z*q), T.subs(q, z*q)
            cross = sp.expand(R*Tq - T*Rq)
            residual = sp.sympify(RESIDUALS[(name, residue)])
            assert sp.expand(cross - expected_prefactor(name, residue)*residual) == 0

            degrees, coefficients = power_to_bernstein(residual)
            assert bernstein_to_power(degrees, coefficients) == sp.expand(residual)
            values = list(coefficients.values())
            stats = (degrees, len(values), len([v for v in values if v > 0]),
                     len([v for v in values if v == 0]), min(values), max(values))
            assert stats == EXPECTED_STATS[(name, residue)]
            assert all(value >= 0 for value in values) and any(value > 0 for value in values)

            direction = directions[name][residue]
            for k in (1, 2):
                direct = direct_phase(a, b, c0 + 4*k)
                for interpolated, concrete in zip((N, P, Q, R, T), direct):
                    assert sp.expand(interpolated.subs(q, z**k) - concrete) == 0
                next_direct = direct_phase(a, b, c0 + 4*k + 4)
                direct_cross = sp.expand(direct[3]*next_direct[4] - direct[4]*next_direct[3])
                assert sp.expand(cross.subs(q, z**k) - direct_cross) == 0
                for point in (sp.Rational(1, 3), sp.Rational(1, 2), sp.Rational(2, 3)):
                    assert sp.sign(direct_cross.subs(z, point)) == direction

            arrow = "increasing" if direction > 0 else "decreasing"
            print(name, residue, arrow, *degrees, stats[1], stats[2], stats[3], stats[4], stats[5])
    print("theta phase monotonicity certificate: PASS")


if __name__ == "__main__":
    main()
