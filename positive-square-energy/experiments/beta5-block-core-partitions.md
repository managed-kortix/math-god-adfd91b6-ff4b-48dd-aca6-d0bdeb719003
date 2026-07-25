# Beta-five block-cut incidence cores

## Scope and credits

This is a purely combinatorial classification for connected block graphs of
cyclomatic number five. Bridge subdivisions and bridge-only branches are
suppressed. The cyclic blocks are necessarily either

1. one `K4` and two triangles, or
2. five triangles.

The partition search uses only induced-subgraph superadditivity and these
previously proved lower bounds for a connected induced piece `H`:

- a triangular piece with cycle-packing number at most two has
  `s+(H)>m(H)=|H|-1+beta(H)`;
- a piece with `K4` as its only cyclic block has
  `s+(H)>m(H)=|H|+2`;
- a cyclic block graph of rank at most four has `s+(H)>|H|`;
- a tree has `s+(H)=|H|-1`.

Thus the calculation tracks integer credits and a strictness bit. It does not
compute eigenvalues.

## Exact enumeration

For each connected cyclic cluster, form its bipartite incidence tree. Its
block nodes have colors `Q` (`K4`) or `T` (triangle). A cut node has degree at
least two, and a block node has degree at most its order. Two colored trees
are identified by color-preserving isomorphism.

The exhaustive generator in `beta5_block_core_partitions.py` loops over all
possible incident-block subsets for cut nodes, retains exactly the connected
incidence trees satisfying the degree constraints, and deduplicates by exact
NetworkX graph isomorphism. It finds:

- `3` connected cores of type `K4+2K3`;
- `8` connected cores of type `5K3`.

This is complete for the only potentially new case. If the cyclic incidence
forest has at least two clusters, cutting the intervening bridge paths gives
induced pieces whose ranks are positive and at most four; the already proved
rank bounds immediately sum to more than `n`.

In the tables, `(A,B,C)` means that the listed blocks meet in one common cut
vertex. Different parentheses denote different cut vertices. Labels may be
permuted among equal blocks.

## The `K4+2K3` templates

Let `Q` be the `K4`, and let `T1,T2` be the triangles. The three connected
cores are

| template | cut incidences | certificate |
|---|---|---|
| `Q-star` | `(Q,T1,T2)` | delete a private vertex of `Q` |
| `Q-double` | `(Q,T1) (Q,T2)` | delete a private vertex of `Q` |
| `chain` | `(Q,T1) (T1,T2)` | delete a private vertex of `Q` |

In every row `Q` has a private vertex `v`. Put `v` and every suppressed
bridge-only branch hanging from `v` into a tree piece `U`; put all remaining
vertices into `R`. The induced `K4-v` is a triangle. Hence `R` is triangular
of rank three, and its three triangles have packing number at most two in all
three templates. Therefore

`s+(G) >= s+(U)+s+(R) > (|U|-1)+(|R|+2) = n+1`.

This single deletion template certifies all three connected cores. It is also
stable under arbitrary bridge subdivisions and attached trees.

## The five-triangle templates

The exact connected list is:

| id | cut incidences | packing | certificate |
|---:|---|---:|---|
| `F1` | `(T0,T1,T2,T3,T4)` | 1 | whole graph, packing theorem |
| `F2` | `(T0,T1) (T0,T2,T3,T4)` | 2 | whole graph, packing theorem |
| `F3` | `(T0,T1,T2) (T0,T3,T4)` | 2 | whole graph, packing theorem |
| `F4` | `(T0,T1) (T0,T2) (T0,T3,T4)` | 3 | break `T1` |
| `F5` | `(T0,T1) (T0,T2) (T1,T3,T4)` | 2 | whole graph, packing theorem |
| `F6` | `(T0,T1) (T2,T3) (T0,T2,T4)` | 3 | break `T1` |
| `F7` | `(T0,T1) (T0,T2) (T0,T3) (T1,T4)` | 3 | break `T2` |
| `F8` | `(T0,T1) (T0,T2) (T1,T3) (T2,T4)` | 3 | break `T0` (or an end triangle) |

For `F1,F2,F3,F5`, the whole graph has packing at most two, so

`s+(G)>m(G)=n+4`.

For each of `F4,F6,F7,F8`, choose a private vertex `v` in the indicated
triangle. Let `U` contain `v` and all bridge-only branches hanging from it,
and let `R=G-U`. The broken triangle contributes only an edge to `R`; its
other four triangular blocks remain, and direct inspection of the displayed
incidences gives packing number two. Thus `R` is triangular with
`beta(R)=4`, while `U` is a tree. The uniform certificate is

`s+(G) >= s+(U)+s+(R) > (|U|-1)+(|R|+3) = n+2`.

The four packing-three rows are exactly the residual after applying the
packing-at-most-two theorem to the whole core. All four succumb to the same
one-private-vertex induced partition. Consequently there is no unresolved
beta-five incidence core under the stated safe-piece library.

## Machine certificates

Run:

```sh
python positive-square-energy/experiments/beta5_block_core_partitions.py
```

The script realizes each minimal core, evaluates every induced vertex subset
by exact graph predicates, and performs an exhaustive set-partition dynamic
program. Its printed partitions are discovery certificates; the finite
templates above simplify them into branch-stable structural certificates.
For the eleven minimal cores, every optimum found has strict integer credit
greater than the core order. No spectral census or floating-point arithmetic
is used.
