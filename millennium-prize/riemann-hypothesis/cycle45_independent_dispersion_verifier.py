#!/usr/bin/env python3
"""Independent 256-bit check of selected Cycle 45 dispersion rows.

This script does not import the production Cycle 45 census or CompensatedBlock.
It reconstructs w, A, eta, H, H0, unsigned W, beta, hat_c and a direct X
contraction from the restricted Gram evaluator.  The restricted Vasyunin Gram
and Mobius sieve remain shared dependencies.  All checks use outward Arb
intervals and fail closed.
"""

import argparse

from flint import arb, ctx

from certify_complete_gram import RestrictedGram, mobius_sieve


def arb_sum(values):
    return sum(values, arb(0))


def verify(start, bits=256):
    if bits < 192:
        raise ValueError("independent verification requires at least 192 bits")
    ctx.prec = bits
    theta = arb(2) / 5
    tau = 1 - 2 * theta
    stop = 2 * start
    mu = mobius_sieve(stop)
    gram = RestrictedGram()
    logs = [arb(0)] + [arb(n).log() for n in range(1, stop + 2)]
    w = {n: 1 - logs[n] / logs[n + 1] for n in range(start, stop)}
    A = {
        n: 1 + logs[n] / logs[n + 1] - 2 * theta
        for n in range(start, stop)
    }
    eta = {n: tau / A[n] for n in range(start, stop)}
    for n in range(start, stop):
        if not A[n] > 0:
            raise RuntimeError(f"unresolved/nonpositive A at n={n}")
    squarefree = [d for d in range(1, stop) if mu[d]]
    rows = [q for q in squarefree if start <= q < stop]

    D = arb(0)
    Delta = arb(0)
    max_error = arb(0)
    for q in rows:
        g_q = (logs[q] + 1 - arb.const_euler()) / q
        beta = -g_q * arb_sum(
            w[n] * A[n] * eta[n] * (logs[q] / logs[n] - eta[n])
            for n in range(max(start, q), stop)
        )
        signed_W = arb(0)
        W2 = arb(0)
        for d in squarefree:
            H = arb_sum(
                w[n] * A[n]
                * (logs[q] / logs[n] - eta[n])
                * (logs[d] / logs[n] - eta[n])
                for n in range(max(start, q, d), stop)
            )
            W = gram.entry(q, d) * H
            signed_W += mu[d] * W
            W2 += W * W
        hat_c = beta + signed_W

        direct = arb_sum(
            w[n] * A[n] * (logs[q] / logs[n] - eta[n])
            * (
                -eta[n] * gram.chi_cross(q)
                + arb_sum(
                    mu[d] * (logs[d] / logs[n] - eta[n])
                    * gram.entry(q, d)
                    for d in squarefree if d <= n
                )
            )
            for n in range(max(start, q), stop)
        )
        error = hat_c - direct
        if not error.contains(0):
            raise RuntimeError(("independent direct identity failed", q, error))
        if abs(error).upper() > max_error:
            max_error = abs(error).upper()
        D += hat_c * hat_c
        Delta += beta * beta + W2

    L = logs[start]
    return {
        "a": start,
        "rank": len(rows),
        "L3D": L ** 3 * D,
        "L2Delta": L ** 2 * Delta,
        "LD_over_Delta": L * D / Delta,
        "direct_identity_error_upper_bound": max_error,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--starts", nargs="+", type=int, default=(32, 128))
    parser.add_argument("--bits", type=int, default=256)
    args = parser.parse_args()
    print("INDEPENDENT FINITE CHECK ONLY; SHARED RESTRICTED-GRAM LAYER")
    for start in args.starts:
        row = verify(start, args.bits)
        print(
            row["a"], row["rank"],
            row["L3D"].str(32),
            row["L2Delta"].str(32),
            row["LD_over_Delta"].str(32),
            row["direct_identity_error_upper_bound"].str(8),
        )


if __name__ == "__main__":
    main()
