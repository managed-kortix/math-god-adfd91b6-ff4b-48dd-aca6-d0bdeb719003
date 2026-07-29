# Private clustered-pentagon router lemma

**Date:** 2026-07-29

## Statement

Let the cyclic hull have nine triangles, an incidence-leaf pentagon `P0` rooted
at cut `x`, and a remote pentagon `P1` whose connector enters a private vertex
of `P0`. If the incidence tree has another cut, let `R` be the first triangle on
the path from `x` to the least other cut. Removing `R` gives the `x`-branch and
a nonempty complementary triangular branch. Split the physical vertices of `R`
as

```text
{x}                         -> two-P child,
V(R)-{x}                    -> strict triangular child.
```

The two-P child owns complete `P0`, complete `P1`, the connector chain and
remnant, and every triangle in the `x`-component. Its cyclic rank is at most
nine. The complementary child is a nonempty connected triangular cactus.

## Bounds

If the two-P child has rank two or three, the connected rank-2/3 theorem gives
nonnegative surplus. If its rank is four through nine, the connected rank-4..9
theorem gives strict positive surplus. In both cases the nonempty pure
triangular sibling has strict positive surplus, so the total bound is strict.

If there is only one incidence cut, the row is a bouquet. For private distance
one open `P0.v3`; for private distance two open `P0.v4`. The opened vertex and
its rooted attachment form the exact nonempty-tree charge `-1`. The retained
territory contains the other four `P0` vertices as a path, all nine common-cut
triangles, complete `P1`, and its connector. The packing-one theorem gives
`9-delta`, hence the exact total is

```text
(9-delta)-1 = 8-delta > 0.
```

## Certificate obligations

The executable independently derives the router, incidence components,
concrete `(1,2)` intervals, every physical vertex owner, every attachment owner,
complete C5 and connector domains, terminal connectivity, theorem records, and
exact `Bound`. A submitted owner map is accepted only if it equals this derived
map at every physical vertex.
