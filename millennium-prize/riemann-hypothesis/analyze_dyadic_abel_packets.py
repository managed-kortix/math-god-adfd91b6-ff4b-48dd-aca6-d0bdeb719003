#!/usr/bin/env python3
"""Certify telescoping Abel packets over consecutive dyadic shell scales."""

import argparse
from dataclasses import dataclass
from fractions import Fraction

from flint import arb, ctx

from analyze_effective_shell import analyze_effective_shell
from verify_separated_kernel import ball


MAX_SCALE = 8192


@dataclass(frozen=True)
class SignPattern:
    signs: tuple
    runs: tuple
    transition_indices: tuple
    certified: bool

    @property
    def compact(self):
        return "".join(self.signs)


@dataclass(frozen=True)
class DyadicAbelAnalysis:
    base_N: int
    depth: int
    scales: tuple
    shell_decrements: tuple
    shell_boundary_packets: tuple
    shell_cumulative_packets: tuple
    shell_recombined_packets: tuple
    direct_sum: object
    packet_sum: object
    telescoped_energy: object
    exterior_boundary: object
    exterior_cumulative: object
    exterior_recombined: object
    interior_boundary_residual: object
    interior_cumulative_residual: object
    shell_packet_recombination_verified: bool
    boundary_telescope_verified: bool
    cumulative_telescope_verified: bool
    total_telescope_verified: bool
    decrement_sign_pattern: SignPattern
    boundary_sign_pattern: SignPattern
    cumulative_sign_pattern: SignPattern


def certified_sign(value):
    if value > 0:
        return "+"
    if value < 0:
        return "-"
    if value == 0:
        return "0"
    return "?"


def detect_sign_pattern(values):
    """Return certified signs, maximal runs, and sign-transition indices."""
    signs = tuple(certified_sign(value) for value in values)
    runs = []
    transitions = []
    for index, sign in enumerate(signs):
        if not runs or runs[-1][0] != sign:
            if runs:
                transitions.append(index)
            runs.append((sign, index, index + 1))
        else:
            old_sign, start, _ = runs[-1]
            runs[-1] = (old_sign, start, index + 1)
    return SignPattern(
        signs, tuple(runs), tuple(transitions), "?" not in signs
    )


def exact_abel_square_energy(values, scale, start):
    """Return boundary and cumulative Abel packets for one rational energy."""
    values = tuple(Fraction(value) for value in values)
    scale = Fraction(scale)
    if not values:
        raise ValueError("need at least one cumulative value")
    if not isinstance(start, int) or start < 1:
        raise ValueError("start must be a positive integer")
    boundary = (
        scale * values[0] ** 2 / start,
        -scale * values[-1] ** 2 / (start + len(values)),
    )
    cumulative = tuple(
        scale * (values[offset] - values[offset - 1])
        * (values[offset] + values[offset - 1]) / (start + offset)
        for offset in range(1, len(values))
    )
    return boundary, cumulative


def _abel_square_energy(values, scale, start):
    boundary = (
        ball(Fraction(scale, start)) * values[0] ** 2,
        -ball(Fraction(scale, start + len(values))) * values[-1] ** 2,
    )
    cumulative = tuple(
        ball(Fraction(scale, start + offset))
        * (values[offset] - values[offset - 1])
        * (values[offset] + values[offset - 1])
        for offset in range(1, len(values))
    )
    return boundary, cumulative


def _sum(values):
    return sum(values, arb(0))


def analyze_dyadic_abel_packets(base_N, depth):
    """Analyze ``depth`` decrements starting at ``base_N``.

    The shell scales are ``base_N * 2**j``.  Their largest value may be 8192;
    the last decrement therefore compares that shell with its completed fine
    energy at twice the scale.
    """
    if (not isinstance(base_N, int) or base_N < 2
            or base_N & (base_N - 1)):
        raise ValueError("base N must be dyadic and at least 2")
    if not isinstance(depth, int) or depth < 1:
        raise ValueError("depth must be a positive integer")
    scales = tuple(base_N << offset for offset in range(depth))
    if scales[-1] > MAX_SCALE:
        raise ValueError("base N and depth exceed maximum shell scale 8192")

    shells = tuple(analyze_effective_shell(N) for N in scales)
    coarse_boundaries = []
    coarse_cumulatives = []
    fine_boundaries = []
    fine_cumulatives = []
    shell_boundaries = []
    shell_cumulatives = []
    shell_recombined = []
    shell_verified = True

    for N, shell in zip(scales, shells):
        coarse_boundary, coarse_cumulative = _abel_square_energy(
            shell.preceding_completed_vector, N, N // 2
        )
        fine_boundary, fine_cumulative = _abel_square_energy(
            shell.fine_completed_vector, 2 * N, N
        )
        coarse_boundary_total = _sum(coarse_boundary)
        coarse_cumulative_total = _sum(coarse_cumulative)
        fine_boundary_total = _sum(fine_boundary)
        fine_cumulative_total = _sum(fine_cumulative)
        boundary = coarse_boundary_total - fine_boundary_total
        cumulative = coarse_cumulative_total - fine_cumulative_total
        recombined = boundary + cumulative

        coarse_boundaries.append(coarse_boundary_total)
        coarse_cumulatives.append(coarse_cumulative_total)
        fine_boundaries.append(fine_boundary_total)
        fine_cumulatives.append(fine_cumulative_total)
        shell_boundaries.append(boundary)
        shell_cumulatives.append(cumulative)
        shell_recombined.append(recombined)
        shell_verified &= recombined.overlaps(shell.coarse_minus_fine)

    interior_boundary_residual = _sum(tuple(
        coarse_boundaries[index + 1] - fine_boundaries[index]
        for index in range(depth - 1)
    ))
    interior_cumulative_residual = _sum(tuple(
        coarse_cumulatives[index + 1] - fine_cumulatives[index]
        for index in range(depth - 1)
    ))
    boundary_telescope_verified = all(
        coarse_boundaries[index + 1].overlaps(fine_boundaries[index])
        for index in range(depth - 1)
    )
    cumulative_telescope_verified = all(
        coarse_cumulatives[index + 1].overlaps(fine_cumulatives[index])
        for index in range(depth - 1)
    )

    exterior_boundary = coarse_boundaries[0] - fine_boundaries[-1]
    exterior_cumulative = coarse_cumulatives[0] - fine_cumulatives[-1]
    exterior_recombined = exterior_boundary + exterior_cumulative
    decrements = tuple(shell.coarse_minus_fine for shell in shells)
    direct_sum = _sum(decrements)
    packet_sum = _sum(tuple(shell_recombined))
    telescoped_energy = (
        shells[0].preceding_completed_energy
        - shells[-1].complete_fine_energy
    )
    total_verified = all((
        direct_sum.overlaps(packet_sum),
        direct_sum.overlaps(telescoped_energy),
        direct_sum.overlaps(exterior_recombined),
    ))

    return DyadicAbelAnalysis(
        base_N, depth, scales, decrements, tuple(shell_boundaries),
        tuple(shell_cumulatives), tuple(shell_recombined), direct_sum,
        packet_sum, telescoped_energy, exterior_boundary,
        exterior_cumulative, exterior_recombined,
        interior_boundary_residual, interior_cumulative_residual,
        shell_verified, boundary_telescope_verified,
        cumulative_telescope_verified, total_verified,
        detect_sign_pattern(decrements), detect_sign_pattern(shell_boundaries),
        detect_sign_pattern(shell_cumulatives),
    )


def _format_runs(pattern, scales):
    return ", ".join(
        f"{sign}:{scales[start]}..{scales[stop - 1]}"
        for sign, start, stop in pattern.runs
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--base-N", type=int, default=2)
    parser.add_argument("--depth", type=int, default=13)
    args = parser.parse_args()
    if args.bits < 80:
        parser.error("need bits >= 80")
    ctx.prec = args.bits
    result = analyze_dyadic_abel_packets(args.base_N, args.depth)

    print(
        f"precision={args.bits} bits; base-N={result.base_N}; "
        f"depth={result.depth}; last-scale={result.scales[-1]}"
    )
    for N, decrement, boundary, cumulative in zip(
            result.scales, result.shell_decrements,
            result.shell_boundary_packets, result.shell_cumulative_packets):
        print(
            f"N={N}: boundary={boundary.str(12)}; "
            f"cumulative={cumulative.str(12)}; "
            f"decrement={decrement.str(12)}; sign={certified_sign(decrement)}"
        )
    print(
        "sign patterns: "
        f"decrement={result.decrement_sign_pattern.compact} "
        f"({_format_runs(result.decrement_sign_pattern, result.scales)}); "
        f"boundary={result.boundary_sign_pattern.compact}; "
        f"cumulative={result.cumulative_sign_pattern.compact}"
    )
    print(
        "interior telescope residuals: "
        f"boundary={result.interior_boundary_residual.str(8)}; "
        f"cumulative={result.interior_cumulative_residual.str(8)}"
    )
    print(
        "exterior packets: "
        f"boundary={result.exterior_boundary.str(12)}; "
        f"cumulative={result.exterior_cumulative.str(12)}; "
        f"total={result.exterior_recombined.str(12)}"
    )
    print(
        f"direct-sum={result.direct_sum.str(12)}; "
        f"packet-sum={result.packet_sum.str(12)}; "
        f"telescoped-energy={result.telescoped_energy.str(12)}"
    )
    verified = all((
        result.shell_packet_recombination_verified,
        result.boundary_telescope_verified,
        result.cumulative_telescope_verified,
        result.total_telescope_verified,
        result.decrement_sign_pattern.certified,
        result.boundary_sign_pattern.certified,
        result.cumulative_sign_pattern.certified,
    ))
    print(f"verified={verified}")
    if not verified:
        raise SystemExit("a dyadic Abel packet certificate failed")


if __name__ == "__main__":
    main()
