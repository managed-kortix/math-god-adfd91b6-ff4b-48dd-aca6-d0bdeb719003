#!/usr/bin/env python3
"""Certified finite sign diagnostics for the Cycle 40 norm difference H_n."""

import argparse

from flint import arb, ctx

from certify_complete_gram import RestrictedGram, mobius_sieve


def h_values(limit, bits=192):
    """Return H_n = ||D_n||^2-log(n)log(n+1)||U_n||^2 for 2 <= n <= limit."""
    if limit < 2:
        raise ValueError("limit must be at least 2")
    ctx.prec = bits
    mu = mobius_sieve(limit)
    logs = [arb(0)] + [arb(n).log() for n in range(1, limit + 2)]
    gram = RestrictedGram()

    # U_1 = chi + rho_1 and D_1 = 0.
    u2 = arb(1) + 2 * gram.chi_cross(1) + gram.entry(1, 1)
    ud = arb(0)
    d2 = arb(0)
    values = {}

    for n in range(2, limit + 1):
        m = mu[n]
        if m:
            row_u = gram.chi_cross(n)
            row_d = arb(0)
            for a in range(1, n):
                if mu[a]:
                    entry = gram.entry(a, n)
                    row_u += mu[a] * entry
                    row_d += mu[a] * logs[a] * entry
            diagonal = gram.entry(n, n)
            old_u2, old_ud, old_d2 = u2, ud, d2
            u2 = old_u2 + 2 * m * row_u + m * m * diagonal
            ud = (
                old_ud + m * row_d + m * logs[n] * row_u
                + m * m * logs[n] * diagonal
            )
            d2 = old_d2 + 2 * m * logs[n] * row_d + m * m * logs[n] ** 2 * diagonal
        values[n] = d2 - logs[n] * logs[n + 1] * u2
    return values


def first_nonnegative_blocks(values):
    """Find first b with sum_[a,b) eta_n H_n >= 0 at every available start."""
    last = max(values)
    result = {}
    for a in range(2, last + 1):
        total = arb(0)
        endpoint = None
        for n in range(a, last + 1):
            log_n = arb(n).log()
            log_next = arb(n + 1).log()
            eta = (log_next - log_n) / (log_n * log_next ** 2)
            total += eta * values[n]
            if total >= 0:
                endpoint = n + 1
                break
        result[a] = (endpoint, total)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=512)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--show-negative", action="store_true")
    args = parser.parse_args()

    values = h_values(args.max_n, args.bits)
    negative = [n for n, value in values.items() if value < 0]
    uncertain = [n for n, value in values.items() if not (value < 0 or value > 0)]
    blocks = first_nonnegative_blocks(values)
    failures = [a for a, (b, _) in blocks.items() if b is None]
    successful = [(b - a, a, b) for a, (b, _) in blocks.items() if b is not None]

    print("CERTIFIED FINITE DIAGNOSTIC ONLY; NOT AN ASYMPTOTIC THEOREM OR RH PROOF")
    print(f"Arb precision={args.bits} bits, H_n range=2..{args.max_n}")
    print(f"positive={len(values) - len(negative) - len(uncertain)} negative={len(negative)} uncertain={len(uncertain)}")
    print(f"negative indices: {negative}")
    if successful:
        wait, start, stop = max(successful)
        print(f"longest first nonnegative weighted block: [{start},{stop}), length {wait}")
    print(f"starts without an endpoint in the available range: {failures}")
    if args.show_negative:
        for n in negative:
            print(f"H_{n} in {values[n]}")


if __name__ == "__main__":
    main()
