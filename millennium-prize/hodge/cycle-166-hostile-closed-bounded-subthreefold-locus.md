# Cycle 166: hostile audit of the bounded subthreefold locus

The Cycle 165 non-density conclusion is repairable, but its final paragraph is
not yet a proof as written.  In particular, a Hilbert scheme is indexed by a
Hilbert polynomial, not by the elementary-divisor type of a restricted
polarization, and a universal polarization need not be represented by a
universal line bundle on the coarse PEL space.  Neither issue destroys the
argument after passing to a fine level cover and using one bounded Hilbert
polynomial.

## Exact object to close

Let `S` be a neat finite-level cover of the relevant complex PEL component and
let

\[
 \pi:{\cal A}\longrightarrow S
\]

be its universal abelian sixfold.  Etale-locally on `S`, a fixed multiple of
the universal polarization is represented by a relatively ample line bundle
`H`; the construction below is intrinsic and descends between such charts.  If
`H` represents `rL`, then an abelian
threefold `Y subset A_s` with

\[
 \chi(L_s|Y)=16
\]

has Hilbert polynomial

\[
 P_Y(n)=\chi(Y,H_s^{\otimes n}|Y)=16r^3n^3.
\]

There are no lower terms because the Todd class of an abelian variety is one.
Thus all four possible elementary-divisor types occur in the same relative
Hilbert scheme `Hilb^P({\cal A}/S)`.  Separating them is unnecessary.

Inside this projective relative Hilbert scheme impose:

1. containment of the zero section;
2. stability under inversion;
3. stability under addition on the fiber product of the universal subscheme
   with itself.

These are closed incidence conditions.  The universal Hilbert family is flat;
over characteristic zero its geometric fibers satisfying the group conditions
are smooth proper group schemes.  Fiberwise connectedness is locally constant
in such a proper smooth group family, so the union of the connected components
parametrizing abelian threefolds is open and closed in the subgroup locus.
It is therefore still projective over `S`.  Its image

\[
 Z_{16}=\{s:\ A_s\text{ contains an abelian threefold }Y
                 \text{ with }\chi(L_s|Y)=16\}
\]

is closed.

This formulation also avoids an exact-type specialization error.  The four
types

\[
 (1,1,16),\quad(1,2,8),\quad(1,4,4),\quad(2,2,4)
\]

are exactly the divisibility-ordered triples with product 16, but the Hilbert
polynomial records only their product.  If exact types are mentioned, one must
add the separate fact that the finite kernel of the restricted polarization is
locally constant in a smooth family; exact type is not supplied merely by
choosing a Hilbert polynomial.

## Descent and properness

The preceding construction is clean on a fine level cover, with the line-bundle
calculation made etale-locally and then descended, not directly on an
unspecified coarse PEL moduli space.  The resulting closed locus is invariant
under the finite level group and descends along the finite surjective map to
the coarse component.  Without this step, the phrase "the universal
polarization" conceals both the absence of a universal abelian scheme on a
coarse space and the possible Brauer obstruction to a global universal
polarizing line bundle.

Properness of `Z_16` uses the geometric generic sixfold on this particular
determinant-`-3`, signature-`(3,3)` component being simple.  Here that input
follows from generic monodromy.  On a neat connected full PEL component, Borel
density gives Zariski-dense monodromy `SU(V,h)`.  Over `C`, the
twelve-dimensional rational representation splits as `W plus W^vee` for
`SL_6`, with `W` and `W^vee` irreducible and nonisomorphic.  Hence

\[
\operatorname{End}_{\operatorname{SU}(V,h)}(V_Q)=K.
\]

Every geometric-generic endomorphism commutes with a finite-index monodromy
subgroup, while the prescribed PEL action supplies the reverse inclusion.
Therefore

\[
\boxed{\operatorname{End}^0(A_{\bar\eta})=K=Q(i).}
\]

The implication

\[
 \operatorname{End}^0(A_{\bar\eta})=K
 \quad\Longrightarrow\quad A_{\bar\eta}\text{ is simple}
\]

is valid, since a nontrivial isogeny decomposition supplies a nontrivial
idempotent in `End^0`, whereas the field `K` has none.  The nonsplit determinant
and polarization type change the rational inner form and integral level, not
the complex representation or its centralizer.  Thus the generic point is
outside `Z_16`, and `Z_16` is proper on every nonempty full connected component.

## Verdict

No counterexample to the carried-orbit conclusion emerges.  With the fine
level, universal-line-bundle, closed subgroup-incidence, and generic-monodromy
steps above, every chain carrying an abelian threefold and
satisfying `eta=1` at every arrow remains in the proper closed locus `Z_16`.
The degree invariant is exactly

\[
 \chi(L_n|Y_n)=16,\qquad \deg\phi_{L_n|Y_n}=256.
\]

The conclusion still says nothing about a Hecke semigroup which forgets the
carried `Y_n`, chooses a new subthreefold after an arrow, or uses arrows with
unbounded restricted degree.  This closure audit by itself does not construct
chains; the separate Cycle 166 lattice note gives periodic and mixed-prime
examples.  This is a restricted orbit-closure theorem, not a Hodge-conjecture
result.
