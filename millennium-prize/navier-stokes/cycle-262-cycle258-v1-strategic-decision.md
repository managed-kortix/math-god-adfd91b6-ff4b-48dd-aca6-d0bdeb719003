# Cycle 262: strategic decision after `C258-V1`

## Evidence boundary

The frozen `C258-V1` matrix promotes no member. All four members pass the
step-halving, fine-resolution, independent cubature, alias-replay, and (except
for index 30) extrema gates, but all four fail the declared conservation gate.
The maximum relative energy drifts are between `7.669640217367046e-7` and
`1.0468543343300496e-6`; the maximum relative enstrophy drifts are between
`6.367448086663785e-5` and `1.4403801072215838e-4`, above the frozen `2e-5`
limit.

This is not evidence that the trajectory signal is a resolution, cubature, or
aliasing artifact. It is also not a reason to ignore the failed gate. In
particular, the current RK4 matrix already contains the relevant step
refinement: at `dt=1/(4N)` every endpoint enstrophy drift is below `4.7e-6`,
while every `dt=1/(2N)` run is above `6.2e-5`. A further RK4 rerun would merely
choose a more favorable step from the same non-invariant-preserving method
after observing the gate, even if the declared numerical thresholds remained
textually unchanged.

The converged signal is moreover too weak for continued production. At
`N=256`, `dt=1/(4N)`, the largest bidirectional ratio is
`1.2328250527754527` (index 43), but its largest directed increase from the
initial state is only `1.0477998704925884`. The bidirectional score still owes
most of its value to a later decline and remains far from the `ND251` target
`2+eta`.

## Exact decision

Record:

`CYCLE258 FAMILY RETIRED FROM PRODUCTION: C258-V1 HAS 0/4 PROMOTIONS; FROZEN CONSERVATION GATE FAILS; NO RERUN AND NO THRESHOLD TUNING; NUMERICAL ONLY.`

This is an operational retirement of the frozen 45-member Cycle 258 family and
its four-member validation branch, not a theorem excluding the underlying
Euler data or nearby smooth Euler orbits. Preserve the completed matrix as
negative validation evidence. Do not rerun Cycle 258 with smaller RK4 steps,
higher resolution, a post hoc conservation check restricted to fine-step
runs, changed drift definitions, relaxed gates, or locally enlarged and tuned
perturbations.

## Next architecture requirement

The next `ND251` production architecture must be genuinely new and must freeze,
before trajectory computation, a discrete evolution whose update preserves the
Galerkin energy and enstrophy invariants by construction (up to nonlinear-solve
and roundoff residuals), together with independently replayable residual bounds.
It must not use smaller-step RK4 as its conservation mechanism.

It must also optimize and promote on the directed endpoint quantity required by
`ND251`, not on bidirectional max/min excursion. Before compute, specify a
finite deterministic family, horizon, resolution/refinement matrix, independent
velocity-`L3` cubature and alias replay, invariant-residual gates, and a strict
directed promotion threshold tied to `2+eta`. Reuse of the Cycle 255 analytic
tail, full-PDE enclosure, cubature, and Cycle 256 transfer interfaces is
allowed; local reuse or tuning of the retired Cycle 258 family is not.

No Euler crossing, Navier--Stokes result, or Millennium result is claimed.
