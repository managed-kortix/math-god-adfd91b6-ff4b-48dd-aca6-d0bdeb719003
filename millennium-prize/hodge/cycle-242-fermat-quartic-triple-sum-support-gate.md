# Cycle 242: Fermat-quartic triple-sum support gate

## Selection

After closure of the graph-generated Karoubi category, select one bounded
support category which is not obtained from graphs by cones, retracts,
thickenings, linkage, determinantal or Pfaffian residuals, or Fourier--Mukai
transport.

Let

\[
 C:\ X^4+Y^4=Z^4
\]

be the smooth Fermat quartic. Its Jacobian is isogenous over a finite extension
of `Q(i)` to `E_i^3`. Fix one such isogeny, obtained from the three elliptic
idempotent factors in `Q[Aut(C)]`, and the resulting Abel--Jacobi map

\[
 \phi:C\longrightarrow E_i^3.
\]

The idempotents, the isogeny, and `phi` are part of the fixed input and must be
printed as rational maps before a candidate can pass. This prevents the phrase
"isogenous to `E_i^3`" from hiding an existence assumption.

For an ordered triple

\[
 L=(L_1,L_2,L_3),\qquad
 L_r\in M_{6\times3}(\mathbb Z[i]),\qquad N((L_r)_{ab})\leq1,
\]

define

\[
 f_L:C^3\longrightarrow A_0=E_i^6,
 \qquad
 f_L(p_1,p_2,p_3)=\sum_{r=1}^3L_r\phi(p_r).
 \tag{242.1}
\]

There are exactly `5^54` labelled triples. Let `Y_L` be the scheme-theoretic
image. The proposed new category is

\[
 \mathcal F_{242}=\operatorname{thick}
 \langle\mathcal O_{Y_L}:L\text{ passes G0--G2 below}\rangle.
 \tag{242.2}
\]

This is a Fermat-product image category, not a graph category. The bound one is
deliberately small and immutable for this scout.

## Exact exceptional class

Put `gamma=phi_*[C] in H^4(E_i^3,Z)`. The fixed rational maps for `phi` compute
all coordinates of `gamma` by exact pullback and intersection on `C`. Addition
on the abelian variety gives

\[
 z_L:=(f_L)_*[C^3]
   =(L_1)_*\gamma*(L_2)_*\gamma*(L_3)_*\gamma
   \in H^6(A_0,\mathbb Z).
 \tag{242.3}
\]

Thus every coordinate of `z_L` is an explicit integer exterior-algebra
expression in the 54 Gaussian entries. If `f_L` is a closed immersion, then
`z_L=[Y_L]`. Since `Y_L` has codimension three in the smooth sixfold,

\[
 \operatorname{ch}_1(\mathcal O_{Y_L})=
 \operatorname{ch}_2(\mathcal O_{Y_L})=0,
 \qquad
 c_3(\mathcal O_{Y_L})=2[Y_L].
 \tag{242.4}
\]

Apply the already explicit Cycle 152 interpolation projector `P_W` to (242.3).
The exceptional test is the exact nonvanishing of one of the two determinant
coordinates of `2P_Wz_L`. It does not ask for a bundle with an unspecified
exceptional `c_3`; it computes `c_3` from a fixed morphism. Hence it avoids the
Cycle 198 circularity theorem.

## Finite geometric and deformation gate

All calculations are over the fixed number field containing the maps defining
`phi`. Use projective equations for `C`, `E_i`, and (242.1), with saturated
homogeneous ideals and exact Groebner bases.

**G0 (genuinely non-graph support).** The graph ideal of `f_L` must certify that
`f_L` is a closed immersion. A passing support is then isomorphic to `C^3`, so

\[
 q(Y_L)=3g(C)=9.
\]

Every translate of an abelian graph threefold has irregularity three. Thus
`q=9` is an intrinsic certificate that `Y_L` is not a graph, a graph union, or
a graph thickening. In addition, the 924-coordinate vector `z_L` must lie
outside the span of the seven Cycle 169 graph vectors; this excludes membership
in the old graph-generated `K_0` category, rather than merely changing its
geometric presentation.

**G1 (exceptional `c_3`).** Exact exterior expansion must give

\[
 P_W(c_3(\mathcal O_{Y_L}))=2P_Wz_L\ne0.
 \tag{242.5}
\]

A certificate prints a nonzero numerator after a fixed common denominator and
the corresponding determinant basis vector. No Hodge or algebraicity
assumption enters this test.

**G2 (all nine first-order PEL directions).** From a finite locally free
resolution of the regular closed immersion, compute the relative cotangent-complex
boundary

\[
 o_L:T_0S\simeq M_3(\mathbb C)
   \longrightarrow
 \operatorname{Ext}^2_{A_0}
   (\mathcal O_{Y_L},\mathcal O_{Y_L}).
 \tag{242.6}
\]

After fixing the nine matrix units and a Cech basis on `C^3`, this is a finite
matrix over the defining number field. Admission requires every entry to be
zero. Separately, the embedded normal boundary
`T_0S -> H^1(Y_L,N_(Y_L/A_0))` must vanish, which certifies that the relative
Hilbert tangent maps onto all nine PEL directions. The Ext condition is retained
because it controls deformation of the pinned object and is not asserted to be
equivalent to the Hilbert condition. This is the requested individual rank-nine
support condition, not cancellation between signed endpoints.

**G3 (quadratic lift).** Write a first-order lift for each of the nine basis
directions and solve the 45 polarized Maurer--Cartan equations

\[
 d\eta_{ab}+\tfrac12[\eta_a,\eta_b]=0,
 \qquad 1\leq a\leq b\leq9,
 \tag{242.7}
\]

in the same finite resolution. Admission requires an exact solution and prints
all coefficients. This is only a second-order checkpoint; it is not an
all-order deformation or algebraization theorem.

## Admission and failure rule

The finite scout has only the following outcomes.

* `PASS`: one labelled triple `L` prints the fixed Fermat quotient maps, a
  closed-immersion Groebner certificate, `q=9`, graph-span nonmembership, a
  nonzero exceptional coordinate in (242.5), zero Ext and embedded-normal
  obstruction matrices, and all 45 exact lifts (242.7).
* `FAIL`: exhaustive enumeration of all `5^54` labelled triples prints a
  checkable witness at the first failed gate for each triple: a non-embedding
  ideal witness, graph-span membership, zero exceptional coordinate, one
  nonzero entry of `o_L` or of the embedded-normal boundary, or an inconsistent
  row in one quadratic lift system. Optional symmetry reduction must print the
  finite acting group, stabilizers, and a verified orbit count summing to
  `5^54`.
* `INCOMPLETE`: enumeration, quotient-map certification, or any exact rank/lift
  computation is unfinished. Numerical evidence cannot change this label.

`PASS` admits one pinned object to the all-order deformation and algebraization
gate. `FAIL` retires only this norm-one Fermat triple-sum category. Neither
outcome decides the Hodge conjecture.

## Architecture separation

The source has fixed dimension three and no rational curve in a Chow space is
used, so the retired Chow-degree-one and Chow-degree-two carrier arguments are
irrelevant. The support is the direct image of a product of positive-genus
curves, not a complete intersection, Ferrand double, liaison residual,
Pfaffian, maximal-minor locus, graph cone, Karoubi image of graph sheaves, or
Fourier--Mukai transport. Its exceptional class is obtained by the explicit
Pontryagin formula (242.3), while its deformation obstruction is computed on
the actual non-graph support. This makes `F_242` a genuinely new bounded scout,
not a renaming of a prior architecture.
