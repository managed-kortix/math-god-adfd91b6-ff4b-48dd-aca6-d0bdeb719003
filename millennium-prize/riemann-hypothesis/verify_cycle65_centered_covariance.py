#!/usr/bin/env python3
"""Certify finite centered-Chebyshev covariance identities for Cycle 65.

For n=N/2 <= k < N, set E_k=psi(k)-k and

    H_k=psi(2k)-2k + k Lambda(2k+1)/(2k+1).

This verifier computes the exact rationally weighted Arb quantities

    A_N = sum E_k^2/(k(k+1)),
    C_N = sum E_k H_k/(k(k+1)),
    T_N = C_N - log(2N) A_N/log(N).

It independently certifies finite Abel formulas for A_N and C_N and the
polarized square identity 2 C_N=A_N+B_N-D_N, where B_N is the H square
energy and D_N is the (H-E) square energy.  These are finite diagnostics;
they are not an asymptotic result and make no claim about RH.
"""

import argparse
from dataclasses import dataclass
from fractions import Fraction

from flint import arb, ctx

from analyze_endpoint_prefix import chebyshev_psi_table
from verify_separated_kernel import ball


SELECTED_N = (4, 64, 220, 8192)


@dataclass(frozen=True)
class CenteredCovarianceResult:
    N: int
    indices: tuple
    weights: tuple
    E: tuple
    H: tuple
    A: object
    C: object
    T: object
    square_H: object
    square_difference: object
    square_covariance: object
    square_T: object
    abel_A_boundary: object
    abel_A_increments: object
    abel_A: object
    abel_C_boundary: object
    abel_C_increments: object
    abel_C: object
    abel_identity_verified: bool
    square_identity_verified: bool
    decomposition_verified: bool
    negative_T_certified: bool


def _weighted_inner(left, right, weights):
    return sum(
        (ball(weight) * a * b for weight, a, b in zip(weights, left, right)),
        arb(0),
    )


def _abel_product(values, start):
    """Abel-sum sum x_k y_k/(k(k+1)) for consecutive Arb pairs."""
    products = tuple(left * right for left, right in values)
    stop = start + len(products) - 1
    boundary = products[0] / start - products[-1] / (stop + 1)
    increments = sum(
        ((products[offset] - products[offset - 1]) / (start + offset)
         for offset in range(1, len(products))),
        arb(0),
    )
    return boundary, increments, boundary + increments


def centered_covariance(N, psi=None):
    """Compute and certify one finite centered covariance certificate."""
    if not isinstance(N, int) or N < 4 or N % 2:
        raise ValueError("N must be an even integer at least 4")
    if psi is None:
        psi = chebyshev_psi_table(2 * N + 1)
    if len(psi) <= 2 * N + 1:
        raise ValueError("psi table must include index 2N+1")

    start = N // 2
    indices = tuple(range(start, N))
    weights = tuple(Fraction(1, k * (k + 1)) for k in indices)
    E = tuple(psi[k] - k for k in indices)
    H = tuple(
        psi[2 * k] - 2 * k
        + ball(Fraction(k, 2 * k + 1))
        * (psi[2 * k + 1] - psi[2 * k])
        for k in indices
    )

    A = _weighted_inner(E, E, weights)
    C = _weighted_inner(E, H, weights)
    log_ratio = ball(2 * N).log() / ball(N).log()
    T = C - log_ratio * A

    square_H = _weighted_inner(H, H, weights)
    difference = tuple(h - e for e, h in zip(E, H))
    square_difference = _weighted_inner(difference, difference, weights)
    square_covariance = (A + square_H - square_difference) / 2
    square_T = (
        (square_H - square_difference) / 2
        + (ball(Fraction(1, 2)) - log_ratio) * A
    )

    A_boundary, A_increments, abel_A = _abel_product(
        tuple(zip(E, E)), start
    )
    C_boundary, C_increments, abel_C = _abel_product(
        tuple(zip(E, H)), start
    )
    abel_verified = A.overlaps(abel_A) and C.overlaps(abel_C)
    square_verified = C.overlaps(square_covariance) and T.overlaps(square_T)

    return CenteredCovarianceResult(
        N, indices, weights, E, H, A, C, T, square_H,
        square_difference, square_covariance, square_T,
        A_boundary, A_increments, abel_A,
        C_boundary, C_increments, abel_C,
        abel_verified, square_verified, abel_verified and square_verified,
        T < 0,
    )


def centered_covariance_values(values=SELECTED_N, bits=192):
    """Compute several certificates with one shared Chebyshev-psi sieve."""
    values = tuple(values)
    if not values:
        raise ValueError("need at least one N")
    if bits < 80:
        raise ValueError("bits must be at least 80")
    for N in values:
        if not isinstance(N, int) or N < 4 or N % 2:
            raise ValueError("N must be an even integer at least 4")
    ctx.prec = bits
    psi = chebyshev_psi_table(2 * max(values) + 1)
    return tuple(centered_covariance(N, psi) for N in values)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--N", type=int, nargs="+", default=list(SELECTED_N))
    args = parser.parse_args()
    try:
        rows = centered_covariance_values(args.N, args.bits)
    except ValueError as error:
        parser.error(str(error))

    print("CERTIFIED FINITE DIAGNOSTIC ONLY; NO RH CLAIM")
    print(f"precision={args.bits} bits")
    for row in rows:
        if not row.decomposition_verified or not row.negative_T_certified:
            raise ArithmeticError(f"certificate failed at N={row.N}")
        print(
            f"N={row.N:5d}: A={row.A.str(16)}; C={row.C.str(16)}; "
            f"T={row.T.str(16)}; Abel/square=verified; T<0=certified"
        )


if __name__ == "__main__":
    main()
