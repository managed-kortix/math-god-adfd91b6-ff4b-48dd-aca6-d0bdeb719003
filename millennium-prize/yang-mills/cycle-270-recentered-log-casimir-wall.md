# Cycle 270: recentered log-Casimir norm for the exact `SU(2)` block map

## Frozen test

Use exactly the Cycle 264 two-dimensional, free-boundary, scale-two
straight-link pushforward. In normalized positive character coordinates its
complete one-plaquette map is

\[
 (Rc)_j=c_j^4,\qquad j=1/2,1,3/2,\ldots .                 \tag{270.1}
\]

This scout tests one norm only. It does not alter the block map, add staples,
or truncate the representation tail.

Let

\[
 C_j=j(j+1),\qquad h_j(c)=-{\log c_j\over C_j},
 \qquad r={1\over2}.                                      \tag{270.2}
\]

For a positive reference point `b`, put `t=h_r(b)>0`. For a logarithmic
variation `delta h` define the coupling-recentered, non-diagonal norm

\[
 \|\delta h\|_{b,*}
 =\max\left\{
 { |\delta h_r|\over t},
 \sup_{j>r}2^{-2j}{|\delta h_j-\delta h_r|\over t}
 \right\}.                                                \tag{270.3}
\]

The first channel measures relative displacement along the running coupling.
The other channels subtract that displacement before measuring shape. Thus
(270.3) is not a diagonal coefficient norm. Its domain is the full-tail space
on which the displayed supremum is finite. The harmless decaying weights
include all bounded log-Casimir profiles; no conclusion below depends on their
particular values.

Equivalently, for two nearby positive points `c,d`, use the recentered distance

\[
 D_b(c,d)=\max\left\{
 {|h_r(c)-h_r(d)|\over t},
 \sup_{j>r}2^{-2j}
 {|[h_j(c)-h_r(c)]-[h_j(d)-h_r(d)]|\over t}
 \right\}.                                                \tag{270.4}
\]

This is the finite-difference form of (270.3). On the Wilson ray one may take
`b=c(beta)`; the target reference is the exact image `Rb`, not an assumed
Wilson point at a fitted coupling.

## Exact test

Equation (270.1) gives, without linearization,

\[
 h_j(Rc)=4h_j(c).                                         \tag{270.5}
\]

The target running scale is consequently

\[
 t'=h_r(Rb)=4h_r(b)=4t.                                  \tag{270.6}
\]

Every numerator in (270.4) is multiplied by four, including every recentered
shape numerator, while its denominator is also multiplied by four. Therefore

\[
 \boxed{D_{Rb}(Rc,Rd)=D_b(c,d)}.                          \tag{270.7}
\]

The same equality holds for the tangent norm. Small one-character variations
of a Wilson point remain admissible by the positivity argument of Cycle 264,
so (270.7) has nonzero admissible test pairs. Hence no `rho<1` can satisfy

\[
 D_{Rb}(Rc,Rd)\leq \rho D_b(c,d)                          \tag{270.8}
\]

on any such neighborhood. The tested norm turns the previous multiplier four
into an exact isometry, not a contraction.

This outcome is structural rather than a bad choice of the displayed tail
weights. If the denominator `t` in (270.3) is replaced by `t^alpha`, exact
homogeneity gives the factor

\[
 4^{1-\alpha}.                                            \tag{270.9}
\]

Thus `alpha=0` recovers expansion by four, the dimensionless relative choice
`alpha=1` gives (270.7), and `alpha>1` manufactures contraction solely by
making the target norm smaller under the prescribed rescaling. Such a norm is
singular beyond relative scaling as `t->0`: perturbations of the natural size
`delta h=O(t)` have size `O(t^(1-alpha))`. It supplies neither a uniform UV
neighborhood nor dynamical suppression of a shape channel. This normalization
artifact is not accepted as an RG contraction mechanism.

## Four-dimensional transfer gate

The only positive lesson that can transfer is organizational: quotienting a
running coupling direction from shape directions is a legitimate way to state
a stability estimate. The contraction mechanism itself cannot transfer from
this test, for two independent reasons.

1. In two dimensions, axial-tree integration makes the map componentwise and
   exactly homogeneous. Recentring cancels that common homogeneity and leaves
   every shape direction neutral. There is no residual smoothing to export.
2. A four-dimensional exact block map generates coupled multi-plaquette and
   multi-representation interactions. It has neither the product factorization
   behind (270.1) nor the identity (270.5). A useful four-dimensional theorem
   would have to prove that the derivative normal to a running renormalized
   trajectory is strictly smaller than the trajectory's scale change in a
   norm controlling all generated polymers. That would be new input, not a
   consequence of (270.7).

## Decision

`Y270-RECENTER-NORM: EXACT ISOMETRY / STRUCTURAL IRRELEVANCE WALL.` The one
coupling-dependent, recentered, non-diagonal log-Casimir norm (270.3) removes
the scalar factor four but yields Lipschitz constant exactly one. Stronger
power normalization creates contraction only by a UV-singular change of units.
Stop this norm. The quotient-coordinate idea may label a future 4D stability
problem, but the tested 2D mechanism supplies no 4D contraction, continuum
construction, mass gap, or Millennium claim.
