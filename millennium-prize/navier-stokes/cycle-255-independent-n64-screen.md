# Cycle 255 independent N=64 numerical screen

## Scope

`cycle255_independent_screen.cpp` is an independent candidate generator for the
Cycle 255 family. It uses an unnormalized forward FFT, normalized inverse FFT,
the square `2/3` mask, classical RK4, and normalized-Haar grid cubature for the
velocity `L^3` norm. It is floating Galerkin numerics only: it supplies no tail
enclosure, interval time integration, cubature enclosure, family exclusion, or
PDE claim.

The screen exactly applies the analytic feasibility formulas before ranking.
All `4,686` profile/tail variants are feasible at `T=1/16`. To keep this
independent run minimal, it ranks those variants by the absolute initial
logarithmic `L^3` derivative, retains 24, and integrates both time directions
through each member's largest feasible terminal time. This strategic subset is
not the deterministic exhaustive trajectory funnel proposed in Cycle 255.

## Recorded run

The production command was

```bash
g++ -O3 -march=native -std=c++20 -Wall -Wextra -pedantic \
  cycle255_independent_screen.cpp -o cycle255_independent_screen
./cycle255_independent_screen --n 64 --steps-per-unit 2048 \
  --shortlist 24 --report 12 --output cycle255-independent-N64.json
```

The largest ratio was `1.0000954185401316`, at `T=1/16`, in the forward
direction for zero-based profile 16,

```text
a = (1,-2,-2,1,-1), sigma = 1/24, epsilon = 1/1024.
```

Its zero-based full-family index is 3232. The symmetry-related zero-based
profile 506, `(1,2,-2,-1,-1)`, gives `1.0000954185401307`. Changing only the
tail parameters changes the reported ratio in the thirteenth decimal place;
the first 12 reported rows all lie between `1.0000954185388318` and
`1.0000954185401316`. None approaches the Cycle 255 promotion threshold `3/2`.

## Controls and convergence caveats

The stationary shear `psi=cos(y)` has exact normalized-Haar norm
`(4/(3 pi))^(1/3)=0.7515011011912177`. The `N=64` grid gives
`0.7515013927428441`, relative cubature error about `3.88e-7`; its computed
Euler right side is exactly zero and its ratio remains one. The unequal
amplitude equal-eigenvalue packet `P1=cos(x)+2cos(y)` is also stationary; its
relative right-side norm is `1.75e-17`, and its ratio, energy, and enstrophy
remain constant to the printed precision.

Step doubling from `dt=1/1024` to `dt=1/2048` changes the top ratio by about
`2e-16`. The auxiliary `N=32`, `dt=1/2048` run gives
`1.0000952313556013`, an absolute spatial change of about `1.87e-7`. Although
small absolutely, that is roughly `0.2%` of the observed excess above one.
There is no `N=128` or `N=256` check, no proof that the derivative shortlist
contains the best finite-time member, and no rigorous control of the omitted
infinite tail. The result is therefore useful only for candidate ranking.

Run the smoke test with

```bash
python -m unittest -q test_cycle255_independent_screen.py
```
