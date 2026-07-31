#!/usr/bin/env python3

from fractions import Fraction
from hashlib import sha256
from pathlib import Path

try:
    from flint import acb, acb_poly, arb, ctx
except ImportError as exc:
    raise SystemExit(
        "python-flint is required; run with: "
        "uv run --with python-flint python3 "
        "millennium-prize/birch-swinnerton-dyer/verify_cycle195_exact_interval.py"
    ) from exc


DEN = 10**50
MODEL = (1, 0, 1, -46813, -3372156843)
POINT = (
    Fraction(399030891253207, 156180668809),
    Fraction(7009131418974188521075, 61722131771310373),
)
CONDUCTOR = 972951433
DISCRIMINANT = -4912444914224609853433
TAMAGAWA = ((433, 1, 5, 1), (1499, 2, -1, 2))
TORSION_ORDER = 1
LPRIME = (
    Fraction(425055458712371550288205049784482504359146782438892, DEN),
    Fraction(425182303658182754137303934460410663840644112448588, DEN),
)
EXPECTED_PERIOD = (
    6258249033705717664048725789876108131610965835281,
    6258249033705717664048725789876108131610965835282,
)
EXPECTED_HEIGHT = (
    3396338096796685137401217818912911624353760513342938,
    3396338096796685137401217818912911624353760513342939,
)


def fail(message):
    raise SystemExit("FAIL: " + message)


def require(condition, message):
    if not condition:
        fail(message)


def fraction_ball(value):
    return arb(value.numerator) / value.denominator


def rational_interval(ball, denominator=DEN):
    scaled = ball * denominator
    lower = scaled.lower().floor()
    upper = scaled.upper().floor() + 1
    require(lower.is_exact() and upper.is_exact(), "non-exact rational endpoint")
    return int(lower.fmpz()), int(upper.fmpz())


def point_check():
    a1, a2, a3, a4, a6 = MODEL
    x, y = POINT
    lhs = y * y + a1 * x * y + a3 * y
    rhs = x**3 + a2 * x**2 + a4 * x + a6
    require(lhs == rhs, "point is not on the stated model")


def invariants():
    a1, a2, a3, a4, a6 = MODEL
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    c4 = b2 * b2 - 24 * b4
    disc = -b2 * b2 * b8 - 8 * b4**3 - 27 * b6**2 + 9 * b2 * b4 * b6
    require((b2, b4, b6, b8, c4, disc) ==
            (1, -93625, -13488627371, -5563566999, 2247001, DISCRIMINANT),
            "Weierstrass invariant mismatch")
    return b2, b4, b6, b8


def real_period(b2, b4, b6):
    roots = acb_poly([b6, 2 * b4, b2, 4]).roots(arb(2) ** -220, maxprec=4096)
    real_roots = [z for z in roots if z.imag.contains(0)]
    upper_roots = [z for z in roots if z.imag > 0]
    require(len(real_roots) == 1 and len(upper_roots) == 1, "cubic root isolation failed")
    e1 = real_roots[0].real
    e2 = upper_roots[0]
    d = e1 - e2.real
    b = e2.imag
    omega = 2 * acb.elliptic_rf(0, d + acb(0, b), d - acb(0, b))
    require(omega.imag.contains(0), "real period has nonzero imaginary part")
    endpoints = rational_interval(omega.real)
    require(endpoints == EXPECTED_PERIOD, "real-period endpoint mismatch")
    return omega.real, endpoints


def exp_height(b2, b4, b6, b8):
    xq, yq = POINT
    x = fraction_ball(xq)
    y = fraction_ball(yq)
    roots = acb_poly([b6, 2 * b4, b2, 4]).roots(arb(2) ** -220, maxprec=4096)
    e1 = [z.real for z in roots if z.imag.contains(0)][0]
    e2 = [z for z in roots if z.imag > 0][0]
    d3 = acb(e1) - e2
    b = (d3.real * d3.real + d3.imag * d3.imag).sqrt()
    t = (12 * e1 + b2) / 16
    if t > 0:
        b = -b
    a = b / 2 - t

    x0 = x - e1
    qdisc = ((x0 + b) ** 2 - 4 * a * x0).sqrt()
    xx = (x0 + b + qdisc) / 2
    x_minus_a = xx - a
    if a > 0:
        old_a = a
        xx = xx - b
        a = -b
        b = old_a - b
    a = (-a).sqrt()
    b = (-b).sqrt()

    values = []
    threshold = arb(2) ** -230
    for _ in range(100):
        old_a = a
        a = (old_a + b) / 2
        delta = a - old_a
        if delta.contains(0) and delta.abs_upper() < threshold:
            break
        ab = old_a * b
        b = ab.sqrt()
        p1 = (xx - ab) / 2
        p2 = a * a
        xx = p1 + (p1 * p1 + xx * p2).sqrt()
        values.append(xx + p2)
    else:
        fail("height AGM did not converge")

    if values:
        xx = values[-1]
        for value in reversed(values[:-1]):
            xx = xx * xx / value
    else:
        xx = xx + a * a
    h_arch_den = (xx * xx / x_minus_a) ** 2 * xq.denominator**2
    h_arch = h_arch_den.log() / 4
    height = 2 * h_arch
    reference = arb("33.963380967966851374012178189129116243537605133429")
    require(abs(height - reference).abs_upper() < arb("1e-48"),
            "height ball misses independent PARI reference")
    endpoints = rational_interval(height)
    require(endpoints == EXPECTED_HEIGHT, "canonical-height endpoint mismatch")

    psi2 = 2 * yq + MODEL[0] * xq + MODEL[2]
    phi2 = MODEL[3] + 2 * MODEL[1] * xq + 3 * xq * xq - MODEL[0] * yq
    from math import gcd
    require(gcd(psi2.numerator, phi2.numerator) == 1,
            "unexpected finite local-height correction prime")
    return height, endpoints


def bsd_quotient(period_endpoints, height_endpoints):
    omega_lo, omega_hi = (Fraction(x, DEN) for x in period_endpoints)
    height_lo, height_hi = (Fraction(x, DEN) for x in height_endpoints)
    tamagawa_product = 1
    for _, _, _, cp in TAMAGAWA:
        tamagawa_product *= cp
    qlo = LPRIME[0] * TORSION_ORDER**2 / (omega_hi * tamagawa_product * height_hi)
    qhi = LPRIME[1] * TORSION_ORDER**2 / (omega_lo * tamagawa_product * height_lo)
    require(qlo < 1 < qhi, "BSD quotient does not contain one")
    require(qlo > 0 and qhi < 2, "interval does not isolate 1 among integers")
    return qlo, qhi


def main():
    ctx.prec = 320
    point_check()
    b2, b4, b6, b8 = invariants()
    period, period_endpoints = real_period(b2, b4, b6)
    height, height_endpoints = exp_height(b2, b4, b6, b8)
    quotient = bsd_quotient(period_endpoints, height_endpoints)
    source_hash = sha256(Path(__file__).read_bytes()).hexdigest()

    print("model=", MODEL, sep="")
    print("point=", POINT, sep="")
    print("conductor=", CONDUCTOR, sep="")
    print("discriminant=", DISCRIMINANT, sep="")
    print("torsion_order=", TORSION_ORDER, sep="")
    print("local_tamagawa_(p,f,kodaira,c_p)=", TAMAGAWA, sep="")
    print("tamagawa_product=2")
    print("real_period_interval=", [Fraction(x, DEN) for x in period_endpoints], sep="")
    print("canonical_height_interval=", [Fraction(x, DEN) for x in height_endpoints], sep="")
    print("Lprime_interval=", list(LPRIME), sep="")
    print("bsd_point_quotient_interval=", list(quotient), sep="")
    print("bsd_point_quotient_decimal_enclosure=0.9998891243271545,1.0001875109945714")
    print("integer_candidate_isolated=1, but quotient_integrality_is_not_a_theorem_input")
    print("sha_index_factor_isolation=NO")
    print("conditional_identity=if refined rank-one BSD holds, quotient=|Sha|*[E(Q)_free:ZP]^(-2)")
    print("scope=certifies exact inputs and Arb/rational intervals; does not prove refined BSD, Sha order, or saturation")
    print("verifier_sha256=", source_hash, sep="")
    print("PASS")


if __name__ == "__main__":
    main()
