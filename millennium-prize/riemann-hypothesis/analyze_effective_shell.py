#!/usr/bin/env python3
"""Exact/Arb first-difference audit of the effective coarse shell.

The shell columns N/2 <= d < N form a unit lower-triangular matrix.  This
analyzer inverts that block by first differences, without constructing a dense
floor matrix, and evaluates the actual scale-N and scale-2N Mobius tapers.
All arithmetic geometry is exact; logarithms, coefficients, and energies are
Arb balls.  The implementation uses divisor sieves and is O(N log N).
"""

import argparse
from dataclasses import dataclass
from fractions import Fraction

from flint import arb, ctx

from analyze_weighted_g_tail import mobius_table
from verify_separated_kernel import ball


@dataclass(frozen=True)
class EffectiveShellAnalysis:
    N: int
    pair_indices: tuple
    fine_indices: tuple
    affine_constant: object
    pair_average: tuple
    first_difference_coefficients: tuple
    even_coefficients: tuple
    effective_coefficients: tuple
    reconstructed_pair_average: tuple
    preceding_taper: tuple
    discrepancy: tuple
    preceding_image: tuple
    fine_completed_vector: tuple
    pair_jumps: tuple
    weighted_coarse_energy: object
    preceding_coarse_energy: object
    discrepancy_image_energy: object
    affine_jump_energy: object
    complete_fine_energy: object
    decomposed_fine_energy: object
    pair_average_verified: bool
    first_difference_verified: bool
    fine_energy_verified: bool
    preceding_affine_constant: object
    preceding_completed_vector: tuple
    pair_average_discrepancy: tuple
    preceding_completed_energy: object
    pair_average_discrepancy_energy: object
    preceding_discrepancy_correlation: object
    delta_A_slopes: tuple
    delta_psi_cross: tuple
    delta_doubled_psi: tuple
    delta_odd_lambda_endpoint: tuple
    correlation_A_slopes: object
    correlation_psi_cross: object
    correlation_doubled_psi: object
    correlation_odd_lambda_endpoint: object
    decomposed_correlation: object
    correlation_decomposition_verified: bool
    centered_quadratic_direct: object
    centered_quadratic_diagonal: object
    centered_quadratic_fixed_shift: object
    centered_quadratic_dilation: object
    centered_quadratic_generic_off_diagonal: object
    centered_quadratic_recombined: object
    centered_quadratic_recombination_verified: bool
    coarse_minus_fine: object
    polarized_coarse_minus_fine: object
    polarization_verified: bool


def exact_shell_first_differences(values):
    """Invert the shell's unit lower-triangular block over Q exactly."""
    values = tuple(Fraction(value) for value in values)
    if not values:
        raise ValueError("need at least one shell value")
    return (values[0],) + tuple(values[i] - values[i - 1]
                                for i in range(1, len(values)))


def exact_shell_reconstruction(coefficients):
    """Apply the shell's unit lower-triangular block over Q exactly."""
    coefficients = tuple(Fraction(value) for value in coefficients)
    running = Fraction(0)
    result = []
    for value in coefficients:
        running += value
        result.append(running)
    return tuple(result)


def _arb_first_differences(values):
    return (values[0],) + tuple(values[i] - values[i - 1]
                                for i in range(1, len(values)))


def _prefix(values):
    running = arb(0)
    result = []
    for value in values:
        running += value
        result.append(running)
    return tuple(result)


def _divisor_sums(coefficients):
    """Return s[n]=sum_{d|n} coefficients[d], using a divisor sieve."""
    limit = len(coefficients) - 1
    sums = [arb(0) for _ in range(limit + 1)]
    for d in range(1, limit + 1):
        value = coefficients[d]
        if value.contains(0) and value.mid() == 0:
            continue
        for multiple in range(d, limit + 1, d):
            sums[multiple] += value
    return tuple(sums)


def _floor_transform_from_divisor_sums(divisor_sums):
    # F(j)-F(j-1)=sum_{d|j} a_d for F(j)=sum_d a_d floor(j/d).
    return (arb(0),) + _prefix(divisor_sums[1:])


def _weighted_energy(values, start, scale):
    return sum((ball(Fraction(scale, k * (k + 1))) * value * value
                for k, value in enumerate(values, start)), arb(0))


def _weighted_inner(left, right, start, scale):
    return sum((ball(Fraction(scale, k * (k + 1))) * a * b
                for k, (a, b) in enumerate(zip(left, right), start)), arb(0))


def _certified_sign(value):
    if value > 0:
        return "+"
    if value < 0:
        return "-"
    return "?"


def analyze_effective_shell(N):
    if (not isinstance(N, int) or N < 2 or N > 8192
            or N & (N - 1)):
        raise ValueError("N must be dyadic with 2 <= N <= 8192")

    half = N // 2
    mu = mobius_table(2 * N)
    log_N = ball(N).log()
    log_2N = ball(2 * N).log()

    fine_coefficients = [arb(0)] * (2 * N + 1)
    for d in range(1, 2 * N + 1):
        fine_coefficients[d] = (
            mu[d] * ball(Fraction(2 * N, d)).log() / log_2N
        )
    fine_coefficients = tuple(fine_coefficients)
    fine_divisor_sums = _divisor_sums(fine_coefficients)
    fine_transform = _floor_transform_from_divisor_sums(fine_divisor_sums)
    A = sum((fine_coefficients[d] / d for d in range(1, 2 * N + 1)), arb(0))
    fine_completed = tuple(
        1 + j * A - fine_transform[j] for j in range(N, 2 * N)
    )

    pair_average = []
    pair_jumps = []
    for k in range(half, N):
        even_value = fine_completed[2 * k - N]
        odd_value = fine_completed[2 * k + 1 - N]
        pair_average.append(
            even_value + ball(Fraction(k, 2 * k + 1))
            * (odd_value - even_value)
        )
        pair_jumps.append(odd_value - even_value)
    pair_average = tuple(pair_average)
    pair_jumps = tuple(pair_jumps)

    shell_differences = _arb_first_differences(pair_average)
    effective = [arb(0) for _ in range(N)]
    for offset, value in enumerate(shell_differences):
        effective[half - 1 + offset] = value
    effective = tuple(effective)
    even_coefficients = tuple(fine_coefficients[2 * d] for d in range(1, N + 1))

    effective_divisor_sums = _divisor_sums((arb(0),) + effective)
    effective_transform = _floor_transform_from_divisor_sums(effective_divisor_sums)
    reconstructed = tuple(effective_transform[k] for k in range(half, N))

    preceding = tuple(
        mu[d] * ball(Fraction(N, d)).log() / log_N
        for d in range(1, N + 1)
    )
    preceding_divisor_sums = _divisor_sums((arb(0),) + preceding)
    preceding_transform = _floor_transform_from_divisor_sums(
        preceding_divisor_sums
    )
    preceding_image = tuple(preceding_transform[k] for k in range(half, N))
    preceding_A = sum((preceding[d - 1] / d for d in range(1, N + 1)), arb(0))
    preceding_completed = tuple(
        1 + k * preceding_A - preceding_transform[k] for k in range(half, N)
    )
    pair_discrepancy = tuple(a - b for a, b in zip(pair_average,
                                                    preceding_completed))
    discrepancy = tuple(gamma - taper
                        for gamma, taper in zip(effective, preceding))
    discrepancy_divisor_sums = _divisor_sums((arb(0),) + discrepancy)
    discrepancy_transform = _floor_transform_from_divisor_sums(
        discrepancy_divisor_sums
    )
    discrepancy_image = tuple(discrepancy_transform[k]
                              for k in range(half, N))

    coarse_energy = _weighted_energy(reconstructed, half, N)
    preceding_energy = _weighted_energy(preceding_image, half, N)
    discrepancy_energy = _weighted_energy(discrepancy_image, half, N)
    jump_energy = sum((ball(Fraction(N, (2 * k + 1) ** 2)) * jump * jump
                       for k, jump in zip(range(half, N), pair_jumps)), arb(0))
    fine_energy = _weighted_energy(fine_completed, N, 2 * N)
    decomposed_energy = coarse_energy + jump_energy
    preceding_completed_energy = _weighted_energy(preceding_completed, half, N)
    pair_discrepancy_energy = _weighted_energy(pair_discrepancy, half, N)
    correlation = _weighted_inner(preceding_completed, pair_discrepancy,
                                  half, N)

    # In the exact Chebyshev form, delta=z-u is the sum of these four
    # arithmetically distinct vectors.  The divisor-sum prefixes equal
    # psi(k)/log(N) and psi(2k)/log(2N), while the odd divisor sum is
    # Lambda(2k+1)/log(2N).
    delta_A_slopes = tuple(
        k * (2 * A - preceding_A)
        + ball(Fraction(k, 2 * k + 1)) * A
        for k in range(half, N)
    )
    delta_psi_cross = tuple(preceding_transform[k] - 1
                            for k in range(half, N))
    delta_doubled_psi = tuple(-(fine_transform[2 * k] - 1)
                              for k in range(half, N))
    delta_odd_lambda_endpoint = tuple(
        -ball(Fraction(k, 2 * k + 1)) * fine_divisor_sums[2 * k + 1]
        for k in range(half, N)
    )
    component_vectors = (delta_A_slopes, delta_psi_cross,
                         delta_doubled_psi, delta_odd_lambda_endpoint)
    component_correlations = tuple(
        _weighted_inner(preceding_completed, component, half, N)
        for component in component_vectors
    )
    decomposed_correlation = sum(component_correlations, arb(0))
    delta_recombined = tuple(sum(values, arb(0))
                             for values in zip(*component_vectors))
    correlation_decomposition_verified = (
        all(delta.overlaps(recombined) for delta, recombined in
            zip(pair_discrepancy, delta_recombined))
        and correlation.overlaps(decomposed_correlation)
    )

    # Let h(r)=Lambda(r)-1, E(k)=sum_{r<=k} h(r), and
    # G(k)=sum_{r<=2k} h(r).  The centered quadratic channel divided by N is
    #   -sum w E^2/log(N)^2
    #   +sum w E(G+k Lambda(2k+1)/(2k+1))/(log(N)log(2N)).
    # Splitting G=E+(G-E) isolates the exact h(r)^2 diagonal, the remaining
    # same-prefix (fixed-shift) pairs, the odd dilation endpoint, and the
    # genuinely cross-window off-diagonal rectangle r<=k<s<=2k.
    lambda_values = tuple(
        arb(0) if r <= 1 else fine_divisor_sums[r] * log_2N
        for r in range(2 * N + 1)
    )
    centered_increments = tuple(value - 1 for value in lambda_values)
    centered_square_prefix = [arb(0)] * (N + 1)
    for r in range(1, N + 1):
        centered_square_prefix[r] = (
            centered_square_prefix[r - 1] + centered_increments[r] ** 2
        )

    quadratic_direct = arb(0)
    quadratic_diagonal_raw = arb(0)
    quadratic_fixed_shift_raw = arb(0)
    quadratic_dilation_raw = arb(0)
    quadratic_generic_raw = arb(0)
    for k in range(half, N):
        weight = ball(Fraction(1, k * (k + 1)))
        E = log_N * (preceding_transform[k] - 1) - k
        G = log_2N * (fine_transform[2 * k] - 1) - 2 * k
        endpoint = ball(Fraction(k, 2 * k + 1)) * lambda_values[2 * k + 1]
        diagonal_at_k = centered_square_prefix[k]
        quadratic_direct += weight * E * (
            -E / (log_N ** 2) + (G + endpoint) / (log_N * log_2N)
        )
        quadratic_diagonal_raw += weight * diagonal_at_k
        quadratic_fixed_shift_raw += weight * (E ** 2 - diagonal_at_k)
        quadratic_generic_raw += weight * E * (G - E)
        quadratic_dilation_raw += weight * E * endpoint

    same_prefix_coefficient = (
        -1 / (log_N ** 2) + 1 / (log_N * log_2N)
    )
    quadratic_diagonal = same_prefix_coefficient * quadratic_diagonal_raw
    quadratic_fixed_shift = (
        same_prefix_coefficient * quadratic_fixed_shift_raw
    )
    quadratic_dilation = quadratic_dilation_raw / (log_N * log_2N)
    quadratic_generic = quadratic_generic_raw / (log_N * log_2N)
    quadratic_recombined = (
        quadratic_diagonal + quadratic_fixed_shift + quadratic_dilation
        + quadratic_generic
    )
    quadratic_verified = quadratic_direct.overlaps(quadratic_recombined)
    coarse_minus_fine = preceding_completed_energy - fine_energy
    polarized = -2 * correlation - pair_discrepancy_energy - jump_energy
    reconstructed_from_differences = _prefix(shell_differences)

    return EffectiveShellAnalysis(
        N, tuple(range(half, N)), tuple(range(N, 2 * N)), A,
        pair_average, shell_differences, even_coefficients, effective,
        reconstructed, preceding, discrepancy, preceding_image,
        fine_completed, pair_jumps, coarse_energy, preceding_energy,
        discrepancy_energy, jump_energy, fine_energy, decomposed_energy,
        all(a.overlaps(b) for a, b in zip(pair_average, reconstructed)),
        all(a.overlaps(b) for a, b in zip(pair_average,
                                          reconstructed_from_differences)),
        fine_energy.overlaps(decomposed_energy),
        preceding_A, preceding_completed, pair_discrepancy,
        preceding_completed_energy, pair_discrepancy_energy, correlation,
        delta_A_slopes, delta_psi_cross, delta_doubled_psi,
        delta_odd_lambda_endpoint, *component_correlations,
        decomposed_correlation, correlation_decomposition_verified,
        quadratic_direct, quadratic_diagonal, quadratic_fixed_shift,
        quadratic_dilation, quadratic_generic, quadratic_recombined,
        quadratic_verified,
        coarse_minus_fine, polarized, coarse_minus_fine.overlaps(polarized),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--N", type=int, nargs="+",
                        default=[32, 128, 512, 2048, 8192])
    args = parser.parse_args()
    if args.bits < 80:
        parser.error("need bits >= 80")
    ctx.prec = args.bits
    failed = False
    print(f"precision={args.bits} bits")
    for N in args.N:
        result = analyze_effective_shell(N)
        print(
            f"N={N}: previous-completed={result.preceding_completed_energy.str(14)}; "
            f"effective={result.weighted_coarse_energy.str(14)}; "
            f"jump={result.affine_jump_energy.str(14)}"
        )
        print(
            f"  fine={result.complete_fine_energy.str(14)}; "
            f"effective+jump={result.decomposed_fine_energy.str(14)}; "
            f"pair-delta={result.pair_average_discrepancy_energy.str(14)}; "
            f"decrement={result.coarse_minus_fine.str(14)}; "
            f"verified={result.pair_average_verified and result.first_difference_verified and result.fine_energy_verified and result.polarization_verified}"
        )
        print(
            "  <u,delta>: "
            f"A-slopes={result.correlation_A_slopes.str(12)}; "
            f"psi-cross={result.correlation_psi_cross.str(12)}; "
            f"doubled-psi={result.correlation_doubled_psi.str(12)}; "
            f"odd-Lambda-endpoint={result.correlation_odd_lambda_endpoint.str(12)}"
        )
        print(
            f"  recombined={result.decomposed_correlation.str(12)}; "
            f"sign={_certified_sign(result.decomposed_correlation)}; "
            f"log(2N)-scaled={(ball(2 * N).log() * result.decomposed_correlation).str(12)}; "
            f"component-verified={result.correlation_decomposition_verified}"
        )
        print(
            "  centered quadratic / N: "
            f"diagonal={result.centered_quadratic_diagonal.str(12)}; "
            f"fixed-shift={result.centered_quadratic_fixed_shift.str(12)}; "
            f"dilation={result.centered_quadratic_dilation.str(12)}; "
            f"generic-off-diagonal={result.centered_quadratic_generic_off_diagonal.str(12)}"
        )
        print(
            f"  quadratic-direct={result.centered_quadratic_direct.str(12)}; "
            f"recombined={result.centered_quadratic_recombined.str(12)}; "
            f"verified={result.centered_quadratic_recombination_verified}"
        )
        failed |= not all((result.pair_average_verified,
                           result.first_difference_verified,
                           result.fine_energy_verified,
                           result.polarization_verified,
                           result.correlation_decomposition_verified,
                           result.centered_quadratic_recombination_verified))
    if failed:
        raise SystemExit("an effective-shell certificate failed")


if __name__ == "__main__":
    main()
