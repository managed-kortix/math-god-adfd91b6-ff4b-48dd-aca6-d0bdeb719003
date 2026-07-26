# Certified one-sided cusp/projection bound

## Finite theorem

Let `0<w_1<...<w_N`, let `Q>0`, `alpha>0`, and put

\[
 f_i(t)=\frac{\sin(w_i t)}t,\qquad
 G_{ij}=\int_0^Q f_i(t)f_j(t)\,dt,
 \qquad K_{ij}=\frac\pi2\min(w_i,w_j)-G_{ij}.
\]

Partition `[0,Q]` into `M` intervals of length `h=Q/M`. For `p=0,1,2,3`, let
`P_p` be the orthogonal projection in `L^2(0,Q)` onto polynomials of degree at
most `p` on each cell. With

\[
 L_{n,[a,b]}(t)=P_n\left(2(t-a)/h-1\right),\qquad
 \int_a^b L_nL_m={h\over 2n+1}\delta_{nm},
\]

the projected Gram matrix is

\[
 (G_p)_{ij}=\langle P_pf_i,P_pf_j\rangle
 =\sum_{[a,b]}\sum_{n=0}^p{2n+1\over h}m_{i,n}m_{j,n},
 \qquad
 m_{i,n}=\int_a^b f_i(t)L_{n,[a,b]}(t)\,dt.
\]

The moments through degree three are finite linear combinations of
`Si(wb)-Si(wa)` and sine/cosine endpoint terms obtained by integration by
parts. Arb evaluates these formulas with outward rounding. In the first cell,
`Si(0)=0`; no value of `sin(wt)/t` or division by `t` is used.

Thus `E_p=G-G_p` is the Gram matrix of `(I-P_p)f_i` and is positive
semidefinite.
For rational vectors `u,d`, set `z=d-u/alpha` and

\[
 \mathcal L_A=2u^TAd-\alpha d^TAd.
\]

Completing the square in the positive semidefinite form gives

\[
 \mathcal L_{E_p}=\alpha^{-1}u^TE_pu-\alpha z^TE_pz,
\]

and consequently the certified one-sided inequality

\[
 \boxed{\mathcal L_K\le
 \mathcal L_{\pi\min/2}-\mathcal L_{G_p}
 +\alpha z^TE_pz.}
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

## Higher-degree residual theorem

For `p=1,2,3`, put `r=p+1`. Since the best polynomial projection is no worse
than the Taylor polynomial of degree `r-1` about a cell midpoint, Taylor's
integral remainder gives

\[
 \|(I-P_p)F_z\|_2^2\le
 {Qh^{2r}\over (r!)^2 2^{2r}(2r+1)}B_r^2,
 \qquad
 B_r=\int_0^{w_N}s^r|A_z(s)|\,ds.
\tag{5}
\]

Indeed, `F_z(t)=int_0^{w_N} A_z(s) cos(st) ds`, so every derivative satisfies
`|F_z^(r)(t)|<=B_r`, including at the origin. For sorted rational frequencies
and rational channels, `B_r` is an exact rational suffix sum. For Arb endpoint
surrogates it is an outward-rounded Arb suffix sum. Formula (5) scales as
`h^(2p+2)`. Degree zero retains the sharper Neumann Poincare constant in (2).

The residual backend uses the weighted Legendre theorem

\[
\|(I-P_p)F\|_{L^2(I)}^2
\le \frac1{\Lambda_{p,m}}
\int_I[(t-a)(b-t)]^m|F^{(m)}(t)|^2\,dt,
\]

where `1<=m<=p+1` and

\[
\Lambda_{p,m}=\frac{(p+1+m)!}{(p+1-m)!}.
\]

The factorial ratio belongs in the denominator. On a cell of length `h`, using
the derivative supremum and integrating the weight exactly gives

\[
 \|(I-P_p)F\|_{L^2(I)}^2
 \le C_{p,m}h^{2m+1}\|F^{(m)}\|_\infty^2,
 \qquad
 C_{p,m}={m!^2(p+1-m)!\over(2m+1)!(p+1+m)!}.
\]

Indeed, the affine map contributes `h^(2m)` and
`int_0^1 x^m(1-x)^m dx=m!^2/(2m+1)!`. Summing uniform cells replaces the final
`h` by `Q`. The implementation computes these constants as exact `Fraction`s,
certifies every admissible `m`, and selects the candidate with the smallest Arb
upper endpoint. For `p=3,m=4`, the constant is `1/25401600`, improving the
midpoint-Taylor constant by the exact factor `1225/64`.

## Signed shadow-shell completion

The primary projection degree remains `p<=3`. An optional practical shadow
degree `r>=p` evaluates additional exact Legendre moments. Writing `S_(p,r)`
for the shell projection and `z=d-u/alpha`, its exact signed contribution is

\[
 \mathcal L_{S_{p,r}}
 ={1\over\alpha}\|S_{p,r}F_u\|_2^2
 -\alpha\|S_{p,r}F_z\|_2^2.
\]

Consequently the completed upper bound is

\[
 \mathcal L_K\le \mathcal L_{\pi\min/2}-\mathcal L_{G_p}
 -\mathcal L_{S_{p,r}}+\alpha\|(I-P_r)F_z\|_2^2.
\]

Both shell squares are accumulated separately from orthogonal Arb moments; no
sign is inferred from an interval difference. The final residual uses the
weighted theorem at degree `r`. The general three-term Legendre recurrence now
supports shadow degrees beyond three, while the advertised primary interface
remains restricted to degrees zero through three. Taking `r=p` recovers the
ordinary weighted certificate exactly.

At fixed total rank `R=M(p+1)`, the verifier compares all four degrees using
`M=R/(p+1)` and independently checks every one-sided upper bound against the
dense Arb `K_Q` form.

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

## Harmonic-first Mobius surrogate

`mobius_endpoint_surrogate.py` constructs the exact finite `N=4 -> 8`, `R=3`
surrogate. It applies the harmonic cutoff before reducing duplicate frequencies,
then converts each reduced `p/q` to angular frequency `2*pi*p/q`. The endpoint
parameter is exactly `alpha=1/3`. There are 18 raw nonzero source-harmonic modes
and 14 reduced active modes. All logarithms and amplitudes are Arb balls with
outward rounding.

## Scope

`verify_cusp_projection.py` certifies a supplied finite rational/Arb-frequency,
two-channel realization and compares (1) with an independent dense Arb
endpoint `Si` evaluation of `K_Q`. It does not certify an omitted frequency tail,
the harmonic aggregation leading to a finite vector, an endpoint decrement,
or RH. Bound (3) preserves suffix cancellation but can still be loose because
it discards oscillation in `t`; cellwise derivative Gram bounds or higher-order
projections reduce this loss but do not remove it. A hostile pair whose coefficients grow as
the inverse frequency gap shows that narrow bandwidth and zero total mass alone
do not force the suffix profile small. Piecewise constants can still require a
cell count proportional to time times carrier frequency.
