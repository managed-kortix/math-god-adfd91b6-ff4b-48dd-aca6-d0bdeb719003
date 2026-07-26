# A rank-uniform router/interface theorem for triangular incidence trees

**Date:** 2026-07-26

## 1. Scope and verdict

Write

```text
sigma(G)=s+(G)-|V(G)|,  T=C3,  P=C5,
delta=sqrt(5)-2<1/4.
```

This note extracts the common, census-free part of the strict-last-bridge
`877=861+16` argument and the fully shared `2116=2110+6` router argument.
There are two conclusions.

1. Router splitting and all of its accounting are rank-uniform. With at most
   two pentagonal demands and at most two labelled external interfaces, the
   numerical interface has finitely many states, independent of the number of
   triangles. The sixteen L-types and six U-types use the same transition
   system.
2. This does not by itself replace either incidence census. The missing step is
   one purely structural separator assertion, stated as Lemma S below. The
   smallest obstruction to proving Lemma S by separator moves alone is exact:
   cycles retained through one common cut cannot be assigned to different
   induced territories. Thus a terminal analytic packet at a locked cut is
   necessary, not an artifact of the octacyclic census.

The local router theorem, finite-state ledger, and obstruction theorem below
are proved. Lemma S is isolated as the sole unproved global step needed for a
census-free induction.

## 2. Incidence objects and interfaces

Let `I` be a bipartite tree. Its cycle nodes are triangles and zero, one, or
two distinguished pentagons; its other nodes are shared cyclic cuts. A triangle
has incidence degree at most three, a pentagon degree at most five, and a cut
has degree at least two. Such an `I` is the cycle-cut incidence tree of a
shared-cut cactus cluster.

An external interface is projected to its first point on the cyclic hull. It
is therefore represented by either

* a cut node of `I`; or
* a private vertex of a cycle node.

Connector remnants and off-hull trees are not additional states. A cactus
component off the cyclic hull has one hull attachment and follows the owner of
that attachment.

We use only the following packet certificates, all uniform over arbitrary
attached trees:

```text
P                                      >= -delta,
nonempty triangular packet             > 0,
common-cut T^k P                        > k-delta,
shared-cut T T P                        > 2-delta,
common-cut T^k P P                      > k-2delta,
acyclic private-interface territory E   = -1.                 (2.1)
```

The displayed two-pentagon weakening follows from the stronger common-cut
Schur-Sachs estimate already available. Only the integer credits in (2.1) are
used below.

## 3. Rank-uniform router separator

**Theorem 3.1 (labelled triangle-router separator).** Let `R` be a triangle
node of `I`. Let `B_1,...,B_d` be the components of `I-R`, where `2<=d<=3`,
and let `z_i` be the incidence mark of `B_i` on `R`. In addition, let `R`
carry interfaces at `e` distinct private vertices, where `d+e<=3`.
Interfaces coinciding at one private vertex count as one mark and must keep the
same owner. Then the vertices of `R` have a partition into `d+e` nonempty
proper consecutive intervals with
the following properties.

1. One interval owns each `z_i` and the entire realized incidence branch
   `B_i`.
2. One interval owns each private interface and its entire connector remnant.
3. Every off-hull tree follows the interval owning its attachment.
4. The resulting territories are connected, induced, disjoint, and exhaustive.
5. The cycle `R` is retained by no territory. A private-interface interval
   which owns no retained cycle is a nonempty tree `E` and has `sigma(E)=-1`.

The same conclusions hold for a second router split performed inside one
territory produced by the first split.

**Proof.** The distinct incidence marks occupy distinct vertices of the
triangle. If there are two total marks, make either marked vertex a singleton
and give the complementary edge to the other mark. If there are three marks,
the three singleton vertices are forced. Adjoin each component of `I-R` to
the interval containing its mark. A private interface has no incidence
component and takes its connector and rooted branches instead.

Every assigned set is connected. The graph induced on it contains all edges
whose endpoints it owns and no unassigned vertex, so the territories are
induced. They partition the triangle vertices, incidence components,
connectors, and hanging trees. Every interval is a proper path, hence no
territory retains the router cycle. An interval with no retained cyclic block
is a nonempty tree; bipartite spectral symmetry gives
`s+(E)=|E(E)|=|V(E)|-1`, and therefore `sigma(E)=-1`.

A later split partitions one induced territory into induced subterritories.
Refinement preserves disjointness, exhaustiveness, and inducedness. In
particular, a shared cut owned before the refinement remains in exactly one
descendant territory. QED.

No part of this theorem depends on rank, a canonical incidence code, cyclic
order beyond the three triangle vertices, or the shape of attached trees.

## 4. The finite interface state

A packetization produced by Theorem 3.1 has the state

```text
(p,e,c,t),
```

where

* `p in {0,1,2}` is the number of pentagonal unicyclic deficits charged
  separately;
* `e in {0,1,2}` is the number of naked private-interface trees `E`;
* `c in {0,1,2,3}` is certified strict integer credit, truncated at three; and
* `t in {0,1}` records a strict packet not already counted in `c`.

Credit is attached only to a proved packet certificate, never to a bare count
of triangles. For example, common-cut `T^kP` contributes `k` credits while
charging its pentagon in the same formula; shared-cut `TTP` contributes two;
and the U6 remainder `A_2` contributes one. Credits above three are identified
because at most two interfaces can become naked and at most two pentagons are
hostile.

**Theorem 4.1 (finite-state ledger).** Every router packetization with at most
two pentagons and two external interfaces satisfies

```text
sigma(G) > c-e-p*delta                                  (4.1)
```

whenever `c` is below the truncation threshold. With truncated `c=3`, the
right side may be replaced by `3-e-p*delta`. Consequently it is positive in
each of the following accepting states:

```text
e=0 and c>=1,
e=1 and c>=2,
e=2 and c>=3.                                           (4.2)
```

A nonnegative `PP` packet together with `t=1` is also accepting.

**Proof.** Add the induced-territory estimates (2.1). Router remnants already
belong to cyclic packets unless they are one of the `e` naked intervals, so no
other tree cost occurs. Since `p<=2` and `delta<1/4`,

```text
c-e-p*delta >= 1-2delta > 0
```

in every state in (4.2). Any credit beyond three is unnecessary for this
test. In the `PP` alternative, the strict packet recorded by `t=1` makes the
sum strict. QED.

Thus the arithmetic automaton has at most `3*3*4*2=72` states. This is a loose
upper bound; unreachable states need not be enumerated. The important point is
that the state count is independent of triangular rank.

## 5. Recovery of both octacyclic router tables

The exceptional tables are instances of one state calculation.

For strict-last-bridge `G6PP`, the last actual bridge is cut first. The remote
pentagon and the clustered pentagon account for `p=2`. The states of the six
ledger rows are:

| classes | certified credit `c` before truncation | naked `e` | lower bound |
|---|---:|---:|---:|
| L1-L2 | 6 | 0 | `6-2delta` |
| L3-L6 | 4 | 0 | `4-2delta` |
| L7 | 4 | 1 | `3-2delta` |
| L8-L10, L12 | 2 | 0 | `2-2delta` |
| L11 | 2 | 1 | `1-2delta` |
| L13-L16 | 2 | 0 | `2-2delta` |

The L7 and L11 charge is not exceptional machinery: it is exactly the naked
private-interface transition in Theorem 3.1(5).

For the fully shared U-types there is no external interface, so `e=0`, and the
two pentagons give `p=2`. U2-U6 have credits `5,4,3,2,1`; hence U6 reaches the
minimal accepting state `(2,0,1,t)`, with value `1-2delta`. U1 is a terminal
common-cut `T^6PP` packet. Binary and saturated routers are precisely the
two-mark and three-mark transitions of Theorem 3.1.

This proves that the twenty-two explicit replacement resolutions are not
rank-eight phenomena. They use one rank-uniform local transition system and
one finite ledger.

## 6. What an inductive census-free theorem must prove

The local theorem does not say that a suitable router always exists. The exact
global statement still needed is the following.

**Lemma S (bounded-demand separator, candidate).** Let `I` be any triangular
incidence tree with one or two distinguished pentagons and at most two labelled
external interfaces. Then repeated labelled router separations produce either

1. an accepting state of Theorem 4.1;
2. a nonnegative `PP` territory and a strict triangular territory; or
3. one terminal locked packet to which a proved common-cut or rooted
   Schur-Sachs estimate applies.

All other resulting cyclic territories are triangular. No operation creates
more naked interface territories than the number of labelled interfaces.

If Lemma S is proved, induction on the number of triangle nodes replaces both
the marked-root and fully shared incidence censuses: split a router, apply the
lemma recursively to the unique descendant territory carrying each demand,
and combine the finite states by Theorem 4.1. The induction is rank-uniform
because a triangle has only two router types and the state is truncated at
three credits.

The qualification "to which a proved estimate applies" is essential. It
cannot be replaced by another separator clause.

## 7. Minimal obstruction

**Theorem 7.1 (locked-cut obstruction).** Suppose two cyclic blocks `C` and
`D` share a cut vertex `x`. No vertex partition into induced territories can
retain `C` as a cycle in one territory and retain `D` as a cycle in another.

**Proof.** Retaining either cycle requires all of its vertices, in particular
`x`. Distinct parts of a vertex partition cannot both own `x`. QED.

The smallest hostile instance is one pentagon and one triangle sharing `x`.
The smallest two-hostile instance is two pentagons and one triangle sharing
`x`. More generally, an arbitrarily large common-cut fan remains one locked
object: increasing the number of triangle petals does not create a separator.

This is the minimal obstruction to an interval-only proof of Lemma S. It also
explains the two terminal transitions already present in the octacyclic proof:

* U1 keeps the common-cut `T^6PP` packet intact;
* L1-L2 keep the common-cut `T^6P` packet intact after the remote pentagon has
  been separated on the last actual bridge.

Opening a private vertex can destroy a locked cycle, but it creates the exact
cost `-1`; repeating that move is not a rank-uniform substitute for absorption.
Likewise, qualitative positivity of arbitrarily many separate triangular
packets cannot pay a fixed pentagonal deficit. A valid proof must retain a
certified mixed packet or invoke a locked-packet analytic estimate.

## 8. Precise remaining target

The census-free problem is now topological and sharply bounded:

```text
prove Lemma S using the two local router transitions,
with terminal locked cuts summarized by established analytic packets.
```

It is not necessary to classify incidence trees by rank. A minimal failed
induction would have all of the following properties:

1. every available degree-two or degree-three triangle separation leads only
   to nonaccepting finite states;
2. every private interface on a sacrificed triangle is charged as `E=-1`;
3. no strict triangular branch is silently used to pay a fixed deficit; and
4. every unsplittable retained pair of cycles is certified as sharing a locked
   cut.

The octacyclic L and U tables show that no such failed kernel occurs with six
triangles. They do not prove its absence at arbitrary rank. Establishing that
absence by pruning the incidence tree, or producing the first kernel satisfying
conditions 1-4, is the exact next step. Until Lemma S is proved, the finite
state theorem abstracts and verifies the existing resolutions but does not
replace the two exhaustive censuses.
