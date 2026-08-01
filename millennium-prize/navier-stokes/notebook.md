# Notebook

## Cycle 177 cubic-flux baseline supplement

For actual receiver flux and orbit energies `x_[j]=2|j||u_j|^2`, the sharp
edge estimate `Phi_e<=gamma_e(x_p x_q x_k)^(1/2)` gives a three-uniform
geometric program. Its weighted-incidence dual is the exact constrained
AM--GM baseline and charges every shared mode only once. Physical cost minus
this baseline is the invariant compatibility excess.

For `L` triads sharing one pump, with `d_i=gamma_i^-2` and
`D=sum_i sqrt(d_i)`, the exact baseline is `3D^(2/3)`. The common-pump Leray
star `p=(N,0,0)`, `q_i=(0,Y_i,0)`, `k_i=(N,Y_i,0)`, with a quarter-turn receiver
phase, attains unit cubic flux on every designated triad and equality in the
baseline. Shared pumping alone therefore has zero excess. This supplements the
filter no-go below; it is not a regularity result.

## Cycle 177

The immediate cubic-flux reinterpretation of the Cycle 176 filter fails.  The
constructed coefficients are real, its nonlinearity has the common Fourier
factor `i`, and its only quadratic outputs are unoccupied terminal modes, so
every physical pairing `Re(conj(u_q) dot N_q(u))` is zero.  A nonzero flux needs
an added receiver with a relative phase.  Exact full convolution over the
four-parameter divergence-free receiver family shows that the outermost
receiver--pump outputs can all vanish only when the receiver quartet is zero;
receiver--receiver terms cannot cancel their unique frequencies.  Invariant
checkerboard parity can
support such phase-locked transfer and supplies neither escape nor a one-sided
sign.  For any fixed shell set, the signed cubic flux integrates to the exact
shell-energy identity, so it is not a new finite budget.  The route is rotated
out of the main funnel.  Its only live bounded-scout gate is a scale-uniform,
arbitrary-depth theorem giving one-sided coherent physical flux on
bounded-overlap intervals, controlling reverse flux, and charging the result to
one declared finite positive Navier--Stokes budget.

## Cycle 176

The Cycle 175 progression filter has an exact simultaneously populated
arbitrary-depth extension. If `R_(n+1)=m_n R_n`, then
`A_(R_0) product_n B_(m_n,R_n)=A_(R_D)`. Partitioning the geometric factors
between an `e_3` rail polynomial and an `e_2` collinear-pump polynomial gives a
single real divergence-free 3D field whose complete quadratic convolution is
only the terminal boundary quartet. Alternating the partition puts arbitrarily
many scales in both silent shear families. A Newton-polytope argument is sharp:
any two Laurent factors whose product has only two boundary monomials have
supports on one common affine line, so a genuinely independent-variable
version is impossible in this two-shear product ansatz. This is a
Fourier-algebra filter, not an invariant subsystem or a regularity result.

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

## Main-funnel cycle 211

The factor-two breaker reduces to one finite-time 2D Euler orbit. If a smooth
Euler solution has endpoint `L^3` ratio greater than `2+eta`, fixed-time
inviscid-limit stability transfers the strict crossing to all sufficiently
small effective viscosities. The exact scaling
`u_lambda(t)=lambda w_(nu/lambda)(lambda t)` then transfers it to any fixed
physical viscosity, and the 2D field embeds in `T^3`. Euler time reversal lets
the search target decay as well as growth. Hyperbolic mixing is relevant because
`||u||_3` is equivalent to the vorticity `W^(-1,3)` norm, but rearrangement alone
does not produce an Euler orbit and generally fails the conserved-energy gate.
The rigorous target is therefore an interval-certified full Euler trajectory,
endpoint cubature, an explicit inviscid-limit constant, and only then amplitude
scaling. See `cycle-211-euler-reversal-breaker.md`.

## Main-funnel cycle 212

The exact velocity identity is
`(1/3)d_t||u||_3^3+nu D=int p u dot grad|u|`. Periodic Calderon--Zygmund and
weighted Holder bound the pressure term by
`C D^(1/2)(int|u|^5)^(1/2)`. In 3D, Gagliardo--Nirenberg makes the resulting
dissipative coefficient proportional to the critical norm, so only small data
are absorbed. In 2D, heat--Leray Duhamel has integrable kernel
`K_2(nu t)^(-5/6)` and gives the explicit local factor-two interval
`t<=nu^5/(24 K_2||u_0||_3)^6`. In 3D the corresponding exponent is one and
does not close from `L^infinity_tL^3_x`; Kato's repair depends on the full heat
profile, not only its `L^3` norm. Two-dimensional vorticity contraction and
Biot--Savart give `||u(t)||_3<=C||omega_0||_(6/5)`, but the ratio to the initial
velocity norm is unbounded. These standard mechanisms support only local or
data-dependent constants and give no reason for the global number two. A
quantitatively enclosed 2D Euler inverse-transfer crossing, followed by a
positive-viscosity inviscid-limit enclosure, remains the cleanest counterexample
route. No crossing or Navier--Stokes result is claimed. See
`cycle-212-l3-bound-mechanisms.md`.

## Main-funnel cycle 213

Disconnected packet superposition does not amplify transient `L^3` ratios when
the claimed nonlinear decoupling is genuine. Cubic endpoint additivity makes
the aggregate ratio the weighted cubic mean of the component ratios, hence no
larger than the best packet; an explicit perturbative inequality gives the same
no-go under asymptotic endpoint additivity and Kato-stability error. Endpoint
`L^3` mild theory can transfer a finite approximate packet sum only after the
cross-interaction residual is controlled, and its constants are not uniform on
critical `L^3` balls. Dyadic frequency separation supplies only a square-function
equivalence: critical high--low interactions need not be small. Therefore any
successful many-scale breaker must exploit initial cancellation, final packet
collision, or a sequential coupled cascade, exactly where decoupling fails.
This retires gain-by-decoupled-replication, not the universal factor-two lemma.
See `cycle-213-disconnected-packet-superposition-no-go.md`.
