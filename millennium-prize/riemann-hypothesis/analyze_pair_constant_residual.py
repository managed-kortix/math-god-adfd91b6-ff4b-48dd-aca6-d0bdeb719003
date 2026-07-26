#!/usr/bin/env python3
"""Exact/Arb audit of the affine pair-constant residual.

The exact layer constructs the left kernel of the coarse shell floor matrix.
The Arb layer evaluates the actual vector bar(c)-Hx, gives its coordinates in
the weighted left-kernel realization, and compares its projection energy with
the odd prime-power diagonal.
"""

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache

from flint import arb, ctx

from analyze_endpoint_prefix import chebyshev_psi_table
from analyze_two_scale_completion import _inverse, exact_rank, floor_matrix, nullspace_basis
from analyze_weighted_g_tail import mobius_table
from verify_separated_kernel import ball


@dataclass(frozen=True)
class ExactLeftNullGeometry:
    matrix: tuple
    weights: tuple
    rank: int
    nullity: int
    basis: tuple
    supports: tuple
    weighted_gram: tuple
    annihilation_verified: bool


@dataclass(frozen=True)
class PairConstantResidualAnalysis:
    N: int
    geometry: ExactLeftNullGeometry
    pair_indices: tuple
    odd_indices: tuple
    affine_constant: object
    pair_average: tuple
    Hx: tuple
    source_vector: tuple
    null_moments: tuple
    residual_coordinates: tuple
    residual_vector: tuple
    weighted_projection_energy: object
    direct_weighted_energy: object
    odd_prime_diagonal: object
    coordinate_supports: tuple
    residual_support: tuple
    projection_verified: bool
    energy_verified: bool
    prime_diagonal_positive: bool


def _transpose(matrix):
    if not matrix:
        return tuple()
    return tuple(tuple(matrix[i][j] for i in range(len(matrix)))
                 for j in range(len(matrix[0])))


def _arb_mat_vec(matrix, vector):
    return tuple(sum((ball(a) * b for a, b in zip(row, vector)), arb(0))
                 for row in matrix)


def _weighted_dot(left, right, weights):
    return sum((ball(w) * x * y for w, x, y in zip(weights, left, right)), arb(0))


def exact_left_null_geometry(matrix, weights):
    """Return a canonical rational left-null basis and its weighted Gram.

    If l is a left-null vector, W^-1 l lies in the W-orthogonal complement of
    the column space.  The Gram stored here is therefore L^T W^-1 L.
    """
    matrix = tuple(tuple(Fraction(value) for value in row) for row in matrix)
    weights = tuple(Fraction(value) for value in weights)
    if len(matrix) != len(weights) or any(weight <= 0 for weight in weights):
        raise ValueError("need one positive weight per matrix row")
    if matrix and any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("matrix must be rectangular")
    basis = nullspace_basis(_transpose(matrix))
    supports = tuple(tuple(i for i, value in enumerate(vector) if value)
                     for vector in basis)
    gram = tuple(tuple(sum((x * y / weight for x, y, weight in
                            zip(left, right, weights)), Fraction(0))
                       for right in basis) for left in basis)
    annihilation = all(
        sum((vector[i] * matrix[i][j] for i in range(len(matrix))), Fraction(0)) == 0
        for vector in basis
        for j in range(len(matrix[0]) if matrix else 0)
    )
    rank = exact_rank(matrix)
    return ExactLeftNullGeometry(
        matrix, weights, rank, len(matrix) - rank, basis, supports, gram,
        annihilation,
    )


@lru_cache(maxsize=None)
def exact_pair_constant_geometry(N):
    if not isinstance(N, int) or N < 2 or N > 128 or N & (N - 1):
        raise ValueError("N must be dyadic with 2 <= N <= 128")
    pairs = tuple(range(N // 2, N))
    coarse = floor_matrix(N // 2, N, N)
    weights = tuple(Fraction(N, k * (k + 1)) for k in pairs)
    return exact_left_null_geometry(coarse, weights)


def analyze_pair_constant_residual(N):
    geometry = exact_pair_constant_geometry(N)
    pairs = tuple(range(N // 2, N))
    odds = tuple(range(1, 2 * N, 2))
    mu = mobius_table(2 * N)
    log_2N = ball(2 * N).log()
    x = tuple(mu[q] * ball(Fraction(2 * N, q)).log() / log_2N for q in odds)
    A = sum((mu[d] * ball(Fraction(2 * N, d)).log()
             / (d * log_2N) for d in range(1, 2 * N + 1)), arb(0))
    pair_average = tuple(
        1 + A * ball(2 * k + Fraction(k, 2 * k + 1)) for k in pairs
    )
    H = tuple(tuple(
        Fraction((2 * k) // q) + (Fraction(k, 2 * k + 1) if (2 * k + 1) % q == 0 else 0)
        for q in odds
    ) for k in pairs)
    Hx = _arb_mat_vec(H, x)
    source = tuple(c - h for c, h in zip(pair_average, Hx))

    moments = tuple(sum((ball(value) * source[i] for i, value in enumerate(left)), arb(0))
                    for left in geometry.basis)
    if geometry.basis:
        coordinates = _arb_mat_vec(_inverse(geometry.weighted_gram), moments)
        residual = tuple(
            sum((coordinates[j] * ball(geometry.basis[j][i] / geometry.weights[i])
                 for j in range(len(geometry.basis))), arb(0))
            for i in range(len(pairs))
        )
        projection_energy = sum((a * b for a, b in zip(moments, coordinates)), arb(0))
    else:
        coordinates = tuple()
        residual = tuple(arb(0) for _ in pairs)
        projection_energy = arb(0)
    direct_energy = _weighted_dot(residual, residual, geometry.weights)

    psi = chebyshev_psi_table(2 * N - 1)
    prime_diagonal = sum((
        N * (psi[r] - psi[r - 1]) ** 2 / (r * r * log_2N ** 2)
        for r in range(N + 1, 2 * N) if r & 1
        if not (psi[r] - psi[r - 1]).contains(0)
    ), arb(0))
    coordinate_supports = tuple(
        geometry.supports[i] for i, value in enumerate(coordinates)
        if not value.contains(0)
    )
    residual_support = tuple(i for i, value in enumerate(residual)
                             if not value.contains(0))
    return PairConstantResidualAnalysis(
        N, geometry, pairs, odds, A, pair_average, Hx, source, moments,
        coordinates, residual, projection_energy, direct_energy, prime_diagonal,
        coordinate_supports, residual_support,
        all(value.contains(0) for value in moments),
        projection_energy.overlaps(direct_energy),
        prime_diagonal.lower() > 0,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--N", type=int, nargs="+", default=[2, 4, 8, 16, 32, 64, 128])
    args = parser.parse_args()
    if args.bits < 80:
        parser.error("need bits >= 80")
    ctx.prec = args.bits
    failed = False
    print(f"precision={args.bits} bits")
    for N in args.N:
        result = analyze_pair_constant_residual(N)
        geometry = result.geometry
        print(
            f"N={N}: coarse rank/nullity={geometry.rank}/{geometry.nullity}; "
            f"left-null supports={[len(s) for s in geometry.supports]}"
        )
        print(
            f"  pair residual={result.weighted_projection_energy.str(12)}; "
            f"odd-prime diagonal={result.odd_prime_diagonal.str(12)}; "
            f"certified support={result.residual_support}"
        )
        failed |= not all((
            geometry.annihilation_verified, result.projection_verified,
            result.energy_verified, result.prime_diagonal_positive,
        ))
    if failed:
        raise SystemExit("a pair-constant residual certificate failed")


if __name__ == "__main__":
    main()
