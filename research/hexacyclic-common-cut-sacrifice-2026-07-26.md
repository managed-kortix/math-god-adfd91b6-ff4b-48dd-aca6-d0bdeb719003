# A common-cut sacrifice lemma for the hexacyclic residuals

## Scope and notation

This note isolates one local argument that applies without change to the
hexacyclic residual families

`TTTTTQ={T1,T2,T3,T4,T5,Q}` and `TTTTPP={T1,T2,T3,T4,P1,P2}`,

where `T=C3`, `P=C5`, and `Q=Cq`, `q>=3`. It proves the bouquet cases and a
larger class of multiway-cut incidences. It is not a classification of every
fully shared six-cycle incidence.

Write

`sigma(X)=s+(X)-|V(X)|`.

We use induced-subgraph superadditivity and the established quantitative fact

`sigma(H)>3`                                                       (FT)

whenever `H` is a connected cactus whose four cyclic blocks are triangles in
one shared-cut cluster, with arbitrary bridge trees and arbitrary trees
attached at arbitrary vertices. The packing-three central-triangle incidence
is included in (FT).

A *cyclic cut* is a vertex belonging to at least two cyclic blocks. A vertex
of a cyclic block is *private* if it is not a cyclic cut. It may still carry
arbitrary bridge-tree branches. An opening below is *admissible* if those
branches contain no further cyclic block; this is automatic in a fully shared
six-cycle core with only trees attached. For a cyclic block `C`, let

`m(C)=|{x in V(C): x is a cyclic cut}|`.

Thus `C` has a private vertex exactly when `m(C)<|C|`.

## 1. The common-cut obstruction

**Lemma 1 (retained-component principle).** Let `V(G)=V1 disjoint union ...
disjoint union Vr` be any vertex partition and put `Gi=G[Vi]`. Form the graph
on the cyclic blocks retained by the `Gi`, joining two retained blocks when
they share a cyclic cut. Every connected component of this retained-block
graph is contained in one `Gi`.

**Proof.** If retained blocks `B` and `B'` share `x`, then every territory
retaining either block contains all of its vertices and hence contains `x`.
Only one part of a vertex partition owns `x`, so both blocks are retained by
the same part. Propagate this conclusion along a path of retained blocks. QED.

In particular, if several cycles share one common cut `x`, all of those which
are retained must lie in one induced territory. This is an obstruction to
separating retained packets, but it is exactly what makes a sacrifice useful:
after two cycles are opened, four triangles can remain concentrated in one
packet rather than being dispersed among packets of inadequate total margin.

## 2. Exact opening at private vertices

For a private vertex `v` of a cyclic block `C`, delete the two cycle edges
incident with `v` and let `R(C,v)` be the component containing `v`. An
admissible opening means that `R(C,v)` is a tree and meets `C` only at `v`.

**Lemma 2 (private-vertex opening).** Let `C1,...,Ck` be distinct cyclic
blocks, and choose an admissible private vertex `vi` on each `Ci`, with the
rooted sets `R(Ci,vi)` pairwise disjoint. Put `Fi=G[R(Ci,vi)]` and
`H=G-[union_i R(Ci,vi)]`. Then:

1. the sets `V(H),V(F1),...,V(Fk)` are an exact vertex partition;
2. every part induces the graph named by it, and every `Fi` is a nonempty
   tree, so `sigma(Fi)=-1`;
3. every block other than the `Ci` is retained in `H`, while `Ci-vi` is a
   path in `H` and hence `Ci` is not retained;
4. every component attached at `vi` is assigned wholly to `Fi`, and every
   component attached at another cycle vertex is assigned wholly to `H`.

If the retained cyclic blocks are connected after each `Ci` node is replaced
by the path `Ci-vi`, then `H` is connected.

**Proof.** In a cactus, a component outside the cyclic hull has a unique hull
attachment; two attachments would create another cycle. Admissibility says
that the component rooted at `vi` is a tree, and pairwise disjointness is an
explicit hypothesis. Therefore no `Fi` meets `H`. Every vertex is assigned by
the displayed definition, proving the exact partition and inducedness.

Removing one vertex from `Ci` leaves the proper path `Ci-vi`. Because `vi` is
private, every cyclic cut formerly on `Ci` remains on this path. Thus replacing
`Ci` by `Ci-vi` preserves precisely the connections represented by the
remaining incidence structure. The final connectedness assertion follows. A
nonempty tree has `s+=|V|-1`, so `sigma(Fi)=-1`. QED.

The statement deliberately charges one full unit for each `Fi`, independent
of its order and shape. This is why arbitrary attached trees, coincident roots
away from the selected vertices, and long hanging branches cause no change in
the margin.

## 3. Shared common-cut/four-triangle sacrifice

**Theorem 3 (four-triangle sacrifice).** Let `G` be a connected cactus and
choose four triangular blocks `T1,...,T4` and distinct sacrificial cyclic
blocks `C1,...,Ck`, where `1<=k<=3`. Assume:

1. each `Ci` has an admissible private vertex `vi`, and their rooted sets are
   pairwise disjoint;
2. after opening all `Ci` at `vi` as in Lemma 2, the induced remainder `H` is
   connected;
3. the only cyclic blocks retained by `H` are `T1,...,T4`;
4. those four triangles form one connected component of their shared-cut
   graph.

Then the exact induced partition

`V(G)=V(H) disjoint union V(F1) disjoint union ... disjoint union V(Fk)`

satisfies

`sigma(G) >= sigma(H)+sum_i sigma(Fi) > 3-k`.

In particular, `sigma(G)>1` for two sacrifices and `sigma(G)>0` for up to
three sacrifices.

**Proof.** Lemma 2 gives the exact connected induced territories and
`sigma(Fi)=-1`. Hypotheses 3 and 4 place `H` under (FT), including arbitrary
trees inherited from `G`, so `sigma(H)>3`. Induced-subgraph superadditivity
gives

`sigma(G) >= sigma(H)-k > 3-k`.

The inequality is strict even when `k=3`; no unquantified triangular
strictness is being spent. QED.

The connectedness hypothesis has a convenient incidence formulation. Let `I`
be the bipartite cycle-cut incidence tree of the shared cluster. Replace every
sacrificial cycle node `Ci` by the path `Ci-vi`, retaining all of its incident
cut nodes. If the resulting realization connects the four triangles, then
hypothesis 2 holds. In a fully shared core this is automatic for private `vi`:
the path `Ci-vi` still contains every cut incident with `Ci`, so replacing the
cycle node does not break any route in `I`. A leaf sacrificial cycle is the
simplest special case.

## 4. The two residual families

**Corollary 4 (`TTTTTQ`).** Suppose the six cyclic blocks are five triangles
and `Q`. Designate one triangle `T5` and `Q` for sacrifice. If both have private
vertices, their openings are admissible, and opening them leaves `T1,...,T4`
in one connected shared-cut cluster, then

`sigma(G)>1`.

This includes `Q=T`: the designation is arbitrary among six triangles. It also
includes every six-cycle bouquet. In the bouquet all cycles share one cut `x`;
choose `vQ != x` and `v5 != x`. Both opened cycles leave paths containing `x`,
and the four retained triangles still share `x`. Thus the exact territories
are one four-triangle bouquet territory and two rooted tree territories.

**Corollary 5 (`TTTTPP`).** Suppose the six cyclic blocks are four triangles
and two pentagons. If each pentagon has an admissible private vertex and opening
both leaves the four triangles in one connected shared-cut cluster, then

`sigma(G)>1`.

This includes the six-cycle bouquet and every incidence in which both
pentagons are leaf cycle nodes and the four triangles remain connected after
the pentagon nodes are suppressed to paths. The conclusion has margin `>1`,
not merely `>0`: the packet contributes `>3` and the two trees cost exactly
two.

These corollaries are the same theorem. The labels `Q`, `P`, and `T` matter
only when selecting two cycles whose removal leaves exactly four triangles.

## 5. Incidence excess and private vertices

Suppose six cyclic blocks form one shared-cut cluster, with incidence tree `I`.
If `X` is its set of cut nodes, then

`sum_{x in X}(deg_I(x)-1)=5`.                                    (1)

For a cycle `C`, write `X(C)` for its incident cut nodes. Each member of
`X(C)` occupies a distinct vertex of `C`, even when its degree is greater than
two. Therefore

`m(C)=|X(C)|` and `C has a private vertex iff |X(C)|<|C|`.         (2)

Formula (1) can certify (2) more sharply when some incidences are multiway.
Define the excess already visible on `C` by

`a(C)=sum_{x in X(C)}(deg_I(x)-1)`.

Every summand is at least one, hence

`m(C)<=a(C)<=5`.                                                  (3)

Let `W` be any witness collection of incidences not on `C`, counted by their
contribution to (1), together with any *extra* degree at cuts on `C`. If these
witnesses certify `e` units disjoint from the baseline one unit for each
member of `X(C)`, then

`m(C)+e<=5`.                                                      (4)

Consequently:

- a sacrificial triangle is guaranteed private when `e>=3`, since then
  `m(C)<=2<3`;
- a sacrificial pentagon is guaranteed private when `e>=1`, since then
  `m(C)<=4<5`;
- a cycle `Q=Cq` is guaranteed private when `e>5-q`; in particular this is
  automatic for `q>=6`, requires `e>=1` for a pentagonal `Q`, `e>=2` for a
  quadrilateral `Q`, and `e>=3` for a triangular `Q`.

Typical valid witnesses are:

1. a cyclic cut `y` off `C`, contributing `deg_I(y)-1` units;
2. at a cut `x` on `C` of degree `d>=3`, the `d-2` units beyond the baseline
   unit used merely to record that `x` is a mark on `C`;
3. an intersecting pair of other cycles: their common cut contributes one
   witness unit if off `C`, and contributes one extra unit if it lies on `C`.

This recovers the useful pentacyclic-style rule in the six-cycle setting:
three independently certified excess units away from a designated triangle
force a private triangle vertex; one such unit forces a private pentagon
vertex. Multiway incidences help because a degree-`d` cut consumes `d-1` of
the fixed excess budget while occupying only one vertex on each incident
cycle.

### Simultaneous openings

For two sacrificial cycles `C,D`, separate inequalities are required. A single
witness unit may prove `m(C)<|C|` and `m(D)<|D|` simultaneously if it is
legitimately outside both baselines, but it must not be counted twice inside
one inequality. The clean exact test is simply

`m(C)<|C|` and `m(D)<|D|`,                                      (5)

read directly from `I`. Excess arguments are sufficient certificates for
(5), not substitutes for checking the two mark counts when the incidence tree
is known.

In `TTTTPP`, each pentagon automatically has a private vertex unless it is
incident with all five cut nodes of the maximum-cut case `|X|=5`. Equivalently,
a nonprivate pentagon forces all cut nodes to have degree two and the entire
excess budget to be the five baseline units on that pentagon. Thus any
multiway cut anywhere, or any cut node off that pentagon, forces it private.
This observation must be applied to both pentagons.

## 6. What opening must preserve

Private vertices alone do not imply Theorem 3. After opening the selected
cycles, two independent facts must be checked:

1. **Concentration:** all four retained triangles lie in one shared-cut
   component, so (FT) applies to one packet.
2. **Connectivity:** the path remnants of the opened cycles and any bridge
   connectors assigned to `H` actually join that packet into one induced
   territory.

For a leaf sacrificial cycle both checks reduce to the retained triangle
incidence. For an internal hub, deleting a genuinely private vertex leaves all
incident cuts on one path, so their cyclic order is irrelevant for ordinary
connectedness. Deleting a marked vertex instead can break several incidence
routes; this is precisely why private means *non-cut*, not merely "not the
common cut currently under discussion."

The common-cut case is strongest: if the four triangles share `x`, then
concentration is immediate, and any opened cycle incident with `x` leaves `x`
on its path. Hence bouquets and hybrids with one triangle-common cut satisfy
the topological part of the criterion as soon as admissible private opening
vertices exist.

## 7. Limits and counterexamples to broader statements

### 7.1 "A leaf cycle can be separated while the others are retained" is false

Take six cycles with one common cut `x`. Every cycle node is a leaf of the
incidence tree, but no retained leaf cycle can be put in a territory separate
from any other retained cycle: both territories would need `x`. Opening a
private vertex of the leaf is legal, but it destroys that cycle and creates a
tree cost. Incidence-leaf status is not induced separability.

### 7.2 "Every cycle in a six-cycle shared cluster has a private vertex" is false

Let a triangle `C` meet three branches at its three distinct vertices. The
three cut degrees can be `(3,2,2)`, contributing excess `2+1+1=4`; place the
remaining excess unit at a cut inside one branch. This is a realizable
bipartite incidence tree with total excess five, and `m(C)=3`. Thus `C` has no
private vertex. A bouquet behaves oppositely: its one degree-six cut consumes
all five excess units but only one vertex of every cycle.

Likewise a pentagon can be saturated at five distinct degree-two cuts, as in a
pentagon hub with five petals. Such a pentagon cannot be opened by Lemma 2 and
must instead be split into consecutive intervals.

### 7.3 "Two private openings always leave a connected four-triangle packet" is false

Use the fully shared incidence path

`T1-x1-P1-x2-T2-x3-T3-x4-P2-x5-T4`.

Both pentagons have private vertices. Opening them leaves a connected induced
remainder because each pentagon path still joins its two cuts. Nevertheless,
the retained triangle shared-cut graph has components `{T1}`, `{T2,T3}`, and
`{T4}`: connectivity through a pentagon path is not a shared cut between the
triangles. Thus (FT) is unavailable. An even simpler non-fully-shared example
bridge-separates two intersecting `TT` clusters and attaches one private
pentagon as a leaf to each cluster. Opening both leaves `TT|TT`, not one shared
`TTTT` cluster. Private vertices certify legal openings and ordinary
connectivity, not concentration.

### 7.4 "Connected four-triangle remainder implies surplus `>3`" is not an
available theorem

The established bound (FT) is for one connected *shared-cut cluster*, not for
an arbitrary connected tetracyclic cactus whose triangle blocks may be joined
by bridges. Qualitative tetracyclic positivity gives only `sigma>0`, and cannot
pay two tree costs. A proof may use a stronger packet decomposition in a
particular bridge-separated incidence, but it may not cite (FT) solely from
ordinary graph connectedness.

### 7.5 "A strict packet pays a tree cost" is false

An arbitrary tree attachment can drive the surplus of a triangular unicyclic
packet arbitrarily close to zero. Therefore `sigma(T)>0`, or generic
pentacyclic positivity, cannot pay even a fixed fractional deficit, much less a
tree cost of one. The sacrifice theorem works because the uniform strict
margin is `>3` and every opened tree costs exactly one.

### 7.6 "Delete a shared cut and allocate it to both sides" is never legal

The territories form a vertex partition. A common cut belongs to exactly one
part. Splitting a cycle at a shared cut without assigning ownership can produce
formally attractive packet symbols which are not simultaneously induced.
Lemma 2 avoids the issue by deleting only private vertices; a consecutive-
interval split must instead state explicitly which interval owns every marked
vertex.

## 8. Reusable criterion for a census

For each fully shared colored incidence tree in `TTTTTQ` or `TTTTPP`, the
following test is sufficient and hand-checkable.

1. Select two sacrificial cycles so that the other four cycles are triangles.
2. Count the distinct cut marks on each selected cycle, using (2), or certify
   the strict inequalities with the excess budget (4).
3. Choose one private vertex on each selected cycle and retain all cyclic cuts
   on the resulting path remnants.
4. Check in the incidence tree that the four retained triangles form one
   shared-cut component; do not replace this by ordinary connectivity.
5. Assign each selected vertex and every tree branch rooted there to its own
   tree territory; assign every other hanging tree wholly to the remainder.
6. Invoke Theorem 3 with `k=2` to obtain the strict reusable margin

   `sigma(G)>1`.

Failure at step 2 signals a saturated hub and calls for a consecutive-interval
split. Failure at step 4 signals a dispersed four-triangle remainder and calls
for a split-packet ledger such as `TT|TT`, `TTT|T`, or an entry-sensitive hub
argument. Neither failure contradicts the desired hexacyclic theorem; it only
marks the exact boundary of the common-cut sacrifice lemma.

## Conclusion

The reusable mechanism is not "leaf deletion." It is an exact induced vertex
partition obtained by opening private vertices, together with a concentrated
four-triangle packet carrying the uniform margin `>3`. The fixed incidence
excess five supplies effective private-vertex criteria, and multiway cuts are
favorable for this purpose because they consume excess faster than cycle
vertices. Under the stated concentration and connectivity hypotheses, both
`TTTTTQ` and `TTTTPP` obtain the same strict bound `sigma(G)>1` after two
sacrifices, with arbitrary attached trees. Saturated hubs and dispersed
triangle remainders are genuine limitations and require interval splitting or
separate packet accounting.
