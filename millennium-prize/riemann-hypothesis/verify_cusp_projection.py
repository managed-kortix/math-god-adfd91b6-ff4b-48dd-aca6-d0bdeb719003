#!/usr/bin/env python3
"""Certified piecewise Legendre cusp/projection bounds for a finite RH form.

Degrees 0 through 3 are supported. Projection features are evaluated from
Arb Si/sine/cosine endpoint formulas, without evaluating sin(w*t)/t at zero.
The projection residual is bounded by an origin-safe derivative theorem.
This is a finite prototype; it does not certify a frequency or harmonic tail.
"""

import argparse
import math
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
    degree: int = 0

    @property
    def residual_bound(self):
        return self.poincare_remainder

    @property
    def total_rank(self):
        return self.cells * (self.degree + 1)


def _validate(frequencies, u, d, alpha, Q, cells, degree=0):
    if not frequencies or len(frequencies) != len(u) or len(u) != len(d):
        raise ValueError("frequency and channel lengths must agree and be nonempty")
    if any(not frequencies[i] < frequencies[i + 1]
           for i in range(len(frequencies) - 1)):
        raise ValueError("frequencies must be strictly increasing")
    if any(not isinstance(w, (Fraction, arb)) or not w > 0 for w in frequencies):
        raise ValueError("frequencies must be positive Fractions or Arb balls")
    if any(not isinstance(x, (Fraction, arb)) for x in tuple(u) + tuple(d)):
        raise ValueError("channels must be Fractions or Arb balls")
    if not isinstance(alpha, Fraction) or alpha <= 0:
        raise ValueError("alpha must be a positive Fraction")
    if not isinstance(Q, Fraction) or Q <= 0 or not isinstance(cells, int) or cells < 1:
        raise ValueError("Q must be a positive Fraction and cells must be positive")
    if not isinstance(degree, int) or not 0 <= degree <= 3:
        raise ValueError("degree must be one of 0, 1, 2, 3")


def cusp_bilinear(frequencies, x, y):
    """Return x^T min(w_i,w_j) y using O(N) exact suffix sums."""
    exact = all(isinstance(value, Fraction)
                for value in tuple(frequencies) + tuple(x) + tuple(y))
    zero = Fraction(0) if exact else arb(0)
    sx = sum(x, zero)
    sy = sum(y, zero)
    previous = zero
    total = zero
    for w, xi, yi in zip(frequencies, x, y):
        total += (w - previous) * sx * sy
        sx -= xi
        sy -= yi
        previous = w
    return total


def cusp_two_channel_form(frequencies, u, d, alpha):
    scale = alpha if all(isinstance(x, Fraction) for x in tuple(u) + tuple(d)) else ball(alpha)
    rational = 2 * cusp_bilinear(frequencies, u, d) - scale * cusp_bilinear(
        frequencies, d, d
    )
    return arb.pi() * ball(rational) / 2


def _sinc_monomial_moments(a, b, w, degree):
    """Return integrals of t^k sin(w t)/t for k=0,...,degree.

    The k=0 endpoint uses Si. Higher moments use integration-by-parts
    endpoint recurrences. In particular, the cell containing zero never uses
    division by t or a removable-singularity evaluation.
    """
    ab, bb, wb = ball(a), ball(b), ball(w)
    wa = ball(w * a) if isinstance(w, Fraction) else wb * ab
    wb_endpoint = ball(w * b) if isinstance(w, Fraction) else wb * bb
    moments = [wb_endpoint.si() - wa.si()]
    if degree == 0:
        return tuple(moments)

    sin_a, sin_b = (wb * ab).sin(), (wb * bb).sin()
    cos_a, cos_b = (wb * ab).cos(), (wb * bb).cos()
    sine_integrals = [(cos_a - cos_b) / wb]
    cosine_integrals = [(sin_b - sin_a) / wb]
    moments.append(sine_integrals[0])
    for power in range(1, degree):
        sine_integrals.append(
            (ab**power * cos_a - bb**power * cos_b) / wb
            + ball(power) * cosine_integrals[power - 1] / wb
        )
        cosine_integrals.append(
            (bb**power * sin_b - ab**power * sin_a) / wb
            - ball(power) * sine_integrals[power - 1] / wb
        )
        moments.append(sine_integrals[power])
    return tuple(moments)


def _poly_multiply(left, right):
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i + j] += x * y
    return result


def shifted_legendre_coefficients(a, h, degree):
    """Exact monomial coefficients of P_degree(2(t-a)/h-1)."""
    x = [-(2 * a / h + 1), 2 / h]
    powers = [[Fraction(1)]]
    for _ in range(3):
        powers.append(_poly_multiply(powers[-1], x))
    if degree == 0:
        return (Fraction(1),)
    if degree == 1:
        return tuple(x)
    if degree == 2:
        result = [value * Fraction(3, 2) for value in powers[2]]
        result[0] -= Fraction(1, 2)
        return tuple(result)
    result = [value * Fraction(5, 2) for value in powers[3]]
    for k, value in enumerate(x):
        result[k] -= Fraction(3, 2) * value
    return tuple(result)


def legendre_feature_moments(Q, frequencies, cells, degree):
    """Arb integrals of f_w against shifted P_0,...,P_degree per cell."""
    if not isinstance(Q, Fraction) or Q <= 0 or cells < 1:
        raise ValueError("Q must be a positive Fraction and cells must be positive")
    if degree not in range(4):
        raise ValueError("degree must be one of 0, 1, 2, 3")
    h = Q / cells
    result = []
    for cell in range(cells):
        a, b = cell * h, (cell + 1) * h
        coefficients = [shifted_legendre_coefficients(a, h, n) for n in range(degree + 1)]
        row = []
        for w in frequencies:
            monomials = _sinc_monomial_moments(a, b, w, degree)
            row.append(tuple(
                sum((ball(c) * monomials[k] for k, c in enumerate(poly)), arb(0))
                for poly in coefficients
            ))
        result.append(tuple(row))
    return tuple(result)


def cell_means(Q, frequencies, cells):
    """Backward-compatible outward-rounded piecewise-constant means."""
    h_rational = Q / cells
    h = ball(h_rational)
    means = []
    for cell in range(cells):
        a, b = cell * h_rational, (cell + 1) * h_rational
        means.append(tuple(
            ((ball(w * b).si() - ball(w * a).si()) / h
             if isinstance(w, Fraction)
             else ((ball(w) * ball(b)).si() - (ball(w) * ball(a)).si()) / h)
            for w in frequencies
        ))
    return tuple(means)


def projected_legendre_two_channel_form(Q, features, u, d, alpha, degree):
    """Evaluate the two-channel form of the orthogonal projected Gramian."""
    h = ball(Q / len(features))
    total = arb(0)
    for row in features:
        for n in range(degree + 1):
            um = sum((ball(x) * item[n] for x, item in zip(u, row)), arb(0))
            dm = sum((ball(x) * item[n] for x, item in zip(d, row)), arb(0))
            total += ball(2 * n + 1) / h * (2 * um * dm - ball(alpha) * dm * dm)
    return total


def projected_two_channel_form(Q, means, u, d, alpha):
    """Backward-compatible form evaluation from piecewise-constant means."""
    h = ball(Q / len(means))
    total = arb(0)
    for row in means:
        um = sum((ball(x) * value for x, value in zip(u, row)), arb(0))
        dm = sum((ball(x) * value for x, value in zip(d, row)), arb(0))
        total += h * (2 * um * dm - ball(alpha) * dm * dm)
    return total


def derivative_linf_bound(frequencies, z, order):
    """Exact rational bound for ||(sum z_i f_i)^(order)||_infinity."""
    exact = all(isinstance(value, Fraction) for value in tuple(frequencies) + tuple(z))
    zero = Fraction(0) if exact else arb(0)
    suffix = sum(z, zero)
    previous = zero
    bound = zero
    for w, zi in zip(frequencies, z):
        bound += abs(suffix) * (w ** (order + 1) - previous ** (order + 1)) / (order + 1)
        suffix -= zi
        previous = w
    return bound


def legendre_residual_bound(Q, frequencies, z, cells, degree):
    """Certify ||(I-P_degree) sum z_i f_i||_2^2.

    For r=degree+1, projection is no worse than the degree-r-1 Taylor
    polynomial about each cell midpoint. Taylor's theorem and the integral
    representation f_w(t)=int_0^w cos(s*t) ds give

      error^2 <= Q h^(2r) B_r^2 / ((r!)^2 2^(2r) (2r+1)),
      B_r = int_0^wmax s^r |sum_{w_i>=s} z_i| ds.

    B_r is an exact rational suffix sum and the representation is valid at
    t=0, so this theorem is origin-safe.
    """
    order = degree + 1
    derivative_linf = derivative_linf_bound(frequencies, z, order)
    derivative_energy = ball(Q) * ball(derivative_linf) * ball(derivative_linf)
    h = ball(Q / cells)
    denominator = math.factorial(order) ** 2 * 2 ** (2 * order) * (2 * order + 1)
    residual = h ** (2 * order) * derivative_energy / denominator
    return derivative_energy, residual


def poincare_derivative_bound(Q, frequencies, z, cells):
    """Original degree-zero Neumann Poincare residual certificate."""
    derivative_linf = derivative_linf_bound(frequencies, z, 1)
    derivative_energy = ball(Q) * ball(derivative_linf) * ball(derivative_linf)
    h = ball(Q / cells)
    return derivative_energy, h * h / (arb.pi() * arb.pi()) * derivative_energy


def certify_one_sided(Q, frequencies, u, d, alpha, cells, degree=0):
    """Certify an upper bound for 2 u^T K_Q d-alpha d^T K_Q d."""
    _validate(frequencies, u, d, alpha, Q, cells, degree)
    scale = alpha if all(isinstance(x, Fraction) for x in tuple(u) + tuple(d)) else ball(alpha)
    z = tuple(di - ui / scale for ui, di in zip(u, d))
    features = legendre_feature_moments(Q, frequencies, cells, degree)
    cusp = cusp_two_channel_form(frequencies, u, d, alpha)
    projected = projected_legendre_two_channel_form(Q, features, u, d, alpha, degree)
    derivative_energy, residual = legendre_residual_bound(
        Q, frequencies, z, cells, degree
    )
    if degree == 0:
        derivative_energy, residual = poincare_derivative_bound(
            Q, frequencies, z, cells
        )
    expression = cusp - projected + ball(alpha) * residual
    return ProjectionCertificate(
        cusp, projected, derivative_energy, residual, expression,
        expression.upper(), cells, degree
    )


def dense_kernel_form(Q, frequencies, u, d, alpha):
    """Independent dense Arb Si evaluation of the two-channel K_Q form."""
    q = ball(Q)

    def endpoint_cosine_tail(delta, diagonal=False):
        if diagonal:
            return 1 / q
        db = ball(abs(delta))
        x = q * db
        return x.cos() / q - db * (arb.pi() / 2 - x.si())

    total = arb(0)
    scale = alpha if all(isinstance(x, Fraction) for x in tuple(u) + tuple(d)) else ball(alpha)
    for i, wi in enumerate(frequencies):
        for j, wj in enumerate(frequencies):
            weight = u[i] * d[j] + d[i] * u[j] - scale * d[i] * d[j]
            kernel = (endpoint_cosine_tail(wi - wj, i == j) - endpoint_cosine_tail(wi + wj)) / 2
            total += ball(weight) * kernel
    return total


def diagnostic_vectors(size):
    frequencies = tuple(Fraction(i + 1, size + 3) for i in range(size))
    u = tuple(Fraction((-1) ** i * (i % 5 + 1), i + 3) for i in range(size))
    d = tuple(Fraction((-1) ** (i // 2) * (i % 3 + 1), i + 4) for i in range(size))
    return frequencies, u, d


def compare_equal_rank(Q, frequencies, u, d, alpha, total_rank, degrees=range(4)):
    """Return dense value and certificates having the same total local rank."""
    certificates = []
    for degree in degrees:
        width = degree + 1
        if total_rank % width:
            raise ValueError("total rank must be divisible by every degree+1")
        certificates.append(
            certify_one_sided(Q, frequencies, u, d, alpha, total_rank // width, degree)
        )
    dense = dense_kernel_form(Q, frequencies, u, d, alpha)
    for certificate in certificates:
        if not dense.upper() <= certificate.upper_bound:
            raise AssertionError("one-sided bound does not enclose dense K_Q evaluation")
    return dense, tuple(certificates)


def run_diagnostics(Q, size, total_ranks, alpha):
    frequencies, u, d = diagnostic_vectors(size)
    dense = dense_kernel_form(Q, frequencies, u, d, alpha)
    print(f"rational two-channel realization: N={size}, Q={Q}, alpha={alpha}")
    print(f"dense K_Q form={dense}")
    print("rank deg cells residual_upper       upper_bound          gap_to_dense        seconds")
    for rank in total_ranks:
        compared_dense, certificates = compare_equal_rank(
            Q, frequencies, u, d, alpha, rank
        )
        for certificate in certificates:
            started = time.perf_counter()
            # Time a fresh certificate rather than reporting comparison overhead.
            certificate = certify_one_sided(
                Q, frequencies, u, d, alpha, certificate.cells, certificate.degree
            )
            elapsed = time.perf_counter() - started
            gap = certificate.upper_bound - compared_dense.upper()
            print(f"{rank:4d} {certificate.degree:3d} {certificate.cells:5d} "
                  f"{float(certificate.residual_bound.upper()): .10e}  "
                  f"{float(certificate.upper_bound): .10e}  {float(gap): .10e}  {elapsed:.4f}")
    return dense


def run_mobius_endpoint(Q, total_ranks):
    """Report the harmonic-first N=4 -> 8, R=3 endpoint realization."""
    from mobius_endpoint_surrogate import generate_exact_4_to_8_surrogate

    surrogate = generate_exact_4_to_8_surrogate()
    dense = dense_kernel_form(
        Q, surrogate.frequencies, surrogate.u, surrogate.d, surrogate.alpha
    )
    print(
        "Mobius endpoint surrogate: N=4->8, R=3, alpha=1/3, "
        f"raw={len(surrogate.raw_modes)}, reduced={len(surrogate.frequencies)}"
    )
    print("angular frequencies omega=2*pi*p/q after harmonic-first aggregation")
    print(f"dense oscillatory K_Q form={dense}")
    print("rank deg cells cusp_form            projected_form       residual_upper       upper_bound          gap")
    for rank in total_ranks:
        _, certificates = compare_equal_rank(
            Q, surrogate.frequencies, surrogate.u, surrogate.d,
            surrogate.alpha, rank
        )
        for certificate in certificates:
            gap = certificate.upper_bound - dense.upper()
            print(
                f"{rank:4d} {certificate.degree:3d} {certificate.cells:5d} "
                f"{float(certificate.cusp_form): .10e}  "
                f"{float(certificate.projected_form): .10e}  "
                f"{float(certificate.residual_bound.upper()): .10e}  "
                f"{float(certificate.upper_bound): .10e}  {float(gap): .10e}"
            )
    return surrogate, dense


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--Q", type=Fraction, default=Fraction(8))
    parser.add_argument("--size", type=int, default=16)
    parser.add_argument("--ranks", type=int, nargs="+", default=[24, 48, 96, 192])
    parser.add_argument("--alpha", type=Fraction, default=Fraction(3, 2))
    parser.add_argument("--mobius-endpoint", action="store_true")
    args = parser.parse_args()
    if (args.bits < 80 or args.size < 1 or args.Q <= 0 or args.alpha <= 0
            or any(rank < 1 or rank % 12 for rank in args.ranks)):
        parser.error("need bits>=80, size>=1, Q>0, alpha>0, and ranks divisible by 12")
    ctx.prec = args.bits
    if args.mobius_endpoint:
        run_mobius_endpoint(args.Q, args.ranks)
    else:
        run_diagnostics(args.Q, args.size, args.ranks, args.alpha)
    print("certified piecewise Legendre diagnostics passed")


if __name__ == "__main__":
    main()
