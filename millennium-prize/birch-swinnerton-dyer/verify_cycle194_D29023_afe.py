#!/usr/bin/env python3
"""Directed-rational certificate for L'(E^(-29023), 1) > 0."""

from fractions import Fraction
from pathlib import Path
import csv
import hashlib


HERE = Path(__file__).resolve().parent
COEFFICIENTS = HERE / "cycle194_D-29023_coefficients.csv"
METADATA = HERE / "cycle194_D-29023_metadata.txt"
N = 364730851057
M = 650000
K = 1
SCALE = 10**15
EXPECTED_SHA256 = "cc7f4e63833e33728233bc8b69a60b6a0609a84cabaafb3c2919b4d79b0992b1"
EXPECTED_METADATA_SHA256 = "b3c1fa2a7f2c7237d76e3e7696d3507f668d66c8c7b4bb25d9433372bfbc9905"
EXPECTED_METADATA = {
    "producer": "PARI/GP [2, 15, 4]",
    "base_curve": "433a1",
    "twist_D": "-29023",
    "minimal_model": "[1, 1, 1, -17548636, -24475377572834]",
    "conductor": str(N),
    "root_number": "-1",
    "bad_prime_433_reduction": "multiplicative",
    "a_433": "1",
    "bad_prime_29023_reduction": "additive",
    "a_29023": "0",
    "coefficient_count": str(M),
    "coefficient_method": "ellan",
}
EXPECTED_PARTIAL = (75518458081702825, 75876773943936645)
EXPECTED_TAIL = 65741880536728361
EXPECTED_FINAL = (9776577544974464, 141618654480665006)

ALPHA_LO = Fraction(
    "0.000010403838892284317869514074224245190037638796397013123501815663368931838482295672"
)
ALPHA_HI = Fraction(
    "0.000010403838892284317869514074224245190037638796397013123501815663368931838482295673"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def floor_fraction(x):
    return x.numerator // x.denominator


def ceil_fraction(x):
    return -((-x.numerator) // x.denominator)


def arctan_bounds_inverse(q, terms):
    total = Fraction(0)
    for j in range(terms):
        term = Fraction(1, (2 * j + 1) * q ** (2 * j + 1))
        total += term if j % 2 == 0 else -term
    nxt = Fraction(1, (2 * terms + 1) * q ** (2 * terms + 1))
    other = total + (nxt if terms % 2 == 0 else -nxt)
    return min(total, other), max(total, other)


def pi_bounds():
    a5_lo, a5_hi = arctan_bounds_inverse(5, 64)
    a239_lo, a239_hi = arctan_bounds_inverse(239, 16)
    return 16 * a5_lo - 4 * a239_hi, 16 * a5_hi - 4 * a239_lo


def exp_minus_fixed(x):
    require(0 <= x < 1, "exponential argument outside [0,1)")
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
            require(0 < scaled_lo <= scaled_hi <= SCALE,
                    "invalid exponential enclosure")
            return scaled_lo, scaled_hi


def mul_interval_positive(a_lo, a_hi, b_lo, b_hi):
    require(0 <= a_lo <= a_hi and 0 <= b_lo <= b_hi,
            "invalid positive interval multiplication")
    return (a_lo * b_lo) // SCALE, (a_hi * b_hi + SCALE - 1) // SCALE


def e1_grid(alpha):
    q_lo, q_hi = exp_minus_fixed(alpha / (2 * K))
    p_lo = p_hi = SCALE
    cells_lo = [0] * (M + 1)
    cells_hi = [0] * (M + 1)
    left_hi = SCALE

    for r in range(1, 2 * K * (M + 1) + 1):
        p_lo, p_hi = mul_interval_positive(p_lo, p_hi, q_lo, q_hi)
        if r % 2 == 1:
            n = r // (2 * K)
            if n >= 1:
                cells_lo[n] += (2 * p_lo) // r
        else:
            n = (r - 2) // (2 * K)
            if n >= 1:
                cells_hi[n] += (left_hi + (r - 2) - 1) // (r - 2)
                cells_hi[n] += (p_hi + r - 1) // r
            left_hi = p_hi

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
    return e1_lo, e1_hi, p_hi


def verify_metadata():
    digest = hashlib.sha256(METADATA.read_bytes()).hexdigest()
    require(digest == EXPECTED_METADATA_SHA256, "metadata SHA-256 mismatch")
    rows = METADATA.read_text(encoding="ascii").splitlines()
    require(len(rows) == len(EXPECTED_METADATA), "wrong metadata row count")
    parsed = {}
    for row in rows:
        require(row.count("=") == 1, "malformed metadata row")
        key, value = row.split("=", 1)
        require(key not in parsed, "duplicate metadata key")
        parsed[key] = value
    require(parsed == EXPECTED_METADATA, "metadata content mismatch")
    return digest


def load_coefficients():
    digest = hashlib.sha256(COEFFICIENTS.read_bytes()).hexdigest()
    require(digest == EXPECTED_SHA256, "coefficient SHA-256 mismatch")
    values = [0]
    with COEFFICIENTS.open(newline="", encoding="ascii") as handle:
        reader = csv.reader(handle, strict=True)
        require(next(reader, None) == ["n", "a_n"], "bad coefficient header")
        for expected, row in enumerate(reader, 1):
            require(len(row) == 2, "malformed coefficient row")
            require(int(row[0]) == expected, "coefficient index mismatch")
            values.append(int(row[1]))
    require(len(values) == M + 1, "wrong coefficient count")
    require(values[1] == 1, "coefficient normalization mismatch")
    return values, digest


def main():
    metadata_digest = verify_metadata()
    pi_lo, pi_hi = pi_bounds()
    require(0 < pi_lo < pi_hi, "invalid pi enclosure")
    require(0 < ALPHA_LO < ALPHA_HI, "invalid alpha enclosure")
    require(ALPHA_LO**2 * N < 4 * pi_lo**2,
            "alpha lower bound not proved")
    require(ALPHA_HI**2 * N > 4 * pi_hi**2,
            "alpha upper bound not proved")

    coeffs, digest = load_coefficients()
    lo_grid, _, _ = e1_grid(ALPHA_HI)
    _, hi_grid, end_hi = e1_grid(ALPHA_LO)

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

    _, exp_step_hi = exp_minus_fixed(ALPHA_LO)
    require(exp_step_hi < SCALE, "invalid geometric-tail ratio")
    tail = Fraction(4 * end_hi * SCALE * SCALE, 1)
    tail /= ALPHA_LO * (M + 1) * (SCALE - exp_step_hi) * SCALE
    tail_scaled = ceil_fraction(tail)

    final_lo = partial_lo - tail_scaled
    final_hi = partial_hi + tail_scaled
    require(partial_lo <= partial_hi, "invalid partial-sum interval")
    require(tail_scaled >= 0, "negative tail bound")
    require(final_lo <= final_hi, "invalid final interval")
    require((partial_lo, partial_hi) == EXPECTED_PARTIAL,
            "partial interval regression")
    require(tail_scaled == EXPECTED_TAIL, "tail bound regression")
    require((final_lo, final_hi) == EXPECTED_FINAL,
            "final interval regression")
    require(final_lo > 0, "certificate does not prove L'(1)>0")
    print(f"metadata_sha256={metadata_digest}")
    print(f"coefficient_count={M}")
    print(f"coefficient_sha256={digest}")
    print(f"mesh_subdivisions={K}")
    print(f"partial_interval=[{partial_lo}/{SCALE},{partial_hi}/{SCALE}]")
    print(f"tail_bound={tail_scaled}/{SCALE}")
    print(f"Lprime_interval=[{final_lo}/{SCALE},{final_hi}/{SCALE}]")
    print("Lprime_positive=PASS")


if __name__ == "__main__":
    main()
