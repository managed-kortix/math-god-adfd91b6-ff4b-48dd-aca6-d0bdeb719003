#!/usr/bin/env python3
"""Generate the frozen exact Cycle 204 S2 Navier--Stokes polynomial system."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SUPPORT_PATH = ROOT / "cycle204_s2_support.json"
EQUATIONS_PATH = ROOT / "cycle204_s2_equations.json"
ZERO_MONOMIAL = ()


def add_wave(left, right):
    return tuple(a + b for a, b in zip(left, right))


def neg_wave(wave):
    return tuple(-value for value in wave)


def wave_key(wave):
    return (wave[2], wave[1], wave[0])


def orbit_representative(wave):
    opposite = neg_wave(wave)
    return min(wave, opposite, key=wave_key)


def wave_text(wave):
    return ",".join(str(value) for value in wave)


def fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


class Poly:
    def __init__(self, terms=None):
        self.terms = {
            tuple(monomial): Fraction(coefficient)
            for monomial, coefficient in (terms or {}).items()
            if coefficient
        }

    @classmethod
    def constant(cls, value):
        value = Fraction(value)
        return cls({ZERO_MONOMIAL: value}) if value else cls()

    @classmethod
    def variable(cls, index):
        return cls({(index,): Fraction(1)})

    def __add__(self, other):
        other = as_poly(other)
        result = defaultdict(Fraction, self.terms)
        for monomial, coefficient in other.terms.items():
            result[monomial] += coefficient
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({monomial: -coefficient for monomial, coefficient in self.terms.items()})

    def __sub__(self, other):
        return self + (-as_poly(other))

    def __rsub__(self, other):
        return as_poly(other) - self

    def __mul__(self, other):
        other = as_poly(other)
        result = defaultdict(Fraction)
        for left, a in self.terms.items():
            for right, b in other.terms.items():
                result[tuple(sorted(left + right))] += a * b
        return Poly(result)

    __rmul__ = __mul__

    def is_zero(self):
        return not self.terms


def as_poly(value):
    return value if isinstance(value, Poly) else Poly.constant(value)


class GaussianPoly:
    def __init__(self, real=0, imag=0):
        self.real = as_poly(real)
        self.imag = as_poly(imag)

    @classmethod
    def variable(cls, real_index, imag_index):
        return cls(Poly.variable(real_index), Poly.variable(imag_index))

    def conjugate(self):
        return GaussianPoly(self.real, -self.imag)

    def __add__(self, other):
        other = as_gaussian(other)
        return GaussianPoly(self.real + other.real, self.imag + other.imag)

    __radd__ = __add__

    def __neg__(self):
        return GaussianPoly(-self.real, -self.imag)

    def __sub__(self, other):
        return self + (-as_gaussian(other))

    def __rsub__(self, other):
        return as_gaussian(other) - self

    def __mul__(self, other):
        other = as_gaussian(other)
        return GaussianPoly(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    __rmul__ = __mul__

    def is_zero(self):
        return self.real.is_zero() and self.imag.is_zero()


def as_gaussian(value):
    return value if isinstance(value, GaussianPoly) else GaussianPoly(value)


ZERO = GaussianPoly()


def vector_add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def vector_scale(value, vector):
    return tuple(value * entry for entry in vector)


def vector_dot(left, right):
    return sum((a * b for a, b in zip(left, right)), ZERO)


def project(wave, vector):
    norm_squared = sum(value * value for value in wave)
    radial = vector_dot(wave, vector)
    return tuple(entry - Fraction(axis, norm_squared) * radial for axis, entry in zip(wave, vector))


def sums(left, right):
    return {add_wave(a, b) for a in left for b in right} - {(0, 0, 0)}


def polarization_basis(wave):
    x, y, _ = wave
    divisor = math.gcd(abs(x), abs(y))
    planar = (Fraction(-y, divisor), Fraction(x, divisor), Fraction(0))
    vertical = (Fraction(0), Fraction(0), Fraction(1))
    return planar, vertical


def seed_field():
    e2 = (GaussianPoly(0), GaussianPoly(1), GaussianPoly(0))
    e3 = (GaussianPoly(0), GaussianPoly(0), GaussianPoly(1))
    field = {}
    for x in (-6, -2, 2, 6):
        field[(x, 0, 0)] = e2
    for wave, coefficient in {
        (-2, 1, 0): 1,
        (2, 1, 0): -1,
        (2, -1, 0): 1,
        (-2, -1, 0): -1,
    }.items():
        field[wave] = vector_scale(GaussianPoly(coefficient), e3)
    return field


def independent_seed_terminal_derivatives(terminals):
    """Compute terminal derivatives directly from the real seed coefficient table."""
    e2 = (Fraction(0), Fraction(1), Fraction(0))
    e3 = (Fraction(0), Fraction(0), Fraction(1))
    field = {}
    for x in (-6, -2, 2, 6):
        field[(x, 0, 0)] = e2
    for wave, coefficient in {
        (-2, 1, 0): 1,
        (2, 1, 0): -1,
        (2, -1, 0): 1,
        (-2, -1, 0): -1,
    }.items():
        field[wave] = tuple(Fraction(coefficient) * entry for entry in e3)

    derivatives = {}
    for wave in terminals:
        convolution = [Fraction(0), Fraction(0), Fraction(0)]
        for left, left_value in field.items():
            right = tuple(wave[index] - left[index] for index in range(3))
            if right not in field:
                continue
            dot = sum(left_value[index] * right[index] for index in range(3))
            for index in range(3):
                convolution[index] += dot * field[right][index]
        radial = sum(Fraction(wave[index]) * convolution[index] for index in range(3))
        norm_squared = sum(axis * axis for axis in wave)
        projected = tuple(
            convolution[index] - Fraction(wave[index], norm_squared) * radial
            for index in range(3)
        )
        derivatives[wave] = tuple((Fraction(0), -entry) for entry in projected)
    return derivatives


def make_support():
    seed = set(seed_field())
    support = seed | sums(seed, seed)
    u2 = sums(support, support)
    u3 = sums(support, u2)
    terminals = {
        (-8, 1, 0), (8, 1, 0), (8, -1, 0), (-8, -1, 0)
    }
    helper_orbits = sorted(
        {orbit_representative(wave) for wave in support - seed}, key=wave_key
    )
    terminal_orbits = {orbit_representative(wave) for wave in terminals}
    variables = []
    for orbit_index, representative in enumerate(helper_orbits):
        status = "pinned_zero_terminal" if representative in terminal_orbits else "free_completion"
        for basis_index, basis_name in enumerate(("planar", "vertical")):
            for part in ("re", "im"):
                variables.append({
                    "id": len(variables),
                    "name": f"q1_o{orbit_index}_{basis_name}_{part}",
                    "orbit_representative": list(representative),
                    "basis": basis_index,
                    "part": part,
                    "status": status,
                })
    data = {
        "schema": "cycle204-s2-support-v1",
        "parameters": {"R": 1, "Y": 1, "nu": 1},
        "definitions": {
            "K0": "occupied Cycle 177 seed modes",
            "S2": "(K0 union (K0+K0)) minus zero",
            "U2": "(S2+S2) minus zero",
            "U3": "(S2+U2) minus zero",
        },
        "terminal_policy": {
            "waves": [list(wave) for wave in sorted(terminals, key=wave_key)],
            "reconciliation": (
                "Terminal Q1 coordinate slots are retained in the frozen support and variable ledger, "
                "but are pinned to zero before polynomial expansion; they are not completion freedoms."
            ),
        },
        "counts": {
            "K0_modes": len(seed),
            "S2_modes": len(support),
            "S2_orbits": len(support) // 2,
            "Q1_helper_orbits_declared": len(helper_orbits),
            "Q1_terminal_orbits_pinned_zero": len(terminal_orbits),
            "Q1_free_orbits": len(helper_orbits) - len(terminal_orbits),
            "Q1_variables_declared": len(variables),
            "Q1_variables_free": sum(row["status"] == "free_completion" for row in variables),
            "U2_modes": len(u2),
            "U3_modes": len(u3),
            "tested_union_modes": len(support | u2 | u3),
            "outside_S2_modes": len((u2 | u3) - support),
        },
        "sets": {
            "K0": [list(wave) for wave in sorted(seed, key=wave_key)],
            "S2": [list(wave) for wave in sorted(support, key=wave_key)],
            "U2": [list(wave) for wave in sorted(u2, key=wave_key)],
            "U3": [list(wave) for wave in sorted(u3, key=wave_key)],
        },
        "variables": variables,
    }
    return data, seed, support, u2, u3, terminals, helper_orbits, terminal_orbits


def make_initial_field(support_data, seed, support, helper_orbits, terminal_orbits):
    field = seed_field()
    variable_rows = support_data["variables"]
    lookup = {(tuple(row["orbit_representative"]), row["basis"], row["part"]): row["id"] for row in variable_rows}
    for representative in helper_orbits:
        if representative in terminal_orbits:
            amplitude = (ZERO, ZERO)
        else:
            amplitude = tuple(
                GaussianPoly.variable(
                    lookup[(representative, basis_index, "re")],
                    lookup[(representative, basis_index, "im")],
                )
                for basis_index in range(2)
            )
        basis = polarization_basis(representative)
        value = tuple(sum((amplitude[j] * basis[j][axis] for j in range(2)), ZERO) for axis in range(3))
        field[representative] = value
        field[neg_wave(representative)] = tuple(entry.conjugate() for entry in value)
    assert set(field) == support
    return field


def navier(field, outputs):
    result = {}
    occupied = list(field)
    for wave in outputs:
        value = vector_scale(GaussianPoly(-sum(axis * axis for axis in wave)), field.get(wave, (ZERO, ZERO, ZERO)))
        nonlinear = (ZERO, ZERO, ZERO)
        for left in occupied:
            right = tuple(wave[index] - left[index] for index in range(3))
            if right not in field:
                continue
            nonlinear = vector_add(
                nonlinear,
                vector_scale(vector_dot(field[left], right), field[right]),
            )
        result[wave] = vector_add(value, vector_scale(GaussianPoly(0, -1), project(wave, nonlinear)))
    return result


def navier_derivative(field, direction, outputs):
    result = {}
    field_modes = list(field)
    direction_modes = list(direction)
    for wave in outputs:
        value = vector_scale(GaussianPoly(-sum(axis * axis for axis in wave)), direction.get(wave, (ZERO, ZERO, ZERO)))
        nonlinear = (ZERO, ZERO, ZERO)
        for left in direction_modes:
            right = tuple(wave[index] - left[index] for index in range(3))
            if right in field:
                nonlinear = vector_add(nonlinear, vector_scale(vector_dot(direction[left], right), field[right]))
        for left in field_modes:
            right = tuple(wave[index] - left[index] for index in range(3))
            if right in direction:
                nonlinear = vector_add(nonlinear, vector_scale(vector_dot(field[left], right), direction[right]))
        result[wave] = vector_add(value, vector_scale(GaussianPoly(0, -1), project(wave, nonlinear)))
    return result


def independent_components(wave):
    return (1, 2) if wave[0] else (0, 2)


def primitive_polynomial(poly):
    if poly.is_zero():
        return None
    denominator_lcm = 1
    for coefficient in poly.terms.values():
        denominator_lcm = math.lcm(denominator_lcm, coefficient.denominator)
    integers = {monomial: int(coefficient * denominator_lcm) for monomial, coefficient in poly.terms.items()}
    divisor = 0
    for coefficient in integers.values():
        divisor = math.gcd(divisor, abs(coefficient))
    integers = {monomial: coefficient // divisor for monomial, coefficient in integers.items()}
    leading = min(integers)
    if integers[leading] < 0:
        integers = {monomial: -coefficient for monomial, coefficient in integers.items()}
    return tuple(sorted(integers.items()))


def serialize_polynomial(primitive, variable_names):
    return [
        {
            "coefficient": str(coefficient),
            "monomial": [variable_names[index] for index in monomial],
        }
        for monomial, coefficient in primitive
    ]


def make_equations(support_data, seed, support, u2, u3, terminals, helper_orbits, terminal_orbits):
    field = make_initial_field(support_data, seed, support, helper_orbits, terminal_orbits)
    first = navier(field, u2)
    second = navier_derivative(field, first, u3)
    variable_names = [row["name"] for row in support_data["variables"]]
    equations = []
    seen = {}
    raw_scalar_count = 0

    def emit(poly, source):
        nonlocal raw_scalar_count
        raw_scalar_count += 1
        primitive = primitive_polynomial(poly)
        if primitive is None:
            return
        if primitive in seen:
            seen[primitive]["sources"].append(source)
            return
        row = {
            "id": f"e{len(equations):04d}",
            "sources": [source],
            "degree": max((len(monomial) for monomial, _ in primitive), default=0),
            "terms": serialize_polynomial(primitive, variable_names),
        }
        equations.append(row)
        seen[primitive] = row

    outside = (u2 | u3) - support
    for order, jet in ((1, first), (2, second)):
        available = u2 if order == 1 else u3
        for wave in sorted(outside & available, key=wave_key):
            if wave != orbit_representative(wave):
                continue
            for component in independent_components(wave):
                emit(jet[wave][component].real, {"kind": "closure", "order": order, "wave": list(wave), "component": component, "part": "real"})
                emit(jet[wave][component].imag, {"kind": "closure", "order": order, "wave": list(wave), "component": component, "part": "imag"})

    independently_computed = independent_seed_terminal_derivatives(terminals)
    assert independently_computed == {
        (-8, -1, 0): ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)), (Fraction(0), Fraction(-1))),
        (8, -1, 0): ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)), (Fraction(0), Fraction(1))),
        (-8, 1, 0): ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)), (Fraction(0), Fraction(-1))),
        (8, 1, 0): ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)), (Fraction(0), Fraction(1))),
    }
    for wave, target_components in independently_computed.items():
        mate = independently_computed[neg_wave(wave)]
        assert mate == tuple((real, -imag) for real, imag in target_components)
        representative = orbit_representative(wave)
        if wave != representative:
            continue
        target = tuple(GaussianPoly(real, imag) for real, imag in target_components)
        for component in independent_components(wave):
            difference = first[wave][component] - target[component]
            emit(difference.real, {"kind": "terminal_normalization", "order": 1, "wave": list(wave), "component": component, "part": "real"})
            emit(difference.imag, {"kind": "terminal_normalization", "order": 1, "wave": list(wave), "component": component, "part": "imag"})

    contradictions = [row["id"] for row in equations if row["degree"] == 0]
    degree_counts = defaultdict(int)
    for row in equations:
        degree_counts[str(row["degree"])] += 1
    return {
        "schema": "cycle204-s2-equations-v1",
        "coefficient_domain": "Z after exact Gaussian-rational expansion and primitive denominator clearing",
        "variable_order": variable_names,
        "active_variables": [row["name"] for row in support_data["variables"] if row["status"] == "free_completion"],
        "eliminated_initial_constraints": {
            "seed": "K0 coefficients are substituted exactly",
            "terminal": "all declared terminal Q1 coordinates are substituted as zero",
            "reality": "negative modes are substituted as Gaussian conjugates",
            "divergence_free": "each orbit uses the recorded two-vector rational basis",
        },
        "terminal_normalization": {
            "P1[-8,-1,0]": ["0", "0", "-i"],
            "P1[8,-1,0]": ["0", "0", "+i"],
            "reality_mates": {
                "P1[-8,1,0]": ["0", "0", "-i"],
                "P1[8,1,0]": ["0", "0", "+i"],
            },
            "note": "All four values are independently recomputed from the seed convolution; the two y=-1 modes represent the Fourier-reality orbits.",
        },
        "simplification": {
            "raw_real_scalar_slots": raw_scalar_count,
            "zero_slots_removed": raw_scalar_count - sum(len(row["sources"]) for row in equations),
            "duplicate_nonzero_slots_merged": sum(len(row["sources"]) - 1 for row in equations),
            "primitive_equations": len(equations),
            "degree_counts": dict(sorted(degree_counts.items())),
            "trivial_contradictions": contradictions,
        },
        "equations": equations,
    }


def canonical_bytes(data):
    return (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("ascii")


def digest(data):
    return hashlib.sha256(canonical_bytes(data)).hexdigest()


def verify_generated(support_data, equations_data):
    counts = support_data["counts"]
    assert counts == {
        "K0_modes": 8,
        "S2_modes": 30,
        "S2_orbits": 15,
        "Q1_helper_orbits_declared": 11,
        "Q1_terminal_orbits_pinned_zero": 2,
        "Q1_free_orbits": 9,
        "Q1_variables_declared": 44,
        "Q1_variables_free": 36,
        "U2_modes": 122,
        "U3_modes": 278,
        "tested_union_modes": 278,
        "outside_S2_modes": 248,
    }
    variables = support_data["variables"]
    free_names = {row["name"] for row in variables if row["status"] == "free_completion"}
    pinned_names = {row["name"] for row in variables if row["status"] == "pinned_zero_terminal"}
    assert len(free_names) == 36 and len(pinned_names) == 8
    assert set(equations_data["active_variables"]) == free_names
    used_names = {
        name
        for equation in equations_data["equations"]
        for term in equation["terms"]
        for name in term["monomial"]
    }
    assert not (used_names & pinned_names)
    assert equations_data["simplification"] == {
        "raw_real_scalar_slots": 688,
        "zero_slots_removed": 152,
        "duplicate_nonzero_slots_merged": 22,
        "primitive_equations": 514,
        "degree_counts": {"1": 44, "2": 238, "3": 232},
        "trivial_contradictions": [],
    }
    assert equations_data["terminal_normalization"] == {
        "P1[-8,-1,0]": ["0", "0", "-i"],
        "P1[8,-1,0]": ["0", "0", "+i"],
        "reality_mates": {
            "P1[-8,1,0]": ["0", "0", "-i"],
            "P1[8,1,0]": ["0", "0", "+i"],
        },
        "note": "All four values are independently recomputed from the seed convolution; the two y=-1 modes represent the Fourier-reality orbits.",
    }


def generate():
    support_args = make_support()
    support_data = support_args[0]
    equations_data = make_equations(*support_args)
    support_data["sha256_without_this_field"] = digest(support_data)
    equations_data["support_sha256"] = digest(support_data)
    equations_data["sha256_without_this_field"] = digest(equations_data)
    verify_generated(support_data, equations_data)
    return support_data, equations_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare regenerated bytes with committed JSON")
    args = parser.parse_args()
    support_data, equations_data = generate()
    outputs = ((SUPPORT_PATH, support_data), (EQUATIONS_PATH, equations_data))
    if args.check:
        for path, data in outputs:
            if not path.exists() or path.read_bytes() != canonical_bytes(data):
                raise SystemExit(f"replay mismatch: {path}")
        print("Cycle 204 S2 replay matches both committed JSON files")
    else:
        for path, data in outputs:
            path.write_bytes(canonical_bytes(data))
        print("Cycle 204 frozen exact S2 system")
        print("support counts:", support_data["counts"])
        print("equation simplification:", equations_data["simplification"])
        print("wrote", SUPPORT_PATH.name, "and", EQUATIONS_PATH.name)


if __name__ == "__main__":
    main()
