# Cacti with triangles and exactly two pentagons

This directory proves that every finite simple connected cactus whose complete
cyclic blocks are `r >= 1` triangles and exactly two copies of `C5` satisfies

```text
s+(G) > |V(G)|.
```

Shared cut vertices, bridge connectors of arbitrary length and branching, and
arbitrary finite trees attached at arbitrary vertices are allowed.

## Proof map

- Apply a maximum-cardinality triangle packing and fixed-priority Voronoi
  partition to the original graph before making any bridge cut. Each induced
  territory is connected, retains its selected triangle, and has
  triangle-packing number one.
- Treat `0P` territories by the strict packing-one triangular theorem.
- Prove Lemma L in full by tree-message elimination, the grouped normalized
  Sachs expansion, an unrestricted multi-port pentagon matching comparison,
  and signed Coulson integration. It gives
  `sigma(T^a P) > a - (sqrt(5)-2) > 0` whenever the retained triangles have
  packing number one.
- Reduce every `2P` territory using a lexicographically well-founded induction
  on complete cyclic blocks and shared-cut clusters, cutting only actual
  bridges on the minimal cyclic-cluster hull.
- Classify the final packing-one shared-cut cluster into the exact forms
  `H1`--`H7`. The common-cut theorem handles `H1`; the rooted two-pentagon hinge
  handles `H2`, `H5`, and `H6`; physical `1+2` router ownership handles `H3`,
  `H4`, and `H7`.
- Assign every shared cut exactly once. Every cycle fragment, connector
  remnant, bridge-tree branch, and attached tree follows its actual physical
  anchor.

The manuscript states all imported packet dependencies explicitly and includes
the self-contained Sachs proof of Lemma L, the owner clarification for the
Voronoi predecessor argument, the marked-state limitation of `H7`, the scope
boundary, and an AI disclosure.

## Build

From the repository root run:

```bash
bash scripts/build-paper.sh all-rank-triangle-two-pentagon-cacti
```

The generated `paper.pdf` is included in this directory.

## Scope

This is a theorem for the stated cactus block profile. It does not cover three
pentagons, non-cactus block intersections, or merely maximal triangle packings,
and it is not a proof of the universal AKMPZ conjecture for all graphs.
