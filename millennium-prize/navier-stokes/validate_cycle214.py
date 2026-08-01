#!/usr/bin/env python3
"""Replay the Cycle 214 finite Fourier/shell-majorant components."""

import argparse
import json
from fractions import Fraction as F
from pathlib import Path

from validate_cycle212 import (
    CInterval, Interval, analytic_velocity_bounds, check_dissipative_shell_cap,
    check_picard_box, l3_cubature, low_mode_tail_remainder_bound, retained_modes,
    shell_convolution_bound, sqrt_interval,
)


def exact_keys(value, expected, context):
    if set(value) != set(expected):
        raise ValueError(f"{context} keys differ: {sorted(set(value) ^ set(expected))}")


def qi(value):
    if not isinstance(value, str):
        raise ValueError("rational literals must be strings")
    return F(value)


def interval(value):
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("interval must be a two-element list")
    return Interval(qi(value[0]), qi(value[1]))


def mode_map(value, modes):
    output = {}
    for key, item in value.items():
        parts = key.split(",")
        if len(parts) != 2:
            raise ValueError("invalid mode key")
        mode = int(parts[0]), int(parts[1])
        exact_keys(item, {"re", "im"}, f"mode {key}")
        output[mode] = CInterval(interval(item["re"]), interval(item["im"]))
    if set(output) != set(modes):
        raise ValueError("mode set mismatch")
    return output


def initial_data(modes):
    output = {k: CInterval.point() for k in modes}
    for k, value in {
        (1, 0): F(-1, 2), (-1, 0): F(-1, 2),
        (0, 1): F(-1, 2), (0, -1): F(-1, 2),
        (1, 1): F(-1), (-1, -1): F(-1),
    }.items():
        output[k] = CInterval.point(value)
    return output


def validate(path):
    data = json.loads(path.read_text(encoding="ascii"))
    exact_keys(data, {"format", "status", "normalization", "selected_datum", "parameters",
                      "tail_majorant", "slabs", "analytic_norm", "cubature", "conclusion"}, "root")
    if data["format"] != "cycle214-components-v1" or data["status"] != "PASS COMPONENTS":
        raise ValueError("format or requested status mismatch")
    if data["normalization"] != "T2-2pi-normalized-vorticity-v1":
        raise ValueError("normalization mismatch")
    if data["selected_datum"] != "psi=cos(x)+cos(y)+cos(x+y)":
        raise ValueError("datum mismatch")
    exact_keys(data["parameters"], {"mu", "T", "retained_cutoff"}, "parameters")
    mu, total = qi(data["parameters"]["mu"]), qi(data["parameters"]["T"])
    cutoff = data["parameters"]["retained_cutoff"]
    if mu != 1 or total != F(1, 64) or cutoff != 2:
        raise ValueError("Cycle 214 parameter mismatch")
    modes = retained_modes(cutoff)
    expected_initial = initial_data(modes)
    exact_keys(data["tail_majorant"], {"lemma", "cap_start", "rho", "cap"}, "tail")
    tail = data["tail_majorant"]
    if tail["lemma"] != "Cycle213-Lemma-A":
        raise ValueError("shell lemma mismatch")
    cap_start, rho, cap = tail["cap_start"], qi(tail["rho"]), qi(tail["cap"])
    if not isinstance(cap_start, int):
        raise ValueError("cap start must be an integer")

    previous = None
    previous_shell = None
    endpoint = None
    for index, slab in enumerate(data["slabs"]):
        exact_keys(slab, {"index", "time", "entry", "box", "endpoint", "shell_entry",
                           "shell_endpoint", "head_masses",
                           "remainders", "finite_cap_margins", "cap_ray_coefficients"}, f"slab {index}")
        if slab["index"] != index or interval(slab["time"]) != Interval(F(index, 4096), F(index + 1, 4096)):
            raise ValueError(f"slab partition failure at {index}")
        entry = mode_map(slab["entry"], modes)
        box = mode_map(slab["box"], modes)
        endpoint = mode_map(slab["endpoint"], modes)
        remainder = mode_map(slab["remainders"], modes)
        shell_entry = {int(n): qi(value) for n, value in slab["shell_entry"].items()}
        shell_endpoint = {int(n): qi(value) for n, value in slab["shell_endpoint"].items()}
        if index == 0 and entry != expected_initial:
            raise ValueError("initial retained coefficients do not equal the selected datum")
        shell_indices = set(range(cutoff + 1, cap_start))
        if set(shell_entry) != shell_indices or set(shell_endpoint) != shell_indices:
            raise ValueError(f"shell head index mismatch at slab {index}")
        if previous is not None and any(not previous[k].subset(entry[k]) for k in modes):
            raise ValueError(f"slab chain failure at {index}")
        if previous_shell is not None and any(previous_shell[n] > shell_entry[n] for n in shell_indices):
            raise ValueError(f"shell chain failure at slab {index}")
        head = {int(n): qi(value) for n, value in slab["head_masses"].items()}
        if set(head) != set(range(1, cap_start)):
            raise ValueError(f"head mass index mismatch at slab {index}")
        retained_mass = {n: F(0) for n in range(1, cutoff + 1)}
        for k, value in box.items():
            retained_mass[max(abs(k[0]), abs(k[1]))] += sqrt_interval(
                value.re.square() + value.im.square()).hi
        if any(retained_mass[n] > head[n] for n in retained_mass):
            raise ValueError(f"retained head mass too small at slab {index}")
        if any(shell_entry[n] > head[n] for n in shell_indices):
            raise ValueError(f"shell tube mass too small at slab {index}")
        for n in shell_indices:
            propagated = shell_entry[n] + F(1, 4096) * shell_convolution_bound(
                n, head, cap, rho, cap_start)
            damped = shell_entry[n] / (1 + F(n * n, 4096)) + F(1, 4096) * shell_convolution_bound(
                n, head, cap, rho, cap_start)
            if propagated > head[n] or damped > shell_endpoint[n]:
                raise ValueError(f"shell Picard/endpoint failure at slab {index}, shell {n}")
        certificate = check_dissipative_shell_cap(head, cap, rho, cap_start, mu, {} if index == 0 else None)
        if [qi(x) for x in slab["finite_cap_margins"]] != list(certificate.finite_margins):
            raise ValueError(f"finite cap margin mismatch at slab {index}")
        if [qi(x) for x in slab["cap_ray_coefficients"]] != list(certificate.ray_coefficients):
            raise ValueError(f"cap ray mismatch at slab {index}")
        for k in modes:
            radius = low_mode_tail_remainder_bound(max(abs(k[0]), abs(k[1])), cutoff,
                                                   head, cap, rho, cap_start)
            declared = remainder[k]
            if not Interval(-radius, radius).subset(declared.re) or not Interval(-radius, radius).subset(declared.im):
                raise ValueError(f"tail remainder too narrow at slab {index}, mode {k}")
        check_picard_box(entry, box, remainder, mu, F(1, 4096), endpoint)
        previous = endpoint
        previous_shell = shell_endpoint
    if len(data["slabs"]) != 64 or endpoint is None:
        raise ValueError("slab chain does not terminate at T")

    exact_keys(data["analytic_norm"], {"scope", "U", "G", "tail_velocity_component"}, "analytic norm")
    u, g, tail_u = analytic_velocity_bounds(endpoint, cap, rho, cap_start)
    declared_norm = data["analytic_norm"]
    if declared_norm["scope"] != "retained-plus-geometric-cap-only; explicit-shell-head-omitted":
        raise ValueError("analytic norm scope mismatch")
    if (qi(declared_norm["U"]), qi(declared_norm["G"]), qi(declared_norm["tail_velocity_component"])) != (u, g, tail_u):
        raise ValueError("analytic norm mismatch")
    exact_keys(data["cubature"], {"scope", "grid", "trig_degree", "l3_cube"}, "cubature")
    cube_data = data["cubature"]
    if cube_data["scope"] != "formal-arithmetic-component-not-a-norm-enclosure":
        raise ValueError("cubature scope mismatch")
    cube = l3_cubature(endpoint, cube_data["grid"], u, g, tail_u, cube_data["trig_degree"])
    if interval(cube_data["l3_cube"]) != cube:
        raise ValueError("cubature mismatch")
    if data["conclusion"] != "finite Fourier and conditional shell-majorant components replayed; no PDE claim":
        raise ValueError("conclusion mismatch")
    return cube


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    try:
        cube = validate(args.certificate)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, ZeroDivisionError) as exc:
        parser.exit(1, f"FAIL CLOSED: {exc}\n")
    print("PASS COMPONENTS Cycle 214")
    print(f"formal retained-plus-cap cubature calculation in [{float(cube.lo):.8g}, {float(cube.hi):.8g}]")
    print("NO FULL-PDE OR AMPLIFICATION CLAIM")


if __name__ == "__main__":
    main()
