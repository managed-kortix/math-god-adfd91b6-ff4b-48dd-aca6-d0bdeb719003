# Physical `C5` interval-router lemma

**Date:** 2026-07-29

## Statement

Let a cactus contain a distinguished pentagon

```text
R=v0v1v2v3v4v0
```

and suppose deleting the cyclic block `R` from the block-cut incidence tree
leaves `d` nonempty cyclic components, where `2<=d<=5`. Bind their distinct
ports to distinct vertices of `R` in cyclic order. Then `V(R)` has an exact
partition into `d` nonempty proper consecutive intervals, one per component,
such that the interval containing a port is assigned to that component. The
only possible size multisets at the saturated arities are

```text
d=4: 1+1+1+2,
d=5: 1+1+1+1+1.
```

Give every component its interval, every incidence branch in that component,
and every arbitrary private connector remnant or off-hull forest rooted at a
vertex in that territory. The resulting territories are connected, induced,
pairwise disjoint, exhaustive cacti. Their complete cyclic blocks are exactly
the complete blocks in the corresponding incidence component; all other added
objects are forest attachments at one owned anchor. Therefore every theorem
proved uniformly for arbitrary trees attached to that complete cactus profile
applies to the territory.

## Proof

List the occupied ports as `p0,...,p(d-1)` in cyclic order. Cut the pentagon
edge immediately before each port. The resulting arcs are nonempty consecutive
intervals, are pairwise disjoint, and exhaust all five vertices. Assign the arc
starting at `pi` to the incidence component at `pi`. This proves existence and
the exact owner binding. Conversely, any partition into `d` nonempty intervals
has positive integer sizes summing to five. For `d=5` every size is one. For
`d=4`, three sizes are one and the remaining size is two. Thus the displayed
saturated profiles are forced.

The block-cut incidence graph is a tree. After deleting `R`, distinct ports lie
in distinct components, so no retained cyclic block or shared cut can belong to
two territories. Adding one consecutive interval reconnects each component to
its port. An edge of `R` whose endpoints receive different owners is a boundary
edge; every edge whose endpoints have one owner lies in that owner's induced
territory. Hence each territory is connected and induced, and the territories
partition the physical vertices.

A private remnant has one specified anchor in its interval territory. More
generally, each off-hull component is a tree with one hull root: two roots or a
cycle would create another cyclic block or a cycle in the block-cut reduction.
Assigning the whole rooted tree to its anchor owner preserves connectivity and
inducedness and creates no complete cycle. The owner-induced cyclomatic number
therefore equals the number of complete retained cyclic blocks. Each territory
is a cactus with exactly the claimed complete profile plus arbitrary forest
attachments, which is precisely the scope of the tree-uniform packet theorems.
QED.

## Grouped-component corollary

One occupied port may instead receive a singleton interval while the
complementary four-vertex path receives several of the other incidence
components under one owner. This two-owner coarsening is valid whenever those
components together with the path form a connected owner-induced physical
territory and its cyclomatic number equals the number of complete cycles derived
after ownership. These are post-ownership physical predicates; a disconnected
incidence carrier receives no exception. The same inducedness and exhaustion
argument applies: the singleton and complementary path partition `C5`, every
branch follows its actual port, and grouping branches cannot duplicate a cut or
vertex. This is the form used by the U4 and U8 rank-eleven repairs; it is not the
one-owner-per-component construction above.

## Executable gate

`geometry_router_owner_core.py` exposes
`verify_c5_router_owner_split`, explicitly allowing owner counts `2,3,4,5` and
enforcing the forced `d=4` and `d=5` sizes. The older generic entry points still
default to owner counts `(2,3)`; callers must opt into broader arity, so this
extension does not weaken existing checks.
