#!/usr/bin/env python3
"""Replay the exact Cycle 224 algebra and refine its floating observation."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "cycle224-triad-chain-screen.json"
SCOUT = ROOT / "scout_2d_triad_chains.py"


def load_scout():
    spec = importlib.util.spec_from_file_location("triad_scout", SCOUT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    scout = load_scout()
    artifact = json.loads(DATA.read_text(encoding="ascii"))
    best = artifact["best"]
    reps = tuple(tuple(k) for k in best["representatives"])
    values = [tuple(v) for v in best["initial_integer_coefficients"]]
    model = scout.Galerkin(reps)

    for p in model.modes:
        for q in model.modes:
            ordered_pair = (-scout.Fraction(scout.cross(p, q), scout.norm2(p))
                            - scout.Fraction(scout.cross(q, p), scout.norm2(q))) / 2
            assert ordered_pair == scout.coefficient(p, q)

    assert scout.exact_invariant_check(model)["passed"]
    expected_ode = scout.exact_ode(model)
    assert expected_ode == best["exact_galerkin_ode"]
    leakage = scout.exact_leakage(model, values)
    encoded = {f"{k[0]},{k[1]}": [str(z[0]), str(z[1])]
               for k, z in sorted(leakage.items())}
    assert encoded == best["exact_initial_leakage"]
    assert leakage

    state = model.state_from_representatives(values)
    e0, z0 = model.invariants(state)
    observations = []
    dt = 0.0015
    for step in range(2001):
        if step % 10 == 0:
            observations.append((step, model.l3(state, 32), model.low_energy(state)))
        if step < 2000:
            state = model.rk4(state, dt)
    e1, z1 = model.invariants(state)
    lo = min(observations, key=lambda x: x[1])
    hi = max(observations, key=lambda x: x[1])
    ratio = hi[1] / lo[1]
    assert abs(e1 / e0 - 1) < 1e-9
    assert abs(z1 / z0 - 1) < 1e-9
    assert ratio > 1.07

    print("PASS exact Galerkin ODE and energy/enstrophy identities")
    print("PASS canonical ordered/symmetrized convolution coefficient cross-test")
    print(f"PASS exact full-Euler initial leakage: {len(leakage)} exterior modes")
    print(f"FLOAT refinement grid=32 dt={dt}: L3 oscillation ratio {ratio:.12f}")
    print(f"FLOAT extrema: step {lo[0]} -> {hi[0]}, L3 {lo[1]:.12f} -> {hi[1]:.12f}")
    print(f"FLOAT invariant drift: energy {e1 / e0 - 1:.3e}, enstrophy {z1 / z0 - 1:.3e}")


if __name__ == "__main__":
    main()
