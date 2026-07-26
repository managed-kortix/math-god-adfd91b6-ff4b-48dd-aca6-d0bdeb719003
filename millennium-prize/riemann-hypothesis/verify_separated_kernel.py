#!/usr/bin/env python3
"""Outward-rounded checks for the certified separated-kernel theorem.

Requires python-flint (Arb).  A non-permanent installation can be made with

  python3 -m pip install --target /tmp/rh-flint python-flint
  PYTHONPATH=/tmp/rh-flint python3 verify_separated_kernel.py

All certification decisions use Arb ball endpoints.  Decimal values printed
for diagnostic ratios are not used to decide whether a check passes.
"""

import argparse
import math
from fractions import Fraction

try:
    from flint import acb, arb, ctx
except ImportError as exc:
    raise SystemExit(
        "python-flint is required; install it into a temporary target as shown "
        "in this script's docstring"
    ) from exc


def ball(x):
    if isinstance(x, Fraction):
        return arb(x.numerator) / x.denominator
    return arb(x)


def assert_ball_le(left, right, label):
    """Prove left <= right by disjoint outward-rounded endpoints."""
    if not left.upper() <= right.lower():
        raise AssertionError(f"{label}: cannot certify {left} <= {right}")


def ratio_upper(left, right):
    return float((left / right).upper())


def direct_j(Q, d):
    """Evaluate J_Q(d) independently using Arb's Si and Ci functions."""
    if d == 0:
        return acb(ball(Fraction(1, Q)))
    db = ball(d)
    x = ball(Q * abs(d))
    real = x.cos() / Q - abs(db) * (arb.pi() / 2 - x.si())
    imag = (1 if d > 0 else -1) * (x.sin() / Q - abs(db) * x.ci())
    return acb(real, imag)


def direct_c(Q, d):
    return direct_j(Q, d).real


def endpoint_sum(Q, d, n):
    db = ball(d)
    phase = (acb(0, 1) * Q * db).exp()
    total = acb(0)
    for k in range(n + 1):
        total -= phase * math.factorial(k + 1) / (
            (acb(0, 1) * db) ** (k + 1) * Q ** (k + 2)
        )
    return total


def next_term(Q, d, n):
    db = ball(d)
    phase = (acb(0, 1) * Q * db).exp()
    return -phase * math.factorial(n + 2) / (
        (acb(0, 1) * db) ** (n + 2) * Q ** (n + 3)
    )


def inverse_taylor(d, center, m, p):
    h = ball(d - center)
    c = ball(center)
    return sum(
        ball((-1) ** j * math.comb(m + j - 1, j)) * h**j / c ** (m + j)
        for j in range(p + 1)
    )


def compressed_j(Q, d, center, n, p):
    phase = (acb(0, 1) * Q * ball(d)).exp()
    total = acb(0)
    for k in range(n + 1):
        m = k + 1
        total -= phase * math.factorial(m) * inverse_taylor(d, center, m, p) / (
            acb(0, 1) ** m * Q ** (m + 1)
        )
    return total


def compressed_d(Q, a, b, d0, s0, n, p):
    return (compressed_j(Q, a - b, d0, n, p).real -
            compressed_j(Q, a + b, s0, n, p).real)


def direct_d(Q, a, b):
    return direct_c(Q, a - b) - direct_c(Q, a + b)


def theorem_bounds(Q, d0, s0, H, n, p):
    q, d, s, h = ball(Q), ball(d0), ball(s0), ball(H)
    dmin, smin = d - h, s - h
    far = ball(math.factorial(n + 1)) / q ** (n + 2) * (
        dmin ** (-n - 1) + smin ** (-n - 1)
    )
    amp = arb(0)
    for k in range(n + 1):
        amp += (
            ball(math.factorial(k + 1) * math.comb(k + p + 1, p + 1))
            * h ** (p + 1) / q ** (k + 2)
            * (d ** (-p - 1) * dmin ** (-k - 1)
               + s ** (-p - 1) * smin ** (-k - 1))
        )
    return far, amp


def block_geometry(A, B):
    amin, amax, bmin, bmax = min(A), max(A), min(B), max(B)
    a0, b0 = (amin + amax) / 2, (bmin + bmax) / 2
    rA, rB = (amax - amin) / 2, (bmax - bmin) / 2
    return a0 - b0, a0 + b0, rA + rB


def check_endpoint_theorems(Q, n):
    samples = [Fraction(1, 97), Fraction(3, 20), Fraction(7, 5),
               Fraction(-11, 8), Fraction(23, 3)]
    worst_raw = worst_half = 0.0
    for d in samples:
        exact = direct_j(Q, d)
        approx = endpoint_sum(Q, d, n)
        raw = ball(math.factorial(n + 1)) / (
            ball(Q) ** (n + 2) * ball(abs(d)) ** (n + 1)
        )
        error = abs(exact - approx)
        assert_ball_le(error, raw, f"endpoint remainder at d={d}")
        worst_raw = max(worst_raw, ratio_upper(error, raw))

        term = next_term(Q, d, n)
        half = ball(math.factorial(n + 2)) / (
            2 * ball(Q) ** (n + 3) * ball(abs(d)) ** (n + 2)
        )
        centered_error = abs(exact - approx - term / 2)
        assert_ball_le(centered_error, half, f"half-next-term at d={d}")
        worst_half = max(worst_half, ratio_upper(centered_error, half))
    print(f"endpoint bounds: {len(samples)} cases, max ratios raw={worst_raw:.6g}, "
          f"half-next={worst_half:.6g}")


def check_amplitude_theorem(p):
    cases = [
        (Fraction(17, 10), Fraction(3, 20), 1),
        (Fraction(17, 10), Fraction(-3, 20), 4),
        (Fraction(-9, 4), Fraction(2, 7), 3),
    ]
    worst = 0.0
    for center, h, m in cases:
        d = center + h
        H = abs(h)
        error = abs(ball(d) ** (-m) - inverse_taylor(d, center, m, p))
        bound = (ball(math.comb(m + p, p + 1)) * ball(H) ** (p + 1) /
                 ball(abs(center) - H) ** (m + p + 1))
        assert_ball_le(error, bound, f"amplitude remainder m={m}")
        worst = max(worst, ratio_upper(error, bound))
    print(f"amplitude bounds: {len(cases)} cases, max ratio={worst:.6g}")


def certify_block(name, Q, A, B, coefficients, n, p):
    d0, s0, H = block_geometry(A, B)
    if not (min(A) > max(B) and H < d0):
        raise AssertionError(f"{name}: block is not theorem-admissible")
    far, amp = theorem_bounds(Q, d0, s0, H, n, p)
    radius = far + amp
    worst = 0.0
    bilinear_error = arb(0)
    l1a = sum(abs(c) for c in coefficients[0])
    l1b = sum(abs(c) for c in coefficients[1])
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            error = direct_d(Q, a, b) - compressed_d(Q, a, b, d0, s0, n, p)
            assert_ball_le(abs(error), radius, f"{name} entry ({i},{j})")
            worst = max(worst, ratio_upper(abs(error), radius))
            bilinear_error += ball(coefficients[0][i] * coefficients[1][j]) * error
    form_radius = radius * ball(l1a * l1b)
    assert_ball_le(abs(bilinear_error), form_radius, f"{name} bilinear form")
    print(f"block {name}: {len(A)}x{len(B)}, rank<={2 * (p + 1)}, "
          f"max entry ratio={worst:.6g}, form ratio="
          f"{ratio_upper(abs(bilinear_error), form_radius):.6g}")


def check_hostile_cases(Q, n, p):
    cusp_A = [Fraction(1), Fraction(1000001, 1000000)]
    cusp_B = [Fraction(999999, 1000000), Fraction(1)]
    d0, _, H = block_geometry(cusp_A, cusp_B)
    assert not (min(cusp_A) > max(cusp_B) and H < d0)
    if not direct_c(Q, Fraction(0)).contains(ball(Fraction(1, Q))):
        raise AssertionError("C_Q(0): direct enclosure does not contain 1/Q")
    print("hostile cusp: overlapping two-point block correctly rejected; C_Q(0) certified")

    farey_B = sorted({Fraction(k, q) for q in range(11, 18) for k in range(1, q)
                      if Fraction(2, 5) <= Fraction(k, q) <= Fraction(3, 5)})
    farey_A = [x + 2 for x in farey_B]
    ca = [Fraction((-1) ** i, i + 1) for i in range(len(farey_A))]
    cb = [Fraction((-1) ** (i + 1), i + 2) for i in range(len(farey_B))]
    certify_block("alternating-Farey", Q, farey_A, farey_B, (ca, cb), n, p)

    grid_B = [Fraction(i, 12) for i in range(3, 10)]
    grid_A = [Fraction(i, 12) for i in range(27, 34)]
    ca = [Fraction((-1) ** i * (i + 2), 7) for i in range(len(grid_A))]
    cb = [Fraction((-1) ** i * (2 * i + 1), 11) for i in range(len(grid_B))]
    certify_block("rational-grid", Q, grid_A, grid_B, (ca, cb), n, p)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--Q", type=int, default=64)
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--p", type=int, default=5)
    args = parser.parse_args()
    if args.bits < 80 or args.Q <= 0 or args.n < 0 or args.p < 0:
        parser.error("need bits>=80, Q>0, n>=0, and p>=0")
    ctx.prec = args.bits
    print(f"python-flint {__import__('flint').__version__}; Arb precision={ctx.prec} bits")
    check_endpoint_theorems(args.Q, args.n)
    check_amplitude_theorem(args.p)
    check_hostile_cases(args.Q, args.n, args.p)
    print("all outward-rounded separated-kernel checks passed")


if __name__ == "__main__":
    main()
