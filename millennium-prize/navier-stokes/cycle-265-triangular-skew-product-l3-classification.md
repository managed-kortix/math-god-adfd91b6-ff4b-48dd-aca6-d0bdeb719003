# Cycle 265: exact triangular skew-product Euler classification

## Verdict

The smooth periodic triangular architecture

\[
 \eta_t(a,z)=(\Phi_t(a),z+t w_0(a)),\qquad a\in\mathbb T^2,
 \tag{265.1}
\]

where `Phi_t` is the flow of a steady two-dimensional Euler field `v`, gives
exact three-dimensional Euler solutions

\[
 u(t,x,z)=(v(x),w_0(\Phi_{-t}x)).                       \tag{265.2}
\]

This class can have genuinely time-dependent velocity `L^3`. It nevertheless
has the universal two-time cap

\[
 {\|u(t)\|_3\over\|u(s)\|_3}\le 2^{1/6}=1.122462\ldots<2. \tag{265.3}
\]

Consequently there is no factor-two example in this architecture. The sharper
answer for specified component norms and endpoint correlations is the exact
formula (265.11) below. The cap is optimal from those data alone, but equality
is not claimed to be dynamically attainable by a smooth steady Euler carrier.

## Classification of the skew-product class

Use product Haar measure on `T^3=T^2 x T`; normalization is immaterial to all
ratios. Let `v` be a smooth periodic divergence-free field satisfying

\[
 v\mathbin\cdot\nabla v=-\nabla p,
 \tag{265.4}
\]

and let `Phi_t` be its area-preserving flow. For arbitrary smooth periodic
`w_0`, set `w(t)=w_0 o Phi_{-t}`. Then

\[
 \partial_t w+v\mathbin\cdot\nabla w=0.
\]

The field (265.2) is divergence free, its first two momentum equations are
(265.4), and its third is the displayed transport equation. It is therefore an
exact smooth periodic 3D Euler solution with pressure `p(x)`. Conversely, every
`z`-independent 2D3C Euler solution with a time-independent horizontal
component has this form. Thus (265.1)--(265.2) classify exactly the stationary-
base triangular, or skew-product, architecture; they do not classify general
3D Euler solutions or time-dependent 2D3C carriers.

Pure parallel shears lie in a degenerate subfamily. Write

\[
 X(x)=|v(x)|,\qquad D(x)=v(x)\mathbin\cdot\nabla X(x)^2.
\]

For

\[
 F(t)=\|u(t)\|_3^3=\int_{\mathbb T^2}(X^2+w(t)^2)^{3/2},
\]

transport and integration by parts give the exact identity

\[
 F'(t)={3\over2}\int_{\mathbb T^2}
       (X^2+w(t)^2)^{1/2}D.                              \tag{265.5}
\]

It follows that:

1. if `D=0`, speed is constant along every base trajectory and `F(t)` is
   constant for every passive component `w_0`; this includes every parallel
   shear and every rigid/isometric carrier;
2. if `D` is not identically zero, there is a smooth passive component for
   which `F'(0)` is nonzero, so velocity `L^3` genuinely varies.

For the second assertion choose `K>0` and nonzero `epsilon` small enough that
`K^2+epsilon D>0`, and put

\[
 w_0=(K^2+\varepsilon D)^{1/2}.                          \tag{265.6}
\]

Because `v` is divergence free,

\[
 \int D\sqrt{X^2+K^2}
 =\int v\mathbin\cdot\nabla G(X^2)=0
\]

for a smooth primitive `G`. Moreover

\[
 {d\over d\varepsilon}\int D\sqrt{X^2+K^2+\varepsilon D}
 ={1\over2}\int {D^2\over\sqrt{X^2+K^2+\varepsilon D}}>0. \tag{265.7}
\]

Hence (265.5) is positive at time zero when `epsilon>0`. This proves both
directions of the universal-constancy classification without a perturbative
PDE argument.

## A concrete variable-`L3` solution

On the standard square torus take

\[
 v(x,y)=(\sin y,-\sin x),\qquad p(x,y)=-\cos x\cos y.    \tag{265.8}
\]

Direct differentiation gives `v dot grad v=-grad p`. Its trajectories are the
integrable Hamiltonian curves of `cos x+cos y`, and

\[
 X^2=\sin^2x+\sin^2y,
 \quad D=2\sin x\sin y(\cos x-\cos y),                  \tag{265.9}
\]

which is not identically zero. Choose, for example, `K=2` and
`0<epsilon<1`; since `|D|<=2`, (265.6) is smooth and positive. Equations
(265.2), (265.6), and (265.8) are then a completely specified global smooth
periodic 3D Euler solution, and (265.7) proves
`d ||u(t)||_3^3/dt|_(t=0)>0`. The solution is not merely translated or rotated:
its complete velocity `L^3` changes with time.

The base flow may alternatively be written with Jacobi elliptic functions on
each regular energy curve, but that parametrization adds no verification value;
the autonomous analytic flow `Phi_t` in (265.2) uniquely and globally specifies
the solution.

## Exact correlation formula and optimal norm-only cap

Set

\[
 A=\|v\|_3,\qquad B=\|w_0\|_3,
\]

and define the nonnegative overlap correlation

\[
 C_r=\int\left[(X^2+w(r)^2)^{3/2}-X^3-|w(r)|^3\right]. \tag{265.10}
\]

Area preservation fixes `A` and `B`. Therefore the exact two-time answer is

\[
 {\|u(t)\|_3\over\|u(s)\|_3}
 =\left({A^3+B^3+C_t\over A^3+B^3+C_s}\right)^{1/3}.   \tag{265.11}
\]

This isolates the only mechanism: transport changes the spatial correlation
between base speed and passive-component magnitude. Pointwise superadditivity
and Minkowski in `L^(3/2)` give

\[
 0\le C_r\le (A^2+B^2)^{3/2}-A^3-B^3.                  \tag{265.12}
\]

Thus, if only the component norms are known,

\[
 R(A,B)\le {\sqrt{A^2+B^2}\over(A^3+B^3)^{1/3}}.       \tag{265.13}
\]

For `A,B>0`, put `q=B/A`. The sixth power of the right side is

\[
 h(q)={(1+q^2)^3\over(1+q^3)^2}.
\]

Its logarithmic derivative is

\[
 {h'(q)\over h(q)}={6q(1-q)\over(1+q^2)(1+q^3)}.
\]

Hence the unique interior maximum is `q=1`, where `h(1)=2`; the endpoint
limits are one. This proves (265.3), including the optimal constant based only
on `A,B`.

On a probability space the measurable configurations

\[
 X=1_E,\quad |w(s)|=1_{E^c},\quad |w(t)|=1_E,
 \qquad |E|=1/2,
\]

saturate all algebraic inequalities and attain `2^(1/6)`. Smooth approximation
shows that separate norms plus equimeasurability cannot imply a smaller
constant. These configurations are not asserted to be endpoints of one smooth
steady-carrier orbit, so the optimal dynamical constant may be lower.

## Scope

The result closes factor two only for the triangular skew-product class
(265.1), equivalently stationary-base 2D3C Euler. A time-dependent horizontal
2D Euler carrier introduces its own varying `L^3` norm and is outside the cap.
Likewise, genuinely `z`-dependent horizontal velocity and nontriangular 3D
coupling are outside the classification. No Navier--Stokes regularity or
Millennium result is claimed.
