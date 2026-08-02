#!/usr/bin/env python3
import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np


STATUS = "NUMERICAL_SCOUT_ONLY"
DELTAS = (0.025, 0.075)


@dataclass(frozen=True)
class Label:
    rho: float
    center: int
    direction_seed: int
    sign: int
    delta: float


def tangent_direction(x, modes, seed):
    j = np.arange(1, len(x) + 1, dtype=float)
    d = np.sin((seed + 1) * j * math.sqrt(2.0))
    d += 0.5 * np.cos((seed + 2) * j * 0.7548776662466927)
    k2 = np.repeat([kx * kx + ky * ky for kx, ky in modes], 2).astype(float)
    ge = k2 * x
    gz = k2 * k2 * x
    gram = np.array([[ge @ ge, ge @ gz], [ge @ gz, gz @ gz]])
    rhs = np.array([ge @ d, gz @ d])
    d -= np.column_stack((ge, gz)) @ np.linalg.solve(gram, rhs)
    return d / np.linalg.norm(d)


def retract(x, modes, rho):
    k2 = np.repeat([kx * kx + ky * ky for kx, ky in modes], 2).astype(float)
    weights = 0.5 * k2

    def ratio(beta):
        y = x * np.exp(beta * (k2 - rho))
        return float(np.sum(weights * k2 * y * y) / np.sum(weights * y * y))

    lo, hi = -1.0, 1.0
    while ratio(lo) > rho:
        lo *= 2.0
    while ratio(hi) < rho:
        hi *= 2.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if ratio(mid) < rho:
            lo = mid
        else:
            hi = mid
    y = x * np.exp(0.5 * (lo + hi) * (k2 - rho))
    return y / math.sqrt(float(np.sum(weights * y * y)))


def frozen_family(source):
    modes = source["modes"]
    family = []
    for center, candidate in enumerate(source["candidates"]):
        x = np.asarray(candidate["coefficients"], dtype=float)
        rho = float(candidate["rho"])
        family.append((Label(rho, center, -1, 0, 0.0), x.copy()))
        for seed in range(2):
            direction = tangent_direction(x, modes, seed)
            for sign in (-1, 1):
                for delta in DELTAS:
                    y = retract(x + sign * delta * direction, modes, rho)
                    family.append((Label(rho, center, seed, sign, delta), y))
    return modes, family


class Euler2D:
    def __init__(self, n):
        self.n = n
        freq = np.fft.fftfreq(n) * n
        self.kx, self.ky = np.meshgrid(freq, freq, indexing="ij")
        self.k2 = self.kx * self.kx + self.ky * self.ky
        self.nonzero = self.k2 != 0
        cutoff = n // 3
        self.mask = (np.abs(self.kx) <= cutoff) & (np.abs(self.ky) <= cutoff)

    def initial(self, modes, coefficients):
        omega = np.zeros((self.n, self.n), dtype=np.complex128)
        for j, (kx, ky) in enumerate(modes):
            psi = 0.5 * (coefficients[2 * j] - 1j * coefficients[2 * j + 1])
            value = -self.n**2 * (kx * kx + ky * ky) * psi
            omega[kx % self.n, ky % self.n] += value
            omega[-kx % self.n, -ky % self.n] += np.conj(value)
        omega[~self.mask] = 0.0
        return omega

    def velocity(self, omega):
        psi = np.zeros_like(omega)
        psi[self.nonzero] = -omega[self.nonzero] / self.k2[self.nonzero]
        return -1j * self.ky * psi, 1j * self.kx * psi

    def rhs(self, omega):
        u, v = self.velocity(omega)
        ux = np.fft.ifft2(u).real
        uy = np.fft.ifft2(v).real
        wx = np.fft.ifft2(1j * self.kx * omega).real
        wy = np.fft.ifft2(1j * self.ky * omega).real
        out = -np.fft.fft2(ux * wx + uy * wy)
        out[~self.mask] = 0.0
        out[0, 0] = 0.0
        return out

    def diagnostics(self, omega, tangent=None):
        u, v = self.velocity(omega)
        ux = np.fft.ifft2(u).real
        uy = np.fft.ifft2(v).real
        speed = np.hypot(ux, uy)
        cube = float(np.mean(speed**3))
        l3 = cube ** (1.0 / 3.0)
        derivative = None
        if tangent is not None:
            du, dv = self.velocity(tangent)
            du = np.fft.ifft2(du).real
            dv = np.fft.ifft2(dv).real
            derivative = float(np.mean(speed * (ux * du + uy * dv)) / cube)
        return l3, derivative

    def invariants(self, omega):
        u, v = self.velocity(omega)
        energy = np.sum(np.abs(u) ** 2 + np.abs(v) ** 2) / self.n**4
        enstrophy = np.sum(np.abs(omega) ** 2) / self.n**4
        return float(energy), float(enstrophy)

    def trajectory(self, initial, direction, dt, final_time, sample_dt):
        omega = initial.copy()
        steps = round(final_time / dt)
        stride = round(sample_dt / dt)
        tangent = self.rhs(omega)
        l3, derivative = self.diagnostics(omega, tangent)
        samples = [(0.0, l3, 0.0, 0.0)]
        integrated = 0.0
        previous_derivative = derivative
        initial_l3 = l3
        for step in range(1, steps + 1):
            h = direction * dt
            k1 = self.rhs(omega)
            k2 = self.rhs(omega + 0.5 * h * k1)
            k3 = self.rhs(omega + 0.5 * h * k2)
            k4 = self.rhs(omega + h * k3)
            omega += (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
            omega[~self.mask] = 0.0
            if step % stride == 0 or step == steps:
                tangent = self.rhs(omega)
                l3, derivative = self.diagnostics(omega, tangent)
                signed_interval = direction * stride * dt
                integrated += 0.5 * signed_interval * (previous_derivative + derivative)
                direct = math.log(l3 / initial_l3)
                samples.append((direction * step * dt, l3, integrated, direct))
                previous_derivative = derivative
        return omega, samples


def run_member(solver, modes, label, coefficients, dt, final_time, sample_dt):
    initial = solver.initial(modes, coefficients)
    initial_invariants = solver.invariants(initial)
    all_samples = []
    energy_drift = 0.0
    enstrophy_drift = 0.0
    for direction in (-1, 1):
        endpoint, samples = solver.trajectory(
            initial, direction, dt, final_time, sample_dt
        )
        all_samples.extend(samples)
        final_invariants = solver.invariants(endpoint)
        energy_drift = max(
            energy_drift, abs(final_invariants[0] / initial_invariants[0] - 1.0)
        )
        enstrophy_drift = max(
            enstrophy_drift,
            abs(final_invariants[1] / initial_invariants[1] - 1.0),
        )
    minimum = min(all_samples, key=lambda row: (row[1], row[0]))
    maximum = max(all_samples, key=lambda row: (row[1], -row[0]))
    best_integral = max(all_samples, key=lambda row: (row[2], -abs(row[0]), -row[0]))
    discrepancy = max(abs(row[2] - row[3]) for row in all_samples)
    return {
        "label": asdict(label),
        "variation_ratio": maximum[1] / minimum[1],
        "minimum": {"time": minimum[0], "l3": minimum[1]},
        "maximum": {"time": maximum[0], "l3": maximum[1]},
        "best_integrated_log_growth": {
            "time": best_integral[0],
            "trapezoidal_integral": best_integral[2],
            "direct_log_ratio": best_integral[3],
        },
        "max_integral_identity_discrepancy": discrepancy,
        "relative_energy_drift": energy_drift,
        "relative_enstrophy_drift": enstrophy_drift,
    }


def screen(source, n, dt, final_time, sample_dt, limit=None):
    modes, family = frozen_family(source)
    if limit is not None:
        family = family[:limit]
    solver = Euler2D(n)
    results = []
    for index, (label, coefficients) in enumerate(family):
        result = run_member(
            solver, modes, label, coefficients, dt, final_time, sample_dt
        )
        result["family_index"] = index
        results.append(result)
        print(
            f"N={n} member={index + 1}/{len(family)} "
            f"ratio={result['variation_ratio']:.12g}",
            flush=True,
        )
    results.sort(key=lambda row: (-row["variation_ratio"], row["family_index"]))
    return {
        "format": "cycle258-integrated-l3-v1",
        "status": STATUS,
        "pde_certificate": False,
        "resolution": n,
        "cutoff": n // 3,
        "dt": dt,
        "final_time_each_direction": final_time,
        "sample_dt": sample_dt,
        "family_size": len(family),
        "promotion_threshold": 1.1,
        "objective": "time-integrated logarithmic velocity-L3 growth",
        "results": results,
    }


def compare_reports(coarse, fine):
    coarse_by_index = {row["family_index"]: row for row in coarse["results"]}
    fine_by_index = {row["family_index"]: row for row in fine["results"]}
    if coarse_by_index.keys() != fine_by_index.keys():
        raise ValueError("resolution reports have different frozen families")
    comparisons = []
    for index in sorted(coarse_by_index):
        coarse_row = coarse_by_index[index]
        fine_row = fine_by_index[index]
        if coarse_row["label"] != fine_row["label"]:
            raise ValueError(f"label mismatch for family index {index}")
        comparisons.append(
            {
                "family_index": index,
                "label": fine_row["label"],
                "ratio_n64": coarse_row["variation_ratio"],
                "ratio_n128": fine_row["variation_ratio"],
                "signed_ratio_difference": (
                    fine_row["variation_ratio"] - coarse_row["variation_ratio"]
                ),
            }
        )
    winner = fine["results"][0]
    return {
        "format": "cycle258-integrated-l3-comparison-v1",
        "status": STATUS,
        "pde_certificate": False,
        "promotion_threshold": fine["promotion_threshold"],
        "family_size": len(comparisons),
        "n64_promotions": sum(
            row["variation_ratio"] > coarse["promotion_threshold"]
            for row in coarse["results"]
        ),
        "n128_promotions": sum(
            row["variation_ratio"] > fine["promotion_threshold"]
            for row in fine["results"]
        ),
        "stop_for_no_ratio_above_threshold": not any(
            row["variation_ratio"] > fine["promotion_threshold"]
            for row in fine["results"]
        ),
        "winner_n128": winner,
        "max_absolute_ratio_difference": max(
            abs(row["signed_ratio_difference"]) for row in comparisons
        ),
        "max_integral_identity_discrepancy": {
            "n64": max(
                row["max_integral_identity_discrepancy"]
                for row in coarse["results"]
            ),
            "n128": max(
                row["max_integral_identity_discrepancy"] for row in fine["results"]
            ),
        },
        "max_relative_energy_drift": {
            "n64": max(row["relative_energy_drift"] for row in coarse["results"]),
            "n128": max(row["relative_energy_drift"] for row in fine["results"]),
        },
        "max_relative_enstrophy_drift": {
            "n64": max(row["relative_enstrophy_drift"] for row in coarse["results"]),
            "n128": max(row["relative_enstrophy_drift"] for row in fine["results"]),
        },
        "comparisons": comparisons,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--n", type=int, choices=(64, 128), required=True)
    parser.add_argument("--dt", type=float)
    parser.add_argument("--time", type=float, default=2.5)
    parser.add_argument("--sample-dt", type=float, default=1.0 / 64.0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    dt = args.dt if args.dt is not None else 1.0 / (2 * args.n)
    source = json.loads(args.source.read_text(encoding="ascii"))
    report = screen(source, args.n, dt, args.time, args.sample_dt, args.limit)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
