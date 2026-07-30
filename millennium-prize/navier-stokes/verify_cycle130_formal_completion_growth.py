#!/usr/bin/env python3
"""Exact formal-completion growth verifier for Cycle 130 (stdlib only)."""

from fractions import Fraction as F
from math import factorial, sqrt


ZERO_MODE = (0, 0, 0)
MAX_DEPTH = 8


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def z(real=0, imag=0):
    return (F(real), F(imag))


def cadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


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
    return sum(coordinate * coordinate for coordinate in k)


def hex_radius(k):
    require(k[2] == 0, f"mode {k} left the planar packet")
    return max(abs(k[0]), abs(k[1]), abs(k[0] - k[1]))


def negate_wave(k):
    return tuple(-coordinate for coordinate in k)


def project(k, value):
    denominator = wave_norm2(k)
    require(denominator, "attempted Leray projection at zero frequency")
    contraction = z()
    for coordinate, component in zip(k, value):
        contraction = cadd(contraction, cscale(component, coordinate))
    return tuple(
        cadd(component, cscale(contraction, F(-coordinate, denominator)))
        for coordinate, component in zip(k, value)
    )


def merge_fields(*fields):
    result = {}
    for field in fields:
        for mode, value in field.items():
            result[mode] = vadd(result.get(mode, ZERO_VECTOR), value)
    return {mode: value for mode, value in result.items() if norm2(value)}


def convolution(left, right):
    """Return -i P_n sum_(a+b=n) (left_a.b) right_b."""
    result = {}
    for a, left_value in left.items():
        for b, right_value in right.items():
            mode = tuple(x + y for x, y in zip(a, b))
            if mode == ZERO_MODE:
                continue
            contraction = z()
            for component, coordinate in zip(left_value, b):
                contraction = cadd(contraction, cscale(component, coordinate))
            raw = tuple(cmul(z(0, -1), cmul(contraction, component))
                        for component in right_value)
            projected = project(mode, raw)
            result[mode] = vadd(result.get(mode, ZERO_VECTOR), projected)
    return {mode: value for mode, value in result.items() if norm2(value)}


def quadratic_coefficient(generations, power):
    return merge_fields(*(
        convolution(generations[left], generations[power - left])
        for left in range(power + 1)
    ))


def add_reality_partners(positive_modes):
    field = dict(positive_modes)
    for mode, value in positive_modes.items():
        partner = negate_wave(mode)
        require(partner not in field, "duplicate reality partner")
        field[partner] = vconj(value)
    return field


def exterior(field, support):
    return {mode: value for mode, value in field.items() if mode not in support}


def check_field(field, name):
    require(ZERO_MODE not in field, f"{name} contains the zero mode")
    for mode, value in field.items():
        partner = negate_wave(mode)
        require(partner in field, f"{name} is missing the partner of {mode}")
        require(field[partner] == vconj(value),
                f"{name} violates Fourier reality at {mode}")
        divergence = z()
        for coordinate, component in zip(mode, value):
            divergence = cadd(divergence, cscale(component, coordinate))
        require(divergence == z(), f"{name} is not divergence-free at {mode}")


def check_parity(field, name):
    for mode, value in field.items():
        odd = (mode[0] + mode[1]) % 2
        for real, imag in value:
            if odd:
                require(imag == 0,
                        f"{name} violates odd-real parity at {mode}")
            else:
                require(real == 0,
                        f"{name} violates even-imaginary parity at {mode}")


def radial_norm_data(field):
    data = {}
    for mode, value in field.items():
        radius2 = wave_norm2(mode)
        data[radius2] = data.get(radius2, F(0)) + norm2(value)
    return dict(sorted(data.items()))


def hhalf_norm(radial_data):
    squared = sum(sqrt(radius2) * float(value)
                  for radius2, value in radial_data.items())
    return sqrt(squared)


def format_fraction(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def format_radial_data(data):
    return ", ".join(
        f"{radius2}:{format_fraction(value)}"
        for radius2, value in data.items()
    )


def main():
    core = add_reality_partners({
        (1, 0, 0): vector((0, 0), (1, 0), (1, 0)),
        (0, 1, 0): vector((1, 0), (0, 0), (1, 0)),
        (1, 1, 0): vector((0, -1), (0, 1), (0, -1)),
    })
    generations = [core]
    supports = [set(core)]
    coefficients = []

    check_field(core, "generation 0")
    check_parity(core, "generation 0")
    require(max(hex_radius(mode) for mode in core) <= 1,
            "generation 0 exceeds its hexagonal radius")

    for power in range(MAX_DEPTH):
        coefficient = quadratic_coefficient(generations, power)
        coefficients.append(coefficient)
        check_field(coefficient, f"quadratic coefficient epsilon^{power}")
        check_parity(coefficient, f"quadratic coefficient epsilon^{power}")

        new_generation = exterior(coefficient, supports[-1])
        require(new_generation, f"generation {power + 1} is empty")
        require(set(new_generation).isdisjoint(supports[-1]),
                f"generation {power + 1} overlaps earlier support")
        check_field(new_generation, f"generation {power + 1}")
        check_parity(new_generation, f"generation {power + 1}")
        require(max(hex_radius(mode) for mode in new_generation) <= power + 2,
                f"generation {power + 1} exceeds hexagonal radius {power + 2}")

        generations.append(new_generation)
        supports.append(supports[-1] | set(new_generation))

    for left in range(len(generations)):
        for right in range(left):
            require(set(generations[left]).isdisjoint(generations[right]),
                    f"generations {right} and {left} overlap")

    for power, coefficient in enumerate(coefficients):
        require(set(coefficient) <= supports[power + 1],
                f"formal coefficient epsilon^{power} is not closed in "
                f"S_{power + 1}")
        require(not exterior(coefficient, supports[-1]),
                f"formal coefficient epsilon^{power} leaks outside S_8")

    sizes = [len(generation) for generation in generations]
    cumulative_sizes = [len(support) for support in supports]
    require(sizes == [6, 4, 14, 24, 28, 34, 40, 46, 52],
            f"generation support sizes changed: {sizes}")
    require(cumulative_sizes == [6, 10, 24, 48, 76, 110, 150, 196, 248],
            f"cumulative support sizes changed: {cumulative_sizes}")

    norms = []
    print("Cycle 130 exact formal completion growth through depth 8")
    print("generation support sizes G_0..G_8 =", sizes)
    print("cumulative support sizes S_0..S_8 =", cumulative_sizes)
    print("verified: reality, incompressibility, parity, disjoint support")
    print("verified: supp Q_j subset S_(j+1) for j=0..7")
    print("verified: hex radius max(|n1|,|n2|,|n1-n2|) <= j+1 on G_j")
    print("exact radial squared-L2 groups are |n|^2:sum |V_j(n)|^2")
    for depth, generation in enumerate(generations):
        radial_data = radial_norm_data(generation)
        norm = hhalf_norm(radial_data)
        norms.append(norm)
        print(f"G_{depth} radial groups = {format_radial_data(radial_data)}")
        print(f"G_{depth} ||V_j||_Hhalf ~= {norm:.12g}")

    print("growth diagnostics (numerical display, not a proof):")
    for depth, norm in enumerate(norms):
        ratio = "-" if depth == 0 else f"{norm / norms[depth - 1]:.9g}"
        factorial_scale = norm / factorial(depth)
        root = "-" if depth == 0 else f"{norm ** (1.0 / depth):.9g}"
        print(f"j={depth}: norm={norm:.9g}, ratio={ratio}, "
              f"norm/j!={factorial_scale:.9g}, jth-root={root}")
    print("ratios are consistent with factorial-like growth but do not prove it")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
