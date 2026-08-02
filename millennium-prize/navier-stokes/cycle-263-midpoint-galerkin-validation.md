# Cycle 263: midpoint Galerkin validation

## Verdict

`C263-MG1` passes every frozen finite-dimensional validation gate. The exact
square Galerkin convolution is tangent to both quadratic invariant level sets,
and implicit midpoint therefore preserves Galerkin energy and enstrophy when
its nonlinear equation is solved exactly. In floating-point computation, the
measured defects agree with the recorded nonlinear residual terms up to the
replayed identity closure and roundoff.

This validation used only the synthetic states specified in the Cycle 263
architecture. It did not load or rerun any member, output, or candidate from
the retired Cycle 258 family.

## Results

Direct retained-mode convolution and independent `4K+1` padded replay agree to
relative discrepancies `1.10e-15` at `K=2` and `8.19e-16` at `K=3`, against
the frozen `2e-13` gate. The maximum normalized energy and enstrophy tangencies
are `3.36e-16` and `1.99e-16`, respectively.

For 32 steps at `K=3`, `h=1/64`, Newton required at most two iterations. Its
maximum residual/scale ratio is `2.02e-14`, below `5e-13`. Maximum one-step
relative defects are `4.88e-15` for energy and `7.58e-15` for enstrophy. The
corresponding maximum Cauchy--Schwarz residual bounds are `6.33e-15` and
`1.80e-14` in absolute invariant units. Both exact defect identities close
within `5.71e-17` on the frozen normalized scale.

Accumulation over the 32 accepted steps gives relative endpoint drifts
`1.36e-13` for energy and `2.16e-13` for enstrophy. These endpoint numbers are
reported as diagnostics, not used in place of the stepwise residual identities.
The 32 negative steps return to the initial state with relative error
`5.83e-16`, below the `2e-11` reversal gate.

Record:

`C263-MG1 PASS: IMPLICIT MIDPOINT ON EXACT GALERKIN CONVOLUTION PRESERVES BOTH QUADRATIC INVARIANTS UP TO REPLAYED NONLINEAR-SOLVE AND ROUNDOFF RESIDUALS; CYCLE258 NOT RERUN; FINITE-DIMENSIONAL NUMERICAL VALIDATION ONLY.`

## Evidence boundary

This establishes the required conservation mechanism for a finite-mode
integrator. It does not establish a full Euler enclosure, Galerkin convergence
with controlled tails, or directed velocity-`L3` amplification beyond
`2+eta`. Before production, freeze a genuinely new deterministic initial-data
family and the separate horizon, resolution/refinement, independent cubature,
alias replay, analytic-tail, and directed endpoint promotion gates.

## Reproduction

```bash
uv run --with numpy python verify_cycle263_midpoint_galerkin.py \
  --output cycle263-midpoint-galerkin-validation.json
uv run --with numpy python -m unittest -q test_cycle263_midpoint_galerkin.py
```
