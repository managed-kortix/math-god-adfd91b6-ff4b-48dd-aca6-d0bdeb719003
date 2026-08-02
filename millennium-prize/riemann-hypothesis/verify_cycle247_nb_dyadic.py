#!/usr/bin/env python3
"""Directed dyadic scan for the logarithmic Nyman--Beurling energies.

All transcendental work is done by Arb. The checked certificate stores only
outward-rounded dyadic rational intervals, so its ratio and threshold tests are
exact rational comparisons.
"""

import argparse
import json
from fractions import Fraction
from pathlib import Path

from flint import arb

from certify_complete_gram import complete_energies
from verify_cycle243_small_nb import (
    _arb_endpoint_fraction,
    decode_fraction,
    encode_fraction,
    rational_enclosure,
)


DEFAULT_CERTIFICATE = Path(__file__).with_name("cycle247-nb-dyadic-certificate.json")
BASE = 3
DEFAULT_MAX_N = 1536


def targets(max_N):
    if max_N < 2 * BASE:
        raise ValueError("max_N must be at least 6")
    result = []
    N = BASE
    while 2 * N <= max_N:
        result.append(N)
        N *= 2
    return tuple(result)


def compute(max_N=DEFAULT_MAX_N, bits=192):
    if bits < 128:
        raise ValueError("at least 128 Arb bits are required")
    energies = complete_energies(max_N, bits)
    rows = {}
    for N in targets(max_N):
        rows[N] = (energies[N], energies[2 * N], energies[2 * N] / energies[N])
    return rows


def _interval(value, denominator_bits):
    lower, upper = rational_enclosure(value, denominator_bits)
    return {"lower": encode_fraction(lower), "upper": encode_fraction(upper)}


def make_certificate(max_N=DEFAULT_MAX_N, bits=192, denominator_bits=100):
    rows = compute(max_N, bits)
    return {
        "cycle": 247,
        "claim": "directed finite dyadic scan only; no asymptotic or RH claim",
        "base": BASE,
        "max_N": max_N,
        "arb_bits": bits,
        "endpoint_denominator_bits": denominator_bits,
        "rows": [
            {
                "j": j,
                "N": N,
                "P_N": _interval(values[0], denominator_bits),
                "P_2N": _interval(values[1], denominator_bits),
                "ratio": _interval(values[2], denominator_bits),
            }
            for j, (N, values) in enumerate(rows.items())
        ],
    }


def _check_encloses(label, interval, value):
    lower = decode_fraction(interval["lower"])
    upper = decode_fraction(interval["upper"])
    actual_lower = _arb_endpoint_fraction(value.lower())
    actual_upper = _arb_endpoint_fraction(value.upper())
    if lower > upper:
        raise ArithmeticError(f"reversed interval for {label}")
    if lower > actual_lower or upper < actual_upper:
        raise ArithmeticError(f"certificate does not enclose recomputed {label}")


def verify_certificate(certificate):
    if int(certificate["base"]) != BASE:
        raise ArithmeticError("unexpected dyadic base")
    max_N = int(certificate["max_N"])
    expected_targets = targets(max_N)
    stored_targets = tuple(int(row["N"]) for row in certificate["rows"])
    if stored_targets != expected_targets:
        raise ArithmeticError("certificate rows are not the complete dyadic target list")

    computed = compute(max_N, int(certificate["arb_bits"]))
    verdicts = []
    for j, row in enumerate(certificate["rows"]):
        N = int(row["N"])
        if int(row["j"]) != j or N != BASE * 2**j:
            raise ArithmeticError("invalid dyadic row index")
        p_N, p_2N, ratio = computed[N]
        _check_encloses(f"P_{N}", row["P_N"], p_N)
        _check_encloses(f"P_{2 * N}", row["P_2N"], p_2N)
        _check_encloses(f"P_{2 * N}/P_{N}", row["ratio"], ratio)

        ratio_lower = decode_fraction(row["ratio"]["lower"])
        ratio_upper = decode_fraction(row["ratio"]["upper"])
        if ratio_upper < Fraction(3, 4):
            verdict = "LT_3_OVER_4"
        elif ratio_lower > Fraction(3, 4):
            verdict = "GT_3_OVER_4"
        else:
            verdict = "OVERLAPS_3_OVER_4"
        verdicts.append(verdict)
    return computed, tuple(verdicts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--max-N", type=int, default=DEFAULT_MAX_N)
    parser.add_argument("--bits", type=int, default=192)
    args = parser.parse_args()

    if args.write_certificate:
        certificate = make_certificate(args.max_N, args.bits)
        args.certificate.write_text(json.dumps(certificate, indent=2) + "\n")
    else:
        certificate = json.loads(args.certificate.read_text())

    computed, verdicts = verify_certificate(certificate)
    print("cycle-247 directed dyadic scan; finite data only")
    for j, ((N, (_, _, ratio)), verdict) in enumerate(zip(computed.items(), verdicts)):
        print(f"j={j:2d} N={N:4d} P_{2*N}/P_{N} in {ratio.str(30)} {verdict}")


if __name__ == "__main__":
    main()
