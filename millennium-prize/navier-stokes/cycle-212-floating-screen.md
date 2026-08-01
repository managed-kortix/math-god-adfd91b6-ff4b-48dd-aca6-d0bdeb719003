# Cycle 212: floating candidate screen

## Scope

This artifact is **numerics screening only**. It is not a directed interval
PDE enclosure, a finite-family exclusion, a factor-two falsifier, a Navier--
Stokes regularity result, or a Millennium result.

The implemented symmetry quotient uses only transformations that preserve the
frozen coefficient cube: translations by multiples of `pi/2`, central
inversion, and coordinate interchange. Continuous translations, arbitrary
rotations, and amplitude rescalings are not quotient operations on this finite
campaign.

`cycle212_screen.cpp` enumerates the frozen ten integer coefficients, removes
nonprimitive scalar duplicates, and canonicalizes the finite symmetries coming
from quarter-period translations, central inversion, and coordinate interchange.
It removes data with identically zero vorticity interaction. An exhaustive
quadratic-activity proxy retains a configurable shortlist; a floating initial
`L^3` derivative then chooses trajectories. Thus the coefficient enumeration
is exhaustive, but the expensive PDE trajectory stage is a candidate screen,
not an exhaustive finite-family exclusion.

The trajectory stage solves

```text
omega_t + u dot grad(omega) = mu Delta omega,
u = (-partial_y psi, partial_x psi),  Delta psi = omega
```

by a dealiased Fourier pseudospectral method with integrating-factor AB2 time
stepping. It samples the full velocity `L^3` norm on the declared `j/16` grid.
The best coarse runs are repeated at higher spatial and temporal resolution.
Agreement between reruns is only a floating convergence check and must not be
reported as an interval bound.

Audit checks confirm the declared normalization: the stored Fourier arrays use
the FFT's unnormalized forward convention, so initial coefficients carry the
factor `N^2`, inverse FFT evaluation recovers the physical velocity, and the
grid average computes normalized-Haar `L^3`. The nonlinear sign implements
`omega_t=-u dot grad(omega)+mu Delta omega`, and the first integrating-factor
Euler step followed by integrating-factor AB2 has the stated heat factors.

## Reproduction

```bash
g++ -O3 -march=native -std=c++20 cycle212_screen.cpp -o cycle212_screen
./cycle212_screen --proxy-keep 1024 --candidate-keep 12 \
  --coarse-steps 512 --fine-steps 1024 --fine-keep 3 \
  --output cycle212-screen.json
python -m unittest -q test_cycle212_screen.py
```

The recorded Cycle 212 run exhaustively reduced `9,765,624` nonzero raw rows to
`152,621` canonical primitive rows, of which `152,586` have nonzero nonlinear
vorticity interaction. It retained `1,024` proxy rows and integrated 12 rows at
all seven viscosities. The largest converged high-resolution sampled ratio was
`1.00201` at `mu=1/64`, `T=3/16`, for

```text
(a10,b10,a01,b01,a11,b11,a21,b21,a12,b12)
  = (-2,-2,-1,-1,0,-1,1,-1,-1,1).
```

No retained trajectory produced a floating candidate above two. This does not
exclude a crossing among the canonical rows discarded by the proxy/derivative
shortlists, and therefore does not exclude the frozen finite family.

Any observed ratio above two is only an interval-validation candidate. Closing
the Cycle 210 gate still requires unresolved-tail, time-discretization, and
spatial-cubature bounds for the full PDE as specified there.
