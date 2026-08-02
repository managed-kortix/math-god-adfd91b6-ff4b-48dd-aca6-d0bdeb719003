# Cycle 265: 3D strain-vorticity alignment numerical scout

## Verdict

The frozen four-member Taylor--Green/ABC family produces no directed
velocity-`L3` endpoint growth at `T=2`. All eight trajectories pass the frozen
local numerical gates. At the fine `K=7` level the directed ratios are

\[
 0.978105159853,\quad 0.985349509125,\quad
 0.973269466483,\quad 0.973269466483.
\]

The maximum is `0.985349509125428`, strictly below the predeclared `1.2` stop
threshold. Therefore the stop fires: do not broaden, tune, phase-search, or
extend this family.

This is numerical finite-dimensional evidence only. It is not a full Euler
enclosure, a Navier--Stokes result, or a Millennium result.

## Frozen computation

`C265-3DA1` contains exactly four common-energy-normalized fields: Taylor--Green
plus or minus amplitude `0.2` times either symmetric ABC `(1,1,1)` or phased
anisotropic ABC `(1,4/5,6/5; pi/2,0,pi/3)`. Every field is mean zero,
divergence free, depends on all three coordinates, and has three nonzero
velocity components. No random starts or adaptive family changes were used.

The symmetric cubic Fourier Galerkin system was evolved in rotational form by
implicit midpoint with exact retained convolution from a `4K+1` padded grid,
step `1/128`, and final time `2`. The two frozen levels were `K=5` and `K=7`.
Midpoint is invariant-aware: at zero solve residual it preserves Galerkin
kinetic energy and helicity. Three-dimensional enstrophy was not treated as an
invariant.

## Diagnostics

The coarse/fine ratio differences by member are `0.000549065717`,
`0.002257908648`, `0.000743640864`, and `0.000743640864`. Fine-level endpoint
cubature differences between grids 48 and 64 are at most `2.6629e-7`.

Across the fine runs, maximum relative energy drift is `5.055e-11`, maximum
energy-scaled helicity drift is `3.670e-11`, maximum divergence defect is
`1.94e-15`, and maximum reality defect is `3.44e-16`. The largest accepted
midpoint residual ratio is `9.963e-12` against the frozen `1e-11` gate.

The initial signed global stretching-alignment diagnostic is zero to cubature
roundoff for these symmetric mixtures. It becomes positive by `T=2`, with fine
endpoint values from `0.25093` to `0.27743`. Thus vortex stretching is active,
but it does not produce directed velocity-`L3` growth in this bounded family at
the frozen endpoint.

## Decision

Record:

`C265-3DA1 STOP: MAX GATE-PASSING K7 DIRECTED L3 ENDPOINT RATIO 0.985349509125428 < 1.2; NO BROAD TUNING; NUMERICAL ONLY.`

## Reproduction

```bash
uv run --with numpy python -m unittest -q test_cycle265_3d_alignment.py
uv run --with numpy python scout_cycle265_3d_alignment.py \
  --output cycle265-3d-alignment-screen.json
```

```text
cycle-265-3d-alignment-scout-architecture.md
  sha256 2cb96b2ae8b0bb929fd3abfbc97b876058b3f6f46320e072a3fc258ece1747e8
scout_cycle265_3d_alignment.py
  sha256 af3cd1abc499c8c5f70b9f1ed061ef55f1ad1c5ee05e68be405d6252dc0207aa
test_cycle265_3d_alignment.py
  sha256 81acc21f37b25a0986c65d17ccc5299a0fde16658b2fe5a40952200efe50175e
cycle265-3d-alignment-screen.json
  sha256 aaaeaae93a2ef4a375f91d8bfe9d9353efca7d73aded2c376466dfe06f9c24a4
```
