# Cycle 214: Euclidean and antisymmetric analytic shell bound

## Paired Fourier coefficient

In the Cycle 212 vorticity normalization, pair the ordered terms `(p,q)` and
`(q,p)` before taking absolute values. Since `omega_p omega_q` is symmetric,

\[
 {1\over2}\left({p^\perp\!\cdot q\over |p|_2^2}
 +{q^\perp\!\cdot p\over |q|_2^2}\right)
 ={(p^\perp\!\cdot q)(|q|_2^2-|p|_2^2)
   \over2|p|_2^2|q|_2^2}.                         \tag{214.1}
\]

Thus equal Euclidean shells cancel exactly. For `p+q=k`, the cosine law gives
`|q|_2^2-|p|_2^2=|k|_2^2-2 k dot p`, while
`p^perp dot q=p^perp dot k`. Consequently

\[
 |(214.1)|\le {|k|_2^2\over2}\left({1\over|q|_2^2}
 +{1\over|p|_2|q|_2}\right),
                                                               \tag{214.2}
\]

and likewise after interchanging `p,q`. When both inputs lie outside the
`l-infinity` shell `L`, (214.2) is at most `|k|_2^2/L^2`. This is the useful low-output cancellation: the previous
ordered bound grows like the input-shell ratio, whereas the paired coefficient
costs two inverse input radii.

The validator now evaluates every retained-retained convolution using the exact
rational coefficient (214.1), so equal-radius cancellation occurs before
interval multiplication.

## Analytic enstrophy tail

Let `s>=0`, `rho>1`, and suppose a slab certificate supplies

\[
 E_{rho,s}=\sum_{j\ne0}rho^{2|j|_infinity}
 (1+|j|_infinity)^{2s}|omega_j|^2\le E.          \tag{214.3}
\]

For a target `k` with `|k|_infinity=n`, write
`A_j=rho^|j| (1+|j|)^s |omega_j|`. The triangle inequality implies
`rho^(-|p|-|q|)<=rho^(-n)`, and
`(1+|p|)^(-s)(1+|q|)^(-s)<=(1+n)^(-s)`. For each fixed `k`,
Cauchy--Schwarz yields

\[
 \sum_{p+q=k}|omega_p omega_q|
 \le rho^{-n}(1+n)^{-s}E.                         \tag{214.4}
\]

There are exactly `8n` lattice modes on the target `l-infinity` shell and
`|k|_2^2<=2n^2`. Combining (214.2)--(214.4), with both inputs at shell at least
`L`, gives the cancellation-aware shell mass bound

\[
 Q_n^{AA}\le {16 n^3\over L^2(1+n)^s}E rho^{-n}. \tag{214.5}
\]

For `s>=2`, its normalized coefficient is at most `16En/L^2`. Hence the finite cap check still
has an exact quadratic dissipative ray: the head-tail contribution is linear,
the analytic tail-tail contribution is linear, and `mu n^2` dominates at
large `n`. This removes the artificial quadratic tail-tail competition that
made small-viscosity faces impractical.

## Validator use and scope

`analytic_enstrophy_tail_bound` implements (214.5) with exact rationals.
`shell_convolution_bound`, `low_mode_tail_remainder_bound`, and
`check_dissipative_shell_cap` accept optional `weighted_enstrophy` and
`analytic_order` arguments. They take the minimum of the old geometric
tail-tail estimate and (214.5) on finite faces. For the infinite ray and
`analytic_order>=2`, the checker uses the linear normalized majorant
`16En/L^2`, preserving a fail-closed exact quadratic test.

The weighted enstrophy bound must itself be enclosed on every slab; ordinary
unweighted enstrophy is insufficient to provide the factor `rho^-n`. This is a
sharper validation primitive, not a completed trajectory certificate or a
Navier--Stokes result.
