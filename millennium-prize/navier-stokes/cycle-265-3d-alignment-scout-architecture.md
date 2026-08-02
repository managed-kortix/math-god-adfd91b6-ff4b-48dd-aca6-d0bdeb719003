# Cycle 265: frozen 3D strain-vorticity alignment scout

## Pre-compute freeze

This document freezes `C265-3DA1` before trajectory computation. The experiment
is a finite-dimensional numerical Euler screen only. It is not a full-PDE
enclosure, a regularity result, or a Navier--Stokes/Millennium result.

The family has exactly four deterministic, mean-zero, divergence-free members
on the normalized `2 pi` torus. Let

\[
 T=(\sin x\cos y\cos z,-\cos x\sin y\cos z,0)
\]

be Taylor--Green and let

\[
 A_{a,b,c;p,q,r}=(a\sin(z+r)+c\cos(y+q),
 b\sin(x+p)+a\cos(z+r),c\sin(y+q)+b\cos(x+p))
\]

be an ABC field. Before one common energy normalization, freeze

1. `TG+0.20 ABC(1,1,1;0,0,0)`;
2. `TG-0.20 ABC(1,1,1;0,0,0)`;
3. `TG+0.20 ABC(1,4/5,6/5;pi/2,0,pi/3)`;
4. `TG-0.20 ABC(1,4/5,6/5;pi/2,0,pi/3)`.

Every member depends nontrivially on all three coordinates and has all three
velocity components nonzero. There are no random starts, coefficient searches,
shortlists, adaptive additions, or post-outcome phase/amplitude changes.

## Invariant-aware evolution

Use the symmetric cubic Fourier Galerkin space `|k_i|<=K` and the rotational
form

\[
 \dot u=P_K P_{div}(u\mathbin\times\operatorname{curl}u).
\]

Evaluate the retained quadratic convolution on a `4K+1` zero-padded grid.
Advance by implicit midpoint with `h=1/128` to `T=2`. At zero nonlinear solve
residual, midpoint preserves the Galerkin kinetic energy and helicity because
both are quadratic invariants. An unconverged step fails closed.

Run all four members at two frozen levels:

- `K5`: cutoff `K=5`, `L3` diagnostic grids 32 and 48;
- `K7`: cutoff `K=7`, `L3` diagnostic grids 48 and 64.

Record divergence, reality, midpoint residual, energy drift, helicity drift,
and independent check-grid endpoint cubature differences. Also record the initial and
endpoint normalized vortex-stretching alignment

\[
 {\langle\omega,S\omega\rangle\over
  \langle|\omega|^2\rangle^{1/2}
  \langle|S\omega|^2\rangle^{1/2}},
 \qquad S=(\nabla u+\nabla u^T)/2,
\]

as a diagnostic, not a promotion objective.

## Directed endpoint stop

The production score is only

\[
 R_T=\|u(T)\|_3/\|u(0)\|_3.
\]

The local gates are midpoint residual ratio at most `1e-11`, relative energy
drift at most `2e-9`, relative helicity drift at most `2e-9` when normalized by
the initial energy scale, divergence and reality defects at most `2e-12`, and
check-grid endpoint-ratio difference at most `2e-3`. Report the memberwise
`K5`/`K7` ratio differences.

Stop this route, with no broad tuning, if the largest gate-passing `K7`
directed endpoint ratio is less than `1.2`. A ratio at least `1.2` is only a
numerical lead and does not certify an Euler trajectory.
