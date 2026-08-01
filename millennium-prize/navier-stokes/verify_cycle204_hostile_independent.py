#!/usr/bin/env python3
"""Independently rebuild and compare the Cycle 204 polynomial system."""

from collections import defaultdict
from fractions import Fraction
import importlib.util
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
GENERATOR = ROOT / "generate_cycle204_s2_system.py"
SUPPORT = ROOT / "cycle204_s2_support.json"
EQUATIONS = ROOT / "cycle204_s2_equations.json"


def load_generator():
    spec = importlib.util.spec_from_file_location("cycle204_generator", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add_wave(left, right):
    return tuple(a + b for a, b in zip(left, right))


def negate(wave):
    return tuple(-entry for entry in wave)


def wave_key(wave):
    return wave[2], wave[1], wave[0]


def representative(wave):
    return min(wave, negate(wave), key=wave_key)


def add_poly(left, right):
    result = defaultdict(Fraction, left)
    for monomial, coefficient in right.items():
        result[monomial] += coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def scale_poly(poly, scalar):
    return {monomial: scalar * coefficient for monomial, coefficient in poly.items() if scalar * coefficient}


def multiply_poly(left, right):
    result = defaultdict(Fraction)
    for a, ca in left.items():
        for b, cb in right.items():
            result[tuple(sorted(a + b))] += ca * cb
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def complex_add(left, right):
    return add_poly(left[0], right[0]), add_poly(left[1], right[1])


def complex_scale(value, scalar):
    return scale_poly(value[0], scalar), scale_poly(value[1], scalar)


def complex_multiply(left, right):
    return (
        add_poly(multiply_poly(left[0], right[0]), scale_poly(multiply_poly(left[1], right[1]), -1)),
        add_poly(multiply_poly(left[0], right[1]), multiply_poly(left[1], right[0])),
    )


ZERO = ({}, {})


def vector_add(left, right):
    return tuple(complex_add(a, b) for a, b in zip(left, right))


def vector_scale(vector, scalar):
    return tuple(complex_scale(entry, scalar) for entry in vector)


def dot(vector, wave):
    result = ZERO
    for entry, axis in zip(vector, wave):
        result = complex_add(result, complex_scale(entry, axis))
    return result


def project(wave, vector):
    norm = sum(axis * axis for axis in wave)
    radial = dot(vector, wave)
    return tuple(complex_add(entry, complex_scale(radial, Fraction(-axis, norm))) for entry, axis in zip(vector, wave))


def basis(wave):
    x, y, _ = wave
    divisor = math.gcd(abs(x), abs(y))
    return ((Fraction(-y, divisor), Fraction(x, divisor), Fraction(0)), (Fraction(0), Fraction(0), Fraction(1)))


def constant(value):
    return ({(): Fraction(value)} if value else {}, {})


def variable(real_name, imag_name):
    return ({(real_name,): Fraction(1)}, {(imag_name,): Fraction(1)})


def conjugate(value):
    return value[0], scale_poly(value[1], -1)


def build_field(support_data):
    e2 = (ZERO, constant(1), ZERO)
    e3 = (ZERO, ZERO, constant(1))
    field = {wave: e2 for wave in ((-6, 0, 0), (-2, 0, 0), (2, 0, 0), (6, 0, 0))}
    for wave, sign in (((-2, 1, 0), 1), ((2, 1, 0), -1), ((2, -1, 0), 1), ((-2, -1, 0), -1)):
        field[wave] = vector_scale(e3, sign)

    rows = support_data["variables"]
    lookup = {(tuple(row["orbit_representative"]), row["basis"], row["part"]): row for row in rows}
    orbits = sorted({tuple(row["orbit_representative"]) for row in rows}, key=wave_key)
    for orbit in orbits:
        status = lookup[(orbit, 0, "re")]["status"]
        amplitudes = []
        for index in range(2):
            if status == "pinned_zero_terminal":
                amplitudes.append(ZERO)
            else:
                amplitudes.append(variable(lookup[(orbit, index, "re")]["name"], lookup[(orbit, index, "im")]["name"]))
        vectors = basis(orbit)
        value = []
        for axis in range(3):
            component = ZERO
            for index in range(2):
                component = complex_add(component, complex_scale(amplitudes[index], vectors[index][axis]))
            value.append(component)
        field[orbit] = tuple(value)
        field[negate(orbit)] = tuple(conjugate(entry) for entry in value)
    return field


def navier(field, outputs):
    result = {}
    for wave in outputs:
        value = vector_scale(field.get(wave, (ZERO, ZERO, ZERO)), -sum(axis * axis for axis in wave))
        convolution = (ZERO, ZERO, ZERO)
        for left, left_value in field.items():
            right = tuple(wave[index] - left[index] for index in range(3))
            if right in field:
                convolution = vector_add(convolution, tuple(complex_multiply(dot(left_value, right), entry) for entry in field[right]))
        projected = project(wave, convolution)
        result[wave] = vector_add(value, tuple((entry[1], scale_poly(entry[0], -1)) for entry in projected))
    return result


def derivative(field, direction, outputs):
    result = {}
    for wave in outputs:
        value = vector_scale(direction.get(wave, (ZERO, ZERO, ZERO)), -sum(axis * axis for axis in wave))
        convolution = (ZERO, ZERO, ZERO)
        for left, left_value in direction.items():
            right = tuple(wave[index] - left[index] for index in range(3))
            if right in field:
                convolution = vector_add(convolution, tuple(complex_multiply(dot(left_value, right), entry) for entry in field[right]))
        for left, left_value in field.items():
            right = tuple(wave[index] - left[index] for index in range(3))
            if right in direction:
                convolution = vector_add(convolution, tuple(complex_multiply(dot(left_value, right), entry) for entry in direction[right]))
        projected = project(wave, convolution)
        result[wave] = vector_add(value, tuple((entry[1], scale_poly(entry[0], -1)) for entry in projected))
    return result


def primitive(poly):
    if not poly:
        return None
    denominator = math.lcm(*(coefficient.denominator for coefficient in poly.values()))
    integers = {monomial: int(coefficient * denominator) for monomial, coefficient in poly.items()}
    divisor = math.gcd(*(abs(coefficient) for coefficient in integers.values()))
    integers = {monomial: coefficient // divisor for monomial, coefficient in integers.items()}
    if integers[min(integers)] < 0:
        integers = {monomial: -coefficient for monomial, coefficient in integers.items()}
    return tuple(sorted(integers.items()))


def rebuild(support_data):
    seed = {tuple(wave) for wave in support_data["sets"]["K0"]}
    support = seed | {add_wave(a, b) for a in seed for b in seed} - {(0, 0, 0)}
    u2 = {add_wave(a, b) for a in support for b in support} - {(0, 0, 0)}
    u3 = {add_wave(a, b) for a in support for b in u2} - {(0, 0, 0)}
    assert [sorted(group, key=wave_key) for group in (support, u2, u3)] == [
        [tuple(wave) for wave in support_data["sets"][name]] for name in ("S2", "U2", "U3")
    ]
    field = build_field(support_data)
    first = navier(field, u2)
    second = derivative(field, first, u3)
    seed_field = {wave: field[wave] for wave in seed}
    terminals = {tuple(wave) for wave in support_data["terminal_policy"]["waves"]}
    seed_terminals = navier(seed_field, terminals)
    assert seed_terminals[(-8, -1, 0)][2] == ({}, {(): Fraction(-1)})
    assert seed_terminals[(8, -1, 0)][2] == ({}, {(): Fraction(1)})
    assert seed_terminals[(-8, 1, 0)][2] == ({}, {(): Fraction(-1)})
    assert seed_terminals[(8, 1, 0)][2] == ({}, {(): Fraction(1)})

    slots = []
    outside = (u2 | u3) - support
    for order, jet, available in ((1, first, u2), (2, second, u3)):
        for wave in sorted(outside & available, key=wave_key):
            if wave != representative(wave):
                continue
            components = (1, 2) if wave[0] else (0, 2)
            for component in components:
                slots.extend((primitive(jet[wave][component][0]), primitive(jet[wave][component][1])))
    for wave in sorted({representative(wave) for wave in terminals}, key=wave_key):
        components = (1, 2) if wave[0] else (0, 2)
        for component in components:
            difference = complex_add(first[wave][component], complex_scale(seed_terminals[wave][component], -1))
            slots.extend((primitive(difference[0]), primitive(difference[1])))
    unique = []
    seen = set()
    for slot in slots:
        if slot is not None and slot not in seen:
            seen.add(slot)
            unique.append(slot)
    return slots, unique


def artifact_primitives(data):
    result = []
    for row in data["equations"]:
        poly = defaultdict(Fraction)
        for term in row["terms"]:
            poly[tuple(sorted(term["monomial"]))] += Fraction(term["coefficient"])
        result.append(primitive(poly))
    return result


def first_mismatch(left, right):
    for index, (a, b) in enumerate(zip(left, right)):
        if a != b:
            return index, a, b
    return min(len(left), len(right)), None, None


def main():
    support_data = json.loads(SUPPORT.read_text())
    equations_data = json.loads(EQUATIONS.read_text())
    slots, rebuilt = rebuild(support_data)
    committed = artifact_primitives(equations_data)
    assert len(rebuilt) == len(committed)
    assert set(rebuilt) == set(committed)
    regenerated_support, regenerated_equations = load_generator().generate()
    assert regenerated_support == support_data
    assert regenerated_equations == equations_data
    print("Cycle 204 hostile independent rebuild verified")
    print("terminal seed signs: x=-8 -> -i e3; x=8 -> +i e3 for y=+/-1")
    print("raw scalar slots:", len(slots))
    print("primitive equations:", len(rebuilt))
    print("independent equations match regenerated and committed artifacts")


if __name__ == "__main__":
    main()
