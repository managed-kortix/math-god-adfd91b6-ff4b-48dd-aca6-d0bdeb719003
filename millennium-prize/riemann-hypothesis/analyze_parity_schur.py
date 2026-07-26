#!/usr/bin/env python3
"""Exact weighted parity Schur analysis of the first dyadic fine block.

For N <= k < 2N, split the fine floor matrix floor(k/d), 1 <= d <= 2N,
into its even and odd divisor columns.  All matrix reduction, weighted
projection, Schur-complement, and rank calculations are over Q.  Arb is used
only after that exact geometry has been built, to project the actual normalized
Mobius-log coefficients and certify the resulting energies.
"""

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache

from flint import arb, ctx

from analyze_endpoint_prefix import chebyshev_psi_table
from analyze_two_scale_completion import _inverse, exact_rank, floor_matrix
from analyze_weighted_g_tail import mobius_table
from verify_separated_kernel import ball


@dataclass(frozen=True)
class ExactParityGeometry:
    weights: tuple
    fine_matrix: tuple
    even_matrix: tuple
    odd_matrix: tuple
    coarse_basis_indices: tuple
    coarse_basis: tuple
    odd_projection: tuple
    odd_residual: tuple
    schur_complement: tuple
    even_rank: int
    odd_rank: int
    fine_rank: int
    schur_rank: int
    schur_verified: bool
    orthogonality_verified: bool
    incidence_schur_verified: bool


@dataclass(frozen=True)
class ArbParityEnergy:
    even_coefficients: tuple
    odd_coefficients: tuple
    even_basis_coefficients: tuple
    odd_projection_coefficients: tuple
    combined_coarse_coefficients: tuple
    even_image: tuple
    odd_image: tuple
    projected_odd_image: tuple
    odd_residual_image: tuple
    coarse_image: tuple
    fine_image: tuple
    even_energy: object
    odd_energy: object
    even_odd_cross: object
    even_projected_odd_cross: object
    projected_odd_energy: object
    residual_energy: object
    projected_residual_cross: object
    coarse_energy: object
    coarse_residual_cross: object
    direct_fine_energy: object
    decomposed_fine_energy: object
    projection_verified: bool
    schur_energy_verified: bool
    direct_energy_verified: bool
    prime_residual_energy: object
    prime_residual_verified: bool


@dataclass(frozen=True)
class ParitySchurAnalysis:
    N: int
    geometry: ExactParityGeometry
    energy: ArbParityEnergy


def _transpose(matrix):
    return tuple(tuple(matrix[i][j] for i in range(len(matrix)))
                 for j in range(len(matrix[0])))


def _matmul(left, right):
    right_t = _transpose(right)
    return tuple(tuple(sum((a * b for a, b in zip(row, column)), Fraction(0))
                       for column in right_t) for row in left)


def _weighted_gram(left, right, weights):
    return tuple(tuple(sum((w * x * y for w, x, y in zip(weights, a, b)),
                           Fraction(0))
                       for b in _transpose(right))
                 for a in _transpose(left))


def _subtract(left, right):
    return tuple(tuple(a - b for a, b in zip(x, y))
                 for x, y in zip(left, right))


def _independent_column_indices(matrix):
    """Return canonical pivot columns, using exact row reduction of A^T."""
    from analyze_two_scale_completion import _rref

    return _rref(_transpose(matrix))[1]


@lru_cache(maxsize=None)
def exact_parity_geometry(N):
    if not isinstance(N, int) or N < 2 or N > 64 or N & (N - 1):
        raise ValueError("N must be dyadic with 2 <= N <= 64")
    fine = floor_matrix(N, 2 * N, 2 * N)
    even = tuple(tuple(row[d - 1] for d in range(2, 2 * N + 1, 2))
                 for row in fine)
    odd = tuple(tuple(row[d - 1] for d in range(1, 2 * N + 1, 2))
                for row in fine)
    weights = tuple(Fraction(1, k * (k + 1)) for k in range(N, 2 * N))
    basis_indices = _independent_column_indices(even)
    basis = tuple(tuple(row[j] for j in basis_indices) for row in even)
    gram = _weighted_gram(basis, basis, weights)
    mixed = _weighted_gram(basis, odd, weights)
    projection = _matmul(_inverse(gram), mixed)
    residual = _subtract(odd, _matmul(basis, projection))
    schur = _weighted_gram(residual, residual, weights)
    direct_schur = _subtract(
        _weighted_gram(odd, odd, weights),
        _matmul(_transpose(mixed), _matmul(_inverse(gram), mixed)),
    )
    orthogonality = _weighted_gram(basis, residual, weights)
    odd_indices = tuple(range(1, 2 * N + 1, 2))
    incidence_schur = tuple(tuple(sum((
        Fraction(1, 2 * r * r)
        for r in range(N + 1, 2 * N)
        if r & 1 and r % d == 0 and r % e == 0
    ), Fraction(0)) for e in odd_indices) for d in odd_indices)
    return ExactParityGeometry(
        weights, fine, even, odd, basis_indices, basis, projection, residual,
        schur, exact_rank(even), exact_rank(odd), exact_rank(fine),
        exact_rank(schur), schur == direct_schur,
        all(value == 0 for row in orthogonality for value in row),
        schur == incidence_schur,
    )


def _arb_mat_vec(matrix, vector):
    return tuple(sum((ball(a) * b for a, b in zip(row, vector)), arb(0))
                 for row in matrix)


def _weighted_dot(left, right, weights):
    return sum((ball(w) * x * y for w, x, y in zip(weights, left, right)), arb(0))


def _arb_add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def actual_mobius_energy(N, geometry):
    mu = mobius_table(2 * N)
    log_2N = ball(2 * N).log()
    coefficients = tuple(
        mu[d] * (ball(Fraction(2 * N, d)).log() / log_2N)
        for d in range(1, 2 * N + 1)
    )
    even_coefficients = coefficients[1::2]
    odd_coefficients = coefficients[0::2]

    basis_to_even = _matmul(
        _inverse(_weighted_gram(geometry.coarse_basis, geometry.coarse_basis,
                                geometry.weights)),
        _weighted_gram(geometry.coarse_basis, geometry.even_matrix,
                       geometry.weights),
    )
    even_basis_coefficients = _arb_mat_vec(basis_to_even, even_coefficients)
    odd_projection_coefficients = _arb_mat_vec(
        geometry.odd_projection, odd_coefficients
    )
    combined_coefficients = _arb_add(
        even_basis_coefficients, odd_projection_coefficients
    )

    even_image = _arb_mat_vec(geometry.even_matrix, even_coefficients)
    odd_image = _arb_mat_vec(geometry.odd_matrix, odd_coefficients)
    projected_odd_image = _arb_mat_vec(
        geometry.coarse_basis, odd_projection_coefficients
    )
    residual_image = _arb_mat_vec(geometry.odd_residual, odd_coefficients)
    coarse_image = _arb_add(even_image, projected_odd_image)
    fine_image = _arb_add(even_image, odd_image)

    even_energy = _weighted_dot(even_image, even_image, geometry.weights)
    odd_energy = _weighted_dot(odd_image, odd_image, geometry.weights)
    even_odd_cross = _weighted_dot(even_image, odd_image, geometry.weights)
    even_projected_odd_cross = _weighted_dot(
        even_image, projected_odd_image, geometry.weights
    )
    projected_energy = _weighted_dot(
        projected_odd_image, projected_odd_image, geometry.weights
    )
    residual_energy = _weighted_dot(residual_image, residual_image,
                                    geometry.weights)
    projected_residual_cross = _weighted_dot(
        projected_odd_image, residual_image, geometry.weights
    )
    coarse_energy = _weighted_dot(coarse_image, coarse_image, geometry.weights)
    coarse_residual_cross = _weighted_dot(coarse_image, residual_image,
                                          geometry.weights)
    direct_energy = _weighted_dot(fine_image, fine_image, geometry.weights)
    decomposed_energy = coarse_energy + 2 * coarse_residual_cross + residual_energy
    schur_image = _arb_mat_vec(geometry.schur_complement, odd_coefficients)
    schur_energy = sum((a * b for a, b in zip(odd_coefficients, schur_image)),
                        arb(0))
    psi = chebyshev_psi_table(2 * N - 1)
    prime_residual_energy = sum((
        (psi[r] - psi[r - 1]) ** 2 / (2 * r * r * log_2N ** 2)
        for r in range(N + 1, 2 * N) if r & 1
    ), arb(0))
    projected_sum = _arb_add(projected_odd_image, residual_image)
    return ArbParityEnergy(
        even_coefficients, odd_coefficients, even_basis_coefficients,
        odd_projection_coefficients, combined_coefficients, even_image,
        odd_image, projected_odd_image, residual_image, coarse_image, fine_image,
        even_energy, odd_energy, even_odd_cross, even_projected_odd_cross,
        projected_energy,
        residual_energy, projected_residual_cross, coarse_energy,
        coarse_residual_cross, direct_energy, decomposed_energy,
        all(a.overlaps(b) for a, b in zip(odd_image, projected_sum)),
        residual_energy.overlaps(schur_energy),
        direct_energy.overlaps(decomposed_energy),
        prime_residual_energy,
        residual_energy.overlaps(prime_residual_energy),
    )


def analyze_parity_schur(N):
    geometry = exact_parity_geometry(N)
    return ParitySchurAnalysis(N, geometry, actual_mobius_energy(N, geometry))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--N", type=int, nargs="+", default=[4, 8, 16, 32, 64])
    args = parser.parse_args()
    if args.bits < 80:
        parser.error("need bits >= 80")
    ctx.prec = args.bits
    failed = False
    print(f"precision={args.bits} bits")
    for N in args.N:
        result = analyze_parity_schur(N)
        g, e = result.geometry, result.energy
        print(
            f"N={N}: ranks even/odd/fine/schur="
            f"{g.even_rank}/{g.odd_rank}/{g.fine_rank}/{g.schur_rank}; "
            f"fine-energy={e.direct_fine_energy.str(14)}"
        )
        print(
            f"  even={e.even_energy.str(12)} odd={e.odd_energy.str(12)} "
            f"even-odd-cross={e.even_odd_cross.str(12)}"
        )
        print(
            f"  coarse={e.coarse_energy.str(12)} residual={e.residual_energy.str(12)} "
            f"coarse-residual-cross={e.coarse_residual_cross.str(8)}; exact="
            f"{g.schur_verified and g.orthogonality_verified and g.incidence_schur_verified}; "
            f"Arb={e.projection_verified and e.schur_energy_verified and e.direct_energy_verified}"
        )
        failed |= not all((
            g.schur_verified, g.orthogonality_verified,
            g.incidence_schur_verified, e.projection_verified,
            e.schur_energy_verified, e.direct_energy_verified,
            e.prime_residual_verified,
            e.projected_residual_cross.contains(0),
            e.coarse_residual_cross.contains(0),
        ))
    if failed:
        raise SystemExit("a parity Schur certificate failed")


if __name__ == "__main__":
    main()
