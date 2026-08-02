# Cycle 264: directed-endpoint midpoint-Galerkin results

## Numerical outcome

`C264-DE1` promotes `0/3`. The genuinely new family was generated from three
fresh Cycle 257 constrained variational runs at `rho=6,10,14`; no Cycle 258
input or trajectory was loaded. All six resolution/member runs pass the frozen
local nonlinear-residual, invariant-tangency, defect-identity, endpoint-drift,
and doubled-cubature gates.

At `N128`, the directed endpoint ratios at `T=4` are respectively
`1.004458192981`, `0.868754094783`, and `0.856193686774`. None approaches the
strict `2.01` numerical promotion threshold. The largest sampled interior
increase is only `1.046663094142`, for `rho=14` at `t=0.390625`; it is reported
only as a diagnostic and receives no endpoint credit.

The absolute `N64`/`N128` endpoint-ratio differences are `0.009105618994`,
`0.017193682924`, and `0.006925672934`. Thus the middle member also misses the
frozen cross-resolution gate, although this is immaterial to the absent
directed amplification.

## Residual replay

Across `N128`, the maximum actual nonlinear residual ratio is
`4.993503745837e-12`, maximum normalized invariant tangency is
`2.844163140354e-16`, and maximum defect-identity relative closure is
`5.482779468522e-15`. Maximum endpoint relative energy and enstrophy drifts are
`4.629630012687e-14` and `3.233857626128e-12`. The largest doubled-grid endpoint
ratio discrepancy is `2.623629136167e-8`.

At `N64`, the corresponding maxima are `4.963545952839e-12`,
`3.233897097153e-16`, `5.971393363361e-15`, `1.058708676283e-12`,
`1.012345762774e-11`, and `9.973028969323e-7`. These are floating residual
diagnostics, not outward interval bounds.

Record:

`C264-DE1 NO PROMOTION: 0/3 DIRECTED ENDPOINT RATIOS EXCEED 2.01; ALL LOCAL INVARIANT-RESIDUAL GATES PASS; CYCLE258 INPUTS NOT USED; FINITE-DIMENSIONAL NUMERICAL ONLY.`

The bounded architecture stops here without family expansion, horizon tuning,
or threshold changes. It establishes neither convergence to full Euler nor an
`ND251`, Navier--Stokes, or Millennium result.
