# Cycle 292: Type-II discriminants, graph rigidity, and the remaining census wall

## Scope and binary verdict

Cycle 291 reduced the proposed passage from the all-self-powers theorem for
discriminant-one Weil fourfolds to arbitrary finite mixed products to two
requirements:

1. literal embedded derived independence (`DI`) after consolidating simple
   isogeny supports; and
2. exact algebraic quotient bridges (`QB`) for every nonsemisimple support.

The `QB` construction and conditional Lemma 291.C survive audit.  This cycle
records conditional fixed-graph implications for the identified Type-III
outer-`D_2`, outer-`A_2`, standard outer-`A_3`, II(1), and II(2) packets,
corrects the reading of Moonen--Zarhin section 2.5(ii), and settles the omitted
Type-II determinant calculations.

**Binary verdict: the mixed-product theorem is still not proved.**  Two
families omitted from the old support inventory really survive the balanced
discriminant-one locus:

- every simple Type-II(1) fourfold, with center `Q` and `D`-rank two, carries
  an intrinsic balanced compatible imaginary-quadratic action and has Weil
  discriminant one;
- a simple Type-II(2) fourfold, with real-quadratic center and `D`-rank one,
  has discriminant class equal to the corestriction class of its quaternion
  algebra, and explicit division supports with split corestriction exist.

For each identified Type-II packet, an actual rational adjoint graph carrying
the exact parametrized projected Hodge circle forces isogeny; the obvious
simple-division/surface cross-graphs are blocked by rational Tits classes.  Moonen--
Zarhin Theorem 0.1(iv) supplies the expected actual Hodge group uniformly for
every simple Type-II fourfold, including special members; this is not a
generic-PEL assertion.  What is still missing is an exhaustive rational
support/packet census for every possible simple support and every isotypic
matrix embedding of the Weil field, together with independently checked
rational Tits/packet descent and projected-circle data in each surviving row.
Therefore `DI` remains fail-closed until that census is finished and every
same/cross rational packet coincidence is checked.  Nothing here proves a new
mixed Hodge-conjecture case, a Clay result, or a publication result.

## 1. Correct reading of Moonen--Zarhin

Section 2.5(ii) of Moonen--Zarhin says that for a simple fourfold one sometimes
needs Weil classes in addition to divisors, that this happens in Type III, and
that the same **exceptional-Weil phenomenon** can otherwise occur only in
Types IV(1,1) and IV(4,1).  The antecedent of “This happens” is the need for
extra generators, not the mere existence of a balanced imaginary-quadratic
action.

This reading agrees with their separate balance and exceptionality tests.
Their balance remark says that, for simple factors of Albert Types I--III,
every subfield of the endomorphism algebra acts with equal conjugate
multiplicities.  The associated Type-II Weil classes are decomposable, not
absent.  Consequently Cycle 291's use of section 2.5(ii) to delete Type II
from the balanced census is retracted.

MZ notation is also essential.  Type II(`e_0`) has totally real center `F` of
degree `e_0` and a totally indefinite quaternion algebra `D/F`.  Hence:

- II(1), `g=4`: `F=Q`, `dim_Q D=4`, and `H_1` has left-`D` rank two;
- II(2), `g=4`: `[F:Q]=2`, `dim_Q D=8`, and `H_1` has left-`D` rank one.

These are different rational groups and have different discriminant formulas.

## 2. The fixed-graph rigidity mechanism

Suppose an actual Goursat graph in a joint Hodge group gives a rational adjoint
isomorphism

\[
 \alpha:G_1^{\mathrm{ad}}\xrightarrow{\sim}G_2^{\mathrm{ad}}
\]

carrying the projected Hodge circle **with its parameter**.  Equality only of
circle images, or equality up to real conjugacy or inversion, is insufficient.
Lift `alpha` uniquely to the simply connected covers and pull the second
rational `H^1` module back along this fixed lift.

Let

\[
 H=\operatorname{Hom}_{G_1^{\mathrm{sc}}}
   (V_1,\widetilde\alpha^*V_2).
\]

Equivariant Hom is the kernel of linear comodule equations and therefore
commutes with flat base change.  If the fixed pulled-back geometric modules
are isomorphic, `H_Qbar` contains an invertible intertwiner.  The determinant
restricted to the rational vector space `H` is then a nonzero rational
polynomial.  Since `Q` is infinite, it has a rational nonvanishing point, so
there is a rational invertible derived intertwiner `f`.

Put `J_2'=f^{-1}J_2f` and `Delta=J_2'-J_1`.  Differentiating exact equality
of parametrized projected circles shows that `Delta` commutes with the lifted
derived action, so `Delta` lies in the full represented derived commutant
`C_1`.  One must also prove, as represented subalgebras,

\[
 f^{-1}C_2f=C_1=\operatorname{End}_{\mathrm{HS}}(V_1).
\]

Only then do both `J_1` and `J_2'` commute with all of `C_1`, making `Delta`
central.  Merely knowing `Delta` lies in the commutant, or merely knowing the
commutants are abstractly isomorphic, would not prove centrality.  In the
Type-II rows below, Moonen--Zarhin Theorem 0.1(iv) gives
`Hg=Sp_D(V,phi)`.  Together with section 1.2---semisimplicity in the absence
of Type-IV factors and
`End_Q(V)^{Hg}=End^0(A)` as represented subalgebras---this implies that `Hg`
is the represented image of its derived/simply connected cover and that the
full centralizer of the represented simply connected action really is
`C_i=End_Hg(V_i)=End_HS(V_i)=End^0(A_i)`, not merely a larger derived
centralizer.  The intertwiner identifies these full centralizers by
conjugation, and their center
is `Q` or a totally real field `F`.  Componentwise `Delta=cI` for a real scalar
`c`; then

\[
 (J_1+cI)^2=J_1^2=-I
\]

forces `c=0`.  Thus, for each identified Type-II packet, any actual rational
adjoint graph transporting the parametrized projected Hodge circle forces a
rational weight-one Hodge isomorphism and hence an isogeny.

The same determinant-open strategy applies to the previously audited
same-Type-III, outer-`A_2`, and standard outer-`A_3` rows only after their own
represented commutant centers and central-correction equations are checked;
they do not inherit the Type-II real-scalar sentence formally.  Their geometric
packets are respectively
`2(Std_2 boxtimes Std_2)`, `Std_3 plus Std_3^dual`, and
`Std_4 plus Std_4^dual`, invariant under the allowed node actions.  Every such
statement is a fixed-graph implication, not an assertion that the exhaustive
support census has already produced or eliminated all graphs.

The argument uses the fixed rational graph and the actual rational modules; it
does not infer descent merely from absolute root type.

## 3. Simple Type II(1): universal discriminant one

Let `A` be a simple Type-II(1) fourfold,

\[
 D=\operatorname{End}^0(A)
\]

an indefinite quaternion division algebra over `Q`, and
`V=H_1(A,Q)` of left-`D` rank two.  Choose a polarization and let `tau` be its
positive orthogonal Rosati involution on `D`.  The anti-fixed line

\[
 D^- = \{x\in D:\tau(x)=-x\}
\]

has rational dimension one.  A nonzero `i` in this line has
`i^2=-d<0`; hence `K=Q(i)` is imaginary quadratic and the chosen polarization
is already `K`-compatible.  The action is balanced `(2,2)`.

Write

\[
 D=K\oplus Kj,\qquad jz=\bar z j,\qquad j^2=b>0,
\]

with `tau(i)=-i` and `tau(j)=j`.  Every alternating form on `V=D^2` whose
adjoint on the left `D`-action is `tau` has a unique `tau`-skew-Hermitian
coefficient matrix

\[
 C=
 \begin{pmatrix}
  q_1 i & u\\
  -\tau(u)&q_2 i
 \end{pmatrix},
 \qquad q_1,q_2\in\mathbb Q,
\]

where

\[
 u=z_0+z_1i+w_0j+w_1ij.
\]

On the left-`K` basis `(e_1,je_1,e_2,je_2)`, direct expansion of van Geemen's
associated four-dimensional `K`-Hermitian Weil form gives

\[
 \det_K H_C
 =16b^2d^2
  \bigl(-bdw_1^2-bw_0^2-dq_1q_2+dz_1^2+z_0^2\bigr)^2. \tag{292.1}
\]

The right side is a rational square, hence a norm from `K`.  Therefore every
nondegenerate compatible form, and in particular every compatible
polarization, has

\[
 \delta(A,K)=1
 \quad\text{in}\quad
 \mathbb Q^\times/N_{K/\mathbb Q}(K^\times). \tag{292.2}
\]

This is not a generic-only existence statement and does not transplant the
rank-one Type-II(2) corestriction formula.

### 3.1 Group, packet, and graph rows

Moonen--Zarhin Theorem 0.1(iv) applies to every simple Type-II(1)
fourfold: it is in none of their exceptional cases (a)--(d).  Hence the
actual Hodge group is uniformly `Sp_D(V,phi)`, is semisimple, and its represented
commutant is `End^0(A)` (up to the explicit homology/cohomology opposite
convention).  For the individual Type-II(1) support,

\[
 G_{\overline{\mathbb Q}}^{\mathrm{sc}}\simeq\operatorname{Sp}_4,
 \qquad
 V_{\overline{\mathbb Q}}\simeq\operatorname{Std}_4^{\oplus2}.
\]

The real group is split `Sp_4(R)`, while the `omega_1` Tits algebra has Brauer
class `[D]`.  The full derived commutant on `V` is the represented image of
`D` (or `D^op` in the dual/right-module convention): geometrically it is
`M_2`, and both sides have rational dimension four.

If an actual rational same-row adjoint graph occurs and transports the exact
parametrized projected Hodge circle, it lifts uniquely.  The `C_2` Dynkin
diagram has no automorphism, so the fixed pulled-back geometric module remains
`Std_4^2`.  Section 2 gives a rational invertible derived intertwiner; the
center of the commutant is `Q`, so the exact projected circle upgrades it to a
Hodge isomorphism.  Thus such a graph between two nonisogenous simple II(1)
supports is impossible.

An `End^0=Q` surface also has split real `Sp_4` and geometric standard packet,
so real form does **not** exclude a graph.  The rational Tits class does:
its `omega_1` algebra is split, whereas the II(1) class is $[D]\ne0$.
Equivalently a compatible rational standard form would force
`D\simeq M_2(Q)`, or `[D]=0`.  If `D` is allowed to split, the boundary
fourfold is isogenous
to the square of the surface and the graph can occur; this is not a simple
Type-II support.

## 4. Simple Type II(2): corestriction criterion and explicit survivors

Let `F/Q` be real quadratic, `D/F` a totally indefinite quaternion division
algebra, and `V=H_1(A,Q)` a rank-one left `D`-module.  Suppose an imaginary
quadratic field `K=Q(i)`, `i^2=-d`, embeds in `D`.  Put `L=FK` and choose a
cyclic presentation

\[
 D=(L/F,b)=L\oplus Lj,\qquad
 j^2=b\in F^\times,
 \quad jz=\bar z j,
\]

where `bar` is `Gal(L/F)` and `b` is totally positive.  The unique positive
orthogonal involution stabilizing `K` and inducing conjugation there is
$\tau=\operatorname{Int}(i)\circ *$, with `*` canonical quaternion conjugation.  The balanced
`K`-action has signature `(2,2)`.  Van Geemen's averaging lemma supplies a
compatible polarization once `(A,K)` exists; equivalently the PEL datum may be
constructed directly from the positive involution.

For a compatible alternating form, the associated `K`-Hermitian determinant
has intrinsic class

\[
 \delta(A,K)=[N_{F/\mathbb Q}(b)]
 \in\mathbb Q^\times/N_{K/\mathbb Q}(K^\times). \tag{292.3}
\]

Indeed, in an `F=Q(t)`, `t^2=m`, basis the two transfer blocks are represented
by `G(q)` and `-G(bq)`, with
`det G(r)=mN_{F/Q}(r)`.  Thus the variable polarization coefficient contributes
a norm square, while the fixed class is `N_F(b)`.  Changing `j` changes `b`
by `N_{L/F}(z)`, whose rational norm is a `K/Q` norm.  Equivalently,

\[
 \operatorname{Cor}_{F/\mathbb Q}[D]
   =[(-d,N_{F/\mathbb Q}(b))_{\mathbb Q}],
\]

so

\[
 \boxed{\delta(A,K)=1
 \iff \operatorname{Cor}_{F/\mathbb Q}[D]=0.} \tag{292.4}
\]

The class is fixed by the support, not chosen by varying compatible
polarizations.

### 4.1 Explicit split-corestriction division support

Choose a rational prime `p>0`, unramified, split in `F`, and inert in `K`, and
put

\[
 D=(FK/F,p).
\]

At every `v|p`, `F_v=Q_p`, `L_v/F_v` is unramified quadratic, and `v(p)=1`, so
`p` is not a local norm and `D_v` is division.  Thus `D` is globally division.
Because `p>0`, it is split at both real places.  Do not claim without further
Hilbert-symbol checks that the places above `p` are its only finite ramified
places; their existence already proves division.

With left coefficients `x=z+wj`, the coordinate pair `(z,w)` is left-`K`
linear.  In the alternative right-coefficient convention `x=z+jw`, use the
twist `(z,w) -> (z,bar w)`.  The induced `K`-Hermitian form is, up to a
harmless rational norm scalar,

\[
 h((z,w),(z',w'))=
 \operatorname{Tr}_{L/K}(\bar z z'-p\bar w w').
\]

For a `Q`-basis of `F`, let
`T=(Tr_{F/Q}(u_iu_j))`.  Then

\[
 \operatorname{Gram}_K(h)=T\oplus(-pT),
 \qquad
 \det_K(h)=p^2\det(T)^2
 =N_{K/\mathbb Q}(p\det T). \tag{292.5}
\]

Hence the signature is `(2,2)` and the discriminant is one.  The indefinite
Hermitian form is not itself a positive Riemann form.  Positivity is supplied
by the alternating trace form

\[
 \psi(x,y)=\operatorname{Tr}_{F/\mathbb Q}
           \operatorname{Trd}_{D/F}(x^*iy)
\]

and a `D`-linear complex structure given at each real place by right
multiplication by the appropriately signed normalized matrix representing
`i/sqrt(d)`.  Then `psi(x,Jx)>0`.  The resulting PEL domain is a product of two
upper half-planes, not the full `U(2,2)` domain.  An order-stable lattice and an
integral multiple give a polarized abelian fourfold.

Varying the two right complex structures independently makes the common real
centralizer exactly left `D_R`.  Each rational endomorphism outside `D` cuts
out a proper analytic locus; avoiding their countable union yields
`End^0(A)=D`.  Since `D` is division, the generic member is simple.  Finally,

\[
 \operatorname{Cor}_{F/\mathbb Q}[D]
 =2[(K/\mathbb Q,p)]=0,
\]

in agreement with (292.5).  Thus simple discriminant-one II(2) supports
really exist.

### 4.2 Group, packet, and graph rows

Moonen--Zarhin Theorem 0.1(iv) likewise applies uniformly to every simple
Type-II(2) fourfold and gives `Hg=Sp_D(V,phi)`.  Together with section 1.2
(semisimplicity and `End_Q(V)^{Hg}=End^0(A)`), this identifies `Hg` with the
represented derived/simply connected image and identifies the full represented
commutant with `End^0(A)`.  Its rational form and complex packet may then be
reconstructed as follows.  For a simple II(2) support,

\[
 G^{\mathrm{sc}}=\operatorname{Res}_{F/\mathbb Q}\operatorname{SL}_1(D),
\]

which is `Q`-simple but becomes `SL_2 times SL_2` over `Qbar`.  Its packet is

\[
 V_{\overline{\mathbb Q}}
 =2(U_1\boxtimes1)\oplus2(1\boxtimes U_2), \tag{292.6}
\]

and its derived commutant is the represented image of `D` (or `D^op` in the
dual/right-module convention), of rational dimension eight and center `F`.
If an actual same-row rational adjoint graph occurs and transports the
exact parametrized projected Hodge circle, it identifies the Lie-algebra
centroids and quaternion Brauer classes, lifts to simply connected covers,
and on `Qbar` is inner up to swapping the two factors.  The packet (292.6) is
swap-invariant.  Section 2 therefore yields a rational derived-module
isomorphism, and centrality in $F\otimes_{\mathbb Q}\mathbb R$ plus `J^2=-1` makes it Hodge.  Such
an exact graph between nonisogenous simple II(2) supports is impossible.

The principal cross-rows are:

- II(2) versus Type III: split--split versus split--compact real form, hence
  no rational graph;
- II(2) versus an RM surface packet: the latter has split quaternion Tits
  class, while II(2) has division class `[D]`; if `D` split, the fourfold is a
  square of the RM surface and is not simple Type II;
- II(2) versus genuine IV(2,1): the latter's non-CM real form is
  split--compact, not split--split.

No rational quotient onto a single geometric `A_1` node exists: the Galois
exchange makes `Res_{F/Q} A_1` one rational packet.

## 5. Type IV(2,1) is not balanced

Here `End^0(A)=E` is a quartic CM field and the four embedding multiplicities,
in conjugate pairs, are `(2,0)` and `(1,1)`.  If `E` is primitive, it has no
imaginary-quadratic subfield.  If it is biquadratic, label
`Gal(E/Q)={1,a,c,ac}`, with `c` complex conjugation, and write

\[
 n_1=2,\quad n_c=0,\quad n_a=n_{ac}=1.
\]

Restriction to either imaginary-quadratic subfield sums over fibers giving
`(3,1)`.  The apparent `(2,2)` grouping is restriction to the real quadratic
field.  Hence genuine simple IV(2,1) does not survive the balanced
imaginary-quadratic census.  The earlier hypothetical `(1,1)+(1,1)` argument
is retracted.

## 6. Why the theorem remains fail-closed

The following Cycle-291 components now survive audit:

1. individual all-self-powers fullness descends to algebraic-motive retracts;
2. the complete rational Weil plane in every identified `3+1` row gives the
   exact determinant quotient bridge, including the finite `mu_3` overlap;
3. the aggregate CM Hodge torus records simultaneous quotient relations;
4. Lemma 291.C correctly turns literal `DI` plus exact `QB` into joint
   fullness;
5. for each identified same-Type-III, outer-`A_2`, standard outer-`A_3`,
   II(1), and II(2) packet, an actual rational adjoint graph transporting the
   exact parametrized projected Hodge circle forces isogeny after the
   row-specific represented-commutant check; the displayed Type-II/surface
   cross rows are excluded for simple division supports, while the split
   cases are decomposable surface-square boundaries.

This still is not an exhaustive proof of `DI`.  The required final census must
start from every possible isotypic matrix embedding

\[
 K\longrightarrow M_m(\operatorname{End}^0 X)
\]

inside a Weil fourfold, consolidate repeated isogeny supports, and for every
simple support prove the actual rational derived group, rational `H^1` packet,
full derived commutant, and projected Hodge circle.  Moonen--Zarhin already
supplies the uniform actual-group and commutant statements for simple II(1),
II(2), and III(1) fourfolds; it does not by itself supply every finer rational
Tits-module identification or exact transport by an arbitrary graph.  The
remaining rows must likewise be uniform for special members, not merely
Hodge-generic PEL points.  The census must then check every same/cross rational
packet coincidence, including any remaining outer or restriction-of-scalars
rows.  Only after that table is complete may one invoke finite-family Goursat
and instantiate Lemma 291.C.

Accordingly:

- do not restore the mixed-product theorem from the repaired graph lemmas;
- do not omit II(1) or split-corestriction II(2);
- do not use real form alone for II(1) versus a split `Sp_4` surface;
- do not generalize the explicit II(2) discriminant-one example to all II(2)
  supports;
- use Moonen--Zarhin 0.1(ii),(iv), not a generic PEL argument, for the
  uniform actual Hodge groups of simple III(1) and Type-II fourfolds;
- do not replace exact parametrized-circle equality by equality of images;
- do not infer rational module descent from absolute highest weights alone.

## Sources and source limits

- Moonen--Zarhin, *Hodge classes on abelian varieties of low dimension*,
  Math. Ann. 315 (1999), 711--733, arXiv:math/9901113, especially Theorem 0.1
  and sections 1.1, 1.9, 2.5, 3, and 5.3.
- Moonen--Zarhin, *Weil classes on abelian varieties*,
  arXiv:alg-geom/9612017, especially the balance remark and Criterion 13.
- van Geemen, *An introduction to the Hodge conjecture for abelian varieties*,
  Lemma 5.2 and section 5.4, for compatible polarizations, the associated
  Hermitian form, signature, and determinant convention.
- Moonen--Zarhin, *Hodge classes and Tate classes on simple abelian
  fourfolds*, Duke Math. J. 77 (1995), 553--581.
- Floccari--Fu, *The Hodge conjecture for Weil fourfolds with discriminant 1
  via singular OG6-varieties*, arXiv:2504.13607v2, Theorem 1.2.
- van Hoften--Sempliner, *The Hodge Conjecture for CM abelian varieties*,
  hexagon:2610.00259v2, Theorem I.

The Type-II determinant formulas and the fixed-graph rigidity arguments above
were independently reconstructed and hostilely audited.  Moonen--Zarhin
Theorem 0.1(iv) proves the expected actual Hodge group uniformly for the two
simple Type-II rows; Lombardo's complexified packet descriptions support the
stated geometric multiplicities but do not, alone, prove all finer rational
Tits descent or arbitrary exact-circle transport.  The remaining limitation
is the absence, at this checkpoint, of a complete citation-grade rational
support/packet and matrix-embedding census.  The secondary source also states
that simple Type III(2) fourfolds do not exist, but the primary Shimura
pinpoint for that exact nonexistence was not located in this audit.
