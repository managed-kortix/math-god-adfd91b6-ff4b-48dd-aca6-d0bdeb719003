# Cycle 104: nonsplit Weil sixfold audit

## Target and novelty

Fix `K=Q(i)`.  Let `A` be a very general polarized abelian sixfold of Weil
type, signature `(3,3)`, whose Hermitian determinant class is represented by
`-3` in
\[
 \mathbf Q^\times/N_{K/\mathbf Q}(K^\times).
\]
The exceptional middle Hodge space is the rational rank-two determinant
subspace
\[
 W_K(A)=\bigwedge_K^6H^1(A,\mathbf Q)\subset H^6(A,\mathbf Q).
\]
The generic Hodge group is `SU(3,3)`; contraction tensors are divisor/
endomorphism-generated, while the determinant invariant is exactly the
exceptional Weil space.

Primary-source review supports that the generic nonsplit `-3` component remains
open as of July 2026.  Schoen/Koike cover relevant split Prym families, and
Markman's 2025 preprint covers polarized Weil sixfolds of split discriminant
`-1`.  The label "smallest" is not intrinsic because discriminants are norm
classes; `-3` is merely the first convenient nonsplit integer representative
after fixing `Q(i)`.

## Exact projection test

Over `K`, write
\[
 H^1(A,K)=W\oplus\bar W,
\]
where the action of `i` has eigenvalues `i,-i`.  The exact projectors are
\[
 e_W=(1-iJ)/2,\qquad e_{\bar W}=(1+iJ)/2.
\]
For a codimension-three cycle class `z`, its exceptional component is
\[
 P_{\rm Weil}(z)=(\wedge^6e_W)z+(\wedge^6e_{\bar W})z.
\]
Thus a proposed construction passes iff its pure `W^6` coefficient is nonzero.
One rational cycle with nonzero projection suffices: applying the algebraic
endomorphism `1+i` acts by opposite determinant scalars on the two lines, so
the original and its transform span the rational rank-two space.

## Mechanism gates

Smooth polarized deformation cannot change the discriminant norm class.
Therefore a nonsplit sixfold cannot smoothly specialize inside the Weil moduli
problem to Markman's split component.  A compatible product degeneration
conserves the Hermitian discriminant, forcing the nonsplit contribution into at
least one factor.  Singular degeneration avoids this only by introducing
nearby-cycle and horizontal-lifting obstructions.

Ordinary principally polarized Pryms and algebraic intermediate Jacobians with
compatible integral `Z[i]` action lie in the unimodular split class.  Isogeny or
scalar polarization changes the determinant only by a norm/sixth power and
does not reach `-3`.  Abel--Prym curves and their straightforward Pontryagin
products remain in the contraction-generated cohomology and have zero Weil
projection.  Markman's secant-sheaf construction has the right semiregularity
mechanism, but its `X x Pic^0(X)` Hermitian form is structurally hyperbolic and
split.

## Exact production lemma

On a neat cover of the nine-dimensional nonsplit Shimura component, it would
suffice to find one codimension-three seed cycle `Z` at a CM point such that:

1. `P_Weil([Z]) != 0`;
2. its relative Hilbert/Chow point is formally unobstructed at every order;
3. the corresponding component maps with rank nine to the Shimura base.

Properness and spreading would then produce a generic cycle with nonzero Weil
projection; the `1+i` transform would span the full exceptional space.

No candidate passes these gates.  The target is a genuine bounded open Hodge
case, but remains a scout rather than the main funnel until a determinant-`-3`
geometric seed is found.  No Hodge result is claimed.
