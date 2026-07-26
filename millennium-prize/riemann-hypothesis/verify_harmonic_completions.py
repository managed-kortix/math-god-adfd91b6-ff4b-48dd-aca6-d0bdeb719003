#!/usr/bin/env python3
"""Exact polynomial harmonic completions and numerical low-mode comparisons.

The exact part treats every logarithm as a formal variable and uses only
``Fraction`` coefficients.  The numerical Mellin/eigenmode comparison is a
separate diagnostic; none of its floating-point agreements is a certificate.
"""

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import math


class Polynomial:
    """Sparse rational polynomial in named, commuting formal variables."""

    def __init__(self, terms=None):
        self.terms = {
            tuple(sorted(monomial)): Fraction(coefficient)
            for monomial, coefficient in (terms or {}).items() if coefficient
        }

    @classmethod
    def constant(cls, value):
        return cls({(): Fraction(value)})

    @classmethod
    def variable(cls, name):
        return cls({(name,): Fraction(1)})

    def __add__(self, other):
        other = as_polynomial(other)
        terms = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            terms[monomial] = terms.get(monomial, Fraction(0)) + coefficient
            if not terms[monomial]:
                del terms[monomial]
        return Polynomial(terms)

    __radd__ = __add__

    def __neg__(self):
        return Polynomial({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-as_polynomial(other))

    def __rsub__(self, other):
        return as_polynomial(other) - self

    def __mul__(self, other):
        other = as_polynomial(other)
        terms = {}
        for left, a in self.terms.items():
            for right, b in other.terms.items():
                monomial = tuple(sorted(left + right))
                terms[monomial] = terms.get(monomial, Fraction(0)) + a * b
        return Polynomial(terms)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        if not isinstance(exponent, int) or exponent < 0:
            raise ValueError("polynomial exponent must be a nonnegative integer")
        result = Polynomial.constant(1)
        base = self
        while exponent:
            if exponent & 1:
                result = result * base
            base = base * base
            exponent //= 2
        return result

    def __eq__(self, other):
        return self.terms == as_polynomial(other).terms

    def __bool__(self):
        return bool(self.terms)


def as_polynomial(value):
    return value if isinstance(value, Polynomial) else Polynomial.constant(value)


@lru_cache(maxsize=None)
def _factorization_items(n):
    factors = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return tuple(factors.items())


def mobius(n):
    factors = _factorization_items(n)
    return 0 if any(e > 1 for _, e in factors) else (-1) ** len(factors)


@lru_cache(maxsize=None)
def divisors(n):
    values = [1]
    for prime, exponent in _factorization_items(n):
        values = [d * prime ** e for d in values for e in range(exponent + 1)]
    return tuple(sorted(values))


@lru_cache(maxsize=None)
def formal_log(n):
    """Return log(n) in the independent basis log(p), one variable per prime."""
    result = Polynomial.constant(0)
    for prime, exponent in _factorization_items(n):
        result += exponent * Polynomial.variable(f"log({prime})")
    return result


@lru_cache(maxsize=None)
def generalized_von_mangoldt(n, order):
    """Exact symbolic Lambda_order = mu * log^order (Lambda_0=epsilon)."""
    if order < 0:
        raise ValueError("order must be nonnegative")
    return sum(
        (mobius(d) * formal_log(n // d) ** order for d in divisors(n)),
        Polynomial.constant(0),
    )


def harmonic_completion(degree, n, log_scale=None):
    """Completed divisor harmonic for mu(d) (log(d)-L)^degree.

    This is the exact identity

      sum_{d|n} mu(d)(log(d)-L)^r
       = sum_{j=0}^r (-1)^j C(r,j)(log(n)-L)^(r-j) Lambda_j(n).
    """
    if degree not in range(4):
        raise ValueError("degree must be in 0..3")
    L = log_scale or Polynomial.variable("L")
    x = formal_log(n) - L
    return sum((
        (-1) ** order * math.comb(degree, order)
        * x ** (degree - order) * generalized_von_mangoldt(n, order)
        for order in range(degree + 1)
    ), Polynomial.constant(0))


def direct_harmonic_completion(degree, n, log_scale=None):
    if degree not in range(4):
        raise ValueError("degree must be in 0..3")
    L = log_scale or Polynomial.variable("L")
    return sum((
        mobius(d) * (formal_log(d) - L) ** degree for d in divisors(n)
    ), Polynomial.constant(0))


def convolution_residual(degree, n, cutoff, log_scale=None):
    """Exact tail after removing divisors d<=cutoff from the completion."""
    if cutoff < 0:
        raise ValueError("cutoff must be nonnegative")
    L = log_scale or Polynomial.variable("L")
    prefix = sum((
        mobius(d) * (formal_log(d) - L) ** degree
        for d in divisors(n) if d <= cutoff
    ), Polynomial.constant(0))
    return harmonic_completion(degree, n, L) - prefix


def direct_convolution_residual(degree, n, cutoff, log_scale=None):
    L = log_scale or Polynomial.variable("L")
    return sum((
        mobius(d) * (formal_log(d) - L) ** degree
        for d in divisors(n) if d > cutoff
    ), Polynomial.constant(0))


def cumulative_convolution_residual(degree, horizon, cutoff, log_scale=None):
    """Completed cumulative tail, retaining the exact floor multiplicities."""
    if horizon < 1 or cutoff < 0:
        raise ValueError("horizon must be positive and cutoff nonnegative")
    L = log_scale or Polynomial.variable("L")
    completed = sum((
        harmonic_completion(degree, n, L) for n in range(1, horizon + 1)
    ), Polynomial.constant(0))
    prefix = sum((
        (horizon // d) * mobius(d) * (formal_log(d) - L) ** degree
        for d in range(1, min(cutoff, horizon) + 1)
    ), Polynomial.constant(0))
    return completed - prefix


def direct_cumulative_convolution_residual(degree, horizon, cutoff, log_scale=None):
    L = log_scale or Polynomial.variable("L")
    return sum((
        (horizon // d) * mobius(d) * (formal_log(d) - L) ** degree
        for d in range(cutoff + 1, horizon + 1)
    ), Polynomial.constant(0))


@dataclass(frozen=True)
class ExactVerification:
    through: int
    cutoffs: tuple
    completion_checks: int
    residual_checks: int
    cumulative_checks: int


def verify_exact_identities(through=64, cutoffs=(0, 1, 4, 16)):
    """Verify all degree 0..3 identities by formal polynomial equality."""
    if not isinstance(through, int) or through < 1:
        raise ValueError("through must be a positive integer")
    completion_checks = residual_checks = cumulative_checks = 0
    for n in range(1, through + 1):
        for degree in range(4):
            if direct_harmonic_completion(degree, n) != harmonic_completion(degree, n):
                raise AssertionError(f"completion failed for degree={degree}, n={n}")
            completion_checks += 1
            for cutoff in cutoffs:
                if direct_convolution_residual(degree, n, cutoff) != convolution_residual(
                    degree, n, cutoff
                ):
                    raise AssertionError(
                        f"residual failed for degree={degree}, n={n}, cutoff={cutoff}"
                    )
                residual_checks += 1
        for cutoff in cutoffs:
            for degree in range(4):
                if cumulative_convolution_residual(degree, n, cutoff) != (
                    direct_cumulative_convolution_residual(degree, n, cutoff)
                ):
                    raise AssertionError(
                        f"cumulative residual failed for degree={degree}, "
                        f"horizon={n}, cutoff={cutoff}"
                    )
                cumulative_checks += 1
    return ExactVerification(
        through, tuple(cutoffs), completion_checks, residual_checks,
        cumulative_checks,
    )


@dataclass(frozen=True)
class LowModeComparison:
    mode: int
    beta: float
    eigenvalue: float
    modal_projection: float
    mellin_projection: float
    completed_polynomial_projections: tuple
    completion_roundoff: tuple
    mellin_minus_modal: float


def _truncated_profile_coefficients(beta, degree):
    """Taylor coefficients of t times the continuum mode at log(x)=0."""
    # t exp(-t/2) [cos(beta t) + sin(beta t)/(2 beta)]
    if degree == 0:
        return (0.0,)
    exponential = [(-0.5) ** j / math.factorial(j) for j in range(degree + 1)]
    oscillatory = []
    for j in range(degree + 1):
        cosine = (beta ** j * math.cos(j * math.pi / 2)) / math.factorial(j)
        sine = 0.0 if j == 0 else (
            beta ** (j - 1) * math.sin(j * math.pi / 2) / (2 * math.factorial(j))
        )
        oscillatory.append(cosine + sine)
    profile = tuple(sum(
        exponential[k] * oscillatory[j - k] for k in range(j + 1)
    ) for j in range(degree))
    return (0.0,) + profile


def completed_polynomial_moments(N, max_degree=3):
    """Numerically evaluate exact completed dyadic moments of degrees 0..3.

    The two returned tuples are the convolution-completed evaluation and its
    difference from the direct dyadic sum.  The latter measures only floating-
    point roundoff; formal equality is certified by ``verify_exact_identities``.
    """
    if not isinstance(N, int) or N < 1:
        raise ValueError("N must be a positive integer")
    if max_degree not in range(4):
        raise ValueError("max_degree must be in 0..3")
    mu = [mobius(n) for n in range(2 * N + 1)]
    L = math.log(N)
    completed_values = []
    discrepancies = []
    for degree in range(max_degree + 1):
        completed = 0.0
        for n in range(1, 2 * N + 1):
            x = math.log(n) - L
            completed += sum(
                (-1) ** order * math.comb(degree, order)
                * x ** (degree - order)
                * sum(
                    mu[d] * math.log(n // d) ** order for d in divisors(n)
                )
                for order in range(degree + 1)
            )
        prefix = sum(
            (2 * N // d) * mu[d] * (math.log(d) - L) ** degree
            for d in range(1, N + 1)
        )
        value = completed - prefix
        direct = sum(
            mu[d] * (math.log(d) - L) ** degree for d in range(N + 1, 2 * N + 1)
        )
        completed_values.append(value)
        discrepancies.append(value - direct)
        if not math.isfinite(value):
            raise ArithmeticError("non-finite completed moment")
    return tuple(completed_values), tuple(discrepancies)


def compare_low_modes(N, modes=3):
    """Numerically compare continuum Mellin samples and discrete K eigenmodes.

    The degree-d entries use the Taylor polynomial through d.  They diagnose how
    the exact degree-0..3 completion basis approximates the transcendental
    Mellin profile; they are not exact identities.
    """
    import numpy as np
    from scipy.linalg import eigh_tridiagonal
    from scipy.optimize import brentq

    if not isinstance(N, int) or N < 2:
        raise ValueError("N must be an integer at least 2")
    if not isinstance(modes, int) or modes < 1 or modes > N:
        raise ValueError("modes must be in 1..N")
    inverse_weights = np.arange(N + 1, 2 * N + 1, dtype=float)
    inverse_weights *= inverse_weights + 1
    diagonal = np.empty(N)
    diagonal[0] = inverse_weights[0]
    diagonal[1:] = inverse_weights[:-1] + inverse_weights[1:]
    off = -inverse_weights[:-1]
    inverse_eigenvalues, vectors = eigh_tridiagonal(
        np.asarray(diagonal, dtype=float), np.asarray(off, dtype=float),
        select="i", select_range=(0, modes - 1), check_finite=False,
    )
    indices = np.arange(N + 1, 2 * N + 1, dtype=float)
    t = np.log(indices / N)
    mu = np.asarray([mobius(n) for n in range(N + 1, 2 * N + 1)], dtype=float)
    source = mu * t
    moments, roundoff = completed_polynomial_moments(N)
    comparisons = []
    for j in range(1, modes + 1):
        left = (j - 0.5) * math.pi / math.log(2) + 1e-10
        right = j * math.pi / math.log(2) - 1e-10
        beta = brentq(lambda b: math.tan(b * math.log(2)) + 2 * b, left, right)
        profile = np.exp(-t / 2) * (np.cos(beta * t) + np.sin(beta * t) / (2 * beta))
        profile_norm = np.linalg.norm(profile)
        profile /= profile_norm
        vector = vectors[:, j - 1]
        if np.dot(vector, profile) < 0:
            vector = -vector
        modal = float(np.dot(source, vector))
        mellin = float(np.dot(source, profile))
        polynomial = []
        for degree in range(4):
            coefficients = _truncated_profile_coefficients(beta, degree)
            polynomial.append(float(sum(
                coefficients[k] * moments[k] for k in range(degree + 1)
            ) / profile_norm))
        comparisons.append(LowModeComparison(
            j, beta, float(1 / inverse_eigenvalues[j - 1]), modal, mellin,
            tuple(polynomial), roundoff, mellin - modal,
        ))
    return tuple(comparisons)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--through", type=int, default=64)
    parser.add_argument("--N", type=int, default=128)
    parser.add_argument("--modes", type=int, default=3)
    args = parser.parse_args()
    exact = verify_exact_identities(args.through)
    print("EXACT formal-polynomial certificates")
    print(f"  degrees=0..3 n<= {exact.through}: completions={exact.completion_checks} "
          f"residuals={exact.residual_checks} cumulative={exact.cumulative_checks} all exact")
    print("APPROXIMATE floating-point Mellin/modal diagnostic")
    for item in compare_low_modes(args.N, args.modes):
        approximations = " ".join(
            f"d{degree}={value:+.7g}"
            for degree, value in enumerate(item.completed_polynomial_projections)
        )
        print(f"  j={item.mode} beta={item.beta:.8g} modal={item.modal_projection:+.7g} "
              f"Mellin={item.mellin_projection:+.7g} delta={item.mellin_minus_modal:+.3g}")
        print(f"    polynomial approximations: {approximations}")


if __name__ == "__main__":
    main()
