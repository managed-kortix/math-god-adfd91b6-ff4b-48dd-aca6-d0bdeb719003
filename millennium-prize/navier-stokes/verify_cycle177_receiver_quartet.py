#!/usr/bin/env python3
"""Exact symbolic receiver audit for the Cycle 176 Laurent filter."""

from collections import defaultdict
from fractions import Fraction as F


NVAR = 4
ZERO_MONOMIAL = (0,) * NVAR


def poly_constant(value):
    value = F(value)
    return {} if value == 0 else {ZERO_MONOMIAL: value}


def poly_variable(index):
    monomial = [0] * NVAR
    monomial[index] = 1
    return {tuple(monomial): F(1)}


def poly_add(left, right):
    result = defaultdict(F)
    for monomial, coefficient in left.items():
        result[monomial] += coefficient
    for monomial, coefficient in right.items():
        result[monomial] += coefficient
    return {m: c for m, c in result.items() if c}


def poly_scale(coefficient, value):
    coefficient = F(coefficient)
    return {m: coefficient * c for m, c in value.items() if coefficient * c}


def poly_multiply(left, right):
    result = defaultdict(F)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(a + b for a, b in zip(left_monomial, right_monomial))
            result[monomial] += left_coefficient * right_coefficient
    return {m: c for m, c in result.items() if c}


def scalar(value):
    return value if isinstance(value, dict) else poly_constant(value)


def vector(*entries):
    return tuple(scalar(entry) for entry in entries)


ZERO_VECTOR = vector(0, 0, 0)


def vector_add(left, right):
    return tuple(poly_add(a, b) for a, b in zip(left, right))


def vector_scale(coefficient, value):
    coefficient = scalar(coefficient)
    return tuple(poly_multiply(coefficient, entry) for entry in value)


def frequency_add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def dot_frequency(frequency, value):
    result = poly_constant(0)
    for coefficient, entry in zip(frequency, value):
        result = poly_add(result, poly_scale(coefficient, entry))
    return result


def project(frequency, value):
    norm_squared = sum(entry * entry for entry in frequency)
    if norm_squared == 0:
        return value
    radial = dot_frequency(frequency, value)
    correction = vector(*(poly_scale(F(entry, norm_squared), radial) for entry in frequency))
    return vector_add(value, vector_scale(-1, correction))


def ordered_symbol(k, ell, a, b):
    return project(frequency_add(k, ell), vector_scale(dot_frequency(ell, a), b))


def polynomial_product(left, right):
    result = defaultdict(int)
    for x, a in left.items():
        for y, b in right.items():
            result[x + y] += a * b
    return {x: a for x, a in result.items() if a}


def a_polynomial(radius):
    return {-radius: 1, radius: -1}


def h_polynomial(radius, multiplier):
    return {
        (2 * index - multiplier + 1) * radius: 1
        for index in range(multiplier)
    }


def selected_factors(radius, multipliers, selected):
    result = {0: 1}
    for index, multiplier in enumerate(multipliers):
        if index in selected:
            result = polynomial_product(result, h_polynomial(radius, multiplier))
        radius *= multiplier
    return result


def add_mode(field, frequency, value):
    field[frequency] = vector_add(field.get(frequency, ZERO_VECTOR), value)
    if field[frequency] == ZERO_VECTOR:
        del field[frequency]


def source_field(radius, y, multipliers, rail_factors):
    indices = set(range(len(multipliers)))
    rail_factors = set(rail_factors)
    assert rail_factors <= indices and indices - rail_factors
    rail = polynomial_product(
        a_polynomial(radius), selected_factors(radius, multipliers, rail_factors)
    )
    pump = selected_factors(radius, multipliers, indices - rail_factors)
    field = {}
    for x, coefficient in rail.items():
        value = vector(0, 0, coefficient)
        add_mode(field, (x, y, 0), value)
        add_mode(field, (-x, -y, 0), value)
    for x, coefficient in pump.items():
        add_mode(field, (x, 0, 0), vector(0, coefficient, 0))
    terminal = radius
    for multiplier in multipliers:
        terminal *= multiplier
    return field, pump, terminal


def receiver_field(terminal, y):
    a_minus, b_minus, a_plus, b_plus = map(poly_variable, range(NVAR))
    field = {
        (-terminal, y, 0): vector(
            poly_scale(y, a_minus), poly_scale(terminal, a_minus), b_minus
        ),
        (terminal, y, 0): vector(
            poly_scale(y, a_plus), poly_scale(-terminal, a_plus), b_plus
        ),
    }
    for frequency, value in tuple(field.items()):
        field[tuple(-entry for entry in frequency)] = value
    return field


def convolution(left, right=None):
    if right is None:
        right = left
    output = {}
    for k, a in left.items():
        for ell, b in right.items():
            frequency = frequency_add(k, ell)
            add_mode(output, frequency, ordered_symbol(k, ell, a, b))
    return output


def sum_outputs(*outputs):
    result = {}
    for output in outputs:
        for frequency, value in output.items():
            add_mode(result, frequency, value)
    return result


def endpoint_formula(terminal, y, pump_endpoint, horizontal_sign, layer_sign):
    receiver = receiver_field(terminal, y)
    receiver_frequency = (
        horizontal_sign * terminal,
        layer_sign * y,
        0,
    )
    pump_frequency = (horizontal_sign * pump_endpoint, 0, 0)
    pump = {pump_frequency: vector(0, 1, 0)}
    pair = sum_outputs(
        convolution({receiver_frequency: receiver[receiver_frequency]}, pump),
        convolution(pump, {receiver_frequency: receiver[receiver_frequency]}),
    )
    return pair[frequency_add(receiver_frequency, pump_frequency)]


def audit(radius, y, multipliers, rail_factors):
    source, pump, terminal = source_field(radius, y, multipliers, rail_factors)
    receiver = receiver_field(terminal, y)
    source_source = convolution(source, source)
    receiver_source = sum_outputs(convolution(source, receiver), convolution(receiver, source))
    receiver_receiver = convolution(receiver, receiver)
    combined = dict(source)
    for frequency, value in receiver.items():
        add_mode(combined, frequency, value)
    full = convolution(combined)
    assert full == sum_outputs(source_source, receiver_source, receiver_receiver)

    expected_source_support = {
        (-terminal, y, 0),
        (terminal, y, 0),
        (-terminal, -y, 0),
        (terminal, -y, 0),
    }
    assert set(source_source) == expected_source_support

    pump_endpoint = max(pump)
    assert 0 < pump_endpoint < terminal
    for horizontal_sign in (-1, 1):
        for layer_sign in (-1, 1):
            endpoint = endpoint_formula(
                terminal, y, pump_endpoint, horizontal_sign, layer_sign
            )
            frequency = (
                horizontal_sign * (terminal + pump_endpoint),
                layer_sign * y,
                0,
            )
            assert receiver_source[frequency] == endpoint

    # At the positive endpoint the unprojected symmetrized vector is
    # (a Y^2, a Y(S-T), b Y). It can project to zero only if b=0 and
    # Y^2=(S-T)(S+T)=S^2-T^2, impossible for 0<S<T and nonzero real Y.
    return {
        "depth": len(multipliers),
        "source_modes": len(source),
        "receiver_modes": len(receiver),
        "ss_outputs": len(source_source),
        "sr_outputs": len(receiver_source),
        "rr_outputs": len(receiver_receiver),
        "full_outputs": len(full),
        "terminal": terminal,
        "pump_endpoint": pump_endpoint,
    }


def main():
    cases = (
        ((2,), ()),
        ((2, 4), (0,)),
        ((2, 4, 2), (0, 2)),
        ((4, 2, 6, 2), (1, 3)),
    )
    print("Cycle 177 receiver-populated full-convolution audit")
    print("depth src recv SS SR RR full terminal pump-end")
    for multipliers, rail_factors in cases:
        result = audit(3, 5, multipliers, rail_factors)
        print(
            result["depth"],
            result["source_modes"],
            result["receiver_modes"],
            result["ss_outputs"],
            result["sr_outputs"],
            result["rr_outputs"],
            result["full_outputs"],
            result["terminal"],
            result["pump_endpoint"],
        )
    print("endpoint equations force all four receiver parameters to zero")
    print("all exact symbolic full-convolution checks passed")


if __name__ == "__main__":
    main()
