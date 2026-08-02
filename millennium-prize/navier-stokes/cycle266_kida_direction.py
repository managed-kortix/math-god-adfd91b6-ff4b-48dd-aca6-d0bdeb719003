#!/usr/bin/env python3
"""Deterministic initial-L3 direction calculations for the C266 candidate."""

import json

import numpy as np

from scout_cycle265_3d_alignment import Galerkin3D


CUTOFF = 8
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
        cube = l3_cube(solver, candidate, grid)
        derivative = initial_l3_cube_derivative(solver, candidate, grid)
        rows.append({
            "grid": grid,
            "candidate_l3_cube": cube,
            "candidate_l3_cube_derivative": derivative,
            "candidate_log_l3_derivative": derivative / (3.0 * cube),
            "directional_derivative_at_kida_along_minus_F":
                derivative_of_initial_derivative(solver, kida, direction, grid),
        })
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
