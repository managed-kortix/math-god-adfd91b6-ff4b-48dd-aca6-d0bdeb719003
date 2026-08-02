# Cycle 258: hostile audit of the integrated-growth screen

## Exact decision

Record the Cycle 258 status as

`SCREEN PASS; LEAD 43 PROVISIONAL; VALIDATION HOLD; ND251 NO CREDIT.`

The frozen numerical gate passes exactly as declared: all 45 members have an
`N=128` sampled bidirectional variation ratio strictly above `1.1`, so the
family is not retired by the Cycle 258 stop rule. Family index 43 is therefore
the deterministic numerical lead from this screen. It is not promoted to an
Euler enclosure, an `ND251` candidate packet, or any PDE statement. The data
do not yet support even a resolution-validated ordering of the local family.

## Hostile checks

### Dynamic aliasing

The evolution uses the square mask `|kx|,|ky| <= floor(N/3)` after every
nonlinear evaluation. For the two runs, `3K=63<N=64` and `3K=126<N=128`.
Thus the retained quadratic convolution is the standard square two-thirds
dealiased Galerkin convolution; there is no evident wraparound alias into the
retained square in exact arithmetic. This addresses dynamic quadratic
aliasing only. The code does not independently replay the right-hand side by
zero-padded convolution, and the normalized-grid cubature of the nonpolynomial
quantity `|u|^3` has no spatial quadrature error estimate. Aliasing is therefore
not the leading observed defect, but it has not been independently broken.

### Time step and checkpointing

The resolution comparison changes `N`, cutoff, and step simultaneously:
`(N,K,dt)=(64,21,1/128)` versus `(128,42,1/256)`. It consequently does not
separate temporal error from Galerkin-resolution error. No fixed-`N` step
halving was run. Checkpoints are fixed at `1/64`, so a narrow extremum between
checkpoints could also perturb the reported max/min ratio. The integrated-log
identity discrepancy is small (`4.11e-5` and `3.29e-5`) but tests only the
diagnostic/integrator consistency along the computed finite system; it is not
a time-step convergence certificate.

### Family perturbations and ranking

The 45-member construction is deterministic, includes every frozen member at
both resolutions, and numerically restores `E=1` and the center's `Z/E`. The
`1.1` gate is robust in the weak sense that all 45 members pass at both
resolutions. It is nonselective: it gives no robust winner.

The `N=64` winner is index 30, while index 43 ranks 28th. At `N=128`, index 43
ranks first and index 30 ranks 17th. Within the `rho=20` family, the `N=128`
lead exceeds the unperturbed center 36 by only `0.00208248`, whereas the lead's
own `N=64`/`N=128` change is `0.04044010`. The claimed perturbative advantage
is therefore below the visible discretization change and receives no credit.

### Max/min score versus `ND251`

For index 43 at `N=128`, the sampled maximum is `1.5125494529` at
`t=0.265625`, the sampled minimum is `1.2249677747` at `t=2.5`, and their ratio
is `1.2347667295`. This is an orbit-excursion statistic. Relative to the frozen
initial state, the maximum is only a factor `1.04779957`; the rest of the
max/min score comes from the later decline. Time reversal and rebasing could
orient a genuinely enclosed orbit excursion, but this floating Galerkin run
does not provide such an enclosure. In any orientation, `1.23477` is far below
the required directed ratio `2+eta` in `ND251`.

### Conservation drift

Across the family, maximum relative energy drift falls from `5.64e-6` to
`1.26e-6`. Maximum relative enstrophy drift changes only from `1.10e-4` to
`1.03e-4`. For index 43 it is `1.06e-4` at `N=64` and `8.19e-5` at `N=128`.
These values are acceptable as scout diagnostics but are not outward error
bounds. The weak enstrophy improvement over a simultaneous resolution and
step refinement is a reason to hold validation.

### Resolution divergence

The largest absolute per-member ratio change is `0.04587356` (index 44). For
index 43 it is `0.04044010`. More seriously, index 43's sampled minimum moves
from `t=-1.65625` at `N=64` to the opposite endpoint `t=2.5` at `N=128`, while
its positive-time maximum remains near `t=0.265625`. The ratio discrepancy is
therefore driven mainly by unresolved long-time denominator behavior, not by
the short positive-time peak. This blocks validation of the winner and of its
ranking.

## Next finite test: C258-V1

Freeze one validation matrix before computation. Use family indices
`{30,36,43,44}`: the coarse winner, the fine winner's unperturbed center, the
fine winner, and the member with largest cross-resolution discrepancy.

1. Run each member at `N in {128,256}` with square cutoffs `42` and `85`.
2. At each `N`, run both `dt=1/(2N)` and `dt=1/(4N)` through both directions to
   `T=2.5`; save diagnostics every `1/256` and include both endpoints.
3. Re-evaluate `L3` from every saved Fourier state on independent grids `2N`
   and `4N`. Compare those cubatures instead of using the evolution grid alone.
4. At `t in {0, +/-0.265625, +/-1.65625, +/-2.5}`, replay the retained
   nonlinear right-hand side by an independent zero-padded convolution and
   compare it with the native two-thirds implementation.
5. Report directed ratios from the frozen initial time separately in each time
   direction, as well as the bidirectional max/min excursion. Never substitute
   the latter for the former.

The finite validation gate passes only if, for one member, all of the following
hold:

- the `N=256` step-halving change in the max/min ratio is at most `0.002`;
- the fine-step `N=128`/`N=256` ratio change is at most `0.005`;
- the `2N`/`4N` diagnostic-cubature ratio change is at most `0.001`;
- the independent retained-RHS relative discrepancy is at most `1e-11`;
- relative endpoint energy and enstrophy drifts are at most `1e-6` and `2e-5`;
- the times of the selected minimum and maximum agree within `1/64` between
  the two fine-step resolutions, unless the reported values differ by at most
  `0.001` over the competing checkpoint plateau.

If no member passes every gate, Cycle 258 remains a screen pass but the lead is
not validated; do not expand the family until the failed temporal, cubature,
alias-replay, conservation, or resolution breaker is identified. If a member
passes, promote it only to a numerical trajectory lead for a separately frozen
finite search toward a larger directed ratio. C258-V1 cannot produce a PDE or
`ND251` claim regardless of outcome.
