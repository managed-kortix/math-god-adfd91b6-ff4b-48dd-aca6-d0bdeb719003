# Cycle 67: reserve-demand increments and the sharp barrier

## Exact demand update

Fix `M` and update an endpoint from `B=M+r` to `B+1`. Write

\[
A=A_{M,r},\qquad a=\beta_B,\qquad A^+=A+a,
\]

and let `bar T,V,N,P` denote the Cycle 52 weighted mean, new-`D` variance,
weighted `U` cost, and projected square. Put

\[
e=T_B-\bar T,\qquad h={a\over A^+}e,
\]

\[
p=\Pi_Z(D+\bar T),\qquad s=\Pi_Zh,
\]

and let

\[
q={(I-\Pi_Z)\rho_B\over\|(I-\Pi_Z)\rho_B\|},
\quad d=\langle D,q\rangle,
\quad \tau={a\over A^+}\langle T_B,q\rangle.
\]

The exact online updates are

\[
\bar T^+=\bar T+{a\over A^+}e,
\qquad
V^+-V={Aa\over A^+}\|e\|^2,
\]

\[
N^+-N=w_B\|U+R_B\|^2,
\]

\[
P^+-P=2\Re\langle p,s\rangle+\|s\|^2+|d+\tau|^2.
\]

Since

\[
\Theta={N-V\over A}-P-W_M,
\]

the demand increment is

\[
\boxed{
\begin{aligned}
\Theta^+-\Theta={}&-{a\over A^+}{N-V\over A}
+{w_B\over A^+}\|U+R_B\|^2
-{Aa\over(A^+)^2}\|e\|^2\\
&-2\Re\langle p,s\rangle-\|s\|^2-|d+\tau|^2.
\end{aligned}}                                                    \tag{67.1}
\]

The staircase `W_M` is fixed; it appears only if the normalization term is
rewritten using `Theta+P+W_M`.

## Cancellation with reserve loss

The nested physical reserve obeys

\[
R^+-R=-|d|^2.
\]

For the normalized slack `F_r=R_(M,r)-Theta_(M,r)`, combining this with (67.1)
cancels the standalone old-`D` square:

\[
\boxed{
\begin{aligned}
F^+-F={}&{a\over A^+}{N-V\over A}
-{w_B\over A^+}\|U+R_B\|^2
+{Aa\over(A^+)^2}\|e\|^2\\
&+2\Re\langle p,s\rangle+\|s\|^2
+2\Re(\bar d\tau)+|\tau|^2.
\end{aligned}}                                                    \tag{67.2}
\]

The unresolved new-row channel is therefore a signed physical correlation,
not reserve loss by itself.

## Sharp finite-horizon barrier

Let

\[
p_r=R_r-R_{r+1}=|\langle D,q_r\rangle|^2,
\qquad
P(a,b)=\sum_{j=a}^{b-1}p_j.
\]

Then, for any current endpoint `a`,

\[
\boxed{
\exists r\in\{a,\ldots,12\}:R_r\ge\Theta_r
\iff
R_a\ge\min_{a\le r\le12}(\Theta_r+P(a,r)).}         \tag{67.3}
\]

This is sharp. Define the adjusted-demand increments

\[
c_r=p_r+\Theta_{r+1}-\Theta_r.                       \tag{67.4}
\]

The slack update is simply `F_(r+1)-F_r=-c_r`. If `c_r` has one sign crossing,
the adjusted demand is unimodal and only its minimizing endpoint must be
checked. More generally, an endpoint `tau` is the adjusted-demand minimizer
exactly when all cumulative sums toward it have the corresponding signs.

Nested Gram geometry gives no convexity: the payments `p_r` can be an arbitrary
nonnegative sequence. Any one-crossing or convexity theorem must come from the
physical arithmetic in (67.1).

## Durable finite path certificates

`verify_cycle67_reserve_demand_paths.py` independently computes:

- `R_r` from the complete restricted Vasyunin Gram and `W_M`;
- `Theta_r` from `V_D,N_U`, the endpoint projection, and `W_M`;
- the rank-one Schur payment `p_r`;
- the stored block budget only after both physical paths are complete.

For all eleven hard starts through the Cycle 51 frontier, Arb verifies

\[
S_M(r)=A_{M,r}(R_{M,r}-\Theta_{M,r})
\]

and every rank-one reserve update. Reserve decreases at every tested step.
Demand decreases in 120 of 132 transitions and increases in 12. In every tested
transition, a demand decrease is larger than the reserve payment; hence slack
rises exactly when demand falls.

The path at `M=222` succeeds at `r=4`, fails again for `r=5,6,7`, then recovers
from `r=8`; success is not endpoint-monotone. The critical `M=219` path has
three setbacks and first succeeds only at `r=12`, after a final demand drop of
about `0.09542` against a reserve payment of about `0.000280`.

These finite patterns strongly suggest demand descent dominates reserve loss on
physical recovery steps, but geometry alone does not imply it. The next target
is a physical bound on (67.1), preferably a cumulative adjusted-demand barrier
rather than one-step monotonicity. No additive-12 theorem or RH result is
claimed.
