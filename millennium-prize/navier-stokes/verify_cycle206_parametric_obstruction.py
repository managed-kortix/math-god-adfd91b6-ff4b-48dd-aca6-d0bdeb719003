#!/usr/bin/env python3
"""Verify the Cycle 205 three-row obstruction for symbolic R, Y, and nu."""

from __future__ import annotations

import sympy as sp


R, Y, nu = sp.symbols("R Y nu", real=True, nonzero=True)
I = sp.I


def add_wave(left, right):
    return tuple(a + b for a, b in zip(left, right))


def neg_wave(wave):
    return tuple(-a for a in wave)


def sums(left, right):
    return {add_wave(a, b) for a in left for b in right} - {(0, 0, 0)}


def physical(wave):
    return (wave[0] * R, wave[1] * Y, sp.Integer(0))


def dot(left, right):
    return sp.expand(sum(a * b for a, b in zip(left, right)))


def vector_add(left, right):
    return tuple(sp.expand(a + b) for a, b in zip(left, right))


def vector_scale(value, vector):
    return tuple(sp.expand(value * entry) for entry in vector)


def project(wave, vector):
    k = physical(wave)
    radial = dot(k, vector)
    norm_squared = dot(k, k)
    return tuple(sp.cancel(entry - axis * radial / norm_squared) for axis, entry in zip(k, vector))


def orbit_representative(wave):
    opposite = neg_wave(wave)
    return min(wave, opposite, key=lambda item: (item[2], item[1], item[0]))


def polarization_basis(wave):
    x, y, _ = wave
    divisor = sp.gcd(abs(x), abs(y))
    return ((-y * Y / divisor, x * R / divisor, 0), (0, 0, 1))


def seed_field():
    e2 = (0, 1, 0)
    e3 = (0, 0, 1)
    field = {(x, 0, 0): e2 for x in (-6, -2, 2, 6)}
    for wave, coefficient in {
        (-2, 1, 0): 1,
        (2, 1, 0): -1,
        (2, -1, 0): 1,
        (-2, -1, 0): -1,
    }.items():
        field[wave] = vector_scale(coefficient, e3)
    return field


def make_data():
    seed = set(seed_field())
    support = seed | sums(seed, seed)
    u2 = sums(support, support)
    u3 = sums(support, u2)
    terminals = {(-8, 1, 0), (8, 1, 0), (8, -1, 0), (-8, -1, 0)}
    helpers = sorted(
        {orbit_representative(wave) for wave in support - seed},
        key=lambda item: (item[2], item[1], item[0]),
    )
    terminal_orbits = {orbit_representative(wave) for wave in terminals}
    return seed, support, u2, u3, terminals, helpers, terminal_orbits


def make_field(support, helpers, terminal_orbits):
    field = seed_field()
    variables = {}
    for orbit_index, representative in enumerate(helpers):
        amplitudes = []
        for basis_name in ("planar", "vertical"):
            real = sp.Symbol(f"q1_o{orbit_index}_{basis_name}_re", real=True)
            imag = sp.Symbol(f"q1_o{orbit_index}_{basis_name}_im", real=True)
            variables[str(real)] = real
            variables[str(imag)] = imag
            amplitudes.append(0 if representative in terminal_orbits else real + I * imag)
        basis = polarization_basis(representative)
        value = tuple(sp.expand(sum(amplitudes[j] * basis[j][axis] for j in range(2))) for axis in range(3))
        field[representative] = value
        field[neg_wave(representative)] = tuple(sp.conjugate(entry) for entry in value)
    assert set(field) == support
    return field, variables


def navier(field, outputs):
    result = {}
    occupied = list(field)
    for wave in outputs:
        k = physical(wave)
        value = vector_scale(-nu * dot(k, k), field.get(wave, (0, 0, 0)))
        nonlinear = (0, 0, 0)
        for left in occupied:
            right = tuple(wave[index] - left[index] for index in range(3))
            if right in field:
                nonlinear = vector_add(nonlinear, vector_scale(dot(field[left], physical(right)), field[right]))
        result[wave] = vector_add(value, vector_scale(-I, project(wave, nonlinear)))
    return result


def navier_derivative(field, direction, outputs):
    result = {}
    for wave in outputs:
        k = physical(wave)
        value = vector_scale(-nu * dot(k, k), direction.get(wave, (0, 0, 0)))
        nonlinear = (0, 0, 0)
        for left in direction:
            right = tuple(wave[index] - left[index] for index in range(3))
            if right in field:
                nonlinear = vector_add(nonlinear, vector_scale(dot(direction[left], physical(right)), field[right]))
        for left in field:
            right = tuple(wave[index] - left[index] for index in range(3))
            if right in direction:
                nonlinear = vector_add(nonlinear, vector_scale(dot(field[left], physical(right)), direction[right]))
        result[wave] = vector_add(value, vector_scale(-I, project(wave, nonlinear)))
    return result


def real_imag(expression, part):
    expression = sp.expand_complex(expression)
    return sp.factor(sp.re(expression) if part == "real" else sp.im(expression))


def main():
    _, support, _, _, _, helpers, terminal_orbits = make_data()
    field, variables = make_field(support, helpers, terminal_orbits)

    linear_sources = [
        ((-10, -2, 0), 1, "real"), ((-10, -2, 0), 1, "imag"),
        ((10, -2, 0), 1, "real"), ((10, -2, 0), 1, "imag"),
        ((-14, -1, 0), 2, "real"), ((-14, -1, 0), 2, "imag"),
        ((-10, -1, 0), 1, "real"), ((-10, -1, 0), 1, "imag"),
        ((-10, -1, 0), 2, "real"), ((-10, -1, 0), 2, "imag"),
        ((-6, -1, 0), 1, "real"), ((-6, -1, 0), 1, "imag"),
        ((-6, -1, 0), 2, "real"), ((-6, -1, 0), 2, "imag"),
        ((6, -1, 0), 2, "imag"),
        ((10, -1, 0), 1, "real"), ((10, -1, 0), 1, "imag"),
        ((10, -1, 0), 2, "real"), ((10, -1, 0), 2, "imag"),
    ]
    second_wave = (-14, -1, 0)
    required_first = {wave for wave, _, _ in linear_sources}
    required_first |= {(-12, -1, 0), (8, -1, 0)}
    required_first |= {
        tuple(second_wave[index] - wave[index] for index in range(3))
        for wave in support
    }
    required_first.discard((0, 0, 0))
    first = navier(field, required_first)

    linear = [real_imag(first[wave][component], part) for wave, component, part in linear_sources]

    a = variables["q1_o9_planar_im"]
    b = variables["q1_o10_planar_im"]
    c = variables["q1_o10_planar_re"]
    zero_planar_orbits = (0, 2, 4, 5, 6, 8)
    substitution = {
        variables[f"q1_o{index}_planar_{part}"]: 0
        for index in zero_planar_orbits
        for part in ("re", "im")
    }
    substitution.update({
        variables["q1_o9_planar_re"]: c / 2,
        variables["q1_o4_vertical_re"]: -R * c / 2,
        variables["q1_o4_vertical_im"]: -R * a,
        variables["q1_o5_vertical_re"]: 0,
        variables["q1_o5_vertical_im"]: R * (2 * a - b),
        variables["q1_o6_vertical_re"]: R * c / 2,
        variables["q1_o6_vertical_im"]: -R * a,
    })
    assert all(sp.cancel(expression.subs(substitution)) == 0 for expression in linear)
    active = [symbol for name, symbol in variables.items() if "_o3_" not in name and "_o7_" not in name]
    matrix, rhs = sp.linear_eq_to_matrix(linear, active)
    solution = sp.linsolve((matrix, rhs), active)
    assert solution is not sp.EmptySet
    solution_tuple = next(iter(solution))
    assert all(
        sp.cancel(value - substitution.get(symbol, symbol)) == 0
        for symbol, value in zip(active, solution_tuple)
    )

    reduced_field = {
        wave: tuple(sp.factor(sp.sympify(entry).subs(substitution)) for entry in value)
        for wave, value in field.items()
    }
    reduced_first = navier(reduced_field, required_first)
    f = sp.factor(real_imag(reduced_first[(-12, -1, 0)][2], "imag"))
    second = navier_derivative(reduced_field, reduced_first, {second_wave})
    g = sp.factor(real_imag(second[second_wave][2], "real"))

    terminal_seed = navier(seed_field(), {(8, -1, 0)})[(8, -1, 0)][2]
    h = sp.factor(real_imag(reduced_first[(8, -1, 0)][2] - terminal_seed, "imag"))

    expected_f = R**2 * Y * (c**2 - 4 * a**2) / 4
    expected_g = Y**2 * (1 + R**2 * (8 * a * b - 3 * c**2 - 4 * a**2) / 4)
    expected_h = R**2 * Y * (4 * a * b - c**2 - 4 * a**2) / 2
    assert sp.cancel(f - expected_f) == 0
    assert sp.cancel(g - expected_g) == 0
    assert sp.cancel(h - expected_h) == 0
    certificate = sp.factor(f / Y + g / Y**2 - h / Y)
    assert certificate == 1

    print("f =", f)
    print("g =", g)
    print("h =", h)
    print("certificate: f/Y + g/Y^2 - h/Y =", certificate)


if __name__ == "__main__":
    main()
