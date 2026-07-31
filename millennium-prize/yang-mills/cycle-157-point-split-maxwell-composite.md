# Cycle 157: the point-split Maxwell composite is OS-positive on a collar

Fix spatial heat smoothing `h_sigma(k)=exp(-sigma|k|^2)` and define, for
`t>=delta` and `0<epsilon<2delta`,

\[
\mathcal E_\epsilon(t,x)=\frac12:E_\sigma(t-\epsilon/2,x)\cdot
E_\sigma(t+\epsilon/2,x):.
\]

Both endpoints remain in the positive-time algebra. Modulo time-zero contact
terms, the reflected elementary electric kernel is

\[
R_{\sigma,ij}(u,z)=\int\frac{d^3k}{(2\pi)^3}e^{-2\sigma|k|^2}
\frac{|k|}{2}P_{ij}(k)e^{-|k|u+ik\cdot z}.
\]

Wick contraction gives

\[
K_{\sigma,\epsilon}=\frac14\sum_{i,j}
\left[R_{ij}(t+s-\epsilon)R_{ij}(t+s+\epsilon)+R_{ij}(t+s)^2\right].
\]

Since `t+s-epsilon>0`, no reflection-plane contact distribution occurs. The
limit is smooth and dominated on the collar:

\[
\boxed{K_{\sigma,0}(t,s;z)=\frac12\sum_{i,j}R_{\sigma,ij}(t+s,z)^2.}
\]

In external momentum `p`, with `r=|k|`, `q=|p-k|`, its two-photon density is

\[
\rho_{\sigma}(\omega,p)=\frac18\int\frac{d^3k}{(2\pi)^3}rq
e^{-2\sigma(r^2+q^2)}
\left[1+(\hat k\cdot\widehat{p-k})^2\right]
\delta(\omega-r-q).
\]

Every factor is nonnegative. Therefore the limiting OS form is positive. At
zero constituent smoothing, angular integration yields

\[
\boxed{
\rho_0(\omega,p)=
\frac{15\omega^4-30\omega^2|p|^2+23|p|^4}{3840\pi^2}
\mathbf1_{\omega\ge|p|}
}
\]

for the `1/2:E^2:` normalization used here. Overall constants vary with field
and Fourier conventions; the polynomial coefficients do not. Positivity is
strict because

\[
15-30x+23x^2=23(x-15/23)^2+120/23>0.
\]

Fixed positive spatial smoothing inserts an internal momentum weight, so the
full density is positive but no longer merely this polynomial times an external
multiplier. It has Gaussian spectral decay and finite moments of all orders.

This proves that reflection positivity is not the obstruction for the
legitimate fixed-regulator composite on tests separated from the reflection
plane. The obstruction is existence of the local composite. The Euclidean
electric covariance contains a temporal contact term; naively sampling and
centering the square on a temporal lattice aliases its square into every fixed
external frequency. Point splitting and normal ordering on the collar control
the reflected noncontact sector but do not define all same-side Schwinger
distributions when the split is removed.

The next construction-grade gate is interacting and shrinking-resolution:
construct a gauge-invariant renormalized composite with spatial resolution
`rho(a)->0` and prove a cutoff- and volume-uniform local negative-Sobolev bound,
together with a noncollapse variance. Fixed `sigma>0` only gives a nonlocal
observable and does not construct local four-dimensional Yang--Mills. A mass
gap would additionally require contraction on the complete physical vacuum
complement, not one composite channel.

This is a free-theory OS admissibility theorem, not an interacting construction
or mass-gap result.
