# Cycle 200: hostile audit of the graph-generated triangulated envelope

## Setup

Let

\[
F_k=O_{\Gamma_{u^k}},\qquad u=2+i,\qquad 0\leq k\leq6,
\]

be the seven graph sheaves in the Cycle 151 special fiber.  Use the Cycle 152
convention

\[
\alpha _0=P_{\rm Weil}[\Gamma],\qquad
D_0q(t)=\sum_{k=0}^6c_kt^k.
\]

The corresponding K-class is

\[
\xi=\sum_{k=0}^6c_k[F_k],
\]

where, in increasing powers of the interpolation variable,

\[
(c_0,\ldots,c_6)=
(317131927490234375,-2073948378906250,12564289203125,
-56707735500,27598945,3626326,-68381).
\]

There is no extra codimension-three sign in passing from cycles to sheaves.  If
`Gamma_(u^k)` is cut out by its three graph divisors with classes
`delta_(k,1),delta_(k,2),delta_(k,3)`, its Koszul resolution gives

\[
\operatorname {ch}(F_k)=\prod_{j=1}^3(1-e^{-\delta_{k,j}}),
\qquad
\operatorname {ch}_3(F_k)=\prod_{j=1}^3\delta_{k,j}
=[\Gamma_{u^k}].
\]

Hence the exact relation is

\[
\operatorname {ch}_3(\xi)=\sum_{k=0}^6c_k[\Gamma_{u^k}]
=D_0\alpha _0.
\tag{0}
\]

The coefficient vector previously displayed here was `(-c_0,...,-c_6)` and
therefore defined `-xi`, whose degree-six Chern character is `-D_0 alpha_0`.
That global sign does not affect the no-go below, because its proof uses only
that each vertex Euler multiplicity is nonzero; nevertheless, `xi` rather than
`-xi` is the target represented by the Cycle 153 split projector object and by
the Cycle 196 divisor-cube formula.

Indeed, Cycle 152's exact interpolation check evaluates
`sum_k c_k lambda_p^k` to `D_0` for `p=0,6` and to zero for `1<=p<=5`.
Moreover the shifted negative summands in Cycle 153 contribute minus their
classes in `K_0`, so

\[
[P_D]=\sum_{c_k>0}c_k[F_k]-\sum_{c_k<0}(-c_k)[F_k]
=\sum_{k=0}^6c_k[F_k]=\xi.
\]

Every coefficient is nonzero.  We ask whether a perfect complex assembled
triangulatedly from the `F_k` can have class `xi` and zero Atiyah obstruction on
the full nine-dimensional PEL tangent space `T`.

There are two different meanings of "generated triangulatedly."  For the
finite twisted-complex/finite-cone envelope, the Ext grading gives a no-go.  For
the idempotent-complete thick closure, the proposed K-theory and localization
argument does not by itself prove a no-go.  Keeping these scopes separate is
essential.

## K-theory is necessary but not an obstruction theory

Additivity gives

\[
[E]=\sum_k c_k[F_k]
\quad\Longrightarrow\quad
\operatorname {ch}(E)=\sum_kc_k\operatorname {ch}(F_k).
\]

The degree-six cohomological obstruction of this sum vanishes because it is the
horizontal Weil projector class.  This says only that the supertrace of the
Atiyah obstruction vanishes after semiregularity.  It does not imply that the
class in `Ext^2(E,E)` vanishes.  Conversely, K-theory additivity alone cannot
prove nonvanishing: it has forgotten the differential and extension data on
which the raw deformation obstruction depends.

A tempting stronger argument is to restrict near a generic point of one graph,
where the other six graph sheaves vanish, and retain the local class
`c_k[O_Gamma_k]`.  This is not a valid proof.  The normal Kodaira--Spencer
obstruction of a graph is a global `H^1(N)` class; restriction to a sufficiently
small affine open can kill it.  Thus support localization separates K-classes
and Ext arrows but need not retain the global Atiyah obstruction.  A Verdier
quotient by the other vertices has the same deformation-compatibility gap,
because those generators do not themselves extend over the PEL direction.

## Finite twisted-complex no-go

For distinct vertices, Cycle 199 computes

\[
\operatorname {Ext}^r(F_i,F_j)=0\quad(r\ne3).
\]

After shifts, a degree-one cross-arrow from `F_i[r]` to `F_j[s]` requires

\[
3+r-s=1.
\tag{1}
\]

There can be no directed cycle of cross-arrows.  Indeed, summing (1) around a
cycle of length `m` cancels all shifts and gives `3m=m`, impossible for
`m>0`.  Therefore the inter-vertex part of every finite twisted complex is a
directed acyclic quiver and admits a topological ordering.

Filter the twisted complex in that ordering.  Its Maurer--Cartan curvature is
upper triangular.  Every term capable of changing a diagonal vertex
obstruction would have to leave that vertex and return to it, hence would give
a directed cycle.  No such term exists.  This includes higher `A_infinity`
operations: an operation contributing to a diagonal block is represented by a
closed composable path, while the shifts telescope exactly as above.  The
diagonal obstruction is consequently the direct collection of the
single-support vertex obstructions.

At vertex `k`, the associated graded object is a finite complex built from
shifts and self-morphisms of `F_k`, with Euler multiplicity `c_k`.  At the
generic point of `Gamma_(u^k)` it is a perfect complex of generic Euler rank
`c_k`.  If it deformed in a PEL direction `v`, its codimension-three support
cycle would deform with multiplicity `c_k`; its leading semiregularity
obstruction is

\[
c_k\rho_k(v),
\qquad
\rho_k(B)=Q^{-1}B^t-N(u^k)B.
\]

The normal map `rho_k` is nonzero and `c_k!=0`, so choose `v` with
`rho_k(v)!=0`.  The vertex obstruction is then nonzero.  Upper-triangular
cross-arrows cannot cancel it.  Hence

\[
\boxed{
E\text{ a finite graph-sheaf twisted complex},\ [E]=\xi
\ \Longrightarrow\ \operatorname {rank}(o_E)>0.}
\]

The same conclusion holds for any object given by a finite iterated-cone
presentation whose associated twisted complex uses only these seven graph
vertices.  This extends the split and filtered no-go from Cycle 153 and uses
the complete cross-Ext computation of Cycles 154 and 199.

## Semiorthogonal and Karoubi boundaries

The seven vertices do not form a semiorthogonal collection in either order:
both directions have large `Ext^3`.  What replaces semiorthogonality for a
fixed twisted complex is the acyclicity of its degree-one cross-arrow quiver,
which supplies an objectwise filtration.  It is enough for finite cones but is
not automatically a semiorthogonal decomposition of the whole category.

An arbitrary direct summand in the idempotent-complete thick closure need not
come equipped with a filtration respected by the splitting idempotent.  The
global Chern obstruction of its projector K-class already cancels, and the
generic-open localization argument fails for the reason above.  Therefore the
stronger statement

\[
E\in\operatorname {thick}\langle F_0,\ldots,F_6\rangle,
\quad [E]=\xi
\quad\Longrightarrow\quad o_E\ne0
\]

is not proved solely by K-additivity, the Ext quiver, or the current
semiorthogonal tools.  To close the Karoubi envelope one would need, for
example, a deformation-compatible categorical quotient retaining each global
`H^1(N)` obstruction, or a theorem that every relevant idempotent is conjugate
to one preserving the acyclic vertex filtration.

Thus the rigorous endpoint is a no-go for finite graph-sheaf cones/twisted
complexes, not yet for every possible retract in the thick closure.  Any viable
finite-cone candidate must introduce nontransverse or genuinely new support.
No Hodge-conjecture result is claimed.
