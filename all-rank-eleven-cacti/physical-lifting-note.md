# Abstract-to-physical lifting for `P|A_9|P`

## Scope

This note supplies the graph-theoretic lifting step between the abstract
two-mark `A_9` owner certificates and an original cactus in the disconnected
endpoint `P_0|A_9|P_1`. It does not enlarge the analytic packet whitelist or
claim that `research/rank-eleven-a9-two-interface-verifier.py` independently
materializes arbitrary bridge connectors.

The central cluster is a cycle-cut incidence tree of nine triangles. Each
triangle has three concrete cyclic positions. A position used by an incidence
edge is the corresponding canonical shared-cut vertex; unused positions are
private. Two complete external pentagons attach to ordered marked hull
positions through the bridge/tree chains represented by the two reduced-tree
edges. The chains may have arbitrary positive lengths and may carry arbitrary
rooted trees.

## Lifting lemma

Assume an abstract certificate:

1. gives every retained triangle, ordered mark, and complete pentagon demand
   exactly one final owner;
2. realizes every sacrificed triangle as nonempty proper consecutive intervals
   of its three concrete positions;
3. permits nested routing only by refining the active interval; and
4. passes the complete final-position gate: every shared cut and every private
   position of every sacrificed router resolves from the root to exactly one
   terminal owner; every interval position agrees through its child; and the
   exact independently derived owner domain has no duplicate keys.

Then it lifts to a partition of the original cactus into connected induced
territories with the same complete-cycle profiles and cyclomatic ranks.

## Proof

Give every retained triangle wholly to its cycle owner. On a sacrificed
triangle, assign the three actual vertices according to its certified cyclic
intervals. At a shared cut, the retained branches and router intervals meeting
that one physical vertex have its verifier-derived owner. This includes cuts
incident only with sacrificed routers. Multiple child matches are rejected;
every interval position has equal root and child terminal owners; and every
nonroot active set is exactly one parent's child, preventing sibling retrieval.
Since the incidence graph is a tree and nested routing refines only an active child, induction over
the router refinement tree proves that the central owner domains are disjoint,
exhaustive, and connected along their retained incidence branches and interval
edges.

For each ordered external mark, assign to its mark owner the complete external
pentagon, every internal vertex and edge of the connector chain, the connector
remnant, and every tree rooted on that chain. The hull endpoint is not copied:
it is the central anchor already present in that owner's domain. If the marks
coincide, they name one physical anchor. Anchor-owner consistency therefore
puts both external connector branches with the same owner; their interiors and
pentagons remain distinct branches in the cactus block-cut tree. Thus there is
neither vertex duplication nor a competing owner at the common anchor. For
distinct marks, each chain follows its own mark owner.

Assign every other off-hull tree component to the owner of its unique anchor.
It has only one anchor: two would form an additional cycle together with the
path in the cyclic hull. These rules assign every vertex once. Taking the
subgraph induced by each owner domain gives an induced partition; cross-owner
edges are simply absent from the induced pieces. Every piece is connected by
the central incidence-tree argument, whole connector chains, and unique-anchor
trees.

Every retained cyclic block is complete in one owner. Every sacrificed router
is split between at least two proper intervals and remains incomplete in each
owner. Connector chains, remnants, and off-hull trees contain only bridge
blocks and cannot create cycles or complete a split router. Since every cycle
of a cactus is one of its cyclic blocks, an owner territory's cycles are
exactly the complete cycles in its abstract terminal profile. Its cyclomatic
rank is therefore unchanged. The argument is independent of connector length
and tree size.

## Executable integrity boundaries

- `research/rank-eleven-a9-two-interface-verifier.py` checks the 355 central
  incidence trees, 128155 ordered labelled placements, 43151 canonical rows,
  concrete `C3` intervals through `research/geometry_router_owner_core.py`,
  recursive cuts/marks/final owners, exhaustive shared-cut and private-router
  position maps, unique child resolution, and post-ownership theorem records. Its
  ordinary demands are abstract complete pentagons, not fully materialized
  arbitrary connector graphs.
- `research/rank-eleven-t9p-p-endpoint-frontier-verifier.py` independently
  corroborates all 43145 ordinary plans through its exact projection to ordered
  `A_9` marks and rebound concrete intervals. It then checks complete physical
  pentagons, the remote connector and remnant, attachment domains, connected
  owner-induced graphs, complete cycles, ranks, and theorem records.
- Exchanging the ordered labels `P_0,P_1` exchanges the two external
  realization orientations. The ordered marked stream includes the exchanged
  placement. This does not mean the `T^9P|P` executable enumerates two arbitrary
  nonzero external connector lengths; length-uniformity follows from the
  bridge/tree lifting proof above.

Exact supporting files:

```text
research/rank-eleven-a9-two-interface-verifier.py
research/rank-eleven-a9-two-interface-fail-closed-note-2026-07-28.md
research/geometry_router_owner_core.py
research/rank-eleven-t9p-p-endpoint-frontier-verifier.py
research/rank-eleven-t9p-p-endpoint-frontier-note-2026-07-28.md
```
