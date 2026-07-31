# Cycle 201: retract-natural obstruction audit

## Question and scope

Retain the Cycle 200 notation

\[
 \mathcal C=\operatorname {thick}\langle F_0,\ldots,F_6\rangle
 \subset \operatorname {Perf}(A),\qquad
 \xi=\sum_{k=0}^6c_k[F_k].
\]

Cycle 200 proves that every finite graph-sheaf twisted complex of class `xi`
has nonzero first-order Atiyah obstruction, but its filtration need not descend
to an arbitrary retract.  This note asks whether categorical trace, Hochschild
support, deformation base change, or central idempotents closes that gap.

The exact answer is negative for all trace/Hochschild and central-splitting
versions of the proposal.  There is an intrinsic retract-natural invariant,
namely the untraced corner of the Atiyah obstruction, but it is exactly the
unknown obstruction and is not determined by the K-class.  Thus these
categorical formalisms do not prove the desired universal statement.

## The intrinsic corner theorem

Let `R=k[epsilon]/(epsilon^2)` encode a first-order deformation direction `v`
of `A`, and let

\[
 o_v(E)\in\operatorname {Ext}^2_A(E,E)
\]

be the usual product of the Atiyah class with the Kodaira--Spencer class.
The Atiyah class is a natural transformation.  Consequently, if

\[
 E\mathop{\longrightarrow}^{i}C
 \mathop{\longrightarrow}^{p}E,\qquad pi=1_E,
 \quad e=ip,
\]

then

\[
 o_v(C)i=i[2]o_v(E),\qquad
 p[2]o_v(C)=o_v(E)p,
\]

and hence

\[
 \boxed{o_v(E)=p[2]o_v(C)i.}                                      \tag{201.1}
\]

Equivalently, under the canonical decomposition `C=E direct-sum E'`,

\[
 o_v(C)=o_v(E)\mathbin\oplus o_v(E').                              \tag{201.2}
\]

This proves both preservation statements that are actually valid:

1. a retract of an unobstructed object is unobstructed;
2. if a retract is obstructed, then every ambient object containing it is
   obstructed.

The converse needed here is false as a categorical principle: a nonzero
endomorphism of a direct sum can have zero corner on one summand and nonzero
corner on the complement.  Therefore nonvanishing of the diagonal obstruction
of a filtered ambient twisted complex does not imply nonvanishing of every
retract corner.  Equation (201.1), rather than filtration preservation, is the
complete retract-natural statement.

There is also a deformation-category formulation.  An object `E` lifts to the
first-order deformation precisely when its classifying map factors through the
base-change category; the primary obstruction to that factorization is
`o_v(E)`.  Base change therefore repackages (201.1), but does not make
liftability a function of `[E]`.  Lifting a chosen ambient object and lifting
its splitting idempotent would suffice, but neither lift is supplied by the
special-fiber K-class `xi`.

## Exact failure of trace and Hochschild detection

For a smooth proper variety, the categorical trace/semiregularity image of the
Atiyah obstruction is determined by the Chern character.  In standard
notation, its components have the form

\[
 \sigma(o_v(E))=\iota_v\operatorname {ch}(E)                       \tag{201.3}
\]

up to the conventional Todd-class identification between Hochschild and Hodge
cohomology.  In particular, (201.3) factors through `K_0(A)` and is additive
under direct sums and triangles.

For every `E` with `[E]=xi`, Cycle 200 gives

\[
 \operatorname {ch}_3(E)=D_0\alpha _0,
\]

There are no hidden higher Chern-character components here.  Both `A` and each
graph are abelian varieties with trivial tangent bundles, so Grothendieck--
Riemann--Roch for `Gamma_k -> A` gives

\[
 \operatorname {ch}(F_k)=[\Gamma_k].
\]

Thus `ch(E)=D_0 alpha_0` is pure of codimension three, and this class is
horizontal on the selected nine-dimensional PEL tangent space.  Hence

\[
 \sigma(o_v(E))=0\qquad(v\in T)                                   \tag{201.4}
\]

in the relevant degree.  The split signed graph object already has nonzero raw
Atiyah obstruction while satisfying (201.4).  It is therefore an explicit
witness that categorical trace, the ordinary Hochschild Chern character, and
every linear functorial image of those classes fail to detect even the known
nonzero obstruction in this K-class.

Inserting the retract projector does not improve this.  Cyclicity gives

\[
 \operatorname {Tr}_C(e\,o_v(C))=\operatorname {Tr}_E(o_v(E)),
\]

which is again (201.3) for `[E]=xi` and hence vanishes.  Keeping the full
untraced element `e[2]o_v(C)e` avoids this loss, but under the identification
of the corner with `Ext^2(E,E)` it is exactly `o_v(E)`.  This is a tautological
reformulation, not a new K-theoretic detector.

The evident Hochschild-support refinement does not repair the issue.  Localizing
at the generic point of a graph separates K-classes, but the graph's normal
obstruction lies in a global `H^1(N)` group and can vanish on an affine
restriction.  Thus generic-support localization retains the same local/global
gap identified in Cycle 200.  A genuinely global supported Hochschild theory
equipped with a projector-sensitive injectivity theorem would be additional
input; it is not a consequence of the support filtration or the ordinary
Hochschild Chern character.

## Central idempotents cannot recover the vertices

One might try to replace the noncentral splitting projector by canonical
central projectors onto the seven graph vertices.  Such projectors do not
exist.

Indeed,

\[
 \operatorname {End}^0(F_k)=k,
\]

so a degree-zero central idempotent acts on each `F_k` by a scalar
`lambda_k` in `{0,1}`.  For every `i!=j`, Cycle 199 gives a nonzero group

\[
 \operatorname {Ext}^3(F_i,F_j).
\]

Naturality of the central transformation on a nonzero element of this group
forces `lambda_i=lambda_j`.  The graph of generators is complete, so all seven
scalars coincide.  Since the `F_k` thickly generate `C`, the central idempotent
is consequently either zero or the identity on all of `C`.  Thus the center
provides no vertexwise summands with which to retain the Cycle 200 filtration.
An idempotent defining a particular Karoubi summand is necessarily an
object-level, generally noncentral projector, and its obstruction corner is
again governed only by (201.1).

## Impossibility theorem for the proposed data

Combining the preceding facts gives the precise endpoint.

**Theorem.**  On the full PEL tangent space, no obstruction invariant that
factors through the ordinary K-class by categorical trace, Hochschild Chern
character, their linear functorial images, or central idempotent decomposition
can prove

\[
 E\in\mathcal C,
 \quad [E]=\xi
 \quad\Longrightarrow\quad o_E\ne0.                              \tag{201.5}
\]

The trace/Hochschild candidates vanish on every object of class `xi`, including
a known obstructed split object, and the category has no nontrivial central
idempotent separating the graph generators.  Deformation-category base change
is equivalent at first order to testing the untraced class `o_E`; it supplies
no K-class criterion.  Therefore K-theory, the Cycle 199 Ext grading, and the
four proposed categorical devices do not decide (201.5).

This is an impossibility result for those methods, not a counterexample to
(201.5).  The universal retract statement itself remains open.  Closing it
requires genuinely nonadditive information about every splitting projector,
for example a classification of degree-zero idempotents in finite graph
twisted complexes together with a proof that every `xi`-corner meets a nonzero
Atiyah block.  Without such a projector theorem, the finite-cone no-go cannot
be promoted to the Karoubi envelope.  No Hodge-conjecture result is claimed.
