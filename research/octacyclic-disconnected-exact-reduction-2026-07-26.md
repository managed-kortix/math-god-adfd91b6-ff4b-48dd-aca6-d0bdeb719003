# Disconnected octacyclic residuals: exact partition and reduced-tree reduction

**Date:** 2026-07-26

## 1. Scope and conclusion

Write `T=C3`, `P=C5`, and `sigma(H)=s+(H)-|V(H)|`. This note treats only
connected octacyclic cacti in the two sharp-DNN residual families

```text
T^7Q,  q=|Q|>=3,       and       T^6PP,
```

whose shared-cut graph is disconnected. It uses the proved theorem
`sigma(H)>0` for every connected heptacyclic cactus, but never uses that
qualitative inequality to pay a tree-opening cost or an isolated odd-cycle
deficit.

The exact colored-partition census and reduced-tree argument first leave only

```text
T^7 | Q,                         (R7Q)
T^6P_0 | P_1.                    (R6PP)
```

The apparent third row `P_0 | T^6 | P_1` is completely solved: it has surplus
strictly greater than `1-2(sqrt(5)-2)>0`. The later exact rooted hostile-cycle
guard theorem proves all of (R7Q), including its formerly locked bridge-bouquet.
In (R6PP), all cases in which `P_0` is internal, and all incidence-leaf cases
entered at a private vertex of `P_0`, are solved. The exact remaining scope is
stated in Section 6; no positivity claim is made there.

## 2. Inputs and territory convention

Let `A_r` denote one shared-cut cluster of `r` triangles, with arbitrary
attached trees. We use

```text
sigma(A_r)>b_r,     (b_1,...,b_7)=(0,1,2,3,2,1,0),
sigma(P)>=-delta,   delta=sqrt(5)-2<1/4,
sigma(Q)>=-delta_q, delta_q=sec(pi/q)-1<1 for hostile Q,
sigma(TP)>1-delta>0,
```

and nonnegativity in ranks two and three, strict positivity in ranks four
through seven. A nonhostile unicyclic `Q` is nonnegative.

Every cluster packet below is a connected induced territory obtained by cuts
on actual bridges in the reduced cluster tree. A cycle split uses nonempty
proper consecutive intervals, one owner for every distinct mark. Connector
remnants, entry vertices, Steiner branches, and hanging trees travel with one
owner. Surpluses may therefore be added by induced-subgraph superadditivity.

## 3. Exact colored-partition census

Encode a cluster by `(t,d)`, where `t` is its triangle count and `d` is its
number of distinguished cycles (`Q`, or pentagons). Recursively subtract a
nonzero pair and require successive pairs to be lexicographically
nondecreasing. The executable certificate is

```bash
python research/octacyclic-disconnected-partition-census.py
```

It uses only `Fraction` comparisons. For `T^7Q` it returns 45 partitions,
including the one-cluster partition, hence 44 proper partitions. The packet
ledger directly proves 42 and leaves exactly

```text
Q|T|T|T|T|T|T|T,       Q|T^7.                         (3.1)
```

For `T^6PP` it returns 77 partitions, hence 76 proper partitions. The ledger
directly proves 70 and leaves exactly

```text
P|P|T|T|T|T|T|T,
P|T|T|T|T|T^2P,
P|T|T|T|T^3P,
P|T|T|T^4P,
P|T|T^5P,
P|T^6P.                                               (3.2)
```

The conservative census treats a singleton `Q` as `>=-1` and a singleton
pentagon as `>-1/4`. Thus a row omitted from (3.1) or (3.2) is rigorously
positive for every reduced-tree topology and connector realization. The
census classifies cluster colors only; the exceptional rows require the next
structural step.

## 4. Reduced-tree elimination of all singleton-triangle rows

First consider the all-singleton `T^7Q` row. If a singleton triangle is a leaf
of the reduced cluster tree, cut its first actual bridge. The two territories
are a strict triangular unicyclic cactus and a connected heptacyclic cactus,
also strict. If no triangle were a leaf, the distinguished singleton `Q` would
be the only possible leaf. This is impossible for a nontrivial finite tree.
Hence this row is solved.

The first five rows of (3.2) have the form

```text
A_k | T | ... | T | P_1,
```

where `A_0=P_0`, and for `k=2,3,4,5`, `A_k=T^kP_0`; at least one singleton
triangle occurs. A singleton-triangle leaf again gives `T` plus a connected
heptacyclic cactus. If none is a leaf, the only possible leaves are `A_k` and
`P_1`. They are therefore the two leaves, and the reduced tree is their path.
Pair the singleton triangle nearest `P_1` with that pentagon. Cuts on the two
sides of the terminal path packet give

```text
TP + (connected hexacyclic cactus),
```

and both terms are strictly positive. This covers every topology and every
connector length without inspecting the incidence inside `A_k`.

Consequently the exact cluster-color residuals are (R7Q) and (R6PP), not the
larger lists (3.1) and (3.2).

## 5. The row `T^7 | Q`

Let `I` be the cycle-cut incidence tree of the `A_7` cluster, and project the
external connector entry to its first point on the cyclic hull.

If `I` is not a bouquet, some triangle node `C` is internal. Split `C` at its
distinct cyclic marks, including the external entry as an additional mark when
the entry lies privately on `C`. If the `Q`-owning territory retains `r`
triangles, then:

- `r>=3` is strict by the rank-four-through-seven theorems;
- `r=2` is nonnegative, while another nonempty triangular branch is strict;
- `r=1` is a positive `TQ` packet, while all other branches are triangular;
- `r=0` can occur only when the entry itself supplies a mark on `C`; the other
  six triangles occupy at most two incidence branches, so one is an `A_s`
  packet with `s>=3` and surplus `>2`, which absorbs `Q>=-delta_q`.

These alternatives prove every nonbouquet incidence. The degree cap used in
the last bullet is essential: a triangle has at most three distinct cyclic
marks, and one is consumed by the `Q` entry.

If every triangle node of `I` is a leaf, the bipartite tree has one cut node;
thus `A_7` is the common-cut bouquet. An entry at a private vertex of one
triangle gives that triangle two distinct marks: its common cut and the entry.
Splitting there produces `A_6+Q`, whose ledger is

```text
sigma(A_6)+sigma(Q)>1-delta_q>0.
```

An entry through a hanging branch rooted at that private vertex is identical.
The interval argument leaves exactly

```text
seven triangles share x, and the arbitrary bridge connector to Q enters at x.
                                                               (G7Q)
```

The connector and all attached trees are unrestricted. The additive cut
`A_7+Q` gives only `>0-delta_q`, and opening `Q` or a triangle incurs a unit
cost not paid by the triangle recurrence. Nevertheless (G7Q) is now solved by
Theorem 1 of `research/rooted-hostile-cycle-guard-absorption-2026-07-26.md`.
That theorem applies to an arbitrary connected triangular cactus rooted at the
connector entry and joined by an arbitrary positive path to a hostile
`Q=C_(4k+1)`; it gives an induced partition with one coupled territory of
surplus `>1-delta_q` and all other territories strict positive. If `Q` is even
or `3 mod 4`, its unicyclic territory is already nonnegative, while `A_7` is
strict positive. The case `Q=T` is also nonhostile. Hence every `T^7|Q`
configuration is proved. The formerly locked bouquet is a gap only for the
additive packet ledger, not for the exact rooted phase method.

## 6. The row `T^6P_0 | P_1`

Let `I` be the incidence tree of the `T^6P_0` cluster and
`d=deg_I(P_0)`.

If `d>=2`, deleting `P_0` gives branches with positive triangle counts
`r_1+...+r_d=6`. Split `P_0` into one interval per branch and give the external
connector and `P_1` to the interval owning its entry. If its branch has `r`
triangles, that territory is `T^rP_1`: it is positive for `r=1`, nonnegative
for `r=2`, and positive for `r>=3`. Every other branch is a strict triangular
packet, and at least one exists. Hence every `d>=2` case is positive, including
all saturated and coincident-entry cases.

Suppose `d=1`. If the external entry projects to a private vertex of `P_0`, the
unique incidence cut and the entry are distinct marks. Split `P_0` between
them. The two resulting cyclic territories are `A_6` and `P_1`, so

```text
sigma(A_6)+sigma(P_1)>1-delta>0.
```

This also covers entry through a tree rooted at that private vertex.

What remains, exactly within this proof, is

```text
deg_I(P_0)=1, and the external connector enters at the unique P_0 cut or
through the triangular incidence component attached at that cut.             (G6PP)
```

This description includes the common-cut `T^6P_0` bouquet, but it may include
nonbouquet router incidences. No assertion that one- and two-router pictures
exhaust (G6PP) is made. Opening both pentagons gives only
`sigma(A_6)-2>1-2`, and opening only `P_0` leaves a heptacyclic packet whose
known strict surplus has no uniform unit margin. These invalid ledgers are not
used. Resolving (G6PP) requires an entry-sensitive incidence census with a new
quantitative packet, or a nonadditive rooted estimate.

## 7. The row `P_0 | T^6 | P_1`

This row is not residual. Cut the two actual bridge interfaces so that the
central cluster and each pentagon, with all connector remnants assigned, are
three induced territories. Then

```text
sigma(G) >= sigma(A_6)+sigma(P_0)+sigma(P_1)
          > 1-2delta
          = 5-2sqrt(5)
          > 0.
```

The strict first inequality comes from `sigma(A_6)>1`; `delta<1/4` also gives
the weaker transparent bound `>1/2`. This proof is independent of connector
lengths, entries, Steiner branches, and attached trees.

## 8. Exact status

Proved here:

1. all 42 direct `T^7Q` and all 70 direct `T^6PP` proper color partitions;
2. every singleton-triangle exceptional row by the heptacyclic theorem and
   reduced-tree leaf/path analysis;
3. every `T^7|Q` incidence, using rooted hostile-cycle guard absorption for
   the unique interval-locked bouquet;
4. every `T^6P|P` incidence with `deg_I(P_0)>=2`, and every `deg_I(P_0)=1`
   incidence whose entry is private on `P_0`;
5. every `P|T^6|P` configuration.

Not proved here:

1. the entry-locked leaf-pentagon class (G6PP), without claiming a finite
   router list;
2. the corresponding fully shared octacyclic residuals, which are outside the
   disconnected hypothesis.

Accordingly this note does not prove the octacyclic cactus theorem. It reduces
the disconnected part to the single explicitly quantified locked-entry class
(G6PP), proves all disconnected `T^7Q`, and removes `P|T^6|P` from the gap
list.
