#!/usr/bin/env python3
"""Diagnostic finite-zero reconnaissance for the shell Gram identity.

This uses mpmath's tabulated/computed critical-line zero ordinates and direct
finite von Mangoldt arithmetic.  It is not an interval calculation, does not
certify zero completeness, and makes no sign claim.  The arithmetic remainder
is defined by the exact finite explicit-formula identity, so adding its full
quadratic correction must recover the directly evaluated shell decrement.
"""

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class AlgebraicDecomposition:
    affine_constant: object
    affine_zero_linear: object
    zero_quadratic: object
    truncated_gram: object
    arithmetic_remainder_correction: object
    recombined_total: object
    direct_total: object


@dataclass(frozen=True)
class FiniteZeroShellReconnaissance:
    N: int
    cutoff: object
    positive_zero_count: int
    positive_ordinates: tuple
    decomposition: AlgebraicDecomposition


def _weighted_inner(weights, left, right):
    return sum((weight * a.conjugate() * b
                for weight, a, b in zip(weights, left, right)), 0)


def _real(value):
    real = getattr(value, "real", None)
    return real if real is not None else value


def decompose_shell_vectors(weights, d0, d1, zero0, zero1,
                            remainder0, remainder1, jump):
    """Algebraically split and reclose a finite affine Gram difference.

    ``d + zero`` is the finite-zero vector and ``d + zero - remainder`` is
    the direct arithmetic vector.  Inputs may be exact real scalars, making
    this helper suitable for algebra-only tests independent of zero data.
    """
    vectors = tuple(tuple(values) for values in (
        weights, d0, d1, zero0, zero1, remainder0, remainder1
    ))
    if not vectors[0] or any(len(values) != len(vectors[0])
                             for values in vectors[1:]):
        raise ValueError("all shell vectors must have the same positive length")
    weights, d0, d1, zero0, zero1, remainder0, remainder1 = vectors
    g0 = tuple(a + z for a, z in zip(d0, zero0))
    g1 = tuple(a + z for a, z in zip(d1, zero1))
    full0 = tuple(g - r for g, r in zip(g0, remainder0))
    full1 = tuple(g - r for g, r in zip(g1, remainder1))

    affine_constant = _real(
        _weighted_inner(weights, d0, d0)
        - _weighted_inner(weights, d1, d1)
    ) - jump
    affine_zero_linear = 2 * _real(
        _weighted_inner(weights, d0, zero0)
        - _weighted_inner(weights, d1, zero1)
    )
    zero_quadratic = _real(
        _weighted_inner(weights, zero0, zero0)
        - _weighted_inner(weights, zero1, zero1)
    )
    truncated = affine_constant + affine_zero_linear + zero_quadratic
    correction = _real(
        -2 * _weighted_inner(weights, g0, remainder0)
        + _weighted_inner(weights, remainder0, remainder0)
        + 2 * _weighted_inner(weights, g1, remainder1)
        - _weighted_inner(weights, remainder1, remainder1)
    )
    direct = _real(
        _weighted_inner(weights, full0, full0)
        - _weighted_inner(weights, full1, full1)
    ) - jump
    return AlgebraicDecomposition(
        affine_constant, affine_zero_linear, zero_quadratic, truncated,
        correction, truncated + correction, direct,
    )


def _mobius_table(limit):
    mu = [1] * (limit + 1)
    prime = [True] * (limit + 1)
    mu[0] = 0
    for p in range(2, limit + 1):
        if not prime[p]:
            continue
        for multiple in range(p, limit + 1, p):
            prime[multiple] = False
            mu[multiple] *= -1
        square = p * p
        for multiple in range(square, limit + 1, square):
            mu[multiple] = 0
    return tuple(mu)


def _arithmetic_tables(limit, mp):
    lambdas = [mp.mpf("0") for _ in range(limit + 1)]
    composite = [False] * (limit + 1)
    for p in range(2, limit + 1):
        if composite[p]:
            continue
        for multiple in range(p + p, limit + 1, p):
            composite[multiple] = True
        power = p
        value = mp.log(p)
        while power <= limit:
            lambdas[power] = value
            power *= p
    psi = [mp.mpf("0")]
    for q in range(1, limit + 1):
        psi.append(psi[-1] + lambdas[q])
    return tuple(lambdas), tuple(psi)


def _A(scale, mu, mp):
    log_scale = mp.log(scale)
    return sum((mu[d] * mp.log(mp.mpf(scale) / d) / (d * log_scale)
                for d in range(1, scale + 1)), mp.mpf("0"))


def _positive_zero_ordinates(cutoff, mp):
    ordinates = []
    index = 1
    while True:
        ordinate = mp.im(mp.zetazero(index))
        if ordinate > cutoff:
            return tuple(ordinates)
        ordinates.append(ordinate)
        index += 1


def reconnoiter_finite_zero_shell(N, cutoff=50, dps=50):
    """Evaluate one small finite-zero shell decomposition with mpmath."""
    if not isinstance(N, int) or N < 4 or N % 2:
        raise ValueError("N must be an even integer at least 4")
    if cutoff <= 0:
        raise ValueError("cutoff must be positive")
    if not isinstance(dps, int) or dps < 30:
        raise ValueError("dps must be an integer at least 30")
    try:
        import mpmath as mp
    except ImportError as exc:
        raise RuntimeError("mpmath is required for numerical reconnaissance") from exc

    mp.mp.dps = dps
    cutoff = mp.mpf(cutoff)
    ordinates = _positive_zero_ordinates(cutoff, mp)
    lambdas, psi = _arithmetic_tables(2 * N, mp)
    mu = _mobius_table(2 * N)
    A_N = _A(N, mu, mp)
    A_2N = _A(2 * N, mu, mp)
    log_N = mp.log(N)
    log_2N = mp.log(2 * N)

    def zero_sum(q):
        log_q = mp.log(q)
        return sum((2 * mp.re(mp.exp((mp.mpf("0.5") + 1j * gamma) * log_q)
                                     / (mp.mpf("0.5") + 1j * gamma))
                    for gamma in ordinates), mp.mpf("0"))

    weights = []
    d0 = []
    d1 = []
    zero0 = []
    zero1 = []
    remainder0 = []
    remainder1 = []
    jump = mp.mpf("0")
    for k in range(N // 2, N):
        theta = mp.mpf(k) / (2 * k + 1)
        p = k * (A_N - 1 / log_N)
        p_plus_h = 2 * k * (A_2N - 1 / log_2N) + theta * A_2N
        B_k = (-mp.log(2 * mp.pi) - mp.log(1 - mp.mpf(k) ** -2) / 2
               + lambdas[k] / 2)
        B_2k = (-mp.log(2 * mp.pi) - mp.log(1 - mp.mpf(2 * k) ** -2) / 2
                + lambdas[2 * k] / 2)
        Z_k = zero_sum(k)
        Z_2k = zero_sum(2 * k)
        r_k = psi[k] - k - B_k + Z_k
        r_2k = psi[2 * k] - 2 * k - B_2k + Z_2k
        weight = mp.mpf(N) / (k * (k + 1))

        weights.append(weight)
        d0.append(p - B_k / log_N)
        d1.append(p_plus_h - (B_2k + theta * lambdas[2 * k + 1]) / log_2N)
        zero0.append(Z_k / log_N)
        zero1.append(Z_2k / log_2N)
        remainder0.append(r_k / log_N)
        remainder1.append(r_2k / log_2N)
        jump += (mp.mpf(N) / (2 * k + 1) ** 2
                 * (A_2N - lambdas[2 * k + 1] / log_2N) ** 2)

    decomposition = decompose_shell_vectors(
        weights, d0, d1, zero0, zero1, remainder0, remainder1, jump
    )
    return FiniteZeroShellReconnaissance(
        N, cutoff, len(ordinates), ordinates, decomposition
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--N", type=int, nargs="+", default=[4, 8, 16, 32])
    parser.add_argument("--T", type=float, default=50.0,
                        help="retain positive mpmath zero ordinates gamma <= T")
    parser.add_argument("--dps", type=int, default=50)
    args = parser.parse_args()

    print("DIAGNOSTIC ONLY: mpmath point values; no zero-completeness, interval, or sign certificate")
    for N in args.N:
        result = reconnoiter_finite_zero_shell(N, args.T, args.dps)
        part = result.decomposition
        mismatch = part.recombined_total - part.direct_total
        print(f"N={N}; T={result.cutoff}; positive-zeros={result.positive_zero_count}")
        print(f"  affine constant (endpoints+jump) = {part.affine_constant}")
        print(f"  affine-zero linear              = {part.affine_zero_linear}")
        print(f"  zero quadratic                  = {part.zero_quadratic}")
        print(f"  finite-zero Gram                = {part.truncated_gram}")
        print(f"  exact-identity arithmetic rest  = {part.arithmetic_remainder_correction}")
        print(f"  recombined / direct decrement   = {part.recombined_total} / {part.direct_total}")
        print(f"  numerical closure residual      = {mismatch}")


if __name__ == "__main__":
    main()
