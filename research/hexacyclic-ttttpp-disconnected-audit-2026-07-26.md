# Disconnected shared-cut audit for the hexacyclic `TTTTPP` residual

## 1. Scope and conclusion

Let `G` be a connected cactus whose six cyclic blocks have multiset

`TTTTPP = {C3,C3,C3,C3,C5,C5}`,

and suppose that its shared-cut graph is disconnected. Put

`sigma(H)=s+(H)-|V(H)|` and `delta=sqrt(5)-2`.

This note tests, rather than assumes, the assertion `sigma(G)>0`. It uses the
proved pentacyclic theorem, the reduced cluster tree, the complete list of 28
proper colored cluster partitions, and connector-entry analysis. The outcome is
not a proof of the whole disconnected case.

The following cases are proved here.

1. A singleton triangular cluster is a leaf of the reduced cluster tree.
2. Direct cluster-packet addition proves 23 of the 28 colored partitions,
   independently of reduced-tree topology.
3. The all-singleton partition is proved for every reduced-tree topology,
   including the pentagon-ended path.
4. The partition `TTP|TTP` is proved for every reduced-tree topology.
5. The three remaining colored partitions are reduced by connector-entry
   analysis; one is proved here, and E2 is subsequently closed by the exact
   incidence-and-entry census cited in Section 7.3.

Thus no global hexacyclic theorem, and not even the full disconnected
`TTTTPP` proposition, is claimed. After the E2 supplement, the unresolved set
consists only of E1 as described in Section 8.

## 2. Territory rules and available bounds

The shared-cut clusters are the connected components of the graph on cyclic
blocks in which two blocks are adjacent when they share a cut vertex. Contract
each cluster in the block-cut tree, take the minimal subtree spanning the
cluster nodes, and suppress only unmarked degree-two nodes. Call the result
`R`, the reduced cluster tree.

We use two established territory operations.

**Bridge territories.** Pairwise disjoint connected subtrees covering all
marked nodes of `R` expand to a vertex partition into connected induced
territories. Cuts are made on actual bridge edges. Genuine Steiner branches,
long connector paths, and arbitrary hanging trees are allowed.

**Cycle intervals.** If a cycle is to be destroyed, its vertices may be split
into nonempty proper consecutive intervals. Each interval is assigned with the
incidence branches whose marks it contains. A shared cut belongs to exactly one
interval. This operation creates no separate tree territory. In contrast,
deleting a private cycle vertex and its rooted branches creates a tree
territory of surplus `-1`.

The proof ledger used below is

```text
sigma(T)>0,                     sigma(P)>=-delta,
sigma(TT)>1,                    sigma(TP)>1-delta,
sigma(PP)>=1-4/(3sqrt(13))      when the two P's share a cut,
sigma(H)>=0                     for every bicyclic or tricyclic cactus,
sigma(TTT)>2                    for one shared-cut triangular cluster,
sigma(TTTT)>3                   for one shared-cut four-triangle cluster,
sigma(TPP)>6-2sqrt(5)           for one shared-cut cluster,
sigma(H)>0                      for every tetracyclic or pentacyclic cactus.
```

Every inequality allows arbitrary attached trees. We repeatedly use
`delta<1/2`. Qualitative tetracyclic or pentacyclic positivity is never charged
against a tree cost or a hostile singleton pentagon.

## 3. The safe pentacyclic reduction

**Lemma 3.1 (bridge-leaf triangle).** If a singleton triangular cluster is a
leaf of `R`, then `sigma(G)>0`.

**Proof.** Cut the first actual bridge on the unique reduced-tree route from
that leaf toward the other marked nodes. The leaf side is a connected induced
triangular unicyclic cactus, and the other side is a connected induced
pentacyclic cactus. Their surpluses are both strict positive. Induced-subgraph
superadditivity proves the assertion. No opening cost occurs. `square`

The hypotheses cannot be weakened to "a triangle is a leaf cycle of a
shared-cut cluster": its common cut would then be required by both retained
parts. Nor can one open such a triangle and appeal only to the pentacyclic
theorem, since the opened tree costs one.

## 4. Exhaustive colored cluster partitions

Up to permutations of the four triangles and the two pentagons, the proper
colored set partitions of `(4,2)` are exactly the following 28 rows. This is the
integer-partition recursion obtained by choosing a first nonempty pair `(t,p)`,
subtracting it from `(4,2)`, and requiring the remaining pairs to be
lexicographically nondecreasing; hence no colored partition is omitted or
duplicated.

In the table, `direct` means that the whole shared-cut clusters themselves,
separated by bridge cuts, have a strict positive total under the ledger in
Section 2. A zero lower bound followed by at least one strict triangular or
positive tetracyclic/pentacyclic cluster is sufficient. The five rows marked
`topology` are analyzed later.

| colored cluster partition | certificate | status |
|---|---:|---|
| `T|T|T|T|P|P` | reduced-tree argument, Section 5 | topology |
| `TT|T|T|P|P` | `>1-2delta` plus strict `T`'s | direct |
| `TTT|T|P|P` | `>2-2delta` plus strict `T` | direct |
| `TT|TT|P|P` | `>2-2delta` | direct |
| `TTTT|P|P` | `>3-2delta` | direct |
| `TP|T|T|T|P` | `>1-2delta` plus strict `T`'s | direct |
| `TTP|T|T|P` | only `>=-delta` plus strict `T`'s | topology |
| `TT|TP|T|P` | `>2-2delta` plus strict `T` | direct |
| `TTTP|T|P` | only `>=-delta` plus strict `T` | topology |
| `TTT|TP|P` | `>3-2delta` | direct |
| `TTP|TT|P` | `>1-delta` | direct |
| `TTTTP|P` | only `>0-delta` | topology |
| `PP|T|T|T|T` | `>0` from shared `PP`, plus strict `T`'s | direct |
| `TT|PP|T|T` | `>1` plus nonnegative `PP`, plus strict `T`'s | direct |
| `TTT|PP|T` | `>2` plus nonnegative `PP`, plus strict `T` | direct |
| `TT|TT|PP` | `>2` plus nonnegative `PP` | direct |
| `TTTT|PP` | `>3` plus nonnegative `PP` | direct |
| `TPP|T|T|T` | `>6-2sqrt(5)` plus strict `T`'s | direct |
| `TP|TP|T|T` | `>2(1-delta)` plus strict `T`'s | direct |
| `TTPP|T|T` | positive tetracyclic cluster plus strict `T`'s | direct |
| `TTP|TP|T` | `>1-delta` plus strict `T` | direct |
| `TPP|TT|T` | `>7-2sqrt(5)` plus strict `T` | direct |
| `TTTPP|T` | positive pentacyclic cluster plus strict `T` | direct |
| `TT|TP|TP` | `>3-2delta` | direct |
| `TTTP|TP` | `>1-delta` | direct |
| `TTT|TPP` | `>8-2sqrt(5)` | direct |
| `TTPP|TT` | positive tetracyclic cluster plus `>1` | direct |
| `TTP|TTP` | Section 6 | topology |

There are therefore 23 topology-free rows and five rows requiring more work.
The coarse statement "all rows but five are direct" is exact only at the
colored-partition level. It does not by itself resolve the five rows, because
the location at which a bridge connector enters a nontrivial shared cluster can
control which interval splits are legal.

## 5. The all-singleton row

**Lemma 5.1.** The partition `T|T|T|T|P|P` has positive surplus for every
reduced cluster tree.

**Proof.** Every leaf of the minimal reduced tree is marked. If a triangle is a
leaf, Lemma 3.1 applies. Otherwise every leaf is one of the two pentagons. A
finite nontrivial tree has at least two leaves, so both pentagons are leaves and
there are exactly two leaves. Therefore the reduced tree is a path, with the
four triangles internal.

Read the triangle marks in path order as `T1,T2,T3,T4`, with pentagonal ends
`P1,P2`. Cut actual bridges to form three connected subtrees carrying

`P1,T1`; `T2,T3`; and `T4,P2`.

The corresponding induced territories have types `TP`, `TT`, and `TP`, and

`sigma(G)>2(1-delta)+1>0`.

Suppressed degree-two connector vertices and a longer actual connector do not
alter the argument; all cuts are on actual bridges. `square`

## 6. The row `TTP|TTP`

Write the two shared-cut clusters as `A` and `B`. Each has two triangles and
one pentagon.

**Lemma 6.1.** Every disconnected `TTP|TTP` cactus has positive surplus.

**Proof.** There are only two marked nodes in the reduced tree, so one bridge
connector joins `A` to `B`. Consider one `TTP` cluster.

If the two triangles in either cluster share a cut, that cluster has surplus
`>2-delta`, while the other tricyclic cluster is nonnegative. This already
proves the result. We may therefore assume that the triangles are disjoint in
both clusters. Incidence-tree acyclicity then forces each cluster to be the
distinct-cut chain

`T1 - x1 - P - x2 - T2`.

For each cluster record the first connector entry into its cyclic core.
An entry through `Ti`, including at `xi` or through a branch rooted on `Ti`, is
declared to lie on side `i`. An entry at a private vertex of `P` is assigned to
either neighboring side in the cyclic order. Split `P` into two nonempty proper
consecutive intervals, one carrying `T1` and the other `T2`, and put the
external connector wholly with either interval containing its entry. This
turns the cluster into two triangular unicyclic branch territories, except that
one selected territory may continue through the external connector.

Perform this construction first in `A`, assigning the connector to the
interval selected by its entry, and then in `B`, assigning the same connector
to the selected interval at the other end. Join those two selected intervals
through the connector. The resulting territory has two triangular cycles and
hence type `TT`; the two unselected intervals give one `T` territory each.
All three territories are connected and induced, and no common cut is used
twice. Their total surplus is `>1` plus two strict triangular terms. Thus
`sigma(G)>0`.

The only delicate point is interval existence. A pentagon with the two
distinct marks `x1,x2` can always be cut in two gaps to give two nonempty proper
intervals. A private entry mark is included with one of them; an entry forced
through a triangle already belongs to that triangle's interval. `square`

## 7. Entry lemmas for the three remaining rows

Sections 5 and 6 dispose of two of the five topology rows. The remaining three
colored partitions are

```text
TTTTP|P,  TTTP|T|P,  TTP|T|T|P,
```

We now prove all entry subcases justified by the inherited packet bounds.

### 7.1 A general remote-pentagon criterion

Let `A` be the unique nontrivial cluster in one of the three rows and let `P1`
be the singleton pentagon. If bridge cuts produce, before adjoining `P1`, a
territory sum of surplus greater than `delta`, then the row is settled. More
usefully, if the connector to `P1` enters a triangle `Ti` of `A` and an
interval split can put `Ti`, the connector, and `P1` in a `TP` territory while
leaving either a `TT` packet or a positive tetracyclic packet on the other side,
then the total is positive:

```text
TP+TT:          sigma>2-delta,
TP+tetracyclic: sigma>1-delta plus a strict positive term.
```

This criterion is valid only if the complement is connected after the split
and every shared cut of retained cycles is owned by one side.

### 7.2 The row `TTTTP|P`

Let `A` contain four triangles and pentagon `P0`; let `P1` be remote. The
pentacyclic proof of `TTTTQ` gives the following exact dichotomy for the
internal incidence of `A`.

- If two triangles of `A` intersect, the proof opens a private vertex of `P0`
  and obtains four triangular clusters with total surplus greater than one.
  That unit is spent by the opened tree. The resulting certificate for `A` is
  only strict positive; it does not absorb `sigma(P1)>=-delta`.
- If the four triangles are pairwise disjoint, `P0` is a four-petal hub with
  four distinct marks. Splitting `P0` gives four strict triangular territories,
  but their strictness has no uniform sum bounded below by `delta`.

There are nevertheless settled entry subcases. If the remote connector enters
a triangular petal `Ti` in the four-petal hub, split `P0` so that one proper
interval carries that petal, the connector, and `P1`; group the other three
petals with the complementary proper interval. This gives `TP` plus a
tricyclic all-triangle cactus. The latter is nonnegative, so the total is
`>1-delta>0`. The same holds when the connector enters at the petal's shared
cut or through a tree rooted on the petal.

If instead the connector enters a private vertex `z` of hub `P0`, choose a
petal mark adjacent to `z` in the cyclic order and use the interval containing
exactly those two designated marks. Again the territories are `TP` and `TTT`,
so the total is positive.

For an intersecting-triangle incidence, an entry at a private vertex `z` of
`P0` is also settled. In the pentacyclic opening argument choose `z` as the
opened vertex and put the entire connector and `P1` with the off-cycle branches
rooted at `z`. This territory is a unicyclic pentagonal cactus, so its surplus
is at least `-delta`, not `-1`. The complementary induced territory contains
the four triangles. The incidence-excess argument from the pentacyclic proof
shows that `P0-z` contains every shared cyclic cut on `P0`; hence the four
triangles remain connected through their shared-cut clusters and bridge
connectors. Since some two intersect, the sum of their cluster margins is
greater than one. The total is therefore `>1-delta>0`.

What is not covered is an entry at a shared cut or through a triangle of an
intersecting-triangle configuration. No universal split has been exhibited
that leaves a nonnegative four-cycle complement. These cases are recorded as
`E1` below.

### 7.3 The row `TTTP|T|P`

Let `A=TTTP`, with singleton clusters `B=T4` and `C=P1`. If the `B-C` path in
`R` avoids `A`, the connector subtree between `B` and `C` is a `TP` territory
and `A` is a positive tetracyclic territory. Hence the total is positive.

Suppose the `B-C` path passes through `A`, producing two external entries into
its cyclic core. Particular instances are settled if the two entries can be
put on one proper interval of an internal cycle while the complementary
interval retains a nonnegative packet. The same packetizations as in the
pentacyclic `TTP|T|P` repair then apply:

```text
TP+TTT,  TT+TTP,  or TTP+T.
```

The first two are positive by `sigma(TP)>1-delta` and nonnegativity of the
three-cycle packet, or by `sigma(TT)>1`; the last is positive because the
tricyclic packet is nonnegative and `T` is strict.

The required exhaustive entry lemma is now proved in
`research/hexacyclic-e2-tttp-two-entry-resolution-2026-07-26.md`. There are
eight colored `TTTP` incidence trees. Seven contain an intersecting triangle
pair and are settled directly by `sigma(TTTP)>1`; the remaining three-petal
pentagon hub has 26 ordered labelled-entry orbits modulo dihedral symmetry.
Every orbit has a legal consecutive-interval certificate of type `TP+TTT` or
`TTP+TT`. The exact verifier is
`research/hexacyclic-e2-tttp-entry-census.py`. Hence the entire path-through
case is proved.

### 7.4 The row `TTP|T|T|P`

Let `A=TTP`; the other clusters are singleton triangles `B,C` and pentagon
`D`. If a singleton triangle is a leaf of `R`, Lemma 3.1 settles the graph.
Assume neither is a leaf.

If the two triangles in `A` meet, then

`sigma(A)>2-delta`.

Together with `sigma(D)>=-delta` and the two strict singleton triangles, the
total is `>2-2delta>0`. Thus only the distinct-cut chain

`T1-P0-T2`

inside `A` can be unresolved.

If some reduced-tree edge separates the four marked clusters into a side of
type `TP` and a side containing `A` and the remaining triangle, bridge
territories give `TP` plus a tetracyclic territory, hence positive surplus.
If an edge gives `TT` on one side and `TPP` on the other, the total is also
positive (`>1+6-2sqrt(5)`). These tests include Steiner trees; they are edge
separation tests, not an assumption that `R` is a path.

The only reduced-tree topologies surviving those tests have both singleton
triangles internal and every leaf among `A` and `D`, or have a Steiner branch
at which each singleton triangle lies on a different internal arm while the
two leaves are `A,D`. Since neither singleton triangle is a leaf, the first
description forces exactly two leaves and hence an `A-D` path; the second is
impossible in a finite reduced tree because an arm ending at a singleton
triangle would make it a leaf. Consequently `R` is an `A-D` path with `B,C`
internal, in one of the orders

```text
A-B-C-D  or  A-C-B-D.
```

At the `A` end there is only one external connector entry. Split the chain
pentagon `P0` into intervals carrying `T1` and `T2`, and assign the connector
to the interval containing its actual entry (through `Ti`, at `xi`, or at a
private vertex of `P0`). Join that interval along the path to one of `B,C` so
as to form a `TT` territory. The other interval gives a strict `T` territory.
The remaining singleton triangle and `D`, with their intervening connector,
form a `TP` territory. Thus the total is

`>1 + 0 + (1-delta)>0`.

No shared vertex is duplicated: the split destroys `P0`, and its two triangle
marks belong to different intervals. Hence this third row is completely
proved.

## 8. Exact unresolved configurations

After the preceding arguments and the E2 supplement, only E1 remains
unresolved. It is a proof gap, not a counterexample.

### E1. `TTTTP|P`: intersecting-triangle cluster with a remote pentagon

`A=TTTTP0` is one shared-cut cluster, at least two of its triangles meet, and
`P1` is bridge-separated. The unique external connector first meets the cyclic
core of `A` at a shared cyclic cut or on a triangle (including a branch rooted
on that triangle). Entries at private vertices of `P0`, and every entry in the
pairwise-disjoint four-petal incidence, are proved in Section 7.2 and are not
in E1. For the entries retained in E1, no currently proved interval split has
been shown to produce one of

```text
TP + (nonnegative tricyclic packet),
TP + (positive tetracyclic packet),
TT + (packet of surplus > delta-1),
or a packet sum with uniform surplus > delta.
```

Equivalently, the inherited pentacyclic proof only yields `sigma(A)>0`: it
opens `P0`, spends the available `>1` triangular-cluster margin on that tree,
and leaves no uniform credit for `P1`. To close E1 one needs an entry-sensitive
strengthening of fully shared `TTTTQ`, retaining the location of the external
entry. A qualitative appeal to the pentacyclic theorem is insufficient.

The pairwise-disjoint four-petal hub is not in E1; all of its entry positions
were settled in Section 7.2.

### Resolved supplement: former E2, `TTTP|T|P`

`A=TTTP0`, `B=T4`, and `C=P1`; the `B-C` path in `R` passes through `A`.
This family is proved in
`research/hexacyclic-e2-tttp-two-entry-resolution-2026-07-26.md`. The exact
census produces a legal consecutive-interval split yielding

```text
TP+TTT  or  TTP+TT,
```

for every incidence and entry configuration. The two entries may be

- at private vertices of `P0` or of a triangle;
- at a shared cut;
- through a branch rooted on an incident triangle; or
- coincident at one shared cut.

The supplement resolves simultaneous ownership by one coordinated split, not
by applying the one-entry lemma twice. Its verifier enumerates the eight
colored incidence trees and all 26 ordered entry orbits of the sole incidence
requiring a split, and prints an actual interval and packet ledger for each.

## 9. Hostile self-audit

The following tempting shortcuts are invalid and have not been used.

1. `sigma(pentacyclic)>0` does not pay an opened tree of surplus `-1` and does
   not absorb a remote pentagon of surplus `-delta`.
2. A triangle leaf in a cycle-cut incidence tree is not a bridge-separable
   triangular territory; its shared cut may be indispensable to the remainder.
3. A proper colored cluster partition does not determine reduced-tree path
   position. Only the all-singleton and `TTP|T|T|P` arguments prove when the
   tree has exactly two leaves and hence is a path.
4. Separate strict triangular terms have no known uniform lower bound under
   arbitrary attached trees. They cannot silently pay `delta`.
5. A cycle interval split is legal only when every interval is nonempty and
   proper, all retained branch marks are assigned, and each shared cut has one
   owner. This remains the missing check in E1; the E2 supplement performs it.
6. The 28-row census is exhaustive only for colored cluster partitions. It is
   not an incidence census inside a nontrivial cluster and not an entry census.
7. `TTP|TTP` is proved by one coordinated split on each side of the same bridge
   connector; two unrelated local decompositions would not establish connector
   ownership.

## 10. Status

The disconnected `TTTTPP` residual is proved for 27 of the 28 colored cluster
partitions: 23 by direct packet addition, the all-singleton row by the
pentagon-ended path argument, `TTP|TTP` by coordinated interval splits, and
`TTP|T|T|P` and `TTTP|T|P` by reduced-tree and entry analysis. The sole
unresolved row is E1 exactly as stated in Section 8.

No assertion is made for E1, for the connected shared-cut case, or for all
connected hexacyclic cacti.
