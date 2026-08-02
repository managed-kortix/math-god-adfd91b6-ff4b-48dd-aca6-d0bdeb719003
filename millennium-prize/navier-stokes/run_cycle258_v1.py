#!/usr/bin/env python3
"""Run one frozen C258-V1 numerical validation matrix entry."""

import argparse
import json
import math
import os
from dataclasses import asdict
from pathlib import Path

import numpy as np

from scout_cycle258_integrated_l3 import Euler2D, frozen_family


INDICES = (30, 36, 43, 44)
REPLAY_TIMES = (0.0, 0.265625, -0.265625, 1.65625, -1.65625, 2.5, -2.5)


def spectral_copy(field, old_n, new_n):
    shifted = np.fft.fftshift(field / old_n**2)
    out = np.zeros((new_n, new_n), dtype=np.complex128)
    start = (new_n - old_n) // 2
    out[start:start + old_n, start:start + old_n] = shifted
    return np.fft.ifftshift(out) * new_n**2


def l3_on_grid(solver, omega, grid):
    u, v = solver.velocity(omega)
    u = spectral_copy(u, solver.n, grid)
    v = spectral_copy(v, solver.n, grid)
    ux = np.fft.ifft2(u).real
    uy = np.fft.ifft2(v).real
    return float(np.mean(np.hypot(ux, uy) ** 3) ** (1.0 / 3.0))


def padded_rhs(solver, omega):
    grid = 2 * solver.n
    omega_pad = spectral_copy(omega, solver.n, grid)
    freq = np.fft.fftfreq(grid) * grid
    kx, ky = np.meshgrid(freq, freq, indexing="ij")
    k2 = kx * kx + ky * ky
    nonzero = k2 != 0
    psi = np.zeros_like(omega_pad)
    psi[nonzero] = -omega_pad[nonzero] / k2[nonzero]
    u = -1j * ky * psi
    v = 1j * kx * psi
    product = (
        np.fft.ifft2(u).real * np.fft.ifft2(1j * kx * omega_pad).real
        + np.fft.ifft2(v).real * np.fft.ifft2(1j * ky * omega_pad).real
    )
    rhs_pad = -np.fft.fft2(product)
    shifted = np.fft.fftshift(rhs_pad / grid**2)
    start = (grid - solver.n) // 2
    rhs = np.fft.ifftshift(
        shifted[start:start + solver.n, start:start + solver.n]
    ) * solver.n**2
    rhs[~solver.mask] = 0.0
    rhs[0, 0] = 0.0
    return rhs


def relative_discrepancy(a, b):
    denominator = np.linalg.norm(a.ravel())
    return float(np.linalg.norm((a - b).ravel()) / denominator)


def run_direction(solver, initial, direction, dt, sample_dt, final_time):
    omega = initial.copy()
    steps = round(final_time / dt)
    stride = round(sample_dt / dt)
    initial_l3 = {}
    samples = []
    replay = []
    replay_steps = {
        round(abs(time) / dt): time
        for time in REPLAY_TIMES
        if time == 0.0 or math.copysign(1.0, time) == direction
    }
    for step in range(steps + 1):
        if step % stride == 0 or step == steps:
            time = direction * step * dt
            l3_2n = l3_on_grid(solver, omega, 2 * solver.n)
            l3_4n = l3_on_grid(solver, omega, 4 * solver.n)
            if step == 0:
                initial_l3 = {"grid_2n": l3_2n, "grid_4n": l3_4n}
            samples.append((time, l3_2n, l3_4n))
        if step in replay_steps:
            native = solver.rhs(omega)
            replay.append({
                "time": direction * step * dt,
                "relative_rhs_discrepancy": relative_discrepancy(native, padded_rhs(solver, omega)),
            })
        if step == steps:
            break
        h = direction * dt
        k1 = solver.rhs(omega)
        k2 = solver.rhs(omega + 0.5 * h * k1)
        k3 = solver.rhs(omega + 0.5 * h * k2)
        k4 = solver.rhs(omega + h * k3)
        omega += (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        omega[~solver.mask] = 0.0
    return omega, initial_l3, samples, replay


def summarize(samples, initial_l3, key):
    column = 1 if key == "grid_2n" else 2
    minimum = min(samples, key=lambda row: (row[column], row[0]))
    maximum = max(samples, key=lambda row: (row[column], -row[0]))
    forward = [row for row in samples if row[0] >= 0.0]
    backward = [row for row in samples if row[0] <= 0.0]
    directed = {}
    for name, rows in (("backward", backward), ("forward", forward)):
        directed[name] = {
            "max_over_initial": max(row[column] for row in rows) / initial_l3[key],
            "initial_over_min": initial_l3[key] / min(row[column] for row in rows),
        }
    return {
        "variation_ratio": maximum[column] / minimum[column],
        "minimum": {"time": minimum[0], "l3": minimum[column]},
        "maximum": {"time": maximum[0], "l3": maximum[column]},
        "directed_ratios": directed,
    }


def run(source, index, n, dt_factor):
    modes, family = frozen_family(source)
    label, coefficients = family[index]
    solver = Euler2D(n)
    initial = solver.initial(modes, coefficients)
    initial_invariants = solver.invariants(initial)
    all_samples = []
    all_replay = []
    endpoint_drifts = []
    initial_l3 = None
    for direction in (-1, 1):
        endpoint, direction_initial_l3, samples, replay = run_direction(
            solver, initial, direction, 1.0 / (dt_factor * n), 1.0 / 256.0, 2.5
        )
        if initial_l3 is None:
            initial_l3 = direction_initial_l3
        all_samples.extend(row for row in samples if direction == -1 or row[0] != 0.0)
        all_replay.extend(row for row in replay if direction == -1 or row["time"] != 0.0)
        endpoint_invariants = solver.invariants(endpoint)
        endpoint_drifts.append({
            "direction": direction,
            "relative_energy_drift": abs(endpoint_invariants[0] / initial_invariants[0] - 1.0),
            "relative_enstrophy_drift": abs(endpoint_invariants[1] / initial_invariants[1] - 1.0),
        })
    cube_2n = summarize(all_samples, initial_l3, "grid_2n")
    cube_4n = summarize(all_samples, initial_l3, "grid_4n")
    return {
        "format": "C258-V1-entry",
        "numerical_only": True,
        "family_index": index,
        "label": asdict(label),
        "resolution": n,
        "cutoff": n // 3,
        "dt": 1.0 / (dt_factor * n),
        "dt_factor": dt_factor,
        "final_time_each_direction": 2.5,
        "sample_dt": 1.0 / 256.0,
        "checkpoint_diagnostics": [
            {"time": row[0], "l3_grid_2n": row[1], "l3_grid_4n": row[2]}
            for row in sorted(all_samples, key=lambda row: row[0])
        ],
        "initial_invariants": {"energy": initial_invariants[0], "enstrophy": initial_invariants[1]},
        "initial_l3": initial_l3,
        "cubature_2n": cube_2n,
        "cubature_4n": cube_4n,
        "cubature_variation_ratio_difference": abs(cube_4n["variation_ratio"] - cube_2n["variation_ratio"]),
        "endpoint_drifts": endpoint_drifts,
        "alias_replay": sorted(all_replay, key=lambda row: row["time"]),
        "max_alias_replay_relative_rhs_discrepancy": max(row["relative_rhs_discrepancy"] for row in all_replay),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--index", type=int, choices=INDICES, required=True)
    parser.add_argument("--n", type=int, choices=(128, 256), required=True)
    parser.add_argument("--dt-factor", type=int, choices=(2, 4), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = json.loads(args.source.read_text(encoding="ascii"))
    report = run(source, args.index, args.n, args.dt_factor)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="ascii")
    os.replace(temporary, args.output)


if __name__ == "__main__":
    main()
