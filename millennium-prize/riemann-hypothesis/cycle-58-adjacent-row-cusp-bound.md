# Cycle 58: adjacent-row cusp bound for the lagged certificate

## Exact adjacent-row error

Retain the Cycle 57 projection

\[
E=I-\Pi_{Z\oplus\langle g_M\rangle},
\qquad r=ED_{M-1},\qquad R=\|r\|^2.
\]

For lag `ell=2`, the omitted suffix is the single row

\[
T_2=\mu(M-1)\log(M-1)\rho_{M-1}.
\]

Put `beta_2=||ET_2||^2`. Since `rho_M` belongs to `Z`, for every scalar `a`,

\[
\beta_2\le\mu(M-1)^2\log^2(M-1)
\|\rho_{M-1}-a\rho_M\|^2.                        \tag{58.1}
\]

The exact optimizer is

\[
a_*={\langle\rho_{M-1},\rho_M\rangle\over\|\rho_M\|^2},
\]

so the right side is a two-by-two restricted Vasyunin Schur complement.
An explicit unconditional bound is

\[
\boxed{
\beta_2\le\mu(M-1)^2\log^2(M-1)
\left[{H_{M-1}\over(M-1)^2}+{2\over M(M-1)}
-{1\over M^2(M-1)^2}\right].}                    \tag{58.2}
\]

Here `H_n` denotes the harmonic number, not the endpoint defect. Consequently,

\[
\boxed{\beta_2=O(\log^3(M)/M^2).}                 \tag{58.3}
\]

This corrects the cruder `O(log^2 M/M)` suffix scale. The extra `1/M` comes
from reciprocal scaling of the near-diagonal cusp.

## Exact lag consequence

Cycle 57 gives

\[
\boxed{G_2\ge R-\beta_2.}                         \tag{58.4}
\]

Combining (58.1) with the exact physical `R` therefore yields a completely
explicit lower certificate using only the post-`g_M` residual norm and the
adjacent two-row Vasyunin determinant.

At 256-bit precision, replacing `beta_2` by the simpler projection onto
`rho_M` alone still certifies all eleven historical delayed first-recovery
windows. On `[219,231)`,

\[
R=0.0584054085893\ldots,
\qquad \widehat\beta_2=0.00310741516629\ldots,
\]

and the resulting block lower margin is

\[
\boxed{3.43318590172\times10^{-6}>0.}             \tag{58.5}
\]

The weakest historical margin under this rho-only bound is
`2.46060003036e-6` at `[222,226)`. Four windows are tautological at this level
because `mu(M-1)=0`, hence `beta_2=0`.

## What the cusp bound does not prove

Small suffix error alone is insufficient. To pay a normalized residual deficit
`delta_(M,B)`, (58.4) still requires

\[
\boxed{R\ge\beta_2+\delta_{M,B}.}                 \tag{58.6}
\]

The optimal staircase reserve `W_M` has already been extracted and gives no
lower bound for `R`. Abstract positive-Gram models can keep `beta_2` fixed while
making the residual orientation defeat the lagged probe. The physically
positive singleton `[98,99)` is a finite warning: no single lagged state
certifies that endpoint, despite its true positive budget.

Thus the adjacent-row cusp solves the finite suffix-size problem and gives a
compact certificate for all known delayed windows, but a uniform theorem still
needs an arithmetic lower bound for the post-staircase residual `R`, or a direct
orientation estimate in the exact gain formula. No additive-12 theorem or RH
result is claimed.
