# Cycle 57: lagged-prefix projection and its limits

## Exact suffix identity

Retain the Cycle 56 notation and project beyond both the local span and the
optimal staircase witness:

\[
E=I-\Pi_{Z\oplus\langle g_M\rangle},
\qquad r=ED_{M-1},
\qquad R=\|r\|^2.
\]

For an integer lag `ell>=1`, put

\[
T_\ell=D_{M-1}-D_{M-\ell}
=\sum_{a=M-\ell+1}^{M-1}\mu(a)\log a\,\rho_a,
\]

\[
s_\ell=ET_\ell,
\qquad x_\ell=ED_{M-\ell}=r-s_\ell.
\]

If `x_ell!=0`, adjoining the lagged state gives the exact Schur gain

\[
\boxed{
G_\ell={|\langle r,x_\ell\rangle|^2\over\|x_\ell\|^2}
={|R-\alpha_\ell|^2\over
R-2\operatorname{Re}\alpha_\ell+\beta_\ell},}    \tag{57.1}
\]

where

\[
\alpha_\ell=\langle r,s_\ell\rangle,
\qquad \beta_\ell=\|s_\ell\|^2.
\]

The uncaptured energy is

\[
\boxed{
R-G_\ell
={R\beta_\ell-|\alpha_\ell|^2\over
R-2\operatorname{Re}\alpha_\ell+\beta_\ell}
=\|(I-\Pi_{x_\ell})s_\ell\|^2.}                 \tag{57.2}
\]

If `x_ell=0`, the gain is zero. In all cases,

\[
\boxed{0\le R-G_\ell\le\beta_\ell,
\qquad G_\ell\ge\max(0,R-\beta_\ell).}          \tag{57.3}
\]

Thus a lagged prefix captures the entire residual except for a projection of
the finitely many omitted recent rows. This is an approximation identity, not
a lower bound for `R` itself.

Writing `H_(a,b)=<E rho_a,E rho_b>`, both `alpha_ell` and `beta_ell` are exact
finite restricted Vasyunin contractions. The suffix norm obeys the
near-diagonal cusp estimate `beta_ell=O_ell(log^2(M)/M)`, but the global
correlation `alpha_ell` is not determined by the local Möbius pattern.

## Degeneracies and generic no-go

The lag is tautological when the omitted suffix vanishes, or more generally
when its residual is collinear with `r`. It gives no direction when
`s_ell=r`. Outside these cases the gain is genuinely partial.

No fixed lag has a positive generic capture fraction. In an abstract positive
Gram model one may choose `r=s_ell+epsilon v`, with `v` orthogonal to
`s_ell`; then the lagged probe is `epsilon v` and its gain tends to zero while
`R` tends to `||s_ell||^2`. The same construction defeats any fixed finite
family of lag probes. Hence a uniform theorem must use the actual old-prefix
Möbius--Vasyunin orientation, not nesting or Gram positivity.

## Certified finite existential map

The complete physical scan through start `3060` has only eleven starts with a
negative singleton defect. At the first physical recovery endpoint for each of
these starts, the optimal `g_M` witness plus one explicitly residualized global
probe `D_(M-3)` gives a positive 256-bit Arb lower bound:

| start | endpoint | certified lower margin |
|---:|---:|---:|
| 39 | 42 | `4.07629007823e-4` |
| 40 | 42 | `4.55296690927e-4` |
| 95 | 103 | `4.76374629673e-5` |
| 96 | 103 | `1.36059524821e-4` |
| 99 | 102 | `7.33582361268e-5` |
| 100 | 102 | `7.83755321344e-5` |
| 219 | 231 | `8.85362206864e-7` |
| 220 | 231 | `9.78785848974e-6` |
| 221 | 231 | `2.06958866470e-5` |
| 222 | 226 | `2.49360151164e-6` |
| 226 | 230 | `1.26259048123e-5` |

Every other certified start succeeds physically at its singleton endpoint, so
no lagged witness is needed to verify the finite additive-12 statement there.
This yields a finite certificate map through `3060`, not a proof for later
starts.

The distinction between physical positivity and certification by this witness
family is important. The physically positive singleton `[98,99)` is **not**
certified by `g_98` plus any one lagged state `D_(98-ell)`, for
`2<=ell<=96`; the best lower margin is still
`-4.8996526752e-7`. Recomputing at later endpoints, the same start is certified
by endpoint `102`. Hence one cannot fix the endpoint first or transfer a Schur
gain between endpoints: the span and residual must be recomputed for every
`(M,B)`.

The finite success of `D_(M-3)` imports nearly the complete old state. It is a
compact exact certificate for the observed delayed windows, but not a local
arithmetic mechanism and not an additive-12 theorem. No RH result is claimed.
