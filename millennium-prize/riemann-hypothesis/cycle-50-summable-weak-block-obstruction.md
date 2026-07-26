# Cycle 50: the logarithmically weakened block estimate is summable

Let

\[
w_n=1-{\log n\over\log(n+1)},\qquad
h_n={1\over\log n}-{1\over\log(n+1)}={w_n\over\log n}.
\]

A genuinely weaker checkpoint asks for constants `kappa>0`, `C>1` such that,
from every large `M`, some `M<B<=M^C` satisfies

\[
\boxed{P_M-P_B\ge {2\kappa\over\log M}
\sum_{n=M}^{B-1}w_nP_n.}                         \tag{50.1}
\]

## Finite effective mass

Choose consecutive successful endpoints `M_j`. The coefficient mass is

\[
\mathfrak M=\sum_j{2\kappa\over\log M_j}
\sum_{n=M_j}^{M_{j+1}-1}w_n.
\]

For `M_j<=n<M_(j+1)`,

\[
1\le{\log n\over\log M_j}\le C,
\qquad {w_n\over\log M_j}={\log n\over\log M_j}h_n.
\]

Since the blocks partition the tail and `sum_(n>=M_0)h_n=1/log M_0`,

\[
\boxed{{2\kappa\over\log M_0}\le\mathfrak M
\le{2C\kappa\over\log M_0}<\infty.}             \tag{50.2}
\]

Block count cannot amplify this normalization. The sharp countermodel is
`P_(n+1)=(1-2 kappa h_n)P_n`: every singleton satisfies (50.1) with equality,
but `P_n` tends to a positive limit because `sum h_n<infinity`. Hence (50.1)
does not imply zero liminf and must not be advertised as an RH theorem.

## Finite diagnostics

For a finite block define

\[
\mathcal C(M,B)={\log M\,(P_M-P_B)
\over\sum_{n=M}^{B-1}w_nP_n}.                    \tag{50.3}
\]

Then (50.1) is `mathcal C(M,B)>=2 kappa`. An exhaustive 192-bit Arb scan of all
`2094081` blocks through endpoint `2048` certifies the unique minimum

\[
\boxed{\mathcal C(2,3)=0.500216360219450559319039750769155\ldots.} \tag{50.4}
\]

Coefficient `0.5` in the unhalved form passes every finite block. Coefficient
`0.75` fails exactly on `(2,B)`, `3<=B<=11`, and coefficient `1` fails on the
entire tested `M=2` row. For `M>=3`, the finite minimum is
`mathcal C(3,5)=1.39454696723279215755...`. These are finite facts only.

The stronger fixed half-strength local pattern remains computationally live:
every tested start `3<=M<=2036` has a half-strength endpoint within `M+12`,
with weakest chosen block `[219,231)` and ratio `0.5023844149...`. A proof of
that fixed-strength statement would retain divergent mass and be RH-sufficient
in this funnel; finite evidence is not a proof.

## Analytic obstruction

On the first post-cutoff shell, the fresh transform is

\[
T_M(k)={1\over\log M}\sum_{M<a\le k}\mu(a)\log(M/a).
\]

Writing the numerator as `R_M(k)`, absorption with only `kappa/log M` reserve
requires

\[
\boxed{\sum_{M<k\le2M}|R_M(k)|^2\ll_\kappa {M^2\over\log M}.} \tag{50.5}
\]

This is RMS cancellation of size `sqrt(M/log M)`. Classical zero-free-region
bounds give only `|R_M(k)| << M E(M)` with
`E(M)=exp[-c(log M)^(3/5)(log log M)^(-1/5)]`, missing (50.5) by the divergent
factor `M log M E(M)^2`. The loss lies in coherent correlations, not isolated
impulse diagonals.

Thus the weakened target is meaningful and genuinely below RH, but separated
magnitude estimates still demand square-root weighted-Mertens cancellation. No
RH result is claimed.
