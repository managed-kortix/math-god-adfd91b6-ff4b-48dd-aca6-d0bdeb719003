#!/usr/bin/env python3
"""Exact-rational audit of the Cycle 45 Mobius/sign normalization.

Arbitrary nonzero rational stand-ins isolate the coefficient algebra from all
transcendental evaluation.  For every tested squarefree q this checks that

  mu(q)[beta(q) + sum_d mu(d)W(q,d)]

is exactly the direct signed probe row with G_qd=mu(q)mu(d)W(q,d) and
G_q0=mu(q)beta(q).  This is a coefficient/sign audit, not a numerical check
of the analytic Gram formulas.
"""

from fractions import Fraction
from math import gcd


def mobius_sieve(limit):
    mu = [0] * (limit + 1)
    mu[1] = 1
    composite = [False] * (limit + 1)
    primes = []
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


def audit(start):
    mu = mobius_sieve(2 * start)
    squarefree = [d for d in range(1, 2 * start) if mu[d]]
    # Independent exact rational stand-ins for H, the spatial Gram, and beta.
    H = {
        (q, d): Fraction((q + d) % 11 + 1, q * d + 1)
        for q in squarefree for d in squarefree
    }
    spatial = {
        (q, d): Fraction(gcd(q, d), q * d)
        for q in squarefree for d in squarefree
    }
    beta = {q: Fraction(-q, 3 * q + 1) for q in squarefree}

    for q in squarefree:
        def W(d):
            return spatial[q, d] * H[q, d]

        hat_c = beta[q] + sum(
            (Fraction(mu[d]) * W(d) for d in squarefree), Fraction(0)
        )
        signed_from_hat = Fraction(mu[q]) * hat_c
        direct_signed_row = Fraction(mu[q]) * beta[q] + sum(
            (Fraction(mu[q] * mu[d]) * W(d) for d in squarefree),
            Fraction(0),
        )
        if signed_from_hat != direct_signed_row:
            raise RuntimeError(("exact sign identity failed", start, q))
    return len(squarefree)


def main():
    for start in (4, 8, 16):
        rows = audit(start)
        print(f"a={start}: exact rational coefficient identity PASS ({rows} rows)")


if __name__ == "__main__":
    main()
