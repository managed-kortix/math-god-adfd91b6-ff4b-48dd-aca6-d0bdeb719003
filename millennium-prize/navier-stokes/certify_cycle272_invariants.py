#!/usr/bin/env python3
"""Rigorous F, logarithmic-rate, and amplitude-invariant bounds for Cycle 272."""

import json
from fractions import Fraction

from flint import arb, ctx

import certify_p3_admission as p3


ZERO = (Fraction(0), Fraction(0))


def vector_add(target, wave, vector):
    row = target.setdefault(wave, [ZERO, ZERO, ZERO])
    for axis in range(3):
        row[axis] = p3.add_complex(row[axis], vector[axis])


def euler_bilinear(left, right):
    """Return -P((left dot grad) right) in exact complex Fourier form."""
    result = {}
    for q, left_vector in left.items():
        for r, right_vector in right.items():
            wave = tuple(q[i] + r[i] for i in range(3))
            if wave == (0, 0, 0):
                continue
            dot = ZERO
            for axis in range(3):
                dot = p3.add_complex(dot, p3.scale_complex(left_vector[axis], r[axis]))
            raw = [p3.mul_complex((Fraction(0), Fraction(-1)),
                                  p3.mul_complex(dot, right_vector[axis]))
                   for axis in range(3)]
            wave2 = sum(value * value for value in wave)
            wave_dot_raw = ZERO
            for axis in range(3):
                wave_dot_raw = p3.add_complex(
                    wave_dot_raw, p3.scale_complex(raw[axis], wave[axis])
                )
            projected = [
                p3.add_complex(
                    raw[axis],
                    p3.scale_complex(wave_dot_raw, Fraction(-wave[axis], wave2)),
                )
                for axis in range(3)
            ]
            vector_add(result, wave, projected)
    return {k: v for k, v in result.items() if any(value != ZERO for value in v)}


def vector_dot_series(left, right):
    result = {}
    for q, left_vector in left.items():
        for r, right_vector in right.items():
            wave = tuple(q[i] + r[i] for i in range(3))
            value = ZERO
            for axis in range(3):
                value = p3.add_complex(
                    value, p3.mul_complex(left_vector[axis], right_vector[axis])
                )
            result[wave] = p3.add_complex(result.get(wave, ZERO), value)
    return {k: v for k, v in result.items() if v != ZERO}


def series_add(left, right):
    result = dict(left)
    for wave, value in right.items():
        result[wave] = p3.add_complex(result.get(wave, ZERO), value)
    return {k: v for k, v in result.items() if v != ZERO}


def series_l1(coefficients):
    return sum(p3.qarb(re * re + im * im).sqrt() for re, im in coefficients.values())


def binomial_integral(weight, x_series, exponent, degree):
    coefficient = arb(1)
    power = {(0, 0, 0): (Fraction(1), Fraction(0))}
    total = arb(0)
    for n in range(degree + 1):
        product = p3.scalar_convolution(power, weight)
        constant = product.get((0, 0, 0), ZERO)
        if constant[1] != 0:
            raise ArithmeticError("non-real constant Fourier coefficient")
        total += coefficient * p3.qarb(constant[0])
        coefficient *= p3.qarb(exponent - n) / (n + 1)
        power = p3.scalar_convolution(power, x_series)
    return total


def enclose_second_derivative(data, precision=128):
    ctx.prec = precision
    velocity = p3.fourier_coefficients(data["modes"])
    acceleration = euler_bilinear(velocity, velocity)
    jerk_left = euler_bilinear(acceleration, velocity)
    jerk_right = euler_bilinear(velocity, acceleration)
    jerk = {}
    for wave in set(jerk_left) | set(jerk_right):
        vector_add(jerk, wave, [
            p3.add_complex(jerk_left.get(wave, [ZERO] * 3)[axis],
                           jerk_right.get(wave, [ZERO] * 3)[axis])
            for axis in range(3)
        ])

    polynomial = data["positive_speed_polynomial"]
    center_fraction = p3.frac(polynomial["speed_squared_center"])
    center = p3.qarb(center_fraction)
    rho = arb(polynomial["relative_perturbation_bound"])
    degree = int(polynomial["degree"])
    speed_squared = p3.speed_squared_coefficients(velocity)
    perturbation = dict(speed_squared)
    perturbation[(0, 0, 0)] = p3.add_complex(
        perturbation.get((0, 0, 0), ZERO), (-center_fraction, Fraction(0))
    )
    x_series = {
        k: p3.scale_complex(value, Fraction(1, 1) / center_fraction)
        for k, value in perturbation.items()
    }
    u_dot_a = vector_dot_series(velocity, acceleration)
    numerator = p3.scalar_convolution(u_dot_a, u_dot_a)
    regular = series_add(
        vector_dot_series(acceleration, acceleration),
        vector_dot_series(velocity, jerk),
    )
    inverse_part = binomial_integral(
        numerator, x_series, Fraction(-1, 2), degree
    ) / center.sqrt()
    direct_part = center.sqrt() * binomial_integral(
        regular, x_series, Fraction(1, 2), degree
    )
    remainder_factor = rho ** (degree + 1) / (1 - rho)
    remainder = 3 * remainder_factor * (
        series_l1(numerator) / center.sqrt() + center.sqrt() * series_l1(regular)
    )
    return 3 * (inverse_part + direct_part) + arb(0, remainder), remainder


def enclose_f(data, precision=128):
    ctx.prec = precision
    velocity = p3.fourier_coefficients(data["modes"])
    p3.check_divergence_free(velocity)
    speed_squared = p3.speed_squared_coefficients(velocity)
    polynomial = data["positive_speed_polynomial"]
    center_fraction = p3.frac(polynomial["speed_squared_center"])
    center = p3.qarb(center_fraction)
    rho = arb(polynomial["relative_perturbation_bound"])
    degree = int(polynomial["degree"])
    if degree < 2 or not rho < 1:
        raise ValueError("F enclosure requires degree >= 2 and rho < 1")

    perturbation = dict(speed_squared)
    perturbation[(0, 0, 0)] = p3.add_complex(
        perturbation.get((0, 0, 0), (Fraction(0), Fraction(0))),
        (-center_fraction, Fraction(0)),
    )
    computed_rho = sum(
        p3.qarb(re * re + im * im).sqrt() for re, im in perturbation.values()
    ) / center
    if not computed_rho <= rho:
        raise ValueError(f"speed perturbation bound fails: {computed_rho}")

    x_series = {
        k: p3.scale_complex(value, Fraction(1, 1) / center_fraction)
        for k, value in perturbation.items()
    }
    coefficient = arb(1)
    power = {(0, 0, 0): (Fraction(1), Fraction(0))}
    normalized_f = arb(0)
    for n in range(degree + 1):
        constant = power.get((0, 0, 0), (Fraction(0), Fraction(0)))
        if constant[1] != 0:
            raise ArithmeticError("non-real constant Fourier coefficient")
        normalized_f += coefficient * p3.qarb(constant[0])
        coefficient *= p3.qarb(Fraction(3 - 2 * n, 2 * (n + 1)))
        power = p3.scalar_convolution(power, x_series)

    scale = center * center.sqrt()
    remainder = scale * rho ** (degree + 1) / (1 - rho)
    f_interval = scale * normalized_f + arb(0, remainder)
    energy = p3.qarb(speed_squared[(0, 0, 0)][0])
    return f_interval, energy.sqrt(), computed_rho, remainder


def main():
    with open("cycle-272-p3-example.json", encoding="ascii") as handle:
        data = json.load(handle)
    with open("cycle-272-p3-certificate.json", encoding="ascii") as handle:
        certificate = json.load(handle)

    f_interval, l2_norm, computed_rho, f_error = enclose_f(data)
    second_derivative, second_error = enclose_second_derivative(data)
    p_lower = arb(certificate["certified_lower_endpoint"])
    p_upper = arb(certificate["certified_upper_endpoint"])
    p_interval = arb((p_lower + p_upper) / 2, (p_upper - p_lower) / 2)
    logarithmic_rate = p_interval / (3 * f_interval)
    invariant_objective = logarithmic_rate / l2_norm
    logarithmic_curvature = (
        second_derivative / (3 * f_interval)
        - p_interval * p_interval / (3 * f_interval * f_interval)
    )
    invariant_curvature = logarithmic_curvature / (l2_norm * l2_norm)
    shear_f = arb(256) ** 3
    shear_l2 = arb(256)
    result = {
        "amplitude_invariant_objective_P3_over_3F_L2": str(invariant_objective),
        "amplitude_invariant_objective_lower_endpoint": str(invariant_objective.lower()),
        "amplitude_invariant_objective_upper_endpoint": str(invariant_objective.upper()),
        "computed_speed_perturbation": str(computed_rho),
        "cubed_L3_second_derivative": str(second_derivative),
        "cubed_L3_second_derivative_remainder_bound": str(second_error),
        "cubed_L3_F": str(f_interval),
        "cubed_L3_F_lower_endpoint": str(f_interval.lower()),
        "cubed_L3_F_upper_endpoint": str(f_interval.upper()),
        "F_polynomial_remainder_bound": str(f_error),
        "L2_norm": str(l2_norm),
        "F_over_256_shear_F": str(f_interval / shear_f),
        "F_excess_over_256_shear_fraction": str(f_interval / shear_f - 1),
        "L2_excess_over_256_shear_fraction": str(l2_norm / shear_l2 - 1),
        "logarithmic_derivative_P3_over_3F": str(logarithmic_rate),
        "logarithmic_derivative_lower_endpoint": str(logarithmic_rate.lower()),
        "logarithmic_derivative_upper_endpoint": str(logarithmic_rate.upper()),
        "logarithmic_curvature": str(logarithmic_curvature),
        "logarithmic_curvature_lower_endpoint": str(logarithmic_curvature.lower()),
        "logarithmic_curvature_upper_endpoint": str(logarithmic_curvature.upper()),
        "amplitude_invariant_logarithmic_curvature": str(invariant_curvature),
        "amplitude_invariant_curvature_lower_endpoint": str(invariant_curvature.lower()),
        "amplitude_invariant_curvature_upper_endpoint": str(invariant_curvature.upper()),
        "normalization": "normalized Haar measure on [0,2*pi]^3",
        "P3_input_interval": str(p_interval),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
