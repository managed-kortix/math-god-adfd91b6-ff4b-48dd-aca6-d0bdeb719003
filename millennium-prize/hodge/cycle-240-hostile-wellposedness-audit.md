# Cycle 240 hostile well-posedness audit

## Verdict

`KI240` is not refuted by a formal direct-sum trick.  After fixing the dg
enhancement, the deformation germ, and the Grothendieck group in which the
class equality is imposed, it is a meaningful and nonvacuous universal
statement.  It is not, however, a theorem about an invariant determined by
`[E]`.  The existing results explicitly show that the raw obstruction is not
K-theoretic, and they supply no principle forcing it to be nonzero on every
object in the fiber over `xi`.

The claimed finite falsifiability is true only in the weak witness sense: one
finite strict bad packet refutes the statement.  It is misleading if read as a
bounded, decidable, or effectively enumerable test.  Cycle 240 gives neither a
packet-size bound nor an effective exact model of all morphisms and higher
products.  The revised Cycle 241 supplies abstract finite strictification, but
not such an algorithmic exact model.

## The class does not determine the obstruction

For a first-order direction `v`, the Atiyah--Kodaira--Spencer obstruction is a
natural degree-two endomorphism

\[
 o_v(E)\in \operatorname{Ext}^2(E,E).
\]

There is no common target group in which `o_v(E)` and `o_v(E')` can be compared
merely from `[E]=[E']`.  Only its trace/semiregularity image factors through
the Chern character.  In the present class that image vanishes for every
object, including the known obstructed split representative.  Thus neither

\[
 [E]=\xi\Longrightarrow o_v(E)=o_v(P_D)
\]

nor any weaker K-theoretic detection statement has been established.  This
does not make `KI240` ill-formed: it is a universal assertion about all objects
in one K-fiber, not an assertion that the obstruction factors through `K_0`.
It does mean that the K-class is only a selection condition, not evidence for
the conclusion.

## Existence and the meaning of the class equality

The quantifier is nonempty.  The split object

\[
 P_D=\bigoplus_{c_k>0}F_k^{\oplus c_k}
       \oplus\bigoplus_{c_k<0}F_k[1]^{\oplus(-c_k)}
\]

is a finite object and has class `xi`; its enormous multiplicities do not
affect existence.  It is already known to be obstructed, so it is not a bad
packet.

Cycle 240 should nevertheless specify whether `[E]=xi` means equality in
`K_0(\mathcal C)`, in `K_0(\operatorname{Perf}(A_0))`, or after applying the
Chern character.  These are not interchangeable.  Cohomological independence
of the seven graph classes proves independence of their span, but it does not
make the Chern character injective on every new Karoubi summand.  In
particular, checking seven Euler multiplicities or `ch(E)=ch(xi)` need not
certify equality in the intended integral Grothendieck group.  A valid packet
must use an explicitly named group and an actual equality there.

## Direct sums, zero-class additions, and retracts

An acyclic perfect complex is zero in the derived category, so adding it does
not change either the object or its obstruction class.  A contractible summand
can change chain-level matrices but not the resulting Ext class.

For a nonzero object `Q`, the zero-K-class pair `Q\oplus Q[1]` is different:

\[
 [Q\oplus Q[1]]=0,
 \qquad
 o_v(Q\oplus Q[1])=o_v(Q)\oplus o_v(Q)[1].
\]

Consequently `P_D\oplus Q\oplus Q[1]` still contains the nonzero `P_D`
corner.  Zero-class stabilization therefore demonstrates failure of
K-determination but does not produce an unobstructed object of class `xi`.

The genuine formal failure is the converse retract implication.  If
`C=E\oplus E'`, then

\[
 o_v(C)=o_v(E)\oplus o_v(E').
\]

The known split object makes this failure completely explicit: take
`C=P_D=0\oplus P_D` and project onto its zero summand.  For a direction in which
`P_D` is obstructed, `o_v(C)\ne0` while the selected corner is zero.  More
generally, any decomposition with `o_v(E)=0` and `o_v(E')\ne0` has the same
effect.  This is exactly the corner left open by Cycle 201.  It is not a
counterexample to `KI240`, because the zero retract does not have class `xi`;
one must still construct an unobstructed `E` inside the specified category with
`[E]=xi`.  No such object is presently given.

## Strict projector packets

For a strict closed idempotent chain map `e` on `C`, with image `E`, the corner
complex

\[
 e\operatorname{Hom}^\bullet(C,C)e
\]

computes `\operatorname{Ext}^\bullet(E,E)`, and the corner of the obstruction
represents `o_v(E)`.  If `e[2]o_v(C)e=D(h)` in the full Hom complex, then
`ehe` is a corner primitive, because `De=0` and `e^2=e`.  Thus the proposed
corner test is correct once a strict split model has been supplied.

What does not follow just from the definition of `thick` is the literal packet
format in Cycle 240.  A retract is initially represented by an idempotent in
the homotopy category.  Chain representatives generally satisfy `e^2-e=Dh`
rather than strict equality.  Passing to a finite strict idempotent after
replacement or contractible stabilization requires a strictification theorem
for the chosen dg enhancement.  Cycle 240 lists this as part of `PASS`, but its
unqualified assertion that every counterexample is already a finite exact
packet assumes the same point.  Until strictification is cited or proved, the
packet protocol may miss homotopy-idempotent retracts.

There is a second presentation issue: a finite-dimensional Ext table is not by
itself an exact finite dg or `A_infinity` model.  To make packets mechanically
checkable one must fix the ground field/model, bases for all required Hom
spaces, the Hom differential and composition (and any transferred higher
products), and an exact encoding of their structure constants.

## Tangent basis

The basis reduction is valid provided the following data are stated:

1. `T_0S` is the nine-dimensional vector space `M_3(C)` for the fixed PEL germ;
2. the fixed basis is, for example, the nine row-major matrix units `E_ab`;
3. `v\mapsto o_v(E)` is linear over the stated ground field.

Under these hypotheses, `o_v(E)=0` for all `v` if and only if the nine basis
classes vanish.  Nine corner primitives therefore certify a counterexample.
The Cycle 240 file refers to a fixed basis without displaying it, so a packet
is not literally self-contained until that convention is imported or printed.

## Correct status of finite falsifiability

The safe claim is:

> Subject to finite strictification and an exact dg encoding, a single finite
> bad projector packet is a certificate that refutes `KI240`.

The stronger impressions are unsupported:

- there is no a priori bound on the size or coefficients of a bad packet;
- failure of every packet up to any bound has no logical value;
- no terminating enumeration of all exact packets is specified;
- exact equality over `C` is not an algorithmic test without a fixed
  computable field of definition;
- the K-class certificate for arbitrary retracts has no defined complete
  coordinate system.

Accordingly, the score `(1,1,1,0)` uses "finite falsifiability" in a very weak
Popperian sense shared by many universal statements over finite presentations.
It does not give a finite campaign or a decision procedure.  Even after the
Cycle 241 pass, the finite-falsifiability coordinate means witness
verifiability, not bounded decidability.

## Cycle 241 strictification repair

The subsequently added connective normal-form proposal addresses the right
issue: nonnegative Ext degrees and semisimple degree zero plausibly imply that
the finite pretriangulated hull is Karoubian.  If Theorem 241.A is supplied as a
correct theorem with its hypotheses matched to the chosen enhancement, then it
repairs the principal packet-coverage objection and reduces `KI240` to Cycle
200.

The revised Cycle 241 now fills this particular gap.  In the finite filtered dg
endomorphism algebra, start with `a^2-a=d h`.  The explicit recursion

\[
 a' = a+(1-2a)(a^2-a),\qquad
 (a')^2-a'=-3(a^2-a)^2+4(a^2-a)^3
\]

squares the filtration order of the defect and prints a primitive for the new
defect.  Nilpotence therefore gives a strict closed idempotent after finitely
many steps.  The finite conjugator
`u=ep+(1-e)(1-p)` then carries it to its diagonal scalar symbol; its inverse is
a terminating geometric series.  This addresses an arbitrary idempotent in
`H^0 End(C)`, not only a strict projector supplied in advance, and does not
assume an infinite telescope or unprinted coherent homotopies.

The exactness claim also remains separate from abstract existence.  Transfer
to a minimal `A_infinity` model over `C` need not provide printable computable
structure constants unless a field of definition, contraction data, and the
finitely used higher products are explicitly fixed.  Thus Cycle 241 supplies
the abstract finite strictification needed for `KI240 PASS`, but it does not
turn arbitrary complex structure constants into an effective machine-readable
packet.  That stronger algorithmic reading of Cycle 240 remains unsupported.

## Hostile endpoint

There is no formal counterexample to the actual boxed theorem in the audited
data.  There is a formal counterexample to the tempting categorical inference
that nonzero obstruction of an ambient finite cone forces nonzero obstruction
of each retract.  The remaining theorem is well-posed after the stated repairs
and nonvacuous.  The revised Cycle 241 supplies the previously missing finite
homotopy-idempotent strictification; regardless, the advertised algorithmic
character remains weaker than the strategic score suggests.
