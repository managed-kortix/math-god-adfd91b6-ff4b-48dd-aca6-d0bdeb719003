#!/usr/bin/env python3
"""Generate and preflight the frozen C266-3DDE1 numerical screen."""

import argparse
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path


Complex = tuple[Fraction, Fraction]
Vector = tuple[Complex, Complex, Complex]


def cadd(a: Complex, b: Complex) -> Complex:
    return a[0] + b[0], a[1] + b[1]


def cmul(a: Complex, b: Complex) -> Complex:
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def cscale(a: Complex, q: Fraction) -> Complex:
    return a[0] * q, a[1] * q


def vadd(a: Vector, b: Vector) -> Vector:
    return tuple(cadd(x, y) for x, y in zip(a, b))  # type: ignore[return-value]


def vscale(a: Vector, q: Fraction) -> Vector:
    return tuple(cscale(x, q) for x in a)  # type: ignore[return-value]


ZERO: Complex = (Fraction(0), Fraction(0))
ZV: Vector = (ZERO, ZERO, ZERO)


def add_mode(field: dict[tuple[int, int, int], Vector], k, component, value):
    vector = list(field.get(k, ZV))
    vector[component] = cadd(vector[component], value)
    field[k] = tuple(vector)


def exponential_product(factors):
    terms = {(0, 0, 0): (Fraction(1), Fraction(0))}
    for axis, frequency, kind in factors:
        expanded = {}
        for k, coefficient in terms.items():
            for sign in (-1, 1):
                shifted = list(k)
                shifted[axis] += sign * frequency
                if kind == "cos":
                    factor = (Fraction(1, 2), Fraction(0))
                else:
                    factor = (Fraction(0), Fraction(-sign, 2))
                value = cmul(coefficient, factor)
                key = tuple(shifted)
                expanded[key] = cadd(expanded.get(key, ZERO), value)
        terms = expanded
    return terms


def kida_pelz() -> dict[tuple[int, int, int], Vector]:
    field = {}
    specifications = (
        (0, 1, ((0, 1, "sin"), (1, 3, "cos"), (2, 1, "cos"))),
        (0, -1, ((0, 1, "sin"), (1, 1, "cos"), (2, 3, "cos"))),
        (1, 1, ((1, 1, "sin"), (2, 3, "cos"), (0, 1, "cos"))),
        (1, -1, ((1, 1, "sin"), (2, 1, "cos"), (0, 3, "cos"))),
        (2, 1, ((2, 1, "sin"), (0, 3, "cos"), (1, 1, "cos"))),
        (2, -1, ((2, 1, "sin"), (0, 1, "cos"), (1, 3, "cos"))),
    )
    for component, sign, factors in specifications:
        for k, value in exponential_product(factors).items():
            add_mode(field, k, component, cscale(value, Fraction(sign)))
    return {k: v for k, v in field.items() if v != ZV}


def euler_rhs(field: dict[tuple[int, int, int], Vector]):
    raw: dict[tuple[int, int, int], Vector] = {}
    for p, vp in field.items():
        for r, vr in field.items():
            k = tuple(p[j] + r[j] for j in range(3))
            if k == (0, 0, 0):
                continue
            dot = ZERO
            for j in range(3):
                dot = cadd(dot, cscale(vp[j], Fraction(r[j])))
            contribution = tuple(cmul((Fraction(0), -1), cmul(dot, x)) for x in vr)
            raw[k] = vadd(raw.get(k, ZV), contribution)  # type: ignore[arg-type]
    projected = {}
    for k, value in raw.items():
        k2 = sum(x * x for x in k)
        dot = ZERO
        for j in range(3):
            dot = cadd(dot, cscale(value[j], Fraction(k[j])))
        result = tuple(
            cadd(value[j], cscale(dot, Fraction(-k[j], k2))) for j in range(3)
        )
        result = tuple(result)
        if result != ZV:
            projected[k] = result
    return projected


def phase_factor(k, phase_bits) -> Complex:
    exponent = sum(k[j] * phase_bits[j] for j in range(3)) % 4
    return ((Fraction(1), ZERO[0]), (ZERO[0], Fraction(1)),
            (Fraction(-1), ZERO[0]), (ZERO[0], Fraction(-1)))[exponent]


def profile_field(base, tangent, a, b, phase_bits):
    result = dict(base)
    for k, value in tangent.items():
        result[k] = vadd(result.get(k, ZV), vscale(value, Fraction(a, 64)))
    if b:
        for k, value in base.items():
            doubled = tuple(2 * x for x in k)
            phased = tuple(cmul(phase_factor(k, phase_bits), x) for x in value)
            result[doubled] = vadd(result.get(doubled, ZV), vscale(phased, b))
    return {k: v for k, v in result.items() if v != ZV}


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def encoded_field(field):
    rows = []
    for k in sorted(field):
        rows.append({
            "k": list(k),
            "v": [[[fraction_text(z[0]), fraction_text(z[1])] for z in field[k]][j]
                  for j in range(3)],
        })
    return rows


def generate_family():
    base = kida_pelz()
    tangent = euler_rhs(base)
    profiles = []
    index = 0
    for a in (-2, -1, 1, 2):
        for b in (Fraction(-1, 4), Fraction(-1, 8), Fraction(0),
                  Fraction(1, 8), Fraction(1, 4)):
            phases = ((0, 0, 0),) if b == 0 else tuple(
                (x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)
            )
            for phase in phases:
                field = profile_field(base, tangent, a, b, phase)
                profiles.append({
                    "index": index,
                    "a": a,
                    "b": fraction_text(b),
                    "phase_pi_over_2": list(phase),
                    "coefficients": encoded_field(field),
                })
                index += 1
    return {
        "format": "C266-3DDE1-exact-family-v1",
        "coefficient_order": "lexicographic k, then velocity component x/y/z, then real/imaginary",
        "number_encoding": "reduced signed rational strings; Gaussian rational as [real,imaginary]",
        "profile_order": "a=-2,-1,1,2; b=-1/4,-1/8,0,1/8,1/4; nonzero-b phase bits lexicographic",
        "profiles": profiles,
    }


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def preflight(manifest, family_path, output_path):
    manifest_raw = canonical_bytes(manifest)
    family_raw = family_path.read_bytes()
    family = json.loads(family_raw.decode("ascii"))
    digest = hashlib.sha256(family_raw).hexdigest()
    if digest != manifest["family"]["sha256"]:
        raise ValueError("exact-family digest mismatch")
    if len(family["profiles"]) != manifest["family"]["profile_count"]:
        raise ValueError("profile count mismatch")
    steps = sum(
        manifest["family"]["profile_count"]
        * int(Fraction(str(manifest["horizons"][-1])) / Fraction(level["step_size"]))
        for level in manifest["levels"]
    )
    minimum_rhs = 2 * steps
    available_cores = os.cpu_count() or 1
    feasible = (
        available_cores >= manifest["resource_policy"]["minimum_logical_cores"]
        and minimum_rhs <= manifest["resource_policy"]["maximum_minimum_rhs_evaluations"]
    )
    outcome = {
        "format": "C266-3DDE1-outcome-v1",
        "status": "NUMERICAL_ONLY",
        "pde_certificate": False,
        "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "family_sha256": digest,
        "family_size": len(family["profiles"]),
        "preflight": {
            "available_logical_cores": available_cores,
            "minimum_midpoint_steps": steps,
            "minimum_rhs_evaluations": minimum_rhs,
            "resource_feasible": feasible,
        },
        "execution": "NOT_RUN_RESOURCE_INFEASIBLE" if not feasible else "AUTHORIZED_NOT_IMPLEMENTED",
        "trajectories_generated": 0,
        "promotions": [],
        "stop_rule_triggered": "RESOURCE_PREFLIGHT_FAIL" if not feasible else None,
        "claim": "No Euler, Navier-Stokes, or Millennium result.",
    }
    output_path.write_text(json.dumps(outcome, indent=2, sort_keys=True) + "\n", encoding="ascii")
    if feasible:
        raise RuntimeError("resource preflight passed, but trajectory backend is unavailable")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate-family", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--family", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.generate_family:
        args.generate_family.write_bytes(canonical_bytes(generate_family()))
        return
    if not all((args.manifest, args.family, args.output)):
        parser.error("preflight requires --manifest, --family, and --output")
    manifest = json.loads(args.manifest.read_text(encoding="ascii"))
    preflight(manifest, args.family, args.output)


if __name__ == "__main__":
    main()
