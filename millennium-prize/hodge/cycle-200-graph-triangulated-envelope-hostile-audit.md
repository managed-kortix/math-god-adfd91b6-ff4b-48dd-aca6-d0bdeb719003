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

There are two different meanings of "generated triangulatedly."  The Ext
grading was previously claimed to give a no-go for the finite twisted-complex/
finite-cone envelope.  The shifted cross-return path recorded below invalidates
that claim.  For both the finite envelope and the idempotent-complete thick
closure, the arguments in this note do not prove a no-go.

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

## Retraction of the finite twisted-complex no-go

For distinct vertices, Cycle 199 computes

\[
\operatorname {Ext}^r(F_i,F_j)=0\quad(r\ne3).
\]

After shifts, a degree-one cross-arrow from `F_i[r]` to `F_j[s]` requires

\[
3+r-s=1.
\tag{1}
\]

Equation (1) excludes a cycle returning to the same shifted cell, but it does
not exclude a return to the same vertex at a different shift.  The shortest
missed path is

\[
 F_i[0]\longrightarrow F_j[2]\longrightarrow F_i[4],\qquad i\ne j. \tag{2}
\]

Both arrows have total degree one because their underlying classes lie in
`Ext^3`.  Their product has total degree two and underlying class

\[
 \operatorname {Ext}^3(F_i,F_j)\otimes
 \operatorname {Ext}^3(F_j,F_i)
 \longrightarrow \operatorname {Ext}^6(F_i,F_i),                  \tag{3}
\]

and the post-audit input is that this product is nonzero.  Thus (2) is an exact
same-vertex cross-return channel in the degree of the obstruction.  The old
telescoping argument silently identified return to `F_i` with return to the
same shifted cell and was false.

A cell-order filtration does not repair the proof.  It places (2) in positive
filtration, so the associated graded still displays the individual graph
obstructions, but the induced spectral sequence has a possible length-two
differential or extension represented by the nonzero product (3).  Grouping
cells by vertex makes the same term a diagonal vertex contribution rather than
removing it.  Refining simultaneously by cell, shift, or bar length only moves
the term to a later page; it does not prove that the term vanishes or that the
original diagonal class is a permanent cycle.  Deciding cancellation now
requires the actual chain-level or minimal-`A_infinity` structure together with
the Atiyah cocycle and its boundary maps.

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
`rho_k(v)!=0`.  The vertex obstruction is nonzero on the associated one-vertex
graded piece, but (2)--(3) show that the present argument does not prove that it
survives in the total twisted complex.  Accordingly the formerly boxed claim

\[
E\text{ a finite graph-sheaf twisted complex},\ [E]=\xi
 \ \Longrightarrow\ \operatorname {rank}(o_E)>0
\]

is formally retracted.  The counter-path is a counterexample to the proof, not
an exhibited object with vanishing Atiyah obstruction; the displayed
implication is therefore unproved, not disproved.

## Semiorthogonal and Karoubi boundaries

The seven vertices do not form a semiorthogonal collection in either order:
both directions have large `Ext^3`.  What replaces semiorthogonality for a
fixed twisted complex is the acyclicity of its degree-one cross-arrow quiver,
which supplies an objectwise cell ordering.  Because that ordering permits the
shifted return (2), it is not enough for the claimed finite-cone obstruction and
is not a semiorthogonal decomposition of the whole category.

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

Thus this note proves neither the finite graph-sheaf twisted-complex no-go nor
the corresponding statement for every retract in the thick closure.  The
single-vertex normal obstruction and the Ext-group calculations remain, but a
total obstruction theorem needs new chain-level analysis of paths such as (2).
No `KI240` decision or Hodge-conjecture result is claimed.

## Subsequent independent repair

Cycle 245 does not revive the failed filtration argument. It restricts first to
the global punctured branch `V_k`, where every other graph cell and every cross
return vanish. Depth preserves the complete graph's normal `H^1`, and the
finite-cell supported Atiyah trace has leading value `c_k rho_k(v)`. That
separate argument proves the corrected finite theorem. The retraction above
remains the correct verdict on the original Cycle 200 proof.
