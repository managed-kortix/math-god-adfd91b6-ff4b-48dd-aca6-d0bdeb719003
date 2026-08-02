# Cycle 264: frozen directed-endpoint midpoint-Galerkin screen

## Pre-compute freeze

This document freezes `C264-DE1` before candidate generation or trajectory
computation. The screen is numerical and finite dimensional only. It does not
enclose the Euler PDE, certify an `ND251` crossing, or claim a Navier--Stokes
result.

No Cycle 258 coefficient, family index, trajectory, or output file is an input.
The new centers are generated from scratch by the Cycle 257 constrained
initial-variation optimizer with Fourier box `|kx|,|ky|<=4`, cubature grid 36,
six deterministic starts, 80 projected-gradient iterations, and enstrophy
levels `rho in {6,10,14}`. Energy is one. The optimizer's deterministic winner
at each level is retained, giving exactly three family members. This uses the
Cycle 257 variational construction but none of the retired Cycle 258 inputs.
The generated center file and its SHA-256 digest are recorded in the report.

## Evolution and directed score

Each center is embedded without interpolation in the symmetric square
Galerkin space. Evolve only forward from the frozen initial state through
`T=4` with step `h=1/64`, using the `C263-MG1` implicit-midpoint equation

\[
 \omega_{n+1}-\omega_n-hF_K((\omega_n+\omega_{n+1})/2)=0.
\]

The nonlinear equation is iterated to an actual residual gate; an unconverged
step fails closed. The Galerkin right-hand side is evaluated on a `4K+1`
zero-padded grid and projected to the retained square, which is the exact
quadratic retained convolution up to floating roundoff.

Run the complete three-member family at both frozen levels:

- label `N64`: cutoff `K=15`, diagnostic grids 64 and 128;
- label `N128`: cutoff `K=31`, diagnostic grids 128 and 256.

Evaluate velocity `L3` at `t=0` and every midpoint step. The production score
is the directed endpoint ratio

\[
 R_T=\|u(T)\|_3/\|u(0)\|_3,
\]

not a bidirectional or interior max/min excursion. Interior sampled maxima are
reported only as diagnostics and cannot promote a member. Independent doubled
grid cubature is mandatory at both endpoints.

## Frozen residuals and decisions

At every step record the actual midpoint residual and both exact quadratic
defect identities from `C263-MG1`. Fail a run if any of the following occurs:

- nonlinear residual ratio exceeds `5e-12`;
- normalized energy or enstrophy tangency exceeds `2e-12`;
- either defect-identity relative closure exceeds `2e-12`;
- endpoint relative energy or enstrophy drift exceeds `2e-9`;
- endpoint `L3` ratio changes by more than `2e-3` on doubling the diagnostic
  grid.

Cross-resolution comparison reports the absolute `N64`/`N128` endpoint-ratio
difference for every member. A member is a numerical lead only if its `N128`
directed endpoint ratio is strictly greater than `2.01`, every residual gate
passes, and the cross-resolution difference is at most `0.01`. Otherwise the
bounded family has no promotion. There is no shortlist, adaptive horizon,
post-compute family expansion, threshold tuning, or Cycle 258 rerun.
