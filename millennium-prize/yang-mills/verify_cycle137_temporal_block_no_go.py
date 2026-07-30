#!/usr/bin/env python3
"""Exact dependency-free verifier for the Cycle 137 temporal-block no-go."""

import sys
from fractions import Fraction


ZERO = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))


class VerificationError(Exception):
    pass


def check(condition, message):
    if not condition:
        raise VerificationError(message)


def add(left, right):
    return left[0] + right[0], left[1] + right[1]


def multiply(left, right):
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conjugate(value):
    return value[0], -value[1]


def norm_squared(value):
    return value[0] * value[0] + value[1] * value[1]


def complex_sum(values):
    total = ZERO
    for value in values:
        total = add(total, value)
    return total


def aperiodic_pair_count(width):
    """Count (i,j,k,l) with i+j=k+l in [0,width)^4."""
    multiplicities = [
        sum(1 for left in range(width) if 0 <= total - left < width)
        for total in range(2 * width - 1)
    ]
    return sum(value * value for value in multiplicities)


def cyclic_pair_count(width, period):
    """Count (i,j,k,l) with i+j=k+l modulo period."""
    multiplicities = [0] * period
    for left in range(width):
        for right in range(width):
            multiplicities[(left + right) % period] += 1
    return sum(value * value for value in multiplicities)


def fourth_moment(width, period=None):
    count = (aperiodic_pair_count(width) if period is None
             else cyclic_pair_count(width, period))
    return Fraction(count, width * width)


def cyclic_autocorrelation(coefficients, period):
    check(len(coefficients) <= period, "FIR is longer than its cyclic period")
    padded = tuple(coefficients) + (ZERO,) * (period - len(coefficients))
    return tuple(
        complex_sum(
            (multiply(padded[(index + lag) % period],
                      conjugate(padded[index]))
             for index in range(period))
        )
        for lag in range(period)
    )


def endpoint_obstruction(coefficients):
    """Return the unique endpoint product at the FIR support span."""
    support = [index for index, value in enumerate(coefficients) if value != ZERO]
    check(support, "zero FIR cannot be normalized")
    first, last = support[0], support[-1]
    span = last - first
    witness = multiply(coefficients[last], conjugate(coefficients[first]))
    if span:
        check(witness != ZERO, "nonzero endpoint product unexpectedly vanished")
    return first, last, span, witness


def certify_allpass_is_delta(coefficients, period):
    """Certify the finite-root all-pass equation forces one-point support."""
    check(period >= 2 * len(coefficients) - 1,
          "period is too short to separate aperiodic correlation lags")
    correlation = cyclic_autocorrelation(coefficients, period)
    check(correlation[0] == ONE, "FIR is not normalized")
    check(all(value == ZERO for value in correlation[1:]),
          "|B|=1 functional equation does not hold at every cyclic root")

    first, last, span, witness = endpoint_obstruction(coefficients)
    if span:
        # Since period >= 2m-1, cyclic lag span has no wraparound term.  Its
        # autocorrelation coefficient is exactly the two endpoint product.
        check(correlation[span] == witness,
              "endpoint lag did not separate from cyclic aliases")
        raise VerificationError(
            "non-delta all-pass FIR survived its endpoint autocorrelation"
        )
    check(norm_squared(coefficients[first]) == 1,
          "singleton coefficient does not have unit modulus")
    return first, coefficients[first]


def verify_fourth_moments():
    rows = []
    for width in range(1, 21):
        exact = fourth_moment(width)
        formula = Fraction(2 * width * width + 1, 3 * width)
        check(exact == formula,
              f"m={width}: fourth moment {exact} != {formula}")
        rows.append(exact)
    return tuple(rows)


def verify_fixed_width_alias_limit():
    rows = []
    for width in range(1, 21):
        limit = Fraction(2 * width * width + 1, 3 * width)
        threshold = 2 * width - 1
        periods = (threshold, threshold + 1, 2 * threshold + 3)
        values = tuple(fourth_moment(width, period) for period in periods)
        check(all(value == limit for value in values),
              f"m={width}: aliases persist beyond period {threshold}")
        if width > 1:
            aliased = fourth_moment(width, threshold - 1)
            check(aliased > limit,
                  f"m={width}: expected boundary alias was not detected")
        rows.append((width, threshold, limit))
    return tuple(rows)


def verify_finite_cyclic_no_go():
    unit_phases = (
        ONE,
        (Fraction(0), Fraction(1)),
        (Fraction(3, 5), Fraction(4, 5)),
        (Fraction(-5, 13), Fraction(12, 13)),
    )
    certified = []
    for width in range(1, 21):
        period = 2 * width + 5
        for location in range(width):
            phase = unit_phases[(width + location) % len(unit_phases)]
            coefficients = [ZERO] * width
            coefficients[location] = phase
            result = certify_allpass_is_delta(tuple(coefficients), period)
            check(result == (location, phase), "wrong delta translation returned")
            certified.append((width, period, location))

    hostile = (
        ((Fraction(3, 5), Fraction(0)),
         (Fraction(4, 5), Fraction(0))),
        ((Fraction(1, 2), Fraction(1, 2)),
         (Fraction(1, 2), Fraction(-1, 2))),
        ((Fraction(0), Fraction(3, 5)), ZERO,
         (Fraction(4, 5), Fraction(0))),
    )
    witnesses = []
    for coefficients in hostile:
        period = 2 * len(coefficients) + 1
        correlation = cyclic_autocorrelation(coefficients, period)
        check(correlation[0] == ONE, "hostile FIR is not normalized")
        first, last, span, witness = endpoint_obstruction(coefficients)
        check(span > 0 and correlation[span] == witness and witness != ZERO,
              "hostile FIR lacks its nonzero endpoint obstruction")
        check(any(value != ZERO for value in correlation[1:]),
              "hostile non-delta FIR accidentally became all-pass")
        witnesses.append((span, witness))
    return tuple(certified), tuple(witnesses)


def main():
    try:
        moments = verify_fourth_moments()
        alias_rows = verify_fixed_width_alias_limit()
        deltas, witnesses = verify_finite_cyclic_no_go()
    except (ArithmeticError, VerificationError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print("PASS Cycle 137 temporal-block no-go (exact Fraction arithmetic)")
    print("fourth moments m=1..20: " + ", ".join(map(str, moments)))
    print("alias limit: M4_N=(2m^2+1)/(3m) exactly for N>=2m-1")
    print(f"fixed-width cases certified: {len(alias_rows)}")
    print(f"cyclic all-pass delta translations certified: {len(deltas)}")
    print(f"non-delta endpoint obstructions certified: {len(witnesses)}")
    print("conclusion: a normalized fixed-width FIR with |B|=1 at all roots")
    print("must be a unit-phase delta translation; temporal blocking cannot help")
    return 0


if __name__ == "__main__":
    sys.exit(main())
