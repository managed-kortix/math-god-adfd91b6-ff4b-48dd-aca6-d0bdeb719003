#!/usr/bin/env python3
"""Certified reserve/defect analysis for complete dyadic endpoint prefixes.

The interval [1,T] is split into the initial reserve [1,N] and the later
segment [N,T].  Unit-cell indices are therefore 1 <= k < N and N <= k < T.
All reported numerical quantities are Arb enclosures.
"""

import argparse
from dataclasses import dataclass
from fractions import Fraction

from flint import arb, ctx

from analyze_unit_cells import analyze_unit_cells
from certify_endpoint_tail import (
    elementary_remainder_constant, finite_endpoint_prefix,
)
from mobius_endpoint_surrogate import endpoint_alpha, endpoint_channels
from verify_separated_kernel import ball


@dataclass(frozen=True)
class AbelMinimum:
    k: int
    value: object


@dataclass(frozen=True)
class AbelDiagnostics:
    start: int
    stop: int
    z_minimum: AbelMinimum
    h_minimum: AbelMinimum
    reconstructed_sum: object


@dataclass(frozen=True)
class DriftFreeCell:
    k: int
    r: object
    s: object
    R: object
    V: object
    w: object
    R_coefficient: object
    V_coefficient: object
    w_coefficient: object
    R_component: object
    V_component: object
    w_component: object
    reconstructed_J: object


@dataclass(frozen=True)
class DriftFreeDiagnostics:
    start: int
    stop: int
    cells: tuple
    R_sum: object
    V_sum: object
    w_sum: object
    reconstructed_sum: object
    prefixes_verified: bool
    max_abs_r: object
    max_abs_s: object
    R_coefficient_bound: object
    V_coefficient_bound: object
    w_coefficient_bound: object
    coefficient_tail_radius: object
    pointwise_tail_radius: object


@dataclass(frozen=True)
class EndpointPrefixAnalysis:
    N: int
    T: int
    reserve: object
    later_contribution: object
    later_defect: object
    defect_endpoint: int
    complete_prefix: object
    tail_radius: object
    reserve_defect_ratio: object | None
    abel: AbelDiagnostics
    drift_free: DriftFreeDiagnostics
    psi_verified: bool
    direct_prefix: object | None

    @property
    def direct_agrees(self):
        return self.direct_prefix is None or self.complete_prefix.overlaps(
            self.direct_prefix
        )


def chebyshev_psi_table(limit):
    """Return psi(k)=sum_{p^j<=k} log(p), independently by prime powers."""
    if not isinstance(limit, int) or limit < 1:
        raise ValueError("psi limit must be a positive integer")
    prime = bytearray(b"\x01") * (limit + 1)
    prime[0:2] = b"\x00\x00"
    for p in range(2, int(limit**0.5) + 1):
        if prime[p]:
            prime[p * p:limit + 1:p] = b"\x00" * (
                (limit - p * p) // p + 1
            )
    increments = [arb(0) for _ in range(limit + 1)]
    for p in range(2, limit + 1):
        if not prime[p]:
            continue
        value = p
        log_p = ball(p).log()
        while value <= limit:
            increments[value] += log_p
            if value > limit // p:
                break
            value *= p
    psi = [arb(0) for _ in range(limit + 1)]
    for k in range(1, limit + 1):
        psi[k] = psi[k - 1] + increments[k]
    return tuple(psi)


def verify_initial_psi_identity(cells, N):
    """Verify b_k=e_k=-psi(k)/log(N) for every available k <= N."""
    psi = chebyshev_psi_table(N)
    log_N = ball(N).log()
    checked = 0
    for cell in cells:
        if cell.k > N:
            break
        expected = -psi[cell.k] / log_N
        if not cell.f_intercept.overlaps(expected):
            return False
        if not cell.d_intercept.overlaps(expected):
            return False
        checked += 1
    return checked == N


def _minimum(records, initial_k=0):
    best = AbelMinimum(initial_k, arb(0))
    for k, value in records:
        if value.lower() < best.value.lower():
            best = AbelMinimum(k, value)
    return best


def _abel_diagnostics_with_slopes(cells, alpha, A, D):
    start = cells[0].k
    z_total = arb(0)
    h_total = arb(0)
    z_records = []
    h_records = []
    scale = ball(alpha)
    for cell in cells:
        b = cell.f_intercept
        e = cell.d_intercept
        z = 2 * D * b + 2 * (A - scale * D) * e
        h = 2 * b * e - scale * e * e
        z_total += z
        h_total += h
        z_records.append((cell.k, z_total))
        h_records.append((cell.k, h_total))

    c2 = 2 * A * D - scale * D * D
    reconstructed = c2 * len(cells)
    last = cells[-1].k
    reconstructed += z_records[-1][1] * (
        ball(last + 1).log() - ball(last).log()
    )
    reconstructed += h_records[-1][1] / (last * (last + 1))
    for (k, z_prefix), (_, h_prefix) in zip(
            z_records[:-1], h_records[:-1]):
        reconstructed += z_prefix * ball(
            Fraction((k + 1) * (k + 1), k * (k + 2))
        ).log()
        reconstructed += 2 * h_prefix / (k * (k + 1) * (k + 2))
    return AbelDiagnostics(
        start, cells[-1].k + 1, _minimum(z_records, start - 1),
        _minimum(h_records, start - 1), reconstructed,
    )


def drift_free_cell_identity(cell, alpha, A, D):
    """Re-express J_k in positive cell moments without large cancellation.

    Here r_k=Ak+b_k and s_k=Dk+e_k are the right-limit channel values at
    the left endpoint.  R, V, and w are respectively the moments of
    x^2, x, and 1 against (k+x)^-2 on 0 <= x <= 1.
    """
    k = cell.k
    scale = ball(alpha)
    log_ratio = ball(k + 1).log() - ball(k).log()
    r = A * k + cell.f_intercept
    s = D * k + cell.d_intercept
    R = ball(Fraction(2 * k + 1, k + 1)) - 2 * k * log_ratio
    V = log_ratio - ball(Fraction(1, k + 1))
    w = ball(Fraction(1, k * (k + 1)))
    R_coefficient = 2 * A * D - scale * D * D
    V_coefficient = 2 * (A * s + D * r) - 2 * scale * D * s
    w_coefficient = 2 * r * s - scale * s * s
    R_component = R_coefficient * R
    V_component = V_coefficient * V
    w_component = w_coefficient * w
    return DriftFreeCell(
        k, r, s, R, V, w, R_coefficient, V_coefficient, w_coefficient,
        R_component, V_component, w_component,
        R_component + V_component + w_component,
    )


def _upper_abs(value):
    return max(abs(value.lower()), abs(value.upper()))


def _drift_free_diagnostics(cells, alpha, A, D, u, d, T):
    identities = tuple(
        drift_free_cell_identity(cell, alpha, A, D) for cell in cells
    )
    R_sum = sum((cell.R_component for cell in identities), arb(0))
    V_sum = sum((cell.V_component for cell in identities), arb(0))
    w_sum = sum((cell.w_component for cell in identities), arb(0))
    reconstructed = R_sum + V_sum + w_sum
    direct_prefix = arb(0)
    rebuilt_prefix = arb(0)
    prefixes_verified = True
    for source, identity in zip(cells, identities):
        direct_prefix += source.J
        rebuilt_prefix += identity.reconstructed_J
        prefixes_verified &= source.J.overlaps(identity.reconstructed_J)
        prefixes_verified &= direct_prefix.overlaps(rebuilt_prefix)

    max_r = max((_upper_abs(cell.r) for cell in identities), default=arb(0))
    max_s = max((_upper_abs(cell.s) for cell in identities), default=arb(0))
    f_bound = ball(1) + sum((abs(ball(value)) for value in u), arb(0))
    d_bound = sum((abs(ball(value)) for value in d), arb(0))
    scale = ball(alpha)
    R_bound = abs(2 * A * D - scale * D * D)
    V_bound = (
        2 * abs(A) * d_bound + 2 * abs(D) * f_bound
        + 2 * scale * abs(D) * d_bound
    )
    w_bound = 2 * f_bound * d_bound + scale * d_bound * d_bound
    coefficient_tail = (R_bound + V_bound + w_bound) / T
    pointwise_tail = elementary_remainder_constant(u, d, alpha) / T
    return DriftFreeDiagnostics(
        cells[0].k, cells[-1].k + 1, identities, R_sum, V_sum, w_sum,
        reconstructed, prefixes_verified, ball(max_r), ball(max_s), R_bound,
        V_bound, w_bound, coefficient_tail, pointwise_tail,
    )


def analyze_endpoint_prefix(N, T, compare_direct=True):
    """Certify the complete [1,T] prefix and its anchored decomposition."""
    if not isinstance(N, int) or N < 2 or N & (N - 1):
        raise ValueError("N must be a dyadic integer at least 2")
    if not isinstance(T, int) or T <= N:
        raise ValueError("T must be an integer larger than N")

    unit = analyze_unit_cells(N, 1, T)
    reserve_cells = tuple(cell for cell in unit.cells if cell.k < N)
    later_cells = tuple(cell for cell in unit.cells if cell.k >= N)
    reserve = sum((cell.J for cell in reserve_cells), arb(0))
    later = sum((cell.J for cell in later_cells), arb(0))

    running = arb(0)
    worst = AbelMinimum(N, arb(0))
    for cell in later_cells:
        running += cell.J
        if running.lower() < worst.value.lower():
            worst = AbelMinimum(cell.k + 1, running)
    defect = -worst.value if worst.value.upper() < 0 else arb(0)
    ratio = reserve / defect if defect.lower() > 0 else None

    u, d = endpoint_channels(N)
    A = sum((value / a for a, value in enumerate(u, 1)), arb(0))
    D = sum((value / a for a, value in enumerate(d, 1)), arb(0))
    abel = _abel_diagnostics_with_slopes(later_cells, endpoint_alpha(N), A, D)
    drift_free = _drift_free_diagnostics(
        unit.cells, endpoint_alpha(N), A, D, u, d, T
    )
    complete = reserve + later
    tail = elementary_remainder_constant(u, d, endpoint_alpha(N)) / T
    direct = None
    if compare_direct:
        direct = finite_endpoint_prefix(1, T, u, d, endpoint_alpha(N))
    return EndpointPrefixAnalysis(
        N, T, reserve, later, defect, worst.k, complete, tail, ratio, abel,
        drift_free, verify_initial_psi_identity(unit.cells, N), direct,
    )


def _fmt(value, digits=14):
    return value.str(digits)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--N", type=int, nargs="+", default=[8, 16, 32, 64, 128])
    parser.add_argument("--T-multiple", type=int, default=16)
    parser.add_argument("--skip-direct", action="store_true")
    args = parser.parse_args()
    if args.bits < 80 or args.T_multiple < 2:
        parser.error("need bits >= 80 and T-multiple >= 2")
    ctx.prec = args.bits
    print(f"precision={args.bits} bits; T={args.T_multiple}N")
    previous = None
    failed = False
    for N in args.N:
        try:
            result = analyze_endpoint_prefix(
                N, args.T_multiple * N, not args.skip_direct
            )
        except ValueError as error:
            parser.error(str(error))
        ratio = "infinite (no anchored defect)" if result.reserve_defect_ratio is None else _fmt(result.reserve_defect_ratio)
        print(f"N={N}; T={result.T}")
        print(f"  reserve[1,N]={_fmt(result.reserve)}")
        print(
            f"  later[N,T]={_fmt(result.later_contribution)}; "
            f"anchored-defect={_fmt(result.later_defect)}@{result.defect_endpoint}; "
            f"reserve/defect={ratio}"
        )
        print(
            f"  complete-prefix={_fmt(result.complete_prefix)}; "
            f"tail-radius={_fmt(result.tail_radius)}"
        )
        drift = result.drift_free
        print(
            f"  drift-free components R={_fmt(drift.R_sum)}; "
            f"V={_fmt(drift.V_sum)}; w={_fmt(drift.w_sum)}; "
            f"prefixes={drift.prefixes_verified}"
        )
        print(
            f"  observed |r|<={_fmt(drift.max_abs_r)}; "
            f"|s|<={_fmt(drift.max_abs_s)}; coefficient bounds "
            f"R={_fmt(drift.R_coefficient_bound)}, "
            f"V={_fmt(drift.V_coefficient_bound)}, "
            f"w={_fmt(drift.w_coefficient_bound)}"
        )
        print(
            f"  bounded coefficient-tail={_fmt(drift.coefficient_tail_radius)}; "
            f"pointwise-tail={_fmt(drift.pointwise_tail_radius)}"
        )
        print(
            f"  Abel min Z={_fmt(result.abel.z_minimum.value)}"
            f"@{result.abel.z_minimum.k}; min H={_fmt(result.abel.h_minimum.value)}"
            f"@{result.abel.h_minimum.k}; identity="
            f"{result.abel.reconstructed_sum.overlaps(result.later_contribution)}"
        )
        print(
            f"  psi-identity={result.psi_verified}; "
            f"direct-prefix={result.direct_agrees}"
        )
        if previous is not None:
            reserve_scale = result.reserve / previous.reserve
            tail_scale = result.tail_radius / previous.tail_radius
            print(
                f"  dyadic scaling reserve={_fmt(reserve_scale)} "
                f"(exponent={_fmt(-reserve_scale.log() / ball(2).log())}); "
                f"tail-radius={_fmt(tail_scale)} "
                f"(exponent={_fmt(tail_scale.log() / ball(2).log())})"
            )
        previous = result
        failed |= not (
            result.psi_verified and result.direct_agrees
            and result.abel.reconstructed_sum.overlaps(result.later_contribution)
            and result.drift_free.prefixes_verified
            and result.drift_free.reconstructed_sum.overlaps(
                result.complete_prefix
            )
        )
    if failed:
        raise SystemExit("a certified identity comparison failed")


if __name__ == "__main__":
    main()
