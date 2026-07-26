# Cycle 46: anchored dispersion geometry and atomic antialignment

## Exact anchored projection decomposition

For `M<b<=B`, retain the Cycle 45 packets

\[
X_b=\sum_{r=M}^{b-1}W_{M,r}h_rD_r,
\qquad
\alpha_b={w_b\over W_{M,b}W_{M,b-1}}.
\]

Then `V_(M,B)=sum alpha_b||X_b||^2`. Let `K_(bc)=<X_b,X_c>`,
`c_b=<F_M,X_b>`, `A=diag(alpha_b)`, and let `K^+` be the Moore--Penrose
inverse. Orthogonal projection onto the packet span gives

\[
\boxed{
P_M-V_{M,B}=\|(I-\Pi)F_M\|^2+c^*K^+c-\operatorname{tr}(AK).} \tag{46.1}
\]

Indeed `c^*K^+c=||Pi F_M||^2` and `tr(AK)=V_(M,B)`. This is an exact
decomposition, not a positivity theorem. The tempting stronger condition
`c^*K^+c>=tr(AK)` already fails for one nonparallel packet by strict
Cauchy--Schwarz. More generally, coefficient-space Loewner domination of the
covariance by the rank-one anchor is impossible unless every centered
coefficient vector lies on the anchor line. Thus neither Schur positivity nor
rank-one PSD comparison supplies the desired anchored contraction.

## Atomic anchor--increment target

Work strictly in the restricted space `L^2(0,1)`. Put

\[
F_M=\chi+\sum_{a\le M}\mu(a)
\left(1-{\log a\over\log M}\right)\rho_a,
\qquad
D_r=\sum_{q\le r}\mu(q)\log q\,\rho_q.
\]

The exact atomic correlation is

\[
\boxed{
\langle F_M,D_r\rangle
=\sum_{q\le r}\mu(q)\log q\left[
g_q+\sum_{a\le M}\mu(a)
\left(1-{\log a\over\log M}\right)G^0_{a,q}
\right],}                                                   \tag{46.2}
\]

where

\[
g_q={\log q+1-\gamma\over q},\qquad
G^0_{a,q}=G^\infty_{a,q}-{1\over aq}.
\]

The rank-one domain correction applies to `G`, not to `g`. Using
`(log q-gamma)/q` is a restricted/full-space error and reverses many finite
signs.

At 192-bit precision, complete restricted Vasyunin evaluation certifies

\[
\boxed{\langle F_M,D_r\rangle<0
\quad(2\le M\le r\le512).}                              \tag{46.3}
\]

All `130816` intervals are strictly negative. The largest is attained at
`(M,r)=(221,221)` and is

\[
-0.1836867664634268575149843177834429\ldots.
\]

Thus finite data suggest the exact restricted antialignment conjecture

\[
\langle F_M,D_r\rangle\le0\qquad(r\ge M\ge2).             \tag{46.4}
\]

Since all coefficients `W_(M,r)h_r` are positive, (46.4) would imply
`<F_M,X_b><=0` and, more basically,

\[
\langle F_M,F_n-F_M\rangle\le0.
\]

## Scope and next obstruction

Even a proof of (46.4) would not prove terminal positivity. Polarization gives

\[
P_n-P_M=2\langle F_M,F_n-F_M\rangle+\|F_n-F_M\|^2,
\]

and the positive displacement square remains uncontrolled. Likewise the Cycle
44 terminal criterion involves all increment--increment correlations through
the future-path dispersion. Atomic antialignment controls only the anchor row.

The next exact target is therefore a coupled inequality in which the negative
anchor correlations pay a quantified part of the cumulative packet squares,
without demanding false rank-one Loewner domination. Equation (46.2) is the
finite Mobius--Vasyunin numerator for that attack. No infinite-tail estimate,
terminal sign theorem, or RH result is claimed.

## Reproduction

```text
uv run --with python-flint python verify_cycle46_atomic_antialignment.py
```
