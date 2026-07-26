#!/usr/bin/env python3
"""Exact rational audit of the finite Cycle 43 terminal identity."""

from fractions import Fraction


def verify() -> None:
    # Arbitrary exact data: the identity is algebraic and does not use a
    # special numerical property of the logarithmic weights.
    a, M, K = 2, 7, 11
    w = {n: Fraction(n + 2, 20 * n + 31) for n in range(a, K)}
    beta = {n: Fraction(2 * n + 1, 17 * n + 23) for n in range(a, M)}
    P = {n: Fraction((K - n + 2) ** 2, 37) for n in range(a, K + 1)}

    # Define H from the residual recurrence through M-1.
    H = {
        n: (P[n] - P[n + 1] - w[n] * P[n]) / beta[n]
        for n in range(a, M)
    }
    A = {q: Fraction(q * q + 1, 29) for q in range(a + 1, M)}
    J = {q: H[q] - H[q - 1] + A[q] for q in range(a + 1, M)}

    def tail(start: int) -> Fraction:
        return sum((w[n] * P[n] for n in range(start, K)), Fraction())

    Q = {n: P[n] - tail(n) for n in range(a, M + 1)}
    B = {
        q: sum((beta[n] for n in range(q, M)), Fraction())
        for q in range(a, M)
    }

    telescope = sum((beta[n] * H[n] for n in range(a, M)), Fraction())
    assert Q[a] - Q[M] == telescope

    packet = (
        Q[M]
        + B[a] * H[a]
        - sum((B[q] * A[q] for q in range(a + 1, M)), Fraction())
        + sum((B[q] * J[q] for q in range(a + 1, M)), Fraction())
    )
    assert packet == Q[a]
    print("cycle 43 terminal identity: exact rational audit passed")


if __name__ == "__main__":
    verify()
