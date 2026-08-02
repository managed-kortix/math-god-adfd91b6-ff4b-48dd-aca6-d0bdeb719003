# Cycle 267: finite-dimensional genuine-3D Euler no-go

## Verdict

There is no nonstationary genuinely three-dimensional real Euler solution on
`T^3` whose Fourier support remains in one finite set. More sharply, after the
constant mean is removed, every finite-mode solution is stationary; if its
support spans three dimensions, it is Beltrami. Thus no linear Fourier
subspace, finite Fourier Lie algebra, coefficient-dependent algebraic variety,
or other invariant family contained in a fixed finite trigonometric ambient
space can have nonconstant velocity `L^3` beyond a Galilean translate, whose
`L^3` is also constant.

Affine velocity fields do not open a periodic loophole. The exact linked-shear
family previously found is nonstationary and can have variable `L^3`, but its
Fourier support is planar and its two-time ratio is at most
`2^(1/6) < 2`. Consequently the requested combination

1. finite-dimensional closure in fixed Fourier/Lie coordinates,
2. genuinely three-dimensional support,
3. nonconstant velocity `L^3`, and
4. nonstationary/non-Beltrami dynamics

is impossible. This does not exclude a finite-parameter nonlinear manifold
whose elements have genuinely infinite Fourier support.

## 1. Normalization and genuine three-dimensionality

Use normalized Haar measure on `T^3=(R/2 pi Z)^3` and write

\[
 u(t,x)=U+\sum_{k\in S}u_k(t)e^{ik\cdot x},
 \qquad k\cdot u_k=0,\quad u_{-k}=\overline{u_k},          \tag{267.1}
\]

where `S` is finite and `U` is the conserved mean. Call the support genuinely
three-dimensional when its real linear span is `R^3`. This is weaker than the
Cycle 265 production test, which additionally asks for nonzero vortex
stretching, so a no-go under this definition also closes the stronger one.

The Galilean change

\[
 v(t,x)=u(t,x+tU)-U                                      \tag{267.2}
\]

is mean zero and has the same fixed finite support.

## 2. Exact fixed-support theorem

Kishimoto and Yoneda's classification theorem applies to real finite-mode
Euler solutions with frequencies in `R^3`, hence in particular to toral
lattice frequencies. It says that every mean-zero such solution is independent
of time. Their three-dimensional branch is even more rigid:

\[
 \operatorname{span}_{\mathbb R} S=\mathbb R^3
 \quad\Longrightarrow\quad
 \nabla\times v=\lambda v
 \quad\hbox{for one }\lambda\ne0.                        \tag{267.3}
\]

Thus `v=v_0` is a stationary Beltrami field. Inverting (267.2) gives

\[
 u(t,x)=U+v_0(x-tU).                                    \tag{267.4}
\]

A change of variables now proves, for every `1 <= p <= infinity`,

\[
 \|u(t)\|_{L^p}=\|U+v_0\|_{L^p}.                        \tag{267.5}
\]

In particular, retaining the mean does not produce velocity-`L^3` dynamics.
When the support is planar, the complete classification consists of stationary
two-dimensional-like fields; these include special 2D3C fields but still give
no time dependence after (267.2).

Reference: N. Kishimoto and T. Yoneda, *Characterization of
three-dimensional Euler flows supported on finitely many Fourier modes*,
Journal of Mathematical Fluid Mechanics 24 (2022), DOI
`10.1007/s00021-022-00703-5`, arXiv `2110.08039`, especially Theorem 1.4
and Theorem 4.1.

## 3. Consequence for finite-dimensional Fourier and Lie families

Let `M` be any finite-dimensional invariant set of real Euler fields contained
in a fixed finite trigonometric space

\[
 E_S=\left\{U+\sum_{k\in S}a_ke^{ik\cdot x}:
 k\cdot a_k=0,\ a_{-k}=\overline{a_k}\right\}.          \tag{267.6}
\]

No regularity, linearity, or algebraicity of `M` is needed. Every local Euler
orbit through every point of `M` remains in `E_S`; Section 2 applies pointwise
to that orbit. After fixing the conserved mean, the Euler vector field
therefore vanishes on `M`. With varying means, its only motion is the Galilean
translation (267.4), which preserves every velocity `L^p` norm.

This subsumes all of the following fixed-support proposals:

- a finite-dimensional Fourier subspace closed under the Euler quadratic map;
- a finite-dimensional Lie algebra of trigonometric divergence-free fields
  whose coefficient family is Euler invariant;
- a nonlinear coefficient variety on which exterior Fourier production
  cancels;
- a finite union or singular stratum of such sets.

The conclusion follows orbit by orbit, so exceptional coefficient
cancellations do not evade it. Galerkin and Zeitlin systems can be
nonstationary only because they project, identify, or wrap the exterior modes;
they are not exact classical Euler restrictions.

## 4. Why affine-in-space closure is unavailable on the torus

Suppose an affine field on the universal cover,

\[
 \widetilde u(t,x)=A(t)x+b(t),                           \tag{267.7}
\]

descends to a vector field on `R^3/(2 pi Z)^3`. Periodicity requires

\[
 A(t)(x+2\pi n)+b(t)=A(t)x+b(t)
 \quad\hbox{for every }n\in\mathbb Z^3.
\]

Hence `A(t)n=0` for the three coordinate vectors and `A(t)=0`. The only
periodic affine fields are spatial constants. They solve Euler with constant
velocity and constant `L^3`. Matrix-Riccati affine Euler families on `R^3`
therefore have no nontrivial toral realization.

## 5. Linked shear: exact family, planar obstruction, and cap

There is an exact smooth periodic skew-product family

\[
 u(t,x,z)=\bigl(v(x),w_0(\Phi_{-t}x)\bigr),              \tag{267.8}
\]

where `x in T^2`, `v` is a steady 2D Euler field, and `Phi_t` is its
area-preserving flow. It has pressure equal to the pressure of `v`. Its cubic
velocity norm satisfies

\[
 {d\over dt}\|u(t)\|_3^3
 ={3\over2}\int_{\mathbb T^2}
 (|v|^2+w(t)^2)^{1/2}\,v\cdot\nabla |v|^2.              \tag{267.9}
\]

Therefore this family can have nonconstant `L^3`; the concrete carrier
`v=(sin y,-sin x)` and
`w_0=(4+epsilon v dot grad |v|^2)^(1/2)` gives a strict initial increase.
However, every Fourier mode in (267.8) has zero third frequency. Its support is
contained in a plane under every time evolution, so it is not genuinely 3D in
the support-span or Cycle 265 senses.

If `A=||v||_3` and `B=||w_0||_3`, scalar transport and Minkowski give, at any
two times,

\[
 {\|u(t)\|_3\over\|u(s)\|_3}
 \le {\sqrt{A^2+B^2}\over(A^3+B^3)^{1/3}}
 \le 2^{1/6}.                                          \tag{267.10}
\]

The last constant is sharp from the separate component norms alone, although
smooth dynamical sharpness is not asserted. Thus linked shear supplies the
desired variable norm only by surrendering genuine three-dimensionality, and
it cannot approach the factor-two Navier target.

Within this stationary-base triangular class, parallel shears do not improve
the mechanism. When the carrier speed is constant along its own trajectories,
`v dot grad |v|^2=0`, (267.9) vanishes for every passive datum. Nonconstant
`L^3` requires correlation rearrangement by a non-isometric planar carrier,
which remains inside (267.8) and (267.10).

## 6. Exact frontier

The no-go is sharp with respect to its hypotheses. It proves neither that all
finite-dimensional invariant manifolds of smooth Euler are stationary nor
that no genuinely 3D variable-`L^3` orbit exists. Indeed, without a structural
restriction, the time translates of any complete nonstationary orbit already
form a one-parameter invariant set. A meaningful surviving proposal must
therefore specify a nonlinear finite-parameter parametrization whose members
have infinite Fourier support and whose Euler evolution closes exactly on the
parameters. It must also verify support spanning `R^3`, nonzero stretching,
and nonconstant complete velocity `L^3` directly.

No such family is produced here. The rigorous output is the fixed-Fourier/Lie
no-go, the periodic-affine no-go, and the planar linked-shear cap. No
Navier--Stokes regularity or Millennium result is claimed.
