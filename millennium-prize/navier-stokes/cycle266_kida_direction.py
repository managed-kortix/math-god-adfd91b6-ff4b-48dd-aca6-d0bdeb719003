#!/usr/bin/env python3
"""Deterministic initial-L3 direction calculations for the C266 candidate."""

import json

import numpy as np

from scout_cycle265_3d_alignment import Galerkin3D


# K has support 3, F(K) support 6, F(u_*) support 12, and
# DF(u_*)F(u_*) support 18.  This cutoff therefore retains the complete
# Fourier time jet used below rather than a Galerkin projection of it.
CUTOFF = 18
CANDIDATE_TANGENT_COEFFICIENT = -1.0 / 32.0


def kida_pelz_state(solver):
    n = solver.width
    axis = 2.0 * np.pi * np.arange(n) / n
    x, y, z = np.meshgrid(axis, axis, axis, indexing="ij")
    field = np.stack((
        np.sin(x) * (np.cos(3 * y) * np.cos(z) - np.cos(y) * np.cos(3 * z)),
        np.sin(y) * (np.cos(3 * z) * np.cos(x) - np.cos(z) * np.cos(3 * x)),
        np.sin(z) * (np.cos(3 * x) * np.cos(y) - np.cos(x) * np.cos(3 * y)),
    ))
    return np.fft.fftshift(np.fft.fftn(field, axes=(1, 2, 3)), axes=(1, 2, 3)) / n**3


def l3_cube(solver, state, grid):
    velocity = solver.physical(state, grid)
    return float(np.mean(np.sum(velocity * velocity, axis=0) ** 1.5))


def cube_first_variation(solver, state, direction, grid):
    velocity = solver.physical(state, grid)
    variation = solver.physical(direction, grid)
    speed = np.sqrt(np.sum(velocity * velocity, axis=0))
    return float(3.0 * np.mean(speed * np.sum(velocity * variation, axis=0)))


def rhs_linearization(solver, state, direction):
    # Polarization is exact in arithmetic because rhs is homogeneous quadratic.
    return solver.rhs(state + direction) - solver.rhs(state) - solver.rhs(direction)


def initial_l3_cube_derivative(solver, state, grid):
    return cube_first_variation(solver, state, solver.rhs(state), grid)


def initial_log_l3_derivatives(solver, state, grid):
    """Return the exact-in-time first two variations, evaluated by cubature."""
    velocity = solver.physical(state, grid)
    tangent = solver.rhs(state)
    acceleration = solver.physical(tangent, grid)
    second_tangent = rhs_linearization(solver, state, tangent)
    jerk = solver.physical(second_tangent, grid)

    speed2 = np.sum(velocity * velocity, axis=0)
    speed = np.sqrt(speed2)
    ua = np.sum(velocity * acceleration, axis=0)
    cube = float(np.mean(speed**3))
    cube_first = float(3.0 * np.mean(speed * ua))
    quotient = np.zeros_like(speed)
    np.divide(ua * ua, speed, out=quotient, where=speed > 0.0)
    cube_second = float(3.0 * np.mean(
        quotient
        + speed * np.sum(acceleration * acceleration, axis=0)
        + speed * np.sum(velocity * jerk, axis=0)
    ))
    log_first = cube_first / (3.0 * cube)
    log_second = cube_second / (3.0 * cube) - cube_first**2 / (3.0 * cube**2)
    return {
        "candidate_l3_cube": cube,
        "candidate_l3_cube_derivative": cube_first,
        "candidate_l3_cube_second_derivative": cube_second,
        "candidate_log_l3_derivative": log_first,
        "candidate_log_l3_second_derivative": log_second,
        "quadratic_turning_time": (
            -log_first / log_second if log_second < 0.0 else None
        ),
        "quadratic_peak_log_growth": (
            -0.5 * log_first**2 / log_second if log_second < 0.0 else None
        ),
    }


def fourier_sup_bound(solver, state, derivative_axis=None):
    weights = np.ones_like(solver.k2)
    if derivative_axis is not None:
        weights = np.abs(solver.k[derivative_axis])
    mode_lengths = np.sqrt(np.sum(np.abs(state) ** 2, axis=0))
    return float(np.sum(weights * mode_lengths))


def cubature_remainders(solver, state, grid):
    """Analytic periodic rectangle-rule errors from Fourier l1 sup norms."""
    tangent = solver.rhs(state)
    second_tangent = rhs_linearization(solver, state, tangent)
    u = fourier_sup_bound(solver, state)
    a = fourier_sup_bound(solver, tangent)
    j = fourier_sup_bound(solver, second_tangent)
    errors = {"cube": 0.0, "cube_first": 0.0, "cube_second": 0.0}
    for axis in range(3):
        ux = fourier_sup_bound(solver, state, axis)
        ax = fourier_sup_bound(solver, tangent, axis)
        jx = fourier_sup_bound(solver, second_tangent, axis)
        errors["cube"] += 3.0 * u**2 * ux
        errors["cube_first"] += 6.0 * u * ux * a + 3.0 * u**2 * ax
        # |D^3 |u|^3| <= 12 and |D^2 |u|^3| <= 6|u|.
        errors["cube_second"] += (
            12.0 * ux * a**2 + 12.0 * u * ax * a
            + 6.0 * u * ux * j + 3.0 * u**2 * jx
        )
    return {key: np.pi * value / grid for key, value in errors.items()}


def derivative_of_initial_derivative(solver, state, direction, grid):
    velocity = solver.physical(state, grid)
    variation = solver.physical(direction, grid)
    acceleration = solver.physical(solver.rhs(state), grid)
    acceleration_variation = solver.physical(
        rhs_linearization(solver, state, direction), grid
    )
    speed = np.sqrt(np.sum(velocity * velocity, axis=0))
    uv = np.sum(velocity * variation, axis=0)
    uf = np.sum(velocity * acceleration, axis=0)
    direct = speed * (
        np.sum(variation * acceleration, axis=0)
        + np.sum(velocity * acceleration_variation, axis=0)
    )
    quotient = np.zeros_like(speed)
    np.divide(uv * uf, speed, out=quotient, where=speed > 0.0)
    return float(3.0 * np.mean(direct + quotient))


def constraint_variations(solver, state, direction):
    curl_state = solver.curl(state)
    curl_direction = solver.curl(direction)
    return {
        "energy": float(np.real(np.vdot(state, direction))),
        "helicity": float(2.0 * np.real(np.vdot(curl_state, direction))),
        "enstrophy_like": float(np.real(np.vdot(curl_state, curl_direction))),
    }


def report():
    solver = Galerkin3D(CUTOFF)
    kida = kida_pelz_state(solver)
    euler_tangent = solver.rhs(kida)
    direction = -euler_tangent
    candidate = kida + CANDIDATE_TANGENT_COEFFICIENT * euler_tangent
    rows = []
    for grid in (64, 96, 128):
        row = {
            "grid": grid,
            "directional_derivative_at_kida_along_minus_F":
                derivative_of_initial_derivative(solver, kida, direction, grid),
        }
        row.update(initial_log_l3_derivatives(solver, candidate, grid))
        row["analytic_cubature_remainders"] = cubature_remainders(
            solver, candidate, grid
        )
        rows.append(row)
    return {
        "format": "C266-KP1-initial-direction",
        "status": "DETERMINISTIC_NUMERICAL_REPLAY",
        "pde_certificate": False,
        "cutoff": CUTOFF,
        "candidate": "K-(1/32)F(K)",
        "coefficient_a_in_cycle265_parameterization": -2,
        "coefficient_b_in_cycle265_parameterization": 0,
        "phase": [0, 0, 0],
        "kida_constraint_variations_along_minus_F":
            constraint_variations(solver, kida, direction),
        "grids": rows,
    }


if __name__ == "__main__":
    print(json.dumps(report(), indent=2, sort_keys=True))
