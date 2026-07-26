# The unique fully shared `T^7PP` leaf-pentagon exception

**Date:** 2026-07-26

## Local statement

Write

```text
sigma(G)=s+(G)-|V(G)|,  T=C3,  P=C5,
delta=sec(pi/5)-1=sqrt(5)-2.
```

Consider the following one incidence type, with arbitrary finite trees attached
at arbitrary core vertices:

1. seven triangles `T_1,...,T_7` and a pentagon `P_0` contain one common cut
   vertex `x`;
2. `P_0` contains a second cut vertex `y!=x`; and
3. a leaf pentagon `P_1` meets the rest of the cyclic hull exactly at `y`.

Then

```text
sigma(G)>6-delta=8-sqrt(5)>0.                         (1)
```

This is only a certificate for the displayed fully shared incidence type. No
rank-nine cactus theorem, disconnected-cluster theorem, or two-interface
statement is asserted.

## Certificate: open the leaf pentagon, not the router pentagon

Let `U=V(P_1)-{y}`. For each `u in U`, include with `u` every off-hull tree
branch whose unique hull attachment is `u`, and call the resulting vertex set
`W`. Put

```text
E=G[W],                 H=G[V(G)-W].                  (2)
```

Thus `y`, every branch rooted at `y`, all of `P_0`, and all seven triangles
belong to `H`. The two edges of `P_1` incident with `y` run between the two
territories and belong to neither induced subgraph.

The exact retained cyclic packets are

```text
H: common-cut T^7 P_0 at x,
E: P_1-y, a nonempty tree.                            (3)
```

In particular, this is not the insufficient split `A_7+P_1`. It destroys
`P_1`, retains `P_0`, and preserves the scalar common pivot `x` needed by the
common-cut phase theorem.

## Proof of the certificate

Every component outside the cyclic hull of a cactus has a unique hull
attachment: two attachments, together with the path between them and a path in
the connected hull, would create an additional cyclic block. Consequently the
branch assignment defining `W` is disjoint and exhaustive. The four private
vertices of `P_1` induce a path, and adjoining rooted tree branches to vertices
of a path produces a tree. Hence `E` is a nonempty tree. The graph `H` is
connected and its only cyclic blocks are `T_1,...,T_7,P_0`; all eight contain
`x` and are otherwise disjoint. All vertices outside those blocks that remain
in `H` lie in arbitrary rooted tree branches. Thus `H` satisfies exactly the
hypotheses of the common-cut `T^kQ` Schur--Sachs theorem with `k=7` and
`Q=P_0=C5`.

For a nonempty tree, bipartite spectral symmetry and
`sum lambda_i^2=2|E(E)|` give

```text
s+(E)=|E(E)|=|V(E)|-1,
sigma(E)=-1.                                           (4)
```

The exact common-cut phase theorem, uniform over all attached trees, gives

```text
sigma(H)>k-(sec(pi/5)-1)=7-delta.                      (5)
```

Positive square energy is superadditive over an induced vertex partition.
Since `(H,E)` is the induced partition (2), equations (4) and (5) yield

```text
sigma(G)>=sigma(H)+sigma(E)
        >(7-delta)-1
         =6-delta
         =8-sqrt(5)>0.                                (6)
```

The last sign is exact, for example from `sqrt(5)<3`. This proves (1).

## Ownership audit

The opening has no hidden duplicated cut and no unspecified tree charge:

| object | owner | effect |
|---|---|---|
| common hub `x` | `H` | retains all seven triangles and `P_0` |
| second cut `y` | `H` | retains `P_0`; opens `P_1` |
| four private vertices of `P_1` | `E` | induce the path `P_1-y` |
| branch rooted at `x`, `y`, `P_0`, or a triangle | `H` | allowed attachment in the common-cut theorem |
| branch rooted at a private vertex of `P_1` | `E` | remains part of one tree |

Therefore `H` and `E` are induced, vertex-disjoint, and exhaustive for every
allowed attachment realization. The strictness in (6) comes from the
common-cut phase inequality; the tree identity (4) is exact.

## Dependency boundary

The sole analytic input is the already proved arbitrary-tree estimate

```text
sigma(common-cut T^k C_q)>k-(sec(pi/q)-1),
q=1 mod 4,
```

applied only at `(k,q)=(7,5)`. Its rooted Schur--Sachs proof is recorded in
`research/common-cut-bouquet-rooted-schur-2026-07-26.md`. No two-pivot phase
comparison, marked-interface margin, rooted hostile-cycle guard, or numerical
spectral experiment is used.
