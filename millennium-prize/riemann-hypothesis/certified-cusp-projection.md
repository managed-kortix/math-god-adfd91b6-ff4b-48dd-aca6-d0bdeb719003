# Certified one-sided cusp/projection bound

## Finite theorem

Let `0<w_1<...<w_N`, let `Q>0`, `alpha>0`, and put

\[
 f_i(t)=\frac{\sin(w_i t)}t,\qquad
 G_{ij}=\int_0^Q f_i(t)f_j(t)\,dt,
 \qquad K_{ij}=\frac\pi2\min(w_i,w_j)-G_{ij}.
\]

Partition `[0,Q]` into `M` intervals of length `h=Q/M`, and let `P` be the
orthogonal projection in `L^2(0,Q)` onto functions constant on each cell.  The
projected Gram matrix is

\[
 (G_0)_{ij}=\langle Pf_i,Pf_j\rangle,
 \qquad
 \overline f_{i,[a,b]}
 =\frac{\operatorname{Si}(w_i b)-\operatorname{Si}(w_i a)}h.
\]

Thus `E=G-G_0` is the Gram matrix of `(I-P)f_i` and is positive semidefinite.
For rational vectors `u,d`, set `z=d-u/alpha` and

\[
 \mathcal L_A=2u^TAd-\alpha d^TAd.
\]

Completing the square in the positive semidefinite form gives

\[
 \mathcal L_E=\alpha^{-1}u^TEu-\alpha z^TEz,
\]

and consequently the certified one-sided inequality

\[
 \boxed{\mathcal L_K\le
 \mathcal L_{\pi\min/2}-\mathcal L_{G_0}
 +\alpha z^TEz.}
\tag{1}
\]

The omitted `u^TEu/alpha` has the favorable sign.  It is not replaced by an
absolute entrywise error.

## Poincare certificate

For `F_z=sum_i z_i f_i`, the sharp mean-zero Neumann Poincare inequality on
each cell yields

\[
 z^TEz=\|(I-P)F_z\|_2^2
 \le \frac{h^2}{\pi^2}\|F_z'\|_2^2.
\tag{2}
\]

Define the frequency suffix profile

\[
A_z(s)=\sum_{w_i\ge s}z_i.
\]

Since `sin(wt)/t=int_0^w cos(st) ds`, the combined derivative satisfies

\[
F_z'(t)=-\int_0^{w_N}sA_z(s)\sin(st)\,ds.
\]

The implementation therefore uses the cancellation-aware certificate

\[
 \|F_z'\|_2^2\le
 Q\left(\int_0^{w_N}s|A_z(s)|\,ds\right)^2.
\tag{3}
\]

For rational sorted frequencies this integral is an exact rational suffix sum.
It is never larger than `sum_i |z_i|w_i^2/2`.

This estimate is rigorous at the origin.  Indeed,

\[
 f_w'(t)=\frac{wt\cos(wt)-\sin(wt)}{t^2},
 \qquad
 x\cos x-\sin x=-\int_0^x s\sin s\,ds,
\]

so `|f_w'(t)|<=w^2/2` for `t>0`, continuously extending to `f_w'(0)=0`.
No division by a small interval or point sampling near zero is used.  Arb
evaluates the first cell mean as `Si(w h)/h`, with `Si(0)=0` exactly.

## Exact cusp evaluation

For sorted frequencies, define suffixes `X_k=sum_{i>=k}x_i` and
`Y_k=sum_{i>=k}y_i`, with `w_0=0`.  Then

\[
 x^T(\min(w_i,w_j))y
 =\sum_{k=1}^N(w_k-w_{k-1})X_kY_k.
\tag{4}
\]

All quantities in (4) are exact rationals.  Hence the cusp costs `O(N)` after
sorting, while forming the `M` projected means and forms costs `O(MN)` and
stores `O(MN)` Arb balls in this prototype.

## Scope

`verify_cusp_projection.py` certifies a supplied finite rational-frequency,
two-channel realization and compares (1) with an independent dense Arb
endpoint `Si` evaluation of `K_Q`.  It does not certify an omitted frequency tail,
the harmonic aggregation leading to a finite vector, an endpoint decrement,
or RH. Bound (3) preserves suffix cancellation but can still be loose because
it discards oscillation in `t`; cellwise derivative Gram bounds or higher-order
projections are natural refinements. A hostile pair whose coefficients grow as
the inverse frequency gap shows that narrow bandwidth and zero total mass alone
do not force the suffix profile small. Piecewise constants can still require a
cell count proportional to time times carrier frequency.
