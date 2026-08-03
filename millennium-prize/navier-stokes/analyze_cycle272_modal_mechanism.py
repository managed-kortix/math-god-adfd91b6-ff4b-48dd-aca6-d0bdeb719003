#!/usr/bin/env python3
"""Exact modal decomposition and deletion audit for the Cycle 272 datum."""

import json
from collections import defaultdict
from copy import deepcopy
from fractions import Fraction

from certify_p3_admission import (
    EXAMPLE,
    add_complex,
    enclose,
    frac,
    mul_complex,
    pressure_coefficients,
    qarb,
    scalar_convolution,
    scale_complex,
)


LABELS = ("Sx", "Sy", "A", "B", "C", "D", "E")
CENTER = Fraction(65536)
DEGREE = 6


def signed_mode_atoms(modes):
    atoms = []
    for label, mode in zip(LABELS, modes):
        k = tuple(mode["k"])
        amplitude = tuple(frac(value) for value in mode["amplitude"])
        if mode["kind"] == "cos":
            factors = ((1, (Fraction(1, 2), Fraction(0))),
                       (-1, (Fraction(1, 2), Fraction(0))))
        else:
            factors = ((1, (Fraction(0), Fraction(-1, 2))),
                       (-1, (Fraction(0), Fraction(1, 2))))
        for sign, factor in factors:
            wave = tuple(sign * value for value in k)
            vector = tuple(scale_complex(factor, value) for value in amplitude)
            atoms.append((label, wave, vector))
    return atoms


def combine_velocity(atoms):
    velocity = {}
    for _, wave, vector in atoms:
        total = velocity.setdefault(
            wave, [(Fraction(0), Fraction(0)) for _ in range(3)]
        )
        for axis in range(3):
            total[axis] = add_complex(total[axis], vector[axis])
    return velocity


def pressure_seed_atoms(atoms):
    seeds = defaultdict(lambda: (Fraction(0), Fraction(0)))
    for left_label, left_wave, left_vector in atoms:
        for right_label, right_wave, right_vector in atoms:
            pressure_wave = tuple(left_wave[i] + right_wave[i] for i in range(3))
            wave_square = sum(value * value for value in pressure_wave)
            if wave_square == 0:
                continue
            pressure = (Fraction(0), Fraction(0))
            for i in range(3):
                for j in range(3):
                    term = mul_complex(left_vector[i], right_vector[j])
                    pressure = add_complex(
                        pressure,
                        scale_complex(
                            term,
                            Fraction(-pressure_wave[i] * pressure_wave[j], wave_square),
                        ),
                    )
            if pressure == (0, 0):
                continue
            for adv_label, adv_wave, adv_vector in atoms:
                output_wave = tuple(adv_wave[i] + pressure_wave[i] for i in range(3))
                derivative_pressure = tuple(
                    mul_complex(pressure, (Fraction(0), Fraction(value)))
                    for value in pressure_wave
                )
                h_value = (Fraction(0), Fraction(0))
                for axis in range(3):
                    h_value = add_complex(
                        h_value, mul_complex(adv_vector[axis], derivative_pressure[axis])
                    )
                if h_value == (0, 0):
                    continue
                signed_members = tuple(sorted(
                    ((adv_label, adv_wave), (left_label, left_wave),
                     (right_label, right_wave))
                ))
                key = (signed_members, output_wave)
                seeds[key] = add_complex(seeds[key], h_value)
    return {key: value for key, value in seeds.items() if value != (0, 0)}


def speed_perturbation_series(velocity):
    speed_squared = {}
    for p, vp in velocity.items():
        for q, vq in velocity.items():
            wave = tuple(p[i] + q[i] for i in range(3))
            value = (Fraction(0), Fraction(0))
            for axis in range(3):
                value = add_complex(value, mul_complex(vp[axis], vq[axis]))
            speed_squared[wave] = add_complex(
                speed_squared.get(wave, (Fraction(0), Fraction(0))), value
            )
    speed_squared[(0, 0, 0)] = add_complex(
        speed_squared.get((0, 0, 0), (Fraction(0), Fraction(0))),
        (-CENTER, Fraction(0)),
    )
    return {
        wave: scale_complex(value, Fraction(1, 1) / CENTER)
        for wave, value in speed_squared.items() if value != (0, 0)
    }


def exact_decomposition(modes):
    atoms = signed_mode_atoms(modes)
    velocity = combine_velocity(atoms)
    x_series = speed_perturbation_series(velocity)
    seeds = pressure_seed_atoms(atoms)
    binomial = [Fraction(1)]
    for n in range(1, DEGREE + 1):
        binomial.append(binomial[-1] * Fraction(3 - 2 * n, 2 * n))
    powers = [{(0, 0, 0): (Fraction(1), Fraction(0))}]
    for _ in range(DEGREE):
        powers.append(scalar_convolution(powers[-1], x_series))

    by_order = [Fraction(0) for _ in range(DEGREE + 1)]
    by_seed = defaultdict(lambda: [Fraction(0) for _ in range(DEGREE + 1)])
    for (members, output_wave), value in seeds.items():
        for n in range(DEGREE + 1):
            complement = tuple(-entry for entry in output_wave)
            multiplier = powers[n].get(complement, (Fraction(0), Fraction(0)))
            constant = mul_complex(value, multiplier)
            # The normalized integral takes the real part; the conjugate signed
            # seed supplies the cancelling imaginary part.
            contribution = -3 * 256 * binomial[n] * constant[0]
            by_order[n] += contribution
            by_seed[members][n] += contribution
    return by_order, dict(by_seed)


def encode_fraction(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def interval_lower(result):
    return result["certified_lower_endpoint"]


def main():
    by_order, by_seed = exact_decomposition(EXAMPLE["modes"])
    seed_rows = []
    for members, contributions in by_seed.items():
        total = sum(contributions)
        if total == 0:
            continue
        seed_rows.append({
            "signed_members": [
                {"label": label, "wave": list(wave)} for label, wave in members
            ],
            "order_contributions": [
                encode_fraction(value) for value in contributions
            ],
            "degree_six_total": encode_fraction(total),
        })
    seed_rows.sort(
        key=lambda row: abs(Fraction(row["degree_six_total"])),
        reverse=True,
    )

    deletions = []
    for deleted in LABELS[2:]:
        data = deepcopy(EXAMPLE)
        data["modes"] = [
            mode for label, mode in zip(LABELS, EXAMPLE["modes"]) if label != deleted
        ]
        deleted_orders, _ = exact_decomposition(data["modes"])
        result = enclose(data, subdivisions=1, precision=128, epsilon_string="1/1024")
        deletions.append({
            "deleted": deleted,
            "exact_degree_six_polynomial": encode_fraction(sum(deleted_orders)),
            "proved_positive": result["proved_positive"],
            "certified_lower_endpoint": interval_lower(result),
            "polynomial_P3": result["polynomial_P3"],
        })

    shear_seed_total = sum(
        sum(values) for members, values in by_seed.items()
        if any(label in {"Sx", "Sy"} for label, _ in members)
    )
    nonshear_seed_total = sum(
        sum(values) for members, values in by_seed.items()
        if all(label not in {"Sx", "Sy"} for label, _ in members)
    )
    output = {
        "format": "CYCLE272-EXACT-MODAL-v1",
        "normalization": "normalized Haar measure; exact entries already include sqrt(65536)=256",
        "labels": dict(zip(LABELS, EXAMPLE["modes"])),
        "degree_six_order_totals": [
            encode_fraction(value) for value in by_order
        ],
        "degree_six_total": encode_fraction(sum(by_order)),
        "shear_containing_seed_total": encode_fraction(shear_seed_total),
        "nonshear_seed_total": encode_fraction(nonshear_seed_total),
        "nonzero_signed_pressure_seeds": seed_rows,
        "single_nonshear_mode_deletions": deletions,
        "notes": [
            "A seed is the exact cubic u dot grad p atom; higher orders close its output wave with powers of x=(|u|^2-65536)/65536.",
            "The pressure pair is symmetrized, and conjugate signed waves are retained explicitly.",
            "Deletion signs are Arb enclosures of the same exact rational Fourier polynomial plus a rigorous binomial remainder.",
        ],
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
