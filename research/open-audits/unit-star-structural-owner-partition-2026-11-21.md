# Unit-star structural owner partition: exact owner ledger, cactus closure, and the noncactus obstruction

Date: 2026-11-21. Status: **PROVED SUBFAMILY / EXACT FAIL-CLOSED OWNER LEDGER / SHARP STRUCTURAL OBSTRUCTION / NONPROMOTIONAL**.

## 1. Scope and reconstructed hypotheses

Let `G` be a finite simple connected graph with cyclomatic rank `beta(G)=7`.
Delete every physical bridge.  Suppose the positive hull of the resulting
bridge-free-component quotient is in the unresolved alternative of the exact
physical-hull reduction: after suppressing zero-rank degree-two hull vertices,
it is a star with `k` unit-rank leaves and center rank

```text
c=7-k,             1<=k<=7.
```

Each positive leaf vertex of the all-physical-bridge quotient is an actual
bridge-free component of rank one, hence is exactly a cycle; assume that every
such cycle is hostile, with length `1 mod 4`.  This quotient component must be
distinguished from a **complete detachable arm side** `U_i`: after cutting a
physical bridge on the corresponding arm, `U_i` may contain arbitrary bridge
chains and rooted trees and is a connected unicyclic graph whose unique cycle
is that leaf component.  Its marked external port may lie anywhere, including
inside an off-cycle tree.  The center is the actual complete bridge-free
component of rank `c`, not owner metadata supplied by a packet.

The following is a literal subfamily theorem.  Sections 6--9 then audit the
complete lower-rank center theorem artifacts at their exact scope and give a
finite fail-closed owner-type ledger.  The audit neither closes arbitrary
centers of ranks `2,...,6` nor the full rank-`(1,6)` marked bridge theorem.

## 2. Exact structural theorem

### Theorem (cactus-center unit stars)

If the actual bridge-free center component is a cactus, then `G` is a cactus
of cyclomatic rank seven and

```text
sigma(G)=s+(G)-|V(G)|>0.
```

This covers every center rank `c=0,...,6` subject to the literal cactus-center
hypothesis.  It includes arbitrary hostile cycle lengths `1 mod 4`, arbitrary
rooted-tree payloads, arbitrary bridge-chain lengths, arbitrary arm ports and
arbitrary center ports.  For the rank-`(1,6)` complement obtained by cutting
any arm, the conclusion is the instance-exact coupled inequality

```text
sigma(R)+Gamma(R,x;U,y) > -sigma(U).
```

### Proof

Work directly in the quotient obtained by deleting all physical bridges.
Every positive rank-one leaf component is a cycle.  Every rank-zero quotient
component is a single vertex, since a nontrivial connected rank-zero graph is
a tree and has a bridge.  By hypothesis every maximal block inside the center
component is a cycle.  Finally, every edge joining quotient components is one
of the deleted physical bridges.  It follows that every maximal block of `G`
is a center cycle, a leaf cycle, or a bridge.  Hence `G` is a cactus.  Its
cyclomatic rank is `c+k=7>=2`, so the established all-rank
nonunicyclic-cactus theorem gives `sigma(G)>0`.

Equivalently, this conclusion is insensitive to the marked arm ports.  If
`e_i` is a physical bridge whose deletion produces a complete arm side `U_i`,
then `delta_G(U_i)={e_i}`.  Every edge `f` of `U_i` outside its unique cycle is
a bridge of `U_i`.  Were `f` not a bridge of `G`, an alternate path between
its endpoints would have to leave and re-enter `U_i`, crossing the one-edge
cut `delta_G(U_i)` at least twice, which is impossible.  Thus all such edges
remain physical bridges of `G` even when the marked port lies in the
corresponding off-cycle tree.

For any selected arm `U`, let `R` be the complete induced complement and let
`Gamma=s+(G)-s+(R)-s+(U)`.  The exact identity

```text
sigma(G)=sigma(R)+sigma(U)+Gamma
```

turns strict positivity into the displayed coupled inequality. `QED`

### Corollary (all centers of rank at most one)

Every hostile unit-star state with `c<=1` (equivalently `k>=6`) satisfies the
theorem.  A bridge-free connected rank-zero component is a single vertex: a
nontrivial connected rank-zero graph is a tree and has a bridge.  A
bridge-free connected rank-one component is a cycle: a connected rank-one
graph is unicyclic and every off-cycle edge is a bridge.  Thus either center is
a cactus, and the theorem applies.

### Exact scope consequence

The hostile unit-star remainder therefore has no noncactus `c=0` or `c=1`
state, and all cactus-center states are closed at every center rank.  The only
potentially noncactus center ranks are

```text
2<=c<=6,           1<=k=7-c<=5.
```

So "at least two hostile arms" alone does **not** finish the structural route:
that condition still permits every center rank `2,...,5`.

## 3. Why a bridge-opening owner partition cannot exploit arm multiplicity alone

### Lemma (physical bridge-cut rigidity)

Let `T` be the all-physical-bridge component quotient of one of these unit-star
states.  Any vertex partition obtained solely by deleting physical bridges has
connected induced owners whose positive-rank profiles are the weight multisets
of connected components of `T-F`, for some `F subset E(T)`.  In particular,
if an owner contains positive material from two distinct arms, it contains the
center component in full.  Hence at most one owner can contain positive
material from two or more arms.

### Proof

Deleting physical bridges is exactly deleting quotient-tree edges.  Components
of `T-F` expand to pairwise disjoint, exhaustive connected induced original-
vertex territories.  The unique quotient path between any two arm leaves runs
through the center.  A connected quotient component containing both leaves
must therefore contain the center.  Since quotient components are disjoint,
only one can do so. `QED`

This proves a method limitation: an induced owner partition using only
physical bridge openings cannot pair each of several hostile arms with a
separate piece of center reserve.  At the level of positive quotient
components, one owner contains the center and some subset of the arm cycles;
every other positive-rank owner contains exactly one arm cycle, together with
whatever zero-rank material remains attached to it.  Further owners, created
by cuts inside rooted trees or by multiple cuts on suppressed chains, may be
trees.

Each single-arm positive owner is still hostile unicyclic and has only the
weak receipt `sigma(U)>=-delta_q<0`; each tree-only owner has exactly
`sigma=-1`.  Qualitative strictness elsewhere is not spendable.  Therefore no
certificate using only physical-bridge openings and the existing lower-rank
and unicyclic receipt library follows from arm multiplicity.  Further progress
requires a new mixed receipt for one retained center owner carrying several
arms, a certified opening inside the actual center component with exact debit
accounting, or marked bridge-gain analysis.  The inherited star topology alone
does not supply any of these.

## 4. Exact obstruction to the tempting `c<=5` center-opening lemma

A natural proposed structural lemma is:

> If the center has rank at most five and at least two hostile arms, one can
> split the center into disjoint induced territories, each retaining the full
> center cycle/rank needed to guard a different hostile arm.

This is false even topologically.  For each `c in {2,3,4,5}`, take the
bridge-free center

```text
C=K_(2,c+1),
```

which has `beta(C)=c`, and attach `7-c>=2` disjoint hostile `C5` arms by
physical bridges (or arbitrary bridge chains) at arbitrary center vertices.
The inherited positive hull is the required unit-star.

The center `K_(2,c+1)` is 2-connected.  More generally, in any 2-connected
center, no vertex partition can put the **complete** center positive block in
more than one territory: retaining that block literally requires every center
vertex, and distinct induced territories cannot duplicate vertices.  The
displayed family has a stronger obstruction.  Every cycle of `K_(2,c+1)` uses
both vertices in its size-two bipartition class, so at most one disjoint
territory can retain even positive center rank.  Thus there is no
topology-only operation that manufactures one center-cycle guard for each
arm.  The arm ports may all coincide or may be distinct; the obstruction is
unchanged.

This does **not** show `sigma(G)<0`, and in fact these graphs are not offered as
spectral counterexamples.  It refutes only the proposed center-rank/arm-count
owner lemma.  Any valid route for `2<=c<=5` must use one of the following extra
inputs:

* a proved mixed packet on one center owner carrying several hostile arms;
* a center-specific structural opening that destroys part of the center but
  leaves separately certified lower-rank owners, with exact debit accounting;
* or the marked reserve--bridge-gain inequality.

Center rank by itself does not authenticate any of these.

## 5. Boundary relative to the graph theorem

Proved here:

* complete closure of actual unit-star hostile states with a cactus center,
  including all `c<=1` states (`k>=6`);
* exact reduction of the remaining noncactus star schemas to `2<=c<=6` and
  at most five hostile arms;
* physical-bridge owner rigidity; and
* an explicit rank-`2,...,5` family refuting a topology-only claim that
  multiple arms or `c<=5` creates multiple intact center guards.

Not proved here:

* any universal theorem for centers of ranks `2,...,6`;
* any theorem for all marked connected rank-six complements;
* any negative spectral counterexample;
* closure of the full actual-hull-bridge lane or the connected rank-seven
  theorem.

The cactus theorem used above is
`all-nonunicyclic-cacti/paper.tex`; the structural starting point and exact
rank/ownership conventions are
`positive-square-energy/heptacyclic-general/physical-hull-bridge-reduction/theorem-note.md`.


## 6. What an exact center-owner ledger must certify

Fix one hostile unit-star state and let `C` denote its complete bridge-free
center component.  Its maximal positive-rank blocks have an integer partition

```text
lambda(C) |- c,             2<=c<=6.
```

There are exactly

```text
p(2)+p(3)+p(4)+p(5)+p(6)=2+3+5+7+11=28
```

such block-rank types.  This finite partition type is only a first index.  A
proof disposition must also say which of the following is actually available
for the physical center realization and the actual arm ports.

* `DNN(c-1)`: an exact correlation certificate
  `kappa(C)<=|E(C)|+(c-1)`, stable under every rooted payload.  This certifies
  the center itself.  It does **not** by itself certify a physical bridge arm:
  a bridge is not a one-vertex sum, and the hostile unicyclic arm can have
  negative surplus.
* `STRUCT(packet)`: a stated induced-territory packet on the complete physical
  center, including its legal opening coordinates, owner classes, rooted
  payloads, and any stated marked shared-cut demands.
* `CACTUS`: the theorem in Section 2, which is already coupled to all arms.
* `OPEN`: none of the cited theorem artifacts has the required physical-bridge
  scope.

This distinction is forced by the exact bridge identity.  If one arm `U` is
attached to `C` at original vertices `y in U`, `x in C`, then

```text
sigma(C+xy+U)=sigma(C)+sigma(U)+Gamma(C,x;U,y).
```

Neither an unmarked conclusion `sigma(C)>=0` nor a DNN certificate for `C`
alone supplies the missing lower bound on `Gamma`.  Likewise a structural
opening whose theorem was proved for a cycle meeting the center at a **shared
cut** cannot be transported across a physical bridge: the endpoints are two
distinct original vertices, and identifying them would change both the graph
and ownership.

The center-owner ledger below therefore records theorem artifacts, not a
fictional decomposition of the center into one owner per arm.  Repeated arm
ports are legal.  Distinct ports are legal.  Arbitrary bridge chains and
rooted payloads stay parameters.  No owner or cut is duplicated.

## 7. Exact finite owner-type ledger for center ranks two through six

The following table is exhaustive at the block-rank level.  `Direct` means an
exact DNN owner at the center's own rank budget.  `Structural` means only the
listed physical theorem family, at exactly the stated scope.  The final column
is the disposition after restoring one or more hostile arms by **physical
bridges**.

| `c` | `lambda(C)` | exact center theorem owner | physical hostile-arm disposition |
|---:|:---|:---|:---|
| 2 | `2` | attached theta theorem; equivalently an exact rank-two center theorem (the theta DNN excess may exceed its budget one in the exceptional family) | `OPEN` outside the cactus case; no marked physical-bridge packet is stated |
| 2 | `1+1` | cactus | `CLOSED` by Section 2 |
| 3 | `3` | exact rank-three ledger: four-path theta is direct; doubled triangle, doubled `C4`, and `K4` each have exact direct rows and exact structural rows | `OPEN` in general; the rank-three-plus-one hostile-cycle packet is a one-cycle theorem and does not cover `k=4` physical arms wholesale |
| 3 | `2+1` | complete theta-plus-cycle theorem, including its two induced residual packets | `OPEN` for the additional physical arms; this center theorem is unmarked |
| 3 | `1+1+1` | cactus | `CLOSED` by Section 2 |
| 4 | `4` | 17-kernel theorem: every physical state is direct DNN or one of the exact structural states in its physical frontier | `OPEN` in general |
| 4 | `3+1` | complete rank-three-plus-cycle ledger, including `rank3-hostile-cycle-packet.md` for the stated canonical residual families | `OPEN` for the remaining two physical arms; no theorem at arbitrary ports is stated |
| 4 | `2+2` | complete two-rank-two packet ledger | `OPEN` for the remaining three physical arms |
| 4 | `2+1+1` | complete theta-plus-two-cycle packet ledger | `OPEN` for the remaining three physical arms |
| 4 | `1^4` | cactus | `CLOSED` by Section 2 |
| 5 | `5` | 118-kernel theorem: exact DNN owners plus structural all-odd `K5-e`, K22, and K71 states at their recorded physical frontiers | `OPEN` in general |
| 5 | `4+1` | complete rank-four-plus-cycle owner ledger | `OPEN` for the remaining physical arm |
| 5 | `3+2` | complete actual-`K4`/theta residual packet plus direct rows | `OPEN` for the remaining physical arm |
| 5 | `3+1+1` | complete rank-three-plus-two-cycle owner ledger | `OPEN` for the remaining physical arm |
| 5 | `2+2+1` | complete two-theta-plus-cycle owner ledger | `OPEN` for the remaining physical arm |
| 5 | `2+1^3` | complete theta-plus-three-cycle owner ledger | `OPEN` for the remaining physical arm |
| 5 | `1^5` | cactus | `CLOSED` by Section 2 |
| 6 | `6` | complete rank-six single-block owner partition: direct DNN except all-odd K110 all-unit/one-long and canonical all-unit K223 structural states | `OPEN`; this is the `k=1` marked physical-bridge obligation |
| 6 | `5+1` | complete hexacyclic multiblock ledger: direct rows, all-odd `K5-e+T`, K22+cycle, and K71+cycle exact packets | `OPEN`; those packets concern the rank-six center before the external physical arm is restored |
| 6 | `4+2` | complete rank-four-plus-theta ledger | `OPEN` |
| 6 | `4+1+1` | complete structural-`S4`/two-cycle ledger plus direct rows | `OPEN` |
| 6 | `3+3` | complete actual-`K4`/rank-three pre-sieve plus direct rows | `OPEN` |
| 6 | `3+2+1` | complete actual-`K4`/theta/cycle pre-sieve plus direct rows | `OPEN` |
| 6 | `3+1^3` | complete rank-three-plus-three-cycle packet ledger plus direct rows | `OPEN` |
| 6 | `2+2+2` | direct DNN | `OPEN` |
| 6 | `2+2+1+1` | complete two-diamond/two-cycle packet ledger plus direct rows | `OPEN` |
| 6 | `2+1^4` | complete theta/four-cycle packet ledger plus direct rows | `OPEN` |
| 6 | `1^6` | cactus | `CLOSED` by Section 2 |

The table has exactly 28 rows and no repeated block-rank type.  It is
important that the center theorem is complete while the restored-star column
can still be `OPEN`: completeness of the unmarked lower-rank theorem is not a
marked bridge-gain theorem.

### Single-block physical owner refinements

For use in any future marked theorem, the structural single-block rows in the
table refine as follows.

| center rank | direct owner | exact non-DNN structural owner types |
|---:|:---|:---|
| 3 | excess at most two Gram rows | doubled-triangle class `111` with both doubled pairs first-simple; doubled-`C4` exceptional eight-anchor orbit with both doubled pairs first-simple; all-odd `K4` with zero or one long path |
| 4 | excess at most three Gram rows | the two no-long states in the four-vertex kernel-8 ledger, each opened to an attached all-odd `K4` packet plus one tree; all other formerly residual five- and six-vertex rows are exact DNN owners |
| 5 | excess at most four Gram rows | all-odd `K5-e` actual-`K4` or favorable-theta states at the exact residue-state split; four K22 targets retaining an actual `K4`; nine K71 targets retaining an actual `K4` and a favorable unicyclic territory |
| 6 | excess at most five Gram rows | all-unit K110, one-long K110, and canonical all-unit K223, and no other structural single-block type |

These rows are a disjoint theorem-owner classification only at the stated
physical frontiers and descendant rules.  In particular, a retained actual
`K4` must remain literal: lengthening one of its six edges moves the state to
its recorded DNN coordinate frontier, not to a widened `K4` packet.

## 8. Packet-scope audit and the stale R61 contradiction

The current file
`positive-square-energy/heptacyclic-general/r61-one-credit-boundary-reduction.md`
begins by asserting that R61 is closed when the cyclic hull contains an actual
bridge.  That sentence is stale and cannot be imported here.  It is exactly
the generic rank-one-side inference rejected by the later physical-hull
reduction: a hostile rank-one side can have negative surplus, and the
unmarked rank-six theorem supplies only `sigma>=0`.

The proved material later in that R61 file has a narrower and valid scope:

1. **shared-cut DNN gate:** the rank-six block `B` and the cycle `Q` meet at one
   original vertex `x`, and `B` has an exact excess-five Gram; one-vertex Gram
   additivity spends the cycle's one DNN unit;
2. **K110 shared-cut packets:** `Q` meets the all-unit or one-long K110 state at
   a shared cut, and the displayed original-vertex partitions retain an actual
   `K4` while assigning the cycle and path remnants once; and
3. **K223 shared-cut packet:** the marked cycle meets canonical K223 at one of
   its two marked-cut orbits, and the actual-`K4` partition pays the two
   cut-open tree territories.

None of these three statements covers two distinct bridge endpoints `x,y` or
a physical bridge chain.  Subdividing or inserting that bridge is not a rooted
one-vertex attachment to either cyclic packet.  Accordingly this audit marks
all physical R61 bridge arms `OPEN`, including the `c=6,k=1` row, and uses the
R61 packets only as bridge-free shared-cut artifacts.

The same rule governs every lower-rank artifact in Section 7.  For example,
`rank3-hostile-cycle-packet.md` genuinely covers one rank-three block plus one
hostile cycle with arbitrary bridge connectors because that scope is stated
and proved there.  It cannot be iterated over four arms while reusing the same
center vertices.  The K22/K71 and structural-`S4` packets cover exactly their
listed number and type of external cyclic demands.  They are not generic port
lemmas.

## 9. Exact residual and smallest obstruction to the proposed route

After the cactus theorem and the artifact audit, the complete unresolved
owner-type set is

```text
OPEN_TYPES =
  { every noncactus row in the 28-row table }
  = 23 block-rank types,
```

with ranks and arm counts

```text
(c,k) in {(2,5),(3,4),(4,3),(5,2),(6,1)}.
```

This set notation classifies outer theorem-owner types, not finitely many
physical graphs: path lengths, ports, bridge-chain lengths, rooted payloads,
and structural frontier coordinates remain parameters.  The five closed
partition types within the 28-row ledger are the cactus types

```text
1+1, 1+1+1, 1^4, 1^5, 1^6,
```

plus the already closed rank-zero/one center schemas from Section 2; among
`c=2,...,6`, exactly five of the 28 table rows are all-rank-one cactus rows.
All other cactus realizations whose center blocks are cycles are also closed,
even when their block-rank partition is written as `1^c`; no noncactus type is
silently removed.

The smallest exact obstruction to the requested “one guard per arm” owner
route occurs already at `(c,k)=(2,5)`: take center `K_(2,3)` and five hostile
`C5` arms.  Every center cycle uses both vertices in the size-two bipartition
class, so pairwise disjoint original-vertex territories can retain positive
center rank in at most one territory.  Five guards therefore cannot be
manufactured.  This is a counterexample to the proposed owner-partition route,
not to `s^+(G)>=|V(G)|`.

The smallest obstruction to closing the complete residual by averaging or by
a theorem that assumes at least two arms is the literal `(c,k)=(6,1)` state.
There is only one arm and hence no arm multiplicity to exploit.  The exact
one-cut ledger remains

```text
sigma(G)=sigma(R)+sigma(U)+Gamma(R,x;U,y),
```

and requires the coupled marked inequality from the physical-hull theorem.
The available R61 shared-cut packets do not apply.  Thus any complete proof
must add at least one genuinely new theorem: a marked physical-bridge theorem
for this `k=1` state, or an equivalent reserve--gain result.  Lower-rank owner
classification alone cannot remove it.

## 10. Machine-readable audit

`research/open-audits/unit-star-owner-type-ledger-verifier.py` is a
stdlib-only, dependency-free verifier for the finite bookkeeping in Sections
7--9.  It regenerates all integer partitions of `2,...,6`, requires the exact
28-key owner registry and exact 5/23 cactus/open split, checks that every
single-block structural family has a cited physical owner type, and rejects a
mutation that promotes the stale R61 physical-bridge claim.  It does not
verify the cited analytic theorems; those are theorem dependencies at their
stated scopes.

Run

```text
python3 research/open-audits/unit-star-owner-type-ledger-verifier.py
python3 -O research/open-audits/unit-star-owner-type-ledger-verifier.py
```

Both runs must be byte-identical.  This ledger is deliberately
nonpromotional: it proves the cactus subfamily and a finite fail-closed
classification of the remaining theorem obligations, not global closure.
