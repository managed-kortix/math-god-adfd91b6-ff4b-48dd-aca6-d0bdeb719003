# Disconnected shared-cut audit for heptacyclic `T^5PP`

## Scope and result

Write `T=C3`, `P=C5`, and

`sigma(H)=s+(H)-|V(H)|`.

This note treats one residual family only. Let `G` be a connected heptacyclic
cactus with cyclic-block multiset

`T^5PP={T,T,T,T,T,P,P}`,

and assume that the graph on cyclic blocks, with adjacency meaning a shared
cut vertex, is disconnected. Then the induced-territory arguments below prove

`sigma(G)>0`.                                                   (1)

This is not a statement about the fully shared `T^5PP` case, the other
heptacyclic residual family `T^6Q`, or all heptacyclic cacti. No global
heptacyclic claim is made.

The proof has three layers. A conservative packet ledger settles 41 of the 46
proper colored cluster partitions. Four of the five remaining rows follow from
the hexacyclic theorem and a reduced-tree path packetization. The last row,
`T^5P|P`, requires an entry-sensitive split of the internal pentagon or two
admissible openings paid by the shared-five-triangle recurrence.

## 1. Territory rules and quantitative inputs

The *shared-cut clusters* are the connected components of the graph on cyclic
blocks in which two blocks are joined when they share a cut vertex. Contract
the clusters in the cactus block-cut tree, retain the minimal tree spanning the
cluster nodes, and suppress only unmarked degree-two nodes. The result is the
reduced cluster tree `R`. Every leaf of `R` is a marked cluster node.

We use the following established operations.

1. Cutting actual bridge edges partitions any collection of disjoint connected
   subtrees of `R` into connected induced territories. Every connector remnant,
   Steiner branch, and hanging tree is assigned wholly to one owner.
2. If a cycle node is split, its vertices are assigned to nonempty proper
   consecutive intervals. Each incident branch and each marked cut has exactly
   one interval owner. The cycle is destroyed and no separate `-1` charge is
   incurred.
3. Opening a cycle at a private vertex, together with all off-core branches
   rooted there, creates a nonempty induced tree territory of surplus exactly
   `-1`.
4. For a vertex partition into induced subgraphs, `sigma` is superadditive.

Put `delta=sqrt(5)-2<1/2`. The conservative ledger used in the colored audit is

```text
sigma(T)>0,                    sigma(P)>=-delta>-1/2,
sigma(TT)>1,                   sigma(TP)>1-delta>1/2,
sigma(PP)>0                    for one shared-cut cluster,
sigma(H)>=0                    for every bi- or tricyclic cactus,
sigma(H)>0                     for every tetra-, penta-, or hexacyclic cactus,
sigma(TTT)>2,                  sigma(TTTT)>3,
sigma(TTTTT)>2,                sigma(TTTTTT)>1
```

in the last four entries the triangles form one shared-cut cluster. We also use
`sigma(TPP)>6-2sqrt(5)>3/2` for one shared-cut cluster. All bounds permit
arbitrary attached trees; the mixed `TP` bound permits arbitrary bridge
connectors.

The five- and six-triangle bounds are instances of the exact opening
recurrence. If `A_r` is one shared-cut cluster of `r>=4` triangles, opening a
private vertex of an incidence-leaf triangle leaves `A_(r-1)` connected and
costs one tree territory. Starting from `sigma(A_4)>3`,

`sigma(A_r)>7-r`.                                                (2)

In particular, `sigma(A_5)>2`. The connectivity in (2) is shared-cut
connectivity, not merely ordinary connectivity.

## 2. Exact colored-partition classification

A cluster is encoded by `(t,p)`, its numbers of triangles and pentagons.
Choose the first nonzero pair, subtract it from `(5,2)`, and require successive
pairs to be lexicographically nondecreasing. This recursion gives 47 colored
set partitions including the one-cluster partition, hence exactly 46 proper
partitions.

For each cluster, assign the conservative lower bound in Section 1. Add the
bounds, retaining whether at least one inequality is strict. A row is *direct*
when the sum is positive, or is zero with a strict summand. This exact audit
returns 41 direct rows and the following five, and no others:

```text
T|T|T|T|T|P|P,
TTP|T|T|T|P,
TTTP|T|T|P,
TTTTP|T|P,
TTTTTP|P.                                                       (3)
```

The executable proof object is
`research/heptacyclic-t5pp-disconnected-partition-audit.py`. It uses exact
`Fraction` arithmetic, asserts the totals `47`, `46`, and `41+5`, and asserts
the list (3). Thus (3) is an exact colored-partition boundary, not a selection
of apparently difficult rows.

For clarity, the 41 direct rows are listed here in the canonical order emitted
by the recursion:

```text
P|P|T|T|T|TT       P|P|T|T|TTT       P|P|T|TT|TT
P|P|T|TTTT         P|P|TT|TTT        P|P|TTTTT
P|T|T|T|T|TP       P|T|T|TP|TT       P|T|TP|TTT
P|T|TT|TTP         P|TP|TT|TT        P|TP|TTTT
P|TT|TTTP          P|TTP|TTT
PP|T|T|T|T|T       PP|T|T|T|TT       PP|T|T|TTT
PP|T|TT|TT         PP|T|TTTT         PP|TT|TTT
PP|TTTTT
T|T|T|T|TPP        T|T|T|TP|TP       T|T|T|TTPP
T|T|TP|TTP         T|T|TPP|TT        T|T|TTTPP
T|TP|TP|TT         T|TP|TTTP         T|TPP|TTT
T|TT|TTPP          T|TTP|TTP         T|TTTTPP
TP|TP|TTT          TP|TT|TTP         TP|TTTTP
TPP|TT|TT          TPP|TTTT          TT|TTTPP
TTP|TTTP           TTPP|TTT
```

This table concerns cluster colors only. It does not by itself classify the
topology of `R`, the incidence inside a nontrivial cluster, or the location of
an external connector entry. Those issues are handled next.

## 3. The four reduced-tree rows with singleton triangles

The first four rows of (3) have the form

`A_k | T | ... | T | P_1`,                                     (4)

where `0<=k<=4`, `A_0=P_0`, and, for `k>=2`, `A_k=T^kP_0` is one
nontrivial shared-cut cluster. The number of singleton triangles in (4) is
`5-k`, and is therefore nonzero. (The absent value `k=1` is the direct row
`TP|T|T|T|T|P`.)

**Lemma 3.1.** Every row in (4) has positive surplus for every reduced-tree
topology and every connector entry.

**Proof.** If a singleton triangular cluster is a leaf of `R`, cut the first
actual bridge toward the rest. One induced territory is triangular unicyclic
and has strict positive surplus. The other is connected, hexacyclic, and has
strict positive surplus by the verified hexacyclic theorem. This cut neither
opens a cycle nor spends a margin.

Suppose no singleton triangle is a leaf. All leaves of `R` are marked, and the
only remaining possible leaf marks are `A_k` and `P_1`. A finite nontrivial
tree has at least two leaves. Hence both are leaves, there are exactly two
leaves, and `R` is their path. In particular every singleton triangle lies
internally on the `A_k`--`P_1` path; no Steiner arm is possible, because its
terminal marked node would be another leaf.

Let `T_*` be the singleton triangle nearest `P_1`. Cut actual bridges on the
two sides of the path edge packet carrying `T_*` and `P_1`. This gives a `TP`
territory and a connected complementary territory containing exactly five
cyclic blocks. The first has surplus `>1-delta>0`; the second is pentacyclic
and has strict positive surplus. The construction never splits `A_k`, so its
internal incidence and its connector entry are irrelevant. Every suppressed
connector segment and hanging tree is assigned by the bridge-territory rule.
Thus the induced packetization is

`TP + (connected pentacyclic cactus)`,                            (5)

and its total is positive. QED.

This proves the all-singleton row as well: if its leaves are both pentagons,
the path is `P-T-T-T-T-T-P`, and (5) uses either endpoint pair. The more
symmetric `TP+TTT+TP` packetization is also valid, but is not needed.

## 4. The final row `T^5P|P`

It remains to treat two clusters: a fully shared cluster

`A=T^5P_0`

and a bridge-separated pentagon `P_1`. There is one connector. Project its
`A`-end to the first point at which it meets the cyclic hull of `A`; an entry
through a hanging branch travels with the root of that branch.

Let `I(A)` be the bipartite cycle-cut incidence tree of `A`, and let

`d=deg_I(P_0)`.

Since `A` is one shared-cut cluster, `1<=d<=5`. Deleting the cycle node `P_0`
from `I(A)` produces exactly `d` components. Each contains at least one
triangle, and the triangle counts form an ordered composition

`r_1+...+r_d=5`, with every `r_i>=1`.                            (6)

The incident cuts on `P_0` are distinct vertices: a cycle is incident only
once with a given cactus cut node. The components in (6) are therefore the
exact branches at distinct cyclic marks, even when one mark is a multiway cut.

### 4.1 At least two branches

Assume `d>=2`. Split the vertices of `P_0` into `d` nonempty proper
consecutive intervals, one owning each incident mark and its entire component.
Such intervals exist for any `d` distinct marks on a pentagon: cut in one gap
between each consecutive pair of marks, assigning unmarked vertices to an
adjacent interval. If the external entry projects to a private vertex of
`P_0`, assign that vertex and the connector to either adjacent interval. If it
projects to a cut, a triangle, or a branch rooted there, its component already
determines the unique owner. Thus coincident entry/cut positions cause no
duplication.

Adjoin the connector and `P_1` to the interval territory owning the entry.
If that branch has `r` triangles, this territory is a connected cactus of type
`T^rP`:

- for `r=1`, it is a `TP` packet and is strictly positive;
- for `r=2`, it is tricyclic and is nonnegative;
- for `r>=3`, it is at least tetracyclic and is strictly positive.

Every other interval territory contains only the triangles of one component
of (6). It is a connected triangular block graph and is strictly positive.
Because `d>=2`, at least one such strict territory exists even in the sole
non-strict possibility `r=2` for the entry territory. Hence the total packet
sum is strictly positive.

This argument includes the saturated pentagon `d=5`: then (6) is
`1+1+1+1+1`, no private opening is required, and the cyclic split gives one
`TP` territory and four strict `T` territories. It also includes all dispersed
two-, three-, and four-branch configurations.

### 4.2 One branch

Assume `d=1`. All five triangles lie in the one component of `I(A)-P_0`, so
they remain one shared-cut cluster after `P_0` is destroyed. The pentagon
`P_0` has four vertices private with respect to cyclic blocks. If the external
connector enters at one of them, avoid that vertex; otherwise any of the four
is available. Choose such a private vertex `v_0`, and choose a private vertex
`v_1` of the remote pentagon away from its connector entry.

Open `P_i` at `v_i` for `i=0,1`, assigning every off-core tree branch rooted at
`v_i` to the resulting tree territory `F_i`. Each `F_i` is nonempty and

`sigma(F_i)=-1`.                                                (7)

All remaining vertices form one connected induced territory `H`. Indeed, the
five triangles remain connected in their incidence component; `P_0-v_0` is a
path attached to that component at the unique cut incident with `P_0`; and
`P_1-v_1` is a path joined to the retained core by the external connector. If
the connector enters through a triangle or a branch rooted there, that root is
already in the retained triangular component. If it enters on `P_0`, the
choice `v_0` away from the entry keeps the entry on `P_0-v_0`. Thus every
entry location is covered. The only cyclic blocks of `H` are the five
triangles. Deleting the leaf node `P_0` from the incidence tree does not alter
their shared-cut component, so these five triangles are concentrated in one
shared-cut cluster, not merely connected by pentagon remnants. By (2),

`sigma(H)>2`.

Using (7) and induced superadditivity gives

`sigma(G)>=sigma(H)+sigma(F_0)+sigma(F_1)>2-1-1=0`.              (8)

The choices away from the two connector entries ensure that no connector or
hanging branch is split between owners. This closes the one-branch case.

Combining Sections 4.1 and 4.2 proves the last row of (3) for every incidence,
pentagon capacity, cyclic order, and external entry.

## 5. Completeness and hostile audit

The proof tree is exhaustive at each level.

1. The exact colored recursion gives all 46 proper partitions; 41 are direct
   and exactly five are listed in (3).
2. In the first four exceptional rows, either a singleton triangle is a leaf,
   or the only possible leaves are the two pentagon-containing endpoints. The
   latter condition forces a path, so (5) omits no branched reduced topology.
3. The final row has only two reduced-tree marks. Its internal classification
   is the exhaustive dichotomy `d=1` or `d>=2` in the incidence tree of `A`.
4. For `d>=2`, interval ownership explicitly covers entry on `P_0`, at a
   shared cut, through a triangular branch, or through an attached tree. A
   shared cut and all branches rooted there have one owner.
5. For `d=1`, opening vertices exist away from the connector entries, and the
   five-triangle margin is invoked only after shared-cut concentration has been
   checked in `I(A)-P_0`.
6. No qualitative theorem pays a hostile pentagon deficit or a tree opening.
   The hexacyclic and pentacyclic theorems are added only to independently
   strict positive packets. The two opening costs in (8) are paid by the
   quantitative strict margin `>2`.
7. An incidence leaf is never treated as a bridge leaf. Bridge cuts occur only
   in `R`; cycle destruction inside `A` uses either legal intervals or explicit
   private openings.

There are no unresolved cases within the stated disconnected `T^5PP` family.
Fully shared `T^5PP`, every `T^6Q` configuration, and noncactus heptacyclic
graphs are outside this note and are not assessed here. Nothing here asserts
positivity for any of those classes, and no global claim is intended.

## Reproduction

From the repository root run

```bash
python research/heptacyclic-t5pp-disconnected-partition-audit.py
```

The asserted output is

```text
colored partitions including one cluster: 47
proper colored partitions: 46
direct packet rows: 41
topology/entry rows: 5
  P|P|T|T|T|T|T
  P|T|T|T|TTP
  P|T|T|TTTP
  P|T|TTTTP
  P|TTTTTP
```
