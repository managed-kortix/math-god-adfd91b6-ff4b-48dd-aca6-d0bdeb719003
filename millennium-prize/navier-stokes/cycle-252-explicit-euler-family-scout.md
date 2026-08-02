# Cycle 252: explicit finite-dimensional Euler-family scout

## Verdict

No exact factor-two velocity-`L^3` orbit is supplied by the standard explicit
finite-dimensional families. The exclusions have different strengths:

1. real solutions confined to a fixed finite Fourier support are stationary,
   after removal of the mean, by the Elgindi--Hu--Sverak rigidity theorem;
2. point vortices do not have finite velocity `L^3` or kinetic energy, while
   the usual regularizations either change the equation or cease to be exact
   finite-dimensional Euler families;
3. Kirchhoff ellipses, Stuart vortices, and smooth desingularized relative
   equilibria move only by isometries, so every velocity `L^p` norm is constant;
4. an exact smooth periodic 2.5D family with a steady two-dimensional carrier
   can vary its velocity `L^3`, but its ratio at any two times is at most
   `2^(1/6)`, far below two.

This is not a theorem that every finite-dimensional invariant submanifold of
smooth periodic Euler is stationary. No classification of such nonlinear
submanifolds is invoked or known here. Without a restriction on what counts as
an explicit family, the phrase is also too broad: the time translates of any
complete Euler orbit form a one-parameter invariant set. Thus a universal
finite-dimensional no-go would already decide the desired orbit rather than
reduce it.

## Exact target

For a smooth mean-zero periodic Euler solution, the required breaker is

\[
 \|u(T)\|_{L^3}>2\|u(0)\|_{L^3},
 \qquad \|u(T)\|_2=\|u(0)\|_2.                         \tag{252.1}
\]

The second identity is automatic energy conservation. It does not force the
first norm to be constant: on an infinite-dimensional fixed `L^2` sphere,
`L^3` has no universal upper/lower ratio. Each candidate must therefore be
tested for genuine shape dynamics rather than merely for energy conservation.

## Point vortices and regularized vortices

For a point vortex of circulation `Gamma`, the local velocity has magnitude

\[
 |u(x)|\sim {|\Gamma|\over 2\pi |x-a|}.
\]

Consequently

\[
 \int_{|x-a|<\epsilon}|u|^3\,dx
 \asymp \int_0^\epsilon r^{-2}\,dr=\infty,             \tag{252.2}
\]

and its kinetic energy also has the familiar logarithmic divergence. Toral
Green functions have the same local singularity. The finite-dimensional point
vortex Hamiltonian is therefore outside both norms in (252.1).

There are three common meanings of regularization, none of which gives the
requested object automatically.

- A vortex blob or mollified Biot--Savart kernel gives a useful convergent
  approximation but solves a regularized ODE/PDE, not the Euler equation.
- Euler-alpha and related models have exact particle formulations but are
  different equations.
- Replacing each point by a smooth radial Euler vortex does not preserve only
  its center and radius in a multi-vortex configuration. The nonuniform field
  of the other vortices strains the profile and generates contour/Fourier
  degrees of freedom. Known desingularizations of point-vortex equilibria are
  steady, rotating, or translating relative equilibria, and hence have
  constant `L^3`.

A vortex patch is an exact Euler object, but its vorticity is discontinuous and
general patch dynamics is infinite dimensional. Smoothing a patch boundary or
its vorticity destroys the exact Kirchhoff closure rather than producing a
smooth finite-dimensional replacement.

## Kirchhoff and related elliptic patches

The Kirchhoff ellipse in the plane preserves its semiaxes and rotates rigidly.
Writing its velocity in the form

\[
 u(t,x)=R(t)u(0,R(t)^{-1}x),                            \tag{252.3}
\]

orthogonality and change of variables give

\[
 \|u(t)\|_p=\|u(0)\|_p
\]

whenever the norm is finite. The family therefore has no `L^3` dynamics.
Moreover, a single nonzero-circulation planar patch has logarithmically
divergent total kinetic energy, and the sharp patch is not smooth vorticity.

Elliptical-vortex models in a prescribed strain can change aspect ratio, but
the strain is external. Kida-type closures and moment models are not closed
unforced periodic Euler solutions unless the alleged background is itself
included and all generated deformation modes are controlled. Corotating or
translating multi-patch solutions again are relative equilibria, so an
isometry preserves their velocity norms.

## Stuart vortices and steady coherent structures

Stuart cat's-eye vortices satisfy a semilinear steady relation

\[
 \omega=F(\psi),\qquad u=\nabla^\perp\psi,             \tag{252.4}
\]

in a stationary or uniformly translating frame. The classical family is
periodic in one direction on a cylinder rather than doubly periodic on the
fixed torus. Periodic analogues and other sinh--Poisson coherent structures
remain equilibria or relative equilibria. A toral translation obeys

\[
 u(t,x)=u_0(x-ct),
\]

so its complete `L^3` norm is constant. Varying the Stuart concentration
parameter compares different solutions, not two times on one energy-conserving
orbit, and cannot establish (252.1).

## Fourier and Lie-algebra closures

For toral Fourier characters, the vorticity bracket is

\[
 \{e^{ip\cdot x},e^{iq\cdot x}\}
 =-(p\wedge q)e^{i(p+q)\cdot x}.                       \tag{252.5}
\]

A finite set containing a noncollinear interacting pair cannot remain closed
under the resulting additions: iterating with one generator creates an
unbounded arithmetic progression unless a wedge product vanishes. At the Euler
vector-field level there is an additional equal-radius cancellation, but the
full real result is stronger: Elgindi--Hu--Sverak prove that a real toral Euler
solution supported in one fixed finite set on a time interval is stationary
after its constant mean is removed, with support on one origin-line or one
origin-circle. Therefore every exact real finite-Fourier invariant variety has
zero Euler vector field and constant `L^3`.

Zeitlin's `su(N)` sine-bracket systems and ordinary Galerkin triads are
finite-dimensional Hamiltonian approximations. Their brackets wrap or project
frequencies and are not invariant subalgebras of the classical toral Poisson
algebra. A factor-two trajectory in such a model would be candidate generation,
not an exact Euler orbit.

## A sharp 2.5D screen

Let

\[
 U(t,x,y,z)=(v_1(x,y),v_2(x,y),w(t,x,y))               \tag{252.6}
\]

be independent of `z`, where `v` is a steady smooth two-dimensional Euler
flow and

\[
 \partial_t w+v\cdot\nabla w=0.                       \tag{252.7}
\]

Then (252.6) is an exact smooth periodic 3D Euler solution. This includes the
explicit steady-shear transport families. The scalar transport preserves
`B=||w(t)||_3`, while `A=||v||_3` is fixed. Minkowski in `L^(3/2)` gives

\[
 \|U(t)\|_3^2
 =\bigl\||v|^2+|w(t)|^2\bigr\|_{3/2}
 \le A^2+B^2.                                         \tag{252.8}
\]

The pointwise inequality `(a^2+b^2)^(3/2)>=a^3+b^3` gives

\[
 \|U(s)\|_3^3\ge A^3+B^3.                             \tag{252.9}
\]

Hence, for every two times,

\[
 {\|U(t)\|_3\over\|U(s)\|_3}
 \le {\sqrt{A^2+B^2}\over(A^3+B^3)^{1/3}}
 \le 2^{1/6}<2.                                       \tag{252.10}
\]

The last inequality is sharp as an algebraic inequality and follows by
setting `r=B/A`, differentiating, or using symmetry and checking the unique
interior maximum `r=1`. This closes every steady-carrier/passive-third-component
proposal, even though the complete velocity `L^3` need not be constant.

For a time-dependent 2D carrier, the 2.5D equations are

\[
 \partial_t v+v\cdot\nabla v=-\nabla p,
 \qquad \partial_t w+v\cdot\nabla w=0.                 \tag{252.11}
\]

The estimate above then contains `A(t)=||v(t)||_3`; a factor-two mechanism must
already obtain substantial `L^3` variation from the two-dimensional Euler
carrier. Thus the passive component does not bypass the unresolved 2D gate.

## Disposition

| family | exact Euler | smooth periodic | finite norms | variable `L^3` | disposition |
|---|---:|---:|---:|---:|---|
| point vortices | yes, weak/singular | toral version yes | no | undefined | reject by (252.2) |
| blobs / Euler-alpha particles | no, for classical Euler | often | yes | possible | wrong equation |
| Kirchhoff ellipse | yes | planar patch | energy issue; nonsmooth vorticity | no | rigid relative equilibrium |
| Stuart / sinh--Poisson vortex | yes | classical Stuart is cylindrical | yes where posed | no | steady/translation |
| finite Fourier or Lie closure | only degenerate supports | yes | yes | no | rigidity theorem |
| Zeitlin / Galerkin closure | projected model | yes | yes | possible | not full Euler |
| steady-carrier 2.5D transport | yes | yes | yes | possible | ratio at most `2^(1/6)` |

The exact conclusion is therefore a family-by-family no-go, not a universal
smooth-periodic factor-two theorem. Any viable finite-parameter proposal must
exhibit non-isometric shape dynamics, remain an exact full Euler solution with
its generated infinite Fourier tail, and evade (252.10). At present none of the
standard named families does so, and no exact factor-two possibility is found.

## Sources

1. T. Elgindi, W. Hu, and V. Sverak, *On 2d Incompressible Euler Equations
   with Partial Damping*, Commun. Math. Phys. 355 (2017), 145--159,
   DOI `10.1007/s00220-017-2877-y`, especially Theorem 5.1.
2. G. R. Kirchhoff, *Vorlesungen uber mathematische Physik: Mechanik*
   (1876), for the uniformly rotating elliptic patch.
3. J. T. Stuart, *On finite amplitude oscillations in laminar mixing layers*,
   J. Fluid Mech. 29 (1967), 417--440, for the steady cat's-eye family.

No Navier--Stokes regularity result or Millennium solution is claimed.
