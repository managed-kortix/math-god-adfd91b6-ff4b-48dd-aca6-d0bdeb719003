#!/usr/bin/env python3
"""Exact 16-case certificate for signed odd-girth-at-least-nine thetas.

The three path lengths are parameterized by X=z^(2a), Y=z^(2b), and
W=z^(2c).  This keeps both the path denominators and their alternating
signed amplitudes polynomial while enforcing that the companion is no
shorter than the path of the same parity.
"""

from collections import deque
from dataclasses import dataclass
from itertools import product
from math import comb

import sympy as sp


z, t, X, Y, W = sp.symbols("z t X Y W")
VARIABLES = (t, X, Y, W)
CAP = sp.Rational(3, 4)
RESIDUE_PAIRS = ((1, 4), (3, 2))
ALLOCATIONS = ("odd", "even")
DOUBLED_PARITIES = ("odd", "even")
DISPLACEMENTS = (0, 2)


@dataclass(frozen=True)
class State:
    d: sp.Expr
    h: sp.Expr
    amplitude: sp.Expr


@dataclass(frozen=True)
class Case:
    odd_residue: int
    even_residue: int
    allocation: str
    doubled_parity: str
    displacement: int

    @property
    def odd_delta(self):
        return 4 if self.allocation == "odd" else 0

    @property
    def even_delta(self):
        return 4 if self.allocation == "even" else 0


def odd_state(residue, delta, U):
    """State of length residue+delta+4k when U=z^(2k)."""
    base = residue + delta
    assert residue in (1, 3) and base % 2 == 1 and base > 0
    return State(
        d=1 + z**base * U**2,
        h=1 - z**(base - 1) * U**2,
        amplitude=(-1) ** ((base - 1) // 2) * z**((base - 1) // 2) * U,
    )


def even_state(residue, delta, U):
    """State of length residue+delta+4k when U=z^(2k)."""
    base = residue + delta
    assert residue in (2, 4) and base % 2 == 0 and base >= 2
    return State(
        d=1 - z**base * U**2,
        h=1 + z**(base - 1) * U**2,
        amplitude=(-1) ** (base // 2) * z**(base // 2 - 1) * U,
    )


def states_for_case(case):
    odd = odd_state(case.odd_residue, case.odd_delta, X)
    even = even_state(case.even_residue, case.even_delta, Y)
    if case.doubled_parity == "odd":
        companion = odd_state(
            case.odd_residue, case.odd_delta + case.displacement, X * W
        )
        return (odd, companion), (even,)
    companion = even_state(
        case.even_residue, case.even_delta + case.displacement, Y * W
    )
    return (odd,), (even, companion)


def carrier(case):
    """Construct F,N,P,Q,R,S,K without rational-function cancellation."""
    odd_states, even_states = states_for_case(case)
    states = odd_states + even_states
    F = sp.prod(state.d for state in states)
    complements = [
        sp.prod(other.d for j, other in enumerate(states) if j != i)
        for i in range(3)
    ]
    N = (1 - z) * F + z * sum(
        state.h * complement for state, complement in zip(states, complements)
    )
    P = sum(
        state.amplitude * complements[i] for i, state in enumerate(odd_states)
    )
    offset = len(odd_states)
    Q = sum(
        state.amplitude * complements[offset + i]
        for i, state in enumerate(even_states)
    )
    c = z * (1 + z) ** 2
    R = N**2 + c * (P**2 - z * Q**2)
    S = 2 * c * P * Q
    K = 4 * z**4 * R - S
    return tuple(map(sp.expand, (F, N, P, Q, R, S, K)))


def concrete_carrier(lengths):
    d = [1 - (-z) ** length for length in lengths]
    h = [1 - (-z) ** (length - 1) for length in lengths]
    F = sp.prod(d)
    complements = [
        sp.prod(other for j, other in enumerate(d) if j != i)
        for i in range(3)
    ]
    N = (1 - z) * F + z * sum(
        value * complement for value, complement in zip(h, complements)
    )
    P = sum(
        (-1) ** ((length - 1) // 2) * z ** ((length - 1) // 2) * complements[i]
        for i, length in enumerate(lengths) if length % 2
    )
    Q = sum(
        (-1) ** (length // 2) * z ** (length // 2 - 1) * complements[i]
        for i, length in enumerate(lengths) if length % 2 == 0
    )
    c = z * (1 + z) ** 2
    R = N**2 + c * (P**2 - z * Q**2)
    S = 2 * c * P * Q
    return tuple(map(sp.expand, (F, N, P, Q, R, S, 4 * z**4 * R - S)))


def sample_lengths(case, a, b, companion_k):
    odd = case.odd_residue + case.odd_delta + 4 * a
    even = case.even_residue + case.even_delta + 4 * b
    if case.doubled_parity == "odd":
        return (odd, odd + case.displacement + 4 * companion_k, even)
    return (odd, even, even + case.displacement + 4 * companion_k)


def verify_integer_samples(case, symbolic):
    for a, b, companion_k in ((0, 0, 0), (1, 2, 1), (3, 1, 2)):
        substitution = {
            X: z ** (2 * a),
            Y: z ** (2 * b),
            W: z ** (2 * companion_k),
        }
        reconstructed = concrete_carrier(
            sample_lengths(case, a, b, companion_k)
        )
        assert all(
            sp.expand(expression.subs(substitution) - concrete) == 0
            for expression, concrete in zip(symbolic, reconstructed)
        )


def power_to_tensor_bernstein(poly):
    """Convert a polynomial to its exact tensor Bernstein control net."""
    power = sp.Poly(sp.expand(poly), *VARIABLES)
    degrees = tuple(power.degree(variable) for variable in VARIABLES)
    coefficients = {monomial: coefficient for monomial, coefficient in power.terms()}
    for axis, degree in enumerate(degrees):
        grouped = {}
        for index, coefficient in coefficients.items():
            key = index[:axis] + index[axis + 1 :]
            grouped.setdefault(key, {})[index[axis]] = coefficient
        converted = {}
        for key, values in grouped.items():
            for i in range(degree + 1):
                value = sum(
                    values.get(j, 0) * sp.Rational(comb(i, j), comb(degree, j))
                    for j in range(i + 1)
                )
                index = key[:axis] + (i,) + key[axis:]
                converted[index] = value
        coefficients = converted
    expected_size = sp.prod(degree + 1 for degree in degrees)
    assert len(coefficients) == expected_size
    assert tensor_bernstein_to_power(coefficients, degrees) == power.as_dict()
    return degrees, coefficients


def tensor_bernstein_to_power(coefficients, degrees):
    """Invert a tensor control net coefficient-wise, without symbolic bases."""
    converted = coefficients
    for axis, degree in enumerate(degrees):
        grouped = {}
        for index, coefficient in converted.items():
            key = index[:axis] + index[axis + 1 :]
            grouped.setdefault(key, {})[index[axis]] = coefficient
        power = {}
        for key, values in grouped.items():
            for j in range(degree + 1):
                value = comb(degree, j) * sum(
                    (-1) ** (j - i) * comb(j, i) * values.get(i, 0)
                    for i in range(j + 1)
                )
                if value:
                    index = key[:axis] + (j,) + key[axis:]
                    power[index] = sp.factor(value)
        converted = power
    return converted


def split_control_net(coefficients, degrees, axis):
    """Bisect one coordinate at 1/2 by exact de Casteljau subdivision."""
    fibers = {}
    for index, coefficient in coefficients.items():
        key = index[:axis] + index[axis + 1 :]
        fibers.setdefault(key, [None] * (degrees[axis] + 1))[index[axis]] = coefficient
    left_net, right_net = {}, {}
    for key, values in fibers.items():
        levels = values
        left = [levels[0]]
        right = [levels[-1]]
        while len(levels) > 1:
            levels = [(levels[i] + levels[i + 1]) / 2 for i in range(len(levels) - 1)]
            left.append(levels[0])
            right.append(levels[-1])
        right.reverse()
        for i in range(degrees[axis] + 1):
            index = key[:axis] + (i,) + key[axis:]
            left_net[index] = left[i]
            right_net[index] = right[i]
    return left_net, right_net


def choose_split_axis(coefficients, degrees):
    scores = []
    for axis, degree in enumerate(degrees):
        if degree == 0:
            scores.append(sp.Integer(-1))
            continue
        score = max(
            abs(value - coefficients[index[:axis] + (index[axis] + 1,) + index[axis + 1 :]])
            for index, value in coefficients.items() if index[axis] < degree
        )
        scores.append(score)
    return max(range(len(degrees)), key=lambda axis: scores[axis])


def certify_tensor(poly, max_depth=24, max_boxes=200000):
    """Certify nonnegativity, adaptively bisecting inconclusive boxes."""
    degrees, root = power_to_tensor_bernstein(poly)
    queue = deque([(root, 0)])
    leaves = 0
    splits = 0
    deepest = 0
    certified_min = None
    while queue:
        coefficients, depth = queue.popleft()
        lower = min(coefficients.values())
        if lower >= 0:
            leaves += 1
            deepest = max(deepest, depth)
            certified_min = lower if certified_min is None else min(certified_min, lower)
            continue
        if depth >= max_depth:
            raise AssertionError(f"Bernstein depth limit {max_depth}; lower={lower}")
        if leaves + len(queue) + 2 > max_boxes:
            raise AssertionError(f"Bernstein box limit {max_boxes}")
        axis = choose_split_axis(coefficients, degrees)
        left, right = split_control_net(coefficients, degrees, axis)
        queue.append((left, depth + 1))
        queue.append((right, depth + 1))
        splits += 1
    return degrees, leaves, splits, deepest, certified_min


def verify_subdivision_engine():
    """Exercise the adaptive path on a nonnegative but inconclusive control net."""
    degrees, leaves, splits, depth, lower = certify_tensor((t - sp.Rational(1, 2)) ** 2)
    assert degrees == (2, 0, 0, 0)
    assert (leaves, splits, depth, lower) == (2, 1, 1, 0)


def cases():
    return [
        Case(odd, even, allocation, doubled, displacement)
        for (odd, even), allocation, doubled, displacement in product(
            RESIDUE_PAIRS, ALLOCATIONS, DOUBLED_PARITIES, DISPLACEMENTS
        )
    ]


def case_label(case):
    displacement = "+4k" if case.displacement == 0 else "+2+4k"
    return (
        f"({case.odd_residue},{case.even_residue}) "
        f"alloc={case.allocation} double={case.doubled_parity} companion={displacement}"
    )


def main():
    all_cases = cases()
    assert len(all_cases) == 16
    verify_subdivision_engine()
    print("case degrees leaves splits depth certified-min")
    total_splits = 0
    for case in all_cases:
        symbolic = carrier(case)
        verify_integer_samples(case, symbolic)
        K = symbolic[-1]
        transformed = sp.expand(K.subs(z, CAP * t) / t**4)
        assert sp.expand(t**4 * transformed - K.subs(z, CAP * t)) == 0
        degrees, leaves, splits, depth, lower = certify_tensor(transformed)
        total_splits += splits
        print(case_label(case), degrees, leaves, splits, depth, lower)
    print(
        "theta g>=9 signed opposite-residue certificate: "
        f"PASS (16/16 cases; adaptive-splits={total_splits})"
    )


if __name__ == "__main__":
    main()
