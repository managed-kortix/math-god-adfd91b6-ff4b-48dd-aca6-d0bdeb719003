# Heptacyclic hull-bridge dispatch: exact blocker and next semantic gate

Date: 2026-11-14.  Status: **OPEN / NONPROMOTIONAL**.

## Scope

The physical `R31-S` packet is closed by its adjacency-only parent gate, but
this does not authenticate the generic actual-hull-bridge sentence formerly
used upstream of the other rank-seven multiblock packets.  A hull bridge gives
two connected induced positive-rank sides, but a rank-one side need not have
nonnegative credit: for example

\[
\sigma(C_5)=s^+(C_5)-5=2-\sqrt 5<0.
\]

Accordingly, the global multiblock master remains intentionally fail-closed.
This note records the exact current blocker and the minimum acceptable next
gate.  It is not a theorem and is not an owner receipt.

## Rejected draft

A prospective hand-written 19-key / 23-row dispatch fixture and companion
script were rejected and deleted before commit.  They checked a duplicated
registry of row, owner, and channel strings; replayed four narrower child
programs; and rejected selected field mutations.  They did **not**:

* construct or enumerate legal physical graphs or reduced block-cut hulls;
* run Tarjan reconstruction or derive actual bridges and articulation cuts;
* derive a channel from adjacency;
* check inducedness, disjointness, exhaustive vertex ownership, or unique cut
  ownership for a physical partition;
* establish completeness over arbitrary legal subdivisions, repeated or
  nested cuts, connector lengths, and rooted payloads; or
* execute the full analytic dependency graph, including the generic
  one-vertex/K2-chain lemma.

Therefore source hashes and literal registry consistency could not support the
proposed words `semantic`, `PASS`, or `COMPLETE`.  In particular, the existing
`synthetic_owner_partition` routine in
`research/rank-seven-nested-induced-piece-verifier.py` manufactures vertex
sets from a supplied channel label; it does not authenticate physical
block-cut topology.

## Exact information-loss witness

The profile `K4+C5+3C3` has legal realizations with very different cyclic
hulls.

* `G_star`: a `K4`, a `C5`, and three triangles all share one cut vertex.  It
  has `14` vertices, `20` edges, and cyclomatic rank `20-14+1=7`.
* `G_chain`: take vertex-disjoint copies of those five cyclic blocks and join
  them in the order `K4--C3--C3--C3--C5` by four bridge edges.  It has `18`
  vertices, `24` edges, and cyclomatic rank `24-18+1=7`.

Both are finite, simple, connected, and have the same cyclic-block profile.
A profile row containing only the strings `K4+Q4-exceptional` and a list of
channel names cannot determine the direct/shared-cut versus bridge/intermediate
routing of these graphs.  This witnesses information loss in the rejected
artifact; it is not a counterexample to the desired square-energy inequality.

## Candidate packet-specific routes

Four profiles require a physical first-boundary dispatch after a hostile
rank-one side is isolated:

1. `R21`: complement `D+T^4`; derive `k=0`, `k=1`, or an actual bridge-free
   `D+TT` anchor from the reduced hull.
2. `R31-K`: complement `K4` plus three cycles, at least two triangles; derive
   `K0`, intermediate-nontriangle, or direct `K4+T` from paths in the hull.
3. `R321`: complement `K4+D+T`; derive whether the triangle is beyond the
   first bridge and whether `D` lies on the `K4--T` path, including the actual
   degree-two/degree-three diamond-entry orbit.
4. `R41`: complement `S4+T+T`; first authenticate the physical `S4` opening,
   compute its owner component, then derive opened-owner, all-bridged,
   intermediate-triangle, or direct retained-packet-plus-triangle routing.

These are **candidate proof plans**, not authenticated channels.

## Minimum acceptable semantic verifier

The next gate must accept adjacency (or a proved equivalent physical block
contract), never a trusted channel or status.  It must:

1. reconstruct biconnected blocks, K2 bridges, articulation equality, block
   types, physical ports, and cyclomatic ranks;
2. reduce to the minimal colored block-cut hull while retaining all marked
   blocks, cut equalities, connector branch points, the diamond entry orbit,
   and the authenticated `S4` opening data;
3. implement bridge components and boundary openings as graph operations that
   return original vertex sets;
4. derive every dispatch branch from topology;
5. verify connectivity and inducedness of every charged territory, pairwise
   disjointness, exhaustive union, unique ownership of each cut/payload, and
   the absence of a positive connector inside every narrow shared-cut anchor;
6. use fixed, independently authenticated packet bounds rather than numeric
   claims supplied by a case record; and
7. prove quotient completeness/invariance under K2-chain length, legal cycle
   length cells, suppressed rooted trees, repeated/nested cuts, and the `S4`
   port cells.

A reduced hull spanning at most six marked cyclic blocks has a finite
combinatorial quotient after suppressing only unmarked nonbranching bridge
chains: a reduced tree has at most `m-2` unmarked branch nodes and hence at
most `2m-2<=10` routing nodes and `2m-3<=9` routing edges.  Finiteness alone
is not a completeness proof; the contraction/expansion invariance lemmas are
part of the obligation.

Required same-label hostile rewires include insertion/removal of a K2 bridge
inside a purported narrow anchor, moving a triangle behind an intermediate
cycle or diamond, moving an `R41` triangle across the physical opening, merging
or splitting cut vertices, swapping the diamond entry orbit, and omitting or
duplicating a connector payload.  Each mutation must change the derived branch
or be rejected.

Until such a replay and its analytic dependencies are independently audited,
the only honest global status is:

```text
bridge-free packet registry: candidate packet proofs available
non-R31-S actual-hull-bridge lane: OPEN / census UNAUTHENTICATED
global multiblock theorem: OPEN
```
