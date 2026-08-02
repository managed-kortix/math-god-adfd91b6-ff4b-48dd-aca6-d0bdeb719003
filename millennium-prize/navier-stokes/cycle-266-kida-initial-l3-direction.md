# Cycle 266: exact initial velocity-L3 derivative at Kida--Pelz

## Candidate decision

Use the deterministic Cycle 265 coefficient choice

\[
 u_* = K-{1\over32}F(K),\qquad F(u)=-\mathbb P((u\cdot\nabla)u).
 \tag{266.1}
\]

Thus the old coordinates are exactly `a=-2`, `b=0`, and
`theta=(0,0,0)`, which is profile index `16` in the already generated
`C266-3DDE1` exact-family ordering. No phase search, random start, or
coefficient optimization is used. Since that 132-profile manifest has already
been frozen and stopped at resource preflight, this note does not alter or
reopen it; the singleton is a recommendation for a later separately named
screen. This is not an Euler amplification certificate.

## Exact first derivative

On normalized `T^3`, set

\[
 C(u)=\int |u|^3,\qquad G(u)=\left.{d\over dt}C(u(t))\right|_{t=0}.
\]

For every smooth divergence-free datum,

\[
 \boxed{G(u)=3\int |u|u\cdot F(u)}.                    \tag{266.2}
\]

The advective contribution vanishes by periodic integration, so equivalently

\[
 G(u)=3\int p\,\operatorname {div}(|u|u),\qquad
 -\Delta p=\partial_i u_j\partial_j u_i.               \tag{266.3}
\]

This is the exact initial derivative of the cubed velocity `L3` norm. The norm
and logarithmic derivatives are

\[
 {d\over dt}\|u\|_3={G(u)\over3C(u)^{2/3}},\qquad
 {d\over dt}\log\|u\|_3={G(u)\over3C(u)}.              \tag{266.4}
\]

For a divergence-free variation `h`, write

\[
 L_u h=DF(u)h=-\mathbb P((h\cdot\nabla)u+(u\cdot\nabla)h).
\]

Direct differentiation, with the quotient assigned value zero where `u=0`,
gives the exact directional gradient

\[
 DG(u)[h]=3\int\left[
 |u|h\cdot F(u)+{(u\cdot h)(u\cdot F(u))\over|u|}
 +|u|u\cdot L_u h\right].                              \tag{266.5}
\]

If `q=P(|u|u)`, its divergence-free `L2` gradient is

\[
 \nabla G=3\mathbb P\left(
 |u|F+{u\cdot F\over|u|}u
 +(u\cdot\nabla)q-(\nabla u)^Tq\right).               \tag{266.6}
\]

Equation (266.5), not finite differencing, is used in the replay.

## Energy, helicity, and scale constraint

Take

\[
 E={1\over2}\int|u|^2,\quad H=\int u\cdot\omega,
 \quad Z={1\over2}\int|\omega|^2.                     \tag{266.7}
\]

Here `Z` is an enstrophy-like scale constraint, not a 3D Euler invariant. Its
only role is to prevent a coefficient step from escaping to higher frequency.
The three `L2` normals are

\[
 n_E=u,\qquad n_H=2\omega,\qquad n_Z=\nabla\times\omega=-\Delta u. \tag{266.8}
\]

For `g=nabla G`, form the Gram matrix
`M_ij=<n_i,n_j>` and `r_i=<n_i,g>`. The constrained gradient is exactly

\[
 g_T=g-\sum_i\lambda_i n_i,\qquad M\lambda=r,          \tag{266.9}
\]

using a pseudoinverse only if the constraint normals are dependent. If the
scale is imposed as `S=Z/E` rather than fixing both `E` and `Z`, replace `n_Z`
by `(E n_Z-Z n_E)/E^2`. Helicity may similarly be made dimensionless before
projection; the Gram construction is unchanged.

## Why the Kida direction is directed

The unperturbed Kida--Pelz field has `G(K)=0` by symmetry. In contrast to the
Taylor--Green/ABC scout, its Euler tangent itself resolves the sign. Exact
Fourier convolution shows

\[
 DE(K)[-F(K)]=DH(K)[-F(K)]=DZ(K)[-F(K)]=0.             \tag{266.10}
\]

The first two equalities hold for every Euler tangent; the third is special to
this Kida--Pelz symmetry point. Therefore `-F(K)` is already tangent to all
three constraint surfaces, without a numerical projection. Formula (266.5)
gives

\[
 DG(K)[-F(K)]\mathrel{\mathop\approx}1.12684>0.         \tag{266.11}
\]

Consequently the negative tangent sign is selected before any trajectory is
viewed. For the exact rational Fourier candidate (266.1), the deterministic
replay gives

\[
 G(u_*)\mathrel{\mathop\approx}0.0356418>0,
 \qquad {d\over dt}\log\|u_*\|_3\big|_0
 \mathrel{\mathop\approx}0.01313.                      \tag{266.12}
\]

All coefficients of `F(K)` are Gaussian rationals because `K` has rational
trigonometric coefficients and the Leray matrices are rational. Equation
(266.1) is therefore an exact coefficient specification; decimal fitting is
not involved. These corrected values retain the complete support through the
first Euler time derivative. The earlier `0.0351456` replay used cutoff 8 and
inadvertently projected modes 9 through 12 from `F(u_*)`.

## Disposition

Promote only `K-F(K)/32` as the first `C266-KP1` profile. The weaker exact
choice `K-F(K)/64` has the same sign but is not needed. Do not add doubled
packets or phase variants before the trajectory manifest is frozen. Positive
initial growth is a local diagnostic only: it neither supplies persistence to
`log 2` nor certifies a full Euler or Navier--Stokes trajectory.

Reproduce the deterministic calculation with

```bash
uv run --with numpy python cycle266_kida_direction.py
uv run --with numpy python -m unittest -q test_cycle266_kida_direction.py
```
