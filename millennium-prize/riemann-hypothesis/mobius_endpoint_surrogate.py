#!/usr/bin/env python3
"""Finite harmonic-first Mobius endpoint surrogate with Arb coefficients."""

from dataclasses import dataclass
from fractions import Fraction
from flint import arb

from verify_separated_kernel import ball


@dataclass(frozen=True)
class HarmonicMode:
    source: int
    harmonic: int
    reduced_frequency: Fraction
    u: object
    d: object


@dataclass(frozen=True)
class MobiusEndpointSurrogate:
    N: int
    endpoint: int
    harmonics: int
    alpha: Fraction
    reduced_frequencies: tuple
    frequencies: tuple
    u: tuple
    d: tuple
    raw_modes: tuple


def mobius(n):
    """Return the integer Mobius function."""
    value = 1
    prime = 2
    while prime * prime <= n:
        if n % prime == 0:
            n //= prime
            value = -value
            if n % prime == 0:
                return 0
            while n % prime == 0:
                n //= prime
        prime += 1
    return -value if n > 1 else value


def _log_ratio(top, bottom):
    return ball(Fraction(top, bottom)).log()


def endpoint_channels(N):
    """Return sawtooth coefficients of F_N and F_N-H_N as Arb balls."""
    if not isinstance(N, int) or N < 2:
        raise ValueError("N must be an integer at least 2")
    endpoint = 2 * N
    log_N = ball(N).log()
    log_two = ball(2).log()
    u = []
    d = []
    for a in range(1, endpoint + 1):
        mu = mobius(a)
        f = arb(0)
        h = arb(0)
        if mu and a <= N:
            if a == 1:
                f = ball(mu)
            elif a < N:
                f = mu * _log_ratio(N, a) / log_N
            h = ball(mu)
        elif mu and a < endpoint:
            h = mu * _log_ratio(endpoint, a) / log_two
        u.append(f)
        d.append(f - h)
    return tuple(u), tuple(d)


def harmonic_modes(N=4, harmonics=3):
    """Expand first, retaining harmonics 1..R before reducing frequencies."""
    if not isinstance(harmonics, int) or harmonics < 1:
        raise ValueError("harmonics must be a positive integer")
    u_source, d_source = endpoint_channels(N)
    modes = []
    for a, (ua, da) in enumerate(zip(u_source, d_source), 1):
        if ua.is_zero() and da.is_zero():
            continue
        for r in range(1, harmonics + 1):
            common = -1 / (arb.pi() * r)
            modes.append(HarmonicMode(a, r, Fraction(r, a), common * ua, common * da))
    return tuple(modes)


def aggregate_modes(modes):
    """Aggregate exact duplicate reduced rationals after harmonic truncation."""
    grouped = {}
    for mode in modes:
        if mode.reduced_frequency not in grouped:
            grouped[mode.reduced_frequency] = [arb(0), arb(0)]
        grouped[mode.reduced_frequency][0] += mode.u
        grouped[mode.reduced_frequency][1] += mode.d
    return tuple(
        (frequency, values[0], values[1])
        for frequency, values in sorted(grouped.items())
        if not (values[0].is_zero() and values[1].is_zero())
    )


def generate_mobius_endpoint_surrogate(N=4, harmonics=3):
    """Build the N -> 2N endpoint surrogate; N=4 gives alpha=1/3."""
    raw = harmonic_modes(N, harmonics)
    aggregated = aggregate_modes(raw)
    reduced = tuple(item[0] for item in aggregated)
    angular = tuple(2 * arb.pi() * ball(value) for value in reduced)
    return MobiusEndpointSurrogate(
        N=N,
        endpoint=2 * N,
        harmonics=harmonics,
        alpha=endpoint_alpha(N),
        reduced_frequencies=reduced,
        frequencies=angular,
        u=tuple(item[1] for item in aggregated),
        d=tuple(item[2] for item in aggregated),
        raw_modes=raw,
    )


def endpoint_alpha(N):
    """Return log(2)/log(2N); it is rational only for N a power of two."""
    exponent = 0
    value = 2 * N
    while value > 1 and value % 2 == 0:
        exponent += 1
        value //= 2
    if value != 1:
        raise ValueError("exact rational endpoint alpha requires 2N to be a power of two")
    return Fraction(1, exponent)


def generate_exact_4_to_8_surrogate(harmonics=3):
    surrogate = generate_mobius_endpoint_surrogate(4, harmonics)
    return MobiusEndpointSurrogate(
        N=surrogate.N,
        endpoint=surrogate.endpoint,
        harmonics=surrogate.harmonics,
        alpha=Fraction(1, 3),
        reduced_frequencies=surrogate.reduced_frequencies,
        frequencies=surrogate.frequencies,
        u=surrogate.u,
        d=surrogate.d,
        raw_modes=surrogate.raw_modes,
    )
