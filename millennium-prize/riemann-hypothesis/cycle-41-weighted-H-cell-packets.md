# Cycle 41: exact unit-cell packets for the weighted H block

## 1. Keep the two squares separate

Retain the notation of Cycle 40:

\[
 C_n=L_nL_{n+1},\qquad
 \beta_n={L_{n+1}-L_n\over L_nL_{n+1}^2},\qquad
 w_n={L_{n+1}-L_n\over L_{n+1}}.
\]

Thus `beta_n C_n=w_n`. On the unit cell `k<t<k+1`, put

\[
 \lambda_k=\log(1+1/k),\qquad
 \tau_k={1\over k(k+1)},\qquad
 q_k=\tau_k-\lambda_k^2.
\]

The integral of an affine function has the exact completed-square form

\[
 \int_k^{k+1}{(at+b)^2\over t^2}\,dt
 =(a+\lambda_kb)^2+q_kb^2.                 \tag{41.1}
\]

Here `q_k>0`: Cauchy--Schwarz on `[k,k+1]` gives
`(int dt/t)^2<(int 1 dt)(int dt/t^2)`. Define the nonnegative packets

\[
 \mathcal D_{n,k}=(\ell_n+\lambda_kv_{n,k})^2+q_kv_{n,k}^2,
 \qquad
 \mathcal U_{n,k}=(m_n+\lambda_ku_{n,k})^2+q_ku_{n,k}^2.             \tag{41.2}
\]

Then the weighted cell is exactly

\[
 \boxed{\beta_n h_{n,k}=\beta_n\mathcal D_{n,k}
                         -w_n\mathcal U_{n,k}.}                     \tag{41.3}
\]

This is the desired local positive/negative packet decomposition. It is an
identity, not an estimate, and no absolute values have been introduced.
Summing complete cells gives

\[
 \boxed{\beta_nH_n=\sum_{k\ge1}
   (\beta_n\mathcal D_{n,k}-w_n\mathcal U_{n,k}).}                  \tag{41.4}
\]

## 2. Initial Chebyshev packets

For `1<=k<=n`, divisor completion gives `u_(n,k)=0` and
`v_(n,k)=psi(k)`. Therefore

\[
 \boxed{\beta_nh_{n,k}
 =\underbrace{\beta_n[(\ell_n+\lambda_k\psi(k))^2
                         +q_k\psi(k)^2]}_{\mathcal P_{n,k}\ge0}
  -\underbrace{w_nm_n^2}_{\mathcal N_n\ge0}.}                      \tag{41.5}
\]

The negative packet is independent of `k`, but occurs in every one of the
first `n` cells. Consequently the exact initial contribution is

\[
 \sum_{k=1}^n\beta_nh_{n,k}
 =\beta_n\sum_{k=1}^n[(\ell_n+\lambda_k\psi(k))^2+q_k\psi(k)^2]
  -nw_nm_n^2.                                                       \tag{41.6}
\]

Formula (41.6) explains why bounding the negative cells individually is the
wrong operation. Their repeated mass `nw_nm_n^2` must be compared with the
coherent Chebyshev square and with the complete divisor-floor tail. Dropping
the tail, or applying `|m_n|` and `|ell_n|` separately, destroys the observed
compensation.

## 3. Exact divisor pairing, valid in every cell

Set

\[
 f_{a,k}=\lfloor k/a\rfloor,
 \qquad c_{a,k}={1\over a}-\lambda_k f_{a,k}.
\]

The affine centers in (41.2) have the exact finite forms

\[
 m_n+\lambda_ku_{n,k}
 =\lambda_k+\sum_{a\le n}\mu(a)c_{a,k},                            \tag{41.7}
\]

\[
 \ell_n+\lambda_kv_{n,k}
 =\sum_{a\le n}\mu(a)(\log a)c_{a,k}.                             \tag{41.8}
\]

Together with

\[
 u_{n,k}=1-\sum_{a\le n}\mu(a)f_{a,k},\qquad
 v_{n,k}=-\sum_{a\le n}\mu(a)(\log a)f_{a,k},                    \tag{41.9}
\]

these give a cancellation-preserving divisor formula for both packets:

\[
 \boxed{\begin{aligned}
 \mathcal U_{n,k}
  &=(\lambda_k+\sum_{a\le n}\mu(a)c_{a,k})^2
    +q_k(1-\sum_{a\le n}\mu(a)f_{a,k})^2,\\
 \mathcal D_{n,k}
  &=(\sum_{a\le n}\mu(a)(\log a)c_{a,k})^2
    +q_k(\sum_{a\le n}\mu(a)(\log a)f_{a,k})^2.
 \end{aligned}}                                                   \tag{41.10}
\]

No Chebyshev substitution is used here, so (41.10) remains exact for `k>n`.
When `k<=n`, the two complete divisor sums in (41.9) become `0` and
`-psi(k)`, recovering (41.5).

There is also an exact adjacent-`n` pairing. If the four linear coordinates
in (41.10) are retained before squaring, admission of the divisor `n` changes
them by

\[
 \mu(n)(c_{n,k},-f_{n,k},(\log n)c_{n,k},-(\log n)f_{n,k}).         \tag{41.11}
\]

Thus every fixed-`k` unweighted packet comparison can be expanded as
`(X+r)^2-X^2=2Xr+r^2`, with the signed old-divisor/new-divisor correlation
`2Xr` still present. The outer weights `beta_n,w_n` also change with `n` and
must remain in the block sum. This is the exact pairing that is lost if either
square is bounded termwise.

## 4. Abel pairing across the scale index

For a block `[A,B)`, do not replace the cell differences by absolute bounds.
First sum them exactly:

\[
 \boxed{\mathfrak R_{1/2}(A,B)
 =\sum_{n=A}^{B-1}\sum_{k\ge1}
   (\beta_n\mathcal D_{n,k}-w_n\mathcal U_{n,k}).}                 \tag{41.12}
\]

Equivalently, with `C_A(m)=sum_(n=A)^m H_n`, finite Abel summation gives

\[
 \boxed{\mathfrak R_{1/2}(A,B)
 =\beta_{B-1}C_A(B-1)
  +\sum_{m=A}^{B-2}(\beta_m-\beta_{m+1})C_A(m).}                   \tag{41.13}
\]

Every outer Abel coefficient is positive. The cumulative terms must still be
formed from the signed packet sum (41.12). Equations (41.10)--(41.13) provide
the exact search space for compensating a negative band: preserve each
old/new-divisor correlation in `C_A(m)`, then test the positive Abel average.

The scalar slopes themselves also possess an exact Abel relation,

\[
 \boxed{\ell_n=L_nm_n-
  \sum_{j=1}^{n-1}(L_{j+1}-L_j)m_j,}                               \tag{41.14}
\]

obtained by summation by parts from
`m_n=sum_(a<=n)mu(a)/a`. Hence `ell_n` and `m_n` in (41.5) are not independent
quantities. Applying separate absolute bounds to them discards precisely the
cross-scale information in (41.14).

## 5. What the pairing does and does not prove

The certified Cycle 40 computation through `n=512` has negative bands

\[
 \{2\},\quad\{39,40\},\quad\{95,96\},\quad\{99,100\},\quad
 \{219,220,221,222\},\quad\{226\}.
\]

Using the exact weight in (41.12), every start in that finite range reaches a
nonnegative block; the longest first passage is `[219,231)`. Thus positive
indices at later `n` do compensate every certified negative band in this range.
This is a finite exact-Arb fact, not a uniform pairing theorem.

The formulas also isolate the unresolved point. The completed squares prove
packet nonnegativity, but they do not compare the differently weighted packets
`beta_n D_(n,k)` and `w_n U_(n,k)`. A global proof still needs a lower bound
for their signed, complete divisor correlation after summation across `n` and
`k`. Neither positivity of the squares nor Abel summation alone supplies that
arithmetic inequality, so no RH result is claimed.
