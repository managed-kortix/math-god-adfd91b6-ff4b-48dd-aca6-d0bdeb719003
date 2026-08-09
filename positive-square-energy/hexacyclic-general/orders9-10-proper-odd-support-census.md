# Orders nine and ten: proper odd-cycle support census

## Exact result

Let `K` be one of the frozen 162 order-nine or 66 order-ten rank-six kernels.
Contract a forest of underlying support pairs, reject loops, merge parallel
images, and retain every uncontracted pair. Suppose the resulting simple graph
`H` is the nonzero graph of the irreducible block of an extremal doubly
nonnegative, non-completely-positive KKT stress. If `H` properly contains a
simple `C5`, `C7`, or `C9`, then `H` is one of the 444 graph6 rows in

```text
positive-square-energy/experiments/rank6_orders9_10_proper_odd_support_census.json
```

The exact distribution is

```text
quotient order:   5   6   7    8    9   10
classes:          0  28  89  146  130   51

contains C5: 406
contains C7: 384
contains C9: 165

admissible extreme ranks   classes
3                           28
3,4                         89
3,4,5                      146
3,4,5,6                    130
3,4,5,6,7                   51
```

Cycle columns overlap. In particular, **every proper support on at most five
vertices is excluded**. More importantly for the existing pure-cycle notes,
neither `K971` nor `K1133` produces a row under the stated filters: their cycle
quotients are terminal. Every listed proper support comes from one of the other
226 high-order kernels.

This is an exact support-side necessary list, not a claim that all 444 graphs
actually carry an extremal DNN ray compatible with the nonlinear path KKT
derivatives. It sharply replaces the unrestricted universe of graphs on at
most ten vertices by a finite, authenticated physical list.

## Why the filters are theorem-valid

### 1. Physical contraction

For a residual KKT stress, a zero off-diagonal derivative pair is contracted
only when its transformed branch vectors agree. Such contracted pairs cannot
contain a cycle unless all signs around it are consistent; forgetting signs
therefore gives a forest as a necessary condition. Every positive derivative
pair remains a support edge. The verifier performs exactly this unsigned
necessary projection: choose any forest among the underlying nonzero kernel
pairs, contract it, reject a resulting retained loop, and merge parallel
images. It does not select only a cycle, unlike the earlier pure `Cq` scripts.

### 2. Irreducible block

The exceptional part lies in a 2-connected block containing the odd cycle.
Other blocks split at cut vertices and belong to separate CP/exceptional
summands in the support decomposition. The census therefore keeps precisely
the biconnected quotient supports. This is the relevant block scope; it does
not assert that an entire mixed stress has biconnected support.

### 3. Extreme-ray dimension obstruction

Let `S=UU^T` have order `n`, rank `r`, and support `H`. Perturbations inside
the minimal PSD face have the form `U X U^T`, with `X` symmetric. Every nonedge
`ij` imposes the homogeneous equation

```text
u_i^T X u_j = 0.
```

If `S` spans an extreme DNN ray, the solution space is one-dimensional.
Consequently

```text
binom(r+1,2) - 1 <= binom(n,2) - |E(H)|.                 (1)
```

A non-CP DNN matrix has rank at least three. The verifier retains `H` only if
some integer `r>=3` satisfies (1), and records every such rank as
`extreme_dnn_rank_candidates`. This immediately proves the order-five
exclusion: a graph properly containing `C5` has at most four nonedges, whereas
rank three needs at least five.

Condition (1) is necessary, not sufficient: the nonedge tensors must have the
required exact rank, the resulting matrix must be entrywise positive on every
edge, and its edge entries must match one common path-derivative KKT system.
Those are the remaining algebraic tests.

## Exact enumeration protocol

For each fixture kernel the verifier checks the rank-six path budget
`sum multiplicities = n+5`, then enumerates all subsets of its underlying
support pairs. A subset survives as a contraction exactly when union-find sees
no cycle. For each quotient it:

1. merges all retained parallel images into one simple support edge;
2. rejects retained loops and non-biconnected graphs;
3. tests directly for simple cycles of lengths five, seven, and nine;
4. requires proper containment by an extra vertex or edge;
5. applies (1) for every possible rank;
6. deduplicates by exact NetworkX isomorphism, using graph6 only as the stored
   transport encoding.

The JSON row gives graph6, order, size, degree sequence, contained odd-cycle
lengths, admissible extreme ranks, and every source `(kernel, order)`. Thus the
artifact is usable as the input ledger for exact PSD-face and KKT elimination,
without reconstructing the contraction search.

## Reproduction

```sh
python3 positive-square-energy/experiments/rank6_orders9_10_proper_odd_support_census.py \
  --verify positive-square-energy/experiments/rank6_orders9_10_proper_odd_support_census.json
python3 -O positive-square-energy/experiments/rank6_orders9_10_proper_odd_support_census.py \
  --verify positive-square-energy/experiments/rank6_orders9_10_proper_odd_support_census.json
```

The verifier pins the kernel fixture SHA-256, derives all rows from scratch,
compares the full JSON payload, and then checks pairwise that no two stored
rows are isomorphic.

The stored schema-v1 JSON SHA-256 is
`fe0078654df18ecf31efa688e021ed8cf9c3ddc455978d302584b9354e31232d`.
The verifier's full-payload comparison, rather than this readable checksum, is
the authoritative audit.

## Theorem boundary

The proved statement is:

> Every biconnected support of an extremal non-CP DNN residual stress obtainable
> by unsigned forest contraction from an order-nine or order-ten frozen rank-six
> kernel, and properly containing `C5`, `C7`, or `C9`, belongs to the displayed
> 444-row ledger; there are no such supports on at most five quotient vertices,
> and none arises from `K971` or `K1133`.

It does **not** prove existence for any row, exclude all 444 rows, classify
mixed CP/non-CP sums, or prove cost-five equality-face exhaustion. The next
exact step is to compute the nonedge-tensor rank locus for each recorded
`(H,r)`, then impose positivity and the physical derivative multiplicities.
