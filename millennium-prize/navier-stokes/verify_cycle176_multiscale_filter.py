#!/usr/bin/env python3
"""Exact full-convolution certificate for the Cycle 176 multiscale filter."""

from collections import defaultdict
from fractions import Fraction as F


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def project(k, v):
    norm2 = dot(k, k)
    if norm2 == 0:
        return v
    return sub(v, scale(dot(k, v) / norm2, k))


def ordered_symbol(k, ell, a, b):
    return project(add(k, ell), scale(dot(a, ell), b))


def polynomial_product(left, right):
    result = defaultdict(int)
    for x, a in left.items():
        for y, b in right.items():
            result[x + y] += a * b
    return {x: a for x, a in result.items() if a}


def a_polynomial(r):
    return {-r: 1, r: -1}


def h_polynomial(r, m):
    return {(2 * j - m + 1) * r: 1 for j in range(m)}


def factors(r, multipliers, selected):
    result = {0: 1}
    radius = r
    for index, m in enumerate(multipliers):
        if index in selected:
            result = polynomial_product(result, h_polynomial(radius, m))
        radius *= m
    return result


def add_mode(field, k, value):
    field[k] = add(field.get(k, (F(0), F(0), F(0))), value)


def make_field(r, y, multipliers, rail_factors):
    indices = set(range(len(multipliers)))
    rail_factors = set(rail_factors)
    assert rail_factors <= indices
    assert indices - rail_factors
    assert r != 0 and y != 0
    assert all(m >= 2 and m % 2 == 0 for m in multipliers)

    rail = polynomial_product(a_polynomial(r), factors(r, multipliers, rail_factors))
    pump = factors(r, multipliers, indices - rail_factors)
    assert all(rail.get(-x) == -coefficient for x, coefficient in rail.items())
    assert all(pump.get(-x) == coefficient for x, coefficient in pump.items())
    assert 0 not in pump

    e2 = (F(0), F(1), F(0))
    e3 = (F(0), F(0), F(1))
    field = {}
    for x, coefficient in rail.items():
        value = scale(F(coefficient), e3)
        add_mode(field, (x, y, 0), value)
        add_mode(field, (-x, -y, 0), value)
    for x, coefficient in pump.items():
        add_mode(field, (x, 0, 0), scale(F(coefficient), e2))

    assert all(value != (0, 0, 0) for value in field.values())
    assert all(field.get(neg(k)) == value for k, value in field.items())
    assert all(dot(k, value) == 0 for k, value in field.items())
    return field, rail, pump


def convolution(field):
    output = defaultdict(lambda: (F(0), F(0), F(0)))
    for k, a in field.items():
        for ell, b in field.items():
            q = add(k, ell)
            output[q] = add(output[q], ordered_symbol(k, ell, a, b))
    return {k: value for k, value in output.items() if value != (0, 0, 0)}


def verify(r, y, multipliers, rail_factors):
    field, rail, pump = make_field(r, y, multipliers, rail_factors)
    terminal = r
    for m in multipliers:
        terminal *= m
    product = polynomial_product(rail, pump)
    assert product == a_polynomial(terminal)

    e3 = (F(0), F(0), F(1))
    expected = {
        (-terminal, y, 0): scale(F(y), e3),
        (terminal, y, 0): scale(F(-y), e3),
        (-terminal, -y, 0): scale(F(y), e3),
        (terminal, -y, 0): scale(F(-y), e3),
    }
    assert convolution(field) == expected
    return len(field), len(rail), len(pump), terminal


def main():
    cases = (
        ((2,), ()),
        ((2, 4), (0,)),
        ((2, 4, 2, 6), (0, 2)),
        ((4, 2, 6, 2, 4), (1, 3)),
        ((2, 2, 2, 2, 2, 2, 2, 2), (0, 2, 4, 6)),
    )
    print("Cycle 176 simultaneous multiscale Laurent filter")
    print("depth, field support, rail support, pump support, terminal radius")
    for multipliers, rail_factors in cases:
        support, rails, pumps, terminal = verify(3, 5, multipliers, rail_factors)
        print(len(multipliers), support, rails, pumps, terminal)
    print("all exact complete-convolution checks passed")


if __name__ == "__main__":
    main()
