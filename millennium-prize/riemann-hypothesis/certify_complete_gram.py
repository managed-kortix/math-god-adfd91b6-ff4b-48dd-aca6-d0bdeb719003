#!/usr/bin/env python3
"""Certified complete restricted energies and adaptive block diagnostics.

The calculation uses the finite Vasyunin cotangent formula for the full
fractional-part Gram matrix and subtracts its exact rank-one x > 1 tail.
All transcendental operations are performed by Arb through python-flint.

The adaptive output is finite diagnostic data.  It does not prove that a
stopping time exists at every later scale or that one kappa works eventually.
"""

import argparse
from dataclasses import dataclass

from flint import arb, ctx


def mobius_sieve(limit):
    mu = [0] * (limit + 1)
    composite = [False] * (limit + 1)
    primes = []
    mu[1] = 1
    for n in range(2, limit + 1):
        if not composite[n]:
            primes.append(n)
            mu[n] = -1
        for p in primes:
            if n * p > limit:
                break
            composite[n * p] = True
            if n % p == 0:
                mu[n * p] = 0
                break
            mu[n * p] = -mu[n]
    return mu


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


class RestrictedGram:
    """Arb evaluator for <rho_a,rho_b> over (0,1)."""

    def __init__(self):
        self._vasyunin = {}
        self._entries = {}
        self.pi = arb.pi()
        self.c0 = (2 * self.pi).log() - arb.const_euler()

    def v(self, p, q):
        if q == 1:
            return arb(0)
        key = (p % q, q)
        if key not in self._vasyunin:
            self._vasyunin[key] = sum(
                (arb((k * p) % q) / q)
                * (self.pi * k / q).cot()
                for k in range(1, q)
            )
        return self._vasyunin[key]

    def entry(self, a, b):
        key = (min(a, b), max(a, b))
        if key in self._entries:
            return self._entries[key]
        d = gcd(a, b)
        p, q = a // d, b // d
        lcm = a * b // d
        full = (
            arb(q - p) * (arb(p) / q).log()
            + arb(p + q) * self.c0
            - self.pi * (self.v(p, q) + self.v(q, p))
        ) / (2 * lcm)
        value = full - arb(1) / (a * b)
        self._entries[key] = value
        return value

    @staticmethod
    def chi_cross(a):
        return (arb(a).log() + 1 - arb.const_euler()) / a


def complete_energies(limit, bits=192):
    """Return rigorous Arb enclosures for P_N, 2 <= N <= limit."""
    if limit < 2:
        raise ValueError("limit must be at least 2")
    ctx.prec = bits
    mu = mobius_sieve(limit)
    logs = [arb(0)] + [arb(n).log() for n in range(1, limit + 1)]
    gram = RestrictedGram()

    # At N=2, F_N = chi + rho_1.  Keep the scalar Gram data for
    # U_m=chi+sum_{a<=m}mu(a)rho_a and D_m=sum mu(a)log(a)rho_a.
    u2 = arb(1) + 2 * gram.chi_cross(1) + gram.entry(1, 1)
    ud = arb(0)
    d2 = arb(0)
    energies = {}

    for N in range(2, limit + 1):
        log_N = logs[N]
        energies[N] = u2 - 2 * ud / log_N + d2 / (log_N * log_N)

        m = mu[N]
        if not m or N == limit:
            continue
        row_u = gram.chi_cross(N)
        row_d = arb(0)
        for a in range(1, N):
            if mu[a]:
                g = gram.entry(a, N)
                row_u += mu[a] * g
                row_d += mu[a] * logs[a] * g
        diagonal = gram.entry(N, N)
        old_u2, old_ud, old_d2 = u2, ud, d2
        u2 = old_u2 + 2 * m * row_u + m * m * diagonal
        ud = (
            old_ud + m * row_d + m * logs[N] * row_u
            + m * m * logs[N] * diagonal
        )
        d2 = old_d2 + 2 * m * logs[N] * row_d + m * m * logs[N] ** 2 * diagonal
    return energies


def block_ratio(energies, a, b):
    """Enclose (P_a-P_b)/(2 sum_[a,b) h_n log(n) P_n)."""
    if not (2 <= a < b and b in energies):
        raise ValueError("block endpoints are outside the energy table")
    denominator = arb(0)
    for n in range(a, b):
        h = 1 / arb(n).log() - 1 / arb(n + 1).log()
        denominator += 2 * h * arb(n).log() * energies[n]
    return (energies[a] - energies[b]) / denominator


@dataclass(frozen=True)
class AdaptiveBlock:
    start: int
    stop: int
    ratio: object


def adaptive_chain(energies, start, stop, kappa):
    """Choose the first certified endpoint whose complete ratio exceeds kappa."""
    if start < 2 or stop not in energies or start >= stop:
        raise ValueError("invalid adaptive range")
    threshold = arb(str(kappa))
    blocks = []
    a = start
    while a < stop:
        accepted = None
        for b in range(a + 1, stop + 1):
            ratio = block_ratio(energies, a, b)
            if ratio > threshold:
                accepted = AdaptiveBlock(a, b, ratio)
                break
        if accepted is None:
            return blocks, a
        blocks.append(accepted)
        a = accepted.stop
    return blocks, None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-N", type=int, default=128)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--start", type=int, default=2)
    parser.add_argument("--kappa", default="0.4")
    parser.add_argument("--show-energies", action="store_true")
    args = parser.parse_args()

    energies = complete_energies(args.max_N, args.bits)
    print("CERTIFIED FINITE DIAGNOSTIC ONLY; NOT AN ASYMPTOTIC THEOREM OR RH PROOF")
    print(f"Arb precision={args.bits} bits, complete P_N range=2..{args.max_N}")
    if args.show_energies:
        for N, value in energies.items():
            print(f"P_{N} in {value}")

    blocks, failure = adaptive_chain(
        energies, args.start, args.max_N, args.kappa
    )
    print(f"first-passage chain for certified ratio > {args.kappa}:")
    for block in blocks:
        print(
            f"  [{block.start},{block.stop})  b/a={block.stop / block.start:.6g}"
            f"  ratio in {block.ratio}"
        )
    if failure is None:
        print(f"finite chain reaches {args.max_N}; blocks={len(blocks)}")
    else:
        print(f"no certified stopping endpoint <= {args.max_N} from a={failure}")


if __name__ == "__main__":
    main()
