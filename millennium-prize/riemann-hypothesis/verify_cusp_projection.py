#!/usr/bin/env python3
"""Certified one-sided cusp/projection bound for a finite RH kernel form.

For f_w(t)=sin(w t)/t and a uniform partition of [0,Q], this module uses
Arb-evaluated exact cell means

    h^(-1) (Si(w b)-Si(w a))

to form the orthogonal piecewise-constant projection G0 of the Gram matrix
G_Q.  The Brownian cusp is evaluated by exact rational suffix sums.  The
remaining adverse term is bounded by the cellwise Neumann Poincare inequality.
This is a finite prototype; it does not certify a frequency or harmonic tail.
"""

import argparse
import time
from dataclasses import dataclass
from fractions import Fraction

from flint import arb, ctx

from verify_separated_kernel import ball


@dataclass(frozen=True)
class ProjectionCertificate:
    cusp_form: object
    projected_form: object
    derivative_energy_bound: object
    poincare_remainder: object
    expression: object
    upper_bound: object
    cells: int


def _validate(frequencies, u, d, alpha, Q, cells):
    if not frequencies or len(frequencies) != len(u) or len(u) != len(d):
        raise ValueError("frequency and channel lengths must agree and be nonempty")
    if list(frequencies) != sorted(frequencies) or len(set(frequencies)) != len(frequencies):
        raise ValueError("frequencies must be strictly increasing")
    if any(not isinstance(w, Fraction) or w <= 0 for w in frequencies):
        raise ValueError("frequencies must be positive Fractions")
    if any(not isinstance(x, Fraction) for x in tuple(u) + tuple(d)):
        raise ValueError("channels must be Fractions")
    if not isinstance(alpha, Fraction) or alpha <= 0:
        raise ValueError("alpha must be a positive Fraction")
    if not isinstance(Q, Fraction) or Q <= 0 or not isinstance(cells, int) or cells < 1:
        raise ValueError("Q must be a positive Fraction and cells must be positive")


def cusp_bilinear(frequencies, x, y):
    """Return x^T min(w_i,w_j) y using O(N) exact suffix sums."""
    sx = sum(x, Fraction(0))
    sy = sum(y, Fraction(0))
    previous = Fraction(0)
    total = Fraction(0)
    for w, xi, yi in zip(frequencies, x, y):
        total += (w - previous) * sx * sy
        sx -= xi
        sy -= yi
        previous = w
    return total


def cusp_two_channel_form(frequencies, u, d, alpha):
    rational = (
        2 * cusp_bilinear(frequencies, u, d)
        - alpha * cusp_bilinear(frequencies, d, d)
    )
    return arb.pi() * ball(rational) / 2


def cell_means(Q, frequencies, cells):
    """Outward-rounded means of sin(w t)/t, including the cell at t=0."""
    h = Q / cells
    means = []
    for cell in range(cells):
        a, b = cell * h, (cell + 1) * h
        row = []
        for w in frequencies:
            # Si(0)=0 in Arb, so no removable-singularity evaluation occurs.
            integral = ball(w * b).si() - ball(w * a).si()
            row.append(integral / ball(h))
        means.append(tuple(row))
    return tuple(means)


def projected_two_channel_form(Q, means, u, d, alpha):
    h = ball(Q / len(means))
    total = arb(0)
    for row in means:
        um = sum((ball(x) * value for x, value in zip(u, row)), arb(0))
        dm = sum((ball(x) * value for x, value in zip(d, row)), arb(0))
        total += h * (2 * um * dm - ball(alpha) * dm * dm)
    return total


def poincare_derivative_bound(Q, frequencies, z, cells):
    """Bound ||(sum z_i f_i)'||_2^2 and its projection error.

    The origin-safe identity

        x cos(x)-sin(x) = -integral_0^x s sin(s) ds

    gives |f_w'(t)| <= w^2/2 for every t>=0, including the limiting value at
    zero.  On each cell, the sharp mean-zero Neumann Poincare constant is
    h^2/pi^2.  No floating-point sampling near zero enters the certificate.
    """
    suffix = sum(z, Fraction(0))
    previous = Fraction(0)
    derivative_linf = Fraction(0)
    for w, zi in zip(frequencies, z):
        derivative_linf += abs(suffix) * (w * w - previous * previous) / 2
        suffix -= zi
        previous = w
    derivative_energy = ball(Q * derivative_linf * derivative_linf)
    h = ball(Q / cells)
    remainder = h * h / (arb.pi() * arb.pi()) * derivative_energy
    return derivative_energy, remainder


def certify_one_sided(Q, frequencies, u, d, alpha, cells):
    """Certify an upper bound for 2 u^T K_Q d-alpha d^T K_Q d."""
    _validate(frequencies, u, d, alpha, Q, cells)
    z = tuple(di - ui / alpha for ui, di in zip(u, d))
    means = cell_means(Q, frequencies, cells)
    cusp = cusp_two_channel_form(frequencies, u, d, alpha)
    projected = projected_two_channel_form(Q, means, u, d, alpha)
    derivative_energy, residual = poincare_derivative_bound(
        Q, frequencies, z, cells
    )
    expression = cusp - projected + ball(alpha) * residual
    # The upper endpoint is itself an Arb point/one-sided outward bound.
    return ProjectionCertificate(
        cusp, projected, derivative_energy, residual, expression,
        expression.upper(), cells
    )


def dense_kernel_form(Q, frequencies, u, d, alpha):
    """Independent dense Arb Si/Ci evaluation of the two-channel K_Q form."""
    q = ball(Q)

    def endpoint_cosine_tail(delta):
        if delta == 0:
            return 1 / q
        db = ball(abs(delta))
        x = q * db
        return x.cos() / q - db * (arb.pi() / 2 - x.si())

    total = arb(0)
    for i, wi in enumerate(frequencies):
        for j, wj in enumerate(frequencies):
            weight = u[i] * d[j] + d[i] * u[j] - alpha * d[i] * d[j]
            kernel = (
                endpoint_cosine_tail(wi - wj)
                - endpoint_cosine_tail(wi + wj)
            ) / 2
            total += ball(weight) * kernel
    return total


def diagnostic_vectors(size):
    frequencies = tuple(Fraction(i + 1, size + 3) for i in range(size))
    u = tuple(Fraction((-1) ** i * (i % 5 + 1), i + 3) for i in range(size))
    d = tuple(Fraction((-1) ** (i // 2) * (i % 3 + 1), i + 4) for i in range(size))
    return frequencies, u, d


def run_diagnostics(Q, size, cell_counts, alpha):
    frequencies, u, d = diagnostic_vectors(size)
    _validate(frequencies, u, d, alpha, Q, cell_counts[0])
    dense = dense_kernel_form(Q, frequencies, u, d, alpha)
    print(f"rational two-channel realization: N={size}, Q={Q}, alpha={alpha}")
    print(f"dense K_Q form={dense}")
    print("cells  remainder_upper       upper_bound           certified_gap         seconds")
    previous = None
    for cells in cell_counts:
        started = time.perf_counter()
        certificate = certify_one_sided(Q, frequencies, u, d, alpha, cells)
        elapsed = time.perf_counter() - started
        if not dense.upper() <= certificate.upper_bound:
            raise AssertionError("one-sided bound does not enclose dense K_Q evaluation")
        remainder = certificate.poincare_remainder.upper()
        if previous is not None and not remainder < previous:
            raise AssertionError("Poincare remainder did not decrease under refinement")
        previous = remainder
        gap = certificate.upper_bound - dense.upper()
        print(f"{cells:5d}  {float(remainder): .10e}  "
              f"{float(certificate.upper_bound): .10e}  {float(gap): .10e}  {elapsed:.4f}")
    return dense


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--Q", type=Fraction, default=Fraction(8))
    parser.add_argument("--size", type=int, default=16)
    parser.add_argument("--cells", type=int, nargs="+", default=[8, 16, 32, 64])
    parser.add_argument("--alpha", type=Fraction, default=Fraction(3, 2))
    args = parser.parse_args()
    if (args.bits < 80 or args.size < 1 or args.Q <= 0 or args.alpha <= 0
            or any(c < 1 for c in args.cells)):
        parser.error(
            "need bits>=80, size>=1, Q>0, alpha>0, and positive cell counts"
        )
    ctx.prec = args.bits
    run_diagnostics(args.Q, args.size, args.cells, args.alpha)
    print("certified cusp/projection diagnostics passed")


if __name__ == "__main__":
    main()
