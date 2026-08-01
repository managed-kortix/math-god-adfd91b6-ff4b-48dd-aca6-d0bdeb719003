#!/usr/bin/env python3
"""Certify Ritz gaps of supplied SU(2) shared-link cutoff matrices."""

import argparse
from fractions import Fraction


def trim(polynomial):
    values = list(map(Fraction, polynomial))
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def add(left, right):
    size = max(len(left), len(right))
    return trim(
        tuple(
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
            for index in range(size)
        )
    )


def scale(polynomial, scalar):
    return trim(tuple(Fraction(scalar) * value for value in polynomial))


def multiply(left, right):
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return trim(result)


def derivative(polynomial):
    if len(polynomial) == 1:
        return (Fraction(0),)
    return tuple(index * polynomial[index] for index in range(1, len(polynomial)))


def divide_remainder(dividend, divisor):
    remainder = list(trim(dividend))
    divisor = trim(divisor)
    if divisor == (0,):
        raise ZeroDivisionError("zero polynomial")
    while len(remainder) >= len(divisor) and any(remainder):
        shift = len(remainder) - len(divisor)
        factor = remainder[-1] / divisor[-1]
        for index, value in enumerate(divisor):
            remainder[index + shift] -= factor * value
        remainder = list(trim(remainder))
    return tuple(remainder)


def evaluate(polynomial, point):
    result = Fraction(0)
    for coefficient in reversed(polynomial):
        result = result * Fraction(point) + coefficient
    return result


def sturm_sequence(polynomial):
    sequence = [trim(polynomial), trim(derivative(polynomial))]
    while sequence[-1] != (0,):
        remainder = divide_remainder(sequence[-2], sequence[-1])
        if remainder == (0,):
            break
        sequence.append(scale(remainder, -1))
    return tuple(sequence)


def sign_variations(values):
    signs = [1 if value > 0 else -1 for value in values if value]
    return sum(left != right for left, right in zip(signs, signs[1:]))


def roots_below(point, sequence, lower_bound=Fraction(-1)):
    return sign_variations(evaluate(item, lower_bound) for item in sequence) - sign_variations(
        evaluate(item, point) for item in sequence
    )


def linear(diagonal):
    """Return diagonal-x in ascending powers of x."""
    return Fraction(diagonal), Fraction(-1)


def shared_symmetric_polynomial(coupling):
    """Characteristic polynomial of the exchange-symmetric four-state block."""
    coupling = Fraction(coupling)
    d0 = linear(2 * coupling)
    d1 = linear(3 + 2 * coupling)
    d2 = linear(Fraction(9, 2) + 2 * coupling)
    d3 = linear(Fraction(13, 2) + 2 * coupling)
    polynomial = multiply(multiply(d0, d1), multiply(d2, d3))
    polynomial = add(polynomial, scale(multiply(d2, d3), -(coupling**2) / 2))
    polynomial = add(polynomial, scale(multiply(d0, d3), -(coupling**2) / 8))
    polynomial = add(polynomial, scale(multiply(d0, d2), -3 * (coupling**2) / 8))
    return trim(polynomial)


def shared_count_below(point, coupling):
    coupling = Fraction(coupling)
    sequence = sturm_sequence(shared_symmetric_polynomial(coupling))
    count = roots_below(Fraction(point), sequence)
    return count + int(3 + 2 * coupling < point)


def shared_eigenvalue_interval(index, coupling, tolerance):
    coupling = Fraction(coupling)
    tolerance = Fraction(tolerance)
    if not 0 <= index < 5:
        raise ValueError("shared-block eigenvalue index must be in [0,4]")
    if coupling < 0 or tolerance <= 0:
        raise ValueError("coupling and tolerance must be nonnegative and positive")
    lower = Fraction(-1)
    upper = Fraction(10) + 4 * coupling
    while upper - lower > tolerance:
        midpoint = (lower + upper) / 2
        if shared_count_below(midpoint, coupling) <= index:
            lower = midpoint
        else:
            upper = midpoint
    return lower, upper


def square_root_interval(value, tolerance):
    value = Fraction(value)
    tolerance = Fraction(tolerance)
    lower, upper = Fraction(0), max(Fraction(1), value)
    while upper - lower > tolerance:
        midpoint = (lower + upper) / 2
        if midpoint * midpoint <= value:
            lower = midpoint
        else:
            upper = midpoint
    return lower, upper


def subtract_intervals(left, right):
    return left[0] - right[1], left[1] - right[0]


def format_interval(interval):
    return f"[{interval[0]}, {interval[1]}]"


def parse_fraction(text):
    try:
        return Fraction(text)
    except (ValueError, ZeroDivisionError) as error:
        raise argparse.ArgumentTypeError(f"not a rational number: {text}") from error


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--coupling", type=parse_fraction, default=Fraction(1))
    parser.add_argument("--tolerance", type=parse_fraction, default=Fraction(1, 10**12))
    args = parser.parse_args()
    if args.coupling < 0:
        parser.error("coupling must be nonnegative")
    if args.tolerance <= 0:
        parser.error("tolerance must be positive")

    shared = tuple(
        shared_eigenvalue_interval(index, args.coupling, args.tolerance) for index in range(2)
    )
    shared_gap = subtract_intervals(shared[1], shared[0])
    product_gap = square_root_interval(9 + args.coupling**2, args.tolerance)
    print(f"lambda={args.coupling}")
    print("shared-link natural spin cutoff j,k <= 1/2 (dimension 5)")
    print(f"  characteristic polynomial: {shared_symmetric_polynomial(args.coupling)}")
    print(f"  E0 in {format_interval(shared[0])}")
    print(f"  E1 in {format_interval(shared[1])}")
    print(f"  Ritz gap in {format_interval(shared_gap)}")
    print("tensor sum of one-plaquette n <= 1 compressions (dimension 4)")
    print(f"  cutoff Ritz gap=sqrt(9+lambda^2) in {format_interval(product_gap)}")
    print(f"  disjoint cutoff Ritz-gap intervals: {shared_gap[1] < product_gap[0]}")


if __name__ == "__main__":
    main()
