#!/usr/bin/env python3
"""Run the frozen, single-profile C267-KP1 Galerkin experiment."""

import argparse
import hashlib
import json
import os
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "2")

import numpy as np

from scout_cycle265_3d_alignment import Galerkin3D


def canonical_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("ascii")


def kida_state(solver):
    n = solver.width
    axis = 2.0 * np.pi * np.arange(n) / n
    x, y, z = np.meshgrid(axis, axis, axis, indexing="ij")
    field = np.stack((
        np.sin(x) * (np.cos(3 * y) * np.cos(z) - np.cos(y) * np.cos(3 * z)),
        np.sin(y) * (np.cos(3 * z) * np.cos(x) - np.cos(z) * np.cos(3 * x)),
        np.sin(z) * (np.cos(3 * x) * np.cos(y) - np.cos(x) * np.cos(3 * y)),
    ))
    return np.fft.fftshift(
        np.fft.fftn(field, axes=(1, 2, 3)), axes=(1, 2, 3)
    ) / n**3


def initial_state(solver):
    base = kida_state(solver)
    return base - solver.rhs(base) / 32.0


def invariant_data(solver, state):
    return solver.energy(state), solver.helicity(state)


def midpoint_step(solver, initial, step_size, gates, maximum_iterations):
    endpoint = initial + step_size * solver.rhs(initial)
    history = []
    for iteration in range(1, maximum_iterations + 1):
        midpoint = 0.5 * (initial + endpoint)
        tangent = solver.rhs(midpoint)
        residual = endpoint - initial - step_size * tangent
        scale = 1.0 + np.linalg.norm(initial) + step_size * np.linalg.norm(tangent)
        residual_ratio = float(np.linalg.norm(residual) / scale)
        if residual_ratio <= gates["nonlinear_residual_ratio_max"]:
            energy0, helicity0 = invariant_data(solver, initial)
            energy1, helicity1 = invariant_data(solver, endpoint)
            energy_tangent = abs(float(np.real(np.vdot(midpoint, tangent))))
            helicity_tangent = abs(float(np.real(np.vdot(solver.curl(midpoint), tangent))))
            norm_scale = max(float(np.linalg.norm(midpoint) * np.linalg.norm(tangent)), 1.0)
            energy_identity = abs((energy1 - energy0) - step_size * float(np.real(np.vdot(midpoint, tangent))))
            helicity_identity = abs((helicity1 - helicity0) - step_size * float(np.real(np.vdot(solver.curl(midpoint), tangent))))
            return endpoint, {
                "iterations": iteration,
                "residual_ratio": residual_ratio,
                "energy_tangency": energy_tangent / norm_scale,
                "helicity_tangency": helicity_tangent / norm_scale,
                "energy_identity_closure": energy_identity / max(abs(energy0), 1.0),
                "helicity_identity_closure": helicity_identity / max(abs(energy0), 1.0),
            }
        image = initial + step_size * tangent
        history.append((image.copy(), (image - endpoint).copy()))
        history = history[-4:]
        if len(history) == 1:
            endpoint = image
            continue
        count = len(history)
        gram = np.empty((count, count))
        for row in range(count):
            for column in range(count):
                gram[row, column] = np.real(np.vdot(history[row][1], history[column][1]))
        system = np.block([
            [gram, np.ones((count, 1))],
            [np.ones((1, count)), np.zeros((1, 1))],
        ])
        target = np.zeros(count + 1)
        target[-1] = 1.0
        try:
            weights = np.linalg.solve(system, target)[:-1]
            endpoint = sum(weight * pair[0] for weight, pair in zip(weights, history))
        except np.linalg.LinAlgError:
            endpoint = image
    raise RuntimeError("implicit midpoint solve did not meet the frozen residual gate")


def update_maxima(maxima, diagnostics):
    maxima["iterations_max"] = max(maxima["iterations_max"], diagnostics["iterations"])
    for key in diagnostics:
        if key != "iterations":
            maxima[key + "_max"] = max(maxima.get(key + "_max", 0.0), diagnostics[key])


def endpoint_record(solver, initial_l3, state, grids):
    norms = {str(grid): solver.l3(state, grid) for grid in grids}
    ratios = {grid: norms[str(grid)] / initial_l3[str(grid)] for grid in grids}
    return {
        "l3": norms,
        "directed_ratios": {str(grid): ratios[grid] for grid in grids},
        "cubature_ratio_difference": abs(ratios[grids[1]] - ratios[grids[0]]),
    }


def run_level(level, manifest):
    solver = Galerkin3D(level["cubic_cutoff"])
    state = initial_state(solver)
    grids = level["endpoint_cubature_grids"]
    step_size = 1.0 / level["steps_per_unit_time"]
    horizons = manifest["directed_horizons"]
    initial_l3 = {str(grid): solver.l3(state, grid) for grid in grids}
    energy0, helicity0 = invariant_data(solver, state)
    maxima = {"iterations_max": 0}
    endpoints = {}
    total_steps = round(horizons[-1] / step_size)
    horizon_steps = {round(horizon / step_size): horizon for horizon in horizons}
    for step in range(1, total_steps + 1):
        state, diagnostics = midpoint_step(
            solver,
            state,
            step_size,
            manifest["gates"],
            manifest["integrator"]["maximum_iterations_per_step"],
        )
        update_maxima(maxima, diagnostics)
        if step in horizon_steps:
            endpoints[str(horizon_steps[step])] = endpoint_record(solver, initial_l3, state, grids)
    energy1, helicity1 = invariant_data(solver, state)
    defects = solver.defects(state)
    maxima.update({
        "relative_energy_drift": abs(energy1 / energy0 - 1.0),
        "energy_scaled_helicity_drift": abs(helicity1 - helicity0) / energy0,
        "divergence_defect": defects["divergence"],
        "reality_defect": defects["reality"],
    })
    gates = manifest["gates"]
    local_pass = (
        maxima["residual_ratio_max"] <= gates["nonlinear_residual_ratio_max"]
        and maxima["energy_tangency_max"] <= gates["energy_tangency_max"]
        and maxima["helicity_tangency_max"] <= gates["helicity_tangency_max"]
        and maxima["energy_identity_closure_max"] <= gates["energy_identity_closure_max"]
        and maxima["helicity_identity_closure_max"] <= gates["helicity_identity_closure_max"]
        and maxima["relative_energy_drift"] <= gates["relative_energy_drift_max"]
        and maxima["energy_scaled_helicity_drift"] <= gates["energy_scaled_helicity_drift_max"]
        and maxima["divergence_defect"] <= gates["divergence_defect_max"]
        and maxima["reality_defect"] <= gates["reality_defect_max"]
        and all(row["cubature_ratio_difference"] <= gates["doubled_cubature_endpoint_ratio_difference_max"] for row in endpoints.values())
    )
    return {
        "cutoff": level["cubic_cutoff"],
        "step_size": step_size,
        "steps": total_steps,
        "initial_l3": initial_l3,
        "initial_energy": energy0,
        "initial_helicity": helicity0,
        "maxima": maxima,
        "endpoints": endpoints,
        "all_local_gates_pass": local_pass,
    }


def run(manifest_path):
    raw = manifest_path.read_bytes()
    manifest = json.loads(raw.decode("ascii"))
    if manifest["status"] != "FROZEN_BEFORE_TRAJECTORY_COMPUTE":
        raise ValueError("manifest is not frozen")
    levels = {}
    for level in manifest["levels"]:
        levels[level["name"]] = run_level(level, manifest)
    comparisons = {}
    all_cross_pass = True
    architecture_promotions = []
    certifications = []
    coarse_name, fine_name = (level["name"] for level in manifest["levels"])
    fine_grids = manifest["levels"][1]["endpoint_cubature_grids"]
    fine_primary = str(fine_grids[0])
    for horizon in manifest["directed_horizons"]:
        key = str(horizon)
        coarse_ratio = levels[coarse_name]["endpoints"][key]["directed_ratios"][str(manifest["levels"][0]["endpoint_cubature_grids"][0])]
        fine_ratio = levels[fine_name]["endpoints"][key]["directed_ratios"][fine_primary]
        difference = abs(fine_ratio - coarse_ratio)
        cross_pass = difference <= manifest["gates"]["cross_resolution_endpoint_ratio_difference_max"]
        comparisons[key] = {
            "coarse_ratio": coarse_ratio,
            "fine_ratio": fine_ratio,
            "absolute_difference": difference,
            "gate_pass": cross_pass,
        }
        all_cross_pass = all_cross_pass and cross_pass
        eligible = cross_pass and all(level["all_local_gates_pass"] for level in levels.values())
        if eligible and fine_ratio >= manifest["promotion"]["architecture_signal_threshold"]:
            architecture_promotions.append({"horizon": horizon, "fine_ratio": fine_ratio})
        if eligible and fine_ratio >= manifest["promotion"]["certification_threshold"]:
            certifications.append({"horizon": horizon, "fine_ratio": fine_ratio})
    return {
        "format": "C267-KP1-outcome-v1",
        "status": "NUMERICAL_ONLY",
        "pde_certificate": False,
        "manifest_sha256": hashlib.sha256(raw).hexdigest(),
        "threads_max": 2,
        "profile": manifest["profile"],
        "levels": levels,
        "cross_resolution": comparisons,
        "all_cross_resolution_gates_pass": all_cross_pass,
        "architecture_signal_promotions": architecture_promotions,
        "certification_promotions": certifications,
        "claim": "Finite-dimensional numerical evidence only; no Euler, Navier-Stokes, or Millennium result.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_bytes(canonical_bytes(run(args.manifest)))


if __name__ == "__main__":
    main()
