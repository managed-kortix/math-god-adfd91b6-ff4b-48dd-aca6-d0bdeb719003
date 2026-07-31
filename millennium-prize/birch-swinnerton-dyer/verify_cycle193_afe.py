#!/usr/bin/env python3
"""Rational interval replay for the pinned D=-1499 AFE coefficient table.

Trust boundary: this verifier checks the interval arithmetic and the pinned
CSV artifact. It does not independently prove the AFE identity, root number,
conductor, or that PARI's ellan output is the curve's newform coefficient list.
Those inputs are external mathematical/generator obligations.
"""

from fractions import Fraction
from pathlib import Path
import csv
import hashlib


HERE = Path(__file__).resolve().parent
COEFFICIENTS = HERE / "cycle193_D-1499_coefficients.csv"
N = 972951433
M = 100000
K = 16
SCALE = 10**50
EXPECTED_SHA256 = "806f69693e70a187fab6d86a966e99ba352b76bfc8a8abc8d24692f125fe9828"
EXPECTED_PARTIAL = (
    425055634725652900855942081984698787572090256053427,
    425182127644901403569566902260194380627700638834053,
)
EXPECTED_TAIL = 176013281350567737032200216283212943473614535
EXPECTED_FINAL = (
    425055458712371550288205049784482504359146782438892,
    425182303658182754137303934460410663840644112448588,
)

# Strict decimal rational bounds; their containment proof is checked below.
ALPHA_LO = Fraction(20143470058089910442088524096749042725, 10**41)
ALPHA_HI = Fraction(20143470058089910442088524096749042727, 10**41)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def floor_fraction(x):
    return x.numerator // x.denominator


def ceil_fraction(x):
    return -((-x.numerator) // x.denominator)


def arctan_bounds_inverse(q, terms):
    """Alternating-series bounds for atan(1/q), using exact rationals."""
    total = Fraction(0)
    for j in range(terms):
        term = Fraction(1, (2 * j + 1) * q ** (2 * j + 1))
        total += term if j % 2 == 0 else -term
    nxt = Fraction(1, (2 * terms + 1) * q ** (2 * terms + 1))
    other = total + (nxt if terms % 2 == 0 else -nxt)
    return min(total, other), max(total, other)


def pi_bounds():
    a5_lo, a5_hi = arctan_bounds_inverse(5, 40)
    a239_lo, a239_hi = arctan_bounds_inverse(239, 12)
    return 16 * a5_lo - 4 * a239_hi, 16 * a5_hi - 4 * a239_lo


def exp_minus_fixed(x):
    """Directed fixed-point bounds for exp(-x), for 0 <= x < 1."""
    require(0 <= x < 1, "exponential argument outside alternating-series range")
    total = Fraction(1)
    term = Fraction(1)
    j = 0
    while True:
        j += 1
        term *= x / j
        total += -term if j % 2 else term
        nxt = term * x / (j + 1)
        if nxt * SCALE < 1:
            other = total + (nxt if (j + 1) % 2 == 0 else -nxt)
            lo, hi = min(total, other), max(total, other)
            scaled_lo = floor_fraction(lo * SCALE)
            scaled_hi = ceil_fraction(hi * SCALE)
            require(0 < scaled_lo <= scaled_hi <= SCALE, "invalid exponential enclosure")
            return scaled_lo, scaled_hi


def mul_interval_positive(a_lo, a_hi, b_lo, b_hi):
    require(0 <= a_lo <= a_hi and 0 <= b_lo <= b_hi, "invalid positive interval")
    return (a_lo * b_lo) // SCALE, (a_hi * b_hi + SCALE - 1) // SCALE


def e1_grid(alpha):
    """Enclose E1(alpha*n), n=1..M, by convex midpoint/trapezoid sums."""
    q_lo, q_hi = exp_minus_fixed(alpha / (2 * K))
    p_lo = p_hi = SCALE
    cells_lo = [0] * (M + 1)
    cells_hi = [0] * (M + 1)
    left_lo = left_hi = SCALE

    for r in range(1, 2 * K * (M + 1) + 1):
        p_lo, p_hi = mul_interval_positive(p_lo, p_hi, q_lo, q_hi)
        if r % 2 == 1:
            # Midpoint lower contribution: 2*exp(-alpha*r/(2K))/r.
            n = r // (2 * K)
            if n >= 1:
                cells_lo[n] += (2 * p_lo) // r
        else:
            # Trapezoid upper contribution from this right endpoint and
            # the previous left endpoint.
            n = (r - 2) // (2 * K)
            if n >= 1:
                cells_hi[n] += (left_hi + (r - 2) - 1) // (r - 2)
                cells_hi[n] += (p_hi + r - 1) // r
            left_lo, left_hi = p_lo, p_hi

    # At u=M+1, e^(-alpha*u)/(alpha*u+1) <= E1(alpha*u)
    # <= e^(-alpha*u)/(alpha*u).
    u = M + 1
    x = alpha * u
    tail_lo = floor_fraction(Fraction(p_lo, 1) / (x + 1))
    tail_hi = ceil_fraction(Fraction(p_hi, 1) / x)
    e1_lo = [0] * (M + 1)
    e1_hi = [0] * (M + 1)
    acc_lo, acc_hi = tail_lo, tail_hi
    for n in range(M, 0, -1):
        acc_lo += cells_lo[n]
        acc_hi += cells_hi[n]
        e1_lo[n], e1_hi[n] = acc_lo, acc_hi
    return e1_lo, e1_hi, q_lo, q_hi, p_lo, p_hi


def load_coefficients():
    digest = hashlib.sha256(COEFFICIENTS.read_bytes()).hexdigest()
    require(digest == EXPECTED_SHA256, "coefficient table digest mismatch")
    values = [0]
    with COEFFICIENTS.open(newline="", encoding="ascii") as handle:
        reader = csv.reader(handle, strict=True)
        require(next(reader, None) == ["n", "a_n"], "coefficient header mismatch")
        for expected, row in enumerate(reader, 1):
            require(len(row) == 2, f"malformed coefficient row {expected}")
            try:
                index, coefficient = int(row[0]), int(row[1])
            except ValueError as exc:
                raise RuntimeError(f"nonintegral coefficient row {expected}") from exc
            require(index == expected, f"coefficient index mismatch at row {expected}")
            values.append(coefficient)
    require(len(values) == M + 1, "coefficient count mismatch")
    require(values[1] == 1, "newform normalization mismatch")
    return values, digest


def main():
    pi_lo, pi_hi = pi_bounds()
    require(0 < pi_lo < pi_hi, "invalid pi enclosure")
    require(0 < ALPHA_LO < ALPHA_HI, "invalid alpha enclosure")
    require(ALPHA_LO**2 * N < 4 * pi_lo**2, "alpha lower bound failed")
    require(ALPHA_HI**2 * N > 4 * pi_hi**2, "alpha upper bound failed")

    coeffs, digest = load_coefficients()
    lo_grid, _, _, _, _, _ = e1_grid(ALPHA_HI)
    _, hi_grid, q_lo, q_hi, end_lo, end_hi = e1_grid(ALPHA_LO)

    partial_lo = 0
    partial_hi = 0
    for n in range(1, M + 1):
        a = coeffs[n]
        if a >= 0:
            partial_lo += (2 * a * lo_grid[n]) // n
            partial_hi += ceil_fraction(Fraction(2 * a * hi_grid[n], n))
        else:
            partial_lo += (2 * a * hi_grid[n]) // n
            partial_hi += ceil_fraction(Fraction(2 * a * lo_grid[n], n))

    # Deligne plus d(n)<=2*sqrt(n): |a_n|<=2n. For alpha=2*pi/sqrt(N),
    # 2*sum_{n>M}|a_n|E1(alpha*n)/n is at most
    # 4*e^(-alpha*(M+1))/(alpha*(M+1)*(1-e^-alpha)).
    exp_step_lo, exp_step_hi = exp_minus_fixed(ALPHA_LO)
    tail = Fraction(4 * end_hi * SCALE * SCALE, 1)
    tail /= ALPHA_LO * (M + 1) * (SCALE - exp_step_hi) * SCALE
    tail_scaled = ceil_fraction(tail)

    final_lo = partial_lo - tail_scaled
    final_hi = partial_hi + tail_scaled
    require(partial_lo <= partial_hi, "partial interval is inverted")
    require(tail_scaled >= 0, "tail bound is negative")
    require((partial_lo, partial_hi) == EXPECTED_PARTIAL, "partial interval regression")
    require(tail_scaled == EXPECTED_TAIL, "tail bound regression")
    require((final_lo, final_hi) == EXPECTED_FINAL, "final interval regression")
    require(final_lo > 0, "certificate does not prove nonvanishing")
    print(f"coefficient_count={M}")
    print(f"coefficient_sha256={digest}")
    print(f"alpha_interval=[{ALPHA_LO},{ALPHA_HI}]")
    print(f"partial_interval=[{partial_lo}/{SCALE},{partial_hi}/{SCALE}]")
    print(f"tail_bound={tail_scaled}/{SCALE}")
    print(f"Lprime_interval=[{final_lo}/{SCALE},{final_hi}/{SCALE}]")
    print("scope=pinned-coefficient rational AFE replay")
    print("nonzero=PASS")


if __name__ == "__main__":
    main()
