# Cycle 156: the smoothable clean graph pair has no derived escape

Consider the globally smoothable connected cycle

\[
\Gamma_I\cup\Gamma_D,
\qquad D=\operatorname{diag}(3,1,1).
\]

Its clean intersection is

\[
E[2]\times E^2,
\]

a disjoint union of four abelian surfaces.  The cross Ext sheaves occur in
local degrees one, two, and three with multiplicities `1,2,1`.  Globally,

\[
\dim\operatorname{Ext}^n(O_{\Gamma_I},O_{\Gamma_D})
=4(1,4,6,4,1),
\qquad1\le n\le5,
\]

and the reverse groups are identical.

Unlike transverse graph pairs, opposite degree-one arrows now exist.  However,
their Yoneda return product vanishes:

\[
\boxed{
\operatorname{Ext}^1(F_0,F_1)\otimes
\operatorname{Ext}^1(F_1,F_0)
\longrightarrow\operatorname{Ext}^2(F_i,F_i)
\text{ has rank }0.
}
\]

Locally both classes use the same unique transverse normal generator, whose
self-wedge is zero.  Shift enumeration does not create another possibility:
opposite degree-one arrows can coexist only at equal shifts, where the same
zero product applies.

The graph obstructions are

\[
\rho_0(B)=Q^{-1}B^t-B,
\qquad
\rho_1(B)=Q^{-1}B^t-DB.
\]

Their common kernel is one-dimensional, so the combined PEL obstruction has
rank eight.  More intrinsically, every cross correction is supported on the
clean intersection.  Restricting to the dense open of either graph removes all
cross arrows and forces the component obstruction to vanish there.  Therefore
intersection-supported twisted-complex terms cannot cancel a transverse ambient
failure.

The geometric smoothing has the same limitation.  Its smooth fiber is
`C_t x E^2`, with full cohomology class

\[
[\Gamma_I]+[\Gamma_D].
\]

Exact contraction of this class has rank eight and one-dimensional kernel.  Its
exceptional projection has coefficient `1+3=4` and is horizontal in all nine
Weil directions, but the balanced components carry the rank-eight obstruction.
The smooth cycle generates an abelian fourfold, so deforming it forces that
fourfold to persist; all genuinely transverse PEL directions are excluded.

Thus connectedness, global smoothing, lower-degree cross Ext, and opposite
degree-one arrows still do not produce a deforming exceptional representative.
This closes the final concrete graph-derived escape.

The dense-Hecke-orbit route also stops at a precise boundedness wall.  A fixed
uniform denominator and degree bound for effective representatives on a dense
set would force a dominating proper Chow component and generic algebraicity.
But isogeny transport grows middle-dimensional degree like the square root of
isogeny degree, while normalization creates unbounded denominators.  Density
alone does not select one finite-type Chow stratum.

The Hodge funnel is therefore rotated after preserving the special nonsplit
seed and these deformation no-gos.  No generic nonsplit Weil theorem or Hodge
solution is claimed.
