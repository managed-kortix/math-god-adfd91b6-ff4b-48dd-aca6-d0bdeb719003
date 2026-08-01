#!/usr/bin/env python3
"""Exact setup and floating screen for small 2D Euler triad chains."""

from __future__ import annotations

import argparse
import cmath
import json
import math
import random
from fractions import Fraction
from pathlib import Path


Mode = tuple[int, int]


def neg(k: Mode) -> Mode:
    return (-k[0], -k[1])


def add(p: Mode, q: Mode) -> Mode:
    return (p[0] + q[0], p[1] + q[1])


def norm2(k: Mode) -> int:
    return k[0] * k[0] + k[1] * k[1]


def cross(p: Mode, q: Mode) -> int:
    return p[0] * q[1] - p[1] * q[0]


def canonical(k: Mode) -> Mode:
    return k if k[0] > 0 or (k[0] == 0 and k[1] > 0) else neg(k)


def coefficient(p: Mode, q: Mode) -> Fraction:
    """Symmetric coefficient in dot(omega_k)=sum_{p+q=k} C omega_p omega_q."""
    return Fraction(cross(p, q), 2) * (Fraction(1, norm2(q)) - Fraction(1, norm2(p)))


def symmetric_support(representatives: list[Mode]) -> tuple[Mode, ...]:
    return tuple(sorted(set(representatives) | {neg(k) for k in representatives}))


def active_triads(bound: int) -> list[tuple[Mode, Mode, Mode]]:
    reps = [(x, y) for x in range(bound + 1) for y in range(-bound, bound + 1)
            if (x > 0 or y > 0) and (x or y)]
    modes = symmetric_support(reps)
    found = set()
    for p in modes:
        for q in modes:
            k = neg(add(p, q))
            if k in modes and coefficient(p, q):
                found.add(tuple(sorted((canonical(p), canonical(q), canonical(k)))))
    return sorted(found)


def enumerate_chains(bound: int, length: int, limit: int) -> list[tuple[Mode, ...]]:
    """Enumerate connected unions in the active-triad incidence graph."""
    triads = active_triads(bound)
    chains = {frozenset(t) for t in triads}
    for _ in range(1, length):
        extended = set()
        for used in chains:
            for triad in triads:
                overlap = used.intersection(triad)
                if overlap and not set(triad).issubset(used):
                    extended.add(used.union(triad))
        chains = extended
        if not chains:
            break
    supports = sorted({tuple(sorted(used)) for used in chains}, key=lambda s: (len(s), s))
    return supports[:limit]


class Galerkin:
    def __init__(self, representatives: tuple[Mode, ...]):
        self.representatives = representatives
        self.modes = symmetric_support(list(representatives))
        self.index = {k: i for i, k in enumerate(self.modes)}
        self.terms: list[list[tuple[int, int, float]]] = []
        for k in self.modes:
            row = []
            for p in self.modes:
                q = (k[0] - p[0], k[1] - p[1])
                if q in self.index:
                    c = coefficient(p, q)
                    if c:
                        row.append((self.index[p], self.index[q], float(c)))
            self.terms.append(row)
        self.velocity_grid: dict[int, list[list[tuple[complex, complex]]]] = {}

    def rhs(self, state: list[complex]) -> list[complex]:
        return [sum(c * state[ip] * state[iq] for ip, iq, c in row) for row in self.terms]

    def rk4(self, state: list[complex], dt: float) -> list[complex]:
        k1 = self.rhs(state)
        k2 = self.rhs([z + dt * w / 2 for z, w in zip(state, k1)])
        k3 = self.rhs([z + dt * w / 2 for z, w in zip(state, k2)])
        k4 = self.rhs([z + dt * w for z, w in zip(state, k3)])
        return [z + dt * (a + 2 * b + 2 * c + d) / 6
                for z, a, b, c, d in zip(state, k1, k2, k3, k4)]

    def invariants(self, state: list[complex]) -> tuple[float, float]:
        enstrophy = sum(abs(z) ** 2 for z in state) / 2
        energy = sum(abs(z) ** 2 / norm2(k) for k, z in zip(self.modes, state)) / 2
        return energy, enstrophy

    def low_energy(self, state: list[complex], cutoff2: int = 2) -> float:
        return sum(abs(z) ** 2 / norm2(k) for k, z in zip(self.modes, state)
                   if norm2(k) <= cutoff2) / 2

    def l3(self, state: list[complex], grid: int = 24) -> float:
        if grid not in self.velocity_grid:
            points = []
            for ix in range(grid):
                x = 2 * math.pi * ix / grid
                for iy in range(grid):
                    y = 2 * math.pi * iy / grid
                    row = []
                    for k in self.modes:
                        phase = cmath.exp(1j * (k[0] * x + k[1] * y))
                        row.append((1j * k[1] * phase / norm2(k),
                                    -1j * k[0] * phase / norm2(k)))
                    points.append(row)
            self.velocity_grid[grid] = points
        total = 0.0
        for row in self.velocity_grid[grid]:
            ux = sum(omega * factors[0] for omega, factors in zip(state, row)).real
            uy = sum(omega * factors[1] for omega, factors in zip(state, row)).real
            total += (ux * ux + uy * uy) ** 1.5
        return (total / (grid * grid)) ** (1 / 3)

    def state_from_representatives(self, values: list[tuple[int, int]]) -> list[complex]:
        data: dict[Mode, complex] = {}
        for k, (a, b) in zip(self.representatives, values):
            data[k] = complex(a, b)
            data[neg(k)] = complex(a, -b)
        return [data[k] for k in self.modes]


def exact_invariant_check(model: Galerkin) -> dict[str, object]:
    """Check both quadratic invariant derivatives coefficient by coefficient."""
    failures = []
    for k in model.modes:
        for p in model.modes:
            q = neg(add(k, p))
            if q not in model.index:
                continue
            cyclic = coefficient(p, q) + coefficient(q, k) + coefficient(k, p)
            weighted = (coefficient(p, q) / norm2(k) + coefficient(q, k) / norm2(p)
                        + coefficient(k, p) / norm2(q))
            if cyclic or weighted:
                failures.append([k, p, q, str(cyclic), str(weighted)])
    return {"passed": not failures, "failures": failures}


def exact_ode(model: Galerkin) -> dict[str, list[dict[str, object]]]:
    equations = {}
    for k, row in zip(model.modes, model.terms):
        combined: dict[tuple[Mode, Mode], Fraction] = {}
        for ip, iq, _ in row:
            p, q = model.modes[ip], model.modes[iq]
            pair = tuple(sorted((p, q)))
            combined[pair] = combined.get(pair, Fraction(0)) + coefficient(p, q)
        equations[f"{k[0]},{k[1]}"] = [
            {"p": list(pair[0]), "q": list(pair[1]), "coefficient": str(c)}
            for pair, c in sorted(combined.items()) if c
        ]
    return equations


def exact_leakage(model: Galerkin, values: list[tuple[int, int]]) -> dict[Mode, tuple[Fraction, Fraction]]:
    data: dict[Mode, tuple[Fraction, Fraction]] = {}
    for k, (a, b) in zip(model.representatives, values):
        data[k] = (Fraction(a), Fraction(b))
        data[neg(k)] = (Fraction(a), Fraction(-b))

    def mul(z: tuple[Fraction, Fraction], w: tuple[Fraction, Fraction]):
        return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])

    exterior: dict[Mode, tuple[Fraction, Fraction]] = {}
    for p in model.modes:
        for q in model.modes:
            k = add(p, q)
            if k == (0, 0) or k in model.index:
                continue
            c = coefficient(p, q)
            if not c:
                continue
            z = mul(data[p], data[q])
            old = exterior.get(k, (Fraction(0), Fraction(0)))
            exterior[k] = (old[0] + c * z[0], old[1] + c * z[1])
    return {k: z for k, z in exterior.items() if z != (0, 0)}


def screen(seed: int, bound: int, length: int, support_limit: int, starts: int,
           steps: int, dt: float, grid: int, sample_every: int) -> dict[str, object]:
    rng = random.Random(seed)
    supports = enumerate_chains(bound, length, support_limit)
    best: dict[str, object] | None = None
    for reps in supports:
        model = Galerkin(reps)
        if not any(norm2(k) <= 2 for k in reps):
            continue
        for _ in range(starts):
            values = [(rng.randint(-2, 2), rng.randint(-2, 2)) for _ in reps]
            if all(v == (0, 0) for v in values):
                continue
            state = model.state_from_representatives(values)
            e0, z0 = model.invariants(state)
            initial_l3 = model.l3(state, grid)
            observations = [(0, initial_l3, model.low_energy(state), [z for z in state])]
            stable = True
            for step in range(1, steps + 1):
                state = model.rk4(state, dt)
                if not all(math.isfinite(z.real) and math.isfinite(z.imag) for z in state):
                    stable = False
                    break
                if step % sample_every == 0:
                    observations.append((step, model.l3(state, grid), model.low_energy(state), [z for z in state]))
            if not stable:
                continue
            e1, z1 = model.invariants(state)
            if abs(e1 / e0 - 1) > 2e-5 or abs(z1 / z0 - 1) > 2e-5:
                continue
            lo = min(observations, key=lambda row: row[1])
            hi = max(observations, key=lambda row: row[1])
            ratio = hi[1] / lo[1]
            low_values = [row[2] for row in observations]
            low_ratio = max(low_values) / max(min(low_values), 1e-30)
            low_fraction_gain = (max(low_values) - min(low_values)) / e0
            score = ratio * (1 + 0.1 * max(low_fraction_gain, 0))
            if best is None or score > best["score"]:
                best = {
                    "score": score,
                    "l3_ratio": ratio,
                    "low_energy_ratio": low_ratio,
                    "low_energy_fraction_gain": low_fraction_gain,
                    "representatives": reps,
                    "initial_integer_coefficients": values,
                    "minimum_step": lo[0],
                    "maximum_step": hi[0],
                    "minimum_l3": lo[1],
                    "maximum_l3": hi[1],
                    "energy_relative_drift": e1 / e0 - 1,
                    "enstrophy_relative_drift": z1 / z0 - 1,
                    "state_at_minimum": [[z.real, z.imag] for z in lo[3]],
                    "state_at_maximum": [[z.real, z.imag] for z in hi[3]],
                }
    if best is None:
        raise RuntimeError("screen produced no stable trajectory")
    model = Galerkin(tuple(tuple(k) for k in best["representatives"]))
    leakage = exact_leakage(model, [tuple(v) for v in best["initial_integer_coefficients"]])
    best["exact_initial_leakage"] = {
        f"{k[0]},{k[1]}": [str(z[0]), str(z[1])] for k, z in sorted(leakage.items())
    }
    best["exact_invariant_check"] = exact_invariant_check(model)
    best["exact_galerkin_ode"] = exact_ode(model)
    return {
        "conventions": {
            "torus": "normalized Haar measure on (R/2piZ)^2",
            "vorticity_ode": "dot omega_k = sum_(p+q=k) cross(p,q)/2*(1/|q|^2-1/|p|^2)*omega_p*omega_q",
            "reality": "omega_-k = conjugate(omega_k)",
        },
        "screen": {"seed": seed, "bound": bound, "chain_length": length,
                   "support_limit": support_limit, "starts_per_support": starts,
                   "steps": steps, "dt": dt, "l3_grid": grid,
                   "sample_every": sample_every,
                   "candidate_supports": len(supports)},
        "best": best,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=224)
    parser.add_argument("--bound", type=int, default=3)
    parser.add_argument("--length", type=int, default=3)
    parser.add_argument("--support-limit", type=int, default=120)
    parser.add_argument("--starts", type=int, default=12)
    parser.add_argument("--steps", type=int, default=800)
    parser.add_argument("--dt", type=float, default=0.0025)
    parser.add_argument("--grid", type=int, default=16)
    parser.add_argument("--sample-every", type=int, default=20)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = screen(args.seed, args.bound, args.length, args.support_limit,
                    args.starts, args.steps, args.dt, args.grid, args.sample_every)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(text + "\n", encoding="ascii")
    print(text)


if __name__ == "__main__":
    main()
