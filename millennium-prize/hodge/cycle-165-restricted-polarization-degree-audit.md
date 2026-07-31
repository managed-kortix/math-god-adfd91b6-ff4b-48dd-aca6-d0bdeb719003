# Cycle 165: restricted polarization degree under adapted isogenies

The `eta=1` identity controls a relative polarization volume.  It does not
make the restricted polarization principal, and it does not turn its degree
into 16.  For the Cycle 151 diagonal the initial restricted type is
`(2,2,4)`, whose volume is 16 and whose polarization-isogeny degree is 256.

## Conventions

Let `N` be an ample line bundle on an abelian threefold and let its
polarization type be `(d_1,d_2,d_3)`.  Then

\[
\chi(N)={c_1(N)^3\over3!}=d_1d_2d_3,
\qquad
c_1(N)^3=3!d_1d_2d_3,
\]

where the second expression denotes the unnormalized top intersection number,
and

\[
\deg(\phi_N)=|\ker\phi_N|=(d_1d_2d_3)^2=\chi(N)^2.
\]

Thus three different integers occur:

\[
\text{polarization volume}=d_1d_2d_3,
\quad
\text{top intersection}=6d_1d_2d_3,
\quad
\text{polarization degree}=(d_1d_2d_3)^2.
\]

Calling all three `degree` causes the apparent contradiction.

## The Cycle 151 seed

On the diagonal `Gamma`, the two product-polarization forms add.  The first
two coordinates have weights `1+1=2`, and the last has weights `1+3=4`.
Therefore

\[
L|_\Gamma\text{ has type }(2,2,4).
\]

Consequently

\[
\boxed{\chi(L|_\Gamma)=16},\qquad
\boxed{c_1(L|_\Gamma)^3=96},\qquad
\boxed{\deg(\phi_{L|_\Gamma})=256}.
\]

The value 16 is the product of the elementary divisors (equivalently the
normalized top self-intersection), not the degree of the polarization
homomorphism.  Under the standard convention `deg polarization = deg(phi_N)`,
the correct seed value is 256.

## One adapted step

Let

\[
f:(A,L)\longrightarrow(B,M),\qquad f^*M=pL,
\]

be a polarized `p`-isogeny, let `Gamma subset A` be an abelian threefold, and
write `Y=f(Gamma)`.  Put

\[
delta=|\ker(f)\cap\Gamma[p]|,
\qquad eta={p^3\over delta}.
\]

For `g=f|_Gamma:Gamma -> Y`, restriction of the pullback identity gives

\[
g^*(M|_Y)=p(L|_Gamma),\qquad \deg(g)=delta.
\]

Taking normalized top intersections yields

\[
delta\,\chi(M|_Y)=p^3\chi(L|_Gamma),
\]

and hence

\[
\boxed{\chi(M|_Y)=eta\,\chi(L|_Gamma)},
\qquad
\boxed{\deg(\phi_{M|_Y})=eta^2\deg(\phi_{L|_Gamma})}.
\]

Therefore an `eta=1` step preserves both the restricted volume and the
restricted polarization-isogeny degree.  Starting from the Cycle 151 diagonal,
every iterated `eta=1` step has

\[
\chi(M_n|_{Y_n})=16,
\qquad
\deg(\phi_{M_n|_{Y_n}})=256.
\]

The elementary-divisor type need not remain `(2,2,4)`: equality of the product
does not determine the type.  Without an integral lattice argument, later
types can only be asserted to have product 16.

## The flaw

The flaw is not in the relative formula from Cycle 162; it is in reading
`eta` as an absolute restricted degree, or in identifying the product of a
polarization type with the degree of its polarization homomorphism.  The exact
formula is

\[
\prod_i d_i(Y)=eta\prod_i e_i(\Gamma),
\]

not `prod_i d_i(Y)=eta`.  The latter silently assumes a principal seed
restriction.  Here the seed product is 16, so `eta=1` preserves 16 as volume
and 256 as polarization degree; it does not produce degree 1, and 16 is not
the standard polarization-homomorphism degree.

There is a second scope issue in any iteration claim.  Cycle 164 proves that a
single split adapted quotient retains a descended threefold and involution.
To iterate, each next kernel must be adapted to the current descended
threefold and must satisfy the same polarized pullback identity.  Preservation
of the numerical invariant follows once such a chain exists; existence of
arbitrarily long PEL-stable `eta=1` chains is a separate integral
prime-power/adelic problem and is not proved by the prime-level count at the
original seed.

No Hodge-conjecture result follows from this degree bookkeeping.

## Conditional orbit-closure consequence

Consider the correspondence graph whose objects are triples `(A,L;Y)` and
whose arrows are polarized isogenies adapted to the **carried** threefold `Y`
with `eta=1`.  The preceding identities put the whole connected orbit from the
Cycle 151 seed in the locus

\[
\deg(\phi_{L|Y})=256.
\]

The following closure argument needs the fine-level and generic-endomorphism
qualifications supplied in Cycle 166.  Only four restricted
polarization types have product 16:

\[
(1,1,16),\quad(1,2,8),\quad(1,4,4),\quad(2,2,4).
\]

On a neat finite-level cover, etale-locally represent a fixed multiple `rL` of
the universal polarization by a line bundle.  All four types then have the
single Hilbert polynomial `16r^3n^3`.  The closed subgroup incidence locus in
that projective relative Hilbert scheme has closed image in the base; the
intrinsic condition descends from the etale charts and then through the finite
level map.  Subject to the standard component-specific theorem that
the geometric generic endomorphism algebra is `K`, the locus is proper because
the geometric generic sixfold is simple.  Exact type itself is not encoded by
the Hilbert polynomial and is not needed for this argument.

Therefore any iterated orbit which continues to require `eta=1` relative to
the transported `Y` is not Zariski dense.  This does not settle a different
semigroup that discards `Y` after each step and chooses a new unrelated
threefold/kernel.  It also does not establish existence of arbitrarily long
adapted chains.
