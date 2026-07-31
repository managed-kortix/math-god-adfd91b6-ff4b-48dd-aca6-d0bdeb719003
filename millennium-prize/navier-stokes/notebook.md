# Notebook

## Cycle 175

The full off-circuit `cL-C` target has an exact conditional frame lemma.  If
`L-C_0` selected cross interactions have weighted norm at least `alpha`, their
sum frequencies have multiplicity at most `A`, colliding Leray vectors have
lower frame constant `1/A`, and the coherently summed unselected convolution
has `ell^2` norm at most `rho sqrt(L-C_0)`, then the complete output is at least
`(alpha/sqrt(A)-rho)^2(L-C_0)`.  Additive energy can provide distinct channels
but not polarized noncancellation.  The residual/completion bound remains the
unproved central assumption, so the lemma is not a regularity result.

Hostile audit showed that "unit designated critical throughput" is not an
invariant hypothesis until it is defined on real frequency orbits, coherently
sums collisions and conjugates, declares its dilation law, and is minimized
over polarization representation gauges and reciprocal-amplitude constraint
symmetries.  The exact real triad
`p=N e1`, `q=N e2`, with Cycle 150 polarizations and amplitudes
`A=(2N)^(-1/2)`, has unit symmetrized output norm and complete input
`H^(1/2)` energy exactly `4` for every `N`.  Reciprocal rescaling preserves the
output while changing the physical field and its energy by a factor
proportional to `r^2+r^-2`; it is a noncompact symmetry of the constraint, not
literally a coordinate gauge.  A raw chosen representative can therefore
manufacture energy growth.  Any surviving many-edge claim must concern the
constrained-minimum joint excess cost or invariant off-circuit output, not the
AM--GM normalization cost.

## Cycle 91

Helical decomposition does not make signed helicity coercive in the full
equation: nonlinear production creates equal positive and negative helicity
magnitudes.  An exact two-wave certificate at `(1,0,0)` and `(0,1,1)` produces
a nonzero negative-helicity mode at `(1,1,1)`.  The proposed shellwise
cumulative positive-excess estimate is finite for global smooth solutions and
implies global regularity, hence is an equivalent continuation reformulation.
Phase-blind spectra also admit phase twins with opposite stretching.  Route
retired; no Navier--Stokes result is claimed.

Bounded scout is queued to compute the exact initial derivative of the cubed
`L^3` norm for rational interacting triads and locate pressure-driven growth
candidates before any interval PDE validation.

## Bounded scout tick 2

For smooth divergence-free data,

`d/dt ||u||_3^3 = 3 int p u.grad|u| - 3 nu int |u|(|grad u|^2+|grad|u||^2)`.

Transport cancels exactly. For finite triad data, pressure has finite
frequencies, but `|u|u` generally has infinite Fourier support. Therefore a
Galerkin projection of `|u|u` back to the original triad does not compute the
exact derivative. The next test must rigorously integrate the unprojected
pointwise field at all pressure frequencies.

## Bounded scout cycle 36

The entire cyclic-shear family used in cycle 35 is degenerate, not merely the
single amplitude choice.  For

`u=(a sin z,b sin x,c sin y)`

on the periodic torus, `div u=0`, and the only nonzero entries of `grad u`
form a directed three-cycle.  There is no reverse pair, so

`sum_(i,j) (partial_i u_j)(partial_j u_i)=0`.

The pressure Poisson equation therefore gives `Delta p=0`; with mean-zero
normalization, `p=0` identically.  Its initial `L^3` derivative contains only
the nonpositive viscous term.  No amplitude choice within this ansatz can test
pressure-driven critical-norm growth, so the next search must include at least
one reverse derivative interaction.

## Bounded scout cycle 39

A reverse derivative interaction alone still does not produce pressure-driven
critical-norm growth.  On the periodic torus let

`u=(a sin y,b sin x,0)`.

Then `div u=0`,
`sum_(i,j) partial_i u_j partial_j u_i=2ab cos x cos y`, and the mean-zero
solution of `Delta p=-2ab cos x cos y` is `p=ab cos x cos y`.  Thus the pressure
is genuinely nonconstant.  However, writing
`|u|=(a^2 sin^2 y+b^2 sin^2 x)^(1/2)`, each term of
`p(a sin y partial_x|u|+b sin x partial_y|u|)` is odd in one coordinate, so its
torus integral is exactly zero.  The two-shear reverse-pair family is therefore
another decisive symmetry obstruction.

## Bounded scout cycle 41

Frequency and phase changes do not rescue the two-shear ansatz.  For

`u=(a sin(my+alpha),b sin(nx+beta),0)`

the mean-zero pressure is

`p=2abmn cos(my+alpha)cos(nx+beta)/(m^2+n^2)`.

In `int p u.grad|u|`, the first summand is odd in the phase-centered `x`
variable: its `x` dependence contains
`sin(nx+beta)cos(nx+beta)^2` divided by a function even in the sine.  The
second summand is likewise odd in the centered `y` variable.  Therefore the
pressure contribution is exactly zero for every pair of integer frequencies,
phases, and amplitudes.  A viable pressure-growth candidate must introduce a
genuinely nonseparable interaction rather than detune this family.

## Bounded scout cycle 42

The next exact ansatz outside that zero theorem is

`u_c=(a sin y+c sin(x+y),b sin x-c sin(x+y),0)`.

It is divergence-free, and direct solution of the pressure Poisson equation
gives

`p_c=ab cos x cos y+c[b cos y+b cos(2x+y)/5-a cos x-a cos(x+2y)/5]`.

The mixed pressure frequencies `(2,1),(1,2)` and the corresponding cross terms
in `|u_c|^2` destroy both coordinate-odd factorizations used for two shears.
This is a structural checkpoint, not a growth certificate: the exact signed
unprojected pressure integral and viscous comparison are next.

## Bounded scout cycle 43

The unprojected pressure integral has a genuinely signed first variation. On
`T^2=[0,2pi]^2`, let `I(c)=int p_c u_c.grad|u_c|`. Periodic integration by
parts, exact differentiation at `c=0`, parity, and one further integration by
parts give

\[
I'(0)={2ab\over5}\int_{\mathbb T^2}
\sqrt{a^2\sin^2y+b^2\sin^2x}\,(\sin^2y-\sin^2x)\,dx\,dy.
\]

Symmetrizing under `x<->y` yields

\[
I'(0)={ab(a^2-b^2)\over5}\int_{\mathbb T^2}
{(\sin^2y-\sin^2x)^2\over
\sqrt{a^2\sin^2y+b^2\sin^2x}+
\sqrt{a^2\sin^2x+b^2\sin^2y}}\,dx\,dy.
\]

For `ab!=0` the remaining integral is finite and strictly positive, so
`sgn I'(0)=sgn(ab(a^2-b^2))`. Differentiation is rigorous in the integrated
form `-int |u_c|u_c.grad p_c`, since `z -> |z|z` is `C^1` even at zero.
This proves a signed pressure interaction outside the two-shear parity family,
but gives no viscous comparison, growth theorem, regularity result, or
Navier--Stokes solution.

## Bounded scout cycle 50

Amplitude scaling `u(t)=lambda w(lambda t)` converts viscosity to
`mu=nu/lambda`. The exact relative finite-time identity is

\[
{\|u(T/\lambda)\|_3^3-\|u(0)\|_3^3\over\|u(0)\|_3^3}
={3\over\|v\|_3^3}\int_0^T[I(w)-\mu D(w)]\,d\tau.
\]

Thus the apparent `O(lambda)` physical-time growth rate is paired with an
`O(1/lambda)` time scale; amplitude cancels except through effective viscosity
and the rescaled trajectory. Instantaneous positivity gives no uniform
persistence interval or arbitrarily large amplification. This is not a blowup
or regularity result.

## Bounded scout cycle 46

For the Cycle 43 perturbation, the viscous functional
`D(c)=int |u_c|(|grad u_c|^2+|grad|u_c||^2)` is exactly even in `c`. The
measure-preserving involution `(x,y)->(pi-x,pi-y)` sends `u_c` to `u_(-c)` and
preserves every norm in the integrand, so `D'(0)=0`. Meanwhile
`sgn I'(0)=sgn(ab(a^2-b^2))`. Choosing `a>b>0` and sufficiently small `c>0`
therefore gives `I(c)>0`. Under amplitude scaling, pressure and viscosity scale
as `I(lambda u)=lambda^4I(u)` and `D(lambda u)=lambda^3D(u)`, so
`lambda>nu D(c)/I(c)` gives positive instantaneous `L^3` growth. This is only
an initial derivative for smooth periodic data; it implies neither blowup nor
failure of global regularity.

## Bounded scout cycle 59

Fixed-interval inviscid-limit continuity upgrades the Cycle 43 positive initial
derivative to positive finite-time relative `L^3` growth at large amplitude.
On bounded rescaled intervals amplification converges to a finite Euler factor,
so amplitude alone cannot make it unbounded. This smooth two-dimensional family
gives no blowup or regularity result.

## Bounded scout cycle 74

The scaling-critical dyadic `L^3` recurrence leaves a high--high tail that does
not close in the proposed `ell^2` envelope. The only high--high-to-low symbol
gain converts the input derivative to the output frequency and is saturated by
opposing waves; many shells can add coherently to one low mode. Low transport
cancellation leaves a Leray commutator rather than pressure cancellation. The
specific envelope tactic is retired at this exact backscatter obstruction. No
regularity result is claimed.

## Main-funnel audit cycle 75

The proposed high--high Duhamel contraction is either false with a perturbative
data remainder or vacuous with an unrestricted quadratic remainder. Even if
assumed, it leaves a low--high quadratic recurrence with a large branch and no
uniform short-time factor. Dissipation repairs the infrared shell sum but leaves
an ultraviolet cutoff. Exact orthogonal packet examples also show that zero
orientation quadrupole does not control phase-sensitive low backscatter. Both
depletion variants are retired. No Navier result is claimed.

## Main-funnel cycle 81

The analytic-scale linear-sparsity criterion is established and admits a sharp
volume-to-centered-line lemma. But energy, enstrophy averaging, negative norms,
CKN theory, and maximum-point identities do not generate its hypothesis.
Dyadic energy costs are summable, and the best energy geometry occurs at
`Omega^(-2/5)` rather than the analytic `Omega^(-1/2)` scale. Exact broad-core
solutions falsify any kinematic automaticity claim. The tactic is retired. No
Navier result is claimed.

## Main-funnel cycle 82

The terminal ancient-profile route fails for arbitrary Type-II singularities.
CKN supplies lower concentration but not global critical upper control;
rescaling cannot reduce the diverging `L^3` norm. Critical bubbles can
proliferate at vanishing energy cost, producing concentration and escape at
infinity. Known Liouville/backward-uniqueness classes require precisely the
nonendpoint critical tightness not inherited by arbitrary profiles. The tactic
is retired. No Navier result is claimed.

## Bounded scout cycle 73

The exact helical triad formula exposes indefinite genuinely three-dimensional
vortex stretching. An integer triad has normalized `Y=540`, `Z=900`, and
stretching `864`, and scaling defeats absolute excursion caps. The best generic
separated paraproduct estimate leaves a `K_0 Y^2/nu^4` remainder, which worsens
at high enstrophy; dyadic passage costs are geometrically summable. Thus the
enstrophy-excursion tactic cannot exclude a finite-time Zeno cascade and is
retired. Any future route must control the scaling-critical full `L^3` flux.

## Bounded scout cycle 63

The invariant two-dimensional ansatz has uniformly bounded long-time `L^3`
amplification for each fixed datum and every effective viscosity. Vorticity
`L^(6/5)` is conserved for Euler and nonincreasing for Navier--Stokes, while
periodic Biot--Savart maps it to velocity `L^3`. Hence neither amplitude nor
arbitrarily long rescaled time can make the Cycle 43 profile amplify without
bound. The estimate is data-dependent, and vorticity rearrangement alone gives
no universal factor. This closes this ansatz, not Navier--Stokes.
