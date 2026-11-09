# Final order-eight residual: two induced tricyclic territories

## Statement

Let `G` be a finite simple graph obtained as follows.  Start with two
vertex-disjoint copies of `K4`, on

```text
A = {0,3,6,7},        B = {1,2,4,5},
```

replace each of their twelve edges by an arbitrary positive-length path, and
join the two copies by two further arbitrary positive-length paths `P_74` and
`P_65`.  All fourteen replacement paths have pairwise disjoint interiors and
meet only at their prescribed branch endpoints.  At arbitrary branch or
internal subdivision vertices, attach arbitrary finite rooted trees, otherwise
disjoint.

Then

```text
s+(G) >= |V(G)|.
```

No parity hypothesis on any replacement path is needed.

This proposition owns the unique residual orbit after the global post-XII
shared-packet lane.  That orbit has stream index `416536`, residual source
index `416987`, global kernel `6832`, orbit size two, support

```text
03,06,07,12,14,15,24,25,36,37,45,47,56,67,
```

and parity row

```text
(1,1,1,1,1,1,1,1,1,1,1,1,0,1).
```

The proposition is stronger than the finite canonical-plus-coordinate
obligation: it treats every length vector and every parity row at once.

## Imported theorem and spectral inequality

We use two established facts from `all-tricyclic-graphs/paper.tex`.

1. Every finite simple connected graph `H` with
   `|E(H)|=|V(H)|+2` satisfies `s+(H)>=|V(H)|`.
2. Positive square energy is induced-superadditive: for a vertex partition
   `V(G)=U disjoint_union W`,

   ```text
   s+(G) >= s+(G[U]) + s+(G[W]).
   ```

The second fact follows by pinching the adjacency matrix to the two principal
blocks and applying the convex positive-part square functional.  It does not
assume that omitted crossing edges help spectrally.

## Territory partition

Let `C_A` be the subdivision of the six edges

```text
03,06,07,36,37,67,
```

and let `C_B` be the subdivision of

```text
12,14,15,24,25,45.
```

Orient the connector paths from `7` to `4` and from `6` to `5`.  Put all
internal connector vertices on the `A` side:

```text
U_0 = V(C_A)
      union (V(P_74) \ {4,7})
      union (V(P_65) \ {5,6}),
W_0 = V(C_B).
```

Every attached rooted tree follows its root: if its root lies in `U_0`, put all
of its nonroot vertices in `U`; otherwise put them in `W`.  Then
`V(G)=U disjoint_union W`.

Each connector contributes exactly one crossing edge.  If a connector is a
unit path, that edge itself crosses.  Otherwise, only its terminal edge into
`4` or `5` crosses.  No branch vertex or connector interior is duplicated.

## The two induced graphs

The induced graph `G[U]` consists of the `K4` subdivision `C_A`, the two
connector stubs obtained by deleting terminals `4` and `5`, and all rooted
trees assigned to these vertices.  Everything outside `C_A` is a forest whose
components meet `C_A` in exactly one root.  Hence `G[U]` is connected and its
unique positive-rank cyclic block is `C_A`.

Similarly, `G[W]` consists of the `K4` subdivision `C_B` with its assigned
rooted trees, and is connected.

For an exact cyclomatic count, let `L_A` be the number of edges in `C_A`, and
let `t_A` be the number of forest edges inside `U`, including the connector
stubs.  A `K4` subdivision has `L_A-2` vertices, and every forest edge adds one
new vertex.  Therefore

```text
|E(G[U])| = L_A + t_A,
|V(G[U])| = L_A - 2 + t_A,
|E(G[U])| = |V(G[U])| + 2.
```

The same calculation applies to `G[W]`.  The complete connected tricyclic
theorem gives

```text
s+(G[U]) >= |U|,       s+(G[W]) >= |W|.
```

Induced superadditivity now yields

```text
s+(G) >= s+(G[U]) + s+(G[W])
      >= |U| + |W|
       = |V(G)|.
```

This proves the proposition.

## Scope audit

- **All lengths and all parities.** Lengthening a path inside either `K4`
  territory preserves a simple `K4` subdivision.  Lengthening a connector only
  lengthens a rooted forest stub on the `A` side.
- **Arbitrary rooted trees.** Every whole attached tree follows its unique root,
  so it remains a one-root forest attachment in exactly one induced territory.
- **No actual-`K4` margin.** The proof uses the all-length tricyclic theorem
  with nonnegative surplus, not the stronger surplus of an unsubdivided `K4`.
- **No connector debit.** Connector interiors are absorbed into `G[U]`; they
  are not charged as separate tree territories.
- **No edge monotonicity.** The two crossing edges are omitted by a vertex
  partition and handled only through induced superadditivity.
- **No DNN gluing.** The territories are disjoint, so no invalid one-vertex
  Gram sum is invoked.

Thus the unique post-XII complement has a uniform structural owner.  Promoting
the complete rank-seven/order-eight kernel theorem additionally requires the
fail-closed global accounting and dependency verifier; this note alone makes no
claim about kernel orders nine through twelve or all connected heptacyclic
graphs.
