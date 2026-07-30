# Cycle 126: isotropic flow does not preserve reflection positivity

Fixed positive four-dimensional heat-flow time cannot in general be treated as
an Osterwalder--Schrader-positive local observable map.  The obstruction is
already exact for one free massive scalar channel.

Fix spatial momentum, write its positive energy as `w`, and heat-flow both
fields for time `t>0`.  The Euclidean-energy covariance is

\[
C_t(p_0)=\frac{e^{-2tp_0^2}}{p_0^2+w^2}.
\]

Its Euclidean-time kernel is

\[
K_t(\tau)=\int_{\mathbb R}\frac{dp_0}{2\pi}
 e^{ip_0\tau}C_t(p_0)
=g_t*h_w(\tau),
\]

where

\[
g_t(\tau)=\frac{e^{-\tau^2/(8t)}}{\sqrt{8\pi t}},
\qquad
h_w(\tau)=\frac{e^{-w|\tau|}}{2w}.
\]

Equivalently,

\[
K_t(\tau)=\frac{e^{2tw^2}}{4w}\left[
e^{-w|\tau|}\operatorname{erfc}
 \left(\frac{4tw-|\tau|}{\sqrt{8t}}\right)
+e^{w|\tau|}\operatorname{erfc}
 \left(\frac{4tw+|\tau|}{\sqrt{8t}}\right)
\right].
\]

Both `g_t` and `h_w` are log-concave, and convolution preserves
log-concavity.  Gaussian convolution makes `K_t` positive and real analytic.
Its log-concavity is strict: equality at two distinct points would make
`log K_t` affine on an interval and hence, by analyticity, everywhere; this is
impossible because `K_t` is even, nonconstant, and tends to zero.

For any distinct positive times `s_1,s_2`, strict log-concavity gives

\[
K_t(s_1+s_2)^2>K_t(2s_1)K_t(2s_2).
\]

Therefore the two-point reflection Hankel matrix

\[
H=\begin{pmatrix}
K_t(2s_1)&K_t(s_1+s_2)\\
K_t(s_1+s_2)&K_t(2s_2)
\end{pmatrix}
\]

has `det H<0`.  For example, the rational parameters

\[
t=w=1,\qquad s_1=1/2,\qquad s_2=1
\]

give the explicit certificate

\[
K_1(1)K_1(2)-K_1(3/2)^2<0.
\]

The same obstruction follows spectrally: a nonzero reflection-positive
translation-invariant scalar covariance is a positive Stieltjes transform in
`p_0^2`, and hence cannot be `o(p_0^{-2})`; the flowed covariance is
exponentially suppressed.

## Exact scope

This proves failure for linear isotropic heat smearing and for any nonzero
flowed channel for which sufficiently rapid Euclidean-energy decay is proved.
It does **not** prove that exact nonlinear Yang--Mills gradient-flow composites
have this decay nonperturbatively, nor that the underlying zero-flow-time gauge
theory loses reflection positivity.

A structurally viable replacement is half-space flow: evolve positive-time
variables using gauge-compatible boundary conditions, reflect the construction
on the negative half, and only then take shrinking flow time.  At the free
level the Dirichlet/Neumann image-kernel defect for points distance `delta` from
the reflection plane is exponentially small, of order
`exp(-delta^2/(4t))`.  Nonlinear uniform bounds and the local shrinking-flow
limit remain open.

No Yang--Mills or Millennium solution is claimed.
