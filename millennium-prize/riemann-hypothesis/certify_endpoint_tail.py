#!/usr/bin/env python3
"""Arb certificates for complete dyadic endpoint functionals.

The calculation stays in the sawtooth representation.  On every open unit
interval all {t/a}, a <= 2N, are affine, so the endpoint integrand is a
quadratic divided by t^2 and has an elementary exact antiderivative.  An
independent calculation constructs F_N and F_2N separately and encloses
P_N-P_2N.  No Fourier expansion or common period is used.
"""

import argparse
import time
from dataclasses import dataclass
from fractions import Fraction

from flint import arb, ctx

from mobius_endpoint_surrogate import endpoint_alpha, endpoint_channels, mobius
from verify_separated_kernel import ball


@dataclass(frozen=True)
class AffineCell:
    left: int
    f_slope: object
    f_intercept: object
    d_slope: object
    d_intercept: object
    quadratic: tuple


@dataclass(frozen=True)
class EndpointTailCertificate:
    N: int
    alpha: Fraction
    start: int
    cutoff: int
    finite_prefix: object
    remainder_radius: object
    lower_bound: object
    upper_bound: object
    remainder_constant: object
    elapsed: float

    @property
    def is_positive(self):
        return self.lower_bound > 0

    @property
    def sign(self):
        if self.lower_bound > 0:
            return "positive"
        if self.upper_bound < 0:
            return "negative"
        return "indeterminate"


@dataclass(frozen=True)
class EndpointComparison:
    endpoint: EndpointTailCertificate
    direct_difference: EndpointTailCertificate
    scaled_endpoint: object

    @property
    def agrees(self):
        direct = self.direct_difference.finite_prefix + arb(
            0, self.direct_difference.remainder_radius.upper()
        )
        return self.scaled_endpoint.overlaps(direct)


def _validate_source_channels(u, d):
    if len(u) != len(d) or not u:
        raise ValueError("source channels must have equal positive length")
    if any(not isinstance(value, (Fraction, arb)) for value in tuple(u) + tuple(d)):
        raise ValueError("source channels must contain Fractions or Arb balls")


def affine_cell(k, u, d, alpha=Fraction(1, 3)):
    """Return the affine channels and quadratic numerator on (k,k+1)."""
    _validate_source_channels(u, d)
    if not isinstance(k, int) or k < 0:
        raise ValueError("cell index must be a nonnegative integer")
    if not isinstance(alpha, Fraction) or alpha <= 0:
        raise ValueError("alpha must be a positive Fraction")

    f_slope = sum((ball(value) / a for a, value in enumerate(u, 1)), arb(0))
    d_slope = sum((ball(value) / a for a, value in enumerate(d, 1)), arb(0))
    f_intercept = ball(1) - sum(
        (ball(value) * (k // a) for a, value in enumerate(u, 1)), arb(0)
    )
    d_intercept = -sum(
        (ball(value) * (k // a) for a, value in enumerate(d, 1)), arb(0)
    )
    scale = ball(alpha)
    c2 = 2 * f_slope * d_slope - scale * d_slope * d_slope
    c1 = (
        2 * (f_slope * d_intercept + f_intercept * d_slope)
        - 2 * scale * d_slope * d_intercept
    )
    c0 = (
        2 * f_intercept * d_intercept
        - scale * d_intercept * d_intercept
    )
    return AffineCell(
        k, f_slope, f_intercept, d_slope, d_intercept, (c2, c1, c0)
    )


def integrate_affine_cell(cell):
    """Integrate (c2*t^2+c1*t+c0)/t^2 on one unit cell."""
    k = cell.left
    if k < 1:
        raise ValueError("weighted cell integration requires a positive left endpoint")
    c2, c1, c0 = cell.quadratic
    log_ratio = ball(k + 1).log() - ball(k).log()
    return c2 + c1 * log_ratio + c0 * ball(Fraction(1, k * (k + 1)))


def finite_endpoint_prefix(start, cutoff, u=None, d=None,
                           alpha=Fraction(1, 3)):
    """Certify the direct-breakpoint integral over [start, cutoff]."""
    if (not isinstance(start, int) or not isinstance(cutoff, int)
            or start < 1 or cutoff < start):
        raise ValueError("start and cutoff must be integers with 1 <= start <= cutoff")
    if u is None or d is None:
        if (u is None) != (d is None):
            raise ValueError("u and d must be supplied together")
        u, d = endpoint_channels(4)
    return sum(
        (integrate_affine_cell(affine_cell(k, u, d, alpha))
         for k in range(start, cutoff)),
        arb(0),
    )


def restricted_channels(N):
    """Construct F_N sawtooth coefficients independently of endpoint channels."""
    if not isinstance(N, int) or N < 2:
        raise ValueError("N must be an integer at least 2")
    log_N = ball(N).log()
    coefficients = []
    for a in range(1, N + 1):
        mu = mobius(a)
        coefficient = arb(0)
        if mu:
            coefficient = ball(mu) * (1 - ball(a).log() / log_N)
        coefficients.append(coefficient)
    return tuple(coefficients)


def _affine_sawtooth(k, coefficients):
    slope = sum(
        (value / a for a, value in enumerate(coefficients, 1)), arb(0)
    )
    intercept = ball(1) - sum(
        (value * (k // a) for a, value in enumerate(coefficients, 1)), arb(0)
    )
    return slope, intercept


def finite_energy_difference_prefix(N, start, cutoff):
    """Directly integrate F_N^2-F_2N^2 over [start, cutoff]."""
    if (not isinstance(start, int) or not isinstance(cutoff, int)
            or start < 1 or cutoff < start):
        raise ValueError("start and cutoff must be integers with 1 <= start <= cutoff")
    old = restricted_channels(N)
    new = restricted_channels(2 * N)
    total = arb(0)
    for k in range(start, cutoff):
        a1, b1 = _affine_sawtooth(k, old)
        a2, b2 = _affine_sawtooth(k, new)
        cell = AffineCell(
            k, a1, b1, a2, b2,
            (a1 * a1 - a2 * a2,
             2 * (a1 * b1 - a2 * b2),
             b1 * b1 - b2 * b2),
        )
        total += integrate_affine_cell(cell)
    return total


def elementary_remainder_constant(u, d, alpha=Fraction(1, 3)):
    """Return C with |2*f*d-alpha*d^2| <= C pointwise."""
    _validate_source_channels(u, d)
    f_bound = ball(1) + sum((abs(ball(value)) for value in u), arb(0))
    d_bound = sum((abs(ball(value)) for value in d), arb(0))
    return 2 * f_bound * d_bound + ball(alpha) * d_bound * d_bound


def certify_endpoint_tail(start=1, cutoff=4096, N=4):
    """Enclose the complete N -> 2N endpoint functional on [start,infinity)."""
    if not isinstance(cutoff, int) or cutoff <= start:
        raise ValueError("cutoff must be an integer larger than start")
    started = time.perf_counter()
    alpha = endpoint_alpha(N)
    u, d = endpoint_channels(N)
    prefix = finite_endpoint_prefix(start, cutoff, u, d, alpha)
    constant = elementary_remainder_constant(u, d, alpha)
    radius = constant / cutoff
    enclosure = prefix + arb(0, radius.upper())
    lower = enclosure.lower()
    upper = enclosure.upper()
    elapsed = time.perf_counter() - started
    return EndpointTailCertificate(
        N, alpha, start, cutoff, prefix, radius, lower, upper, constant, elapsed
    )


def certify_energy_difference(N=4, start=1, cutoff=4096):
    """Independently enclose P_N-P_2N by constructing both energies."""
    if not isinstance(cutoff, int) or cutoff <= start:
        raise ValueError("cutoff must be an integer larger than start")
    started = time.perf_counter()
    old = restricted_channels(N)
    new = restricted_channels(2 * N)
    prefix = finite_energy_difference_prefix(N, start, cutoff)
    old_bound = ball(1) + sum((abs(value) for value in old), arb(0))
    new_bound = ball(1) + sum((abs(value) for value in new), arb(0))
    constant = old_bound * old_bound + new_bound * new_bound
    radius = constant / cutoff
    enclosure = prefix + arb(0, radius.upper())
    elapsed = time.perf_counter() - started
    return EndpointTailCertificate(
        N, endpoint_alpha(N), start, cutoff, prefix, radius,
        enclosure.lower(), enclosure.upper(), constant, elapsed,
    )


def compare_endpoint_to_energy_difference(N=4, start=1, cutoff=4096):
    """Compare alpha times the endpoint functional with direct P_N-P_2N."""
    endpoint = certify_endpoint_tail(start, cutoff, N)
    difference = certify_energy_difference(N, start, cutoff)
    endpoint_enclosure = endpoint.finite_prefix + arb(
        0, endpoint.remainder_radius.upper()
    )
    scaled = ball(endpoint.alpha) * endpoint_enclosure
    return EndpointComparison(endpoint, difference, scaled)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--N", type=int, nargs="+", default=[2, 4, 8, 16])
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--cutoff", type=int, default=4096)
    args = parser.parse_args()
    if args.bits < 80 or args.start < 1 or args.cutoff <= args.start:
        parser.error("need bits>=80 and 1<=start<cutoff")
    ctx.prec = args.bits
    print(f"precision={args.bits} bits; interval=[{args.start}, infinity)")
    failed = False
    for N in args.N:
        comparison = compare_endpoint_to_energy_difference(
            N, args.start, args.cutoff
        )
        endpoint = comparison.endpoint
        difference = comparison.direct_difference
        print(f"N={N}->2N={2 * N}; alpha={endpoint.alpha}")
        print(f"  endpoint=[{endpoint.lower_bound}, {endpoint.upper_bound}] ({endpoint.sign})")
        print(
            "  alpha*endpoint="
            f"[{comparison.scaled_endpoint.lower()}, "
            f"{comparison.scaled_endpoint.upper()}]"
        )
        print(f"  direct P_N-P_2N=[{difference.lower_bound}, {difference.upper_bound}] ({difference.sign})")
        print(f"  independent intervals overlap={comparison.agrees}")
        print(f"  runtime={endpoint.elapsed + difference.elapsed:.6f} seconds")
        failed |= not comparison.agrees
    if failed:
        raise SystemExit("an independent comparison failed")


if __name__ == "__main__":
    main()
