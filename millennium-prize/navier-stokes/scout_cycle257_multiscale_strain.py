#!/usr/bin/env python3
import argparse
import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np


STATUS = "NUMERICAL_SCOUT_ONLY"


@dataclass(frozen=True)
class Member:
    alpha: float
    rho: float
    epsilon: float
    beta: float
    packet: int
    rotation: int
    phase_seed: int


PACKETS = (
    (((2, 1), (5, 2), (9, 4)), (1.0, 0.5, 0.25)),
    (((2, 1), (5, 2), (9, 4)), (1.0, -0.5, 0.25)),
    (((2, 1), (5, -2), (9, 4)), (1.0, 0.5, -0.25)),
)


def members():
    values = itertools.product(
        (0.5, 1.0, 2.0),
        (-0.5, 0.0, 0.5),
        (1.0 / 16.0, 1.0 / 8.0),
        (1.0 / 16.0, 1.0 / 8.0, 1.0 / 4.0),
        range(len(PACKETS)),
        range(4),
        range(8),
    )
    return [Member(*value) for value in values]


class Euler2D:
    def __init__(self, n):
        self.n = n
        freq = np.fft.fftfreq(n) * n
        self.kx, self.ky = np.meshgrid(freq, freq, indexing="ij")
        self.k2 = self.kx * self.kx + self.ky * self.ky
        self.nonzero = self.k2 != 0
        cutoff = n // 3
        self.mask = (np.abs(self.kx) <= cutoff) & (np.abs(self.ky) <= cutoff)

    def index(self, k):
        return k % self.n

    def add_mode(self, out, kx, ky, coefficient):
        if abs(kx) <= self.n // 3 and abs(ky) <= self.n // 3:
            out[self.index(kx), self.index(ky)] += self.n * self.n * coefficient

    @staticmethod
    def rotate(q, turns):
        x, y = q
        for _ in range(turns):
            x, y = -y, x
        return x, y

    def initial(self, member):
        omega = np.zeros((self.n, self.n), dtype=np.complex128)
        self.add_mode(omega, 1, 0, 0.5)
        self.add_mode(omega, -1, 0, 0.5)
        self.add_mode(omega, 0, 1, 0.5 * member.alpha)
        self.add_mode(omega, 0, -1, 0.5 * member.alpha)
        self.add_mode(omega, 1, 1, 0.5 * member.rho)
        self.add_mode(omega, -1, -1, 0.5 * member.rho)

        directions, weights = PACKETS[member.packet]
        cutoff = self.n // 3
        for j, (direction, weight) in enumerate(zip(directions, weights)):
            qx, qy = self.rotate(direction, member.rotation)
            qnorm = math.hypot(qx, qy)
            phase_index = (member.phase_seed * (2 * j + 1) + j * j) % 16
            phase = 2.0 * math.pi * phase_index / 16.0
            max_harmonic = min(
                cutoff // max(1, abs(qx)), cutoff // max(1, abs(qy))
            )
            for harmonic in range(1, max_harmonic + 1):
                coefficient = (
                    member.beta
                    * weight
                    * qnorm
                    * 1j
                    * harmonic
                    * math.exp(-member.epsilon * harmonic * harmonic)
                    * np.exp(1j * harmonic * phase)
                )
                self.add_mode(omega, harmonic * qx, harmonic * qy, coefficient)
                self.add_mode(
                    omega, -harmonic * qx, -harmonic * qy, np.conj(coefficient)
                )
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
        result = -np.fft.fft2(ux * wx + uy * wy)
        result[~self.mask] = 0.0
        result[0, 0] = 0.0
        return result

    def l3(self, omega):
        u, v = self.velocity(omega)
        speed = np.hypot(np.fft.ifft2(u).real, np.fft.ifft2(v).real)
        return float(np.mean(speed**3) ** (1.0 / 3.0))

    def invariants(self, omega):
        u, v = self.velocity(omega)
        energy = np.sum(np.abs(u) ** 2 + np.abs(v) ** 2) / self.n**4
        enstrophy = np.sum(np.abs(omega) ** 2) / self.n**4
        return float(energy), float(enstrophy)

    def log_l3_derivative(self, omega):
        tangent = self.rhs(omega)
        u, v = self.velocity(omega)
        du, dv = self.velocity(tangent)
        u = np.fft.ifft2(u).real
        v = np.fft.ifft2(v).real
        du = np.fft.ifft2(du).real
        dv = np.fft.ifft2(dv).real
        speed = np.hypot(u, v)
        return float(np.mean(speed * (u * du + v * dv)) / np.mean(speed**3))

    def integrate(self, initial, direction, dt, final_time, sample_dt):
        omega = initial.copy()
        steps = round(final_time / dt)
        stride = max(1, round(sample_dt / dt))
        samples = [(0.0, self.l3(omega))]
        for step in range(1, steps + 1):
            h = direction * dt
            k1 = self.rhs(omega)
            k2 = self.rhs(omega + 0.5 * h * k1)
            k3 = self.rhs(omega + 0.5 * h * k2)
            k4 = self.rhs(omega + h * k3)
            omega += (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
            omega[~self.mask] = 0.0
            if step % stride == 0 or step == steps:
                samples.append((direction * step * dt, self.l3(omega)))
        return omega, samples


def screen(n, shortlist, dt, final_time, sample_dt):
    solver = Euler2D(n)
    family = members()
    ranked = []
    for index, member in enumerate(family):
        derivative = solver.log_l3_derivative(solver.initial(member))
        ranked.append((abs(derivative), derivative, index, member))
    ranked.sort(reverse=True, key=lambda row: (row[0], -row[2]))

    results = []
    for score, derivative, index, member in ranked[:shortlist]:
        initial = solver.initial(member)
        before = solver.invariants(initial)
        all_samples = []
        max_energy_drift = 0.0
        max_enstrophy_drift = 0.0
        for direction in (-1, 1):
            endpoint, samples = solver.integrate(
                initial, direction, dt, final_time, sample_dt
            )
            all_samples.extend(samples)
            after = solver.invariants(endpoint)
            max_energy_drift = max(max_energy_drift, abs(after[0] / before[0] - 1.0))
            max_enstrophy_drift = max(
                max_enstrophy_drift, abs(after[1] / before[1] - 1.0)
            )
        all_samples.sort()
        minimum = min(all_samples, key=lambda row: row[1])
        maximum = max(all_samples, key=lambda row: row[1])
        results.append(
            {
                "family_index": index,
                "member": asdict(member),
                "absolute_initial_log_l3_derivative": score,
                "initial_log_l3_derivative": derivative,
                "variation_ratio": maximum[1] / minimum[1],
                "minimum": {"time": minimum[0], "l3": minimum[1]},
                "maximum": {"time": maximum[0], "l3": maximum[1]},
                "relative_energy_drift": max_energy_drift,
                "relative_enstrophy_drift": max_enstrophy_drift,
            }
        )
    results.sort(key=lambda row: (-row["variation_ratio"], row["family_index"]))
    return {
        "status": STATUS,
        "pde_certificate": False,
        "resolution": n,
        "cutoff": n // 3,
        "dt": dt,
        "final_time_each_direction": final_time,
        "sample_dt": sample_dt,
        "family_size": len(family),
        "shortlist_size": shortlist,
        "promotion_threshold": 1.05,
        "top_results": results,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=64)
    parser.add_argument("--shortlist", type=int, default=16)
    parser.add_argument("--dt", type=float, default=1.0 / 1024.0)
    parser.add_argument("--time", type=float, default=0.5)
    parser.add_argument("--sample-dt", type=float, default=1.0 / 64.0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = screen(args.n, args.shortlist, args.dt, args.time, args.sample_dt)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        f"N={args.n} family={report['family_size']} shortlist={args.shortlist} "
        f"max_variation={report['top_results'][0]['variation_ratio']:.12g}"
    )


if __name__ == "__main__":
    main()
