#!/usr/bin/env python3
"""Exact certificate for a P|A_7|P two-pivot winding obstruction."""

import sympy as sp


def add_cycle(edges, cycle):
    for left, right in zip(cycle, cycle[1:] + cycle[:1]):
        edges.add(tuple(sorted((left, right))))


def main():
    x = sp.symbols("x")
    t = sp.symbols("t", real=True)
    triangles = [
        (0, 1, 2),
        (0, 3, 4),
        (3, 5, 6),
        (5, 7, 8),
        (3, 9, 10),
        (6, 11, 12),
        (12, 17, 18),
    ]
    pentagons = [(0, 13, 14, 15, 16), (18, 19, 20, 21, 22)]
    edges = set()
    for cycle in triangles + pentagons:
        add_cycle(edges, cycle)

    order = 23
    adjacency = sp.zeros(order)
    for left, right in edges:
        adjacency[left, right] = 1
        adjacency[right, left] = 1

    polynomial = sp.Poly(adjacency.charpoly(x).as_expr(), x)
    residual_expected = (
        x**13
        - 4 * x**12
        - 15 * x**11
        + 64 * x**10
        + 83 * x**9
        - 370 * x**8
        - 212 * x**7
        + 924 * x**6
        + 257 * x**5
        - 896 * x**4
        - 153 * x**3
        + 164 * x**2
        + 43 * x
        + 2
    )
    factor = (x - 1) * (x + 1) ** 3 * (x**2 - 3) * (x**2 + x - 1) ** 2
    assert polynomial.as_expr() == sp.expand(factor * residual_expected)

    normalized = sp.expand(sp.I ** (-order) * polynomial.as_expr().subs(x, sp.I * t))
    real_part = sp.expand(sp.re(normalized))
    imaginary_part = sp.expand(sp.im(normalized))
    expected_real = (
        t**23
        + 31 * t**21
        + 394 * t**19
        + 2640 * t**17
        + 10055 * t**15
        + 21899 * t**13
        + 25637 * t**11
        + 12713 * t**9
        - 1296 * t**7
        - 3522 * t**5
        - 1159 * t**3
        - 129 * t
    )
    expected_imaginary = -(
        14 * t**20
        + 320 * t**18
        + 2928 * t**16
        + 13908 * t**14
        + 37286 * t**12
        + 57480 * t**10
        + 50042 * t**8
        + 23608 * t**6
        + 5512 * t**4
        + 460 * t**2
        - 6
    )
    assert real_part == expected_real
    assert imaginary_part == expected_imaginary

    residual_polynomial = sp.Poly(residual_expected, x)
    root_bound = 1 + max(abs(coefficient) for coefficient in residual_polynomial.all_coeffs()[1:])
    residual_negative = residual_polynomial.count_roots(-root_bound, 0)
    residual_positive = residual_polynomial.count_roots(0, root_bound)
    assert (residual_positive, residual_negative) == (6, 7)

    inertia = (residual_positive + 4, residual_negative + 6, 0)
    assert inertia == (10, 13, 0)

    print(f"vertices={order}, edges={len(edges)}")
    print(f"inertia={inertia}")
    print("R(t)=-129t+O(t^3) and I(t)=6+O(t^2) at zero")
    print("continuous phase limit=(pi/2)(10-13)=-3pi/2")
    print("principal phase limit=+pi/2, so the lift differs by -2pi")


if __name__ == "__main__":
    main()
