#!/usr/bin/env python3
"""Exact/Arb analysis of the completed first-block Z_N versus Z_2N form.

The floor matrices and all kernel/rank calculations are exact over Q.  Arb is
used for logarithms, the actual Mobius vectors, completed squares, and the
comparison with the independently computed weighted-g total.
"""

import argparse
from dataclasses import dataclass
from fractions import Fraction

from flint import arb, ctx

from analyze_endpoint_prefix import chebyshev_psi_table
from analyze_weighted_g_tail import analyze_weighted_g_tail, mobius_table
from mobius_endpoint_surrogate import endpoint_alpha, endpoint_channels
from verify_separated_kernel import ball


@dataclass(frozen=True)
class ExactInertia:
    positive: int
    negative: int
    zero: int
    dimension: int


@dataclass(frozen=True)
class ScaleProjection:
    scale: int
    columns: int
    rank: int
    nullity: int
    source: tuple
    row_projection: tuple
    kernel_projection: tuple
    image: tuple
    projected_image: tuple
    kernel_image: tuple
    decomposition_verified: bool
    kernel_verified: bool
    image_verified: bool


@dataclass(frozen=True)
class TwoScaleCompletionAnalysis:
    N: int
    alpha: Fraction
    floor_N: tuple
    floor_2N: tuple
    kernel_N: tuple
    kernel_2N: tuple
    joint_kernel_basis: tuple
    inertia: ExactInertia
    projection_N: ScaleProjection
    projection_2N: ScaleProjection
    Z_N: tuple
    Z_2N: tuple
    completed_cells: tuple
    completed_total: object
    weighted_g_total: object
    scaled_weighted_g_total: object
    z_2N_psi_verified: bool
    joint_kernel_verified: bool
    inertia_verified: bool
    completed_cells_verified: bool
    weighted_g_verified: bool


def floor_matrix(start, stop, cutoff):
    """Return F[k,d]=floor(k/d), start <= k < stop, 1 <= d <= cutoff."""
    if not all(isinstance(value, int) for value in (start, stop, cutoff)):
        raise ValueError("floor-matrix arguments must be integers")
    if start < 1 or stop <= start or cutoff < 1:
        raise ValueError("need 1 <= start < stop and cutoff >= 1")
    return tuple(tuple(Fraction(k // d) for d in range(1, cutoff + 1))
                 for k in range(start, stop))


def _rref(matrix):
    rows = [list(row) for row in matrix]
    if not rows:
        return tuple(), tuple()
    width = len(rows[0])
    pivots = []
    pivot_row = 0
    for column in range(width):
        found = next((r for r in range(pivot_row, len(rows))
                      if rows[r][column]), None)
        if found is None:
            continue
        rows[pivot_row], rows[found] = rows[found], rows[pivot_row]
        pivot = rows[pivot_row][column]
        rows[pivot_row] = [value / pivot for value in rows[pivot_row]]
        for r in range(len(rows)):
            if r == pivot_row or not rows[r][column]:
                continue
            factor = rows[r][column]
            rows[r] = [a - factor * b for a, b in zip(rows[r], rows[pivot_row])]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return tuple(tuple(row) for row in rows), tuple(pivots)


def exact_rank(matrix):
    return len(_rref(matrix)[1])


def nullspace_basis(matrix):
    """Return a canonical exact column-kernel basis from reduced echelon form."""
    reduced, pivots = _rref(matrix)
    width = len(matrix[0]) if matrix else 0
    free = [column for column in range(width) if column not in pivots]
    basis = []
    for column in free:
        vector = [Fraction(0)] * width
        vector[column] = Fraction(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][column]
        basis.append(tuple(vector))
    return tuple(basis)


def _inverse(matrix):
    size = len(matrix)
    augmented = [list(row) + [Fraction(i == j) for j in range(size)]
                 for i, row in enumerate(matrix)]
    for column in range(size):
        found = next((r for r in range(column, size) if augmented[r][column]), None)
        if found is None:
            raise ArithmeticError("singular exact matrix")
        augmented[column], augmented[found] = augmented[found], augmented[column]
        pivot = augmented[column][column]
        augmented[column] = [value / pivot for value in augmented[column]]
        for r in range(size):
            if r == column:
                continue
            factor = augmented[r][column]
            augmented[r] = [a - factor * b
                            for a, b in zip(augmented[r], augmented[column])]
    return tuple(tuple(row[size:]) for row in augmented)


def _mat_vec(matrix, vector, zero):
    return tuple(sum((ball(a) * b for a, b in zip(row, vector)), zero)
                 for row in matrix)


def _row_projection(matrix, source, scale):
    reduced, pivots = _rref(matrix)
    rows = tuple(reduced[i] for i in range(len(pivots)))
    gram = tuple(tuple(sum((a * b for a, b in zip(left, right)), Fraction(0))
                       for right in rows) for left in rows)
    inverse = _inverse(gram)
    coordinates = tuple(sum((ball(a) * b for a, b in zip(row, source)), arb(0))
                        for row in rows)
    dual = tuple(sum((ball(inverse[i][j]) * coordinates[j]
                      for j in range(len(rows))), arb(0))
                 for i in range(len(rows)))
    row_part = tuple(sum((dual[i] * ball(rows[i][j]) for i in range(len(rows))),
                         arb(0)) for j in range(len(source)))
    kernel_part = tuple(a - b for a, b in zip(source, row_part))
    image = _mat_vec(matrix, source, arb(0))
    projected_image = _mat_vec(matrix, row_part, arb(0))
    kernel_image = _mat_vec(matrix, kernel_part, arb(0))
    return ScaleProjection(
        scale, len(source), len(pivots), len(source) - len(pivots), source,
        row_part, kernel_part, image, projected_image, kernel_image,
        all(a.overlaps(b + c) for a, b, c in zip(source, row_part, kernel_part)),
        all(value.contains(0) for value in kernel_image),
        all(a.overlaps(b) for a, b in zip(image, projected_image)),
    )


def _embedded_joint_basis(left, right, left_width, right_width):
    zero_left = (Fraction(0),) * left_width
    zero_right = (Fraction(0),) * right_width
    return (tuple(vector + zero_right for vector in left)
            + tuple(zero_left + vector for vector in right))


def _exact_kernel_check(matrix, basis):
    return all(all(sum((a * b for a, b in zip(row, vector)), Fraction(0)) == 0
                       for row in matrix) for vector in basis)


def analyze_two_scale_completion(N):
    """Analyze the complete first block N <= k < 2N."""
    if not isinstance(N, int) or N < 2 or N & (N - 1):
        raise ValueError("N must be a dyadic integer at least 2")
    matrix_N = floor_matrix(N, 2 * N, N)
    matrix_2N = floor_matrix(N, 2 * N, 2 * N)
    rank_N = exact_rank(matrix_N)
    rank_2N = exact_rank(matrix_2N)
    kernel_N = nullspace_basis(matrix_N)
    kernel_2N = nullspace_basis(matrix_2N)
    joint_basis = _embedded_joint_basis(kernel_N, kernel_2N, N, 2 * N)
    inertia = ExactInertia(rank_N, rank_2N, 3 * N - rank_N - rank_2N, 3 * N)

    mu = mobius_table(2 * N)
    log_N = ball(N).log()
    log_2N = ball(2 * N).log()
    source_N = tuple(mu[d] * ball(Fraction(N, d)).log() / log_N
                     for d in range(1, N + 1))
    source_2N = tuple(mu[d] * ball(Fraction(2 * N, d)).log() / log_2N
                      for d in range(1, 2 * N + 1))
    projection_N = _row_projection(matrix_N, source_N, N)
    projection_2N = _row_projection(matrix_2N, source_2N, 2 * N)
    z_N_normalized = projection_N.image
    z_2N_normalized = projection_2N.image
    Z_N = tuple(value * log_N for value in z_N_normalized)
    Z_2N = tuple(value * log_2N for value in z_2N_normalized)

    psi = chebyshev_psi_table(2 * N - 1)
    z_2N_psi_verified = all(
        Z_2N[k - N].overlaps(log_2N + psi[k]) for k in range(N, 2 * N)
    )
    alpha = endpoint_alpha(N)
    scale = ball(alpha)
    u, d = endpoint_channels(N)
    A = sum((value / index for index, value in enumerate(u, 1)), arb(0))
    D = sum((value / index for index, value in enumerate(d, 1)), arb(0))
    completed_cells = tuple(
        ((k * A + 1 - z_N_normalized[k - N]) ** 2
         - (k * (A - scale * D) + 1 - z_2N_normalized[k - N]) ** 2)
        / (k * (k + 1))
        for k in range(N, 2 * N)
    )
    completed_total = sum(completed_cells, arb(0))
    weighted_analysis = analyze_weighted_g_tail(N)
    weighted_g_total = weighted_analysis.horizons[0].reconstructed_sum
    scaled_weighted_g_total = scale * weighted_g_total
    completed_cells_verified = all(
        completed.overlaps(scale * weighted.weighted_reconstruction)
        for completed, weighted in zip(completed_cells, weighted_analysis.cells)
    )
    joint_matrix = tuple(
        tuple(matrix_N[row]) + tuple(Fraction(0) for _ in range(2 * N))
        for row in range(N)
    ) + tuple(
        tuple(Fraction(0) for _ in range(N)) + tuple(matrix_2N[row])
        for row in range(N)
    )
    joint_kernel_verified = (
        _exact_kernel_check(joint_matrix, joint_basis)
        and len(joint_basis) == inertia.zero
    )
    inertia_verified = (
        inertia.positive == rank_N and inertia.negative == rank_2N
        and inertia.zero == len(kernel_N) + len(kernel_2N)
        and sum((inertia.positive, inertia.negative, inertia.zero)) == inertia.dimension
    )
    return TwoScaleCompletionAnalysis(
        N, alpha, matrix_N, matrix_2N, kernel_N, kernel_2N, joint_basis,
        inertia, projection_N, projection_2N, Z_N, Z_2N, completed_cells,
        completed_total, weighted_g_total, scaled_weighted_g_total,
        z_2N_psi_verified, joint_kernel_verified, inertia_verified,
        completed_cells_verified,
        completed_total.overlaps(scaled_weighted_g_total),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--N", type=int, nargs="+", default=[4, 8, 16, 32])
    args = parser.parse_args()
    if args.bits < 80:
        parser.error("need bits >= 80")
    ctx.prec = args.bits
    failed = False
    print(f"precision={args.bits} bits")
    for N in args.N:
        result = analyze_two_scale_completion(N)
        inertia = result.inertia
        print(
            f"N={N}: inertia=({inertia.positive},{inertia.negative},{inertia.zero}); "
            f"completed={result.completed_total.str(14)}; "
            f"alpha*weighted_g={result.scaled_weighted_g_total.str(14)}"
        )
        print(
            f"  ranks=({result.projection_N.rank},{result.projection_2N.rank}); "
            f"nullities=({result.projection_N.nullity},{result.projection_2N.nullity}); "
            f"joint-kernel={result.joint_kernel_verified}; "
            f"projections={result.projection_N.kernel_verified and result.projection_2N.kernel_verified}; "
            f"psi={result.z_2N_psi_verified}; cells={result.completed_cells_verified}; "
            f"weighted-g={result.weighted_g_verified}"
        )
        failed |= not all((
            result.joint_kernel_verified, result.inertia_verified,
            result.projection_N.decomposition_verified,
            result.projection_N.kernel_verified, result.projection_N.image_verified,
            result.projection_2N.decomposition_verified,
            result.projection_2N.kernel_verified, result.projection_2N.image_verified,
            result.z_2N_psi_verified, result.completed_cells_verified,
            result.weighted_g_verified,
        ))
    if failed:
        raise SystemExit("a two-scale certificate failed")


if __name__ == "__main__":
    main()
