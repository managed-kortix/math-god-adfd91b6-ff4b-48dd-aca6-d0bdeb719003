#!/usr/bin/env python3
"""Rigorous finite Arb verification of lambda_(n+1)-lambda_n > 0.

This proves only the requested finite list of inequalities, not their uniform
continuation and not the Riemann hypothesis.
"""

import argparse

import flint
from flint import arb, arb_series, ctx


def li_coefficients(count, bits):
    """Return balls for lambda_1,...,lambda_count."""
    old_prec, old_cap = ctx.prec, ctx.cap
    try:
        ctx.prec = bits
        ctx.cap = count + 1
        x = arb_series([0, 1])
        # By xi(s)=xi(1-s), evaluate near zero and avoid zeta's pole at one.
        t = -x / (1 - x)
        xi = ((t - 1) * (1 + t / 2).gamma() * t.zeta()
              * (-t * arb.pi().log() / 2).exp())
        series = (2 * xi).log()
        if not series[0].contains(0):
            raise ArithmeticError("log(2 xi(1)) normalization failed")
        return [None] + [n * series[n] for n in range(1, count + 1)]
    finally:
        ctx.prec, ctx.cap = old_prec, old_cap


def certify(max_n, initial_bits=128, max_bits=8192):
    bits = initial_bits
    while bits <= max_bits:
        lam = li_coefficients(max_n + 1, bits)
        diffs = [None] + [lam[n + 1] - lam[n]
                          for n in range(1, max_n + 1)]
        unresolved = []
        for n in range(1, max_n + 1):
            if diffs[n].lower() > 0:
                continue
            if diffs[n].upper() <= 0:
                raise ArithmeticError(
                    f"certified nonpositive difference at n={n}: {diffs[n]}")
            unresolved.append(n)
        if not unresolved:
            return bits, lam, diffs
        bits *= 2
    raise ArithmeticError(f"unresolved through {max_n} at {max_bits} bits")


def self_test():
    lam = li_coefficients(5, 256)
    old_prec = ctx.prec
    try:
        ctx.prec = 256
        exact = 1 + arb.const_euler() / 2 - (4 * arb.pi()).log() / 2
        if not lam[1].overlaps(exact):
            raise AssertionError((lam[1], exact))
        expected = [
            None,
            arb("0.0230957089661210 +/- 1e-15"),
            arb("0.0923457352280467 +/- 1e-15"),
            arb("0.2076389205543250 +/- 1e-15"),
            arb("0.3687904794922420 +/- 1e-15"),
            arb("0.5755427144611770 +/- 1e-15"),
        ]
        for n in range(1, 6):
            if not lam[n].overlaps(expected[n]):
                raise AssertionError((n, lam[n], expected[n]))
    finally:
        ctx.prec = old_prec
    certify(10, 96, 1024)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("max_n", type=int)
    parser.add_argument("--bits", type=int, default=128)
    parser.add_argument("--max-bits", type=int, default=8192)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.max_n < 1:
        raise SystemExit("max_n must be positive")
    if args.self_test:
        self_test()
    bits, _, diffs = certify(args.max_n, args.bits, args.max_bits)
    weakest = min(range(1, args.max_n + 1), key=lambda n: diffs[n].lower())
    print(f"python-flint {flint.__version__}")
    print(f"PASS D_n=lambda_(n+1)-lambda_n>0 for 1<=n<={args.max_n}")
    print(f"precision={bits} bits; weakest index={weakest}; ball={diffs[weakest]}")


if __name__ == "__main__":
    main()
