#!/usr/bin/env python3
"""Run the frozen C264-DE1 directed endpoint finite-Galerkin screen."""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


RESIDUAL_GATE = 5.0e-12
TANGENCY_GATE = 2.0e-12
IDENTITY_GATE = 2.0e-12
DRIFT_GATE = 2.0e-9
CUBATURE_GATE = 2.0e-3
PROMOTION_RATIO = 2.01
CROSS_RESOLUTION_GATE = 0.01
STEP_SIZE = 1.0 / 64.0
FINAL_TIME = 4.0
MAX_ITERATIONS = 80


class PaddedGalerkin:
    def __init__(self, cutoff):
        self.cutoff = cutoff
        self.width = 2 * cutoff + 1
        self.side = 4 * cutoff + 1
        frequency = np.arange(-cutoff, cutoff + 1, dtype=float)
        self.kx, self.ky = np.meshgrid(frequency, frequency, indexing="ij")
        self.k2 = self.kx * self.kx + self.ky * self.ky
        self.nonzero = self.k2 != 0.0
        self.energy_weights = np.zeros_like(self.k2)
        self.energy_weights[self.nonzero] = 1.0 / self.k2[self.nonzero]

        padded_frequency = np.fft.fftfreq(self.side) * self.side
        self.pkx, self.pky = np.meshgrid(
            padded_frequency, padded_frequency, indexing="ij"
        )
        self.pk2 = self.pkx * self.pkx + self.pky * self.pky
        self.pnonzero = self.pk2 != 0.0
        values = np.arange(-cutoff, cutoff + 1)
        self.pindices = values % self.side

    def pad(self, omega):
        spectrum = np.zeros((self.side, self.side), dtype=np.complex128)
        spectrum[np.ix_(self.pindices, self.pindices)] = self.side**2 * omega
        return spectrum

    def rhs(self, omega):
        spectrum = self.pad(omega)
        psi = np.zeros_like(spectrum)
        psi[self.pnonzero] = -spectrum[self.pnonzero] / self.pk2[self.pnonzero]
        ux = np.fft.ifft2(-1j * self.pky * psi).real
        uy = np.fft.ifft2(1j * self.pkx * psi).real
        wx = np.fft.ifft2(1j * self.pkx * spectrum).real
        wy = np.fft.ifft2(1j * self.pky * spectrum).real
        transformed = -np.fft.fft2(ux * wx + uy * wy) / self.side**2
        return transformed[np.ix_(self.pindices, self.pindices)]

    def inner(self, left, right, invariant):
        weights = self.energy_weights if invariant == "energy" else 1.0
        return float(np.real(np.vdot(left * weights, right)))

    def invariant(self, omega, invariant):
        return 0.5 * self.inner(omega, omega, invariant)

    def midpoint_step(self, initial):
        endpoint = initial + STEP_SIZE * self.rhs(initial)
        solve = None
        history = []
        for iteration in range(1, MAX_ITERATIONS + 1):
            midpoint = 0.5 * (initial + endpoint)
            tangent = self.rhs(midpoint)
            residual = endpoint - initial - STEP_SIZE * tangent
            residual_norm = float(np.linalg.norm(residual))
            scale = float(
                1.0 + np.linalg.norm(initial) + STEP_SIZE * np.linalg.norm(tangent)
            )
            solve = (endpoint, midpoint, tangent, residual, iteration,
                     residual_norm / scale)
            if residual_norm <= RESIDUAL_GATE * scale:
                return solve
            image = initial + STEP_SIZE * tangent
            fixed_residual = image - endpoint
            history.append((image.copy(), fixed_residual.copy()))
            history = history[-5:]
            if len(history) == 1:
                endpoint = image
            else:
                gram = np.empty((len(history), len(history)))
                for row, (_, left) in enumerate(history):
                    for column, (_, right) in enumerate(history):
                        gram[row, column] = float(np.real(np.vdot(left, right)))
                system = np.empty((len(history) + 1, len(history) + 1))
                system[:-1, :-1] = gram
                system[:-1, -1] = 1.0
                system[-1, :-1] = 1.0
                system[-1, -1] = 0.0
                rhs = np.zeros(len(history) + 1)
                rhs[-1] = 1.0
                try:
                    coefficients = np.linalg.solve(system, rhs)[:-1]
                    endpoint = sum(
                        coefficient * pair[0]
                        for coefficient, pair in zip(coefficients, history)
                    )
                except np.linalg.LinAlgError:
                    endpoint = image
        raise RuntimeError(
            f"midpoint iteration failed: residual ratio {solve[-1]:.3e}"
        )

    def l3(self, omega, grid):
        spectrum = np.zeros((grid, grid), dtype=np.complex128)
        indices = np.arange(-self.cutoff, self.cutoff + 1) % grid
        embedded = grid**2 * omega
        spectrum[np.ix_(indices, indices)] = embedded
        frequency = np.fft.fftfreq(grid) * grid
        kx, ky = np.meshgrid(frequency, frequency, indexing="ij")
        k2 = kx * kx + ky * ky
        nonzero = k2 != 0.0
        psi = np.zeros_like(spectrum)
        psi[nonzero] = -spectrum[nonzero] / k2[nonzero]
        ux = np.fft.ifft2(-1j * ky * psi).real
        uy = np.fft.ifft2(1j * kx * psi).real
        return float(np.mean(np.hypot(ux, uy) ** 3) ** (1.0 / 3.0))


def initial_state(solver, modes, coefficients):
    omega = np.zeros((solver.width, solver.width), dtype=np.complex128)
    for j, (kx, ky) in enumerate(modes):
        psi = 0.5 * (coefficients[2 * j] - 1j * coefficients[2 * j + 1])
        value = -(kx * kx + ky * ky) * psi
        omega[kx + solver.cutoff, ky + solver.cutoff] += value
        omega[-kx + solver.cutoff, -ky + solver.cutoff] += np.conj(value)
    return omega


def run_member(solver, modes, candidate, diagnostic_grid):
    state = initial_state(solver, modes, candidate["coefficients"])
    initial = state.copy()
    initial_invariants = {
        name: solver.invariant(state, name) for name in ("energy", "enstrophy")
    }
    initial_l3 = solver.l3(state, diagnostic_grid)
    initial_l3_double = solver.l3(state, 2 * diagnostic_grid)
    max_l3 = initial_l3
    max_l3_time = 0.0
    maxima = {
        "residual_ratio": 0.0,
        "energy_tangency": 0.0,
        "enstrophy_tangency": 0.0,
        "energy_identity_closure": 0.0,
        "enstrophy_identity_closure": 0.0,
        "iterations": 0,
    }
    for step in range(1, round(FINAL_TIME / STEP_SIZE) + 1):
        endpoint, midpoint, tangent, residual, iterations, residual_ratio = (
            solver.midpoint_step(state)
        )
        maxima["residual_ratio"] = max(maxima["residual_ratio"], residual_ratio)
        maxima["iterations"] = max(maxima["iterations"], iterations)
        for invariant in ("energy", "enstrophy"):
            before = solver.invariant(state, invariant)
            after = solver.invariant(endpoint, invariant)
            tangent_inner = solver.inner(midpoint, tangent, invariant)
            weights = solver.energy_weights if invariant == "energy" else 1.0
            denominator = np.linalg.norm(np.sqrt(weights) * midpoint) * np.linalg.norm(
                np.sqrt(weights) * tangent
            )
            tangency = abs(tangent_inner) / denominator if denominator else 0.0
            residual_term = solver.inner(midpoint, residual, invariant)
            closure = (after - before) - STEP_SIZE * tangent_inner - residual_term
            closure_scale = 1.0 + abs(after - before) + abs(
                STEP_SIZE * tangent_inner
            ) + abs(residual_term)
            maxima[f"{invariant}_tangency"] = max(
                maxima[f"{invariant}_tangency"], tangency
            )
            maxima[f"{invariant}_identity_closure"] = max(
                maxima[f"{invariant}_identity_closure"], abs(closure) / closure_scale
            )
        state = endpoint
        sampled_l3 = solver.l3(state, diagnostic_grid)
        if sampled_l3 > max_l3:
            max_l3 = sampled_l3
            max_l3_time = step * STEP_SIZE

    endpoint_l3 = solver.l3(state, diagnostic_grid)
    endpoint_l3_double = solver.l3(state, 2 * diagnostic_grid)
    ratio = endpoint_l3 / initial_l3
    double_ratio = endpoint_l3_double / initial_l3_double
    drifts = {
        name: abs(solver.invariant(state, name) / initial_invariants[name] - 1.0)
        for name in ("energy", "enstrophy")
    }
    passed = (
        maxima["residual_ratio"] <= RESIDUAL_GATE
        and maxima["energy_tangency"] <= TANGENCY_GATE
        and maxima["enstrophy_tangency"] <= TANGENCY_GATE
        and maxima["energy_identity_closure"] <= IDENTITY_GATE
        and maxima["enstrophy_identity_closure"] <= IDENTITY_GATE
        and max(drifts.values()) <= DRIFT_GATE
        and abs(double_ratio - ratio) <= CUBATURE_GATE
    )
    return {
        "rho": candidate["rho"],
        "variational_start": candidate["start"],
        "initial_objective": candidate["objective"],
        "directed_endpoint_ratio": ratio,
        "doubled_grid_endpoint_ratio": double_ratio,
        "cubature_ratio_difference": abs(double_ratio - ratio),
        "interior_maximum_ratio": max_l3 / initial_l3,
        "interior_maximum_time": max_l3_time,
        "relative_energy_drift": drifts["energy"],
        "relative_enstrophy_drift": drifts["enstrophy"],
        "residual_maxima": maxima,
        "all_local_gates_pass": passed,
    }


def screen(source_path):
    raw = source_path.read_bytes()
    source = json.loads(raw.decode("ascii"))
    levels = (("N64", 15, 64), ("N128", 31, 128))
    reports = {}
    for label, cutoff, grid in levels:
        solver = PaddedGalerkin(cutoff)
        rows = []
        for index, candidate in enumerate(source["candidates"]):
            row = run_member(solver, source["modes"], candidate, grid)
            row["family_index"] = index
            rows.append(row)
            print(
                f"{label} member={index} endpoint={row['directed_endpoint_ratio']:.12g} "
                f"residual={row['residual_maxima']['residual_ratio']:.3e}",
                flush=True,
            )
        reports[label] = {
            "cutoff": cutoff,
            "diagnostic_grids": [grid, 2 * grid],
            "results": rows,
        }
    comparisons = []
    promotions = []
    for coarse, fine in zip(reports["N64"]["results"], reports["N128"]["results"]):
        difference = abs(
            fine["directed_endpoint_ratio"] - coarse["directed_endpoint_ratio"]
        )
        promoted = (
            fine["directed_endpoint_ratio"] > PROMOTION_RATIO
            and fine["all_local_gates_pass"]
            and coarse["all_local_gates_pass"]
            and difference <= CROSS_RESOLUTION_GATE
        )
        comparisons.append({
            "family_index": fine["family_index"],
            "rho": fine["rho"],
            "absolute_endpoint_ratio_difference": difference,
            "promoted": promoted,
        })
        if promoted:
            promotions.append(fine["family_index"])
    return {
        "format": "C264-DE1-screen",
        "status": "NUMERICAL_ONLY",
        "pde_certificate": False,
        "cycle258_inputs_used": False,
        "family_source": source_path.name,
        "family_source_sha256": hashlib.sha256(raw).hexdigest(),
        "family_size": len(source["candidates"]),
        "step_size": STEP_SIZE,
        "final_time": FINAL_TIME,
        "promotion_threshold": PROMOTION_RATIO,
        "gates": {
            "nonlinear_residual_ratio": RESIDUAL_GATE,
            "normalized_tangency": TANGENCY_GATE,
            "identity_closure": IDENTITY_GATE,
            "endpoint_invariant_drift": DRIFT_GATE,
            "cubature_ratio_difference": CUBATURE_GATE,
            "cross_resolution_ratio_difference": CROSS_RESOLUTION_GATE,
        },
        "levels": reports,
        "comparisons": comparisons,
        "promotions": promotions,
        "passed_any": bool(promotions),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = screen(args.source)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="ascii"
    )


if __name__ == "__main__":
    main()
