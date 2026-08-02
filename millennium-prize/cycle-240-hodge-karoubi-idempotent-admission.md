# Cycle 240: Hodge Karoubi-idempotent structural admission

## Selection

Replace the Navier genuinely-infinite-tail admission scout by one finitely
falsifiable Hodge structural gate. The target is the open Karoubi boundary left by Cycles
200--201, not another degree-one or degree-two Chow carrier.

Retain

\[
 A_0=E_i^3\times E_i^3,\qquad
 \mathcal C=\operatorname {thick}\langle F_0,\ldots,F_6\rangle,
 \qquad \xi=\sum_{k=0}^6c_k[F_k],
\]

where `F_k=O_(Gamma_(u^k))`, `u=2+i`, and

\[
 (c_0,\ldots,c_6)=
 (317131927490234375,-2073948378906250,12564289203125,
 -56707735500,27598945,3626326,-68381).
\]

For a PEL tangent direction `v`, write `o_v(E)` for the Atiyah--Kodaira--
Spencer obstruction in `Ext^2(E,E)`. Cycles 200--201 prove nonvanishing for
finite graph-sheaf twisted complexes but leave arbitrary retracts open because
the splitting idempotent need not preserve the acyclic vertex filtration.

## Why this beats the Navier admission

Under the established lexicographic score

\[
 L=(\text{barrier crossing},\text{non-equivalence},
     \text{finite falsifiability},\text{official transfer}),
\]

this gate scores `(1,1,1,0)`. The Navier infinite-tail admission remains
`(1,1,0,1)`: its official continuation transfer is stronger, but it has no
frozen finite production object. Lexicographically the Hodge gate wins at the
third coordinate.

- **Barrier crossing:** its accepted theorem closes the exact retract loophole
  preventing the finite-cone obstruction from reaching the idempotent-complete
  category.
- **Non-equivalence:** it concerns one explicit exceptional class inside one
  graph-generated category. It neither assumes nor restates algebraicity of
  arbitrary Hodge classes.
- **Finite falsifiability:** one explicit bad projector packet refutes the
  universal theorem; every identity in that packet is finite exact algebra.
- **Official transfer:** zero. A pass is an obstruction theorem for this
  support category, not the Hodge conjecture.

The gate is new relative to the retired Hodge architectures: it does not use a
Chow line or conic, degree escalation, graph-union smoothing, complete-
intersection or Pfaffian linkage, Ferrand doubles, Fourier--Mukai relabeling,
ordinary trace/Hochschild detection, or central idempotents.

## Frozen structural gate `KI240`

The candidate theorem is

\[
 \boxed{
 E\in\mathcal C,\ [E]=\xi
 \Longrightarrow
 \exists v\in T_0S:\ o_v(E)\ne0.}
 \tag{KI240}
\]

It must be attacked through finite noncentral projector packets `(C,d,e)`, with
the following literal data.

1. `C` is a bounded finite twisted complex of finite direct sums of shifts of
   the seven `F_k`. Print every multiplicity, shift, differential matrix, and
   exact structure constant needed to multiply chain maps. The differential
   must satisfy `d^2=0` exactly.
2. `e` is a degree-zero chain map with `de=ed` and `e^2=e`. Print an exact
   splitting or exact projector data in the finite endomorphism algebra.
3. The image object `E=im(e)` has `[E]=xi`. Supply an exact Grothendieck-class
   certificate, including the proof that the chosen coordinates detect this
   equality; an alternating multiplicity vector for `C` alone is insufficient.
4. Print the nine corner cocycles `e[2]o_(v_j)(C)e` for the fixed PEL tangent
   basis and the degree-one Hom differential against which their cohomology
   classes are tested.

Every purported counterexample is therefore a finite exact object. No bound on
packet size is needed for falsifiability: one valid packet refutes `(KI240)`.
A bounded enumeration may scout for it, but exhaustion of a bound has no
acceptance or transfer value.

## Exact acceptance

`KI240 PASS` is assigned only to a proof of the universal boxed theorem. The
proof must include all three statements:

1. every object `E` of `C` is represented by a finite packet `(C,d,e)` of the
   displayed kind, with `[E]=xi` preserved under the chosen replacements;
2. a terminating filtration-normalization or invariant argument applies to
   every such noncentral `e`, not only to central, generic, bounded-height, or
   filtration-preserving projectors; and
3. the argument produces a tangent basis element `v_j` and proves
   `[e[2]o_(v_j)(C)e]!=0` by either a dual cocycle annihilating every coboundary
   or exact row reduction outside the degree-one Hom image.

The proof must specialize to and reproduce the known nonzero diagonal
obstruction for each generator `F_k`. One favorable idempotent, any finite
enumeration, numerical rank, trace, semiregularity image, or generic-open
localization is not acceptance.

## Exact rejection and wall outcomes

`KI240 FAIL` requires one explicit packet satisfying the structural identities
and `[im(e)]=xi`, together with nine exact
degree-one primitives proving

\[
 [\,e[2]o_v(C)e\,]=0
\]

for the fixed basis of all nine PEL tangent directions. This is a genuine bad
retract and refutes `(KI240)`.

`KI240 WALL` requires a proof that the proposed universal normalization reduces
to the already-open raw corner assertion without adding a strictly stronger
invariant, as happened for the Cycle 201 trace/Hochschild proposals, or an exact
counterexample to a named indispensable intermediate lemma that does not by
itself give a bad retract. Timeout, memory exhaustion, floating ambiguity, or
failure to find a conjugator is not `WALL`.

Any other outcome is `INCOMPLETE`. `FAIL` retires `(KI240)`; `WALL` retires only
the named normalization or invariant. Neither outcome retires the entire
graph-generated category or Hodge.

## Exact transfer

The transfer from `KI240 PASS` is exactly

\[
 \begin{aligned}
 &E\in\mathcal C,\ [E]=\xi
   \Longrightarrow \exists v\in T_0S:\ o_v(E)\ne0\\
 &\Longrightarrow
 \text{no object in this graph-generated category and of class }\xi\\
 &\hspace{2.8cm}\text{deforms in all nine PEL directions}\\
 &\Longrightarrow
 \text{this graph-generated support cannot produce the required dominating
 relative object.}
 \end{aligned}
\]

This closes the Cycle 201 Karoubi boundary for this category. It only rules out
this graph-generated support mechanism. It does not
produce an algebraic representative on a very general fiber, exclude genuinely
new support, or imply the official Hodge conjecture.

There is no transfer from bounded enumeration, and no positive transfer from
`FAIL`, `WALL`, or `INCOMPLETE`.

## Stop rule

Promote Hodge to the assigned main gate now under the boxed theorem and finite
breaker protocol. The first campaign must either prove one projector-normal-
form lemma applying to arbitrary noncentral `e`, or print one exact bad packet;
bounded packet exhaustion does not close the gate. Do not revive Chow degrees
one or two, escalate to degree three, substitute trace/Hochschild or central
projectors, resume nearby BSD primary checks, or launch an unbounded Navier tail
search.

No Hodge or other Millennium problem is claimed solved.
