#!/usr/bin/env python3
"""Numerical-only periodic contour-dynamics scout for opposite-sign patches."""

import argparse
import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np


STATUS = "NUMERICAL_SCOUT_ONLY"


@dataclass(frozen=True)
class Geometry:
    semimajor: float
    aspect: float
    gap: float
    angle_index: int

    @property
    def semiminor(self):
        return self.semimajor * self.aspect

    @property
    def angle(self):
        return self.angle_index * math.pi / 4.0

    @property
    def center_offset(self):
        return self.semimajor + 0.5 * self.gap


def geometries():
    return [
        Geometry(*values)
        for values in itertools.product(
            (0.45, 0.65), (0.45, 0.70), (0.15, 0.30), range(3)
        )
    ]


def periodic_delta(value):
    return (value + math.pi) % (2.0 * math.pi) - math.pi


def signed_area(curve):
    nxt = np.roll(curve, -1, axis=0)
    delta = periodic_delta(nxt - curve)
    unwrapped = curve[0] + np.vstack((np.zeros(2), np.cumsum(delta[:-1], axis=0)))
    unext = np.vstack((unwrapped, unwrapped[0]))
    return 0.5 * float(
        np.sum(unext[:-1, 0] * unext[1:, 1] - unext[1:, 0] * unext[:-1, 1])
    )


def ellipse(center, a, b, angle, points):
    parameter = 2.0 * math.pi * np.arange(points) / points
    base = np.column_stack((a * np.cos(parameter), b * np.sin(parameter)))
    cosine, sine = math.cos(angle), math.sin(angle)
    rotation = np.array(((cosine, -sine), (sine, cosine)))
    return (base @ rotation.T + center + math.pi) % (2.0 * math.pi) - math.pi


def initial_contours(geometry, points):
    d = geometry.center_offset
    positive = ellipse((d, 0.0), geometry.semimajor, geometry.semiminor, 0.0, points)
    negative = ellipse(
        (-d, 0.0),
        geometry.semimajor,
        geometry.semiminor,
        geometry.angle,
        points,
    )
    return np.stack((positive, negative))


class PeriodicContourSolver:
    def __init__(self, points, kernel_grid=512, kernel_cutoff=96, velocity_grid=64):
        self.points = points
        self.kernel_grid = kernel_grid
        self.velocity_grid = velocity_grid
        frequency = np.fft.fftfreq(kernel_grid) * kernel_grid
        kx, ky = np.meshgrid(frequency, frequency, indexing="ij")
        k2 = kx * kx + ky * ky
        coefficients = np.zeros((kernel_grid, kernel_grid), dtype=np.complex128)
        retained = (k2 > 0) & (np.abs(kx) <= kernel_cutoff) & (np.abs(ky) <= kernel_cutoff)
        coefficients[retained] = -(kernel_grid**2) / (4.0 * math.pi**2 * k2[retained])
        self.green = np.fft.ifft2(coefficients).real

    def interpolate_green(self, dx, dy):
        scale = self.kernel_grid / (2.0 * math.pi)
        gx = np.mod(dx, 2.0 * math.pi) * scale
        gy = np.mod(dy, 2.0 * math.pi) * scale
        ix = np.floor(gx).astype(int)
        iy = np.floor(gy).astype(int)
        fx, fy = gx - ix, gy - iy
        ix1, iy1 = (ix + 1) % self.kernel_grid, (iy + 1) % self.kernel_grid
        return (
            (1.0 - fx) * (1.0 - fy) * self.green[ix, iy]
            + fx * (1.0 - fy) * self.green[ix1, iy]
            + (1.0 - fx) * fy * self.green[ix, iy1]
            + fx * fy * self.green[ix1, iy1]
        )

    def rhs(self, contours):
        targets = contours.reshape((-1, 2))
        velocity = np.zeros_like(targets)
        signs = (1.0, -1.0)
        for sign, source in zip(signs, contours):
            segments = periodic_delta(np.roll(source, -1, axis=0) - source)
            midpoints = source + 0.5 * segments
            dx = targets[:, None, 0] - midpoints[None, :, 0]
            dy = targets[:, None, 1] - midpoints[None, :, 1]
            weights = self.interpolate_green(dx, dy)
            velocity -= sign * weights @ segments
        return velocity.reshape(contours.shape)

    @staticmethod
    def reparameterize(curve):
        segments = periodic_delta(np.roll(curve, -1, axis=0) - curve)
        lengths = np.linalg.norm(segments, axis=1)
        cumulative = np.concatenate(([0.0], np.cumsum(lengths)))
        targets = np.arange(len(curve)) * cumulative[-1] / len(curve)
        indices = np.minimum(np.searchsorted(cumulative, targets, side="right") - 1, len(curve) - 1)
        fractions = (targets - cumulative[indices]) / lengths[indices]
        result = curve[indices] + fractions[:, None] * segments[indices]
        return (result + math.pi) % (2.0 * math.pi) - math.pi

    def step(self, contours, h):
        k1 = self.rhs(contours)
        k2 = self.rhs(contours + 0.5 * h * k1)
        k3 = self.rhs(contours + 0.5 * h * k2)
        k4 = self.rhs(contours + h * k3)
        updated = contours + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        return np.stack([self.reparameterize(curve) for curve in updated])

    def velocity_l3(self, contours):
        n = self.velocity_grid
        frequency = np.fft.fftfreq(n) * n
        kx, ky = np.meshgrid(frequency, frequency, indexing="ij")
        k2 = kx * kx + ky * ky
        omega = np.zeros((n, n), dtype=np.complex128)
        for sign, curve in zip((1.0, -1.0), contours):
            segments = periodic_delta(np.roll(curve, -1, axis=0) - curve)
            midpoints = curve + 0.5 * segments
            for i in range(n):
                phase = np.exp(-1j * (kx[i, :, None] * midpoints[None, :, 0] + ky[i, :, None] * midpoints[None, :, 1]))
                boundary = np.sum(
                    phase * (kx[i, :, None] * segments[None, :, 1] - ky[i, :, None] * segments[None, :, 0]),
                    axis=1,
                )
                nonzero = k2[i] > 0
                omega[i, nonzero] += sign * 1j * boundary[nonzero] / (4.0 * math.pi**2 * k2[i, nonzero])
        ux = np.zeros_like(omega)
        uy = np.zeros_like(omega)
        nonzero = k2 > 0
        ux[nonzero] = 1j * ky[nonzero] * omega[nonzero] / k2[nonzero]
        uy[nonzero] = -1j * kx[nonzero] * omega[nonzero] / k2[nonzero]
        ux = np.fft.ifft2(n * n * ux).real
        uy = np.fft.ifft2(n * n * uy).real
        return float(np.mean(np.hypot(ux, uy) ** 3) ** (1.0 / 3.0))


def curve_metrics(curve):
    segments = periodic_delta(np.roll(curve, -1, axis=0) - curve)
    lengths = np.linalg.norm(segments, axis=1)
    perimeter = float(np.sum(lengths))
    area = abs(signed_area(curve))
    cumulative = np.concatenate(([0.0], np.cumsum(lengths)))
    chord_arc = 1.0
    for i in range(len(curve)):
        for j in range(i + 2, len(curve)):
            if i == 0 and j == len(curve) - 1:
                continue
            arc = cumulative[j] - cumulative[i]
            arc = min(arc, perimeter - arc)
            chord = np.linalg.norm(periodic_delta(curve[j] - curve[i]))
            chord_arc = max(chord_arc, arc / max(chord, 1e-14))
    centered = curve - np.mean(curve, axis=0)
    mode3 = abs(np.mean((centered[:, 0] + 1j * centered[:, 1]) * np.exp(-6j * math.pi * np.arange(len(curve)) / len(curve))))
    return {
        "area": area,
        "chord_arc": chord_arc,
        "isoperimetric_ratio": perimeter * perimeter / (4.0 * math.pi * area),
        "normalized_mode3": mode3 / math.sqrt(area),
    }


def diagnostics(contours):
    first, second = contours
    differences = periodic_delta(first[:, None, :] - second[None, :, :])
    separation = float(np.min(np.linalg.norm(differences, axis=2)))
    metrics = [curve_metrics(curve) for curve in contours]
    return separation, metrics


def run_member(solver, geometry, dt, final_time, sample_dt):
    initial = np.stack(
        [solver.reparameterize(curve) for curve in initial_contours(geometry, solver.points)]
    )
    initial_sep, initial_metrics = diagnostics(initial)
    samples = []
    worst_separation = initial_sep
    worst_chord_arc = max(item["chord_arc"] for item in initial_metrics)
    maximum_area_drift = 0.0
    maximum_shape_change = 0.0
    for direction in (-1, 1):
        contours = initial.copy()
        steps = round(final_time / dt)
        stride = max(1, round(sample_dt / dt))
        for step in range(steps + 1):
            if step % stride == 0 or step == steps:
                time = direction * step * dt
                l3 = solver.velocity_l3(contours)
                separation, metrics = diagnostics(contours)
                worst_separation = min(worst_separation, separation)
                worst_chord_arc = max(worst_chord_arc, *(item["chord_arc"] for item in metrics))
                maximum_area_drift = max(
                    maximum_area_drift,
                    *(abs(metrics[i]["area"] / initial_metrics[i]["area"] - 1.0) for i in range(2)),
                )
                maximum_shape_change = max(
                    maximum_shape_change,
                    *(abs(metrics[i]["isoperimetric_ratio"] - initial_metrics[i]["isoperimetric_ratio"]) for i in range(2)),
                    *(abs(metrics[i]["normalized_mode3"] - initial_metrics[i]["normalized_mode3"]) for i in range(2)),
                )
                samples.append((time, l3))
            if step < steps:
                contours = solver.step(contours, direction * dt)
    samples.sort()
    minimum = min(samples, key=lambda item: item[1])
    maximum = max(samples, key=lambda item: item[1])
    return {
        "geometry": asdict(geometry),
        "variation_ratio": maximum[1] / minimum[1],
        "minimum": {"time": minimum[0], "l3": minimum[1]},
        "maximum": {"time": maximum[0], "l3": maximum[1]},
        "minimum_node_separation": worst_separation,
        "maximum_chord_arc": worst_chord_arc,
        "maximum_relative_area_drift": maximum_area_drift,
        "nonrelative_shape_change": maximum_shape_change,
    }


def screen(points, dt, final_time, sample_dt, limit=None, indices=None):
    complete_family = geometries()
    family = (
        [complete_family[index] for index in indices]
        if indices is not None
        else complete_family[:limit]
    )
    solver = PeriodicContourSolver(points)
    results = [run_member(solver, geometry, dt, final_time, sample_dt) for geometry in family]
    results.sort(key=lambda row: -row["variation_ratio"])
    return {
        "status": STATUS,
        "pde_certificate": False,
        "method": "RK4 periodic Fourier-Green panel contour dynamics",
        "contour_points_per_patch": points,
        "kernel_grid": solver.kernel_grid,
        "kernel_fourier_cutoff": 96,
        "velocity_cubature_grid": solver.velocity_grid,
        "dt": dt,
        "final_time_each_direction": final_time,
        "sample_dt": sample_dt,
        "family_size": len(family),
        "promotion_threshold": 1.2,
        "promotions": sum(row["variation_ratio"] > 1.2 for row in results),
        "top_results": results,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--points", type=int, default=64)
    parser.add_argument("--dt", type=float, default=1.0 / 256.0)
    parser.add_argument("--time", type=float, default=0.75)
    parser.add_argument("--sample-dt", type=float, default=3.0 / 64.0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--indices", type=int, nargs="+")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = screen(
        args.points, args.dt, args.time, args.sample_dt, args.limit, args.indices
    )
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        f"family={report['family_size']} points={args.points} "
        f"max_variation={report['top_results'][0]['variation_ratio']:.12g} "
        f"promotions={report['promotions']}"
    )


if __name__ == "__main__":
    main()
