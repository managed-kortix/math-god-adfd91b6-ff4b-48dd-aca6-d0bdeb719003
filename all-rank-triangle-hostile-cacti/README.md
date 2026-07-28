# Cacti with arbitrarily many triangles and one hostile cycle

This folder proves that every connected cactus whose cyclic blocks are at
least one triangle and one cycle `C_q`, `q=1 mod 4`, `q>=5`, satisfies
`s+(G)>|V(G)|`.  Incidence topology, connector lengths, and attached trees are
arbitrary.

The proof is rank-uniform and uses:

- maximum-packing triangular Voronoi territories;
- a rooted packing-one hostile-cycle Sachs/Coulson inequality;
- induction on the reduced shared-cut cluster tree;
- consecutive-interval destruction of `Q` when it has at least two shared-cut
  interfaces;
- exact final ownership of cuts, connector remnants, and attached trees.

The paper does not claim the two-pentagon family `T^rPP`.
