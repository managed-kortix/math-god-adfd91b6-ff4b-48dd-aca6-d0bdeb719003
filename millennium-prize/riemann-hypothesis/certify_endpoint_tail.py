#!/usr/bin/env python3
"""Arb certificate for the untruncated N=4 -> 8 endpoint tail.

The calculation stays in the sawtooth representation.  On every open unit
interval all {t/a}, a <= 8, are affine, so the endpoint integrand is a
quadratic divided by t^2 and has an elementary exact antiderivative.  No
Fourier expansion or common period is used.
"""

import argparse
import time
from dataclasses import dataclass
from fractions import Fraction

from flint import arb, ctx

from mobius_endpoint_surrogate import endpoint_channels
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


def elementary_remainder_constant(u, d, alpha=Fraction(1, 3)):
    """Return C with |2*f*d-alpha*d^2| <= C pointwise."""
    _validate_source_channels(u, d)
    f_bound = ball(1) + sum((abs(ball(value)) for value in u), arb(0))
    d_bound = sum((abs(ball(value)) for value in d), arb(0))
    return 2 * f_bound * d_bound + ball(alpha) * d_bound * d_bound


def certify_endpoint_tail(start=8, cutoff=1024):
    """Enclose the complete untruncated endpoint tail on [start,infinity)."""
    if not isinstance(cutoff, int) or cutoff <= start:
        raise ValueError("cutoff must be an integer larger than start")
    started = time.perf_counter()
    u, d = endpoint_channels(4)
    prefix = finite_endpoint_prefix(start, cutoff, u, d)
    constant = elementary_remainder_constant(u, d)
    radius = constant / cutoff
    enclosure = prefix + arb(0, radius.upper())
    lower = enclosure.lower()
    upper = enclosure.upper()
    elapsed = time.perf_counter() - started
    return EndpointTailCertificate(
        start, cutoff, prefix, radius, lower, upper, constant, elapsed
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--start", type=int, default=8)
    parser.add_argument("--cutoff", type=int, default=1024)
    args = parser.parse_args()
    if args.bits < 80 or args.start < 1 or args.cutoff <= args.start:
        parser.error("need bits>=80 and 1<=start<cutoff")
    ctx.prec = args.bits
    certificate = certify_endpoint_tail(args.start, args.cutoff)
    print("direct unit-breakpoint N=4->8 endpoint-tail certificate")
    print(f"precision={args.bits} bits; interval=[{args.start}, infinity)")
    print(f"finite prefix [{args.start},{args.cutoff}]={certificate.finite_prefix}")
    print(f"elementary remainder radius={certificate.remainder_radius}")
    print(f"certified interval=[{certificate.lower_bound}, {certificate.upper_bound}]")
    print(f"strictly positive={certificate.is_positive}")
    print(f"runtime={certificate.elapsed:.6f} seconds")
    if not certificate.is_positive:
        raise SystemExit("positivity was not certified")


if __name__ == "__main__":
    main()
