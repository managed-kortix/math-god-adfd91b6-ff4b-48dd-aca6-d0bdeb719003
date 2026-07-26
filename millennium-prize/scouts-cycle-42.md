# Bounded scout checkpoints — cycle 42

These are exactly five bounded checkpoints or counterexamples, one for each
non-RH Millennium dossier. RH remains the active funnel. None of these items
resolves a Millennium problem.

## Birch--Swinnerton-Dyer

The weight-to-cyclotomic conversion extends exactly through degree three. Let

`F(T)=a_0+a_1T+a_2T^2+a_3T^3+O(T^4)`, `T=exp(Ls)-1`, `G(s)=F(T(s))`.

Direct differentiation gives

`G'''(0)=L^3(a_1+6a_2+6a_3)`.

Thus, even after `a_0=a_1=0`, a third weight derivative contains the already
present quadratic cyclotomic moment. The exact inversion is

`a_3=G'''(0)/(6L^3)-G''(0)/(2L^2)`.

Consequently no higher-weight derivative can be read coefficientwise without
triangular subtraction. This is only a normalization checkpoint and supplies
no cyclotomic-to-complex derivative identity.

## Hodge conjecture

The Fermat-type plane calibration has an exact reduced local Hilbert model
despite the first obstruction. For a cubic fourfold, the normal map on the plane is

`O_P(1)^3 -> O_P(3)`, `(l_1,l_2,l_3) |-> l_1u^2+l_2v^2+l_3w^2`.

Its cokernel is the one-dimensional span of `uvw`. Hence
`H^0(N_(P/X))=0` and `H^1(N_(P/X))=C[uvw]`. Since the Zariski tangent space of
the Hilbert scheme at `[P]` is `H^0(N_(P/X))`, the local ring has maximal ideal
`m` satisfying `m/m^2=0`; Nakayama gives `m=0`. Therefore `[P]` is a reduced
isolated Hilbert point despite nonzero obstruction space. This is an exact
counterexample to using `H^1(N) != 0` as a nonreducedness test; it gives no
dominance theorem for other Hodge loci.

## Navier--Stokes

A genuinely nonseparable one-mode perturbation breaks the parity mechanism
behind the two-shear zero. On the two-dimensional periodic torus, embedded in
three dimensions, set

`u_c=(a sin y+c sin(x+y), b sin x-c sin(x+y), 0)`.

It is divergence-free. Solving `Delta p=-partial_i u_j partial_j u_i` gives

`p_c=ab cos x cos y+c[b cos y+b cos(2x+y)/5-a cos x-a cos(x+2y)/5]`.

The new pressure contains the mixed frequencies `(2,1)` and `(1,2)`, while
`|u_c|^2` contains `sin(x+y)sin x` and `sin(x+y)sin y`. None is odd under the
coordinate reflections that killed the complete two-shear integral. Thus one
diagonal Fourier mode is the first exact ansatz not covered by the previous
zero theorem in this dossier. This is a bounded structural checkpoint only: the signed
unprojected integral and the viscous comparison remain to be certified.

## P versus NP

The memorization obstruction has an exact piecewise inversion. If an
antichecker has `h` distinct `N`-bit examples and defeats every circuit of size
at most `s`, then

`3(h-1)+min(N,h-1)>s`.

For `h<=N+1` this is `4(h-1)>s`, hence
`h>=floor(s/4)+2`. For `h>=N+1` it is `3(h-1)+N>s`, hence
`h>=floor((s-N)/3)+2`. In particular, at the route's quadratic target
`s=N^2`, for `N>=4` every antichecker must have

`h>=floor((N^2-N)/3)+2`.

This sharpens the integer threshold only. It remains a same-exponent lower
bound and supplies no all-exponents amplification.

## Yang--Mills mass gap

Even convergence of every fixed bounded continuous functional calculus does
not remove escaping zero-gap states. For `0<q<1`, let

`T_n=qI+(1-q)P_(e_n)` on `ell^2(N)`.

For every bounded continuous `f` on `[0,1]`, spectral calculus gives

`f(T_n)=f(q)I+(f(1)-f(q))P_(e_n) -> f(q)I`

strongly. Nevertheless `1` remains an eigenvalue of every `T_n`, so
`||T_n||=1` and the corresponding transfer Hamiltonian has zero gap at every
cutoff. This strictly extends the fixed-power obstruction: the whole fixed
continuous functional calculus may converge strongly while the spectral edge
escapes. A cutoff-uniform full-complement contraction is still indispensable.
