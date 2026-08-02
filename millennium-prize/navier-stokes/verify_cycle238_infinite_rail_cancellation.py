#!/usr/bin/env python3
"""Exact geometric-amplitude cancellation audit for Fibonacci rails."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = ROOT / "cycle238-infinite-rail-cancellation-certificate.json"


def add(p: tuple[int, int], q: tuple[int, int]) -> tuple[int, int]:
    return p[0] + q[0], p[1] + q[1]


def subtract(p: tuple[int, int], q: tuple[int, int]) -> tuple[int, int]:
    return p[0] - q[0], p[1] - q[1]


def det(p: tuple[int, int], q: tuple[int, int]) -> int:
    return p[0] * q[1] - p[1] * q[0]


def norm2(p: tuple[int, int]) -> int:
    return p[0] * p[0] + p[1] * p[1]


def paired_coefficient(p: tuple[int, int], q: tuple[int, int]) -> Fraction:
    return -det(p, q) * (Fraction(1, norm2(p)) - Fraction(1, norm2(q)))


def fibonacci_rails(count: int) -> list[tuple[int, int]]:
    fibonacci = [0, 1]
    for _ in range(count + 1):
        fibonacci.append(fibonacci[-1] + fibonacci[-2])
    return [(fibonacci[j + 1], fibonacci[j]) for j in range(1, count + 1)]


def rational(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def canonical(vector: tuple[int, int]) -> tuple[int, int]:
    if vector[0] < 0 or (vector[0] == 0 and vector[1] < 0):
        return -vector[0], -vector[1]
    return vector


def cancellation_equations(depth: int) -> list[dict[str, object]]:
    rails = fibonacci_rails(depth + 2)
    on_infinite_rail = set(rails)
    terms: dict[tuple[int, int], list[tuple[int, int, str, Fraction]]] = defaultdict(list)

    for i in range(depth):
        for j in range(i + 1, depth):
            left, right = rails[i], rails[j]
            sum_mode = add(left, right)
            difference_mode = subtract(right, left)
            sum_coefficient = paired_coefficient(left, right)
            difference_coefficient = paired_coefficient(right, (-left[0], -left[1]))
            if sum_mode not in on_infinite_rail and sum_coefficient:
                terms[canonical(sum_mode)].append((i + 1, j + 1, "sum", sum_coefficient))
            if difference_mode not in on_infinite_rail and difference_coefficient:
                terms[canonical(difference_mode)].append(
                    (i + 1, j + 1, "difference", difference_coefficient)
                )

    equations = []
    for mode in sorted(terms):
        combined: dict[int, Fraction] = defaultdict(Fraction)
        exact_terms = []
        for i, j, kind, coefficient in terms[mode]:
            exponent = i + j - 2
            combined[exponent] += coefficient
            exact_terms.append(
                {
                    "pair": [i, j],
                    "kind": kind,
                    "coefficient": rational(coefficient),
                    "geometric_exponent": exponent,
                }
            )
        polynomial = [
            {"exponent": exponent, "coefficient": rational(coefficient)}
            for exponent, coefficient in sorted(combined.items())
            if coefficient
        ]
        equations.append(
            {
                "mode": list(mode),
                "equation": "A^2*sum(c_e*r^e)=0",
                "polynomial_in_r": polynomial,
                "terms": exact_terms,
            }
        )
    return equations


def equation_digest(equations: list[dict[str, object]]) -> str:
    payload = json.dumps(equations, sort_keys=True, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-depth", type=int, default=12)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.max_depth < 3:
        parser.error("--max-depth must be at least 3")

    depth_certificates = []
    maximum_equations = []
    for depth in range(2, args.max_depth + 1):
        equations = cancellation_equations(depth)
        if depth == args.max_depth:
            maximum_equations = equations
        witness = next((equation for equation in equations if equation["mode"] == [1, 0]), None)
        if depth >= 2:
            if witness is None:
                raise RuntimeError("stable (1,0) obstruction disappeared")
            expected = [{"exponent": 1, "coefficient": "-3/10"}]
            if witness["polynomial_in_r"] != expected or len(witness["terms"]) != 1:
                raise RuntimeError("stable (1,0) obstruction changed")
        depth_certificates.append(
            {
                "depth": depth,
                "off_rail_equation_count": len(equations),
                "equation_sha256": equation_digest(equations),
                "saturated_ideal": "unit",
                "witness_mode": [1, 0],
            }
        )

    # The output (1,0)=k_2-k_1 has no other sum or difference representation.
    # A bounded exact search suffices: a difference with second coordinate zero
    # needs equal Fibonacci coordinates, whose only repeated positive value is
    # F_1=F_2=1. A sum cannot have second coordinate zero.
    bounded = fibonacci_rails(5)
    representations = []
    for i, left in enumerate(bounded, 1):
        for j, right in enumerate(bounded[i:], i + 1):
            if add(left, right) == (1, 0):
                representations.append(["sum", i, j])
            if subtract(right, left) == (1, 0):
                representations.append(["difference", i, j])
    if representations != [["difference", 1, 2]]:
        raise RuntimeError("uniqueness proof check failed")

    artifact = {
        "architecture": {
            "rails": "k_j=(F_(j+1),F_j), F_1=F_2=1",
            "real_even_amplitudes": "a_j=A*r^(j-1)",
            "nondegeneracy": "A*r!=0",
            "paired_euler_coefficient": "-det(p,q)*(1/|p|^2-1/|q|^2)",
        },
        "decision": {
            "exact_off_rail_cancellation": False,
            "first_obstructed_depth": 2,
            "extrapolates_to_infinite_depth": True,
        },
        "stable_unit_ideal_obstruction": {
            "mode": [1, 0],
            "unique_representation": "k_2-k_1",
            "equation": "(-3/10)*A^2*r=0",
            "normalized_generator": "g=A^2*r",
            "saturation_generator": "h=t*A^2*r^2-1",
            "groebner_basis_Q": ["1"],
            "bezout_identity": "t*r*g-h=1",
            "uniqueness_reason": "F_j=F_i only for {i,j}={1,2}; positive rail sums have positive second coordinate",
            "bounded_representations": representations,
        },
        "depth_certificates": depth_certificates,
        "max_depth": args.max_depth,
        "max_depth_exact_equations": maximum_equations,
    }
    args.output.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="ascii")

    print("Cycle 238 exact infinite Fibonacci-rail cancellation audit")
    print("depths checked: 2 through", args.max_depth)
    print("stable equation: (-3/10)*A^2*r = 0 at mode (1,0)")
    print("saturation certificate: t*r*(A^2*r) - (t*A^2*r^2-1) = 1")
    print("wrote", args.output)


if __name__ == "__main__":
    main()
