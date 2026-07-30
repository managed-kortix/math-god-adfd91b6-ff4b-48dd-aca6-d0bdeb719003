# Cycle 134: collision containment and Koszul categorical gates

Two canonical continuations of the Hermitian-plane route fail exactly.  The
flat doubled-plane collision of the dependent pencil is not contained in the
characteristic-two Fermat fiber, and the alpha-visible plane's unrestricted
graded Koszul matrix factorization has the same nonzero first obstruction as
its embedded normal deformation.

## Flat collision fails at order zero

The ambient flat limit of the dependent-pencil cubics as `lambda -> 1` is

\[
Z_{\rm coll}=V(H_1,H_2,s(s+U)^2).
\]

It is a `(1,1,3)` complete intersection in projective space with fundamental
cycle

\[
[L_A]+2[L_B].
\]

However, reduction of the characteristic-two Fermat equation modulo the cubic
gives

\[
\boxed{
F_0\bmod s(s+U)^2
=sU^{32}+s^2\sum_{j=0}^{31}x_0^jx_2^{31-j}\ne0.
}
\]

The remainder has 34 terms.  Therefore the collision is not a subscheme of the
special Fermat fiber, so no divided `W_2` obstruction or relative normal map is
defined for it.  The order-ten zero of the Cycle 133 pencil obstruction at
`lambda=1` records degeneration of that distinct-plane functional, not a
collision lift.

The fundamental cycle remains alpha-visible: in the verifier encoding,

\[
P_\alpha(A)=14,\qquad P_\alpha(B)=29,
\]

and the odd-multiplicity component survives.  Visibility does not repair
zeroth-order containment.

## Unrestricted Koszul matrix factorization

Write the degree-33 Fermat polynomial as

\[
F=\sum_{i=0}^2\ell_i g_i
\]

using the three linear equations of `L_A`.  The standard Koszul matrix
factorization has parity ranks `4|4`.

For any homogeneous scalar `h`, multiplication by `h` is null-homotopic in the
Koszul endomorphism complex exactly when

\[
h\in(\ell_0,\ell_1,\ell_2,g_0,g_1,g_2)
\]

in the appropriate graded piece.  After restriction to the plane, the
degree-33 scalar boundary space is

\[
\operatorname{span}\{x_j(Ax)_i^{32}:0\le i,j\le2\},
\]

of rank nine inside the 595-dimensional target.

The genuine divided Fermat defect has 17 terms and eight surviving
middle-exponent monomials.  Exact elimination gives

\[
\boxed{\operatorname{rank}M=9},\qquad
\boxed{\operatorname{rank}[M\mid h]=10}.
\]

Thus no arbitrary graded correction of this fixed `4|4` Koszul differential
lifts it modulo four.  Categorically, this quantifies over all graded odd
endomorphism corrections, not only motions of the linear plane.  In this
specific scalar degree, however, Koszul contraction identifies its boundary
space with the existing rank-nine normal image.  It is therefore a categorical
reformulation of the Cycle 117 obstruction, not a stronger geometric theorem.

Contractible stabilization cannot kill an object-level obstruction.  A
successful off-diagonal cancellation would require a genuinely different,
already coupled matrix factorization whose target Chern character and rational
alpha-orbit component must be verified separately.

This closes the canonical collision and the fixed plane-Koszul object.  It does
not obstruct all nonreduced cycles, different matrix factorizations, relative
Chow classes, rational equivalences, or the Hodge conjecture.

Reproduce with

```sh
python3 millennium-prize/hodge/verify_cycle134_collision_and_mf.py
```

No Hodge or Millennium solution is claimed.
