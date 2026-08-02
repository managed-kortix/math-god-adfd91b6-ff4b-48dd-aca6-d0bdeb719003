#!/usr/bin/env python3
"""Validate the frozen C263-MG1 invariant-preserving Galerkin update."""

import argparse
import json
import math
from pathlib import Path

import numpy as np


RHS_GATE = 2.0e-13
TANGENCY_GATE = 2.0e-13
IDENTITY_GATE = 2.0e-13
REVERSAL_GATE = 2.0e-11
NEWTON_RTOL = 5.0e-13
MAX_NEWTON = 12


class GalerkinEuler:
    def __init__(self, cutoff):
        self.cutoff = cutoff
        self.modes = tuple(
            (kx, ky)
            for kx in range(-cutoff, cutoff + 1)
            for ky in range(-cutoff, cutoff + 1)
            if (kx, ky) != (0, 0)
        )
        self.index = {mode: j for j, mode in enumerate(self.modes)}
        self.weights = np.array(
            [1.0 / (kx * kx + ky * ky) for kx, ky in self.modes]
        )
        self.representatives = tuple(
            mode for mode in self.modes if mode[0] > 0 or (mode[0] == 0 and mode[1] > 0)
        )

    def from_real(self, coordinates):
        omega = np.zeros(len(self.modes), dtype=np.complex128)
        for j, mode in enumerate(self.representatives):
            value = coordinates[2 * j] + 1j * coordinates[2 * j + 1]
            omega[self.index[mode]] = value
            omega[self.index[(-mode[0], -mode[1])]] = np.conj(value)
        return omega

    def to_real(self, omega):
        coordinates = np.empty(2 * len(self.representatives))
        for j, mode in enumerate(self.representatives):
            value = omega[self.index[mode]]
            coordinates[2 * j] = value.real
            coordinates[2 * j + 1] = value.imag
        return coordinates

    def bilinear(self, left, right):
        out = np.zeros(len(self.modes), dtype=np.complex128)
        for p_index, (px, py) in enumerate(self.modes):
            p2 = px * px + py * py
            for q_index, (qx, qy) in enumerate(self.modes):
                target = (px + qx, py + qy)
                target_index = self.index.get(target)
                if target_index is not None:
                    cross = px * qy - py * qx
                    out[target_index] -= (cross / p2) * left[p_index] * right[q_index]
        return out

    def rhs(self, omega):
        return self.bilinear(omega, omega)

    def derivative(self, omega, direction):
        return self.bilinear(direction, omega) + self.bilinear(omega, direction)

    def padded_rhs(self, omega):
        side = 4 * self.cutoff + 1
        spectrum = np.zeros((side, side), dtype=np.complex128)
        for mode, value in zip(self.modes, omega):
            spectrum[mode[0] % side, mode[1] % side] = side**2 * value
        freq = np.fft.fftfreq(side) * side
        kx, ky = np.meshgrid(freq, freq, indexing="ij")
        k2 = kx * kx + ky * ky
        nonzero = k2 != 0.0
        psi = np.zeros_like(spectrum)
        psi[nonzero] = -spectrum[nonzero] / k2[nonzero]
        velocity_x = -1j * ky * psi
        velocity_y = 1j * kx * psi
        omega_x = 1j * kx * spectrum
        omega_y = 1j * ky * spectrum
        product = (
            np.fft.ifft2(velocity_x).real * np.fft.ifft2(omega_x).real
            + np.fft.ifft2(velocity_y).real * np.fft.ifft2(omega_y).real
        )
        transformed = -np.fft.fft2(product) / side**2
        return np.array(
            [transformed[kx_value % side, ky_value % side] for kx_value, ky_value in self.modes]
        )

    def inner(self, left, right, invariant):
        weights = np.ones(len(self.modes)) if invariant == "enstrophy" else self.weights
        return float(np.real(np.vdot(left * weights, right)))

    def invariant(self, omega, invariant):
        return 0.5 * self.inner(omega, omega, invariant)

    def normalized_tangency(self, omega, tangent, invariant):
        weights = np.ones(len(self.modes)) if invariant == "enstrophy" else self.weights
        numerator = abs(self.inner(omega, tangent, invariant))
        denominator = np.linalg.norm(np.sqrt(weights) * omega) * np.linalg.norm(
            np.sqrt(weights) * tangent
        )
        return numerator / denominator if denominator else 0.0

    def midpoint_step(self, initial, step_size):
        initial_real = self.to_real(initial)
        solution = initial_real + step_size * self.to_real(self.rhs(initial))
        final_residual = None
        final_scale = None
        for iteration in range(1, MAX_NEWTON + 1):
            endpoint = self.from_real(solution)
            midpoint = 0.5 * (initial + endpoint)
            tangent = self.rhs(midpoint)
            residual = solution - initial_real - step_size * self.to_real(tangent)
            final_residual = np.linalg.norm(self.from_real(residual))
            final_scale = 1.0 + np.linalg.norm(initial) + abs(step_size) * np.linalg.norm(tangent)
            if final_residual <= NEWTON_RTOL * final_scale:
                return endpoint, {
                    "iterations": iteration,
                    "residual_norm": float(final_residual),
                    "residual_scale": float(final_scale),
                }
            dimension = len(solution)
            jacobian = np.eye(dimension)
            for column in range(dimension):
                basis = np.zeros(dimension)
                basis[column] = 1.0
                direction = self.from_real(basis)
                derivative = 0.5 * self.derivative(midpoint, direction)
                jacobian[:, column] -= step_size * self.to_real(derivative)
            solution += np.linalg.solve(jacobian, -residual)
        raise RuntimeError(
            f"Newton failed: residual={final_residual:.3e}, scale={final_scale:.3e}"
        )


def synthetic_state(solver):
    coordinates = []
    for kx, ky in solver.representatives:
        k2 = kx * kx + ky * ky
        coordinates.extend(
            (
                math.cos(0.37 * kx + 0.19 * ky) / (1.0 + k2) ** 2,
                math.sin(0.23 * kx - 0.41 * ky) / (1.0 + k2) ** 2,
            )
        )
    return solver.from_real(np.array(coordinates))


def relative_norm(value, reference):
    denominator = np.linalg.norm(reference)
    return float(np.linalg.norm(value) / denominator) if denominator else float(np.linalg.norm(value))


def one_step_record(solver, initial, endpoint, step_size, solve):
    midpoint = 0.5 * (initial + endpoint)
    tangent = solver.rhs(midpoint)
    residual = endpoint - initial - step_size * tangent
    record = {"solve": solve, "invariants": {}}
    for invariant in ("energy", "enstrophy"):
        weights = (
            np.ones(len(solver.modes))
            if invariant == "enstrophy"
            else solver.weights
        )
        before = solver.invariant(initial, invariant)
        after = solver.invariant(endpoint, invariant)
        change = after - before
        tangency_term = step_size * solver.inner(midpoint, tangent, invariant)
        residual_term = solver.inner(midpoint, residual, invariant)
        residual_bound = float(
            np.linalg.norm(np.sqrt(weights) * midpoint)
            * np.linalg.norm(np.sqrt(weights) * residual)
        )
        closure = change - tangency_term - residual_term
        scale = 1.0 + abs(change) + abs(tangency_term) + abs(residual_term)
        record["invariants"][invariant] = {
            "absolute_defect": abs(change),
            "relative_defect": abs(change) / before,
            "tangency_term": tangency_term,
            "residual_term": residual_term,
            "residual_bound": residual_bound,
            "identity_relative_closure": abs(closure) / scale,
        }
    return record


def validate():
    algebra = []
    for cutoff in (2, 3):
        solver = GalerkinEuler(cutoff)
        omega = synthetic_state(solver)
        direct = solver.rhs(omega)
        padded = solver.padded_rhs(omega)
        algebra.append({
            "cutoff": cutoff,
            "rhs_relative_discrepancy": relative_norm(direct - padded, direct),
            "energy_normalized_tangency": solver.normalized_tangency(omega, direct, "energy"),
            "enstrophy_normalized_tangency": solver.normalized_tangency(
                omega, direct, "enstrophy"
            ),
        })

    solver = GalerkinEuler(3)
    initial = synthetic_state(solver)
    state = initial.copy()
    records = []
    for _ in range(32):
        endpoint, solve = solver.midpoint_step(state, 1.0 / 64.0)
        records.append(one_step_record(solver, state, endpoint, 1.0 / 64.0, solve))
        state = endpoint
    forward_endpoint = state.copy()
    for _ in range(32):
        state, _ = solver.midpoint_step(state, -1.0 / 64.0)

    max_residual_ratio = max(
        row["solve"]["residual_norm"] / row["solve"]["residual_scale"] for row in records
    )
    maxima = {}
    for invariant in ("energy", "enstrophy"):
        maxima[invariant] = {
            key: max(row["invariants"][invariant][key] for row in records)
            for key in (
                "absolute_defect",
                "relative_defect",
                "residual_bound",
                "identity_relative_closure",
            )
        }
    report = {
        "format": "C263-MG1-validation",
        "numerical_only": True,
        "cycle258_family_used": False,
        "method": "implicit midpoint on exact square Galerkin convolution",
        "algebra_replay": algebra,
        "trajectory": {
            "cutoff": 3,
            "step_size": 1.0 / 64.0,
            "forward_steps": 32,
            "max_newton_residual_ratio": max_residual_ratio,
            "max_newton_iterations": max(row["solve"]["iterations"] for row in records),
            "maximum_step_defects": maxima,
            "forward_endpoint_energy_relative_drift": abs(
                solver.invariant(forward_endpoint, "energy") / solver.invariant(initial, "energy") - 1.0
            ),
            "forward_endpoint_enstrophy_relative_drift": abs(
                solver.invariant(forward_endpoint, "enstrophy")
                / solver.invariant(initial, "enstrophy")
                - 1.0
            ),
            "reversal_relative_state_error": relative_norm(state - initial, initial),
        },
        "gates": {
            "rhs_replay": RHS_GATE,
            "normalized_tangency": TANGENCY_GATE,
            "identity_closure": IDENTITY_GATE,
            "newton_residual_ratio": NEWTON_RTOL,
            "reversal": REVERSAL_GATE,
        },
    }
    failures = []
    if max(row["rhs_relative_discrepancy"] for row in algebra) > RHS_GATE:
        failures.append("RHS replay")
    if max(
        max(row["energy_normalized_tangency"], row["enstrophy_normalized_tangency"])
        for row in algebra
    ) > TANGENCY_GATE:
        failures.append("invariant tangency")
    if max_residual_ratio > NEWTON_RTOL:
        failures.append("Newton residual")
    if max(maxima[name]["identity_relative_closure"] for name in maxima) > IDENTITY_GATE:
        failures.append("defect identity")
    if report["trajectory"]["reversal_relative_state_error"] > REVERSAL_GATE:
        failures.append("reversal")
    report["passed"] = not failures
    report["failures"] = failures
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = validate()
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="ascii")
    else:
        print(text, end="")
    if not report["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
