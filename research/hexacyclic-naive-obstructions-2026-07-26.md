# Hexacyclic cacti: obstructions to naive triangular leaf deletion

## Scope

This note adversarially tests the following proposed proof template for a
connected hexacyclic cactus `G`:

1. find a triangle which is a leaf of a suitable reduced tree;
2. cut off that triangle as a connected induced triangular unicyclic
   territory;
3. apply the pentacyclic positivity theorem to the connected remainder; and
4. add the two strict inequalities by induced-subgraph superadditivity.

Write `sigma(H)=s+(H)-|V(H)|`, `T=C3`, and `P=C5`. The established inputs are

- every triangular unicyclic cactus has `sigma>0`;
- every connected pentacyclic cactus has `sigma>0`;
- these assertions allow arbitrary attached trees and bridge connectors.

Thus the template is valid whenever the triangle territory and pentacyclic
remainder really form a vertex partition into connected induced subgraphs. The
question here is only whether a strict triangular leaf is structurally forced.
It is not. The configurations below are obstructions to this proof strategy,
not counterexamples to positive square energy, and no hexacyclic theorem is
claimed.

The exact sharp-DNN reduction in the companion residual audit leaves only

`TTTTPP` and `TTTTTQ` for arbitrary `Q=Cq` (including `Q=T`).

Accordingly, `TTTTPP` is the relevant leaf-avoidance family: its two pentagons
can occupy both ends of a tree. In `TTTTTQ` with six singleton reduced-tree
marks, the unique `Q` cannot occupy both leaves, so a triangular reduced-tree
leaf is forced. That does not settle `TTTTTQ`, because clustering and shared-cut
locking can still prevent a strict triangle separation.

## Three distinct meanings of a leaf

The naive argument becomes ambiguous unless the tree is specified.

1. In the **reduced cluster tree**, one marked node represents an entire
   shared-cut cluster. A leaf node can therefore contain several cycles.
2. In a fully shared cluster, the **cycle-cut incidence tree** has cycle nodes
   and cut nodes. A triangle may be a leaf cycle node even though there is no
   bridge on which to separate it.
3. A **strict triangle leaf** for the naive strategy must be stronger: there
   must be a vertex partition `V(G)=V(U) dotcup V(R)` such that `U` is a
   connected induced triangular unicyclic cactus and `R` is a connected
   induced pentacyclic cactus.

A bridge-leaf singleton triangle supplies (3): cut the first actual bridge on
its connector and assign all hanging trees by their unique attachment. A leaf
cycle node in the incidence tree generally does not. If `T` meets the rest at
a shared cut vertex `x`, retaining `T` requires its territory to contain `x`,
while retaining the other five cycles may also require the remainder to contain
`x`. A vertex partition cannot do both.

This shared-vertex conflict is the basic local obstruction. The reduced-tree
obstruction below is a different, global one.

## Smallest reduced-cluster-tree obstruction

Let the six cycles be singleton shared-cut clusters. Connect them in series by
arbitrary bridge connectors so that, after suppressing unmarked degree-two
connector nodes, the reduced cluster tree is the marked path

`P1 - T1 - T2 - T3 - T4 - P2`.

Both reduced-tree leaves are pentagons. Every triangle is internal, so there is
no triangular leaf to cut off. This is realizable with single bridge edges
between successive cycles: choose distinct attachment vertices on each
internal cycle for its two incident bridges. More generally, every reduced edge
may be replaced by an arbitrary nontrivial bridge tree and arbitrary hanging
trees may be attached anywhere.

This is the smallest obstruction measured by number of singleton cycle marks.
A tree whose leaves avoid triangles needs at least two nontriangle marks,
because every nontrivial finite tree has at least two leaves. Hence:

- with five triangles and one nontriangle, some triangle is necessarily a
  reduced-tree leaf;
- with four triangles and two nontriangles, the six-mark path above already
  avoids all triangular leaves.

The labels of the two endpoints need not both be `P`: they can be any two
nontriangular cyclic blocks. The hostile `TTTTPP` choice is the unique such
pattern on the exact hexacyclic DNN frontier and is especially relevant because
neither endpoint can itself serve as the desired strict positive triangular
packet.

The colored reduced-tree shape is forced in this minimal case. Any reduced tree
with all leaves among two nontriangle marks has exactly those two leaves and is
therefore the pentagon-ended path; suppressed Steiner structure is impossible
after minimization. There are still arbitrarily many realizations through
connector lengths, attachment positions, and hanging trees. With three or more
nontriangle marks, branching reduced-tree shapes occur, but they are outside
the hexacyclic DNN frontier.

## Reduced cluster nodes can hide every triangle

The leaf-count argument only sees marked clusters, not their internal cycles.
Take one shared-cut cluster `A` containing five triangles and attach a remote
pentagon cluster `B` by any bridge connector. The reduced cluster tree is the
single edge

`A - B`.

Its leaves are clusters, not cycles. The leaf `A` is five-cyclic, so cutting its
connector leaves a five-triangle component and a unicyclic pentagon component,
not a triangular unicyclic component and a pentacyclic remainder. None of the
five triangles is a singleton reduced-tree leaf.

An even smaller cluster-count example has all six cycles in one shared-cut
cluster. Its reduced cluster tree is one marked node and has no connector edge
at all. Consequently any argument of the form “a finite tree has a leaf, so cut
off a triangle” has already lost the relevant information before it starts.

The one-cluster example is smallest in reduced-tree size; the two-cluster
`TTTTT|P` example is the smallest nontrivial reduced tree exposing the mismatch
between a leaf cluster and a leaf cycle.

## Fully shared incidence trees

Suppose all six cycles form one shared-cut cluster, and let `I` be the bipartite
cycle-cut incidence tree. If `c` is the number of shared cut nodes, then

`|E(I)|=c+5`, and sum_x `(deg_I(x)-1)=5`.

Leaf counting in `I` does not recover the naive strategy.

### One-cut bouquet: smallest local bottleneck

Identify one vertex from each of six cycles to one common vertex `x`. For the
hostile mix, take four triangles and two pentagons. The incidence tree is the
star with central cut node `x` and six leaf cycle nodes. In particular every
triangle is a leaf cycle node.

Nevertheless no strict triangle leaf can be separated while all other five
cycles are retained. A territory retaining a chosen triangle contains `x`.
Every other cycle also contains `x`, and a connected induced remainder
retaining any of them must contain `x` as well. Since `x` cannot belong to both
parts, the required two-territory partition does not exist.

This obstruction uses one cut node, the minimum possible for a nontrivial fully
shared cluster, and no connector edges. Opening the triangle at a private
vertex does not implement the proposed strategy: it destroys the triangular
cycle and incurs a tree cost rather than contributing strict triangular
surplus. Assigning `x` to the triangle territory instead opens all five cycles
in the putative remainder.

The same conflict occurs for any leaf cycle node of a fully shared incidence
tree whose unique incident cut node separates it from five retained cycles.
“Leaf in incidence” means pendant through a shared vertex, not vertex-disjoint
separability. The bouquet also obstructs the other DNN residual family: use five
triangles and `Q`, or six triangles when `Q=T`.

### No triangular incidence leaf

There are also fully shared six-cycle incidence trees in which no triangle is a
leaf even in the weak cycle-node sense. A minimal hostile `TTTTPP` example is
the alternating path

`P1 - x1 - T1 - x2 - T2 - x3 - T3 - x4 - T4 - x5 - P2`,

where all five cuts are distinct and each has degree two. Each triangle uses
two distinct vertices, which is feasible on `C3`; both pentagons are incidence
leaves. The incidence-excess sum is exactly five, as required.

Here the naive search fails before the shared-vertex issue is reached: no
triangle cycle node is a leaf. This is also cycle-count minimal for avoiding
triangular leaves, for the same reason as in the reduced tree: a tree needs two
leaves, so two nontriangular cycles are necessary. The path is the unique
unbranched degree pattern when exactly those two cycle nodes are leaves,
although multiway-cut variants can represent different shared incidences.

## Hostile triangle/pentagon census by count

For six singleton clusters in a reduced tree, or six cycle nodes in a fully
shared incidence tree after suppressing cut subdivisions for leaf counting, the
coarse triangle/pentagon threshold is simple. Only its first two rows occur on
the exact DNN frontier (with `P` replaced by arbitrary `Q` in the first row).

| cycle multiset | can all tree leaves be nontriangular? | smallest pattern |
|---|:---:|---|
| `TTTTTP` | no | at least one triangle leaf is forced |
| `TTTTPP` | yes | `P-T-T-T-T-P` path |
| `TTTPPP` | yes | path with pentagonal ends, or a pentagon-ended branch tree |
| `TTPPPP` | yes | many paths and branch trees |
| `TPPPPP` | yes | many paths and branch trees |
| `PPPPPP` | yes | no triangle exists |

This table records only the existence of a triangle leaf in the chosen tree.
It does not certify a strict triangle leaf. In a fully shared bouquet, for
example, `TTTTTP` has five triangular incidence leaves but none is separable by
the desired vertex partition. Thus there are two independent failure modes:

- **leaf avoidance:** two hostile cycles occupy all tree leaves;
- **leaf locking:** a triangle is a tree leaf but its shared cut vertex is
  needed by the pentacyclic remainder.

Pentagons make the first failure spectrally hostile as well as combinatorial.
Writing `delta=sqrt(5)-2`, a bare pentagonal packet has only
`sigma(P)>=-delta`, while triangular strictness has no uniform positive margin.
Therefore replacing the missing leaf reduction by “cut off a pentagon and use
the remaining strict triangles” is not justified by the current packet ledger.
A growing star attached at a triangle vertex can drive its positive surplus to
zero, so an unspecified strict triangle cannot silently pay `delta`.

## Arbitrary connectors do not repair the obstructions

The reduced-path obstruction is stable under all connector complications
allowed in the cactus theorem.

- Replace any reduced edge by a path of bridge blocks of arbitrary length.
- Replace a connector path by a bridge tree with unmarked Steiner branches.
- Attach arbitrary finite trees at any cycle or connector vertex.
- Let several hanging branches have the same attachment root.

After taking the minimal subtree spanning cycle clusters and suppressing only
unmarked degree-two nodes, the marked leaves remain the two pentagons. A
Steiner branch can be assigned to one territory and cut on actual incident
bridges, but this allocation does not turn an internal triangle mark into a
leaf.

Likewise, connector entry position can make a coarse cluster picture less
useful, never more automatic. A connector may enter a shared cluster through a
private cycle vertex, a shared cut, or an attached cycle. Two external routes
may enter through the same attached triangle. The pentacyclic repairs for
`TTTP|P` and `TTP|T|P` required entry-sensitive interval splits precisely
because cluster labels alone do not determine valid induced territories. A
hexacyclic induction that simply deletes an abstract leaf while ignoring its
actual entry vertex inherits the same gap.

For fully shared obstructions, adding bridge connectors or hanging trees
outside the cyclic core cannot split a shared cut vertex. The one-cut bouquet
therefore remains locked under arbitrary attachments. Subdividing incidence
edges is not available without changing shared incidence into bridge
separation; when one does change it, the resulting reduced-tree type must be
reanalyzed rather than identified with the original bouquet.

## Smallest obstruction catalogue

The following examples separate the logically different defects.

| obstruction | cycles | reduced clusters | shared cut nodes | why the naive step fails |
|---|---:|---:|---:|---|
| all-six bouquet | 6 | 1 | 1 | triangle incidence leaves share the indispensable vertex `x` |
| alternating fully shared `TTTTPP` path | 6 | 1 | 5 | both incidence leaves are pentagons |
| `TTTTT|P` | 6 | 2 | at least 1 inside first cluster | a leaf cluster is not a one-cycle leaf |
| singleton `P-T-T-T-T-P` | 6 | 6 | 0 | both reduced-tree leaves are pentagons |

Minimality is meant only in the displayed structural parameter and within a
six-cycle problem:

- one cluster is the smallest reduced cluster tree;
- one shared cut is the smallest nontrivial fully shared incidence;
- two nontriangle cycles are the minimum needed to occupy both leaves of a
  nontrivial tree;
- six singleton clusters are required when the obstruction is specifically
  that every one of four triangle marks is internal.

No claim is made that these cores minimize graph order after all choices of
cycle lengths, identifications, and connector subdivisions. The bare bouquet
orders are easy to compute, but graph-order minimality is not the point of this
audit.

## What a viable hexacyclic proof would need instead

The pentacyclic theorem remains a powerful induction input, but it cannot be
invoked by leaf counting alone. A replacement argument must address at least
one of the following.

1. **A non-leaf deletion lemma.** Split an internal cycle or connector into
   induced territories while preserving a connected pentacyclic packet, with
   entry positions audited.
2. **Quantitative pentacyclic margins.** If opening a triangle or hostile cycle
   creates a tree cost of one or a pentagonal deficit, the remainder needs a
   certified margin large enough to pay it. Bare positivity is insufficient.
3. **Six-cycle incidence analysis.** Fully shared bouquets, alternating paths,
   multiway cuts, and hub configurations need direct packetizations or phase
   estimates; incidence leaves cannot simply be treated as bridge leaves.
4. **Adaptive reduced-tree packetization.** For `TTTTPP`, the pentagon-ended
   path suggests packets such as `TP`, a middle tetracyclic territory, and
   `TP`, rather than deletion of one triangle. Such a decomposition must be
   checked against actual connector entries and shared clusters.
5. **A genuine shared-cut separation lemma.** Any proposed lemma must state
   which cycles are retained after assigning a common cut vertex. It cannot
   allocate that vertex to two induced territories.

The smallest adversarial cores show that both global tree geometry and local
shared-vertex geometry must enter. They rule out the naive universal strategy
“cut off a strict triangle leaf and use pentacyclic positivity” as stated, but
they do not indicate that any hexacyclic cactus violates `s+(G)>|V(G)|`.

## Status

This is a structural no-go audit for one induction template. It gives explicit
realizable cactus cores, explains their stability under arbitrary connectors
and attached trees, and identifies minimality in several combinatorial senses.
It contains no theorem claim about all connected hexacyclic cacti and no
spectral counterexample.
