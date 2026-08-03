#!/usr/bin/env python3
"""Certified bounded witnesses for the Cycle 264 dyadic cell functional."""

from flint import arb, ctx


def mobius_table(limit):
    mu = [1] * (limit + 1)
    prime = [True] * (limit + 1)
    mu[0] = 0
    for p in range(2, limit + 1):
        if not prime[p]:
            continue
        for multiple in range(p, limit + 1, p):
            prime[multiple] = False
            mu[multiple] *= -1
        for multiple in range(p * p, limit + 1, p * p):
            mu[multiple] = 0
    return mu


def certify_cell(k, u, d, alpha, A, D, C):
    X = sum((u[a] * (k // a) for a in range(1, len(u))), arb(0))
    Y = sum((d[a] * (k // a) for a in range(1, len(d))), arb(0))
    quadratic = 2 * (X - 1) * Y - alpha * Y * Y
    linear = (
        2 * D * (1 - X) - 2 * (A - alpha * D) * Y
    ) * (arb(k + 1) / k).log()
    bracket = C + linear + quadratic / (k * (k + 1))
    return X, Y, quadratic, linear, bracket


def main():
    ctx.prec = 256
    m = 3
    N = 2**m
    alpha = arb(1) / (m + 1)
    mu = mobius_table(2 * N)
    log_n = arb(N).log()
    log_2 = arb(2).log()
    u = [arb(0) for _ in range(2 * N + 1)]
    d = [arb(0) for _ in range(2 * N + 1)]

    for a in range(1, 2 * N + 1):
        if a < N:
            u[a] = mu[a] * (arb(N) / a).log() / log_n
        if 2 <= a <= N:
            d[a] = -mu[a] * arb(a).log() / log_n
        elif N < a < 2 * N:
            d[a] = -mu[a] * (arb(2 * N) / a).log() / log_2

    A = sum((u[a] / a for a in range(1, 2 * N + 1)), arb(0))
    D = sum((d[a] / a for a in range(1, 2 * N + 1)), arb(0))
    C = 2 * A * D - alpha * D * D

    positive = certify_cell(1, u, d, alpha, A, D, C)
    negative = certify_cell(35, u, d, alpha, A, D, C)
    assert not positive[4].contains(0) and positive[4] > 0
    assert not negative[4].contains(0) and negative[4] < 0
    assert not negative[2].contains(0) and negative[2] > 0
    assert not negative[3].contains(0) and negative[3] < 0

    print(f"N={N}, alpha=1/{m + 1}")
    print(f"C={C.str(40)}")
    for k, values in ((1, positive), (35, negative)):
        X, Y, quadratic, linear, bracket = values
        print(f"k={k}")
        print(f"  X={X.str(40)}")
        print(f"  Y={Y.str(40)}")
        print(f"  quadratic numerator={quadratic.str(40)}")
        print(f"  linear piece={linear.str(40)}")
        print(f"  grouped bracket={bracket.str(40)}")


if __name__ == "__main__":
    main()
