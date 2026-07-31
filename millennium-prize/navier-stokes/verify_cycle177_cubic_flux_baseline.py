#!/usr/bin/env python3
"""Numerical certificate for the Cycle 177 shared-pump cubic-flux baseline."""

import math


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(a):
    return math.sqrt(dot(a, a))


def project(k, value):
    return add(value, scale(-dot(k, value) / dot(k, k), k))


def symbol(p, q, a, b):
    raw = add(scale(dot(a, q), b), scale(dot(b, p), a))
    return project(add(p, q), raw)


def close(a, b, tolerance=1e-11):
    return math.isclose(a, b, rel_tol=tolerance, abs_tol=tolerance)


def main():
    n = 7
    layers = (8, 13, 21, 34, 55, 89, 144, 233)
    pump_wave = (n, 0, 0)
    pump_direction = (0.0, 1.0, 0.0)
    rail_direction = (0.0, 0.0, 1.0)

    data = []
    for y in layers:
        rail_wave = (0, y, 0)
        receiver_wave = add(pump_wave, rail_wave)
        interaction = symbol(
            pump_wave, rail_wave, pump_direction, rail_direction
        )
        assert interaction == (0.0, 0.0, float(y))

        gamma = y / math.sqrt(
            2.0 * norm(pump_wave) * norm(rail_wave) * norm(receiver_wave)
        )
        d = gamma ** -2
        data.append((rail_wave, receiver_wave, gamma, d))

    d_sum = sum(math.sqrt(row[3]) for row in data)
    pump_energy = d_sum ** (2.0 / 3.0)
    baseline = 3.0 * d_sum ** (2.0 / 3.0)
    total_energy = pump_energy

    pump_amplitude = math.sqrt(pump_energy / (2.0 * norm(pump_wave)))
    for rail_wave, receiver_wave, gamma, d in data:
        side_energy = math.sqrt(d / pump_energy)
        rail_amplitude = math.sqrt(side_energy / (2.0 * norm(rail_wave)))
        receiver_amplitude = math.sqrt(
            side_energy / (2.0 * norm(receiver_wave))
        )
        forcing = -1j * rail_wave[1] * pump_amplitude * rail_amplitude
        receiver = 1j * receiver_amplitude
        orbit_flux = 2.0 * abs((receiver.conjugate() * forcing).real)
        normalized_bound = gamma * math.sqrt(
            pump_energy * side_energy * side_energy
        )
        assert close(orbit_flux, 1.0)
        assert close(normalized_bound, 1.0)
        total_energy += 2.0 * side_energy

    assert close(total_energy, baseline)

    equal_d = 11.0
    for edge_count in (1, 2, 4, 16, 256):
        direct = 3.0 * (edge_count * math.sqrt(equal_d)) ** (2.0 / 3.0)
        formula = 3.0 * edge_count ** (2.0 / 3.0) * equal_d ** (1.0 / 3.0)
        assert close(direct, formula)

    print("Cycle 177 invariant cubic-flux baseline")
    print("shared pump edges =", len(data))
    print("D =", f"{d_sum:.12f}")
    print("optimal pump energy =", f"{pump_energy:.12f}")
    print("AM-GM baseline =", f"{baseline:.12f}")
    print("realized critical energy =", f"{total_energy:.12f}")
    print("all designated physical orbit fluxes = 1")
    print("shared-pump excess = 0")
    print("all symbol and normalization checks passed")


if __name__ == "__main__":
    main()
