#!/usr/bin/env python3
"""Exact full-convolution certificate for the Cycle 175 progression filter."""

from collections import defaultdict
from fractions import Fraction as F


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def scale(c, a):
    return tuple(c * x for x in a)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def norm2(a):
    return dot(a, a)


def project(k, v):
    if norm2(k) == 0:
        return v
    return sub(v, scale(dot(k, v) / norm2(k), k))


def symbol(k, ell, a, b):
    raw = add(scale(dot(a, ell), b), scale(dot(b, k), a))
    return project(add(k, ell), raw)


def ordered_symbol(k, ell, a, b):
    return project(add(k, ell), scale(dot(a, ell), b))


def add_mode(field, k, value):
    field[k] = add(field.get(k, (F(0), F(0), F(0))), value)


def make_field(r, y, m):
    assert r != 0 and y != 0 and m >= 2 and m % 2 == 0
    e2 = (F(0), F(1), F(0))
    e3 = (F(0), F(0), F(1))
    field = {}

    rails = [((-r, y, 0), e3), ((r, y, 0), scale(-1, e3))]
    for k, value in rails:
        add_mode(field, k, value)
        add_mode(field, neg(k), value)

    for j in range(m):
        s = (2 * j - m + 1) * r
        add_mode(field, (s, 0, 0), e2)

    assert all(value != (0, 0, 0) for value in field.values())
    assert all(field.get(neg(k)) == value for k, value in field.items())
    assert all(dot(k, value) == 0 for k, value in field.items())
    return field


def convolution(field):
    output = defaultdict(lambda: (F(0), F(0), F(0)))
    for k, a in field.items():
        for ell, b in field.items():
            q = add(k, ell)
            output[q] = add(output[q], ordered_symbol(k, ell, a, b))
    return {k: value for k, value in output.items() if value != (0, 0, 0)}


def expected_output(r, y, m):
    e3 = (F(0), F(0), F(1))
    return {
        (-m * r, y, 0): scale(y, e3),
        (m * r, y, 0): scale(-y, e3),
        (-m * r, -y, 0): scale(y, e3),
        (m * r, -y, 0): scale(-y, e3),
    }


def verify_block(r, y, m):
    field = make_field(r, y, m)
    output = convolution(field)
    assert output == expected_output(r, y, m)
    assert not set(output).intersection(field)
    return len(field), len(output)


def main():
    rows = []
    for m in (2, 4, 6, 10, 20):
        support, outputs = verify_block(3, 5, m)
        rows.append((m, support, outputs, 2 * (m - 1)))

    r = 1
    multipliers = (2, 4, 2, 6, 2, 8, 2, 10)
    for m in multipliers:
        verify_block(r, 7, m)
        r *= m

    print("Cycle 175 progression collision filter")
    print("m, input support, output support, canceled output frequencies")
    for row in rows:
        print(*row)
    print("sequential multipliers =", multipliers)
    print("terminal radius parameter =", r)
    print("all exact full-convolution checks passed")


if __name__ == "__main__":
    main()
