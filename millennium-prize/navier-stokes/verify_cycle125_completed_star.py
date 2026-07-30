#!/usr/bin/env python3
"""Exact full-Fourier verifier for the Cycle 125 completed star (stdlib only)."""

from fractions import Fraction as F


ZERO_MODE = (0, 0, 0)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def z(real=0, imag=0):
    return (F(real), F(imag))


def cadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def cneg(a):
    return (-a[0], -a[1])


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def cscale(a, scalar):
    return (a[0] * scalar, a[1] * scalar)


def cconj(a):
    return (a[0], -a[1])


def vector(*entries):
    return tuple(z(real, imag) for real, imag in entries)


ZERO_VECTOR = vector((0, 0), (0, 0), (0, 0))


def vadd(a, b):
    return tuple(cadd(x, y) for x, y in zip(a, b))


def vdot(a, b):
    result = z()
    for x, y in zip(a, b):
        result = cadd(result, cmul(x, y))
    return result


def vconj(a):
    return tuple(cconj(x) for x in a)


def norm2(a):
    value = vdot(vconj(a), a)
    require(value[1] == 0, "squared norm is not real")
    return value[0]


def wave_norm2(k):
    return sum(x * x for x in k)


def negate_wave(k):
    return tuple(-x for x in k)


def project(k, value):
    denominator = wave_norm2(k)
    require(denominator > 0, "attempted Leray projection at zero frequency")
    k_dot_value = z()
    for coordinate, component in zip(k, value):
        k_dot_value = cadd(k_dot_value, cscale(component, coordinate))
    return tuple(
        cadd(component, cneg(cscale(k_dot_value, F(coordinate, denominator))))
        for coordinate, component in zip(k, value)
    )


def merge_fields(*fields):
    result = {}
    for field in fields:
        for mode, value in field.items():
            result[mode] = vadd(result.get(mode, ZERO_VECTOR), value)
    return {mode: value for mode, value in result.items() if norm2(value)}


def convolution(left, right):
    """Return -i P_n sum_(r+s=n) (left_r.s) right_s and pair count."""
    result = {}
    pair_count = 0
    for r, left_value in left.items():
        for s, right_value in right.items():
            pair_count += 1
            n = tuple(x + y for x, y in zip(r, s))
            if n == ZERO_MODE:
                continue
            contraction = z()
            for component, coordinate in zip(left_value, s):
                contraction = cadd(contraction, cscale(component, coordinate))
            raw = tuple(cmul(z(0, -1), cmul(contraction, component))
                        for component in right_value)
            result[n] = vadd(result.get(n, ZERO_VECTOR), project(n, raw))
    return ({mode: value for mode, value in result.items() if norm2(value)},
            pair_count)


def add_reality_partners(positive_modes):
    field = dict(positive_modes)
    for mode, value in positive_modes.items():
        negative = negate_wave(mode)
        require(negative not in field, "duplicate reality partner")
        field[negative] = vconj(value)
    return field


def check_field(field, name):
    require(ZERO_MODE not in field, f"{name} contains the zero mode")
    for mode, value in field.items():
        require(negate_wave(mode) in field, f"{name} is missing a reality partner")
        require(field[negate_wave(mode)] == vconj(value),
                f"{name} violates Fourier reality at {mode}")
        divergence = z()
        for coordinate, component in zip(mode, value):
            divergence = cadd(divergence, cscale(component, coordinate))
        require(divergence == z(), f"{name} is not divergence-free at {mode}")


def grouped_quadratic(coefficients, allowed_modes=None):
    """Group |sum_j epsilon^j v_j(n)|^2 by power and |n|^2."""
    groups = {}
    powers = sorted(coefficients)
    modes = set().union(*(set(coefficients[power]) for power in powers))
    if allowed_modes is not None:
        modes &= set(allowed_modes)
    for mode in modes:
        for left_power in powers:
            left = coefficients[left_power].get(mode)
            if left is None:
                continue
            for right_power in powers:
                right = coefficients[right_power].get(mode)
                if right is None:
                    continue
                value = vdot(vconj(left), right)
                require(value[1] == 0, "quadratic coefficient is not real")
                power = left_power + right_power
                radius2 = wave_norm2(mode)
                groups.setdefault(power, {})[radius2] = (
                    groups.setdefault(power, {}).get(radius2, F(0)) + value[0]
                )
    return {
        power: {radius2: value for radius2, value in radii.items() if value}
        for power, radii in groups.items()
        if any(radii.values())
    }


def grouped_phi(u_coefficients, q_coefficients):
    """Group 2 Re sum |n| conjugate(u_n).B_n by epsilon power and |n|^2."""
    groups = {}
    for u_power, u_field in u_coefficients.items():
        for q_power, q_field in q_coefficients.items():
            power = u_power + q_power
            for mode, u_value in u_field.items():
                q_value = q_field.get(mode)
                if q_value is None:
                    continue
                value = vdot(vconj(u_value), q_value)
                require(value[1] == 0, "critical flux coefficient is not real")
                radius2 = wave_norm2(mode)
                groups.setdefault(power, {})[radius2] = (
                    groups.setdefault(power, {}).get(radius2, F(0))
                    + 2 * value[0]
                )
    return {
        power: {radius2: value for radius2, value in radii.items() if value}
        for power, radii in groups.items()
        if any(radii.values())
    }


def grouped_ordinary_energy_derivative(u_coefficients, q_coefficients):
    values = {}
    for u_power, u_field in u_coefficients.items():
        for q_power, q_field in q_coefficients.items():
            power = u_power + q_power
            for mode, u_value in u_field.items():
                q_value = q_field.get(mode)
                if q_value is None:
                    continue
                value = vdot(vconj(u_value), q_value)
                require(value[1] == 0, "ordinary energy derivative is not real")
                values[power] = values.get(power, F(0)) + 2 * value[0]
    return {power: value for power, value in values.items() if value}


def main():
    k = (1, 0, 0)
    p = (0, 1, 0)
    q = (1, 1, 0)
    core = add_reality_partners({
        k: vector((0, 0), (1, 0), (1, 0)),
        p: vector((1, 0), (0, 0), (1, 0)),
        q: vector((0, -1), (0, 1), (0, -1)),
    })
    check_field(core, "Cycle 113 core")

    q0, count00 = convolution(core, core)
    leaf_modes = set(q0) - set(core)
    expected_leaf_modes = {
        (1, 2, 0), (2, 1, 0), (-1, -2, 0), (-2, -1, 0),
    }
    require(leaf_modes == expected_leaf_modes,
            "Cycle 113 exterior launch support changed")
    leaves = {mode: q0[mode] for mode in leaf_modes}
    require(leaves[(1, 2, 0)] == vector((-F(2, 5), 0), (F(1, 5), 0), (0, 0)),
            "launch vector at (1,2,0) changed")
    require(leaves[(2, 1, 0)] == vector((-F(1, 5), 0), (F(2, 5), 0), (-2, 0)),
            "launch vector at (2,1,0) changed")
    check_field(leaves, "Cycle 113 launch leaves")

    support = set(core) | set(leaves)
    require(len(support) == 10, "completed support must contain ten modes")

    q01, count01 = convolution(core, leaves)
    q10, count10 = convolution(leaves, core)
    q1 = merge_fields(q01, q10)
    q2, count11 = convolution(leaves, leaves)
    require(count00 + count01 + count10 + count11 == len(support) ** 2,
            "full ordered-pair convolution count changed")
    q_coefficients = {0: q0, 1: q1, 2: q2}
    u_coefficients = {0: core, 1: leaves}

    require(not (set(q0) - support),
            "completed support retains order-one exterior leakage")
    require(any(mode in q1 and norm2(q1[mode]) for mode in core),
            "leaf additions unexpectedly leave core dynamics unchanged")

    energy_groups = grouped_quadratic(u_coefficients)
    expected_energy = {
        0: {1: F(8), 2: F(6)},
        2: {5: F(44, 5)},
    }
    require(energy_groups == expected_energy, "E_half coefficients changed")

    phi_groups = grouped_phi(u_coefficients, q_coefficients)
    expected_phi = {
        0: {1: F(-8), 2: F(8)},
        1: {1: F(-16, 5), 2: F(-72, 5), 5: F(88, 5)},
    }
    require(phi_groups == expected_phi, "Phi_half coefficients changed")

    exterior = set().union(*(set(field) for field in q_coefficients.values())) - support
    lambda_groups = grouped_quadratic(q_coefficients, exterior)
    expected_lambda = {
        2: {4: F(208, 5), 8: F(864, 25),
            10: F(1252, 125), 13: F(2168, 325)},
        4: {2: F(72, 25), 18: F(72, 25)},
    }
    require(lambda_groups == expected_lambda, "Lambda_half coefficients changed")

    require(grouped_ordinary_energy_derivative(u_coefficients, q_coefficients) == {},
            "Euler convolution fails exact kinetic-energy conservation")

    energy_valuation = min(energy_groups)
    phi_valuation = min(phi_groups)
    lambda_valuation = min(lambda_groups)
    ratio_valuation = 2 * phi_valuation - energy_valuation - lambda_valuation
    require((energy_valuation, phi_valuation, lambda_valuation) == (0, 0, 2),
            "observable valuations changed")
    require(ratio_valuation == -2, "ratio does not diverge as epsilon^-2")

    print("Cycle 125 epsilon-completed Cycle 113 star")
    print("full ordered Fourier pairs checked = 100")
    print("completed support modes = 10; exterior generated modes =", len(exterior))
    print("E_half(epsilon) = 8 + 6 sqrt(2) + (44 sqrt(5)/5) epsilon^2")
    print("Phi_half(epsilon) = 8(sqrt(2)-1)"
          " + (-16-72 sqrt(2)+88 sqrt(5))/5 epsilon")
    print("Lambda_half(epsilon) = A epsilon^2 + B epsilon^4")
    print("A = 416/5 + 1728 sqrt(2)/25 + 1252 sqrt(10)/125"
          " + 2168 sqrt(13)/325")
    print("B = 288 sqrt(2)/25")
    print("Phi_half^2/(E_half Lambda_half) ~ K epsilon^-2")
    print("K = 64(sqrt(2)-1)^2 / ((8+6 sqrt(2)) A) > 0")
    print("valuations: v(E_half)=0, v(Phi_half)=0, v(Lambda_half)=2, v(ratio)=-2")
    print("support additions alter internal dynamics at order epsilon: verified")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
