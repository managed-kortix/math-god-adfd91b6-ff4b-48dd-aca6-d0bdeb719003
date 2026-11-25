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
from cycle45_runtime import require_exact_runtime


def arb_sum(values):
    return sum(values, arb(0))


def require_finite(value, label):
    if not isinstance(value, arb) or not value.is_finite():
        raise RuntimeError(("nonfinite Arb value", label, value))
    return value


def certify_zero_error(value, label, bits):
    require_finite(value, label)
    if not value.contains(0):
        raise RuntimeError(("identity interval excludes zero", label, value))
    upper = abs(value).upper()
    require_finite(upper, f"{label} absolute upper bound")
    ceiling = arb(2) ** (-(bits // 2))
    if not upper <= ceiling:
        raise RuntimeError(("identity interval too wide", label, value,
                            "ceiling", ceiling))
    return upper


def verify(start, bits=256):
    require_exact_runtime()
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
        for label, value in (("w", w[n]), ("A", A[n]),
                             ("eta", eta[n])):
            require_finite(value, f"{label}[{n}]")
        if not A[n] > 0:
            raise RuntimeError(f"unresolved/nonpositive A at n={n}")
    squarefree = [d for d in range(1, stop) if mu[d]]
    rows = [q for q in squarefree if start <= q < stop]
    if not rows:
        raise RuntimeError(("empty squarefree row set", start))

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
        error_upper = certify_zero_error(
            error, f"independent direct identity a={start}, q={q}", bits
        )
        if error_upper > max_error:
            max_error = error_upper
        for label, value in (("beta", beta), ("signed_W", signed_W),
                             ("W2", W2), ("hat_c", hat_c),
                             ("direct", direct)):
            require_finite(value, f"{label}, a={start}, q={q}")
        D += hat_c * hat_c
        Delta += beta * beta + W2

    L = logs[start]
    require_finite(D, f"D, a={start}")
    require_finite(Delta, f"Delta, a={start}")
    if not Delta > 0:
        raise RuntimeError(("nonpositive or unresolved Delta", start, Delta))
    outputs = {
        "L3D": L ** 3 * D,
        "L2Delta": L ** 2 * Delta,
        "LD_over_Delta": L * D / Delta,
    }
    for label, value in outputs.items():
        require_finite(value, f"{label}, a={start}")
    return {
        "a": start,
        "rank": len(rows),
        **outputs,
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
