# Pentacyclic cactus theorem: hostile disconnected-cluster audit

## Decision

Subject to the stated assumption that the two fully shared residual proofs are
accepted, every connected pentacyclic cactus `G` satisfies

`s+(G) > |V(G)|`.

The two proposed repairs, `TTTP|P` and `TTP|T|P`, are valid, but only after
the connector entry topology is made explicit. A proof that merely lists the
cluster multisets is incomplete: a reduced connector can enter an internal
cycle, an attached triangle, a shared cut, or two routes can enter the same
attached triangle. The interval constructions below cover all of these cases.

## Input ledger

Put `sigma(H)=s+(H)-|V(H)|`, `T=C3`, `P=C5`, and
`delta=sqrt(5)-2<1/2`. We use the established bounds, all stable under
arbitrary attached trees and bridge connectors:

- `sigma(T)>0`, `sigma(P)>=-delta`;
- `sigma(TT)>1`, `sigma(TP)>1-delta`;
- every bicyclic or tricyclic cactus has nonnegative surplus;
- a connected shared-cut `TTT` cluster has `sigma>2`;
- a connected shared-cut `TTTT` cluster has `sigma>3`;
- a connected shared-cut `TPP` cluster has
  `sigma>6-2sqrt(5)>3/2`;
- every tetracyclic cactus has positive surplus.

For the `TTTT` entry, packing at most two gives `sigma>3`. The only
packing-three shared-cut incidence is the central-triangle/three-petal core,
for which the established direct Sachs argument again gives `sigma>3`.

Connector territories are always cut on actual bridge edges. At a Steiner
branch, assign the branch vertex to one side and cut one bridge on every other
side. Every hanging tree has a unique attachment to the retained cyclic hull
and is assigned wholly to the territory containing that attachment. Thus all
territories below are connected and induced; no edge-monotonicity assertion is
being used.

## Exact DNN reduction

If the five cycle lengths are `l1,...,l5`, the optimized cactus DNN bound is

`sigma(G) >= 4-sum_i epsilon_li`,

where `epsilon_3=1`, even cycles contribute zero,
`epsilon_5=5-2sqrt(5)`, the odd sequence decreases, and
`epsilon_5+epsilon_7<1`.

If there are at most two triangles, then

`sum epsilon_li <= 2+3 epsilon_5<4`.

With three triangles, the sum can reach four only when both remaining cycles
are pentagons. With at least four triangles the cycle multiset is `TTTTQ`,
where `Q` is arbitrary and includes the all-triangle case. Hence the only DNN
residual families are

`TTTTQ` and `TTTPP`.

## Disconnected `TTTTQ`

Up to equal-cycle permutation, the proper shared-cut cluster partitions are

`TTTT|Q`, `TTTQ|T`, `TTT|TQ`, `TTQ|TT`,

`TTT|T|Q`, `TT|TT|Q`, `TTQ|T|T`, `TT|TQ|T`,

`TT|T|T|Q`, `TQ|T|T|T`, and `T|T|T|T|Q`.

They are all positive as follows.

| partition | certificate |
|---|---|
| `TTTT|Q` | `>3-delta_q>0` when `Q=1 mod 4`; the other parities are nonhostile |
| `TTTQ|T` | positive tetracyclic territory plus a strict `T` |
| `TTT|TQ` | `>2+(1-delta_q)>0` |
| `TTQ|TT` | nonnegative tricyclic territory plus `>1` |
| `TTT|T|Q` | `>2+0-delta_q>0` |
| `TT|TT|Q` | `>2-delta_q>0` |
| `TTQ|T|T` | nonnegative territory plus two strict triangles |
| `TT|TQ|T` | `>1+(1-delta_q)+0` |
| `TT|T|T|Q` | `>1+0+0-delta_q>0` |
| `TQ|T|T|T` | `>1-delta_q` plus strict triangles |

Here `delta_q=sec(pi/q)-1<1` in the hostile `1 mod 4` case. An even unicyclic
territory has zero surplus, and a `3 mod 4` one is favorable.

For five singleton clusters, inspect the minimal reduced tree spanning their
marked nodes. Every leaf is marked. If a triangle is a leaf, cut its first
bridge: it gives a strict triangular territory and the connected remainder is
tetracyclic, hence has positive surplus. If no triangle is a leaf, every leaf
would have to be the unique `Q` node, impossible because a finite nontrivial
tree has at least two leaves. This proves the last partition without assuming
that the reduced tree is a path.

## Disconnected `TTTPP`: complete partition list

The 15 proper colored set partitions are

`TTTP|P`, `TTT|PP`, `TTPP|T`, `TTP|TP`, `TPP|TT`,

`TTT|P|P`, `TTP|T|P`, `TT|TP|P`, `TT|T|PP`,
`TPP|T|T`, `TP|TP|T`, `TT|T|P|P`, `TP|T|T|P`,
`PP|T|T|T`, and `T|T|T|P|P`.

Apart from the first and seventh rows, direct packet accounting gives:

| partition | lower surplus |
|---|---:|
| `TTT|PP` | `>2+0` |
| `TTPP|T` | positive tetracyclic territory plus a strict `T` |
| `TTP|TP` | `>0+(1-delta)` |
| `TPP|TT` | `>(6-2sqrt(5))+1` |
| `TTT|P|P` | `>2-2delta` |
| `TT|TP|P` | `>1+(1-delta)-delta` |
| `TT|T|PP` | `>1+0+0` |
| `TPP|T|T` | `>6-2sqrt(5)` plus strict triangles |
| `TP|TP|T` | `>2(1-delta)` plus a strict triangle |
| `TT|T|P|P` | `>1-2delta` plus a strict triangle |
| `TP|T|T|P` | `>1-2delta` plus strict triangles |
| `PP|T|T|T` | nonnegative `PP` plus strict triangles |

For five singleton clusters, the leaf argument must not be replaced by an
unsupported claim about a linear cycle order. If a triangle is a reduced-tree
leaf, separate it and invoke the tetracyclic theorem on the remainder. If no
triangle is a leaf, all leaves are the two pentagons. The tree then has exactly
two leaves and is a path, with all three triangle marks internal. Cutting the
path into `TP`, `T`, and `TP` territories gives total surplus
`>2(1-delta)>0`. This is exhaustive even in the presence of suppressed
Steiner vertices.

## Repair 1: `TTTP|P`

Let `A` be the shared-cut `TTTP` cluster and let `P1` be the remote pentagon.
If two of the three triangles of `A` meet, the accepted fully shared `TTTQ`
argument gives `sigma(A)>1`; therefore

`sigma(A)+sigma(P1)>1-delta>0`.

Otherwise the three triangles are pairwise disjoint. Incidence-tree
acyclicity forces the pentagon `P0` in `A` to be central, with the triangles
attached at three distinct vertices `x1,x2,x3`.

Let the connector from `P1` first meet the cyclic core of `A` at `z`.

- If it enters through a triangle `Ti` (including at `xi`), put `Ti`, the
  connector, and `P1` in one territory. Put `P0-xi` and the other two
  triangles in the other. These are `TP` and `TT` territories.
- If it enters `P0` at a private vertex `z`, cyclically order
  `z,x1,x2,x3`. Choose a mark `xi` adjacent to `z` in this cyclic order and
  split `P0` at the two boundary edges of the interval containing `z,xi`.
  That interval, its triangle, the connector, and `P1` form `TP`; the
  complementary proper interval and the other two triangles form `TT`.

An entry through a tree branch rooted at a core vertex is the corresponding
core-vertex case. All branches rooted at a boundary vertex go with the
territory owning that vertex. Consequently

`sigma(G)> (1-delta)+1>0`.

This repair is topology-complete. Merely saying “pair the remote pentagon with
a triangle” would not be enough, because the common cut vertex cannot be
assigned to both packets; splitting `P0` is essential.

## Repair 2: `TTP|T|P`

Let `A` be the `TTP` cluster and let `B=T3`, `C=P1` be the singleton clusters.
If the two triangles in `A` share a cut, the shared-triangle packet bound and
the singleton bounds already give a positive total. Thus assume the incidence
inside `A` is the distinct-cut chain

`T1-P0-T2`,

where `T1,T2` meet `P0` at distinct vertices `x1,x2`.

Use the actual minimal connector tree on the three marked clusters, not an
imagined linear order.

### The `B-C` path avoids `A`

Take the entire `B-C` connector subtree as one `TP` territory and `A` as the
other territory. The former has surplus `>1-delta`; the latter is a
tricyclic cactus and has nonnegative surplus. This includes a genuine Steiner
`Y`, because the branch vertex is assigned to the `B-C` territory and the
`A` branch is cut on an actual bridge.

### The `B-C` path passes through `A`

There are two connector entries into the cyclic core of `A`.

- Treat an entry through `Ti`, including an entry at the shared vertex `xi`,
  as a mark at `xi` forced to travel with `Ti`. An entry at a private vertex
  of `P0` is marked at that vertex. If both external entries are forced to the
  same `Ti`, put both external cycles, both connector branches, and all of
  `Ti` in one `TTP` territory. Put `P0-xi` and the other triangle in a strict
  triangular territory.
- Suppose the external pentagon entry is forced to `Ti`, but the external
  triangle entry is not. Isolate the mark `xi` by two cuts of `P0`. Its
  interval carries `P1+Ti`, hence is `TP`; the complementary interval carries
  `T3+Tj`, hence is `TT`. If instead the external triangle is forced to `Ti`,
  isolate `xi` on the `TT` side and put `P1+Tj` on the complementary `TP`
  side.
- It remains that both external entries occur at private vertices of `P0`.
  If they coincide, take an interval containing that common mark and one
  adjacent `xi`; it gives `TTP`, while the complement gives `T`. If they are
  distinct, cyclically order the four marks consisting of the two entries and
  `x1,x2`. One neighbor of the pentagon-entry mark is an `xi` such that the
  other `xj` is adjacent to the triangle-entry mark: this is immediate from
  the three possible cyclic orders of two labeled external marks and two
  unlabeled triangle marks. Cut in the two gaps between these adjacent pairs.
  The two intervals carry respectively `P1+Ti` and `T3+Tj`, so they are `TP`
  and `TT`.

These cases also cover coincident entries at a shared vertex: both external
cycles are then forced to the same `Ti`, which is the first case. Every
interval is proper because both resulting sides contain a marked vertex of
`P0`.

Thus every entry pattern gives either

`TP + TT`, with surplus `>(1-delta)+1`,

or `TTP + T`, with nonnegative plus strict surplus. This covers entries on
private cycle vertices, shared cuts, attached triangles, and coincident
attachment roots.

## Theorem proof

Let `G` be a connected pentacyclic cactus. The DNN estimate proves
`sigma(G)>0` unless its cycle multiset is `TTTTQ` or `TTTPP`. If the shared-cut
graph is connected, the two assumed fully shared theorems apply. If it is
disconnected, the exact colored set partitions are the 11 and 15 rows listed
above. Connector territories and the displayed packet bounds settle every row;
the only rows not settled by direct addition are closed by the two topology
lemmas and the explicitly audited all-singleton leaf argument. Therefore

`s+(G)>|V(G)|`.

## Publication recommendation

**Accept after integration, not as currently scattered notes.** There is no
remaining mathematical blocker under the assumed fully shared results. Before
submission, the manuscript must include:

1. the exact 11-row and 15-row colored cluster-partition lists;
2. the reduced-tree leaf argument for both all-singleton rows;
3. the entry-sensitive interval proofs for `TTTP|P` and `TTP|T|P`;
4. an explicit statement that cuts occur on actual bridge edges and that
   hanging trees are assigned by their unique cyclic-hull attachment.

Omitting any of these would leave a real enumeration or inducedness gap, not a
cosmetic exposition issue.
