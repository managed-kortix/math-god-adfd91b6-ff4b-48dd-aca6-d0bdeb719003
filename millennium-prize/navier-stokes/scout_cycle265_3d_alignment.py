#!/usr/bin/env python3
"""Run the frozen C265-3DA1 finite-Galerkin 3D Euler scout."""

import argparse
import json
from pathlib import Path

import numpy as np


STEP_SIZE = 1.0 / 128.0
FINAL_TIME = 2.0
RESIDUAL_GATE = 1.0e-11
DRIFT_GATE = 2.0e-9
STRUCTURE_GATE = 2.0e-12
CUBATURE_GATE = 2.0e-3
STOP_RATIO = 1.2
MAX_ITERATIONS = 60

FAMILY = (
    {"name": "tg_plus_abc_symmetric", "sign": 1, "abc": (1.0, 1.0, 1.0), "phase": (0.0, 0.0, 0.0)},
    {"name": "tg_minus_abc_symmetric", "sign": -1, "abc": (1.0, 1.0, 1.0), "phase": (0.0, 0.0, 0.0)},
    {"name": "tg_plus_abc_phased", "sign": 1, "abc": (1.0, 0.8, 1.2), "phase": (np.pi / 2.0, 0.0, np.pi / 3.0)},
    {"name": "tg_minus_abc_phased", "sign": -1, "abc": (1.0, 0.8, 1.2), "phase": (np.pi / 2.0, 0.0, np.pi / 3.0)},
)


class Galerkin3D:
    def __init__(self, cutoff):
        self.cutoff = cutoff
        self.width = 2 * cutoff + 1
        self.side = 4 * cutoff + 1
        frequency = np.arange(-cutoff, cutoff + 1, dtype=float)
        self.k = np.stack(np.meshgrid(frequency, frequency, frequency, indexing="ij"))
        self.k2 = np.sum(self.k * self.k, axis=0)
        self.nonzero = self.k2 != 0.0
        padded_frequency = np.fft.fftfreq(self.side) * self.side
        self.pk = np.stack(
            np.meshgrid(padded_frequency, padded_frequency, padded_frequency, indexing="ij")
        )
        self.pk2 = np.sum(self.pk * self.pk, axis=0)
        self.pnonzero = self.pk2 != 0.0
        self.pindices = np.arange(-cutoff, cutoff + 1) % self.side

    def pad(self, state):
        spectrum = np.zeros((3, self.side, self.side, self.side), dtype=np.complex128)
        target = np.ix_(np.arange(3), self.pindices, self.pindices, self.pindices)
        spectrum[target] = self.side**3 * state
        return spectrum

    def curl(self, state):
        return 1j * np.stack((
            self.k[1] * state[2] - self.k[2] * state[1],
            self.k[2] * state[0] - self.k[0] * state[2],
            self.k[0] * state[1] - self.k[1] * state[0],
        ))

    def rhs(self, state):
        spectrum = self.pad(state)
        velocity = np.fft.ifftn(spectrum, axes=(1, 2, 3)).real
        vorticity_spectrum = 1j * np.stack((
            self.pk[1] * spectrum[2] - self.pk[2] * spectrum[1],
            self.pk[2] * spectrum[0] - self.pk[0] * spectrum[2],
            self.pk[0] * spectrum[1] - self.pk[1] * spectrum[0],
        ))
        vorticity = np.fft.ifftn(vorticity_spectrum, axes=(1, 2, 3)).real
        rotational = np.cross(velocity, vorticity, axisa=0, axisb=0, axisc=0)
        transformed = np.fft.fftn(rotational, axes=(1, 2, 3)) / self.side**3
        dot = np.sum(self.pk * transformed, axis=0)
        transformed[:, self.pnonzero] -= (
            self.pk[:, self.pnonzero] * dot[self.pnonzero] / self.pk2[self.pnonzero]
        )
        transformed[:, ~self.pnonzero] = 0.0
        source = np.ix_(np.arange(3), self.pindices, self.pindices, self.pindices)
        return transformed[source]

    @staticmethod
    def energy(state):
        return 0.5 * float(np.real(np.vdot(state, state)))

    def helicity(self, state):
        return 0.5 * float(np.real(np.vdot(state, self.curl(state))))

    def defects(self, state):
        divergence = np.sum(self.k * state, axis=0)
        scale = max(float(np.linalg.norm(state)), 1.0)
        reversed_state = np.conj(state[:, ::-1, ::-1, ::-1])
        return {
            "divergence": float(np.linalg.norm(divergence)) / scale,
            "reality": float(np.linalg.norm(state - reversed_state)) / scale,
        }

    def midpoint_step(self, initial):
        endpoint = initial + STEP_SIZE * self.rhs(initial)
        history = []
        for iteration in range(1, MAX_ITERATIONS + 1):
            tangent = self.rhs(0.5 * (initial + endpoint))
            residual = endpoint - initial - STEP_SIZE * tangent
            scale = 1.0 + np.linalg.norm(initial) + STEP_SIZE * np.linalg.norm(tangent)
            ratio = float(np.linalg.norm(residual) / scale)
            if ratio <= RESIDUAL_GATE:
                return endpoint, ratio, iteration
            image = initial + STEP_SIZE * tangent
            history.append((image.copy(), (image - endpoint).copy()))
            history = history[-4:]
            if len(history) == 1:
                endpoint = image
                continue
            count = len(history)
            gram = np.empty((count, count))
            for row in range(count):
                for column in range(count):
                    gram[row, column] = np.real(
                        np.vdot(history[row][1], history[column][1])
                    )
            system = np.block([[gram, np.ones((count, 1))], [np.ones((1, count)), np.zeros((1, 1))]])
            target = np.zeros(count + 1)
            target[-1] = 1.0
            try:
                weights = np.linalg.solve(system, target)[:-1]
                endpoint = sum(weight * pair[0] for weight, pair in zip(weights, history))
            except np.linalg.LinAlgError:
                endpoint = image
        raise RuntimeError(f"midpoint solve failed at residual ratio {ratio:.3e}")

    def physical(self, state, grid):
        spectrum = np.zeros((3, grid, grid, grid), dtype=np.complex128)
        indices = np.arange(-self.cutoff, self.cutoff + 1) % grid
        target = np.ix_(np.arange(3), indices, indices, indices)
        spectrum[target] = grid**3 * state
        return np.fft.ifftn(spectrum, axes=(1, 2, 3)).real

    def l3(self, state, grid):
        velocity = self.physical(state, grid)
        magnitude = np.sqrt(np.sum(velocity * velocity, axis=0))
        return float(np.mean(magnitude**3) ** (1.0 / 3.0))

    def alignment(self, state, grid):
        indices = np.arange(-self.cutoff, self.cutoff + 1) % grid
        spectrum = np.zeros((3, grid, grid, grid), dtype=np.complex128)
        spectrum[np.ix_(np.arange(3), indices, indices, indices)] = grid**3 * state
        frequency = np.fft.fftfreq(grid) * grid
        wave = np.stack(np.meshgrid(frequency, frequency, frequency, indexing="ij"))
        gradient = np.empty((3, 3, grid, grid, grid))
        for component in range(3):
            for direction in range(3):
                gradient[component, direction] = np.fft.ifftn(
                    1j * wave[direction] * spectrum[component]
                ).real
        strain = 0.5 * (gradient + gradient.swapaxes(0, 1))
        vorticity = np.stack((
            gradient[2, 1] - gradient[1, 2],
            gradient[0, 2] - gradient[2, 0],
            gradient[1, 0] - gradient[0, 1],
        ))
        stretched = np.einsum("ijxyz,jxyz->ixyz", strain, vorticity)
        numerator = float(np.mean(np.sum(vorticity * stretched, axis=0)))
        denominator = np.sqrt(
            np.mean(np.sum(vorticity * vorticity, axis=0))
            * np.mean(np.sum(stretched * stretched, axis=0))
        )
        return numerator / denominator if denominator else 0.0


def initial_state(solver, member):
    n = solver.width
    axis = 2.0 * np.pi * np.arange(n) / n
    x, y, z = np.meshgrid(axis, axis, axis, indexing="ij")
    tg = np.stack((np.sin(x) * np.cos(y) * np.cos(z),
                   -np.cos(x) * np.sin(y) * np.cos(z), np.zeros_like(x)))
    a, b, c = member["abc"]
    p, q, r = member["phase"]
    abc = np.stack((a * np.sin(z + r) + c * np.cos(y + q),
                    b * np.sin(x + p) + a * np.cos(z + r),
                    c * np.sin(y + q) + b * np.cos(x + p)))
    field = tg + member["sign"] * 0.2 * abc
    state = np.fft.fftshift(np.fft.fftn(field, axes=(1, 2, 3)), axes=(1, 2, 3)) / n**3
    state /= np.sqrt(solver.energy(state))
    return state


def run_member(solver, member, grid, check_grid):
    state = initial_state(solver, member)
    initial = state.copy()
    energy0 = solver.energy(state)
    helicity0 = solver.helicity(state)
    l3_initial = solver.l3(state, grid)
    l3_initial_check = solver.l3(state, check_grid)
    alignment_initial = solver.alignment(state, grid)
    residual_max = 0.0
    iteration_max = 0
    for _ in range(round(FINAL_TIME / STEP_SIZE)):
        state, residual, iterations = solver.midpoint_step(state)
        residual_max = max(residual_max, residual)
        iteration_max = max(iteration_max, iterations)
    l3_endpoint = solver.l3(state, grid)
    l3_endpoint_check = solver.l3(state, check_grid)
    ratio = l3_endpoint / l3_initial
    ratio_check = l3_endpoint_check / l3_initial_check
    energy_drift = abs(solver.energy(state) / energy0 - 1.0)
    helicity_drift = abs(solver.helicity(state) - helicity0) / energy0
    defects = solver.defects(state)
    passed = (residual_max <= RESIDUAL_GATE and energy_drift <= DRIFT_GATE
              and helicity_drift <= DRIFT_GATE and max(defects.values()) <= STRUCTURE_GATE
              and abs(ratio_check - ratio) <= CUBATURE_GATE)
    return {
        "name": member["name"],
        "directed_endpoint_ratio": ratio,
        "check_grid_endpoint_ratio": ratio_check,
        "cubature_ratio_difference": abs(ratio_check - ratio),
        "initial_alignment": alignment_initial,
        "endpoint_alignment": solver.alignment(state, grid),
        "initial_helicity": helicity0,
        "relative_energy_drift": energy_drift,
        "energy_scaled_helicity_drift": helicity_drift,
        "residual_ratio_max": residual_max,
        "iterations_max": iteration_max,
        "endpoint_defects": defects,
        "all_local_gates_pass": passed,
    }


def screen():
    levels = (("K5", 5, 32, 48), ("K7", 7, 48, 64))
    reports = {}
    for label, cutoff, grid, check_grid in levels:
        solver = Galerkin3D(cutoff)
        rows = []
        for index, member in enumerate(FAMILY):
            row = run_member(solver, member, grid, check_grid)
            row["family_index"] = index
            rows.append(row)
            print(f"{label} member={index} endpoint={row['directed_endpoint_ratio']:.12g} "
                  f"dE={row['relative_energy_drift']:.3e} dH={row['energy_scaled_helicity_drift']:.3e}",
                  flush=True)
        reports[label] = {"cutoff": cutoff, "diagnostic_grids": [grid, check_grid], "results": rows}
    comparisons = [
        {"family_index": index,
         "absolute_endpoint_ratio_difference": abs(fine["directed_endpoint_ratio"] - coarse["directed_endpoint_ratio"])}
        for index, (coarse, fine) in enumerate(zip(reports["K5"]["results"], reports["K7"]["results"]))
    ]
    eligible = [row for row in reports["K7"]["results"] if row["all_local_gates_pass"]]
    maximum = max((row["directed_endpoint_ratio"] for row in eligible), default=None)
    stop = maximum is None or maximum < STOP_RATIO
    return {
        "format": "C265-3DA1-screen", "status": "NUMERICAL_ONLY", "pde_certificate": False,
        "family_size": len(FAMILY), "amplitude": 0.2, "step_size": STEP_SIZE,
        "final_time": FINAL_TIME, "stop_threshold": STOP_RATIO, "levels": reports,
        "comparisons": comparisons, "maximum_gate_passing_K7_ratio": maximum,
        "stop_no_broad_tuning": stop,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(screen(), indent=2, sort_keys=True) + "\n", encoding="ascii")


if __name__ == "__main__":
    main()
