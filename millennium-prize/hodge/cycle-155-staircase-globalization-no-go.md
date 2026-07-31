# Cycle 155: the staircase determinant does not globalize

The Cycle 154 staircase union is a valid connected effective cycle with nonzero
exceptional projection, but the claimed local determinantal presentation was
incorrect.  Its ideal is the initial ideal, not the maximal-minor ideal, and
the evident global Eagon--Northcott smoothing is obstructed by Picard labels.

Locally put `a_j=y_j-2x_j`, `b_j=y_j-x_j`.  The four graph ideals are

\[
(b_1,b_2,b_3),\quad(a_1,b_2,b_3),\quad
(a_1,a_2,b_3),\quad(a_1,a_2,a_3).
\]

Their reduced union has squarefree monomial ideal

\[
J=(a_1b_1,a_1b_2,a_1b_3,a_2b_2,a_2b_3,a_3b_3).
\]

The `2x2` minors of the matrix printed in Cycle 154 instead generate

\[
D=(a_1b_1,a_1b_2,a_1b_3,a_2b_2-a_3b_1,a_2b_3,a_3b_3).
\]

Thus `J != D`.  For a term order with leading term `a_2b_2`,

\[
\operatorname{in}(D)=J.
\]

The determinantal scheme has three components, with one irreducible quadric
middle component replacing the two middle graph planes.  The staircase has four
linear components.  They have the same Hilbert series because one is a flat
Groebner degeneration of the other, not because their ideals coincide.

Replacing the corner zeros by `t` gives a flat family with smooth nonzero fiber
`G_m x A^2`, but its central fiber is `V(D)`, not the staircase `V(J)`.  Hence
it is not a smoothing of the claimed graph union.

There is also a global line-bundle obstruction.  On the `j`-th coordinate pair,
let `A_j=O(Gamma_2)` and `B_j=O(Gamma_1)`.  A global split `2x4` bundle matrix
with the displayed entries would require

\[
A_2B_2\simeq A_3B_1.
\]

This fails in the Neron--Severi group: the two sides have different nonzero
classes on different coordinate factors.  Equivalently, the compatibility
bundle

\[
\Delta=A_3B_1A_2^{-1}B_2^{-1}
\]

is nontrivial.  The prospective corner-entry bundles also have no global
sections because each contains an inverse effective graph-divisor factor.
Therefore the literal split Eagon--Northcott matrix and its corner-`t`
deformation cannot globalize.

Even abstractly, a local smoothing would not pass the Hodge gate.  On the dense
smooth opens of all four graph components, a PEL base tangent `B` must satisfy

\[
Q^{-1}B^t=M_0B=M_1B=M_2B=M_3B.
\]

Successive differences kill all three rows of `B`, so `B=0`.  Intersection-
supported smoothing parameters cannot repair failure of holomorphicity on the
dense opens.  Thus any staircase Hilbert deformation projects trivially to the
PEL tangent at first order.

A simpler global smoothable special cycle does exist:

\[
\Gamma_{\operatorname{diag}(1,1,1)}
\cup
\Gamma_{\operatorname{diag}(3,1,1)}.
\]

Its double locus is a disjoint union of four abelian surfaces with trivial
product of branch-normal lines, and it globally smooths inside a special
fourfold as `(C_1 union C_3) x E^2`.  Its exceptional coefficient is `1+3=4`.
But the ambient fourfold, graph maps, and smoothing line bundle remain on the
extra-endomorphism locus; no transverse PEL tangent follows.

This closes the staircase globalization mechanism.  It does not rule out a
different nonsplit global resolution or another connected representative of
the exceptional class.
