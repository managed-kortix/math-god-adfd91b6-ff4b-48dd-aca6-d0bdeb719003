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

Time integration is classical explicit RK4. Gradients are automatic forward tangent
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
`2`. The best coefficient vector is also reevaluated without gradients at both
spatial resolutions and at the base and doubled step counts. Ratios are endpoint
ratios, not maxima sampled along a trajectory.

## Reproduction

The frozen max-wave-four budget uses exactly 16 starts from PRNG seed `214` and
12 RK4-gradient iterations per start. Optimization is fixed at `N=16` with 64
steps; the best endpoint is then checked at `N=16,32` and 64,128 steps. No
fine-resolution optimization is included in this bounded scout:

```bash
./cycle214_gradient --seeds 16 --seed 214 --max-wave 4 \
  --n32 16 --n64 32 --steps 64 \
  --iterations32 12 --iterations64 0 --promote 99 --target 2 \
  --output cycle214-wave4-gradient-screen.json
```

The general build and test commands are:

```bash
g++ -O3 -march=native -std=c++20 cycle214_gradient.cpp -o cycle214_gradient
python -m unittest -q test_cycle214_gradient.py
```

The random campaign can be partitioned reproducibly with `--seed`. Increasing
`--max-wave` increases both the search dimension and tangent cost. Any apparent
high-variance crossing should be rerun with smaller time steps, larger `N`, and
multiple nearby initializations before interval validation.

## Frozen max-wave-four result

The 16-start budget completed without extension. Seed `0` was best at the search
resolution, with optimized `T=1.0547139450639225` and endpoint ratio
`1.1699662837490548`. Doubling the RK4 steps at fixed `N=16` gave
`1.1699682602545018`, a change of about `1.98e-6`. The spatial check did not
agree: at `N=32` the same coefficients and time gave `1.0137912554951243` with
64 steps and `1.0137985433626824` with 128 steps. Thus the time discretization
is stable at each tested spatial grid, but the coarse optimized value is not
spatially resolved. No ratio above two was observed, and no certificate or PDE
claim follows. Full coefficients and all 16 outcomes are stored in
`cycle214-wave4-gradient-screen.json`.
