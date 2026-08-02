# Cycle 258: integrated logarithmic L3 trajectory scout

## Verdict

The architecture in `cycle-258-integrated-l3-architecture.md` was written and
frozen before computation. All 45 deterministic perturbations of the five
Cycle 257 finite-Fourier candidates were then integrated in both time
directions at `N=64` and `N=128`.

The prescribed stop condition does not fire: all 45 members have an `N=128`
bidirectional sampled variation ratio strictly greater than `1.1`. The largest
ratio is `1.2347667295419633` for family index 43, the `rho=20` center perturbed
by `+0.025` in deterministic tangent direction 1. Its sampled minimum is
`1.2249677746507477` at `t=2.5`, and its sampled maximum is
`1.5125494528998005` at `t=0.265625`. The same member has ratio
`1.1943266343927748` at `N=64`.

This is numerical candidate selection only. It is not a full-Euler enclosure,
an `ND251` factor-two crossing, a Navier--Stokes result, or a Millennium result.

## Frozen family and objective

The five Cycle 257 candidate coefficient vectors are the centers. At each
center, two formula-defined coefficient directions are projected onto the
common energy/enstrophy tangent space. Perturbation radii `0.025` and `0.075`
and both signs give eight neighbors per center; the Cycle 257 spectral-tilt
retraction restores `E=1` and the center's floating `Z/E=rho`. Including the
centers gives 45 members. No random starts, adaptive additions, or derivative
shortlisting occur.

Each member is evolved by square-two-thirds Fourier pseudospectral Euler and
classical RK4 on `[-2.5,2.5]`, with `dt=1/128` at `N=64`, `dt=1/256` at
`N=128`, and diagnostics every `1/64`. The optimized quantity is accumulated
logarithmic velocity-`L3` growth,

\[
 I(t)=\int_0^t {d\over ds}\log\|u(s)\|_3\,ds,
\]

using composite trapezoidal quadrature at diagnostic checkpoints. Direct
`log(||u(t)||_3/||u(0)||_3)` is retained as an identity breaker. The promotion
statistic is the largest sampled `L3` divided by the smallest sampled `L3`
over the complete bidirectional trajectory.

## Results

At `N=64`, all 45 ratios exceed `1.1`; the range is
`[1.1190226338491913,1.2237733052113158]`. The winner is family index 30, a
`rho=16`, `+0.025`, direction-0 perturbation. Its maximum occurs at
`t=0.28125` and its minimum at `t=2.5`.

At `N=128`, all 45 ratios again exceed `1.1`; the range is
`[1.1189680701843887,1.2347667295419633]`. The winner changes to family index
43. The `N=64` winner has ratio `1.2070654709549251` at `N=128`.

The largest absolute per-member difference between the two resolution ratios
is `0.04587355572051899`, attained by family index 44. This sizeable discrepancy
is a warning against treating the finite-resolution ratios as certified. The
winner itself rises from `1.1943266343927748` to `1.2347667295419633`.

For the `N=128` winner, the best positive-time integrated logarithmic growth is
`0.04667580793398817` at `t=0.265625`; the direct logarithmic ratio is
`0.04669231467381471`. The ratio `1.2347667295419633` is larger because its
denominator is the later sampled minimum, rather than the initial norm.
Consequently this computation identifies a bidirectional orbit excursion, not
a `1.2347` directed gain from the frozen initial instant.

Across the complete runs, the maximum integrated-identity discrepancies are
`4.108726879731295e-05` at `N=64` and `3.2851291873470245e-05` at `N=128`.
Maximum relative energy drifts are `5.642958342377824e-06` and
`1.2617323021935078e-06`; maximum relative enstrophy drifts are
`1.0999643183673413e-04` and `1.027133299327243e-04`, respectively.

## Decision

Record:

`CYCLE258 INTEGRATED-L3 FAMILY PASSES 1.1 NUMERICAL GATE: 45/45 AT N=128; MAX 1.2347667295419633; NUMERICAL ONLY.`

Do not stop under the declared no-ratio-above-`1.1` rule. Promote family index
43 only as the deterministic numerical lead. The next stage, if pursued, must
be separately frozen and should first resolve the visible `N=64`/`N=128`
difference and the long-time enstrophy drift before any exact trajectory
enclosure. The present family remains far below factor two.

## Reproduction

```bash
uv run --with numpy python -m unittest -q test_cycle258_integrated_l3.py
uv run --with numpy python scout_cycle258_integrated_l3.py \
  --source cycle257-initial-l3-candidates.json --n 64 \
  --output cycle258-integrated-l3-N64.json
uv run --with numpy python scout_cycle258_integrated_l3.py \
  --source cycle257-initial-l3-candidates.json --n 128 \
  --output cycle258-integrated-l3-N128.json
uv run --with numpy python compare_cycle258_integrated_l3.py \
  --n64 cycle258-integrated-l3-N64.json \
  --n128 cycle258-integrated-l3-N128.json \
  --output cycle258-integrated-l3-comparison.json
```

```text
scout_cycle258_integrated_l3.py
  sha256 a8af3811e73523cfefc02a71fb43287e0f639656c0693c546ff4506521dd4aa2
compare_cycle258_integrated_l3.py
  sha256 5b7bce01a95f0d4bc68c45f4fb27e5662d36f08a213b01d0ca92a8a735d5f723
cycle258-integrated-l3-N64.json
  sha256 e3e56c372f61242dad6b177a5c6d4bf35965b23da054c4143e8297586844ae32
cycle258-integrated-l3-N128.json
  sha256 774daaf6071b7676540c0752f6b5f8dc14253755bf5b90ce4e40ff804e0d2ab4
cycle258-integrated-l3-comparison.json
  sha256 3dc8e51453b2423d02eb94db884c254721d965806450c4c85adef608c9a20a3a
```
