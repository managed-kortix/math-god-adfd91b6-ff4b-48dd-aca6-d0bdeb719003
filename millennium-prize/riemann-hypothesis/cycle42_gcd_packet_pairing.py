#!/usr/bin/env python3
"""Certified finite tests for Cycle 42 gcd-packet domination pairings."""

import argparse
import json
from dataclasses import dataclass
from math import gcd

from flint import arb, ctx

from certify_complete_gram import RestrictedGram, mobius_sieve


@dataclass(frozen=True)
class Packet:
    kind: str
    key: tuple
    weight: object


def _suffix_tables(A, B, logs):
    beta_tail = [arb(0) for _ in range(B + 1)]
    beta_c_tail = [arb(0) for _ in range(B + 1)]
    for n in range(B - 1, A - 1, -1):
        beta = ((logs[n + 1] - logs[n])
                / (logs[n] * logs[n + 1] ** 2))
        beta_tail[n] = beta_tail[n + 1] + beta
        beta_c_tail[n] = (beta_c_tail[n + 1]
                          + beta * logs[n] * logs[n + 1])
    for n in range(A - 1, -1, -1):
        beta_tail[n] = beta_tail[A]
        beta_c_tail[n] = beta_c_tail[A]
    return beta_tail, beta_c_tail


def packet_census(A, B, bits=192):
    """Return exact-formula Arb enclosures for all nonzero packet weights."""
    if not 2 <= A < B:
        raise ValueError("require 2 <= A < B")
    ctx.prec = bits
    mu = mobius_sieve(B)
    logs = [arb(0)] + [arb(n).log() for n in range(1, B + 1)]
    beta_tail, beta_c_tail = _suffix_tables(A, B, logs)
    gram = RestrictedGram()

    def R(a, b):
        start = max(A, a, b)
        if start >= B:
            return arb(0)
        return beta_c_tail[start] - logs[a] * logs[b] * beta_tail[start]

    diagonal = []
    for a in range(1, B):
        if mu[a]:
            diagonal.append(Packet("diagonal", (a,), R(a, a) * gram.entry(a, a)))

    unfavorable = []
    favorable = []
    for p in range(1, B):
        if not mu[p]:
            continue
        for q in range(p + 1, B):
            if not mu[q] or gcd(p, q) != 1:
                continue
            weight = arb(0)
            for d in range(1, (B - 1) // q + 1):
                if mu[d * p] and mu[d * q]:
                    weight += (2 * R(d * p, d * q)
                               * gram.entry(d * p, d * q))
            if not weight > 0:
                raise ArithmeticError(f"packet {(p, q)} is not certified positive")
            packet = Packet("reduced", (p, q), weight)
            if mu[p] * mu[q] < 0:
                favorable.append(packet)
            else:
                unfavorable.append(packet)
    return diagonal, unfavorable, favorable


def _total(packets):
    return sum((packet.weight for packet in packets), arb(0))


def pairing_audit(A, B, bits=192):
    diagonal, equal_sign, opposite_sign = packet_census(A, B, bits)
    sources = diagonal + equal_sign
    source_weight = _total(sources)
    target_weight = _total(opposite_sign)
    return {
        "block": [A, B],
        "precision_bits": bits,
        "counts": {
            "diagonal": len(diagonal),
            "equal_sign": len(equal_sign),
            "unfavorable_total": len(sources),
            "opposite_sign": len(opposite_sign),
        },
        "weights": {
            "diagonal": _total(diagonal),
            "equal_sign": _total(equal_sign),
            "unfavorable_total": source_weight,
            "opposite_sign": target_weight,
            "deficit": source_weight - target_weight,
        },
        "injective_domination_obstructed_by_count": len(sources) > len(opposite_sign),
        "arbitrary_capacity_domination_obstructed_by_mass": source_weight > target_weight,
    }


def serializable(audit):
    return {
        **audit,
        "weights": {key: value.str(40) for key, value in audit["weights"].items()},
        "scope": ("finite certified packet-only obstruction; the omitted linear "
                  "term can still compensate, so this is not an RH claim"),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("blocks", nargs="*", default=["2:8", "2:16", "2:32"],
                        help="half-open blocks A:B")
    parser.add_argument("--bits", type=int, default=192)
    args = parser.parse_args()
    reports = []
    for block in args.blocks:
        A, B = map(int, block.split(":"))
        reports.append(serializable(pairing_audit(A, B, args.bits)))
    print(json.dumps(reports, indent=2))


if __name__ == "__main__":
    main()
