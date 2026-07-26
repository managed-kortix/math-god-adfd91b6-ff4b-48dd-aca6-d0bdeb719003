# Bounded scout checkpoints — cycle 41

These are exactly five bounded checkpoints or obstructions, one for each
non-RH Millennium dossier. They do not rotate or alter the active RH funnel,
and they do not resolve any Millennium problem.

## Birch--Swinnerton-Dyer

The cyclotomic/weight-variable second-derivative normalization is exact. Write

`F(T)=a_0+a_1 T+a_2 T^2+O(T^3)`, `T=exp(Ls)-1`, `L=log_p(1+p)`.

For `G(s)=F(exp(Ls)-1)`, the chain rule gives

`G(0)=a_0`, `G'(0)=L a_1`, `G''(0)=L^2(a_1+2a_2)`.

Consequently, after exact certification that `a_0=a_1=0`, one has
`a_2=G''(0)/(2L^2)`. Before those two exact zero tests, the second weight
derivative mixes the linear cyclotomic moment into the alleged quadratic
coefficient. This fixes the rank-two transfer normalization but supplies no
complex `L`-derivative identity.

## Hodge conjecture

For the Fermat-type plane calibration in a smooth degree-`d` hypersurface
fourfold, `d>=3`, take the normal map

`O_P(1)^3 -> O_P(d)`, `(l_1,l_2,l_3) |-> l_1u^(d-1)+l_2v^(d-1)+l_3w^(d-1)`.

The nine resulting degree-`d` monomials are distinct, so the map on global
sections is injective. The normal-sequence cohomology therefore gives

`h^0(N_(P/X_d))=0`, `h^1(N_(P/X_d))=binom(d+2,2)-9`.

This equals the expected codimension of the image of the plane incidence:
containing a fixed plane imposes `binom(d+2,2)` conditions and planes vary in
the 9-dimensional `Gr(3,6)`. At `d=3` the obstruction-space dimension is one,
even though the plane point is reduced and the incidence image is a genuine
divisor. Thus `H^1(N) != 0` is not itself an obstruction to incidence
smoothness or dominance.

## Navier--Stokes

Every phase-shifted, unequal-frequency two-shear still has zero pressure
contribution to the initial critical-norm derivative. On the periodic torus let

`u=(a sin(my+alpha), b sin(nx+beta), 0)`.

It is divergence-free, and the mean-zero pressure is

`p=2abmn cos(my+alpha)cos(nx+beta)/(m^2+n^2)`.

In `int p u.grad|u|`, the `x`-derivative term contains, after centering its
phase, `sin(nx+beta)cos(nx+beta)^2` times a function even in that sine; its
integral over a period is zero. The `y`-derivative term vanishes identically by
the same argument. Hence

`int p u.grad|u|=0`

for all amplitudes, integer frequencies, and phases in this family. Breaking
the earlier parity by frequency or phase choices is therefore impossible; a
pressure-growth search needs a genuinely nonseparable interaction.

## P versus NP

The decision-tree memorization obstruction has an exact sample-size form. For
arbitrary labels on `h` distinct `N`-bit inputs, recursively querying a bit that
splits the remaining examples gives a decision tree with at most `h-1`
internal nodes. Converting each node to

`(x and A) or ((not x) and B)`

uses three binary De Morgan gates, while at most `min(N,h-1)` input negations
are shared. Thus some circuit fits every such sample with size at most

`3(h-1)+min(N,h-1)`.

An antichecker against all circuits of size at most `s` must consequently
satisfy `3(h-1)+min(N,h-1)>s`; in the regime `h>=N+1`, this is
`h>(s-N)/3+1`. A sample intended to defeat size `N^k` circuits must itself have
order `N^k` under this direct route. This does not amplify one fixed exponent
to a superpolynomial lower bound.

## Yang--Mills mass gap

The escaping-state obstruction persists simultaneously at every fixed
integer Euclidean time. For `0<q<1`, on `ell^2(N)` set

`T_n=qI+(1-q)P_(e_n)`.

For every integer `k>=1`,

`T_n^k=q^k I+(1-q^k)P_(e_n)`.

Hence `T_n^k -> q^k I` strongly for every fixed `k`, and every fixed-state
integer-time correlator converges to one with exponential factor `q^k`.
Nevertheless `T_n^k e_n=e_n` and `||T_n^k||=1` for every `n,k`; every cutoff
still has a unit spectral value and zero transfer-Hamiltonian gap. Even
simultaneous strong convergence of all fixed-time transfer powers cannot
replace a cutoff-uniform full-vacuum-complement contraction.
