#!/usr/bin/env python3
"""Exact finite-cutoff Sturm certificates for the SU(2) plaquette matrix."""

import argparse
from fractions import Fraction


def parse_fraction(text):
    try:
        return Fraction(text)
    except (ValueError, ZeroDivisionError) as error:
        raise argparse.ArgumentTypeError(f"not a rational number: {text}") from error


def finite_matrix(coupling, cutoff):
    """Return the rational diagonal and off-diagonal of J_N, N=cutoff."""
    coupling = Fraction(coupling)
    if coupling < 0:
        raise ValueError("lambda must be nonnegative")
    if cutoff < 0:
        raise ValueError("cutoff N must be nonnegative")
    diagonal = tuple(Fraction(n * (n + 2)) + coupling for n in range(cutoff + 1))
    off_diagonal = (coupling / 2,) * cutoff
    return diagonal, off_diagonal


def sturm_polynomials(x, diagonal, off_diagonal):
    """Return det(J_k-xI), k=0,...,N, using exact rational arithmetic."""
    x = Fraction(x)
    previous_previous = Fraction(1)
    previous = diagonal[0] - x
    values = [previous_previous, previous]
    for index in range(1, len(diagonal)):
        current = (
            (diagonal[index] - x) * previous
            - off_diagonal[index - 1] ** 2 * previous_previous
        )
        values.append(current)
        previous_previous, previous = previous, current
    return tuple(values)


def sturm_count(x, diagonal, off_diagonal):
    """Return the number of eigenvalues of the finite matrix strictly below x."""
    if not off_diagonal or all(value == 0 for value in off_diagonal):
        return sum(value < x for value in diagonal)

    signs = []
    for value in sturm_polynomials(x, diagonal, off_diagonal):
        if value:
            signs.append(1 if value > 0 else -1)
    return sum(left != right for left, right in zip(signs, signs[1:]))


def eigenvalue_interval(index, diagonal, off_diagonal, tolerance=Fraction(1, 10**12)):
    """Enclose finite-matrix eigenvalue ``index`` in an exact rational interval."""
    if not 0 <= index < len(diagonal):
        raise ValueError("eigenvalue index is outside the finite matrix")
    tolerance = Fraction(tolerance)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if not off_diagonal or all(value == 0 for value in off_diagonal):
        value = sorted(diagonal)[index]
        return value, value

    radius = 2 * max(off_diagonal, default=Fraction(0))
    lower = min(diagonal) - radius - 1
    upper = max(diagonal) + radius + 1
    while upper - lower > tolerance:
        midpoint = (lower + upper) / 2
        if sturm_count(midpoint, diagonal, off_diagonal) <= index:
            lower = midpoint
        else:
            upper = midpoint
    return lower, upper


def low_spectrum_intervals(coupling, cutoff, tolerance=Fraction(1, 10**12)):
    diagonal, off_diagonal = finite_matrix(coupling, cutoff)
    count = min(3, cutoff + 1)
    return tuple(
        eigenvalue_interval(index, diagonal, off_diagonal, tolerance)
        for index in range(count)
    )


def subtract_intervals(left, right):
    """Enclose x-y for x in left and y in right."""
    return left[0] - right[1], left[1] - right[0]


def format_interval(interval):
    return f"[{interval[0]}, {interval[1]}]"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cutoff", type=int, default=32, help="finite cutoff N")
    parser.add_argument(
        "--tolerance",
        type=parse_fraction,
        default=Fraction(1, 10**12),
        help="positive rational interval width (default: 1/10^12)",
    )
    parser.add_argument(
        "--couplings",
        type=parse_fraction,
        nargs="*",
        default=tuple(map(Fraction, (0, "1/10", 1, 10, 100))),
        help="nonnegative rational lambda values",
    )
    args = parser.parse_args()
    if args.cutoff < 1:
        parser.error("cutoff N must be at least 1")
    if args.tolerance <= 0:
        parser.error("tolerance must be positive")
    if any(coupling < 0 for coupling in args.couplings):
        parser.error("lambda values must be nonnegative")

    print(f"finite matrix J_N: N={args.cutoff}, dimension={args.cutoff + 1}")
    print(f"exact target width: {args.tolerance}")
    for coupling in args.couplings:
        spectrum = low_spectrum_intervals(coupling, args.cutoff, args.tolerance)
        gap = subtract_intervals(spectrum[1], spectrum[0])
        print(f"lambda={coupling}")
        print(f"  E0(J_N) in {format_interval(spectrum[0])}")
        print(f"  E1(J_N) in {format_interval(spectrum[1])}")
        print(f"  gap(J_N) in {format_interval(gap)}")


if __name__ == "__main__":
    main()
