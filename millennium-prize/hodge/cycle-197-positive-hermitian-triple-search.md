# Cycle 197: positive Hermitian triples do not preserve the projector cancellation

Cycle 196 writes the denominator-cleared seed as a signed sum of cubes of
rank-one nef divisor classes.  This cycle replaces every factor by a positive
Hermitian divisor, searches the resulting finite family exactly, and computes
its tangent Hodge equations on

\[
T_0S=M_3(\mathbb C).
\]

The outcome is negative for this minimal polarization repair.  Every
nonconstant positive triple has a proper tangent Hodge locus, and the signed
triple combination itself has only the zero tangent direction.  Thus the
cohomological horizontality of the Weil projector is not preserved by this
particular divisor-cube identity.

## Minimal positive replacement

Let

\[
\Theta=\operatorname {diag}(1,1,1,1,1,3)
\]

be the product polarization, and retain the Cycle 196 rank-one matrices

\[
H_{a,j}=\ell_{a,j}^{*}\ell_{a,j},\qquad
\ell_{a,j}(z)=z_{j+3}-az_j.
\]

They satisfy

\[
[\Gamma_a]=H_{a,1}H_{a,2}H_{a,3}.
\]

The coefficient one in `Theta+H_(a,j)` is the smallest positive integer
padding: `H_(a,j)` has rank one, while `Theta+H_(a,j)` is positive definite.
In the divisor ring, inclusion-exclusion gives

\[
H_{a,1}H_{a,2}H_{a,3}
=\sum_{I\subseteq\{1,2,3\}}(-1)^{3-|I|}
 \prod_{j=1}^{3}L_{a,I,j},
\]

where

\[
L_{a,I,j}=\begin{cases}
\Theta+H_{a,j},&j\in I,\\
\Theta,&j\notin I.
\end{cases}
\]

All three factors in every summand are positive definite integral Hermitian
classes.  Applying this to the seven projector terms gives 56 raw triples.
The seven all-`Theta` terms consolidate, so there are exactly 50 distinct
nonzero signed triples.  Their common all-`Theta` coefficient is

\[
-\sum_{k=0}^{6}c_k=-315070486723952640.
\]

This is minimal only within the natural integral padding architecture
`Theta+H_(a,j)`; it is not a proof that no shorter positive decomposition exists
in the full ample cone.

## Exact factor Hodge conditions

For `B in M_3(C)`, put

\[
\mu_B=\begin{pmatrix}0&B\\Q^{-1}B^t&0\end{pmatrix},
\qquad Q=\operatorname {diag}(1,1,3).
\]

For any Hermitian divisor matrix `L`, its first-order Hodge condition is

\[
\boxed{L\mu_B-(L\mu_B)^t=0.}
\]

The polarization `Theta` satisfies this identity for every `B`, as it must for
the polarized PEL family.  For a graph factor `H_(a,j)`, direct substitution
reduces it to

\[
\boxed{B_{jr}=0\ (r\ne j),\qquad B_{rj}=0\ (r\ne j),\qquad
(Q_j^{-1}-N(a))B_{jj}=0.}
\]

Here indices are `1,2,3`.  Hence for a subset `I` of nonconstant factors, the
intersection of the three individual divisor Hodge loci has the following
tangent dimensions, listed in subset order
`000,001,010,011,100,101,110,111`:

\[
\begin{array}{c|c}
a=1&(9,5,5,3,4,2,2,2)\\
N(a)>1&(9,4,4,1,4,1,1,0).
\end{array}
\]

Adding `Theta` does not alter these equations.  Consequently the individual
class Hodge loci intersect the full base only for the all-`Theta` triple.  No
triple containing a graph-derived factor has full intersection with `S`.

## Product and signed-cycle conditions

The exact tangent condition for one codimension-three product
`L_1L_2L_3` is the vanishing of its `(2,4)` derivative

\[
\boxed{
\sum_{r=1}^{3}
\bigl(L_r\mu_B-(L_r\mu_B)^t\bigr)
\wedge\prod_{s\ne r}L_s=0.
}
\]

This condition can be weaker than requiring every factor to remain Hodge, so
the verifier computes it directly rather than inferring it from the factor
intersection.  Among the 56 raw triples, exactly the seven repeated
all-`Theta` triples have full tangent Hodge locus.  Every nonconstant product
has a nonzero tangent condition.

Finally, summing these product derivatives with the exact inclusion-exclusion
and projector coefficients gives a map of rank nine on `M_3(C)`.  Therefore

\[
\boxed{T_0\operatorname {Hdg}(\text{signed positive-triple expression})=0.}
\]

There is no contradiction with the horizontality of `alpha_0`.  The divisor
identity is an equality in the special-fiber divisor/cohomology ring.  Away
from the CM point the graph divisors cease to be `(1,1)`, so the same fixed
flat-factor expression does not remain an identity of Hodge classes.  The
Weil projector class deforms as a flat Hodge class, but this chosen collection
of factors does not.  Nor can signs cancel embedded deformations of separate
effective complete intersections in a product of Chow spaces.

Reproduce the finite search, the 50-term consolidation, and all exact tangent
ranks with

```sh
python3 millennium-prize/hodge/verify_cycle197_positive_hermitian_triples.py
```

This rules out the minimal polarization-padded divisor-cube repair.  It does
not obstruct all positive Hermitian decompositions, all rationally equivalent
representatives, or the Cycle 195 relative-Chow gate.
