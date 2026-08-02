# Cycle 258: frozen integrated-logarithmic-L3 trajectory architecture

## Pre-compute freeze

This architecture is fixed before any Cycle 258 trajectory computation. It is
a numerical candidate screen only. It neither encloses the full Euler PDE nor
certifies an `ND251` crossing.

The five Cycle 257 finite-Fourier streamfunction candidates in
`cycle257-initial-l3-candidates.json` are the only centers. Their mode list,
coefficients, energy normalization, and enstrophy values
`rho in {4,8,12,16,20}` are copied without further initial-derivative
optimization.

For each center `x`, define two deterministic coefficient directions

\[
 d^{(s)}_j=\sin((s+1)(j+1)\sqrt2)
          +\tfrac12\cos((s+2)(j+1)0.7548776662466927),\qquad s=0,1.
\]

Project each direction onto the simultaneous tangent space of the Cycle 257
energy and enstrophy constraints at `x`, then normalize it in Euclidean
coefficient norm. The frozen local family consists of the center and

\[
 x+\sigma\delta d^{(s)},\qquad
 s\in\{0,1\},\quad \sigma\in\{-1,1\},\quad
 \delta\in\{0.025,0.075\}.
\]

Each perturbed vector is retracted exactly as in Cycle 257: a deterministic
spectral tilt restores `Z/E=rho`, followed by scalar normalization to `E=1`.
Thus the family has exactly `5*(1+2*2*2)=45` labelled members. There are no
random starts, adaptive additions, or derivative-based exclusions.

## Numerical flow and objective

For every member solve the square-two-thirds Fourier pseudospectral vorticity
Euler system with classical RK4, independently in directions `-1` and `+1`.
Use normalized-Haar grid cubature for velocity `L3`. Freeze:

- resolutions `N=64` and `N=128`, with square cutoffs `21` and `42`;
- horizon `T=2.5` in each direction;
- steps `dt=1/128` at `N=64` and `dt=1/256` at `N=128`;
- checkpoints every `1/64`, including `t=0` and both endpoints;
- all 45 members at both resolutions, with no N=64 shortlist.

The optimization score is finite-time accumulated logarithmic growth, not the
initial derivative. Along each directed trajectory compute

\[
 I(t)=\int_0^t {d\over ds}\log\|u(s)\|_3\,ds
\]

by composite trapezoidal quadrature of the Euler right-hand-side expression at
the frozen `1/64` checkpoints. Select each member's best directed checkpoint by
maximum `I`.
As a mandatory numerical breaker, also compute
`log(||u(t)||_3/||u(0)||_3)` directly and report the largest discrepancy from
`I(t)`. The bidirectional variation ratio is the largest sampled `L3` divided
by the smallest sampled `L3` over `[-T,T]`; this is the promotion statistic.

Report endpoint relative energy and enstrophy drift, the N=64/N=128 ratio
difference for every common member, and the deterministic winner. Stop this
frozen family after these two resolutions if no N=128 bidirectional variation
ratio is strictly greater than `1.1`. A pass would only promote a numerical
candidate to a separately designed validation stage; it would not be a PDE
claim.
