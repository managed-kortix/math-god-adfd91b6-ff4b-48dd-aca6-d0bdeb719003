# Notebook

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
