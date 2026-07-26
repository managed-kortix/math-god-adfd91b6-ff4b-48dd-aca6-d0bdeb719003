#!/usr/bin/env python3
"""Divisor-sieve diagnostics for complete dyadic endpoint unit cells.

The sieve constructs the floor-sum intercepts by divisor impulses and evaluates
each unit-cell functional with Arb.  It then reports rigorous negative runs,
prefix minima, sliding fixed-length block tests, and fixed-lag pairings of every
certified negative cell.
"""

import argparse
from dataclasses import dataclass

from flint import arb, ctx

from certify_endpoint_tail import AffineCell, integrate_affine_cell
from mobius_endpoint_surrogate import endpoint_alpha, endpoint_channels
from verify_separated_kernel import ball


@dataclass(frozen=True)
class UnitCell:
    k: int
    u_impulse: object
    d_impulse: object
    f_intercept: object
    d_intercept: object
    J: object
    prefix: object

    @property
    def sign(self):
        if self.J.lower() > 0:
            return "positive"
        if self.J.upper() < 0:
            return "negative"
        return "indeterminate"


@dataclass(frozen=True)
class NegativeRun:
    start: int
    end: int
    total: object

    @property
    def length(self):
        return self.end - self.start + 1


@dataclass(frozen=True)
class PrefixMinimum:
    k: int
    value: object
    record_minima: tuple


@dataclass(frozen=True)
class BlockDiagnostic:
    length: int
    status: str
    tested: int
    minimum_start: int
    minimum_sum: object
    negative_windows: int
    indeterminate_windows: int


@dataclass(frozen=True)
class PairingDiagnostic:
    lag: int
    status: str
    negative_cells: int
    paired_cells: int
    failing_cell: int | None
    weakest_cell: int | None
    weakest_sum: object | None


@dataclass(frozen=True)
class UnitCellAnalysis:
    N: int
    start: int
    cutoff: int
    cells: tuple
    negative_runs: tuple
    prefix_minimum: PrefixMinimum

    @property
    def finite_prefix(self):
        return self.cells[-1].prefix if self.cells else arb(0)


def _validate_range(N, start, cutoff):
    if not isinstance(N, int) or N < 2 or N & (N - 1):
        raise ValueError("N must be a dyadic integer at least 2")
    if (not isinstance(start, int) or not isinstance(cutoff, int)
            or start < 1 or cutoff <= start):
        raise ValueError("need integer bounds with 1 <= start < cutoff")


def divisor_impulses(coefficients, cutoff):
    """Sieve sum_{a|n} coefficients[a-1] for 1 <= n <= cutoff."""
    if not isinstance(cutoff, int) or cutoff < 1:
        raise ValueError("cutoff must be a positive integer")
    impulses = [arb(0) for _ in range(cutoff + 1)]
    for a, coefficient in enumerate(coefficients, 1):
        for multiple in range(a, cutoff + 1, a):
            impulses[multiple] += coefficient
    return tuple(impulses)


def _negative_runs(cells):
    runs = []
    first = None
    total = arb(0)
    previous = None
    for cell in cells:
        if cell.sign == "negative":
            if first is None or cell.k != previous + 1:
                if first is not None:
                    runs.append(NegativeRun(first, previous, total))
                first = cell.k
                total = arb(0)
            total += cell.J
            previous = cell.k
        elif first is not None:
            runs.append(NegativeRun(first, previous, total))
            first = None
            previous = None
            total = arb(0)
    if first is not None:
        runs.append(NegativeRun(first, previous, total))
    return tuple(runs)


def _prefix_minimum(cells, start):
    best_k = start - 1
    best = arb(0)
    records = [(best_k, best)]
    for cell in cells:
        if cell.prefix.lower() < best.lower():
            best_k = cell.k
            best = cell.prefix
        if cell.prefix.upper() < records[-1][1].lower():
            records.append((cell.k, cell.prefix))
    return PrefixMinimum(best_k, best, tuple(records))


def analyze_unit_cells(N, start=1, cutoff=4096):
    """Analyze cells [start, cutoff) using sparse divisor-impulse updates."""
    _validate_range(N, start, cutoff)
    alpha = endpoint_alpha(N)
    u, d = endpoint_channels(N)
    u_impulses = divisor_impulses(u, cutoff)
    d_impulses = divisor_impulses(d, cutoff)
    f_slope = sum((value / a for a, value in enumerate(u, 1)), arb(0))
    d_slope = sum((value / a for a, value in enumerate(d, 1)), arb(0))
    f_intercept = ball(1)
    d_intercept = arb(0)
    prefix = arb(0)
    cells = []
    scale = ball(alpha)
    for k in range(1, cutoff):
        f_intercept = f_intercept - u_impulses[k]
        d_intercept = d_intercept - d_impulses[k]
        if k < start:
            continue
        c2 = 2 * f_slope * d_slope - scale * d_slope * d_slope
        c1 = (
            2 * (f_slope * d_intercept + f_intercept * d_slope)
            - 2 * scale * d_slope * d_intercept
        )
        c0 = 2 * f_intercept * d_intercept - scale * d_intercept**2
        cell = AffineCell(
            k, f_slope, f_intercept, d_slope, d_intercept, (c2, c1, c0)
        )
        value = integrate_affine_cell(cell)
        prefix = prefix + value
        cells.append(UnitCell(
            k, u_impulses[k], d_impulses[k], f_intercept, d_intercept,
            value, prefix,
        ))
    cell_tuple = tuple(cells)
    return UnitCellAnalysis(
        N, start, cutoff, cell_tuple, _negative_runs(cell_tuple),
        _prefix_minimum(cell_tuple, start),
    )


def contiguous_block_diagnostic(cells, length):
    """Test whether every sliding contiguous block of a fixed length is >= 0."""
    if not isinstance(length, int) or length < 1:
        raise ValueError("block length must be a positive integer")
    if length > len(cells):
        raise ValueError("block length exceeds the analyzed range")
    window = sum((cell.J for cell in cells[:length]), arb(0))
    minimum_start = cells[0].k
    minimum_sum = window
    negative = int(window.upper() < 0)
    indeterminate = int(not (window.lower() >= 0 or window.upper() < 0))
    for index in range(1, len(cells) - length + 1):
        window += cells[index + length - 1].J - cells[index - 1].J
        if window.lower() < minimum_sum.lower():
            minimum_start = cells[index].k
            minimum_sum = window
        negative += int(window.upper() < 0)
        indeterminate += int(not (window.lower() >= 0 or window.upper() < 0))
    status = "failure" if negative else ("indeterminate" if indeterminate else "success")
    return BlockDiagnostic(
        length, status, len(cells) - length + 1, minimum_start, minimum_sum,
        negative, indeterminate,
    )


def search_block_lengths(cells, maximum):
    """Return all diagnostics through maximum and the first rigorous success."""
    if not isinstance(maximum, int) or maximum < 1:
        raise ValueError("maximum block length must be a positive integer")
    diagnostics = tuple(
        contiguous_block_diagnostic(cells, length)
        for length in range(1, min(maximum, len(cells)) + 1)
    )
    first_success = next(
        (diagnostic for diagnostic in diagnostics
         if diagnostic.status == "success"),
        None,
    )
    return diagnostics, first_success


def fixed_lag_pairing_diagnostic(cells, lag):
    """Test J_k + J_(k+lag) for every certified negative J_k."""
    if not isinstance(lag, int) or lag == 0:
        raise ValueError("pairing lag must be a nonzero integer")
    by_k = {cell.k: cell for cell in cells}
    negatives = [cell for cell in cells if cell.sign == "negative"]
    paired = 0
    failing = None
    weakest_cell = None
    weakest_sum = None
    indeterminate = False
    for cell in negatives:
        partner = by_k.get(cell.k + lag)
        if partner is None:
            if failing is None:
                failing = cell.k
            continue
        pair_sum = cell.J + partner.J
        paired += 1
        if weakest_sum is None or pair_sum.lower() < weakest_sum.lower():
            weakest_cell = cell.k
            weakest_sum = pair_sum
        if pair_sum.upper() < 0:
            if failing is None:
                failing = cell.k
            continue
        if pair_sum.lower() < 0:
            indeterminate = True
    status = "failure" if failing is not None else (
        "indeterminate" if indeterminate else "success"
    )
    return PairingDiagnostic(
        lag, status, len(negatives), paired, failing, weakest_cell, weakest_sum
    )


def _format_ball(value, digits=12):
    return value.str(digits)


def _print_analysis(analysis, block_lengths, pair_lags, max_block):
    negative_count = sum(run.length for run in analysis.negative_runs)
    print(
        f"N={analysis.N}->2N={2 * analysis.N}; cells="
        f"[{analysis.start},{analysis.cutoff}); negative={negative_count}; "
        f"runs={len(analysis.negative_runs)}"
    )
    print(f"  prefix={_format_ball(analysis.finite_prefix)}")
    minimum = analysis.prefix_minimum
    print(
        f"  prefix-min k={minimum.k}; value={_format_ball(minimum.value)}; "
        f"decisive-records={len(minimum.record_minima)}"
    )
    if analysis.negative_runs:
        displayed_runs = analysis.negative_runs[:12]
        rendered = ", ".join(
            f"{run.start}-{run.end}:{_format_ball(run.total, 8)}"
            for run in displayed_runs
        )
        if len(analysis.negative_runs) > len(displayed_runs):
            rendered += f", ... ({len(analysis.negative_runs) - len(displayed_runs)} more)"
        print(f"  negative-runs {rendered}")
    else:
        print("  negative-runs none (SUCCESS: cellwise nonnegative on range)")
    for length in block_lengths:
        if length > len(analysis.cells):
            continue
        diagnostic = contiguous_block_diagnostic(analysis.cells, length)
        print(
            f"  blocks L={length}: {diagnostic.status.upper()}; "
            f"min@{diagnostic.minimum_start}={_format_ball(diagnostic.minimum_sum)}; "
            f"negative={diagnostic.negative_windows}/{diagnostic.tested}"
        )
    searched, first_success = search_block_lengths(analysis.cells, max_block)
    if first_success is None:
        print(
            f"  block-search L=1..{len(searched)}: FAILURE; "
            "no universally nonnegative length"
        )
    else:
        print(
            f"  block-search L=1..{len(searched)}: SUCCESS first at "
            f"L={first_success.length}; min@{first_success.minimum_start}="
            f"{_format_ball(first_success.minimum_sum)}"
        )
    for lag in pair_lags:
        diagnostic = fixed_lag_pairing_diagnostic(analysis.cells, lag)
        weakest = "none" if diagnostic.weakest_sum is None else (
            f"k={diagnostic.weakest_cell}, sum={_format_ball(diagnostic.weakest_sum)}"
        )
        failure = "" if diagnostic.failing_cell is None else (
            f"; first-failure={diagnostic.failing_cell}"
        )
        print(
            f"  pairing lag={lag:+d}: {diagnostic.status.upper()}; "
            f"paired={diagnostic.paired_cells}/{diagnostic.negative_cells}; "
            f"weakest {weakest}{failure}"
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--N", type=int, nargs="+", default=[2, 4, 8, 16, 32, 64])
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--cutoff", type=int, default=4096)
    parser.add_argument("--blocks", type=int, nargs="+", default=[1, 2, 3, 4, 8, 16])
    parser.add_argument("--max-block", type=int, default=128)
    parser.add_argument("--pair-lags", type=int, nargs="+", default=[-4, -3, -2, -1, 1, 2, 3, 4])
    args = parser.parse_args()
    if args.bits < 80:
        parser.error("need bits >= 80")
    ctx.prec = args.bits
    for N in args.N:
        try:
            analysis = analyze_unit_cells(N, args.start, args.cutoff)
        except ValueError as error:
            parser.error(str(error))
        _print_analysis(analysis, args.blocks, args.pair_lags, args.max_block)


if __name__ == "__main__":
    main()
