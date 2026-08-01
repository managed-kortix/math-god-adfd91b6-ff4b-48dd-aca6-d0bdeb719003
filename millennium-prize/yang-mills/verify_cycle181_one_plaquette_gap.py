#!/usr/bin/env python3
"""Exact half-line and finite-cutoff certificates for the SU(2) plaquette."""

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


def tail_resolvent_bounds(x, coupling, cutoff):
    """Bound <e_(N+1),(T_N-x)^-1 e_(N+1)> by rational numbers."""
    coupling = Fraction(coupling)
    x = Fraction(x)
    if coupling < 0:
        raise ValueError("lambda must be nonnegative")
    if cutoff < 0:
        raise ValueError("cutoff N must be nonnegative")

    first = cutoff + 1
    first_diagonal = Fraction(first * (first + 2)) + coupling
    tail_floor = Fraction(first * (first + 2))
    if x >= tail_floor:
        raise ValueError("spectral parameter must lie below the tail floor")
    return Fraction(1, first_diagonal - x), Fraction(1, tail_floor - x)


def half_line_count_bounds(x, coupling, cutoff):
    """Enclose the number of half-line eigenvalues strictly below x."""
    coupling = Fraction(coupling)
    diagonal, off_diagonal = finite_matrix(coupling, cutoff)
    if coupling == 0:
        count = sturm_count(Fraction(x), diagonal, off_diagonal)
        return count, count

    resolvent_lower, resolvent_upper = tail_resolvent_bounds(x, coupling, cutoff)
    boundary_square = (coupling / 2) ** 2

    def schur_count(resolvent_bound):
        adjusted = list(diagonal)
        adjusted[-1] -= boundary_square * resolvent_bound
        return sturm_count(Fraction(x), tuple(adjusted), off_diagonal)

    return schur_count(resolvent_lower), schur_count(resolvent_upper)


def half_line_eigenvalue_interval(
    index, coupling, cutoff, tolerance=Fraction(1, 10**12)
):
    """Enclose a low half-line eigenvalue using the exact boundary Schur bounds."""
    coupling = Fraction(coupling)
    tolerance = Fraction(tolerance)
    if not 0 <= index <= cutoff:
        raise ValueError("eigenvalue index is outside the retained block")
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if coupling == 0:
        value = Fraction(index * (index + 2))
        return value, value

    diagonal, off_diagonal = finite_matrix(coupling, cutoff)
    _, ritz_upper = eigenvalue_interval(index, diagonal, off_diagonal, tolerance / 4)
    tail_floor = Fraction((cutoff + 1) * (cutoff + 3))
    if ritz_upper >= tail_floor:
        raise ValueError("retained Ritz value is not below the certified tail floor")

    # Positivity gives a common certified lower bracket.  The two searches locate
    # the count transition for the largest and smallest admissible Schur terms.
    lower_good, lower_bad = Fraction(0), ritz_upper
    if half_line_count_bounds(lower_good, coupling, cutoff)[1] > index:
        raise ValueError("zero is not a certified lower eigenvalue bracket")
    if half_line_count_bounds(lower_bad, coupling, cutoff)[0] <= index:
        raise ValueError("Ritz bracket does not resolve the Schur count")
    while lower_bad - lower_good > tolerance / 2:
        midpoint = (lower_good + lower_bad) / 2
        _, maximum_count = half_line_count_bounds(midpoint, coupling, cutoff)
        if maximum_count <= index:
            lower_good = midpoint
        else:
            lower_bad = midpoint

    upper_bad, upper_good = Fraction(0), ritz_upper
    while upper_good - upper_bad > tolerance / 2:
        midpoint = (upper_bad + upper_good) / 2
        minimum_count, _ = half_line_count_bounds(midpoint, coupling, cutoff)
        if minimum_count > index:
            upper_good = midpoint
        else:
            upper_bad = midpoint

    return lower_good, upper_good


def half_line_low_spectrum(coupling, cutoff, tolerance=Fraction(1, 10**12)):
    """Enclose E0 and E1 of the half-line Jacobi operator."""
    if cutoff < 1:
        raise ValueError("cutoff N must be at least 1")
    return tuple(
        half_line_eigenvalue_interval(index, coupling, cutoff, tolerance)
        for index in range(2)
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

    print(f"retained Jacobi block: N={args.cutoff}, dimension={args.cutoff + 1}")
    print(f"exact target width: {args.tolerance}")
    for coupling in args.couplings:
        finite_spectrum = low_spectrum_intervals(coupling, args.cutoff, args.tolerance)
        finite_gap = subtract_intervals(finite_spectrum[1], finite_spectrum[0])
        spectrum = half_line_low_spectrum(coupling, args.cutoff, args.tolerance)
        gap = subtract_intervals(spectrum[1], spectrum[0])
        print(f"lambda={coupling}")
        print(f"  E0(J_N) in {format_interval(finite_spectrum[0])}")
        print(f"  E1(J_N) in {format_interval(finite_spectrum[1])}")
        print(f"  gap(J_N) in {format_interval(finite_gap)}")
        print("  half-line Schur certificate")
        print(f"  E0(K_lambda) in {format_interval(spectrum[0])}")
        print(f"  E1(K_lambda) in {format_interval(spectrum[1])}")
        print(f"  gap in {format_interval(gap)}")


if __name__ == "__main__":
    main()
