# Tick 36: complete missing-graph cover for the k=4 residual

The previous scout campaigns did not preserve a reproducible parent list.  This
attempt replaces that bookkeeping with a complete hierarchy for the entire
isolated-root `m=9,k=4` normal form; no old solver status is imported.

For each `rho in {0,1,2}`, one of the eleven four-edge T-hole shapes is fixed.
Let `M` be its vertices of hole-degree at least two.  The placement coordinates
partition `M` among `A'`, `B`, and the witness root:

```
alpha=|M intersect A'|, beta=|M intersect B|,
epsilon=|M intersect {w}|.
```

For the dynamically defined common-C-dominator set `K subset B`, the remaining
coordinates are

```
kappa=|K| in {5,6}, eta=e_hole(K), lambda=|K intersect M|.
```

The exact set-intersection range is

```
max(0,beta-(7-kappa)) <= lambda <= min(beta,kappa).
```

The raw Cartesian hierarchy has 2,925 terminal keys.  To test whether a key is
even compatible with its claimed missing-graph shape, color every nonisolated
vertex of a canonical shape by one of four cells

```
{w}, A', B\K, K
```

of capacities `1,7,7-kappa,kappa`.  The hole-isolated vertices fill unused
capacities.  A coloring realizes a key exactly when it has the specified
`alpha,beta,epsilon,lambda` and exactly `eta` shape edges have both endpoints
colored K.

This criterion is exact.  Any graph in a key induces such a coloring.
Conversely, from a coloring add the required hole-isolated vertices to the
unused cells; this constructs the claimed four-edge missing graph on
`{w} union A' union B`.  It asserts only missing-graph compatibility, not a
completion to an oriented counterexample.

Two implementations reproduce the same canonical ledger. The production code
colors support vertices directly. The separately implemented cross-check
chooses support subsets assigned to the root, B, and K; it duplicates the shape
representatives and terminal-key loops and imports no production-cover code. It
also audits each representative against the five shape invariants used by the
CNF emitter. This is an implementation cross-check of the proved coloring
criterion, not an independent derivation of the hierarchy or oracle.

Results:

```
terminal keys       2925
structurally feasible 1140
structurally empty    1785
key stream SHA-256 51700d5bd4f592859442da60b83b9c49a434d9a31b09618bfe61b09326b61195
ledger SHA-256     9e8ebba3b2617beb5ee58c052e4f59a03abbb20a3a09f9d11c4ee6b2019f1cae
```

Reproduce from `experiments/`:

```
python3 m9_k4_cover.py m9-k4-cover.tsv
python3 check_m9_k4_cover.py m9-k4-cover.tsv
python3 test_m9_k4_shapes.py
```

This removes 1,785 impossible terminal cells without SAT and freezes the 1,140
surviving CNF jobs.  It is a cover theorem only for the k=4 missing-graph
coordinate hierarchy, not an elimination of k=4, order 18, or SNC.
