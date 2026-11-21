#!/usr/bin/env python3
"""Certified fixed-theta dyadic boundary-envelope projection scan.

For a dyadic block [a, 2a) and fixed 0 < theta < 1/2, this script studies

    E(a,h) = span{p_q : a-h <= q < 2a, mu(q)^2 = 1},

where p_q is the exact triangular divisor column in the Cycle 43 completed
square.  The family is affine-free.  Since E(a,h) is nested in h, its exact
projection is monotone; binary search locates the least integer width whose
Arb-certified projection reaches the negative budget.  An unresolved sign,
nonpositive Gram determinant, or failed solve aborts rather than becoming a
verdict.

This is a finite diagnostic only.  It proves neither an eventual envelope
bound nor the Riemann hypothesis.
"""

import argparse
import json
from pathlib import Path

from flint import arb, ctx

from cycle43_divisor_admission_multiprobe import (
    AFFINE,
    CompensatedBlock,
    certified_sign,
    interval_text,
    jsonable,
)

DEFAULT_STARTS = (32, 64, 128, 256, 512)


def set_fixed_theta(block, theta):
    """Replace the pilot theta and clear every theta-dependent cache."""
    block.theta = theta
    for n in block.scales:
        ratio_inverse = block.logs[n] / block.logs[n + 1]
        block.positive_weight[n] = 1 + ratio_inverse - 2 * theta
        block.eta[n] = (1 - 2 * theta) / block.positive_weight[n]
        block.negative_factor[n] = (
            2 * theta
            + (1 - 2 * theta) ** 2 / block.positive_weight[n]
        )
        if certified_sign(block.positive_weight[n]) != 1:
            raise RuntimeError(
                f"nonpositive completed-square coefficient at n={n}"
            )
    block._probe_gram.clear()
    block._correlation.clear()
    block._positive_energy = None
    block._negative_budget = None


def envelope_family(block, width):
    """All nonzero-Mobius labels q in [a-width,2a), without affine."""
    if not (0 <= width <= block.start - 1):
        raise ValueError("width must satisfy 0 <= width <= start-1")
    lower = block.start - width
    return tuple(
        q for q in block.labels
        if q != AFFINE and lower <= q < block.stop
    )


def envelope_certificate(block, width):
    family = envelope_family(block, width)
    projection, determinant = block.projection(family)
    margin = projection - block.negative_budget
    return {
        "width": width,
        "lower_label": block.start - width,
        "family": family,
        "rank": len(family),
        "projection": projection,
        "determinant": determinant,
        "negative_budget": block.negative_budget,
        "margin": margin,
        "projection_fraction_of_budget": projection / block.negative_budget,
        "verdict": "PASS" if certified_sign(margin) >= 0 else "FAIL",
    }


def first_passing_width(block):
    """Find the least passing width, or return None if the maximal span fails."""
    cache = {}

    def certificate(width):
        if width not in cache:
            cache[width] = envelope_certificate(block, width)
        return cache[width]

    maximum = block.start - 1
    if certificate(maximum)["verdict"] == "FAIL":
        return None, cache
    low, high = -1, maximum
    while high - low > 1:
        middle = (low + high) // 2
        if certificate(middle)["verdict"] == "PASS":
            high = middle
        else:
            low = middle
    # Minimality is certified by the adjacent signs, not assumed from floats.
    if high > 0 and certificate(high - 1)["verdict"] != "FAIL":
        raise RuntimeError("binary search did not certify minimality")
    return high, cache


def natural_width(start):
    """Certified integer ceil(start/log(start)), clipped to the search range."""
    value = (arb(start) / arb(start).log()).ceil()
    if not value.is_exact():
        raise RuntimeError("unresolved natural-width ceiling")
    # python-flint does not define int(arb); exact integer balls stringify safely.
    return min(start - 1, int(str(value).split(".")[0]))


def scan_start(start, theta, bits):
    block = CompensatedBlock(start, 2 * start, bits)
    set_fixed_theta(block, theta)
    first_width, cache = first_passing_width(block)
    natural = natural_width(start)
    requested = {0, natural, start - 1}
    if first_width is not None:
        requested.add(first_width)
        if first_width > 0:
            requested.add(first_width - 1)
    for width in requested:
        if width not in cache:
            cache[width] = envelope_certificate(block, width)
    return {
        "start": start,
        "stop": 2 * start,
        "theta": theta,
        "positive_energy": block.positive_energy,
        "negative_budget": block.negative_budget,
        "residual": block.residual,
        "current_only": cache[0],
        "natural_width": natural,
        "natural_width_certificate": cache[natural],
        "first_passing_width": first_width,
        "scaled_first_width": (
            None if first_width is None
            else arb(first_width) * arb(start).log() / start
        ),
        "predecessor_certificate": (
            None if first_width in (None, 0) else cache[first_width - 1]
        ),
        "threshold_certificate": (
            None if first_width is None else cache[first_width]
        ),
        "maximal_certificate": cache[start - 1],
    }


def run(starts=DEFAULT_STARTS, theta_text="2/5", bits=192):
    if bits < 128:
        raise ValueError("bits must be at least 128")
    starts = tuple(starts)
    if not starts or any(start < 2 for start in starts):
        raise ValueError("every start must be at least 2")
    ctx.prec = bits
    if "/" in theta_text:
        numerator, denominator = theta_text.split("/", 1)
        theta = arb(int(numerator)) / int(denominator)
    else:
        theta = arb(theta_text)
    if not (theta > 0 and theta < arb(1) / 2):
        raise ValueError("theta must satisfy 0 < theta < 1/2")
    rows = [scan_start(start, theta, bits) for start in starts]
    return {
        "scope": "certified finite diagnostic only; no eventual theorem or RH claim",
        "arb_precision_bits": bits,
        "theta": theta,
        "starts": starts,
        "family": "all squarefree q in [start-width,2*start), affine excluded",
        "verdict_policy": "Arb signs only; unresolved signs abort",
        "search_policy": "nested-family binary search, certified at h*-1 and h*",
        "rows": rows,
    }


def print_summary(payload):
    print("CERTIFIED FINITE DIAGNOSTIC ONLY; NOT AN RH PROOF")
    print(
        f"Arb precision={payload['arb_precision_bits']} bits; "
        f"theta={interval_text(payload['theta'], 20)}"
    )
    for row in payload["rows"]:
        current = row["current_only"]
        natural = row["natural_width_certificate"]
        threshold = row["threshold_certificate"]
        print(
            f"a={row['start']}: current rank={current['rank']} "
            f"margin={interval_text(current['margin'], 18)}; "
            f"ceil(a/log a)={row['natural_width']} rank={natural['rank']} "
            f"margin={interval_text(natural['margin'], 18)}"
        )
        if threshold is None:
            print("  no passing width in the declared historical envelope")
        else:
            predecessor = row["predecessor_certificate"]
            before = "none" if predecessor is None else interval_text(
                predecessor["margin"], 18
            )
            print(
                f"  h*={row['first_passing_width']}, "
                f"h* log(a)/a={interval_text(row['scaled_first_width'], 18)}, "
                f"margin(h*-1)={before}, "
                f"margin(h*)={interval_text(threshold['margin'], 18)}"
            )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--starts", type=int, nargs="+", default=DEFAULT_STARTS)
    parser.add_argument("--theta", default="2/5")
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    payload = run(args.starts, args.theta, args.bits)
    print_summary(payload)
    if args.json:
        args.json.write_text(
            json.dumps(jsonable(payload), indent=2) + "\n", encoding="ascii"
        )


if __name__ == "__main__":
    main()
