#!/usr/bin/env python3
"""Certified decomposition of the post-reserve weighted g_k tail.

For N <= k < H <= 2N, this analyzer expands the drift-free coefficient

    g_k = 2 r_k s_k - alpha s_k^2

using the exact truncated Mobius transform T_N(k).  Integer arithmetic is used
for the Mobius sieve and Arb balls are used for every logarithm and sum.
"""

import argparse
from dataclasses import dataclass
from fractions import Fraction

from flint import arb, ctx

from analyze_endpoint_prefix import chebyshev_psi_table, drift_free_cell_identity
from analyze_unit_cells import analyze_unit_cells
from mobius_endpoint_surrogate import endpoint_alpha, endpoint_channels
from verify_separated_kernel import ball


@dataclass(frozen=True)
class WeightedGTailCell:
    k: int
    psi_over_log_N: object
    T_N: object
    baseline_r: object
    baseline_s: object
    baseline_slope: object
    baseline_cross: object
    baseline_psi_square: object
    baseline: object
    linear: object
    quadratic: object
    reconstructed_g: object
    drift_free_g: object
    weight: object
    weighted_baseline: object
    weighted_linear: object
    weighted_quadratic: object
    weighted_reconstruction: object
    identities_verified: bool


@dataclass(frozen=True)
class WeightedGTailHorizon:
    start: int
    stop: int
    baseline_slope_sum: object
    baseline_cross_sum: object
    baseline_psi_square_sum: object
    baseline_sum: object
    linear_sum: object
    quadratic_sum: object
    reconstructed_sum: object
    drift_free_sum: object
    cells_verified: bool
    prefixes_verified: bool


@dataclass(frozen=True)
class WeightedGTailAnalysis:
    N: int
    alpha: Fraction
    A: object
    D: object
    cells: tuple
    horizons: tuple


def mobius_table(limit):
    """Return exact integer mu(n), 0 <= n <= limit, by a linear sieve."""
    if not isinstance(limit, int) or limit < 1:
        raise ValueError("Mobius limit must be a positive integer")
    mu = [0] * (limit + 1)
    mu[1] = 1
    primes = []
    composite = bytearray(limit + 1)
    for n in range(2, limit + 1):
        if not composite[n]:
            primes.append(n)
            mu[n] = -1
        for prime in primes:
            product = n * prime
            if product > limit:
                break
            composite[product] = 1
            if n % prime == 0:
                mu[product] = 0
                break
            mu[product] = -mu[n]
    return tuple(mu)


def truncated_mobius_transform(N, limit, mu=None):
    """Return Arb balls T_N(k) for 0 <= k <= limit, with limit <= 2N."""
    if not isinstance(N, int) or N < 2:
        raise ValueError("N must be an integer at least 2")
    if not isinstance(limit, int) or limit < N or limit > 2 * N:
        raise ValueError("transform limit must satisfy N <= limit <= 2N")
    if mu is None:
        mu = mobius_table(limit)
    if len(mu) <= limit:
        raise ValueError("Mobius table is shorter than the transform limit")
    log_N = ball(N).log()
    values = [arb(0) for _ in range(limit + 1)]
    running = arb(0)
    for k in range(N + 1, limit + 1):
        if mu[k]:
            running += mu[k] * ball(Fraction(N, k)).log() / log_N
        values[k] = running
    return tuple(values)


def _weighted_g_cell(cell, identity, alpha, A, D, psi, transform, log_N):
    k = cell.k
    scale = ball(alpha)
    p = psi[k] / log_N
    T = transform[k]
    r0 = k * A - p
    s0 = k * D - p
    baseline_slope = k * k * (2 * A * D - scale * D * D)
    baseline_cross = -2 * k * p * (A + (1 - scale) * D)
    baseline_psi_square = (2 - scale) * p * p
    baseline = baseline_slope + baseline_cross + baseline_psi_square
    linear = 2 * r0 * T / scale
    quadratic = T * T / scale
    reconstructed = baseline + linear + quadratic
    w = identity.w
    weighted_baseline = baseline * w
    weighted_linear = linear * w
    weighted_quadratic = quadratic * w
    weighted_reconstruction = reconstructed * w
    verified = (
        baseline.overlaps(2 * r0 * s0 - scale * s0 * s0)
        and identity.r.overlaps(r0 + T)
        and identity.s.overlaps(s0 + T / scale)
        and reconstructed.overlaps(identity.w_coefficient)
        and weighted_reconstruction.overlaps(identity.w_component)
    )
    return WeightedGTailCell(
        k, p, T, r0, s0, baseline_slope, baseline_cross,
        baseline_psi_square, baseline, linear, quadratic, reconstructed,
        identity.w_coefficient, w, weighted_baseline, weighted_linear,
        weighted_quadratic, weighted_reconstruction, verified,
    )


def _horizon(cells, stop):
    selected = tuple(cell for cell in cells if cell.k < stop)
    slope = arb(0)
    cross = arb(0)
    psi_square = arb(0)
    baseline = arb(0)
    linear = arb(0)
    quadratic = arb(0)
    rebuilt = arb(0)
    direct = arb(0)
    prefixes_verified = True
    for cell in selected:
        slope += cell.baseline_slope * cell.weight
        cross += cell.baseline_cross * cell.weight
        psi_square += cell.baseline_psi_square * cell.weight
        baseline += cell.weighted_baseline
        linear += cell.weighted_linear
        quadratic += cell.weighted_quadratic
        rebuilt += cell.weighted_reconstruction
        direct += cell.drift_free_g * cell.weight
        prefixes_verified &= rebuilt.overlaps(direct)
    return WeightedGTailHorizon(
        cells[0].k, stop, slope, cross, psi_square, baseline, linear,
        quadratic, rebuilt, direct,
        all(cell.identities_verified for cell in selected), prefixes_verified,
    )


def analyze_weighted_g_tail(N, horizons=None):
    """Analyze weighted g_k over each half-open interval [N, H)."""
    if not isinstance(N, int) or N < 2 or N & (N - 1):
        raise ValueError("N must be a dyadic integer at least 2")
    if horizons is None:
        horizons = (2 * N,)
    horizons = tuple(sorted(set(horizons)))
    if not horizons or any(
            not isinstance(stop, int) or stop <= N or stop > 2 * N
            for stop in horizons):
        raise ValueError("horizons must be integer endpoints with N < H <= 2N")

    maximum = horizons[-1]
    unit = analyze_unit_cells(N, N, maximum)
    alpha = endpoint_alpha(N)
    u, d = endpoint_channels(N)
    A = sum((value / a for a, value in enumerate(u, 1)), arb(0))
    D = sum((value / a for a, value in enumerate(d, 1)), arb(0))
    psi = chebyshev_psi_table(maximum - 1)
    transform = truncated_mobius_transform(N, maximum - 1)
    log_N = ball(N).log()
    cells = []
    for cell in unit.cells:
        identity = drift_free_cell_identity(cell, alpha, A, D)
        cells.append(_weighted_g_cell(
            cell, identity, alpha, A, D, psi, transform, log_N
        ))
    cells = tuple(cells)
    return WeightedGTailAnalysis(
        N, alpha, A, D, cells,
        tuple(_horizon(cells, stop) for stop in horizons),
    )


def _fmt(value, digits=14):
    return value.str(digits)


def _sign(value):
    if value.lower() > 0:
        return "+"
    if value.upper() < 0:
        return "-"
    if value.is_zero():
        return "0"
    return "?"


def _parse_multiple(text):
    try:
        value = Fraction(text)
    except (ValueError, ZeroDivisionError) as error:
        raise argparse.ArgumentTypeError(str(error)) from error
    if value <= 1 or value > 2:
        raise argparse.ArgumentTypeError("horizon multiples must lie in (1,2]")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--N", type=int, nargs="+", default=[8, 16, 32, 64, 128])
    parser.add_argument(
        "--horizon-multiples", type=_parse_multiple, nargs="+",
        default=[Fraction(2)], metavar="RATIO",
    )
    args = parser.parse_args()
    if args.bits < 80:
        parser.error("need bits >= 80")
    ctx.prec = args.bits
    previous = {}
    failed = False
    print(f"precision={args.bits} bits")
    for N in args.N:
        requested = []
        for multiple in args.horizon_multiples:
            endpoint = N * multiple
            if endpoint.denominator != 1:
                parser.error(f"{multiple}N is not integral for N={N}")
            requested.append((endpoint.numerator, multiple))
        requested = sorted(set(requested))
        try:
            result = analyze_weighted_g_tail(
                N, [endpoint for endpoint, _ in requested]
            )
        except ValueError as error:
            parser.error(str(error))
        for (_, multiple), horizon in zip(requested, result.horizons):
            terms = (
                ("baseline", horizon.baseline_sum),
                ("linear", horizon.linear_sum),
                ("quadratic", horizon.quadratic_sum),
                ("total", horizon.reconstructed_sum),
            )
            rendered = "; ".join(
                f"{name}={_sign(value)}{_fmt(abs(value))}"
                for name, value in terms
            )
            print(f"N={N}; H={horizon.stop} ({multiple}N): {rendered}")
            print(
                "  baseline pieces "
                f"slope={_sign(horizon.baseline_slope_sum)}{_fmt(abs(horizon.baseline_slope_sum))}; "
                f"psi-cross={_sign(horizon.baseline_cross_sum)}{_fmt(abs(horizon.baseline_cross_sum))}; "
                f"psi^2={_sign(horizon.baseline_psi_square_sum)}{_fmt(abs(horizon.baseline_psi_square_sum))}; "
                f"cells={horizon.cells_verified}; prefixes={horizon.prefixes_verified}"
            )
            old = previous.get(multiple)
            if old is not None:
                scales = []
                for name, value in terms:
                    old_value = dict(old)[name]
                    ratio = abs(value) / abs(old_value)
                    exponent = ratio.log() / ball(2).log()
                    scales.append(f"{name}={_fmt(ratio)} (p={_fmt(exponent)})")
                print("  dyadic |value| scaling " + "; ".join(scales))
            previous[multiple] = terms
            failed |= not (
                horizon.cells_verified and horizon.prefixes_verified
                and horizon.reconstructed_sum.overlaps(horizon.drift_free_sum)
            )
    if failed:
        raise SystemExit("a certified weighted-g identity comparison failed")


if __name__ == "__main__":
    main()
