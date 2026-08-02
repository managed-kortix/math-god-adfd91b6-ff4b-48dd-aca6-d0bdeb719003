#!/usr/bin/env python3

from fractions import Fraction
from math import gcd, isqrt

try:
    from flint import arb, ctx
except ImportError as exc:
    raise SystemExit(
        "python-flint is required; run with: uv run --with python-flint "
        "python3 millennium-prize/birch-swinnerton-dyer/"
        "verify_cycle237_exact_height_index.py"
    ) from exc


DEN = 10**50
MODEL = (1, 0, 1, -46813, -3372156843)
DISCRIMINANT = -4912444914224609853433
C4 = 2247001
POINT_HEIGHT = (
    Fraction(3396338096796685137401217818912911624353760513342938, DEN),
    Fraction(3396338096796685137401217818912911624353760513342939, DEN),
)
TAMAGAWA_EXPONENT_WITH_REAL_PLACE = 2
NUMERICAL_TRACE_MULTIPLE = 8


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL: " + message)


def rational_interval(value, denominator=DEN):
    scaled = value * denominator
    lower = scaled.lower().floor()
    upper = scaled.upper().floor() + 1
    require(lower.is_exact() and upper.is_exact(), "non-exact endpoint")
    return Fraction(int(lower.fmpz()), denominator), Fraction(int(upper.fmpz()), denominator)


def ceil_fraction(value):
    return -(-value.numerator // value.denominator)


def floor_sqrt_fraction(value):
    require(value >= 0, "square-root input is negative")
    candidate = isqrt(value.numerator // value.denominator)
    while (candidate + 1) ** 2 * value.denominator <= value.numerator:
        candidate += 1
    while candidate**2 * value.denominator > value.numerator:
        candidate -= 1
    return candidate


def silverman_constant():
    # Silverman's explicit bound as implemented by eclib, with Bremner's
    # corrected 2*0.961 term. Here j=c4^3/Delta=-1/433 exactly and b2=1.
    numerator = C4**3
    common = gcd(numerator, abs(DISCRIMINANT))
    j_num = numerator // common
    j_den = DISCRIMINANT // common
    require((j_num, j_den) == (1, -433), "unexpected reduced j-invariant")

    h_j = max(arb(abs(j_num)).log(), arb(abs(j_den)).log())
    log_plus_j = arb(0)  # abs(j)=1/433 < 1
    log_plus_b2_over_12 = arb(0)  # abs(b2/12)=1/12 < 1
    mu = (
        arb(1922) / 1000
        + h_j / 12
        + arb(abs(DISCRIMINANT)).log() / 6
        + log_plus_j / 6
        + log_plus_b2_over_12
        + arb(2).log()
    )
    return rational_interval(mu), (j_num, j_den)


def main():
    ctx.prec = 320
    silverman, j = silverman_constant()

    # The published Cremona-Siksek computation gives >7 only on the
    # everywhere-good-reduction subgroup. Division by the exact global
    # component exponent squared makes 7/4 a valid global lower bound.
    h_min = Fraction(7, TAMAGAWA_EXPONENT_WITH_REAL_PLACE**2)
    h_point_upper = POINT_HEIGHT[1]
    m_point = floor_sqrt_fraction(h_point_upper / h_min)
    require(m_point == 4, "unexpected point-index cutoff")

    # This is an exact conditional consequence only: Cycle 209 has not
    # certified that the mathematical Heegner trace is +/-8P.
    h_trace_upper_if_identified = NUMERICAL_TRACE_MULTIPLE**2 * h_point_upper
    trace_height_integer_upper_if_identified = ceil_fraction(h_trace_upper_if_identified)
    m_trace_if_identified = floor_sqrt_fraction(
        Fraction(trace_height_integer_upper_if_identified, 1) / h_min
    )
    require(trace_height_integer_upper_if_identified == 2174, "unexpected trace-height ceiling")
    require(m_trace_if_identified == 35, "unexpected conditional trace-index cutoff")

    print("model=", MODEL, sep="")
    print("j_invariant=", Fraction(*j), sep="")
    print("silverman_height_difference_constant_interval=", list(silverman), sep="")
    print("siksek_egr_lower_bound=7 (strict; theorem certificate still required)")
    print("global_component_exponent=", TAMAGAWA_EXPONENT_WITH_REAL_PLACE, sep="")
    print("global_non_torsion_height_lower_bound=7/4 (strict; conditional on directed Siksek certificate)")
    print("point_height_interval=", list(POINT_HEIGHT), sep="")
    print("point_index_cutoff_M=", m_point, sep="")
    print("candidate_heegner_trace=+/-8P (not certified)")
    print("conditional_trace_height_upper_integer=", trace_height_integer_upper_if_identified, sep="")
    print("conditional_trace_index_cutoff_M=", m_trace_if_identified, sep="")
    print("OBSTRUCTION=no directed proof of the Cremona-Siksek >7 test and no certified y=+/-8P trace identity")
    print("NO_UNCONDITIONAL_FINITE_M")


if __name__ == "__main__":
    main()
