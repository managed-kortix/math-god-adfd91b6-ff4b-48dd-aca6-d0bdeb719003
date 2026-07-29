# Cycle 107: quartic-CM secant-sheaf audit

## Primary-source result

Markman, arXiv:2509.23079v1 (27 September 2025), considers a genus-four
Jacobian `X=J(C)` with real multiplication by a real quadratic field `F`, plus
an automorphism induced by a norm-one element `f in F` with `f^2 != 1`.  For
the biquadratic quartic CM field
\[
 K=F(\sqrt{-q}),
\]
the eightfold `A=X x X^` is of split Weil type and has a rational four-
dimensional exceptional space
\[
 HW(A,K)=\bigwedge_K^4H^1(A,\mathbf Q)\subset H^4(A,\mathbf Q).
\]

Using two secant sheaves and an Orlov transform, the paper constructs a derived
object `E` of nonzero rank.  Its normalized degree-four Chern component is
\[
 \kappa_2(E)=\operatorname{ch}_2(E)-\frac{c_1(E)^2}{2\operatorname{rk}E}.
\]
Lemma 11.2.8 proves that this algebraic class has nonzero projection to
`HW(A,K)`.  Thus the special base eightfold already has an explicit
determinant-bearing algebraic seed.  The flat class remains Hodge throughout
the relevant deformation component.

The missing statement is algebraic deformation, not determinant projection.
Markman explicitly leaves the required semiregularity unresolved; no family-
wide Hodge theorem follows in the preprint.

## Exact semiregularity certificate

For the genus-four secant sheaf `F_2`, the relevant generalized obstruction map
is
\[
 ob_{F_2}:HT^2(X)=H^2(\mathcal O_X)\oplus H^1(T_X)
 \oplus H^0(\wedge^2T_X)\longrightarrow\operatorname{Ext}^2(F_2,F_2).
\]
The Buchweitz--Flenner map has components
\[
 \xi\longmapsto
 \left(\operatorname{Tr}\xi,
 \operatorname{Tr}(\xi\operatorname{At}(F_2)),
 \tfrac12\operatorname{Tr}(\xi\operatorname{At}(F_2)^2)\right).
\]
Its composition with `ob` is contraction by `ch(F_2)`.  The open condition is
injectivity on `im(ob)`, equivalently
\[
 \ker(ob_{F_2})=
 \ker\bigl(HT^2(X)\xrightarrow{\lrcorner\,\operatorname{ch}(F_2)}
 H^2(\mathcal O_X)\oplus H^3(\Omega_X^1)\oplus H^4(\Omega_X^2)\bigr).
\]
Both deformation source and cohomological target have dimension `28`, so after
choosing explicit data the claim is an exact finite rank/kernel certificate.

The cohomological contraction matrix is directly symbolic in the exterior
algebra of `H^1(X)`.  The Ext/Atiyah matrix is not currently reproducible from
the paper: the sheaf uses sufficiently large unspecified multiples, generic
translates, an effective curve, and gluing data, with no explicit RM curve,
resolution, or invariant Ext complex.

## Decision

This is a genuine bounded open Hodge lemma with a stronger starting position
than the nonsplit sixfold: the nonzero exceptional algebraic seed is already
proved.  It is not promoted because no explicit finite arithmetic-geometric
instance instantiates the `28`-column certificate.  Promotion requires either
an explicit equivariant locally free resolution and exact rank computation, or
a structural proof of the kernel equality.  No new Hodge case is claimed.
