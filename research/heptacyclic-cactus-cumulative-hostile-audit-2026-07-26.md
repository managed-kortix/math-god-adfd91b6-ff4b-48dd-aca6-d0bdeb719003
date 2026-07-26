# Hostile independent audit: connected heptacyclic cacti

**Date:** 2026-07-26

## Verdict

**ACCEPT, with one nonfatal certificate defect that must be repaired before the
`T^6Q` census is cited with its printed counts.**

The cumulative mathematical argument proves that every connected heptacyclic
cactus `G` satisfies

`s+(G)>|V(G)|`.

The proof does not need the defective counts: the uniform fully shared `T^6Q`
leaf-or-split lemma proves that family directly, and the valid subcensus still
has the same sole SAFE exception (the bouquet). Nevertheless,
`research/heptacyclic-t6q-incidence-census.py` omits the triangle degree cap
after leaf extension and consequently counts unrealizable incidence trees.
Its tables are not presently valid cactus censuses.

## Proof coverage

The proof tree is exhaustive:

1. The sharp DNN estimate gives
   `sigma(G)>=6-sum epsilon_li`, where `sigma=s+-n`. Exact monotonicity and
   comparisons leave only `T^6Q` and `T^5PP`.
2. If the shared-cut graph is disconnected, `T^6Q` is closed by a `Q`-free
   all-triangle leaf cluster of the reduced cluster tree. The rank ledger
   handles `r=1,...,6`, with the only negative remote term paid by
   `sigma(A_6)>1` against `delta_q<1`.
3. All 46 proper colored cluster partitions of `T^5PP` are present. The exact
   ledger directly closes 41. Four exceptional rows reduce to either a
   triangle leaf plus a hexacyclic complement or a forced path packetization.
   The final `T^5P|P` row is closed by the exhaustive internal-pentagon degree
   dichotomy `d=1` versus `d>=2`.
4. If all cycles form one shared-cut cluster, `T^6Q` is closed by inspecting
   `Q`: open it when it is an incidence leaf, retaining `A_6`, and split it
   into all-triangle incidence branches when it is internal.
5. Fully shared `T^5PP` is closed by inspecting the two pentagons: if both are
   incidence leaves, open both and retain `A_5`; otherwise split an internal
   pentagon. The mixed branch is nonnegative/positive, or a singleton hostile
   pentagon is paid by a forced `A_2`-or-larger branch.

These cases cover every connected heptacyclic cactus after the DNN reduction.

## Hostile checks

### Sharp DNN reduction

The block identity `b+sum li=n+6`, the exact cactus DNN constant, and
`s++s-=2(n+6)` give the stated lower bound. The residual classification is
correct: at most four triangles gives `4+3 epsilon_5<6`; exactly five is
residual only for two pentagons; six or seven triangles is `T^6Q`. The strict
comparisons are supplied without floating point.

### The 46 disconnected `T^5PP` partitions

The partition recursion was rerun and returns `47` partitions including the
one-cluster row, hence `46` proper rows, split as `41+5`. The five emitted rows
match the note. The script is only a color-ledger certificate, but the note
correctly supplies the missing topology and connector-entry arguments.

### The `T^5P|P` internal-degree proof

Deleting the internal pentagon node produces `d` nonempty triangle-bearing
incidence components, with `1<=d<=5`.

- For `d>=2`, one-mark consecutive intervals exist because the marks are
  distinct vertices of the pentagon. The entry branch plus the remote
  pentagon has type `T^rP`; every other branch is a strict all-triangle packet.
  The only zero-bound mixed possibility is accompanied by a strict branch.
- For `d=1`, the internal pentagon has four cyclically private vertices, so an
  opening can avoid the connector entry. The remote pentagon also has an
  opening away from its unique connector. The five triangles remain one
  shared-cut component after deleting the leaf pentagon node, and
  `sigma(A_5)>2` strictly pays the two tree territories.

No incidence leaf is mistaken for a bridge leaf and no cut gets two owners.

### `T^6Q` census completeness by leaf extension

The inverse construction itself is exhaustive. Every bipartite incidence tree
has at least two cycle leaves; at most one is `Q`, so a leaf `T` exists. Removing
it either leaves its cut with degree at least two, or suppresses a now-degree-one
cut. These are exactly the two inverse extensions implemented by the script.

However, the implementation checks the triangle degree cap only in the rank-six
seed (`lines 136-137`) and not after attaching the new leaf to an existing cut
(`lines 171-176`). This creates trees in which an old triangle has incidence
degree four, impossible for a triangle. For example, the generated `q=3`,
`c=4` edge set

`((0,7),(0,8),(0,9),(0,10),(1,7),(2,8),(3,9),(4,9),(5,10),(6,9))`

has `deg(T_0)=4`. Filtering all such objects changes the total rows to:

| regime | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | total |
|---|---:|---:|---:|---:|---:|---:|---:|
| `q=3` | 1 | 8 | 33 | 71 | 74 | 29 | 216 |
| `q=4` | 1 | 8 | 33 | 73 | 77 | 32 | 224 |
| `q=5` | 1 | 8 | 33 | 73 | 78 | 33 | 226 |
| `q=6` or `q>=7` | 1 | 8 | 33 | 73 | 78 | 34 | 227 |

On the filtered valid objects, every nonbouquet still has a SAFE split and the
bouquet remains the unique exception. More importantly, Lemma 2.1 in the
sacrifice/splitting note proves fully shared `T^6Q` without any census.
Therefore this is a blocker to the printed census claim, not to the theorem.

### `T^5PP` SAFE ledger and three exceptions

The independent generator enforces triangle degree at most three and pentagon
degree at most five. Rerunning it reproduces `560=557+3`, the SAFE-choice
distribution, and the three canonical exceptions. Its retained-incidence tests
guard every stronger packet bound.

All three exceptions have both pentagons as incidence leaves. Simultaneous
private openings are disjoint; deleting two leaves from a tree leaves the five
triangle nodes connected (with irrelevant cut leaves suppressible). Thus the
five triangles form one `A_5` territory and `>2-2=0` closes each exception.
The broader two-pentagon dichotomy also proves every fully shared object without
depending on the census.

### Triangle recurrence

In a shared triangular cluster, an incidence-leaf triangle has two vertices
private from all cyclic blocks. Assigning one such vertex and its rooted
off-core branches to a tree gives exact surplus `-1`; the complement remains
connected and its retained triangles remain one shared-cut cluster. Iterating
from the established `A_4>3` base yields `A_r>7-r`, in particular `A_5>2` and
`A_6>1`. Strictness survives weak superadditivity because the base inequality
is strict and every tree charge is exact.

### Arbitrary attachments and connectors

The territory and opening lemmas cover arbitrary attached trees. Every
off-core tree component has one hull attachment and follows its owner. Reduced
cluster cuts are made on actual bridge blocks; interval splits assign each
cyclic mark and branch once; private openings take all branches rooted at the
opened vertex. The packet estimates invoked in the ledgers explicitly permit
these attachments, and mixed packets permit arbitrary bridge connectors.

## Required repair

Before publication or use as an exact census certificate:

1. enforce all six triangle degree caps after each rank-seven extension in
   `research/heptacyclic-t6q-incidence-census.py`;
2. replace the asserted count, support, and margin tables in the script and
   `research/heptacyclic-t6q-incidence-census-2026-07-26.md`;
3. preferably retain the census as a consistency check only, since the direct
   `Q` leaf-or-split proof is shorter and stronger.

Subject to that certificate correction, there is no mathematical blocker to
the global strict theorem.
