# Cycle 273: ND270 P3 items 5--6 freeze

## Verdict: `ND270-ADMIT`, THEN PRE-TRAJECTORY REJECT

The corrected Cycle 272 audit supplies admission items 1--4 and excludes the
duplicate outcome. The separate manifest
`cycle273-nd270-p3-manifest.json` now freezes items 5--6 before any trajectory
is generated. Admission authorizes exactly this bounded computation; it is not
an Euler endpoint, Navier--Stokes, or Millennium claim.

The frozen manifest remains byte-for-byte the compute authorization, with
SHA-256 `2a0e301c5e41060d423cf82c8052a3949d96475e924b858ffa4da763abbe4cce`.
Its originally pinned admission certificate is recovered separately as
`cycle273-frozen-admission-certificate.json`; the later hardened certificate
does not replace that historical object. The durable amendment
`cycle273-nd270-p3-amendment.json` invalidates compute authorization without
rewriting the manifest.

The amendment also records an independent analytic rejection without generating
the trajectory. On the same Wiener slab, Minkowski and the exact datum norm give

\[
 \left|\log{\|u(T)\|_3\over\|u(0)\|_3}\right|
 <{50625\over80959}<{2\over3}<\log2<\log{201\over100}.
\]

Thus the frozen promotion gate is unreachable. The admission verdict remains
historical; the manifest remains frozen, while the amendment authorizes no
compute. The executor verifies every manifest, dependency, recovery,
superseding, and analytic-source digest before emitting either rejection or any
other status.

## Item 5: directed promotion

The family is the unscaled singleton in `cycle-272-p3-example.json`, on
normalized Haar `T^3`, in the forward direction, with

\[
 T={1\over65536}
\]

and checkpoints `0,T/4,T/2,3T/4,T`. Only the endpoint `T` can promote. The
complete-field threshold is frozen at

\[
 {\|u(T)\|_3\over\|u(0)\|_3}>{201\over100}=2.01.
\]

If outward rational cubature gives
`C_T>=L_T` and `C_0<=U_0` for the normalized-Haar cubic integrals, the exact
gate is

\[
 1000000L_T>8120601U_0.
\]

Equality fails. A sampled value, interior extremum, Galerkin-only ratio, or
post-output reversal cannot satisfy this gate.

## Item 6: finite replay path

The retained lead is fixed at cubic cutoffs `K=4,6`, with respectively 16 and
32 implicit-midpoint steps, dealiased sides 17 and 25, and doubled endpoint
cubature grids `(24,48)` and `(32,64)`. The sole full-Euler attempt uses `K=6`,
64 equal slabs, rationalized midpoint nodes, complete omitted-convolution
boxes, and the recentered Picard inclusions (265.13). Its endpoint cubature is
the fixed `64^3` cell rule with degree-four directed Taylor bounds and the full
analytic tail.

The generated-scale majorant remains exactly

\[
 q(t)={33\over32}(1-600t),\qquad A_{q(t)}(u(t))\le600,
 \qquad q(T)={267861\over262144}>1.
\]

Thus every absent initial mode enters through the analytic shell cap and the
retained--tail/tail--tail remainder, never through a Galerkin substitution.
The inviscid interface is frozen to Cycle 265 (265.17)--(265.24), with

\[
 Q={267861\over262144},\quad \rho_0={65\over64},\quad
 \beta=601,\quad \epsilon=1.
\]

These values satisfy `1<rho0<Q`, `beta>=600+epsilon`, and `rho(T)>1` in exact
rational arithmetic. A promoted certificate must recompute `B_up`, exhibit
the endpoint margin `delta`, and print the positive threshold
`nu0_rat=min(epsilon,delta)/B_up`.

## Resource preflight and stop

The manifest permits two logical cores, 1024 MiB resident memory, 21600 wall
seconds, 48 midpoint steps, 1920 nonlinear iterations, and one full-Euler
certificate attempt. The present host reports two logical cores and
`1002256*4096` bytes of physical memory, so the declared two-core preflight is
feasible. The current preflight also reports more than 1024 MiB available.
Thread counts are pinned to two. If available memory falls below 1024 MiB at
launch, preflight returns `ND270-RESOURCE-WALL` before producing a partial
trajectory.

No horizon, cutoff, slab, cubature, gate, or threshold may be changed after
output is observed. No trajectory was run while preparing this freeze.
