#!/usr/bin/env python3
"""Directed audit of the complete Cycle 243 Nyman--Beurling energies.

Arb evaluates every logarithm, Euler's constant, pi, and rational-angle
cotangent with outward rounding.  The emitted certificate contains only exact
rational endpoints.  Binary floating-point arithmetic is not used.
"""

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from flint import arb, ctx

from certify_complete_gram import RestrictedGram, mobius_sieve


DEFAULT_CERTIFICATE = Path(__file__).with_name("cycle243-small-nb-certificate.json")
TARGETS = (3, 6)


@dataclass(frozen=True)
class EnergyParts:
    constant: object
    affine: object
    diagonal: object
    offdiagonal: object

    @property
    def total(self):
        return self.constant + self.affine + self.diagonal + self.offdiagonal


def complete_energy_parts(N, gram, mu, logs):
    """Evaluate all four terms in the complete restricted Vasyunin formula."""
    log_N = logs[N]
    coefficients = {
        a: arb(mu[a]) * (1 - logs[a] / log_N)
        for a in range(1, N + 1)
        if mu[a]
    }
    constant = arb(1)
    affine = 2 * sum(
        (coefficients[a] * gram.chi_cross(a) for a in coefficients), arb(0)
    )
    diagonal = sum(
        (coefficient * coefficient * gram.entry(a, a)
         for a, coefficient in coefficients.items()),
        arb(0),
    )
    active = tuple(coefficients)
    offdiagonal = 2 * sum(
        (coefficients[a] * coefficients[b] * gram.entry(a, b)
         for i, a in enumerate(active) for b in active[i + 1:]),
        arb(0),
    )
    return EnergyParts(constant, affine, diagonal, offdiagonal)


def _arb_endpoint_fraction(value):
    """Convert an exact finite Arb endpoint to a Fraction."""
    mantissa, exponent = value.man_exp()
    mantissa = int(mantissa)
    exponent = int(exponent)
    if exponent >= 0:
        return Fraction(mantissa << exponent)
    return Fraction(mantissa, 1 << (-exponent))


def rational_enclosure(value, denominator_bits=80):
    """Round an Arb ball outwards to a stable dyadic rational interval."""
    scale = 1 << denominator_bits
    lower = _arb_endpoint_fraction(value.lower())
    upper = _arb_endpoint_fraction(value.upper())
    lower_numerator = lower.numerator * scale // lower.denominator
    upper_numerator = -((-upper.numerator * scale) // upper.denominator)
    return Fraction(lower_numerator, scale), Fraction(upper_numerator, scale)


def encode_fraction(value):
    return f"{value.numerator}/{value.denominator}"


def decode_fraction(value):
    return Fraction(value)


def compute(bits=256):
    if bits < 128:
        raise ValueError("at least 128 Arb bits are required")
    ctx.prec = bits
    mu = mobius_sieve(max(TARGETS))
    logs = [arb(0)] + [arb(n).log() for n in range(1, max(TARGETS) + 1)]
    gram = RestrictedGram()
    parts = {N: complete_energy_parts(N, gram, mu, logs) for N in TARGETS}
    margin = parts[6].total - arb(3) * parts[3].total / 4
    return parts, margin


def make_certificate(bits=256, denominator_bits=80):
    parts, margin = compute(bits)
    names = ("constant", "affine", "diagonal", "offdiagonal", "total")
    energies = {}
    for N in TARGETS:
        rows = {}
        for name in names:
            value = parts[N].total if name == "total" else getattr(parts[N], name)
            lower, upper = rational_enclosure(value, denominator_bits)
            rows[name] = {
                "lower": encode_fraction(lower),
                "upper": encode_fraction(upper),
            }
        energies[str(N)] = rows
    lower, upper = rational_enclosure(margin, denominator_bits)
    return {
        "cycle": 243,
        "claim": "P_6 <= (3/4) P_3",
        "verdict": "PROVED",
        "formula": "1 + affine + diagonal + offdiagonal; restricted Vasyunin Gram",
        "arb_bits": bits,
        "endpoint_denominator_bits": denominator_bits,
        "energies": energies,
        "margin_P6_minus_3P3_over_4": {
            "lower": encode_fraction(lower),
            "upper": encode_fraction(upper),
        },
    }


def _check_encloses(label, certified, computed):
    lower = decode_fraction(certified["lower"])
    upper = decode_fraction(certified["upper"])
    computed_lower = _arb_endpoint_fraction(computed.lower())
    computed_upper = _arb_endpoint_fraction(computed.upper())
    if lower > computed_lower or upper < computed_upper:
        raise ArithmeticError(f"certificate does not enclose recomputed {label}")
    if lower > upper:
        raise ArithmeticError(f"reversed certificate interval for {label}")


def verify_certificate(certificate):
    bits = int(certificate["arb_bits"])
    parts, margin = compute(bits)
    for N in TARGETS:
        rows = certificate["energies"][str(N)]
        for name in ("constant", "affine", "diagonal", "offdiagonal"):
            _check_encloses(f"P_{N} {name}", rows[name], getattr(parts[N], name))
        _check_encloses(f"P_{N}", rows["total"], parts[N].total)
    margin_row = certificate["margin_P6_minus_3P3_over_4"]
    _check_encloses("P_6-(3/4)P_3", margin_row, margin)

    p3_lower = decode_fraction(certificate["energies"]["3"]["total"]["lower"])
    p6_upper = decode_fraction(certificate["energies"]["6"]["total"]["upper"])
    margin_upper = decode_fraction(margin_row["upper"])
    if not p6_upper <= Fraction(3, 4) * p3_lower:
        raise ArithmeticError("rational endpoint test does not prove the claim")
    if margin_upper >= 0:
        raise ArithmeticError("certified margin is not strictly negative")
    return parts, margin


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--bits", type=int, default=256)
    args = parser.parse_args()

    if args.write_certificate:
        certificate = make_certificate(args.bits)
        args.certificate.write_text(json.dumps(certificate, indent=2) + "\n")
    else:
        certificate = json.loads(args.certificate.read_text())

    parts, margin = verify_certificate(certificate)
    print("cycle-243 complete directed Vasyunin certificate")
    for N in TARGETS:
        print(f"P_{N} in {parts[N].total.str(30)}")
        print(
            "  constant={} affine={} diagonal={} offdiagonal={}".format(
                parts[N].constant.str(16), parts[N].affine.str(16),
                parts[N].diagonal.str(16), parts[N].offdiagonal.str(16),
            )
        )
    print(f"P_6-(3/4)P_3 in {margin.str(30)}")
    print("PROVED: exact rational endpoints certify P_6 <= (3/4) P_3")


if __name__ == "__main__":
    main()
