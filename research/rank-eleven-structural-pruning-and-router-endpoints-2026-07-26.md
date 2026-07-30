# Rank eleven without a large marked census: structural pruning and router endpoints

**Date:** 2026-07-26

## 1. Status and objective

Put

```text
sigma(G)=s+(G)-|V(G)|,  T=C3,  P=C5,
delta=sqrt(5)-2<1/4.
```

This note seeks a rank-uniform proof of the rank-eleven cactus case from the
proved rank-ten theorem. The intended replacement for a large marked census is:

1. prune the reduced shared-cut cluster tree only at actual bridges;
2. stop at a short list of marked endpoint families;
3. inside one shared-cut cluster, use only proved proper-interval router
   operations and one-pivot analytic packets.

The bridge-pruning step is proved below. It gives an exact finite endpoint list,
not a census. The genuinely new four-port shape and all nine inherited ladder
shapes are repaired with final owners; see
`research/rank-eleven-t9pp-ladder-inheritance-2026-07-26.md`. The remaining
global router assertion is isolated explicitly and is open. Therefore this
note does **not** prove the rank-eleven theorem.

The inputs used as theorems are:

```text
connected cactus of rank 2 or 3:       sigma>=0,
connected cactus of rank 4,...,10:     sigma>0,
T, TP, TQ, PP, TPP:                    the established packet bounds,
A_r, 1<=r<=10:                         sigma(A_r)>0,
common-cut T^kQ, T^kP, T^kPP:          established one-pivot bounds,
packing-one hostile arm:               established rooted bound.
```

Here `A_r` denotes one connected shared-cut cluster of `r` triangles. The
statement for `A_10` is an immediate instance of the rank-ten theorem. The
sharp-DNN reduction and the exact colored-partition list are taken from
`research/rank-eleven-conditional-frontier-census-2026-07-26.md`; they do not
require any marked incidence enumeration.

## 2. DNN frontier and actual bridge ownership

The sharp cactus DNN estimate leaves exactly

```text
T^10Q,  q>=3 (including Q=T),
T^9PP.                                                   (2.1)
```

Contract each maximal shared-cut cyclic cluster to one marked vertex in the
block-cut tree and take the minimal subtree spanning those marks. Call the
resulting marked/Steiner tree `R`. An edge of `R` records a nonempty chain of
actual bridge blocks; it is not itself treated as an analytic edge. Every
component outside the hull has one hull attachment and follows the owner of
that attachment.

Whenever a proof below cuts a reduced edge, choose an actual bridge in its
bridge chain. The two chain remnants, the two endpoints of the removed bridge,
and every branch rooted on either remnant stay with their respective sides.
The lifted sides are connected, induced, disjoint, and exhaustive. No cyclic
block is opened during this global pruning.

### Lemma 2.1 (certified leaf pruning)

Let `L` be a leaf cluster of `R`. Cutting the first actual bridge away from `L`
proves `sigma(G)>0` whenever proved bounds for the resulting connected leaf and
complement packets have positive sum.

**Proof.** The ownership convention above proves that the two packets are
genuine induced territories. Positive-square-energy superadditivity makes the
global surplus at least the sum of their proved bounds, which is positive by
hypothesis. QED.

In particular, every use below is one of the following certified combinations:
a triangular singleton plus a strict rank-ten complement; `A_7` plus a strict
rank-four complement; `A_8` plus a nonnegative rank-three complement; `A_9`
plus a nonnegative rank-two complement; or nonnegative `T^2P` plus a strict
rank-eight complement. We do not use the invalid blanket inference that an
arbitrary strict rank-ten leaf pays an otherwise uncontrolled hostile
rank-one complement.

Thus a disconnected residual can survive pruning only while every leaf mark
is a hostile singleton `P` or `Q`, except that a rank-two or rank-three leaf may
also be retained when the complement, rather than the leaf, supplies the strict
summand. The row analyses below use this stronger observation directly.

### Lemma 2.2 (two-hostile-end path)

Suppose that after all strict leaf moves the only possible leaf marks are two
specified hostile singleton cycles. Then `R` is a path with those marks as its
ends.

**Proof.** Every finite tree with at least two vertices has at least two
leaves. Under the hypothesis it has exactly the two specified leaves. A finite
tree has exactly two leaves if and only if every vertex has degree at most two,
so it is a path. QED.

All later uses of this lemma cut actual bridge chains, not formal edges of `R`.

## 3. Exact disconnected endpoints for `T^10Q`

The five structural color partitions are

```text
Q|T|T|T|T|T|T|T|T|T|T,
Q|T|T|T|A_7,
Q|T|T|A_8,
Q|T|A_9,
Q|A_10.                                                 (3.1)
```

### Proposition 3.1

Every disconnected `T^10Q` row in (3.1) has a positive actual-bridge split or
reduces to exactly

```text
E_Q = A_10 | Q.                                         (3.2)
```

The connector entry into `A_10` is one labelled interface.

**Proof.** In the first row, any singleton triangle leaf is strict and leaves a
connected rank-ten complement, also strict. If no triangle is a leaf, `Q` is
the only possible leaf, impossible for a nontrivial finite tree.

For `Q|T|T|T|A_7`, first remove a singleton-triangle leaf. If none exists,
`Q` and `A_7` are the only possible leaves, so Lemma 2.2 makes `R` a path
between them. If the first marked cluster from `Q` is a triangle, cut after it:
`TQ` and its rank-nine complement are strict. If it is `A_7`, cut after it:
the `A_7Q` side has rank eight and is strict, while the three-triangle
complement has rank three and is nonnegative.

For `Q|T|T|A_8`, the same argument gives a strict triangle leaf, a leaf `A_8`,
or a path whose leaves are `Q,A_8`. In the path case, the first mark from `Q`
is either `T`, giving strict `TQ` plus a strict rank-nine complement, or `A_8`,
giving a strict rank-nine `A_8Q` side plus a nonnegative rank-two complement.

For `Q|T|A_9`, a leaf `T` is handled by Lemma 2.1. If `A_9` is a leaf, it is
strict and its rank-two `TQ` complement is strict. If neither were a leaf,
`Q` would be the only possible marked leaf, impossible in the minimal marked
hull.

Finally `Q|A_10` has two marks and hence one reduced path. This is `E_Q`.
All cuts lift by Section 2. QED.

Consequently the only unresolved disconnected `T^10Q` family is the
one-interface endpoint `A_10|Q`.

## 4. Exact disconnected endpoints for `T^9PP`

The thirteen structural rows are

```text
P|P|9T,
P|P|T|T|A_7,
P|P|T|A_8,
P|P|A_9,
P|7T|T^2P,
P|6T|T^3P,
P|5T|T^4P,
P|4T|T^5P,
P|3T|T^6P,
P|2T|T^7P,
P|T|T^8P,
P|T^2P|A_7,
P|T^9P.                                                 (4.1)
```

### Proposition 4.1

Every disconnected `T^9PP` row in (4.1) has a positive actual-bridge split or
reduces to one of the following two finite families:

```text
E_P^0 = T^9P_0 | P_1,                                  one interface,
E_P^1 = P_0 | A_9 | P_1.                               two interfaces. (4.2)
```

**Proof.** For `P|P|9T`, remove a triangular leaf. If none exists, the two
pentagons are the only leaves, so `R` is a path. The first triangle from either
pentagon gives a strict `TP` terminal and leaves a connected rank-nine cactus,
hence a strict complement.

For `P|P|T|T|A_7`, remove a triangular leaf. If neither singleton is a leaf,
and `A_7` is a leaf, cutting `A_7` gives a strict packet and a strict rank-four
complement. Otherwise the two pentagons are the only leaves and `R` is a path.
At a pentagonal end, the next marked cluster is either `T`, giving strict `TP`
and a strict rank-nine complement, or `A_7`, giving a strict rank-eight `A_7P`
side and a nonnegative rank-three complement.

For `P|P|T|A_8`, a leaf `T` or leaf `A_8` closes the row. Otherwise `T` and
`A_8` are internal, so the two pentagons are the only leaves and `R` is a path.
Whichever of `T,A_8` is first from an end gives respectively strict `TP` plus a
strict rank-nine complement, or strict rank-nine `A_8P` plus strict `TP`.

For `P|P|A_9`, a leaf `A_9` gives strict `A_9` plus nonnegative `PP`. If
`A_9` is internal, deleting it separates the two pentagons and gives `E_P^1`.
A pentagon internal to the three-mark path instead leaves `A_9` as a leaf and
is already covered.

In each row `P|sT|T^kP`, where `2<=k<=8` and `s=9-k>=1`, remove a singleton
triangle leaf. If none exists, the bare pentagon and the `T^kP` cluster are the
only leaves by Lemma 2.2. They form the ends of a path. Pair the bare pentagon
with its nearest singleton triangle, giving strict `TP`; the complement has
rank nine and is strict.

The row `P|T^2P|A_7` has no singleton triangle cluster. A finite tree on these
three marks has at least two marked leaves. If `A_7` is a leaf, cutting it gives
a strict packet and a connected rank-four complement, also strict. Otherwise
`T^2P` must be a leaf: cutting it gives a nonnegative rank-three packet and a
strict connected rank-eight complement. This includes the three-arm Steiner
topology and exhausts the row.

Finally `P|T^9P` has two marks and one reduced path, giving `E_P^0`. All
separations are actual-bridge separations with the ownership convention of
Section 2. QED.

Thus bridge pruning replaces the thirteen disconnected rows by exactly two
marked endpoint families, independent of a marked incidence census.

## 5. Shared-cut cluster model and proved router moves

Inside an endpoint cluster, let `I` be its cycle-cut incidence tree. Triangle
nodes have incidence degree at most three, pentagons at most five, and cut nodes
degree at least two. Each external connector is projected to its first point
on the cyclic hull, either a cut or a private cycle vertex. Connector remnants
and off-hull trees follow that projected mark.

The following local moves are rigorous.

### Lemma 5.1 (triangle router)

A triangle with two or three occupied ports can be partitioned into proper
consecutive intervals, one for each retained incidence branch or private
interface. The resulting territories are connected, induced, disjoint, and
exhaustive; the triangle is destroyed. A private interval retaining no cycle
is a nonempty tree of surplus `-1`. Later splits may refine one territory.

This is Theorem 3.1 of
`research/rank-uniform-triangular-router-interface-theorem-2026-07-26.md`.

### Lemma 5.2 (coalescing two demands on a triangle)

Suppose two external demand marks occupy two distinct private vertices `a,b`
of a triangle `R`, and all retained incidence branches meet the third vertex
`x`. Then the interval `{a,b}` may own both demands and their connector
remnants, while `{x}` owns every retained incidence branch. These two induced
territories are connected, disjoint, and exhaustive. If the remote demanded
cycles are two pentagons, the first territory is a connected `PP` packet and
the second is a triangular packet.

**Proof.** The edge `ab` and singleton `x` are the two nonempty proper
consecutive intervals of `R`. Attach each connector remnant at its endpoint in
`{a,b}` and every incidence branch at `x`. There is no edge between the two
sets except the two destroyed triangle edges, whose endpoints lie in different
territories; inducedness concerns only edges with both endpoints in one set.
Connectivity, disjointness, and exhaustion are immediate. The remote
pentagons and the path between them through `ab` form one connected cactus of
profile `PP`. QED.

This proves the local repair proposed in
`research/bounded-demand-separator-next-obstruction-2026-07-26.md`. It does not
prove that arbitrary nested router sequences can always expose this pattern.

### Lemma 5.3 (pentagon interval router with at most four marks)

Let a pentagon carry `d`, `2<=d<=4`, distinct occupied vertices. For any
chosen occupied vertex `z`, there is a partition of the pentagon into `d`
nonempty proper consecutive intervals, one containing each mark, such that the
interval at `z` is a singleton, provided that when `d=2` the other mark is not
adjacent to `z`. Without that proviso, and without any proviso for `d>=3`,
there is still a partition into `d` proper intervals with one mark in each.
All incidence branches, connector remnants, and attached trees may be assigned
to the interval containing their mark, and the resulting territories are
connected, induced, disjoint, and exhaustive.

**Proof.** Traverse the five vertices cyclically and choose one boundary edge
in each open arc between consecutive occupied vertices. This gives `d`
nonempty consecutive intervals, one per mark. To isolate `z`, choose both edges
incident with `z` as boundaries. For `d>=3`, these lie in the two distinct open
arcs adjacent to `z`; choose one boundary in every remaining open arc. For
`d=2`, the two incident edges lie in the two distinct open arcs exactly when
the other mark is nonadjacent to `z`. Every interval is proper because there
are at least two intervals. The owner argument is the same as for Lemma 5.1.
QED.

The lemma gives graph-level ownership for a four-port pentagon router. Unlike a
triangle router, sacrificing the pentagon does not automatically give a useful
uniform spectral ledger; that arithmetic is treated separately below.

## 6. Rank-uniform endpoint target

The bridge reduction says that a rank-eleven proof needs only the following
cluster interfaces:

| family | cluster profile | external demands |
|---|---|---:|
| `E_Q` | `A_10` | one `Q` |
| `E_P^0` | `T^9P` | one remote `P` |
| `E_P^1` | `A_9` | two remote `P` cycles |
| `F_Q` | fully shared `T^10Q` | none |
| `F_P` | fully shared `T^9PP` | none |

The list has five
families and at most two external hostile demands. It is rank-uniform in the
sense that increasing triangular rank changes only the number of triangle
nodes, not the interface alphabet.

The arithmetic state can be taken as

```text
(p,e,c,t,q),
p,e in {0,1,2}, c in {0,1,2,3}, t,q in {0,1}.          (6.1)
```

Here `p` counts separately charged pentagonal deficits, `e` naked interface
trees, `c` certified integer credit truncated at three, `t` an uncounted strict
packet, and `q=1` a certified nonnegative coalesced `PP` territory. There are at
most `144` states. The old accepting rules remain

```text
e=0,c>=1;  e=1,c>=2;  e=2,c>=3,
```

and `q=t=1` is also accepting. This proves finiteness of the arithmetic, but
not reachability of an accepting state.

## 7. Candidate repairs for the fully shared endpoint shapes

The exact unmarked conditional frontier identifies ten ordinary-split
exceptions for fully shared `T^9PP`. Nine are the rank-ten ladder shapes with
one additional triangle. The tenth is

```text
P(X(P())X(T())X(T())X(T()T()T()T()T()T()T())).        (7.1)
```

It has a unique degree-four pentagon router. Its four branch profiles are

```text
P, T, T, A_7.                                          (7.2)
```

The signature and profiles are independently checked by
`research/rank-eleven-conditional-frontier-census.py`. This use of a small
unmarked census is diagnostic only; the structural repair below applies to
every realization of (7.1).

For reference, the exact ten unmarked endpoint signatures are

```text
U1  X(P()P()T()T()T()T()T()T()T()T()T())
U2  P(X(P())X(T()T()T()T()T()T()T()T()T()))
U3  T(X(P())X(P()T()T()T()T()T()T()T()T()))
U4  P(X(P())X(T())X(T()T()T()T()T()T()T()T()))
U5  T(X(P())X(P())X(T()T()T()T()T()T()T()T()))
U6  T(X(P())X(P()T()T()T()T()T()T()T())X(T()))
U7  X(T()T()T()T()T()T()T()T(X(P()))T(X(P())))
U8  P(X(P())X(T())X(T())X(T()T()T()T()T()T()T()))
U9  X(T()T()T()T()T()T()T(X(P()))T(X(P())X(T())))
U10 X(T()T()T()T()T()T(X(P())X(T()))T(X(P())X(T())))
```

Their cut-count distribution is `1,2,4,2,1` at one through five cuts. `U8` is
the new degree-four pentagon shape (7.1). For `U1`--`U7`,`U9`,`U10`, the
rank-ten N1--N9 owner templates identify the repairs, but every numerical
ledger must be recomputed after extension. The companion G3 proof does this:
eight rows extend directly, while `U7` instead uses one router to leave `P`
plus a packing-one `T^8P` packet.

### Proposition 7.1 (repair of the new degree-four pentagon router)

Every cactus with incidence shape (7.1) has positive surplus.

**Proof.** Let `R` be the central pentagon. Choose either mark whose incidence
branch is a singleton triangle. Isolate that marked vertex of `R`; the other
four vertices form one consecutive path containing the other three occupied
marks, regardless of cyclic order. Give the isolated vertex and its incidence
branch to one territory, and give the complementary path and all other
incidence branches to the second. The first territory has profile `T`; the
second has profile `T^8P`, consisting of the other singleton triangle, the
seven triangles of `A_7`, and the remote pentagon. The central pentagon is
destroyed and is not charged separately. Thus the split is

```text
T + connected rank-nine T^8P,                           (7.4)
```

Both packets are strict by the rank-ten theorem. The interval-owner argument
proves connectivity, inducedness, disjointness, exhaustion, and ownership of
arbitrary attached trees. QED.

### Proposition 7.2 (rank-ten ladder inheritance, corrected)

Every realization of `U1`--`U7`,`U9`,`U10`, with arbitrary attached trees, has
positive surplus and an exhaustive final-owner packetization. Their exact
packet ledgers are

```text
U1  common-cut T^9PP                         >10-4/(3sqrt(13)),
U2  common-cut T^9P + opened tree            >8-delta,
U3  P + common-cut T^8P                      >8-2delta,
U4  A_8 + TP                                 >3/4,
U5  packing-one T^9P + opened tree           >8-delta,
U6  P + T + common-cut T^7P                  >7-2delta,
U7  P + packing-one T^8P                     >8-2delta,
U9  P + P + T + A_6                          >1-2delta,
U10 P + P + T + T + A_5                      >2-2delta.
```

The proof, including the owner-preserving leaf extension and every router
interval, is
`research/rank-eleven-t9pp-ladder-inheritance-2026-07-26.md`.

The correction at `U7` is essential. Literal N7 extension gives `P+P+A_7`,
whose available ledger is only `>-2delta`; qualitative strictness cannot pay
the deficits. Sacrificing just one router leaves the other router and seven fan
triangles as a packing-one `T^8P` packet. Also, a leaf triangle has two private
vertices, not three.

### Candidate Repair 7.3 (`T^10Q` ladder)

The hostile fully shared `T^10Q` ordinary ledger leaves only the common bouquet
and the two familiar saturated extensions. Their rank-ten repairs extend
formally:

```text
common-cut T^10Q:                    >10-delta_q,
packing-one ten-triangle Q arm:      >10-delta_q,
open one leaf triangle, retain T^9Q: >8-delta_q.
```

All are positive because `delta_q<1`. The first two are direct applications of
the established one-pivot theorems. The third is rigorous when the nine
retained triangles visibly share the packing-one hub and the opened territory
is exactly the private two-vertex path of the leaf triangle with its rooted
trees. This repairs the three displayed unmarked shapes without a marked
census. A structural proof that no other fully shared shape survives the
rank-uniform router rules is still needed.

## 8. The exact remaining structural lemma

The large marked censuses would be unnecessary if the following statement were
proved.

### Lemma R11 (candidate shared-cut router lemma)

Let `I` be a cycle-cut incidence tree belonging to one of the five families in
Section 6. Project every external connector to its first hull mark. Repeatedly
apply:

1. the triangle-router move of Lemma 5.1;
2. the demand-coalescing move of Lemma 5.2;
3. the pentagon interval move of Lemma 5.3 only when its resulting packets have
   one of the certified profiles below.

Then final-owner refinement produces one of:

```text
(a) an accepting state of (6.1);
(b) PP plus a strict triangular packet;
(c) a connected packet of rank at most ten;
(d) common-cut T^kQ, T^kP, or T^kPP;
(e) a packing-one hostile arm;
(f) one of the finite ladder repairs in Section 7.
```

Every shared cut, router interval, connector remnant, incidence branch, and
attached tree has exactly one final owner.

This is deliberately restricted to rank-eleven endpoint profiles. It is
stronger than a list of marked rows but weaker than the false unrestricted
Candidate Lemma S: bounded-rank connected packets are explicit terminals, and
coalescence of two demands is an allowed transition.

No proof of Lemma R11 is currently given. A plausible induction roots `I` at
the unique hostile demand carrier (or at the path between two carriers), prunes
an outermost triangle router, and records only the state (6.1). The induction
must prove that a locked common cut is terminal rather than attempting to give
the same cut to two territories. It must also include pentagon cyclic order in
the local state whenever four marks occur.

## 9. Explicit gaps and no-go statements

The proof status is exactly as follows.

**G1 -- proved:** Sharp DNN leaves only `T^10Q` and `T^9PP`.

**G2 -- proved:** Actual bridge leaf/path pruning reduces every disconnected
structural row to the finite endpoint families (3.2) and (4.2). The unresolved
disconnected core list is exactly `A_10|Q`, `T^9P|P`, and `P|A_9|P`.

**G3 -- proved, with one corrected recipe:** All nine inherited signatures
have graph-level final-owner repairs. Eight extend a rank-ten owner template
with a recomputed ledger. `U7` instead uses one router and a retained
packing-one `T^8P` packet. See the companion G3 proof.

**G4 -- open:** Lemma R11, the global reachability of a good local router or a
certified terminal, is unproved. The finite `144`-state ledger proves only that
the arithmetic state space is bounded.

**G5 -- proved locally, open globally:** Demand coalescence is a valid induced
two-interval split in the local configuration of Lemma 5.2. Its compatibility
with arbitrary earlier nested router splits is not yet formalized as a
final-owner theorem.

**G6 -- repaired:** The new degree-four pentagon signature (7.1) admits the
uniform split (7.4): isolate either singleton-triangle branch and give the
complementary four-vertex pentagon path to all other branches. This yields a
strict triangle and a strict connected rank-nine cactus. No fixed deficit is
paid.

**G6a -- finite endpoint data:** The ten fully shared `T^9PP` signatures
`U1`--`U10` and the three hostile fully shared `T^10Q` signatures are exact for
the stated ordinary one-cycle split ledger. This does not prove that the
candidate router automaton reaches that ledger on every marked endpoint.

**G7 -- forbidden shortcut:** Qualitative strict positivity of one or more
triangular packets cannot absorb `delta` or an exact tree cost `1`. Every such
payment needs a displayed numerical margin or a packet in which the hostile
cycle is retained.

**G8 -- forbidden shortcut:** Two cycles sharing one cut cannot be retained in
different induced territories. Locked fans require a one-pivot analytic packet;
router interval bookkeeping alone cannot separate them.

## 10. Conclusion

The rank-ten theorem does give a substantial rank-uniform rank-eleven
reduction. A large marked census is not needed for the disconnected bridge
topology: actual leaf pruning leaves exactly three unresolved marked cluster
cores. The interface alphabet
has at most two hostile demands, and the exact arithmetic automaton has at most
`144` states after adding demand coalescence. The genuinely new four-port
pentagon shape has the uniform repair `T +` strict rank-nine.

What remains is not the finite ladder inheritance, which is now proved, but the
global existential router reachability theorem R11 with final ownership. Until
that theorem or an equivalent bounded local verification is supplied, no
rank-eleven conclusion is claimed.
