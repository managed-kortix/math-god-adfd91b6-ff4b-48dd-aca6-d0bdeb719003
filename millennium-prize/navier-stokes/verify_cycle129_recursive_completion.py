#!/usr/bin/env python3
"""Exact recursive Fourier-completion verifier for Cycle 129 (stdlib only)."""

from fractions import Fraction as F


ZERO_MODE = (0, 0, 0)


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
            result[mode] = vadd(result.get(mode, ZERO_VECTOR), project(mode, raw))
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


def exterior(field, support):
    return {mode: value for mode, value in field.items() if mode not in support}


def radial_norm_data(field):
    data = {}
    for mode, value in field.items():
        radius2 = wave_norm2(mode)
        data[radius2] = data.get(radius2, F(0)) + norm2(value)
    return dict(sorted(data.items()))


def format_fraction(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def format_radial_data(data):
    return ", ".join(
        f"|n|^2={radius2}:{format_fraction(value)}"
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
    for power in range(3):
        coefficient = quadratic_coefficient(generations, power)
        coefficients.append(coefficient)
        new_generation = exterior(coefficient, supports[-1])
        require(new_generation, f"generation {power + 1} is empty")
        require(not (set(new_generation) & supports[-1]),
                f"generation {power + 1} overlaps earlier support")
        check_field(coefficient, f"quadratic coefficient epsilon^{power}")
        check_field(new_generation, f"generation {power + 1}")
        generations.append(new_generation)
        supports.append(supports[-1] | set(new_generation))

    for left in range(len(generations)):
        for right in range(left):
            require(set(generations[left]).isdisjoint(generations[right]),
                    f"generations {right} and {left} are not disjoint")

    for completed_depth, support in enumerate(supports):
        for power in range(completed_depth):
            require(not exterior(coefficients[power], support),
                    f"depth {completed_depth} leaks below epsilon^{completed_depth}")

    leading_leak = exterior(quadratic_coefficient(generations, 3), supports[3])
    require(leading_leak, "depth-three completion has no epsilon^3 leading leak")
    check_field(leading_leak, "epsilon^3 leading leak")

    q0 = coefficients[0]
    core_flux_by_radius = {}
    for mode, value in core.items():
        pairing = vdot(vconj(value), q0.get(mode, ZERO_VECTOR))
        require(pairing[1] == 0, "core flux pairing is not real")
        radius2 = wave_norm2(mode)
        core_flux_by_radius[radius2] = (
            core_flux_by_radius.get(radius2, F(0)) + 2 * pairing[0]
        )
    core_flux_by_radius = {
        radius2: value for radius2, value in core_flux_by_radius.items() if value
    }
    require(core_flux_by_radius == {1: F(-8), 2: F(8)},
            "Cycle 113 core flux coefficients changed")
    require(core_flux_by_radius[2] == -core_flux_by_radius[1] > 0,
            "the exact core critical flux is not 8(sqrt(2)-1) > 0")

    sizes = [len(generation) for generation in generations]
    cumulative_sizes = [len(support) for support in supports]
    print("Cycle 129 recursive exact Fourier completion through r=3")
    print("generation support sizes G_0..G_3 =", sizes)
    print("cumulative support sizes S_0..S_3 =", cumulative_sizes)
    print("supports are pairwise disjoint, symmetric, real, and divergence-free")
    print("depth r has no exterior coefficients below epsilon^r: r=0,1,2,3")
    print("core critical flux = 8(sqrt(2)-1) > 0")
    print("leading exterior order after S_3 = epsilon^3")
    print("leading leak support size =", len(leading_leak))
    print("leading leak radial squared-norm data =",
          format_radial_data(radial_norm_data(leading_leak)))
    print("all exact checks passed")


if __name__ == "__main__":
    main()
