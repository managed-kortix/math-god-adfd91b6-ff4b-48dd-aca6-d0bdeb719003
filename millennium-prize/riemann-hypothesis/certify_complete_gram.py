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
from math import gcd

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


class RestrictedGram:
    """Arb evaluator for <rho_a,rho_b> over (0,1)."""

    def __init__(self):
        self._vasyunin = {}
        self._cotangent_rows = {}
        self._entries = {}
        self.pi = arb.pi()
        self.c0 = (2 * self.pi).log() - arb.const_euler()

    def v(self, p, q):
        if q == 1:
            return arb(0)
        p %= q
        sign = 1
        if p > q // 2:
            p = q - p
            sign = -1
        key = (p, q)
        if key not in self._vasyunin:
            if q not in self._cotangent_rows:
                self._cotangent_rows[q] = tuple(
                    (self.pi * k / q).cot() / q for k in range(1, q)
                )
            cotangents = self._cotangent_rows[q]
            self._vasyunin[key] = sum(
                (arb((k * p) % q) * cotangents[k - 1]
                 for k in range(1, q)),
                arb(0),
            )
        return sign * self._vasyunin[key]

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


def weighted_prefixes(energies):
    """Return prefix sums of 2 h_n log(n) P_n for O(1) block queries."""
    limit = max(energies)
    prefixes = [arb(0) for _ in range(limit + 1)]
    total = arb(0)
    for n in range(2, limit):
        weight = 2 * (1 - arb(n).log() / arb(n + 1).log())
        total += weight * energies[n]
        prefixes[n + 1] = total
    return prefixes


def block_ratio(energies, a, b, prefixes=None):
    """Enclose (P_a-P_b)/(2 sum_[a,b) h_n log(n) P_n)."""
    if not (2 <= a < b and b in energies):
        raise ValueError("block endpoints are outside the energy table")
    if prefixes is None:
        prefixes = weighted_prefixes(energies)
    denominator = prefixes[b] - prefixes[a]
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
    prefixes = weighted_prefixes(energies)
    a = start
    while a < stop:
        accepted = None
        for b in range(a + 1, stop + 1):
            ratio = block_ratio(energies, a, b, prefixes)
            if ratio > threshold:
                accepted = AdaptiveBlock(a, b, ratio)
                break
        if accepted is None:
            return blocks, a
        blocks.append(accepted)
        a = accepted.stop
    return blocks, None


@dataclass(frozen=True)
class MaximalRatio:
    start: int
    stop: int
    ratio: object


def maximal_ratios(energies, start=2, stop=None):
    """Enclose the finite maximum block ratio from each starting index."""
    if stop is None:
        stop = max(energies)
    if start < 2 or stop not in energies or start >= stop:
        raise ValueError("invalid scan range")
    prefixes = weighted_prefixes(energies)
    maxima = []
    for a in range(start, stop):
        first = block_ratio(energies, a, a + 1, prefixes)
        best_stop = a + 1
        max_lower = first.lower()
        max_upper = first.upper()
        for b in range(a + 2, stop + 1):
            ratio = block_ratio(energies, a, b, prefixes)
            if ratio.lower() > max_lower:
                max_lower = ratio.lower()
                best_stop = b
            if ratio.upper() > max_upper:
                max_upper = ratio.upper()
        maxima.append(MaximalRatio(
            a,
            best_stop,
            arb((max_lower + max_upper) / 2, (max_upper - max_lower) / 2),
        ))
    return maxima


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-N", type=int, default=128)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--start", type=int, default=2)
    parser.add_argument("--kappa", default="0.4")
    parser.add_argument("--show-energies", action="store_true")
    parser.add_argument(
        "--scan-maximal", action="store_true",
        help="scan the maximal certified block ratio from every starting index",
    )
    parser.add_argument(
        "--show-maximal", action="store_true",
        help="print every row of the maximal-ratio scan",
    )
    parser.add_argument(
        "--summary-only", action="store_true",
        help="suppress individual adaptive blocks",
    )
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
    if not args.summary_only:
        for block in blocks:
            print(
                f"  [{block.start},{block.stop})  b/a={block.stop / block.start:.6g}"
                f"  ratio in {block.ratio}"
            )
    if failure is None:
        longest = max(blocks, key=lambda block: block.stop - block.start)
        largest_dilation = max(blocks, key=lambda block: block.stop / block.start)
        print(
            f"finite chain reaches {args.max_N}; blocks={len(blocks)};"
            f" longest=[{longest.start},{longest.stop})"
            f" length={longest.stop - longest.start};"
            f" largest b/a={largest_dilation.stop / largest_dilation.start:.12g}"
            f" at [{largest_dilation.start},{largest_dilation.stop})"
        )
    else:
        print(f"no certified stopping endpoint <= {args.max_N} from a={failure}")

    if args.scan_maximal:
        maxima = maximal_ratios(energies, args.start, args.max_N)
        threshold = arb(str(args.kappa))
        failures = [item for item in maxima if not item.ratio > threshold]
        global_lower = min(item.ratio.lower() for item in maxima)
        global_upper = min(item.ratio.upper() for item in maxima)
        weakest = min(maxima, key=lambda item: item.ratio.lower())
        global_maximal = arb(
            (global_lower + global_upper) / 2,
            (global_upper - global_lower) / 2,
        )
        print(
            f"finite every-start maximal kappa in {global_maximal};"
            f" weakest certified start a={weakest.start},"
            f" witness b={weakest.stop}"
        )
        if args.show_maximal:
            for item in maxima:
                verdict = "PASS" if item.ratio > threshold else "FAIL/UNRESOLVED"
                print(
                    f"  a={item.start} best b={item.stop}"
                    f"  ratio in {item.ratio}  {verdict}"
                )
        if failures:
            item = failures[0]
            print(
                f"first start with no certified ratio > {args.kappa}:"
                f" a={item.start}; best endpoint={item.stop};"
                f" maximal candidate in {item.ratio}"
            )
        else:
            print(
                f"every start a={args.start}..{args.max_N - 1} has a certified"
                f" endpoint <= {args.max_N} with ratio > {args.kappa}"
            )


if __name__ == "__main__":
    main()
