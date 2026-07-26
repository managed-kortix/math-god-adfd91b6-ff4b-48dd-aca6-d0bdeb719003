# Cycle 44: physical terminal residual as future-path dispersion

## Finite theorem

Work in the restricted Nyman--Beurling Hilbert space and retain the physical
vectors `F_n` with `P_n=||F_n||^2`. For a fixed start `M` and endpoint `B>=M`,
put

\[
W_{M,B}=\sum_{n=M}^B w_n,\qquad
\bar F_{M,B}=W_{M,B}^{-1}\sum_{n=M}^Bw_nF_n,
\]

and define the truncated terminal budget

\[
Q_{M,B}=P_M-\sum_{n=M}^Bw_nP_n.
\]

The weighted variance identity gives the exact cancellation-preserving formula

\[
\boxed{
Q_{M,B}=P_M-W_{M,B}\|\bar F_{M,B}\|^2
-\sum_{n=M}^Bw_n\|F_n-\bar F_{M,B}\|^2.}        \tag{44.1}
\]

Equivalently,

\[
\boxed{
Q_{M,B}=P_M-W_{M,B}\|\bar F_{M,B}\|^2
-{1\over2W_{M,B}}\sum_{m,n=M}^Bw_mw_n\|F_m-F_n\|^2.} \tag{44.2}
\]

These are finite Hilbert-space identities. In coefficient coordinates their
last term contracts the complete positive coefficient covariance with the
restricted Vasyunin Gram matrix. The affine coordinate cancels from every
centered vector and pair difference. No entrywise infinite Gram limit is used.

**Proof.** Expand
`sum w_n||F_n-bar F||^2` and use `sum w_n(F_n-bar F)=0`.
Expanding the double pair sum gives the same variance with the factor
`1/(2W)`. Subtract the result from `P_M`.

The variance is nondecreasing when endpoints are added. If a vector `F` with
weight `w>0` is appended to an old packet of mass `W` and mean `bar F`, then

\[
\mathcal V_{new}-\mathcal V_{old}
={wW\over W+w}\|F-\bar F\|^2\ge0.              \tag{44.3}
\]

## Conditional exhaustion

Assume the substantive global estimate

\[
E_M:=\sum_{n=M}^\infty w_nP_n<\infty.           \tag{44.4}
\]

Because `sum_(n>=M)w_n=infinity`, one then has

\[
W_{M,B}\|\bar F_{M,B}\|^2\longrightarrow0.     \tag{44.5}
\]

To prove this, write `S_B=sum_(n=M)^B w_nF_n`, split it at a fixed endpoint
`K`, and apply Cauchy--Schwarz only to the tail:

\[
{\|S_B\|\over\sqrt{W_{M,B}}}
\le {\|S_K\|\over\sqrt{W_{M,B}}}
+\left(\sum_{n=K+1}^Bw_nP_n\right)^{1/2}.
\]

First let `B` tend to infinity and then `K` tend to infinity. Equations
(44.1)--(44.2) therefore yield

\[
\boxed{
Q_M=P_M-\lim_{B\to\infty}{1\over2W_{M,B}}
\sum_{m,n=M}^Bw_mw_n\|F_m-F_n\|^2.}            \tag{44.6}
\]

Thus terminal positivity is exactly the nonlocal physical dispersion bound

\[
\lim_{B\to\infty}{1\over2W_{M,B}}
\sum_{m,n=M}^Bw_mw_n\|F_m-F_n\|^2\le P_M.       \tag{44.7}
\]

## Audit and scope

The assumption (44.4) is not an innocuous technical hypothesis. Since the
weights have infinite total mass, it already forces `liminf P_n=0`, the
RH-sufficient target in this route. Hence (44.6) is a structural description
of the missing terminal arithmetic, not a proof of its existence or sign.
Positivity of the Gram matrix proves only that the dispersion is nonnegative;
it gives no comparison with `P_M`.

Finite complete-Gram data through endpoint `2048` certify both
`P_M-P_2048-sum_(n=M)^2047 w_nP_n>0` and the larger truncation
`P_M-sum_(n=M)^2047 w_nP_n>0` for every `2<=M<2048`. Neither statement bounds
the omitted infinite tail. Restricted and full norms must also remain distinct:
the full-space variance has an additional rank-one coefficient channel.

No tail estimate, terminal sign theorem, or RH result is claimed.
