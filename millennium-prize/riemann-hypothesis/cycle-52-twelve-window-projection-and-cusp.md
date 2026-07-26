# Cycle 52: twelve-window projection failure and near-diagonal cusp

## Sharp finite-window projection

Fix `M<B<=M+12` and let the incoming state be

\[
U=U_{M-1},\qquad D=D_{M-1}.
\]

For `M<=n<B`, put

\[
R_n=\sum_{q=M}^n\mu(q)\rho_q,
\qquad T_n=\sum_{q=M}^n\mu(q)\log q\,\rho_q,
\]

and let `A=sum_[M,B) beta_n`,

\[
\bar T=A^{-1}\sum_{n=M}^{B-1}\beta_nT_n,
\qquad
V_D=\sum_{n=M}^{B-1}\beta_n\|T_n-\bar T\|^2,
\]

\[
N_U=\sum_{n=M}^{B-1}w_n\|U+R_n\|^2.
\]

Then the exact local budget is

\[
\boxed{
\mathcal L_{M,B}=V_D+A\|D+\bar T\|^2-N_U.}       \tag{52.1}
\]

Project `D+bar T` onto

\[
Z=\operatorname{span}\{U,\rho_M,\ldots,\rho_{B-1}\}.
\]

If `Gamma` is the restricted Gram matrix of these at most thirteen probes and
`b_z=<D+bar T,z>`, then

\[
\boxed{
\mathcal L_{M,B}=V_D+A b^*\Gamma^+b-N_U
+A\|(I-\Pi_Z)(D+\bar T)\|^2.}                    \tag{52.2}
\]

This is the sharp lower bound obtainable from that finite probe span. It fails
on the longest physical recovery window `[219,231)`:

\[
V_D+A b^*\Gamma^+b-N_U
=-0.000800940341739026513185152934022\ldots<0,
\]

while

\[
\mathcal L_{219,231}
=0.00000447638964978814930552741203924\ldots>0.
\]

The missing orthogonal old-`D` square is
`0.000805416731388814662490680346061...`. Thus essentially all recovery lies
outside the incoming `U` plus twelve-new-vector span. Adding `D` as a probe
makes the identity exact and tautological. Finite-window Schur positivity alone
cannot prove additive-12 recovery.

## Near-diagonal Vasyunin cusp

For `0<a<=b`, let

\[
K(r)=\int_0^\infty\{t\}\{rt\}{dt\over t^2},
\qquad r=a/b.
\]

The restricted correlation is exactly

\[
G_{a,b}={K(a/b)\over a}-{1\over ab}.              \tag{52.3}
\]

Writing

\[
D(r)=\int_0^\infty(\{t\}-\{rt\})^2{dt\over t^2},
\]

polarization gives `K(r)=[c_0(1+r)-D(r)]/2`, where
`c_0=log(2pi)-gamma`. For `r=1-epsilon`,

\[
\boxed{D(1-\varepsilon)=\varepsilon\log(1/\varepsilon)
+O(\varepsilon).}                                 \tag{52.4}
\]

Consequently, uniformly for fixed `0<=k<j<=11`,

\[
\boxed{
G_{M+k,M+j}={c_0\over M}
-{j-k\over2M^2}\log{M\over j-k}+O(M^{-2}).}      \tag{52.5}
\]

The kernel is not differentiable at coincident scales. A pure Taylor expansion
in `j/M` is therefore invalid; the correct local scale contains
`(j/M)log(M/j)`.

The newly generated portion of the impulse has a universal local leading term
depending on the twelve Möbius values, but the incoming part retains twelve
distinct old-state projections

\[
\Phi_{M,j}=\log(M+j)\langle D_{M-1},\rho_{M+j}\rangle
-C_{M+j}\langle U_{M-1},\rho_{M+j}\rangle.        \tag{52.6}
\]

The cusp estimate controls differences only by norms of the full old vectors,
at a scale much larger than the local main term. Hence the window does not
reduce to local Möbius moments plus one incoming scalar without new global
Vasyunin cancellation.

## Finite pattern and budget audit

Among all `3058` complete twelve-windows through start `3060`, only eleven
starts require more than one cell:

```text
39, 40, 95, 96, 99, 100, 219, 220, 221, 222, 226.
```

Möbius pattern alone is insufficient: the same twelve-symbol pattern occurs at
starts `100` and `2084`, but the former begins with negative `H_100` and the
latter with positive `H_2084`. The full twelve-cell sum is also too strong: it
is negative at starts `217,218`, even though both windows succeed at an earlier
prefix.

At first-success endpoints, the weakest certified full budget remains
`4.4763896497881493e-6` at `[219,231)`. Decomposing into incoming level,
negative drift, signed linear event correlations, and negative event diagonal
shows no fixed sign pattern. The exact state threshold remains the weighted
quantitative impulse budget, not a local symbol classifier.

## Explicit hostile arithmetic window

The first known run of twelve consecutive nonsquarefree integers begins at

\[
\boxed{M=47\,255\,689\,915.}                      \tag{52.7}
\]

Exact square divisors are verified by `verify_cycle52_crt_window.py`. On this
window every impulse vanishes, so

\[
H_{M+j}=H_{M-1}-(C_{M+j}-C_{M-1})\|U_{M-1}\|^2.
\]

All twelve prefixes fail if and only if `H_M<0`. The current complete-Gram
implementation cannot evaluate this index, so it is a concrete hostile test
point, not a counterexample.

No additive-12 theorem or RH result is claimed.
