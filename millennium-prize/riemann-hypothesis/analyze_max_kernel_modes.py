#!/usr/bin/env python3
"""Eigenmode analysis of the first-block max kernel.

The coefficient indices are n=N+1,...,M (M=2N by default), and

    K(n,m) = 1/max(n,m) - 1/(M+1).

The analyzer diagonalizes the exact symmetric tridiagonal K^{-1}, rather than
forming the increasingly ill-conditioned dense kernel.  It projects the actual
vector a_n=mu(n) log(n/N), the Euclidean linear target R, and the completed-
square center c=log(N) K^{-1}R.  SciPy is used only for its stable symmetric
tridiagonal eigensolver.  Optional small cases are independently certified with
Arb eigenvalue/eigenvector balls.
"""

import argparse
from dataclasses import dataclass
from fractions import Fraction
import math

from analyze_endpoint_prefix import chebyshev_psi_table
from analyze_weighted_g_tail import mobius_table
from mobius_endpoint_surrogate import endpoint_channels
from verify_separated_kernel import ball


@dataclass(frozen=True)
class ModeSummary:
    mode: int
    eigenvalue: float
    actual_projection: float
    linear_target_projection: float
    center_projection: float
    quadratic: float
    linear: float
    tracking: float


@dataclass(frozen=True)
class Explanation:
    quadratic_90: int
    quadratic_99: int
    linear_90: int
    linear_99: int
    tracking_sign_first: int
    tracking_sign_locked: int


@dataclass(frozen=True)
class ArbCertificate:
    bits: int
    dimension: int
    eigenvalues_isolated: bool
    orthonormal: bool
    quadratic_identity: bool
    linear_identity: bool
    tracking_identity: bool


@dataclass(frozen=True)
class MaxKernelAnalysis:
    N: int
    M: int
    modes: tuple
    quadratic_total: float
    linear_total: float
    tracking_total: float
    center_energy: float
    explanation: Explanation
    certificate: object = None


def inverse_tridiagonal(N, M=None):
    """Return the exact rational diagonal/off-diagonal of K_M^{-1}.

    If w_n=1/(n(n+1)), the correct difference form is

        y_M^2/w_M + sum_{n=N+1}^{M-1} (y_n-y_{n+1})^2/w_n.

    Thus the boundary condition is at the terminal end.  This orientation is
    important for a max kernel (a min kernel has the opposite orientation).
    """
    if not isinstance(N, int) or N < 1:
        raise ValueError("N must be a positive integer")
    if M is None:
        M = 2 * N
    if not isinstance(M, int) or M <= N:
        raise ValueError("M must be an integer greater than N")
    size = M - N
    inverse_weights = [n * (n + 1) for n in range(N + 1, M + 1)]
    diagonal = [Fraction(inverse_weights[0])]
    diagonal.extend(
        Fraction(inverse_weights[i - 1] + inverse_weights[i])
        for i in range(1, size)
    )
    off_diagonal = tuple(-Fraction(inverse_weights[i]) for i in range(size - 1))
    return tuple(diagonal), off_diagonal


def max_kernel(N, M=None):
    """Return the exact rational dense K_M, for tests and small certificates."""
    if M is None:
        M = 2 * N
    if M <= N:
        raise ValueError("M must be greater than N")
    indices = range(N + 1, M + 1)
    return tuple(tuple(
        Fraction(1, max(n, m)) - Fraction(1, M + 1) for m in indices
    ) for n in indices)


def _arb_mid(value):
    return float(value.mid())


def _target_balls(N, M):
    """Build rigorous Arb balls for a, R, c, and log(N)."""
    from flint import arb

    if M > 2 * N:
        raise ValueError("the first-block targets require M <= 2N")
    log_N = arb(N).log()
    mu = mobius_table(M)
    psi = chebyshev_psi_table(M)
    u, _ = endpoint_channels(N)
    A = sum((value / a for a, value in enumerate(u, 1)), arb(0))
    p = [arb(0)] * (M + 1)
    for k in range(N + 1, M + 1):
        p[k] = k * A - psi[k] / log_N

    actual = [mu[n] * (arb(n) / N).log() for n in range(N + 1, M + 1)]
    target = [arb(0)] * (M - N)
    suffix = arb(0)
    for n in range(M, N, -1):
        suffix += p[n] / (n * (n + 1))
        target[n - N - 1] = suffix

    diagonal, off = inverse_tridiagonal(N, M)
    center = []
    for i in range(M - N):
        value = ball(diagonal[i]) * target[i]
        if i:
            value += ball(off[i - 1]) * target[i - 1]
        if i + 1 < M - N:
            value += ball(off[i]) * target[i + 1]
        center.append(log_N * value)
    return tuple(actual), tuple(target), tuple(center), log_N


def _targets(N, M):
    """Build a, R, and c with Arb, then return midpoint floats."""
    actual, target, center, log_N = _target_balls(N, M)
    return (
        tuple(map(_arb_mid, actual)), tuple(map(_arb_mid, target)),
        tuple(map(_arb_mid, center)), _arb_mid(log_N),
    )


def _prefix_modes(terms, threshold):
    scale = sum(abs(value) for value in terms)
    if scale == 0:
        return 0
    remainder = sum(terms)
    tolerance = (1.0 - threshold) * scale
    for count, value in enumerate(terms, 1):
        remainder -= value
        if abs(remainder) <= tolerance:
            return count
    return len(terms)


def _sign(value, tolerance=1e-14):
    return 1 if value > tolerance else -1 if value < -tolerance else 0


def _sign_modes(terms):
    wanted = _sign(sum(terms))
    if wanted == 0:
        return 0, 0
    signs = []
    running = 0.0
    for value in terms:
        running += value
        signs.append(_sign(running) == wanted)
    first = next((i + 1 for i, good in enumerate(signs) if good), len(terms))
    locked = len(terms)
    for i in range(len(terms)):
        if all(signs[i:]):
            locked = i + 1
            break
    return first, locked


def _certify_arb(N, M, bits):
    """Certify the complete small-N modal decomposition with Arb balls."""
    from flint import arb, arb_mat, ctx

    old_precision = ctx.prec
    ctx.prec = bits
    try:
        kernel = max_kernel(N, M)
        matrix = arb_mat([[ball(value) for value in row] for row in kernel])
        eigenvalues, vectors = matrix.eig(right=True, algorithm="rump")
        order = sorted(range(len(eigenvalues)),
                       key=lambda i: float(eigenvalues[i].real.mid()), reverse=True)
        columns = []
        lambdas = []
        for index in order:
            lam = eigenvalues[index]
            if not lam.imag.contains(0) or lam.real.lower() <= 0:
                raise ArithmeticError("Arb did not isolate positive real eigenvalues")
            column = [vectors[row, index].real for row in range(M - N)]
            norm = sum((value * value for value in column), arb(0)).sqrt()
            columns.append([value / norm for value in column])
            lambdas.append(lam.real)

        gram = arb_mat(M - N, M - N)
        for i in range(M - N):
            for j in range(M - N):
                gram[i, j] = sum(
                    (columns[i][k] * columns[j][k] for k in range(M - N)), arb(0)
                )
        orthonormal = True
        for i in range(M - N):
            for j in range(M - N):
                orthonormal &= gram[i, j].contains(1 if i == j else 0)

        av, rv, cv, log_N = _target_balls(N, M)
        ap = [sum((v[k] * av[k] for k in range(M - N)), arb(0)) for v in columns]
        rp = [sum((v[k] * rv[k] for k in range(M - N)), arb(0)) for v in columns]
        cp = [sum((v[k] * cv[k] for k in range(M - N)), arb(0)) for v in columns]
        modal_q = sum((lambdas[i] * ap[i] ** 2 for i in range(M - N)), arb(0))
        modal_l = sum((-2 * log_N * ap[i] * rp[i] for i in range(M - N)), arb(0))
        modal_t = sum((
            lambdas[i] * ((ap[i] - cp[i]) ** 2 - cp[i] ** 2)
            for i in range(M - N)
        ), arb(0))
        direct_q = sum((
            av[i] * matrix[i, j] * av[j]
            for i in range(M - N) for j in range(M - N)
        ), arb(0))
        direct_l = -2 * log_N * sum(
            (av[i] * rv[i] for i in range(M - N)), arb(0)
        )
        return ArbCertificate(
            bits, M - N, True, bool(orthonormal),
            modal_q.overlaps(direct_q), modal_l.overlaps(direct_l),
            modal_t.overlaps(direct_q + direct_l),
        )
    finally:
        ctx.prec = old_precision


def analyze_max_kernel_modes(N, M=None, certify=False, bits=192):
    """Compute descending-K eigenmodes and modal sign/explanation statistics."""
    try:
        import numpy as np
        from scipy.linalg import eigh_tridiagonal
    except ImportError as error:
        raise RuntimeError(
            "numpy and scipy are required; run with "
            "`uv run --with python-flint --with numpy --with scipy python ...`"
        ) from error
    if M is None:
        M = 2 * N
    if certify and M - N > 32:
        raise ValueError("Arb certification is limited to dimension 32")
    diagonal, off = inverse_tridiagonal(N, M)
    actual, target, center, log_N = _targets(N, M)
    q_eigenvalues, vectors = eigh_tridiagonal(
        np.asarray(diagonal, dtype=float), np.asarray(off, dtype=float),
        check_finite=False,
    )
    # eigh_tridiagonal returns increasing eigenvalues of K^{-1}; reciprocation
    # therefore already puts the K eigenmodes in decreasing order.
    order = np.arange(M - N)
    eigenvalues = 1.0 / q_eigenvalues[order]
    vectors = vectors[:, order]
    ap = vectors.T @ np.asarray(actual)
    rp = vectors.T @ np.asarray(target)
    cp = vectors.T @ np.asarray(center)
    quadratic = eigenvalues * ap * ap
    linear = -2.0 * log_N * ap * rp
    tracking = eigenvalues * ((ap - cp) ** 2 - cp ** 2)
    modes = tuple(ModeSummary(
        i + 1, float(eigenvalues[i]), float(ap[i]), float(rp[i]), float(cp[i]),
        float(quadratic[i]), float(linear[i]), float(tracking[i]),
    ) for i in range(M - N))
    first, locked = _sign_modes(tracking)
    explanation = Explanation(
        _prefix_modes(quadratic, 0.90), _prefix_modes(quadratic, 0.99),
        _prefix_modes(linear, 0.90), _prefix_modes(linear, 0.99), first, locked,
    )
    certificate = None
    if certify:
        certificate = _certify_arb(N, M, bits)
    return MaxKernelAnalysis(
        N, M, modes, float(sum(quadratic)), float(sum(linear)),
        float(sum(tracking)), float(sum(eigenvalues * cp * cp)),
        explanation, certificate,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--N", type=int, nargs="+", default=[8, 32, 128, 512])
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--certify-through", type=int, default=32, metavar="DIM")
    parser.add_argument("--show-modes", type=int, default=8)
    args = parser.parse_args()
    for N in args.N:
        result = analyze_max_kernel_modes(
            N, certify=N <= args.certify_through, bits=args.bits
        )
        e = result.explanation
        print(
            f"N={N} dim={N}: quadratic={result.quadratic_total:+.12g} "
            f"linear={result.linear_total:+.12g} "
            f"tracking={result.tracking_total:+.12g}"
        )
        print(
            f"  modes: quadratic 90%/99%={e.quadratic_90}/{e.quadratic_99}; "
            f"linear 90%/99%={e.linear_90}/{e.linear_99}; "
            f"tracking sign first/locked={e.tracking_sign_first}/{e.tracking_sign_locked}"
        )
        if result.certificate:
            c = result.certificate
            print(
                f"  Arb({c.bits} bits): isolated={c.eigenvalues_isolated}; "
                f"orthonormal={c.orthonormal}; identities="
                f"{c.quadratic_identity}/{c.linear_identity}/{c.tracking_identity}"
            )
        for mode in result.modes[:args.show_modes]:
            print(
                f"    j={mode.mode:4d} lambda={mode.eigenvalue:.8g} "
                f"a={mode.actual_projection:+.5g} R={mode.linear_target_projection:+.5g} "
                f"c={mode.center_projection:+.5g} track={mode.tracking:+.5g}"
            )


if __name__ == "__main__":
    main()
