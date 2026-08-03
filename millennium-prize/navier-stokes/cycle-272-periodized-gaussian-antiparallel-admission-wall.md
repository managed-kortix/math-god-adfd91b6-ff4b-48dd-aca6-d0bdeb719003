# Cycle 272: periodized Gaussian anti-parallel tube admission

## Verdict: `ND270-ARCH-WALL` at item 1

The proposed architecture is identified only as a "periodized Gaussian
anti-parallel tube family." This does not define the map `a -> u_a` required by
`ND270-ADMISSION`. Therefore the fail-closed gate stops before choosing a
rational witness or performing any trajectory computation.

## First missing object

Item 1 requires one finite symbolic, real, mean-zero, divergence-free analytic
velocity family on a declared torus, with genuinely three-dimensional and
infinite Fourier support. The description supplied here fixes none of the data
needed to determine that family:

1. the torus periods and Haar normalization;
2. whether the Gaussian profile defines velocity, vorticity, or a vector
   potential;
3. the two oriented centrelines, their periodic images, core covariance,
   circulation, and any three-dimensional perturbation;
4. the exact operation enforcing periodicity, zero mean, and incompressibility
   (in particular, any Leray or Biot--Savart multiplier at nonzero modes);
5. the rational parameter coordinates and compact rational box.

These choices are mathematically substantive. For example, periodizing a
scalar Gaussian profile does not by itself produce a divergence-free vector
field. Applying the Leray projector or periodic Biot--Savart operator produces
different Fourier coefficients and hence different pressure flux. Exactly
straight parallel centrelines with opposite orientation can instead leave the
support planar, while a bent or displaced construction need not. Thus neither
nonplanarity nor the sign of the complete-velocity `L3` derivative is a
property of the words "Gaussian anti-parallel tubes."

The earlier source audit reaches the same reproducibility boundary: every
centreline, core profile, amplitude, periodization, and symmetry image must be
frozen independently; a Gaussian tube reconstructed from prose is not an
admissible datum. See
`cycle-266-3d-euler-velocity-lp-literature-scout.md`, lines 121--125 and
127--175.

## Consequences for the revised gate

Because no map `a -> u_a` or rational parameter domain exists, there is no
well-typed rational witness `a_*`. Consequently the following requested
certificates cannot even be formed:

- three spanning nonzero Fourier coefficients for nonplanarity;
- a Fourier obstruction to
  `-P(u_* dot grad u_*)+c dot grad u_*=0` for every constant `c`;
- the pressure solve
  `-Delta p_*=partial_i partial_j(u_{*,i}u_{*,j})`;
- an interval/Fourier-tail enclosure of
  `3 integral p_* u_* dot grad|u_*|` and of `integral |u_*|^3`;
- a common analytic majorant, truncation indices, and outward-rounding rule;
- a finite resource manifest and promoted-member interface.

Supplying a canonical Gaussian, selecting a perturbation, or choosing rational
parameters now would substitute a new architecture. The `ND270` stop rule
forbids such tuning or substitution after the first wall. An analytic Gaussian
tail estimate in the abstract cannot repair this defect: its constants depend
on the omitted periods, covariance, geometry, and projection multiplier.

## Exact return

`ND270-ARCH-WALL`: admission item 1 is missing. No finite symbolic family
`a -> u_a` and no rational parameter box were supplied, so no rational witness,
local-production interval certificate, analytic majorant, or finite resource
interface can be defined. No trajectory screen was run.

This is an architecture-local wall, not a claim that every fully specified
periodized Gaussian anti-parallel tube family fails the revised gate.
