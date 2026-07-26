# Bounded scout checkpoints — cycle 39

These are five bounded exact checkpoints or obstructions for the non-main
Millennium routes.  They do not alter the active RH funnel and do not resolve
any Millennium problem.

## Birch--Swinnerton-Dyer

Finite `5`-adic precision cannot certify cyclotomic vanishing.  For every
`M>=1`, the series `T^2` and `T^2+5^M` are identical modulo `5^M`, but their
orders at `T=0` are respectively two and zero.  Both have `mu=0` and
`lambda=2`.  Thus the rank-two transfer calibration needs exact zero tests for
the constant and linear modular-symbol moments, not valuations at any fixed
precision.

## Hodge conjecture

For a plane `P` in a smooth degree-`d` hypersurface fourfold in `P^5`,

`c(N_(P/X))=(1+h)^3/(1+d h)`

gives `P^2=d^2-3d+3`.  Since `h^4=d` and `P.h^2=1`, the primitive rational
class `P-h^2/d` has square

`d^2-3d+3-1/d`.

At `d=3` this recovers `8/3`, and the integral multiple `3[P]-h^2` has square
`24`.  The plane calibration is therefore fixed by the normal sequence, not
by tangent dimensions alone.

## Navier--Stokes

Adding a reverse derivative pair is necessary but not sufficient for
pressure-driven initial `L^3` growth.  For

`u=(a sin y,b sin x,0)`,

the pressure source is `2ab cos x cos y` and the mean-zero pressure is
`p=ab cos x cos y`.  Nevertheless `int p u.grad|u|=0`: each of its two terms
is odd in one torus coordinate.  This exact two-shear family has nonconstant
pressure but zero pressure contribution to the critical-norm derivative.

## P versus NP

The six-vertex mask calculation extends exactly to every `n>=3`.  Covering all
labeled `n`-vertex 3-colorable graphs by partition masks requires and is
sufficed by every partition into exactly three nonempty blocks.  Hence the
minimum cover size is

`S(n,3)=(3^n-3*2^n+3)/6`.

Necessity follows from the complete tripartite graph of each partition;
sufficiency follows by splitting a color class of any one- or two-coloring.
Thus this witness-mask DNF grows exponentially and remains irrelevant to
unrestricted circuit lower bounds.

## Yang--Mills mass gap

The escaping-state obstruction survives strong operator convergence.  For
`T_n=qI+(1-q)P_(e_n)` on `ell^2(N)`,

`||(T_n-qI)f||=(1-q)|f_n| -> 0`

for every fixed `f`, so `T_n -> qI` strongly.  Yet `||T_n||=1` and
`T_n e_n=e_n` at every cutoff.  Even strong convergence to a strictly
contractive limit does not provide the cutoff-uniform full-vacuum-complement
contraction needed for a mass gap.
