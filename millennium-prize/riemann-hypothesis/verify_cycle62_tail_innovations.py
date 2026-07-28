#!/usr/bin/env python3
"""Certify finite-tail Cycle 62 cumulative Omega values with Arb balls.

For the window [M, B), the cells are K_N={M,...,N}.  Floor constraints are
formed exactly over ``fractions.Fraction``.  The only inexact quantities are
logarithms, and those and every matrix operation use Arb through python-flint.

The output is a finite diagnostic for the Cycle 59--61 dual.  It is not an
asymptotic theorem and makes no claim about the Riemann hypothesis.
"""

import argparse
from fractions import Fraction

from flint import arb, arb_mat, ctx


PUBLISHED_K24_220_231 = "0.00108172461837439381"
PUBLISHED_CROSSING_THRESHOLD = "0.0186372067026351066091997"


def mobius_sieve(limit):
    """Return mu(0),...,mu(limit) as exact integers."""
    mu = [0] * (limit + 1)
    composite = bytearray(limit + 1)
    primes = []
    mu[1] = 1
    for n in range(2, limit + 1):
        if not composite[n]:
            primes.append(n)
            mu[n] = -1
        for prime in primes:
            if n * prime > limit:
                break
            composite[n * prime] = 1
            if n % prime == 0:
                break
            mu[n * prime] = -mu[n]
    return mu


def _ball(value):
    if isinstance(value, Fraction):
        return arb(value.numerator) / value.denominator
    return arb(value)


def exact_constraint_rows(M, B, N, mu):
    """Return the Cycle 59 old-U and new-row constraints exactly."""
    cells = range(M, N + 1)
    m = sum((Fraction(mu[a], a) for a in range(1, M)), Fraction())
    rows = [[m] + [Fraction(1 - sum(
        mu[a] * (k // a) for a in range(1, M)
    )) for k in cells]]
    for q in range(M, B):
        rows.append([Fraction(1, q)] + [Fraction(-(k // q)) for k in cells])
    return rows


def cumulative_omega(M, B, N, bits=256):
    """Return a certified Arb enclosure for Omega on cells M through N.

    Individual affine cell moments have inverse energy Gram matrix

        H = [[|K|, lambda^T], [lambda, diag(tau)]].

    Therefore the constrained quotient is the small Schur complement
    ``w'Hw-(CHw)'(CHC')^-1(CHw)``.  This avoids a growing dense nullspace
    solve while retaining the exact rational floor matrix C.
    """
    if not (2 <= M < B <= N + 1):
        raise ValueError("require 2 <= M < B <= N + 1")
    if bits < 80:
        raise ValueError("bits must be at least 80")
    ctx.prec = bits
    mu = mobius_sieve(M - 1)
    cells = list(range(M, N + 1))
    constraints = exact_constraint_rows(M, B, N, mu)
    dimension = len(cells) + 1

    logs = [arb(0)] + [arb(a).log() for a in range(1, N + 2)]
    lambdas = [logs[k + 1] - logs[k] for k in cells]
    taus = [arb(1) / (k * (k + 1)) for k in cells]

    H = arb_mat(dimension, dimension)
    H[0, 0] = len(cells)
    for column, (lam, tau) in enumerate(zip(lambdas, taus), 1):
        H[0, column] = lam
        H[column, 0] = lam
        H[column, column] = tau

    ell = sum(
        (mu[a] * logs[a] / a for a in range(1, M)), arb(0)
    )
    score = [ell]
    for k in cells:
        score.append(-sum(
            (mu[a] * logs[a] * (k // a) for a in range(1, M)), arb(0)
        ))
    w = arb_mat([[value] for value in score])
    C = arb_mat([[_ball(value) for value in row] for row in constraints])

    hw = H * w
    unconstrained = (w.transpose() * hw)[0, 0]
    chc = C * H * C.transpose()
    chw = C * hw
    correction = (chw.transpose() * chc.solve(chw))[0, 0]
    omega = unconstrained - correction
    if not omega >= 0:
        raise ArithmeticError(f"Omega is not certified nonnegative: {omega}")
    return omega


def innovation_table(M, B, endpoints, bits=256):
    """Return ``(N, Omega_N, Omega_N-Omega_previous)`` rows."""
    rows = []
    previous = arb(0)
    for N in endpoints:
        omega = cumulative_omega(M, B, N, bits)
        innovation = omega - previous
        if rows and not innovation >= 0:
            raise ArithmeticError(
                f"innovation at N={N} is not certified nonnegative: {innovation}"
            )
        rows.append((N, omega, innovation))
        previous = omega
    return rows


def dyadic_endpoints(B, max_n):
    """Return B+23 followed by doubled tail lengths up to max_n."""
    endpoints = []
    length = 24
    while B + length - 1 <= max_n:
        endpoints.append(B + length - 1)
        length *= 2
    if not endpoints or endpoints[-1] != max_n:
        endpoints.append(max_n)
    return endpoints


def agrees_with_published_k24(value):
    """Certify agreement with the published 20-significant-digit K24 value."""
    return abs(value - arb(PUBLISHED_K24_220_231)) < arb("5e-20")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--M", type=int, default=220)
    parser.add_argument("--B", type=int, default=231)
    parser.add_argument("--max-n", type=int, default=880)
    parser.add_argument("--bits", type=int, default=256)
    parser.add_argument(
        "--target", type=str, default=PUBLISHED_CROSSING_THRESHOLD,
        help=(
            "decimal threshold whose first sampled crossing is reported "
            "(default: the certified Cycle 62 beta_2+delta threshold)"
        ),
    )
    parser.add_argument(
        "--every", action="store_true",
        help="evaluate every endpoint instead of the compact dyadic table",
    )
    args = parser.parse_args()
    if args.max_n < args.B:
        parser.error("--max-n must be at least B")

    ctx.prec = args.bits
    endpoints = (
        range(args.B, args.max_n + 1) if args.every
        else dyadic_endpoints(args.B, args.max_n)
    )
    target = arb(args.target) if args.target is not None else None
    crossing = None

    print("CERTIFIED FINITE DIAGNOSTIC ONLY; NO RH CLAIM")
    print(f"window=[{args.M},{args.B}) bits={args.bits}")
    print(" N                 Omega_N              table_increment")
    previous = arb(0)
    for N in endpoints:
        omega = cumulative_omega(args.M, args.B, N, args.bits)
        increment = omega - previous
        print(f"{N:4d} {omega.str(20):>24s} {increment.str(20):>28s}")
        if target is not None and crossing is None and omega > target:
            crossing = (N, omega - target)
        previous = omega

    if args.M == 220 and args.B == 231 and args.max_n >= 254:
        k24 = cumulative_omega(220, 231, 254, args.bits)
        print("published K24 agreement:", agrees_with_published_k24(k24))
    if target is not None:
        if crossing is None:
            print(f"no certified crossing of {target} through N={args.max_n}")
        else:
            print(
                f"first sampled certified crossing: N={crossing[0]} "
                f"margin={crossing[1].str(20)}"
            )


if __name__ == "__main__":
    main()
