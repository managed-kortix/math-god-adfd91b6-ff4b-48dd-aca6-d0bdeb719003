#!/usr/bin/env python3
"""Numerical certificate for the Cycle 177 receiver-flux counterexample."""

from collections import defaultdict
from math import isclose, sqrt


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), 0j)


def hermitian(a, b):
    return sum((x * y.conjugate() for x, y in zip(a, b)), 0j)


def project(k, v):
    norm2 = sum(x * x for x in k)
    if norm2 == 0:
        return v
    coefficient = sum(x * y for x, y in zip(k, v)) / norm2
    return tuple(y - coefficient * x for x, y in zip(k, v))


def neg(k):
    return tuple(-x for x in k)


def add_mode(field, k, value):
    field[k] = add(field.get(k, (0j, 0j, 0j)), value)


def make_field(r, heights, b, amplitudes):
    e2 = (0j, 1 + 0j, 0j)
    e3 = (0j, 0j, 1 + 0j)
    field = {(r, 0, 0): scale(b, e2), (-r, 0, 0): scale(b, e2)}

    for y, (a, c) in zip(heights, amplitudes):
        positive_layer = {
            (-r, y, 0): scale(a, e3),
            (r, y, 0): scale(-a, e3),
            (-2 * r, y, 0): scale(1j * c, e3),
            (2 * r, y, 0): scale(-1j * c, e3),
        }
        for k, value in positive_layer.items():
            add_mode(field, k, value)
            add_mode(field, neg(k), tuple(x.conjugate() for x in value))
    return field


def nonlinearity(field):
    output = defaultdict(lambda: (0j, 0j, 0j))
    for p, a in field.items():
        for q, b in field.items():
            k = add(p, q)
            ordered = project(k, scale(1j * dot(a, q), b))
            output[k] = add(output[k], ordered)
    return {k: v for k, v in output.items() if max(abs(x) for x in v) > 1e-10}


def critical_energy(field):
    representatives = []
    seen = set()
    for k in field:
        if k not in seen:
            representatives.append(k)
            seen.add(k)
            seen.add(neg(k))
    return sum(
        2 * sqrt(sum(x * x for x in k)) * float(hermitian(field[k], field[k]).real)
        for k in representatives
    )


def optimized_parameters(r, heights):
    geometry = []
    for y in heights:
        rail_weight = sqrt(r * r + y * y)
        receiver_weight = sqrt(4 * r * r + y * y)
        geometry.append((rail_weight, receiver_weight))
    s_l = sum(sqrt(k * q) / y for y, (k, q) in zip(heights, geometry))
    b = (2 * s_l / r) ** (1 / 3)
    amplitudes = []
    for y, (k, q) in zip(heights, geometry):
        a = sqrt(sqrt(q / k) / (y * b))
        c = sqrt(sqrt(k / q) / (y * b))
        amplitudes.append((a, c))
    minimum = 3 * 2 ** (5 / 3) * r ** (1 / 3) * s_l ** (2 / 3)
    return b, amplitudes, minimum


def verify(length):
    r = 1
    heights = list(range(1, length + 1))
    b, amplitudes, minimum = optimized_parameters(r, heights)
    field = make_field(r, heights, b, amplitudes)
    output = nonlinearity(field)

    expected_support = set()
    for y, (a, c) in zip(heights, amplitudes):
        for x in (-2 * r, 2 * r):
            k = (x, y, 0)
            flux = hermitian(output[k], field[k]).real
            assert isclose(flux, 1.0, rel_tol=1e-9, abs_tol=1e-9)
            expected_support.add(k)
            expected_support.add(neg(k))

        leakage = y * b * c
        expected = {
            (-3 * r, y, 0): -leakage,
            (-r, y, 0): -leakage,
            (r, y, 0): leakage,
            (3 * r, y, 0): leakage,
        }
        for k, coefficient in expected.items():
            assert isclose(output[k][2].real, coefficient, rel_tol=1e-9, abs_tol=1e-9)
            assert isclose(output[k][2].imag, 0.0, abs_tol=1e-9)
            expected_support.add(k)
            expected_support.add(neg(k))

    assert set(output) == expected_support
    energy = critical_energy(field)
    assert isclose(energy, minimum, rel_tol=1e-9, abs_tol=1e-9)
    return energy


def main():
    print("Cycle 177 shared-pump receiver-flux counterexample")
    print("L, exact minimized energy, energy/L")
    for length in (1, 2, 4, 8, 16, 32, 64):
        energy = verify(length)
        print(length, f"{energy:.12f}", f"{energy / length:.12f}")
    print("all complete-convolution, flux, and energy checks passed")


if __name__ == "__main__":
    main()
