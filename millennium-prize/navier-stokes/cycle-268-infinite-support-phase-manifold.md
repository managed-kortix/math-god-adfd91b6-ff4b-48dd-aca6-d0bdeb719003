# Cycle 268: exact infinite-support phase manifold

## Verdict

Finite-mode rigidity does not extend to finite-parameter invariant sets in an
analytic function space. There is an explicit two-parameter invariant family
of global smooth periodic Euler fields whose initial members have genuinely
infinite Fourier support and whose velocity `L^3` varies along each nontrivial
orbit. The construction is triangular and has planar Fourier support, so the
previous `2^(1/6)` cap still prevents a factor-two crossing. It is an exact
escape from the fixed-support theorem, not a Navier--Stokes regularity result.

## The invariant family

Use normalized Haar measure on `T^3`. On `T^2` set

\[
 v(x,y)=(\sin y,-\sin x),\qquad
 p(x,y)=-\cos x\cos y,
 \tag{268.1}
\]

and let `Phi_t` be the global area-preserving flow of `v`. Define

\[
 X^2=|v|^2=\sin^2x+\sin^2y,
 \qquad
 D=v\mathbin\cdot\nabla X^2
   =2\sin x\sin y(\cos x-\cos y).
 \tag{268.2}
\]

For `0<epsilon<1`, put

\[
 w_\varepsilon=(4+\varepsilon D)^{1/2},
 \qquad
 u_{\varepsilon,\tau}(x,y,z)
 =\left(v(x,y),w_\varepsilon(\Phi_{-\tau}(x,y))\right).
 \tag{268.3}
\]

The bound `|D|<=2` makes the positive square root real analytic. Direct
differentiation gives `v dot grad v=-grad p`, while the last component obeys

\[
 \partial_\tau(w_\varepsilon\circ\Phi_{-\tau})
 +v\mathbin\cdot\nabla(w_\varepsilon\circ\Phi_{-\tau})=0.
 \tag{268.4}
\]

Thus (268.3) is a global analytic Euler solution with pressure (268.1).
Euler evolution acts on the finite-parameter set by

\[
 S_t u_{\varepsilon,\tau}=u_{\varepsilon,\tau+t}.
 \tag{268.5}
\]

Consequently the image of `(epsilon,tau) in (0,1) x R` is an exact
two-parameter invariant set. For each fixed `epsilon`, its `tau`-curve is an
exact one-dimensional orbit. This is a phase-function parametrization rather
than a finite Fourier truncation.

## Genuine infinite Fourier support

Every initial member `u_(epsilon,0)` has infinite Fourier support. It is enough
to prove this for its third component. If `w_epsilon` were a trigonometric
polynomial in `(x,y)`, its restriction at `y=pi/2` would be a trigonometric
polynomial `f(x)` satisfying

\[
 f(x)^2=4+\varepsilon\sin 2x.                            \tag{268.6}
\]

Write `z=e^(ix)`. Because `f` is real-valued, its Laurent support is symmetric.
The extreme exponents in (268.6) therefore force
`f=a z+b+c z^(-1)`. The absent exponents `z` and `z^(-1)`, together with the
nonzero extreme coefficients, force `b=0`. If

\[
 A={\varepsilon\over2i},
\]

coefficient comparison then gives `a^2=A`, `c^2=-A`, and `2ac=4`. Squaring the
last equality gives `4a^2c^2=16`, whereas the first two give
`4a^2c^2=epsilon^2`. This would require `epsilon=4`, contrary to
`0<epsilon<1`. Hence `w_epsilon`, and therefore `u_(epsilon,0)`, has infinitely
many nonzero Fourier coefficients. Analyticity gives exponential Fourier
decay; infinite support here is not a loss of regularity.

This pinpoints why finite-mode rigidity is inapplicable: two scalar parameters
describe the family, but no one finite trigonometric space contains it.

## Exact `L^3` variation

Let

\[
 F_\varepsilon(\tau)=\|u_{\varepsilon,\tau}\|_3^3.
\]

Transport and integration by parts give

\[
 F_\varepsilon'(0)
 ={3\over2}\int_{\mathbb T^2}
 D\sqrt{X^2+4+\varepsilon D}.                            \tag{268.7}
\]

At `epsilon=0` the integral vanishes because its integrand is
`v dot grad G(X^2)` for a smooth primitive `G`. Its derivative with respect to
`epsilon` is

\[
 {1\over2}\int_{\mathbb T^2}
 {D^2\over\sqrt{X^2+4+\varepsilon D}}>0.                 \tag{268.8}
\]

Since `D` is not identically zero, (268.7) is strictly positive for every
`0<epsilon<1`. Thus the complete velocity `L^3`, not merely a component or a
derivative norm, changes along every displayed orbit.

The mechanism is only changing overlap between the fixed horizontal speed
`X` and an equimeasurably transported vertical component. If
`A=||v||_3` and `B=||w_epsilon||_3`, the component-correlation argument from
Cycle 265 applies verbatim and yields, for any two times,

\[
 {\|u_{\varepsilon,t}\|_3\over\|u_{\varepsilon,s}\|_3}
 \le {\sqrt{A^2+B^2}\over(A^3+B^3)^{1/3}}
 \le 2^{1/6}<2.                                         \tag{268.9}
\]

Hence this family witnesses variability but cannot satisfy the factor-two
production gate.

## Generalized-Beltrami branch: a structural no-go

The most direct generalized-Beltrami ansatz cannot provide another moving
finite-parameter manifold. If a divergence-free periodic field satisfies

\[
 \operatorname{curl}u=\lambda(x)u,
\]

then `u cross curl u=0`, and the identity

\[
 (u\mathbin\cdot\nabla)u
 =\nabla(|u|^2/2)-u\mathbin\times\operatorname{curl}u
\]

shows that it is a steady Euler field with pressure `-|u|^2/2`. Equivalently,
the Leray projection of its nonlinearity vanishes. An Euler trajectory that
remains pointwise generalized Beltrami at every time therefore has
`partial_t u=0`, so every `L^p` is constant.
Allowing a spatially varying proportionality factor does not evade this
obstruction.

Clebsch variables alone impose no comparable restriction: they are a
representation of vorticity, not a finite-dimensional closure condition. A
useful Clebsch scout would still have to specify a finite-parameter class closed
under both material transport equations and reconstruct a periodic velocity.

## Scope

The positive example is `z`-independent and all of its Fourier frequencies lie
in the plane `k_3=0`. It therefore does not supply the genuinely three-
dimensional stretching sought by `ND251`, and viscosity does not preserve this
two-parameter set. The result closes the logical question left by Cycle 267:
nonlinear finite-parameter analytic invariant sets with infinite Fourier
support do exist and can vary velocity `L^3`. It does not produce a factor-two
Euler crossing, a Navier--Stokes counterexample, or a Millennium solution.
