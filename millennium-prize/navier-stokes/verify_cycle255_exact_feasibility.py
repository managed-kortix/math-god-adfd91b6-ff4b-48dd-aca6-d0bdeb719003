#!/usr/bin/env python3
"""Independent exact verifier for the Cycle 255 feasibility artifact."""

import hashlib
import itertools
import json
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ARTIFACT = HERE / "cycle255-exact-analytic-feasibility.json"
SPEC = HERE / "cycle-255-euler-fourier-tail-certificate-design.md"


def text(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def exact_a(profile, q, sigma, epsilon):
    p = tuple(abs(x) for x in profile)
    low = (3 * (p[0] + p[1]) * q + 2 * p[2] * q**2 + (5 * p[2] + 10 * p[3]) * q**3 + 20 * p[4] * q**4) / 64
    x = q * sigma
    removed = sum(x ** (abs(i) + abs(j)) for i in range(-4, 5) for j in range(-4, 5))
    return low + epsilon * ((1 + x) ** 2 / (1 - x) ** 2 - removed)


def verify():
    supplied = json.loads(ARTIFACT.read_text(encoding="ascii"))
    if supplied["format"] != "cycle255-exact-analytic-feasibility-v1":
        raise AssertionError("unknown format")
    if supplied["spec_sha256"] != hashlib.sha256(SPEC.read_bytes()).hexdigest():
        raise AssertionError("spec digest mismatch")

    q_values = (F(33, 32), F(17, 16), F(9, 8), F(5, 4))
    sigmas = (F(1, 16), F(1, 24))
    epsilons = (F(1, 256), F(1, 512), F(1, 1024))
    expected_records = []
    times = Counter()
    tuples = Counter()
    q_counts = Counter()
    index = 0
    for first in range(5):
        for suffix in itertools.product((-2, -1, 0, 1, 2), repeat=4 - first):
            profile = (0,) * first + (1,) + suffix
            for sigma in sigmas:
                for epsilon in epsilons:
                    bounds = []
                    for q in q_values:
                        norm = exact_a(profile, q, sigma, epsilon)
                        j = max(1, (64 * norm.numerator + norm.denominator - 1) // norm.denominator)
                        bounds.append((q, j, F(j, 64)))
                    for m in range(1, 33):
                        index += 1
                        T = F(m, 16)
                        chosen = None
                        for q, j, M in bounds:
                            if j <= 256 and q * (1 - M * T) > 1:
                                chosen = (q, M, M)
                                break
                        if chosen is None:
                            continue
                        row = {
                            "index": index,
                            "a": list(profile),
                            "sigma": text(sigma),
                            "epsilon": text(epsilon),
                            "T": text(T),
                            "tuple": [text(x) for x in chosen],
                        }
                        expected_records.append(row)
                        times[text(T)] += 1
                        tuples[",".join(row["tuple"])] += 1
                        q_counts[text(chosen[0])] += 1

    if index != 149952:
        raise AssertionError("family cardinality mismatch")
    if supplied["feasible_records"] != expected_records:
        raise AssertionError("feasible record mismatch")
    expected_counts = {"total": index, "feasible": len(expected_records), "infeasible": index - len(expected_records)}
    if supplied["counts"] != expected_counts:
        raise AssertionError("count mismatch")
    expected_times = dict(sorted(times.items(), key=lambda item: F(item[0])))
    if supplied["feasible_by_T"] != expected_times:
        raise AssertionError("T distribution mismatch")
    expected_tuples = dict(sorted(tuples.items(), key=lambda item: tuple(F(x) for x in item[0].split(","))))
    if supplied["lexicographic_tuple_distribution"] != expected_tuples:
        raise AssertionError("tuple distribution mismatch")
    expected_q = {text(q): q_counts[text(q)] for q in q_values}
    if supplied["feasible_by_q0"] != expected_q:
        raise AssertionError("q0 distribution mismatch")
    if supplied["diagnosis"]["empty"] or times["1/16"] != 4686:
        raise AssertionError("diagnosis mismatch")
    if supplied["diagnosis"]["feasible_fraction"] != text(F(len(expected_records), index)):
        raise AssertionError("feasible fraction mismatch")
    print(f"PASS exact Cycle255 feasibility: {len(expected_records)}/{index}")


if __name__ == "__main__":
    try:
        verify()
    except Exception as exc:
        print(f"FAIL CLOSED: {exc}", file=sys.stderr)
        raise SystemExit(1)
