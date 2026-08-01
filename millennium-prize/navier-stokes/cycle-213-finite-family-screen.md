# Cycle 213: exhaustive floating finite-family screen

## Scope

This is a floating numerical screen, not an interval certificate or a PDE
theorem. It exhausts the frozen finite coefficient family at reduced spectral
resolution, then reruns retained rows at higher resolution. The phrase
"floating maximum" below refers to this declared pipeline only.

`cycle213_screen.cpp` reuses the Cycle 212 symmetry reduction and integrates all
`152,586` nonlinear canonical rows, rather than applying the old activity and
initial-derivative shortlists first. Each row is integrated at all seven frozen
viscosities on an `N=8` dealiased grid with 32 steps per unit through `T=4`.
The best 1,024 reduced rows are retained; the best 32 are integrated at `N=64`,
512 steps per unit, and the best eight trajectory-viscosity pairs are rerun at
`N=128`, 1,024 steps per unit. Maxima include the initial ratio one and are
sampled on the `j/16` time grid.

## Upper proxy

For correlation diagnostics, the program also computes a cheap first-order
Fourier upper proxy. The initial nonlinear and viscous time-derivative
coefficients are formed directly on their exact finite convolution support.
Triangle and Minkowski inequalities bound the `L^3` norm of the linear
predictor `u(0)+t u_t(0)` by the Fourier coefficient `l^1` norm. The resulting
ratio proxy has Pearson correlation `0.238089` with the reduced floating maxima
over the full family. It is an upper proxy for that first-order predictor, not
an upper bound on the nonlinear PDE trajectory, and it is not used to discard
rows before reduced integration.

## Recorded result

The exhaustive reduced run found maximum `1.0464625141939732` for

```text
(a10,b10,a01,b01,a11,b11,a21,b21,a12,b12)
  = (-2,-2,-1,0,1,1,0,0,2,2)
```

at `mu=1/64`, sampled time `9/16`. After the declared coarse and fine reruns,
the actual floating maximum of the pipeline is `1.0132639341307961`, attained
at `mu=1/64`, sampled time `1`, for

```text
(a10,b10,a01,b01,a11,b11,a21,b21,a12,b12)
  = (-2,-2,0,0,0,0,0,0,-2,1).
```

No row in this floating finite-family screen produced a retained candidate
above two. This is not an interval claim: there are no directed-rounding,
spatial-tail, time-discretization, or cubature error bounds.

## Reproduction

```bash
g++ -O3 -march=native -std=c++20 -pthread cycle213_screen.cpp -o cycle213_screen
./cycle213_screen --threads 2 --reduced-n 8 --reduced-steps 32 \
  --reduced-time 4 --reduced-keep 1024 --candidate-keep 32 \
  --coarse-n 64 --coarse-steps 512 --fine-n 128 --fine-steps 1024 \
  --fine-keep 8 --final-time 2 --output cycle213-screen.json
python -m unittest -q test_cycle212_screen.py test_cycle213_screen.py
```
