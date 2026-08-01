#!/usr/bin/env python3
"""Exact leakage optimization and zero-leakage certificate for Cycle 225."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

from sympy import QQ, groebner, symbols


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "cycle225-quadratic-leakage-certificate.json"


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def neg(p):
    return (-p[0], -p[1])


def det(p, q):
    return p[0] * q[1] - p[1] * q[0]


def norm2(p):
    return p[0] * p[0] + p[1] * p[1]


def ordered_euler_coefficient(p, q):
    """Cycle 212 coefficient for k_perp=(k2,-k1)."""
    return F(-det(p, q), norm2(p))


def canonical_convolution(omega):
    result = {}
    for p, omega_p in omega.items():
        for q, omega_q in omega.items():
            r = add(p, q)
            if r != (0, 0):
                result[r] = result.get(r, F(0)) + ordered_euler_coefficient(p, q) * omega_p * omega_q
    return {r: value for r, value in result.items() if value}


def main() -> None:
    fib = [0, 1]
    for _ in range(8):
        fib.append(fib[-1] + fib[-2])
    rails = {j: (fib[j + 1], fib[j]) for j in range(1, 9)}

    signs = {1: -1, 2: -1}
    for j in range(1, 7):
        signs[j + 2] = -det(rails[j], rails[j + 1]) * signs[j] * signs[j + 1]

    epsilon = F(1, 1000)
    amplitudes = {
        j: F(signs[j]) * (F(1) if j in (3, 4, 5) else epsilon)
        for j in range(1, 9)
    }
    omega = {}
    for j in range(1, 9):
        omega[rails[j]] = amplitudes[j]
        omega[neg(rails[j])] = amplitudes[j]

    convolution = canonical_convolution(omega)
    paired_convolution = {}
    modes = list(omega)
    for i, p in enumerate(modes):
        for q in modes[i + 1:]:
            r = add(p, q)
            if r == (0, 0):
                continue
            coefficient = -det(p, q) * (F(1, norm2(p)) - F(1, norm2(q)))
            paired_convolution[r] = paired_convolution.get(r, F(0)) + coefficient * omega[p] * omega[q]
    paired_convolution = {r: value for r, value in paired_convolution.items() if value}
    assert paired_convolution == convolution

    leakage_sq = sum(
        value * value / norm2(r)
        for r, value in convolution.items()
        if r not in omega
    )
    intended_sq = sum(
        convolution.get(r, F(0)) ** 2 / norm2(r) for r in omega
    )
    margin = intended_sq - 16 * leakage_sq
    assert intended_sq > 0 and margin > 0

    rates = []
    for j in range(1, 7):
        p, q, r = rails[j], rails[j + 1], rails[j + 2]
        phase_product = amplitudes[j] * amplitudes[j + 1] * amplitudes[j + 2]
        lower_rate = (
            -4
            * det(p, q)
            * (F(1, norm2(q)) - F(1, norm2(r)))
            * phase_product
        )
        assert lower_rate > 0
        isolated = {
            mode: amplitudes[index]
            for index, rail in ((j, p), (j + 1, q), (j + 2, r))
            for mode in (rail, neg(rail))
        }
        isolated_rhs = canonical_convolution(isolated)
        assert 4 * amplitudes[j] * isolated_rhs[p] == lower_rate
        rates.append(lower_rate)

    # The exterior output m=k7+k8 has only the unordered pair {k7,k8}.
    # Its coefficient is c*z7*z8, c=-det(k7,k8)*(1/|k7|^2-1/|k8|^2).
    exterior_mode = add(rails[7], rails[8])
    exterior_coefficient = F(-det(rails[7], rails[8])) * (
        F(1, norm2(rails[7])) - F(1, norm2(rails[8]))
    )
    assert exterior_coefficient == F(987, 974170)

    x7, y7, x8, y8, t = symbols("x7 y7 x8 y8 t")
    real_product = x7 * x8 - y7 * y8
    imag_product = x7 * y8 + y7 * x8
    nonzero = t * (x7**2 + y7**2) * (x8**2 + y8**2) - 1
    basis = groebner([real_product, imag_product, nonzero], t, x7, y7, x8, y8,
                     order="grevlex", domain=QQ)
    assert list(basis) == [1]
    certificate = t * real_product**2 + t * imag_product**2 - nonzero
    assert certificate.expand() == 1

    artifact = {
        "convention": {
            "k_perp": "(k2,-k1)",
            "ordered_euler_coefficient": "-det(p,q)/|p|^2",
        },
        "decision": {
            "threshold_packet_exists": True,
            "zero_first_order_exterior_leakage_with_six_nonzero_triads": False,
        },
        "rails": {str(j): list(rails[j]) for j in range(1, 9)},
        "packet": {
            "epsilon": str(epsilon),
            "real_amplitudes": {str(j): str(amplitudes[j]) for j in range(1, 9)},
            "phases": {str(j): ("0" if amplitudes[j] > 0 else "pi") for j in range(1, 9)},
            "lower_receiver_rates": [str(rate) for rate in rates],
            "leakage_hminus1_squared": str(leakage_sq),
            "intended_hminus1_squared": str(intended_sq),
            "ratio": str(leakage_sq / intended_sq),
            "threshold_margin_I2_minus_16L2": str(margin),
        },
        "zero_leakage_certificate": {
            "exterior_mode": list(exterior_mode),
            "coefficient": str(exterior_coefficient),
            "generators": [
                "f=x7*x8-y7*y8",
                "g=x7*y8+y7*x8",
                "h=t*(x7^2+y7^2)*(x8^2+y8^2)-1",
            ],
            "groebner_basis_Q": ["1"],
            "bezout_identity": "t*f^2+t*g^2-h=1",
        },
    }
    OUTPUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="ascii")

    print("Cycle 225 exact quadratic leakage gate")
    print("L^2/I^2 =", leakage_sq / intended_sq)
    print("I^2 - 16 L^2 =", margin)
    print("six isolated-triad lower-receiver rates are positive")
    print("canonical ordered/pair-symmetrized convolution cross-test passed")
    print("zero-leakage saturated Groebner basis = [1]")
    print("certificate: t*f^2 + t*g^2 - h = 1")
    print("wrote", OUTPUT)


if __name__ == "__main__":
    main()
