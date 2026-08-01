# Cycle 214: automatic-gradient Euler endpoint screen

## Scope

This is a floating numerical candidate screen, not an interval certificate or a
PDE theorem. It searches finite dealiased Fourier discretizations of 2D Euler
for endpoint amplification of the normalized-Haar velocity `L^3` norm. A
crossing must still be rerun with convergence checks and then enclosed with the
Cycle 211 full-PDE validation pipeline.

`cycle214_gradient.cpp` parameterizes a real streamfunction by every independent
Fourier mode in the square `|kx|,|ky| <= max_wave`, removes the zero mode, and
normalizes the real coefficient vector to eliminate amplitude scaling. Terminal
time `T` is optimized jointly with the coefficients.

The solver uses the standard `2/3`-dealiased vorticity equation

```text
omega_t = -u dot grad(omega),
u = (-partial_y psi, partial_x psi),
Delta psi = omega.
```

Time integration is explicit midpoint. Gradients are automatic forward tangent
derivatives of the complete discrete trajectory, including the endpoint `L^3`
objective and the time step `h=T/steps`. This is a discrete automatic gradient,
not a continuous-adjoint identity. Forward tangent mode is appropriate for the
default 24 coefficient variables; larger Fourier boxes should replace it with a
reverse discrete adjoint to avoid one tangent solve per variable.

## Screening funnel

Each random unit-norm seed is optimized at `N=32`. Candidates with ratio greater
than `1.2` are promoted to `N=64`, where optimization continues with twice as
many time steps and half learning rates. The JSON output records every seed,
both ratios, optimized `T`, coefficients, promotion count, and crossings above
`2`. Ratios are endpoint ratios, not maxima sampled along a trajectory.

## Reproduction

```bash
g++ -O3 -march=native -std=c++20 cycle214_gradient.cpp -o cycle214_gradient
./cycle214_gradient --seeds 64 --max-wave 2 --n32 32 --n64 64 \
  --steps 128 --iterations32 30 --iterations64 20 \
  --promote 1.2 --target 2 --output cycle214-gradient-screen.json
python -m unittest -q test_cycle214_gradient.py
```

The random campaign can be partitioned reproducibly with `--seed`. Increasing
`--max-wave` increases both the search dimension and tangent cost. Any apparent
high-variance crossing should be rerun with smaller time steps, larger `N`, and
multiple nearby initializations before interval validation.
