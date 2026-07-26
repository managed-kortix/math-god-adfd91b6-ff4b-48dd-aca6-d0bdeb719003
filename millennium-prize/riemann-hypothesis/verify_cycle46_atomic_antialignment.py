#!/usr/bin/env python3
"""Certified finite audit of Cycle 46 restricted atomic antialignment."""

import argparse

from flint import arb, ctx

from certify_complete_gram import RestrictedGram, mobius_sieve


def main(max_n: int = 512, bits: int = 192) -> None:
    ctx.prec = bits
    mu = mobius_sieve(max_n)
    gram = RestrictedGram()
    logs = [arb(0)] + [arb(n).log() for n in range(1, max_n + 1)]
    gamma = arb.const_euler()

    # g[q]=<chi,rho_q> in the restricted space.  The rank-one correction is
    # already inside RestrictedGram.entry and must not be applied to g.
    g = [arb(0)] * (max_n + 1)
    for q in range(1, max_n + 1):
        g[q] = (logs[q] + 1 - gamma) / q

    count = 0
    largest = None
    largest_pair = None
    for M in range(2, max_n + 1):
        coeff = [arb(0)] * (M + 1)
        for a in range(1, M + 1):
            coeff[a] = mu[a] * (1 - logs[a] / logs[M])

        value = arb(0)
        for r in range(1, max_n + 1):
            if mu[r]:
                row = g[r]
                for a in range(1, M + 1):
                    if mu[a]:
                        row += coeff[a] * gram.entry(a, r)
                value += mu[r] * logs[r] * row
            if r >= M:
                assert value < 0, (M, r, value)
                count += 1
                if largest is None or value > largest:
                    largest = value
                    largest_pair = (M, r)

    assert count == (max_n - 1) * max_n // 2
    print(f"certified {count} negative restricted correlations")
    print("largest pair:", largest_pair)
    print("largest value:", largest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=512)
    parser.add_argument("--bits", type=int, default=192)
    args = parser.parse_args()
    main(args.max_n, args.bits)
