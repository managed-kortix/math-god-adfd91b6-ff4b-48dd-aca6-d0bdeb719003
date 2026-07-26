# The `{3,3,5,5}` tetracyclic cactus: packet proof

## Statement and scope

Let `G` be a connected cactus of order `n` whose four cyclic blocks have
lengths `3,3,5,5`. The bridge-block incidence, the lengths and branching of
all connector trees, and all trees attached at cycle or connector vertices
are arbitrary. Then

`s+(G)>n`.

This proof is internal to the `{3,3,5,5}` family. The sharp DNN residual
classification is not needed: DNN explains why this family arose, but none of
its inequalities is used below.

The proof uses induced-subgraph superadditivity

`s+(G) >= sum_j s+(G[V_j])`                              (1)

for every vertex partition `(V_j)`, together with the following previously
proved packet bounds. If `h` is the packet order and
`delta=sqrt(5)-2`, then arbitrary tree attachments are allowed in every row.

| cyclic blocks in a connected packet | bound | credit over `h` |
|:---|:---|:---|
| tree | `s+=h-1` | `-1` |
| one triangle | `s+>h` | `0`, strict |
| two triangles | `s+>h+1` | `1`, strict |
| one pentagon | `s+>=h-delta` | `-delta=2-sqrt(5)` |
| triangle and pentagon | `s+>h+1-delta` | `1-delta=3-sqrt(5)`, strict |
| two pentagons | `s+>=h` | `0` |
| two triangles and one pentagon | `s+>h+2-delta` | `2-delta=4-sqrt(5)`, strict |
| one triangle and two pentagons | `s+>h` | `0`, strict |

The last row is sufficient in its weak quantitative form; some connected
shared-cut incidences have the stronger bound `h+6-2sqrt(5)`. The rows are
dependencies, not new claims proved by the finite audit in this note.

## Cyclic clusters and the tree bookkeeping

Join two cyclic blocks when they share a cut vertex. A *shared cluster* is a
connected component of this relation. Contract each shared cluster and each
maximal bridge-only part between clusters. Because `G` is a cactus, the
resulting cluster incidence is a tree: a cycle in the contracted incidence
would produce a cycle using bridge blocks, contrary to the list of cyclic
blocks.

Every edge outside the cyclic blocks is a bridge. Hence deleting a selected
connector edge partitions the vertices into the vertex sets of two connected
induced subgraphs. Repeating this operation gives induced territories for any
connected pieces of the cluster tree. No edge is deleted from either induced
packet; only cross edges are ignored in (1).

There are two equivalent ways to see that arbitrary connector trees and
hanging trees cause no bookkeeping gap.

1. After connector cuts, each remaining bridge-tree component lies wholly on
   one side of every cut and stays with that side.
2. For a fixed connected cyclic core, every component outside the core has a
   unique core root. Existence follows from connectivity. If one component
   met two distinct core vertices, its internal path between them together
   with a core path would create an additional cycle. Assign the entire
   rooted component to the unique packet containing its root.

Thus every core partition below extends to a genuine partition of `V(G)`.
Each extended packet has exactly the advertised cyclic blocks and otherwise
arbitrary trees, so the packet bounds apply without replacing a tree by a
star or bounding a connector length.

## Disconnected shared-cluster graph

Assume first that there is more than one shared cluster. Ordinary connector
cuts reduce the proof to the possible distributions of four cycles among the
clusters.

### A `3+1` distribution

Cut the connector incident with the singleton leaf cluster. If that cycle is
a triangle, its packet has strict credit `0`, while the complementary
tricyclic cactus has credit at least `0`; (1) gives `s+(G)>n`.

If the singleton is a pentagon, the complementary packet necessarily has
blocks `{3,3,5}`. This is the genuinely least favorable leaf cut:

`{3,3,5} | {5}`.                                          (2)

This cut must be retained exactly rather than replaced by two separate
triangle/pentagon estimates. The two packet rows give

`s+(G) > (h+2-delta) + (k-delta)`

`        = n+2-2delta = n+6-2sqrt(5) > n`.                 (3)

This is the hostile `{335}|5` induced partition. Both sides include their
full connector-rooted trees, so (3) covers every connector length and shape.

### A `2+2` distribution

One connector cut gives either

- `{3,3}|{5,5}`, with total credit strictly greater than `1+0`; or
- `{3,5}|{3,5}`, with total credit strictly greater than
  `2(1-delta)=6-2sqrt(5)>0`.

In both cases (1) proves the result.

### A `2+1+1` distribution

Cut the two connector edges of the three-node cluster tree. According to the
two-cycle cluster, the total credits are

- `{3,3}|{5}|{5}`: strictly greater than
  `1-2delta=5-2sqrt(5)>0`;
- `{3,5}|{3}|{5}`: strictly greater than
  `1-2delta=5-2sqrt(5)>0`;
- `{5,5}|{3}|{3}`: strictly greater than `0`.

### A `1+1+1+1` distribution

If the four-node cluster tree has a triangle leaf, isolate it; the remaining
tricyclic cactus has `s+>=` its order, and the triangle is strict. If it has no
triangle leaf, both triangles are internal and a pentagon is a leaf. Removing
that leaf leaves the connected `{3,3,5}` territory, so the hostile partition
(2)--(3) applies. This exhausts the ordinary disconnected-cluster cases.

## One connected shared cluster

Now every pair of adjacent cycle blocks in the block-cut incidence meets at a
cut vertex. The bare cyclic core has 13 vertices and 16 edges. Exact
generation by recursively adjoining leaf blocks, followed independently by
exact graph isomorphism and canonical colored-cycle coding, gives precisely
20 quotient types. Cycles are ordered `T0,T1,P2,P3`; an incidence string such
as `012+23` records the sets of cycles meeting at each shared cut vertex.

For each type, the audit exhausts every partition of the 13 core vertices
into connected induced packets whose cycle contents have one of the proved
rows above. A subset DP anchors each new part at the least remaining vertex,
so packet order creates no duplicates. Every induced subset is checked for
connectivity, and its number of retained listed cycles is checked against its
cyclomatic number. Exact credits lie in `Z+Z sqrt(5)` and are compared by
integer sign and squaring tests, not floating point.

The resulting optimal certificates for types 2--20 are:

| type | incidence | packet cycle contents | total credit |
|---:|:---|:---|:---|
| 2 | `012+03` | `P3`; `T1,P2` | `5-2sqrt(5)`, strict |
| 3 | `012+23` | `P3`; `T0,T1` | `3-sqrt(5)`, strict |
| 4 | `012+23` | `P3`; `T0,T1` | `3-sqrt(5)`, strict |
| 5 | `023+01` | `P2,P3`; `T1` | `0`, strict |
| 6 | `01+02+03` | `P2`; `T1,P3` | `5-2sqrt(5)`, strict |
| 7 | `01+02+13` | `P2`; `T1,P3` | `5-2sqrt(5)`, strict |
| 8 | `01+02+23` | `P3`; `T0,T1` | `3-sqrt(5)`, strict |
| 9 | `01+02+23` | `P3`; `T0,T1` | `3-sqrt(5)`, strict |
| 10 | `023+12` | `T1`; `T0,P3` | `3-sqrt(5)`, strict |
| 11 | `02+03+12` | `T1`; `T0,P3` | `3-sqrt(5)`, strict |
| 12 | `02+12+23` | `T1`; `T0,P3` | `3-sqrt(5)`, strict |
| 13 | `02+12+23` | `T1`; `T0,P3` | `3-sqrt(5)`, strict |
| 14 | `023+12` | `T1`; `T0,P3` | `3-sqrt(5)`, strict |
| 15 | `02+03+12` | `T1`; `T0,P3` | `3-sqrt(5)`, strict |
| 16 | `02+12+23` | `T1`; `T0,P3` | `3-sqrt(5)`, strict |
| 17 | `02+12+23` | `T1`; `T0,P3` | `3-sqrt(5)`, strict |
| 18 | `02+13+23` | `T1`; `T0,P2` | `3-sqrt(5)`, strict |
| 19 | `02+13+23` | `T1`; `T0,P2` | `3-sqrt(5)`, strict |
| 20 | `02+13+23` | `T1`; `T0,P2` | `3-sqrt(5)`, strict |

Here the omitted core vertices in a displayed packet decomposition are not
discarded: the exact vertex subsets are in the audit ledger, and every vertex
belongs to exactly one packet. The cycle-content table is only the concise
proof summary. Since `5-2sqrt(5)>0`, `3-sqrt(5)>0`, and type 5 has total credit
zero with a strict triangular packet, (1) proves `s+(G)>n` for types 2--20.

### Type 1: the common-root bouquet

Type 1 has incidence `0123`: all four cycles have one common cut vertex `c`.
The two-packet table used in the finite audit has optimum credit `-1`, so that
audit alone does **not** prove this type.

Use instead the common-root cycle-bouquet phase theorem. Its exact two-state
lobe calculation and matching-BP elimination include arbitrary trees at all
core vertices. For a bouquet of `r` cycles, it gives

`s+(G) >= n+r-1-sum_(ell=1 mod 4) (sec(pi/ell)-1)`.         (4)

Here `r=4`; only the two pentagons occur in the adverse sum. Therefore

`s+(G) >= n+3-2(sqrt(5)-2)`

`        = n+7-2sqrt(5)>n`.                                 (5)

This is the required common-root bouquet exception to the type-2--20 audit.
It uses the separately recorded exact common-root phase argument, not an
unrecorded tetracyclic certificate or DNN argument.

## Exhaustion and conclusion

The shared-cluster graph is either disconnected or connected. The
disconnected case is exhausted by the integer distributions `3+1`, `2+2`,
`2+1+1`, and `1+1+1+1`, with ordinary bridge cuts except for the explicit
hostile `{3,3,5}|{5}` calculation. The connected case is exhausted by the
20-type exact census; types 2--20 have induced packet certificates and type 1
is the common-root bouquet calculation (4)--(5). The unique-root assignment
extends every finite core partition over arbitrary attached trees, while
actual bridge cuts cover arbitrary connector trees. Therefore every graph in
the stated family satisfies `s+(G)>n`.

## Dependency and reproduction paths

The logical dependencies are:

- induced-subgraph superadditivity and the packet table:
  `all-tricyclic-cacti/paper.tex`, especially the phase-and-packet lemma;
- arbitrary `{3,3,5}` tricyclic packets:
  `research/c3-c3-cq-tricyclic-cactus-2026-07-25.md`;
- arbitrary bicyclic cactus packets, including mixed and two-pentagon cases:
  `all-bicyclic-cacti/paper.tex`;
- connected shared-cut `{3,5,5}` and its bouquet coefficient certificate:
  `research/c3-c5-c5-shared-cluster-2026-07-25.md` and
  `positive-square-energy/experiments/c3_c5_c5_shared_cluster_certificate.py`;
- the direct type-1 common-root phase theorem:
  `research/common-root-cycle-bouquet-phase-2026-07-26.md`;
- the 20-type `{3,3,5,5}` census:
  `research/c3-c3-c5-c5-shared-cluster-census-2026-07-25.md` and
  `positive-square-energy/experiments/c3_c3_c5_c5_shared_cluster_certificate.py`;
- the exact induced-packet DP, including full vertex subsets:
  `research/c3-c3-c5-c5-induced-packet-partition-audit-2026-07-26.md` and
  `positive-square-energy/experiments/c3_c3_c5_c5_induced_packet_partitions.py`.

Reproduce the finite part with

```sh
python positive-square-energy/experiments/c3_c3_c5_c5_induced_packet_partitions.py
```

The expected summary is

```text
SUMMARY exact_positive=18/20 strict_target=19/20 minimum_score=-1 minimum_decimal=-1.000000000000
```

That line must be interpreted correctly: `19/20` covers exactly types 2--20;
the missing type 1 is supplied analytically by (4)--(5). The computation does
not prove the packet dependencies, the arbitrary-tree extension, or the
disconnected-cluster argument. Conversely, those structural arguments do not
replace the finite 20-type census. Subject to the cited packet theorems and
exact scripts, the two parts together form the complete proof recorded here.
