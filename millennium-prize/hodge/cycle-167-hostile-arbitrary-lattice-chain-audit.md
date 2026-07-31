# Cycle 167: hostile audit of the arbitrary lattice chain

The Cycle 166 chain is mathematically sound after one notation repair.  The
displayed definition of `Lambda_1`, however, is not literally well typed:
`K` was defined as a subgroup of `A_0[p]=p^{-1}Lambda_0/Lambda_0`, whereas the
map in the next paragraph has target `Lambda_0/pLambda_0`.  These groups are
canonically isomorphic by multiplication by `p`, but that isomorphism was not
stated, and the following sentence gives a second, incompatible description
of `widetilde K`.  There is no additional failure in integrality, polarization
type, mixed-prime globalization, or polarized periodicity once this is fixed.

## Correct over-lattice definition

Let

\[
 q:p^{-1}\Lambda _0\longrightarrow
 p^{-1}\Lambda _0/\Lambda _0=A_0[p]
\]

be the quotient map.  The quotient lattice attached to `K` is simply

\[
 \boxed{\Lambda _1=q^{-1}(K).}
\]

Equivalently, use multiplication by `p` to identify

\[
 p^{-1}\Lambda _0/\Lambda _0\simeq\Lambda _0/p\Lambda _0,
\]

let

\[
 \widehat K=\{a\in\Lambda _0:a\bmod p\Lambda _0\in pK\},
\]

and write

\[
 \Lambda _1=p^{-1}\widehat K.
\]

Here `pK` denotes the image of `K` under the displayed identification.  Since
`pLambda_0 subset widehat K`, this lattice already contains `Lambda_0`; the
summand `Lambda_0+` in Cycle 166 is redundant.  The original notation can be
made correct by declaring this identification and setting
`widetilde K=widehat K`, but it cannot simultaneously call `widetilde K` the
inverse image in `Lambda_0` and call `(1/p)widetilde K` the inverse image in
`p^{-1}Lambda_0` without explaining the identification.

The same repair gives

\[
 U\cap\Lambda _1=q_U^{-1}(D)
 =p^{-1}\widehat D,
\]

where `q_U:p^{-1}Delta_0 -> Gamma[p]` and `widehat D` is the lift of `pD` in
`Delta_0`.  Thus the asserted index is still `p^3`.

## Integrality and ambient polarization type

Put `E_1=pE_0`.  If `x=a/p` and `y=b/p` belong to `Lambda_1`, isotropy of `K`
means

\[
 E_0(a,b)\equiv0\pmod p.
\]

Consequently `E_1(x,y)=E_0(a,b)/p` is integral.  Positivity is unchanged, so
this is a polarization rather than merely an integral alternating form.

The exact ambient type is also preserved.  At `p`, the original form is
unimodular because `p>=5` does not divide its type `(1,1,1,1,1,3)`.
Maximal isotropy of `K` says precisely that `Lambda_{1,p}` is self-dual for
`pE_0`.  At every prime `l!=p`, the lattice is unchanged and multiplication of
the form by the unit `p in Z_l^x` does not alter its local elementary divisors.
Hence

\[
 (\Lambda _1,pE_0)\quad\hbox{again has type}\quad(1,1,1,1,1,3).
\]

The same local argument proves type preservation at every stage of the chain.
On the carried threefold it in fact also preserves the exact type `(2,2,4)`,
not only its product 16: all allowed primes are prime to 16, `D` is a maximal
isotropic subgroup of `Gamma[p]`, and the identical local self-duality argument
applies to the restricted lattice.

## Mixed-prime globalization

For finite-support exponents `e=(e_p)`, define the local lattices as in Cycle
166, but regard them as lattices in `V(Q_p)`.  Since they equal
`Lambda_0 tensor Z_p` away from finitely many primes, the intersection

\[
 \Lambda(e)=V(Q)\cap\prod_p\Lambda(e)_p
\]

is a global lattice and has those completions.  With
`m=prod_p p^{e_p}`, each local pair `(Lambda(e)_l,mE_0)` has the seed
elementary divisors: at primes in the support this follows by the alternating
maximal-isotropic construction, and elsewhere `m` is a unit.  Therefore the
global form is integral and has the seed type.  Local indices multiply, giving
the claimed ambient degree `m^6`, carried degree `m^3`, and `eta_m=1`.

This proves every finite prefix of an arbitrary word.  An infinite word with
infinite prime support does not define one finite-index global lattice or one
integer `m`; the valid statement is that it defines an infinite chain whose
individual stages are obtained from finite prefixes.  Cycle 166's surrounding
wording uses this finite-prefix interpretation, so no correction to its degree
formulas is needed.

## Polarized periodicity

The fixed-prime periodicity claim is correct, but the isomorphism should be
displayed.  Multiplication by `p^r` on `V` induces

\[
 h_{2r}:V/(p^{-r}\Lambda_0)\longrightarrow V/\Lambda_0,
 \qquad
 h_{2r+1}:V/(p^{-r}\Lambda_1)\longrightarrow V/\Lambda_1.
\]

It satisfies

\[
 h_{2r}^*E_0=p^{2r}E_0=E_{2r},
 \qquad
 h_{2r+1}^*E_1=p^{2r}(pE_0)=E_{2r+1}.
\]

Thus these are genuine polarized isomorphisms, not similarities obtained by
forgetting the integral lattice.  The one-prime chain really alternates
between two polarized isomorphism classes.  For a mixed-prime word no analogous
two-periodicity was claimed and none follows.

## Verdict

The flaw is the ill-typed and internally ambiguous definition of
`widetilde K`, not the chain itself.  Replacing it by
`Lambda_1=q^{-1}(K)` removes the problem.  The polarization type, finite-prefix
mixed-prime globalization, and fixed-prime polarized periodicity then follow
from explicit local lattice arguments.  The construction remains a periodic
or carried special-locus construction and still supplies no generic Hodge
transport.
