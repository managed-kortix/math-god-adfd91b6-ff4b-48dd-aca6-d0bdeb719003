# R331-K adjacency ownership lemma and source-conditional gate

## Status and exact nonclaim

This note proves the **combinatorial ownership and rank lemma** used by the
adjacency-only `R331-K` gate. It does not prove a new spectral estimate. The
last ledger in this note is conditional on the separately proved, byte-pinned
analytic inputs listed in Section 7. The executable is a fail-closed semantic
replay and finite corroboration; its fixtures are not a finite proof over
unbounded block-cut trees.

No claim is made here about another packet, a subdivided `K4`, a noncycle
rank-one block, a single-block graph, the full rank-seven problem, or
publication status.

## 1. Physical adjacency scope

Let `G` be a finite simple connected graph. Reconstruct its maximal
edge-biconnected blocks from adjacency, retaining every physical bridge as a
one-edge `K2` block. Assume the positive-rank blocks are exactly

- two literal, unsubdivided `K4` blocks `B_0,B_1`; and
- one literal cycle block `Q=C_q`.

Thus their cyclomatic ranks are `3,3,1`, so `beta(G)=7`. The `R331-K`
residual sieve further requires `q` to be odd. Every other block is an actual
`K2`. Arbitrarily long bridge chains, repeated articulation vertices,
arbitrary nesting, arbitrary branching, and arbitrary finite one-root tree
payloads are allowed.

The gate accepts only the two frozensets `(vertices,edges)`. It accepts no
claimed anchor, packet label, block inventory, route, owner, rank, threshold,
charge, or partition. It replays the construction below with **each** of the
two adjacency-derived `K4` blocks as the root.

## 2. The full block-cut tree and the exhaustive mark relations

Build the full block-cut incidence tree `T`. It has one node for every block,
including every `K2`, and one node for every articulation. Root `T` at either
literal `K4`, call it `B`. Call the other literal `K4` block `K`. The two
marked block nodes are now `K,Q`.

Two nodes in a rooted tree have exactly one of three relations:

1. `K,Q` are incomparable;
2. `K` is a strict ancestor of `Q`;
3. `Q` is a strict ancestor of `K`.

This is the complete sibling/nested case split. It is incidence-sensitive. If
`Q` is incident at the upstream articulation of `K`, their block nodes are
siblings, not nested. Genuine nesting requires the route to the lower mark to
leave the upper marked block through another articulation. The same statement
holds with `K,Q` reversed. Inserting any number of `K2` block/cut pairs on a
route cannot introduce a fourth relation.

Let `F` be the ancestor-minimal subset of `{K,Q}`. It is an antichain. It has
two elements in the incomparable case and one element in either nested case.

## 3. Original-vertex boundary ownership

For `X in F`, let `c_X` be its immediate upstream articulation. Remove only
the edges of `X` from the current physical adjacency. Every resulting
component meets `V(X)` in exactly one vertex. To see this, suppose a component
met `X` first at `u` and later at a different vertex `v`. A shortest subpath
between consecutive hits has internal vertices outside `X`; it is an ear
between two vertices of the 2-connected block `X`. Adding an ear to a
2-connected graph preserves 2-connectivity, contradicting the maximality of
`X` as a block.

Write `C_x` for the component meeting `X` at `x`, and define

```text
W_X = union_{x in V(X) minus {c_X}} V(C_x).              (3.1)
```

The set `W_X` is an original-vertex owner, not a supplied edge set. The charged
graph is always the induced graph `G[W_X]`. It contains `X-c_X`, every full
descendant block-cut branch leaving a private vertex of `X`, every connector
remnant on those branches, and every one-root payload on those branches. A
branch incident at `c_X` stays upstream.

Both `K4-c_X` and `C_q-c_X` are connected. Hence `G[W_X]` is nonempty and
connected. Since `F` is an antichain, the sets `W_X` are pairwise disjoint.
Put

```text
C = V(G) minus dot_union_{X in F} W_X.                   (3.2)
```

Pruning the strict descendant branches through the frontier nodes leaves the
root-side subtree of `T`, so `G[C]` is connected and contains `B`. Equations
(3.1)--(3.2) therefore give an induced, connected, pairwise disjoint,
exhaustive original-vertex partition. Each physical articulation belongs to
exactly one part. A nested mark is owned by its first selected ancestor and is
never opened a second time.

## 4. Exact cyclomatic-rank additivity

The needed rank statement does not follow from a fixture bound. It is an exact
block-tree identity.

**Lemma 4.1 (rank additivity over a connected block subtree).** If a connected
graph `H` is the union of edge blocks whose block-cut incidence is a tree, then

```text
beta(H) = sum_D beta(D),                                 (4.1)
```

where the sum is over its edge blocks.

**Proof.** Add the blocks in a leaf order. The first block contributes
`|E(D)|-|V(D)|+1`. Every later block meets the preceding connected union in
exactly one articulation, so it adds `|E(D)|` edges and `|V(D)|-1` vertices.
The change in `|E|-|V|+1` is again
`|E(D)|-|V(D)|+1=beta(D)`. This proves (4.1). In particular every physical
`K2` block contributes zero. `square`

Apply the lemma to `G[W_X]`. Its local edge blocks are exactly

- the block decomposition of `X-c_X`;
- every intact positive marked block strictly below `X`; and
- rank-zero `K2` descendants and rooted-tree blocks.

No other positive block exists in the physical inventory. Therefore

```text
beta(G[W_X])
 = beta(X-c_X)
   + sum_{marked positive D strictly below X} beta(D).    (4.2)
```

Here

```text
beta(K4-c)=1,                 beta(C_q-c)=0.              (4.3)
```

Consequently the complete exact table is

| selected frontier `X` | descendant mark | exact rank of `G[W_X]` |
|---|---|---:|
| `Q` | none | `0` |
| `K` | none | `1` |
| `K` | intact `Q` | `1+1=2` |
| `Q` | intact `K` | `0+3=3` |

Arbitrary bridge descendants do not alter the table because each contributes
rank zero. The executable independently reruns Tarjan on every induced piece,
compares its reconstructed positive edge blocks with the right side of (4.2),
and recomputes `|E|-|V|+1`; it does not trust the table as input.

## 5. Why the anchor has one positive block

Every mark outside `B` is either in `F` or lies below exactly one member of
`F`. Hence all private vertices of every nonanchor positive block lie in one
opened owner. For a selected block `X`, its upstream cut `c_X` stays in `C`,
while every other vertex of `X` lies in `W_X`. Thus edges from `c_X` to
`X-c_X` cross the partition and no edge of `X` remains in `G[C]`. A nested
marked block is intact in its selected ancestor's owner and likewise has no
edge in `G[C]`.

All unmarked blocks are physical `K2` blocks. The root block `B` is untouched
and intact. The retained root-side block subtree therefore has `B` as its
unique positive block; everything else in `G[C]` is bridge-tree material. In
particular, no omitted connector remnant can manufacture an additional cycle.
The executable verifies this conclusion by a fresh Tarjan decomposition of
`G[C]` and requires its positive edge-block set to be exactly `{E(B)}`.

## 6. Source-conditional integer ledger

The exact territory table uses the following receipts:

- `G[C]` has a unique literal `K4` block, so the pinned rooted-`K4` estimate
  gives `sigma(G[C])>2`;
- a leaf `Q` opening is a nonempty tree, so its credit is exactly `-1`;
- a leaf `K` opening leaves a literal triangle with bridge trees, so its credit
  is positive;
- a `K`-above-`Q` owner has connected rank two, so its credit is positive;
- a `Q`-above-`K` owner has connected rank three, so its credit is
  nonnegative.

Only the incomparable case has a tree territory, and it has exactly one. If
`t` is the number of tree territories, then `t` is `0` or `1`. Induced
superadditivity on the partition (3.2) gives the source-conditional bound

```text
sigma(G) > 2-t >= 1 > 0.                                (6.1)
```

The strictness comes only from the rooted-`K4` receipt. This exact R331-K
ledger is stronger than the generic two-demand allowance of two possible tree
debits. Nothing in the finite fixture suite is used to infer (6.1).

## 7. Byte-pinned analytic inputs

On repository snapshot `d4c4b40a4a4fa8151764f84ac742d7ec52d02400`, the gate
authenticates these source bytes before accepting an adjacency:

| use | source | SHA-256 |
|---|---|---|
| generic two-demand owner theorem containing R331-K | `positive-square-energy/heptacyclic-general/two-debit-induced-piece-theorem.md` | `29304b8c920c6efd43d05ce0e8f2c21f44e2656ded0c3ce69ea79b5271454213` |
| exact residual registry (`K4+K4+Q`, `Q` odd) | `positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md` | `f45d60cbeefdf523e5aab053af708a388687f05b64a3d569bd1ddda885396ac2` |
| induced superadditivity; trees; connected rank three | `all-tricyclic-graphs/paper.tex` | `4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02` |
| connected rank two | `all-bicyclic-graphs/paper.tex` | `56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da` |
| rooted literal `K4`; triangular unicycle | `packing-two-square-energy/paper.tex` | `9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791` |

The gate also pins this note as the combinatorial semantics it implements. A
source hash authenticates bytes; it is not evidence beyond the mathematical
claim in those bytes.

## 8. Gate coverage and reproducibility boundary

The companion program is

```text
research/r331-k-adjacency-semantic-verifier.py
```

Its finite suite includes same-cut siblings, separate direct arms, separate
bridge arms, a shared bridge stem, both nesting orders, positive-length nested
connectors, upstream-cut sibling degeneracies, rooted payloads, opaque
relabeling, and connectors longer than the usual recursive DFS limit. It
replays both possible literal-`K4` anchors.

Hostile tests reject wrong inventory, an even residual cycle, subdivisions of
a literal `K4`, cycle chords or edge deletion, cross-block ears, omitted
payload edges, malformed API containers, foreign endpoints, changed source
bytes, changed contract records, missing sources, forged frontiers, forged
owner metadata, and forged ledger values. The verifier contains no Python
`assert`, so optimized execution cannot remove a safety condition.

These checks test the implementation. Sections 2--5 prove the unbounded
combinatorial ownership statement. Section 6 remains conditional exactly on
the byte-pinned analytic inputs in Section 7.
