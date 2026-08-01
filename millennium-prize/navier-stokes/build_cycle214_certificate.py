#!/usr/bin/env python3
"""Build the Cycle 214 finite Fourier/shell-majorant component artifact."""

import argparse
import json
from fractions import Fraction as F
from pathlib import Path

from validate_cycle212 import (
    CInterval, Interval, analytic_velocity_bounds, check_dissipative_shell_cap,
    check_picard_box, l3_cubature, low_mode_tail_remainder_bound,
    retained_modes, shell_convolution_bound, sqrt_interval, vorticity_rhs,
)


N, L, SLABS = 2, 32, 64
H = F(1, 4096)
RHO, CAP = F(33, 32), F(1, 1024)
ROUND_BITS = 70


def down(x):
    scale = 1 << ROUND_BITS
    return F(x.numerator * scale // x.denominator, scale)


def up(x):
    return -down(-x)


def round_interval(x):
    return Interval(down(x.lo), up(x.hi))


def round_complex(x):
    return CInterval(round_interval(x.re), round_interval(x.im))


def hull(a, b, padding=F(1, 1 << ROUND_BITS)):
    return CInterval(
        Interval(down(min(a.re.lo, b.re.lo) - padding), up(max(a.re.hi, b.re.hi) + padding)),
        Interval(down(min(a.im.lo, b.im.lo) - padding), up(max(a.im.hi, b.im.hi) + padding)),
    )


def initial():
    values = {k: CInterval.point() for k in retained_modes(N)}
    for k, value in {
        (1, 0): F(-1, 2), (-1, 0): F(-1, 2),
        (0, 1): F(-1, 2), (0, -1): F(-1, 2),
        (1, 1): F(-1), (-1, -1): F(-1),
    }.items():
        values[k] = CInterval.point(value)
    return values


def qs(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def interval_json(value):
    return [qs(value.lo), qs(value.hi)]


def complex_map_json(values):
    return {
        f"{k[0]},{k[1]}": {"re": interval_json(value.re), "im": interval_json(value.im)}
        for k, value in sorted(values.items())
    }


def retained_masses(box):
    masses = {n: F(0) for n in range(1, N + 1)}
    for k, value in box.items():
        magnitude = sqrt_interval(value.re.square() + value.im.square()).hi
        masses[max(abs(k[0]), abs(k[1]))] += magnitude
    return {n: up(value) for n, value in masses.items()}


def symmetric_remainder(head):
    output = {}
    for k in retained_modes(N):
        shell = max(abs(k[0]), abs(k[1]))
        radius = up(low_mode_tail_remainder_bound(shell, N, head, CAP, RHO, L))
        output[k] = CInterval(Interval(-radius, radius), Interval(-radius, radius))
    return output


def build_slab(entry, shell_entry):
    tube = dict(entry)
    shell_box = dict(shell_entry)
    for _ in range(80):
        retained = retained_masses(tube)
        head = {n: retained[n] if n <= N else shell_box[n] for n in range(1, L)}
        remainder = symmetric_remainder(head)
        rhs = vorticity_rhs(tube, F(1))
        candidate = {}
        for k in tube:
            derivative = rhs[k] + remainder[k]
            candidate[k] = hull(entry[k], entry[k] + derivative.scale(H))
        new_shell = dict(shell_box)
        for n in range(N + 1, L):
            new_shell[n] = up(shell_entry[n] + H * shell_convolution_bound(n, head, CAP, RHO, L))
        if all(candidate[k].subset(tube[k]) for k in tube) and all(
            new_shell[n] <= shell_box[n] for n in new_shell
        ):
            break
        tube = {k: hull(tube[k], candidate[k]) for k in tube}
        shell_box = {n: max(shell_box[n], new_shell[n] + F(1, 1 << ROUND_BITS)) for n in shell_box}
    else:
        raise RuntimeError("joint Fourier/shell Picard iteration did not close")

    retained = retained_masses(tube)
    head = {n: retained[n] if n <= N else shell_box[n] for n in range(1, L)}
    tail = check_dissipative_shell_cap(head, CAP, RHO, L, F(1), {})
    remainder = symmetric_remainder(head)
    derivative = check_picard_box(entry, tube, remainder, F(1), H, tube)
    endpoint = {k: round_complex(entry[k] + derivative[k].scale(H)) for k in entry}
    check_picard_box(entry, tube, remainder, F(1), H, endpoint)
    shell_endpoint = {
        n: up(shell_entry[n] / (1 + n * n * H)
              + H * shell_convolution_bound(n, head, CAP, RHO, L))
        for n in shell_entry
    }
    return tube, endpoint, shell_endpoint, head, remainder, tail


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("cycle214-components-certificate.json"))
    args = parser.parse_args()
    entry = initial()
    shell_entry = {n: F(0) for n in range(N + 1, L)}
    slabs = []
    for index in range(SLABS):
        tube, endpoint, shell_endpoint, head, remainder, tail = build_slab(entry, shell_entry)
        slabs.append({
            "index": index,
            "time": [qs(index * H), qs((index + 1) * H)],
            "entry": complex_map_json(entry),
            "box": complex_map_json(tube),
            "endpoint": complex_map_json(endpoint),
            "shell_entry": {str(n): qs(shell_entry[n]) for n in shell_entry},
            "shell_endpoint": {str(n): qs(shell_endpoint[n]) for n in shell_endpoint},
            "head_masses": {str(n): qs(head[n]) for n in range(1, L)},
            "remainders": complex_map_json(remainder),
            "finite_cap_margins": [qs(value) for value in tail.finite_margins],
            "cap_ray_coefficients": [qs(value) for value in tail.ray_coefficients],
        })
        print(index, float(head[1]), float(head[2]), float(max(remainder[k].re.hi for k in remainder)), flush=True)
        entry, shell_entry = endpoint, shell_endpoint
    u, g, tail_u = analytic_velocity_bounds(entry, CAP, RHO, L)
    cube = l3_cubature(entry, 16, u, g, tail_u, degree=20)
    document = {
        "format": "cycle214-components-v1",
        "status": "PASS COMPONENTS",
        "normalization": "T2-2pi-normalized-vorticity-v1",
        "selected_datum": "psi=cos(x)+cos(y)+cos(x+y)",
        "parameters": {"mu": "1", "T": "1/64", "retained_cutoff": N},
        "tail_majorant": {"lemma": "Cycle213-Lemma-A", "cap_start": L,
                            "rho": qs(RHO), "cap": qs(CAP)},
        "slabs": slabs,
        "analytic_norm": {"scope": "retained-plus-geometric-cap-only; explicit-shell-head-omitted",
                          "U": qs(u), "G": qs(g), "tail_velocity_component": qs(tail_u)},
        "cubature": {"scope": "formal-arithmetic-component-not-a-norm-enclosure",
                      "grid": 16, "trig_degree": 20, "l3_cube": interval_json(cube)},
        "conclusion": "finite Fourier and conditional shell-majorant components replayed; no PDE claim",
    }
    args.output.write_text(json.dumps(document, indent=2) + "\n", encoding="ascii")
    print("PASS COMPONENTS", float(cube.lo), float(cube.hi), float(u), float(g))


if __name__ == "__main__":
    main()
