# Cycle 161: polarized-isogeny transport and Hecke normalization audit

Let `(A,L)` and `(B,M)` be polarized abelian sixfolds and let

\[
f:A\longrightarrow B,
\qquad f^*M\equiv qL
\]

for a positive integer `q`.  Assume first that the polarizations have the same
top self-intersection, as they do for principal polarizations.  Taking sixth
powers gives

\[
\deg(f)=q^6.
\]

This convention must not be confused with either an isogeny of degree `m` or
the multiplication map `[m]`.  For `[m]`, one has `q=m^2` and
`deg([m])=m^12`.  For a principally polarized `m`-isogeny in the convention
`f^*M=mL`, one has `q=m` and `deg(f)=m^6`.

Accordingly, the three common meanings of `m` give different-looking formulas:

| meaning of `m` | polarization multiplier | isogeny degree | raw cycle multiplier | normalizing factor |
|---|---:|---:|---:|---:|
| `f^*M=mL` | `m` | `m^6` | `m^3` | `m^-3` |
| `deg(f)=m` | `m^(1/6)` | `m` | `m^(1/2)` | `m^(-1/2)` |
| multiplication `[m]` | `m^2` | `m^12` | `m^6` | `m^-6` |

The middle row is numerical notation, not generally an integral polarized
similitude parameter; for equal-volume integral polarizations, `deg(f)` is a
sixth power whenever a scalar relation `f^*M=qL` actually holds.

If `Z` is a codimension-three cycle on `A`, hence a three-dimensional cycle,
then the raw effective transport is `f_*Z` and

\[
\deg_M(f_*Z)
=\frac1{3!}\int_B[f_*Z]c_1(M)^3
=\frac1{3!}\int_A[Z]f^*c_1(M)^3
=q^3\deg_L(Z).
\]

For an integral `Z`, let

\[
\delta_Z=\deg(Z\longrightarrow f(Z)).
\]

Then the exact cycle-level and reduced-image formulas are

\[
f_*[Z]=\delta_Z[f(Z)],
\qquad
\deg_M(f(Z))=\frac{q^3}{\delta_Z}\deg_L(Z),
\qquad
q^{-3}f_*[Z]=\frac{\delta_Z}{q^3}[f(Z)].
\]

If `Z` is an abelian threefold translate, then
`delta_Z=|ker(f) cap Stab(Z)|`; for an abelian subvariety this is simply
`|ker(f) cap Z|`.  Thus one must distinguish the degree of the pushforward
cycle, which always acquires `q^3`, from the degree of its reduced geometric
image, which acquires `q^3/delta_Z`.

Thus the relevant exponent is three, not six.  The sixth power occurs only in
the ambient polarization volume and in `deg(f)`.  Equivalently,

\[
q^3=\sqrt{\deg(f)}.
\]

The middle-degree, polarization-intersection-normalized transport is

\[
\boxed{\mathcal T_f(Z)=q^{-3}f_*Z.}
\]

It preserves the polarization intersection:

\[
\deg_M(\mathcal T_f(Z))=\deg_L(Z).
\]

This is not the inverse-isogeny normalization.  Since

\[
f_*f^*=\deg(f)\,\mathrm{id}=q^6\,\mathrm{id},
\]

the rational map inverse to pullback is

\[
(f^*)^{-1}=q^{-6}f_*.
\]

Thus there are already three distinct operations: raw effective pushforward
`f_*`, the inverse-to-pullback transport `q^-6 f_*`, and the middle-weight or
intersection-normalized transport `q^-3 f_*`.  Calling any one of these simply
"the transport" is ambiguous.  The square-root degree/denominator tradeoff in
Cycle 156 concerns the third operation, not the inverse-to-pullback map.

For the convention `f^*M=mL`, the displayed representative is
`m^{-3}f_*Z`; for `[m]` it is `m^{-6}[m]_*Z`.  Writing `m^{-3}` for `[m]`, or
writing `m^{-6}` for a polarized `m`-isogeny, mixes the two conventions.

The denominator statement therefore has an exact answer in the free group of
cycles: for integral `Z`, the coefficient of the reduced image has denominator

\[
\boxed{\frac{q^3}{\gcd(q^3,\delta_Z)}}.
\]

Its denominator in the Chow group or in a selected integral cohomology lattice
can be smaller if `[f(Z)]` becomes divisible there.  Without a primitivity
calculation there is no exact reduced Chow or cohomological denominator.  What
is exact uniformly is the normalizing factor and the degree
`q^3 deg_L(Z)` of the denominator-cleared pushforward cycle.

For a finite Hecke correspondence consisting of polarized `q`-isogenies
`f_1,...,f_N`, further normalizations must also be separated.  The
middle-weight-normalized sum is

\[
T_q^{\mathrm{wt}}(Z)=q^{-3}\sum_{j=1}^N(f_j)_*Z.
\]

If "normalized Hecke action" means the average over the finite correspondence,
it is instead

\[
T_q^{\mathrm{avg}}(Z)=\frac1N q^{-3}
\sum_{j=1}^N(f_j)_*Z.
\]

The factor `q^-3` corrects middle cohomological weight; `N^-1` corrects the
degree of the Hecke correspondence.  They are logically independent.  An
unnormalized Hecke operator may omit both by convention.  An action defined as
pull-push along the two legs of a moduli correspondence can have an additional
degree from either leg, and the inverse-isogeny identification uses `q^-6`
rather than `q^-3`.  Therefore no unique "normalized Hecke action" can be
recovered from the word normalized: the correspondence, direction, and whether
one wants raw, inverse, unitary/middle-weight, or probabilistic normalization
must all be stated.

This confirms the square-root growth sentence in Cycle 156 only after fixing
the polarized-similitude convention: the denominator-cleared transported cycle
has degree `q^3 deg_L(Z)=sqrt(deg(f)) deg_L(Z)`.  The normalized rational cycle
has constant polarization intersection but potentially unbounded displayed
denominator.  Cycle 156 would be too strong if read as asserting that the
reduced denominator is always exactly `q^3`, or if its `m` denoted the degree
of the isogeny rather than its polarization multiplier.

There is also a dimension check on kernel-index formulations.  For a polarized
`q`-isogeny of abelian sixfolds, `ker(f)` is a Lagrangian in `A[q]` of order
`q^6`, because `A[q]` has rank twelve.  A rank-six symplectic module with
Lagrangians of order `q^3` describes a threefold (or an explicitly identified
six-dimensional subquotient), not the full sixfold Hecke kernel.  Any use of
such a smaller module must construct that subquotient and prove that its index
is the same `delta_Z` appearing above.

Finally, if two kernels `L` and `Gamma` contain `I=L cap Gamma`, the common
cover `A/I` maps to both quotients with degrees `[L:I]` and `[Gamma:I]`.  This
does not by itself produce a direct isogeny of that degree between `A/L` and
`A/Gamma`.  It produces a span.  Both quotients map to
`A/(L+Gamma)` (when the subgroup sum is used), and a direct isogeny or a precise
Hecke label requires an additional construction.  Consequently a claimed
containment in a union of degree-`d` Hecke translates does not follow with the
same bound merely from the common-quotient diagram, although a weaker bounded
degree statement may follow after tracking the extra maps and polarizations.

Consequently a dense Hecke orbit still does not land in one bounded integral
Chow stratum.  Using raw effective cycles loses the degree bound; using
weight-normalized rational cycles loses a uniform denominator bound.  Averaging
over the correspondence adds the generally varying factor `N` and does not
repair either problem.  This audit is a normalization correction, not a generic
algebraicity theorem.
