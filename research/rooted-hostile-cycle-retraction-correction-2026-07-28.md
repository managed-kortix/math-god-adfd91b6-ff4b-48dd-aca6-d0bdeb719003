# Correction: the rooted hostile-cycle Voronoi theorem is valid

**Date:** 2026-07-28

## Verdict

The retraction formerly printed at the top of
`research/rooted-hostile-cycle-guard-absorption-2026-07-26.md` was wrong.  Two
independent hostile audits reproduced the proof and approved the restored
theorem.

Let `A` be a connected cactus whose cyclic blocks are at least one triangle,
rooted at an arbitrary vertex `r`.  Let `Q=C_q`, where `q=1 mod 4` and `q>=5`,
and put

```text
delta_q=sec(pi/q)-1.
```

Join `Q` to `A` through exactly one interface: identify a vertex of `Q` with
`r`, or join them by one internally disjoint positive-length path.  Arbitrary
finite trees may be attached anywhere, including on the connector.  Then

```text
sigma(G)=s+(G)-|V(G)| > 1-delta_q > 0.                 (1)
```

No shared-cut-cluster assumption is required.  The unique-interface condition
means that the `Q`/connector subgraph meets `A` only at `r`.

## 1. Exact error in the retraction

Choose a maximum-cardinality family of pairwise vertex-disjoint triangles

```text
C_0,...,C_(k-1)
```

in `A`, choosing `C_0` nearest the root and giving it first priority.  Assign
each vertex to its lexicographically nearest selected triangle, and let `A_i`
be the induced territories.

Suppose `A_i` contained two vertex-disjoint cycles `D,E`.  Every other selected
cycle `C_j`, `j!=i`, lies in a disjoint territory.  Therefore

```text
D,E,{C_j : j!=i}
```

is a packing of size `k+1`.  This contradicts maximal cardinality.  There is no
need for `D,E` to be disjoint from `C_i`, because `C_i` is replaced rather than
retained.

The former retraction overlooked this replacement and incorrectly attempted to
use `D,E` together with `C_i`.  The territory packing-one proof in
`research/arbitrary-r-shared-triangle-uniform-surplus-2026-07-26.md` was
correct all along.

## 2. Restored proof

The standard predecessor-on-a-shortest-path argument shows that the `A_i` are
connected induced subgraphs partitioning `A`, each containing `C_i`.  The
replacement argument above proves that every `A_i` has cycle-packing number
one.  Since induced subgraphs of a cactus contain only original block cycles,
all cycles retained in every `A_i` are triangles.  Split triangles contribute
only forest fragments and create no new cycles.

Root priority gives `r in A_0`.  Form `H_0` from `A_0`, all of `Q`, the complete
connector, and all trees attached there.  Assign every remaining off-hull tree
wholly to the territory owning its unique attachment.  These are connected
induced territories, disjoint and exhaustive.

The triangular blocks retained in `H_0` have packing number one and include
`C_0`.  The proved rooted packing-one hostile-cycle lemma gives

```text
sigma(H_0)>a_0-delta_q>=1-delta_q,                    (2)
```

where `a_0>=1` is the number of retained triangles in `H_0`.  For every other
territory `H_i`, all retained cycles are triangles, their packing number is
one, and at least `C_i` is retained.  The favorable Sachs phase theorem gives

```text
s+(H_i)>s-(H_i),
sigma(H_i)>b_i-1>=0,                                  (3)
```

where `b_i>=1` is its cyclomatic number.

Positive square energy is superadditive over induced vertex partitions.
Summing (2)--(3) proves (1).  Strictness does not come from adding unspecified
small triangular margins: it is already present in the coupled rooted packet
bound (2).

## 3. Scope boundary

The restored theorem proves the all-rank `T^rQ` case only when `Q` has exactly
one interface with the triangular cactus.  It does not prove:

* a multi-interface distinguished cycle theorem;
* a two-hostile-cycle theorem;
* the arbitrary `T^rPP` family;
* the global separator-reachability lemma.

Maximum-packing Voronoi applied to the entire `T^rPP` graph can isolate both
pentagons and split every triangular guard.  The minimal example is
`P-x-T-y-P`, `x!=y`: the maximum packing is the two pentagons, and the triangle
is retained nowhere.  Thus the restored one-root theorem does not bypass the
two-demand ownership obstruction.

## 4. Audit gates

Two independent auditors checked maximum versus merely maximal packing,
replacement of `C_i`, root priority, connectedness, inducedness, arbitrary
trees, connector ownership, retained versus split triangles, applicability of
the rooted packing-one lemma, and strict margins.  Both approved the theorem
under the unique-interface scope above.
