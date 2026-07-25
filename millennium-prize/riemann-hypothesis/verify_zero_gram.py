#!/usr/bin/env python3
"""Symbolically verify the conjugate-pair restricted-energy floor."""

import sympy as s

beta, gamma, A = s.symbols("beta gamma A", real=True)
I = s.I
rho = beta + I * gamma
rhobar = beta - I * gamma

G = s.Matrix([
    [1 / (rho + rhobar - 1), 1 / (rho + rho - 1)],
    [1 / (rhobar + rhobar - 1), 1 / (rhobar + rho - 1)],
])
u = s.Matrix([1 / rho, 1 / rhobar])
v = s.Matrix([1 / (1 - rho), 1 / (1 - rhobar)])
H = s.simplify(G.inv())

alpha = s.simplify((s.conjugate(u).T * H * u)[0])
delta = s.simplify((s.conjugate(v).T * H * v)[0])
r = s.simplify(s.re((s.conjugate(v).T * H * u)[0]))
floor_value = s.factor(alpha - r**2 / delta)

d = 2 * beta - 1
claimed = (
    2 * d * (d**2 + 4 * gamma**2)
    / ((beta**2 + gamma**2)**2 * (d**2 + 4 * gamma**2 + 1))
)

assert s.simplify(floor_value - claimed) == 0
print("conjugate-pair floor:", s.factor(floor_value))
print("symbolic zero-Gram check passed")
