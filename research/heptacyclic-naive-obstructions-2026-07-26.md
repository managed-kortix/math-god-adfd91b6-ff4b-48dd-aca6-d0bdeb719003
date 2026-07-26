# Heptacyclic cacti: adversarial residual configurations and packet needs

## Scope

This is a structural no-go note, not a heptacyclic theorem.  It tests two
tempting extensions of the hexacyclic argument:

1. detach a strict triangular leaf and apply the connected hexacyclic theorem
   to the remainder;
2. in a fully shared core, open two cycles into tree territories and pay their
   two units of loss from a concentrated five-triangle packet.

Write `sigma(H)=s+(H)-|V(H)|`, `T=C3`, and `P=C5`.  An *opening* at a private
cycle vertex destroys that cycle and produces a nonempty tree territory of
surplus `-1`.  A retained cycle must keep all its vertices.  Consequently two
retained cycles joined through a shared cyclic cut must belong to the same
induced territory.

The configurations below are realizable cactus cores.  Every bridge edge may
be subdivided or replaced by a bridge tree, and arbitrary trees may be attached
at any vertex.  None is asserted to violate positive square energy.

## 1. The sharp-DNN residual level

For seven cyclic blocks of lengths `l1,...,l7`, the usual cactus DNN ledger is

`sigma(G) >= 6-sum_i epsilon_li`,

where `epsilon_3=1`, `epsilon_5=5-2sqrt(5)=:a`, `3a<2`, `2a>1`, and
`epsilon_5+epsilon_7<1`.  Hence four triangles are uniformly safe because

`4+3a<6`.

With five triangles, the other two cycles reach the threshold only when both
are pentagons.  With at least six triangles there is one unrestricted cycle.
Thus the exact residual multisets for this ledger are

`TTTTTTQ={T1,...,T6,Q}` and `TTTTTPP={T1,...,T5,P1,P2}`.               (R)

This calculation only identifies the frontier on which structural work would
be needed.  It does not prove that either family is positive.

The two naive reductions have different quantitative inputs.  A strict
triangle plus a positive hexacyclic remainder is safe.  By contrast, opening
two cycles costs exactly two, so the second reduction needs a retained packet
with margin strictly greater than two.  The known five-triangle shared-cluster
bound supplies `sigma(TTTTT)>2`, but only when all five retained triangles are
concentrated in the required shared-cut cluster.  Private opening vertices and
concentration are separate hypotheses.

## 2. Four independent failure mechanisms

It is useful not to call all failures a missing leaf.

**Leaf avoidance.**  Every leaf of the reduced cluster tree, or of the
cycle-cut incidence tree, can be nontriangular.

**Leaf locking.**  A triangle can be a leaf cycle node but share the vertex
needed by all other retained cycles.  It is not a vertex-disjoint triangular
territory.

**Sacrifice saturation.**  A cycle selected for opening can use every one of
its vertices as a cyclic cut and therefore have no private opening vertex.

**Sacrifice dispersion.**  The selected cycles can be opened, and the induced
remainder can even remain connected through their path remnants, while the
five retained triangles split into several shared-cut components.  Bare
connectedness does not activate the concentrated `TTTTT>2` estimate.

The last distinction is easy to miss.  Opening an internal cycle at a private
vertex leaves a path containing all of its cut vertices, so it preserves
ordinary connectivity.  It does not make triangles in different branches
share a cyclic cut after the opened cycle itself is no longer retained.

## 3. Reduced-tree obstructions

### 3.1 Pentagon-ended singleton path

Take seven singleton shared-cut clusters connected by bridges in the reduced
path

`P1-T1-T2-T3-T4-T5-P2`.                                           (A1)

Both leaves are hostile pentagons and every triangle is internal.  There is no
strict triangular leaf to place beside a hexacyclic remainder.  This is the
minimal leaf-avoidance pattern on the residual frontier: a finite nontrivial
tree needs two leaves, and two nontriangular cycles are the minimum number that
can occupy both of them.  With `TTTTTTQ`, only one cycle is possibly
nontriangular, so seven singleton marks force a triangular reduced-tree leaf.

Cutting off a pentagon does not repair the proof.  A pentagonal unicyclic
territory has only `sigma>=-delta`, where `delta=sqrt(5)-2`, while the
hexacyclic theorem supplies strict positivity with no uniform margin known from
that theorem alone.  The valid packet suggested by (A1) is instead

`TP + TTT + TP`,                                                   (A1-packet)

or a refinement such as `TP+TT+T+TP`.  The two `TP` packets give fixed positive
margin; the middle all-triangle packet need only be nonnegative.  Actual bridge
cuts and connector ownership still have to be checked.

### 3.2 A leaf cluster is not a leaf cycle

Put six triangles in one shared-cut cluster `A` and join it by one bridge
connector to a remote cycle `Q`:

`TTTTTT | Q`.                                                      (A2)

The reduced tree has two leaves, but cutting either edge side gives ranks six
and one, not `T | hexacyclic`.  The same hiding occurs in `TTTTTP|P` and in
coarser partitions of `TTTTTPP`.  At the extreme, all seven cycles form one
shared-cut cluster and the reduced tree has no edge at all.

The needed input is a cluster-leaf release lemma indexed by the actual entry
vertex.  Depending on whether the connector enters at a private cycle vertex,
a cyclic cut, or through a petal, the output must be one of:

- `T +` a connected hexacyclic territory;
- a fixed-margin mixed packet such as `TP`, `TT`, or `TTP`, plus lower-rank
  nonnegative territories;
- a proper interval split of the entry cycle.

Cluster labels alone do not determine which output is induced.

### 3.3 Two hostile leaves against qualitative positivity

More generally, let `P1` and `P2` be the only leaves of a reduced path and
allow its internal marks to be nontrivial triangle-containing clusters.  Any
argument which successively removes the pentagonal leaves writes a lower bound
containing `-2delta` and only qualitative strict terms.  Strict positivity of a
hexacyclic or lower-rank remainder cannot silently pay either fixed deficit.

The required replacement is a simultaneous packetization which gives each
pentagon a quantitative partner: `TP+TP+X`, `TTP+TP+X`, or a shared `PP`
packet with a proved bound, where `X` is nonnegative or has a separately stated
margin.  This is the multiple-hostile-pentagon obstruction on the exact
heptacyclic frontier.

## 4. Fully shared incidence obstructions

For one shared-cut cluster let `I` be the bipartite incidence tree on seven
cycle nodes and its cyclic-cut nodes.  If there are `c` cut nodes, then

`|E(I)|=c+6`, and `sum_x(deg_I(x)-1)=6`.                           (I)

Thus `1<=c<=6`, triangle incidence degree is at most three, and pentagon
incidence degree is at most five.

### 4.1 Seven-cycle bouquet: maximal leaf locking

Identify one vertex from every cycle to a common cut `x`.  The incidence tree
is a star with seven leaf cycle nodes.  Every triangle is an incidence leaf,
but no retained triangle can be separated from a retained remainder: both
territories would have to own `x`.

The bouquet therefore defeats triangle-leaf induction in the strongest local
way.  It does *not* defeat the ordinary two-opening repair.  In `TTTTTTQ`, open
a private vertex of `Q` and of one triangle; in `TTTTTPP`, open private vertices
of both pentagons.  Five triangles still share `x`, giving the formal ledger

`sigma(G) > 2-1-1 = 0`.

This distinction belongs in any obstruction catalogue: the bouquet is a
minimal obstruction to retained leaf separation, but a positive test case for
private two-cycle sacrifice.

### 4.2 Alternating pentagon-ended incidence path

Use six distinct degree-two cuts in the fully shared core

`P1-x1-T1-x2-T2-x3-T3-x4-T4-x5-T5-x6-P2`.                        (A3)

All six cut nodes in (A3) have degree two, as required by (I).  Both cycle-node
leaves are pentagons, so no triangle is even an incidence
leaf.  This is the fully shared analogue of (A1), and it is minimal by the same
two-leaf argument.

Again, (A3) is not an obstruction to every repair.  Both pentagons have private
vertices; opening them leaves the five triangles in one distinct-cut chain.
Alternatively, split at internal cycle marks to realize
`TP+TTT+TP`.  Its role is to refute leaf counting, not the two-opening method.

### 4.3 A dispersing `Q` hub

In `TTTTTTQ`, let `Q` meet three disjoint two-triangle arms at three distinct
vertices:

`(T1-T2) - Q - (T3-T4)` with a third arm `(T5-T6)`.                 (A4)

Formally, each arm is a distinct-cut chain `Q-xi-T2i-1-yi-T2i`.  The incidence
graph is a tree.  If `q>=4`, `Q` has a private vertex, and a leaf triangle also
has private vertices.  Nevertheless the simple prescribed sacrifice
`Q + one T` does not leave five triangles in one shared-cut component: deleting
`Q` creates three nonempty triangular branches, and deleting one triangle
cannot erase two of them.  The path remnant `Q-v` keeps the whole induced
remainder connected, which exposes exactly the difference between connectivity
and retained-cycle concentration.

The natural packet is obtained by splitting `Q` into three proper consecutive
intervals, one per arm:

`TT + TT + TT`.                                                    (A4-packet)

This uses the fixed margins of three bicyclic all-triangle packets and avoids
charging two tree openings.  If external connector entries are present, one
needs a rooted interval version assigning each entry to exactly one interval.

When `Q=T=C3`, the same three-arm incidence saturates the hub triangle: all
three vertices are cuts.  It then exhibits both dispersion and absence of a
private vertex on the designated hub.

### 4.4 Saturated pentagon hub with a multiway triangular branch

In `TTTTTPP`, take `P0` incident at all five of its vertices.  Attach triangular
petals `T1,T2,T3,T4` at four marks and a pentagonal petal `P1` at the fifth.
Attach the remaining triangle `T5` at the `P0-T1` mark, making that cut
degree three.  The incidence edge set is

`P0-xi` for `1<=i<=5`, `Ti-xi` for `1<=i<=4`, `P1-x5`, and `T5-x1`. (A5)

It has twelve nodes and eleven edges and is therefore a valid incidence tree.
The hub pentagon has no private vertex.  Thus the simple instruction "open
both pentagons and retain five triangles" is impossible, although the petal
pentagon is private.  The same core also defeats retained triangle-leaf
separation because every petal uses a cut needed by the rest.

The required repair is a cyclic interval packet on the saturated hub, not a
private opening.  Merge the `P1` mark with a neighboring triangular mark and
give the other hub marks proper intervals.  If the merged neighbor is chosen
away from the degree-three mark, the visible packet pattern is

`TP + TT + T + T`,                                                 (A5-packet)

where the `TT` packet is the `T1,T5` multiway branch.  The quantitative total
is already positive from `sigma(TP)>1-delta`, `sigma(TT)>1`, and strict
singleton triangles.  A formal lemma must audit cyclic order and ownership at
the degree-three cut; merely listing the packet multiset is not enough.

This is minimal for saturation of a pentagonal hub: five distinct incident cut
vertices are necessary and sufficient.  A degree-three cut permits the seventh
cycle to be added without creating a sixth mark on the hub.

### 4.5 Saturated triangle router

A triangle can use all three vertices as cuts and route three nonempty branches.
If the two cycles proposed for sacrifice include this triangle, no private
opening exists.  If another triangle is substituted, the three branches can
remain dispersed exactly as in (A4).  This small router shows why a statement
quantified over a *designated* sacrificial pair is too weak: a useful lemma must
either find a pair satisfying both privacy and concentration, or return an
interval packet around the saturated router.

## 5. Minimal obstruction catalogue

Minimality here is only with respect to the displayed structural resource, not
graph order.

| core | residual family | naive triangle + hexacyclic | simple two-opening sacrifice | missing packet or operation |
|---|---|---|---|---|
| seven-cycle bouquet | both | locked common cut | works when selected cycles are private | common-cut sacrifice |
| `P-T-T-T-T-T-P` reduced path | `TTTTTPP` | no triangular reduced leaf | not a fully shared opening problem | `TP+TTT+TP` |
| `TTTTTT|Q` leaf cluster | `TTTTTTQ` | leaf has rank six | depends on internal incidence | entry-sensitive cluster release |
| alternating incidence path (A3) | `TTTTTPP` | no triangular incidence leaf | works by opening endpoint pentagons | `TP+TTT+TP` or endpoint opening |
| three-arm `Q` hub (A4) | `TTTTTTQ` | shared-cut locking | five triangles disperse | `TT+TT+TT` interval split |
| saturated pentagon hub (A5) | `TTTTTPP` | shared-cut locking | hub has no private vertex | `TP+TT+T+T` hub split |
| two hostile reduced leaves | `TTTTTPP` | leaves are pentagons | qualitative positivity cannot pay deficits | two quantitative pentagon partners |

The catalogue separates examples which defeat only the leaf method from those
which also defeat the simplest sacrifice.  In particular, neither bouquets nor
alternating paths should be advertised as universal hard cases: each has an
elementary repair, but the repairs are different.  The genuinely new sacrifice
obstructions are saturation and dispersion.

## 6. Packet inventory suggested by the audit

A heptacyclic proof organized around the hexacyclic theorem would need at least
the following explicit tools.

1. **Strict leaf packet:** `T + H6`, but only for an actual bridge-separated
   singleton triangle with a connected induced hexacyclic remainder.
2. **Pentagon-ended path packet:** `TP+TTT+TP` and refinements, with arbitrary
   bridge connectors and entries.
3. **Two-opening concentrated packet:** five shared triangles with margin
   `>2`, plus two disjoint admissible private openings.  Privacy, inducedness,
   and retained-triangle concentration must all be hypotheses.
4. **Dispersed-hub packet:** proper cyclic intervals producing
   `TT+TT+TT`, or the corresponding rooted branch variants.
5. **Saturated-pentagon packet:** a cyclic-order lemma producing
   `TP+TT+T+T` (and variants when the multiway branch has a different size).
6. **Entry-sensitive cluster release:** a finite list for rank-six leaf
   clusters such as `TTTTTT|Q` and `TTTTTP|P`; abstract cluster partitions are
   insufficient.
7. **Multiple-hostile budget:** every negative singleton pentagon must be
   paired with a stated quantitative packet.  Neither strict triangular
   surplus nor the qualitative hexacyclic theorem has a uniform margin that
   may be spent without proof.

An exact colored incidence census would still be needed to show that these
packets cover every fully shared residual.  Its acceptance test should record,
for each proposed split, private-vertex availability, cyclic interval
realizability, retained shared-cut components, strict versus non-strict packet
bounds, and ownership of every external entry.  Counting only branch cycle
multisets would miss (A4) and (A5).

## Status

This note gives explicit heptacyclic residual cores which obstruct naive
triangle-leaf induction, and two cores which additionally obstruct the simplest
two-cycle sacrifice through dispersion or saturation.  It proposes a minimal
working packet catalogue but does not claim completeness, does not perform the
seven-cycle incidence census, and makes no theorem claim for connected
heptacyclic cacti.
