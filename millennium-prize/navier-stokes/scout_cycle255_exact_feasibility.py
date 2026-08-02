#!/usr/bin/env python3
"""Enumerate the frozen Cycle 255 analytic-feasibility grid exactly."""

import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


Q0_VALUES = (Fraction(33, 32), Fraction(17, 16), Fraction(9, 8), Fraction(5, 4))
SIGMAS = (Fraction(1, 16), Fraction(1, 24))
EPSILONS = (Fraction(1, 256), Fraction(1, 512), Fraction(1, 1024))
SPEC_NAME = "cycle-255-euler-fourier-tail-certificate-design.md"


def rational(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def profiles():
    for first in range(5):
        for suffix in itertools.product(range(-2, 3), repeat=4 - first):
            yield (0,) * first + (1,) + suffix


def low_norm(profile, q0):
    a1, a2, a3, a4, a5 = map(abs, profile)
    return (
        3 * (a1 + a2) * q0
        + 2 * a3 * q0**2
        + (5 * a3 + 10 * a4) * q0**3
        + 20 * a5 * q0**4
    ) / 64


def tail_norm(q0, sigma, epsilon):
    x = q0 * sigma
    finite_box = sum(
        x ** (abs(k1) + abs(k2))
        for k1 in range(-4, 5)
        for k2 in range(-4, 5)
    )
    return epsilon * (((1 + x) / (1 - x)) ** 2 - finite_box)


def grid_ceiling(value):
    numerator = (64 * value.numerator + value.denominator - 1) // value.denominator
    return Fraction(max(1, numerator), 64)


def first_tuple(bounds, terminal_time):
    for q0, minimum_m in bounds:
        if minimum_m > 4:
            continue
        # Lexicographic M then alpha makes alpha=M whenever a tuple exists.
        if q0 * (1 - minimum_m * terminal_time) > 1:
            return q0, minimum_m, minimum_m
    return None


def build_artifact(spec_path):
    all_profiles = list(profiles())
    assert len(all_profiles) == 781
    records = []
    time_counts = Counter()
    tuple_counts = Counter()
    q0_counts = Counter()
    member_index = 0
    for profile in all_profiles:
        for sigma in SIGMAS:
            for epsilon in EPSILONS:
                bounds = tuple(
                    (q0, grid_ceiling(low_norm(profile, q0) + tail_norm(q0, sigma, epsilon)))
                    for q0 in Q0_VALUES
                )
                for m in range(1, 33):
                    member_index += 1
                    terminal_time = Fraction(m, 16)
                    selected = first_tuple(bounds, terminal_time)
                    if selected is None:
                        continue
                    q0, bound, alpha = selected
                    record = {
                        "index": member_index,
                        "a": list(profile),
                        "sigma": rational(sigma),
                        "epsilon": rational(epsilon),
                        "T": rational(terminal_time),
                        "tuple": [rational(q0), rational(bound), rational(alpha)],
                    }
                    records.append(record)
                    time_counts[rational(terminal_time)] += 1
                    tuple_counts[",".join(record["tuple"])] += 1
                    q0_counts[rational(q0)] += 1
    total = member_index
    feasible = len(records)
    return {
        "format": "cycle255-exact-analytic-feasibility-v1",
        "scope": "exact rational test of (255.3) and q(T)>1; no PDE screen",
        "spec_sha256": hashlib.sha256(spec_path.read_bytes()).hexdigest(),
        "enumeration": {
            "profile_order": "first nonzero position 1..5, then suffix lexicographic over -2,-1,0,1,2",
            "inner_order": ["sigma:1/16,1/24", "epsilon:1/256,1/512,1/1024", "T:m/16,m=1..32"],
            "index_base": 1,
        },
        "grid": {
            "q0": [rational(x) for x in Q0_VALUES],
            "M": "j/64,1<=j<=256",
            "alpha": "j/64,1<=j<=256",
            "tuple_order": "q0 displayed order, then M increasing, then alpha increasing",
        },
        "counts": {
            "total": total,
            "feasible": feasible,
            "infeasible": total - feasible,
        },
        "diagnosis": {
            "empty": feasible == 0,
            "all_shortest_time_members_feasible": time_counts["1/16"] == 781 * 2 * 3,
            "feasible_fraction": rational(Fraction(feasible, total)),
            "interpretation": "nonempty; globally restrictive (over 93% rejected), but not restrictive at T=1/16; feasibility decreases with T",
        },
        "feasible_by_T": dict(sorted(time_counts.items(), key=lambda item: Fraction(item[0]))),
        "feasible_by_q0": {key: q0_counts[key] for key in map(rational, Q0_VALUES)},
        "lexicographic_tuple_distribution": dict(
            sorted(tuple_counts.items(), key=lambda item: tuple(Fraction(x) for x in item[0].split(",")))
        ),
        "feasible_records": records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("cycle255-exact-analytic-feasibility.json"),
    )
    args = parser.parse_args()
    spec_path = Path(__file__).with_name(SPEC_NAME)
    artifact = build_artifact(spec_path)
    args.output.write_text(json.dumps(artifact, indent=2, sort_keys=False) + "\n", encoding="ascii")
    print(f"wrote {args.output}")
    print(json.dumps(artifact["counts"], sort_keys=True))


if __name__ == "__main__":
    main()
