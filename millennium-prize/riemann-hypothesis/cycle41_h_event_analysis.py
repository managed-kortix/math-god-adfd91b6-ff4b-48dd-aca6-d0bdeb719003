#!/usr/bin/env python3
"""Certified event decomposition for the Cycle 41 H_n negative bands."""

import argparse
from math import isqrt

from flint import arb, ctx

from certify_complete_gram import RestrictedGram, mobius_sieve


def factorization(n):
    factors = []
    p = 2
    while p <= isqrt(n):
        if n % p:
            p = 3 if p == 2 else p + 2
            continue
        exponent = 0
        while n % p == 0:
            n //= p
            exponent += 1
        factors.append((p, exponent))
        p = 3 if p == 2 else p + 2
    if n > 1:
        factors.append((n, 1))
    return factors


def event_name(q, mu_q):
    factors = factorization(q)
    if len(factors) == 1 and factors[0][1] == 1:
        return "prime"
    if mu_q == 0:
        return "nonsquarefree"
    return "squarefree-composite"


def h_event_rows(limit, bits=192):
    """Return H_n and the exact three-term update decomposition through limit."""
    if limit < 3:
        raise ValueError("limit must be at least 3")
    ctx.prec = bits
    mu = mobius_sieve(limit)
    logs = [arb(0)] + [arb(n).log() for n in range(1, limit + 2)]
    gram = RestrictedGram()

    u2 = arb(1) + 2 * gram.chi_cross(1) + gram.entry(1, 1)
    ud = arb(0)
    d2 = arb(0)
    values = {}
    rows = []

    # Advance U_1,D_1 to U_2,D_2 before evaluating H_2.
    m = mu[2]
    cross_u = gram.chi_cross(2) + mu[1] * gram.entry(1, 2)
    cross_d = mu[1] * logs[1] * gram.entry(1, 2)
    diagonal_gram = gram.entry(2, 2)
    old_u2, old_ud, old_d2 = u2, ud, d2
    u2 = old_u2 + 2 * m * cross_u + m * m * diagonal_gram
    ud = (
        old_ud + m * cross_d + m * logs[2] * cross_u
        + m * m * logs[2] * diagonal_gram
    )
    d2 = (
        old_d2 + 2 * m * logs[2] * cross_d
        + m * m * logs[2] ** 2 * diagonal_gram
    )

    for n in range(2, limit + 1):
        c_n = logs[n] * logs[n + 1]
        values[n] = d2 - c_n * u2
        if n == limit:
            break

        q = n + 1
        m = mu[q]
        c_next = logs[q] * logs[q + 1]
        delta_c = c_next - c_n
        drift = -delta_c * u2
        linear = arb(0)
        diagonal = arb(0)

        if m:
            cross_u = gram.chi_cross(q)
            cross_d = arb(0)
            for a in range(1, q):
                if mu[a]:
                    entry = gram.entry(a, q)
                    cross_u += mu[a] * entry
                    cross_d += mu[a] * logs[a] * entry
            diagonal_gram = gram.entry(q, q)
            linear = 2 * m * (logs[q] * cross_d - c_next * cross_u)
            diagonal = m * m * (logs[q] ** 2 - c_next) * diagonal_gram

            old_u2, old_ud, old_d2 = u2, ud, d2
            u2 = old_u2 + 2 * m * cross_u + m * m * diagonal_gram
            ud = (
                old_ud + m * cross_d + m * logs[q] * cross_u
                + m * m * logs[q] * diagonal_gram
            )
            d2 = (
                old_d2 + 2 * m * logs[q] * cross_d
                + m * m * logs[q] ** 2 * diagonal_gram
            )

        rows.append({
            "n": n,
            "q": q,
            "mu_q": m,
            "event": event_name(q, m),
            "factors": factorization(q),
            "H_n": values[n],
            "drift": drift,
            "linear": linear,
            "diagonal": diagonal,
            "delta_H": drift + linear + diagonal,
        })

    return values, rows


def first_weighted_recovery(values, start):
    total = arb(0)
    trace = []
    for n in range(start, max(values) + 1):
        log_n = arb(n).log()
        log_next = arb(n + 1).log()
        eta = (log_next - log_n) / (log_n * log_next ** 2)
        contribution = eta * values[n]
        total += contribution
        trace.append((n + 1, contribution, total))
        if total >= 0:
            return n + 1, trace
    return None, trace


def sign(value):
    if value.is_zero():
        return "0"
    if value > 0:
        return "+"
    if value < 0:
        return "-"
    return "?"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=240)
    parser.add_argument("--bits", type=int, default=192)
    args = parser.parse_args()
    values, rows = h_event_rows(args.max_n, args.bits)

    windows = ((35, 43), (91, 103), (215, 232))
    print("CERTIFIED FINITE DIAGNOSTIC ONLY; NOT AN ASYMPTOTIC THEOREM OR RH PROOF")
    for low, high in windows:
        print(f"\ntransitions H_n -> H_(n+1), {low} <= n <= {high}:")
        print(" n   q  mu event                   H_n  drift linear diagonal delta  H_(n+1)")
        for row in rows:
            if low <= row["n"] <= high:
                print(
                    f'{row["n"]:3d} {row["q"]:3d} {row["mu_q"]:3d} '
                    f'{row["event"]:22s} {sign(row["H_n"]):>3s}'
                    f' {sign(row["drift"]):>5s} {sign(row["linear"]):>6s}'
                    f' {sign(row["diagonal"]):>8s} {sign(row["delta_H"]):>5s}'
                    f' {sign(values[row["q"]]):>8s}'
                )

    for start in (39, 95, 219, 226):
        stop, trace = first_weighted_recovery(values, start)
        minimum = min(trace, key=lambda item: float(item[2].mid()))
        print(
            f"start {start}: first weighted recovery {stop}, "
            f"minimum at {minimum[0]} in {minimum[2].str(20)}"
        )


if __name__ == "__main__":
    main()
