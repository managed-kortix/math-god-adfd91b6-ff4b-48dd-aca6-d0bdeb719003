#!/usr/bin/env python3
"""Rigorous Arb enclosure of the Euler velocity-L3 production functional.

Run with, for example:
  uv run --with python-flint python certify_p3_admission.py --example --subdivisions 32

The input format and proof bounds are documented in
cycle-272-p3-interval-admission-tool.md.  All spatial integrals use normalized
Haar measure on [0,2*pi]^3.
"""

import argparse
import json
from fractions import Fraction
from itertools import product

from flint import arb, ctx


def frac(value):
    return Fraction(str(value))


def add_complex(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul_complex(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def scale_complex(a, scale):
    return (a[0] * scale, a[1] * scale)


def fourier_coefficients(modes):
    coefficients = {}
    for mode in modes:
        k = tuple(mode["k"])
        amplitude = [frac(x) for x in mode["amplitude"]]
        if mode["kind"] == "cos":
            factors = ((k, (Fraction(1, 2), Fraction(0))),
                       (tuple(-x for x in k), (Fraction(1, 2), Fraction(0))))
        elif mode["kind"] == "sin":
            factors = ((k, (Fraction(0), Fraction(-1, 2))),
                       (tuple(-x for x in k), (Fraction(0), Fraction(1, 2))))
        else:
            raise ValueError("mode kind must be 'sin' or 'cos'")
        for wave, factor in factors:
            vector = coefficients.setdefault(wave, [(Fraction(0), Fraction(0)) for _ in range(3)])
            for axis in range(3):
                vector[axis] = add_complex(vector[axis], scale_complex(factor, amplitude[axis]))
    return coefficients


def check_divergence_free(coefficients):
    for k, vector in coefficients.items():
        divergence = (Fraction(0), Fraction(0))
        for axis in range(3):
            divergence = add_complex(divergence, scale_complex(vector[axis], k[axis]))
        if divergence != (0, 0):
            raise ValueError(f"nonzero divergence coefficient at {k}: {divergence}")


def pressure_coefficients(velocity):
    pressure = {}
    waves = list(velocity)
    for p in waves:
        for q in waves:
            k = tuple(p[i] + q[i] for i in range(3))
            k2 = sum(x * x for x in k)
            if k2 == 0:
                continue
            value = (Fraction(0), Fraction(0))
            for i in range(3):
                for j in range(3):
                    term = mul_complex(velocity[p][i], velocity[q][j])
                    value = add_complex(value, scale_complex(term, Fraction(-k[i] * k[j], k2)))
            pressure[k] = add_complex(pressure.get(k, (Fraction(0), Fraction(0))), value)
    return {k: value for k, value in pressure.items() if value != (0, 0)}


def speed_squared_coefficients(velocity):
    result = {}
    for p, vp in velocity.items():
        for q, vq in velocity.items():
            k = tuple(p[i] + q[i] for i in range(3))
            value = (Fraction(0), Fraction(0))
            for axis in range(3):
                value = add_complex(value, mul_complex(vp[axis], vq[axis]))
            result[k] = add_complex(result.get(k, (Fraction(0), Fraction(0))), value)
    return result


def scalar_convolution(left, right):
    result = {}
    for p, a in left.items():
        for q, b in right.items():
            k = tuple(p[i] + q[i] for i in range(3))
            result[k] = add_complex(result.get(k, (Fraction(0), Fraction(0))), mul_complex(a, b))
    return {k: value for k, value in result.items() if value != (0, 0)}


def qarb(value):
    value = Fraction(value)
    return arb(value.numerator) / value.denominator


def evaluate_real_series(coefficients, point):
    total = arb(0)
    for k, coefficient in coefficients.items():
        phase = sum(k[i] * point[i] for i in range(3))
        total += 2 * (qarb(coefficient[0]) * phase.cos() - qarb(coefficient[1]) * phase.sin())
    return total


def positive_half(coefficients):
    return {k: value for k, value in coefficients.items() if k > tuple(-x for x in k)}


def interval_abs_upper(value):
    return value.abs_upper()


def square_interval(value):
    if value.contains(0):
        upper = value.abs_upper() ** 2
        return arb(upper / 2, upper / 2)
    return value * value


def evaluate_box(velocity_half, pressure_half, point, epsilon):
    u = [evaluate_real_series({k: value[axis] for k, value in velocity_half.items()}, point)
         for axis in range(3)]
    derivative = [[evaluate_real_series(
        {k: mul_complex(value[component], (Fraction(0), Fraction(k[axis])))
         for k, value in velocity_half.items()}, point)
        for axis in range(3)] for component in range(3)]
    pressure = evaluate_real_series(pressure_half, point)
    pressure_gradient = [evaluate_real_series(
        {k: mul_complex(value, (Fraction(0), Fraction(k[axis])))
        for k, value in pressure_half.items()}, point) for axis in range(3)]
    pressure_hessian = [[evaluate_real_series(
        {k: scale_complex(value, Fraction(-k[i] * k[j]))
         for k, value in pressure_half.items()}, point)
        for j in range(3)] for i in range(3)]
    speed2 = sum(square_interval(value) for value in u)
    grad_speed2 = [2 * sum(u[j] * derivative[j][axis] for j in range(3)) for axis in range(3)]
    numerator = pressure * sum(u[axis] * grad_speed2[axis] for axis in range(3))
    speed2_upper = speed2.abs_upper()
    speed2_nonnegative = (
        arb(speed2_upper / 2, speed2_upper / 2) if speed2.contains(0) else speed2
    )
    epsilon2 = epsilon * epsilon
    denominator2 = speed2 + epsilon2
    lower = epsilon2.abs_lower() / 2
    upper = denominator2.abs_upper()
    denominator2 = arb((lower + upper) / 2, (upper - lower) / 2)
    regularized = qarb(Fraction(3, 2)) * numerator / denominator2.sqrt()
    speed_upper = sum(interval_abs_upper(value) ** 2 for value in u).sqrt()
    gradient_upper = sum(interval_abs_upper(value) ** 2 for row in derivative for value in row).sqrt()
    near_bound = 3 * interval_abs_upper(pressure) * speed_upper * gradient_upper
    speed_interval = speed2_nonnegative.sqrt()
    if speed_interval.is_nan():
        speed_interval = arb(speed_upper / 2, speed_upper / 2)
    integrated_by_parts = -3 * speed_interval * sum(
        u[axis] * pressure_gradient[axis] for axis in range(3)
    )
    h_upper = abs(sum(u[axis] * pressure_gradient[axis] for axis in range(3))).abs_upper()
    g_upper = sum(interval_abs_upper(value) ** 2 for value in pressure_gradient).sqrt()
    local_lipschitz = arb(0)
    for axis in range(3):
        du_upper = sum(interval_abs_upper(derivative[j][axis]) ** 2 for j in range(3)).sqrt()
        Hessian_upper = sum(interval_abs_upper(pressure_hessian[axis][j]) ** 2
                            for j in range(3)).sqrt()
        local_lipschitz += 3 * (
            du_upper * h_upper
            + speed_upper * (du_upper * g_upper + speed_upper * Hessian_upper)
        )
    if speed2.abs_lower() > 0:
        direct = qarb(Fraction(3, 2)) * numerator / speed2.sqrt()
        return direct, regularized, integrated_by_parts, False, near_bound, local_lipschitz
    return arb(0, near_bound), regularized, integrated_by_parts, True, near_bound, local_lipschitz


def coefficient_norms(velocity):
    a0 = arb(0)
    a1 = arb(0)
    for k, vector in velocity.items():
        length = sum(qarb(re * re + im * im) for re, im in vector).sqrt()
        a0 += length
        a1 += sum(abs(x) for x in k) * length
    return a0, a1


def scalar_derivative_norm(coefficients, order):
    total = arb(0)
    for k, (re, im) in coefficients.items():
        weight = sum(abs(x) for x in k) ** order
        total += weight * (qarb(re * re + im * im)).sqrt()
    return total


def scalar_l2_derivative_norm(coefficients, derivative):
    return sum(
        qarb(re * re + im * im) * (abs(k[derivative]) ** 2)
        for k, (re, im) in coefficients.items()
    ).sqrt()


def vector_l2_derivative_norm(coefficients, derivative):
    return sum(
        qarb(re * re + im * im) * (abs(k[derivative]) ** 2)
        for k, vector in coefficients.items() for re, im in vector
    ).sqrt()


def enclose(data, subdivisions, precision, epsilon_string):
    ctx.prec = precision
    modes = data["modes"]
    velocity = fourier_coefficients(modes)
    check_divergence_free(velocity)
    pressure = pressure_coefficients(velocity)
    velocity_half = positive_half(velocity)
    pressure_half = positive_half(pressure)
    epsilon = arb(epsilon_string)
    direct_total = arb(0)
    regularized_total = arb(0)
    by_parts_total = arb(0)
    midpoint_total = arb(0)
    local_midpoint_error = arb(0)
    near_boxes = 0
    near_absolute_mass = arb(0)
    pi = arb.pi()
    radius = pi / subdivisions
    for indices in product(range(subdivisions), repeat=3):
        midpoint = [arb(2 * index + 1) * radius for index in indices]
        box = [arb(value, radius) for value in midpoint]
        direct, regularized, by_parts, near, near_bound, local_lipschitz = evaluate_box(
            velocity_half, pressure_half, box, epsilon
        )
        direct_total += direct
        regularized_total += regularized
        by_parts_total += by_parts
        _, _, midpoint_value, _, _, _ = evaluate_box(
            velocity_half, pressure_half, midpoint, epsilon
        )
        midpoint_total += midpoint_value
        local_midpoint_error += radius * local_lipschitz
        if near:
            near_boxes += 1
            near_absolute_mass += near_bound
    box_mass = arb(1) / subdivisions**3
    direct_total *= box_mass
    regularized_total *= box_mass
    by_parts_total *= box_mass
    midpoint_total *= box_mass
    local_midpoint_error *= box_mass
    near_absolute_mass *= box_mass

    v0, v1 = coefficient_norms(velocity)
    pressure_wiener = 3 * v0 * v0
    pressure_gradient_wiener = scalar_derivative_norm(pressure, 1)
    pressure_hessian_wiener = scalar_derivative_norm(pressure, 2)
    gradp_l2 = sum(scalar_l2_derivative_norm(pressure, axis) ** 2
                   for axis in range(3)).sqrt()
    h_l2 = v0 * gradp_l2
    lipschitz = arb(0)
    for axis in range(3):
        du_l2 = vector_l2_derivative_norm(velocity, axis)
        du_sup = sum(
            abs(k[axis]) * sum(qarb(re * re + im * im) for re, im in vector).sqrt()
            for k, vector in velocity.items()
        )
        hessian_column_l2 = sum(
            scalar_l2_derivative_norm(
                {k: mul_complex(value, (Fraction(0), Fraction(k[j])))
                 for k, value in pressure.items()}, axis
            ) ** 2 for j in range(3)
        ).sqrt()
        dh_l2 = du_sup * gradp_l2 + v0 * hessian_column_l2
        lipschitz += du_l2 * h_l2 + v0 * dh_l2
    midpoint_lipschitz_error = (arb.pi() / subdivisions) * 3 * lipschitz
    midpoint_total += arb(0, local_midpoint_error)
    regularization_error = 3 * epsilon * pressure_wiener * v1
    regularized_total += arb(0, regularization_error)

    tail = data.get("analytic_tail", {"velocity_l1": "0", "gradient_l1": "0"})
    r0 = arb(tail["velocity_l1"])
    r1 = arb(tail["gradient_l1"])
    full_u0 = v0 + r0
    full_u1 = v1 + r1
    pressure_tail = 3 * (2 * v0 * r0 + r0 * r0)
    h_full = full_u0 * full_u1
    h_difference = full_u0 * r1 + 3 * v1 * r0
    functional_tail = 3 * (pressure_tail * h_full + pressure_wiener * h_difference)
    direct_total += arb(0, functional_tail)
    regularized_total += arb(0, functional_tail)
    by_parts_total += arb(0, functional_tail)
    midpoint_total += arb(0, functional_tail)

    polynomial_total = None
    polynomial_error = None
    polynomial = data.get("positive_speed_polynomial")
    if polynomial:
        center = qarb(frac(polynomial["speed_squared_center"]))
        degree = int(polynomial["degree"])
        perturbation_bound = arb(polynomial["relative_perturbation_bound"])
        speed_squared = speed_squared_coefficients(velocity)
        speed_squared[(0, 0, 0)] = add_complex(
            speed_squared.get((0, 0, 0), (Fraction(0), Fraction(0))),
            (-frac(polynomial["speed_squared_center"]), Fraction(0)),
        )
        computed_perturbation = sum(
            qarb(re * re + im * im).sqrt() for re, im in speed_squared.values()
        ) / center
        if not computed_perturbation <= perturbation_bound:
            raise ValueError(f"speed perturbation bound fails: {computed_perturbation}")
        if not perturbation_bound < 1:
            raise ValueError("relative_perturbation_bound must be below one")
        polynomial_total = arb(0)
        coefficients = [arb(1)]
        for n in range(1, degree + 1):
            coefficients.append(coefficients[-1] * qarb(Fraction(3 - 2 * n, 2 * n)))
        center_fraction = frac(polynomial["speed_squared_center"])
        x_series = {k: scale_complex(value, Fraction(1, 1) / center_fraction)
                    for k, value in speed_squared.items()}
        h_series = {}
        for axis in range(3):
            gradp_series = {k: mul_complex(value, (Fraction(0), Fraction(k[axis])))
                            for k, value in pressure.items()}
            h_axis = scalar_convolution(
                {k: value[axis] for k, value in velocity.items()}, gradp_series
            )
            for k, value in h_axis.items():
                h_series[k] = add_complex(h_series.get(k, (Fraction(0), Fraction(0))), value)
        power = {(0, 0, 0): (Fraction(1), Fraction(0))}
        for n in range(degree + 1):
            product_series = scalar_convolution(power, h_series)
            constant = product_series.get((0, 0, 0), (Fraction(0), Fraction(0)))
            if constant[1] != 0:
                raise ArithmeticError("non-real constant Fourier coefficient")
            polynomial_total += -3 * center.sqrt() * coefficients[n] * qarb(constant[0])
            power = scalar_convolution(power, x_series)
        h_bound = v0 * pressure_gradient_wiener
        polynomial_error = 3 * center.sqrt() * h_bound * (
            perturbation_bound ** (degree + 1) / (1 - perturbation_bound)
        )
        polynomial_total += arb(0, polynomial_error + functional_tail)

    chosen = polynomial_total if polynomial_total is not None else midpoint_total
    if subdivisions < data.get("minimum_certifying_subdivisions", 1):
        chosen = arb(0, chosen.abs_upper())
    return {
        "format": "P3-ADMISSION-ARB-v1",
        "normalization": "normalized Haar measure on [0,2*pi]^3",
        "precision_bits": precision,
        "subdivisions_per_axis": subdivisions,
        "boxes": subdivisions**3,
        "near_zero_boxes": near_boxes,
        "epsilon": epsilon_string,
        "finite_velocity_wiener_l1": str(v0),
        "finite_gradient_wiener_l1": str(v1),
        "pressure_wiener_bound": str(pressure_wiener),
        "pressure_gradient_wiener": str(pressure_gradient_wiener),
        "pressure_hessian_wiener": str(pressure_hessian_wiener),
        "near_box_absolute_mass": str(near_absolute_mass),
        "regularization_error_bound": str(regularization_error),
        "fourier_tail_error_bound": str(functional_tail),
        "domain_partition_P3": str(direct_total),
        "regularized_P3": str(regularized_total),
        "integrated_by_parts_P3": str(by_parts_total),
        "midpoint_lipschitz_error": str(midpoint_lipschitz_error),
        "local_midpoint_error": str(local_midpoint_error),
        "midpoint_P3": str(midpoint_total),
        "polynomial_P3": None if polynomial_total is None else str(polynomial_total),
        "polynomial_error": None if polynomial_error is None else str(polynomial_error),
        "computed_speed_perturbation": (
            None if polynomial_total is None else str(computed_perturbation)
        ),
        "intersection_P3": str(chosen),
        "certified_lower_endpoint": str(chosen.lower()),
        "certified_upper_endpoint": str(chosen.upper()),
        "proved_positive": bool(chosen.lower() > 0),
        "mode_count": len(modes),
        "pressure_fourier_count": len(pressure),
    }


EXAMPLE = {
    "name": "genuine-3d-five-wave-datum",
    "modes": [
        {"k": [0, 0, 1], "amplitude": [256, 0, 0], "kind": "sin"},
        {"k": [0, 0, 1], "amplitude": [0, 256, 0], "kind": "cos"},
        {"k": [1, 1, 0], "amplitude": [2, -2, -3], "kind": "cos"},
        {"k": [2, 1, 0], "amplitude": ["-6/5", "12/5", 3], "kind": "sin"},
        {"k": [1, 1, 1], "amplitude": ["8/3", "2/3", "-10/3"], "kind": "cos"},
        {"k": [0, 1, 1], "amplitude": [2, 1, -1], "kind": "cos"},
        {"k": [0, 0, 1], "amplitude": [3, -2, 0], "kind": "sin"},
    ],
    "analytic_tail": {"velocity_l1": "0", "gradient_l1": "0"},
    "positive_speed_polynomial": {
        "speed_squared_center": "65536",
        "relative_perturbation_bound": "19/125",
        "degree": 6
    },
}


def main():
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--example", action="store_true")
    source.add_argument("--input")
    parser.add_argument("--subdivisions", type=int, default=32)
    parser.add_argument("--precision", type=int, default=128)
    parser.add_argument("--epsilon", default="1/1024")
    parser.add_argument("--output")
    args = parser.parse_args()
    if args.subdivisions <= 0:
        parser.error("--subdivisions must be positive")
    data = EXAMPLE if args.example else json.load(open(args.input, encoding="ascii"))
    result = enclose(data, args.subdivisions, args.precision, args.epsilon)
    result["datum"] = data["name"]
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="ascii") as handle:
            handle.write(encoded)
    print(encoded, end="")
    if not result["proved_positive"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
